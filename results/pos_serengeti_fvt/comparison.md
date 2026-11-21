# POS: Serengeti vocabulary (FVT) vs plain LoRA

Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. Metric: accuracy (%). See src/variants_report.py for what the variant changes.

## In-language

| lang | LoRA | variant | difference | 95% CI (paired) | tokens/word |
|---|---|---|---|---|---|
| amh | 91.9 | 89.7 | -2.2 | [-3.2, -1.4] | 2.10 -> 1.38 |
| hau | 92.0 | 91.0 | -0.9 | [-1.2, -0.7] | 1.55 -> 1.14 |
| kin | 98.1 | 95.3 | -2.7 | [-3.0, -2.5] | 2.34 -> 1.50 |
| lug | 91.7 | 87.5 | -4.2 | [-4.7, -3.8] | 2.44 -> 1.62 |
| swa | 92.5 | 91.7 | -0.9 | [-1.1, -0.6] | 1.51 -> 1.08 |
| zul | 89.1 | 86.4 | -2.7 | [-3.1, -2.3] | 2.43 -> 1.68 |

Pooled over 6 languages and all seeds: -2.3 points, 95% CI [-2.5, -2.1] (paired bootstrap over test sentences).

## Zero-shot transfer (off-diagonal)

| cells | LoRA | variant | difference |
|---|---|---|---|
| all 30 cells | 55.0 | 49.7 | -5.3 |
| Bantu -> Bantu | 65.2 | 61.4 | -3.9 |
| amh/hau -> Bantu | 47.2 | 39.8 | -7.4 |

### Difference per cell (variant minus LoRA; rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | -2.2 | -3.6 | -14.8 | -17.2 | -5.9 | -14.0 |
| hau | -3.2 | -0.9 | -4.0 | -3.2 | +0.6 | -0.4 |
| kin | -11.2 | -2.6 | -2.7 | -4.6 | -3.2 | -2.9 |
| lug | -13.1 | -4.8 | -5.1 | -4.2 | -2.9 | -4.7 |
| swa | -6.7 | -1.4 | -6.4 | -4.6 | -0.9 | -3.5 |
| zul | -6.4 | +0.1 | -3.3 | -3.2 | -2.1 | -2.7 |

