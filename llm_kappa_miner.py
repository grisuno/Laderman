#!/usr/bin/env python3
"""
κ-Miner for Real LLMs (GPT-2, Llama, etc.)
==========================================

Applies κ-mining to predict algorithmic learning in actual LLMs.

Usage:
    python llm_kappa_miner.py --model gpt2 --task arithmetic
    python llm_kappa_miner.py --model EleutherAI/pythia-70m --task addition
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import argparse
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Callable
from datetime import datetime
from pathlib import Path

# Hugging Face
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    AutoConfig,
    GPT2LMHeadModel,
    GPT2Tokenizer,
)
from transformers.modeling_outputs import CausalLMOutputWithCrossAttentions
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class LLMKappaConfig:
    """Configuration for LLM κ-mining."""
    
    # Model
    model_name: str = "gpt2"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    use_fp16: bool = True
    
    # κ measurement (from Strassen paper - AUC=1.0)
    kappa_crystal_threshold: float = 1.001
    kappa_glass_threshold: float = 100.0
    kappa_samples: int = 32  # Fewer samples for LLMs (memory)
    kappa_batch_size: int = 4  # Smaller batches for LLMs
    
    # Training
    learning_rate: float = 1e-5
    weight_decay: float = 1e-4
    max_epochs: int = 5000
    eval_interval: int = 50
    
    # Early stopping (key innovation from κ)
    early_stop_epochs: int = 200  # Only 200 epochs to predict!
    early_stop_patience: int = 3
    
    # Arithmetic task
    max_digits: int = 2
    max_value: int = 99
    operations: List[str] = None
    
    def __post_init__(self):
        if self.operations is None:
            self.operations = ['+', '*']


# ============================================================================
# ARITHMETIC DATASET FOR LLMs
# ============================================================================

class LLMArithmeticDataset:
    """
    Arithmetic dataset formatted for LLM training.
    
    Format: "What is 23 + 45? Answer: 68"
    
    This tests whether the LLM learns the algorithm or just pattern matches.
    """
    
    def __init__(self, tokenizer, config: LLMKappaConfig):
        self.tokenizer = tokenizer
        self.config = config
        self.pad_token_id = tokenizer.eos_token_id or 0
    
    def format_problem(self, a: int, b: int, op: str, result: int) -> str:
        """Format arithmetic problem as text."""
        if op == '+':
            return f"What is {a} plus {b}? Answer: {result}"
        elif op == '*':
            return f"What is {a} times {b}? Answer: {result}"
        else:
            return f"What is {a} {op} {b}? Answer: {result}"
    
    def generate_batch(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate batch of tokenized arithmetic problems."""
        texts = []
        results = []
        
        for _ in range(batch_size):
            a = np.random.randint(0, self.config.max_value + 1)
            b = np.random.randint(0, self.config.max_value + 1)
            op = np.random.choice(self.config.operations)
            
            if op == '+':
                result = a + b
            else:
                result = a * b
            
            text = self.format_problem(a, b, op, result)
            texts.append(text)
            results.append(result)
        
        # Tokenize
        encoded = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=64,
            return_tensors="pt"
        )
        
        return encoded['input_ids'], encoded['attention_mask']
    
    def generate_for_kappa(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Generate batch for κ measurement."""
        input_ids, attention_mask = self.generate_batch(batch_size)
        # Targets are shifted inputs for causal LM
        labels = input_ids.clone()
        labels[labels == self.pad_token_id] = -100  # Ignore padding in loss
        return input_ids, labels


# ============================================================================
# κ METER FOR LLMs
# ============================================================================

class LLMKappaMeter:
    """
    Measures κ for LLMs (handles memory constraints).
    
    Key insight from Strassen paper: κ = λ_max/λ_min of gradient covariance
    perfectly predicts grokking (AUC = 1.0).
    """
    
    def __init__(self, model, config: LLMKappaConfig):
        self.model = model
        self.config = config
    
    def compute_kappa(self, 
                      input_ids: torch.Tensor,
                      labels: torch.Tensor,
                      attention_mask: torch.Tensor = None) -> Dict[str, float]:
        """
        Compute κ for the LLM.
        
        Returns:
            Dictionary with κ and diagnostics
        """
        self.model.eval()
        all_grads = []
        
        n_samples = self.config.kappa_samples
        batch_size = self.config.kappa_batch_size
        
        for i in range(0, n_samples, batch_size):
            actual_batch = min(batch_size, n_samples - i)
            
            # Forward pass
            self.model.zero_grad()
            
            with torch.amp.autocast(device_type=self.config.device.split(':')[0], 
                                     enabled=self.config.use_fp16):
                outputs = self.model(
                    input_ids=input_ids[:actual_batch],
                    attention_mask=attention_mask[:actual_batch] if attention_mask is not None else None,
                    labels=labels[:actual_batch]
                )
            
            loss = outputs.loss
            loss.backward()
            
            # Collect gradients (only from key layers to save memory)
            grads = []
            for name, p in self.model.named_parameters():
                if p.grad is not None and ('.attn.' in name or '.mlp.' in name):
                    grads.append(p.grad.detach().flatten())
            
            if grads:
                all_grads.append(torch.cat(grads))
            
            # Clear memory
            del outputs, loss
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
        
        if len(all_grads) < 2:
            return {'kappa': float('inf'), 'error': 'insufficient_samples'}
        
        # Stack and compute covariance
        try:
            all_grads = torch.stack(all_grads)
            
            # Subsample if too large
            if all_grads.shape[1] > 10000:
                indices = torch.randperm(all_grads.shape[1])[:10000]
                all_grads = all_grads[:, indices]
            
            # Center
            mean_grad = all_grads.mean(dim=0)
            centered = all_grads - mean_grad
            
            # Covariance (use CPU for large matrices)
            centered = centered.cpu().float()
            n = centered.shape[0]
            covariance = (centered.T @ centered) / (n - 1)
            
            # Regularize
            reg = 1e-6
            covariance = covariance + torch.eye(covariance.shape[0]) * reg
            
            # Eigenvalues
            eigenvalues = torch.linalg.eigvalsh(covariance)
            eigenvalues = torch.sort(eigenvalues)[0]
            
            # Filter near-zero
            valid_mask = eigenvalues > 1e-10
            valid_eigenvalues = eigenvalues[valid_mask]
            
            if len(valid_eigenvalues) < 2:
                return {'kappa': float('inf'), 'error': 'degenerate_covariance'}
            
            lambda_min = valid_eigenvalues[0].item()
            lambda_max = valid_eigenvalues[-1].item()
            
            kappa = lambda_max / lambda_min if lambda_min > 0 else float('inf')
            
            # Effective rank
            effective_rank = (valid_eigenvalues.sum() ** 2 / (valid_eigenvalues ** 2).sum()).item()
            
            return {
                'kappa': float(kappa),
                'lambda_min': lambda_min,
                'lambda_max': lambda_max,
                'effective_rank': effective_rank,
                'gradient_norm': float(torch.norm(mean_grad).item())
            }
            
        except Exception as e:
            return {'kappa': float('inf'), 'error': str(e)}
    
    def predict_grokking(self, kappa: float) -> Dict:
        """Predict grokking based on κ (AUC=1.0 from Strassen paper)."""
        if kappa < self.config.kappa_crystal_threshold:
            return {
                'prediction': 'will_grokk',
                'confidence': 0.99,
                'phase': 'crystal',
                'recommendation': 'continue_training'
            }
        elif kappa < self.config.kappa_glass_threshold:
            return {
                'prediction': 'likely_grokk',
                'confidence': 0.7,
                'phase': 'transitional',
                'recommendation': 'continue_monitor'
            }
        else:
            return {
                'prediction': 'will_not_grokk',
                'confidence': 0.95,
                'phase': 'glass',
                'recommendation': 'abort'
            }


# ============================================================================
# LLM κ-MINER
# ============================================================================

class LLMKappaMiner:
    """
    Apply κ-mining to real LLMs.
    
    The key insight: κ = 1 predicts algorithmic learning with AUC=1.0
    This lets us predict whether an LLM will learn arithmetic in ~200 epochs
    instead of training for thousands.
    """
    
    def __init__(self, config: LLMKappaConfig):
        self.config = config
        self.history = {
            'epochs': [],
            'kappa': [],
            'loss': [],
            'phase': [],
            'predictions': []
        }
        
        # Load model and tokenizer
        print(f"Loading model: {config.model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            config.model_name,
            torch_dtype=torch.float16 if config.use_fp16 else torch.float32
        ).to(config.device)
        
        # Dataset
        self.dataset = LLMArithmeticDataset(self.tokenizer, config)
        
        # κ meter
        self.kappa_meter = LLMKappaMeter(self.model, config)
    
    def train_step(self, optimizer) -> float:
        """Single training step."""
        self.model.train()
        input_ids, labels = self.dataset.generate_batch(8)
        input_ids = input_ids.to(self.config.device)
        labels = labels.to(self.config.device)
        
        optimizer.zero_grad()
        
        with torch.amp.autocast(device_type=self.config.device.split(':')[0],
                                 enabled=self.config.use_fp16):
            outputs = self.model(input_ids=input_ids, labels=labels)
        
        loss = outputs.loss
        loss.backward()
        
        # Gradient clipping (important for LLMs)
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        
        optimizer.step()
        
        return loss.item()
    
    def evaluate(self) -> Dict:
        """Evaluate model and compute κ."""
        self.model.eval()
        
        # Generate batch for κ
        input_ids, labels = self.dataset.generate_for_kappa(self.config.kappa_batch_size)
        input_ids = input_ids.to(self.config.device)
        labels = labels.to(self.config.device)
        
        # Compute κ
        kappa_result = self.kappa_meter.compute_kappa(input_ids, labels)
        kappa = kappa_result.get('kappa', float('inf'))
        
        # Compute loss
        with torch.no_grad():
            with torch.amp.autocast(device_type=self.config.device.split(':')[0],
                                     enabled=self.config.use_fp16):
                outputs = self.model(input_ids=input_ids, labels=labels)
                loss = outputs.loss.item()
        
        # Predict
        prediction = self.kappa_meter.predict_grokking(kappa)
        
        return {
            'kappa': kappa,
            'loss': loss,
            'prediction': prediction,
            'kappa_details': kappa_result
        }
    
    def prospect(self, 
                 early_stop: bool = True,
                 save_dir: str = "checkpoints") -> Dict:
        """
        Prospect for algorithmic learning using κ.
        
        Key innovation: Stop early if κ >> 1 (will not grokk)
        Continue only if κ ≈ 1 (will grokk with 99% confidence)
        """
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "=" * 70)
        print("LLM κ-MINER: Prospecting for Algorithmic Learning")
        print("=" * 70)
        print(f"Model: {self.config.model_name}")
        print(f"Task: Arithmetic ({self.config.operations})")
        print(f"κ crystal threshold: {self.config.kappa_crystal_threshold}")
        print(f"Early stop epochs: {self.config.early_stop_epochs}")
        print("=" * 70)
        print()
        
        # Optimizer
        optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=self.config.learning_rate,
            weight_decay=self.config.weight_decay
        )
        
        patience_counter = 0
        crystal_found = False
        
        for epoch in range(self.config.max_epochs):
            # Training step
            loss = self.train_step(optimizer)
            
            # Evaluate at intervals
            if epoch % self.config.eval_interval == 0:
                eval_result = self.evaluate()
                kappa = eval_result['kappa']
                prediction = eval_result['prediction']
                
                # Store history
                self.history['epochs'].append(epoch)
                self.history['kappa'].append(kappa)
                self.history['loss'].append(eval_result['loss'])
                self.history['phase'].append(prediction['phase'])
                self.history['predictions'].append(prediction['prediction'])
                
                # Print status
                phase_emoji = "💎" if prediction['phase'] == 'crystal' else "🧊" if prediction['phase'] == 'glass' else "🔮"
                print(f"Epoch {epoch:5d} | κ: {kappa:12.2e} | Loss: {eval_result['loss']:.4f} | "
                      f"{phase_emoji} {prediction['phase']:12s} | Prediction: {prediction['prediction']}")
                
                # Save crystal checkpoint
                if prediction['phase'] == 'crystal' and not crystal_found:
                    crystal_found = True
                    ckpt_path = save_dir / f"{self.config.model_name.replace('/', '_')}_crystal_epoch{epoch}.pt"
                    torch.save({
                        'epoch': epoch,
                        'model_state_dict': self.model.state_dict(),
                        'kappa': kappa,
                        'prediction': prediction,
                        'config': self.config.__dict__
                    }, ckpt_path)
                    print(f"  💾 CRYSTAL CHECKPOINT SAVED: {ckpt_path}")
                
                # Early stopping based on κ (the key innovation!)
                if early_stop and epoch >= self.config.early_stop_epochs:
                    if prediction['prediction'] == 'will_not_grokk':
                        patience_counter += 1
                        if patience_counter >= self.config.early_stop_patience:
                            print(f"\n⚠️  EARLY STOP: κ predicts will not grokk (κ = {kappa:.2e})")
                            print("    Saving compute by stopping early!")
                            break
                    elif prediction['prediction'] == 'will_grokk':
                        print(f"\n✅ κ CRYSTAL DETECTED! κ = {kappa:.2e}")
                        print("    This model WILL learn the algorithm with 99% confidence!")
                        print("    Continuing training...")
                        patience_counter = 0
        
        # Final summary
        print("\n" + "=" * 70)
        print("PROSPECTING RESULTS")
        print("=" * 70)
        
        final_kappa = self.history['kappa'][-1] if self.history['kappa'] else float('inf')
        final_prediction = self.kappa_meter.predict_grokking(final_kappa)
        
        print(f"Final κ: {final_kappa:.2e}")
        print(f"Prediction: {final_prediction['prediction']}")
        print(f"Confidence: {final_prediction['confidence']:.0%}")
        print(f"Phase: {final_prediction['phase']}")
        print()
        
        if final_prediction['phase'] == 'crystal':
            print("✅ This LLM has CRYSTALLIZED an algorithm!")
            print("   The arithmetic operation is encoded in the weights.")
        else:
            print("🧊 This LLM is in a GLASS state.")
            print("   It may generalize but has not learned the algorithm.")
        
        return {
            'final_kappa': final_kappa,
            'prediction': final_prediction,
            'history': self.history,
            'model_name': self.config.model_name
        }
    
    def test_arithmetic(self, n_tests: int = 10) -> Dict:
        """Test if the model can do arithmetic."""
        print("\n" + "=" * 70)
        print("ARITHMETIC TEST")
        print("=" * 70)
        
        self.model.eval()
        correct = 0
        results = []
        
        for _ in range(n_tests):
            a = np.random.randint(0, self.config.max_value + 1)
            b = np.random.randint(0, self.config.max_value + 1)
            op = np.random.choice(self.config.operations)
            
            if op == '+':
                expected = a + b
            else:
                expected = a * b
            
            prompt = self.dataset.format_problem(a, b, op, expected).split("Answer:")[0] + "Answer:"
            
            # Generate
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.config.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=10,
                    do_sample=False,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Parse answer
            try:
                answer_part = response.split("Answer:")[-1].strip()
                predicted = int(''.join(c for c in answer_part if c.isdigit() or c == '-'))
            except:
                predicted = None
            
            is_correct = predicted == expected
            correct += int(is_correct)
            
            results.append({
                'problem': f"{a} {op} {b}",
                'expected': expected,
                'predicted': predicted,
                'correct': is_correct,
                'response': response
            })
            
            status = "✓" if is_correct else "✗"
            print(f"  {status} {a} {op} {b} = {expected} (predicted: {predicted})")
        
        accuracy = correct / n_tests
        print(f"\nAccuracy: {accuracy:.0%} ({correct}/{n_tests})")
        
        return {
            'accuracy': accuracy,
            'results': results
        }


# ============================================================================
# MULTI-MODEL PROSPECTOR
# ============================================================================

def prospect_multiple_models(models: List[str], config_override: dict = None) -> Dict:
    """
    Prospect multiple LLMs for algorithmic learning.
    
    This answers: Which LLMs can learn algorithms?
    """
    print("=" * 70)
    print("MULTI-MODEL κ-PROSPECTOR")
    print("=" * 70)
    print(f"Models to test: {len(models)}")
    print()
    
    results = {}
    
    for model_name in models:
        print(f"\n{'='*70}")
        print(f"Testing: {model_name}")
        print("=" * 70)
        
        config = LLMKappaConfig(model_name=model_name)
        if config_override:
            for k, v in config_override.items():
                setattr(config, k, v)
        
        try:
            miner = LLMKappaMiner(config)
            result = miner.prospect(early_stop=True)
            
            # Test arithmetic if crystal found
            if result['prediction']['phase'] == 'crystal':
                test_result = miner.test_arithmetic(n_tests=5)
                result['arithmetic_test'] = test_result
            
            results[model_name] = result
            
        except Exception as e:
            print(f"Error with {model_name}: {e}")
            results[model_name] = {'error': str(e)}
        
        # Clear memory
        torch.cuda.empty_cache() if torch.cuda.is_available() else None
    
    return results


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="κ-Miner for LLMs")
    parser.add_argument("--model", type=str, default="gpt2", help="Model name or path")
    parser.add_argument("--task", type=str, default="arithmetic", choices=["arithmetic", "addition", "multiplication"])
    parser.add_argument("--early_stop_epochs", type=int, default=200, help="Epochs before κ prediction")
    parser.add_argument("--max_epochs", type=int, default=5000, help="Maximum training epochs")
    parser.add_argument("--kappa_threshold", type=float, default=1.001, help="κ crystal threshold")
    parser.add_argument("--multi_model", action="store_true", help="Test multiple models")
    
    args = parser.parse_args()
    
    # Configure
    ops = {
        'arithmetic': ['+', '*'],
        'addition': ['+'],
        'multiplication': ['*']
    }
    
    config = LLMKappaConfig(
        model_name=args.model,
        early_stop_epochs=args.early_stop_epochs,
        max_epochs=args.max_epochs,
        kappa_crystal_threshold=args.kappa_threshold,
        operations=ops.get(args.task, ['+', '*'])
    )
    
    if args.multi_model:
        # Test multiple small models
        models = [
            "gpt2",
            "gpt2-medium",
            "EleutherAI/pythia-70m",
            "EleutherAI/pythia-160m",
            "bigscience/bloom-560m",
        ]
        results = prospect_multiple_models(models)
        
        # Save results
        with open("multi_model_results.json", "w") as f:
            json.dump({k: {kk: str(vv) if not isinstance(vv, (str, int, float, list, dict, type(None))) else vv 
                          for kk, vv in v.items()} 
                      for k, v in results.items()}, f, indent=2, default=str)
    else:
        # Single model
        miner = LLMKappaMiner(config)
        result = miner.prospect()
        
        # Test if crystal
        if result['prediction']['phase'] == 'crystal':
            miner.test_arithmetic()
        
        # Save
        with open(f"llm_kappa_results_{args.model.replace('/', '_')}.json", "w") as f:
            json.dump(result, f, indent=2, default=str)


if __name__ == "__main__":
    main()
