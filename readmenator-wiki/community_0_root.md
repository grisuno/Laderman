# root

*Community 0 | 2 files | cohesion 1.00*

## Definition

This community groups 2 file(s) rooted at `root` with dominant language py (cohesion 1.00). Central symbols: `AdaptiveAnnealingScheduler`, `AdaptiveTemperatureScheduler`, `CheckpointManager`, `ComprehensiveMetricsAggregator`, `DeltaCalculator`, `ExecutionMode`, `GlassDetector`, `GravitationalConstantCalculator`. Core file: `seed_miner.py` (77 symbols). Documented purpose: Leibler Transformer Seed Prospector.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `seed_miner.py` | py | data_access | 77 | yes |
| `tran5.py` | py | utility | 36 | yes |

## Key Symbols

- `ExecutionMode` (class, `seed_miner.py:63`) `class ExecutionMode(Enum)`
- `ProspectorConfig` (class, `seed_miner.py:69`) `class ProspectorConfig` - Immutable unified configuration for transformer seed prospecting.
- `IMetricCalculator` (class, `seed_miner.py:160`) `class IMetricCalculator(ABC)`
- `calculate` (method, `seed_miner.py:162`) `def calculate(self)`
- `ILossComponent` (class, `seed_miner.py:166`) `class ILossComponent(ABC)`
- `compute` (method, `seed_miner.py:168`) `def compute(self, model, loss_ce, epoch)`
- `ICheckpointManager` (class, `seed_miner.py:173`) `class ICheckpointManager(ABC)`
- `save` (method, `seed_miner.py:175`) `def save(self, state, path)`
- `load` (method, `seed_miner.py:179`) `def load(self, path)`
- `should_checkpoint` (method, `seed_miner.py:183`) `def should_checkpoint(self)`
- `ITrainingPhase` (class, `seed_miner.py:187`) `class ITrainingPhase(ABC)`
- `execute` (method, `seed_miner.py:189`) `def execute(self, model)`
- `build_leiderman_config` (method, `seed_miner.py:193`) `def build_leiderman_config(config)`
- `DeltaCalculator` (class, `seed_miner.py:239`) `class DeltaCalculator(IMetricCalculator)`
- `calculate` (method, `seed_miner.py:240`) `def calculate(self, model)`
- `KappaCalculator` (class, `seed_miner.py:257`) `class KappaCalculator`
- `__init__` (method, `seed_miner.py:258`) `def __init__(self, config)`
- `accumulate_gradient` (method, `seed_miner.py:265`) `def accumulate_gradient(self, model)`
- `calculate_kappa` (method, `seed_miner.py:276`) `def calculate_kappa(self)`
- `get_gradient_covariance` (method, `seed_miner.py:296`) `def get_gradient_covariance(self)`
- `get_kappa_trend` (method, `seed_miner.py:307`) `def get_kappa_trend(self)`
- `is_crystallizing` (method, `seed_miner.py:317`) `def is_crystallizing(self)`
- `reset` (method, `seed_miner.py:323`) `def reset(self)`
- `ThermodynamicMetricsCalculator` (class, `seed_miner.py:328`) `class ThermodynamicMetricsCalculator(IMetricCalculator)`
- `__init__` (method, `seed_miner.py:329`) `def __init__(self, config)`
- `calculate` (method, `seed_miner.py:332`) `def calculate(self, model, gradient_covariance)`
- `LocalComplexityCalculator` (class, `seed_miner.py:378`) `class LocalComplexityCalculator(IMetricCalculator)`
- `__init__` (method, `seed_miner.py:379`) `def __init__(self, config)`
- `calculate` (method, `seed_miner.py:382`) `def calculate(self, model, train_x, train_y, device)`
- `SuperpositionCalculator` (class, `seed_miner.py:430`) `class SuperpositionCalculator(IMetricCalculator)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 2
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- [INFERRED] shares_context community 0 <-> 1 (strength 0.5): Inferred shared context (language py and layer utility) with no import path between community 0 (root) and community 1 (orphans).

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- What would break if the most connected file in root changed?
- Should root be split, given cohesion 1.00?

## Sources

- `seed_miner.py`
- `tran5.py`
