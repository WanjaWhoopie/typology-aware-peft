# Language Embeddings Sometimes Contain Typological Generalizations

## Reference

| Field | Details |
|---|---|
| **Title** | Language Embeddings Sometimes Contain Typological Generalizations |
| **Authors** | Robert Östling, Murathan Kurfalı |
| **Year** | 2023 |
| **Venue** | Computational Linguistics, 49(4), pp. 1003-1051 |
| **DOI / URL** | https://doi.org/10.1162/coli_a_00491 |
| **PDF (online)** | [ACL Anthology (open access, CC BY-NC-ND 4.0)](https://aclanthology.org/2023.cl-4.6.pdf) ; [arXiv 2301.08115](https://arxiv.org/abs/2301.08115) |
| **Code / data** | https://github.com/robertostling/parallel-text-typology ; data on Zenodo (Östling & Kurfalı 2023) |

**Citation (APA):**
> Östling, R., & Kurfalı, M. (2023). Language embeddings sometimes contain typological generalizations. *Computational Linguistics, 49*(4), 1003-1051. https://doi.org/10.1162/coli_a_00491

<details>
<summary>BibTeX</summary>

```bibtex
@article{ostling-kurfali-2023-language,
  title   = {Language Embeddings Sometimes Contain Typological Generalizations},
  author  = {{\"O}stling, Robert and Kurfal{\i}, Murathan},
  journal = {Computational Linguistics},
  volume  = {49},
  number  = {4},
  pages   = {1003--1051},
  year    = {2023},
  doi     = {10.1162/coli_a_00491}
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
| **Tags** | #typology #language-embeddings #evaluation #probing #controls #XLM-R #parallel-text |

## Summary

Trains many multilingual models (word LM, character LM, reinflection, word encoder, NMT) on Bible translations in 1,295 languages and asks whether the learned language embeddings encode typological features (word order, affixation). Uses a strict evaluation: logistic regression probes with leave-one-out training folds that exclude same-family, same-macro-area and potential contact languages, family-balanced Monte Carlo sampling, shuffled-label baselines, and lexical-only baseline embeddings. Only the word-level LM (word order features) and reinflection models (prefixing vs suffixing) show clear typological signal. Embeddings from prior work (Malaviya et al. 2017; Östling & Tiedemann 2017) and mBERT/XLM-R mostly do not; naive cross-validation produces false positives, especially for lexical and character-LM embeddings.

## Review claim check

- **Claim:** "most learned language embeddings do not make linguistically meaningful generalizations; careful evaluation is essential to avoid false positives".
- **Verdict: holds.** Abstract (p. 1003) states both points; Sec. 8.3 and 8.5 show naive cross-validation inflates results. Nuance: "most" refers to their 12 sets of representations; the WordLM and reinflection models do encode some features, and mBERT/XLM-R pass for one feature (numeral-noun order).

## Research question / problem

- Which typological features are discovered by neural models with language embeddings, and how accurately can features be predicted without using information from related or nearby languages?

## Method

- **Approach:** build embeddings; probe each binary typological feature with L2-regularized logistic regression under linguistically sound cross-validation.
- **Model(s) / architecture:** WordLM, CharLM, Reinflect-Noun/Verb, Encoder, NMT x2eng / eng2x; prior embeddings (MTVec, MTCell, Ö&T); mBERT, XLM-R base and large (mean-pooled last layer over Bible verses); lexical baselines ASJP and LEXICAL.
- **PEFT method (if any):** none.
- **Languages covered:** 1,295 languages (Bible corpus); evaluation limited to features covering at least 50 families.
- **Datasets:** Parallel Bible Corpus; URIEL (WALS, Ethnologue) as gold; projected word order features via annotation projection.
- **Tasks:** typological feature prediction (8 word order, 7 morphology features).
- **Evaluation metrics:** family-weighted F1 (mean of both classes).
- **Compute / hardware:** Swedish national HPC (SNIC).

## Evaluation controls (to adopt)

| Control | What they do | Why |
|---|---|---|
| Independence filter | Training fold excludes languages sharing top-level Glottolog family, same Glottolog macro-area, or listed as potential contact languages (Grossman et al. 2020) | Stops genealogical, areal and global-contact (e.g. English, Arabic) leakage |
| Family-wise Monte Carlo | Each sample: one test language per family; for each, a training fold of one independent language per family; 201 samples in Sec. 3.2, 401 in Sec. 7.2 (text gives both) | Equal weight per family; gives uncertainty |
| Shuffled-label baseline | Same classifier and data with shuffled training labels, paired per sample; check it behaves like binomial p = 0.5 | Empirical chance level; it caught their under-regularization bug |
| Lexical-only baselines | ASJP and Bible word-list embeddings that cannot encode structure | If these pass, the test is leaking relatedness |
| Strong regularization | Fixed C = 1e-3, features standardized; binary classes weighted equally | Small samples otherwise give chance effects from minority classes |
| Minimum sample | Skip features with fewer than 50 families | Data sparsity |
| Projection ceiling | Compare with F1 of hand-crafted projected labels vs URIEL | Upper reference |
| Correlated-feature check | Test all other features; report when a correlated feature explains the result equally well (within 3 points) | Avoid crediting the wrong feature |
| Naive CV contrast | Report naive CV too, to show inflation | Demonstrates false positives |
| Clean gold labels | Keep only URIEL entries with exactly one of a set of mutually exclusive values | URIEL binarization creates contradictions |

## Key findings

1. Clear detections: object-verb, adposition-noun, numeral-noun order (WordLM); prefixing vs suffixing (reinflection models).
2. mBERT, XLM-R base and XLM-R large: numeral-noun order only.
3. Most other embeddings, including previously published ones, are at shuffled-label level.
4. Under naive CV, ASJP, LEXICAL and character LMs look much better, showing they encode lexical similarity, which correlates with typology through relatedness.
5. Similarity of embeddings reproducing family trees does not show typological generalization.

## What we got from it

- A ready protocol for testing whether any "typology learned from text" vector really encodes typology, before using it in RQ2.
- A warning that agreement with family trees (what Yu et al. 2021 and Entropy2Vec report) is not evidence of typology.

## Gaps and limitations

- **Stated by the authors:** only binary features; set-up unsuitable for samples much smaller than about a thousand languages; features may be encoded non-linearly; Bible domain.
- **Our observations:** the protocol cannot be run on 4-6 languages. For us it must be applied to the vectors on a large language sample (e.g. all FLORES/SIB-200 languages), and only then used for our pairs.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** central to RQ2's validity; shows XLM-R-family representations carry little linearly decodable typology.
- **Low-resource / African language angle:** includes African languages in the Bible corpus; macro-area exclusion means African test languages are probed with non-African training languages.
- **Efficiency / low-cost hardware angle:** probes are cheap logistic regressions.
- **Baseline or control for us:** **Evaluation control** (adopt the full table above); ASJP/LEXICAL as negative baselines.

## Quotes and figures worth citing

> "Careful attention to details in the evaluation turns out to be essential to avoid false positives." (p. 1003)

- Fig. 1 vs Fig. 8: sound vs naive cross-validation for the same features.
- Table 3: 3-way confusion matrices (URIEL, projected, predicted).

## Related papers to follow up

- [ ] Malaviya, Neubig & Littell (2017), language vectors from NMT
- [ ] Bjerva & Augenstein (2018), typology from language embeddings
- [ ] Grossman et al. (2020), phoneme inventory borrowing (contact data)

## Open questions / discussion points

- Can we run their released software on AfroXLMR-large mean-pooled FLORES vectors and our BPE productivity vectors before RQ2?
