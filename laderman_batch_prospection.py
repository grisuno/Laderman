#!/usr/bin/env python3
"""
Laderman Batch Size Prospection Script
======================================

Este script explora sistemáticamente diferentes batch sizes para encontrar
el óptimo para la cristalización del algoritmo de Laderman (3x3, rank 23).

Fundamento teórico:
- Strassen (2x2, 7 slots, ~21 params): batch_size óptimo [24, 128]
- Laderman (3x3, 23 slots, ~621 params): ~30x más parámetros

Según la teoría del ħ_eff, el batch size óptimo escala con:
  B_opt ∝ √(d) × (1/η) × ħ_eff_min

donde d es la dimensionalidad del espacio de parámetros.

Author: Análisis basado en el framework termodinámico de grisun0
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
import time
import math
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

try:
    from tqdm.auto import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable


# =============================================================================
# CONFIGURACIÓN PARA PROSPECCIÓN
# =============================================================================

@dataclass
class ProspectionConfig:
    """Configuración para la prospección de batch size."""
    
    # Parámetros fijos de Laderman
    matrix_size: int = 3
    target_rank: int = 23
    initial_slots: int = 27
    
    # Parámetros del modelo
    hidden_size: int = 128
    num_hidden_layers: int = 2
    num_attention_heads: int = 4
    intermediate_size: int = 256
    
    # Rango de batch sizes a explorar
    # Basado en teoría: si Strassen [24,128] para 21 params,
    # Laderman con 621 params podría necesitar batch sizes más grandes
    batch_sizes_to_test: Tuple[int, ...] = (16, 24, 32, 48, 64, 96, 128, 192, 256, 384)
    
    # Parámetros de entrenamiento
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    epochs_per_batch_size: int = 500  # Epochs cortos para prospección rápida
    
    # Métricas termodinámicas
    kappa_threshold: float = 10.0  # κ < 10 indica estabilidad
    delta_threshold: float = 0.1   # δ < 0.1 indica discretizabilidad
    lc_threshold: float = 5.0      # LC < 5 indica colapso parcial
    
    # Otros
    seed: int = 42
    device: str = "cpu"
    num_workers: int = 0
    output_dir: str = "./laderman_prospection_results"
    
    def __post_init__(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)


# =============================================================================
# DATASET Y MODELO (Simplificados para prospección)
# =============================================================================

class MatrixMultiplicationDataset(Dataset):
    """Dataset para multiplicación de matrices."""
    
    def __init__(self, matrix_size: int, num_samples: int, seed: int = 42):
        self.matrix_size = matrix_size
        self.num_samples = num_samples
        
        generator = torch.Generator().manual_seed(seed)
        self.matrices_a = torch.randn(num_samples, matrix_size, matrix_size, generator=generator)
        self.matrices_b = torch.randn(num_samples, matrix_size, matrix_size, generator=generator)
        self.matrices_c = torch.bmm(self.matrices_a, self.matrices_b)
        
        self.inputs_a = self.matrices_a.view(num_samples, -1)
        self.inputs_b = self.matrices_b.view(num_samples, -1)
        self.targets = self.matrices_c.view(num_samples, -1)
    
    def __len__(self) -> int:
        return self.num_samples
    
    def __getitem__(self, idx: int):
        return self.inputs_a[idx], self.inputs_b[idx], self.targets[idx]


class BilinearModel(nn.Module):
    """Modelo bilineal simplificado para prospección rápida."""
    
    def __init__(self, matrix_size: int, initial_slots: int):
        super().__init__()
        n2 = matrix_size * matrix_size
        
        # Solo los tensores bilineales U, V, W
        self.U = nn.Parameter(torch.randn(initial_slots, n2) * 0.02)
        self.V = nn.Parameter(torch.randn(initial_slots, n2) * 0.02)
        self.W = nn.Parameter(torch.randn(n2, initial_slots) * 0.02)
    
    def forward(self, input_a, input_b):
        # C = W @ ((U @ a) * (V @ b))
        m = (input_a @ self.U.t()) * (input_b @ self.V.t())
        return m @ self.W.t()
    
    def compute_discretization_margin(self):
        all_params = torch.cat([self.U.view(-1), self.V.view(-1), self.W.view(-1)])
        theta_rounded = torch.round(all_params).clamp(-1, 1)
        return torch.norm(all_params - theta_rounded, p=float('inf')).item()


# =============================================================================
# COMPUTADORES DE MÉTRICAS TERMODINÁMICAS
# =============================================================================

def compute_kappa(model, batch, num_samples=10):
    """Computa κ (número de condición de la covarianza de gradientes)."""
    input_a, input_b, target = batch
    gradients = []
    
    max_samples = min(num_samples, input_a.size(0))
    
    for i in range(max_samples):
        model.zero_grad()
        output = model(input_a[i:i+1], input_b[i:i+1])
        loss = F.mse_loss(output, target[i:i+1])
        loss.backward()
        
        grad_list = []
        for name, param in model.named_parameters():
            if param.grad is not None:
                grad_list.append(param.grad.view(-1))
        
        if grad_list:
            gradients.append(torch.cat(grad_list))
    
    if len(gradients) < 2:
        return float('inf')
    
    try:
        grad_matrix = torch.stack(gradients)
        grad_mean = grad_matrix.mean(dim=0, keepdim=True)
        grad_centered = grad_matrix - grad_mean
        
        u, s, v = torch.svd(grad_centered)
        s_nonzero = s[s > 1e-6]
        
        if len(s_nonzero) == 0:
            return float('inf')
        return (s_nonzero.max() / s_nonzero.min()).item()
    except:
        return float('inf')


def compute_local_complexity(model):
    """Computa la complejidad local (rango efectivo de U)."""
    with torch.no_grad():
        u = model.U.detach()
        try:
            u_s = torch.linalg.svdvals(u)
            threshold = 0.01 * u_s.max()
            return (u_s > threshold).sum().item()
        except:
            return float(u.size(0))


def compute_effective_temperature(model, batch, num_samples=10):
    """Computa la temperatura efectiva T_eff."""
    input_a, input_b, target = batch
    grad_norms = []
    
    max_samples = min(num_samples, input_a.size(0))
    
    for i in range(max_samples):
        model.zero_grad()
        output = model(input_a[i:i+1], input_b[i:i+1])
        loss = F.mse_loss(output, target[i:i+1])
        loss.backward()
        
        grad_norm = 0.0
        for param in model.parameters():
            if param.grad is not None:
                grad_norm += param.grad.norm(2).item() ** 2
        grad_norms.append(grad_norm ** 0.5)
    
    if len(grad_norms) == 0:
        return 1.0
    
    grad_norms = torch.tensor(grad_norms)
    return grad_norms.var().item()


def compute_entropy(model, batch, num_samples=10):
    """Computa la entropía h_bar de los gradientes."""
    input_a, input_b, target = batch
    grad_norms = []
    
    max_samples = min(num_samples, input_a.size(0))
    
    for i in range(max_samples):
        model.zero_grad()
        output = model(input_a[i:i+1], input_b[i:i+1])
        loss = F.mse_loss(output, target[i:i+1])
        loss.backward()
        
        grad_norm = 0.0
        for param in model.parameters():
            if param.grad is not None:
                grad_norm += param.grad.norm(2).item() ** 2
        grad_norms.append(grad_norm ** 0.5)
    
    if len(grad_norms) < 2:
        return 0.0
    
    grad_norms = torch.tensor(grad_norms)
    
    # Entropía del histograma de gradientes
    hist = torch.histc(grad_norms, bins=min(20, len(grad_norms)))
    hist = hist / hist.sum()
    return -(hist * torch.log(hist + 1e-10)).sum().item()


# =============================================================================
# FUNCIÓN DE ENTRENAMIENTO PARA PROSPECCIÓN
# =============================================================================

def train_prospection_run(config: ProspectionConfig, batch_size: int) -> Dict:
    """
    Ejecuta un entrenamiento corto con un batch size específico
    y devuelve las métricas termodinámicas.
    """
    print(f"\n{'='*60}")
    print(f"PROSPECTING BATCH SIZE: {batch_size}")
    print(f"{'='*60}")
    
    # Set seed
    torch.manual_seed(config.seed + batch_size)  # Diferente seed por batch size
    np.random.seed(config.seed + batch_size)
    
    # Crear datasets
    train_dataset = MatrixMultiplicationDataset(
        matrix_size=config.matrix_size,
        num_samples=5000,
        seed=config.seed
    )
    test_dataset = MatrixMultiplicationDataset(
        matrix_size=config.matrix_size,
        num_samples=1000,
        seed=config.seed + 1000
    )
    
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True,
        num_workers=config.num_workers
    )
    test_loader = DataLoader(
        test_dataset, batch_size=batch_size, shuffle=False,
        num_workers=config.num_workers
    )
    
    # Crear modelo
    model = BilinearModel(config.matrix_size, config.initial_slots)
    
    # Optimizer
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay
    )
    
    # Métricas a registrar
    metrics_history = {
        'train_loss': [],
        'test_loss': [],
        'test_accuracy': [],
        'kappa': [],
        'delta': [],
        'local_complexity': [],
        'T_eff': [],
        'entropy': []
    }
    
    # Obtener un batch de test para métricas
    test_batch = next(iter(test_loader))
    
    # Entrenar
    for epoch in tqdm(range(config.epochs_per_batch_size), desc=f"BS={batch_size}"):
        # Training
        model.train()
        total_loss = 0.0
        total_samples = 0
        
        for input_a, input_b, target in train_loader:
            optimizer.zero_grad()
            output = model(input_a, input_b)
            loss = F.mse_loss(output, target)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item() * input_a.size(0)
            total_samples += input_a.size(0)
        
        train_loss = total_loss / total_samples
        
        # Evaluation
        model.eval()
        total_test_loss = 0.0
        total_test_samples = 0
        correct = 0
        
        with torch.no_grad():
            for input_a, input_b, target in test_loader:
                output = model(input_a, input_b)
                loss = F.mse_loss(output, target)
                
                total_test_loss += loss.item() * input_a.size(0)
                total_test_samples += input_a.size(0)
                
                # Accuracy: predicción correcta si error < 0.01
                pred_correct = torch.all(torch.abs(output - target) < 0.01, dim=1)
                correct += pred_correct.sum().item()
        
        test_loss = total_test_loss / total_test_samples
        test_accuracy = correct / total_test_samples
        
        # Métricas termodinámicas (cada 50 epochs para ahorrar tiempo)
        if epoch % 50 == 0 or epoch == config.epochs_per_batch_size - 1:
            kappa = compute_kappa(model, test_batch)
            delta = model.compute_discretization_margin()
            lc = compute_local_complexity(model)
            T_eff = compute_effective_temperature(model, test_batch)
            entropy = compute_entropy(model, test_batch)
        else:
            kappa = metrics_history['kappa'][-1] if metrics_history['kappa'] else float('inf')
            delta = metrics_history['delta'][-1] if metrics_history['delta'] else 0.5
            lc = metrics_history['local_complexity'][-1] if metrics_history['local_complexity'] else 27.0
            T_eff = metrics_history['T_eff'][-1] if metrics_history['T_eff'] else 1.0
            entropy = metrics_history['entropy'][-1] if metrics_history['entropy'] else 0.0
        
        # Guardar métricas
        metrics_history['train_loss'].append(train_loss)
        metrics_history['test_loss'].append(test_loss)
        metrics_history['test_accuracy'].append(test_accuracy)
        metrics_history['kappa'].append(kappa)
        metrics_history['delta'].append(delta)
        metrics_history['local_complexity'].append(lc)
        metrics_history['T_eff'].append(T_eff)
        metrics_history['entropy'].append(entropy)
    
    # Resumen final
    final_metrics = {
        'batch_size': batch_size,
        'final_train_loss': metrics_history['train_loss'][-1],
        'final_test_loss': metrics_history['test_loss'][-1],
        'final_test_accuracy': metrics_history['test_accuracy'][-1],
        'final_kappa': metrics_history['kappa'][-1],
        'final_delta': metrics_history['delta'][-1],
        'final_local_complexity': metrics_history['local_complexity'][-1],
        'final_T_eff': metrics_history['T_eff'][-1],
        'final_entropy': metrics_history['entropy'][-1],
        'min_delta': min(metrics_history['delta']),
        'min_kappa': min([k for k in metrics_history['kappa'] if k != float('inf')] or [float('inf')]),
        'max_test_accuracy': max(metrics_history['test_accuracy']),
        'kappa_stable_epochs': sum(1 for k in metrics_history['kappa'] if k < config.kappa_threshold),
        'delta_low_epochs': sum(1 for d in metrics_history['delta'] if d < config.delta_threshold),
        'history': metrics_history
    }
    
    # Imprimir resumen
    print(f"\n  Final Test Accuracy: {final_metrics['final_test_accuracy']:.4f}")
    print(f"  Final κ: {final_metrics['final_kappa']:.4f}")
    print(f"  Final δ: {final_metrics['final_delta']:.4f}")
    print(f"  Final LC: {final_metrics['final_local_complexity']:.1f}")
    print(f"  Final T_eff: {final_metrics['final_T_eff']:.2e}")
    print(f"  Min δ achieved: {final_metrics['min_delta']:.4f}")
    print(f"  Epochs with κ < {config.kappa_threshold}: {final_metrics['kappa_stable_epochs']}")
    print(f"  Epochs with δ < {config.delta_threshold}: {final_metrics['delta_low_epochs']}")
    
    return final_metrics


# =============================================================================
# ANÁLISIS Y RECOMENDACIÓN
# =============================================================================

def analyze_results(results: List[Dict], config: ProspectionConfig) -> Dict:
    """
    Analiza los resultados de la prospección y recomienda el batch size óptimo.
    """
    print(f"\n{'='*80}")
    print("ANÁLISIS DE RESULTADOS")
    print(f"{'='*80}")
    
    # Crear tabla de resultados
    print("\n" + "-"*80)
    print(f"{'Batch Size':^12} | {'Test Acc':^10} | {'κ':^10} | {'δ':^10} | {'LC':^8} | {'T_eff':^12} | {'Score':^8}")
    print("-"*80)
    
    scores = {}
    
    for r in results:
        # Calcular un score compuesto
        # Queremos: alta accuracy, bajo κ, bajo δ, bajo LC, T_eff moderado
        
        acc_score = r['max_test_accuracy'] * 100
        
        # κ score: 100 si κ=1, 0 si κ>100 o inf
        kappa = r['final_kappa']
        if kappa == float('inf') or kappa > 100:
            kappa_score = 0
        else:
            kappa_score = max(0, 100 - kappa)
        
        # δ score: 100 si δ=0, 0 si δ>0.5
        delta = r['final_delta']
        delta_score = max(0, 100 * (1 - delta / 0.5))
        
        # LC score: premiamos LC bajo
        lc = r['final_local_complexity']
        lc_score = max(0, 100 * (1 - lc / 27))
        
        # T_eff score: queremos temperatura moderada
        T_eff = r['final_T_eff']
        if T_eff < 1e-6:
            T_eff_score = 50  # Frío pero puede estar atascado
        elif T_eff > 0.1:
            T_eff_score = 30  # Muy caliente
        else:
            T_eff_score = 100  # Temperatura óptima
        
        # Score compuesto (pesos ajustables)
        composite_score = (
            acc_score * 0.25 +
            kappa_score * 0.25 +
            delta_score * 0.25 +
            lc_score * 0.15 +
            T_eff_score * 0.10
        )
        
        scores[r['batch_size']] = composite_score
        
        print(f"{r['batch_size']:^12} | {r['final_test_accuracy']:^10.4f} | "
              f"{r['final_kappa']:^10.4f} | {r['final_delta']:^10.4f} | "
              f"{r['final_local_complexity']:^8.1f} | {r['final_T_eff']:^12.2e} | "
              f"{composite_score:^8.1f}")
    
    print("-"*80)
    
    # Encontrar el mejor batch size
    best_batch_size = max(scores, key=scores.get)
    
    # Análisis de rangos
    print(f"\n{'='*80}")
    print("ANÁLISIS TERMODINÁMICO")
    print(f"{'='*80}")
    
    # Agrupar por rangos
    ranges = {
        'small': [r for r in results if r['batch_size'] <= 32],
        'medium': [r for r in results if 48 <= r['batch_size'] <= 128],
        'large': [r for r in results if r['batch_size'] >= 192]
    }
    
    for range_name, range_results in ranges.items():
        if not range_results:
            continue
        
        avg_acc = np.mean([r['final_test_accuracy'] for r in range_results])
        avg_kappa = np.mean([r['final_kappa'] for r in range_results if r['final_kappa'] != float('inf')])
        avg_delta = np.mean([r['final_delta'] for r in range_results])
        avg_T_eff = np.mean([r['final_T_eff'] for r in range_results])
        
        print(f"\nRango {range_name.upper()} (BS {[r['batch_size'] for r in range_results]}):")
        print(f"  Accuracy promedio: {avg_acc:.4f}")
        print(f"  κ promedio: {avg_kappa:.4f}")
        print(f"  δ promedio: {avg_delta:.4f}")
        print(f"  T_eff promedio: {avg_T_eff:.2e}")
    
    # Recomendación
    print(f"\n{'='*80}")
    print("RECOMENDACIÓN")
    print(f"{'='*80}")
    print(f"\n🏆 BATCH SIZE ÓPTIMO RECOMENDADO: {best_batch_size}")
    print(f"   Score compuesto: {scores[best_batch_size]:.1f}")
    
    # Explicación teórica
    print(f"\n📊 JUSTIFICACIÓN TEÓRICA:")
    print(f"   - Laderman tiene ~621 parámetros bilineales vs ~21 de Strassen")
    print(f"   - El batch size óptimo escala con √(dimensión del espacio de parámetros)")
    print(f"   - Para Strassen: B* ∈ [24, 128]")
    print(f"   - Para Laderman: B* estimado por prospección = {best_batch_size}")
    
    # Verificar si el óptimo está en el borde del rango probado
    all_bs = [r['batch_size'] for r in results]
    if best_batch_size == min(all_bs):
        print(f"\n⚠️  ADVERTENCIA: El mejor BS está en el límite inferior del rango.")
        print(f"   Considere probar batch sizes más pequeños: {max(8, min(all_bs)//2)} - {min(all_bs)}")
    elif best_batch_size == max(all_bs):
        print(f"\n⚠️  ADVERTENCIA: El mejor BS está en el límite superior del rango.")
        print(f"   Considere probar batch sizes más grandes: {max(all_bs)} - {max(all_bs)*2}")
    
    return {
        'best_batch_size': best_batch_size,
        'scores': scores,
        'all_results': results
    }


# =============================================================================
# MAIN
# =============================================================================

def run_prospection(config: Optional[ProspectionConfig] = None):
    """Ejecuta la prospección completa de batch size."""
    
    if config is None:
        config = ProspectionConfig()
    
    print("\n" + "="*80)
    print("LADERMAN BATCH SIZE PROSPECTION")
    print("="*80)
    print(f"\nMatrix size: {config.matrix_size}x{config.matrix_size}")
    print(f"Target rank: {config.target_rank}")
    print(f"Initial slots: {config.initial_slots}")
    print(f"Batch sizes to test: {config.batch_sizes_to_test}")
    print(f"Epochs per batch size: {config.epochs_per_batch_size}")
    print(f"Output directory: {config.output_dir}")
    
    # Ejecutar prospección
    results = []
    
    for batch_size in config.batch_sizes_to_test:
        result = train_prospection_run(config, batch_size)
        results.append(result)
    
    # Analizar resultados
    analysis = analyze_results(results, config)
    
    # Guardar resultados
    output_file = Path(config.output_dir) / "prospection_results.json"
    
    # Convertir a formato serializable
    serializable_results = []
    for r in results:
        sr = {k: v for k, v in r.items() if k != 'history'}
        sr['history'] = {
            k: [float(x) if isinstance(x, (int, float)) else x for x in v]
            for k, v in r['history'].items()
        }
        serializable_results.append(sr)
    
    with open(output_file, 'w') as f:
        json.dump({
            'config': asdict(config),
            'results': serializable_results,
            'analysis': {
                'best_batch_size': analysis['best_batch_size'],
                'scores': {str(k): v for k, v in analysis['scores'].items()}
            }
        }, f, indent=2)
    
    print(f"\n✅ Resultados guardados en: {output_file}")
    
    return analysis


if __name__ == "__main__":
    # Configuración personalizada
    config = ProspectionConfig(
        batch_sizes_to_test=(16, 24, 32, 48, 64, 96, 128, 192, 256, 384),
        epochs_per_batch_size=500
    )
    
    analysis = run_prospection(config)
    
    print(f"\n{'='*80}")
    print("PRÓXIMOS PASOS RECOMENDADOS")
    print(f"{'='*80}")
    print(f"""
1. Ejecutar entrenamiento completo con batch_size = {analysis['best_batch_size']}
2. Monitorear métricas termodinámicas:
   - κ debe acercarse a 1 para cristalización
   - δ debe disminuir hacia 0
   - LC debe colapsar hacia 23 (target rank)
3. Ajustar weight_decay si δ no disminuye
4. Considerar learning rate scheduling si el entrenamiento es inestable
""")
