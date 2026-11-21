# NER: Serengeti vocabulary (FVT) vs plain LoRA

Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. Metric: entity F1 (%). See src/variants_report.py for what the variant changes.

## In-language

| lang | LoRA | variant | difference | 95% CI (paired) | tokens/word |
|---|---|---|---|---|---|
| amh | 73.6 | 55.1 | -18.5 | [-21.7, -15.6] | 2.10 -> 1.38 |
| hau | 83.1 | 80.5 | -2.6 | [-3.3, -1.9] | 1.55 -> 1.14 |
| kin | 84.6 | 80.6 | -4.0 | [-4.9, -3.2] | 2.34 -> 1.50 |
| lug | 84.1 | 81.0 | -3.1 | [-4.2, -2.0] | 2.44 -> 1.62 |
| swa | 91.4 | 90.5 | -0.9 | [-1.3, -0.6] | 1.51 -> 1.08 |
| zul | 86.5 | 80.6 | -5.9 | [-7.2, -4.7] | 2.43 -> 1.68 |

Pooled over 6 languages and all seeds: -5.8 points, 95% CI [-6.5, -5.2] (paired bootstrap over test sentences).

## Zero-shot transfer (off-diagonal)

| cells | LoRA | variant | difference |
|---|---|---|---|
| all 30 cells | 57.5 | 53.0 | -4.5 |
| Bantu -> Bantu | 63.6 | 61.9 | -1.6 |
| amh/hau -> Bantu | 58.1 | 52.8 | -5.2 |

### Difference per cell (variant minus LoRA; rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | -18.5 | -10.7 | -10.1 | -14.8 | -1.8 | -5.4 |
| hau | -10.6 | -2.6 | -4.7 | -6.5 | -2.0 | +3.4 |
| kin | -11.9 | -2.8 | -4.0 | -4.7 | -1.5 | +0.8 |
| lug | -9.7 | -1.6 | -7.4 | -3.1 | -2.7 | +7.9 |
| swa | -3.9 | -3.0 | -6.1 | -8.3 | -0.9 | +7.5 |
| zul | -21.7 | +1.5 | -4.5 | -2.8 | +2.4 | -5.9 |

