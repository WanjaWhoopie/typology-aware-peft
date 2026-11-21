# Tokenization variants vs plain LoRA (NER and POS)

All variants: LoRA r=8 on Davlan/afro-xlmr-large-76L, seeds 1-3, the settings and trainable parameters of the LoRA baseline; only the input differs. Differences in points; CIs are paired bootstraps over test sentences, pooled over 6 languages and seeds.

## Pooled

| task | variant | in-language difference | 95% CI | zero-shot difference (30 cells) |
|---|---|---|---|---|
| NER | Morfessor, morphemes as separate words | -7.0 | [-7.5, -6.4] | -12.4 |
| NER | Morfessor, cuts inside words | -3.9 | [-4.4, -3.4] | -3.9 |
| NER | Serengeti vocabulary (FVT) | -5.8 | [-6.5, -5.2] | -4.5 |
| POS | Morfessor, morphemes as separate words | -3.4 | [-3.6, -3.2] | -9.8 |
| POS | Morfessor, cuts inside words | -0.5 | [-0.6, -0.3] | -2.3 |
| POS | Serengeti vocabulary (FVT) | -2.3 | [-2.5, -2.1] | -5.3 |

## NER per language: plain LoRA entity F1 and each variant's difference

| lang | LoRA | Morfessor, morphemes as separate words | Morfessor, cuts inside words | Serengeti vocabulary (FVT) |
|---|---|---|---|---|
| amh | 73.6 | -11.3 | -9.2 | -18.5 |
| hau | 83.1 | -14.3 | -7.4 | -2.6 |
| kin | 84.6 | -4.9 | -1.8 | -4.0 |
| lug | 84.1 | -4.5 | -1.7 | -3.1 |
| swa | 91.4 | -3.9 | -2.1 | -0.9 |
| zul | 86.5 | -2.8 | -1.0 | -5.9 |

## POS per language: plain LoRA accuracy and each variant's difference

| lang | LoRA | Morfessor, morphemes as separate words | Morfessor, cuts inside words | Serengeti vocabulary (FVT) |
|---|---|---|---|---|
| amh | 91.9 | -3.3 | +0.1 | -2.2 |
| hau | 92.0 | -5.9 | -1.2 | -0.9 |
| kin | 98.1 | -2.0 | -0.2 | -2.7 |
| lug | 91.7 | -3.6 | -0.5 | -4.2 |
| swa | 92.5 | -3.1 | -0.8 | -0.9 |
| zul | 89.1 | -2.6 | -0.3 | -2.7 |

## Tokens per word (NER + POS training words)

| lang | AfroXLMR | Morfessor, separate words | Morfessor, inside words | Serengeti | Serengeti tokens new to AfroXLMR | same, NER test entity words |
|---|---|---|---|---|---|---|
| amh | 2.10 | 2.77 | 2.44 | 1.38 | 39% | 44% |
| hau | 1.55 | 2.24 | 2.23 | 1.14 | 33% | 27% |
| kin | 2.34 | 2.79 | 2.76 | 1.50 | 50% | 33% |
| lug | 2.44 | 2.85 | 2.84 | 1.62 | 47% | 32% |
| swa | 1.51 | 2.28 | 2.22 | 1.08 | 33% | 24% |
| zul | 2.43 | 2.84 | 2.77 | 1.68 | 46% | 37% |

## Interpretation

None of the three input-side variants beats plain LoRA. They all keep the model, the LoRA settings and the trainable parameters, and change only how words reach the model. All 72 runs finished; none collapsed.

**1. Most of the first Morfessor attempt's loss came from the extra word starts, not from extra tokens.**
- Keeping Morfessor's cuts inside words gives almost the same number of tokens per word (for example hau 2.23 against 2.24, zul 2.77 against 2.84).
- Yet the loss is roughly halved for NER (−3.9 against −7.0) and nearly gone for POS (−0.5 against −3.4).
- Zero-shot transfer recovers most (NER −3.9 against −12.4, POS −2.3 against −9.8).
- Feeding each morpheme as a new word is what moved the input away from what the model knows.

**2. The remaining loss with cuts inside words is small for the Bantu languages and large where Morfessor is least reliable.**
- In NER, kin, lug and zul lose 1.0 to 1.8 points, against 7.4 for hau and 9.2 for amh.
- In POS every language is within 1.2 points, and Amharic is level (+0.1).
- Forcing token boundaries onto morpheme boundaries is close to harmless where the cuts are good, but it does not help either. AfroXLMR's own pieces already carry what the task needs.

**3. Serengeti's vocabulary (option B) shortens words a lot but costs accuracy, because many tokens get averaged vectors.**
- Tokens per word drop by about a third (for example zul 2.43 → 1.68, swa 1.51 → 1.08). Yet NER loses 5.8 points and POS 2.3.
- The NER loss follows how many entity-word tokens are new to AfroXLMR, and so carry an averaged vector: amh 44% → −18.5, zul 37% → −5.9, kin 33% → −4.0, lug 32% → −3.1, hau 27% → −2.6, swa 24% → −0.9. That is a perfect rank order over six languages.
- POS shows the same split: the languages with 46 to 50% new tokens (kin, lug, zul) lose 2.7 to 4.2 points, those with 33% (hau, swa) lose 0.9.
- The vocabulary is not the problem. The averaged vectors are, and LoRA cannot change them because the embeddings stay frozen.
- Tokenizer-transfer papers therefore train the new embeddings briefly before fine-tuning. That is the natural next step for option B: a short embedding-only masked-LM pass on the raw text, then the same LoRA runs.

**4. What this means for the thesis.**
Changing only the input, while the representations stay fixed, costs accuracy. The cost is smallest when the change keeps the input close to what the model saw in pretraining. A morphology-aware method therefore has to adapt the model side as well (adapter weights, or embeddings), not just re-cut the words. This supports moving the morphology into the typology-aware adapter rather than into the tokenizer alone.

