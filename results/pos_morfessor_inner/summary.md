# POS baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 92.0 ± 0.4 | [90.7, 93.3] | 0.14 | 3.4 | 41 | 9.0 | 216 | 3 |
| hau | 90.8 ± 0.2 | [90.2, 91.4] | 0.14 | 5.5 | 58 | 9.7 | 601 | 3 |
| kin | 97.9 ± 0.0 | [97.7, 98.1] | 0.14 | 5.1 | 54 | 7.3 | 604 | 3 |
| lug | 91.2 ± 0.1 | [90.6, 91.8] | 0.14 | 4.5 | 43 | 7.3 | 586 | 3 |
| swa | 91.7 ± 0.1 | [91.2, 92.3] | 0.14 | 5.5 | 56 | 8.7 | 553 | 3 |
| zul | 88.8 ± 0.0 | [88.1, 89.6] | 0.14 | 4.9 | 47 | 9.0 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 92.0 | 39.5 | 41.5 | 44.0 | 45.4 | 37.4 |
| hau | 39.2 | 90.8 | 53.0 | 43.7 | 48.3 | 44.7 |
| kin | 43.1 | 55.6 | 97.9 | 67.3 | 60.8 | 68.8 |
| lug | 42.7 | 55.8 | 68.8 | 91.2 | 61.9 | 66.5 |
| swa | 35.1 | 48.2 | 71.0 | 62.1 | 91.7 | 65.6 |
| zul | 35.2 | 54.1 | 69.8 | 56.5 | 55.4 | 88.8 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.44 | 0.42 | 0.48 | 0.50 | 0.42 | 0.45 |
| hau | 0.43 | 1.00 | 0.54 | 0.48 | 0.53 | 0.50 | 0.50 |
| kin | 0.47 | 0.61 | 1.00 | 0.74 | 0.66 | 0.77 | 0.65 |
| lug | 0.46 | 0.61 | 0.70 | 1.00 | 0.68 | 0.75 | 0.64 |
| swa | 0.38 | 0.53 | 0.72 | 0.68 | 1.00 | 0.74 | 0.61 |
| zul | 0.38 | 0.60 | 0.71 | 0.62 | 0.60 | 1.00 | 0.58 |
| mean as target | 0.42 | 0.56 | 0.62 | 0.60 | 0.59 | 0.64 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 36% |
| share of variance explained by the source (row means) | 35% |
| Bantu -> Bantu, mean accuracy % | 64.5 |
| amh/hau -> Bantu, mean accuracy % | 44.8 |

