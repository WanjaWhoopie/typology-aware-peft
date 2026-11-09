# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: full

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 78.3 ± 0.5 | [75.1, 81.4] | 100.00 | 11.2 | 167 | 4.0 | 500 | 3 |
| hau | 86.2 ± 0.3 | [85.1, 87.2] | 100.00 | 11.3 | 566 | 4.3 | 1633 | 3 |
| kin | 87.6 ± 0.2 | [86.7, 88.6] | 100.00 | 11.3 | 817 | 4.7 | 2235 | 3 |
| lug | 89.5 ± 0.8 | [88.3, 90.6] | 100.00 | 11.3 | 493 | 5.0 | 1412 | 3 |
| swa | 92.4 ± 0.0 | [91.7, 93.2] | 100.00 | 11.3 | 648 | 4.7 | 1883 | 3 |
| zul | 89.2 ± 0.2 | [87.9, 90.5] | 100.00 | 11.3 | 574 | 4.3 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 78.3 | 55.2 | 47.2 | 65.8 | 58.9 | 44.4 |
| hau | 38.3 | 86.2 | 65.2 | 81.5 | 73.4 | 45.0 |
| kin | 47.8 | 72.4 | 87.6 | 82.4 | 78.2 | 50.5 |
| lug | 35.0 | 66.3 | 68.7 | 89.5 | 79.5 | 41.6 |
| swa | 38.4 | 66.1 | 65.8 | 81.9 | 92.4 | 40.6 |
| zul | 44.1 | 56.8 | 58.0 | 68.0 | 68.8 | 89.2 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.64 | 0.54 | 0.74 | 0.64 | 0.50 | 0.61 |
| hau | 0.49 | 1.00 | 0.74 | 0.91 | 0.79 | 0.50 | 0.69 |
| kin | 0.61 | 0.84 | 1.00 | 0.92 | 0.85 | 0.57 | 0.76 |
| lug | 0.45 | 0.77 | 0.78 | 1.00 | 0.86 | 0.47 | 0.67 |
| swa | 0.49 | 0.77 | 0.75 | 0.91 | 1.00 | 0.46 | 0.68 |
| zul | 0.56 | 0.66 | 0.66 | 0.76 | 0.74 | 1.00 | 0.68 |
| mean as target | 0.52 | 0.74 | 0.70 | 0.85 | 0.78 | 0.50 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 81% |
| share of variance explained by the source (row means) | 6% |
| Bantu -> Bantu, mean entity F1 % | 65.3 |
| amh/hau -> Bantu, mean entity F1 % | 60.2 |

