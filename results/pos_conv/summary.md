# POS baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: full

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 98.2 ± 0.0 | [97.9, 98.4] | 100.00 | 11.3 | 166 | 7.0 | 604 | 3 |
| lug | 92.2 ± 0.4 | [91.6, 92.9] | 100.00 | 11.2 | 112 | 4.7 | 586 | 3 |
| swa | 93.0 ± 0.2 | [92.5, 93.5] | 100.00 | 11.3 | 140 | 6.3 | 553 | 3 |
| zul | 89.7 ± 0.1 | [89.0, 90.4] | 100.00 | 11.3 | 179 | 8.3 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 98.2 | 69.6 | 62.4 | 71.5 |
| lug | 71.3 | 92.2 | 64.7 | 69.1 |
| swa | 75.0 | 62.3 | 93.0 | 65.7 |
| zul | 71.3 | 57.1 | 59.0 | 89.7 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.75 | 0.67 | 0.80 | 0.74 |
| lug | 0.73 | 1.00 | 0.70 | 0.77 | 0.73 |
| swa | 0.76 | 0.68 | 1.00 | 0.73 | 0.72 |
| zul | 0.73 | 0.62 | 0.63 | 1.00 | 0.66 |
| mean as target | 0.74 | 0.68 | 0.67 | 0.77 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 65% |
| share of variance explained by the source (row means) | 20% |
| Bantu -> Bantu, mean accuracy % | 66.6 |
| amh/hau -> Bantu, mean accuracy % | n/a |

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 98.3 ± 0.0 | [98.1, 98.6] | 0.14 | 4.8 | 68 | 11.0 | 604 | 3 |
| lug | 91.8 ± 0.2 | [91.2, 92.4] | 0.14 | 4.3 | 54 | 9.7 | 586 | 3 |
| swa | 92.7 ± 0.1 | [92.2, 93.2] | 0.14 | 4.5 | 50 | 8.7 | 553 | 3 |
| zul | 89.2 ± 0.2 | [88.5, 90.0] | 0.14 | 4.6 | 47 | 7.3 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 98.3 | 68.2 | 62.1 | 69.8 |
| lug | 69.8 | 91.8 | 63.3 | 67.0 |
| swa | 74.6 | 60.6 | 92.7 | 65.3 |
| zul | 70.4 | 56.1 | 57.1 | 89.2 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.74 | 0.67 | 0.78 | 0.73 |
| lug | 0.71 | 1.00 | 0.68 | 0.75 | 0.71 |
| swa | 0.76 | 0.66 | 1.00 | 0.73 | 0.72 |
| zul | 0.72 | 0.61 | 0.62 | 1.00 | 0.65 |
| mean as target | 0.73 | 0.67 | 0.66 | 0.76 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 66% |
| share of variance explained by the source (row means) | 20% |
| Bantu -> Bantu, mean accuracy % | 65.3 |
| amh/hau -> Bantu, mean accuracy % | n/a |

## lora minus full, in-language accuracy (percentage points)

| lang | difference |
|---|---|
| kin | +0.2 |
| lug | -0.4 |
| swa | -0.3 |
| zul | -0.5 |

Pooled over 4 languages and all seeds: -0.2 points, 95% CI [-0.5, -0.0] (bootstrap over test sentences, paired, and over seeds).

