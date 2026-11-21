# NER: Morfessor, morphemes as separate words vs plain LoRA

Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. Metric: entity F1 (%). See src/variants_report.py for what the variant changes.

## In-language

| lang | LoRA | variant | difference | 95% CI (sentences + seeds) | tokens/word |
|---|---|---|---|---|---|
| amh | 73.6 | 62.3 | -11.3 | [-14.9, -7.8] | 2.10 -> 2.77 |
| hau | 83.1 | 68.8 | -14.3 | [-16.3, -12.4] | 1.55 -> 2.24 |
| kin | 84.6 | 79.7 | -4.9 | [-6.1, -3.9] | 2.34 -> 2.79 |
| lug | 84.1 | 79.6 | -4.5 | [-6.5, -2.7] | 2.44 -> 2.85 |
| swa | 91.4 | 87.5 | -3.9 | [-4.7, -3.1] | 1.51 -> 2.28 |
| zul | 86.5 | 83.6 | -2.8 | [-4.3, -1.4] | 2.43 -> 2.84 |

Pooled over 6 languages and all seeds: -7.0 points, 95% CI [-7.8, -6.1] (bootstrap over test sentences, paired, and seeds).

## Zero-shot transfer (off-diagonal)

| cells | LoRA | variant | difference |
|---|---|---|---|
| all 30 cells | 57.5 | 45.1 | -12.4 |
| Bantu -> Bantu | 63.6 | 55.0 | -8.5 |
| amh/hau -> Bantu | 58.1 | 47.2 | -10.8 |

### Difference per cell (variant minus LoRA; rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | -11.3 | -22.4 | -10.5 | -19.2 | -9.7 | -3.4 |
| hau | -23.3 | -14.3 | -9.4 | -14.9 | -10.7 | -9.1 |
| kin | -17.9 | -20.1 | -4.9 | -10.2 | -5.1 | -7.5 |
| lug | -12.9 | -18.4 | -7.0 | -4.5 | -7.4 | -3.2 |
| swa | -21.2 | -17.0 | -7.4 | -10.5 | -3.9 | -5.2 |
| zul | -14.4 | -14.8 | -11.5 | -17.3 | -10.1 | -2.8 |

## Interpretation

Morfessor pre-segmentation lowers NER in every language: -7.0 points pooled, 95% CI [-7.8, -6.1] (sentences and seeds resampled). Zero-shot transfer drops even more (-12.4 points over the 30 off-diagonal cells). Test sentences are never cut off by the 256-token limit in either setting, so the loss comes from the input, not from truncation.

- **Smallest losses** are for the three languages AfroXLMR already splits the most (zul -2.8, lug -4.5, kin -4.9). These are agglutinative Bantu languages. One possible reason is that Morfessor's cuts are more often real morpheme boundaries there, but that is untested: Morfessor's precision on isiZulu gold is only 0.51, and no gold exists for the others.
- **Largest losses** are for hau (-14.3) and amh (-11.3). Hausa has little agglutinative morphology, so many cuts are probably spurious (no gold to check). Amharic script writes a consonant and a vowel as one character, so a morpheme boundary often falls inside a character and cannot be marked.
- **Likely cause (with embeddings frozen):** each morpheme enters the model as a separate word (with its own word-start marker), a form the pretrained model never saw. LoRA (0.14% of the weights, embeddings frozen) cannot relearn that. Splitting words while keeping the vocabulary therefore moves the input away from what the model knows, rather than towards morphology.
- **Follow-up (done):** keeping the morpheme cuts inside words, without the extra word starts, halves the NER loss (−3.9) and nearly removes the POS loss (−0.5). See results/variants_summary.md.

