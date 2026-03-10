#!/usr/bin/env python3
"""
Laderman Algorithm Crystallization in Transformers
Thermodynamic Algorithmic Crystallization Framework

This module implements the two-phase protocol for inducing algorithmic structures
in neural networks, specifically targeting the Laderman matrix multiplication
algorithm for 3x3 matrices with rank 23 decomposition.

The implementation follows thermodynamic principles where:
- kappa (kappa) serves as the order parameter for phase classification
- delta measures discretization margin (distance to integer lattice)
- T_eff represents effective temperature from gradient fluctuations
- Local Complexity (LC) captures the phase transition
- Superposition coefficient (psi) measures feature entanglement

Author: Implementation based on thermodynamic grokking framework
License: AGPL v3
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import time
import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from pathlib import Path
from collections import deque

try:
    from tqdm.auto import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable


@dataclass(frozen=True)
class LadermanConfig:
    """
    Complete configuration for Laderman crystallization experiment.
    All parameters are centralized here to avoid magic numbers throughout the codebase.
    
    Architecture parameters control the Transformer model structure.
    Training parameters control the optimization process.
    Thermodynamic parameters control phase detection and grokking.
    Expansion parameters control zero-shot transfer verification.
    """

    experiment_name: str = "laderman_crystallization"
    seed: int = 42

    matrix_size: int = 3
    target_rank: int = 23
    initial_slots: int = 27
    expansion_sizes: Tuple[int, ...] = (3, 6, 12, 24)

    hidden_size: int = 128
    num_hidden_layers: int = 2
    num_attention_heads: int = 4
    intermediate_size: int = 256
    hidden_dropout_prob: float = 0.0
    attention_probs_dropout_prob: float = 0.0
    max_position_embeddings: int = 512
    initializer_range: float = 0.02
    layer_norm_eps: float = 1e-12

    batch_size: int = 64
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    num_epochs: int = 5000
    warmup_steps: int = 100
    gradient_clipping_max_norm: float = 1.0

    pruning_target: int = 23
    discretization_threshold: float = 0.1
    accuracy_tolerance: float = 0.01

    grokking_detection_enabled: bool = True
    grokking_window_size: int = 100
    grokking_accuracy_threshold: float = 0.99
    grokking_past_accuracy_threshold: float = 0.5
    grokking_stability_epochs: int = 3

    crystallization_check_interval: int = 50
    crystallization_confirmation_epochs: int = 50

    lc_collapse_threshold: float = 1.0
    kappa_stability_threshold: float = 10.0
    kappa_crystal_threshold: float = 1.001
    delta_crystal_threshold: float = 0.01
    delta_polycrystal_threshold: float = 0.15
    delta_glass_threshold: float = 0.45
    T_eff_cold_threshold: float = 1e-10
    T_eff_crystal_threshold: float = 1e-16
    entropy_crystal_threshold: float = 0.5

    checkpoint_interval_minutes: float = 5.0
    checkpoint_dir: str = "./laderman_checkpoints"
    keep_last_n_checkpoints: int = 3

    gradient_covariance_samples: int = 10
    temperature_samples: int = 10

    train_samples: int = 10000
    test_samples: int = 2000
    num_workers: int = 0

    device: str = "cpu"

    def __post_init__(self):
        self._validate_parameters()
        self._ensure_directories()
        object.__setattr__(self, 'device', torch.device(self.device))

    def _validate_parameters(self) -> None:
        if not (8 <= self.batch_size <= 512):
            raise ValueError(f"Batch size {self.batch_size} outside valid range [8, 512]")
        if self.grokking_window_size < 10:
            raise ValueError(f"Grokking window size must be at least 10, got {self.grokking_window_size}")
        if self.weight_decay < 0:
            raise ValueError(f"Weight decay must be non-negative, got {self.weight_decay}")
        if self.crystallization_check_interval < 1:
            raise ValueError(f"Crystallization check interval must be >= 1, got {self.crystallization_check_interval}")
        if self.initial_slots < self.target_rank:
            raise ValueError(f"Initial slots ({self.initial_slots}) must be >= target rank ({self.target_rank})")
        if self.matrix_size != 3:
            raise ValueError(f"This implementation is designed for 3x3 matrices, got {self.matrix_size}")

    def _ensure_directories(self) -> None:
        Path(self.checkpoint_dir).mkdir(parents=True, exist_ok=True)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d['device'] = str(d['device'])
        d['expansion_sizes'] = list(d['expansion_sizes'])
        return d


@dataclass
class ThermodynamicState:
    """
    Complete thermodynamic state tracking for phase classification.
    
    This class captures all metrics required for thermodynamic analysis
    of the training dynamics, following the methodology established in
    the Strassen grokking research.
    """

    epoch: int
    step: int
    timestamp: float
    train_loss: float
    test_loss: float
    train_accuracy: float
    test_accuracy: float
    delta: float
    is_discretized: bool
    kappa: float
    kappa_stable: bool
    local_complexity: float
    lc_transition_detected: bool
    superposition_coefficient: float
    effective_feature_count: float
    effective_temperature: float
    entropy: float
    heat_capacity: float
    weight_norm: float
    gradient_norm: float
    h_bar_eff: float
    phase: str = "unknown"
    grokking_detected: bool = False
    grokking_stable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            'epoch': self.epoch,
            'step': self.step,
            'timestamp': self.timestamp,
            'train_loss': self.train_loss,
            'test_loss': self.test_loss,
            'train_accuracy': self.train_accuracy,
            'test_accuracy': self.test_accuracy,
            'delta': self.delta,
            'is_discretized': self.is_discretized,
            'kappa': self.kappa,
            'kappa_stable': self.kappa_stable,
            'local_complexity': self.local_complexity,
            'lc_transition_detected': self.lc_transition_detected,
            'superposition_coefficient': self.superposition_coefficient,
            'effective_feature_count': self.effective_feature_count,
            'effective_temperature': self.effective_temperature,
            'entropy': self.entropy,
            'heat_capacity': self.heat_capacity,
            'weight_norm': self.weight_norm,
            'gradient_norm': self.gradient_norm,
            'h_bar_eff': self.h_bar_eff,
            'phase': self.phase,
            'grokking_detected': self.grokking_detected,
            'grokking_stable': self.grokking_stable
        }


class MetricComputerInterface(ABC):
    """Abstract base class for metric computation following SOLID principles."""

    @abstractmethod
    def compute(self, model: nn.Module, batch: Optional[Tuple] = None) -> Dict[str, float]:
        pass


class GradientCovarianceComputer(MetricComputerInterface):
    """
    Compute kappa: condition number of gradient covariance matrix.
    
    The gradient covariance condition number serves as an order parameter
    for phase classification. Values near 1.0 indicate crystalline states,
    while large values indicate glassy states.
    
    Memory-efficient implementation using SVD decomposition.
    """

    def __init__(self, num_samples: int = 10):
        self.num_samples = num_samples

    def compute(self, model: nn.Module, batch: Optional[Tuple] = None) -> Dict[str, float]:
        if batch is None:
            return {'kappa': float('inf'), 'kappa_stable': False}

        input_a, input_b, target = batch
        gradients = self._collect_gradients(model, input_a, input_b, target)

        if len(gradients) < 2:
            return {'kappa': float('inf'), 'kappa_stable': False}

        kappa = self._compute_condition_number(gradients)
        kappa_stable = abs(kappa - 1.0) < 0.001

        return {'kappa': kappa, 'kappa_stable': kappa_stable}

    def _collect_gradients(self, model: nn.Module, input_a: torch.Tensor,
                          input_b: torch.Tensor, target: torch.Tensor) -> List[torch.Tensor]:
        gradients = []
        max_samples = min(self.num_samples, input_a.size(0), 10)

        for i in range(max_samples):
            model.zero_grad()
            output = self._forward_model(model, input_a[i:i+1], input_b[i:i+1])
            loss = F.mse_loss(output, target[i:i+1])
            loss.backward()

            grad_vector = self._extract_bilinear_gradients(model)
            if grad_vector is not None:
                gradients.append(grad_vector)

        return gradients

    def _forward_model(self, model: nn.Module, input_a: torch.Tensor,
                       input_b: torch.Tensor) -> torch.Tensor:
        output = model(input_a, input_b)
        if hasattr(output, 'last_hidden_state'):
            return output.last_hidden_state.squeeze(1)
        return output[0] if isinstance(output, tuple) else output

    def _extract_bilinear_gradients(self, model: nn.Module) -> Optional[torch.Tensor]:
        grad_list = []
        for name, param in model.named_parameters():
            if param.grad is not None and name in ['U', 'V', 'W']:
                grad_list.append(param.grad.view(-1).detach())
        
        return torch.cat(grad_list) if grad_list else None

    def _compute_condition_number(self, gradients: List[torch.Tensor]) -> float:
        grad_matrix = torch.stack(gradients)
        grad_mean = grad_matrix.mean(dim=0, keepdim=True)
        grad_centered = grad_matrix - grad_mean

        try:
            _, s, _ = torch.svd(grad_centered)
            s_nonzero = s[s > 1e-6]
            if len(s_nonzero) == 0:
                return float('inf')
            return (s_nonzero.max() / s_nonzero.min()).item()
        except Exception:
            return float('inf')


class LocalComplexityComputer(MetricComputerInterface):
    """
    Compute Local Complexity (LC) as a phase transition marker.
    
    LC measures the effective local dimensionality of the model.
    It falls from initial high values to near-zero exactly at
    the grokking transition, capturing the phase change.
    """

    def __init__(self, singular_value_threshold_ratio: float = 0.01):
        self.singular_value_threshold_ratio = singular_value_threshold_ratio

    def compute(self, model: nn.Module, batch: Optional[Tuple] = None) -> Dict[str, float]:
        if not hasattr(model, 'get_bilinear_tensors'):
            return {'local_complexity': 100.0, 'lc_transition_detected': False}

        u, _, _ = model.get_bilinear_tensors()
        lc = self._compute_effective_rank(u)
        lc_transition = lc < 1.0

        return {'local_complexity': lc, 'lc_transition_detected': lc_transition}

    def _compute_effective_rank(self, tensor: torch.Tensor) -> float:
        try:
            singular_values = torch.linalg.svdvals(tensor)
            threshold = self.singular_value_threshold_ratio * singular_values.max()
            return float((singular_values > threshold).sum().item())
        except Exception:
            return float(tensor.size(0))


class SuperpositionComputer(MetricComputerInterface):
    """
    Compute superposition coefficient psi and effective feature count.
    
    The superposition coefficient measures feature entanglement in the
    weight space. Crystalline states show lower psi values, indicating
    reduced feature entanglement compared to glassy states.
    """

    def compute(self, model: nn.Module, batch: Optional[Tuple] = None) -> Dict[str, float]:
        if not hasattr(model, 'get_bilinear_tensors'):
            return {'superposition_coefficient': 2.0, 'effective_feature_count': 27.0}

        u, _, _ = model.get_bilinear_tensors()
        psi = self._compute_superposition_coefficient(u)
        f_eff = self._compute_effective_feature_count(u)

        return {'superposition_coefficient': psi, 'effective_feature_count': f_eff}

    def _compute_superposition_coefficient(self, u: torch.Tensor) -> float:
        u_norm = F.normalize(u, dim=1)
        overlap = torch.mm(u_norm, u_norm.t())
        mask = ~torch.eye(overlap.size(0), dtype=torch.bool, device=overlap.device)
        return overlap[mask].abs().mean().item() + 1.0

    def _compute_effective_feature_count(self, u: torch.Tensor) -> float:
        singular_values = torch.linalg.svdvals(u)
        sv_squared = singular_values ** 2
        total = sv_squared.sum()
        if total <= 0:
            return float(u.size(0))
        return (total ** 2 / (sv_squared ** 2).sum()).item()


class TemperatureComputer(MetricComputerInterface):
    """
    Compute effective temperature T_eff from gradient fluctuations.
    
    The effective temperature is derived from the fluctuation-dissipation
    relation. Crystalline states exhibit T_eff < 1e-16, while glassy
    states show higher values, allowing phase classification.
    """

    def __init__(self, num_samples: int = 10):
        self.num_samples = num_samples

    def compute(self, model: nn.Module, batch: Optional[Tuple] = None) -> Dict[str, float]:
        if batch is None:
            return {'effective_temperature': 1.0, 'entropy': 0.0, 'heat_capacity': 0.0}

        input_a, input_b, target = batch
        grad_norms = self._collect_gradient_norms(model, input_a, input_b, target)

        if len(grad_norms) == 0:
            return {'effective_temperature': 1.0, 'entropy': 0.0, 'heat_capacity': 0.0}

        grad_norms_tensor = torch.tensor(grad_norms)
        t_eff = grad_norms_tensor.var().item()
        entropy = self._compute_entropy(grad_norms_tensor)
        heat_capacity = self._compute_heat_capacity(grad_norms_tensor, t_eff)

        return {
            'effective_temperature': t_eff,
            'entropy': entropy,
            'heat_capacity': heat_capacity
        }

    def _collect_gradient_norms(self, model: nn.Module, input_a: torch.Tensor,
                                 input_b: torch.Tensor, target: torch.Tensor) -> List[float]:
        grad_norms = []
        max_samples = min(self.num_samples, input_a.size(0), 10)

        for i in range(max_samples):
            model.zero_grad()
            output = self._forward_model(model, input_a[i:i+1], input_b[i:i+1])
            loss = F.mse_loss(output, target[i:i+1])
            loss.backward()

            grad_norm = self._compute_bilinear_grad_norm(model)
            if grad_norm > 0:
                grad_norms.append(grad_norm)

        return grad_norms

    def _forward_model(self, model: nn.Module, input_a: torch.Tensor,
                       input_b: torch.Tensor) -> torch.Tensor:
        output = model(input_a, input_b)
        if hasattr(output, 'last_hidden_state'):
            return output.last_hidden_state.squeeze(1)
        return output[0] if isinstance(output, tuple) else output

    def _compute_bilinear_grad_norm(self, model: nn.Module) -> float:
        grad_norm_sq = 0.0
        for name, param in model.named_parameters():
            if param.grad is not None and name in ['U', 'V', 'W']:
                grad_norm_sq += param.grad.norm(2).item() ** 2
        return grad_norm_sq ** 0.5

    def _compute_entropy(self, values: torch.Tensor) -> float:
        num_bins = min(20, len(values))
        hist = torch.histc(values, bins=num_bins)
        hist = hist / hist.sum()
        return -(hist * torch.log(hist + 1e-10)).sum().item()

    def _compute_heat_capacity(self, values: torch.Tensor, t_eff: float) -> float:
        if t_eff <= 0:
            return 0.0
        return values.var().item() / t_eff


class HBarEffComputer(MetricComputerInterface):
    """
    Compute effective Planck constant h_bar_eff.
    
    The effective Planck constant governs the minimum gradient temperature
    required for algorithm crystallization. It characterizes the quantum-like
    behavior of the optimization landscape.
    """

    def compute(self, model: nn.Module, batch: Optional[Tuple] = None,
                effective_temperature: float = 0.0, kappa: float = float('inf')) -> Dict[str, float]:
        if not hasattr(model, 'get_bilinear_tensors'):
            return {'h_bar_eff': float('inf')}

        u, v, w = model.get_bilinear_tensors()
        weight_variance = self._compute_weight_variance(u, v, w)

        if effective_temperature < 1e-20:
            h_bar_eff = self._estimate_crystal_h_bar(weight_variance, kappa)
        else:
            h_bar_eff = self._estimate_glass_h_bar(effective_temperature, weight_variance)

        return {'h_bar_eff': h_bar_eff}

    def _compute_weight_variance(self, u: torch.Tensor, v: torch.Tensor, w: torch.Tensor) -> float:
        all_weights = torch.cat([u.flatten(), v.flatten(), w.flatten()])
        return torch.var(all_weights).item()

    def _estimate_crystal_h_bar(self, weight_variance: float, kappa: float) -> float:
        if kappa < 1.001:
            return 1e-7
        return weight_variance / (kappa + 1e-10)

    def _estimate_glass_h_bar(self, t_eff: float, weight_variance: float) -> float:
        return t_eff * (weight_variance ** 0.5 + 1.0)


class MatrixMultiplicationDataset(Dataset):
    """Dataset for matrix multiplication task."""

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

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return self.inputs_a[idx], self.inputs_b[idx], self.targets[idx]


class BilinearTransformerModel(nn.Module):
    """
    Transformer model for bilinear matrix multiplication.
    
    This model combines a Transformer encoder with bilinear tensors (U, V, W)
    to implement the Laderman algorithm structure for 3x3 matrix multiplication.
    """

    def __init__(self, config: LadermanConfig):
        super().__init__()
        self.config = config

        n = config.matrix_size
        n_squared = n * n

        self.input_proj_a = nn.Linear(n_squared, config.hidden_size)
        self.input_proj_b = nn.Linear(n_squared, config.hidden_size)

        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config.hidden_size,
            nhead=config.num_attention_heads,
            dim_feedforward=config.intermediate_size,
            dropout=config.hidden_dropout_prob,
            activation='gelu',
            batch_first=True,
            norm_first=False
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=config.num_hidden_layers,
            norm=nn.LayerNorm(config.hidden_size, eps=config.layer_norm_eps)
        )

        self.U = nn.Parameter(torch.randn(config.initial_slots, n_squared) * config.initializer_range)
        self.V = nn.Parameter(torch.randn(config.initial_slots, n_squared) * config.initializer_range)
        self.W = nn.Parameter(torch.randn(n_squared, config.initial_slots) * config.initializer_range)

        self.output_proj = nn.Linear(config.hidden_size, n_squared)

        self._init_weights()

    def _init_weights(self) -> None:
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, mean=0.0, std=self.config.initializer_range)

    def forward(self, input_a: torch.Tensor, input_b: torch.Tensor,
                output_attentions: bool = False, return_dict: bool = True) -> Any:
        batch_size = input_a.size(0)

        emb_a = self.input_proj_a(input_a)
        emb_b = self.input_proj_b(input_b)

        positions = torch.arange(2, device=input_a.device).unsqueeze(0).expand(batch_size, -1)
        pos_emb = self.position_embeddings(positions)

        sequence = torch.stack([emb_a, emb_b], dim=1) + pos_emb

        hidden_states = self.encoder(sequence)

        pooled = hidden_states.mean(dim=1)

        m = (input_a @ self.U.t()) * (input_b @ self.V.t())
        bilinear_out = m @ self.W.t()

        combined = self.output_proj(pooled) + bilinear_out

        if return_dict:
            return type('Output', (), {
                'last_hidden_state': combined.unsqueeze(1),
                'attentions': None
            })()
        return (combined,)

    def get_bilinear_tensors(self) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return self.U.detach().clone(), self.V.detach().clone(), self.W.detach().clone()

    def set_bilinear_tensors(self, u: torch.Tensor, v: torch.Tensor, w: torch.Tensor) -> None:
        with torch.no_grad():
            if u.size(0) != self.U.size(0):
                self.U = nn.Parameter(torch.empty_like(u))
                self.V = nn.Parameter(torch.empty_like(v))
                self.W = nn.Parameter(torch.empty_like(w))

            self.U.copy_(u)
            self.V.copy_(v)
            self.W.copy_(w)

    def compute_discretization_margin(self) -> float:
        all_params = torch.cat([self.U.view(-1), self.V.view(-1), self.W.view(-1)])
        rounded = torch.round(all_params).clamp(-1, 1)
        return torch.norm(all_params - rounded, p=float('inf')).item()

    def discretize(self, threshold: float = 0.1) -> bool:
        if self.compute_discretization_margin() > threshold:
            return False
        with torch.no_grad():
            for param in [self.U, self.V, self.W]:
                param.copy_(torch.round(param).clamp(-1, 1))
        return True

    def get_weight_norm(self) -> float:
        return sum(p.data.norm(2).item() ** 2 for p in self.parameters()) ** 0.5

    def compute_gradient_norm(self) -> float:
        return sum(p.grad.data.norm(2).item() ** 2 
                   for p in self.parameters() if p.grad is not None) ** 0.5


class MagnitudePruning:
    """Prune slots based on L2 magnitude importance."""

    def prune(self, model: nn.Module, target_slots: int) -> nn.Module:
        if not hasattr(model, 'get_bilinear_tensors'):
            return model

        u, v, w = model.get_bilinear_tensors()
        current_slots = u.size(0)

        if current_slots <= target_slots:
            print(f"No pruning needed: {current_slots} slots <= {target_slots} target")
            return model

        print(f"Pruning from {current_slots} to {target_slots} slots...")

        importance = self._compute_importance(u, v, w)
        keep_indices = self._select_top_k(importance, target_slots)

        print(f"Keeping indices: {keep_indices.tolist()}")

        u_new = u[keep_indices]
        v_new = v[keep_indices]
        w_new = w[:, keep_indices]

        model.set_bilinear_tensors(u_new, v_new, w_new)

        self._verify_pruning(model, target_slots)

        return model

    def _compute_importance(self, u: torch.Tensor, v: torch.Tensor, w: torch.Tensor) -> torch.Tensor:
        importance = torch.zeros(u.size(0))
        for i in range(u.size(0)):
            importance[i] = u[i].norm(2).item() + v[i].norm(2).item() + w[:, i].norm(2).item()
        return importance

    def _select_top_k(self, importance: torch.Tensor, k: int) -> torch.Tensor:
        _, keep_indices = torch.topk(importance, k)
        return keep_indices.sort()[0]

    def _verify_pruning(self, model: nn.Module, target_slots: int) -> None:
        u_check, v_check, w_check = model.get_bilinear_tensors()
        assert u_check.size(0) == target_slots, f"U size mismatch: {u_check.size(0)} != {target_slots}"
        assert v_check.size(0) == target_slots, f"V size mismatch: {v_check.size(0)} != {target_slots}"
        assert w_check.size(1) == target_slots, f"W size mismatch: {w_check.size(1)} != {target_slots}"
        print(f"Pruning complete. New sizes: U{u_check.shape}, V{v_check.shape}, W{w_check.shape}")


class FileCheckpointManager:
    """Checkpoint management with configurable time-based intervals."""

    def __init__(self, config: LadermanConfig):
        self.config = config
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints: List[Path] = []
        self.grokking_checkpoints: List[Path] = []
        self.last_checkpoint_time = time.time()
        self.latest_path = self.checkpoint_dir / "latest.pt"

    def should_checkpoint(self) -> bool:
        elapsed = time.time() - self.last_checkpoint_time
        return elapsed > (self.config.checkpoint_interval_minutes * 60)

    def save(self, model: nn.Module, optimizer: torch.optim.Optimizer,
             state: ThermodynamicState, path: Optional[str] = None,
             checkpoint_type: str = "regular") -> str:

        if path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            if checkpoint_type == "grokking":
                path = self.checkpoint_dir / f"grokking_epoch{state.epoch}_{timestamp}.pt"
            elif checkpoint_type == "crystallization":
                path = self.checkpoint_dir / f"crystallization_epoch{state.epoch}_{timestamp}.pt"
            else:
                path = self.checkpoint_dir / f"checkpoint_epoch{state.epoch}_{timestamp}.pt"
        else:
            path = Path(path)

        checkpoint = {
            'epoch': state.epoch,
            'step': state.step,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'thermodynamic_state': state.to_dict(),
            'config': self.config.to_dict(),
            'timestamp': time.time(),
            'checkpoint_type': checkpoint_type
        }

        temp_path = path.with_suffix('.tmp')
        torch.save(checkpoint, temp_path)
        temp_path.replace(path)

        torch.save(checkpoint, self.latest_path)

        if checkpoint_type == "grokking":
            self.grokking_checkpoints.append(path)
            print(f"\n*** GROKKING CHECKPOINT SAVED: {path.name} ***")
        elif checkpoint_type == "crystallization":
            self.grokking_checkpoints.append(path)
            print(f"\n*** CRYSTALLIZATION CHECKPOINT SAVED: {path.name} ***")
        else:
            self.checkpoints.append(path)
            self._cleanup()
            self.last_checkpoint_time = time.time()

        return str(path)

    def _cleanup(self) -> None:
        if len(self.checkpoints) > self.config.keep_last_n_checkpoints:
            to_remove = self.checkpoints[:-self.config.keep_last_n_checkpoints]
            for cp in to_remove:
                if cp.exists() and cp.name != 'latest.pt':
                    cp.unlink()
            self.checkpoints = self.checkpoints[-self.config.keep_last_n_checkpoints:]


class PhaseClassifier:
    """
    Classify thermodynamic phase based on order parameters.
    
    Phase classification follows the criteria established in the Strassen
    grokking research, using delta, kappa, LC, and T_eff as order parameters.
    
    Phases:
    - crystal: Discrete algorithmic structure with perfect discretization
    - polycrystal: Intermediate state from pruning, stable but not fully discrete
    - warm_glass: High accuracy but not discretizable, high temperature
    - glass: Non-discretizable state with high delta and entropy
    - unknown: Transitional or unclassifiable state
    """

    def __init__(self, config: LadermanConfig):
        self.config = config

    def classify(self, delta: float, kappa: float, lc: float,
                 t_eff: float, test_accuracy: float) -> str:
        is_high_accuracy = test_accuracy > self.config.grokking_accuracy_threshold
        is_kappa_stable = kappa < self.config.kappa_stability_threshold
        is_kappa_crystal = kappa < self.config.kappa_crystal_threshold
        is_lc_collapsed = lc < self.config.lc_collapse_threshold
        is_delta_discrete = delta < self.config.delta_crystal_threshold
        is_delta_intermediate = (
            self.config.delta_crystal_threshold <= delta < self.config.delta_polycrystal_threshold
        )
        is_delta_extended = delta >= self.config.delta_glass_threshold
        is_cold = t_eff < self.config.T_eff_cold_threshold
        is_very_cold = t_eff < self.config.T_eff_crystal_threshold

        if is_delta_discrete and is_kappa_crystal and is_lc_collapsed and is_high_accuracy and is_very_cold:
            return "crystal"

        if is_delta_intermediate and is_kappa_stable and is_high_accuracy:
            return "polycrystal"

        if is_delta_extended and not is_kappa_stable:
            if is_cold:
                return "glass"
            else:
                return "warm_glass"

        if is_high_accuracy and not is_delta_discrete:
            return "glass"

        return "unknown"


class GrokkingDetector:
    """
    Detect grokking events with stability verification.
    
    Grokking is detected when test accuracy jumps from low values to near-perfect
    while training loss remains low. The implementation requires sustained accuracy
    over multiple epochs to avoid false positives from transient fluctuations.
    """

    def __init__(self, config: LadermanConfig):
        self.config = config
        self.accuracy_history: deque = deque(maxlen=config.grokking_window_size)
        self.stable_epochs = 0
        self.prev_test_acc = 0.0
        self.grokking_confirmed = False

    def update(self, test_accuracy: float, train_loss: float) -> Tuple[bool, bool]:
        self.accuracy_history.append(test_accuracy)

        grokking_detected = False
        grokking_stable = False

        if len(self.accuracy_history) >= self.config.grokking_window_size:
            past_accuracy = list(self.accuracy_history)[0]
            
            if (test_accuracy >= self.config.grokking_accuracy_threshold and
                past_accuracy <= self.config.grokking_past_accuracy_threshold and
                train_loss < 1e-3):
                
                self.stable_epochs += 1
                
                if self.stable_epochs >= self.config.grokking_stability_epochs:
                    grokking_detected = True
                    grokking_stable = True
                    self.grokking_confirmed = True
            else:
                if self.stable_epochs > 0:
                    self.stable_epochs = 0

        self.prev_test_acc = test_accuracy
        return grokking_detected, grokking_stable


class CrystallizationTrainer:
    """
    Two-phase training protocol for algorithmic crystallization.
    
    Phase 1: Extended training with thermodynamic monitoring until grokking
             occurs or crystallization is confirmed.
    Phase 2: Pruning to target rank followed by discretization verification.
    """

    def __init__(self, config: LadermanConfig, model: nn.Module,
                 train_loader: DataLoader, test_loader: DataLoader,
                 checkpoint_manager: FileCheckpointManager):
        self.config = config
        self.model = model.to(config.device)
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.checkpoint_manager = checkpoint_manager

        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )

        self.metric_computers = self._initialize_metric_computers()
        self.phase_classifier = PhaseClassifier(config)
        self.grokking_detector = GrokkingDetector(config)

        self.current_epoch = 0
        self.current_step = 0
        self.trajectory: List[ThermodynamicState] = []

    def _initialize_metric_computers(self) -> Dict[str, MetricComputerInterface]:
        return {
            'gradient_covariance': GradientCovarianceComputer(
                num_samples=self.config.gradient_covariance_samples
            ),
            'local_complexity': LocalComplexityComputer(),
            'superposition': SuperpositionComputer(),
            'temperature': TemperatureComputer(
                num_samples=self.config.temperature_samples
            ),
            'h_bar_eff': HBarEffComputer()
        }

    def train_epoch(self) -> Dict[str, float]:
        self.model.train()
        total_loss = 0.0
        total_samples = 0
        correct = 0
        total_grad_norm = 0.0
        num_batches = 0

        for input_a, input_b, target in self.train_loader:
            input_a = input_a.to(self.config.device)
            input_b = input_b.to(self.config.device)
            target = target.to(self.config.device)

            self.optimizer.zero_grad()

            output = self._get_model_output(input_a, input_b)
            loss = F.mse_loss(output, target)
            loss.backward()

            grad_norm = torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                max_norm=self.config.gradient_clipping_max_norm
            )
            total_grad_norm += grad_norm
            num_batches += 1

            self.optimizer.step()

            total_loss += loss.item() * input_a.size(0)
            total_samples += input_a.size(0)

            predictions = torch.all(torch.abs(output - target) < self.config.accuracy_tolerance, dim=1)
            correct += predictions.sum().item()

            self.current_step += 1

            if self.checkpoint_manager.should_checkpoint() and self.trajectory:
                self.checkpoint_manager.save(
                    self.model, self.optimizer, self.trajectory[-1]
                )

        avg_grad_norm = total_grad_norm / num_batches if num_batches > 0 else 0.0

        return {
            'loss': total_loss / total_samples,
            'accuracy': correct / total_samples,
            'gradient_norm': avg_grad_norm
        }

    def evaluate(self) -> Dict[str, float]:
        self.model.eval()
        total_loss = 0.0
        total_samples = 0
        correct = 0

        with torch.no_grad():
            for input_a, input_b, target in self.test_loader:
                input_a = input_a.to(self.config.device)
                input_b = input_b.to(self.config.device)
                target = target.to(self.config.device)

                output = self._get_model_output(input_a, input_b)
                loss = F.mse_loss(output, target)

                total_loss += loss.item() * input_a.size(0)
                total_samples += input_a.size(0)

                predictions = torch.all(torch.abs(output - target) < self.config.accuracy_tolerance, dim=1)
                correct += predictions.sum().item()

        return {
            'loss': total_loss / total_samples,
            'accuracy': correct / total_samples
        }

    def _get_model_output(self, input_a: torch.Tensor, input_b: torch.Tensor) -> torch.Tensor:
        output = self.model(input_a, input_b)
        if hasattr(output, 'last_hidden_state'):
            return output.last_hidden_state.squeeze(1)
        return output[0] if isinstance(output, tuple) else output

    def compute_thermodynamic_state(self, train_metrics: Dict[str, float],
                                    test_metrics: Dict[str, float]) -> ThermodynamicState:
        sample_batch = self._get_sample_batch()

        metrics = self._compute_all_metrics(sample_batch)

        delta = self.model.compute_discretization_margin() if hasattr(self.model, 'compute_discretization_margin') else 0.5
        is_discretized = delta < self.config.discretization_threshold

        kappa = metrics.get('kappa', float('inf'))
        kappa_stable = metrics.get('kappa_stable', False)
        lc = metrics.get('local_complexity', float(self.config.initial_slots))
        lc_transition = metrics.get('lc_transition_detected', False)
        psi = metrics.get('superposition_coefficient', 2.0)
        n_eff = metrics.get('effective_feature_count', float(self.config.initial_slots))
        t_eff = metrics.get('effective_temperature', 1.0)
        entropy = metrics.get('entropy', 0.0)
        heat_capacity = metrics.get('heat_capacity', 0.0)
        h_bar_eff = metrics.get('h_bar_eff', float('inf'))

        weight_norm = self.model.get_weight_norm() if hasattr(self.model, 'get_weight_norm') else 0.0
        gradient_norm = train_metrics.get('gradient_norm', 0.0)

        phase = self.phase_classifier.classify(
            delta=delta,
            kappa=kappa,
            lc=lc,
            t_eff=t_eff,
            test_accuracy=test_metrics['accuracy']
        )

        grokking_detected, grokking_stable = self.grokking_detector.update(
            test_metrics['accuracy'],
            train_metrics['loss']
        )

        return ThermodynamicState(
            epoch=self.current_epoch,
            step=self.current_step,
            timestamp=time.time(),
            train_loss=train_metrics['loss'],
            test_loss=test_metrics['loss'],
            train_accuracy=train_metrics['accuracy'],
            test_accuracy=test_metrics['accuracy'],
            delta=delta,
            is_discretized=is_discretized,
            kappa=kappa,
            kappa_stable=kappa_stable,
            local_complexity=lc,
            lc_transition_detected=lc_transition,
            superposition_coefficient=psi,
            effective_feature_count=n_eff,
            effective_temperature=t_eff,
            entropy=entropy,
            heat_capacity=heat_capacity,
            weight_norm=weight_norm,
            gradient_norm=gradient_norm,
            h_bar_eff=h_bar_eff,
            phase=phase,
            grokking_detected=grokking_detected,
            grokking_stable=grokking_stable
        )

    def _get_sample_batch(self) -> Optional[Tuple[torch.Tensor, ...]]:
        try:
            sample_batch = next(iter(self.test_loader))
            return tuple(t.to(self.config.device) for t in sample_batch)
        except Exception:
            return None

    def _compute_all_metrics(self, sample_batch: Optional[Tuple[torch.Tensor, ...]]) -> Dict[str, float]:
        metrics = {}

        for name, computer in self.metric_computers.items():
            try:
                if name == 'h_bar_eff':
                    t_eff = metrics.get('effective_temperature', 1.0)
                    kappa = metrics.get('kappa', float('inf'))
                    m = computer.compute(self.model, sample_batch, t_eff, kappa)
                else:
                    m = computer.compute(self.model, sample_batch)
                metrics.update(m)
            except Exception:
                pass

        return metrics

    def detect_confirmed_crystallization(self) -> bool:
        if self.current_epoch % self.config.crystallization_check_interval != 0:
            return False

        if len(self.trajectory) < self.config.crystallization_confirmation_epochs:
            return False

        recent_states = self.trajectory[-self.config.crystallization_confirmation_epochs:]

        all_lc_collapsed = all(
            state.local_complexity < self.config.lc_collapse_threshold
            for state in recent_states
        )

        all_kappa_stable = all(
            state.kappa < self.config.kappa_stability_threshold
            for state in recent_states
        )

        all_high_accuracy = all(
            state.test_accuracy > self.config.grokking_accuracy_threshold
            for state in recent_states
        )

        all_delta_low = all(
            state.delta < self.config.delta_crystal_threshold
            for state in recent_states
        )

        return all_lc_collapsed and all_kappa_stable and all_high_accuracy and all_delta_low

    def train(self, num_epochs: Optional[int] = None) -> List[ThermodynamicState]:
        if num_epochs is None:
            num_epochs = self.config.num_epochs

        self._print_training_header(num_epochs)

        pbar = tqdm(range(num_epochs), desc="Training")

        consecutive_crystal_epochs = 0
        last_phase = "unknown"

        for epoch in pbar:
            self.current_epoch = epoch

            train_metrics = self.train_epoch()
            test_metrics = self.evaluate()

            state = self.compute_thermodynamic_state(train_metrics, test_metrics)
            self.trajectory.append(state)

            consecutive_crystal_epochs = self._update_phase_tracking(state, last_phase, consecutive_crystal_epochs)
            last_phase = state.phase

            self._update_progress_bar(pbar, state, consecutive_crystal_epochs)

            if state.grokking_detected and state.grokking_stable:
                self._handle_grokking_event(epoch, state)

            if self.detect_confirmed_crystallization():
                self._handle_crystallization_event(epoch, state)

            if self.checkpoint_manager.should_checkpoint():
                self.checkpoint_manager.save(self.model, self.optimizer, state)

            if consecutive_crystal_epochs >= self.config.crystallization_confirmation_epochs:
                print(f"\n*** STABLE CRYSTALLIZATION ACHIEVED at epoch {epoch} ***")
                print(f"System remained in crystal phase for {consecutive_crystal_epochs} consecutive epochs")
                break

        if self.trajectory:
            self.checkpoint_manager.save(
                self.model, self.optimizer, self.trajectory[-1], checkpoint_type="final"
            )

        return self.trajectory

    def _print_training_header(self, num_epochs: int) -> None:
        print(f"\n{'='*80}")
        print("PHASE 1: EXTENDED TRAINING")
        print(f"{'='*80}")
        print(f"Epochs: {num_epochs}")
        print(f"Batch size: {self.config.batch_size}")
        print(f"Learning rate: {self.config.learning_rate}")
        print(f"Weight decay: {self.config.weight_decay}")
        print(f"Target: Laderman rank {self.config.target_rank} for {self.config.matrix_size}x{self.config.matrix_size}")
        if self.config.grokking_detection_enabled:
            print(f"Grokking detection: ENABLED (window={self.config.grokking_window_size}, threshold={self.config.grokking_accuracy_threshold})")
        print(f"Crystallization check interval: every {self.config.crystallization_check_interval} epochs")
        print(f"Crystallization confirmation: {self.config.crystallization_confirmation_epochs} consecutive stable epochs")
        print(f"  LC collapse threshold: {self.config.lc_collapse_threshold}")
        print(f"  Kappa stability threshold: {self.config.kappa_stability_threshold}")
        print(f"  Delta crystal threshold: {self.config.delta_crystal_threshold}")

    def _update_phase_tracking(self, state: ThermodynamicState, last_phase: str,
                               consecutive_crystal_epochs: int) -> int:
        if state.phase == "crystal":
            consecutive_crystal_epochs += 1
        else:
            consecutive_crystal_epochs = 0

        if state.phase != last_phase:
            print(f"\n*** PHASE TRANSITION at epoch {state.epoch}: {last_phase} -> {state.phase} ***")

        return consecutive_crystal_epochs

    def _update_progress_bar(self, pbar, state: ThermodynamicState, consecutive_crystal_epochs: int) -> None:
        kappa_str = f"{state.kappa:.3f}" if state.kappa < 1000 else "inf"
        t_eff_str = f"{state.effective_temperature:.2e}"
        h_bar_str = f"{state.h_bar_eff:.2e}" if state.h_bar_eff < 1e10 else "inf"

        pbar.set_postfix({
            'train_loss': f"{state.train_loss:.2e}",
            'test_loss': f"{state.test_loss:.2e}",
            'test_acc': f"{state.test_accuracy:.3f}",
            'kappa': kappa_str,
            'delta': f"{state.delta:.3f}",
            'LC': f"{state.local_complexity:.1f}",
            'psi': f"{state.superposition_coefficient:.3f}",
            'T_eff': t_eff_str,
            'h_bar': h_bar_str,
            'S': f"{state.entropy:.2f}",
            'C_v': f"{state.heat_capacity:.2e}",
            '|W|': f"{state.weight_norm:.2f}",
            '|grad|': f"{state.gradient_norm:.2e}",
            'phase': state.phase[:4],
            'c_ep': consecutive_crystal_epochs
        })

    def _handle_grokking_event(self, epoch: int, state: ThermodynamicState) -> None:
        print(f"\n{'='*80}")
        print(f"*** STABLE GROKKING DETECTED at epoch {epoch} ***")
        print(f"Test accuracy: {state.test_accuracy:.4f}")
        print(f"Train loss: {state.train_loss:.2e}")
        print(f"Kappa: {state.kappa:.6f}")
        print(f"Delta: {state.delta:.6f}")
        print(f"Phase: {state.phase}")
        print(f"{'='*80}")
        self.checkpoint_manager.save(
            self.model, self.optimizer, state, checkpoint_type="grokking"
        )

    def _handle_crystallization_event(self, epoch: int, state: ThermodynamicState) -> None:
        print(f"\n{'='*80}")
        print(f"*** CONFIRMED CRYSTALLIZATION at epoch {epoch} ***")
        print(f"LC collapsed: {state.local_complexity:.4f} < {self.config.lc_collapse_threshold}")
        print(f"Kappa stable: {state.kappa:.4f} < {self.config.kappa_stability_threshold}")
        print(f"Delta discrete: {state.delta:.4f} < {self.config.delta_crystal_threshold}")
        print(f"T_eff: {state.effective_temperature:.2e}")
        print(f"{'='*80}")
        self.checkpoint_manager.save(
            self.model, self.optimizer, state, checkpoint_type="crystallization"
        )

    def phase2_pruning_and_discretization(self) -> bool:
        print(f"\n{'='*80}")
        print("PHASE 2: PRUNING AND DISCRETIZATION")
        print(f"{'='*80}")

        pruner = MagnitudePruning()
        self.model = pruner.prune(self.model, self.config.pruning_target)

        print(f"\nModel pruned to {self.config.pruning_target} slots")

        success = False
        if hasattr(self.model, 'discretize'):
            success = self.model.discretize(self.config.discretization_threshold)

            if success:
                print("Discretization successful!")
                delta = self.model.compute_discretization_margin()
                print(f"Final delta: {delta:.6f}")
            else:
                print("Discretization failed - weights not close enough to integers")

        test_metrics = self.evaluate()
        print(f"Post-discretization test accuracy: {test_metrics['accuracy']:.4f}")

        return success and test_metrics['accuracy'] > 0.95


def run_laderman_experiment(config: Optional[LadermanConfig] = None) -> Tuple[bool, List[ThermodynamicState]]:
    """
    Run complete Laderman crystallization experiment.
    
    Returns:
        Tuple of (success, trajectory) where success indicates whether
        discretization was achieved and trajectory contains all thermodynamic states.
    """
    if config is None:
        config = LadermanConfig()

    print("\n" + "="*80)
    print("LADERMAN ALGORITHM CRYSTALLIZATION IN TRANSFORMERS")
    print("="*80)
    print(f"Experiment: {config.experiment_name}")
    print(f"Matrix size: {config.matrix_size}x{config.matrix_size}")
    print(f"Target rank: {config.target_rank} (Laderman decomposition)")
    print(f"Initial slots: {config.initial_slots}")

    torch.manual_seed(config.seed)
    np.random.seed(config.seed)

    print("\nPreparing datasets...")
    train_dataset = MatrixMultiplicationDataset(
        matrix_size=config.matrix_size,
        num_samples=config.train_samples,
        seed=config.seed
    )
    test_dataset = MatrixMultiplicationDataset(
        matrix_size=config.matrix_size,
        num_samples=config.test_samples,
        seed=config.seed + 1000
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers
    )

    print(f"Train samples: {len(train_dataset)}, Test samples: {len(test_dataset)}")

    print("\nInitializing Bilinear Transformer Model...")
    model = BilinearTransformerModel(config)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,}")
    print(f"Hidden size: {config.hidden_size}")
    print(f"Attention heads: {config.num_attention_heads}")
    print(f"Transformer layers: {config.num_hidden_layers}")

    checkpoint_manager = FileCheckpointManager(config)

    trainer = CrystallizationTrainer(
        config=config,
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        checkpoint_manager=checkpoint_manager
    )

    trajectory = trainer.train()

    discretization_success = trainer.phase2_pruning_and_discretization()

    print("\n" + "="*80)
    print("EXPERIMENT SUMMARY")
    print("="*80)
    if trajectory:
        final_state = trajectory[-1]
        print(f"Total epochs trained: {len(trajectory)}")
        print(f"Final phase: {final_state.phase}")
        print(f"Final kappa: {final_state.kappa:.6f}")
        print(f"Final delta: {final_state.delta:.6f}")
        print(f"Final test accuracy: {final_state.test_accuracy:.4f}")
        print(f"Final T_eff: {final_state.effective_temperature:.2e}")
        print(f"Final h_bar_eff: {final_state.h_bar_eff:.2e}")
        print(f"Discretization success: {discretization_success}")

        if final_state.grokking_detected:
            print(f"\nGrokking was detected during training")

    print(f"\nCheckpoint saved to: {checkpoint_manager.latest_path}")

    return discretization_success, trajectory


if __name__ == '__main__':
    config = LadermanConfig(
        batch_size=32,
        learning_rate=1e-3,
        weight_decay=1e-4,
        num_epochs=5000,
        initial_slots=27,
        target_rank=23,
        matrix_size=3,
        checkpoint_interval_minutes=5.0
    )

    success, trajectory = run_laderman_experiment(config)

    print(f"\nExperiment completed. Success: {success}")
