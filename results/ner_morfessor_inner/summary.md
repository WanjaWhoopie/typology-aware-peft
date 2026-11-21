# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 64.4 ± 5.1 | [58.3, 71.2] | 0.14 | 3.9 | 50 | 5.0 | 500 | 3 |
| hau | 75.7 ± 0.7 | [74.1, 77.1] | 0.14 | 5.4 | 194 | 5.0 | 1633 | 3 |
| kin | 82.9 ± 0.3 | [81.6, 84.2] | 0.14 | 5.6 | 268 | 4.7 | 2235 | 3 |
| lug | 82.4 ± 0.0 | [80.8, 84.0] | 0.14 | 5.5 | 150 | 5.0 | 1412 | 3 |
| swa | 89.4 ± 0.1 | [88.4, 90.3] | 0.14 | 6.2 | 220 | 4.3 | 1883 | 3 |
| zul | 85.5 ± 0.3 | [83.9, 87.0] | 0.14 | 5.2 | 173 | 4.0 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 64.4 | 42.0 | 42.5 | 59.6 | 59.4 | 45.3 |
| hau | 24.1 | 75.7 | 60.0 | 74.6 | 68.6 | 44.0 |
| kin | 30.0 | 63.9 | 82.9 | 77.6 | 75.2 | 46.6 |
| lug | 28.6 | 55.9 | 62.0 | 82.4 | 78.2 | 38.8 |
| swa | 26.0 | 57.5 | 62.2 | 77.2 | 89.4 | 39.5 |
| zul | 28.8 | 50.4 | 56.2 | 63.8 | 69.8 | 85.5 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.56 | 0.51 | 0.72 | 0.66 | 0.53 | 0.60 |
| hau | 0.37 | 1.00 | 0.72 | 0.91 | 0.77 | 0.51 | 0.66 |
| kin | 0.47 | 0.84 | 1.00 | 0.94 | 0.84 | 0.55 | 0.73 |
| lug | 0.44 | 0.74 | 0.75 | 1.00 | 0.88 | 0.45 | 0.65 |
| swa | 0.40 | 0.76 | 0.75 | 0.94 | 1.00 | 0.46 | 0.66 |
| zul | 0.45 | 0.67 | 0.68 | 0.77 | 0.78 | 1.00 | 0.67 |
| mean as target | 0.43 | 0.71 | 0.68 | 0.86 | 0.79 | 0.50 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 86% |
| share of variance explained by the source (row means) | 3% |
| Bantu -> Bantu, mean entity F1 % | 62.3 |
| amh/hau -> Bantu, mean entity F1 % | 56.8 |

