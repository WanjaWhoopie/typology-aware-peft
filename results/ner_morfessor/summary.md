# NER baseline summary

Model: Davlan/afro-xlmr-large-76L. Metric: entity F1 (%). Seeds per cell: [1, 2, 3].

Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh (different annotation round and splits).

## Method: lora

### In-language baseline (diagonal)

| lang | entity F1 % (mean ± sd over seeds) | 95% CI (test sentences) | trainable % | peak GPU GB | seconds/run | best epoch (mean) | test sentences | seeds |
|---|---|---|---|---|---|---|---|---|
| amh | 62.3 ± 1.9 | [58.3, 66.4] | 0.14 | 4.1 | 52 | 5.0 | 500 | 3 |
| hau | 68.8 ± 1.2 | [66.7, 70.8] | 0.14 | 5.4 | 203 | 4.3 | 1633 | 3 |
| kin | 79.7 ± 0.5 | [78.3, 81.2] | 0.14 | 5.4 | 280 | 5.0 | 2235 | 3 |
| lug | 79.6 ± 0.8 | [77.7, 81.5] | 0.14 | 5.7 | 157 | 5.0 | 1412 | 3 |
| swa | 87.5 ± 0.2 | [86.5, 88.5] | 0.14 | 6.2 | 233 | 4.7 | 1883 | 3 |
| zul | 83.6 ± 0.7 | [81.7, 85.4] | 0.14 | 5.4 | 182 | 4.3 | 1670 | 3 |

### Zero-shot transfer matrix: entity F1 % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 62.3 | 31.7 | 33.8 | 42.6 | 45.4 | 39.2 |
| hau | 16.0 | 68.8 | 52.3 | 64.5 | 63.3 | 36.8 |
| kin | 21.9 | 50.2 | 79.7 | 69.6 | 69.5 | 42.8 |
| lug | 18.6 | 44.1 | 57.0 | 79.6 | 70.2 | 34.8 |
| swa | 19.2 | 48.0 | 57.9 | 70.9 | 87.5 | 37.6 |
| zul | 26.3 | 38.7 | 44.6 | 50.3 | 54.8 | 83.6 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 0.46 | 0.42 | 0.54 | 0.52 | 0.47 | 0.48 |
| hau | 0.26 | 1.00 | 0.66 | 0.81 | 0.72 | 0.44 | 0.58 |
| kin | 0.35 | 0.73 | 1.00 | 0.87 | 0.79 | 0.51 | 0.65 |
| lug | 0.30 | 0.64 | 0.72 | 1.00 | 0.80 | 0.42 | 0.57 |
| swa | 0.31 | 0.70 | 0.73 | 0.89 | 1.00 | 0.45 | 0.62 |
| zul | 0.42 | 0.56 | 0.56 | 0.63 | 0.63 | 1.00 | 0.56 |
| mean as target | 0.33 | 0.62 | 0.62 | 0.75 | 0.69 | 0.46 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 76% |
| share of variance explained by the source (row means) | 6% |
| Bantu -> Bantu, mean entity F1 % | 55.0 |
| amh/hau -> Bantu, mean entity F1 % | 47.2 |

## Interpretation

Morfessor pre-segmentation lowers NER in every language: -7.0 points pooled, 95% CI [-7.5, -6.4]. Zero-shot transfer drops even more (-12.4 points over the 30 off-diagonal cells). Test sentences are never cut off by the 256-token limit in either setting, so the loss comes from the input, not from truncation.

- **Smallest losses** are for the three languages AfroXLMR already splits the most (zul -2.8, lug -4.5, kin -4.9). These are agglutinative Bantu languages, where Morfessor's cuts are most often real morpheme boundaries.
- **Largest losses** are for hau (-14.3) and amh (-11.3). Hausa has little agglutinative morphology, so most cuts are spurious. Amharic script writes a consonant and a vowel as one character, so a morpheme boundary often falls inside a character and cannot be marked.
- **Likely cause:** each morpheme enters the model as a separate word (with its own word-start marker), a form the pretrained model never saw. LoRA (0.14% of the weights, embeddings frozen) cannot relearn that. Splitting words while keeping the vocabulary therefore moves the input away from what the model knows, rather than towards morphology.
- **Follow-up (done):** keeping the morpheme cuts inside words, without the extra word starts, halves the NER loss (−3.9) and nearly removes the POS loss (−0.5). See results/variants_summary.md.

