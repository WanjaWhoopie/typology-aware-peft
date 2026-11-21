# POS: Morfessor, cuts inside words vs plain LoRA

Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. Metric: accuracy (%). See src/variants_report.py for what the variant changes.

## In-language

| lang | LoRA | variant | difference | 95% CI (sentences + seeds) | tokens/word |
|---|---|---|---|---|---|
| amh | 91.9 | 92.0 | +0.1 | [-0.7, +1.0] | 2.10 -> 2.44 |
| hau | 92.0 | 90.8 | -1.2 | [-1.6, -0.8] | 1.55 -> 2.23 |
| kin | 98.1 | 97.9 | -0.2 | [-0.4, +0.1] | 2.34 -> 2.76 |
| lug | 91.7 | 91.2 | -0.5 | [-0.9, -0.1] | 2.44 -> 2.84 |
| swa | 92.5 | 91.7 | -0.8 | [-1.1, -0.5] | 1.51 -> 2.22 |
| zul | 89.1 | 88.8 | -0.3 | [-0.7, +0.1] | 2.43 -> 2.77 |

Pooled over 6 languages and all seeds: -0.5 points, 95% CI [-0.6, -0.3] (bootstrap over test sentences, paired, and seeds).

## Zero-shot transfer (off-diagonal)

| cells | LoRA | variant | difference |
|---|---|---|---|
| all 30 cells | 55.0 | 52.7 | -2.3 |
| Bantu -> Bantu | 65.2 | 64.5 | -0.7 |
| amh/hau -> Bantu | 47.2 | 44.8 | -2.4 |

### Difference per cell (variant minus LoRA; rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | +0.1 | -1.4 | -5.7 | -5.3 | -0.8 | -4.7 |
| hau | -3.0 | -1.2 | -3.1 | +0.4 | -2.7 | +2.4 |
| kin | -5.7 | -4.2 | -0.2 | -1.2 | -0.8 | -1.3 |
| lug | -7.0 | -3.1 | -1.0 | -0.5 | -0.9 | +0.1 |
| swa | -6.9 | -2.0 | -3.1 | +1.4 | -0.8 | +0.5 |
| zul | -5.9 | -1.8 | +0.0 | +0.7 | -2.4 | -0.3 |

