# POS baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: full

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 97.5 ± 0.3 | [97.0, 97.9] | 100.00 | 11.2 | 75 | 16.7 | 604 | 3 |
| lug | 89.7 ± 0.1 | [89.0, 90.3] | 100.00 | 11.2 | 80 | 21.3 | 586 | 3 |
| swa | 91.5 ± 0.1 | [90.9, 92.0] | 100.00 | 11.3 | 70 | 16.7 | 553 | 3 |
| zul | 87.6 ± 0.1 | [86.8, 88.4] | 100.00 | 11.3 | 91 | 23.7 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 97.5 | 68.8 | 61.8 | 71.8 |
| lug | 72.0 | 89.7 | 64.8 | 68.4 |
| swa | 73.4 | 60.8 | 91.5 | 65.1 |
| zul | 70.6 | 56.5 | 56.5 | 87.6 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.77 | 0.68 | 0.82 | 0.75 |
| lug | 0.74 | 1.00 | 0.71 | 0.78 | 0.74 |
| swa | 0.75 | 0.68 | 1.00 | 0.74 | 0.72 |
| zul | 0.72 | 0.63 | 0.62 | 1.00 | 0.66 |
| mean as target | 0.74 | 0.69 | 0.67 | 0.78 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 64% |
| share of variance explained by the source (row means) | 24% |
| Bantu -> Bantu, mean accuracy % | 65.9 |
| amh/hau -> Bantu, mean accuracy % | n/a |

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 97.4 ± 0.2 | [97.0, 97.7] | 0.14 | 4.6 | 39 | 29.7 | 604 | 3 |
| lug | 88.6 ± 0.3 | [87.9, 89.3] | 0.14 | 3.8 | 30 | 29.3 | 586 | 3 |
| swa | 91.0 ± 0.3 | [90.3, 91.6] | 0.14 | 4.4 | 36 | 32.7 | 553 | 3 |
| zul | 86.2 ± 0.3 | [85.4, 87.1] | 0.14 | 4.6 | 32 | 28.7 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 97.4 | 68.0 | 62.0 | 69.5 |
| lug | 69.0 | 88.6 | 63.4 | 65.3 |
| swa | 71.3 | 58.9 | 91.0 | 62.7 |
| zul | 69.1 | 55.2 | 54.9 | 86.2 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.77 | 0.68 | 0.81 | 0.75 |
| lug | 0.71 | 1.00 | 0.70 | 0.76 | 0.72 |
| swa | 0.73 | 0.66 | 1.00 | 0.73 | 0.71 |
| zul | 0.71 | 0.62 | 0.60 | 1.00 | 0.65 |
| mean as target | 0.72 | 0.69 | 0.66 | 0.76 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 55% |
| share of variance explained by the source (row means) | 25% |
| Bantu -> Bantu, mean accuracy % | 64.1 |
| amh/hau -> Bantu, mean accuracy % | n/a |

## lora minus full, in-language accuracy (percentage points)

| lang | difference |
|---|---|
| kin | -0.1 |
| lug | -1.1 |
| swa | -0.5 |
| zul | -1.4 |

Pooled over 4 languages and all seeds: -0.8 points, 95% CI [-1.0, -0.5] (bootstrap over test sentences, paired, and over seeds).

