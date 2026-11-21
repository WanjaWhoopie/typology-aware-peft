# NER: Morfessor, cuts inside words vs plain LoRA

Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. Metric: entity F1 (%). See src/variants_report.py for what the variant changes.

## In-language

| lang | LoRA | variant | difference | 95% CI (sentences + seeds) | tokens/word |
|---|---|---|---|---|---|
| amh | 73.6 | 64.4 | -9.2 | [-15.1, -2.8] | 2.10 -> 2.44 |
| hau | 83.1 | 75.7 | -7.4 | [-8.8, -6.1] | 1.55 -> 2.23 |
| kin | 84.6 | 82.9 | -1.8 | [-2.6, -0.9] | 2.34 -> 2.76 |
| lug | 84.1 | 82.4 | -1.7 | [-3.3, -0.3] | 2.44 -> 2.84 |
| swa | 91.4 | 89.4 | -2.1 | [-2.7, -1.4] | 1.51 -> 2.22 |
| zul | 86.5 | 85.5 | -1.0 | [-2.0, +0.1] | 2.43 -> 2.77 |

Pooled over 6 languages and all seeds: -3.9 points, 95% CI [-4.9, -2.8] (bootstrap over test sentences, paired, and seeds).

## Zero-shot transfer (off-diagonal)

| cells | LoRA | variant | difference |
|---|---|---|---|
| all 30 cells | 57.5 | 53.6 | -3.9 |
| Bantu -> Bantu | 63.6 | 62.3 | -1.3 |
| amh/hau -> Bantu | 58.1 | 56.8 | -1.3 |

### Difference per cell (variant minus LoRA; rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | -9.2 | -12.1 | -1.8 | -2.2 | +4.4 | +2.8 |
| hau | -15.2 | -7.4 | -1.8 | -4.8 | -5.3 | -1.9 |
| kin | -9.8 | -6.4 | -1.8 | -2.2 | +0.5 | -3.7 |
| lug | -2.9 | -6.6 | -2.0 | -1.7 | +0.6 | +0.8 |
| swa | -14.5 | -7.5 | -3.1 | -4.2 | -2.1 | -3.3 |
| zul | -11.8 | -3.0 | +0.1 | -3.8 | +4.9 | -1.0 |

