# Languages Through the Looking Glass of BPE Compression

## Reference

| Field | Details |
|---|---|
| **Title** | Languages Through the Looking Glass of BPE Compression |
| **Authors** | Ximena Gutierrez-Vasques, Christian Bentz, Tanja Samardžić |
| **Year** | 2023 |
| **Venue** | Computational Linguistics, 49(4), pp. 943-1001 |
| **DOI / URL** | https://doi.org/10.1162/coli_a_00489 |
| **PDF (online)** | [ACL Anthology (open access, CC BY-NC-ND 4.0)](https://aclanthology.org/2023.cl-4.5.pdf) |
| **Code / data** | Language sample: http://www.christianbentz.de/MLC2019_data.html ; Parallel Bible Corpus, JW300, UDHR |

**Citation (APA):**
> Gutierrez-Vasques, X., Bentz, C., & Samardžić, T. (2023). Languages through the looking glass of BPE compression. *Computational Linguistics, 49*(4), 943-1001. https://doi.org/10.1162/coli_a_00489

<details>
<summary>BibTeX</summary>

```bibtex
@article{gutierrez-vasques-etal-2023-languages,
  title   = {Languages Through the Looking Glass of {BPE} Compression},
  author  = {Gutierrez-Vasques, Ximena and Bentz, Christian and Samard{\v{z}}i{\'c}, Tanja},
  journal = {Computational Linguistics},
  volume  = {49},
  number  = {4},
  pages   = {943--1001},
  year    = {2023},
  doi     = {10.1162/coli_a_00489}
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
| **Tags** | #tokenization #BPE #typology #morphology #language-vectors #swahili |

## Summary

Asks whether the first BPE merges reflect a language's morphology. For each of the first 200 merged subwords they measure productivity (number of word types containing it), idiosyncrasy (high frequency in few types) and cumulative frequency, then average to a 3-dimensional vector per language. On 47 languages from the WALS 100-language sample (Parallel Bible Corpus, 1,150 shared verses), richly inflecting languages favour productive subwords early, analytic ones favour idiosyncratic subwords. Agreement with WALS morphology clusters (k-means, k = 4, 15 features) is measured by mean silhouette: 0.12 for BPE vectors vs 0.23 upper bound and -0.17 random. Results are stable on JW300 (25 languages) and UDHR (31).

## Review claim check

- **Claim:** "language vectors from BPE subword statistics across 47 languages that encode typological knowledge induced from raw text".
- **Verdict: holds** (the abstract says this almost verbatim). Two caveats: the vectors are only 3-dimensional and capture a synthetic-to-analytic morphology axis, not typology broadly; and the paper proposes, but does not test, their use for cross-lingual transfer.

## Research question / problem

- Are early BPE subwords linguistically meaningful, and can they characterize a language's morphological type without annotation?

## Method

- **Approach:** subword-nmt BPE per language; productivity, idiosyncrasy, cumulative frequency per merge; average over first 200 merges; standardize; compare with WALS clusters via silhouette coefficient; sweep 1-1,000 merges; WordPiece as alternative.
- **Model(s) / architecture:** none (compression algorithm only).
- **PEFT method (if any):** none.
- **Languages covered:** 47 diverse languages (incl. Swahili, Yoruba, Sango; no other Bantu named in the text I saw).
- **Datasets:** PBC (1.1M tokens), JW300 (4.7M), UDHR (56.1K).
- **Tasks:** typological characterization.
- **Evaluation metrics:** mean silhouette coefficient against WALS-based k-means clusters; random baseline.
- **Compute / hardware:** trivial (CPU).

## Key findings

1. Silhouette (Table 6): WALS own space 0.23; BPE-200 vectors 0.12; random -0.17; BPE-1000 0.13; WordPiece-200 only 0.05.
2. 200 merges are enough; WordPiece merges are less indicative of morphology.
3. Swahili sits near Turkish, Finnish and Russian in BPE space, but in a different WALS cluster, an example of disagreement.
4. Language positions are stable across corpora; UDHR (tiny texts) is noisier.

## What we got from it

- A cheap, annotation-free, interpretable morphological feature we can compute for all our languages from any corpus (e.g. FLORES, the pre-training data, our task data).
- Its weakness is our opportunity: nobody here tests whether the vectors predict transfer.

## Gaps and limitations

- **Stated by the authors:** orthographic word boundaries are hard-coded as delimiters; Hangul and Burmese need special handling; WALS is incomplete and discrete; k = 4 is a judgment call; no gold standard.
- **Our observations:** the silhouette test uses random-label baselines but not the family/area controls of Östling & Kurfalı (2023); 3 dimensions limit what can be encoded; dependence on word boundaries means disjunctive orthographies (Setswana) will look more analytic than they are (links to Meyer & Buys 2024).

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** a ready "typology learned from text" feature for RQ2 that targets morphology, which is what separates Bantu from Hausa.
- **Low-resource / African language angle:** works on tiny parallel corpora; Swahili already in the sample.
- **Efficiency / low-cost hardware angle:** essentially free to compute.
- **Baseline or control for us:** **Baseline feature** (text-derived typology vector to compare against URIEL and model-derived similarity), not a control.

## Quotes and figures worth citing

> "This allows us to have language vectors that encode typological knowledge induced from raw text." (p. 943)

- Table 6: silhouette scores vs random and upper bound.
- Fig. 8: BPE space coloured by WALS clusters.

## Related papers to follow up

- [ ] Gutierrez-Vasques et al. (2021), BPE compression in first merges
- [ ] Bentz et al. (2016), WALS morphology features
- [ ] Pelloni et al. (2022), subword properties for tokenization

## Open questions / discussion points

- Does BPE productivity distance between source and target predict our transfer residuals after controlling for target and token overlap?
- Compute it on AfroXLMR's own SentencePiece segmentation as well as fresh BPE.
