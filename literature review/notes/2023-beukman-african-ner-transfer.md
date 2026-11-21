# Analysing Cross-Lingual Transfer in Low-Resourced African Named Entity Recognition

## Reference

| Field | Details |
|---|---|
| **Title** | Analysing Cross-Lingual Transfer in Low-Resourced African Named Entity Recognition |
| **Authors** | Michael Beukman, Manuel Fokam |
| **Year** | 2023 |
| **Venue** | IJCNLP-AACL 2023 (13th IJCNLP and 3rd AACL, Vol. 1: Long Papers), pp. 199-224 |
| **DOI / URL** | https://aclanthology.org/2023.ijcnlp-main.14 |
| **PDF (online)** | [ACL Anthology](https://aclanthology.org/2023.ijcnlp-main.14.pdf) |
| **Code / data** | Code and models released on GitHub (link in paper footnote 1); MasakhaNER 1.0 |

**Citation (APA):**
> Beukman, M., & Fokam, M. (2023). Analysing cross-lingual transfer in low-resourced African named entity recognition. In *Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 199-224). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{beukman-fokam-2023-analysing,
  title     = {Analysing Cross-Lingual Transfer in Low-Resourced {A}frican Named Entity Recognition},
  author    = {Beukman, Michael and Fokam, Manuel},
  booktitle = {Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2023},
  pages     = {199--224},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2023.ijcnlp-main.14}
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
| **Tags** | #NER #transfer #token-overlap #LAFT #amharic #hausa #swahili #kinyarwanda #luganda #low-resource |

## Summary

Zero-shot NER transfer among the ten MasakhaNER 1.0 languages with xlm-roberta-base, with and without language-adaptive fine-tuning (LAFT) on each language, 5 seeds per run. LAFT helps in-language F1 (about +3 on average) but large LAFT corpora reduce transfer from that language (Pearson R = -0.82 between LAFT size and transfer gain). Entity token overlap between source and target datasets correlates with transfer at Pearson R = 0.73, far above any URIEL or geographic feature (best: genetic distance, R = -0.30). Most overlapping entity tokens are "international" English-written names, numbers and places.

## Review claim check

| Claim | Verdict | Evidence |
|---|---|---|
| "data overlap between source and target datasets is a better predictor of transfer than geographical or genetic distance" | **Holds** | Abstract and Table 2: data overlap R = 0.73 vs genetic -0.30, geographic -0.21 (p = 0.05). Authors stress it is correlational: Amharic has zero overlap yet still transfers. |
| "correlation 0.73 between token overlap and transfer" | **Holds** (wording) | Pearson R = 0.73, p = 3.5e-16, off-diagonal pairs, base model (Fig. 2b). It is overlap of entity-labelled tokens (same token, same entity type), counted over train+dev+test, not all tokens. |
| "most overlapping entity tokens are international names (p. 6)" | **Holds** | PDF page 6 (proceedings p. 204): international tokens are about 35% of all entity tokens but about 69% of overlapping ones (28% vs 64% for unique tokens). "International" also includes numbers, punctuation and words like "December". |

## Research question / problem

- How do LAFT and source choice affect zero-shot NER transfer in low-resource African languages, and which features explain transfer?

## Method

- **Approach:** NER fine-tuning on one language, zero-shot evaluation on the other nine; Pearson correlation of transfer F1 with dataset and URIEL features (Lin et al. 2019 feature set).
- **Model(s) / architecture:** xlm-roberta-base; LAFT variants per language.
- **PEFT method (if any):** none.
- **Languages covered:** amh, hau, ibo, kin, lug, luo, pcm, swa, wol, yor.
- **Datasets:** MasakhaNER 1.0; LAFT corpora (42K to 12.6M sentences).
- **Tasks:** NER.
- **Evaluation metrics:** F1 ("begin" repair strategy), mean of 5 seeds.
- **Compute / hardware:** Wits HPC cluster.

## Key findings

1. Data overlap vs transfer F1: R = 0.73; similar when computed on international or local tokens only, and without Amharic (App. C.7).
2. Language features (Table 2): featural -0.00, phonological -0.02, inventory -0.06, syntactic -0.23, genetic -0.30, geographic -0.21; first five not significant.
3. Amharic (Ge'ez script) has no lexical overlap with others but still transfers somewhat, best to swa, hau and pcm.
4. Swahili and Hausa share about 33% of tokens.
5. LAFT on the target helps that target (+5 yor, +7 amh), but LAFT on a large source corpus (notably swa, hau) reduces transfer from it.
6. Seed variance is large in transfer settings.

## What we got from it

- Entity token overlap is the first covariate to control for before claiming typology predicts NER transfer.
- Explains our NER pattern: Hausa sources may do well on Bantu targets via shared international and East/West African entity names, not grammar; Amharic (no overlap, different script) is our one low outlier (54.1).
- Suggests a test: recompute transfer F1 on non-international entities only.

## Gaps and limitations

- **Stated by the authors:** NER only; overlap may be NER-specific; ten languages from one dataset; one model (xlm-roberta-base); results may not hold on lower-quality data.
- **Our observations:** pairs are not independent (each language appears in 18 pairs), so p-values are optimistic; overlap uses train+dev+test of the target; MasakhaNER 1.0 has no Southern Bantu language; no partial correlation of typology controlling for overlap.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** direct evidence that, for NER on African news, URIEL typology explains little once you look at overlap. RQ2 claims on NER need overlap partialled out.
- **Low-resource / African language angle:** covers hau, kin, lug, swa, amh, our older language set.
- **Efficiency / low-cost hardware angle:** LAFT result is relevant to MAFT-style models like AfroXLMR (adapted on many languages, which Beukman notes loses less generality).
- **Baseline or control for us:** **Control to adopt** (entity token overlap as covariate; international vs local split).

## Quotes and figures worth citing

> "the amount of data overlap between the source and target datasets is a better predictor of transfer performance than either the geographical or genetic distance" (p. 199)

- Fig. 2: overlap matrix and correlation plot (R = 0.73).
- Table 2: all feature correlations with p-values.

## Related papers to follow up

- [ ] Lin et al. (2019) LangRank
- [ ] Dolicki & Spanakis (2021), task dependence of transfer features
- [ ] Pfeiffer et al. (2020), source LAFT reduces transfer

## Open questions / discussion points

- Does the 0.73 hold for AfroXLMR-large on MasakhaNER 2.0 and for our LoRA runs?
- Remove international tokens from evaluation: does the Hausa-to-Bantu parity on NER survive?
