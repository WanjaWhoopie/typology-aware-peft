# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: full

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 57.4 ± 1.5 | [55.1, 59.9] | 100.00 | 11.3 | 172 | 27.7 | 2235 | 3 |
| lug | 74.2 ± 1.4 | [71.8, 76.5] | 100.00 | 11.2 | 81 | 15.7 | 1412 | 3 |
| swa | 85.5 ± 0.2 | [84.4, 86.6] | 100.00 | 11.3 | 109 | 18.3 | 1883 | 3 |
| zul | 71.9 ± 0.7 | [69.8, 73.9] | 100.00 | 11.3 | 121 | 23.0 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 57.4 | 61.1 | 65.6 | 38.1 |
| lug | 50.1 | 74.2 | 67.5 | 33.5 |
| swa | 59.6 | 70.8 | 85.5 | 39.0 |
| zul | 32.1 | 53.1 | 38.8 | 71.9 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.82 | 0.77 | 0.53 | 0.71 |
| lug | 0.87 | 1.00 | 0.79 | 0.47 | 0.71 |
| swa | 1.04 | 0.95 | 1.00 | 0.54 | 0.84 |
| zul | 0.56 | 0.72 | 0.45 | 1.00 | 0.58 |
| mean as target | 0.82 | 0.83 | 0.67 | 0.51 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 51% |
| share of variance explained by the source (row means) | 19% |
| Bantu -> Bantu, mean entity F1 % | 50.8 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 57.8 ± 2.3 | [54.9, 60.9] | 0.56 | 4.6 | 123 | 38.3 | 2235 | 3 |
| lug | 74.8 ± 1.0 | [72.6, 76.8] | 0.56 | 4.6 | 48 | 22.0 | 1412 | 3 |
| swa | 85.3 ± 0.9 | [83.9, 86.9] | 0.56 | 4.2 | 92 | 32.7 | 1883 | 3 |
| zul | 48.3 ± 32.0 | [3.1, 72.4] | 0.56 | 4.1 | 54 | 17.7 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 57.8 | 65.1 | 65.6 | 41.7 |
| lug | 49.0 | 74.8 | 65.9 | 37.0 |
| swa | 61.4 | 72.8 | 85.3 | 40.3 |
| zul | 25.3 | 35.8 | 29.7 | 48.3 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.87 | 0.77 | 0.86 | 0.83 |
| lug | 0.85 | 1.00 | 0.77 | 0.77 | 0.80 |
| swa | 1.06 | 0.97 | 1.00 | 0.83 | 0.96 |
| zul | 0.44 | 0.48 | 0.35 | 1.00 | 0.42 |
| mean as target | 0.78 | 0.77 | 0.63 | 0.82 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 21% |
| share of variance explained by the source (row means) | 52% |
| Bantu -> Bantu, mean entity F1 % | 49.1 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

Collapsed runs: zul seed 3

## lora minus full, in-language entity F1 (percentage points)

| lang | difference |
|---|---|
| kin | +0.4 |
| lug | +0.6 |
| swa | -0.2 |
| zul | -23.6 |

Pooled over 4 languages and all seeds: -5.7 points, 95% CI [-17.8, +1.3] (bootstrap over test sentences, paired, and over seeds).

