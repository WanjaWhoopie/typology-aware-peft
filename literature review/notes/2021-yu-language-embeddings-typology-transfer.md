# Language Embeddings for Typology and Cross-lingual Transfer Learning

## Reference

| Field | Details |
|---|---|
| **Title** | Language Embeddings for Typology and Cross-lingual Transfer Learning |
| **Authors** | Dian Yu, Taiqi He, Kenji Sagae |
| **Year** | 2021 |
| **Venue** | ACL-IJCNLP 2021 (59th Annual Meeting of the ACL and 11th IJCNLP, Vol. 1: Long Papers), pp. 7210-7225 |
| **DOI / URL** | https://aclanthology.org/2021.acl-long.560 |
| **PDF (online)** | [ACL Anthology](https://aclanthology.org/2021.acl-long.560.pdf) |
| **Code / data** | https://github.com/DianDYu/language_embeddings |

**Citation (APA):**
> Yu, D., He, T., & Sagae, K. (2021). Language embeddings for typology and cross-lingual transfer learning. In *Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)* (pp. 7210-7225). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{yu-etal-2021-language,
  title     = {Language Embeddings for Typology and Cross-lingual Transfer Learning},
  author    = {Yu, Dian and He, Taiqi and Sagae, Kenji},
  booktitle = {Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)},
  year      = {2021},
  pages     = {7210--7225},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2021.acl-long.560}
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
| **Tags** | #typology #language-embeddings #WALS #transfer #parsing #XNLI #XLM-R |

## Summary

Learns 50-dimensional language embeddings for 29 languages (10 genera, mostly European) from monolingual CommonCrawl text with a denoising autoencoder: an LSTM seq2seq model restores shuffled sentences, with MUSE-aligned word vectors and a language code. Embeddings recover genera (adjusted Rand 0.58) and predict WALS features above majority and random baselines with leave-one-language-out CV. Concatenating the embeddings into a zero-shot parser improves average UAS from 64.61 to 68.01 over random embeddings across 16 UD languages; adding them to XLM/XLM-R gives small XNLI gains (+0.6 average for XLM-R large).

## Review claim check

- **Claim:** "learn language embeddings from text and test them on WALS and zero-shot transfer".
- **Verdict: holds.** Abstract and Sec. 4-5. Note that "zero-shot transfer" here means feeding the embedding into a model as an extra input; it does not predict or rank which source transfers best, so it is a different question from our RQ2.

## Research question / problem

- Can language representations learned from plain monolingual text (no parallel data, no typology) capture typology and help zero-shot cross-lingual tasks?

## Method

- **Approach:** denoising autoencoder (word reordering) with a language embedding concatenated to each token; decoder-side language embeddings used.
- **Model(s) / architecture:** LSTM seq2seq; downstream biaffine parser (frozen MUSE embeddings); XLM, XLM-R base and large for XNLI.
- **PEFT method (if any):** none (embedding injected through a learned linear projection).
- **Languages covered:** 29 (English, French, Romanian, Arabic, German, Russian, Bulgarian, Greek, Slovak, Catalan, Hebrew, Slovene, Croatian, Hungarian, Spanish, Czech, Indonesian, Swedish, Danish, Italian, Turkish, Dutch, Norwegian, Ukrainian, Estonian, Polish, Vietnamese, Finnish, Portuguese). No African language.
- **Datasets:** CoNLL 2017 CommonCrawl (200K sentences per language), Wikipedia; UD v2.6; XNLI.
- **Tasks:** WALS prediction, genus clustering, zero-shot dependency parsing, zero-shot XNLI.
- **Evaluation metrics:** accuracy, adjusted Rand index, UAS, XNLI accuracy (3 seeds).
- **Compute / hardware:** not emphasized.

## Key findings

1. WALS prediction (26 shared languages, Table 1), Eng. embeddings: lexicon 0.87, syntax 0.81, partially morphological 0.71, vs majority 0.64 / 0.75 / 0.69. "Non-learnable" (phonology, morphology) features stay at majority level.
2. Genus clustering: adjusted Rand 0.58 vs much lower for Malaviya et al. (2017) embeddings.
3. Zero-shot parsing: average UAS 64.61 (random embedding) to 68.01 (language embedding); big gains for Romance (+7.32 to +10.62), drop for Hebrew (-8.21).
4. XNLI: +1.1 average for XLM (English dev selection); +0.5 XLM-R base, +0.6 XLM-R large (averaged dev selection).

## What we got from it

- A precedent for "typology from text, then used in transfer"; the embedding can be added to a model, which links to typology-aware PEFT (e.g. conditioning LoRA on a language vector).
- Shows the effect on strong models (XLM-R large) is small.

## Gaps and limitations

- **Stated by the authors:** depends on MUSE-aligned embeddings (limits languages); mapping to English is noisy.
- **Our observations:** WALS CV is plain leave-one-language-out with no family or area exclusion, exactly the set-up Östling & Kurfalı (2023) show inflates results; only 29 mostly European languages; genus recovery is not typology; no African or Bantu language; morphology essentially not captured.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** their method captures word order, not morphology, so it is a poor fit for Bantu vs Hausa contrasts.
- **Low-resource / African language angle:** none.
- **Efficiency / low-cost hardware angle:** small LSTM; cheap.
- **Baseline or control for us:** **Possible baseline** for "language vector injected into the model"; not a transfer-prediction baseline. Re-evaluate any such vector with Östling-style controls.

## Quotes and figures worth citing

> "language representations that capture relationships among languages can be learned and subsequently leveraged in cross-lingual tasks without the use of parallel data" (p. 7210)

- Table 1: WALS prediction by feature category.
- Table 3: XNLI with and without language embeddings.

## Related papers to follow up

- [ ] Malaviya et al. (2017)
- [ ] K et al. (2020), structural similarity in multilingual BERT
- [ ] Bjerva et al. (2019), typology from translations

## Open questions / discussion points

- Would a LoRA conditioned on a typology vector (rather than on language identity) help unseen Bantu targets more than a plain shared LoRA?
