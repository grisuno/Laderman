# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM.
> No LLMs. No tokens. Pure static analysis. See more [here](https://github.com/grisuno/ReadMenator)

**Total Files Parsed:** 12 | **Total Symbols Extracted:** 709 | **Total Imports:** 158

## Structural Knowledge Map
```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray:5 5,color:#aaa;
    seed_miner_py["seed_miner.py (py)"]
    class seed_miner_py mod;
    seed_miner_py_ExecutionMode["ExecutionMode"]
    class seed_miner_py_ExecutionMode cls;
    seed_miner_py --> seed_miner_py_ExecutionMode
    seed_miner_py_ProspectorConfig["ProspectorConfig"]
    class seed_miner_py_ProspectorConfig cls;
    seed_miner_py --> seed_miner_py_ProspectorConfig
    seed_miner_py_IMetricCalculator["IMetricCalculator"]
    class seed_miner_py_IMetricCalculator cls;
    seed_miner_py --> seed_miner_py_IMetricCalculator
    seed_miner_py_ILossComponent["ILossComponent"]
    class seed_miner_py_ILossComponent cls;
    seed_miner_py --> seed_miner_py_ILossComponent
    seed_miner_py_ICheckpointManager["ICheckpointManager"]
    class seed_miner_py_ICheckpointManager cls;
    seed_miner_py --> seed_miner_py_ICheckpointManager
    superconducting_transformer_py["superconducting_transformer.py (py)"]
    class superconducting_transformer_py mod;
    superconducting_transformer_py_ExecutionMode["ExecutionMode"]
    class superconducting_transformer_py_ExecutionMode cls;
    superconducting_transformer_py --> superconducting_transformer_py_ExecutionMode
    superconducting_transformer_py_SuperconductorConfig["SuperconductorConfig"]
    class superconducting_transformer_py_SuperconductorConfig cls;
    superconducting_transformer_py --> superconducting_transformer_py_SuperconductorConfig
    superconducting_transformer_py_IMetricCalculator["IMetricCalculator"]
    class superconducting_transformer_py_IMetricCalculator cls;
    superconducting_transformer_py --> superconducting_transformer_py_IMetricCalculator
    superconducting_transformer_py_ILossComponent["ILossComponent"]
    class superconducting_transformer_py_ILossComponent cls;
    superconducting_transformer_py --> superconducting_transformer_py_ILossComponent
    superconducting_transformer_py_ICheckpointManager["ICheckpointManager"]
    class superconducting_transformer_py_ICheckpointManager cls;
    superconducting_transformer_py --> superconducting_transformer_py_ICheckpointManager
    superconducting_transformer2_py["superconducting_transformer2.py (py)"]
    class superconducting_transformer2_py mod;
    superconducting_transformer2_py_ExecutionMode["ExecutionMode"]
    class superconducting_transformer2_py_ExecutionMode cls;
    superconducting_transformer2_py --> superconducting_transformer2_py_ExecutionMode
    superconducting_transformer2_py_SuperconductorConfig["SuperconductorConfig"]
    class superconducting_transformer2_py_SuperconductorConfig cls;
    superconducting_transformer2_py --> superconducting_transformer2_py_SuperconductorConfig
    superconducting_transformer2_py_IMetricCalculator["IMetricCalculator"]
    class superconducting_transformer2_py_IMetricCalculator cls;
    superconducting_transformer2_py --> superconducting_transformer2_py_IMetricCalculator
    superconducting_transformer2_py_ILossComponent["ILossComponent"]
    class superconducting_transformer2_py_ILossComponent cls;
    superconducting_transformer2_py --> superconducting_transformer2_py_ILossComponent
    superconducting_transformer2_py_ICheckpointManager["ICheckpointManager"]
    class superconducting_transformer2_py_ICheckpointManager cls;
    superconducting_transformer2_py --> superconducting_transformer2_py_ICheckpointManager
    complex_leibler_transformer_py["complex_leibler_transformer.py (py)"]
    class complex_leibler_transformer_py mod;
    complex_leibler_transformer_py_ExecutionMode["ExecutionMode"]
    class complex_leibler_transformer_py_ExecutionMode cls;
    complex_leibler_transformer_py --> complex_leibler_transformer_py_ExecutionMode
    complex_leibler_transformer_py_ProspectorConfig["ProspectorConfig"]
    class complex_leibler_transformer_py_ProspectorConfig cls;
    complex_leibler_transformer_py --> complex_leibler_transformer_py_ProspectorConfig
    complex_leibler_transformer_py_IMetricCalculator["IMetricCalculator"]
    class complex_leibler_transformer_py_IMetricCalculator cls;
    complex_leibler_transformer_py --> complex_leibler_transformer_py_IMetricCalculator
    complex_leibler_transformer_py_ILossComponent["ILossComponent"]
    class complex_leibler_transformer_py_ILossComponent cls;
    complex_leibler_transformer_py --> complex_leibler_transformer_py_ILossComponent
    complex_leibler_transformer_py_ICheckpointManager["ICheckpointManager"]
    class complex_leibler_transformer_py_ICheckpointManager cls;
    complex_leibler_transformer_py --> complex_leibler_transformer_py_ICheckpointManager
    tran2_py["tran2.py (py)"]
    class tran2_py mod;
    tran2_py_LadermanConfig["LadermanConfig"]
    class tran2_py_LadermanConfig cls;
    tran2_py --> tran2_py_LadermanConfig
    tran2_py_ThermodynamicState["ThermodynamicState"]
    class tran2_py_ThermodynamicState cls;
    tran2_py --> tran2_py_ThermodynamicState
    tran2_py_MatrixMultiplicationDataset["MatrixMultiplicationDataset"]
    class tran2_py_MatrixMultiplicationDataset cls;
    tran2_py --> tran2_py_MatrixMultiplicationDataset
    tran2_py_BilinearTransformerModel["BilinearTransformerModel"]
    class tran2_py_BilinearTransformerModel cls;
    tran2_py --> tran2_py_BilinearTransformerModel
    tran2_py_GradientCovarianceComputer["GradientCovarianceComputer"]
    class tran2_py_GradientCovarianceComputer cls;
    tran2_py --> tran2_py_GradientCovarianceComputer
    laderman_crystallization_py["laderman_crystallization.py (py)"]
    class laderman_crystallization_py mod;
    laderman_crystallization_py_LadermanConfig["LadermanConfig"]
    class laderman_crystallization_py_LadermanConfig cls;
    laderman_crystallization_py --> laderman_crystallization_py_LadermanConfig
    laderman_crystallization_py_ThermodynamicState["ThermodynamicState"]
    class laderman_crystallization_py_ThermodynamicState cls;
    laderman_crystallization_py --> laderman_crystallization_py_ThermodynamicState
    laderman_crystallization_py_MetricComputerInterface["MetricComputerInterface"]
    class laderman_crystallization_py_MetricComputerInterface cls;
    laderman_crystallization_py --> laderman_crystallization_py_MetricComputerInterface
    laderman_crystallization_py_GradientCovarianceComputer["GradientCovarianceComputer"]
    class laderman_crystallization_py_GradientCovarianceComputer cls;
    laderman_crystallization_py --> laderman_crystallization_py_GradientCovarianceComputer
    laderman_crystallization_py_LocalComplexityComputer["LocalComplexityComputer"]
    class laderman_crystallization_py_LocalComplexityComputer cls;
    laderman_crystallization_py --> laderman_crystallization_py_LocalComplexityComputer
    llm_kappa_miner_py["llm_kappa_miner.py (py)"]
    class llm_kappa_miner_py mod;
    llm_kappa_miner_py_LLMKappaConfig["LLMKappaConfig"]
    class llm_kappa_miner_py_LLMKappaConfig cls;
    llm_kappa_miner_py --> llm_kappa_miner_py_LLMKappaConfig
    llm_kappa_miner_py_LLMArithmeticDataset["LLMArithmeticDataset"]
    class llm_kappa_miner_py_LLMArithmeticDataset cls;
    llm_kappa_miner_py --> llm_kappa_miner_py_LLMArithmeticDataset
    llm_kappa_miner_py_LLMKappaMeter["LLMKappaMeter"]
    class llm_kappa_miner_py_LLMKappaMeter cls;
    llm_kappa_miner_py --> llm_kappa_miner_py_LLMKappaMeter
    llm_kappa_miner_py_LLMKappaMiner["LLMKappaMiner"]
    class llm_kappa_miner_py_LLMKappaMiner cls;
    llm_kappa_miner_py --> llm_kappa_miner_py_LLMKappaMiner
    llm_kappa_miner_py_prospect_multiple_models["prospect_multiple_models"]
    class llm_kappa_miner_py_prospect_multiple_models fn;
    llm_kappa_miner_py --> llm_kappa_miner_py_prospect_multiple_models
    laderman_batch_prospection_py["laderman_batch_prospection.py (py)"]
    class laderman_batch_prospection_py mod;
    laderman_batch_prospection_py_ProspectionConfig["ProspectionConfig"]
    class laderman_batch_prospection_py_ProspectionConfig cls;
    laderman_batch_prospection_py --> laderman_batch_prospection_py_ProspectionConfig
    laderman_batch_prospection_py_MatrixMultiplicationDataset["MatrixMultiplicationDataset"]
    class laderman_batch_prospection_py_MatrixMultiplicationDataset cls;
    laderman_batch_prospection_py --> laderman_batch_prospection_py_MatrixMultiplicationDataset
    laderman_batch_prospection_py_BilinearModel["BilinearModel"]
    class laderman_batch_prospection_py_BilinearModel cls;
    laderman_batch_prospection_py --> laderman_batch_prospection_py_BilinearModel
    laderman_batch_prospection_py_compute_kappa["compute_kappa"]
    class laderman_batch_prospection_py_compute_kappa fn;
    laderman_batch_prospection_py --> laderman_batch_prospection_py_compute_kappa
    laderman_batch_prospection_py_compute_local_complexity["compute_local_complexity"]
    class laderman_batch_prospection_py_compute_local_complexity fn;
    laderman_batch_prospection_py --> laderman_batch_prospection_py_compute_local_complexity
    kappa_miner_py["kappa_miner.py (py)"]
    class kappa_miner_py mod;
    kappa_miner_py_KappaConfig["KappaConfig"]
    class kappa_miner_py_KappaConfig cls;
    kappa_miner_py --> kappa_miner_py_KappaConfig
    kappa_miner_py_KappaMeter["KappaMeter"]
    class kappa_miner_py_KappaMeter cls;
    kappa_miner_py --> kappa_miner_py_KappaMeter
    kappa_miner_py_ArithmeticTask["ArithmeticTask"]
    class kappa_miner_py_ArithmeticTask cls;
    kappa_miner_py --> kappa_miner_py_ArithmeticTask
    kappa_miner_py_MinimalTransformer["MinimalTransformer"]
    class kappa_miner_py_MinimalTransformer cls;
    kappa_miner_py --> kappa_miner_py_MinimalTransformer
    kappa_miner_py_KappaMiner["KappaMiner"]
    class kappa_miner_py_KappaMiner cls;
    kappa_miner_py --> kappa_miner_py_KappaMiner
    tran5_py["tran5.py (py)"]
    class tran5_py mod;
    tran5_py_LeidermanConfig["LeidermanConfig"]
    class tran5_py_LeidermanConfig cls;
    tran5_py --> tran5_py_LeidermanConfig
    tran5_py_LeiblerAttention["LeiblerAttention"]
    class tran5_py_LeiblerAttention cls;
    tran5_py --> tran5_py_LeiblerAttention
    tran5_py_LeiblerTransformerLayer["LeiblerTransformerLayer"]
    class tran5_py_LeiblerTransformerLayer cls;
    tran5_py --> tran5_py_LeiblerTransformerLayer
    tran5_py_LeiblerTransformer["LeiblerTransformer"]
    class tran5_py_LeiblerTransformer cls;
    tran5_py --> tran5_py_LeiblerTransformer
    tran5_py_AdaptiveTemperatureScheduler["AdaptiveTemperatureScheduler"]
    class tran5_py_AdaptiveTemperatureScheduler cls;
    tran5_py --> tran5_py_AdaptiveTemperatureScheduler
    app_py["app.py (py)"]
    class app_py mod;
    install_sh["install.sh (sh)"]
    class install_sh mod;
    ext_argparse["argparse"]
    class ext_argparse ext;
    complex_leibler_transformer_py -.->|imports| ext_argparse
    ext_torch["torch"]
    class ext_torch ext;
    complex_leibler_transformer_py -.->|imports| ext_torch
    ext_torch_nn["torch.nn"]
    class ext_torch_nn ext;
    complex_leibler_transformer_py -.->|imports| ext_torch_nn
    ext_torch_nn_functional["torch.nn.functional"]
    class ext_torch_nn_functional ext;
    complex_leibler_transformer_py -.->|imports| ext_torch_nn_functional
    ext_torch_optim["torch.optim"]
    class ext_torch_optim ext;
    complex_leibler_transformer_py -.->|imports| ext_torch_optim
    ext_numpy["numpy"]
    class ext_numpy ext;
    complex_leibler_transformer_py -.->|imports| ext_numpy
    ext_json["json"]
    class ext_json ext;
    complex_leibler_transformer_py -.->|imports| ext_json
    ext_os["os"]
    class ext_os ext;
    complex_leibler_transformer_py -.->|imports| ext_os
    ext_sys["sys"]
    class ext_sys ext;
    complex_leibler_transformer_py -.->|imports| ext_sys
    ext_math["math"]
    class ext_math ext;
    complex_leibler_transformer_py -.->|imports| ext_math
    ext_time["time"]
    class ext_time ext;
    complex_leibler_transformer_py -.->|imports| ext_time
    ext_signal["signal"]
    class ext_signal ext;
    complex_leibler_transformer_py -.->|imports| ext_signal
    ext_warnings["warnings"]
    class ext_warnings ext;
    complex_leibler_transformer_py -.->|imports| ext_warnings
    ext_pathlib["pathlib"]
    class ext_pathlib ext;
    complex_leibler_transformer_py -.->|imports| ext_pathlib
    ext_dataclasses["dataclasses"]
    class ext_dataclasses ext;
    complex_leibler_transformer_py -.->|imports| ext_dataclasses
    ext_typing["typing"]
    class ext_typing ext;
    complex_leibler_transformer_py -.->|imports| ext_typing
    ext_abc["abc"]
    class ext_abc ext;
    complex_leibler_transformer_py -.->|imports| ext_abc
    ext_collections["collections"]
    class ext_collections ext;
    complex_leibler_transformer_py -.->|imports| ext_collections
    ext_datetime["datetime"]
    class ext_datetime ext;
    complex_leibler_transformer_py -.->|imports| ext_datetime
    ext_enum["enum"]
    class ext_enum ext;
    complex_leibler_transformer_py -.->|imports| ext_enum
    kappa_miner_py -.->|imports| ext_torch
    kappa_miner_py -.->|imports| ext_torch_nn
    kappa_miner_py -.->|imports| ext_torch_nn_functional
    kappa_miner_py -.->|imports| ext_numpy
    kappa_miner_py -.->|imports| ext_json
    kappa_miner_py -.->|imports| ext_math
    kappa_miner_py -.->|imports| ext_dataclasses
    kappa_miner_py -.->|imports| ext_typing
    kappa_miner_py -.->|imports| ext_pathlib
    kappa_miner_py -.->|imports| ext_datetime
    kappa_miner_py -.->|imports| ext_warnings
    laderman_batch_prospection_py -.->|imports| ext_torch
    laderman_batch_prospection_py -.->|imports| ext_torch_nn
    laderman_batch_prospection_py -.->|imports| ext_torch_nn_functional
    ext_torch_utils_data["torch.utils.data"]
    class ext_torch_utils_data ext;
    laderman_batch_prospection_py -.->|imports| ext_torch_utils_data
    laderman_batch_prospection_py -.->|imports| ext_numpy
    laderman_batch_prospection_py -.->|imports| ext_json
    laderman_batch_prospection_py -.->|imports| ext_time
    laderman_batch_prospection_py -.->|imports| ext_math
    laderman_batch_prospection_py -.->|imports| ext_dataclasses
    laderman_batch_prospection_py -.->|imports| ext_pathlib
    laderman_batch_prospection_py -.->|imports| ext_typing
    laderman_batch_prospection_py -.->|imports| ext_collections
    ext_tqdm_auto["tqdm.auto"]
    class ext_tqdm_auto ext;
    laderman_batch_prospection_py -.->|imports| ext_tqdm_auto
    laderman_crystallization_py -.->|imports| ext_torch
    laderman_crystallization_py -.->|imports| ext_torch_nn
    laderman_crystallization_py -.->|imports| ext_torch_nn_functional
    laderman_crystallization_py -.->|imports| ext_torch_utils_data
    laderman_crystallization_py -.->|imports| ext_numpy
    laderman_crystallization_py -.->|imports| ext_time
    laderman_crystallization_py -.->|imports| ext_math
    laderman_crystallization_py -.->|imports| ext_typing
    laderman_crystallization_py -.->|imports| ext_dataclasses
    laderman_crystallization_py -.->|imports| ext_abc
    laderman_crystallization_py -.->|imports| ext_pathlib
    laderman_crystallization_py -.->|imports| ext_collections
    laderman_crystallization_py -.->|imports| ext_tqdm_auto
    llm_kappa_miner_py -.->|imports| ext_torch
    llm_kappa_miner_py -.->|imports| ext_torch_nn
    llm_kappa_miner_py -.->|imports| ext_torch_nn_functional
    llm_kappa_miner_py -.->|imports| ext_numpy
    llm_kappa_miner_py -.->|imports| ext_argparse
    llm_kappa_miner_py -.->|imports| ext_json
    llm_kappa_miner_py -.->|imports| ext_dataclasses
    llm_kappa_miner_py -.->|imports| ext_typing
    llm_kappa_miner_py -.->|imports| ext_datetime
    llm_kappa_miner_py -.->|imports| ext_pathlib
    ext_transformers["transformers"]
    class ext_transformers ext;
    llm_kappa_miner_py -.->|imports| ext_transformers
    ext_transformers_modeling_outputs["transformers.modeling_outputs"]
    class ext_transformers_modeling_outputs ext;
    llm_kappa_miner_py -.->|imports| ext_transformers_modeling_outputs
    llm_kappa_miner_py -.->|imports| ext_warnings
    seed_miner_py -.->|imports| ext_argparse
    seed_miner_py -.->|imports| ext_torch
    seed_miner_py -.->|imports| ext_torch_nn
    seed_miner_py -.->|imports| ext_torch_nn_functional
    seed_miner_py -.->|imports| ext_torch_optim
    seed_miner_py -.->|imports| ext_numpy
    seed_miner_py -.->|imports| ext_json
    seed_miner_py -.->|imports| ext_os
    seed_miner_py -.->|imports| ext_sys
    seed_miner_py -.->|imports| ext_math
    seed_miner_py -.->|imports| ext_time
    seed_miner_py -.->|imports| ext_signal
    seed_miner_py -.->|imports| ext_pathlib
    seed_miner_py -.->|imports| ext_dataclasses
    seed_miner_py -.->|imports| ext_typing
    seed_miner_py -.->|imports| ext_abc
    seed_miner_py -.->|imports| ext_collections
    seed_miner_py -.->|imports| ext_datetime
    seed_miner_py -.->|imports| ext_enum
    seed_miner_py -.->|imports| ext_warnings
    ext_tran5["tran5"]
    class ext_tran5 ext;
    seed_miner_py -.->|imports| ext_tran5
    seed_miner_py -.->|imports| ext_tran5
    seed_miner_py -.->|imports| ext_dataclasses
    superconducting_transformer_py -.->|imports| ext_argparse
    superconducting_transformer_py -.->|imports| ext_torch
    superconducting_transformer_py -.->|imports| ext_torch_nn
    superconducting_transformer_py -.->|imports| ext_torch_nn_functional
    superconducting_transformer_py -.->|imports| ext_torch_optim
    superconducting_transformer_py -.->|imports| ext_numpy
    superconducting_transformer_py -.->|imports| ext_json
    superconducting_transformer_py -.->|imports| ext_os
    superconducting_transformer_py -.->|imports| ext_sys
    superconducting_transformer_py -.->|imports| ext_math
    superconducting_transformer_py -.->|imports| ext_time
    superconducting_transformer_py -.->|imports| ext_signal
    superconducting_transformer_py -.->|imports| ext_warnings
    superconducting_transformer_py -.->|imports| ext_pathlib
    superconducting_transformer_py -.->|imports| ext_dataclasses
    superconducting_transformer_py -.->|imports| ext_typing
    superconducting_transformer_py -.->|imports| ext_abc
    superconducting_transformer_py -.->|imports| ext_collections
    superconducting_transformer_py -.->|imports| ext_datetime
    superconducting_transformer_py -.->|imports| ext_enum
    superconducting_transformer2_py -.->|imports| ext_argparse
    superconducting_transformer2_py -.->|imports| ext_torch
    superconducting_transformer2_py -.->|imports| ext_torch_nn
    superconducting_transformer2_py -.->|imports| ext_torch_nn_functional
    superconducting_transformer2_py -.->|imports| ext_torch_optim
    superconducting_transformer2_py -.->|imports| ext_numpy
    superconducting_transformer2_py -.->|imports| ext_json
    superconducting_transformer2_py -.->|imports| ext_os
    superconducting_transformer2_py -.->|imports| ext_sys
    superconducting_transformer2_py -.->|imports| ext_math
    superconducting_transformer2_py -.->|imports| ext_time
    superconducting_transformer2_py -.->|imports| ext_signal
    superconducting_transformer2_py -.->|imports| ext_warnings
    superconducting_transformer2_py -.->|imports| ext_pathlib
    superconducting_transformer2_py -.->|imports| ext_dataclasses
    superconducting_transformer2_py -.->|imports| ext_typing
    superconducting_transformer2_py -.->|imports| ext_abc
    superconducting_transformer2_py -.->|imports| ext_collections
    superconducting_transformer2_py -.->|imports| ext_datetime
    superconducting_transformer2_py -.->|imports| ext_enum
    tran2_py -.->|imports| ext_torch
    tran2_py -.->|imports| ext_torch_nn
    tran2_py -.->|imports| ext_torch_nn_functional
    tran2_py -.->|imports| ext_torch_utils_data
    tran2_py -.->|imports| ext_numpy
    tran2_py -.->|imports| ext_json
    tran2_py -.->|imports| ext_os
    tran2_py -.->|imports| ext_time
    tran2_py -.->|imports| ext_math
    tran2_py -.->|imports| ext_warnings
    tran2_py -.->|imports| ext_typing
    tran2_py -.->|imports| ext_dataclasses
    tran2_py -.->|imports| ext_abc
    tran2_py -.->|imports| ext_pathlib
    tran2_py -.->|imports| ext_collections
    tran2_py -.->|imports| ext_tqdm_auto
    tran5_py -.->|imports| ext_torch
    tran5_py -.->|imports| ext_torch_nn
    tran5_py -.->|imports| ext_torch_nn_functional
    tran5_py -.->|imports| ext_numpy
    tran5_py -.->|imports| ext_dataclasses
    tran5_py -.->|imports| ext_typing
    ext_tqdm["tqdm"]
    class ext_tqdm ext;
    tran5_py -.->|imports| ext_tqdm
    tran5_py -.->|imports| ext_argparse
    tran5_py -.->|imports| ext_datetime
```

---

## Architecture Reference

### PY (11 files)

#### `app.py`
**Path:** `app.py`

*No symbols extracted*

#### `complex_leibler_transformer.py`
**Path:** `complex_leibler_transformer.py`

**Classes:**
- `ExecutionMode` (line 59) `class ExecutionMode(Enum)`
- `ProspectorConfig` (line 69) `class ProspectorConfig`
- `IMetricCalculator` (line 197) `class IMetricCalculator(ABC)`
- `ILossComponent` (line 203) `class ILossComponent(ABC)`
- `ICheckpointManager` (line 210) `class ICheckpointManager(ABC)`
- `ITrainingPhase` (line 224) `class ITrainingPhase(ABC)`
- `IPhaseDetector` (line 230) `class IPhaseDetector(ABC)`
- `IGlassDetector` (line 236) `class IGlassDetector(ABC)`
- `IGrokkinDetector` (line 242) `class IGrokkinDetector(ABC)`
- `SeedManager` (line 252) `class SeedManager`
- `ComplexOperations` (line 268) `class ComplexOperations`
- `ComplexLinear` (line 337) `class ComplexLinear`
- `ComplexLayerNorm` (line 364) `class ComplexLayerNorm`
- `ComplexLeiblerAttention` (line 379) `class ComplexLeiblerAttention`
- `ComplexLeiblerTransformerLayer` (line 485) `class ComplexLeiblerTransformerLayer`
- `ComplexLeiblerTransformer` (line 529) `class ComplexLeiblerTransformer`
- `ModularAdditionDatasetFactory` (line 653) `class ModularAdditionDatasetFactory`
- `TrainingPrimitives` (line 688) `class TrainingPrimitives`
- `DeltaCalculator` (line 754) `class DeltaCalculator(IMetricCalculator)`
- `KappaCalculator` (line 772) `class KappaCalculator`
- `ThermodynamicMetricsCalculator` (line 841) `class ThermodynamicMetricsCalculator(IMetricCalculator)`
- `LocalComplexityCalculator` (line 894) `class LocalComplexityCalculator(IMetricCalculator)`
- `SuperpositionCalculator` (line 949) `class SuperpositionCalculator(IMetricCalculator)`
- `GravitationalConstantCalculator` (line 988) `class GravitationalConstantCalculator(IMetricCalculator)`
- `ComplexPhaseMetricsCalculator` (line 1003) `class ComplexPhaseMetricsCalculator(IMetricCalculator)`
- `PhaseDetector` (line 1015) `class PhaseDetector(IPhaseDetector)`
- `AdaptiveAnnealingScheduler` (line 1058) `class AdaptiveAnnealingScheduler`
- `GlassDetector` (line 1130) `class GlassDetector(IGlassDetector)`
- `GrokkinDetector` (line 1169) `class GrokkinDetector(IGrokkinDetector)`
- `CheckpointManager` (line 1205) `class CheckpointManager(ICheckpointManager)`
- `ModelPruner` (line 1241) `class ModelPruner`
- `ModelDiscretizer` (line 1261) `class ModelDiscretizer`
- `ComplexPhaseLoss` (line 1296) `class ComplexPhaseLoss(ILossComponent)`
- `ComprehensiveMetricsAggregator` (line 1335) `class ComprehensiveMetricsAggregator`
- `DisplayFormatter` (line 1444) `class DisplayFormatter`
- `ProspectorPhase` (line 1464) `class ProspectorPhase(ITrainingPhase)`
- `LongTrainingPhase` (line 1651) `class LongTrainingPhase(ITrainingPhase)`
- `SeedProspector` (line 1877) `class SeedProspector`
- `LongTrainingPipeline` (line 2020) `class LongTrainingPipeline`
- `Application` (line 2151) `class Application`

**Functions:**
- `main` (line 2238) `def main()`
- `calculate` (line 199) `def calculate(self)`
- `compute` (line 205) `def compute(self, model, loss_ce, epoch)`
- `save` (line 212) `def save(self, state, path)`
- `load` (line 216) `def load(self, path)`
- `should_checkpoint` (line 220) `def should_checkpoint(self)`
- `execute` (line 226) `def execute(self, model)`
- `detect` (line 232) `def detect(self, metrics)`
- `should_stop` (line 238) `def should_stop(self, epoch, metrics)`
- `update` (line 244) `def update(self, metrics)`
- `set_seed` (line 254) `def set_seed(seed, device)`
- `complex_linear` (line 271) `def complex_linear(input_real, input_imag, weight_real, weight_imag, bias_real, bias_imag)`
- `complex_gelu` (line 288) `def complex_gelu(real, imag)`
- `complex_layer_norm` (line 295) `def complex_layer_norm(real, imag, weight, bias, eps)`
- `compute_phase` (line 311) `def compute_phase(real, imag)`
- `compute_magnitude` (line 315) `def compute_magnitude(real, imag)`
- `complex_softmax` (line 319) `def complex_softmax(real, imag, temperature, dim)`
- `__init__` (line 338) `def __init__(self, in_features, out_features, bias, init_std)`
- `forward` (line 352) `def forward(self, real, imag)`
- `__init__` (line 365) `def __init__(self, normalized_shape, eps)`
- `forward` (line 371) `def forward(self, real, imag)`
- `__init__` (line 380) `def __init__(self, config)`
- `forward` (line 404) `def forward(self, real, imag, mask)`
- `_update_thermodynamic_state` (line 450) `def _update_thermodynamic_state(self, attn_real, attn_imag)`
- `__init__` (line 486) `def __init__(self, config)`
- `forward` (line 498) `def forward(self, real, imag, mask)`
- `__init__` (line 530) `def __init__(self, config)`
- `_init_weights` (line 554) `def _init_weights(self)`
- `forward` (line 564) `def forward(self, x, mask)`
- `get_thermodynamic_state` (line 584) `def get_thermodynamic_state(self)`
- `get_complex_weight_statistics` (line 610) `def get_complex_weight_statistics(self)`
- `create` (line 655) `def create(modulus, train_fraction)`
- `train_epoch` (line 690) `def train_epoch(model, train_x, train_y, optimizer, config, device)`
- `evaluate` (line 724) `def evaluate(model, test_x, test_y, config, device)`
- `__init__` (line 755) `def __init__(self, config)`
- `calculate` (line 758) `def calculate(self, model)`
- `__init__` (line 773) `def __init__(self, config)`
- `accumulate_gradient` (line 778) `def accumulate_gradient(self, model)`
- `calculate_kappa` (line 789) `def calculate_kappa(self)`
- `get_gradient_covariance` (line 809) `def get_gradient_covariance(self)`
- `get_kappa_trend` (line 820) `def get_kappa_trend(self)`
- `is_crystallizing` (line 830) `def is_crystallizing(self)`
- `reset` (line 836) `def reset(self)`
- `__init__` (line 842) `def __init__(self, config)`
- `calculate` (line 845) `def calculate(self, model, gradient_covariance)`
- `__init__` (line 895) `def __init__(self, config)`
- `calculate` (line 898) `def calculate(self, model, train_x, train_y, device)`
- `__init__` (line 950) `def __init__(self, config)`
- `_initialize_sae` (line 955) `def _initialize_sae(self, input_dim, device)`
- `calculate` (line 961) `def calculate(self, model)`
- `__init__` (line 989) `def __init__(self, config)`
- `calculate` (line 992) `def calculate(self, model)`
- `__init__` (line 1004) `def __init__(self, config)`
- `calculate` (line 1007) `def calculate(self, model)`
- `__init__` (line 1016) `def __init__(self, config)`
- `detect` (line 1021) `def detect(self, metrics)`
- `__init__` (line 1059) `def __init__(self, model, config, optimizer)`
- `step` (line 1074) `def step(self, metrics)`
- `_update_model_temperatures` (line 1117) `def _update_model_temperatures(self)`
- `_update_optimizer_weight_decay` (line 1121) `def _update_optimizer_weight_decay(self)`
- `__init__` (line 1131) `def __init__(self, config)`
- `should_stop` (line 1135) `def should_stop(self, epoch, metrics)`
- `__init__` (line 1170) `def __init__(self, config)`
- `update` (line 1177) `def update(self, metrics)`
- `__init__` (line 1206) `def __init__(self, config)`
- `save` (line 1212) `def save(self, state, path)`
- `load` (line 1221) `def load(self, path)`
- `should_checkpoint` (line 1228) `def should_checkpoint(self)`
- `get_latest_path` (line 1232) `def get_latest_path(self)`
- `prune` (line 1243) `def prune(model, threshold)`
- `discretize` (line 1263) `def discretize(model, tolerance)`
- `__init__` (line 1297) `def __init__(self, config)`
- `compute` (line 1300) `def compute(self, model, loss_ce, epoch)`
- `__init__` (line 1336) `def __init__(self, config)`
- `compute_all` (line 1347) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- `accumulate_gradient` (line 1432) `def accumulate_gradient(self, model)`
- `reset` (line 1435) `def reset(self)`
- `format_kappa` (line 1446) `def format_kappa(kappa, max_display)`
- `format_lc` (line 1452) `def format_lc(lc)`
- `__init__` (line 1465) `def __init__(self, config, seed)`
- `execute` (line 1469) `def execute(self, model)`
- `__init__` (line 1652) `def __init__(self, config)`
- `execute` (line 1656) `def execute(self, model)`
- `__init__` (line 1878) `def __init__(self, config)`
- `prospect` (line 1885) `def prospect(self, total_attempts, start_seed)`
- `__init__` (line 2021) `def __init__(self, config)`
- `_signal_handler` (line 2029) `def _signal_handler(self, signum, frame)`
- `run` (line 2033) `def run(self, resume_from, seed)`
- `__init__` (line 2152) `def __init__(self)`
- `_create_argument_parser` (line 2155) `def _create_argument_parser(self)`
- `run` (line 2190) `def run(self)`

#### `kappa_miner.py`
**Path:** `kappa_miner.py`

**Classes:**
- `KappaConfig` (line 39) `class KappaConfig` - *Configuration for κ-mining experiments.*
- `KappaMeter` (line 68) `class KappaMeter` - *Measures κ(Σ) = λ_max/λ_min of gradient covariance matrix.

This is the core metric that predicts grokking with AUC=1.0.*
- `ArithmeticTask` (line 201) `class ArithmeticTask` - *Arithmetic task for testing κ prediction on transformers.

Models must learn to:
- Add numbers (a + b = c)
- Multiply numbers (a * b = c)
- Combined operations

This is a canonical "algorithmic" task that requires learning
exact computation, not just pattern matching.*
- `MinimalTransformer` (line 316) `class MinimalTransformer` - *Minimal transformer for arithmetic tasks.

Architecture designed to be small enough to train quickly
but expressive enough to learn algorithms.*
- `KappaMiner` (line 391) `class KappaMiner` - *Main class for κ-mining experiments on LLMs.

Uses κ to predict algorithmic learning before training completes,
based on the AUC=1.0 result from Strassen paper.*
- `BatchProspector` (line 563) `class BatchProspector` - *Prospect multiple seeds/configurations to find crystals efficiently.

Uses κ-mining to avoid wasting compute on configurations that
will not grokk.*

**Functions:**
- `__init__` (line 75) `def __init__(self, config)`
- `compute_kappa` (line 78) `def compute_kappa(self, model, loss_fn, data_generator, n_samples, batch_size)` - *Compute gradient covariance condition number κ.

Returns:
    Dictionary with κ, eigenvalues, and diagnostics*
- `predict_grokking` (line 168) `def predict_grokking(self, kappa)` - *Predict whether model will grokk based on κ.

Returns prediction with confidence based on Strassen paper results.*
- `__init__` (line 214) `def __init__(self, max_digits, operations, tokenizer_vocab)` - *Args:
    max_digits: Maximum number of digits per operand
    operations: List of operations ['+', '-', '*']
    tokenizer_vocab: Vocabulary size for tokenizer*
- `generate_batch` (line 240) `def generate_batch(self, batch_size, operation)` - *Generate batch of arithmetic problems.

Returns:
    inputs: (batch, seq_len) - "a + b ="
    targets: (batch, seq_len) - "c"*
- `_encode_number` (line 292) `def _encode_number(self, n)` - *Encode number as sequence of digit tokens.*
- `__init__` (line 324) `def __init__(self, vocab_size, d_model, n_heads, n_layers, d_ff, max_seq_len, dropout)`
- `_init_weights` (line 356) `def _init_weights(self)` - *Xavier initialization.*
- `forward` (line 362) `def forward(self, x)` - *Args:
    x: (batch, seq_len) input tokens

Returns:
    logits: (batch, seq_len, vocab_size)*
- `__init__` (line 399) `def __init__(self, model, task, config)`
- `prospect` (line 417) `def prospect(self, early_epochs, save_checkpoints, checkpoint_dir)` - *Prospect for algorithmic learning using κ-mining.

Key idea: Only train models that κ predicts will succeed.

Args:
    early_epochs: Epochs to train before κ prediction
    save_checkpoints: Save model checkpoints
    checkpoint_dir: Directory for checkpoints

Returns:
    Dictionary with prospecting results and predictions*
- `__init__` (line 571) `def __init__(self, model_class, task, config)`
- `prospect_seeds` (line 579) `def prospect_seeds(self, n_candidates, early_epochs)` - *Prospect multiple random seeds to find crystals.

Returns list of seeds that κ predicts will succeed.*
- `loss_fn` (line 449) `def loss_fn(outputs, targets)`
- `data_generator` (line 455) `def data_generator(batch_size)`

#### `laderman_batch_prospection.py`
**Path:** `laderman_batch_prospection.py`

**Classes:**
- `ProspectionConfig` (line 46) `class ProspectionConfig` - *Configuración para la prospección de batch size.*
- `MatrixMultiplicationDataset` (line 89) `class MatrixMultiplicationDataset(Dataset)` - *Dataset para multiplicación de matrices.*
- `BilinearModel` (line 112) `class BilinearModel` - *Modelo bilineal simplificado para prospección rápida.*

**Functions:**
- `compute_kappa` (line 139) `def compute_kappa(model, batch, num_samples)` - *Computa κ (número de condición de la covarianza de gradientes).*
- `compute_local_complexity` (line 178) `def compute_local_complexity(model)` - *Computa la complejidad local (rango efectivo de U).*
- `compute_effective_temperature` (line 190) `def compute_effective_temperature(model, batch, num_samples)` - *Computa la temperatura efectiva T_eff.*
- `compute_entropy` (line 216) `def compute_entropy(model, batch, num_samples)` - *Computa la entropía h_bar de los gradientes.*
- `train_prospection_run` (line 250) `def train_prospection_run(config, batch_size)` - *Ejecuta un entrenamiento corto con un batch size específico
y devuelve las métricas termodinámicas.*
- `analyze_results` (line 409) `def analyze_results(results, config)` - *Analiza los resultados de la prospección y recomienda el batch size óptimo.*
- `run_prospection` (line 536) `def run_prospection(config)` - *Ejecuta la prospección completa de batch size.*
- `__post_init__` (line 81) `def __post_init__(self)`
- `__init__` (line 92) `def __init__(self, matrix_size, num_samples, seed)`
- `__len__` (line 105) `def __len__(self)`
- `__getitem__` (line 108) `def __getitem__(self, idx)`
- `__init__` (line 115) `def __init__(self, matrix_size, initial_slots)`
- `forward` (line 124) `def forward(self, input_a, input_b)`
- `compute_discretization_margin` (line 129) `def compute_discretization_margin(self)`
- `tqdm` (line 37) `def tqdm(iterable)`

#### `laderman_crystallization.py`
**Path:** `laderman_crystallization.py`

**Classes:**
- `LadermanConfig` (line 42) `class LadermanConfig` - *Complete configuration for Laderman crystallization experiment.
All parameters are centralized here to avoid magic numbers throughout the codebase.

Architecture parameters control the Transformer model structure.
Training parameters control the optimization process.
Thermodynamic parameters control phase detection and grokking.
Expansion parameters control zero-shot transfer verification.*
- `ThermodynamicState` (line 144) `class ThermodynamicState` - *Complete thermodynamic state tracking for phase classification.

This class captures all metrics required for thermodynamic analysis
of the training dynamics, following the methodology established in
the Strassen grokking research.*
- `MetricComputerInterface` (line 207) `class MetricComputerInterface(ABC)` - *Abstract base class for metric computation following SOLID principles.*
- `GradientCovarianceComputer` (line 215) `class GradientCovarianceComputer(MetricComputerInterface)` - *Compute kappa: condition number of gradient covariance matrix.

The gradient covariance condition number serves as an order parameter
for phase classification. Values near 1.0 indicate crystalline states,
while large values indicate glassy states.

Memory-efficient implementation using SVD decomposition.*
- `LocalComplexityComputer` (line 291) `class LocalComplexityComputer(MetricComputerInterface)` - *Compute Local Complexity (LC) as a phase transition marker.

LC measures the effective local dimensionality of the model.
It falls from initial high values to near-zero exactly at
the grokking transition, capturing the phase change.*
- `SuperpositionComputer` (line 322) `class SuperpositionComputer(MetricComputerInterface)` - *Compute superposition coefficient psi and effective feature count.

The superposition coefficient measures feature entanglement in the
weight space. Crystalline states show lower psi values, indicating
reduced feature entanglement compared to glassy states.*
- `TemperatureComputer` (line 356) `class TemperatureComputer(MetricComputerInterface)` - *Compute effective temperature T_eff from gradient fluctuations.

The effective temperature is derived from the fluctuation-dissipation
relation. Crystalline states exhibit T_eff < 1e-16, while glassy
states show higher values, allowing phase classification.*
- `HBarEffComputer` (line 432) `class HBarEffComputer(MetricComputerInterface)` - *Compute effective Planck constant h_bar_eff.

The effective Planck constant governs the minimum gradient temperature
required for algorithm crystallization. It characterizes the quantum-like
behavior of the optimization landscape.*
- `MatrixMultiplicationDataset` (line 469) `class MatrixMultiplicationDataset(Dataset)` - *Dataset for matrix multiplication task.*
- `BilinearTransformerModel` (line 493) `class BilinearTransformerModel` - *Transformer model for bilinear matrix multiplication.

This model combines a Transformer encoder with bilinear tensors (U, V, W)
to implement the Laderman algorithm structure for 3x3 matrix multiplication.*
- `MagnitudePruning` (line 609) `class MagnitudePruning` - *Prune slots based on L2 magnitude importance.*
- `FileCheckpointManager` (line 658) `class FileCheckpointManager` - *Checkpoint management with configurable time-based intervals.*
- `PhaseClassifier` (line 728) `class PhaseClassifier` - *Classify thermodynamic phase based on order parameters.

Phase classification follows the criteria established in the Strassen
grokking research, using delta, kappa, LC, and T_eff as order parameters.

Phases:
- crystal: Discrete algorithmic structure with perfect discretization
- polycrystal: Intermediate state from pruning, stable but not fully discrete
- warm_glass: High accuracy but not discretizable, high temperature
- glass: Non-discretizable state with high delta and entropy
- unknown: Transitional or unclassifiable state*
- `GrokkingDetector` (line 778) `class GrokkingDetector` - *Detect grokking events with stability verification.

Grokking is detected when test accuracy jumps from low values to near-perfect
while training loss remains low. The implementation requires sustained accuracy
over multiple epochs to avoid false positives from transient fluctuations.*
- `CrystallizationTrainer` (line 821) `class CrystallizationTrainer` - *Two-phase training protocol for algorithmic crystallization.

Phase 1: Extended training with thermodynamic monitoring until grokking
         occurs or crystallization is confirmed.
Phase 2: Pruning to target rank followed by discretization verification.*

**Functions:**
- `run_laderman_experiment` (line 1215) `def run_laderman_experiment(config)` - *Run complete Laderman crystallization experiment.

Returns:
    Tuple of (success, trajectory) where success indicates whether
    discretization was achieved and trajectory contains all thermodynamic states.*
- `__post_init__` (line 114) `def __post_init__(self)`
- `_validate_parameters` (line 119) `def _validate_parameters(self)`
- `_ensure_directories` (line 133) `def _ensure_directories(self)`
- `to_dict` (line 136) `def to_dict(self)`
- `to_dict` (line 178) `def to_dict(self)`
- `compute` (line 211) `def compute(self, model, batch)`
- `__init__` (line 226) `def __init__(self, num_samples)`
- `compute` (line 229) `def compute(self, model, batch)`
- `_collect_gradients` (line 244) `def _collect_gradients(self, model, input_a, input_b, target)`
- `_forward_model` (line 261) `def _forward_model(self, model, input_a, input_b)`
- `_extract_bilinear_gradients` (line 268) `def _extract_bilinear_gradients(self, model)`
- `_compute_condition_number` (line 276) `def _compute_condition_number(self, gradients)`
- `__init__` (line 300) `def __init__(self, singular_value_threshold_ratio)`
- `compute` (line 303) `def compute(self, model, batch)`
- `_compute_effective_rank` (line 313) `def _compute_effective_rank(self, tensor)`
- `compute` (line 331) `def compute(self, model, batch)`
- `_compute_superposition_coefficient` (line 341) `def _compute_superposition_coefficient(self, u)`
- `_compute_effective_feature_count` (line 347) `def _compute_effective_feature_count(self, u)`
- `__init__` (line 365) `def __init__(self, num_samples)`
- `compute` (line 368) `def compute(self, model, batch)`
- `_collect_gradient_norms` (line 389) `def _collect_gradient_norms(self, model, input_a, input_b, target)`
- `_forward_model` (line 406) `def _forward_model(self, model, input_a, input_b)`
- `_compute_bilinear_grad_norm` (line 413) `def _compute_bilinear_grad_norm(self, model)`
- `_compute_entropy` (line 420) `def _compute_entropy(self, values)`
- `_compute_heat_capacity` (line 426) `def _compute_heat_capacity(self, values, t_eff)`
- `compute` (line 441) `def compute(self, model, batch, effective_temperature, kappa)`
- `_compute_weight_variance` (line 456) `def _compute_weight_variance(self, u, v, w)`
- `_estimate_crystal_h_bar` (line 460) `def _estimate_crystal_h_bar(self, weight_variance, kappa)`
- `_estimate_glass_h_bar` (line 465) `def _estimate_glass_h_bar(self, t_eff, weight_variance)`
- `__init__` (line 472) `def __init__(self, matrix_size, num_samples, seed)`
- `__len__` (line 486) `def __len__(self)`
- `__getitem__` (line 489) `def __getitem__(self, idx)`
- `__init__` (line 501) `def __init__(self, config)`
- `_init_weights` (line 537) `def _init_weights(self)`
- `forward` (line 546) `def forward(self, input_a, input_b, output_attentions, return_dict)`
- `get_bilinear_tensors` (line 574) `def get_bilinear_tensors(self)`
- `set_bilinear_tensors` (line 577) `def set_bilinear_tensors(self, u, v, w)`
- `compute_discretization_margin` (line 588) `def compute_discretization_margin(self)`
- `discretize` (line 593) `def discretize(self, threshold)`
- `get_weight_norm` (line 601) `def get_weight_norm(self)`
- `compute_gradient_norm` (line 604) `def compute_gradient_norm(self)`
- `prune` (line 612) `def prune(self, model, target_slots)`
- `_compute_importance` (line 640) `def _compute_importance(self, u, v, w)`
- `_select_top_k` (line 646) `def _select_top_k(self, importance, k)`
- `_verify_pruning` (line 650) `def _verify_pruning(self, model, target_slots)`
- `__init__` (line 661) `def __init__(self, config)`
- `should_checkpoint` (line 670) `def should_checkpoint(self)`
- `save` (line 674) `def save(self, model, optimizer, state, path, checkpoint_type)`
- `_cleanup` (line 719) `def _cleanup(self)`
- `__init__` (line 743) `def __init__(self, config)`
- `classify` (line 746) `def classify(self, delta, kappa, lc, t_eff, test_accuracy)`
- `__init__` (line 787) `def __init__(self, config)`
- `update` (line 794) `def update(self, test_accuracy, train_loss)`
- `__init__` (line 830) `def __init__(self, config, model, train_loader, test_loader, checkpoint_manager)`
- `_initialize_metric_computers` (line 853) `def _initialize_metric_computers(self)`
- `train_epoch` (line 866) `def train_epoch(self)`
- `evaluate` (line 915) `def evaluate(self)`
- `_get_model_output` (line 941) `def _get_model_output(self, input_a, input_b)`
- `compute_thermodynamic_state` (line 947) `def compute_thermodynamic_state(self, train_metrics, test_metrics)`
- `_get_sample_batch` (line 1010) `def _get_sample_batch(self)`
- `_compute_all_metrics` (line 1017) `def _compute_all_metrics(self, sample_batch)`
- `detect_confirmed_crystallization` (line 1034) `def detect_confirmed_crystallization(self)`
- `train` (line 1065) `def train(self, num_epochs)`
- `_print_training_header` (line 1111) `def _print_training_header(self, num_epochs)`
- `_update_phase_tracking` (line 1128) `def _update_phase_tracking(self, state, last_phase, consecutive_crystal_epochs)`
- `_update_progress_bar` (line 1140) `def _update_progress_bar(self, pbar, state, consecutive_crystal_epochs)`
- `_handle_grokking_event` (line 1163) `def _handle_grokking_event(self, epoch, state)`
- `_handle_crystallization_event` (line 1176) `def _handle_crystallization_event(self, epoch, state)`
- `phase2_pruning_and_discretization` (line 1188) `def phase2_pruning_and_discretization(self)`
- `tqdm` (line 37) `def tqdm(iterable)`

#### `llm_kappa_miner.py`
**Path:** `llm_kappa_miner.py`

**Classes:**
- `LLMKappaConfig` (line 42) `class LLMKappaConfig` - *Configuration for LLM κ-mining.*
- `LLMArithmeticDataset` (line 80) `class LLMArithmeticDataset` - *Arithmetic dataset formatted for LLM training.

Format: "What is 23 + 45? Answer: 68"

This tests whether the LLM learns the algorithm or just pattern matches.*
- `LLMKappaMeter` (line 146) `class LLMKappaMeter` - *Measures κ for LLMs (handles memory constraints).

Key insight from Strassen paper: κ = λ_max/λ_min of gradient covariance
perfectly predicts grokking (AUC = 1.0).*
- `LLMKappaMiner` (line 288) `class LLMKappaMiner` - *Apply κ-mining to real LLMs.

The key insight: κ = 1 predicts algorithmic learning with AUC=1.0
This lets us predict whether an LLM will learn arithmetic in ~200 epochs
instead of training for thousands.*

**Functions:**
- `prospect_multiple_models` (line 554) `def prospect_multiple_models(models, config_override)` - *Prospect multiple LLMs for algorithmic learning.

This answers: Which LLMs can learn algorithms?*
- `main` (line 603) `def main()`
- `__post_init__` (line 71) `def __post_init__(self)`
- `__init__` (line 89) `def __init__(self, tokenizer, config)`
- `format_problem` (line 94) `def format_problem(self, a, b, op, result)` - *Format arithmetic problem as text.*
- `generate_batch` (line 103) `def generate_batch(self, batch_size)` - *Generate batch of tokenized arithmetic problems.*
- `generate_for_kappa` (line 133) `def generate_for_kappa(self, batch_size)` - *Generate batch for κ measurement.*
- `__init__` (line 154) `def __init__(self, model, config)`
- `compute_kappa` (line 158) `def compute_kappa(self, input_ids, labels, attention_mask)` - *Compute κ for the LLM.

Returns:
    Dictionary with κ and diagnostics*
- `predict_grokking` (line 259) `def predict_grokking(self, kappa)` - *Predict grokking based on κ (AUC=1.0 from Strassen paper).*
- `__init__` (line 297) `def __init__(self, config)`
- `train_step` (line 323) `def train_step(self, optimizer)` - *Single training step.*
- `evaluate` (line 346) `def evaluate(self)` - *Evaluate model and compute κ.*
- `prospect` (line 376) `def prospect(self, early_stop, save_dir)` - *Prospect for algorithmic learning using κ.

Key innovation: Stop early if κ >> 1 (will not grokk)
Continue only if κ ≈ 1 (will grokk with 99% confidence)*
- `test_arithmetic` (line 485) `def test_arithmetic(self, n_tests)` - *Test if the model can do arithmetic.*

#### `seed_miner.py`
**Path:** `seed_miner.py`

**Classes:**
- `ExecutionMode` (line 63) `class ExecutionMode(Enum)`
- `ProspectorConfig` (line 69) `class ProspectorConfig` - *Immutable unified configuration for transformer seed prospecting.*
- `IMetricCalculator` (line 160) `class IMetricCalculator(ABC)`
- `ILossComponent` (line 166) `class ILossComponent(ABC)`
- `ICheckpointManager` (line 173) `class ICheckpointManager(ABC)`
- `ITrainingPhase` (line 187) `class ITrainingPhase(ABC)`
- `DeltaCalculator` (line 239) `class DeltaCalculator(IMetricCalculator)`
- `KappaCalculator` (line 257) `class KappaCalculator`
- `ThermodynamicMetricsCalculator` (line 328) `class ThermodynamicMetricsCalculator(IMetricCalculator)`
- `LocalComplexityCalculator` (line 378) `class LocalComplexityCalculator(IMetricCalculator)`
- `SuperpositionCalculator` (line 430) `class SuperpositionCalculator(IMetricCalculator)`
- `GravitationalConstantCalculator` (line 471) `class GravitationalConstantCalculator(IMetricCalculator)`
- `PhaseDetector` (line 483) `class PhaseDetector`
- `AdaptiveAnnealingScheduler` (line 518) `class AdaptiveAnnealingScheduler`
- `GlassDetector` (line 590) `class GlassDetector`
- `GrokkinDetector` (line 635) `class GrokkinDetector`
- `CheckpointManager` (line 671) `class CheckpointManager(ICheckpointManager)`
- `ComprehensiveMetricsAggregator` (line 705) `class ComprehensiveMetricsAggregator`
- `ProspectorPhase` (line 822) `class ProspectorPhase(ITrainingPhase)`
- `LongTrainingPhase` (line 975) `class LongTrainingPhase(ITrainingPhase)`
- `SeedProspector` (line 1162) `class SeedProspector`
- `LongTrainingPipeline` (line 1304) `class LongTrainingPipeline`

**Functions:**
- `build_leiderman_config` (line 193) `def build_leiderman_config(config)`
- `format_kappa` (line 808) `def format_kappa(kappa)`
- `format_lc` (line 814) `def format_lc(lc)`
- `main` (line 1415) `def main()`
- `calculate` (line 162) `def calculate(self)`
- `compute` (line 168) `def compute(self, model, loss_ce, epoch)`
- `save` (line 175) `def save(self, state, path)`
- `load` (line 179) `def load(self, path)`
- `should_checkpoint` (line 183) `def should_checkpoint(self)`
- `execute` (line 189) `def execute(self, model)`
- `calculate` (line 240) `def calculate(self, model)`
- `__init__` (line 258) `def __init__(self, config)`
- `accumulate_gradient` (line 265) `def accumulate_gradient(self, model)`
- `calculate_kappa` (line 276) `def calculate_kappa(self)`
- `get_gradient_covariance` (line 296) `def get_gradient_covariance(self)`
- `get_kappa_trend` (line 307) `def get_kappa_trend(self)`
- `is_crystallizing` (line 317) `def is_crystallizing(self)`
- `reset` (line 323) `def reset(self)`
- `__init__` (line 329) `def __init__(self, config)`
- `calculate` (line 332) `def calculate(self, model, gradient_covariance)`
- `__init__` (line 379) `def __init__(self, config)`
- `calculate` (line 382) `def calculate(self, model, train_x, train_y, device)`
- `__init__` (line 431) `def __init__(self, config)`
- `_initialize_sae` (line 436) `def _initialize_sae(self, input_dim, device)`
- `calculate` (line 442) `def calculate(self, model)`
- `calculate` (line 472) `def calculate(self, model)`
- `__init__` (line 484) `def __init__(self, config)`
- `detect` (line 489) `def detect(self, metrics)`
- `__init__` (line 519) `def __init__(self, model, config, optimizer)`
- `step` (line 534) `def step(self, metrics)`
- `_update_model_temperatures` (line 581) `def _update_model_temperatures(self)`
- `_update_optimizer_weight_decay` (line 585) `def _update_optimizer_weight_decay(self)`
- `__init__` (line 591) `def __init__(self, config)`
- `should_stop` (line 597) `def should_stop(self, epoch, metrics)`
- `__init__` (line 636) `def __init__(self, config)`
- `update` (line 643) `def update(self, metrics)`
- `__init__` (line 672) `def __init__(self, config)`
- `save` (line 678) `def save(self, state, path)`
- `load` (line 689) `def load(self, path)`
- `should_checkpoint` (line 696) `def should_checkpoint(self)`
- `get_latest_path` (line 700) `def get_latest_path(self)`
- `__init__` (line 706) `def __init__(self, config)`
- `compute_all` (line 716) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- `accumulate_gradient` (line 800) `def accumulate_gradient(self, model)`
- `reset` (line 803) `def reset(self)`
- `__init__` (line 823) `def __init__(self, config, seed)`
- `execute` (line 827) `def execute(self, model)`
- `__init__` (line 976) `def __init__(self, config)`
- `execute` (line 980) `def execute(self, model)`
- `__init__` (line 1163) `def __init__(self, config)`
- `prospect` (line 1170) `def prospect(self, total_attempts, start_seed)`
- `_set_seed` (line 1296) `def _set_seed(self, seed)`
- `__init__` (line 1305) `def __init__(self, config)`
- `_signal_handler` (line 1313) `def _signal_handler(self, signum, frame)`
- `run` (line 1317) `def run(self, resume_from, seed)`

#### `superconducting_transformer.py`
**Path:** `superconducting_transformer.py`

**Classes:**
- `ExecutionMode` (line 72) `class ExecutionMode(Enum)`
- `SuperconductorConfig` (line 78) `class SuperconductorConfig`
- `IMetricCalculator` (line 197) `class IMetricCalculator(ABC)`
- `ILossComponent` (line 203) `class ILossComponent(ABC)`
- `ICheckpointManager` (line 210) `class ICheckpointManager(ABC)`
- `ITrainingPhase` (line 224) `class ITrainingPhase(ABC)`
- `IPhaseDetector` (line 230) `class IPhaseDetector(ABC)`
- `IGlassDetector` (line 236) `class IGlassDetector(ABC)`
- `IGrokkinDetector` (line 242) `class IGrokkinDetector(ABC)`
- `IAttentionMechanism` (line 248) `class IAttentionMechanism(ABC)`
- `SeedManager` (line 254) `class SeedManager`
- `SparsemaxFunction` (line 266) `class SparsemaxFunction`
- `Sparsemax` (line 312) `class Sparsemax`
- `TopologicalGate` (line 321) `class TopologicalGate`
- `ChemicalPotentialScheduler` (line 369) `class ChemicalPotentialScheduler`
- `SuperconductingAttention` (line 392) `class SuperconductingAttention`
- `SuperconductingTransformerLayer` (line 480) `class SuperconductingTransformerLayer`
- `SuperconductingTransformer` (line 516) `class SuperconductingTransformer`
- `ModularAdditionDatasetFactory` (line 682) `class ModularAdditionDatasetFactory`
- `DeltaCalculator` (line 711) `class DeltaCalculator(IMetricCalculator)`
- `KappaCalculator` (line 732) `class KappaCalculator`
- `ThermodynamicMetricsCalculator` (line 801) `class ThermodynamicMetricsCalculator(IMetricCalculator)`
- `LocalComplexityCalculator` (line 854) `class LocalComplexityCalculator(IMetricCalculator)`
- `SuperpositionCalculator` (line 909) `class SuperpositionCalculator(IMetricCalculator)`
- `GravitationalConstantCalculator` (line 948) `class GravitationalConstantCalculator(IMetricCalculator)`
- `SuperconductivityLoss` (line 963) `class SuperconductivityLoss(ILossComponent)`
- `PhaseDetector` (line 1018) `class PhaseDetector(IPhaseDetector)`
- `AdaptiveAnnealingScheduler` (line 1060) `class AdaptiveAnnealingScheduler`
- `GlassDetector` (line 1128) `class GlassDetector(IGlassDetector)`
- `GrokkinDetector` (line 1163) `class GrokkinDetector(IGrokkinDetector)`
- `CheckpointManager` (line 1195) `class CheckpointManager(ICheckpointManager)`
- `ModelPruner` (line 1227) `class ModelPruner`
- `ModelDiscretizer` (line 1252) `class ModelDiscretizer`
- `ComprehensiveMetricsAggregator` (line 1273) `class ComprehensiveMetricsAggregator`
- `DisplayFormatter` (line 1386) `class DisplayFormatter`
- `TrainingPrimitives` (line 1402) `class TrainingPrimitives`
- `ProspectorPhase` (line 1429) `class ProspectorPhase(ITrainingPhase)`
- `LongTrainingPhase` (line 1619) `class LongTrainingPhase(ITrainingPhase)`
- `SeedProspector` (line 1874) `class SeedProspector`
- `LongTrainingPipeline` (line 2004) `class LongTrainingPipeline`
- `Application` (line 2136) `class Application`

**Functions:**
- `main` (line 2236) `def main()`
- `calculate` (line 199) `def calculate(self)`
- `compute` (line 205) `def compute(self, model, loss_ce, epoch)`
- `save` (line 212) `def save(self, state, path)`
- `load` (line 216) `def load(self, path)`
- `should_checkpoint` (line 220) `def should_checkpoint(self)`
- `execute` (line 226) `def execute(self, model)`
- `detect` (line 232) `def detect(self, metrics)`
- `should_stop` (line 238) `def should_stop(self, epoch, metrics)`
- `update` (line 244) `def update(self, metrics)`
- `forward` (line 250) `def forward(self, scores)`
- `set_seed` (line 256) `def set_seed(seed, device)`
- `forward` (line 268) `def forward(ctx, input_tensor, dim)`
- `backward` (line 298) `def backward(ctx, grad_output)`
- `__init__` (line 313) `def __init__(self, dim)`
- `forward` (line 317) `def forward(self, input_tensor)`
- `__init__` (line 322) `def __init__(self, num_units, config)`
- `forward` (line 331) `def forward(self)`
- `get_expected_l0` (line 344) `def get_expected_l0(self)`
- `get_sparsity_ratio` (line 349) `def get_sparsity_ratio(self)`
- `get_topological_charge` (line 354) `def get_topological_charge(self)`
- `update_temperature` (line 360) `def update_temperature(self, epoch)`
- `__init__` (line 370) `def __init__(self, config)`
- `update` (line 374) `def update(self, test_accuracy)`
- `get_mu` (line 388) `def get_mu(self)`
- `__init__` (line 393) `def __init__(self, config)`
- `forward` (line 420) `def forward(self, x, mask)`
- `_update_thermodynamic_state` (line 454) `def _update_thermodynamic_state(self, attn_weights)`
- `__init__` (line 481) `def __init__(self, config, layer_index)`
- `forward` (line 497) `def forward(self, x, mask)`
- `__init__` (line 517) `def __init__(self, config)`
- `_init_weights` (line 535) `def _init_weights(self)`
- `forward` (line 545) `def forward(self, x, mask)`
- `get_thermodynamic_state` (line 556) `def get_thermodynamic_state(self)`
- `get_gate_statistics` (line 580) `def get_gate_statistics(self)`
- `get_cooper_pair_coherence` (line 604) `def get_cooper_pair_coherence(self)`
- `get_gap_energy` (line 652) `def get_gap_energy(self)`
- `get_meissner_fraction` (line 667) `def get_meissner_fraction(self)`
- `update_gate_temperatures` (line 676) `def update_gate_temperatures(self, epoch)`
- `create` (line 684) `def create(modulus, train_fraction)`
- `__init__` (line 712) `def __init__(self, config)`
- `calculate` (line 715) `def calculate(self, model)`
- `__init__` (line 733) `def __init__(self, config)`
- `accumulate_gradient` (line 738) `def accumulate_gradient(self, model)`
- `calculate_kappa` (line 749) `def calculate_kappa(self)`
- `get_gradient_covariance` (line 769) `def get_gradient_covariance(self)`
- `get_kappa_trend` (line 780) `def get_kappa_trend(self)`
- `is_crystallizing` (line 790) `def is_crystallizing(self)`
- `reset` (line 796) `def reset(self)`
- `__init__` (line 802) `def __init__(self, config)`
- `calculate` (line 805) `def calculate(self, model, gradient_covariance)`
- `__init__` (line 855) `def __init__(self, config)`
- `calculate` (line 858) `def calculate(self, model, train_x, train_y, device)`
- `__init__` (line 910) `def __init__(self, config)`
- `_initialize_sae` (line 915) `def _initialize_sae(self, input_dim, device)`
- `calculate` (line 921) `def calculate(self, model)`
- `__init__` (line 949) `def __init__(self, config)`
- `calculate` (line 952) `def calculate(self, model)`
- `__init__` (line 964) `def __init__(self, config, mu_scheduler)`
- `compute` (line 968) `def compute(self, model, loss_ce, epoch)`
- `__init__` (line 1019) `def __init__(self, config)`
- `detect` (line 1024) `def detect(self, metrics)`
- `__init__` (line 1061) `def __init__(self, model, config, optimizer)`
- `step` (line 1076) `def step(self, metrics)`
- `_update_model_temperatures` (line 1119) `def _update_model_temperatures(self)`
- `_update_optimizer_weight_decay` (line 1123) `def _update_optimizer_weight_decay(self)`
- `__init__` (line 1129) `def __init__(self, config)`
- `should_stop` (line 1133) `def should_stop(self, epoch, metrics)`
- `__init__` (line 1164) `def __init__(self, config)`
- `update` (line 1171) `def update(self, metrics)`
- `__init__` (line 1196) `def __init__(self, config)`
- `save` (line 1202) `def save(self, state, path)`
- `load` (line 1211) `def load(self, path)`
- `should_checkpoint` (line 1218) `def should_checkpoint(self)`
- `get_latest_path` (line 1222) `def get_latest_path(self)`
- `prune` (line 1229) `def prune(model, threshold)`
- `discretize` (line 1254) `def discretize(model, tolerance)`
- `__init__` (line 1274) `def __init__(self, config)`
- `compute_all` (line 1284) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, mu_scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- `accumulate_gradient` (line 1378) `def accumulate_gradient(self, model)`
- `reset` (line 1381) `def reset(self)`
- `format_kappa` (line 1388) `def format_kappa(kappa, max_display)`
- `format_lc` (line 1394) `def format_lc(lc)`
- `evaluate` (line 1405) `def evaluate(model, test_x, test_y, config, device)`
- `__init__` (line 1430) `def __init__(self, config, seed)`
- `execute` (line 1434) `def execute(self, model)`
- `delta_calc_fast` (line 1614) `def delta_calc_fast(self, model)`
- `__init__` (line 1620) `def __init__(self, config)`
- `execute` (line 1624) `def execute(self, model)`
- `__init__` (line 1875) `def __init__(self, config)`
- `prospect` (line 1882) `def prospect(self, total_attempts, start_seed)`
- `__init__` (line 2005) `def __init__(self, config)`
- `_signal_handler` (line 2013) `def _signal_handler(self, signum, frame)`
- `run` (line 2017) `def run(self, resume_from, seed)`
- `__init__` (line 2137) `def __init__(self)`
- `_create_argument_parser` (line 2140) `def _create_argument_parser(self)`
- `run` (line 2180) `def run(self)`

#### `superconducting_transformer2.py`
**Path:** `superconducting_transformer2.py`

**Classes:**
- `ExecutionMode` (line 72) `class ExecutionMode(Enum)`
- `SuperconductorConfig` (line 78) `class SuperconductorConfig`
- `IMetricCalculator` (line 197) `class IMetricCalculator(ABC)`
- `ILossComponent` (line 203) `class ILossComponent(ABC)`
- `ICheckpointManager` (line 210) `class ICheckpointManager(ABC)`
- `ITrainingPhase` (line 224) `class ITrainingPhase(ABC)`
- `IPhaseDetector` (line 230) `class IPhaseDetector(ABC)`
- `IGlassDetector` (line 236) `class IGlassDetector(ABC)`
- `IGrokkinDetector` (line 242) `class IGrokkinDetector(ABC)`
- `IAttentionMechanism` (line 248) `class IAttentionMechanism(ABC)`
- `SeedManager` (line 254) `class SeedManager`
- `SparsemaxFunction` (line 266) `class SparsemaxFunction`
- `Sparsemax` (line 312) `class Sparsemax`
- `TopologicalGate` (line 321) `class TopologicalGate`
- `ChemicalPotentialScheduler` (line 369) `class ChemicalPotentialScheduler`
- `SuperconductingAttention` (line 396) `class SuperconductingAttention`
- `SuperconductingTransformerLayer` (line 484) `class SuperconductingTransformerLayer`
- `SuperconductingTransformer` (line 520) `class SuperconductingTransformer`
- `ModularAdditionDatasetFactory` (line 686) `class ModularAdditionDatasetFactory`
- `DeltaCalculator` (line 715) `class DeltaCalculator(IMetricCalculator)`
- `KappaCalculator` (line 736) `class KappaCalculator`
- `ThermodynamicMetricsCalculator` (line 805) `class ThermodynamicMetricsCalculator(IMetricCalculator)`
- `LocalComplexityCalculator` (line 858) `class LocalComplexityCalculator(IMetricCalculator)`
- `SuperpositionCalculator` (line 913) `class SuperpositionCalculator(IMetricCalculator)`
- `GravitationalConstantCalculator` (line 952) `class GravitationalConstantCalculator(IMetricCalculator)`
- `SuperconductivityLoss` (line 967) `class SuperconductivityLoss(ILossComponent)`
- `PhaseDetector` (line 1047) `class PhaseDetector(IPhaseDetector)`
- `AdaptiveAnnealingScheduler` (line 1089) `class AdaptiveAnnealingScheduler`
- `GlassDetector` (line 1157) `class GlassDetector(IGlassDetector)`
- `GrokkinDetector` (line 1192) `class GrokkinDetector(IGrokkinDetector)`
- `CheckpointManager` (line 1224) `class CheckpointManager(ICheckpointManager)`
- `ModelPruner` (line 1256) `class ModelPruner`
- `ModelDiscretizer` (line 1281) `class ModelDiscretizer`
- `ComprehensiveMetricsAggregator` (line 1302) `class ComprehensiveMetricsAggregator`
- `DisplayFormatter` (line 1415) `class DisplayFormatter`
- `TrainingPrimitives` (line 1431) `class TrainingPrimitives`
- `ProspectorPhase` (line 1458) `class ProspectorPhase(ITrainingPhase)`
- `LongTrainingPhase` (line 1634) `class LongTrainingPhase(ITrainingPhase)`
- `SeedProspector` (line 1889) `class SeedProspector`
- `LongTrainingPipeline` (line 2019) `class LongTrainingPipeline`
- `Application` (line 2151) `class Application`

**Functions:**
- `main` (line 2251) `def main()`
- `calculate` (line 199) `def calculate(self)`
- `compute` (line 205) `def compute(self, model, loss_ce, epoch)`
- `save` (line 212) `def save(self, state, path)`
- `load` (line 216) `def load(self, path)`
- `should_checkpoint` (line 220) `def should_checkpoint(self)`
- `execute` (line 226) `def execute(self, model)`
- `detect` (line 232) `def detect(self, metrics)`
- `should_stop` (line 238) `def should_stop(self, epoch, metrics)`
- `update` (line 244) `def update(self, metrics)`
- `forward` (line 250) `def forward(self, scores)`
- `set_seed` (line 256) `def set_seed(seed, device)`
- `forward` (line 268) `def forward(ctx, input_tensor, dim)`
- `backward` (line 298) `def backward(ctx, grad_output)`
- `__init__` (line 313) `def __init__(self, dim)`
- `forward` (line 317) `def forward(self, input_tensor)`
- `__init__` (line 322) `def __init__(self, num_units, config)`
- `forward` (line 331) `def forward(self)`
- `get_expected_l0` (line 344) `def get_expected_l0(self)`
- `get_sparsity_ratio` (line 349) `def get_sparsity_ratio(self)`
- `get_topological_charge` (line 354) `def get_topological_charge(self)`
- `update_temperature` (line 360) `def update_temperature(self, epoch)`
- `__init__` (line 370) `def __init__(self, config)`
- `update` (line 374) `def update(self, test_accuracy)`
- `get_mu` (line 392) `def get_mu(self)`
- `__init__` (line 397) `def __init__(self, config)`
- `forward` (line 424) `def forward(self, x, mask)`
- `_update_thermodynamic_state` (line 458) `def _update_thermodynamic_state(self, attn_weights)`
- `__init__` (line 485) `def __init__(self, config, layer_index)`
- `forward` (line 501) `def forward(self, x, mask)`
- `__init__` (line 521) `def __init__(self, config)`
- `_init_weights` (line 539) `def _init_weights(self)`
- `forward` (line 549) `def forward(self, x, mask)`
- `get_thermodynamic_state` (line 560) `def get_thermodynamic_state(self)`
- `get_gate_statistics` (line 584) `def get_gate_statistics(self)`
- `get_cooper_pair_coherence` (line 608) `def get_cooper_pair_coherence(self)`
- `get_gap_energy` (line 656) `def get_gap_energy(self)`
- `get_meissner_fraction` (line 671) `def get_meissner_fraction(self)`
- `update_gate_temperatures` (line 680) `def update_gate_temperatures(self, epoch)`
- `create` (line 688) `def create(modulus, train_fraction)`
- `__init__` (line 716) `def __init__(self, config)`
- `calculate` (line 719) `def calculate(self, model)`
- `__init__` (line 737) `def __init__(self, config)`
- `accumulate_gradient` (line 742) `def accumulate_gradient(self, model)`
- `calculate_kappa` (line 753) `def calculate_kappa(self)`
- `get_gradient_covariance` (line 773) `def get_gradient_covariance(self)`
- `get_kappa_trend` (line 784) `def get_kappa_trend(self)`
- `is_crystallizing` (line 794) `def is_crystallizing(self)`
- `reset` (line 800) `def reset(self)`
- `__init__` (line 806) `def __init__(self, config)`
- `calculate` (line 809) `def calculate(self, model, gradient_covariance)`
- `__init__` (line 859) `def __init__(self, config)`
- `calculate` (line 862) `def calculate(self, model, train_x, train_y, device)`
- `__init__` (line 914) `def __init__(self, config)`
- `_initialize_sae` (line 919) `def _initialize_sae(self, input_dim, device)`
- `calculate` (line 925) `def calculate(self, model)`
- `__init__` (line 953) `def __init__(self, config)`
- `calculate` (line 956) `def calculate(self, model)`
- `__init__` (line 968) `def __init__(self, config, mu_scheduler)`
- `compute` (line 972) `def compute(self, model, loss_ce, epoch)`
- `__init__` (line 1048) `def __init__(self, config)`
- `detect` (line 1053) `def detect(self, metrics)`
- `__init__` (line 1090) `def __init__(self, model, config, optimizer)`
- `step` (line 1105) `def step(self, metrics)`
- `_update_model_temperatures` (line 1148) `def _update_model_temperatures(self)`
- `_update_optimizer_weight_decay` (line 1152) `def _update_optimizer_weight_decay(self)`
- `__init__` (line 1158) `def __init__(self, config)`
- `should_stop` (line 1162) `def should_stop(self, epoch, metrics)`
- `__init__` (line 1193) `def __init__(self, config)`
- `update` (line 1200) `def update(self, metrics)`
- `__init__` (line 1225) `def __init__(self, config)`
- `save` (line 1231) `def save(self, state, path)`
- `load` (line 1240) `def load(self, path)`
- `should_checkpoint` (line 1247) `def should_checkpoint(self)`
- `get_latest_path` (line 1251) `def get_latest_path(self)`
- `prune` (line 1258) `def prune(model, threshold)`
- `discretize` (line 1283) `def discretize(model, tolerance)`
- `__init__` (line 1303) `def __init__(self, config)`
- `compute_all` (line 1313) `def compute_all(self, model, train_loss, test_loss, test_acc, epoch, weight_norm, grad_norm, thermo_state, scheduler, mu_scheduler, train_x, train_y, device, force_kappa, force_lc, force_sp)`
- `accumulate_gradient` (line 1407) `def accumulate_gradient(self, model)`
- `reset` (line 1410) `def reset(self)`
- `format_kappa` (line 1417) `def format_kappa(kappa, max_display)`
- `format_lc` (line 1423) `def format_lc(lc)`
- `evaluate` (line 1434) `def evaluate(model, test_x, test_y, config, device)`
- `__init__` (line 1459) `def __init__(self, config, seed)`
- `execute` (line 1463) `def execute(self, model)`
- `__init__` (line 1635) `def __init__(self, config)`
- `execute` (line 1639) `def execute(self, model)`
- `__init__` (line 1890) `def __init__(self, config)`
- `prospect` (line 1897) `def prospect(self, total_attempts, start_seed)`
- `__init__` (line 2020) `def __init__(self, config)`
- `_signal_handler` (line 2028) `def _signal_handler(self, signum, frame)`
- `run` (line 2032) `def run(self, resume_from, seed)`
- `__init__` (line 2152) `def __init__(self)`
- `_create_argument_parser` (line 2155) `def _create_argument_parser(self)`
- `run` (line 2195) `def run(self)`

#### `tran2.py`
**Path:** `tran2.py`

**Classes:**
- `LadermanConfig` (line 44) `class LadermanConfig` - *Complete configuration for Laderman crystallization experiment.*
- `ThermodynamicState` (line 122) `class ThermodynamicState` - *Complete thermodynamic state tracking.*
- `MatrixMultiplicationDataset` (line 169) `class MatrixMultiplicationDataset(Dataset)` - *Dataset for matrix multiplication.*
- `BilinearTransformerModel` (line 197) `class BilinearTransformerModel` - *Transformer model for bilinear matrix multiplication.
Uses PyTorch's native TransformerEncoder with multi-head attention.*
- `GradientCovarianceComputer` (line 332) `class GradientCovarianceComputer` - *Compute kappa: condition number of gradient covariance matrix.
FIXED: Reduced memory usage by sampling fewer gradients and using approximation.*
- `LocalComplexityComputer` (line 400) `class LocalComplexityComputer` - *Compute Local Complexity (LC).*
- `SuperpositionComputer` (line 420) `class SuperpositionComputer` - *Compute superposition coefficient psi.*
- `TemperatureComputer` (line 441) `class TemperatureComputer` - *Compute effective temperature T_eff.*
- `MagnitudePruning` (line 494) `class MagnitudePruning` - *Prune slots based on L2 norm.
FIXED: Properly handles tensor resizing.*
- `FileCheckpointManager` (line 547) `class FileCheckpointManager` - *Checkpoint management with 5-minute intervals.*
- `CrystallizationTrainer` (line 615) `class CrystallizationTrainer` - *Two-phase training protocol from Strassen paper.*

**Functions:**
- `run_laderman_experiment` (line 916) `def run_laderman_experiment(config)` - *Run complete Laderman crystallization experiment.*
- `__post_init__` (line 103) `def __post_init__(self)`
- `to_dict` (line 111) `def to_dict(self)`
- `to_dict` (line 148) `def to_dict(self)`
- `__init__` (line 172) `def __init__(self, matrix_size, num_samples, seed)`
- `__len__` (line 186) `def __len__(self)`
- `__getitem__` (line 189) `def __getitem__(self, idx)`
- `__init__` (line 203) `def __init__(self, config)`
- `_init_weights` (line 248) `def _init_weights(self)` - *BERT-style initialization.*
- `forward` (line 258) `def forward(self, input_a, input_b, output_attentions, return_dict)`
- `get_bilinear_tensors` (line 292) `def get_bilinear_tensors(self)`
- `set_bilinear_tensors` (line 295) `def set_bilinear_tensors(self, u, v, w)` - *Set bilinear tensors with proper size handling.*
- `compute_discretization_margin` (line 308) `def compute_discretization_margin(self)`
- `discretize` (line 313) `def discretize(self, threshold)`
- `get_weight_norm` (line 321) `def get_weight_norm(self)`
- `compute_gradient_norm` (line 324) `def compute_gradient_norm(self)`
- `__init__` (line 338) `def __init__(self, num_samples)`
- `compute` (line 341) `def compute(self, model, batch)`
- `compute` (line 403) `def compute(self, model, batch)`
- `compute` (line 423) `def compute(self, model, batch)`
- `__init__` (line 444) `def __init__(self, num_samples)`
- `compute` (line 447) `def compute(self, model, batch)`
- `prune` (line 500) `def prune(self, model, target_slots)`
- `__init__` (line 550) `def __init__(self, config)`
- `should_checkpoint` (line 558) `def should_checkpoint(self)`
- `save` (line 561) `def save(self, model, optimizer, state, path, checkpoint_type)`
- `_cleanup` (line 602) `def _cleanup(self)` - *Remove old regular checkpoints but keep all grokking checkpoints.*
- `__init__` (line 618) `def __init__(self, config, model, train_loader, test_loader, checkpoint_manager)`
- `train_epoch` (line 646) `def train_epoch(self)` - *Train for one epoch with all metrics.*
- `evaluate` (line 694) `def evaluate(self)` - *Evaluate on test set.*
- `compute_thermodynamic_state` (line 726) `def compute_thermodynamic_state(self, train_metrics, test_metrics)` - *Compute complete thermodynamic state with ALL metrics.*
- `_detect_grokking` (line 788) `def _detect_grokking(self, current_test_accuracy)` - *Detect grokking: sudden jump in test accuracy.
Returns True if grokking is detected at current epoch.*
- `train` (line 809) `def train(self, num_epochs)` - *Phase 1: Extended training with thermodynamic monitoring.*
- `phase2_pruning_and_discretization` (line 879) `def phase2_pruning_and_discretization(self)` - *Phase 2: Prune to target rank and discretize.*
- `tqdm` (line 35) `def tqdm(iterable)`

#### `tran5.py`
**Path:** `tran5.py`

**Classes:**
- `LeidermanConfig` (line 19) `class LeidermanConfig` - *Configuration for Leibler-Leiderman architecture*
- `LeiblerAttention` (line 70) `class LeiblerAttention` - *Thermodynamic attention mechanism implementing Leibler's cerebral principles*
- `LeiblerTransformerLayer` (line 167) `class LeiblerTransformerLayer` - *Transformer layer with Leibler attention and thermodynamic principles*
- `LeiblerTransformer` (line 205) `class LeiblerTransformer` - *Complete Leibler Transformer implementing thermodynamic grokking*
- `AdaptiveTemperatureScheduler` (line 292) `class AdaptiveTemperatureScheduler` - *Adaptive temperature scheduler implementing thermodynamic cooling*
- `ThermodynamicTracker` (line 407) `class ThermodynamicTracker` - *Track thermodynamic properties and phase transitions during training*
- `AdaptiveTemperatureScheduler` (line 540) `class AdaptiveTemperatureScheduler` - *Thermodynamic thermostat implementing phase-dependent annealing.

Controls both temperature (attention softmax divisor) and pressure 
(weight_decay) according to the current thermodynamic phase.

Gas phase: High WD forces weights through the Leiderman slot
Liquid phase: Moderate WD allows structure formation
Glass phase: Low WD permits approach to integer lattice
Crystal approach: Minimal WD avoids disrupting fragile crystalline order*

**Functions:**
- `create_modular_addition_dataset` (line 633) `def create_modular_addition_dataset(modulus, train_fraction)` - *Create dataset for modular addition task

Args:
    modulus: Modulus for addition (vocabulary size - 1)
    train_fraction: Fraction of data for training
    
Returns:
    train_x, train_y, test_x, test_y*
- `compute_kappa_from_gradient_covariance` (line 678) `def compute_kappa_from_gradient_covariance(model, train_x, train_y, config, device)` - *Compute κ = cond(Σ) where Σ is the gradient covariance matrix.

Samples gradients from multiple mini-batches to estimate Σ.
Crystal state: κ → 1 (gradient noise is isotropic)
Glass state: κ → ∞ (gradient noise is highly anisotropic)

This is the core thermodynamic measurement from the paper.*
- `compute_order_parameters` (line 756) `def compute_order_parameters(model)` - *Compute thermodynamic order parameters per paper definitions.

κ = cond(Σ) where Σ = gradient covariance matrix
    Crystal: κ → 1.0 (isotropic gradient noise)
    Glass: κ → ∞ (anisotropic gradient noise)

δ = ||θ - Q(θ)||∞ where Q rounds to nearest integer
    Crystal: δ → 0 (weights on integer lattice)
    Glass: δ → 0.5 (weights between integers)

Returns:
    kappa, delta*
- `train_epoch` (line 824) `def train_epoch(model, train_x, train_y, optimizer, config, device)` - *Train for one epoch*
- `evaluate` (line 868) `def evaluate(model, test_x, test_y, config, device)` - *Evaluate model*
- `prune_model` (line 905) `def prune_model(model, threshold)` - *Prune slots with low weight magnitudes

Args:
    model: Model to prune
    threshold: Magnitude threshold for pruning
    
Returns:
    Number of slots remaining after pruning*
- `discretize_model` (line 955) `def discretize_model(model, tolerance)` - *Attempt to discretize model weights to integers

Args:
    model: Model to discretize
    tolerance: Maximum distance from integer
    
Returns:
    True if discretization successful*
- `main` (line 998) `def main()`
- `__init__` (line 75) `def __init__(self, config)`
- `forward` (line 97) `def forward(self, x, mask)` - *Forward pass with thermodynamic attention

Args:
    x: Input tensor [batch, seq_len, d_model]
    mask: Optional attention mask
    
Returns:
    Output tensor [batch, seq_len, d_model]*
- `_update_thermodynamic_state` (line 140) `def _update_thermodynamic_state(self)` - *Update thermodynamic state variables with stable computation*
- `__init__` (line 172) `def __init__(self, config)`
- `forward` (line 192) `def forward(self, x, mask)` - *Forward pass with residual connections*
- `__init__` (line 210) `def __init__(self, config)`
- `_init_weights` (line 234) `def _init_weights(self)` - *Initialize weights with small values for stability*
- `forward` (line 244) `def forward(self, x, mask)` - *Forward pass

Args:
    x: Input token indices [batch, seq_len]
    mask: Optional attention mask
    
Returns:
    Logits [batch, seq_len, vocab_size]*
- `get_thermodynamic_state` (line 268) `def get_thermodynamic_state(self)` - *Extract current thermodynamic state from all layers*
- `__init__` (line 297) `def __init__(self, model, config)`
- `step` (line 312) `def step(self, metrics)` - *Update temperature based on training metrics with enhanced stability*
- `_update_model_temperatures` (line 401) `def _update_model_temperatures(self)` - *Apply current temperature to all attention layers*
- `__init__` (line 412) `def __init__(self, config)`
- `update` (line 439) `def update(self, metrics)` - *Update tracker with new metrics*
- `_detect_phase` (line 455) `def _detect_phase(self, metrics)` - *Detect current thermodynamic phase based on paper-defined order parameters.

Phase classification from paper measurements:
- crystal: κ < κ_threshold AND δ < δ_threshold AND T_eff < T_eff_ceiling
- glass: κ < κ_threshold AND δ > δ_threshold (cold glass, ordered but not discrete)
- liquid: moderate κ, decreasing δ (structure forming)
- gas: high κ, high δ (disordered, high entropy)*
- `_detect_grokking` (line 489) `def _detect_grokking(self, metrics)` - *Detect grokking transitions with stability requirement*
- `get_summary` (line 529) `def get_summary(self)` - *Get summary statistics*
- `__init__` (line 553) `def __init__(self, model, config, optimizer)`
- `step` (line 566) `def step(self, metrics)` - *Update temperature and weight_decay based on thermodynamic phase*
- `_update_model_temperatures` (line 622) `def _update_model_temperatures(self)` - *Apply current temperature to all attention layers*
- `_update_optimizer_weight_decay` (line 627) `def _update_optimizer_weight_decay(self)` - *Apply current weight_decay (pressure) to optimizer*

### SH (1 files)

#### `install.sh`
**Path:** `install.sh`

*No symbols extracted*
