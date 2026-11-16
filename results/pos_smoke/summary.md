# POS baseline summary

Model: Davlan/afro-xlmr-base. Metric: accuracy (%). Seeds per cell: [1].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 3.2 ± 0.0 | [2.0, 4.5] | 0.11 | n/a | 10 | 1.0 | 64 | 1 |
| swa | 6.8 ± 0.0 | [5.7, 8.0] | 0.11 | n/a | 27 | 1.0 | 64 | 1 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | swa |
|---|---|---|
| amh | 3.2 | 4.3 |
| swa | 2.7 | 6.8 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | swa | mean as source |
|---|---|---|---|
| amh | 1.00 | 0.64 | 0.64 |
| swa | 0.85 | 1.00 | 0.85 |
| mean as target | 0.85 | 0.64 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 100% |
| share of variance explained by the source (row means) | 100% |
| Bantu -> Bantu, mean accuracy % | n/a |
| amh/hau -> Bantu, mean accuracy % | 4.3 |

Collapsed runs: swa seed 1, amh seed 1

