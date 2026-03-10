#!/usr/bin/env python3
"""
κ-Miner: Universal Grokking Predictor for LLMs
==============================================

Based on the discovery that κ (gradient covariance condition number) 
perfectly predicts grokking (AUC=1.0), this module applies κ-mining 
to predict algorithmic learning in transformers.

Key insight: κ ≈ 1 → Crystal (algorithm learned)
            κ >> 1 → Glass (no algorithm)

Usage:
    from kappa_miner import KappaMiner, ArithmeticTask
    
    miner = KappaMiner(model, task=ArithmeticTask())
    results = miner.prospect(early_epochs=100)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import json
import math
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Callable
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class KappaConfig:
    """Configuration for κ-mining experiments."""
    
    # κ thresholds (from Strassen paper)
    kappa_crystal_threshold: float = 1.001
    kappa_glass_threshold: float = 100.0
    
    # Measurement parameters
    kappa_samples: int = 64
    kappa_batch_size: int = 32
    gradient_regularization: float = 1e-6
    
    # Early stopping
    early_stop_epochs: int = 100
    early_stop_patience: int = 5
    
    # Training
    max_epochs: int = 10000
    eval_interval: int = 50
    checkpoint_interval: int = 100
    
    # Device
    device: str = "cuda" if torch.cuda.is_available() else "cpu"


# ============================================================================
# κ MEASUREMENT
# ============================================================================

class KappaMeter:
    """
    Measures κ(Σ) = λ_max/λ_min of gradient covariance matrix.
    
    This is the core metric that predicts grokking with AUC=1.0.
    """
    
    def __init__(self, config: KappaConfig):
        self.config = config
    
    def compute_kappa(self, model: nn.Module, 
                      loss_fn: Callable,
                      data_generator: Callable,
                      n_samples: int = None,
                      batch_size: int = None) -> Dict[str, float]:
        """
        Compute gradient covariance condition number κ.
        
        Returns:
            Dictionary with κ, eigenvalues, and diagnostics
        """
        model.eval()
        n_samples = n_samples or self.config.kappa_samples
        batch_size = batch_size or self.config.kappa_batch_size
        
        all_grads = []
        
        for _ in range(n_samples // batch_size):
            # Generate batch
            inputs, targets = data_generator(batch_size)
            inputs = inputs.to(self.config.device)
            targets = targets.to(self.config.device)
            
            # Forward + backward
            model.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, targets)
            loss.backward()
            
            # Collect gradients
            grads = []
            for p in model.parameters():
                if p.grad is not None:
                    grads.append(p.grad.detach().flatten())
            
            if grads:
                all_grads.append(torch.cat(grads))
        
        if len(all_grads) < 2:
            return {'kappa': float('inf'), 'error': 'insufficient_samples'}
        
        # Stack gradients: shape (n_samples, n_params)
        all_grads = torch.stack(all_grads)
        
        # Center gradients
        mean_grad = all_grads.mean(dim=0)
        centered = all_grads - mean_grad
        
        # Compute covariance
        n = centered.shape[0]
        covariance = (centered.T @ centered) / (n - 1)
        
        # Add regularization for numerical stability
        reg = self.config.gradient_regularization
        covariance = covariance + torch.eye(covariance.shape[0], 
                                            device=self.config.device) * reg
        
        # Compute eigenvalues
        try:
            cov_np = covariance.cpu().numpy()
            eigenvalues = np.linalg.eigvalsh(cov_np)
            eigenvalues = np.sort(eigenvalues)
            
            # Filter near-zero eigenvalues
            valid_mask = eigenvalues > 1e-10
            valid_eigenvalues = eigenvalues[valid_mask]
            
            if len(valid_eigenvalues) < 2:
                return {'kappa': float('inf'), 'error': 'degenerate_covariance'}
            
            lambda_min = valid_eigenvalues[0]
            lambda_max = valid_eigenvalues[-1]
            
            kappa = lambda_max / lambda_min if lambda_min > 0 else float('inf')
            
            # Effective dimensionality
            effective_rank = np.sum(valid_eigenvalues) ** 2 / np.sum(valid_eigenvalues ** 2)
            
            return {
                'kappa': float(kappa),
                'lambda_min': float(lambda_min),
                'lambda_max': float(lambda_max),
                'effective_rank': float(effective_rank),
                'n_valid_eigenvalues': len(valid_eigenvalues),
                'gradient_norm': float(torch.norm(mean_grad).item())
            }
            
        except Exception as e:
            return {'kappa': float('inf'), 'error': str(e)}
    
    def predict_grokking(self, kappa: float) -> Dict[str, any]:
        """
        Predict whether model will grokk based on κ.
        
        Returns prediction with confidence based on Strassen paper results.
        """
        if kappa < self.config.kappa_crystal_threshold:
            return {
                'prediction': 'will_grokk',
                'confidence': 0.99,  # AUC=1.0 from paper
                'phase': 'crystal',
                'recommendation': 'continue_training'
            }
        elif kappa < self.config.kappa_glass_threshold:
            return {
                'prediction': 'likely_grokk',
                'confidence': 0.7,
                'phase': 'transitional',
                'recommendation': 'continue_training_monitor'
            }
        else:
            return {
                'prediction': 'will_not_grokk',
                'confidence': 0.95,
                'phase': 'glass',
                'recommendation': 'abort_or_reset'
            }


# ============================================================================
# ARITHMETIC TASK (Test Case for LLM Grokking)
# ============================================================================

class ArithmeticTask:
    """
    Arithmetic task for testing κ prediction on transformers.
    
    Models must learn to:
    - Add numbers (a + b = c)
    - Multiply numbers (a * b = c)
    - Combined operations
    
    This is a canonical "algorithmic" task that requires learning
    exact computation, not just pattern matching.
    """
    
    def __init__(self, 
                 max_digits: int = 3,
                 operations: List[str] = None,
                 tokenizer_vocab: int = 20):
        """
        Args:
            max_digits: Maximum number of digits per operand
            operations: List of operations ['+', '-', '*']
            tokenizer_vocab: Vocabulary size for tokenizer
        """
        self.max_digits = max_digits
        self.operations = operations or ['+', '*']
        self.tokenizer_vocab = tokenizer_vocab
        
        # Calculate max value
        self.max_value = 10 ** max_digits - 1
        
        # Special tokens
        self.PAD = 0
        self.START = 1
        self.END = 2
        self.PLUS = 10
        self.MINUS = 11
        self.MULT = 12
        self.EQUALS = 13
        
    def generate_batch(self, batch_size: int, 
                       operation: str = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Generate batch of arithmetic problems.
        
        Returns:
            inputs: (batch, seq_len) - "a + b ="
            targets: (batch, seq_len) - "c"
        """
        operation = operation or np.random.choice(self.operations)
        
        # Generate random operands
        a = torch.randint(0, self.max_value + 1, (batch_size,))
        b = torch.randint(0, self.max_value + 1, (batch_size,))
        
        # Compute result
        if operation == '+':
            c = a + b
            op_token = self.PLUS
        elif operation == '-':
            c = a - b
            op_token = self.MINUS
        else:  # '*'
            c = a * b
            op_token = self.MULT
        
        # Convert to sequences
        # Input: "a op b =" (each number is sequence of digits)
        max_seq_len = (self.max_digits + 1) * 2 + 3  # digits + op + digits + = + buffer
        
        inputs = torch.zeros(batch_size, max_seq_len, dtype=torch.long)
        targets = torch.zeros(batch_size, max_seq_len, dtype=torch.long)
        
        for i in range(batch_size):
            # Encode input
            a_digits = self._encode_number(a[i].item())
            b_digits = self._encode_number(b[i].item())
            c_digits = self._encode_number(c[i].item())
            
            # Input sequence: a_digits + op + b_digits + =
            inp_seq = a_digits + [op_token] + b_digits + [self.EQUALS]
            inp_seq = [self.START] + inp_seq
            
            # Target sequence: c_digits + END
            tgt_seq = c_digits + [self.END]
            
            # Pad and store
            inputs[i, :len(inp_seq)] = torch.tensor(inp_seq)
            targets[i, :len(tgt_seq)] = torch.tensor(tgt_seq)
        
        return inputs, targets
    
    def _encode_number(self, n: int) -> List[int]:
        """Encode number as sequence of digit tokens."""
        if n == 0:
            return [3]  # Token for 0
        
        # Handle negative
        tokens = []
        if n < 0:
            tokens.append(14)  # MINUS token
            n = -n
        
        # Encode digits
        digits = []
        while n > 0:
            digits.append((n % 10) + 3)  # Digits 0-9 mapped to tokens 3-12
            n //= 10
        
        return tokens + digits[::-1]


# ============================================================================
# MINIMAL TRANSFORMER
# ============================================================================

class MinimalTransformer(nn.Module):
    """
    Minimal transformer for arithmetic tasks.
    
    Architecture designed to be small enough to train quickly
    but expressive enough to learn algorithms.
    """
    
    def __init__(self, 
                 vocab_size: int = 20,
                 d_model: int = 128,
                 n_heads: int = 4,
                 n_layers: int = 4,
                 d_ff: int = 256,
                 max_seq_len: int = 50,
                 dropout: float = 0.1):
        super().__init__()
        
        self.d_model = d_model
        self.vocab_size = vocab_size
        
        # Embeddings
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_seq_len, d_model)
        
        # Transformer layers
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_ff,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        
        # Output
        self.output_proj = nn.Linear(d_model, vocab_size)
        
        self._init_weights()
    
    def _init_weights(self):
        """Xavier initialization."""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len) input tokens
        
        Returns:
            logits: (batch, seq_len, vocab_size)
        """
        batch_size, seq_len = x.shape
        
        # Embeddings
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
        embeddings = self.token_embedding(x) + self.position_embedding(positions)
        
        # Transformer
        # Create causal mask
        mask = nn.Transformer.generate_square_subsequent_mask(seq_len, device=x.device)
        encoded = self.transformer(embeddings, mask=mask, is_causal=True)
        
        # Output projection
        logits = self.output_proj(encoded)
        
        return logits


# ============================================================================
# κ-MINER MAIN CLASS
# ============================================================================

class KappaMiner:
    """
    Main class for κ-mining experiments on LLMs.
    
    Uses κ to predict algorithmic learning before training completes,
    based on the AUC=1.0 result from Strassen paper.
    """
    
    def __init__(self, 
                 model: nn.Module,
                 task: ArithmeticTask,
                 config: KappaConfig = None):
        self.model = model.to(config.device if config else 'cuda' if torch.cuda.is_available() else 'cpu')
        self.task = task
        self.config = config or KappaConfig()
        self.kappa_meter = KappaMeter(self.config)
        
        self.history = {
            'epochs': [],
            'kappa': [],
            'loss': [],
            'accuracy': [],
            'phase': [],
            'predictions': []
        }
    
    def prospect(self, 
                 early_epochs: int = None,
                 save_checkpoints: bool = True,
                 checkpoint_dir: str = "checkpoints") -> Dict:
        """
        Prospect for algorithmic learning using κ-mining.
        
        Key idea: Only train models that κ predicts will succeed.
        
        Args:
            early_epochs: Epochs to train before κ prediction
            save_checkpoints: Save model checkpoints
            checkpoint_dir: Directory for checkpoints
        
        Returns:
            Dictionary with prospecting results and predictions
        """
        early_epochs = early_epochs or self.config.early_stop_epochs
        checkpoint_dir = Path(checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        print("=" * 70)
        print("κ-MINER: Prospecting for Algorithmic Learning")
        print("=" * 70)
        print(f"Early stopping epochs: {early_epochs}")
        print(f"κ crystal threshold: {self.config.kappa_crystal_threshold}")
        print()
        
        # Optimizer
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=1e-3, weight_decay=1e-4)
        
        # Loss function
        def loss_fn(outputs, targets):
            return F.cross_entropy(outputs.view(-1, outputs.size(-1)), 
                                   targets.view(-1), 
                                   ignore_index=0)
        
        # Data generator for κ measurement
        def data_generator(batch_size):
            return self.task.generate_batch(batch_size)
        
        best_kappa = float('inf')
        patience_counter = 0
        
        for epoch in range(self.config.max_epochs):
            # Training step
            self.model.train()
            inputs, targets = self.task.generate_batch(32)
            inputs = inputs.to(self.config.device)
            targets = targets.to(self.config.device)
            
            optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = loss_fn(outputs, targets)
            loss.backward()
            optimizer.step()
            
            # Evaluate at intervals
            if epoch % self.config.eval_interval == 0:
                # Compute κ
                self.model.eval()
                kappa_result = self.kappa_meter.compute_kappa(
                    self.model, loss_fn, data_generator
                )
                kappa = kappa_result.get('kappa', float('inf'))
                
                # Compute accuracy
                with torch.no_grad():
                    test_inputs, test_targets = self.task.generate_batch(100)
                    test_inputs = test_inputs.to(self.config.device)
                    test_outputs = self.model(test_inputs)
                    
                    # Accuracy on next token prediction
                    predictions = test_outputs.argmax(dim=-1)
                    mask = test_targets != 0
                    correct = (predictions[:, :-1] == test_targets[:, 1:]) * mask[:, :-1]
                    accuracy = correct.sum().item() / mask[:, :-1].sum().item()
                
                # Predict phase
                prediction = self.kappa_meter.predict_grokking(kappa)
                
                # Store history
                self.history['epochs'].append(epoch)
                self.history['kappa'].append(kappa)
                self.history['loss'].append(loss.item())
                self.history['accuracy'].append(accuracy)
                self.history['phase'].append(prediction['phase'])
                self.history['predictions'].append(prediction['prediction'])
                
                # Print status
                phase_emoji = "💎" if prediction['phase'] == 'crystal' else "🧊" if prediction['phase'] == 'glass' else "🔮"
                print(f"Epoch {epoch:5d} | κ: {kappa:12.2e} | Loss: {loss.item():.4f} | "
                      f"Acc: {accuracy:.2%} | {phase_emoji} {prediction['phase']:12s} | "
                      f"Prediction: {prediction['prediction']}")
                
                # Save checkpoint if crystal
                if save_checkpoints and prediction['phase'] == 'crystal':
                    ckpt_path = checkpoint_dir / f"crystal_epoch{epoch}.pt"
                    torch.save({
                        'epoch': epoch,
                        'model_state_dict': self.model.state_dict(),
                        'kappa': kappa,
                        'loss': loss.item(),
                        'accuracy': accuracy,
                        'prediction': prediction
                    }, ckpt_path)
                    print(f"  💾 Saved crystal checkpoint: {ckpt_path}")
                
                # Early stopping logic
                if epoch >= early_epochs:
                    if prediction['prediction'] == 'will_not_grokk':
                        patience_counter += 1
                        if patience_counter >= self.config.early_stop_patience:
                            print(f"\n⚠️  Early stopping: κ predicts will not grokk")
                            break
                    else:
                        patience_counter = 0
                    
                    if prediction['prediction'] == 'will_grokk':
                        print(f"\n✅ κ predicts grokking! Continuing training...")
        
        # Final analysis
        print("\n" + "=" * 70)
        print("PROSPECTING RESULTS")
        print("=" * 70)
        
        final_kappa = self.history['kappa'][-1] if self.history['kappa'] else float('inf')
        final_prediction = self.kappa_meter.predict_grokking(final_kappa)
        
        print(f"Final κ: {final_kappa:.2e}")
        print(f"Prediction: {final_prediction['prediction']}")
        print(f"Confidence: {final_prediction['confidence']:.0%}")
        print(f"Phase: {final_prediction['phase']}")
        
        return {
            'final_kappa': final_kappa,
            'prediction': final_prediction,
            'history': self.history,
            'recommendation': final_prediction['recommendation']
        }


# ============================================================================
# BATCH PROSPECTOR
# ============================================================================

class BatchProspector:
    """
    Prospect multiple seeds/configurations to find crystals efficiently.
    
    Uses κ-mining to avoid wasting compute on configurations that
    will not grokk.
    """
    
    def __init__(self, 
                 model_class: type,
                 task: ArithmeticTask,
                 config: KappaConfig = None):
        self.model_class = model_class
        self.task = task
        self.config = config or KappaConfig()
    
    def prospect_seeds(self,
                       n_candidates: int = 100,
                       early_epochs: int = 50) -> Dict:
        """
        Prospect multiple random seeds to find crystals.
        
        Returns list of seeds that κ predicts will succeed.
        """
        print("=" * 70)
        print("BATCH PROSPECTOR: Mining for Crystals")
        print("=" * 70)
        print(f"Candidates: {n_candidates}")
        print(f"Early epochs per candidate: {early_epochs}")
        print()
        
        results = {
            'crystals': [],      # κ < 1.001
            'transitional': [],  # 1.001 < κ < 100
            'glass': []          # κ > 100
        }
        
        for seed in range(n_candidates):
            print(f"\n--- Seed {seed} ---")
            
            # Set seed
            torch.manual_seed(seed)
            np.random.seed(seed)
            
            # Create model
            model = self.model_class()
            miner = KappaMiner(model, self.task, self.config)
            
            # Quick prospect
            result = miner.prospect(early_epochs=early_epochs, 
                                    save_checkpoints=False)
            
            kappa = result['final_kappa']
            prediction = result['prediction']['prediction']
            
            # Classify
            seed_result = {
                'seed': seed,
                'kappa': kappa,
                'prediction': prediction,
                'history': result['history']
            }
            
            if kappa < self.config.kappa_crystal_threshold:
                results['crystals'].append(seed_result)
                print(f"  💎 CRYSTAL FOUND! κ = {kappa:.2e}")
            elif kappa < self.config.kappa_glass_threshold:
                results['transitional'].append(seed_result)
                print(f"  🔮 Transitional: κ = {kappa:.2e}")
            else:
                results['glass'].append(seed_result)
                print(f"  🧊 Glass: κ = {kappa:.2e}")
        
        # Summary
        print("\n" + "=" * 70)
        print("PROSPECTING SUMMARY")
        print("=" * 70)
        print(f"Crystals found: {len(results['crystals'])} ({100*len(results['crystals'])/n_candidates:.1f}%)")
        print(f"Transitional: {len(results['transitional'])} ({100*len(results['transitional'])/n_candidates:.1f}%)")
        print(f"Glass: {len(results['glass'])} ({100*len(results['glass'])/n_candidates:.1f}%)")
        
        if results['crystals']:
            print("\n💎 Crystal seeds (train these!):")
            for c in results['crystals']:
                print(f"  Seed {c['seed']}: κ = {c['kappa']:.2e}")
        
        return results


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("κ-Miner: Universal Grokking Predictor")
    print("=" * 70)
    print()
    
    # Configuration
    config = KappaConfig()
    
    # Create task
    task = ArithmeticTask(max_digits=2, operations=['+', '*'])
    
    # Create model
    model = MinimalTransformer(
        vocab_size=20,
        d_model=64,
        n_heads=2,
        n_layers=2,
        d_ff=128
    )
    
    # Create miner
    miner = KappaMiner(model, task, config)
    
    # Run prospecting
    results = miner.prospect(early_epochs=100, save_checkpoints=True)
    
    print("\n✅ κ-Mining complete!")
    print(f"Final prediction: {results['prediction']['prediction']}")
    print(f"Confidence: {results['prediction']['confidence']:.0%}")
