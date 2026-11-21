# MasakhaNER 2.0: Africa-centric Transfer Learning for Named Entity Recognition

## Reference

| Field | Details |
|---|---|
| **Title** | MasakhaNER 2.0: Africa-centric Transfer Learning for Named Entity Recognition |
| **Authors** | David Ifeoluwa Adelani, Graham Neubig, Sebastian Ruder, Shruti Rijhwani, Michael Beukman, et al. (Masakhane NLP) |
| **Year** | 2022 |
| **Venue** | EMNLP 2022 (Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing), Abu Dhabi, pp. 4488-4508 |
| **DOI / URL** | https://doi.org/10.18653/v1/2022.emnlp-main.298 |
| **PDF (online)** | [arXiv 2210.12391](https://arxiv.org/pdf/2210.12391) (read: v2) |
| **Code / data** | https://github.com/masakhane-io/masakhane-ner/tree/main/MasakhaNER2.0 |

**Citation (APA):**
> Adelani, D. I., Neubig, G., Ruder, S., Rijhwani, S., Beukman, M., et al. (2022). MasakhaNER 2.0: Africa-centric transfer learning for named entity recognition. In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing* (pp. 4488-4508). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.emnlp-main.298

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{adelani-etal-2022-masakhaner,
  title     = {{MasakhaNER} 2.0: Africa-centric Transfer Learning for Named Entity Recognition},
  author    = {Adelani, David Ifeoluwa and Neubig, Graham and Ruder, Sebastian and Rijhwani, Shruti and Beukman, Michael and others},
  booktitle = {Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing},
  year      = {2022},
  pages     = {4488--4508},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2022.emnlp-main.298}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | High |
| **Tags** | #benchmark #NER #transfer #source-selection #hausa #swahili #zulu #kinyarwanda #luganda #low-resource |

## Summary

Builds MasakhaNER 2.0, a news-domain NER dataset for 20 Sub-Saharan African languages (PER, ORG, LOC, DATE). Benchmarks multilingual PLMs; AfroXLMR-large is best (87.0 average F1 over 5 runs). Runs a 42 x 42 zero-shot transfer study (mDeBERTaV3, 22 non-MasakhaNER datasets plus the 20 new ones) and trains LangRank with lang2vec distances and entity overlap. Geographic distance and entity overlap are the most useful features; the best source beats English by about 14 F1 on average.

## Review claim check

| Claim | Verdict | Evidence |
|---|---|---|
| "AfroXLMR-large NER scores 87.4 / 87.5 / 89.6 / 92.7 / 90.6 for hau / kin / lug / swa / zul in Table 4" | **Holds** | Table 4, AfroXLMR-large row: hau 87.4, kin 87.5, lug 89.6, swa 92.7, zul 90.6 (average over 5 runs). |
| "Southern Bantu languages capitalise names after the noun-class prefix, which may limit transfer from languages without this feature as NER models overfit on capitalization" | **Holds** (with scope note) | Sec. 3.2 says this for three languages, chiShona, isiXhosa and isiZulu, citing Mayhew et al. (2019). It is stated as a possibility, not tested. |

## Research question / problem

- No large NER data for Southern African languages; unclear how to pick a source language for zero-shot NER in Africa.

## Method

- **Approach:** dataset creation; in-language fine-tuning baselines; single-source and top-2 co-training zero-shot transfer; LangRank source ranking (leave-one-target-out).
- **Model(s) / architecture:** mBERT, XLM-R base/large, RemBERT, mDeBERTaV3, AfriBERTa, AfroXLMR base/large (baselines); mDeBERTaV3 for all transfer runs.
- **PEFT method (if any):** none.
- **Languages covered:** 20 African (bam, bbj, ewe, fon, hau, ibo, kin, lug, luo, mos, nya, pcm, sna, swa, tsn, twi, wol, xho, yor, zul) plus 22 other NER datasets (42 languages total). No Amharic in 2.0.
- **Datasets:** MasakhaNER 2.0 (news), MasakhaNER 1.0, other public NER sets.
- **Tasks:** NER.
- **Evaluation metrics:** entity-level micro F1.
- **Compute / hardware:** V100 for large PLMs; lr 5e-5, batch 16, grad. accum. 2, max length 200, 50 epochs (App. J).

## Key findings

1. AfroXLMR-large in-language F1 (Table 4, 5 runs):

| hau | kin | lug | swa | zul | avg (20 langs) |
|---|---|---|---|---|---|
| 87.4 | 87.5 | 89.6 | 92.7 | 90.6 | 87.0 |

2. Our full fine-tuning (86.2 / 87.6 / 89.5 / 92.4 / 89.2) is within 0.3 F1 for kin, lug, swa, but 1.2 lower for hau and 1.4 lower for zul.
3. Transfer from African sources averages 57.3 F1 vs 51.7 from non-African sources; sna is the best average source (64), bbj the worst (41.0).
4. Best sources (Table 6, single source F1): kin <- hau (71.1), then swa (70.6); lug <- kin (81.1), then nya (80.0); swa <- deu (88.7), then ara (88.1); zul <- xho (82.1), then sna (69.4); hau <- pcm (75.9), then yor (74.3). English is far worse for zul (44.7) and xho (24.5).
5. sna, xho, zul transfer well among themselves; Nigerian and East African groups also cluster, credited to geography and syntax.
6. LangRank top-3 features: geographic distance and entity overlap most often; entity overlap vs transfer F1 Spearman R = 0.6 (App. F), 0.49 with an all-token variant. Dataset size was not important.
7. Co-training top-2 sources adds about +3 F1 over the best single source.

Off-diagonal mDeBERTaV3 transfer for our languages, read from Fig. 5 (rounded F1, one model, seeds not stated):

| source \ target | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|
| hau | (87) | 71 | 79 | 79 | 41 |
| kin | 72 | (89) | 81 | 85 | 48 |
| lug | 67 | 69 | (92) | 85 | 41 |
| swa | 70 | 71 | 78 | (95) | 45 |
| zul | 70 | 56 | 62 | 76 | (89) |

- Our arithmetic on this table: hau to the 4 Bantu targets averages 67.5; Bantu to Bantu (12 off-diagonal cells) averages 66.4. Same pattern as our AfroXLMR result (66.3 vs 65.3).

## What we got from it

- Table 4 is the reference for our full fine-tuning replication; hau and zul gaps need explaining (epochs, max length 200, seeds).
- An independent transfer matrix on the same data that already shows "Hausa transfers to Bantu as well as Bantu does" on NER.
- zul is a hard target from all non-Nguni sources (41-56 except swa 76): a target effect, consistent with our finding that the target explains most variance.

## Gaps and limitations

- **Stated by the authors:** news domain only; one task (NER); some families (Khoisan, Austronesian) and central Africa not covered.
- **Our observations:** transfer study uses mDeBERTaV3, not AfroXLMR; no seeds or CIs on the transfer matrix; the capitalization hypothesis is never tested; entity overlap and geography are confounded (same-country news shares names).

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** lang2vec typology features (syntax, phonology, inventory, genetic) were rarely chosen by LangRank; geography and entity overlap won. A direct counterpoint to "typology predicts NER transfer".
- **Low-resource / African language angle:** covers all four of our Bantu languages and Hausa; same dataset as ours.
- **Efficiency / low-cost hardware angle:** none (full fine-tuning only).
- **Baseline or control for us:** **Baseline** (Table 4 numbers; Fig. 5 transfer matrix as an external replication of our NER matrix). **Control to adopt:** entity overlap as a covariate in any RQ2 regression.

## Quotes and figures worth citing

> "This characteristic may limit transfer from languages without this feature as NER models overfit on capitalization" (Sec. 3.2)

- Table 4: in-language baselines incl. AfroXLMR-large.
- Table 6: best and second-best source per target; LangRank features.
- Fig. 5 (App. G): full 26-source x 20-target zero-shot heatmap.

## Related papers to follow up

- [ ] Lin et al. (2019), LangRank, "Choosing transfer languages for cross-lingual learning"
- [ ] Mayhew et al. (2019), capitalization and NER robustness
- [ ] Beukman (2022) overlap analysis (see 2023-beukman-african-ner-transfer.md)

## Open questions / discussion points

- Does lowercasing the input remove the zul penalty from non-Nguni sources? That would test the capitalization claim directly.
- Our hau gap (86.2 vs 87.4): is it epochs (they use 50) or max length?
