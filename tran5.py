#!/usr/bin/env python3
"""
Leibler Transformer with Thermodynamic Grokking
Implementación completa con fixes para estabilizar el grokking
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm
import argparse
from datetime import datetime


@dataclass
class LeidermanConfig:
    """Configuration for Leibler-Leiderman architecture"""
    # Model architecture
    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 256
    dropout: float = 0.1
    
    # Vocabulary and sequence
    vocab_size: int = 27
    max_seq_len: int = 5
    
    # Thermodynamic parameters
    T_min: float = 0.01
    T_max: float = 2.0
    cooling_rate: float = 0.001
    phase_transition_threshold: float = 0.1
    
    # Training — dentro de la ventana de cristalización del paper
    batch_size: int = 64
    learning_rate: float = 1e-3
    weight_decay_initial: float = 1e-2
    weight_decay_crystal: float = 1e-4
    weight_decay_min: float = 1e-5
    max_epochs: int = 25000
    warmup_epochs: int = 100
    grokking_epochs: int = 3000
    
    # Grokking detection
    grokking_threshold: float = 0.95
    phase_window: int = 10
    
    # Pruning and discretization
    pruning_threshold: float = 0.1
    discretization_tolerance: float = 0.1
    
    # Phase-dependent annealing schedule
    annealing_gas_wd: float = 1e-2
    annealing_liquid_wd: float = 1e-3
    annealing_glass_wd: float = 1e-4
    annealing_crystal_wd: float = 1e-5
    
    # Gradient covariance sampling
    kappa_n_batches: int = 8
    
    # Phase boundaries (from paper measurements)
    kappa_crystal_threshold: float = 2.0
    delta_crystal_threshold: float = 0.1
    t_eff_crystal_ceiling: float = 1e-8

class LeiblerAttention(nn.Module):
    """
    Thermodynamic attention mechanism implementing Leibler's cerebral principles
    """
    
    def __init__(self, config: LeidermanConfig):
        super().__init__()
        self.config = config
        self.d_model = config.d_model
        self.n_heads = config.n_heads
        self.d_head = config.d_model // config.n_heads
        
        # Learnable temperature parameter
        self.temperature = nn.Parameter(torch.ones(1) * config.T_max)
        
        # Projection matrices (slots)
        self.q_proj = nn.Linear(config.d_model, config.d_model)
        self.k_proj = nn.Linear(config.d_model, config.d_model)
        self.v_proj = nn.Linear(config.d_model, config.d_model)
        self.o_proj = nn.Linear(config.d_model, config.d_model)
        
        # Thermodynamic state variables
        self.entropy = 0.0
        self.heat_capacity = 0.0
        self.T_eff = config.T_max
        self.scores = None
        
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass with thermodynamic attention
        
        Args:
            x: Input tensor [batch, seq_len, d_model]
            mask: Optional attention mask
            
        Returns:
            Output tensor [batch, seq_len, d_model]
        """
        batch_size, seq_len, _ = x.shape
        
        # Project to Q, K, V
        Q = self.q_proj(x).view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        K = self.k_proj(x).view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        V = self.v_proj(x).view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        
        # Compute attention scores
        scores = torch.matmul(Q, K.transpose(-2, -1)) / np.sqrt(self.d_head)
        
        # Store for thermodynamic analysis
        self.scores = scores.detach()
        
        # Apply mask if provided
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Thermodynamic attention weights
        attn_weights = F.softmax(scores / self.temperature, dim=-1)
        
        # Apply attention
        attn_output = torch.matmul(attn_weights, V)
        
        # Reshape and project
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        output = self.o_proj(attn_output)
        
        # Update thermodynamic state
        self._update_thermodynamic_state()
        
        return output
    
    def _update_thermodynamic_state(self):
        """Update thermodynamic state variables with stable computation"""
        with torch.no_grad():
            # Entropy from attention distribution
            attn_dist = F.softmax(self.scores / self.temperature, dim=-1)
            entropy = -torch.sum(attn_dist * torch.log(attn_dist + 1e-10), dim=-1)
            self.entropy = entropy.mean().item()
            
            # Heat capacity from variance of energy
            energies = -torch.log(attn_dist + 1e-10)
            energy_mean = energies.mean()
            energy_var = ((energies - energy_mean) ** 2).mean()
            self.heat_capacity = (energy_var / (self.temperature ** 2 + 1e-10)).item()
            
            # Effective temperature: usar directamente temperature cuando está estable
            # y solo calcular T_eff cuando hay gradiente significativo
            if hasattr(self, 'temperature_grad'):
                grad_magnitude = torch.abs(self.temperature_grad).mean().item()
                if grad_magnitude > 1e-6:
                    energy_fluctuation = torch.sqrt(energy_var + 1e-10)
                    self.T_eff = (energy_fluctuation / (1.0 + entropy.mean())).item()
                else:
                    self.T_eff = self.temperature.item()
            else:
                self.T_eff = self.temperature.item()


class LeiblerTransformerLayer(nn.Module):
    """
    Transformer layer with Leibler attention and thermodynamic principles
    """
    
    def __init__(self, config: LeidermanConfig):
        super().__init__()
        self.config = config
        
        # Attention mechanism
        self.attention = LeiblerAttention(config)
        
        # Feed-forward network
        self.ff = nn.Sequential(
            nn.Linear(config.d_model, config.d_ff),
            nn.GELU(),
            nn.Dropout(config.dropout),
            nn.Linear(config.d_ff, config.d_model),
            nn.Dropout(config.dropout)
        )
        
        # Layer normalization
        self.norm1 = nn.LayerNorm(config.d_model)
        self.norm2 = nn.LayerNorm(config.d_model)
        
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """Forward pass with residual connections"""
        # Attention with residual
        attn_out = self.attention(self.norm1(x), mask)
        x = x + attn_out
        
        # Feed-forward with residual
        ff_out = self.ff(self.norm2(x))
        x = x + ff_out
        
        return x


class LeiblerTransformer(nn.Module):
    """
    Complete Leibler Transformer implementing thermodynamic grokking
    """
    
    def __init__(self, config: LeidermanConfig):
        super().__init__()
        self.config = config
        
        # Token embedding
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        
        # Positional encoding
        self.pos_encoding = nn.Parameter(
            torch.randn(1, config.max_seq_len, config.d_model) * 0.02
        )
        
        # Transformer layers
        self.layers = nn.ModuleList([
            LeiblerTransformerLayer(config) for _ in range(config.n_layers)
        ])
        
        # Output projection
        self.output_norm = nn.LayerNorm(config.d_model)
        self.output_proj = nn.Linear(config.d_model, config.vocab_size)
        
        # Initialize weights
        self._init_weights()
        
    def _init_weights(self):
        """Initialize weights with small values for stability"""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, std=0.02)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, std=0.02)
    
    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            x: Input token indices [batch, seq_len]
            mask: Optional attention mask
            
        Returns:
            Logits [batch, seq_len, vocab_size]
        """
        # Embed tokens and add positional encoding
        x = self.token_embedding(x) + self.pos_encoding[:, :x.size(1), :]
        
        # Apply transformer layers
        for layer in self.layers:
            x = layer(x, mask)
        
        # Project to vocabulary
        x = self.output_norm(x)
        logits = self.output_proj(x)
        
        return logits
    
    def get_thermodynamic_state(self) -> Dict[str, float]:
        """Extract current thermodynamic state from all layers"""
        state = {
            'entropy': 0.0,
            'heat_capacity': 0.0,
            'T_eff': 0.0,
            'temperature': 0.0
        }
        
        n_layers = len(self.layers)
        for layer in self.layers:
            attn = layer.attention
            state['entropy'] += attn.entropy
            state['heat_capacity'] += attn.heat_capacity
            state['T_eff'] += attn.T_eff
            state['temperature'] += attn.temperature.item()
        
        # Average over layers
        for key in state:
            state[key] /= n_layers
            
        return state


class AdaptiveTemperatureScheduler:
    """
    Adaptive temperature scheduler implementing thermodynamic cooling
    """
    
    def __init__(self, model: LeiblerTransformer, config: LeidermanConfig):
        self.model = model
        self.config = config
        self.step_count = 0
        
        # Temperature state
        self.current_temperature = config.T_max
        self.base_temperature = config.T_max
        
        # Phase tracking
        self.phase_transitions = []
        self.accuracy_history = []
        self.phase_stability_counter = 0
        self.phase_window = config.phase_window
        
    def step(self, metrics: Dict[str, float]):
        """Update temperature based on training metrics with enhanced stability"""
        epoch = metrics.get('epoch', 0)
        test_acc = metrics.get('test_acc', 0.0)
        
        # Store accuracy history
        self.accuracy_history.append(test_acc)
        if len(self.accuracy_history) > self.phase_window:
            self.accuracy_history.pop(0)
        
        # Detect phase transition
        if len(self.accuracy_history) >= 2:
            acc_change = self.accuracy_history[-1] - self.accuracy_history[-2]
            if abs(acc_change) > self.config.phase_transition_threshold:
                self.phase_transitions.append(epoch)
                self.phase_stability_counter = 0
            else:
                self.phase_stability_counter += 1
        
        # Phase-specific temperature adjustments
        current_phase = metrics.get('phase', 'unknown')
        
        if current_phase == 'glass':
            # En fase glass, mantener temperatura BAJA y estable
            target_temp = self.config.T_min
            self.base_temperature = self.base_temperature * 0.95 + target_temp * 0.05
            
        elif current_phase == 'warm_glass':
            # En warm_glass, temperatura moderada pero NO oscilar
            if self.phase_stability_counter < 5:
                # Recién entrando a warm_glass, mantener temperatura
                target_temp = self.base_temperature
            else:
                # Estable en warm_glass, enfriar MUY gradualmente
                target_temp = max(
                    self.config.T_min,
                    self.base_temperature * (1.0 - self.config.cooling_rate * 0.1)
                )
            self.base_temperature = target_temp
            
        elif test_acc > 0.9:
            # Si accuracy es alta, MANTENER temperatura baja
            target_temp = self.config.T_min * 1.5
            self.base_temperature = min(self.base_temperature, target_temp)
            
        else:
            # Fase de exploración normal
            progress = min(epoch / self.config.grokking_epochs, 1.0)
            
            # Cooling schedule más suave
            if epoch < self.config.warmup_epochs:
                # Warmup muy gradual
                warmup_progress = epoch / self.config.warmup_epochs
                target_temp = (
                    self.config.T_max * (1.0 - warmup_progress * 0.3) +
                    self.config.T_min * warmup_progress * 0.3
                )
            else:
                # Enfriamiento exponencial MUY suave después de warmup
                cool_epochs = epoch - self.config.warmup_epochs
                decay_factor = np.exp(-self.config.cooling_rate * cool_epochs / 1000.0)
                target_temp = (
                    self.config.T_min +
                    (self.config.T_max - self.config.T_min) * decay_factor
                )
            
            # Transición suave hacia target
            self.base_temperature = (
                self.base_temperature * 0.9 + target_temp * 0.1
            )
        
        # Adaptive modulation basado en estabilidad de fase
        if self.phase_stability_counter > 10:
            # Fase estable: reducir modulación
            modulation = 1.0 - 0.1 * min(self.phase_stability_counter / 50.0, 1.0)
        else:
            # Fase inestable: mantener exploración mínima
            modulation = 1.0
        
        self.current_temperature = max(
            self.config.T_min,
            min(self.config.T_max, self.base_temperature * modulation)
        )
        
        self.step_count += 1
        
        # Update model temperatures
        self._update_model_temperatures()
    
    def _update_model_temperatures(self):
        """Apply current temperature to all attention layers"""
        for layer in self.model.layers:
            layer.attention.temperature.data.fill_(self.current_temperature)


class ThermodynamicTracker:
    """
    Track thermodynamic properties and phase transitions during training
    """
    
    def __init__(self, config: LeidermanConfig):
        self.config = config
        
        # Metrics history
        self.history = {
            'train_loss': [],
            'test_loss': [],
            'test_acc': [],
            'entropy': [],
            'heat_capacity': [],
            'T_eff': [],
            'temperature': [],
            'phase': [],
            'kappa': [],
            'delta': []
        }
        
        # Phase detection
        self.current_phase = 'unknown'
        self.phase_history = []
        
        # Grokking detection
        self.grokking_detected = False
        self.grokking_epoch = None
        self.grokking_candidate_epochs = 0
        self.prev_test_acc = 0.0
        
    def update(self, metrics: Dict[str, float]):
        """Update tracker with new metrics"""
        # Store metrics
        for key, value in metrics.items():
            if key in self.history:
                self.history[key].append(value)
        
        # Detect phase
        self._detect_phase(metrics)
        
        # Detect grokking with stability requirement
        self._detect_grokking(metrics)
        
        # Actualizar accuracy previa AL FINAL
        self.prev_test_acc = metrics['test_acc']
    
    def _detect_phase(self, metrics: Dict[str, float]):
            """
            Detect current thermodynamic phase based on paper-defined order parameters.
            
            Phase classification from paper measurements:
            - crystal: κ < κ_threshold AND δ < δ_threshold AND T_eff < T_eff_ceiling
            - glass: κ < κ_threshold AND δ > δ_threshold (cold glass, ordered but not discrete)
            - liquid: moderate κ, decreasing δ (structure forming)
            - gas: high κ, high δ (disordered, high entropy)
            """
            kappa = metrics.get('kappa', 999999.0)
            delta = metrics.get('delta', 0.5)
            T_eff = metrics.get('T_eff', 1.0)
            test_acc = metrics.get('test_acc', 0.0)
            
            if (kappa < self.config.kappa_crystal_threshold and 
                delta < self.config.delta_crystal_threshold and 
                T_eff < self.config.t_eff_crystal_ceiling and
                test_acc > self.config.grokking_threshold):
                phase = 'crystal'
            elif (delta < 0.3 and test_acc > 0.8):
                phase = 'glass'
            elif (delta < 0.45 and test_acc > 0.5):
                phase = 'liquid'
            else:
                phase = 'gas'
            
            if phase != self.current_phase:
                print(f"*** PHASE TRANSITION at epoch {metrics.get('epoch', 0)}: {self.current_phase} -> {phase} ***")
                self.current_phase = phase
                self.phase_history.append((metrics.get('epoch', 0), phase))
            
            metrics['phase'] = phase
            
    def _detect_grokking(self, metrics: Dict[str, float]):
        """Detect grokking transitions with stability requirement"""
        test_acc = metrics['test_acc']
        train_loss = metrics['train_loss']
        
        # Grokking requirements
        high_test_acc = test_acc > self.config.grokking_threshold
        low_train_loss = train_loss < 1e-3
        
        # Verificar estabilidad: necesitamos MÚLTIPLES epochs consecutivos
        if high_test_acc and low_train_loss:
            self.grokking_candidate_epochs += 1
        else:
            self.grokking_candidate_epochs = 0
        
        # Solo declarar grokking después de estabilidad sostenida
        stability_required = 3
        
        if self.grokking_candidate_epochs >= stability_required and not self.grokking_detected:
            self.grokking_detected = True
            self.grokking_epoch = metrics['epoch'] - stability_required + 1
            
            # Log grokking con información de estabilidad
            print("\n" + "="*80)
            print(f"*** STABLE GROKKING DETECTED at epoch {self.grokking_epoch} ***")
            print(f"Test accuracy jumped from {self.prev_test_acc:.4f} to {test_acc:.4f}")
            print(f"Stability confirmed over {stability_required} epochs")
            print("="*80 + "\n")
            
            # Save checkpoint
            checkpoint_path = f"grokking_epoch{self.grokking_epoch}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pt"
            torch.save({
                'epoch': self.grokking_epoch,
                'model_state_dict': metrics.get('model_state_dict'),
                'test_acc': test_acc,
                'train_loss': train_loss,
                'phase': metrics['phase']
            }, checkpoint_path)
            print(f"*** GROKKING CHECKPOINT SAVED: {checkpoint_path} ***")
    
    def get_summary(self) -> Dict:
        """Get summary statistics"""
        return {
            'total_epochs': len(self.history['train_loss']),
            'final_phase': self.current_phase,
            'phase_transitions': len(self.phase_history),
            'grokking_detected': self.grokking_detected,
            'grokking_epoch': self.grokking_epoch,
            'final_test_acc': self.history['test_acc'][-1] if self.history['test_acc'] else 0.0
        }

class AdaptiveTemperatureScheduler:
    """
    Thermodynamic thermostat implementing phase-dependent annealing.
    
    Controls both temperature (attention softmax divisor) and pressure 
    (weight_decay) according to the current thermodynamic phase.
    
    Gas phase: High WD forces weights through the Leiderman slot
    Liquid phase: Moderate WD allows structure formation
    Glass phase: Low WD permits approach to integer lattice
    Crystal approach: Minimal WD avoids disrupting fragile crystalline order
    """
    
    def __init__(self, model: LeiblerTransformer, config: LeidermanConfig, optimizer: torch.optim.Optimizer):
        self.model = model
        self.config = config
        self.optimizer = optimizer
        self.step_count = 0
        
        self.current_temperature = config.T_max
        self.base_temperature = config.T_max
        self.current_weight_decay = config.weight_decay_initial
        
        self.accuracy_history = []
        self.phase_stability_counter = 0
        
    def step(self, metrics: Dict[str, float]):
        """Update temperature and weight_decay based on thermodynamic phase"""
        epoch = metrics.get('epoch', 0)
        test_acc = metrics.get('test_acc', 0.0)
        current_phase = metrics.get('phase', 'gas')
        kappa = metrics.get('kappa', 999999.0)
        delta = metrics.get('delta', 0.5)
        
        self.accuracy_history.append(test_acc)
        if len(self.accuracy_history) > self.config.phase_window:
            self.accuracy_history.pop(0)
        
        if len(self.accuracy_history) >= 2:
            acc_change = abs(self.accuracy_history[-1] - self.accuracy_history[-2])
            if acc_change > self.config.phase_transition_threshold:
                self.phase_stability_counter = 0
            else:
                self.phase_stability_counter += 1
        
        # Phase-dependent thermostat: temperature AND pressure (weight_decay)
        if current_phase == 'crystal':
            target_temp = self.config.T_min
            target_wd = self.config.annealing_crystal_wd
        elif current_phase == 'glass':
            target_temp = self.config.T_min
            target_wd = self.config.annealing_glass_wd
        elif current_phase == 'liquid':
            progress = min(epoch / self.config.grokking_epochs, 1.0)
            target_temp = self.config.T_min + (self.config.T_max - self.config.T_min) * (1.0 - progress)
            target_wd = self.config.annealing_liquid_wd
        else:
            # Gas phase or unknown — high pressure exploration
            if epoch < self.config.warmup_epochs:
                warmup_progress = epoch / self.config.warmup_epochs
                target_temp = self.config.T_max * (1.0 - warmup_progress * 0.3)
            else:
                cool_epochs = epoch - self.config.warmup_epochs
                decay_factor = np.exp(-self.config.cooling_rate * cool_epochs)
                target_temp = self.config.T_min + (self.config.T_max - self.config.T_min) * decay_factor
            target_wd = self.config.annealing_gas_wd
        
        # Smooth transitions to avoid shocking the system
        smooth_factor = 0.95
        self.base_temperature = self.base_temperature * smooth_factor + target_temp * (1.0 - smooth_factor)
        self.current_weight_decay = self.current_weight_decay * smooth_factor + target_wd * (1.0 - smooth_factor)
        
        self.current_temperature = max(
            self.config.T_min,
            min(self.config.T_max, self.base_temperature)
        )
        
        self.step_count += 1
        
        self._update_model_temperatures()
        self._update_optimizer_weight_decay()
    
    def _update_model_temperatures(self):
        """Apply current temperature to all attention layers"""
        for layer in self.model.layers:
            layer.attention.temperature.data.fill_(self.current_temperature)
    
    def _update_optimizer_weight_decay(self):
        """Apply current weight_decay (pressure) to optimizer"""
        for param_group in self.optimizer.param_groups:
            param_group['weight_decay'] = self.current_weight_decay


def create_modular_addition_dataset(
    modulus: int = 27,
    train_fraction: float = 0.5
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Create dataset for modular addition task
    
    Args:
        modulus: Modulus for addition (vocabulary size - 1)
        train_fraction: Fraction of data for training
        
    Returns:
        train_x, train_y, test_x, test_y
    """
    # Generate all possible pairs
    all_pairs = []
    all_results = []
    
    for a in range(modulus):
        for b in range(modulus):
            # Format: [a, +, b, =]
            pair = [a + 1, modulus, b + 1, modulus + 1]  # +1 because 0 is padding
            result = (a + b) % modulus + 1
            
            all_pairs.append(pair)
            all_results.append(result)
    
    # Convert to tensors
    all_pairs = torch.tensor(all_pairs, dtype=torch.long)
    all_results = torch.tensor(all_results, dtype=torch.long)
    
    # Shuffle
    indices = torch.randperm(len(all_pairs))
    all_pairs = all_pairs[indices]
    all_results = all_results[indices]
    
    # Split
    n_train = int(len(all_pairs) * train_fraction)
    train_x = all_pairs[:n_train]
    train_y = all_results[:n_train]
    test_x = all_pairs[n_train:]
    test_y = all_results[n_train:]
    
    return train_x, train_y, test_x, test_y

def compute_kappa_from_gradient_covariance(
    model: LeiblerTransformer,
    train_x: torch.Tensor,
    train_y: torch.Tensor,
    config: LeidermanConfig,
    device: torch.device
) -> float:
    """
    Compute κ = cond(Σ) where Σ is the gradient covariance matrix.
    
    Samples gradients from multiple mini-batches to estimate Σ.
    Crystal state: κ → 1 (gradient noise is isotropic)
    Glass state: κ → ∞ (gradient noise is highly anisotropic)
    
    This is the core thermodynamic measurement from the paper.
    """
    model.eval()
    
    n_samples = len(train_x)
    n_batches = min(config.kappa_n_batches, max(1, n_samples // config.batch_size))
    
    gradient_samples = []
    
    indices = torch.randperm(n_samples)
    
    for i in range(n_batches):
        start = i * config.batch_size
        end = min(start + config.batch_size, n_samples)
        if start >= n_samples:
            break
            
        batch_indices = indices[start:end]
        batch_x = train_x[batch_indices].to(device)
        batch_y = train_y[batch_indices].to(device)
        
        model.zero_grad()
        logits = model(batch_x)
        loss = F.cross_entropy(logits[:, -1, :], batch_y)
        loss.backward()
        
        grad_vec = []
        for p in model.parameters():
            if p.grad is not None:
                grad_vec.append(p.grad.detach().flatten())
        
        if grad_vec:
            gradient_samples.append(torch.cat(grad_vec).cpu())
    
    model.train()
    
    if len(gradient_samples) < 2:
        return 999999.0
    
    # Stack into matrix: [n_batches, n_params]
    G = torch.stack(gradient_samples)
    
    # Compute covariance matrix Σ = (1/n) G^T G - μμ^T
    mean_g = G.mean(dim=0, keepdim=True)
    G_centered = G - mean_g
    
    # For high-dimensional params, use the dual form: Σ_small = G_centered @ G_centered^T / (n-1)
    # eigenvalues of this are same as eigenvalues of full covariance (up to zeros)
    n_b = G_centered.shape[0]
    cov_small = G_centered @ G_centered.T / max(n_b - 1, 1)
    
    try:
        eigenvalues = torch.linalg.eigvalsh(cov_small)
        eigenvalues = eigenvalues[eigenvalues > 1e-12]
        
        if len(eigenvalues) < 2:
            return 1.0
        
        kappa = (eigenvalues[-1] / eigenvalues[0]).item()
    except Exception:
        kappa = 999999.0
    
    return max(kappa, 1.0)

def compute_order_parameters(model: LeiblerTransformer) -> Tuple[float, float]:
    """
    Compute thermodynamic order parameters per paper definitions.
    
    κ = cond(Σ) where Σ = gradient covariance matrix
        Crystal: κ → 1.0 (isotropic gradient noise)
        Glass: κ → ∞ (anisotropic gradient noise)
    
    δ = ||θ - Q(θ)||∞ where Q rounds to nearest integer
        Crystal: δ → 0 (weights on integer lattice)
        Glass: δ → 0.5 (weights between integers)
    
    Returns:
        kappa, delta
    """
    all_weights = []
    for layer in model.layers:
        attn = layer.attention
        all_weights.extend([
            attn.q_proj.weight.detach().flatten(),
            attn.k_proj.weight.detach().flatten(),
            attn.v_proj.weight.detach().flatten(),
            attn.o_proj.weight.detach().flatten()
        ])
    
    weights = torch.cat(all_weights)
    
    # δ = ||θ - round(θ)||∞ — discretization margin
    rounded = torch.round(weights)
    delta = torch.abs(weights - rounded).max().item()
    
    # κ from accumulated gradients — uses gradient information stored on parameters
    grad_vectors = []
    for p in model.parameters():
        if p.grad is not None:
            grad_vectors.append(p.grad.detach().flatten())
    
    if len(grad_vectors) == 0:
        return 999999.0, delta
    
    grads = torch.cat(grad_vectors)
    
    # Approximate gradient covariance condition number from the gradient vector itself
    # For a single gradient snapshot, we reshape into a matrix and compute condition number
    # This approximates cond(Σ) — with multiple batches this converges to the true value
    n = len(grads)
    side = int(np.sqrt(n))
    if side * side < n:
        side += 1
    
    # Pad to make it reshapeable
    padded = torch.zeros(side * side, device=grads.device)
    padded[:n] = grads
    grad_matrix = padded.reshape(side, side)
    
    # Condition number via SVD
    try:
        s = torch.linalg.svdvals(grad_matrix)
        s_nonzero = s[s > 1e-12]
        if len(s_nonzero) < 2:
            kappa = 1.0
        else:
            kappa = (s_nonzero[0] / s_nonzero[-1]).item()
    except Exception:
        kappa = 999999.0
    
    return kappa, delta

def train_epoch(
    model: LeiblerTransformer,
    train_x: torch.Tensor,
    train_y: torch.Tensor,
    optimizer: torch.optim.Optimizer,
    config: LeidermanConfig,
    device: torch.device
) -> float:
    """Train for one epoch"""
    model.train()
    total_loss = 0.0
    n_batches = 0
    
    # Create batches
    n_samples = len(train_x)
    indices = torch.randperm(n_samples)
    
    for i in range(0, n_samples, config.batch_size):
        batch_indices = indices[i:i + config.batch_size]
        batch_x = train_x[batch_indices].to(device)
        batch_y = train_y[batch_indices].to(device)
        
        # Forward pass
        logits = model(batch_x)
        
        # Loss on last token (result position)
        loss = F.cross_entropy(logits[:, -1, :], batch_y)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        
        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        
        optimizer.step()
        
        total_loss += loss.item()
        n_batches += 1
    
    return total_loss / n_batches


@torch.no_grad()
def evaluate(
    model: LeiblerTransformer,
    test_x: torch.Tensor,
    test_y: torch.Tensor,
    config: LeidermanConfig,
    device: torch.device
) -> Tuple[float, float]:
    """Evaluate model"""
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    
    # Process in batches
    n_samples = len(test_x)
    for i in range(0, n_samples, config.batch_size):
        batch_x = test_x[i:i + config.batch_size].to(device)
        batch_y = test_y[i:i + config.batch_size].to(device)
        
        # Forward pass
        logits = model(batch_x)
        
        # Loss
        loss = F.cross_entropy(logits[:, -1, :], batch_y)
        total_loss += loss.item() * len(batch_x)
        
        # Accuracy
        predictions = torch.argmax(logits[:, -1, :], dim=-1)
        correct += (predictions == batch_y).sum().item()
        total += len(batch_x)
    
    avg_loss = total_loss / total
    accuracy = correct / total
    
    return avg_loss, accuracy


def prune_model(model: LeiblerTransformer, threshold: float = 0.1) -> int:
    """
    Prune slots with low weight magnitudes
    
    Args:
        model: Model to prune
        threshold: Magnitude threshold for pruning
        
    Returns:
        Number of slots remaining after pruning
    """
    print(f"\nPruning slots with magnitude < {threshold}...")
    
    for layer in model.layers:
        attn = layer.attention
        
        # Compute slot magnitudes
        q_mag = torch.norm(attn.q_proj.weight, dim=1)
        k_mag = torch.norm(attn.k_proj.weight, dim=1)
        v_mag = torch.norm(attn.v_proj.weight, dim=1)
        o_mag = torch.norm(attn.o_proj.weight, dim=0)
        
        # Average magnitude across projections
        avg_mag = (q_mag + k_mag + v_mag + o_mag) / 4.0
        
        # Keep slots above threshold
        keep_mask = avg_mag > threshold
        keep_indices = torch.where(keep_mask)[0]
        
        if len(keep_indices) < len(avg_mag):
            print(f"Pruning from {len(avg_mag)} to {len(keep_indices)} slots...")
            print(f"Keeping indices: {keep_indices.tolist()}")
            
            # Prune weights
            with torch.no_grad():
                attn.q_proj.weight.data = attn.q_proj.weight.data[keep_indices, :]
                attn.k_proj.weight.data = attn.k_proj.weight.data[keep_indices, :]
                attn.v_proj.weight.data = attn.v_proj.weight.data[keep_indices, :]
                attn.o_proj.weight.data = attn.o_proj.weight.data[:, keep_indices]
                
                if attn.q_proj.bias is not None:
                    attn.q_proj.bias.data = attn.q_proj.bias.data[keep_indices]
                    attn.k_proj.bias.data = attn.k_proj.bias.data[keep_indices]
                    attn.v_proj.bias.data = attn.v_proj.bias.data[keep_indices]
            
            print(f"Pruning complete. New sizes: U{attn.q_proj.weight.shape}, V{attn.k_proj.weight.shape}, W{attn.o_proj.weight.shape}")
    
    return len(keep_indices)


def discretize_model(model: LeiblerTransformer, tolerance: float = 0.1) -> bool:
    """
    Attempt to discretize model weights to integers
    
    Args:
        model: Model to discretize
        tolerance: Maximum distance from integer
        
    Returns:
        True if discretization successful
    """
    print(f"\nAttempting discretization with tolerance {tolerance}...")
    
    can_discretize = True
    
    for layer in model.layers:
        attn = layer.attention
        
        for name, param in [
            ('q_proj', attn.q_proj.weight),
            ('k_proj', attn.k_proj.weight),
            ('v_proj', attn.v_proj.weight),
            ('o_proj', attn.o_proj.weight)
        ]:
            # Check if weights are close to integers
            rounded = torch.round(param.data)
            distance = torch.abs(param.data - rounded).max().item()
            
            if distance > tolerance:
                print(f"Cannot discretize {name}: max distance {distance:.4f} > {tolerance}")
                can_discretize = False
            else:
                # Discretize
                param.data = rounded
    
    if can_discretize:
        print("Discretization successful!")
    else:
        print("Discretization failed - weights not close enough to integers")
    
    return can_discretize


def main():
    parser = argparse.ArgumentParser(description='Train Leibler Transformer with Thermodynamic Grokking')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size (crystal window: 24-128)')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning rate')
    parser.add_argument('--epochs', type=int, default=25000, help='Number of epochs')
    parser.add_argument('--modulus', type=int, default=26, help='Modulus for addition')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu')
    parser.add_argument('--kappa_interval', type=int, default=50, help='Epochs between full kappa measurements')
    args = parser.parse_args()
    
    config = LeidermanConfig(
        vocab_size=args.modulus + 2,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        max_epochs=args.epochs
    )
    
    device = torch.device(args.device)
    print(f"Using device: {device}")
    print(f"Configuration: {config}")
    
    print("\nCreating modular addition dataset...")
    train_x, train_y, test_x, test_y = create_modular_addition_dataset(
        modulus=args.modulus,
        train_fraction=0.5
    )
    print(f"Train size: {len(train_x)}, Test size: {len(test_x)}")
    
    print("\nInitializing Leibler Transformer...")
    model = LeiblerTransformer(config).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,}")
    
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.learning_rate,
        weight_decay=config.weight_decay_initial
    )
    
    # Scheduler receives optimizer to control weight_decay (pressure)
    temp_scheduler = AdaptiveTemperatureScheduler(model, config, optimizer)
    
    tracker = ThermodynamicTracker(config)
    
    # Cached kappa value (expensive to compute every epoch)
    cached_kappa = 999999.0
    
    print("\n" + "="*80)
    print("PHASE 1: THERMODYNAMIC TRAINING WITH GROKKING")
    print("="*80 + "\n")
    
    pbar = tqdm(range(config.max_epochs), desc="Training")
    
    for epoch in pbar:
        train_loss = train_epoch(model, train_x, train_y, optimizer, config, device)
        
        test_loss, test_acc = evaluate(model, test_x, test_y, config, device)
        
        thermo_state = model.get_thermodynamic_state()
        
        # Fast order parameters every epoch (δ from weights, κ approximate from last grad)
        _, delta = compute_order_parameters(model)
        
        # Full κ measurement from gradient covariance every kappa_interval epochs
        if epoch % args.kappa_interval == 0:
            cached_kappa = compute_kappa_from_gradient_covariance(
                model, train_x, train_y, config, device
            )
        
        kappa = cached_kappa
        
        grad_norm = 0.0
        for p in model.parameters():
            if p.grad is not None:
                grad_norm += p.grad.norm().item() ** 2
        grad_norm = np.sqrt(grad_norm)
        
        weight_norm = sum(p.norm().item() for p in model.parameters())
        
        metrics = {
            'epoch': epoch,
            'train_loss': train_loss,
            'test_loss': test_loss,
            'test_acc': test_acc,
            'entropy': thermo_state['entropy'],
            'heat_capacity': thermo_state['heat_capacity'],
            'T_eff': thermo_state['T_eff'],
            'temperature': thermo_state['temperature'],
            'kappa': kappa,
            'delta': delta,
            'grad_norm': grad_norm,
            'weight_norm': weight_norm,
            'model_state_dict': model.state_dict()
        }
        
        tracker.update(metrics)
        temp_scheduler.step(metrics)
        
        pbar.set_postfix({
            'train_loss': f'{train_loss:.2e}',
            'test_loss': f'{test_loss:.2e}',
            'test_acc': f'{test_acc:.3f}',
            'kappa': f'{kappa:.3f}',
            'delta': f'{delta:.3f}',
            'WD': f'{temp_scheduler.current_weight_decay:.1e}',
            'T_eff': f'{thermo_state["T_eff"]:.2e}',
            'S': f'{thermo_state["entropy"]:.2f}',
            'C_v': f'{thermo_state["heat_capacity"]:.2e}',
            '|W|': f'{weight_norm:.2f}',
            '|grad|': f'{grad_norm:.2e}',
            'phase': tracker.current_phase[:4]
        })
    
    print("\n" + "="*80)
    print("PHASE 2: PRUNING AND DISCRETIZATION")
    print("="*80 + "\n")
    
    n_slots = prune_model(model, threshold=config.pruning_threshold)
    print(f"\nModel pruned to {n_slots} slots")
    
    discretized = discretize_model(model, tolerance=config.discretization_tolerance)
    
    test_loss, test_acc = evaluate(model, test_x, test_y, config, device)
    print(f"Post-discretization test accuracy: {test_acc:.4f}")
    
    # Final κ measurement
    final_kappa = compute_kappa_from_gradient_covariance(
        model, train_x, train_y, config, device
    )
    _, final_delta = compute_order_parameters(model)
    
    print("\n" + "="*80)
    print("EXPERIMENT SUMMARY")
    print("="*80)
    summary = tracker.get_summary()
    print(f"Total epochs trained: {summary['total_epochs']}")
    print(f"Final phase: {summary['final_phase']}")
    print(f"Final kappa: {final_kappa:.6f}")
    print(f"Final delta: {final_delta:.6f}")
    print(f"Final test accuracy: {test_acc:.4f}")
    print(f"Discretization success: {discretized}")
    
    if tracker.grokking_detected:
        print(f"\nGrokking detected at epoch {tracker.grokking_epoch}")


if __name__ == '__main__':
    main()