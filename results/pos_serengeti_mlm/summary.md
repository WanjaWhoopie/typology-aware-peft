# POS baseline summary

Model: /content/serengeti_fvt_mlm. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 97.5 ± 0.2 | [97.1, 97.8] | 0.14 | 4.0 | 67 | 13.0 | 604 | 3 |
| lug | 91.0 ± 0.1 | [90.4, 91.6] | 0.14 | 3.7 | 65 | 13.0 | 586 | 3 |
| swa | 92.3 ± 0.2 | [91.8, 92.9] | 0.14 | 4.2 | 56 | 11.7 | 553 | 3 |
| zul | 88.2 ± 0.3 | [87.4, 89.0] | 0.14 | 4.0 | 60 | 11.3 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 97.5 | 68.8 | 60.4 | 70.0 |
| lug | 70.2 | 91.0 | 63.3 | 66.0 |
| swa | 71.6 | 61.2 | 92.3 | 64.6 |
| zul | 69.3 | 56.4 | 57.8 | 88.2 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.76 | 0.65 | 0.79 | 0.73 |
| lug | 0.72 | 1.00 | 0.69 | 0.75 | 0.72 |
| swa | 0.73 | 0.67 | 1.00 | 0.73 | 0.71 |
| zul | 0.71 | 0.62 | 0.63 | 1.00 | 0.65 |
| mean as target | 0.72 | 0.68 | 0.66 | 0.76 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 62% |
| share of variance explained by the source (row means) | 20% |
| Bantu -> Bantu, mean accuracy % | 65.0 |
| amh/hau -> Bantu, mean accuracy % | n/a |

