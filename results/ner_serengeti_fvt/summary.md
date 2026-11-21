# NER baseline summary

Model: /content/afroxlmr_serengeti_fvt. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 55.1 ± 0.6 | [51.2, 58.9] | 0.14 | 3.5 | 47 | 4.7 | 500 | 3 |
| hau | 80.5 ± 0.0 | [79.2, 81.7] | 0.14 | 4.3 | 157 | 5.0 | 1633 | 3 |
| kin | 80.6 ± 0.3 | [79.3, 82.0] | 0.14 | 4.8 | 216 | 4.3 | 2235 | 3 |
| lug | 81.0 ± 0.5 | [79.2, 82.7] | 0.14 | 4.3 | 134 | 4.3 | 1412 | 3 |
| swa | 90.5 ± 0.1 | [89.6, 91.3] | 0.14 | 4.4 | 181 | 5.0 | 1883 | 3 |
| zul | 80.6 ± 0.5 | [78.7, 82.3] | 0.14 | 4.7 | 161 | 4.3 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 55.1 | 43.4 | 34.2 | 47.1 | 53.2 | 37.1 |
| hau | 28.7 | 80.5 | 57.1 | 72.9 | 71.9 | 49.3 |
| kin | 27.9 | 67.5 | 80.6 | 75.1 | 73.1 | 51.1 |
| lug | 21.8 | 60.9 | 56.7 | 81.0 | 74.9 | 45.9 |
| swa | 36.5 | 62.1 | 59.2 | 73.2 | 90.5 | 50.3 |
| zul | 19.0 | 55.0 | 51.6 | 64.8 | 67.3 | 80.6 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.54 | 0.42 | 0.58 | 0.59 | 0.46 | 0.52 |
| hau | 0.52 | 1.00 | 0.71 | 0.90 | 0.79 | 0.61 | 0.71 |
| kin | 0.51 | 0.84 | 1.00 | 0.93 | 0.81 | 0.63 | 0.74 |
| lug | 0.40 | 0.76 | 0.70 | 1.00 | 0.83 | 0.57 | 0.65 |
| swa | 0.66 | 0.77 | 0.73 | 0.90 | 1.00 | 0.62 | 0.74 |
| zul | 0.34 | 0.68 | 0.64 | 0.80 | 0.74 | 1.00 | 0.64 |
| mean as target | 0.49 | 0.72 | 0.64 | 0.82 | 0.75 | 0.58 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 75% |
| share of variance explained by the source (row means) | 10% |
| Bantu -> Bantu, mean entity F1 % | 61.9 |
| amh/hau -> Bantu, mean entity F1 % | 52.8 |

