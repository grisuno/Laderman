# Polyglot Codebase Knowledge Graph

> Generated offline by **readmenator**. Supports C, C++, Python, Go, Rust, JS/TS, Java, C#, Shell, PHP, Dart, GDScript, Nim, ASM.
> No LLMs. No tokens. Pure static analysis.

**Total Files Parsed:** 12 | **Total Symbols Extracted:** 709 | **Total Imports:** 158

## Structural Knowledge Map
```mermaid
graph TD
    classDef mod fill:#1e1e1e,stroke:#ff6666,stroke-width:2px,color:#fff;
    classDef cls fill:#2d2d2d,stroke:#4ec9b0,stroke-width:2px,color:#fff;
    classDef fn fill:#333,stroke:#dcdcaa,stroke-width:1px,color:#dcdcaa;
    classDef ext fill:#111,stroke:#666,stroke-dasharray: 5 5,color:#aaa;
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

**Classs:**
- `ExecutionMode` (line 59)
- `ProspectorConfig` (line 69)
- `IMetricCalculator` (line 197)
- `ILossComponent` (line 203)
- `ICheckpointManager` (line 210)
- `ITrainingPhase` (line 224)
- `IPhaseDetector` (line 230)
- `IGlassDetector` (line 236)
- `IGrokkinDetector` (line 242)
- `SeedManager` (line 252)
- `ComplexOperations` (line 268)
- `ComplexLinear` (line 337)
- `ComplexLayerNorm` (line 364)
- `ComplexLeiblerAttention` (line 379)
- `ComplexLeiblerTransformerLayer` (line 485)
- `ComplexLeiblerTransformer` (line 529)
- `ModularAdditionDatasetFactory` (line 653)
- `TrainingPrimitives` (line 688)
- `DeltaCalculator` (line 754)
- `KappaCalculator` (line 772)
- `ThermodynamicMetricsCalculator` (line 841)
- `LocalComplexityCalculator` (line 894)
- `SuperpositionCalculator` (line 949)
- `GravitationalConstantCalculator` (line 988)
- `ComplexPhaseMetricsCalculator` (line 1003)
- `PhaseDetector` (line 1015)
- `AdaptiveAnnealingScheduler` (line 1058)
- `GlassDetector` (line 1130)
- `GrokkinDetector` (line 1169)
- `CheckpointManager` (line 1205)
- `ModelPruner` (line 1241)
- `ModelDiscretizer` (line 1261)
- `ComplexPhaseLoss` (line 1296)
- `ComprehensiveMetricsAggregator` (line 1335)
- `DisplayFormatter` (line 1444)
- `ProspectorPhase` (line 1464)
- `LongTrainingPhase` (line 1651)
- `SeedProspector` (line 1877)
- `LongTrainingPipeline` (line 2020)
- `Application` (line 2151)

**Functions:**
- `main` (line 2238)
- `calculate` (line 199)
- `compute` (line 205)
- `save` (line 212)
- `load` (line 216)
- `should_checkpoint` (line 220)
- `execute` (line 226)
- `detect` (line 232)
- `should_stop` (line 238)
- `update` (line 244)
- `set_seed` (line 254)
- `complex_linear` (line 271)
- `complex_gelu` (line 288)
- `complex_layer_norm` (line 295)
- `compute_phase` (line 311)
- `compute_magnitude` (line 315)
- `complex_softmax` (line 319)
- `__init__` (line 338)
- `forward` (line 352)
- `__init__` (line 365)
- `forward` (line 371)
- `__init__` (line 380)
- `forward` (line 404)
- `_update_thermodynamic_state` (line 450)
- `__init__` (line 486)
- `forward` (line 498)
- `__init__` (line 530)
- `_init_weights` (line 554)
- `forward` (line 564)
- `get_thermodynamic_state` (line 584)
- `get_complex_weight_statistics` (line 610)
- `create` (line 655)
- `train_epoch` (line 690)
- `evaluate` (line 724)
- `__init__` (line 755)
- `calculate` (line 758)
- `__init__` (line 773)
- `accumulate_gradient` (line 778)
- `calculate_kappa` (line 789)
- `get_gradient_covariance` (line 809)
- `get_kappa_trend` (line 820)
- `is_crystallizing` (line 830)
- `reset` (line 836)
- `__init__` (line 842)
- `calculate` (line 845)
- `__init__` (line 895)
- `calculate` (line 898)
- `__init__` (line 950)
- `_initialize_sae` (line 955)
- `calculate` (line 961)
- `__init__` (line 989)
- `calculate` (line 992)
- `__init__` (line 1004)
- `calculate` (line 1007)
- `__init__` (line 1016)
- `detect` (line 1021)
- `__init__` (line 1059)
- `step` (line 1074)
- `_update_model_temperatures` (line 1117)
- `_update_optimizer_weight_decay` (line 1121)
- `__init__` (line 1131)
- `should_stop` (line 1135)
- `__init__` (line 1170)
- `update` (line 1177)
- `__init__` (line 1206)
- `save` (line 1212)
- `load` (line 1221)
- `should_checkpoint` (line 1228)
- `get_latest_path` (line 1232)
- `prune` (line 1243)
- `discretize` (line 1263)
- `__init__` (line 1297)
- `compute` (line 1300)
- `__init__` (line 1336)
- `compute_all` (line 1347)
- `accumulate_gradient` (line 1432)
- `reset` (line 1435)
- `format_kappa` (line 1446)
- `format_lc` (line 1452)
- `__init__` (line 1465)
- `execute` (line 1469)
- `__init__` (line 1652)
- `execute` (line 1656)
- `__init__` (line 1878)
- `prospect` (line 1885)
- `__init__` (line 2021)
- `_signal_handler` (line 2029)
- `run` (line 2033)
- `__init__` (line 2152)
- `_create_argument_parser` (line 2155)
- `run` (line 2190)

#### `kappa_miner.py`
**Path:** `kappa_miner.py`

**Classs:**
- `KappaConfig` (line 39) - *Configuration for κ-mining experiments.*
- `KappaMeter` (line 68) - *Measures κ(Σ) = λ_max/λ_min of gradient covariance matrix.

This is the core metric that predicts grokking with AUC=1.0.*
- `ArithmeticTask` (line 201) - *Arithmetic task for testing κ prediction on transformers.

Models must learn to:
- Add numbers (a + b = c)
- Multiply numbers (a * b = c)
- Combined operations

This is a canonical "algorithmic" task that requires learning
exact computation, not just pattern matching.*
- `MinimalTransformer` (line 316) - *Minimal transformer for arithmetic tasks.

Architecture designed to be small enough to train quickly
but expressive enough to learn algorithms.*
- `KappaMiner` (line 391) - *Main class for κ-mining experiments on LLMs.

Uses κ to predict algorithmic learning before training completes,
based on the AUC=1.0 result from Strassen paper.*
- `BatchProspector` (line 563) - *Prospect multiple seeds/configurations to find crystals efficiently.

Uses κ-mining to avoid wasting compute on configurations that
will not grokk.*

**Functions:**
- `__init__` (line 75)
- `compute_kappa` (line 78) - *Compute gradient covariance condition number κ.

Returns:
    Dictionary with κ, eigenvalues, and diagnostics*
- `predict_grokking` (line 168) - *Predict whether model will grokk based on κ.

Returns prediction with confidence based on Strassen paper results.*
- `__init__` (line 214) - *Args:
    max_digits: Maximum number of digits per operand
    operations: List of operations ['+', '-', '*']
    tokenizer_vocab: Vocabulary size for tokenizer*
- `generate_batch` (line 240) - *Generate batch of arithmetic problems.

Returns:
    inputs: (batch, seq_len) - "a + b ="
    targets: (batch, seq_len) - "c"*
- `_encode_number` (line 292) - *Encode number as sequence of digit tokens.*
- `__init__` (line 324)
- `_init_weights` (line 356) - *Xavier initialization.*
- `forward` (line 362) - *Args:
    x: (batch, seq_len) input tokens

Returns:
    logits: (batch, seq_len, vocab_size)*
- `__init__` (line 399)
- `prospect` (line 417) - *Prospect for algorithmic learning using κ-mining.

Key idea: Only train models that κ predicts will succeed.

Args:
    early_epochs: Epochs to train before κ prediction
    save_checkpoints: Save model checkpoints
    checkpoint_dir: Directory for checkpoints

Returns:
    Dictionary with prospecting results and predictions*
- `__init__` (line 571)
- `prospect_seeds` (line 579) - *Prospect multiple random seeds to find crystals.

Returns list of seeds that κ predicts will succeed.*
- `loss_fn` (line 449)
- `data_generator` (line 455)

#### `laderman_batch_prospection.py`
**Path:** `laderman_batch_prospection.py`

**Classs:**
- `ProspectionConfig` (line 46) - *Configuración para la prospección de batch size.*
- `MatrixMultiplicationDataset` (line 89) - *Dataset para multiplicación de matrices.*
- `BilinearModel` (line 112) - *Modelo bilineal simplificado para prospección rápida.*

**Functions:**
- `compute_kappa` (line 139) - *Computa κ (número de condición de la covarianza de gradientes).*
- `compute_local_complexity` (line 178) - *Computa la complejidad local (rango efectivo de U).*
- `compute_effective_temperature` (line 190) - *Computa la temperatura efectiva T_eff.*
- `compute_entropy` (line 216) - *Computa la entropía h_bar de los gradientes.*
- `train_prospection_run` (line 250) - *Ejecuta un entrenamiento corto con un batch size específico
y devuelve las métricas termodinámicas.*
- `analyze_results` (line 409) - *Analiza los resultados de la prospección y recomienda el batch size óptimo.*
- `run_prospection` (line 536) - *Ejecuta la prospección completa de batch size.*
- `__post_init__` (line 81)
- `__init__` (line 92)
- `__len__` (line 105)
- `__getitem__` (line 108)
- `__init__` (line 115)
- `forward` (line 124)
- `compute_discretization_margin` (line 129)
- `tqdm` (line 37)

#### `laderman_crystallization.py`
**Path:** `laderman_crystallization.py`

**Classs:**
- `LadermanConfig` (line 42) - *Complete configuration for Laderman crystallization experiment.
All parameters are centralized here to avoid magic numbers throughout the codebase.

Architecture parameters control the Transformer model structure.
Training parameters control the optimization process.
Thermodynamic parameters control phase detection and grokking.
Expansion parameters control zero-shot transfer verification.*
- `ThermodynamicState` (line 144) - *Complete thermodynamic state tracking for phase classification.

This class captures all metrics required for thermodynamic analysis
of the training dynamics, following the methodology established in
the Strassen grokking research.*
- `MetricComputerInterface` (line 207) - *Abstract base class for metric computation following SOLID principles.*
- `GradientCovarianceComputer` (line 215) - *Compute kappa: condition number of gradient covariance matrix.

The gradient covariance condition number serves as an order parameter
for phase classification. Values near 1.0 indicate crystalline states,
while large values indicate glassy states.

Memory-efficient implementation using SVD decomposition.*
- `LocalComplexityComputer` (line 291) - *Compute Local Complexity (LC) as a phase transition marker.

LC measures the effective local dimensionality of the model.
It falls from initial high values to near-zero exactly at
the grokking transition, capturing the phase change.*
- `SuperpositionComputer` (line 322) - *Compute superposition coefficient psi and effective feature count.

The superposition coefficient measures feature entanglement in the
weight space. Crystalline states show lower psi values, indicating
reduced feature entanglement compared to glassy states.*
- `TemperatureComputer` (line 356) - *Compute effective temperature T_eff from gradient fluctuations.

The effective temperature is derived from the fluctuation-dissipation
relation. Crystalline states exhibit T_eff < 1e-16, while glassy
states show higher values, allowing phase classification.*
- `HBarEffComputer` (line 432) - *Compute effective Planck constant h_bar_eff.

The effective Planck constant governs the minimum gradient temperature
required for algorithm crystallization. It characterizes the quantum-like
behavior of the optimization landscape.*
- `MatrixMultiplicationDataset` (line 469) - *Dataset for matrix multiplication task.*
- `BilinearTransformerModel` (line 493) - *Transformer model for bilinear matrix multiplication.

This model combines a Transformer encoder with bilinear tensors (U, V, W)
to implement the Laderman algorithm structure for 3x3 matrix multiplication.*
- `MagnitudePruning` (line 609) - *Prune slots based on L2 magnitude importance.*
- `FileCheckpointManager` (line 658) - *Checkpoint management with configurable time-based intervals.*
- `PhaseClassifier` (line 728) - *Classify thermodynamic phase based on order parameters.

Phase classification follows the criteria established in the Strassen
grokking research, using delta, kappa, LC, and T_eff as order parameters.

Phases:
- crystal: Discrete algorithmic structure with perfect discretization
- polycrystal: Intermediate state from pruning, stable but not fully discrete
- warm_glass: High accuracy but not discretizable, high temperature
- glass: Non-discretizable state with high delta and entropy
- unknown: Transitional or unclassifiable state*
- `GrokkingDetector` (line 778) - *Detect grokking events with stability verification.

Grokking is detected when test accuracy jumps from low values to near-perfect
while training loss remains low. The implementation requires sustained accuracy
over multiple epochs to avoid false positives from transient fluctuations.*
- `CrystallizationTrainer` (line 821) - *Two-phase training protocol for algorithmic crystallization.

Phase 1: Extended training with thermodynamic monitoring until grokking
         occurs or crystallization is confirmed.
Phase 2: Pruning to target rank followed by discretization verification.*

**Functions:**
- `run_laderman_experiment` (line 1215) - *Run complete Laderman crystallization experiment.

Returns:
    Tuple of (success, trajectory) where success indicates whether
    discretization was achieved and trajectory contains all thermodynamic states.*
- `__post_init__` (line 114)
- `_validate_parameters` (line 119)
- `_ensure_directories` (line 133)
- `to_dict` (line 136)
- `to_dict` (line 178)
- `compute` (line 211)
- `__init__` (line 226)
- `compute` (line 229)
- `_collect_gradients` (line 244)
- `_forward_model` (line 261)
- `_extract_bilinear_gradients` (line 268)
- `_compute_condition_number` (line 276)
- `__init__` (line 300)
- `compute` (line 303)
- `_compute_effective_rank` (line 313)
- `compute` (line 331)
- `_compute_superposition_coefficient` (line 341)
- `_compute_effective_feature_count` (line 347)
- `__init__` (line 365)
- `compute` (line 368)
- `_collect_gradient_norms` (line 389)
- `_forward_model` (line 406)
- `_compute_bilinear_grad_norm` (line 413)
- `_compute_entropy` (line 420)
- `_compute_heat_capacity` (line 426)
- `compute` (line 441)
- `_compute_weight_variance` (line 456)
- `_estimate_crystal_h_bar` (line 460)
- `_estimate_glass_h_bar` (line 465)
- `__init__` (line 472)
- `__len__` (line 486)
- `__getitem__` (line 489)
- `__init__` (line 501)
- `_init_weights` (line 537)
- `forward` (line 546)
- `get_bilinear_tensors` (line 574)
- `set_bilinear_tensors` (line 577)
- `compute_discretization_margin` (line 588)
- `discretize` (line 593)
- `get_weight_norm` (line 601)
- `compute_gradient_norm` (line 604)
- `prune` (line 612)
- `_compute_importance` (line 640)
- `_select_top_k` (line 646)
- `_verify_pruning` (line 650)
- `__init__` (line 661)
- `should_checkpoint` (line 670)
- `save` (line 674)
- `_cleanup` (line 719)
- `__init__` (line 743)
- `classify` (line 746)
- `__init__` (line 787)
- `update` (line 794)
- `__init__` (line 830)
- `_initialize_metric_computers` (line 853)
- `train_epoch` (line 866)
- `evaluate` (line 915)
- `_get_model_output` (line 941)
- `compute_thermodynamic_state` (line 947)
- `_get_sample_batch` (line 1010)
- `_compute_all_metrics` (line 1017)
- `detect_confirmed_crystallization` (line 1034)
- `train` (line 1065)
- `_print_training_header` (line 1111)
- `_update_phase_tracking` (line 1128)
- `_update_progress_bar` (line 1140)
- `_handle_grokking_event` (line 1163)
- `_handle_crystallization_event` (line 1176)
- `phase2_pruning_and_discretization` (line 1188)
- `tqdm` (line 37)

#### `llm_kappa_miner.py`
**Path:** `llm_kappa_miner.py`

**Classs:**
- `LLMKappaConfig` (line 42) - *Configuration for LLM κ-mining.*
- `LLMArithmeticDataset` (line 80) - *Arithmetic dataset formatted for LLM training.

Format: "What is 23 + 45? Answer: 68"

This tests whether the LLM learns the algorithm or just pattern matches.*
- `LLMKappaMeter` (line 146) - *Measures κ for LLMs (handles memory constraints).

Key insight from Strassen paper: κ = λ_max/λ_min of gradient covariance
perfectly predicts grokking (AUC = 1.0).*
- `LLMKappaMiner` (line 288) - *Apply κ-mining to real LLMs.

The key insight: κ = 1 predicts algorithmic learning with AUC=1.0
This lets us predict whether an LLM will learn arithmetic in ~200 epochs
instead of training for thousands.*

**Functions:**
- `prospect_multiple_models` (line 554) - *Prospect multiple LLMs for algorithmic learning.

This answers: Which LLMs can learn algorithms?*
- `main` (line 603)
- `__post_init__` (line 71)
- `__init__` (line 89)
- `format_problem` (line 94) - *Format arithmetic problem as text.*
- `generate_batch` (line 103) - *Generate batch of tokenized arithmetic problems.*
- `generate_for_kappa` (line 133) - *Generate batch for κ measurement.*
- `__init__` (line 154)
- `compute_kappa` (line 158) - *Compute κ for the LLM.

Returns:
    Dictionary with κ and diagnostics*
- `predict_grokking` (line 259) - *Predict grokking based on κ (AUC=1.0 from Strassen paper).*
- `__init__` (line 297)
- `train_step` (line 323) - *Single training step.*
- `evaluate` (line 346) - *Evaluate model and compute κ.*
- `prospect` (line 376) - *Prospect for algorithmic learning using κ.

Key innovation: Stop early if κ >> 1 (will not grokk)
Continue only if κ ≈ 1 (will grokk with 99% confidence)*
- `test_arithmetic` (line 485) - *Test if the model can do arithmetic.*

#### `seed_miner.py`
**Path:** `seed_miner.py`

**Classs:**
- `ExecutionMode` (line 63)
- `ProspectorConfig` (line 69) - *Immutable unified configuration for transformer seed prospecting.*
- `IMetricCalculator` (line 160)
- `ILossComponent` (line 166)
- `ICheckpointManager` (line 173)
- `ITrainingPhase` (line 187)
- `DeltaCalculator` (line 239)
- `KappaCalculator` (line 257)
- `ThermodynamicMetricsCalculator` (line 328)
- `LocalComplexityCalculator` (line 378)
- `SuperpositionCalculator` (line 430)
- `GravitationalConstantCalculator` (line 471)
- `PhaseDetector` (line 483)
- `AdaptiveAnnealingScheduler` (line 518)
- `GlassDetector` (line 590)
- `GrokkinDetector` (line 635)
- `CheckpointManager` (line 671)
- `ComprehensiveMetricsAggregator` (line 705)
- `ProspectorPhase` (line 822)
- `LongTrainingPhase` (line 975)
- `SeedProspector` (line 1162)
- `LongTrainingPipeline` (line 1304)

**Functions:**
- `build_leiderman_config` (line 193)
- `format_kappa` (line 808)
- `format_lc` (line 814)
- `main` (line 1415)
- `calculate` (line 162)
- `compute` (line 168)
- `save` (line 175)
- `load` (line 179)
- `should_checkpoint` (line 183)
- `execute` (line 189)
- `calculate` (line 240)
- `__init__` (line 258)
- `accumulate_gradient` (line 265)
- `calculate_kappa` (line 276)
- `get_gradient_covariance` (line 296)
- `get_kappa_trend` (line 307)
- `is_crystallizing` (line 317)
- `reset` (line 323)
- `__init__` (line 329)
- `calculate` (line 332)
- `__init__` (line 379)
- `calculate` (line 382)
- `__init__` (line 431)
- `_initialize_sae` (line 436)
- `calculate` (line 442)
- `calculate` (line 472)
- `__init__` (line 484)
- `detect` (line 489)
- `__init__` (line 519)
- `step` (line 534)
- `_update_model_temperatures` (line 581)
- `_update_optimizer_weight_decay` (line 585)
- `__init__` (line 591)
- `should_stop` (line 597)
- `__init__` (line 636)
- `update` (line 643)
- `__init__` (line 672)
- `save` (line 678)
- `load` (line 689)
- `should_checkpoint` (line 696)
- `get_latest_path` (line 700)
- `__init__` (line 706)
- `compute_all` (line 716)
- `accumulate_gradient` (line 800)
- `reset` (line 803)
- `__init__` (line 823)
- `execute` (line 827)
- `__init__` (line 976)
- `execute` (line 980)
- `__init__` (line 1163)
- `prospect` (line 1170)
- `_set_seed` (line 1296)
- `__init__` (line 1305)
- `_signal_handler` (line 1313)
- `run` (line 1317)

#### `superconducting_transformer.py`
**Path:** `superconducting_transformer.py`

**Classs:**
- `ExecutionMode` (line 72)
- `SuperconductorConfig` (line 78)
- `IMetricCalculator` (line 197)
- `ILossComponent` (line 203)
- `ICheckpointManager` (line 210)
- `ITrainingPhase` (line 224)
- `IPhaseDetector` (line 230)
- `IGlassDetector` (line 236)
- `IGrokkinDetector` (line 242)
- `IAttentionMechanism` (line 248)
- `SeedManager` (line 254)
- `SparsemaxFunction` (line 266)
- `Sparsemax` (line 312)
- `TopologicalGate` (line 321)
- `ChemicalPotentialScheduler` (line 369)
- `SuperconductingAttention` (line 392)
- `SuperconductingTransformerLayer` (line 480)
- `SuperconductingTransformer` (line 516)
- `ModularAdditionDatasetFactory` (line 682)
- `DeltaCalculator` (line 711)
- `KappaCalculator` (line 732)
- `ThermodynamicMetricsCalculator` (line 801)
- `LocalComplexityCalculator` (line 854)
- `SuperpositionCalculator` (line 909)
- `GravitationalConstantCalculator` (line 948)
- `SuperconductivityLoss` (line 963)
- `PhaseDetector` (line 1018)
- `AdaptiveAnnealingScheduler` (line 1060)
- `GlassDetector` (line 1128)
- `GrokkinDetector` (line 1163)
- `CheckpointManager` (line 1195)
- `ModelPruner` (line 1227)
- `ModelDiscretizer` (line 1252)
- `ComprehensiveMetricsAggregator` (line 1273)
- `DisplayFormatter` (line 1386)
- `TrainingPrimitives` (line 1402)
- `ProspectorPhase` (line 1429)
- `LongTrainingPhase` (line 1619)
- `SeedProspector` (line 1874)
- `LongTrainingPipeline` (line 2004)
- `Application` (line 2136)

**Functions:**
- `main` (line 2236)
- `calculate` (line 199)
- `compute` (line 205)
- `save` (line 212)
- `load` (line 216)
- `should_checkpoint` (line 220)
- `execute` (line 226)
- `detect` (line 232)
- `should_stop` (line 238)
- `update` (line 244)
- `forward` (line 250)
- `set_seed` (line 256)
- `forward` (line 268)
- `backward` (line 298)
- `__init__` (line 313)
- `forward` (line 317)
- `__init__` (line 322)
- `forward` (line 331)
- `get_expected_l0` (line 344)
- `get_sparsity_ratio` (line 349)
- `get_topological_charge` (line 354)
- `update_temperature` (line 360)
- `__init__` (line 370)
- `update` (line 374)
- `get_mu` (line 388)
- `__init__` (line 393)
- `forward` (line 420)
- `_update_thermodynamic_state` (line 454)
- `__init__` (line 481)
- `forward` (line 497)
- `__init__` (line 517)
- `_init_weights` (line 535)
- `forward` (line 545)
- `get_thermodynamic_state` (line 556)
- `get_gate_statistics` (line 580)
- `get_cooper_pair_coherence` (line 604)
- `get_gap_energy` (line 652)
- `get_meissner_fraction` (line 667)
- `update_gate_temperatures` (line 676)
- `create` (line 684)
- `__init__` (line 712)
- `calculate` (line 715)
- `__init__` (line 733)
- `accumulate_gradient` (line 738)
- `calculate_kappa` (line 749)
- `get_gradient_covariance` (line 769)
- `get_kappa_trend` (line 780)
- `is_crystallizing` (line 790)
- `reset` (line 796)
- `__init__` (line 802)
- `calculate` (line 805)
- `__init__` (line 855)
- `calculate` (line 858)
- `__init__` (line 910)
- `_initialize_sae` (line 915)
- `calculate` (line 921)
- `__init__` (line 949)
- `calculate` (line 952)
- `__init__` (line 964)
- `compute` (line 968)
- `__init__` (line 1019)
- `detect` (line 1024)
- `__init__` (line 1061)
- `step` (line 1076)
- `_update_model_temperatures` (line 1119)
- `_update_optimizer_weight_decay` (line 1123)
- `__init__` (line 1129)
- `should_stop` (line 1133)
- `__init__` (line 1164)
- `update` (line 1171)
- `__init__` (line 1196)
- `save` (line 1202)
- `load` (line 1211)
- `should_checkpoint` (line 1218)
- `get_latest_path` (line 1222)
- `prune` (line 1229)
- `discretize` (line 1254)
- `__init__` (line 1274)
- `compute_all` (line 1284)
- `accumulate_gradient` (line 1378)
- `reset` (line 1381)
- `format_kappa` (line 1388)
- `format_lc` (line 1394)
- `evaluate` (line 1405)
- `__init__` (line 1430)
- `execute` (line 1434)
- `delta_calc_fast` (line 1614)
- `__init__` (line 1620)
- `execute` (line 1624)
- `__init__` (line 1875)
- `prospect` (line 1882)
- `__init__` (line 2005)
- `_signal_handler` (line 2013)
- `run` (line 2017)
- `__init__` (line 2137)
- `_create_argument_parser` (line 2140)
- `run` (line 2180)

#### `superconducting_transformer2.py`
**Path:** `superconducting_transformer2.py`

**Classs:**
- `ExecutionMode` (line 72)
- `SuperconductorConfig` (line 78)
- `IMetricCalculator` (line 197)
- `ILossComponent` (line 203)
- `ICheckpointManager` (line 210)
- `ITrainingPhase` (line 224)
- `IPhaseDetector` (line 230)
- `IGlassDetector` (line 236)
- `IGrokkinDetector` (line 242)
- `IAttentionMechanism` (line 248)
- `SeedManager` (line 254)
- `SparsemaxFunction` (line 266)
- `Sparsemax` (line 312)
- `TopologicalGate` (line 321)
- `ChemicalPotentialScheduler` (line 369)
- `SuperconductingAttention` (line 396)
- `SuperconductingTransformerLayer` (line 484)
- `SuperconductingTransformer` (line 520)
- `ModularAdditionDatasetFactory` (line 686)
- `DeltaCalculator` (line 715)
- `KappaCalculator` (line 736)
- `ThermodynamicMetricsCalculator` (line 805)
- `LocalComplexityCalculator` (line 858)
- `SuperpositionCalculator` (line 913)
- `GravitationalConstantCalculator` (line 952)
- `SuperconductivityLoss` (line 967)
- `PhaseDetector` (line 1047)
- `AdaptiveAnnealingScheduler` (line 1089)
- `GlassDetector` (line 1157)
- `GrokkinDetector` (line 1192)
- `CheckpointManager` (line 1224)
- `ModelPruner` (line 1256)
- `ModelDiscretizer` (line 1281)
- `ComprehensiveMetricsAggregator` (line 1302)
- `DisplayFormatter` (line 1415)
- `TrainingPrimitives` (line 1431)
- `ProspectorPhase` (line 1458)
- `LongTrainingPhase` (line 1634)
- `SeedProspector` (line 1889)
- `LongTrainingPipeline` (line 2019)
- `Application` (line 2151)

**Functions:**
- `main` (line 2251)
- `calculate` (line 199)
- `compute` (line 205)
- `save` (line 212)
- `load` (line 216)
- `should_checkpoint` (line 220)
- `execute` (line 226)
- `detect` (line 232)
- `should_stop` (line 238)
- `update` (line 244)
- `forward` (line 250)
- `set_seed` (line 256)
- `forward` (line 268)
- `backward` (line 298)
- `__init__` (line 313)
- `forward` (line 317)
- `__init__` (line 322)
- `forward` (line 331)
- `get_expected_l0` (line 344)
- `get_sparsity_ratio` (line 349)
- `get_topological_charge` (line 354)
- `update_temperature` (line 360)
- `__init__` (line 370)
- `update` (line 374)
- `get_mu` (line 392)
- `__init__` (line 397)
- `forward` (line 424)
- `_update_thermodynamic_state` (line 458)
- `__init__` (line 485)
- `forward` (line 501)
- `__init__` (line 521)
- `_init_weights` (line 539)
- `forward` (line 549)
- `get_thermodynamic_state` (line 560)
- `get_gate_statistics` (line 584)
- `get_cooper_pair_coherence` (line 608)
- `get_gap_energy` (line 656)
- `get_meissner_fraction` (line 671)
- `update_gate_temperatures` (line 680)
- `create` (line 688)
- `__init__` (line 716)
- `calculate` (line 719)
- `__init__` (line 737)
- `accumulate_gradient` (line 742)
- `calculate_kappa` (line 753)
- `get_gradient_covariance` (line 773)
- `get_kappa_trend` (line 784)
- `is_crystallizing` (line 794)
- `reset` (line 800)
- `__init__` (line 806)
- `calculate` (line 809)
- `__init__` (line 859)
- `calculate` (line 862)
- `__init__` (line 914)
- `_initialize_sae` (line 919)
- `calculate` (line 925)
- `__init__` (line 953)
- `calculate` (line 956)
- `__init__` (line 968)
- `compute` (line 972)
- `__init__` (line 1048)
- `detect` (line 1053)
- `__init__` (line 1090)
- `step` (line 1105)
- `_update_model_temperatures` (line 1148)
- `_update_optimizer_weight_decay` (line 1152)
- `__init__` (line 1158)
- `should_stop` (line 1162)
- `__init__` (line 1193)
- `update` (line 1200)
- `__init__` (line 1225)
- `save` (line 1231)
- `load` (line 1240)
- `should_checkpoint` (line 1247)
- `get_latest_path` (line 1251)
- `prune` (line 1258)
- `discretize` (line 1283)
- `__init__` (line 1303)
- `compute_all` (line 1313)
- `accumulate_gradient` (line 1407)
- `reset` (line 1410)
- `format_kappa` (line 1417)
- `format_lc` (line 1423)
- `evaluate` (line 1434)
- `__init__` (line 1459)
- `execute` (line 1463)
- `__init__` (line 1635)
- `execute` (line 1639)
- `__init__` (line 1890)
- `prospect` (line 1897)
- `__init__` (line 2020)
- `_signal_handler` (line 2028)
- `run` (line 2032)
- `__init__` (line 2152)
- `_create_argument_parser` (line 2155)
- `run` (line 2195)

#### `tran2.py`
**Path:** `tran2.py`

**Classs:**
- `LadermanConfig` (line 44) - *Complete configuration for Laderman crystallization experiment.*
- `ThermodynamicState` (line 122) - *Complete thermodynamic state tracking.*
- `MatrixMultiplicationDataset` (line 169) - *Dataset for matrix multiplication.*
- `BilinearTransformerModel` (line 197) - *Transformer model for bilinear matrix multiplication.
Uses PyTorch's native TransformerEncoder with multi-head attention.*
- `GradientCovarianceComputer` (line 332) - *Compute kappa: condition number of gradient covariance matrix.
FIXED: Reduced memory usage by sampling fewer gradients and using approximation.*
- `LocalComplexityComputer` (line 400) - *Compute Local Complexity (LC).*
- `SuperpositionComputer` (line 420) - *Compute superposition coefficient psi.*
- `TemperatureComputer` (line 441) - *Compute effective temperature T_eff.*
- `MagnitudePruning` (line 494) - *Prune slots based on L2 norm.
FIXED: Properly handles tensor resizing.*
- `FileCheckpointManager` (line 547) - *Checkpoint management with 5-minute intervals.*
- `CrystallizationTrainer` (line 615) - *Two-phase training protocol from Strassen paper.*

**Functions:**
- `run_laderman_experiment` (line 916) - *Run complete Laderman crystallization experiment.*
- `__post_init__` (line 103)
- `to_dict` (line 111)
- `to_dict` (line 148)
- `__init__` (line 172)
- `__len__` (line 186)
- `__getitem__` (line 189)
- `__init__` (line 203)
- `_init_weights` (line 248) - *BERT-style initialization.*
- `forward` (line 258)
- `get_bilinear_tensors` (line 292)
- `set_bilinear_tensors` (line 295) - *Set bilinear tensors with proper size handling.*
- `compute_discretization_margin` (line 308)
- `discretize` (line 313)
- `get_weight_norm` (line 321)
- `compute_gradient_norm` (line 324)
- `__init__` (line 338)
- `compute` (line 341)
- `compute` (line 403)
- `compute` (line 423)
- `__init__` (line 444)
- `compute` (line 447)
- `prune` (line 500)
- `__init__` (line 550)
- `should_checkpoint` (line 558)
- `save` (line 561)
- `_cleanup` (line 602) - *Remove old regular checkpoints but keep all grokking checkpoints.*
- `__init__` (line 618)
- `train_epoch` (line 646) - *Train for one epoch with all metrics.*
- `evaluate` (line 694) - *Evaluate on test set.*
- `compute_thermodynamic_state` (line 726) - *Compute complete thermodynamic state with ALL metrics.*
- `_detect_grokking` (line 788) - *Detect grokking: sudden jump in test accuracy.
Returns True if grokking is detected at current epoch.*
- `train` (line 809) - *Phase 1: Extended training with thermodynamic monitoring.*
- `phase2_pruning_and_discretization` (line 879) - *Phase 2: Prune to target rank and discretize.*
- `tqdm` (line 35)

#### `tran5.py`
**Path:** `tran5.py`

**Classs:**
- `LeidermanConfig` (line 19) - *Configuration for Leibler-Leiderman architecture*
- `LeiblerAttention` (line 70) - *Thermodynamic attention mechanism implementing Leibler's cerebral principles*
- `LeiblerTransformerLayer` (line 167) - *Transformer layer with Leibler attention and thermodynamic principles*
- `LeiblerTransformer` (line 205) - *Complete Leibler Transformer implementing thermodynamic grokking*
- `AdaptiveTemperatureScheduler` (line 292) - *Adaptive temperature scheduler implementing thermodynamic cooling*
- `ThermodynamicTracker` (line 407) - *Track thermodynamic properties and phase transitions during training*
- `AdaptiveTemperatureScheduler` (line 540) - *Thermodynamic thermostat implementing phase-dependent annealing.

Controls both temperature (attention softmax divisor) and pressure 
(weight_decay) according to the current thermodynamic phase.

Gas phase: High WD forces weights through the Leiderman slot
Liquid phase: Moderate WD allows structure formation
Glass phase: Low WD permits approach to integer lattice
Crystal approach: Minimal WD avoids disrupting fragile crystalline order*

**Functions:**
- `create_modular_addition_dataset` (line 633) - *Create dataset for modular addition task

Args:
    modulus: Modulus for addition (vocabulary size - 1)
    train_fraction: Fraction of data for training
    
Returns:
    train_x, train_y, test_x, test_y*
- `compute_kappa_from_gradient_covariance` (line 678) - *Compute κ = cond(Σ) where Σ is the gradient covariance matrix.

Samples gradients from multiple mini-batches to estimate Σ.
Crystal state: κ → 1 (gradient noise is isotropic)
Glass state: κ → ∞ (gradient noise is highly anisotropic)

This is the core thermodynamic measurement from the paper.*
- `compute_order_parameters` (line 756) - *Compute thermodynamic order parameters per paper definitions.

κ = cond(Σ) where Σ = gradient covariance matrix
    Crystal: κ → 1.0 (isotropic gradient noise)
    Glass: κ → ∞ (anisotropic gradient noise)

δ = ||θ - Q(θ)||∞ where Q rounds to nearest integer
    Crystal: δ → 0 (weights on integer lattice)
    Glass: δ → 0.5 (weights between integers)

Returns:
    kappa, delta*
- `train_epoch` (line 824) - *Train for one epoch*
- `evaluate` (line 868) - *Evaluate model*
- `prune_model` (line 905) - *Prune slots with low weight magnitudes

Args:
    model: Model to prune
    threshold: Magnitude threshold for pruning
    
Returns:
    Number of slots remaining after pruning*
- `discretize_model` (line 955) - *Attempt to discretize model weights to integers

Args:
    model: Model to discretize
    tolerance: Maximum distance from integer
    
Returns:
    True if discretization successful*
- `main` (line 998)
- `__init__` (line 75)
- `forward` (line 97) - *Forward pass with thermodynamic attention

Args:
    x: Input tensor [batch, seq_len, d_model]
    mask: Optional attention mask
    
Returns:
    Output tensor [batch, seq_len, d_model]*
- `_update_thermodynamic_state` (line 140) - *Update thermodynamic state variables with stable computation*
- `__init__` (line 172)
- `forward` (line 192) - *Forward pass with residual connections*
- `__init__` (line 210)
- `_init_weights` (line 234) - *Initialize weights with small values for stability*
- `forward` (line 244) - *Forward pass

Args:
    x: Input token indices [batch, seq_len]
    mask: Optional attention mask
    
Returns:
    Logits [batch, seq_len, vocab_size]*
- `get_thermodynamic_state` (line 268) - *Extract current thermodynamic state from all layers*
- `__init__` (line 297)
- `step` (line 312) - *Update temperature based on training metrics with enhanced stability*
- `_update_model_temperatures` (line 401) - *Apply current temperature to all attention layers*
- `__init__` (line 412)
- `update` (line 439) - *Update tracker with new metrics*
- `_detect_phase` (line 455) - *Detect current thermodynamic phase based on paper-defined order parameters.

Phase classification from paper measurements:
- crystal: κ < κ_threshold AND δ < δ_threshold AND T_eff < T_eff_ceiling
- glass: κ < κ_threshold AND δ > δ_threshold (cold glass, ordered but not discrete)
- liquid: moderate κ, decreasing δ (structure forming)
- gas: high κ, high δ (disordered, high entropy)*
- `_detect_grokking` (line 489) - *Detect grokking transitions with stability requirement*
- `get_summary` (line 529) - *Get summary statistics*
- `__init__` (line 553)
- `step` (line 566) - *Update temperature and weight_decay based on thermodynamic phase*
- `_update_model_temperatures` (line 622) - *Apply current temperature to all attention layers*
- `_update_optimizer_weight_decay` (line 627) - *Apply current weight_decay (pressure) to optimizer*

### SH (1 files)

#### `install.sh`
**Path:** `install.sh`

*No symbols extracted*
