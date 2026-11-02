# SIB-200 baseline summary

Model: Davlan/afro-xlmr-large-76L. Seeds per cell: [1, 2, 3]. Test set: 204 items per language.

## Method: full

### In-language baseline (diagonal)

| lang | acc % (mean ± sd over seeds) | 95% CI (test items) | macro-F1 % | trainable % | peak GPU GB | seconds/run | seeds |
|---|---|---|---|---|---|---|---|
| amh | 86.1 ± 1.2 | [81.9, 90.2] | 85.1 | 100.00 | 11.3 | 267 | 3 |
| hau | 83.8 ± 0.7 | [79.4, 88.2] | 82.8 | 100.00 | 11.3 | 142 | 3 |
| kin | 86.3 ± 2.1 | [82.2, 90.0] | 85.4 | 100.00 | 11.3 | 147 | 3 |
| lug | 70.9 ± 2.1 | [65.4, 76.5] | 67.7 | 100.00 | 11.3 | 145 | 3 |
| swa | 87.9 ± 1.2 | [83.8, 91.5] | 87.7 | 100.00 | 11.3 | 138 | 3 |
| zul | 84.5 ± 2.2 | [79.9, 88.6] | 84.3 | 100.00 | 11.3 | 145 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 86.1 | 84.5 | 83.2 | 65.2 | 86.9 | 81.9 |
| hau | 86.1 | 83.8 | 85.3 | 68.0 | 86.8 | 82.2 |
| kin | 82.8 | 81.9 | 86.3 | 66.5 | 83.8 | 77.9 |
| lug | 82.2 | 81.5 | 80.6 | 70.9 | 84.3 | 81.4 |
| swa | 84.3 | 83.8 | 84.5 | 67.3 | 87.9 | 84.5 |
| zul | 85.1 | 83.8 | 83.0 | 66.8 | 88.1 | 84.5 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 1.01 | 0.96 | 0.92 | 0.99 | 0.97 | 0.97 |
| hau | 1.00 | 1.00 | 0.99 | 0.96 | 0.99 | 0.97 | 0.98 |
| kin | 0.96 | 0.98 | 1.00 | 0.94 | 0.95 | 0.92 | 0.95 |
| lug | 0.95 | 0.97 | 0.93 | 1.00 | 0.96 | 0.96 | 0.96 |
| swa | 0.98 | 1.00 | 0.98 | 0.95 | 1.00 | 1.00 | 0.98 |
| zul | 0.99 | 1.00 | 0.96 | 0.94 | 1.00 | 1.00 | 0.98 |
| mean as target | 0.98 | 0.99 | 0.97 | 0.94 | 0.98 | 0.97 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 95% |
| share of variance explained by the source (row means) | 3% |
| Bantu -> Bantu, mean acc % | 79.1 |
| amh/hau -> Bantu, mean acc % | 79.9 |

## Method: lora

### In-language baseline (diagonal)

| lang | acc % (mean ± sd over seeds) | 95% CI (test items) | macro-F1 % | trainable % | peak GPU GB | seconds/run | seeds |
|---|---|---|---|---|---|---|---|
| amh | 88.1 ± 0.8 | [84.0, 92.0] | 87.2 | 0.33 | 4.4 | 43 | 3 |
| hau | 86.6 ± 0.6 | [82.4, 90.5] | 85.9 | 0.33 | 4.4 | 43 | 3 |
| kin | 85.0 ± 2.6 | [80.7, 88.7] | 84.0 | 0.33 | 4.6 | 44 | 3 |
| lug | 70.1 ± 2.0 | [64.4, 75.5] | 67.2 | 0.33 | 4.4 | 43 | 3 |
| swa | 88.7 ± 0.0 | [84.6, 92.5] | 88.5 | 0.33 | 4.2 | 43 | 3 |
| zul | 85.3 ± 1.4 | [80.9, 89.2] | 84.3 | 0.33 | 4.6 | 44 | 3 |

### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | 88.1 | 86.4 | 84.0 | 64.4 | 90.2 | 83.3 |
| hau | 84.0 | 86.6 | 81.4 | 66.8 | 87.9 | 84.6 |
| kin | 83.3 | 84.3 | 85.0 | 65.2 | 84.8 | 81.7 |
| lug | 83.7 | 82.8 | 82.5 | 70.1 | 83.5 | 81.9 |
| swa | 83.0 | 84.8 | 83.0 | 66.0 | 88.7 | 83.2 |
| zul | 86.4 | 85.9 | 84.8 | 66.8 | 86.6 | 85.3 |

### Relative transfer (zero-shot / in-language score of the target)

| source \ target | amh | hau | kin | lug | swa | zul | mean as source |
|---|---|---|---|---|---|---|---|
| amh | 1.00 | 1.00 | 0.99 | 0.92 | 1.02 | 0.98 | 0.98 |
| hau | 0.95 | 1.00 | 0.96 | 0.95 | 0.99 | 0.99 | 0.97 |
| kin | 0.95 | 0.97 | 1.00 | 0.93 | 0.96 | 0.96 | 0.95 |
| lug | 0.95 | 0.96 | 0.97 | 1.00 | 0.94 | 0.96 | 0.96 |
| swa | 0.94 | 0.98 | 0.98 | 0.94 | 1.00 | 0.98 | 0.96 |
| zul | 0.98 | 0.99 | 1.00 | 0.95 | 0.98 | 1.00 | 0.98 |
| mean as target | 0.95 | 0.98 | 0.98 | 0.94 | 0.98 | 0.97 |  |

### Structure of the zero-shot matrix (off-diagonal cells)

| measure | value |
|---|---|
| share of variance explained by the target (column means) | 96% |
| share of variance explained by the source (row means) | 2% |
| Bantu -> Bantu, mean acc % | 79.2 |
| amh/hau -> Bantu, mean acc % | 80.3 |

## lora minus full, in-language accuracy (percentage points)

| lang | difference |
|---|---|
| amh | +2.0 |
| hau | +2.8 |
| kin | -1.3 |
| lug | -0.8 |
| swa | +0.8 |
| zul | +0.8 |

Pooled over 6 languages and all seeds: +0.7 points, 95% CI [-0.7, +2.0] (paired bootstrap over test items).

## Interpretation

Note `src/sib200_report.py` rebuilds summary.md and appends this file at the end. If the runs change, check that the numbers below still hold.

**1. In-language accuracy is 84 to 89% for five languages; Luganda is the outlier at about 70%.** Luganda is also the weakest target from every source (64 to 68%), so the difficulty lies in the model's handling of Luganda text, not in training on it. The data do not say why. Thinner pretraining coverage or heavier tokenizer fragmentation are candidates; the fragmentation study can test the second. Luganda LoRA runs also reached their best dev score late (epochs 8 to 10), so a few more epochs might help slightly.

**2. LoRA (r=8) matches full fine-tuning.** Per-language differences run from -1.3 to +2.8 points, each well inside the ±4 to 5 point test-set CI. Pooled over languages and seeds the difference is about +0.7 points with a CI that includes zero (see above), so the claim is "LoRA matches full fine-tuning", not "LoRA is better". LoRA trains 0.33% of the parameters, peaks at about 4.4 GB instead of 11.3 GB and takes about 43 s per run instead of about 140 s. Both fit on a 16 GB GPU, which supports G7. (The 267 s for Amharic full fine-tuning is inflated by the model download in the first run, 520 s; the other two runs took about 140 s.)

**3. Zero-shot transfer is close to in-language accuracy and carries almost no pair-specific signal.** Every off-diagonal cell reaches 92 to 102% of the target's in-language score. About 95% of the off-diagonal variance comes from which language is the target, and only 2 to 3% from the source. Bantu sources transfer to Bantu targets no better than Amharic and Hausa do (about 79 vs 80%), so there is no visible Bantu cluster. A likely reason is that SIB-200 is built from FLORES: every language has the same sentences, and topic labels are easy for a multilingual encoder to carry across languages. Most cell differences are also within the noise of a 204-item test set.

**What this means for the plan.** The SIB-200 matrix is a weak signal for RQ2 check (a), correlating typological distance with transfer. Report it, but rely on the NER and POS matrices for that check, and state the ceiling effect as a finding in the write-up. Off-diagonal cells above 100% (for example amh -> swa with LoRA) are noise, not real gains.

