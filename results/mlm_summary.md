# Serengeti vocabulary with the masked-LM step (NER and POS)

Tuned LoRA from the sweep (NER r=32 qv, POS r=8 qv), seeds 1-3, kin lug swa zul, up to 20 epochs with early stopping. Differences in points; CIs bootstrap test sentences (paired) and seeds.

## Pooled

| task | comparison | in-language difference | 95% CI | zero-shot difference |
|---|---|---|---|---|
| NER | Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect) | -1.5 | [-2.2, -0.7] | +1.4 |
| POS | Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect) | -0.9 | [-1.1, -0.6] | -0.4 |

## Masked-LM pass: held-out loss before -> after (embedding-only, 3,000 steps of 32 blocks)

| model | kin | lug | swa | zul |
|---|---|---|---|---|
| serengeti_mlm | 7.75 -> 3.58 | 7.49 -> 3.34 | 5.96 -> 3.22 | 6.97 -> 3.41 |
| afroxlmr_mlm | 1.30 -> 1.22 | 1.55 -> 1.42 | 1.34 -> 1.28 | 1.29 -> 1.30 |

Losses are per predicted token, and the two vocabularies cut text differently, so the two rows are not directly comparable; the gap is still large.

## NER: Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect)

| lang | afroxlmr_mlm | serengeti_mlm | difference | 95% CI (sentences + seeds) |
|---|---|---|---|---|
| kin | 86.1 | 84.9 | -1.2 | [-2.9, +0.8] |
| lug | 89.5 | 88.2 | -1.3 | [-2.8, +0.1] |
| swa | 92.2 | 91.4 | -0.8 | [-1.3, -0.3] |
| zul | 88.9 | 86.4 | -2.5 | [-4.3, -0.9] |

Pooled over 4 languages: -1.5 points, 95% CI [-2.2, -0.7].

Zero-shot, all 12 transfer cells: 65.1 -> 66.5 (+1.4).

Difference per transfer cell (rows = source, columns = target):

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin |  | -1.4 | +1.1 | +0.4 |
| lug | -4.7 |  | -0.6 | +9.5 |
| swa | -1.7 | -1.2 |  | +12.4 |
| zul | -0.6 | +1.0 | +2.2 |  |

## POS: Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect)

| lang | afroxlmr_mlm | serengeti_mlm | difference | 95% CI (sentences + seeds) |
|---|---|---|---|---|
| kin | 98.3 | 97.5 | -0.8 | [-1.1, -0.5] |
| lug | 92.0 | 91.0 | -0.9 | [-1.4, -0.5] |
| swa | 92.8 | 92.3 | -0.5 | [-0.8, -0.1] |
| zul | 89.4 | 88.2 | -1.3 | [-1.8, -0.7] |

Pooled over 4 languages: -0.9 points, 95% CI [-1.1, -0.6].

Zero-shot, all 12 transfer cells: 65.3 -> 65.0 (-0.4).

Difference per transfer cell (rows = source, columns = target):

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin |  | +1.4 | -1.0 | +0.3 |
| lug | +0.6 |  | -0.6 | -1.2 |
| swa | -3.4 | +0.8 |  | -0.4 |
| zul | -1.3 | +0.1 | +0.4 |  |

## Interpretation

Written 2026-11-22 from the runs above (one GPU, A100, bf16, for both models).

- **With the masked-LM step, Serengeti's vocabulary is still slightly worse in-language than the original vocabulary given the same step:** NER −1.5 points [−2.2, −0.7], POS −0.9 [−1.1, −0.6], lower in every language. The step is what FVT prescribes, so this is now a fair test of option B at this amount of adaptation, and it does not help in-language.
- **The gap is much smaller than the frozen version suggested** (−5.8 NER, −2.3 POS against plain LoRA). The baselines differ (the frozen run was compared with untuned LoRA r=8 trained for 5 or 10 epochs), so read this only as a rough sign that training the new embeddings recovers most of the loss.
- **NER transfer into isiZulu rises again, now against a matched control:** lug→zul +9.5 [+7.3, +11.7] and swa→zul +12.4 [+10.3, +14.6]; kin→zul +0.4 (wide CI). The frozen Serengeti run showed the same two cells (+7.9, +7.5) against a different baseline, so the effect replicates across two setups. It is NER only: POS transfer into isiZulu does not move (−1.2, −0.4, +0.3). This fits the isiZulu lead: a third of isiZulu entity words are prefix + capital (uKaunda), AfroXLMR splits the prefix off on its own in 89% of them and Serengeti keeps prefix and capital together in about half. The capital-split run (block B) tests this directly.
- **Transfer into Kinyarwanda drops** for NER (lug→kin −4.7 [−6.2, −3.3], swa→kin −1.7) and POS (swa→kin −3.4 [−4.4, −2.5]). Pooled over the 12 transfer cells, NER +1.4 and POS −0.4: the vocabulary moves transfer between pairs rather than improving it overall.
- **The new embeddings are probably undertrained.** Held-out masked-LM loss for the Serengeti model fell from 6 to 7.7 down to 3.2 to 3.6, but stays far above AfroXLMR's 1.2 to 1.4. The units differ (losses are per token, and Serengeti's tokens are longer), so the gap overstates the difference, but not by a factor of 2.5. 3,000 steps on the embeddings alone may be too little; Kumar & Dušek (2026) train the whole body after the swap.
- **The masked-LM pass barely changed plain AfroXLMR** (loss 1.30 → 1.22 kin, 1.29 → 1.30 zul). Whether it changed fine-tuning results is answered once the converged LoRA baseline (block A) is in: `src/mlm_report.py` then adds that comparison.

What this means for RQ1: changing the vocabulary did not help in-language with frozen or with trained embeddings, consistent with FOCUS finding the original vocabulary with the same adaptation almost as good. The one robust effect is on NER transfer into isiZulu, which points to how isiZulu writes names rather than to morphology in general.

