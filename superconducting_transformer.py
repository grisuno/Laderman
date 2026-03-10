#!/usr/bin/env python3
"""
Superconducting Attention Transformer with Spontaneous Symmetry Breaking
=========================================================================

The Neuronal Higgs Mechanism: Inducing spontaneous symmetry breaking in
Transformers to achieve algorithmic superconductivity.

Core innovations:
  1. Sparsemax replaces Softmax -- allows exact hard zeros in attention,
     creating the vacuum the crystal needs.
  2. Topological Gating -- learnable gates that enforce discrete routing,
     measuring information pathway uniqueness.
  3. Chemical Potential (mu) -- an energy cost for maintaining active weights.
     Low mu during exploration (liquid phase), high mu as accuracy rises,
     forcing the network to eject noise by internal pressure rather than
     external pruning.
  4. Cooper Pair Coherence (Psi) -- measures phase coherence between layer
     pairs, detecting the formation of exact algorithmic routes.
  5. Quantum Annealing Protocol -- smooth thermodynamic schedule that
     transitions from hot gas through liquid to superconducting crystal.

Theoretical Framework (from Preprint + Extensions):
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
  - Psi_cooper: Cooper pair coherence between adjacent layers
  - mu_eff: effective chemical potential (weight maintenance cost)
  - sparsity_ratio: fraction of exact zeros in attention
  - resistance: attention entropy (analog of electrical resistance)
  - conductance: 1/resistance (analog of superconducting order parameter)
  - gap_energy: energy gap between active and pruned weight populations
  - topological_charge: winding number of gate activations
  - meissner_fraction: fraction of weights expelled from the interior

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
from dataclasses import dataclass, replace
from typing import Dict, List, Tuple, Optional, Any, Deque
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime
from enum import Enum

warnings.filterwarnings("ignore")


class ExecutionMode(Enum):
    PROSPECT = "prospect"
    TRAIN = "train"


@dataclass(frozen=True)
class SuperconductorConfig:

    d_model: int = 64
    n_heads: int = 4
    n_layers: int = 2
    d_ff: int = 256
    dropout: float = 0.1

    modulus: int = 26
    vocab_size: int = 28
    max_seq_len: int = 5
    train_fraction: float = 0.5

    t_min: float = 0.01
    t_max: float = 2.0
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

    checkpoint_interval_minutes: float = 5.0
    checkpoint_dir: str = "checkpoints_superconductor"
    latest_checkpoint_name: str = "latest.pt"
    crystal_dir: str = "crystal_seeds_superconductor"
    output_dir: str = "outputs_superconductor"
    prospector_results_dir: str = "prospector_results_superconductor"

    smoothing_factor: float = 0.95

    sparsemax_initial_lambda: float = 1.0
    sparsemax_lambda_growth_rate: float = 0.001

    mu_initial: float = 0.0
    mu_max: float = 1.0
    mu_onset_accuracy: float = 0.3
    mu_ramp_accuracy: float = 0.9
    mu_exponent: float = 3.0

    gate_init_bias: float = 0.5
    gate_temperature_initial: float = 1.0
    gate_temperature_min: float = 0.01
    gate_temperature_decay_rate: float = 0.001
    gate_l0_regularization_weight: float = 0.01
    gate_topological_regularization_weight: float = 0.005

    cooper_pair_loss_weight: float = 0.01
    cooper_pair_threshold: float = 0.8

    resistance_loss_weight: float = 0.01

    gap_energy_percentile_low: float = 10.0
    gap_energy_percentile_high: float = 90.0

    meissner_threshold: float = 0.01

    weight_init_std: float = 0.02

    numerical_epsilon: float = 1e-10
    log_floor: float = 1e-15
    max_kappa_display: float = 1e6
    phase_coherence_bins: int = 64

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


class IAttentionMechanism(ABC):
    @abstractmethod
    def forward(self, scores: torch.Tensor) -> torch.Tensor:
        pass


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


class SparsemaxFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input_tensor: torch.Tensor, dim: int = -1) -> torch.Tensor:
        original_size = input_tensor.size()
        input_tensor = input_tensor.transpose(dim, -1)
        flat_size = input_tensor.size()
        input_tensor = input_tensor.contiguous().view(-1, flat_size[-1])

        z = input_tensor
        n = z.size(-1)
        z_sorted, _ = torch.sort(z, descending=True, dim=-1)

        k_range = torch.arange(1, n + 1, dtype=z.dtype, device=z.device)
        z_cumsum = z_sorted.cumsum(dim=-1)
        k_check = 1.0 + k_range * z_sorted > z_cumsum
        k_z = k_check.sum(dim=-1, keepdim=True).clamp(min=1)

        indices = (k_z - 1).long()
        tau_sum = z_cumsum.gather(-1, indices)
        tau = (tau_sum - 1.0) / k_z.float()

        output = torch.clamp(z - tau, min=0.0)

        output = output.view(flat_size)
        output = output.transpose(dim, -1)
        output = output.contiguous().view(original_size)

        ctx.save_for_backward(output)
        ctx.dim = dim
        return output

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> Tuple[Optional[torch.Tensor], None]:
        output, = ctx.saved_tensors
        dim = ctx.dim

        support = (output > 0).float()
        n_support = support.sum(dim=dim, keepdim=True).clamp(min=1)

        grad_input = support * grad_output
        mean_grad = grad_input.sum(dim=dim, keepdim=True) / n_support
        grad_input = grad_input - support * mean_grad

        return grad_input, None


class Sparsemax(nn.Module):
    def __init__(self, dim: int = -1):
        super().__init__()
        self.dim = dim

    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        return SparsemaxFunction.apply(input_tensor, self.dim)


class TopologicalGate(nn.Module):
    def __init__(self, num_units: int, config: SuperconductorConfig):
        super().__init__()
        self.config = config
        self.num_units = num_units
        self.gate_logits = nn.Parameter(
            torch.full((num_units,), config.gate_init_bias)
        )
        self.gate_temperature = config.gate_temperature_initial

    def forward(self) -> torch.Tensor:
        if self.training:
            uniform_noise = torch.rand_like(self.gate_logits)
            uniform_noise = uniform_noise.clamp(self.config.numerical_epsilon,
                                                 1.0 - self.config.numerical_epsilon)
            logistic_noise = torch.log(uniform_noise) - torch.log(1.0 - uniform_noise)
            gate_values = torch.sigmoid(
                (self.gate_logits + logistic_noise) / max(self.gate_temperature, self.config.numerical_epsilon)
            )
        else:
            gate_values = (self.gate_logits > 0.0).float()
        return gate_values

    def get_expected_l0(self) -> torch.Tensor:
        return torch.sigmoid(
            self.gate_logits - self.gate_temperature * math.log(-math.log(0.5 + self.config.numerical_epsilon) + self.config.numerical_epsilon)
        ).sum()

    def get_sparsity_ratio(self) -> float:
        with torch.no_grad():
            hard_gates = (self.gate_logits > 0.0).float()
            return 1.0 - hard_gates.mean().item()

    def get_topological_charge(self) -> float:
        with torch.no_grad():
            hard_gates = (self.gate_logits > 0.0).float()
            transitions = torch.abs(hard_gates[1:] - hard_gates[:-1])
            return transitions.sum().item()

    def update_temperature(self, epoch: int) -> None:
        self.gate_temperature = max(
            self.config.gate_temperature_min,
            self.config.gate_temperature_initial * math.exp(
                -self.config.gate_temperature_decay_rate * epoch
            )
        )


class ChemicalPotentialScheduler:
    def __init__(self, config: SuperconductorConfig):
        self.config = config
        self.current_mu = config.mu_initial

    def update(self, test_accuracy: float) -> float:
        if test_accuracy < self.config.mu_onset_accuracy:
            self.current_mu = self.config.mu_initial
        else:
            progress = (test_accuracy - self.config.mu_onset_accuracy) / max(
                self.config.mu_ramp_accuracy - self.config.mu_onset_accuracy,
                self.config.numerical_epsilon
            )
            progress = min(max(progress, 0.0), 1.0)
            self.current_mu = self.config.mu_initial + (
                self.config.mu_max - self.config.mu_initial
            ) * (progress ** self.config.mu_exponent)
        return self.current_mu

    def get_mu(self) -> float:
        return self.current_mu


class SuperconductingAttention(nn.Module):
    def __init__(self, config: SuperconductorConfig):
        super().__init__()
        self.config = config
        self.d_model = config.d_model
        self.n_heads = config.n_heads
        self.d_head = config.d_model // config.n_heads

        self.temperature = nn.Parameter(torch.ones(1) * config.t_max)

        self.q_proj = nn.Linear(config.d_model, config.d_model)
        self.k_proj = nn.Linear(config.d_model, config.d_model)
        self.v_proj = nn.Linear(config.d_model, config.d_model)
        self.o_proj = nn.Linear(config.d_model, config.d_model)

        self.sparsemax = Sparsemax(dim=-1)

        self.head_gate = TopologicalGate(config.n_heads, config)

        self.entropy = 0.0
        self.heat_capacity = 0.0
        self.t_eff = config.t_max
        self.sparsity_ratio = 0.0
        self.resistance = 0.0
        self.conductance = 0.0
        self.attention_scores_detached: Optional[torch.Tensor] = None
        self.attention_weights_detached: Optional[torch.Tensor] = None

    def forward(
        self,
        x: torch.Tensor,
        mask: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        batch_size, seq_len, _ = x.shape

        Q = self.q_proj(x).view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        K = self.k_proj(x).view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)
        V = self.v_proj(x).view(batch_size, seq_len, self.n_heads, self.d_head).transpose(1, 2)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_head)
        self.attention_scores_detached = scores.detach()

        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)

        scaled_scores = scores / (self.temperature + self.config.numerical_epsilon)
        attn_weights = self.sparsemax(scaled_scores)

        self.attention_weights_detached = attn_weights.detach()

        gate_values = self.head_gate()
        gate_expanded = gate_values.view(1, self.n_heads, 1, 1)
        attn_weights = attn_weights * gate_expanded

        attn_output = torch.matmul(attn_weights, V)
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        output = self.o_proj(attn_output)

        self._update_thermodynamic_state(attn_weights)

        return output

    def _update_thermodynamic_state(self, attn_weights: torch.Tensor) -> None:
        with torch.no_grad():
            nonzero_mask = attn_weights > self.config.numerical_epsilon
            total_elements = attn_weights.numel()
            zero_elements = (~nonzero_mask).sum().item()
            self.sparsity_ratio = zero_elements / max(total_elements, 1)

            safe_weights = attn_weights.clamp(min=self.config.numerical_epsilon)
            log_weights = torch.log(safe_weights)
            entropy_per_head = -torch.sum(
                attn_weights * log_weights * nonzero_mask.float(), dim=-1
            )
            self.entropy = entropy_per_head.mean().item()

            self.resistance = self.entropy
            self.conductance = 1.0 / (self.resistance + self.config.numerical_epsilon)

            energies = -log_weights * nonzero_mask.float()
            energy_mean = energies.sum() / max(nonzero_mask.sum().item(), 1)
            energy_var = ((energies - energy_mean) ** 2 * nonzero_mask.float()).sum() / max(nonzero_mask.sum().item(), 1)
            self.heat_capacity = (energy_var / (self.temperature ** 2 + self.config.numerical_epsilon)).item()

            energy_fluctuation = torch.sqrt(energy_var + self.config.numerical_epsilon)
            self.t_eff = (energy_fluctuation / (1.0 + entropy_per_head.mean())).item()


class SuperconductingTransformerLayer(nn.Module):
    def __init__(self, config: SuperconductorConfig, layer_index: int):
        super().__init__()
        self.config = config
        self.layer_index = layer_index

        self.attention = SuperconductingAttention(config)

        self.ff_gate = TopologicalGate(config.d_ff, config)

        self.ff_up = nn.Linear(config.d_model, config.d_ff)
        self.ff_down = nn.Linear(config.d_ff, config.d_model)

        self.norm1 = nn.LayerNorm(config.d_model)
        self.norm2 = nn.LayerNorm(config.d_model)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        normed = self.norm1(x)
        attn_out = self.attention(normed, mask)
        attn_out = self.dropout(attn_out)
        x = x + attn_out

        normed = self.norm2(x)
        ff_hidden = F.gelu(self.ff_up(normed))

        gate_values = self.ff_gate()
        ff_hidden = ff_hidden * gate_values.unsqueeze(0).unsqueeze(0)

        ff_out = self.ff_down(ff_hidden)
        ff_out = self.dropout(ff_out)
        x = x + ff_out

        return x


class SuperconductingTransformer(nn.Module):
    def __init__(self, config: SuperconductorConfig):
        super().__init__()
        self.config = config

        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.pos_encoding = nn.Parameter(
            torch.randn(1, config.max_seq_len, config.d_model) * config.weight_init_std
        )

        self.layers = nn.ModuleList([
            SuperconductingTransformerLayer(config, i) for i in range(config.n_layers)
        ])

        self.output_norm = nn.LayerNorm(config.d_model)
        self.output_proj = nn.Linear(config.d_model, config.vocab_size)

        self._init_weights()

    def _init_weights(self) -> None:
        init_std = self.config.weight_init_std
        for module in self.modules():
            if isinstance(module, nn.Linear):
                nn.init.normal_(module.weight, std=init_std)
                if module.bias is not None:
                    nn.init.zeros_(module.bias)
            elif isinstance(module, nn.Embedding):
                nn.init.normal_(module.weight, std=init_std)

    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        seq_len = x.size(1)
        x = self.token_embedding(x) + self.pos_encoding[:, :seq_len, :]

        for layer in self.layers:
            x = layer(x, mask)

        x = self.output_norm(x)
        logits = self.output_proj(x)
        return logits

    def get_thermodynamic_state(self) -> Dict[str, float]:
        n_layers = len(self.layers)
        state = {
            "entropy": 0.0,
            "heat_capacity": 0.0,
            "T_eff": 0.0,
            "temperature": 0.0,
            "sparsity_ratio": 0.0,
            "resistance": 0.0,
            "conductance": 0.0,
        }
        for layer in self.layers:
            attn = layer.attention
            state["entropy"] += attn.entropy
            state["heat_capacity"] += attn.heat_capacity
            state["T_eff"] += attn.t_eff
            state["temperature"] += attn.temperature.item()
            state["sparsity_ratio"] += attn.sparsity_ratio
            state["resistance"] += attn.resistance
            state["conductance"] += attn.conductance
        for key in state:
            state[key] /= max(n_layers, 1)
        return state

    def get_gate_statistics(self) -> Dict[str, float]:
        total_head_sparsity = 0.0
        total_ff_sparsity = 0.0
        total_head_topo_charge = 0.0
        total_ff_topo_charge = 0.0
        total_head_l0 = 0.0
        total_ff_l0 = 0.0
        n = len(self.layers)
        for layer in self.layers:
            total_head_sparsity += layer.attention.head_gate.get_sparsity_ratio()
            total_ff_sparsity += layer.ff_gate.get_sparsity_ratio()
            total_head_topo_charge += layer.attention.head_gate.get_topological_charge()
            total_ff_topo_charge += layer.ff_gate.get_topological_charge()
            total_head_l0 += layer.attention.head_gate.get_expected_l0().item()
            total_ff_l0 += layer.ff_gate.get_expected_l0().item()
        return {
            "head_gate_sparsity": total_head_sparsity / max(n, 1),
            "ff_gate_sparsity": total_ff_sparsity / max(n, 1),
            "head_topological_charge": total_head_topo_charge / max(n, 1),
            "ff_topological_charge": total_ff_topo_charge / max(n, 1),
            "head_expected_l0": total_head_l0 / max(n, 1),
            "ff_expected_l0": total_ff_l0 / max(n, 1),
        }

    def get_cooper_pair_coherence(self) -> Dict[str, float]:
        if len(self.layers) < 2:
            return {
                "psi_cooper": 0.0,
                "cooper_pair_count": 0.0,
                "mean_interlayer_correlation": 0.0,
            }

        correlations = []
        for i in range(len(self.layers) - 1):
            w_i = []
            w_j = []
            for name, param in self.layers[i].named_parameters():
                if "weight" in name and param.dim() >= 2:
                    w_i.append(param.detach().flatten())
            for name, param in self.layers[i + 1].named_parameters():
                if "weight" in name and param.dim() >= 2:
                    w_j.append(param.detach().flatten())

            if w_i and w_j:
                flat_i = torch.cat(w_i)
                flat_j = torch.cat(w_j)
                min_len = min(len(flat_i), len(flat_j))
                flat_i = flat_i[:min_len]
                flat_j = flat_j[:min_len]

                norm_i = torch.norm(flat_i) + 1e-8
                norm_j = torch.norm(flat_j) + 1e-8
                correlation = torch.dot(flat_i / norm_i, flat_j / norm_j).item()
                correlations.append(abs(correlation))

        if not correlations:
            return {
                "psi_cooper": 0.0,
                "cooper_pair_count": 0.0,
                "mean_interlayer_correlation": 0.0,
            }

        mean_corr = np.mean(correlations)
        cooper_count = sum(1 for c in correlations if c > self.config.cooper_pair_threshold)
        psi = mean_corr * (cooper_count / max(len(correlations), 1))

        return {
            "psi_cooper": psi,
            "cooper_pair_count": float(cooper_count),
            "mean_interlayer_correlation": mean_corr,
        }

    def get_gap_energy(self) -> Dict[str, float]:
        all_magnitudes = []
        for param in self.parameters():
            if param.dim() >= 2:
                all_magnitudes.append(param.detach().abs().flatten())
        if not all_magnitudes:
            return {"gap_energy": 0.0, "gap_ratio": 0.0}

        magnitudes = torch.cat(all_magnitudes)
        low_percentile = torch.quantile(magnitudes, self.config.gap_energy_percentile_low / 100.0).item()
        high_percentile = torch.quantile(magnitudes, self.config.gap_energy_percentile_high / 100.0).item()
        gap = high_percentile - low_percentile
        ratio = gap / (high_percentile + self.config.numerical_epsilon)
        return {"gap_energy": gap, "gap_ratio": ratio}

    def get_meissner_fraction(self) -> float:
        total = 0
        expelled = 0
        for param in self.parameters():
            if param.dim() >= 2:
                total += param.numel()
                expelled += (param.detach().abs() < self.config.meissner_threshold).sum().item()
        return expelled / max(total, 1)

    def update_gate_temperatures(self, epoch: int) -> None:
        for layer in self.layers:
            layer.attention.head_gate.update_temperature(epoch)
            layer.ff_gate.update_temperature(epoch)


class ModularAdditionDatasetFactory:
    @staticmethod
    def create(
        modulus: int = 26,
        train_fraction: float = 0.5,
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


class DeltaCalculator(IMetricCalculator):
    def __init__(self, config: SuperconductorConfig):
        self.config = config

    def calculate(self, model: SuperconductingTransformer, **kwargs) -> Dict[str, float]:
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
        alpha = -np.log(delta + self.config.log_floor) if delta > 0 else 20.0
        return {"delta": delta, "alpha_purity": alpha}


class KappaCalculator:
    def __init__(self, config: SuperconductorConfig):
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
    def __init__(self, config: SuperconductorConfig):
        self.config = config

    def calculate(
        self,
        model: SuperconductingTransformer,
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
    def __init__(self, config: SuperconductorConfig):
        self.config = config

    def calculate(
        self,
        model: SuperconductingTransformer,
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
                param.data = perturbed[idx: idx + numel].reshape(param.shape)
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
    def __init__(self, config: SuperconductorConfig):
        self.config = config
        self.sae_encoder: Optional[nn.Linear] = None
        self.sae_decoder: Optional[nn.Linear] = None

    def _initialize_sae(self, input_dim: int, device: torch.device) -> None:
        if self.sae_encoder is None:
            hidden = self.config.superposition_hidden_dim
            self.sae_encoder = nn.Linear(input_dim, hidden).to(device)
            self.sae_decoder = nn.Linear(hidden, input_dim).to(device)

    def calculate(self, model: SuperconductingTransformer, **kwargs) -> Dict[str, float]:
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
    def __init__(self, config: SuperconductorConfig):
        self.config = config

    def calculate(self, model: SuperconductingTransformer, **kwargs) -> Dict[str, float]:
        g_alg = 0.0
        count = 0
        for p in model.parameters():
            if p.grad is not None:
                g_alg += torch.mean(p.grad.detach() ** 2).item()
                count += 1
        g_alg = g_alg / max(count, 1)
        return {"G_alg": g_alg}


class SuperconductivityLoss(ILossComponent):
    def __init__(self, config: SuperconductorConfig, mu_scheduler: ChemicalPotentialScheduler):
        self.config = config
        self.mu_scheduler = mu_scheduler

    def compute(
        self,
        model: SuperconductingTransformer,
        loss_ce: torch.Tensor,
        epoch: int,
        **kwargs,
    ) -> torch.Tensor:
        total = loss_ce

        mu = self.mu_scheduler.get_mu()
        if mu > self.config.numerical_epsilon:
            weight_cost = torch.tensor(0.0, device=loss_ce.device)
            param_count = 0
            for param in model.parameters():
                if param.dim() >= 2:
                    weight_cost = weight_cost + param.abs().sum()
                    param_count += param.numel()
            if param_count > 0:
                total = total + mu * (weight_cost / param_count)

        gate_l0_cost = torch.tensor(0.0, device=loss_ce.device)
        for layer in model.layers:
            gate_l0_cost = gate_l0_cost + layer.attention.head_gate.get_expected_l0()
            gate_l0_cost = gate_l0_cost + layer.ff_gate.get_expected_l0()
        total = total + self.config.gate_l0_regularization_weight * gate_l0_cost

        topo_cost = torch.tensor(0.0, device=loss_ce.device)
        for layer in model.layers:
            head_logits = layer.attention.head_gate.gate_logits
            topo_cost = topo_cost + torch.sum(torch.abs(head_logits[1:] - head_logits[:-1]))
            ff_logits = layer.ff_gate.gate_logits
            topo_cost = topo_cost + torch.sum(torch.abs(ff_logits[1:] - ff_logits[:-1]))
        total = total + self.config.gate_topological_regularization_weight * topo_cost

        resistance_cost = torch.tensor(0.0, device=loss_ce.device)
        for layer in model.layers:
            if layer.attention.attention_weights_detached is not None:
                aw = layer.attention.attention_weights_detached
                safe_aw = aw.clamp(min=self.config.numerical_epsilon)
                entropy_per_position = -torch.sum(aw * torch.log(safe_aw), dim=-1)
                resistance_cost = resistance_cost + entropy_per_position.mean()
        total = total + self.config.resistance_loss_weight * resistance_cost

        cooper = model.get_cooper_pair_coherence()
        psi_cooper = cooper["psi_cooper"]
        total = total - self.config.cooper_pair_loss_weight * psi_cooper

        return total


class PhaseDetector(IPhaseDetector):
    def __init__(self, config: SuperconductorConfig):
        self.config = config
        self.current_phase = "unknown"
        self.phase_history: List[Tuple[int, str]] = []

    def detect(self, metrics: Dict[str, float]) -> str:
        kappa = metrics.get("kappa", float("inf"))
        delta = metrics.get("delta", 0.5)
        t_eff = metrics.get("T_eff_gradient", 1.0)
        test_acc = metrics.get("test_acc", 0.0)
        conductance = metrics.get("conductance", 0.0)
        meissner = metrics.get("meissner_fraction", 0.0)

        if (
            kappa < self.config.kappa_crystal_threshold
            and delta < self.config.delta_crystal_threshold
            and t_eff < self.config.t_eff_crystal_ceiling
            and test_acc > self.config.grokking_threshold
        ):
            phase = "superconductor"
        elif delta < 0.2 and test_acc > 0.9 and conductance > 10.0:
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
                f"(cond={conductance:.2f}, meissner={meissner:.4f}) ***"
            )
            self.current_phase = phase
            self.phase_history.append((epoch, phase))
        return phase


class AdaptiveAnnealingScheduler:
    def __init__(
        self,
        model: SuperconductingTransformer,
        config: SuperconductorConfig,
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

        if phase in ("crystal", "superconductor"):
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


class GlassDetector(IGlassDetector):
    def __init__(self, config: SuperconductorConfig):
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


class GrokkinDetector(IGrokkinDetector):
    def __init__(self, config: SuperconductorConfig):
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


class CheckpointManager(ICheckpointManager):
    def __init__(self, config: SuperconductorConfig):
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


class ModelPruner:
    @staticmethod
    def prune(model: SuperconductingTransformer, threshold: float = 0.1) -> int:
        print(f"\nPruning weights with magnitude < {threshold}...")
        total_pruned = 0
        total_params = 0
        for layer in model.layers:
            attn = layer.attention
            for proj in [attn.q_proj, attn.k_proj, attn.v_proj, attn.o_proj]:
                with torch.no_grad():
                    mask = proj.weight.abs() > threshold
                    proj.weight.data *= mask.float()
                    total_pruned += (~mask).sum().item()
                    total_params += mask.numel()
            with torch.no_grad():
                for ff_layer in [layer.ff_up, layer.ff_down]:
                    mask = ff_layer.weight.abs() > threshold
                    ff_layer.weight.data *= mask.float()
                    total_pruned += (~mask).sum().item()
                    total_params += mask.numel()
        remaining = total_params - total_pruned
        print(f"Pruned {total_pruned}/{total_params} weights. Remaining: {remaining}")
        return remaining


class ModelDiscretizer:
    @staticmethod
    def discretize(model: SuperconductingTransformer, tolerance: float = 0.1) -> bool:
        print(f"\nAttempting discretization with tolerance {tolerance}...")
        can_discretize = True
        for name, param in model.named_parameters():
            if param.dim() >= 2:
                rounded = torch.round(param.data)
                distance = torch.abs(param.data - rounded).max().item()
                if distance > tolerance:
                    print(f"Cannot discretize {name}: max distance {distance:.4f} > {tolerance}")
                    can_discretize = False
                else:
                    param.data = rounded
        if can_discretize:
            print("Discretization successful!")
        else:
            print("Discretization failed - weights not close enough to integers")
        return can_discretize


class ComprehensiveMetricsAggregator:
    def __init__(self, config: SuperconductorConfig):
        self.config = config
        self.delta_calc = DeltaCalculator(config)
        self.kappa_calc = KappaCalculator(config)
        self.thermo_calc = ThermodynamicMetricsCalculator(config)
        self.lc_calc = LocalComplexityCalculator(config)
        self.sp_calc = SuperpositionCalculator(config)
        self.grav_calc = GravitationalConstantCalculator(config)
        self._gradient_covariance: Optional[torch.Tensor] = None

    def compute_all(
        self,
        model: SuperconductingTransformer,
        train_loss: float,
        test_loss: float,
        test_acc: float,
        epoch: int,
        weight_norm: float,
        grad_norm: float,
        thermo_state: Dict[str, float],
        scheduler: AdaptiveAnnealingScheduler,
        mu_scheduler: ChemicalPotentialScheduler,
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
        metrics["sparsity_ratio"] = thermo_state["sparsity_ratio"]
        metrics["resistance"] = thermo_state["resistance"]
        metrics["conductance"] = thermo_state["conductance"]

        metrics["weight_decay"] = scheduler.current_weight_decay
        metrics["scheduler_temperature"] = scheduler.current_temperature
        metrics["mu_eff"] = mu_scheduler.get_mu()

        gate_stats = model.get_gate_statistics()
        metrics.update(gate_stats)

        cooper = model.get_cooper_pair_coherence()
        metrics.update(cooper)

        gap = model.get_gap_energy()
        metrics.update(gap)

        metrics["meissner_fraction"] = model.get_meissner_fraction()

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


class TrainingPrimitives:
    @staticmethod
    @torch.no_grad()
    def evaluate(
        model: SuperconductingTransformer,
        test_x: torch.Tensor,
        test_y: torch.Tensor,
        config: SuperconductorConfig,
        device: torch.device,
    ) -> Tuple[float, float]:
        model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        n_samples = len(test_x)
        for i in range(0, n_samples, config.batch_size):
            batch_x = test_x[i: i + config.batch_size].to(device)
            batch_y = test_y[i: i + config.batch_size].to(device)
            logits = model(batch_x)
            loss = F.cross_entropy(logits[:, -1, :], batch_y)
            total_loss += loss.item() * len(batch_x)
            predictions = torch.argmax(logits[:, -1, :], dim=-1)
            correct += (predictions == batch_y).sum().item()
            total += len(batch_x)
        return total_loss / max(total, 1), correct / max(total, 1)


class ProspectorPhase(ITrainingPhase):
    def __init__(self, config: SuperconductorConfig, seed: int):
        self.config = config
        self.seed = seed

    def execute(
        self,
        model: SuperconductingTransformer,
        **kwargs,
    ) -> Tuple[bool, Dict[str, Any]]:
        train_x = kwargs["train_x"]
        train_y = kwargs["train_y"]
        test_x = kwargs["test_x"]
        test_y = kwargs["test_y"]
        device = kwargs["device"]

        mu_scheduler = ChemicalPotentialScheduler(self.config)
        aggregator = ComprehensiveMetricsAggregator(self.config)
        phase_detector = PhaseDetector(self.config)
        glass_detector = GlassDetector(self.config)
        grokking_detector = GrokkinDetector(self.config)
        sc_loss = SuperconductivityLoss(self.config, mu_scheduler)

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
            model.update_gate_temperatures(epoch)
            total_loss = 0.0
            n_batches = 0
            n_samples = len(train_x)
            indices = torch.randperm(n_samples)

            for i in range(0, n_samples, self.config.batch_size):
                batch_indices = indices[i: i + self.config.batch_size]
                batch_x = train_x[batch_indices].to(device)
                batch_y = train_y[batch_indices].to(device)

                logits = model(batch_x)
                loss_ce = F.cross_entropy(logits[:, -1, :], batch_y)
                loss = sc_loss.compute(model, loss_ce, epoch)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.config.gradient_clip)
                optimizer.step()
                total_loss += loss.item()
                n_batches += 1

            train_loss = total_loss / max(n_batches, 1)
            aggregator.accumulate_gradient(model)

            test_loss, test_acc = TrainingPrimitives.evaluate(model, test_x, test_y, self.config, device)
            mu_scheduler.update(test_acc)

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
                    mu_scheduler=mu_scheduler,
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
                        f" {crystal_flag} E{epoch:>5}: "
                        f"d={metrics['delta']:.4f} "
                        f"Acc={test_acc:.4f} "
                        f"k={DisplayFormatter.format_kappa(metrics['kappa'])} "
                        f"S={metrics['entropy']:.3f} "
                        f"Cv={metrics['heat_capacity']:.2e} "
                        f"Te={metrics['T_eff_gradient']:.2e} "
                        f"hb={metrics['h_bar_eff']:.2e} "
                        f"G={metrics['G_alg']:.4f} "
                        f"mu={metrics['mu_eff']:.4f} "
                        f"sp={metrics['sparsity_ratio']:.3f} "
                        f"R={metrics['resistance']:.3f} "
                        f"Psi={metrics['psi_cooper']:.4f} "
                        f"Meiss={metrics['meissner_fraction']:.3f} "
                        f"gap={metrics['gap_energy']:.4f} "
                        f"|W|={weight_norm:.2f} "
                        f"|g|={grad_norm:.2e} "
                        f"ph={phase[:4]} "
                        f"(bd={best_delta:.4f}@{best_epoch})"
                    )

                    if (
                        metrics["delta"] < self.config.delta_crystal_threshold
                        and test_acc > self.config.grokking_threshold
                        and metrics["kappa"] < self.config.kappa_crystal_threshold
                    ):
                        print(f" [SUPERCONDUCTOR] Detected at epoch {epoch}")
                        return True, {
                            **metrics,
                            "best_delta": best_delta,
                            "best_epoch": best_epoch,
                            "metrics_history": history,
                        }
            else:
                fast_delta_m = self.delta_calc_fast(model)
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

    def delta_calc_fast(self, model: SuperconductingTransformer) -> Dict[str, float]:
        calc = DeltaCalculator(self.config)
        return calc.calculate(model)


class LongTrainingPhase(ITrainingPhase):
    def __init__(self, config: SuperconductorConfig):
        self.config = config
        self.history: List[Dict[str, float]] = []

    def execute(
        self,
        model: SuperconductingTransformer,
        **kwargs,
    ) -> SuperconductingTransformer:
        train_x = kwargs["train_x"]
        train_y = kwargs["train_y"]
        test_x = kwargs["test_x"]
        test_y = kwargs["test_y"]
        device = kwargs["device"]
        checkpoint_manager = kwargs.get("checkpoint_manager")

        mu_scheduler = ChemicalPotentialScheduler(self.config)
        aggregator = ComprehensiveMetricsAggregator(self.config)
        phase_detector = PhaseDetector(self.config)
        grokking_detector = GrokkinDetector(self.config)
        sc_loss = SuperconductivityLoss(self.config, mu_scheduler)

        optimizer = optim.AdamW(
            model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay_initial,
        )
        scheduler = AdaptiveAnnealingScheduler(model, self.config, optimizer)

        print("\n" + "=" * 140)
        print("PHASE 1: SUPERCONDUCTING THERMODYNAMIC TRAINING")
        print("=" * 140)
        print(f"Pressure (WD): {self.config.weight_decay_initial} (adaptive by phase)")
        print(f"Chemical Potential: mu_onset={self.config.mu_onset_accuracy}, mu_max={self.config.mu_max}")
        print(f"Sparsemax: replacing softmax for hard-zero attention")
        print(f"Topological Gating: head gates + FF gates with L0 regularization")
        print(f"Cooper Pair Loss: weight={self.config.cooper_pair_loss_weight}")
        print(f"Resistance Loss: weight={self.config.resistance_loss_weight}")
        print(f"Target: kappa->1, delta->0, T_eff->0, Acc->1.0, Resistance->0, Conductance->inf")
        print("=" * 140)

        header = (
            f"{'E':>6} | {'Loss':>9} | {'tLoss':>9} | {'Acc':>6} | "
            f"{'delta':>6} | {'kappa':>8} | {'S':>5} | {'Cv':>8} | "
            f"{'Te':>8} | {'hb':>8} | {'G':>6} | "
            f"{'mu':>6} | {'sparse':>6} | {'R':>6} | {'cond':>7} | "
            f"{'Psi':>6} | {'Meiss':>5} | {'gap':>6} | "
            f"{'|W|':>6} | {'|g|':>8} | {'WD':>7} | {'Ph':>5}"
        )
        print(header)
        print("-" * len(header))

        crystallization_counter = 0

        for epoch in range(1, self.config.train_epochs + 1):
            model.train()
            model.update_gate_temperatures(epoch)
            total_loss = 0.0
            n_batches = 0
            n_samples = len(train_x)
            indices = torch.randperm(n_samples)

            for i in range(0, n_samples, self.config.batch_size):
                batch_indices = indices[i: i + self.config.batch_size]
                batch_x = train_x[batch_indices].to(device)
                batch_y = train_y[batch_indices].to(device)

                logits = model(batch_x)
                loss_ce = F.cross_entropy(logits[:, -1, :], batch_y)
                loss = sc_loss.compute(model, loss_ce, epoch)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), self.config.gradient_clip)
                optimizer.step()
                total_loss += loss.item()
                n_batches += 1

            train_loss = total_loss / max(n_batches, 1)
            aggregator.accumulate_gradient(model)

            test_loss, test_acc = TrainingPrimitives.evaluate(model, test_x, test_y, self.config, device)
            mu_scheduler.update(test_acc)

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
                    mu_scheduler=mu_scheduler,
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
                    f"{epoch:>6} | "
                    f"{train_loss:>9.2e} | "
                    f"{test_loss:>9.2e} | "
                    f"{test_acc:>6.4f} | "
                    f"{metrics['delta']:>6.4f} | "
                    f"{DisplayFormatter.format_kappa(metrics['kappa'])} | "
                    f"{metrics['entropy']:>5.3f} | "
                    f"{metrics['heat_capacity']:>8.2e} | "
                    f"{metrics['T_eff_gradient']:>8.2e} | "
                    f"{metrics['h_bar_eff']:>8.2e} | "
                    f"{metrics['G_alg']:>6.4f} | "
                    f"{metrics['mu_eff']:>6.4f} | "
                    f"{metrics['sparsity_ratio']:>6.3f} | "
                    f"{metrics['resistance']:>6.3f} | "
                    f"{metrics['conductance']:>7.2f} | "
                    f"{metrics['psi_cooper']:>6.4f} | "
                    f"{metrics['meissner_fraction']:>5.3f} | "
                    f"{metrics['gap_energy']:>6.4f} | "
                    f"{weight_norm:>6.2f} | "
                    f"{grad_norm:>8.2e} | "
                    f"{scheduler.current_weight_decay:>7.1e} | "
                    f"{phase[:5]:>5}"
                )

                if force_lc:
                    print(
                        f"       LC={DisplayFormatter.format_lc(metrics.get('local_complexity', 0.0))} "
                        f"psi_sp={metrics.get('superposition_psi', 0.0):.3f} "
                        f"F={metrics.get('superposition_F', 0.0):.1f} "
                        f"alpha={metrics.get('alpha_purity', 0.0):.2f} "
                        f"hd_gate_sp={metrics.get('head_gate_sparsity', 0.0):.3f} "
                        f"ff_gate_sp={metrics.get('ff_gate_sparsity', 0.0):.3f} "
                        f"hd_topo={metrics.get('head_topological_charge', 0.0):.1f} "
                        f"ff_topo={metrics.get('ff_topological_charge', 0.0):.1f} "
                        f"cooper_n={metrics.get('cooper_pair_count', 0.0):.0f} "
                        f"gap_r={metrics.get('gap_ratio', 0.0):.4f}"
                    )

                if phase == "superconductor":
                    crystallization_counter += 1
                    if crystallization_counter >= self.config.crystallization_confirmation_epochs:
                        print(f"\n{'=' * 70}")
                        print(
                            f"[SUPERCONDUCTOR FREEZE] Confirmed after "
                            f"{self.config.crystallization_confirmation_epochs} stable epochs"
                        )
                        print(f"{'=' * 70}")
                        if checkpoint_manager is not None:
                            checkpoint_manager.save({
                                "epoch": epoch,
                                "model_state_dict": model.state_dict(),
                                "history": self.history,
                                "phase": "superconductor",
                                "kappa": metrics["kappa"],
                                "delta": metrics["delta"],
                                "test_acc": test_acc,
                                "conductance": metrics["conductance"],
                                "psi_cooper": metrics["psi_cooper"],
                                "meissner_fraction": metrics["meissner_fraction"],
                                "timestamp": datetime.now().isoformat(),
                            }, path=str(checkpoint_manager.checkpoint_dir / "superconductor.pt"))
                        return model
                elif phase == "crystal":
                    crystallization_counter += 1
                    if crystallization_counter >= self.config.crystallization_confirmation_epochs:
                        print(f"\n{'=' * 70}")
                        print(
                            f"[CRYSTAL FREEZE] Confirmed after "
                            f"{self.config.crystallization_confirmation_epochs} stable epochs"
                        )
                        print(f"{'=' * 70}")
                        if checkpoint_manager is not None:
                            checkpoint_manager.save({
                                "epoch": epoch,
                                "model_state_dict": model.state_dict(),
                                "history": self.history,
                                "phase": "crystal",
                                "kappa": metrics["kappa"],
                                "delta": metrics["delta"],
                                "test_acc": test_acc,
                                "timestamp": datetime.now().isoformat(),
                            }, path=str(checkpoint_manager.checkpoint_dir / "crystallized.pt"))
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
                        "mu": mu_scheduler.get_mu(),
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


class SeedProspector:
    def __init__(self, config: SuperconductorConfig):
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

        print(f"\nStarting superconducting transformer seed prospecting: {total_attempts} attempts")
        print(f"Target: delta < {self.config.delta_crystal_threshold}, "
              f"Acc > {self.config.grokking_threshold}, "
              f"kappa < {self.config.kappa_crystal_threshold}")
        print(f"Superconductor mechanisms: Sparsemax, Chemical Potential, Topological Gating")
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

            model = SuperconductingTransformer(self.config).to(device)
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
            safe_metrics = {k: v for k, v in final_metrics.items() if k != "metrics_history"}
            with open(seed_path, "w") as f:
                json.dump({"seed": seed, "is_crystal": is_crystal, "metrics": safe_metrics},
                          f, indent=2, default=str)

            if "metrics_history" in final_metrics:
                hist_path = self.results_dir / f"seed_{seed:05d}_history.json"
                with open(hist_path, "w") as f:
                    json.dump(final_metrics["metrics_history"], f, indent=2, default=str)

            if is_crystal:
                print(f"\n{'=' * 60}")
                print(f"[+] SUPERCONDUCTOR FOUND -- Seed {seed}")
                print(f"{'=' * 60}")
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


class LongTrainingPipeline:
    def __init__(self, config: SuperconductorConfig):
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

        print("\n" + "=" * 90)
        print("  SUPERCONDUCTING ATTENTION TRANSFORMER")
        print("  Spontaneous Symmetry Breaking via Chemical Potential + Sparsemax")
        print("=" * 90)
        print(f"Device: {device}")
        print(f"Architecture: d_model={config.d_model}, n_heads={config.n_heads}, "
              f"n_layers={config.n_layers}, d_ff={config.d_ff}")
        print(f"Task: modular addition mod {config.modulus}")
        print(f"Batch size: {config.batch_size}")
        print(f"Weight decay: {config.weight_decay_initial} (adaptive)")
        print(f"Chemical potential: mu_max={config.mu_max}, onset={config.mu_onset_accuracy}, exponent={config.mu_exponent}")
        print(f"Gate L0 reg: {config.gate_l0_regularization_weight}")
        print(f"Topological reg: {config.gate_topological_regularization_weight}")
        print(f"Cooper pair loss: {config.cooper_pair_loss_weight}")
        print(f"Resistance loss: {config.resistance_loss_weight}")
        print(f"Kappa threshold: {config.kappa_crystal_threshold}")
        print(f"Delta target: {config.delta_crystal_threshold}")
        print("=" * 90)

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

        model = SuperconductingTransformer(config).to(device)
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

        n_remaining = ModelPruner.prune(model, threshold=config.pruning_threshold)
        discretized = ModelDiscretizer.discretize(model, tolerance=config.discretization_tolerance)

        test_loss, test_acc = TrainingPrimitives.evaluate(model, test_x, test_y, config, device)
        delta_calc = DeltaCalculator(config)
        delta_m = delta_calc.calculate(model)

        print(f"\nPost-discretization test accuracy: {test_acc:.4f}")
        print(f"Post-discretization delta: {delta_m['delta']:.6f}")
        print(f"Discretization success: {discretized}")
        print(f"Meissner fraction: {model.get_meissner_fraction():.6f}")

        gate_stats = model.get_gate_statistics()
        print(f"Head gate sparsity: {gate_stats['head_gate_sparsity']:.4f}")
        print(f"FF gate sparsity: {gate_stats['ff_gate_sparsity']:.4f}")

        cooper = model.get_cooper_pair_coherence()
        print(f"Cooper pair coherence Psi: {cooper['psi_cooper']:.6f}")

        torch.save({
            "model_state_dict": model.state_dict(),
            "test_acc": test_acc,
            "delta": delta_m["delta"],
            "discretized": discretized,
            "history": phase1.history,
            "config": config,
            "gate_statistics": gate_stats,
            "cooper_pair_coherence": cooper,
            "meissner_fraction": model.get_meissner_fraction(),
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
        print(f"Remaining active weights: {n_remaining}")
        return discretized


class Application:
    def __init__(self):
        self.parser = self._create_argument_parser()

    def _create_argument_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Superconducting Attention Transformer with Spontaneous Symmetry Breaking",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Modes:
  prospect    Fast seed mining with superconducting loss
  train       Long-term training with full thermodynamic + superconductivity monitoring

Examples:
  python superconducting_transformer.py prospect --attempts 100 --start-seed 1
  python superconducting_transformer.py train --seed 42 --epochs 25000
  python superconducting_transformer.py train --seed 42 --mu-max 2.0 --mu-exponent 4.0
  python superconducting_transformer.py train --resume checkpoints_superconductor/latest.pt
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
        parser.add_argument("--mu-max", type=float, default=None)
        parser.add_argument("--mu-onset", type=float, default=None)
        parser.add_argument("--mu-exponent", type=float, default=None)
        parser.add_argument("--gate-l0-weight", type=float, default=None)
        parser.add_argument("--gate-topo-weight", type=float, default=None)
        parser.add_argument("--cooper-weight", type=float, default=None)
        parser.add_argument("--resistance-weight", type=float, default=None)
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
        if args.mu_max is not None:
            overrides["mu_max"] = args.mu_max
        if args.mu_onset is not None:
            overrides["mu_onset_accuracy"] = args.mu_onset
        if args.mu_exponent is not None:
            overrides["mu_exponent"] = args.mu_exponent
        if args.gate_l0_weight is not None:
            overrides["gate_l0_regularization_weight"] = args.gate_l0_weight
        if args.gate_topo_weight is not None:
            overrides["gate_topological_regularization_weight"] = args.gate_topo_weight
        if args.cooper_weight is not None:
            overrides["cooper_pair_loss_weight"] = args.cooper_weight
        if args.resistance_weight is not None:
            overrides["resistance_loss_weight"] = args.resistance_weight
        if args.device is not None:
            overrides["device"] = args.device

        config = replace(SuperconductorConfig(), **overrides)

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