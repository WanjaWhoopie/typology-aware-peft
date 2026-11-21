# POS baseline summary

Model: /content/afroxlmr_serengeti_fvt. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 89.7 ± 0.6 | [88.2, 91.0] | 0.14 | 3.3 | 41 | 8.0 | 216 | 3 |
| hau | 91.0 ± 0.2 | [90.5, 91.6] | 0.14 | 4.2 | 44 | 10.0 | 601 | 3 |
| kin | 95.3 ± 0.4 | [95.0, 95.6] | 0.14 | 4.0 | 45 | 9.7 | 604 | 3 |
| lug | 87.5 ± 0.3 | [86.8, 88.1] | 0.14 | 3.7 | 41 | 8.7 | 586 | 3 |
| swa | 91.7 ± 0.0 | [91.1, 92.2] | 0.14 | 4.2 | 41 | 9.7 | 553 | 3 |
| zul | 86.4 ± 0.1 | [85.7, 87.2] | 0.14 | 4.0 | 44 | 10.0 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 89.7 | 37.3 | 32.4 | 32.1 | 40.3 | 28.1 |
| hau | 39.1 | 91.0 | 52.1 | 40.1 | 51.7 | 41.9 |
| kin | 37.6 | 57.2 | 95.3 | 64.0 | 58.5 | 67.3 |
| lug | 36.5 | 54.2 | 64.6 | 87.5 | 60.0 | 61.7 |
| swa | 35.3 | 48.8 | 67.6 | 56.1 | 91.7 | 61.7 |
| zul | 34.6 | 56.0 | 66.5 | 52.6 | 55.7 | 86.4 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.41 | 0.34 | 0.37 | 0.44 | 0.32 | 0.38 |
| hau | 0.44 | 1.00 | 0.55 | 0.46 | 0.56 | 0.49 | 0.50 |
| kin | 0.42 | 0.63 | 1.00 | 0.73 | 0.64 | 0.78 | 0.64 |
| lug | 0.41 | 0.59 | 0.68 | 1.00 | 0.65 | 0.71 | 0.61 |
| swa | 0.39 | 0.54 | 0.71 | 0.64 | 1.00 | 0.71 | 0.60 |
| zul | 0.39 | 0.61 | 0.70 | 0.60 | 0.61 | 1.00 | 0.58 |
| mean as target | 0.41 | 0.56 | 0.59 | 0.56 | 0.58 | 0.60 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 27% |
| share of variance explained by the source (row means) | 44% |
| Bantu -> Bantu, mean accuracy % | 61.4 |
| amh/hau -> Bantu, mean accuracy % | 39.8 |

