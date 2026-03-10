#!/usr/bin/env python3
"""
Laderman Algorithm Crystallization in Transformers - FIXED VERSION
Thermodynamic Algorithmic Crystallization Framework

FIXES:
- Reduced memory usage in gradient covariance computation
- Fixed pruning to properly resize model parameters
- Added proper tensor resizing

Author: grisun0
License: AGPL v3
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np
import json
import os
import time
import math
import warnings
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from pathlib import Path
from collections import defaultdict

# Progress tracking
try:
    from tqdm.auto import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        return iterable


# =============================================================================
# CONFIGURATION (Single Source of Truth)
# =============================================================================

@dataclass(frozen=True)
class LadermanConfig:
    """Complete configuration for Laderman crystallization experiment."""

    # Experiment
    experiment_name: str = "laderman_crystallization"
    seed: int = 42

    # Matrix dimensions
    matrix_size: int = 3
    target_rank: int = 23
    initial_slots: int = 27

    # Transformer Architecture - ALL CONFIGURABLE
    hidden_size: int = 128
    num_hidden_layers: int = 2
    num_attention_heads: int = 4
    intermediate_size: int = 256
    hidden_dropout_prob: float = 0.0
    attention_probs_dropout_prob: float = 0.0
    max_position_embeddings: int = 512
    initializer_range: float = 0.02
    layer_norm_eps: float = 1e-12

    # Training Protocol
    batch_size: int = 32
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    num_epochs: int = 100000
    warmup_steps: int = 100

    # Phase 2
    pruning_target: int = 23
    discretization_threshold: float = 0.1

    # Metrics
    compute_gradient_covariance: bool = True
    compute_local_complexity: bool = True
    compute_superposition: bool = True
    compute_temperature: bool = True

    # Checkpointing every 5 minutes
    checkpoint_interval_minutes: int = 5
    checkpoint_dir: str = "./laderman_checkpoints"
    keep_last_n_checkpoints: int = 3
    
    # Grokking detection
    grokking_detection_enabled: bool = True
    grokking_window_size: int = 100
    grokking_accuracy_threshold: float = 0.99
    grokking_past_accuracy_threshold: float = 0.5

    # Verification
    verify_expansion: bool = True
    test_sizes: Tuple[int, ...] = (3, 6, 12, 24)

    # Hardware
    device: str = "cuda"
    num_workers: int = 0

    def __post_init__(self):
        if not (8 <= self.batch_size <= 512):
            raise ValueError(f"Batch size {self.batch_size} outside range [8, 512]")
        if self.grokking_window_size < 10:
            raise ValueError(f"Grokking window size must be at least 10, got {self.grokking_window_size}")
        Path(self.checkpoint_dir).mkdir(parents=True, exist_ok=True)
        object.__setattr__(self, 'device', torch.device(self.device))

    def to_dict(self):
        d = asdict(self)
        d['device'] = str(d['device'])
        return d


# =============================================================================
# THERMODYNAMIC STATE (All metrics from Strassen paper)
# =============================================================================

@dataclass
class ThermodynamicState:
    """Complete thermodynamic state tracking."""

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
    phase: str = "unknown"
    grokking_detected: bool = False

    def to_dict(self):
        return {
            'epoch': self.epoch, 'step': self.step, 'timestamp': self.timestamp,
            'train_loss': self.train_loss, 'test_loss': self.test_loss,
            'train_accuracy': self.train_accuracy, 'test_accuracy': self.test_accuracy,
            'delta': self.delta, 'is_discretized': self.is_discretized,
            'kappa': self.kappa, 'kappa_stable': self.kappa_stable,
            'local_complexity': self.local_complexity,
            'lc_transition_detected': self.lc_transition_detected,
            'superposition_coefficient': self.superposition_coefficient,
            'effective_feature_count': self.effective_feature_count,
            'effective_temperature': self.effective_temperature,
            'entropy': self.entropy, 'heat_capacity': self.heat_capacity,
            'weight_norm': self.weight_norm, 'gradient_norm': self.gradient_norm,
            'phase': self.phase, 'grokking_detected': self.grokking_detected
        }

# =============================================================================
# DATASET
# =============================================================================

class MatrixMultiplicationDataset(Dataset):
    """Dataset for matrix multiplication."""

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


# =============================================================================
# BILINEAR TRANSFORMER MODEL (Using PyTorch Transformer)
# =============================================================================

class BilinearTransformerModel(nn.Module):
    """
    Transformer model for bilinear matrix multiplication.
    Uses PyTorch's native TransformerEncoder with multi-head attention.
    """

    def __init__(self, config: LadermanConfig):
        super().__init__()
        self.config = config

        n = config.matrix_size
        n2 = n * n

        # Input projections
        self.input_proj_a = nn.Linear(n2, config.hidden_size)
        self.input_proj_b = nn.Linear(n2, config.hidden_size)

        # Positional embeddings
        self.position_embeddings = nn.Embedding(
            config.max_position_embeddings, 
            config.hidden_size
        )

        # TRANSFORMER ENCODER using PyTorch native implementation
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

        # Bilinear tensors (U, V, W) for Laderman structure
        self.U = nn.Parameter(torch.randn(config.initial_slots, n2) * config.initializer_range)
        self.V = nn.Parameter(torch.randn(config.initial_slots, n2) * config.initializer_range)
        self.W = nn.Parameter(torch.randn(n2, config.initial_slots) * config.initializer_range)

        # Output projection
        self.output_proj = nn.Linear(config.hidden_size, n2)

        # Initialize
        self._init_weights()

    def _init_weights(self):
        """BERT-style initialization."""
        for module in self.modules():
            if isinstance(module, nn.Linear):
                module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)
                if module.bias is not None:
                    module.bias.data.zero_()
            elif isinstance(module, nn.Embedding):
                module.weight.data.normal_(mean=0.0, std=self.config.initializer_range)

    def forward(self, input_a, input_b, output_attentions=False, return_dict=True):
        batch_size = input_a.size(0)

        # Project inputs
        emb_a = self.input_proj_a(input_a)
        emb_b = self.input_proj_b(input_b)

        # Add positional embeddings
        positions = torch.arange(2, device=input_a.device).unsqueeze(0).expand(batch_size, -1)
        pos_emb = self.position_embeddings(positions)

        # Stack as sequence [A, B]
        sequence = torch.stack([emb_a, emb_b], dim=1) + pos_emb

        # Pass through TRANSFORMER ENCODER
        hidden_states = self.encoder(sequence)

        # Pool
        pooled = hidden_states.mean(dim=1)

        # Bilinear computation: C = W @ ((U @ a) * (V @ b))
        m = (input_a @ self.U.t()) * (input_b @ self.V.t())
        bilinear_out = m @ self.W.t()

        # Combine
        combined = self.output_proj(pooled) + bilinear_out

        if return_dict:
            return type('Output', (), {
                'last_hidden_state': combined.unsqueeze(1),
                'attentions': None
            })()
        return (combined,)

    def get_bilinear_tensors(self):
        return self.U.detach().clone(), self.V.detach().clone(), self.W.detach().clone()

    def set_bilinear_tensors(self, u, v, w):
        """Set bilinear tensors with proper size handling."""
        with torch.no_grad():
            # Resize parameters if needed
            if u.size(0) != self.U.size(0):
                self.U = nn.Parameter(torch.empty_like(u))
                self.V = nn.Parameter(torch.empty_like(v))
                self.W = nn.Parameter(torch.empty_like(w))

            self.U.copy_(u)
            self.V.copy_(v)
            self.W.copy_(w)

    def compute_discretization_margin(self):
        all_params = torch.cat([self.U.view(-1), self.V.view(-1), self.W.view(-1)])
        theta_rounded = torch.round(all_params).clamp(-1, 1)
        return torch.norm(all_params - theta_rounded, p=float('inf')).item()

    def discretize(self, threshold=0.1):
        if self.compute_discretization_margin() > threshold:
            return False
        with torch.no_grad():
            for param in [self.U, self.V, self.W]:
                param.copy_(torch.round(param).clamp(-1, 1))
        return True

    def get_weight_norm(self):
        return sum(p.data.norm(2).item() ** 2 for p in self.parameters()) ** 0.5

    def compute_gradient_norm(self):
        return sum(p.grad.data.norm(2).item() ** 2 for p in self.parameters() if p.grad is not None) ** 0.5


# =============================================================================
# METRIC COMPUTERS (FIXED FOR MEMORY)
# =============================================================================

class GradientCovarianceComputer:
    """
    Compute kappa: condition number of gradient covariance matrix.
    FIXED: Reduced memory usage by sampling fewer gradients and using approximation.
    """

    def __init__(self, num_samples: int = 10):  # Reduced from 100 to 10
        self.num_samples = num_samples

    def compute(self, model, batch=None):
        if batch is None:
            return {'kappa': float('inf'), 'kappa_stable': False}

        input_a, input_b, target = batch
        gradients = []

        # Sample only a few gradients to save memory
        max_samples = min(self.num_samples, input_a.size(0), 10)

        for i in range(max_samples):
            model.zero_grad()

            output = model(input_a[i:i+1], input_b[i:i+1])
            if hasattr(output, 'last_hidden_state'):
                output = output.last_hidden_state.squeeze(1)
            else:
                output = output[0] if isinstance(output, tuple) else output

            loss = F.mse_loss(output, target[i:i+1])
            loss.backward()

            # Collect only U, V, W gradients (not all parameters) to save memory
            grad_list = []
            for name, param in model.named_parameters():
                if param.grad is not None and name in ['U', 'V', 'W']:
                    grad_list.append(param.grad.view(-1))

            if grad_list:
                grad_vector = torch.cat(grad_list)
                gradients.append(grad_vector)

        if len(gradients) < 2:
            return {'kappa': float('inf'), 'kappa_stable': False}

        # Compute covariance with memory-efficient approach
        grad_matrix = torch.stack(gradients)

        # Use SVD instead of full covariance matrix for memory efficiency
        try:
            # Center the gradients
            grad_mean = grad_matrix.mean(dim=0, keepdim=True)
            grad_centered = grad_matrix - grad_mean

            # Compute SVD of centered gradients
            u, s, v = torch.svd(grad_centered)

            # Condition number from singular values
            s_nonzero = s[s > 1e-6]
            if len(s_nonzero) == 0:
                kappa = float('inf')
            else:
                kappa = (s_nonzero.max() / s_nonzero.min()).item()
        except Exception as e:
            kappa = float('inf')

        return {'kappa': kappa, 'kappa_stable': abs(kappa - 1.0) < 0.001}


class LocalComplexityComputer:
    """Compute Local Complexity (LC)."""

    def compute(self, model, batch=None):
        if hasattr(model, 'get_bilinear_tensors'):
            u, v, w = model.get_bilinear_tensors()
            try:
                # Use SVD to compute effective rank
                u_s = torch.linalg.svdvals(u)
                # Effective rank: number of singular values above threshold
                threshold = 0.01 * u_s.max()
                lc = (u_s > threshold).sum().item()
            except:
                lc = float(u.size(0))
        else:
            lc = 100.0

        return {'local_complexity': lc, 'lc_transition_detected': lc < 1.0}


class SuperpositionComputer:
    """Compute superposition coefficient psi."""

    def compute(self, model, batch=None):
        if hasattr(model, 'get_bilinear_tensors'):
            u, v, w = model.get_bilinear_tensors()
            u_norm = F.normalize(u, dim=1)
            overlap = torch.mm(u_norm, u_norm.t())
            mask = ~torch.eye(overlap.size(0), dtype=torch.bool)
            psi = overlap[mask].abs().mean().item() + 1.0

            singular_values = torch.linalg.svdvals(u)
            sv_squared = singular_values ** 2
            f_eff = (sv_squared.sum() ** 2 / (sv_squared ** 2).sum()).item() if sv_squared.sum() > 0 else float(u.size(0))
        else:
            psi = 2.0
            f_eff = 27.0

        return {'superposition_coefficient': psi, 'effective_feature_count': f_eff}


class TemperatureComputer:
    """Compute effective temperature T_eff."""

    def __init__(self, num_samples: int = 10):  # Reduced from 50 to 10
        self.num_samples = num_samples

    def compute(self, model, batch=None):
        if batch is None:
            return {'effective_temperature': 1.0, 'entropy': 0.0, 'heat_capacity': 0.0}

        input_a, input_b, target = batch
        grad_norms = []

        max_samples = min(self.num_samples, input_a.size(0), 10)

        for i in range(max_samples):
            model.zero_grad()
            output = model(input_a[i:i+1], input_b[i:i+1])
            if hasattr(output, 'last_hidden_state'):
                output = output.last_hidden_state.squeeze(1)
            else:
                output = output[0] if isinstance(output, tuple) else output

            loss = F.mse_loss(output, target[i:i+1])
            loss.backward()

            # Only compute norm of U, V, W gradients
            grad_norm = 0.0
            for name, param in model.named_parameters():
                if param.grad is not None and name in ['U', 'V', 'W']:
                    grad_norm += param.grad.norm(2).item() ** 2
            grad_norms.append(grad_norm ** 0.5)

        if len(grad_norms) == 0:
            return {'effective_temperature': 1.0, 'entropy': 0.0, 'heat_capacity': 0.0}

        grad_norms = torch.tensor(grad_norms)
        t_eff = grad_norms.var().item()

        # Compute entropy
        hist = torch.histc(grad_norms, bins=min(20, len(grad_norms)))
        hist = hist / hist.sum()
        entropy = -(hist * torch.log(hist + 1e-10)).sum().item()

        cv = grad_norms.var().item() / (t_eff + 1e-10) if t_eff > 0 else 0.0

        return {'effective_temperature': t_eff, 'entropy': entropy, 'heat_capacity': cv}


# =============================================================================
# PRUNING (FIXED)
# =============================================================================

class MagnitudePruning:
    """
    Prune slots based on L2 norm.
    FIXED: Properly handles tensor resizing.
    """

    def prune(self, model: nn.Module, target_slots: int) -> nn.Module:
        if not hasattr(model, 'get_bilinear_tensors'):
            return model

        u, v, w = model.get_bilinear_tensors()
        current_slots = u.size(0)

        if current_slots <= target_slots:
            print(f"No pruning needed: {current_slots} slots <= {target_slots} target")
            return model

        print(f"Pruning from {current_slots} to {target_slots} slots...")

        # Compute importance as L2 norm of each slot
        importance = torch.zeros(current_slots)
        for i in range(current_slots):
            importance[i] = u[i].norm(2) + v[i].norm(2) + w[:, i].norm(2)

        # Keep top-k
        _, keep_indices = torch.topk(importance, target_slots)
        keep_indices = keep_indices.sort()[0]

        print(f"Keeping indices: {keep_indices.tolist()}")

        # Create new tensors
        u_new = u[keep_indices]
        v_new = v[keep_indices]
        w_new = w[:, keep_indices]

        # Update model - this will recreate parameters with correct size
        model.set_bilinear_tensors(u_new, v_new, w_new)

        # Verify
        u_check, v_check, w_check = model.get_bilinear_tensors()
        assert u_check.size(0) == target_slots, f"U size mismatch: {u_check.size(0)} != {target_slots}"
        assert v_check.size(0) == target_slots, f"V size mismatch: {v_check.size(0)} != {target_slots}"
        assert w_check.size(1) == target_slots, f"W size mismatch: {w_check.size(1)} != {target_slots}"

        print(f"Pruning complete. New sizes: U{u_check.shape}, V{v_check.shape}, W{w_check.shape}")

        return model


# =============================================================================
# CHECKPOINT MANAGER
# =============================================================================

class FileCheckpointManager:
    """Checkpoint management with 5-minute intervals."""

    def __init__(self, config: LadermanConfig):
        self.config = config
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.checkpoints: List[Path] = []
        self.grokking_checkpoints: List[Path] = []
        self.last_checkpoint_time = time.time()

    def should_checkpoint(self) -> bool:
        return (time.time() - self.last_checkpoint_time) > (self.config.checkpoint_interval_minutes * 60)

    def save(self, model: nn.Module, optimizer: torch.optim.Optimizer, 
             state: ThermodynamicState, path: Optional[str] = None,
             checkpoint_type: str = "regular") -> str:

        if path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            if checkpoint_type == "grokking":
                path = self.checkpoint_dir / f"grokking_epoch{state.epoch}_{timestamp}.pt"
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

        latest_path = self.checkpoint_dir / "latest.pt"
        torch.save(checkpoint, latest_path)

        if checkpoint_type == "grokking":
            self.grokking_checkpoints.append(path)
            print(f"\n*** GROKKING CHECKPOINT SAVED: {path.name} ***")
        else:
            self.checkpoints.append(path)
            self._cleanup()
            self.last_checkpoint_time = time.time()

        return str(path)

    def _cleanup(self):
        """Remove old regular checkpoints but keep all grokking checkpoints."""
        if len(self.checkpoints) > self.config.keep_last_n_checkpoints:
            to_remove = self.checkpoints[:-self.config.keep_last_n_checkpoints]
            for cp in to_remove:
                if cp.exists() and cp.name != 'latest.pt':
                    cp.unlink()
            self.checkpoints = self.checkpoints[-self.config.keep_last_n_checkpoints:]

# =============================================================================
# TRAINING ENGINE
# =============================================================================

class CrystallizationTrainer:
    """Two-phase training protocol from Strassen paper."""

    def __init__(self, config: LadermanConfig, model: nn.Module,
                 train_loader: DataLoader, test_loader: DataLoader,
                 checkpoint_manager: FileCheckpointManager):
        self.config = config
        self.model = model.to(config.device)
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.checkpoint_manager = checkpoint_manager

        # AdamW optimizer
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )

        # All metric computers (with reduced memory usage)
        self.metric_computers = [
            GradientCovarianceComputer(num_samples=10),
            LocalComplexityComputer(),
            SuperpositionComputer(),
            TemperatureComputer(num_samples=10)
        ]

        self.current_epoch = 0
        self.current_step = 0
        self.trajectory: List[ThermodynamicState] = []

    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch with all metrics."""
        self.model.train()
        total_loss = 0.0
        total_samples = 0
        correct = 0

        for batch_idx, (input_a, input_b, target) in enumerate(self.train_loader):
            input_a = input_a.to(self.config.device)
            input_b = input_b.to(self.config.device)
            target = target.to(self.config.device)

            self.optimizer.zero_grad()

            # Forward through TRANSFORMER
            output = self.model(input_a, input_b)
            if hasattr(output, 'last_hidden_state'):
                output = output.last_hidden_state.squeeze(1)
            else:
                output = output[0] if isinstance(output, tuple) else output

            # Loss
            loss = F.mse_loss(output, target)
            loss.backward()
            self.optimizer.step()

            # Metrics
            total_loss += loss.item() * input_a.size(0)
            total_samples += input_a.size(0)

            # Accuracy (within tolerance)
            pred_correct = torch.all(torch.abs(output - target) < 0.01, dim=1)
            correct += pred_correct.sum().item()

            self.current_step += 1

            # Periodic checkpointing every 5 minutes
            if self.checkpoint_manager.should_checkpoint():
                if self.trajectory:
                    self.checkpoint_manager.save(
                        self.model, self.optimizer, self.trajectory[-1]
                    )

        return {
            'loss': total_loss / total_samples,
            'accuracy': correct / total_samples
        }

    def evaluate(self) -> Dict[str, float]:
        """Evaluate on test set."""
        self.model.eval()
        total_loss = 0.0
        total_samples = 0
        correct = 0

        with torch.no_grad():
            for input_a, input_b, target in self.test_loader:
                input_a = input_a.to(self.config.device)
                input_b = input_b.to(self.config.device)
                target = target.to(self.config.device)

                output = self.model(input_a, input_b)
                if hasattr(output, 'last_hidden_state'):
                    output = output.last_hidden_state.squeeze(1)
                else:
                    output = output[0] if isinstance(output, tuple) else output

                loss = F.mse_loss(output, target)

                total_loss += loss.item() * input_a.size(0)
                total_samples += input_a.size(0)

                pred_correct = torch.all(torch.abs(output - target) < 0.01, dim=1)
                correct += pred_correct.sum().item()

        return {
            'loss': total_loss / total_samples,
            'accuracy': correct / total_samples
        }

    def compute_thermodynamic_state(self, train_metrics: Dict[str, float],
                                    test_metrics: Dict[str, float]) -> ThermodynamicState:
        """Compute complete thermodynamic state with ALL metrics."""

        sample_batch = None
        try:
            sample_batch = next(iter(self.test_loader))
            sample_batch = tuple(t.to(self.config.device) for t in sample_batch)
        except:
            pass

        metrics = {}
        for computer in self.metric_computers:
            try:
                m = computer.compute(self.model, sample_batch)
                metrics.update(m)
            except Exception as e:
                pass

        delta = self.model.compute_discretization_margin() if hasattr(self.model, 'compute_discretization_margin') else 0.5
        is_discretized = delta < self.config.discretization_threshold

        weight_norm = self.model.get_weight_norm() if hasattr(self.model, 'get_weight_norm') else 0.0
        grad_norm = self.model.compute_gradient_norm() if hasattr(self.model, 'compute_gradient_norm') else 0.0

        kappa = metrics.get('kappa', float('inf'))
        kappa_stable = metrics.get('kappa_stable', False)

        if is_discretized and kappa_stable:
            phase = "crystal"
        elif delta < 0.2:
            phase = "polycrystal"
        else:
            phase = "glass"

        grokking_detected = self._detect_grokking(test_metrics['accuracy'])

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
            local_complexity=metrics.get('local_complexity', 100.0),
            lc_transition_detected=metrics.get('lc_transition_detected', False),
            superposition_coefficient=metrics.get('superposition_coefficient', 2.0),
            effective_feature_count=metrics.get('effective_feature_count', 27.0),
            effective_temperature=metrics.get('effective_temperature', 1.0),
            entropy=metrics.get('entropy', 0.0),
            heat_capacity=metrics.get('heat_capacity', 0.0),
            weight_norm=weight_norm,
            gradient_norm=grad_norm,
            phase=phase,
            grokking_detected=grokking_detected
        )

    def _detect_grokking(self, current_test_accuracy: float) -> bool:
        """
        Detect grokking: sudden jump in test accuracy.
        Returns True if grokking is detected at current epoch.
        """
        if not self.config.grokking_detection_enabled:
            return False
        
        if len(self.trajectory) < self.config.grokking_window_size:
            return False
        
        past_state = self.trajectory[-self.config.grokking_window_size]
        past_accuracy = past_state.test_accuracy
        
        grokking_occurred = (
            current_test_accuracy >= self.config.grokking_accuracy_threshold and
            past_accuracy <= self.config.grokking_past_accuracy_threshold
        )
        
        return grokking_occurred

    def train(self, num_epochs: Optional[int] = None) -> List[ThermodynamicState]:
        """
        Phase 1: Extended training with thermodynamic monitoring.
        """
        if num_epochs is None:
            num_epochs = self.config.num_epochs

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

        pbar = tqdm(range(num_epochs), desc="Training")

        for epoch in pbar:
            self.current_epoch = epoch

            train_metrics = self.train_epoch()
            test_metrics = self.evaluate()

            state = self.compute_thermodynamic_state(train_metrics, test_metrics)
            self.trajectory.append(state)

            pbar.set_postfix({
                'train_loss': f"{state.train_loss:.2e}",
                'test_loss': f"{state.test_loss:.2e}",
                'test_acc': f"{state.test_accuracy:.3f}",
                'kappa': f"{state.kappa:.3f}" if state.kappa < 1000 else "inf",
                'delta': f"{state.delta:.3f}",
                'LC': f"{state.local_complexity:.1f}",
                'psi': f"{state.superposition_coefficient:.3f}",
                'T_eff': f"{state.effective_temperature:.2e}",
                'S': f"{state.entropy:.2f}",
                'C_v': f"{state.heat_capacity:.2e}",
                '|W|': f"{state.weight_norm:.2f}",
                '|grad|': f"{state.gradient_norm:.2e}",
                'phase': state.phase
            })

            if state.grokking_detected:
                print(f"\n{'='*80}")
                print(f"*** GROKKING DETECTED at epoch {epoch} ***")
                print(f"Test accuracy jumped from {self.trajectory[-self.config.grokking_window_size].test_accuracy:.4f} to {state.test_accuracy:.4f}")
                print(f"{'='*80}")
                self.checkpoint_manager.save(
                    self.model, self.optimizer, state, checkpoint_type="grokking"
                )

            if self.checkpoint_manager.should_checkpoint():
                self.checkpoint_manager.save(
                    self.model, self.optimizer, state
                )

            if state.phase == "crystal":
                print(f"\n*** CRYSTALLIZATION ACHIEVED at epoch {epoch} ***")
                break

        if self.trajectory:
            self.checkpoint_manager.save(
                self.model, self.optimizer, self.trajectory[-1]
            )

        return self.trajectory
        
    def phase2_pruning_and_discretization(self) -> bool:
        """
        Phase 2: Prune to target rank and discretize.
        """
        print(f"\n{'='*80}")
        print("PHASE 2: PRUNING AND DISCRETIZATION")
        print(f"{'='*80}")

        # Pruning
        pruner = MagnitudePruning()
        self.model = pruner.prune(self.model, self.config.pruning_target)

        print(f"\nModel pruned to {self.config.pruning_target} slots")

        # Discretization
        success = False
        if hasattr(self.model, 'discretize'):
            success = self.model.discretize(self.config.discretization_threshold)

            if success:
                print("Discretization successful!")
                delta = self.model.compute_discretization_margin()
                print(f"Final delta: {delta:.6f}")
            else:
                print("Discretization failed - weights not close enough to integers")

        # Evaluate after phase 2
        test_metrics = self.evaluate()
        print(f"Post-discretization test accuracy: {test_metrics['accuracy']:.4f}")

        return success and test_metrics['accuracy'] > 0.95


# =============================================================================
# MAIN RUNNER
# =============================================================================

def run_laderman_experiment(config: Optional[LadermanConfig] = None):
    """Run complete Laderman crystallization experiment."""

    if config is None:
        config = LadermanConfig()

    print("\n" + "="*80)
    print("LADERMAN ALGORITHM CRYSTALLIZATION IN TRANSFORMERS")
    print("="*80)

    # Set seed
    torch.manual_seed(config.seed)
    np.random.seed(config.seed)

    # Create datasets
    print("\nPreparing datasets...")
    train_dataset = MatrixMultiplicationDataset(
        matrix_size=config.matrix_size,
        num_samples=10000,
        seed=config.seed
    )
    test_dataset = MatrixMultiplicationDataset(
        matrix_size=config.matrix_size,
        num_samples=2000,
        seed=config.seed + 1
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

    # Create model (TRANSFORMER-based)
    print("\nInitializing Transformer model...")
    model = BilinearTransformerModel(config)

    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"  Total parameters: {total_params:,}")
    print(f"  Trainable parameters: {trainable_params:,}")
    print(f"  Transformer layers: {config.num_hidden_layers}")
    print(f"  Attention heads: {config.num_attention_heads}")

    # Create checkpoint manager
    checkpoint_manager = FileCheckpointManager(config)

    # Create trainer
    trainer = CrystallizationTrainer(
        config=config,
        model=model,
        train_loader=train_loader,
        test_loader=test_loader,
        checkpoint_manager=checkpoint_manager
    )

    # Phase 1: Training
    print("\n" + "="*80)
    print("PHASE 1: EXTENDED TRAINING")
    print("="*80)
    trajectory = trainer.train()

    # Phase 2: Pruning and Discretization
    print("\n" + "="*80)
    print("PHASE 2: PRUNING AND DISCRETIZATION")
    print("="*80)
    discretization_success = trainer.phase2_pruning_and_discretization()

    # Summary
    print("\n" + "="*80)
    print("EXPERIMENT SUMMARY")
    print("="*80)
    print(f"Total epochs trained: {len(trajectory)}")
    if trajectory:
        final_state = trajectory[-1]
        print(f"Final phase: {final_state.phase}")
        print(f"Final kappa: {final_state.kappa:.6f}")
        print(f"Final delta: {final_state.delta:.6f}")
        print(f"Final test accuracy: {final_state.test_accuracy:.4f}")
    print(f"Discretization success: {discretization_success}")

    return trajectory


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    # Configuration - ALL PARAMETERS EXPLICIT
    config = LadermanConfig(
        experiment_name="laderman_3x3_rank23",
        matrix_size=3,
        target_rank=23,
        initial_slots=27,

        # Transformer architecture - CONFIGURABLE
        hidden_size=64,  # Reduced for CPU
        num_hidden_layers=2,
        num_attention_heads=4,
        intermediate_size=128,

        # Training - from Strassen paper
        batch_size=32,
        learning_rate=1e-3,
        weight_decay=1e-4,
        num_epochs=10000,  # Use 3000 for full experiment

        # Checkpointing every 5 minutes
        checkpoint_interval_minutes=5,
        checkpoint_dir="./laderman_checkpoints"
    )

    # Run
    result = run_laderman_experiment(config)