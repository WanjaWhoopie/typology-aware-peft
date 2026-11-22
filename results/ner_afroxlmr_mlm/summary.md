# NER baseline summary

Model: /content/afroxlmr_mlm. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 86.1 ± 1.3 | [84.1, 87.9] | 0.56 | 5.3 | 562 | 9.7 | 2235 | 3 |
| lug | 89.5 ± 0.3 | [88.3, 90.7] | 0.56 | 4.8 | 418 | 12.0 | 1412 | 3 |
| swa | 92.2 ± 0.1 | [91.4, 93.0] | 0.56 | 5.2 | 451 | 9.0 | 1883 | 3 |
| zul | 88.9 ± 1.1 | [87.2, 90.9] | 0.56 | 4.8 | 400 | 9.0 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 86.1 | 80.2 | 75.5 | 54.1 |
| lug | 68.9 | 89.5 | 78.5 | 41.2 |
| swa | 65.0 | 82.2 | 92.2 | 41.9 |
| zul | 56.4 | 69.0 | 68.2 | 88.9 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.90 | 0.82 | 0.61 | 0.77 |
| lug | 0.80 | 1.00 | 0.85 | 0.46 | 0.70 |
| swa | 0.75 | 0.92 | 1.00 | 0.47 | 0.71 |
| zul | 0.65 | 0.77 | 0.74 | 1.00 | 0.72 |
| mean as target | 0.74 | 0.86 | 0.80 | 0.51 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 84% |
| share of variance explained by the source (row means) | 5% |
| Bantu -> Bantu, mean entity F1 % | 65.1 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

