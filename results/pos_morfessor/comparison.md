# POS: Morfessor pre-segmentation vs plain LoRA

Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. Metric: accuracy (%). Only the input differs: words split into Morfessor morphemes (corpus weight 0.1, seen words only), vocabulary unchanged.

## In-language

| lang | LoRA | LoRA + Morfessor | difference | 95% CI (paired) | AfroXLMR tokens/word |
|---|---|---|---|---|---|
| amh | 91.9 | 88.7 | -3.3 | [-4.2, -2.4] | 2.10 -> 2.77 |
| hau | 92.0 | 86.1 | -5.9 | [-6.4, -5.4] | 1.55 -> 2.24 |
| kin | 98.1 | 96.1 | -2.0 | [-2.2, -1.7] | 2.34 -> 2.79 |
| lug | 91.7 | 88.1 | -3.6 | [-4.0, -3.2] | 2.44 -> 2.85 |
| swa | 92.5 | 89.4 | -3.1 | [-3.5, -2.8] | 1.51 -> 2.28 |
| zul | 89.1 | 86.6 | -2.6 | [-3.0, -2.1] | 2.43 -> 2.84 |

Pooled over 6 languages and all seeds: -3.4 points, 95% CI [-3.6, -3.2] (paired bootstrap over test sentences).

## Zero-shot transfer (off-diagonal)

| cells | LoRA | LoRA + Morfessor | difference |
|---|---|---|---|
| all 30 cells | 55.0 | 45.2 | -9.8 |
| Bantu -> Bantu | 65.2 | 59.9 | -5.3 |
| amh/hau -> Bantu | 47.2 | 31.0 | -16.2 |

### Difference per cell (LoRA + Morfessor minus LoRA; rows = source, columns = target)

| source \ target | amh | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|---|
| amh | -3.3 | -13.8 | -24.7 | -26.4 | -16.0 | -23.8 |
| hau | -9.0 | -5.9 | -14.3 | -9.1 | -7.6 | -8.1 |
| kin | -8.9 | -12.9 | -2.0 | -5.2 | -5.6 | -5.2 |
| lug | -12.7 | -12.4 | -5.1 | -3.6 | -5.9 | -6.6 |
| swa | -10.7 | -7.3 | -7.4 | -6.2 | -3.1 | -4.1 |
| zul | -5.6 | -6.8 | -4.1 | -3.1 | -5.4 | -2.6 |

## Interpretation

Morfessor pre-segmentation lowers POS accuracy in every language: -3.4 points pooled, 95% CI [-3.6, -3.2]. Zero-shot transfer drops more (-9.8 points over the 30 off-diagonal cells), most from Amharic and Hausa as sources into the Bantu languages (-16.2). No test words are lost to truncation in either setting.

- **The pattern matches NER.** Losses are smallest for kin (-2.0), zul (-2.6) and swa (-3.1), and largest for hau (-5.9).
- **The loss is smaller than for NER.** A POS tag depends mostly on the word itself, while NER needs whole names, which the split breaks apart.
- **See results/ner_morfessor/interpretation.md** for the likely cause and the next variant worth testing.

