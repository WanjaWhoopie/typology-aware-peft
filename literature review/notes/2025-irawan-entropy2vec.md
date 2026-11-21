# Entropy2Vec: Crosslingual Language Modeling Entropy as End-to-End Learnable Language Representations

## Reference

| Field | Details |
|---|---|
| **Title** | Entropy2Vec: Crosslingual Language Modeling Entropy as End-to-End Learnable Language Representations |
| **Authors** | Patrick Amadeus Irawan, Ryandito Diandaru, Belati Jagad Bintang Syuhada, Randy Zakya Suchrady, Alham Fikri Aji, Genta Indra Winata, Fajri Koto, Samuel Cahyawijaya |
| **Year** | 2025 |
| **Venue** | Proceedings of the 5th Workshop on Multilingual Representation Learning (MRL 2025), Suzhou, pp. 426-437 (per ACL Anthology page); arXiv preprint 2509.05060 |
| **DOI / URL** | https://doi.org/10.18653/v1/2025.mrl-main.29 |
| **PDF (online)** | [arXiv 2509.05060](https://arxiv.org/pdf/2509.05060) (read: v1) |
| **Code / data** | Glot500-c corpus; LinguAlchemy framework |

**Citation (APA):**
> Irawan, P. A., Diandaru, R., Syuhada, B. J. B., Suchrady, R. Z., Aji, A. F., Winata, G. I., Koto, F., & Cahyawijaya, S. (2025). Entropy2Vec: Crosslingual language modeling entropy as end-to-end learnable language representations. In *Proceedings of the 5th Workshop on Multilingual Representation Learning (MRL 2025)* (pp. 426-437). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.mrl-main.29

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{irawan-etal-2025-entropy2vec,
  title     = {{E}ntropy2{V}ec: Crosslingual Language Modeling Entropy as End-to-End Learnable Language Representations},
  author    = {Irawan, Patrick Amadeus and Diandaru, Ryandito and Syuhada, Belati Jagad Bintang and Suchrady, Randy Zakya and Aji, Alham Fikri and Winata, Genta Indra and Koto, Fajri and Cahyawijaya, Samuel},
  booktitle = {Proceedings of the 5th Workshop on Multilingual Representation Learning (MRL 2025)},
  year      = {2025},
  pages     = {426--437},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2025.mrl-main.29}
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
| **Tags** | #typology #language-vectors #perplexity #SIB-200 #URIEL #XLM-R |

## Summary

Trains a small GPT-2 (4 layers, 512 dims) separately on each of 33 languages from Glot500-c (up to 1M sentences each). A language's vector is the average cross-entropy of its LM on every other language's test data, so the vector has one dimension per language. Trees from these vectors (DBSCAN) are compared with Glottolog using Robinson-Foulds and LCA distance, and are about as close as URIEL/URIEL+ trees. As a regularizer in LinguAlchemy, the vectors give SIB-200 and MASSIVE accuracy close to URIEL+ with XLM-R and similar to baselines with mBERT.

## Review claim check

- **Claim:** "language vectors from LM entropy". Venue?
- **Verdict: holds.** The vector is the per-language cross-entropy of monolingual LMs (Sec. 3.2). Venue: arXiv 2509.05060 (Sep 2025), published at the MRL 2025 workshop (ACL Anthology 2025.mrl-main.29, pp. 426-437), a workshop paper, not a main-conference paper.

## Research question / problem

- Can language vectors be built without hand-curated typology, dense and with no missing values, and still align with typology and help multilingual tasks?

## Method

- **Approach:** monolingual LM per language; cross-lingual perplexity matrix as language vectors; DBSCAN trees; LinguAlchemy regularization for downstream tasks.
- **Model(s) / architecture:** GPT-2 small config (4 layers); downstream XLM-R and mBERT.
- **PEFT method (if any):** none (LinguAlchemy regularization of full fine-tuning).
- **Languages covered:** 33 (mostly Austronesian and Indo-European; e.g. eng, vie, ind, tha, tam, mya, jav, sun, tgl, deu, fra, hin, spa). No African language in the tables I saw.
- **Datasets:** Glot500-c; SIB-200 and MASSIVE (seen vs unseen splits).
- **Tasks:** tree reconstruction; topic classification (SIB-200); intent classification (MASSIVE).
- **Evaluation metrics:** RF distance, LCA MAE; accuracy.
- **Compute / hardware:** small LMs; details in their appendix.

## Key findings

1. Tree vs Glottolog (Table 1): Entropy2Vec LCA MAE 11.15 and RF 13.0, comparable to URIEL/URIEL+ trees.
2. XLM-R + LinguAlchemy, SIB-200 average (text): Entropy2Vec 81.3 vs URIEL+ 81.5 (best baseline), URIEL Geo 78.5, URIEL Syntax 78.1.
3. mBERT: no clear gain from Entropy2Vec alone; concatenation with URIEL helps mBERT but not XLM-R.
4. Concatenating vectors is inconsistent (gains on one metric, losses on the other).

## What we got from it

- A second cheap text-derived similarity (cross-lingual LM surprise) that can be computed for our six languages with small LMs.
- It uses SIB-200, one of our tasks.

## Gaps and limitations

- **Stated by the authors:** quality depends on monolingual corpus size and quality; entropy may miss less predictable linguistic aspects; script/encoding drives clustering (Thai and Lao split early despite shared ancestry); only a 33-language prototype.
- **Our observations:** "typology" evaluation is tree agreement with Glottolog, which Östling & Kurfalı (2023) argue shows relatedness, not typological generalization; vectors mix lexical overlap, script and domain into one number per pair; no significance tests or seeds shown; table columns did not extract cleanly, so I used the numbers given in the text; vector dimension grows with the number of languages.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** a model-free but data-driven similarity; probably dominated by lexical and orthographic overlap rather than morphology. Needs Östling-style controls before being called typology.
- **Low-resource / African language angle:** none in the paper; easy to extend to our languages.
- **Efficiency / low-cost hardware angle:** small LMs, cheap.
- **Baseline or control for us:** **Candidate baseline** similarity measure for RQ2 (alongside URIEL, BPE productivity and model-embedding similarity).

## Quotes and figures worth citing

> "Low entropy indicates high similarity, while high entropy suggests greater divergence." (Abstract)

- Table 1: tree distances vs Glottolog.
- Table 3/4: SIB-200 and MASSIVE results with different vectors.

## Related papers to follow up

- [ ] Adilazuarda et al. (2024), LinguAlchemy
- [ ] Khan et al. (2025), URIEL+

## Open questions / discussion points

- Is cross-lingual perplexity between our languages mostly explained by subword overlap? Check correlation with token overlap first.
