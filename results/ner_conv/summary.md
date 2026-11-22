# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: full

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 86.4 ± 0.5 | [85.2, 87.6] | 100.00 | 11.3 | 1465 | 6.0 | 2235 | 3 |
| lug | 90.0 ± 0.2 | [88.7, 91.0] | 100.00 | 11.3 | 1341 | 10.7 | 1412 | 3 |
| swa | 93.1 ± 0.1 | [92.3, 93.8] | 100.00 | 11.3 | 2023 | 12.7 | 1883 | 3 |
| zul | 89.7 ± 0.5 | [88.3, 91.1] | 100.00 | 11.3 | 1069 | 6.3 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 86.4 | 81.6 | 76.9 | 48.6 |
| lug | 69.3 | 90.0 | 78.3 | 43.8 |
| swa | 66.9 | 82.1 | 93.1 | 43.0 |
| zul | 58.0 | 69.4 | 71.3 | 89.7 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.91 | 0.83 | 0.54 | 0.76 |
| lug | 0.80 | 1.00 | 0.84 | 0.49 | 0.71 |
| swa | 0.77 | 0.91 | 1.00 | 0.48 | 0.72 |
| zul | 0.67 | 0.77 | 0.77 | 1.00 | 0.74 |
| mean as target | 0.75 | 0.86 | 0.81 | 0.50 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 90% |
| share of variance explained by the source (row means) | 2% |
| Bantu -> Bantu, mean entity F1 % | 65.8 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 86.9 ± 0.2 | [85.8, 87.9] | 0.56 | 5.3 | 562 | 8.7 | 2235 | 3 |
| lug | 89.3 ± 0.5 | [87.9, 90.5] | 0.56 | 4.8 | 440 | 12.0 | 1412 | 3 |
| swa | 92.1 ± 0.4 | [91.2, 92.9] | 0.56 | 5.2 | 432 | 8.0 | 1883 | 3 |
| zul | 88.9 ± 0.2 | [87.6, 90.2] | 0.56 | 4.8 | 394 | 8.3 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 86.9 | 81.3 | 77.8 | 53.4 |
| lug | 69.1 | 89.3 | 81.2 | 39.7 |
| swa | 66.4 | 82.4 | 92.1 | 43.7 |
| zul | 56.8 | 67.9 | 68.2 | 88.9 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.91 | 0.84 | 0.60 | 0.79 |
| lug | 0.80 | 1.00 | 0.88 | 0.45 | 0.71 |
| swa | 0.76 | 0.92 | 1.00 | 0.49 | 0.73 |
| zul | 0.65 | 0.76 | 0.74 | 1.00 | 0.72 |
| mean as target | 0.74 | 0.87 | 0.82 | 0.51 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 83% |
| share of variance explained by the source (row means) | 5% |
| Bantu -> Bantu, mean entity F1 % | 65.7 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

## lora minus full, in-language entity F1 (percentage points)

| lang | difference |
|---|---|
| kin | +0.5 |
| lug | -0.7 |
| swa | -1.0 |
| zul | -0.9 |

Pooled over 4 languages and all seeds: -0.5 points, 95% CI [-1.0, -0.0] (bootstrap over test sentences, paired, and over seeds).

