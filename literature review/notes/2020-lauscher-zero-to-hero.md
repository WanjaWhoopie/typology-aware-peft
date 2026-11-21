# From Zero to Hero: On the Limitations of Zero-Shot Language Transfer with Multilingual Transformers

## Reference

| Field | Details |
|---|---|
| **Title** | From Zero to Hero: On the Limitations of Zero-Shot Language Transfer with Multilingual Transformers |
| **Authors** | Anne Lauscher, Vinit Ravishankar, Ivan Vulić, Goran Glavaš |
| **Year** | 2020 |
| **Venue** | EMNLP 2020, pp. 4483-4499 |
| **DOI / URL** | https://doi.org/10.18653/v1/2020.emnlp-main.363 |
| **PDF (online)** | https://aclanthology.org/2020.emnlp-main.363.pdf |
| **Code / data** | not checked |

**Citation (APA):**
> Lauscher, A., Ravishankar, V., Vulić, I., & Glavaš, G. (2020). From zero to hero: On the limitations of zero-shot language transfer with multilingual transformers. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)* (pp. 4483-4499). Association for Computational Linguistics. https://doi.org/10.18653/v1/2020.emnlp-main.363

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{lauscher-etal-2020-zero,
  title     = {From Zero to Hero: On the Limitations of Zero-Shot Language Transfer with Multilingual Transformers},
  author    = {Lauscher, Anne and Ravishankar, Vinit and Vuli{\'c}, Ivan and Glava{\v{s}}, Goran},
  booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  year      = {2020},
  pages     = {4483--4499},
  doi       = {10.18653/v1/2020.emnlp-main.363}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | Medium |
| **Tags** | #cross-lingual-transfer #few-shot #zero-shot #typology #mBERT #XLM-R |

## Summary

The paper shows that zero-shot transfer from English with mBERT and XLM-R drops sharply for distant languages and for languages with small pretraining corpora, across DEP, POS, NER, XNLI and XQuAD. Transfer for low-level tasks is predicted by lang2vec syntactic similarity; for high-level tasks, by similarity plus target pretraining corpus size. Adding k target-language examples (10 to 1,000) after English fine-tuning gives large gains on DEP and POS, smaller on NER, and small on XNLI and XQuAD.

## Review claim check

- **Claim:** "few-shot transfer is surprisingly effective across the board".
- **Verdict:** partly holds.
- **Evidence:** the abstract says exactly this (p. 4483), but Table 4 shows gains are large for low-level tasks and small for high-level ones: XNLI with mBERT is -0.03 at k = 10 and -1.00 at k = 100, and maximum gains for XNLI/XQuAD are 2.52 to 4.57 points.

## Research question / problem

- Where does zero-shot transfer with MMTs fail, what predicts it, and is cheap few-shot annotation a better investment?

## Method

- **Approach:** zero-shot from English, then sequential fine-tuning on k random target examples; correlation and regression with lang2vec similarity and corpus size.
- **Model(s) / architecture:** mBERT, XLM-R (base). For DEP, POS, NER the transformer is frozen and only a task head is trained (p. 4486); full fine-tuning for XNLI and XQuAD.
- **PEFT method (if any):** none (frozen encoder + head for low-level tasks).
- **Languages covered:** 12 target languages for DEP/POS/NER (e.g. ZH, TR, RU, AR, HI, EU, FI, HE, IT, JA, KO, SV); XNLI includes Swahili and Urdu.
- **Datasets:** UD, WikiANN (Rahimi et al. splits), XNLI, XQuAD.
- **Tasks:** DEP, POS, NER, XNLI, XQuAD.
- **Evaluation metrics:** UAS, accuracy, F1, accuracy, F1.
- **Compute / hardware:** not a focus.

## Key findings

Few-shot gains over zero-shot (Table 4, averaged across languages; k = number of target sentences, articles for XQuAD):

| Task (mBERT / XLM-R) | k = 0 | gain at k = 10 | gain at k = 100 | gain at k = 1000 |
|---|---|---|---|---|
| DEP (UAS) | 52.96 / 48.60 | +13.73 / +16.97 | +21.84 / +25.48 | +29.77 / +34.73 |
| POS (acc) | 67.2 / 65.5 | +12.96 / +15.18 | +19.88 / +22.09 | +25.44 / +27.3 |
| NER (F1) | 79.34 / 85.43 | +3.84 / +2.63 | +5.91 / +6.06 | +9.97 / +8.39 |
| XNLI (acc) | 65.92 / 73.32 | -0.03 / +0.41 | -1.00 / +1.71 | +2.24 / +2.52 |
| XQuAD (F1), k in articles 2 to 10 | 45.62 / 53.68 | max +4.57 / +2.10 at 10 articles | | |

1. Distant languages with small corpora gain most from few-shot data.
2. Sampling: longer sentences best for DEP/POS; random best for NER.
3. Even 10 sentences help DEP and POS by double digits.

## What we got from it

- Few-shot fine-tuning on target data is a cheap, strong baseline for any transfer method, including our RQ3 transfer to related languages; typology-aware zero-shot methods must be compared with "k = 10 to 100 target sentences".
- lang2vec syntactic similarity predicts low-level task transfer, supporting typology as a gate signal for POS/NER.

## Gaps and limitations

- **Stated by the authors:** focus on zero-shot limitations; analysis restricted to available datasets.
- **Our observations:** no African languages in the low-level tasks; base-size MMTs; low-level tasks use a frozen encoder, so gains are for a linear/biaffine head, not for full or PEFT fine-tuning.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** linguistic proximity explains part of transfer; supports using typology for routing but shows it is incomplete (corpus size also matters).
- **Low-resource / African language angle:** Swahili only (XNLI), where zero-shot XNLI drops about 20%.
- **Efficiency / low-cost hardware angle:** annotating tens of sentences can beat expensive model changes.
- **Baseline for us?** Yes: few-shot target fine-tuning (same LoRA, k in {10, 50, 100}) as a baseline next to the typology-gated mixture for unseen related languages.

## Quotes and figures worth citing

> "the inexpensive few-shot transfer (i.e., additional fine-tuning on a few target-language instances) is surprisingly effective across the board" (abstract, p. 4483)

> "we improve dependency parsing for some target languages up to 40 UAS points with as few as 10 target language sentences." (p. 4484)

- Table 4: few-shot gains per task and k.

## Related papers to follow up

- [ ] Hu et al. 2020, XTREME.
- [ ] Wu and Dredze 2020, are all languages created equal in mBERT?

## Open questions / discussion points

- For Bantu NER, how many target sentences close the gap that a typology gate is meant to close?
