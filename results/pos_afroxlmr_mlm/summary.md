# POS baseline summary

Model: /content/afroxlmr_mlm. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 98.3 ± 0.1 | [98.0, 98.5] | 0.14 | 4.8 | 45 | 7.3 | 604 | 3 |
| lug | 92.0 ± 0.2 | [91.3, 92.6] | 0.14 | 4.3 | 45 | 8.0 | 586 | 3 |
| swa | 92.8 ± 0.2 | [92.3, 93.3] | 0.14 | 4.5 | 54 | 10.7 | 553 | 3 |
| zul | 89.4 ± 0.1 | [88.7, 90.2] | 0.14 | 4.6 | 51 | 9.0 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 98.3 | 67.4 | 61.4 | 69.8 |
| lug | 69.7 | 92.0 | 63.9 | 67.2 |
| swa | 75.0 | 60.4 | 92.8 | 65.0 |
| zul | 70.6 | 56.4 | 57.4 | 89.4 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.73 | 0.66 | 0.78 | 0.73 |
| lug | 0.71 | 1.00 | 0.69 | 0.75 | 0.72 |
| swa | 0.76 | 0.66 | 1.00 | 0.73 | 0.72 |
| zul | 0.72 | 0.61 | 0.62 | 1.00 | 0.65 |
| mean as target | 0.73 | 0.67 | 0.66 | 0.75 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 68% |
| share of variance explained by the source (row means) | 17% |
| Bantu -> Bantu, mean accuracy % | 65.3 |
| amh/hau -> Bantu, mean accuracy % | n/a |

