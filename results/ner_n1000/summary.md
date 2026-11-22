# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: full

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 82.4 ± 0.9 | [80.9, 84.0] | 100.00 | 11.2 | 486 | 15.7 | 2235 | 3 |
| lug | 86.3 ± 1.6 | [83.9, 88.3] | 100.00 | 11.3 | 447 | 16.0 | 1412 | 3 |
| swa | 91.2 ± 0.7 | [90.1, 92.3] | 100.00 | 11.3 | 377 | 12.3 | 1883 | 3 |
| zul | 85.4 ± 0.6 | [83.7, 87.0] | 100.00 | 11.3 | 466 | 16.7 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 82.4 | 78.6 | 76.2 | 47.5 |
| lug | 64.2 | 86.3 | 78.6 | 40.4 |
| swa | 64.1 | 79.9 | 91.2 | 40.6 |
| zul | 57.3 | 68.0 | 67.6 | 85.4 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.91 | 0.84 | 0.56 | 0.77 |
| lug | 0.78 | 1.00 | 0.86 | 0.47 | 0.70 |
| swa | 0.78 | 0.93 | 1.00 | 0.48 | 0.73 |
| zul | 0.69 | 0.79 | 0.74 | 1.00 | 0.74 |
| mean as target | 0.75 | 0.87 | 0.81 | 0.50 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 90% |
| share of variance explained by the source (row means) | 3% |
| Bantu -> Bantu, mean entity F1 % | 63.6 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 80.7 ± 1.0 | [79.0, 82.4] | 0.56 | 4.6 | 189 | 17.7 | 2235 | 3 |
| lug | 83.9 ± 1.4 | [81.8, 86.1] | 0.56 | 4.6 | 163 | 18.7 | 1412 | 3 |
| swa | 90.7 ± 0.7 | [89.4, 91.9] | 0.56 | 4.6 | 140 | 13.3 | 1883 | 3 |
| zul | 85.0 ± 0.3 | [83.5, 86.5] | 0.56 | 4.5 | 207 | 22.7 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 80.7 | 77.8 | 73.7 | 48.0 |
| lug | 61.5 | 83.9 | 74.6 | 35.4 |
| swa | 63.7 | 80.3 | 90.7 | 42.2 |
| zul | 58.0 | 68.3 | 65.5 | 85.0 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.93 | 0.81 | 0.57 | 0.77 |
| lug | 0.76 | 1.00 | 0.82 | 0.42 | 0.67 |
| swa | 0.79 | 0.96 | 1.00 | 0.50 | 0.75 |
| zul | 0.72 | 0.81 | 0.72 | 1.00 | 0.75 |
| mean as target | 0.76 | 0.90 | 0.79 | 0.49 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 90% |
| share of variance explained by the source (row means) | 6% |
| Bantu -> Bantu, mean entity F1 % | 62.4 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

## lora minus full, in-language entity F1 (percentage points)

| lang | difference |
|---|---|
| kin | -1.8 |
| lug | -2.4 |
| swa | -0.5 |
| zul | -0.3 |

Pooled over 4 languages and all seeds: -1.2 points, 95% CI [-1.8, -0.7] (bootstrap over test sentences, paired, and over seeds).

