# κ-Miner for LLMs

## El Descubrimiento

En el paper de Strassen se descubrió que **κ (número de condición de la covarianza del gradiente)** predice perfectamente si una red neuronal aprenderá un algoritmo:

| κ | Predicción | Confianza |
|---|------------|-----------|
| κ ≈ 1.0 | **Will Grokk** | 99% |
| κ >> 1 | **Will Not Grokk** | 95% |

**AUC = 1.000** (separación perfecta)

## La Pregunta

> **¿Funciona esto para LLMs?**

Si κ funciona como order parameter universal, entonces podríamos predecir si un LLM aprenderá aritmética, razonamiento lógico, o cualquier algoritmo, **en solo ~200 epochs en lugar de miles**.

## El Experimento

```
┌─────────────────────────────────────────────────────────┐
│                    LLM κ-MINER                          │
├─────────────────────────────────────────────────────────┤
│  1. Cargar LLM (GPT-2, Llama, etc.)                     │
│  2. Entrenar en aritmética por ~200 epochs              │
│  3. Medir κ de la covarianza del gradiente              │
│  4. PREDICCIÓN:                                         │
│     - κ ≈ 1.0 → Continuar, WILL LEARN                   │
│     - κ >> 1 → ABORTAR, WILL NOT LEARN                  │
└─────────────────────────────────────────────────────────┘
```

## Instalación

```bash
cd /home/z/my-project/llm_kappa_mining
pip install -r requirements.txt
```

## Uso

### Test rápido con GPT-2

```bash
python llm_kappa_miner.py --model gpt2 --task arithmetic
```

### Test con múltiples modelos

```bash
python llm_kappa_miner.py --multi_model
```

### Parámetros clave

| Parámetro | Default | Descripción |
|-----------|---------|-------------|
| `--model` | gpt2 | Modelo de Hugging Face |
| `--task` | arithmetic | arithmetic, addition, multiplication |
| `--early_stop_epochs` | 200 | Epochs antes de predecir |
| `--kappa_threshold` | 1.001 | Umbral κ para cristal |

## Resultados Esperados

### Si κ funciona para LLMs:

```
Epoch   100 | κ: 1.002 | 💎 crystal | Prediction: will_grokk
Epoch   150 | κ: 1.001 | 💎 crystal | Prediction: will_grokk
...
✅ κ CRYSTAL DETECTED! κ = 1.001
   This model WILL learn the algorithm with 99% confidence!

Arithmetic Test:
  ✓ 23 + 45 = 68 (predicted: 68)
  ✓ 12 * 7 = 84 (predicted: 84)
  ...
Accuracy: 90%
```

### Si κ NO funciona para LLMs:

```
Epoch   100 | κ: 1.5e+08 | 🧊 glass | Prediction: will_not_grokk
Epoch   150 | κ: 2.3e+09 | 🧊 glass | Prediction: will_not_grokk
...
⚠️ EARLY STOP: κ predicts will not grokk (κ = 2.3e+09)
   Saving compute by stopping early!
```

## Implicaciones

### Si κ predice para LLMs:

1. **Ahorro de 90% en compute**: Solo entrenar modelos que κ=1
2. **Seed mining**: Encontrar configuraciones exitosas sin entrenar
3. **Architecture search**: Usar κ como proxy para arquitecturas
4. **Transfer learning**: κ indica si el transfer funcionará

### Si κ NO predice para LLMs:

1. El fenómeno es específico de la arquitectura bilineal
2. LLMs tienen dinámicas de gradiente diferentes
3. Necesitamos adaptar κ para transformers

## Arquitectura del Código

```
llm_kappa_mining/
├── llm_kappa_miner.py    # Código principal
├── kappa_miner.py        # Versión transformer minimal
├── requirements.txt      # Dependencias
├── run_experiment.sh     # Script de ejecución GPT-2
├── run_multi_model.sh    # Script multi-modelo
└── README.md             # Este archivo
```

## Teoría

κ mide la **anisotropía del ruido del gradiente**:

```
κ = λ_max / λ_min

donde λ_i son autovalores de Cov(∇L)
```

- **κ ≈ 1**: Gradientes isotrópicos → trayectoria suave → algoritmo aprendido
- **κ >> 1**: Gradientes anisotrópicos → trayectoria caótica → glass

## Referencias

- Paper original: "Engineering Algorithmic Structures in Neural Networks"
- GitHub: https://github.com/grisuno/strass_strassen
- Descubrimiento clave: AUC = 1.000 para κ como predictor de grokking

---

**Autor**: Basado en el descubrimiento de κ como order parameter universal
**Fecha**: 2025
