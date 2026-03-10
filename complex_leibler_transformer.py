#!/usr/bin/env python3
"""
Complex-Valued Leibler Transformer with Thermodynamic Crystallization
=====================================================================

Hypothesis: If the HPU used phase to protect information in the vacuum,
a Complex Transformer can crystallize attention in the phase domain,
allowing Leiderman to emerge as perfect constructive interference.

Theoretical Framework:
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
  - phase_coherence: complex phase alignment across attention heads
  - interference_pattern: constructive/destructive interference metric
  - complex_modulus_variance: stability of complex weight magnitudes
  - phase_entropy: entropy of the phase distribution of complex weights

Author: Gris Iscomeback
Email: grisiscomeback@gmail.com
License: AGPL v3
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
import warnings
from pathlib import Path
from dataclasses import dataclass, replace, field
from typing import Dict, List, Tuple, Optional, Any, Deque
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from enum import Enum

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# Execution Mode Enumeration
# ---------------------------------------------------------------------------

class ExecutionMode(Enum):
    PROSPECT = "prospect"
    TRAIN = "train"


# ---------------------------------------------------------------------------
# Immutable Configuration
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProspectorConfig:

    # Architecture
    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 256
    dropout: float = 0.1

    # Complex expansion factor for internal complex hidden dimension
    complex_expansion_factor: float = 1.0

    # Task
    modulus: int = 26
    vocab_size: int = 28
    max_seq_len: int = 5
    train_fraction: float = 0.5

    # Thermodynamic parameters
    t_min: float = 0.01
    t_max: float = 2.0
    cooling_rate: float = 0.001
    phase_transition_threshold: float = 0.1

    # Training hyperparameters
    batch_size: int = 384
    learning_rate: float = 1e-3
    weight_decay_initial: float = 1e-2
    weight_decay_gas: float = 1e-2
    weight_decay_liquid: float = 1e-3
    weight_decay_glass: float = 1e-4
    weight_decay_crystal: float = 1e-5
    gradient_clip: float = 1.0

    # Epoch budgets
    prospect_epochs: int = 5000
    train_epochs: int = 25000
    warmup_epochs: int = 100
    grokking_epochs: int = 3000

    # Grokking detection
    grokking_threshold: float = 0.95
    grokking_stability_required: int = 3
    grokking_train_loss_ceiling: float = 1e-3
    phase_window: int = 10

    # Pruning and discretization
    pruning_threshold: float = 0.1
    discretization_tolerance: float = 0.1

    # Kappa calculation
    kappa_n_batches: int = 8
    kappa_calculation_freq: int = 50
    kappa_min_samples: int = 4
    kappa_crystal_threshold: float = 2.0
    kappa_window_size: int = 100
    spectral_regularization: float = 1e-6
    eigenvalue_floor: float = 1e-10
    kappa_max_dim: int = 10000

    # Crystal thresholds
    delta_crystal_threshold: float = 0.1
    t_eff_crystal_ceiling: float = 1e-8

    # Local complexity
    local_complexity_epsilon: float = 1e-3
    local_complexity_num_samples: int = 50
    local_complexity_calculation_freq: int = 200

    # Superposition
    superposition_hidden_dim: int = 64
    superposition_sparsity_threshold: float = 0.1
    superposition_calculation_freq: int = 200

    # Planck constant
    planck_constant_regularization: float = 1e-6

    # Glass detection
    glass_patience_epochs: int = 100
    glass_check_interval: int = 50
    glass_delta_ceiling: float = 0.4
    glass_accuracy_floor: float = 0.3
    glass_kappa_divergence_threshold: float = 1000.0

    # Mining
    mining_max_attempts: int = 100
    mining_start_seed: int = 1
    mining_metrics_display_interval: int = 25
    mining_partial_log_interval: int = 10

    # Crystallization
    crystallization_confirmation_epochs: int = 50
    resilience_test_samples: int = 1000
    resilience_pruning_steps: int = 20
    resilience_sparsity_max: float = 0.6
    resilience_check_interval: int = 5000

    # Checkpointing
    checkpoint_interval_minutes: float = 5.0
    checkpoint_dir: str = "checkpoints_complex_transformer"
    latest_checkpoint_name: str = "latest.pt"
    crystal_dir: str = "crystal_seeds_complex_transformer"
    output_dir: str = "outputs_complex_transformer"
    prospector_results_dir: str = "prospector_results_complex_transformer"

    # Smoothing
    smoothing_factor: float = 0.95

    # Complex-specific parameters
    phase_regularization_weight: float = 0.01
    interference_loss_weight: float = 0.01
    complex_weight_init_std: float = 0.02
    phase_coherence_bins: int = 64
    modulus_stability_epsilon: float = 1e-8

    # Numerical stability
    numerical_epsilon: float = 1e-10
    log_floor: float = 1e-15
    max_kappa_display: float = 1e6

    # Device
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


# ---------------------------------------------------------------------------
# Abstract Interfaces (SOLID: Interface Segregation)
# ---------------------------------------------------------------------------

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


class IPhaseDetector(ABC):
    @abstractmethod
    def detect(self, metrics: Dict[str, float]) -> str:
        pass


class IGlassDetector(ABC):
    @abstractmethod
    def should_stop(self, epoch: int, metrics: Dict[str, float]) -> Tuple[bool, str]:
        pass


class IGrokkinDetector(ABC):
    @abstractmethod
    def update(self, metrics: Dict[str, float]) -> bool:
        pass


# ---------------------------------------------------------------------------
# Seed Management (Single Responsibility)
# ---------------------------------------------------------------------------

class SeedManager:
    @staticmethod
    def set_seed(seed: int, device: str = "cpu") -> None:
        torch.manual_seed(seed)
        np.random.seed(seed)
        if device == "cuda" and torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False


# ---------------------------------------------------------------------------
# Complex-Valued Operations Module (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexOperations:

    @staticmethod
    def complex_linear(
        input_real: torch.Tensor,
        input_imag: torch.Tensor,
        weight_real: torch.Tensor,
        weight_imag: torch.Tensor,
        bias_real: Optional[torch.Tensor] = None,
        bias_imag: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        out_real = F.linear(input_real, weight_real) - F.linear(input_imag, weight_imag)
        out_imag = F.linear(input_real, weight_imag) + F.linear(input_imag, weight_real)
        if bias_real is not None:
            out_real = out_real + bias_real
        if bias_imag is not None:
            out_imag = out_imag + bias_imag
        return out_real, out_imag

    @staticmethod
    def complex_gelu(real: torch.Tensor, imag: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        magnitude = torch.sqrt(real ** 2 + imag ** 2 + 1e-8)
        gate = F.gelu(magnitude)
        scale = gate / (magnitude + 1e-8)
        return real * scale, imag * scale

    @staticmethod
    def complex_layer_norm(
        real: torch.Tensor,
        imag: torch.Tensor,
        weight: torch.Tensor,
        bias: torch.Tensor,
        eps: float = 1e-5
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        variance = (real ** 2 + imag ** 2).mean(dim=-1, keepdim=True)
        std = torch.sqrt(variance + eps)
        real_normed = real / std
        imag_normed = imag / std
        real_out = real_normed * weight + bias
        imag_out = imag_normed * weight
        return real_out, imag_out

    @staticmethod
    def compute_phase(real: torch.Tensor, imag: torch.Tensor) -> torch.Tensor:
        return torch.atan2(imag, real + 1e-10)

    @staticmethod
    def compute_magnitude(real: torch.Tensor, imag: torch.Tensor) -> torch.Tensor:
        return torch.sqrt(real ** 2 + imag ** 2 + 1e-8)

    @staticmethod
    def complex_softmax(
        real: torch.Tensor,
        imag: torch.Tensor,
        temperature: torch.Tensor,
        dim: int = -1
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        magnitude = torch.sqrt(real ** 2 + imag ** 2 + 1e-8)
        phase = torch.atan2(imag, real + 1e-10)
        attn_weights = F.softmax(magnitude / temperature, dim=dim)
        out_real = attn_weights * torch.cos(phase)
        out_imag = attn_weights * torch.sin(phase)
        return out_real, out_imag


# ---------------------------------------------------------------------------
# Complex Linear Layer (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexLinear(nn.Module):
    def __init__(self, in_features: int, out_features: int, bias: bool = True,
                 init_std: float = 0.02):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight_real = nn.Parameter(torch.randn(out_features, in_features) * init_std)
        self.weight_imag = nn.Parameter(torch.randn(out_features, in_features) * init_std)
        if bias:
            self.bias_real = nn.Parameter(torch.zeros(out_features))
            self.bias_imag = nn.Parameter(torch.zeros(out_features))
        else:
            self.register_parameter("bias_real", None)
            self.register_parameter("bias_imag", None)

    def forward(self, real: torch.Tensor, imag: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        return ComplexOperations.complex_linear(
            real, imag,
            self.weight_real, self.weight_imag,
            self.bias_real, self.bias_imag
        )


# ---------------------------------------------------------------------------
# Complex Layer Normalization (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexLayerNorm(nn.Module):
    def __init__(self, normalized_shape: int, eps: float = 1e-5):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(normalized_shape))
        self.bias = nn.Parameter(torch.zeros(normalized_shape))

    def forward(self, real: torch.Tensor, imag: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        return ComplexOperations.complex_layer_norm(real, imag, self.weight, self.bias, self.eps)


# ---------------------------------------------------------------------------
# Complex Attention with Phase Interference (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexLeiblerAttention(nn.Module):
    def __init__(self, config: ProspectorConfig):
        super().__init__()
        self.config = config
        self.d_model = config.d_model
        self.n_heads = config.n_heads
        self.d_head = config.d_model // config.n_heads

        self.temperature = nn.Parameter(torch.ones(1) * config.t_max)

        self.q_proj = ComplexLinear(config.d_model, config.d_model, init_std=config.complex_weight_init_std)
        self.k_proj = ComplexLinear(config.d_model, config.d_model, init_std=config.complex_weight_init_std)
        self.v_proj = ComplexLinear(config.d_model, config.d_model, init_std=config.complex_weight_init_std)
        self.o_proj = ComplexLinear(config.d_model, config.d_model, init_std=config.complex_weight_init_std)

        self.entropy = 0.0
        self.heat_capacity = 0.0
        self.t_eff = config.t_max
        self.phase_coherence = 0.0
        self.interference_strength = 0.0
        self.attention_magnitude_mean = 0.0
        self.attention_phase_std = 0.0
        self.scores_real: Optional[torch.Tensor] = None
        self.scores_imag: Optional[torch.Tensor] = None

    def forward(
        self,
        real: torch.Tensor,
        imag: torch.Tensor,
        mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        batch_size, seq_len, _ = real.shape

        q_r, q_i = self.q_proj(real, imag)
        k_r, k_i = self.k_proj(real, imag)
        v_r, v_i = self.v_proj(real, imag)

        q_r = q_r.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        q_i = q_i.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        k_r = k_r.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        k_i = k_i.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        v_r = v_r.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        v_i = v_i.view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)

        scale = np.sqrt(self.d_head)
        scores_real = (torch.matmul(q_r, k_r.transpose(-2, -1)) + torch.matmul(q_i, k_i.transpose(-2, -1))) / scale
        scores_imag = (torch.matmul(q_i, k_r.transpose(-2, -1)) - torch.matmul(q_r, k_i.transpose(-2, -1))) / scale

        self.scores_real = scores_real.detach()
        self.scores_imag = scores_imag.detach()

        if mask is not None:
            scores_real = scores_real.masked_fill(mask == 0, float("-inf"))
            scores_imag = scores_imag.masked_fill(mask == 0, 0.0)

        attn_real, attn_imag = ComplexOperations.complex_softmax(
            scores_real, scores_imag, self.temperature
        )

        out_r = torch.matmul(attn_real, v_r) - torch.matmul(attn_imag, v_i)
        out_i = torch.matmul(attn_real, v_i) + torch.matmul(attn_imag, v_r)

        out_r = out_r.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        out_i = out_i.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)

        out_r, out_i = self.o_proj(out_r, out_i)

        self._update_thermodynamic_state(attn_real, attn_imag)

        return out_r, out_i

    def _update_thermodynamic_state(
        self, attn_real: torch.Tensor, attn_imag: torch.Tensor
    ) -> None:
        with torch.no_grad():
            magnitude = ComplexOperations.compute_magnitude(attn_real, attn_imag)
            phase = ComplexOperations.compute_phase(attn_real, attn_imag)

            mag_sum = magnitude.sum(dim=-1, keepdim=True) + self.config.numerical_epsilon
            prob = magnitude / mag_sum
            entropy = -torch.sum(prob * torch.log(prob + self.config.numerical_epsilon), dim=-1)
            self.entropy = entropy.mean().item()

            energies = -torch.log(prob + self.config.numerical_epsilon)
            energy_mean = energies.mean()
            energy_var = ((energies - energy_mean) ** 2).mean()
            self.heat_capacity = (energy_var / (self.temperature ** 2 + self.config.numerical_epsilon)).item()

            energy_fluctuation = torch.sqrt(energy_var + self.config.numerical_epsilon)
            self.t_eff = (energy_fluctuation / (1.0 + entropy.mean())).item()

            phase_mean = phase.mean(dim=-1, keepdim=True)
            phase_diff = phase - phase_mean
            self.phase_coherence = torch.cos(phase_diff).mean().item()

            constructive = torch.cos(phase).mean().item()
            self.interference_strength = abs(constructive)

            self.attention_magnitude_mean = magnitude.mean().item()
            self.attention_phase_std = phase.std().item()


# ---------------------------------------------------------------------------
# Complex Transformer Layer (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexLeiblerTransformerLayer(nn.Module):
    def __init__(self, config: ProspectorConfig):
        super().__init__()
        self.attention = ComplexLeiblerAttention(config)

        ff_hidden = int(config.d_ff * config.complex_expansion_factor)
        self.ff_real_1 = ComplexLinear(config.d_model, ff_hidden, init_std=config.complex_weight_init_std)
        self.ff_real_2 = ComplexLinear(ff_hidden, config.d_model, init_std=config.complex_weight_init_std)
        self.dropout_rate = config.dropout

        self.norm1 = ComplexLayerNorm(config.d_model)
        self.norm2 = ComplexLayerNorm(config.d_model)

    def forward(
        self,
        real: torch.Tensor,
        imag: torch.Tensor,
        mask: Optional[torch.Tensor] = None
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        norm_r, norm_i = self.norm1(real, imag)
        attn_r, attn_i = self.attention(norm_r, norm_i, mask)
        attn_r = F.dropout(attn_r, p=self.dropout_rate, training=self.training)
        attn_i = F.dropout(attn_i, p=self.dropout_rate, training=self.training)
        real = real + attn_r
        imag = imag + attn_i

        norm_r, norm_i = self.norm2(real, imag)
        ff_r, ff_i = self.ff_real_1(norm_r, norm_i)
        ff_r, ff_i = ComplexOperations.complex_gelu(ff_r, ff_i)
        ff_r = F.dropout(ff_r, p=self.dropout_rate, training=self.training)
        ff_i = F.dropout(ff_i, p=self.dropout_rate, training=self.training)
        ff_r, ff_i = self.ff_real_2(ff_r, ff_i)
        ff_r = F.dropout(ff_r, p=self.dropout_rate, training=self.training)
        ff_i = F.dropout(ff_i, p=self.dropout_rate, training=self.training)
        real = real + ff_r
        imag = imag + ff_i

        return real, imag


# ---------------------------------------------------------------------------
# Complete Complex Leibler Transformer (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexLeiblerTransformer(nn.Module):
    def __init__(self, config: ProspectorConfig):
        super().__init__()
        self.config = config

        self.token_embedding_real = nn.Embedding(config.vocab_size, config.d_model)
        self.token_embedding_imag = nn.Embedding(config.vocab_size, config.d_model)

        self.pos_encoding_real = nn.Parameter(
            torch.randn(1, config.max_seq_len, config.d_model) * config.complex_weight_init_std
        )
        self.pos_encoding_imag = nn.Parameter(
            torch.randn(1, config.max_seq_len, config.d_model) * config.complex_weight_init_std
        )

        self.layers = nn.ModuleList([
            ComplexLeiblerTransformerLayer(config) for _ in range(config.n_layers)
        ])

        self.output_norm = ComplexLayerNorm(config.d_model)
        self.output_proj_real = nn.Linear(config.d_model, config.vocab_size)
        self.output_proj_imag = nn.Linear(config.d_model, config.vocab_size)

        self._init_weights()

    def _init_weights(self) -> None:
        init_std = self.config.complex_weight_init_std
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, std=init_std)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, std=init_std)

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None
    ) -> torch.Tensor:
        seq_len = x.size(1)
        real = self.token_embedding_real(x) + self.pos_encoding_real[:, :seq_len, :]
        imag = self.token_embedding_imag(x) + self.pos_encoding_imag[:, :seq_len, :]

        for layer in self.layers:
            real, imag = layer(real, imag, mask)

        real, imag = self.output_norm(real, imag)

        logits_real = self.output_proj_real(real)
        logits_imag = self.output_proj_imag(imag)

        logits_magnitude = ComplexOperations.compute_magnitude(logits_real, logits_imag)
        return logits_magnitude

    def get_thermodynamic_state(self) -> Dict[str, float]:
        n_layers = len(self.layers)
        state = {
            "entropy": 0.0,
            "heat_capacity": 0.0,
            "T_eff": 0.0,
            "temperature": 0.0,
            "phase_coherence": 0.0,
            "interference_strength": 0.0,
            "attention_magnitude_mean": 0.0,
            "attention_phase_std": 0.0,
        }
        for layer in self.layers:
            attn = layer.attention
            state["entropy"] += attn.entropy
            state["heat_capacity"] += attn.heat_capacity
            state["T_eff"] += attn.t_eff
            state["temperature"] += attn.temperature.item()
            state["phase_coherence"] += attn.phase_coherence
            state["interference_strength"] += attn.interference_strength
            state["attention_magnitude_mean"] += attn.attention_magnitude_mean
            state["attention_phase_std"] += attn.attention_phase_std
        for key in state:
            state[key] /= max(n_layers, 1)
        return state

    def get_complex_weight_statistics(self) -> Dict[str, float]:
        all_real = []
        all_imag = []
        for name, param in self.named_parameters():
            if "weight_real" in name:
                all_real.append(param.detach().flatten())
            elif "weight_imag" in name:
                all_imag.append(param.detach().flatten())

        if not all_real or not all_imag:
            return {
                "complex_modulus_mean": 0.0,
                "complex_modulus_std": 0.0,
                "complex_phase_mean": 0.0,
                "complex_phase_std": 0.0,
                "complex_phase_entropy": 0.0,
            }

        wr = torch.cat(all_real)
        wi = torch.cat(all_imag)
        modulus = torch.sqrt(wr ** 2 + wi ** 2 + 1e-10)
        phase = torch.atan2(wi, wr + 1e-10)

        phase_hist = torch.histc(phase, bins=self.config.phase_coherence_bins,
                                 min=-math.pi, max=math.pi)
        phase_prob = phase_hist / (phase_hist.sum() + 1e-10)
        phase_entropy = -torch.sum(
            phase_prob * torch.log(phase_prob + self.config.numerical_epsilon)
        ).item()

        return {
            "complex_modulus_mean": modulus.mean().item(),
            "complex_modulus_std": modulus.std().item(),
            "complex_phase_mean": phase.mean().item(),
            "complex_phase_std": phase.std().item(),
            "complex_phase_entropy": phase_entropy,
        }


# ---------------------------------------------------------------------------
# Dataset Creation (Single Responsibility)
# ---------------------------------------------------------------------------

class ModularAdditionDatasetFactory:
    @staticmethod
    def create(
        modulus: int = 26,
        train_fraction: float = 0.5
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        all_pairs = []
        all_results = []
        for a in range(modulus):
            for b in range(modulus):
                pair = [a + 1, modulus, b + 1, modulus + 1]
                result = (a + b) % modulus + 1
                all_pairs.append(pair)
                all_results.append(result)

        all_pairs = torch.tensor(all_pairs, dtype=torch.long)
        all_results = torch.tensor(all_results, dtype=torch.long)

        indices = torch.randperm(len(all_pairs))
        all_pairs = all_pairs[indices]
        all_results = all_results[indices]

        n_train = int(len(all_pairs) * train_fraction)
        return (
            all_pairs[:n_train],
            all_results[:n_train],
            all_pairs[n_train:],
            all_results[n_train:],
        )


# ---------------------------------------------------------------------------
# Training and Evaluation Primitives (Single Responsibility)
# ---------------------------------------------------------------------------

class TrainingPrimitives:
    @staticmethod
    def train_epoch(
        model: ComplexLeiblerTransformer,
        train_x: torch.Tensor,
        train_y: torch.Tensor,
        optimizer: optim.Optimizer,
        config: ProspectorConfig,
        device: torch.device,
    ) -> float:
        model.train()
        total_loss = 0.0
        n_batches = 0
        n_samples = len(train_x)
        indices = torch.randperm(n_samples)

        for i in range(0, n_samples, config.batch_size):
            batch_indices = indices[i : i + config.batch_size]
            batch_x = train_x[batch_indices].to(device)
            batch_y = train_y[batch_indices].to(device)

            logits = model(batch_x)
            loss = F.cross_entropy(logits[:, -1, :], batch_y)

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), config.gradient_clip)
            optimizer.step()

            total_loss += loss.item()
            n_batches += 1

        return total_loss / max(n_batches, 1)

    @staticmethod
    @torch.no_grad()
    def evaluate(
        model: ComplexLeiblerTransformer,
        test_x: torch.Tensor,
        test_y: torch.Tensor,
        config: ProspectorConfig,
        device: torch.device,
    ) -> Tuple[float, float]:
        model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        n_samples = len(test_x)

        for i in range(0, n_samples, config.batch_size):
            batch_x = test_x[i : i + config.batch_size].to(device)
            batch_y = test_y[i : i + config.batch_size].to(device)
            logits = model(batch_x)
            loss = F.cross_entropy(logits[:, -1, :], batch_y)
            total_loss += loss.item() * len(batch_x)
            predictions = torch.argmax(logits[:, -1, :], dim=-1)
            correct += (predictions == batch_y).sum().item()
            total += len(batch_x)

        return total_loss / max(total, 1), correct / max(total, 1)


# ---------------------------------------------------------------------------
# Metric Calculators (Open/Closed Principle: each calculator is independent)
# ---------------------------------------------------------------------------

class DeltaCalculator(IMetricCalculator):
    def __init__(self, config: ProspectorConfig):
        self.config = config

    def calculate(self, model: ComplexLeiblerTransformer, **kwargs) -> Dict[str, float]:
        all_weights = []
        for layer in model.layers:
            attn = layer.attention
            for proj in [attn.q_proj, attn.k_proj, attn.v_proj, attn.o_proj]:
                all_weights.append(proj.weight_real.detach().flatten())
                all_weights.append(proj.weight_imag.detach().flatten())
        weights = torch.cat(all_weights)
        rounded = torch.round(weights)
        delta = torch.abs(weights - rounded).max().item()
        alpha = -np.log(delta + self.config.log_floor) if delta > 0 else 20.0
        return {"delta": delta, "alpha_purity": alpha}


class KappaCalculator:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.gradient_buffer: Deque[torch.Tensor] = deque(maxlen=config.kappa_window_size)
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

    def calculate(
        self,
        model: ComplexLeiblerTransformer,
        gradient_covariance: Optional[torch.Tensor] = None,
        **kwargs,
    ) -> Dict[str, float]:
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

    def calculate(
        self,
        model: ComplexLeiblerTransformer,
        train_x: torch.Tensor,
        train_y: torch.Tensor,
        device: torch.device,
        **kwargs,
    ) -> Dict[str, float]:
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
        flat_params = torch.cat([p.data.flatten() for p in model.parameters()])
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

    def calculate(self, model: ComplexLeiblerTransformer, **kwargs) -> Dict[str, float]:
        device = next(model.parameters()).device
        theta = torch.cat([p.detach().flatten() for p in model.parameters()])
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
            feature_var / (feature_norms.mean().item() + self.config.numerical_epsilon)
        )
        effective_features = active * (1.0 - recon_error)
        return {
            "superposition_psi": psi,
            "superposition_F": effective_features,
            "superposition_active_fraction": active / max(total, 1),
        }


class GravitationalConstantCalculator(IMetricCalculator):
    def __init__(self, config: ProspectorConfig):
        self.config = config

    def calculate(self, model: ComplexLeiblerTransformer, **kwargs) -> Dict[str, float]:
        g_alg = 0.0
        count = 0
        for p in model.parameters():
            if p.grad is not None:
                g_alg += torch.mean(p.grad.detach() ** 2).item()
                count += 1
        g_alg = g_alg / max(count, 1)
        return {"G_alg": g_alg}


class ComplexPhaseMetricsCalculator(IMetricCalculator):
    def __init__(self, config: ProspectorConfig):
        self.config = config

    def calculate(self, model: ComplexLeiblerTransformer, **kwargs) -> Dict[str, float]:
        return model.get_complex_weight_statistics()


# ---------------------------------------------------------------------------
# Phase Detection (Single Responsibility)
# ---------------------------------------------------------------------------

class PhaseDetector(IPhaseDetector):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.current_phase = "unknown"
        self.phase_history: List[Tuple[int, str]] = []

    def detect(self, metrics: Dict[str, float]) -> str:
        kappa = metrics.get("kappa", float("inf"))
        delta = metrics.get("delta", 0.5)
        t_eff = metrics.get("T_eff_gradient", 1.0)
        test_acc = metrics.get("test_acc", 0.0)
        phase_coherence = metrics.get("phase_coherence", 0.0)

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
                f"{self.current_phase} -> {phase} "
                f"(phase_coh={phase_coherence:.4f}) ***"
            )
            self.current_phase = phase
            self.phase_history.append((epoch, phase))
        return phase


# ---------------------------------------------------------------------------
# Adaptive Annealing Scheduler (Single Responsibility)
# ---------------------------------------------------------------------------

class AdaptiveAnnealingScheduler:
    def __init__(
        self,
        model: ComplexLeiblerTransformer,
        config: ProspectorConfig,
        optimizer: optim.Optimizer,
    ):
        self.model = model
        self.config = config
        self.optimizer = optimizer
        self.current_temperature = config.t_max
        self.base_temperature = config.t_max
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
            target_temp = self.config.t_min
            target_wd = self.config.weight_decay_crystal
        elif phase == "glass":
            target_temp = self.config.t_min
            target_wd = self.config.weight_decay_glass
        elif phase == "liquid":
            progress = min(epoch / self.config.grokking_epochs, 1.0)
            target_temp = self.config.t_min + (self.config.t_max - self.config.t_min) * (1.0 - progress)
            target_wd = self.config.weight_decay_liquid
        else:
            if epoch < self.config.warmup_epochs:
                warmup_progress = epoch / max(self.config.warmup_epochs, 1)
                target_temp = self.config.t_max * (1.0 - warmup_progress * 0.3)
            else:
                cool = epoch - self.config.warmup_epochs
                decay = np.exp(-self.config.cooling_rate * cool)
                target_temp = self.config.t_min + (self.config.t_max - self.config.t_min) * decay
            target_wd = self.config.weight_decay_gas

        sf = self.config.smoothing_factor
        self.base_temperature = self.base_temperature * sf + target_temp * (1.0 - sf)
        self.current_weight_decay = self.current_weight_decay * sf + target_wd * (1.0 - sf)
        self.current_temperature = max(
            self.config.t_min, min(self.config.t_max, self.base_temperature)
        )
        self._update_model_temperatures()
        self._update_optimizer_weight_decay()

    def _update_model_temperatures(self) -> None:
        for layer in self.model.layers:
            layer.attention.temperature.data.fill_(self.current_temperature)

    def _update_optimizer_weight_decay(self) -> None:
        for group in self.optimizer.param_groups:
            group["weight_decay"] = self.current_weight_decay


# ---------------------------------------------------------------------------
# Glass Detector (Single Responsibility)
# ---------------------------------------------------------------------------

class GlassDetector(IGlassDetector):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.metrics_buffer: Deque[Dict[str, float]] = deque(maxlen=config.glass_patience_epochs)

    def should_stop(self, epoch: int, metrics: Dict[str, float]) -> Tuple[bool, str]:
        self.metrics_buffer.append({
            "epoch": epoch,
            "delta": metrics.get("delta", float("inf")),
            "test_acc": metrics.get("test_acc", 0.0),
            "kappa": metrics.get("kappa", float("inf")),
        })
        if epoch < self.config.glass_patience_epochs:
            return False, "warming_up"
        recent = list(self.metrics_buffer)[-self.config.glass_patience_epochs:]
        avg_delta = np.mean([m["delta"] for m in recent])
        avg_acc = np.mean([m["test_acc"] for m in recent])
        if avg_delta > self.config.glass_delta_ceiling and recent[-1]["delta"] > self.config.glass_delta_ceiling:
            return True, f"delta_stuck_high ({avg_delta:.4f})"
        if avg_acc < self.config.glass_accuracy_floor and recent[-1]["test_acc"] < self.config.glass_accuracy_floor:
            return True, f"accuracy_stuck_low ({avg_acc:.4f})"
        if len(recent) > 10:
            recent_k = [
                m["kappa"] for m in recent[-10:]
                if m["kappa"] != float("inf")
            ]
            if (
                len(recent_k) >= 10
                and all(recent_k[i] < recent_k[i + 1] for i in range(len(recent_k) - 1))
                and recent_k[-1] > self.config.glass_kappa_divergence_threshold
            ):
                return True, f"kappa_diverging ({recent_k[-1]:.1f})"
        return False, ""


# ---------------------------------------------------------------------------
# Grokking Detector (Single Responsibility)
# ---------------------------------------------------------------------------

class GrokkinDetector(IGrokkinDetector):
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
            print(f"Test accuracy: {self.prev_test_acc:.4f} -> {test_acc:.4f}")
            print(f"Stability confirmed over {self.config.grokking_stability_required} epochs")
            print("=" * 80 + "\n")
        self.prev_test_acc = test_acc
        return self.detected


# ---------------------------------------------------------------------------
# Checkpoint Manager (Single Responsibility)
# ---------------------------------------------------------------------------

class CheckpointManager(ICheckpointManager):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.checkpoint_dir = Path(config.checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.last_checkpoint_time = time.time()

    def save(self, state: Dict[str, Any], path: Optional[str] = None) -> str:
        if path is None:
            path = str(self.checkpoint_dir / self.config.latest_checkpoint_name)
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


# ---------------------------------------------------------------------------
# Pruning and Discretization (Single Responsibility)
# ---------------------------------------------------------------------------

class ModelPruner:
    @staticmethod
    def prune(model: ComplexLeiblerTransformer, threshold: float = 0.1) -> int:
        print(f"\nPruning slots with magnitude < {threshold}...")
        slots_remaining = 0
        for layer in model.layers:
            attn = layer.attention
            for proj in [attn.q_proj, attn.k_proj, attn.v_proj, attn.o_proj]:
                with torch.no_grad():
                    magnitude = torch.sqrt(
                        proj.weight_real ** 2 + proj.weight_imag ** 2
                    )
                    mask = magnitude.abs() > threshold
                    proj.weight_real.data *= mask.float()
                    proj.weight_imag.data *= mask.float()
                    slots_remaining += mask.sum().item()
        print(f"Pruning complete. Active slots: {slots_remaining}")
        return slots_remaining


class ModelDiscretizer:
    @staticmethod
    def discretize(model: ComplexLeiblerTransformer, tolerance: float = 0.1) -> bool:
        print(f"\nAttempting discretization with tolerance {tolerance}...")
        can_discretize = True
        for layer in model.layers:
            attn = layer.attention
            for name, proj in [
                ("q_proj", attn.q_proj),
                ("k_proj", attn.k_proj),
                ("v_proj", attn.v_proj),
                ("o_proj", attn.o_proj),
            ]:
                for weight_name, param in [
                    (f"{name}.weight_real", proj.weight_real),
                    (f"{name}.weight_imag", proj.weight_imag),
                ]:
                    rounded = torch.round(param.data)
                    distance = torch.abs(param.data - rounded).max().item()
                    if distance > tolerance:
                        print(f"Cannot discretize {weight_name}: max distance {distance:.4f} > {tolerance}")
                        can_discretize = False
                    else:
                        param.data = rounded
        if can_discretize:
            print("Discretization successful!")
        else:
            print("Discretization failed - weights not close enough to integers")
        return can_discretize


# ---------------------------------------------------------------------------
# Complex Phase Loss Component (Single Responsibility)
# ---------------------------------------------------------------------------

class ComplexPhaseLoss(ILossComponent):
    def __init__(self, config: ProspectorConfig):
        self.config = config

    def compute(
        self,
        model: ComplexLeiblerTransformer,
        loss_ce: torch.Tensor,
        epoch: int,
        **kwargs,
    ) -> torch.Tensor:
        phase_reg = torch.tensor(0.0, device=loss_ce.device)
        interference_reg = torch.tensor(0.0, device=loss_ce.device)
        count = 0
        for layer in model.layers:
            attn = layer.attention
            if attn.scores_real is not None and attn.scores_imag is not None:
                phase = ComplexOperations.compute_phase(attn.scores_real, attn.scores_imag)
                phase_var = phase.var()
                phase_reg = phase_reg + phase_var

                constructive = torch.cos(phase).mean()
                interference_reg = interference_reg - constructive
                count += 1

        if count > 0:
            phase_reg = phase_reg / count
            interference_reg = interference_reg / count

        total = loss_ce
        total = total + self.config.phase_regularization_weight * phase_reg
        total = total + self.config.interference_loss_weight * interference_reg
        return total


# ---------------------------------------------------------------------------
# Comprehensive Metrics Aggregator (Single Responsibility)
# ---------------------------------------------------------------------------

class ComprehensiveMetricsAggregator:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.delta_calc = DeltaCalculator(config)
        self.kappa_calc = KappaCalculator(config)
        self.thermo_calc = ThermodynamicMetricsCalculator(config)
        self.lc_calc = LocalComplexityCalculator(config)
        self.sp_calc = SuperpositionCalculator(config)
        self.grav_calc = GravitationalConstantCalculator(config)
        self.complex_phase_calc = ComplexPhaseMetricsCalculator(config)
        self._gradient_covariance: Optional[torch.Tensor] = None

    def compute_all(
        self,
        model: ComplexLeiblerTransformer,
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
        metrics["phase_coherence"] = thermo_state["phase_coherence"]
        metrics["interference_strength"] = thermo_state["interference_strength"]
        metrics["attention_magnitude_mean"] = thermo_state["attention_magnitude_mean"]
        metrics["attention_phase_std"] = thermo_state["attention_phase_std"]

        metrics["weight_decay"] = scheduler.current_weight_decay
        metrics["scheduler_temperature"] = scheduler.current_temperature

        delta_m = self.delta_calc.calculate(model)
        metrics.update(delta_m)

        if force_kappa or epoch % self.config.kappa_calculation_freq == 0:
            kappa = self.kappa_calc.calculate_kappa()
            metrics["kappa"] = kappa
            metrics["kappa_trend"] = (
                1.0 if self.kappa_calc.get_kappa_trend() == "decreasing"
                else (-1.0 if self.kappa_calc.get_kappa_trend() == "increasing" else 0.0)
            )
            metrics["is_crystallizing"] = float(self.kappa_calc.is_crystallizing())
            self._gradient_covariance = self.kappa_calc.get_gradient_covariance()
        else:
            metrics["kappa"] = (
                self.kappa_calc.kappa_history[-1]
                if self.kappa_calc.kappa_history
                else float("inf")
            )
            metrics["kappa_trend"] = 0.0
            metrics["is_crystallizing"] = float(self.kappa_calc.is_crystallizing())

        thermo_m = self.thermo_calc.calculate(model, gradient_covariance=self._gradient_covariance)
        metrics.update(thermo_m)

        grav_m = self.grav_calc.calculate(model)
        metrics.update(grav_m)

        complex_m = self.complex_phase_calc.calculate(model)
        metrics.update(complex_m)

        if force_lc and train_x is not None and train_y is not None and device is not None:
            lc_m = self.lc_calc.calculate(model, train_x=train_x, train_y=train_y, device=device)
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


# ---------------------------------------------------------------------------
# Display Formatting Utilities
# ---------------------------------------------------------------------------

class DisplayFormatter:
    @staticmethod
    def format_kappa(kappa: float, max_display: float = 1e6) -> str:
        if kappa == float("inf") or kappa > max_display:
            return "     inf"
        return f"{kappa:8.2f}"

    @staticmethod
    def format_lc(lc: float) -> str:
        if lc == -math.inf:
            return "   -inf"
        if lc == math.inf:
            return "    inf"
        return f"{lc:>7.2f}"


# ---------------------------------------------------------------------------
# Prospector Phase (Single Responsibility)
# ---------------------------------------------------------------------------

class ProspectorPhase(ITrainingPhase):
    def __init__(self, config: ProspectorConfig, seed: int):
        self.config = config
        self.seed = seed

    def execute(
        self,
        model: ComplexLeiblerTransformer,
        **kwargs,
    ) -> Tuple[bool, Dict[str, Any]]:
        train_x = kwargs["train_x"]
        train_y = kwargs["train_y"]
        test_x = kwargs["test_x"]
        test_y = kwargs["test_y"]
        device = kwargs["device"]

        aggregator = ComprehensiveMetricsAggregator(self.config)
        phase_detector = PhaseDetector(self.config)
        glass_detector = GlassDetector(self.config)
        grokking_detector = GrokkinDetector(self.config)
        phase_loss = ComplexPhaseLoss(self.config)

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
            total_loss = 0.0
            n_batches = 0
            n_samples = len(train_x)
            indices = torch.randperm(n_samples)

            for i in range(0, n_samples, self.config.batch_size):
                batch_indices = indices[i : i + self.config.batch_size]
                batch_x = train_x[batch_indices].to(device)
                batch_y = train_y[batch_indices].to(device)

                logits = model(batch_x)
                loss_ce = F.cross_entropy(logits[:, -1, :], batch_y)
                loss = phase_loss.compute(model, loss_ce, epoch)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.config.gradient_clip)
                optimizer.step()
                total_loss += loss.item()
                n_batches += 1

            train_loss = total_loss / max(n_batches, 1)
            aggregator.accumulate_gradient(model)

            test_loss, test_acc = TrainingPrimitives.evaluate(
                model, test_x, test_y, self.config, device
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
                        f"kappa={DisplayFormatter.format_kappa(metrics['kappa'])} "
                        f"S={metrics['entropy']:.3f} "
                        f"C_v={metrics['heat_capacity']:.2e} "
                        f"T_eff={metrics['T_eff_gradient']:.2e} "
                        f"h_bar={metrics['h_bar_eff']:.2e} "
                        f"G_alg={metrics['G_alg']:.4f} "
                        f"PhCoh={metrics['phase_coherence']:.4f} "
                        f"Interf={metrics['interference_strength']:.4f} "
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
                fast_delta = self.config
                delta_calc = DeltaCalculator(self.config)
                fast_delta_m = delta_calc.calculate(model)
                scheduler.step({
                    "test_acc": test_acc,
                    "epoch": epoch,
                    "phase": phase_detector.current_phase,
                    "delta": fast_delta_m["delta"],
                    "kappa": (
                        aggregator.kappa_calc.kappa_history[-1]
                        if aggregator.kappa_calc.kappa_history
                        else float("inf")
                    ),
                    "T_eff_gradient": 0.0,
                })

            if epoch % self.config.glass_check_interval == 0 and history:
                is_glass, reason = glass_detector.should_stop(epoch, history[-1])
                if is_glass:
                    print(f" [-] GLASS DETECTED: {reason}")
                    print(f"     Best delta was {best_delta:.4f} at epoch {best_epoch}")
                    return False, {
                        "delta": best_delta,
                        "best_epoch": best_epoch,
                        "metrics_history": history,
                    }

        print(f" [-] Max epochs reached. Best delta: {best_delta:.4f} at epoch {best_epoch}")
        return False, {
            "delta": best_delta,
            "best_epoch": best_epoch,
            "metrics_history": history,
        }


# ---------------------------------------------------------------------------
# Long Training Phase (Single Responsibility)
# ---------------------------------------------------------------------------

class LongTrainingPhase(ITrainingPhase):
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.history: List[Dict[str, float]] = []

    def execute(
        self,
        model: ComplexLeiblerTransformer,
        **kwargs,
    ) -> ComplexLeiblerTransformer:
        train_x = kwargs["train_x"]
        train_y = kwargs["train_y"]
        test_x = kwargs["test_x"]
        test_y = kwargs["test_y"]
        device = kwargs["device"]
        checkpoint_manager = kwargs.get("checkpoint_manager")

        aggregator = ComprehensiveMetricsAggregator(self.config)
        phase_detector = PhaseDetector(self.config)
        grokking_detector = GrokkinDetector(self.config)
        phase_loss = ComplexPhaseLoss(self.config)

        optimizer = optim.AdamW(
            model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay_initial,
        )
        scheduler = AdaptiveAnnealingScheduler(model, self.config, optimizer)

        print("\n" + "=" * 120)
        print("PHASE 1: COMPLEX THERMODYNAMIC TRAINING WITH PHASE INTERFERENCE")
        print("=" * 120)
        print(f"Pressure (WD): {self.config.weight_decay_initial} (adaptive by phase)")
        print(f"Batch size: {self.config.batch_size}")
        print(f"Kappa calculated every {self.config.kappa_calculation_freq} epochs")
        print(f"Target: kappa->1, delta->0, T_eff->0, Acc->1.0, PhaseCoherence->1.0")
        print("=" * 120)

        header = (
            f"{'Epoch':>7} | {'Loss':>9} | {'tLoss':>9} | {'Acc':>6} | "
            f"{'delta':>7} | {'kappa':>8} | {'S':>6} | {'C_v':>9} | "
            f"{'T_eff':>9} | {'h_bar':>9} | {'G_alg':>7} | "
            f"{'PhCoh':>6} | {'Interf':>7} | {'PhStd':>6} | "
            f"{'|W|':>7} | {'|g|':>9} | {'WD':>8} | {'Phase':>5}"
        )
        print(header)
        print("-" * len(header))

        crystallization_counter = 0

        for epoch in range(1, self.config.train_epochs + 1):
            model.train()
            total_loss = 0.0
            n_batches = 0
            n_samples = len(train_x)
            indices = torch.randperm(n_samples)

            for i in range(0, n_samples, self.config.batch_size):
                batch_indices = indices[i : i + self.config.batch_size]
                batch_x = train_x[batch_indices].to(device)
                batch_y = train_y[batch_indices].to(device)

                logits = model(batch_x)
                loss_ce = F.cross_entropy(logits[:, -1, :], batch_y)
                loss = phase_loss.compute(model, loss_ce, epoch)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.config.gradient_clip)
                optimizer.step()
                total_loss += loss.item()
                n_batches += 1

            train_loss = total_loss / max(n_batches, 1)
            aggregator.accumulate_gradient(model)

            test_loss, test_acc = TrainingPrimitives.evaluate(
                model, test_x, test_y, self.config, device
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
                    f"{DisplayFormatter.format_kappa(metrics['kappa'])} | "
                    f"{metrics['entropy']:>6.3f} | "
                    f"{metrics['heat_capacity']:>9.2e} | "
                    f"{metrics['T_eff_gradient']:>9.2e} | "
                    f"{metrics['h_bar_eff']:>9.2e} | "
                    f"{metrics['G_alg']:>7.4f} | "
                    f"{metrics['phase_coherence']:>6.4f} | "
                    f"{metrics['interference_strength']:>7.4f} | "
                    f"{metrics['attention_phase_std']:>6.4f} | "
                    f"{weight_norm:>7.2f} | "
                    f"{grad_norm:>9.2e} | "
                    f"{scheduler.current_weight_decay:>8.1e} | "
                    f"{phase[:5]:>5}"
                )

                if force_lc:
                    print(
                        f"        LC={DisplayFormatter.format_lc(metrics.get('local_complexity', 0.0))} "
                        f"psi={metrics.get('superposition_psi', 0.0):.3f} "
                        f"F={metrics.get('superposition_F', 0.0):.1f} "
                        f"alpha={metrics.get('alpha_purity', 0.0):.2f} "
                        f"cmMean={metrics.get('complex_modulus_mean', 0.0):.4f} "
                        f"cmStd={metrics.get('complex_modulus_std', 0.0):.4f} "
                        f"cphEnt={metrics.get('complex_phase_entropy', 0.0):.4f}"
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
                                    checkpoint_manager.checkpoint_dir / "crystallized.pt"
                                ),
                            )
                        return model
                else:
                    if crystallization_counter > 0:
                        print(f"  [RESET] Phase reverted to {phase}, counter reset")
                    crystallization_counter = 0

                if checkpoint_manager is not None and checkpoint_manager.should_checkpoint():
                    cp_path = checkpoint_manager.save({
                        "epoch": epoch,
                        "model_state_dict": model.state_dict(),
                        "optimizer_state_dict": optimizer.state_dict(),
                        "history": self.history,
                        "phase": phase,
                        "timestamp": datetime.now().isoformat(),
                    })
                    print(f"  [CHECKPOINT] {cp_path}")
            else:
                delta_calc = DeltaCalculator(self.config)
                fast_delta = delta_calc.calculate(model)
                scheduler.step({
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
                })

        if checkpoint_manager is not None:
            checkpoint_manager.save({
                "epoch": self.config.train_epochs,
                "model_state_dict": model.state_dict(),
                "history": self.history,
                "phase": phase_detector.current_phase,
                "timestamp": datetime.now().isoformat(),
                "training_completed": True,
            })
        return model


# ---------------------------------------------------------------------------
# Seed Prospector (Single Responsibility)
# ---------------------------------------------------------------------------

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

        print(f"\nStarting complex transformer seed prospecting with {total_attempts} attempts")
        print(f"Target: delta < {self.config.delta_crystal_threshold}, "
              f"Acc > {self.config.grokking_threshold}, "
              f"kappa < {self.config.kappa_crystal_threshold}")
        print(f"Batch size: {self.config.batch_size}")
        print(f"Device: {device}")

        results_log: List[Dict[str, Any]] = []

        for i in range(start_seed, start_seed + total_attempts):
            seed = i
            attempt = i - start_seed + 1
            print(f"\n{'=' * 60}")
            print(f"[*] MINING SEED {seed} ({attempt}/{total_attempts})")
            print(f"{'=' * 60}")

            SeedManager.set_seed(seed, self.config.device)

            train_x, train_y, test_x, test_y = ModularAdditionDatasetFactory.create(
                modulus=self.config.modulus,
                train_fraction=self.config.train_fraction,
            )
            train_x = train_x.to(device)
            train_y = train_y.to(device)
            test_x = test_x.to(device)
            test_y = test_y.to(device)

            model = ComplexLeiblerTransformer(self.config).to(device)
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
                k: v for k, v in final_metrics.items() if k != "metrics_history"
            }
            with open(seed_path, "w") as f:
                json.dump(
                    {"seed": seed, "is_crystal": is_crystal, "metrics": safe_metrics},
                    f, indent=2, default=str,
                )

            if "metrics_history" in final_metrics:
                hist_path = self.results_dir / f"seed_{seed:05d}_history.json"
                with open(hist_path, "w") as f:
                    json.dump(final_metrics["metrics_history"], f, indent=2, default=str)

            if is_crystal:
                print(f"\n{'=' * 60}")
                print(f"[+] CRYSTAL FOUND -- Seed {seed}")
                print(f"{'=' * 60}")
                print(f"  delta: {final_metrics.get('delta', 'N/A')}")
                print(f"  kappa: {final_metrics.get('kappa', 'N/A')}")
                print(f"  test_acc: {final_metrics.get('test_acc', 'N/A')}")
                print(f"  alpha_purity: {final_metrics.get('alpha_purity', 'N/A')}")
                print(f"  phase_coherence: {final_metrics.get('phase_coherence', 'N/A')}")
                crystal_path = (
                    self.crystal_dir
                    / f"crystal_seed_{seed}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pt"
                )
                torch.save({
                    "seed": seed,
                    "model_state_dict": model.state_dict(),
                    "metrics": safe_metrics,
                    "config": self.config,
                }, crystal_path)
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


# ---------------------------------------------------------------------------
# Long Training Pipeline (Single Responsibility)
# ---------------------------------------------------------------------------

class LongTrainingPipeline:
    def __init__(self, config: ProspectorConfig):
        self.config = config
        self.checkpoint_manager = CheckpointManager(config)
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.interrupted = False
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame) -> None:
        print("\n\n[INFO] Interrupt received. Will save checkpoint at next opportunity...")
        self.interrupted = True

    def run(
        self,
        resume_from: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> bool:
        config = self.config
        device = torch.device(config.device)

        print("\n" + "=" * 80)
        print("  COMPLEX-VALUED LEIBLER TRANSFORMER CRYSTALLIZATION FRAMEWORK")
        print("  Thermodynamic Phase Transition via Complex Interference")
        print("=" * 80)
        print(f"Device: {device}")
        print(f"Architecture: d_model={config.d_model}, n_heads={config.n_heads}, "
              f"n_layers={config.n_layers}, d_ff={config.d_ff}")
        print(f"Complex expansion factor: {config.complex_expansion_factor}")
        print(f"Task: modular addition mod {config.modulus}")
        print(f"Batch size: {config.batch_size}")
        print(f"Weight decay: {config.weight_decay_initial} (adaptive)")
        print(f"Kappa threshold: {config.kappa_crystal_threshold}")
        print(f"Delta target: {config.delta_crystal_threshold}")
        print(f"Phase regularization: {config.phase_regularization_weight}")
        print(f"Interference loss weight: {config.interference_loss_weight}")
        print("=" * 80)

        if seed is not None:
            SeedManager.set_seed(seed, config.device)
            print(f"Using seed: {seed}")

        train_x, train_y, test_x, test_y = ModularAdditionDatasetFactory.create(
            modulus=config.modulus, train_fraction=config.train_fraction
        )
        train_x = train_x.to(device)
        train_y = train_y.to(device)
        test_x = test_x.to(device)
        test_y = test_y.to(device)
        print(f"Train: {len(train_x)}, Test: {len(test_x)}")

        model = ComplexLeiblerTransformer(config).to(device)
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
            checkpoint_manager=self.checkpoint_manager,
        )

        if self.interrupted:
            return False

        print("\n" + "=" * 80)
        print("PHASE 2: PRUNING AND DISCRETIZATION")
        print("=" * 80 + "\n")

        n_slots = ModelPruner.prune(model, threshold=config.pruning_threshold)
        print(f"Model pruned to {n_slots} active weight elements")

        discretized = ModelDiscretizer.discretize(model, tolerance=config.discretization_tolerance)

        test_loss, test_acc = TrainingPrimitives.evaluate(
            model, test_x, test_y, config, device
        )
        delta_calc = DeltaCalculator(config)
        delta_m = delta_calc.calculate(model)

        print(f"\nPost-discretization test accuracy: {test_acc:.4f}")
        print(f"Post-discretization delta: {delta_m['delta']:.6f}")
        print(f"Discretization success: {discretized}")

        complex_stats = model.get_complex_weight_statistics()
        print(f"Complex modulus mean: {complex_stats['complex_modulus_mean']:.6f}")
        print(f"Complex phase entropy: {complex_stats['complex_phase_entropy']:.6f}")

        torch.save({
            "model_state_dict": model.state_dict(),
            "test_acc": test_acc,
            "delta": delta_m["delta"],
            "discretized": discretized,
            "history": phase1.history,
            "config": config,
            "complex_stats": complex_stats,
            "timestamp": datetime.now().isoformat(),
        }, self.output_dir / "final_model.pt")

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


# ---------------------------------------------------------------------------
# Application Entry Point (Single Responsibility)
# ---------------------------------------------------------------------------

class Application:
    def __init__(self):
        self.parser = self._create_argument_parser()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Complex-Valued Leibler Transformer Seed Prospector",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Modes:
  prospect    Fast seed mining using delta as primary compass
  train       Long-term training with full thermodynamic monitoring

Examples:
  python complex_leibler_transformer.py prospect --attempts 100 --start-seed 1
  python complex_leibler_transformer.py train --seed 42 --epochs 25000
  python complex_leibler_transformer.py train --resume checkpoints_complex_transformer/latest.pt
            """,
        )
        parser.add_argument("mode", type=str, choices=["prospect", "train"], help="Execution mode")
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
        parser.add_argument("--complex-expansion-factor", type=float, default=None)
        parser.add_argument("--phase-reg-weight", type=float, default=None)
        parser.add_argument("--interference-loss-weight", type=float, default=None)
        parser.add_argument("--device", type=str, default=None)
        return parser

    def run(self) -> None:
        args = self.parser.parse_args()

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
        if args.complex_expansion_factor is not None:
            overrides["complex_expansion_factor"] = args.complex_expansion_factor
        if args.phase_reg_weight is not None:
            overrides["phase_regularization_weight"] = args.phase_reg_weight
        if args.interference_loss_weight is not None:
            overrides["interference_loss_weight"] = args.interference_loss_weight
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


def main():
    app = Application()
    app.run()


if __name__ == "__main__":
    main()