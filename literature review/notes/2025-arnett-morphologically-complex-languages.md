# Why do language models perform worse for morphologically complex languages?

## Reference

| Field | Details |
|---|---|
| **Title** | Why do language models perform worse for morphologically complex languages? |
| **Authors** | Catherine Arnett, Benjamin K. Bergen |
| **Year** | 2025 |
| **Venue** | Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025), pp. 6607-6623 |
| **DOI / URL** | https://aclanthology.org/2025.coling-main.441 |
| **PDF (online)** | https://aclanthology.org/2025.coling-main.441.pdf |
| **Code / data** | OSF: https://osf.io/jukzd/ (MorphScore datasets for 22 languages) |

**Citation (APA):**
> Arnett, C., & Bergen, B. K. (2025). Why do language models perform worse for morphologically complex languages? In *Proceedings of the 31st International Conference on Computational Linguistics* (pp. 6607-6623). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{arnett2025why,
  title     = {Why do language models perform worse for morphologically complex languages?},
  author    = {Arnett, Catherine and Bergen, Benjamin K.},
  year      = {2025},
  booktitle = {Proceedings of the 31st International Conference on Computational Linguistics},
  pages     = {6607--6623},
  url       = {https://aclanthology.org/2025.coling-main.441}
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
| **Tags** | #morphology #tokenization #typology #MorphScore #byte-premium #zulu |

## Summary

Replicates a performance gap where agglutinative languages get worse LM scores than fusional ones, across older and newer multilingual models and 1,989 monolingual models. Tests three explanations: tokenizers are less morphologically aligned for agglutinative languages (introducing MorphScore, 22 languages), tokenization quality (compression, Rényi entropy) is worse, or dataset size is measured unfairly across languages. MorphScore is actually higher for agglutinative languages and does not explain the gap; tokenization quality explains some; scaling training data by the byte premium makes the gap largely disappear.

## Review claim check

- **Claim:** "some evidence that tokenization quality explains the performance gap, but none for the role of morphological alignment".
- **Verdict:** holds.
- **Evidence:** the abstract states this almost word for word (p. 6607). Agglutinative MorphScore mean 66.3% vs fusional 53.3% (p = .008), the opposite of the alignment hypothesis.

## Research question / problem

- Why do agglutinative languages show worse language-modelling performance, and is tokenizer misalignment with morphemes the cause?

## Method

- **Approach:** regression/ANOVA of performance on morphological type with controls; MorphScore (share of words where a token boundary falls on the annotated morpheme boundary, one boundary per word); compression (corpus token count on FLORES) and Rényi entropy; Goldfish models trained with byte-premium-scaled data.
- **Model(s) / architecture:** XGLM, BLOOM, mT0, MaLA, LLaMA2; Chang et al. (2023) monolingual models; Goldfish models.
- **PEFT method (if any):** none.
- **Languages covered:** MorphScore: 22 languages including Zulu (UniMorph data); performance analyses over many more.
- **Datasets:** UD and UniMorph for MorphScore; FLORES; benchmark scores from prior work.
- **Tasks:** perplexity and existing benchmark scores (no new fine-tuning).
- **Evaluation metrics:** MorphScore, corpus token count, Rényi entropy, perplexity.
- **Compute / hardware:** analysis-level; no training except reuse of existing models.

## Key findings

1. Agglutinative languages have higher, not lower, MorphScore; alignment does not correlate with performance.
2. Agglutinative languages compress worse; tokenization quality explains part of the gap.
3. Once data are scaled by byte premium (Goldfish), the agglutinative vs fusional difference is not significant.
4. Zulu MorphScore with the monolingual SentencePiece tokenizer: 0.541 (Table 3).

## What we got from it

- A metric (MorphScore) and a Zulu dataset to score our tokenizers (AfroXLMR, Serengeti, Morfessor-constrained).
- A strong counter-hypothesis to "morphology misalignment hurts": data size and encoding efficiency may matter more.

## Gaps and limitations

- **Stated by the authors:** marginal significance of the byte-premium difference; limited sample of languages.
- **Our observations:**
  - Monolingual and multilingual decoder LMs and perplexity; nothing on fine-tuned encoders or token-level tasks like NER/POS.
  - MorphScore uses a single boundary per word, which is thin for Bantu words with many morphemes.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** directly challenges the premise of RQ1. Our negative results (Morfessor input hurts) are consistent with it.
- **Low-resource / African language angle:** Zulu is one of the 22 languages; no other Bantu.
- **Efficiency / low-cost hardware angle:** none.
- **Our results:** use as framing: "morphological alignment" may not be the lever; if supervised cuts and scrambled cuts perform the same, this paper is the main citation.
- **Baseline for us?** No; use MorphScore as a diagnostic metric.

## Quotes and figures worth citing

> "We find some evidence that tokenization quality explains the performance gap, but none for the role of morphological alignment." (p. 6607)

- Table 3 (appendix): MorphScore per language (Zulu 0.541).

## Related papers to follow up

- [ ] Arnett et al. (2024), byte premium.
- [ ] Gerz et al. (2018), typology and LM difficulty.
- [ ] Arnett, Hudspeth and O'Connor (2025), MorphScore in 70 languages.

## Open questions / discussion points

- Does the same null hold for fine-tuned token-level tasks, where word boundaries and readout matter (see Antall and Saha 2026)?
