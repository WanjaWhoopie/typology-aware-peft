# POS baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: full

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 93.7 ± 0.5 | [92.7, 94.6] | 100.00 | 11.2 | 145 | 6.7 | 216 | 3 |
| hau | 93.1 ± 0.2 | [92.7, 93.6] | 100.00 | 11.3 | 162 | 6.3 | 601 | 3 |
| kin | 98.4 ± 0.0 | [98.1, 98.6] | 100.00 | 11.3 | 165 | 5.0 | 604 | 3 |
| lug | 92.3 ± 0.3 | [91.7, 92.8] | 100.00 | 11.3 | 145 | 5.7 | 586 | 3 |
| swa | 93.0 ± 0.1 | [92.6, 93.5] | 100.00 | 11.2 | 149 | 5.0 | 553 | 3 |
| zul | 89.9 ± 0.1 | [89.2, 90.5] | 100.00 | 11.3 | 161 | 9.0 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 93.7 | 45.1 | 51.1 | 53.4 | 48.2 | 49.2 |
| hau | 40.6 | 93.1 | 59.0 | 44.4 | 50.9 | 43.9 |
| kin | 47.2 | 59.7 | 98.4 | 68.8 | 61.8 | 71.7 |
| lug | 46.8 | 57.1 | 69.7 | 92.3 | 64.2 | 68.4 |
| swa | 39.6 | 50.4 | 74.9 | 61.4 | 93.0 | 65.1 |
| zul | 43.1 | 55.2 | 71.6 | 56.9 | 59.2 | 89.9 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.48 | 0.52 | 0.58 | 0.52 | 0.55 | 0.53 |
| hau | 0.43 | 1.00 | 0.60 | 0.48 | 0.55 | 0.49 | 0.51 |
| kin | 0.50 | 0.64 | 1.00 | 0.75 | 0.66 | 0.80 | 0.67 |
| lug | 0.50 | 0.61 | 0.71 | 1.00 | 0.69 | 0.76 | 0.65 |
| swa | 0.42 | 0.54 | 0.76 | 0.67 | 1.00 | 0.72 | 0.62 |
| zul | 0.46 | 0.59 | 0.73 | 0.62 | 0.64 | 1.00 | 0.61 |
| mean as target | 0.46 | 0.57 | 0.66 | 0.62 | 0.61 | 0.66 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 44% |
| share of variance explained by the source (row means) | 30% |
| Bantu -> Bantu, mean accuracy % | 66.1 |
| amh/hau -> Bantu, mean accuracy % | 50.0 |

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 91.9 ± 0.4 | [90.8, 93.0] | 0.14 | 3.4 | 41 | 7.3 | 216 | 3 |
| hau | 92.0 ± 0.2 | [91.5, 92.5] | 0.14 | 4.6 | 46 | 7.3 | 601 | 3 |
| kin | 98.1 ± 0.2 | [97.8, 98.3] | 0.14 | 4.8 | 48 | 7.3 | 604 | 3 |
| lug | 91.7 ± 0.1 | [91.2, 92.2] | 0.14 | 4.3 | 42 | 7.7 | 586 | 3 |
| swa | 92.5 ± 0.1 | [92.0, 93.0] | 0.14 | 4.5 | 42 | 9.3 | 553 | 3 |
| zul | 89.1 ± 0.2 | [88.4, 89.8] | 0.14 | 4.6 | 45 | 8.0 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 91.9 | 40.9 | 47.2 | 49.3 | 46.2 | 42.1 |
| hau | 42.3 | 92.0 | 56.1 | 43.3 | 51.1 | 42.4 |
| kin | 48.7 | 59.8 | 98.1 | 68.5 | 61.7 | 70.2 |
| lug | 49.7 | 58.9 | 69.8 | 91.7 | 62.9 | 66.4 |
| swa | 42.0 | 50.2 | 74.0 | 60.7 | 92.5 | 65.2 |
| zul | 41.1 | 55.8 | 69.8 | 55.8 | 57.8 | 89.1 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.44 | 0.48 | 0.54 | 0.50 | 0.47 | 0.49 |
| hau | 0.46 | 1.00 | 0.57 | 0.47 | 0.55 | 0.48 | 0.51 |
| kin | 0.53 | 0.65 | 1.00 | 0.75 | 0.67 | 0.79 | 0.68 |
| lug | 0.54 | 0.64 | 0.71 | 1.00 | 0.68 | 0.75 | 0.66 |
| swa | 0.46 | 0.55 | 0.75 | 0.66 | 1.00 | 0.73 | 0.63 |
| zul | 0.45 | 0.61 | 0.71 | 0.61 | 0.63 | 1.00 | 0.60 |
| mean as target | 0.49 | 0.58 | 0.65 | 0.61 | 0.60 | 0.64 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 30% |
| share of variance explained by the source (row means) | 42% |
| Bantu -> Bantu, mean accuracy % | 65.2 |
| amh/hau -> Bantu, mean accuracy % | 47.2 |

## lora minus full, in-language accuracy (percentage points)

| lang | difference |
|---|---|
| amh | -1.8 |
| hau | -1.1 |
| kin | -0.3 |
| lug | -0.5 |
| swa | -0.5 |
| zul | -0.7 |

Pooled over 6 languages and all seeds: -0.8 points, 95% CI [-1.0, -0.7] (paired bootstrap over test sentences).

