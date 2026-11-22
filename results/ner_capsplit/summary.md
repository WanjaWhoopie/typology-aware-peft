# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 86.7 ± 0.2 | [85.7, 87.7] | 0.56 | 5.3 | 639 | 10.3 | 2235 | 3 |
| lug | 87.5 ± 1.3 | [85.5, 89.3] | 0.56 | 4.8 | 302 | 7.3 | 1412 | 3 |
| swa | 92.5 ± 0.0 | [91.7, 93.2] | 0.56 | 5.2 | 665 | 14.0 | 1883 | 3 |
| zul | 88.6 ± 0.3 | [87.1, 90.0] | 0.56 | 4.8 | 441 | 9.7 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 86.7 | 80.4 | 76.6 | 48.9 |
| lug | 67.0 | 87.5 | 77.2 | 34.8 |
| swa | 66.3 | 82.9 | 92.5 | 43.5 |
| zul | 50.0 | 56.2 | 60.3 | 88.6 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.92 | 0.83 | 0.55 | 0.77 |
| lug | 0.77 | 1.00 | 0.83 | 0.39 | 0.67 |
| swa | 0.76 | 0.95 | 1.00 | 0.49 | 0.73 |
| zul | 0.58 | 0.64 | 0.65 | 1.00 | 0.62 |
| mean as target | 0.71 | 0.84 | 0.77 | 0.48 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 66% |
| share of variance explained by the source (row means) | 11% |
| Bantu -> Bantu, mean entity F1 % | 62.0 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

