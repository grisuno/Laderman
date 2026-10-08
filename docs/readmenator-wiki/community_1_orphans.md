# orphans

*Community 1 | 10 files | cohesion 0.00*

## Definition

This community groups 10 file(s) rooted at `root` with dominant language py (cohesion 0.00). Central symbols: `AdaptiveAnnealingScheduler`, `Application`, `ArithmeticTask`, `BatchProspector`, `BilinearModel`, `BilinearTransformerModel`, `CheckpointManager`, `ChemicalPotentialScheduler`. Core file: `superconducting_transformer.py` (138 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: xx/xx/xxxx Licencia: GPL v3  Descripción:.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 0 | yes |
| `complex_leibler_transformer.py` | py | utility | 131 | yes |
| `install.sh` | sh | utility | 0 | no |
| `kappa_miner.py` | py | utility | 21 | yes |
| `laderman_batch_prospection.py` | py | utility | 18 | yes |
| `laderman_crystallization.py` | py | utility | 86 | yes |
| `llm_kappa_miner.py` | py | utility | 19 | yes |
| `superconducting_transformer.py` | py | utility | 138 | yes |
| `superconducting_transformer2.py` | py | utility | 137 | yes |
| `tran2.py` | py | utility | 46 | yes |

## Key Symbols

- `ExecutionMode` (class, `complex_leibler_transformer.py:59`) `class ExecutionMode(Enum)`
- `ProspectorConfig` (class, `complex_leibler_transformer.py:69`) `class ProspectorConfig`
- `IMetricCalculator` (class, `complex_leibler_transformer.py:197`) `class IMetricCalculator(ABC)`
- `calculate` (method, `complex_leibler_transformer.py:199`) `def calculate(self)`
- `ILossComponent` (class, `complex_leibler_transformer.py:203`) `class ILossComponent(ABC)`
- `compute` (method, `complex_leibler_transformer.py:205`) `def compute(self, model, loss_ce, epoch)`
- `ICheckpointManager` (class, `complex_leibler_transformer.py:210`) `class ICheckpointManager(ABC)`
- `save` (method, `complex_leibler_transformer.py:212`) `def save(self, state, path)`
- `load` (method, `complex_leibler_transformer.py:216`) `def load(self, path)`
- `should_checkpoint` (method, `complex_leibler_transformer.py:220`) `def should_checkpoint(self)`
- `ITrainingPhase` (class, `complex_leibler_transformer.py:224`) `class ITrainingPhase(ABC)`
- `execute` (method, `complex_leibler_transformer.py:226`) `def execute(self, model)`
- `IPhaseDetector` (class, `complex_leibler_transformer.py:230`) `class IPhaseDetector(ABC)`
- `detect` (method, `complex_leibler_transformer.py:232`) `def detect(self, metrics)`
- `IGlassDetector` (class, `complex_leibler_transformer.py:236`) `class IGlassDetector(ABC)`
- `should_stop` (method, `complex_leibler_transformer.py:238`) `def should_stop(self, epoch, metrics)`
- `IGrokkinDetector` (class, `complex_leibler_transformer.py:242`) `class IGrokkinDetector(ABC)`
- `update` (method, `complex_leibler_transformer.py:244`) `def update(self, metrics)`
- `SeedManager` (class, `complex_leibler_transformer.py:252`) `class SeedManager`
- `set_seed` (method, `complex_leibler_transformer.py:254`) `def set_seed(seed, device)`
- `ComplexOperations` (class, `complex_leibler_transformer.py:268`) `class ComplexOperations`
- `complex_linear` (method, `complex_leibler_transformer.py:271`) `def complex_linear(input_real, input_imag, weight_real, weight_imag, bias_real,`
- `complex_gelu` (method, `complex_leibler_transformer.py:288`) `def complex_gelu(real, imag)`
- `complex_layer_norm` (method, `complex_leibler_transformer.py:295`) `def complex_layer_norm(real, imag, weight, bias, eps)`
- `compute_phase` (method, `complex_leibler_transformer.py:311`) `def compute_phase(real, imag)`
- `compute_magnitude` (method, `complex_leibler_transformer.py:315`) `def compute_magnitude(real, imag)`
- `complex_softmax` (method, `complex_leibler_transformer.py:319`) `def complex_softmax(real, imag, temperature, dim)`
- `ComplexLinear` (class, `complex_leibler_transformer.py:337`) `class ComplexLinear(Module)`
- `__init__` (method, `complex_leibler_transformer.py:338`) `def __init__(self, in_features, out_features, bias, init_std)`
- `forward` (method, `complex_leibler_transformer.py:352`) `def forward(self, real, imag)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- [INFERRED] shares_context community 0 <-> 1 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root) and community 1 (orphans).

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 1 file(s) lack file-level docs (e.g. `install.sh`)? What purpose do they serve?
- What would break if the most connected file in orphans changed?
- Should orphans be split, given cohesion 0.00?

## Sources

- `app.py`
- `complex_leibler_transformer.py`
- `install.sh`
- `kappa_miner.py`
- `laderman_batch_prospection.py`
- `laderman_crystallization.py`
- `llm_kappa_miner.py`
- `superconducting_transformer.py`
- `superconducting_transformer2.py`
- `tran2.py`
