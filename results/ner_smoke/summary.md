# NER baseline summary

Model: Davlan/afro-xlmr-base. Metric: entity F1 (%). Seeds per cell: [1].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 0.6 ± 0.0 | [0.0, 1.4] | 0.11 | n/a | 14 | 1.0 | 64 | 1 |
| swa | 1.2 ± 0.0 | [0.5, 1.9] | 0.11 | n/a | 41 | 1.0 | 64 | 1 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | amh | swa |
|---|---|---|
| amh | 0.6 | 1.2 |
| swa | 0.6 | 1.2 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | swa | mean as source |
|---|---|---|---|
| amh | 1.00 | 0.98 | 0.98 |
| swa | 0.97 | 1.00 | 0.97 |
| mean as target | 0.97 | 0.98 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 100% |
| share of variance explained by the source (row means) | 100% |
| Bantu -> Bantu, mean entity F1 % | n/a |
| amh/hau -> Bantu, mean entity F1 % | 1.2 |

Collapsed runs: swa seed 1, amh seed 1

