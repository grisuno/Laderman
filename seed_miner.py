#!/usr/bin/env python3
"""
Leibler Transformer Seed Prospector
====================================

Seed prospecting and long-term training framework for modular arithmetic
crystallization via thermodynamic phase transitions in transformer architectures.

Theoretical Framework (from Preprint):
  - delta: discretization margin ||theta - round(theta)||_inf
  - kappa: condition number of gradient covariance matrix cond(Sigma)
  - T_eff: effective temperature from gradient noise Tr(Sigma)/d
  - h_bar_eff: effective Planck constant (resolution floor)
  - S: attention entropy from attention weight distribution
  - C_v: heat capacity from energy variance
  - LC: local complexity (effective local dimensionality)
  - SP(psi): superposition coefficient from weight entanglement
  - alpha: purity index -log(delta)
  - G_alg: algorithmic gravitational constant (gradient tension)

Modes:
  prospect: Fast seed mining using delta as primary compass
  train: Long-term training with full thermodynamic monitoring

Repository: https://github.com/grisuno/strass_strassen
"""

import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import json
import os
import sys
import math
import time
import signal
from pathlib import Path
from dataclasses import dataclass, replace, field
from typing import Dict, List, Tuple, Optional, Any, Deque
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from enum import Enum
import warnings

warnings.filterwarnings("ignore")

from tran5 import (
    LeiblerAttention,
    LeiblerTransformerLayer,
    LeiblerTransformer,
    create_modular_addition_dataset,
    train_epoch,
    evaluate,
    prune_model,
    discretize_model,
)


class ExecutionMode(Enum):
    PROSPECT = "prospect"
    TRAIN = "train"


@dataclass(frozen=True)
class ProspectorConfig:
    """Immutable unified configuration for transformer seed prospecting."""

    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 256
    dropout: float = 0.1

    modulus: int = 26
    vocab_size: int = 28
    max_seq_len: int = 5
    train_fraction: float = 0.5

    T_min: float = 0.01
    T_max: float = 2.0
    cooling_rate: float = 0.001
    phase_transition_threshold: float = 0.1

    batch_size: int = 384
    learning_rate: float = 1e-3
    weight_decay_initial: float = 1e-2
    weight_decay_gas: float = 1e-2
    weight_decay_liquid: float = 1e-3
    weight_decay_glass: float = 1e-4
    weight_decay_crystal: float = 1e-5
    gradient_clip: float = 1.0

    prospect_epochs: int = 5000
    train_epochs: int = 25000
    warmup_epochs: int = 100
    grokking_epochs: int = 3000

    grokking_threshold: float = 0.95
    grokking_stability_required: int = 3
    grokking_train_loss_ceiling: float = 1e-3
    phase_window: int = 10

    pruning_threshold: float = 0.1
    discretization_tolerance: float = 0.1

    kappa_n_batches: int = 8
    kappa_calculation_freq: int = 50
    kappa_min_samples: int = 4
    kappa_crystal_threshold: float = 2.0
    kappa_window_size: int = 100
    spectral_regularization: float = 1e-6
    eigenvalue_floor: float = 1e-10

    delta_crystal_threshold: float = 0.1
    t_eff_crystal_ceiling: float = 1e-8

    local_complexity_epsilon: float = 1e-3
    local_complexity_num_samples: int = 50
    local_complexity_calculation_freq: int = 200

    superposition_hidden_dim: int = 64
    superposition_sparsity_threshold: float = 0.1
    superposition_calculation_freq: int = 200

    planck_constant_regularization: float = 1e-6

    glass_patience_epochs: int = 100
    glass_check_interval: int = 50
    glass_delta_ceiling: float = 0.4
    glass_accuracy_floor: float = 0.3
    glass_kappa_divergence_threshold: float = 1000.0

    mining_max_attempts: int = 100
    mining_start_seed: int = 1
    mining_metrics_display_interval: int = 25
    mining_partial_log_interval: int = 10

    crystallization_confirmation_epochs: int = 50
    resilience_test_samples: int = 1000
    resilience_pruning_steps: int = 20
    resilience_sparsity_max: float = 0.6
    resilience_check_interval: int = 5000

    checkpoint_interval_minutes: float = 5.0
    checkpoint_dir: str = "checkpoints_transformer"
    latest_checkpoint_name: str = "latest.pt"
    crystal_dir: str = "crystal_seeds_transformer"
    output_dir: str = "outputs_transformer"
    prospector_results_dir: str = "prospector_results_transformer"

    smoothing_factor: float = 0.95

    device: str = "cuda" if torch.cuda.is_available() else "cpu"


class IMetricCalculator(ABC):
    @abstractmethod
    def calculate(self, **kwargs) -> Dict[str, float]:
        pass


class ILossComponent(ABC):
    @abstractmethod
    def compute(self, model: nn.Module, loss_ce: torch.Tensor,
                epoch: int, **kwargs) -> torch.Tensor:
        pass


class ICheckpointManager(ABC):
    @abstractmethod
    def save(self, state: Dict[str, Any], path: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def load(self, path: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def should_checkpoint(self) -> bool:
        pass


class ITrainingPhase(ABC):
    @abstractmethod
    def execute(self, model: nn.Module, **kwargs) -> Any:
        pass


def build_leiderman_config(config: ProspectorConfig):
    from tran5 import LeidermanConfig
    import dataclasses as _dc

    leiderman_fields = {f.name for f in _dc.fields(LeidermanConfig)}

    field_mapping = {
        "d_model": config.d_model,
        "n_heads": config.n_heads,
        "n_layers": config.n_layers,
        "d_ff": config.d_ff,
        "dropout": config.dropout,
        "vocab_size": config.vocab_size,
        "max_seq_len": config.max_seq_len,
        "T_min": config.T_min,
        "T_max": config.T_max,
        "cooling_rate": config.cooling_rate,
        "phase_transition_threshold": config.phase_transition_threshold,
        "batch_size": config.batch_size,
        "learning_rate": config.learning_rate,
        "max_epochs": config.train_epochs,
        "warmup_epochs": config.warmup_epochs,
        "grokking_epochs": config.grokking_epochs,
        "grokking_threshold": config.grokking_threshold,
        "phase_window": config.phase_window,
        "pruning_threshold": config.pruning_threshold,
        "discretization_tolerance": config.discretization_tolerance,
        "weight_decay": config.weight_decay_initial,
        "weight_decay_initial": config.weight_decay_initial,
        "weight_decay_crystal": config.weight_decay_crystal,
        "weight_decay_min": config.weight_decay_crystal,
        "annealing_gas_wd": config.weight_decay_gas,
        "annealing_liquid_wd": config.weight_decay_liquid,
        "annealing_glass_wd": config.weight_decay_glass,
        "annealing_crystal_wd": config.weight_decay_crystal,
        "kappa_n_batches": config.kappa_n_batches,
        "kappa_crystal_threshold": config.kappa_crystal_threshold,
        "delta_crystal_threshold": config.delta_crystal_threshold,
        "t_eff_crystal_ceiling": config.t_eff_crystal_ceiling,
    }

    kwargs = {k: v for k, v in field_mapping.items() if k in leiderman_fields}

    return LeidermanConfig(**kwargs)


class DeltaCalculator(IMetricCalculator):
    def calculate(self, model: LeiblerTransformer, **kwargs) -> Dict[str, float]:
        all_weights = []
        for layer in model.layers:
            attn = layer.attention
            all_weights.extend([
                attn.q_proj.weight.detach().flatten(),
                attn.k_proj.weight.detach().flatten(),
                attn.v_proj.weight.detach().flatten(),
                attn.o_proj.weight.detach().flatten(),
            ])
        weights = torch.cat(all_weights)
        rounded = torch.round(weights)
        delta = torch.abs(weights - rounded).max().item()
        alpha = -np.log(delta + 1e-15) if delta > 0 else 20.0
        return {"delta": delta, "alpha_purity": alpha}


class KappaCalculator:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.gradient_buffer: Deque[torch.Tensor] = deque(
            maxlen=config.kappa_window_size
        )
        self.kappa_history: Deque[float] = deque(maxlen=100)

    def accumulate_gradient(self, model: nn.Module) -> None:
        if not any(p.grad is not None for p in model.parameters()):
            return
        grad_vector = []
        for p in model.parameters():
            if p.grad is not None:
                grad_vector.append(p.grad.detach().flatten().cpu())
            else:
                grad_vector.append(torch.zeros(p.numel()))
        self.gradient_buffer.append(torch.cat(grad_vector))

    def calculate_kappa(self) -> float:
        if len(self.gradient_buffer) < self.config.kappa_min_samples:
            return float("inf")
        try:
            G = torch.stack(list(self.gradient_buffer))
            G_centered = G - G.mean(dim=0, keepdim=True)
            n = G.shape[0]
            cov_small = (G_centered @ G_centered.T) / max(n - 1, 1)
            reg = torch.eye(cov_small.shape[0]) * self.config.spectral_regularization
            cov_reg = cov_small + reg
            eigenvalues = torch.linalg.eigvalsh(cov_reg)
            eigenvalues = eigenvalues[eigenvalues > self.config.eigenvalue_floor]
            if len(eigenvalues) < 2:
                return 1.0
            kappa = (eigenvalues[-1] / eigenvalues[0]).item()
            self.kappa_history.append(kappa)
            return max(kappa, 1.0)
        except Exception:
            return float("inf")

    def get_gradient_covariance(self) -> Optional[torch.Tensor]:
        if len(self.gradient_buffer) < self.config.kappa_min_samples:
            return None
        try:
            G = torch.stack(list(self.gradient_buffer))
            G_centered = G - G.mean(dim=0, keepdim=True)
            n = G.shape[0]
            return (G_centered.T @ G_centered) / max(n - 1, 1)
        except Exception:
            return None

    def get_kappa_trend(self) -> str:
        if len(self.kappa_history) < 10:
            return "insufficient_data"
        recent = list(self.kappa_history)[-10:]
        if all(recent[i] >= recent[i + 1] for i in range(len(recent) - 1)):
            return "decreasing"
        elif all(recent[i] <= recent[i + 1] for i in range(len(recent) - 1)):
            return "increasing"
        return "fluctuating"

    def is_crystallizing(self) -> bool:
        if len(self.kappa_history) < 20:
            return False
        recent = list(self.kappa_history)[-20:]
        return np.mean(recent) < self.config.kappa_crystal_threshold

    def reset(self) -> None:
        self.gradient_buffer.clear()
        self.kappa_history.clear()


class ThermodynamicMetricsCalculator(IMetricCalculator):
    def __init__(self, config: ProspectorConfig):
        self.config = config

    def calculate(self, model: LeiblerTransformer,
                  gradient_covariance: Optional[torch.Tensor] = None,
                  **kwargs) -> Dict[str, float]:
        if gradient_covariance is None:
            return {
                "h_bar_eff": 0.0,
                "T_eff_gradient": 0.0,
                "thermodynamic_entropy": 0.0,
                "trace_gradient_covariance": 0.0,
            }
        try:
            eigenvalues = torch.linalg.eigvalsh(gradient_covariance)
            eigenvalues = eigenvalues[eigenvalues > self.config.eigenvalue_floor]
            if len(eigenvalues) == 0:
                return {
                    "h_bar_eff": 0.0,
                    "T_eff_gradient": 0.0,
                    "thermodynamic_entropy": 0.0,
                    "trace_gradient_covariance": 0.0,
                }
            trace_sigma = eigenvalues.sum().item()
            dimension = len(eigenvalues)
            t_eff_gradient = trace_sigma / dimension if dimension > 0 else 0.0
            position_uncertainty = torch.sqrt(eigenvalues.mean()).item()
            h_bar_eff = position_uncertainty * self.config.planck_constant_regularization
            if t_eff_gradient > 0:
                boltzmann_entropy = -torch.sum(
                    eigenvalues * torch.log(eigenvalues + 1e-300)
                ).item() / t_eff_gradient
            else:
                boltzmann_entropy = 0.0
            return {
                "h_bar_eff": h_bar_eff,
                "T_eff_gradient": t_eff_gradient,
                "thermodynamic_entropy": boltzmann_entropy,
                "trace_gradient_covariance": trace_sigma,
            }
        except Exception:
            return {
                "h_bar_eff": 0.0,
                "T_eff_gradient": 0.0,
                "thermodynamic_entropy": 0.0,
                "trace_gradient_covariance": 0.0,
            }


class LocalComplexityCalculator(IMetricCalculator):
    def __init__(self, config: ProspectorConfig):
        self.config = config

    def calculate(self, model: LeiblerTransformer,
                  train_x: torch.Tensor, train_y: torch.Tensor,
                  device: torch.device, **kwargs) -> Dict[str, float]:
        epsilon = self.config.local_complexity_epsilon
        num_samples = self.config.local_complexity_num_samples
        original_params = {
            name: param.data.clone() for name, param in model.named_parameters()
        }
        model.eval()
        n_eval = min(len(train_x), 200)
        eval_x = train_x[:n_eval].to(device)
        eval_y = train_y[:n_eval].to(device)
        with torch.no_grad():
            logits_0 = model(eval_x)
            loss_0 = F.cross_entropy(logits_0[:, -1, :], eval_y).item()
        compatible_count = 0
        flat_params = torch.cat(
            [p.data.flatten() for p in model.parameters()]
        )
        n_params = flat_params.numel()
        for _ in range(num_samples):
            perturbation = torch.randn_like(flat_params) * epsilon
            perturbed = flat_params + perturbation
            idx = 0
            for param in model.parameters():
                numel = param.numel()
                param.data = perturbed[idx : idx + numel].reshape(param.shape)
                idx += numel
            with torch.no_grad():
                logits_p = model(eval_x)
                loss_p = F.cross_entropy(logits_p[:, -1, :], eval_y).item()
            if abs(loss_p - loss_0) < epsilon:
                compatible_count += 1
        for name, param in model.named_parameters():
            param.data = original_params[name]
        model.train()
        if compatible_count > 0:
            frac = compatible_count / num_samples
            volume = frac * ((2 * epsilon) ** n_params)
            lc = math.log(volume) if volume > 0 else -math.inf
        else:
            lc = -math.inf
        return {
            "local_complexity": lc,
            "lc_compatible_fraction": compatible_count / num_samples,
        }


class SuperpositionCalculator(IMetricCalculator):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.sae_encoder: Optional[nn.Linear] = None
        self.sae_decoder: Optional[nn.Linear] = None

    def _initialize_sae(self, input_dim: int, device: torch.device) -> None:
        if self.sae_encoder is None:
            hidden = self.config.superposition_hidden_dim
            self.sae_encoder = nn.Linear(input_dim, hidden).to(device)
            self.sae_decoder = nn.Linear(hidden, input_dim).to(device)

    def calculate(self, model: LeiblerTransformer, **kwargs) -> Dict[str, float]:
        device = next(model.parameters()).device
        theta = torch.cat(
            [p.detach().flatten() for p in model.parameters()]
        )
        input_dim = theta.numel()
        self._initialize_sae(input_dim, device)
        theta_exp = theta.unsqueeze(0)
        encoded = self.sae_encoder(theta_exp)
        encoded_sparse = torch.relu(encoded)
        reconstructed = self.sae_decoder(encoded_sparse)
        recon_error = torch.mean((theta_exp - reconstructed) ** 2).item()
        active = (
            encoded_sparse.abs() > self.config.superposition_sparsity_threshold
        ).sum().item()
        total = encoded_sparse.numel()
        feature_norms = torch.norm(encoded_sparse, dim=0)
        feature_var = torch.var(feature_norms).item()
        psi = 1.0 + recon_error + (
            feature_var / (feature_norms.mean().item() + 1e-8)
        )
        effective_features = active * (1.0 - recon_error)
        return {
            "superposition_psi": psi,
            "superposition_F": effective_features,
            "superposition_active_fraction": active / max(total, 1),
        }


class GravitationalConstantCalculator(IMetricCalculator):
    def calculate(self, model: LeiblerTransformer, **kwargs) -> Dict[str, float]:
        g_alg = 0.0
        count = 0
        for p in model.parameters():
            if p.grad is not None:
                g_alg += torch.mean(p.grad.detach() ** 2).item()
                count += 1
        g_alg = g_alg / max(count, 1)
        return {"G_alg": g_alg}


class PhaseDetector:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.current_phase = "unknown"
        self.phase_history: List[Tuple[int, str]] = []

    def detect(self, metrics: Dict[str, float]) -> str:
        kappa = metrics.get("kappa", float("inf"))
        delta = metrics.get("delta", 0.5)
        t_eff = metrics.get("T_eff_gradient", 1.0)
        test_acc = metrics.get("test_acc", 0.0)
        if (
            kappa < self.config.kappa_crystal_threshold
            and delta < self.config.delta_crystal_threshold
            and t_eff < self.config.t_eff_crystal_ceiling
            and test_acc > self.config.grokking_threshold
        ):
            phase = "crystal"
        elif delta < 0.3 and test_acc > 0.8:
            phase = "glass"
        elif delta < 0.45 and test_acc > 0.5:
            phase = "liquid"
        else:
            phase = "gas"
        epoch = int(metrics.get("epoch", 0))
        if phase != self.current_phase:
            print(
                f"*** PHASE TRANSITION at epoch {epoch}: "
                f"{self.current_phase} -> {phase} ***"
            )
            self.current_phase = phase
            self.phase_history.append((epoch, phase))
        return phase


class AdaptiveAnnealingScheduler:
    def __init__(
        self,
        model: LeiblerTransformer,
        config: ProspectorConfig,
        optimizer: optim.Optimizer,
    ):
        self.model = model
        self.config = config
        self.optimizer = optimizer
        self.current_temperature = config.T_max
        self.base_temperature = config.T_max
        self.current_weight_decay = config.weight_decay_initial
        self.accuracy_history: List[float] = []
        self.phase_stability_counter = 0

    def step(self, metrics: Dict[str, float]) -> None:
        test_acc = metrics.get("test_acc", 0.0)
        epoch = int(metrics.get("epoch", 0))
        phase = metrics.get("phase", "gas")
        self.accuracy_history.append(test_acc)
        if len(self.accuracy_history) > self.config.phase_window:
            self.accuracy_history.pop(0)
        if len(self.accuracy_history) >= 2:
            change = abs(self.accuracy_history[-1] - self.accuracy_history[-2])
            if change > self.config.phase_transition_threshold:
                self.phase_stability_counter = 0
            else:
                self.phase_stability_counter += 1
        if phase == "crystal":
            target_temp = self.config.T_min
            target_wd = self.config.weight_decay_crystal
        elif phase == "glass":
            target_temp = self.config.T_min
            target_wd = self.config.weight_decay_glass
        elif phase == "liquid":
            progress = min(epoch / self.config.grokking_epochs, 1.0)
            target_temp = self.config.T_min + (
                self.config.T_max - self.config.T_min
            ) * (1.0 - progress)
            target_wd = self.config.weight_decay_liquid
        else:
            if epoch < self.config.warmup_epochs:
                warmup_progress = epoch / max(self.config.warmup_epochs, 1)
                target_temp = self.config.T_max * (1.0 - warmup_progress * 0.3)
            else:
                cool = epoch - self.config.warmup_epochs
                decay = np.exp(-self.config.cooling_rate * cool)
                target_temp = self.config.T_min + (
                    self.config.T_max - self.config.T_min
                ) * decay
            target_wd = self.config.weight_decay_gas
        sf = self.config.smoothing_factor
        self.base_temperature = self.base_temperature * sf + target_temp * (1.0 - sf)
        self.current_weight_decay = (
            self.current_weight_decay * sf + target_wd * (1.0 - sf)
        )
        self.current_temperature = max(
            self.config.T_min, min(self.config.T_max, self.base_temperature)
        )
        self._update_model_temperatures()
        self._update_optimizer_weight_decay()

    def _update_model_temperatures(self) -> None:
        for layer in self.model.layers:
            layer.attention.temperature.data.fill_(self.current_temperature)

    def _update_optimizer_weight_decay(self) -> None:
        for group in self.optimizer.param_groups:
            group["weight_decay"] = self.current_weight_decay


class GlassDetector:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.metrics_buffer: Deque[Dict[str, float]] = deque(
            maxlen=config.glass_patience_epochs
        )

    def should_stop(
        self, epoch: int, metrics: Dict[str, float]
    ) -> Tuple[bool, str]:
        self.metrics_buffer.append(
            {
                "epoch": epoch,
                "delta": metrics.get("delta", float("inf")),
                "test_acc": metrics.get("test_acc", 0.0),
                "kappa": metrics.get("kappa", float("inf")),
            }
        )
        if epoch < self.config.glass_patience_epochs:
            return False, "warming_up"
        recent = list(self.metrics_buffer)[-self.config.glass_patience_epochs :]
        avg_delta = np.mean([m["delta"] for m in recent])
        avg_acc = np.mean([m["test_acc"] for m in recent])
        if avg_delta > self.config.glass_delta_ceiling and recent[-1]["delta"] > self.config.glass_delta_ceiling:
            return True, f"delta_stuck_high ({avg_delta:.4f})"
        if avg_acc < self.config.glass_accuracy_floor and recent[-1]["test_acc"] < self.config.glass_accuracy_floor:
            return True, f"accuracy_stuck_low ({avg_acc:.4f})"
        if len(recent) > 10:
            recent_k = [
                m["kappa"]
                for m in recent[-10:]
                if m["kappa"] != float("inf")
            ]
            if (
                len(recent_k) >= 10
                and all(
                    recent_k[i] < recent_k[i + 1]
                    for i in range(len(recent_k) - 1)
                )
                and recent_k[-1] > self.config.glass_kappa_divergence_threshold
            ):
                return True, f"kappa_diverging ({recent_k[-1]:.1f})"
        return False, ""


class GrokkinDetector:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.detected = False
        self.epoch: Optional[int] = None
        self.candidate_count = 0
        self.prev_test_acc = 0.0

    def update(self, metrics: Dict[str, float]) -> bool:
        test_acc = metrics.get("test_acc", 0.0)
        train_loss = metrics.get("train_loss", float("inf"))
        high_acc = test_acc > self.config.grokking_threshold
        low_loss = train_loss < self.config.grokking_train_loss_ceiling
        if high_acc and low_loss:
            self.candidate_count += 1
        else:
            self.candidate_count = 0
        if (
            self.candidate_count >= self.config.grokking_stability_required
            and not self.detected
        ):
            self.detected = True
            self.epoch = int(metrics.get("epoch", 0)) - self.config.grokking_stability_required + 1
            print("\n" + "=" * 80)
            print(f"*** STABLE GROKKING DETECTED at epoch {self.epoch} ***")
            print(
                f"Test accuracy: {self.prev_test_acc:.4f} -> {test_acc:.4f}"
            )
            print(
                f"Stability confirmed over {self.config.grokking_stability_required} epochs"
            )
            print("=" * 80 + "\n")
        self.prev_test_acc = test_acc
        return self.detected


class CheckpointManager(ICheckpointManager):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.last_checkpoint_time = time.time()

    def save(self, state: Dict[str, Any], path: Optional[str] = None) -> str:
        if path is None:
            path = str(
                self.checkpoint_dir / self.config.latest_checkpoint_name
            )
        path_obj = Path(path)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        torch.save(state, path)
        self.last_checkpoint_time = time.time()
        return str(path)

    def load(self, path: str) -> Optional[Dict[str, Any]]:
        try:
            return torch.load(path, map_location=self.config.device, weights_only=False)
        except Exception as e:
            print(f"Failed to load checkpoint from {path}: {e}")
            return None

    def should_checkpoint(self) -> bool:
        elapsed = (time.time() - self.last_checkpoint_time) / 60.0
        return elapsed >= self.config.checkpoint_interval_minutes

    def get_latest_path(self) -> Optional[str]:
        latest = self.checkpoint_dir / self.config.latest_checkpoint_name
        return str(latest) if latest.exists() else None


class ComprehensiveMetricsAggregator:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.delta_calc = DeltaCalculator()
        self.kappa_calc = KappaCalculator(config)
        self.thermo_calc = ThermodynamicMetricsCalculator(config)
        self.lc_calc = LocalComplexityCalculator(config)
        self.sp_calc = SuperpositionCalculator(config)
        self.grav_calc = GravitationalConstantCalculator()
        self._gradient_covariance: Optional[torch.Tensor] = None

    def compute_all(
        self,
        model: LeiblerTransformer,
        train_loss: float,
        test_loss: float,
        test_acc: float,
        epoch: int,
        weight_norm: float,
        grad_norm: float,
        thermo_state: Dict[str, float],
        scheduler: AdaptiveAnnealingScheduler,
        train_x: Optional[torch.Tensor] = None,
        train_y: Optional[torch.Tensor] = None,
        device: Optional[torch.device] = None,
        force_kappa: bool = False,
        force_lc: bool = False,
        force_sp: bool = False,
    ) -> Dict[str, float]:
        metrics: Dict[str, float] = {}
        metrics["epoch"] = float(epoch)
        metrics["train_loss"] = train_loss
        metrics["test_loss"] = test_loss
        metrics["test_acc"] = test_acc
        metrics["weight_norm"] = weight_norm
        metrics["grad_norm"] = grad_norm
        metrics["entropy"] = thermo_state["entropy"]
        metrics["heat_capacity"] = thermo_state["heat_capacity"]
        metrics["T_eff_attention"] = thermo_state["T_eff"]
        metrics["temperature"] = thermo_state["temperature"]
        metrics["weight_decay"] = scheduler.current_weight_decay
        metrics["scheduler_temperature"] = scheduler.current_temperature
        delta_m = self.delta_calc.calculate(model)
        metrics.update(delta_m)
        if force_kappa or epoch % self.config.kappa_calculation_freq == 0:
            kappa = self.kappa_calc.calculate_kappa()
            metrics["kappa"] = kappa
            metrics["kappa_trend"] = (
                1.0
                if self.kappa_calc.get_kappa_trend() == "decreasing"
                else (
                    -1.0
                    if self.kappa_calc.get_kappa_trend() == "increasing"
                    else 0.0
                )
            )
            metrics["is_crystallizing"] = float(
                self.kappa_calc.is_crystallizing()
            )
            self._gradient_covariance = (
                self.kappa_calc.get_gradient_covariance()
            )
        else:
            metrics["kappa"] = (
                self.kappa_calc.kappa_history[-1]
                if self.kappa_calc.kappa_history
                else float("inf")
            )
            metrics["kappa_trend"] = 0.0
            metrics["is_crystallizing"] = float(
                self.kappa_calc.is_crystallizing()
            )
        thermo_m = self.thermo_calc.calculate(
            model, gradient_covariance=self._gradient_covariance
        )
        metrics.update(thermo_m)
        grav_m = self.grav_calc.calculate(model)
        metrics.update(grav_m)
        if force_lc and train_x is not None and train_y is not None and device is not None:
            lc_m = self.lc_calc.calculate(
                model, train_x=train_x, train_y=train_y, device=device
            )
            metrics.update(lc_m)
        else:
            metrics.setdefault("local_complexity", 0.0)
            metrics.setdefault("lc_compatible_fraction", 0.0)
        if force_sp:
            sp_m = self.sp_calc.calculate(model)
            metrics.update(sp_m)
        else:
            metrics.setdefault("superposition_psi", 0.0)
            metrics.setdefault("superposition_F", 0.0)
            metrics.setdefault("superposition_active_fraction", 0.0)
        return metrics

    def accumulate_gradient(self, model: nn.Module) -> None:
        self.kappa_calc.accumulate_gradient(model)

    def reset(self) -> None:
        self.kappa_calc.reset()
        self._gradient_covariance = None


def format_kappa(kappa: float) -> str:
    if kappa == float("inf") or kappa > 1e6:
        return "     inf"
    return f"{kappa:8.2f}"


def format_lc(lc: float) -> str:
    if lc == -math.inf:
        return "   -inf"
    if lc == math.inf:
        return "    inf"
    return f"{lc:>7.2f}"


class ProspectorPhase(ITrainingPhase):
    def __init__(self, config: ProspectorConfig, seed: int):
        self.config = config
        self.seed = seed

    def execute(
        self, model: LeiblerTransformer, **kwargs
    ) -> Tuple[bool, Dict[str, Any]]:
        train_x = kwargs["train_x"]
        train_y = kwargs["train_y"]
        test_x = kwargs["test_x"]
        test_y = kwargs["test_y"]
        device = kwargs["device"]
        leiderman_config = kwargs["leiderman_config"]
        aggregator = ComprehensiveMetricsAggregator(self.config)
        phase_detector = PhaseDetector(self.config)
        glass_detector = GlassDetector(self.config)
        grokking_detector = GrokkinDetector(self.config)
        optimizer = optim.AdamW(
            model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay_initial,
        )
        scheduler = AdaptiveAnnealingScheduler(model, self.config, optimizer)
        best_delta = float("inf")
        best_epoch = 0
        history: List[Dict[str, float]] = []
        for epoch in range(1, self.config.prospect_epochs + 1):
            model.train()
            train_loss = train_epoch(
                model, train_x, train_y, optimizer, leiderman_config, device
            )
            aggregator.accumulate_gradient(model)
            test_loss, test_acc = evaluate(
                model, test_x, test_y, leiderman_config, device
            )
            thermo_state = model.get_thermodynamic_state()
            grad_norm = 0.0
            for p in model.parameters():
                if p.grad is not None:
                    grad_norm += p.grad.norm().item() ** 2
            grad_norm = np.sqrt(grad_norm)
            weight_norm = sum(p.norm().item() for p in model.parameters())
            should_display = (
                epoch % self.config.mining_metrics_display_interval == 0
                or epoch == self.config.prospect_epochs
            )
            force_kappa = epoch % self.config.kappa_calculation_freq == 0
            force_lc = epoch % self.config.local_complexity_calculation_freq == 0
            force_sp = epoch % self.config.superposition_calculation_freq == 0
            if should_display or force_kappa:
                metrics = aggregator.compute_all(
                    model=model,
                    train_loss=train_loss,
                    test_loss=test_loss,
                    test_acc=test_acc,
                    epoch=epoch,
                    weight_norm=weight_norm,
                    grad_norm=grad_norm,
                    thermo_state=thermo_state,
                    scheduler=scheduler,
                    train_x=train_x,
                    train_y=train_y,
                    device=device,
                    force_kappa=force_kappa,
                    force_lc=force_lc,
                    force_sp=force_sp,
                )
                phase = phase_detector.detect(metrics)
                metrics["phase"] = phase
                scheduler.step(metrics)
                grokking_detector.update(metrics)
                history.append(metrics.copy())
                if metrics["delta"] < best_delta:
                    best_delta = metrics["delta"]
                    best_epoch = epoch
                if should_display:
                    crystal_flag = (
                        "[+]"
                        if (
                            metrics["delta"] < self.config.delta_crystal_threshold
                            and test_acc > self.config.grokking_threshold
                        )
                        else "   "
                    )
                    print(
                        f" {crystal_flag} Epoch {epoch:>5}: "
                        f"delta={metrics['delta']:.4f} "
                        f"Acc={test_acc:.4f} "
                        f"kappa={format_kappa(metrics['kappa'])} "
                        f"S={metrics['entropy']:.3f} "
                        f"C_v={metrics['heat_capacity']:.2e} "
                        f"T_eff={metrics['T_eff_gradient']:.2e} "
                        f"h_bar={metrics['h_bar_eff']:.2e} "
                        f"G_alg={metrics['G_alg']:.4f} "
                        f"|W|={weight_norm:.2f} "
                        f"|g|={grad_norm:.2e} "
                        f"WD={scheduler.current_weight_decay:.1e} "
                        f"phase={phase[:4]} "
                        f"(best_d={best_delta:.4f}@{best_epoch})"
                    )
                    if (
                        metrics["delta"] < self.config.delta_crystal_threshold
                        and test_acc > self.config.grokking_threshold
                        and metrics["kappa"] < self.config.kappa_crystal_threshold
                    ):
                        print(f" [CRYSTAL] Detected at epoch {epoch}")
                        return True, {
                            **metrics,
                            "best_delta": best_delta,
                            "best_epoch": best_epoch,
                            "metrics_history": history,
                        }
            else:
                fast_delta = DeltaCalculator().calculate(model)
                scheduler.step(
                    {
                        "test_acc": test_acc,
                        "epoch": epoch,
                        "phase": phase_detector.current_phase,
                        "delta": fast_delta["delta"],
                        "kappa": (
                            aggregator.kappa_calc.kappa_history[-1]
                            if aggregator.kappa_calc.kappa_history
                            else float("inf")
                        ),
                        "T_eff_gradient": 0.0,
                    }
                )
            if epoch % self.config.glass_check_interval == 0 and history:
                is_glass, reason = glass_detector.should_stop(
                    epoch, history[-1]
                )
                if is_glass:
                    print(f" [-] GLASS DETECTED: {reason}")
                    print(
                        f"     Best delta was {best_delta:.4f} at epoch {best_epoch}"
                    )
                    return False, {
                        "delta": best_delta,
                        "best_epoch": best_epoch,
                        "metrics_history": history,
                    }
        print(
            f" [-] Max epochs reached. Best delta: {best_delta:.4f} at epoch {best_epoch}"
        )
        return False, {
            "delta": best_delta,
            "best_epoch": best_epoch,
            "metrics_history": history,
        }


class LongTrainingPhase(ITrainingPhase):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.history: List[Dict[str, float]] = []

    def execute(
        self, model: LeiblerTransformer, **kwargs
    ) -> LeiblerTransformer:
        train_x = kwargs["train_x"]
        train_y = kwargs["train_y"]
        test_x = kwargs["test_x"]
        test_y = kwargs["test_y"]
        device = kwargs["device"]
        leiderman_config = kwargs["leiderman_config"]
        checkpoint_manager = kwargs.get("checkpoint_manager")
        aggregator = ComprehensiveMetricsAggregator(self.config)
        phase_detector = PhaseDetector(self.config)
        grokking_detector = GrokkinDetector(self.config)
        optimizer = optim.AdamW(
            model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay_initial,
        )
        scheduler = AdaptiveAnnealingScheduler(model, self.config, optimizer)
        print("\n" + "=" * 80)
        print("PHASE 1: THERMODYNAMIC TRAINING WITH GROKKING")
        print("=" * 80)
        print(f"Pressure (WD): {self.config.weight_decay_initial} (adaptive by phase)")
        print(f"Batch size: {self.config.batch_size} (crystal window)")
        print(f"Kappa calculated every {self.config.kappa_calculation_freq} epochs")
        print(f"Target: kappa->1, delta->0, T_eff->0, Acc->1.0")
        print("=" * 80)
        header = (
            f"{'Epoch':>7} | {'Loss':>9} | {'tLoss':>9} | {'Acc':>6} | "
            f"{'delta':>7} | {'kappa':>8} | {'S':>6} | {'C_v':>9} | "
            f"{'T_eff':>9} | {'h_bar':>9} | {'G_alg':>7} | "
            f"{'|W|':>7} | {'|g|':>9} | {'WD':>8} | {'Phase':>5}"
        )
        print(header)
        print("-" * len(header))
        crystallization_counter = 0
        for epoch in range(1, self.config.train_epochs + 1):
            model.train()
            train_loss = train_epoch(
                model, train_x, train_y, optimizer, leiderman_config, device
            )
            aggregator.accumulate_gradient(model)
            test_loss, test_acc = evaluate(
                model, test_x, test_y, leiderman_config, device
            )
            thermo_state = model.get_thermodynamic_state()
            grad_norm = 0.0
            for p in model.parameters():
                if p.grad is not None:
                    grad_norm += p.grad.norm().item() ** 2
            grad_norm = np.sqrt(grad_norm)
            weight_norm = sum(p.norm().item() for p in model.parameters())
            force_kappa = epoch % self.config.kappa_calculation_freq == 0
            force_lc = epoch % self.config.local_complexity_calculation_freq == 0
            force_sp = epoch % self.config.superposition_calculation_freq == 0
            should_display = (
                epoch % self.config.mining_metrics_display_interval == 0
                or epoch == self.config.train_epochs
                or force_kappa
            )
            if should_display:
                metrics = aggregator.compute_all(
                    model=model,
                    train_loss=train_loss,
                    test_loss=test_loss,
                    test_acc=test_acc,
                    epoch=epoch,
                    weight_norm=weight_norm,
                    grad_norm=grad_norm,
                    thermo_state=thermo_state,
                    scheduler=scheduler,
                    train_x=train_x,
                    train_y=train_y,
                    device=device,
                    force_kappa=force_kappa,
                    force_lc=force_lc,
                    force_sp=force_sp,
                )
                phase = phase_detector.detect(metrics)
                metrics["phase"] = phase
                scheduler.step(metrics)
                grokking_detector.update(metrics)
                self.history.append(metrics.copy())
                print(
                    f"{epoch:>7} | "
                    f"{train_loss:>9.2e} | "
                    f"{test_loss:>9.2e} | "
                    f"{test_acc:>6.4f} | "
                    f"{metrics['delta']:>7.4f} | "
                    f"{format_kappa(metrics['kappa'])} | "
                    f"{metrics['entropy']:>6.3f} | "
                    f"{metrics['heat_capacity']:>9.2e} | "
                    f"{metrics['T_eff_gradient']:>9.2e} | "
                    f"{metrics['h_bar_eff']:>9.2e} | "
                    f"{metrics['G_alg']:>7.4f} | "
                    f"{weight_norm:>7.2f} | "
                    f"{grad_norm:>9.2e} | "
                    f"{scheduler.current_weight_decay:>8.1e} | "
                    f"{phase[:5]:>5}"
                )
                if force_lc:
                    print(
                        f"        LC={format_lc(metrics.get('local_complexity', 0.0))} "
                        f"psi={metrics.get('superposition_psi', 0.0):.3f} "
                        f"F={metrics.get('superposition_F', 0.0):.1f} "
                        f"alpha={metrics.get('alpha_purity', 0.0):.2f}"
                    )
                if phase == "crystal":
                    crystallization_counter += 1
                    if crystallization_counter >= self.config.crystallization_confirmation_epochs:
                        print(f"\n{'=' * 70}")
                        print(
                            f"[FREEZE] Crystallization confirmed after "
                            f"{self.config.crystallization_confirmation_epochs} stable epochs"
                        )
                        print(f"{'=' * 70}")
                        if checkpoint_manager is not None:
                            checkpoint_manager.save(
                                {
                                    "epoch": epoch,
                                    "model_state_dict": model.state_dict(),
                                    "history": self.history,
                                    "phase": "crystal",
                                    "kappa": metrics["kappa"],
                                    "delta": metrics["delta"],
                                    "test_acc": test_acc,
                                    "timestamp": datetime.now().isoformat(),
                                },
                                path=str(
                                    checkpoint_manager.checkpoint_dir
                                    / "crystallized.pt"
                                ),
                            )
                        return model
                else:
                    if crystallization_counter > 0:
                        print(
                            f"  [RESET] Phase reverted to {phase}, counter reset"
                        )
                    crystallization_counter = 0
                if checkpoint_manager is not None and checkpoint_manager.should_checkpoint():
                    cp_path = checkpoint_manager.save(
                        {
                            "epoch": epoch,
                            "model_state_dict": model.state_dict(),
                            "optimizer_state_dict": optimizer.state_dict(),
                            "history": self.history,
                            "phase": phase,
                            "timestamp": datetime.now().isoformat(),
                        }
                    )
                    print(f"  [CHECKPOINT] {cp_path}")
            else:
                fast_delta = DeltaCalculator().calculate(model)
                scheduler.step(
                    {
                        "test_acc": test_acc,
                        "epoch": epoch,
                        "phase": phase_detector.current_phase,
                        "delta": fast_delta["delta"],
                        "kappa": (
                            aggregator.kappa_calc.kappa_history[-1]
                            if aggregator.kappa_calc.kappa_history
                            else float("inf")
                        ),
                        "T_eff_gradient": 0.0,
                    }
                )
        if checkpoint_manager is not None:
            checkpoint_manager.save(
                {
                    "epoch": self.config.train_epochs,
                    "model_state_dict": model.state_dict(),
                    "history": self.history,
                    "phase": phase_detector.current_phase,
                    "timestamp": datetime.now().isoformat(),
                    "training_completed": True,
                }
            )
        return model


class SeedProspector:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.crystal_dir = Path(config.crystal_dir)
        self.crystal_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir = Path(config.prospector_results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def prospect(
        self,
        total_attempts: Optional[int] = None,
        start_seed: Optional[int] = None,
    ) -> bool:
        if total_attempts is None:
            total_attempts = self.config.mining_max_attempts
        if start_seed is None:
            start_seed = self.config.mining_start_seed
        device = torch.device(self.config.device)
        leiderman_config = build_leiderman_config(self.config)
        print(f"\nStarting transformer seed prospecting with {total_attempts} attempts")
        print(f"Target: delta < {self.config.delta_crystal_threshold}, "
              f"Acc > {self.config.grokking_threshold}, "
              f"kappa < {self.config.kappa_crystal_threshold}")
        print(f"Batch size: {self.config.batch_size} (crystal window [24, 128])")
        print(f"Device: {device}")
        results_log: List[Dict[str, Any]] = []
        for i in range(start_seed, start_seed + total_attempts):
            seed = i
            attempt = i - start_seed + 1
            print(f"\n{'=' * 60}")
            print(f"[*] MINING SEED {seed} ({attempt}/{total_attempts})")
            print(f"{'=' * 60}")
            self._set_seed(seed)
            train_x, train_y, test_x, test_y = create_modular_addition_dataset(
                modulus=self.config.modulus,
                train_fraction=self.config.train_fraction,
            )
            train_x = train_x.to(device)
            train_y = train_y.to(device)
            test_x = test_x.to(device)
            test_y = test_y.to(device)
            model = LeiblerTransformer(leiderman_config).to(device)
            n_params = sum(p.numel() for p in model.parameters())
            print(f"  Parameters: {n_params:,}")
            phase = ProspectorPhase(self.config, seed)
            start_time = time.time()
            is_crystal, final_metrics = phase.execute(
                model,
                train_x=train_x,
                train_y=train_y,
                test_x=test_x,
                test_y=test_y,
                device=device,
                leiderman_config=leiderman_config,
            )
            elapsed = time.time() - start_time
            result = {
                "seed": seed,
                "is_crystal": is_crystal,
                "elapsed_seconds": elapsed,
                "best_delta": final_metrics.get("best_delta", final_metrics.get("delta", 1.0)),
                "best_epoch": final_metrics.get("best_epoch", 0),
                "timestamp": datetime.now().isoformat(),
            }
            results_log.append(result)
            seed_path = self.results_dir / f"seed_{seed:05d}_metrics.json"
            safe_metrics = {
                k: v
                for k, v in final_metrics.items()
                if k != "metrics_history"
            }
            with open(seed_path, "w") as f:
                json.dump(
                    {"seed": seed, "is_crystal": is_crystal, "metrics": safe_metrics},
                    f,
                    indent=2,
                    default=str,
                )
            if "metrics_history" in final_metrics:
                hist_path = self.results_dir / f"seed_{seed:05d}_history.json"
                with open(hist_path, "w") as f:
                    json.dump(
                        final_metrics["metrics_history"], f, indent=2, default=str
                    )
            if is_crystal:
                print(f"\n{'=' * 60}")
                print(f"[+] CRYSTAL FOUND -- Seed {seed}")
                print(f"{'=' * 60}")
                print(f"  delta: {final_metrics.get('delta', 'N/A')}")
                print(f"  kappa: {final_metrics.get('kappa', 'N/A')}")
                print(f"  test_acc: {final_metrics.get('test_acc', 'N/A')}")
                print(f"  alpha_purity: {final_metrics.get('alpha_purity', 'N/A')}")
                crystal_path = (
                    self.crystal_dir
                    / f"crystal_seed_{seed}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pt"
                )
                torch.save(
                    {
                        "seed": seed,
                        "model_state_dict": model.state_dict(),
                        "metrics": safe_metrics,
                        "config": self.config,
                    },
                    crystal_path,
                )
                print(f"  Saved: {crystal_path}")
            else:
                print(f"  [-] Seed {seed} vitrified (glass)")
            if attempt % self.config.mining_partial_log_interval == 0:
                log_path = self.crystal_dir / "mining_log_partial.json"
                with open(log_path, "w") as f:
                    json.dump(results_log, f, indent=2, default=str)
        final_log = self.crystal_dir / "mining_log_complete.json"
        with open(final_log, "w") as f:
            json.dump(results_log, f, indent=2, default=str)
        crystals = sum(1 for r in results_log if r["is_crystal"])
        print(f"\n{'=' * 60}")
        print("MINING COMPLETE")
        print(f"{'=' * 60}")
        print(f"Total attempts: {total_attempts}")
        print(f"Crystals found: {crystals}")
        print(f"Success rate: {100.0 * crystals / max(total_attempts, 1):.1f}%")
        if crystals > 0:
            seeds = [r["seed"] for r in results_log if r["is_crystal"]]
            print(f"Crystal seeds: {seeds}")
        best_seeds = sorted(results_log, key=lambda r: r["best_delta"])[:5]
        print(f"\nTop 5 seeds by delta:")
        for r in best_seeds:
            print(
                f"  Seed {r['seed']:>5}: delta={r['best_delta']:.6f} "
                f"crystal={'YES' if r['is_crystal'] else ' NO'}"
            )
        return crystals > 0

    def _set_seed(self, seed: int) -> None:
        torch.manual_seed(seed)
        np.random.seed(seed)
        if self.config.device == "cuda":
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)


class LongTrainingPipeline:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.checkpoint_manager = CheckpointManager(config)
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print("\n\n[INFO] Interrupt received. Will save checkpoint at next opportunity...")
        self.interrupted = True

    def run(
        self,
        resume_from: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> bool:
        config = self.config
        device = torch.device(config.device)
        leiderman_config = build_leiderman_config(config)
        print("\n" + "=" * 70)
        print("  LEIBLER TRANSFORMER CRYSTALLIZATION FRAMEWORK")
        print("  Thermodynamic Phase Transition in Weight Space")
        print("=" * 70)
        print(f"Device: {device}")
        print(f"Architecture: d_model={config.d_model}, n_heads={config.n_heads}, "
              f"n_layers={config.n_layers}, d_ff={config.d_ff}")
        print(f"Task: modular addition mod {config.modulus}")
        print(f"Batch size: {config.batch_size}")
        print(f"Weight decay: {config.weight_decay_initial} (adaptive)")
        print(f"Kappa threshold: {config.kappa_crystal_threshold}")
        print(f"Delta target: {config.delta_crystal_threshold}")
        print("=" * 70)
        if seed is not None:
            torch.manual_seed(seed)
            np.random.seed(seed)
            print(f"Using seed: {seed}")
        train_x, train_y, test_x, test_y = create_modular_addition_dataset(
            modulus=config.modulus, train_fraction=config.train_fraction
        )
        train_x = train_x.to(device)
        train_y = train_y.to(device)
        test_x = test_x.to(device)
        test_y = test_y.to(device)
        print(f"Train: {len(train_x)}, Test: {len(test_x)}")
        model = LeiblerTransformer(leiderman_config).to(device)
        n_params = sum(p.numel() for p in model.parameters())
        print(f"Parameters: {n_params:,}")
        start_epoch = 0
        if resume_from is None:
            resume_from = self.checkpoint_manager.get_latest_path()
        if resume_from is not None:
            checkpoint = self.checkpoint_manager.load(resume_from)
            if checkpoint is not None:
                model.load_state_dict(checkpoint["model_state_dict"])
                start_epoch = checkpoint.get("epoch", 0)
                print(f"[RESUME] From epoch {start_epoch}")
        phase1 = LongTrainingPhase(config)
        model = phase1.execute(
            model,
            train_x=train_x,
            train_y=train_y,
            test_x=test_x,
            test_y=test_y,
            device=device,
            leiderman_config=leiderman_config,
            checkpoint_manager=self.checkpoint_manager,
        )
        if self.interrupted:
            return False
        print("\n" + "=" * 80)
        print("PHASE 2: PRUNING AND DISCRETIZATION")
        print("=" * 80 + "\n")
        n_slots = prune_model(model, threshold=config.pruning_threshold)
        print(f"Model pruned to {n_slots} slots")
        discretized = discretize_model(
            model, tolerance=config.discretization_tolerance
        )
        test_loss, test_acc = evaluate(
            model, test_x, test_y, leiderman_config, device
        )
        delta_m = DeltaCalculator().calculate(model)
        print(f"\nPost-discretization test accuracy: {test_acc:.4f}")
        print(f"Post-discretization delta: {delta_m['delta']:.6f}")
        print(f"Discretization success: {discretized}")
        torch.save(
            {
                "model_state_dict": model.state_dict(),
                "test_acc": test_acc,
                "delta": delta_m["delta"],
                "discretized": discretized,
                "history": phase1.history,
                "config": config,
                "timestamp": datetime.now().isoformat(),
            },
            self.output_dir / "final_model.pt",
        )
        if phase1.history:
            with open(self.output_dir / "training_history.json", "w") as f:
                json.dump(phase1.history, f, indent=2, default=str)
        print("\n" + "=" * 80)
        print("EXPERIMENT SUMMARY")
        print("=" * 80)
        print(f"Total epochs: {len(phase1.history)}")
        print(f"Final test accuracy: {test_acc:.4f}")
        print(f"Final delta: {delta_m['delta']:.6f}")
        print(f"Discretization: {'SUCCESS' if discretized else 'FAILED'}")
        return discretized


def main():
    parser = argparse.ArgumentParser(
        description="Leibler Transformer Seed Prospector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  prospect    Fast seed mining using delta as primary compass
  train       Long-term training with full thermodynamic monitoring

Examples:
  python seed_miner.py prospect --attempts 100 --start-seed 1
  python seed_miner.py train --seed 42 --epochs 25000
  python seed_miner.py train --resume checkpoints_transformer/latest.pt
        """,
    )
    parser.add_argument(
        "mode",
        type=str,
        choices=["prospect", "train"],
        help="Execution mode",
    )
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument("--attempts", type=int, default=None)
    parser.add_argument("--start-seed", type=int, default=None)
    parser.add_argument("--epochs", type=int, default=None)
    parser.add_argument("--prospect-epochs", type=int, default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--learning-rate", type=float, default=None)
    parser.add_argument("--modulus", type=int, default=None)
    parser.add_argument("--d-model", type=int, default=None)
    parser.add_argument("--n-heads", type=int, default=None)
    parser.add_argument("--n-layers", type=int, default=None)
    parser.add_argument("--d-ff", type=int, default=None)
    parser.add_argument(
        "--device",
        type=str,
        default=None,
    )
    args = parser.parse_args()
    overrides: Dict[str, Any] = {}
    if args.epochs is not None:
        overrides["train_epochs"] = args.epochs
    if args.prospect_epochs is not None:
        overrides["prospect_epochs"] = args.prospect_epochs
    if args.batch_size is not None:
        overrides["batch_size"] = args.batch_size
    if args.learning_rate is not None:
        overrides["learning_rate"] = args.learning_rate
    if args.attempts is not None:
        overrides["mining_max_attempts"] = args.attempts
    if args.start_seed is not None:
        overrides["mining_start_seed"] = args.start_seed
    if args.modulus is not None:
        overrides["modulus"] = args.modulus
        overrides["vocab_size"] = args.modulus + 2
    if args.d_model is not None:
        overrides["d_model"] = args.d_model
    if args.n_heads is not None:
        overrides["n_heads"] = args.n_heads
    if args.n_layers is not None:
        overrides["n_layers"] = args.n_layers
    if args.d_ff is not None:
        overrides["d_ff"] = args.d_ff
    if args.device is not None:
        overrides["device"] = args.device
    config = replace(ProspectorConfig(), **overrides)
    if args.mode == "prospect":
        prospector = SeedProspector(config)
        success = prospector.prospect()
        sys.exit(0 if success else 1)
    elif args.mode == "train":
        pipeline = LongTrainingPipeline(config)
        success = pipeline.run(resume_from=args.resume, seed=args.seed)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()