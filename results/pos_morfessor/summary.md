# POS baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: accuracy (%). Seeds per cell: [1, 2, 3].

Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. Amharic tokens are UD syntactic words (clitics split off), not surface words.

## Method: lora

### In-language baseline (diagonal)

| lang | accuracy % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 88.7 ± 0.1 | [87.1, 90.1] | 0.14 | 3.5 | 43 | 8.7 | 216 | 3 |
| hau | 86.1 ± 0.0 | [85.3, 86.8] | 0.14 | 5.6 | 60 | 9.7 | 601 | 3 |
| kin | 96.1 ± 0.1 | [95.8, 96.5] | 0.14 | 5.1 | 57 | 10.0 | 604 | 3 |
| lug | 88.1 ± 0.1 | [87.4, 88.8] | 0.14 | 4.5 | 45 | 9.0 | 586 | 3 |
| swa | 89.4 ± 0.2 | [88.7, 90.0] | 0.14 | 5.5 | 60 | 9.3 | 553 | 3 |
| zul | 86.6 ± 0.1 | [85.8, 87.4] | 0.14 | 5.0 | 49 | 9.3 | 601 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 88.7 | 27.2 | 22.5 | 22.9 | 30.3 | 18.3 |
| hau | 33.2 | 86.1 | 41.8 | 34.3 | 43.5 | 34.3 |
| kin | 39.8 | 46.9 | 96.1 | 63.3 | 56.1 | 65.0 |
| lug | 37.0 | 46.5 | 64.6 | 88.1 | 57.0 | 59.8 |
| swa | 31.3 | 42.9 | 66.7 | 54.5 | 89.4 | 61.0 |
| zul | 35.5 | 49.0 | 65.6 | 52.7 | 52.4 | 86.6 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.32 | 0.23 | 0.26 | 0.34 | 0.21 | 0.27 |
| hau | 0.37 | 1.00 | 0.43 | 0.39 | 0.49 | 0.40 | 0.42 |
| kin | 0.45 | 0.54 | 1.00 | 0.72 | 0.63 | 0.75 | 0.62 |
| lug | 0.42 | 0.54 | 0.67 | 1.00 | 0.64 | 0.69 | 0.59 |
| swa | 0.35 | 0.50 | 0.69 | 0.62 | 1.00 | 0.71 | 0.57 |
| zul | 0.40 | 0.57 | 0.68 | 0.60 | 0.59 | 1.00 | 0.57 |
| mean as target | 0.40 | 0.49 | 0.54 | 0.52 | 0.54 | 0.55 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 14% |
| share of variance explained by the source (row means) | 60% |
| Bantu -> Bantu, mean accuracy % | 59.9 |
| amh/hau -> Bantu, mean accuracy % | 31.0 |

## Interpretation

Morfessor pre-segmentation lowers POS accuracy in every language: -3.4 points pooled, 95% CI [-3.6, -3.2]. Zero-shot transfer drops more (-9.8 points over the 30 off-diagonal cells), most from Amharic and Hausa as sources into the Bantu languages (-16.2). No test words are lost to truncation in either setting.

- **The pattern matches NER.** Losses are smallest for kin (-2.0), zul (-2.6) and swa (-3.1), and largest for hau (-5.9).
- **The loss is smaller than for NER.** A POS tag depends mostly on the word itself, while NER needs whole names, which the split breaks apart.
- **See results/ner_morfessor/interpretation.md** for the likely cause and the next variant worth testing.

