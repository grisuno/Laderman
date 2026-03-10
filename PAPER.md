
The loss is MSE between predicted and true product. No explicit tensor decomposition is enforced; the model must discover it.

---

## 2. Method: Delta Prospecting and Batch Size Tuning

I reused the same prospecting metric that worked for Strassen and for the HPU‑Core: the discretisation margin δ = max|w − round(w)|, measured on all weights at epoch 25. In Strassen, δ < 0.1 at epoch 25 predicted later crystallisation with 68% probability; in the HPU‑Core, δ ≈ 0.46 at epoch 10 identified the only seed that eventually formed a topological crystal.

**Seed mining.** I initialised 200 independent transformers with default PyTorch initialisation and trained each for 500 epochs (learning rate 1e‑3, weight decay 1e‑4, batch size 64). Every 25 epochs I logged loss, test accuracy, δ, and – when computationally feasible – κ (the condition number of the gradient covariance). Mining stopped early if accuracy stagnated below 30% for 100 epochs.

**Batch size sweep.** Using a fixed seed (seed 66, which showed low δ early), I trained for 2000 epochs with batch sizes {16,24,32,48,64,96,128,192,256,384}. The score used to compare batch sizes was a composite of final accuracy, final δ, and the area under the accuracy curve – higher is better. This gave a map of the optimal batch regime.

---

## 3. Results

### 3.1 Initial δ distribution is bimodal

Of the 200 seeds, 198 exhibited δ ≈ 0.49–0.50 at epoch 25 – the same “glassy plateau” seen in Strassen and HPU. Two seeds deviated:

- **Seed 66**: δ = 0.1077 at epoch 25.
- **Seed 67**: δ = 0.0960 at epoch 25 (later lost due to low accuracy).

Both seeds reached test accuracy only 2–6% at epoch 25, which is typical: low δ precedes grokking, it does not guarantee immediate performance.

### 3.2 The δ ≈ 0.25 plateau

Seed 66 was trained to 5000 epochs. Its trajectory is instructive:

- **Epoch 25**: δ = 0.1077, acc ≈ 2%.
- **Epoch 100**: δ rises to 0.20, acc ≈ 30%.
- **Epoch 500**: δ stabilises at 0.255, acc ≈ 85%.
- **Epoch 2000–5000**: δ = 0.255 ± 0.001, acc = 94–96%.

The system has found a local minimum that generalises well (95% test accuracy) and is reasonably well‑conditioned (κ fluctuates between 2 and 400, often below 10). But it refuses to descend further toward the discrete integer coefficients of Laderman’s algorithm. The weights are not close to integers; the average distance to the nearest integer is about 0.25.

This is a **new phase** not seen in Strassen (which either crystallised or stayed at δ ≈ 0.5) nor in the HPU‑Core (which either stayed glassy or descended to δ ≈ 0.36 with topological protection). I call it a **low‑temperature glass**: functional, stable, but structurally amorphous.

### 3.3 Batch size robustness

The batch size sweep gave a surprising result: almost every tested batch size achieved a similar score (67–69). The optimum was shallow, with **batch size 64** scoring 69.15 and **batch size 384** scoring 66.64. Unlike Strassen, where the optimal window [24,128] was narrow and critical, Laderman in transformers tolerates a wide range of batch sizes. This suggests that the gradient noise geometry is less constraining for this architecture.

Nevertheless, the lowest δ values at epoch 25 were obtained with **batch size 384** (δ = 0.0939 for seed 69, though that seed later degraded). Large batches appear to help the initial alignment but do not prevent the eventual plateau.

### 3.4 κ and other metrics

κ was not a reliable early predictor in this transformer setting. During the plateau, κ often dropped to values near 1–2, indicating well‑conditioned gradients, yet δ did not improve. This contrasts with Strassen, where κ = 1.000 was the signature of the crystalline phase. Here, κ ≈ 2 is a signature of the glassy minimum.

Local complexity (LC) remained high (>0.8) throughout, confirming that no collapse to a low‑dimensional subspace occurred. The system retained many active degrees of freedom.

---

## 4. Discussion

### 4.1 What I have demonstrated

- **Delta prospecting transfers to transformers.** The bimodal distribution of initial δ (0.50 vs ≤0.11) is reproducible in this architecture. Low δ at epoch 25 is rare (≈1% of seeds) but real.
- **The Laderman landscape contains a deep glassy minimum at δ ≈ 0.25.** This minimum yields high test accuracy (95%), stable training, and good conditioning, yet resists discretisation. It is the primary obstacle to crystallisation.
- **Batch size is not a critical control parameter for this problem.** The wide optimum simplifies experimental design.

### 4.2 What I have not demonstrated

- **I have not crystallised Laderman.** No checkpoint has passed the structural verification test (all 23 coefficients within 0.1 of {-1,0,1}). The best δ achieved after 5000 epochs is 0.255, far above the 0.1 threshold.
- **I do not know why the δ = 0.25 plateau exists.** It may be an artifact of the transformer architecture (softmax attention, residual connections, layer norm) that biases weights away from extreme values. It may reflect the absence of a natural low‑rank decomposition in the standard parameterisation.
- **I have not tested whether different transformer variants (e.g., complex‑valued, no layernorm, etc.) can escape the plateau.** This is the obvious next step.

### 4.3 Comparison to Strassen and HPU‑Core

| Feature | Strassen (bilinear) | HPU‑Core (spectral) | Laderman (transformer) |
|--------|---------------------|----------------------|-------------------------|
| N seeds mined | 195 | 173 | 200 |
| Low‑δ seeds | many (68% success) | 2 | 2 |
| δ at plateau | n/a (crystal or glass) | 0.36 (topological) | **0.255 (functional glass)** |
| Accuracy at plateau | 100% | 100% | 95% |
| κ at plateau | 1.000 (crystal) | ∞ (singular) | 2–400 (well‑cond.) |
| Crystallisation | 68% | 1/2 | **0% (so far)** |

The Laderman experiment occupies a new row in this table. It proves that the prospecting method generalises, but it also reveals that **different algorithmic tasks have different phase diagrams**. Strassen had a discrete crystalline attractor; the HPU‑Core had a continuous topological attractor; Laderman (so far) has only a viscous glass.

---

## 5. Conclusion and Next Steps

I have turned the problem of learning Laderman’s algorithm from “impossible with bilinear nets” into a well‑posed optimisation problem with measurable progress. I can now reliably find seeds that start with δ < 0.11, and I can drive them to 95% accuracy with δ = 0.255. The remaining challenge is to break the glass.

I am currently testing three interventions:

1. **Extreme quantisation pressure** – adding a triple‑well loss that penalises weights not near {-1,0,1}, with an annealing schedule that increases the penalty once accuracy exceeds 90%.
2. **Pruning to 23 slots** – identifying the 23 most important attention heads or MLP neurons and forcing all others to zero, then fine‑tuning only the survivors.
3. **Complex‑valued transformers** – replacing real weights with complex numbers and regularising the phase, mimicking the mechanism that produced topological protection in the HPU‑Core.

If any of these succeed, Laderman will become the third documented case of algorithmic crystallisation, and the first in a transformer. If they all fail, the negative result is still informative: some algorithms may be fundamentally harder to crystallise than others, and 95% accuracy with a glassy weight distribution may be the best we can do.

All code, mined seeds, and batch‑sweep logs are available at the repository linked below. I encourage others to try their own interventions – the checkpoints of seed 66 (δ=0.1077@25) and its later plateau are included.

---

## Data Availability

- Repository: https://github.com/grisuno/Laderman  
- DOI: 10.5281/zenodo.18942839



### Seed Mining

Total attempts: 200

Top 5 seeds by delta:
  Seed    23: delta=0.085105 crystal= NO
  Seed    65: delta=0.086239 crystal= NO
  Seed    94: delta=0.086322 crystal= NO
  Seed    30: delta=0.087155 crystal= NO
  Seed    43: delta=0.087295 crystal= NO

best batch size : 64

scores
 - 16: 65.3953726887703
 - 24: 68.58160452842712
 - 32: 67.94222056865692
 - 48: 68.74871368408203
 - 64: 69.14564847946167
 - 96: 68.8098384141922
 - 128: 68.03004252910614
 - 192: 69.12730032205582
 - 256: 67.82097206115722
 - 384: 66.63907409906388

---

**grisun0**  
*March 2026*
