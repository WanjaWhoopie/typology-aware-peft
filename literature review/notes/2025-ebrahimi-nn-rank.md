# Model-Based Ranking of Source Languages for Zero-Shot Cross-Lingual Transfer

## Reference

| Field | Details |
|---|---|
| **Title** | Model-Based Ranking of Source Languages for Zero-Shot Cross-Lingual Transfer |
| **Authors** | Abteen Ebrahimi, Adam Wiemerslage, Katharina von der Wense |
| **Year** | 2025 |
| **Venue** | EMNLP 2025 (Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing), pp. 32405-32450 |
| **DOI / URL** | https://aclanthology.org/2025.emnlp-main.1650 |
| **PDF (online)** | [ACL Anthology](https://aclanthology.org/2025.emnlp-main.1650.pdf) |
| **Code / data** | UD, WikiANN, JHU Bible Corpus (code link not checked) |

**Citation (APA):**
> Ebrahimi, A., Wiemerslage, A., & von der Wense, K. (2025). Model-based ranking of source languages for zero-shot cross-lingual transfer. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 32405-32450). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{ebrahimi-etal-2025-model,
  title     = {Model-Based Ranking of Source Languages for Zero-Shot Cross-Lingual Transfer},
  author    = {Ebrahimi, Abteen and Wiemerslage, Adam and von der Wense, Katharina},
  booktitle = {Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing},
  year      = {2025},
  pages     = {32405--32450},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2025.emnlp-main.1650}
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
| **Tags** | #transfer #source-selection #ranking #LangRank #NER #POS #XLM-R #mBERT |

## Summary

NN-Rank ranks source datasets for a target by encoding unlabeled target text and all source training text with a multilingual model (layer 8), finding the 5 nearest source subwords for every target subword (FAISS), and counting how often each source dataset appears. Tested on POS (UD) and NER (WikiANN) with mBERT and XLM-R base as task models, 51 source languages, 56 POS and 72 NER targets. It beats LangRank by large NDCG@5 margins (up to 35.56 POS, 18.14 NER) with in-domain data, stays competitive using only Bible text, and needs as few as 25 target examples for about 93% of full NDCG.

## Review claim check

- **Claim:** "ranks sources from model representations over 51 source languages; the baseline to beat".
- **Verdict: partly holds.** 51 source languages and model-representation ranking are correct (Sec. 4). "The baseline to beat" is our reviewer's judgment: it beats LangRank in their setting, but it ranks a large pool (25-78 source datasets) by NDCG@5 and is weaker for poorly represented targets and with domain mismatch on NER. With our 3-5 candidate sources per target, NDCG@5 is not meaningful.

## Research question / problem

- Static lexical and typological features ignore the model; can a model's own hidden representations rank source languages better?

## Method

- **Approach:** subword-level kNN voting from target to pooled source representations; rank by tally.
- **Model(s) / architecture:** mBERT and XLM-R base (as encoder and as task models); LangRank (pretrained) and re-trained N-LangRank as baselines.
- **PEFT method (if any):** none.
- **Languages covered:** 51 source languages for each task; 56 POS and 72 NER targets; up to 13 families, majority Indo-European. African targets in NER test-all include amh, ibo, kin, som, yor, afr; I saw no Swahili.
- **Datasets:** UD (POS, multiple treebanks per language), WikiANN (NER), JHU Bible Corpus.
- **Tasks:** POS, NER.
- **Evaluation metrics:** NDCG@5 (relevance from gold ranking, max = 10), average accuracy/F1 of top-5 sources.
- **Compute / hardware:** GPU needed for encoding (LangRank does not need one, as they note).

## Key findings

1. NN-Rank beats LangRank on NDCG in all main settings. First block of Table 2 (train-large sources, test-all targets, mBERT task model): POS NDCG@5 62.91 (NN-Rank-mBERT) vs 36.47 (LangRank); NER 47.94 vs 28.55. Average accuracy/F1 of top-5 sources differs less (POS 74.59 vs 70.60; NER 60.77 vs 57.48). The PDF table extracted with broken alignment, so check other blocks against the PDF.
2. mBERT representations rank better than XLM-R, even when XLM-R is the task model (Wikipedia-only pre-training suggested as a reason).
3. Layer 8 beats layer 0 (embedding layer, closest to lexical overlap) almost always.
4. Ranking quality drops for targets the model represents poorly (Fig. 1); LangRank is flat across representation quality.
5. With Bible-only data, NN-Rank still beats LangRank on NDCG for NER; with domain mismatch on NER, LangRank wins on average F1.

## What we got from it

- The strongest model-based ranking method; useful as a baseline only if we expand the source pool (e.g. all 20 MasakhaNER 2.0 languages).
- The layer-8 vs layer-0 ablation is a neat way to separate lexical from deeper similarity.

## Gaps and limitations

- **Stated by the authors:** encoder-only models; single-source transfer; target-data ablations sample tokens unrealistically; quality depends on target representations, so not reliable for languages outside pre-training.
- **Our observations:** base models only; WikiANN NER is noisy (silver data) and Wikipedia-domain; Indo-European heavy; no Bantu-focused analysis; NN-Rank is a black box: it predicts but does not explain transfer, so it does not answer "does typology predict transfer".

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** argues against static typology features for source selection; a direct challenge to RQ2's premise if RQ2 is framed as prediction.
- **Low-resource / African language angle:** a few African NER targets only.
- **Efficiency / low-cost hardware angle:** needs only unlabeled target text (25+ examples) and one forward pass per source.
- **Baseline or control for us:** **Baseline** for prediction, applicable only with a larger source pool; otherwise cite as the model-based alternative.

## Quotes and figures worth citing

> "this is qualified with the assumption that the representations are strong" (p. 32414)

- Table 2: NN-Rank vs LangRank (NDCG@5, Acc@5, F1@5).
- Fig. 1: NDCG by target representation quality.
- Table 5: layer 8 vs layer 0 ablation.

## Related papers to follow up

- [ ] Lin et al. (2019), LangRank
- [ ] Rice et al. (2025), LangRank for multilingual models (POS)
- [ ] Dou & Neubig (2021), word alignment from middle layers

## Open questions / discussion points

- Run NN-Rank with AfroXLMR-large over the 20 MasakhaNER 2.0 languages to rank sources for our four Bantu targets; compare with typology-based ranking by top-3 selection loss.
