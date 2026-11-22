# NER baseline summary

Model: /content/serengeti_fvt_mlm. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| kin | 84.9 ± 0.7 | [83.6, 86.3] | 0.56 | 4.9 | 503 | 8.3 | 2235 | 3 |
| lug | 88.2 ± 1.0 | [86.3, 89.9] | 0.56 | 4.3 | 341 | 9.0 | 1412 | 3 |
| swa | 91.4 ± 0.2 | [90.6, 92.2] | 0.56 | 4.4 | 374 | 7.0 | 1883 | 3 |
| zul | 86.4 ± 0.2 | [84.9, 87.9] | 0.56 | 4.8 | 472 | 11.0 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin | 84.9 | 78.8 | 76.6 | 54.5 |
| lug | 64.2 | 88.2 | 77.9 | 50.7 |
| swa | 63.2 | 81.1 | 91.4 | 54.3 |
| zul | 55.8 | 70.0 | 70.4 | 86.4 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|
| kin | 1.00 | 0.89 | 0.84 | 0.63 | 0.79 |
| lug | 0.76 | 1.00 | 0.85 | 0.59 | 0.73 |
| swa | 0.74 | 0.92 | 1.00 | 0.63 | 0.76 |
| zul | 0.66 | 0.79 | 0.77 | 1.00 | 0.74 |
| mean as target | 0.72 | 0.87 | 0.82 | 0.62 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 88% |
| share of variance explained by the source (row means) | 4% |
| Bantu -> Bantu, mean entity F1 % | 66.5 |
| amh/hau -> Bantu, mean entity F1 % | n/a |

