# Subword Segmental Language Modelling for Nguni Languages

## Reference

| Field | Details |
|---|---|
| **Title** | Subword Segmental Language Modelling for Nguni Languages |
| **Authors** | Francois Meyer, Jan Buys |
| **Year** | 2022 |
| **Venue** | Findings of the Association for Computational Linguistics: EMNLP 2022, pp. 6636-6649 |
| **DOI / URL** | https://doi.org/10.18653/v1/2022.findings-emnlp.494 |
| **PDF (online)** | https://aclanthology.org/2022.findings-emnlp.494.pdf |
| **Code / data** | https://github.com/francois-meyer/subword-segmental-lm (code, models, LM datasets) |

**Citation (APA):**
> Meyer, F., & Buys, J. (2022). Subword segmental language modelling for Nguni languages. In *Findings of the Association for Computational Linguistics: EMNLP 2022* (pp. 6636-6649). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.findings-emnlp.494

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{meyer2022subword,
  title     = {Subword Segmental Language Modelling for {N}guni Languages},
  author    = {Meyer, Francois and Buys, Jan},
  year      = {2022},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2022},
  pages     = {6636--6649},
  doi       = {10.18653/v1/2022.findings-emnlp.494}
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
| **Tags** | #segmentation #morphology #zulu #xhosa #nguni #language-modelling #unsupervised |

## Summary

Proposes a subword segmental language model (SSLM) that learns to segment words while being trained as an autoregressive LM: a character-level LSTM encodes history and a mixture of a lexicon model and a character model generates each segment, with segmentation marginalised by dynamic programming. Trained from scratch on curated corpora for isiXhosa, isiZulu, isiNdebele and Siswati. SSLM gets the best average bits-per-character, slightly ahead of BPE and ULM LMs, and its segmentations (especially a word-level variant) beat BPE, ULM and Morfessor on unsupervised morphological segmentation against the NCHLT gold.

## Review claim check

- **Claim:** "gains from morphology-aware segmentation, but pretrained from scratch with it".
- **Verdict:** partly holds.
- **Evidence:** the models are indeed trained from scratch (LSTM LMs, no pretrained encoder). But the segmentation is learned, not morphology-supervised, and the "gains" are small intrinsic BPC gains (test average 1.28 vs 1.30 for BPE-LSTM), not downstream-task gains; no NER/POS is evaluated.

## Research question / problem

- Can learning segmentation jointly with language modelling give better LMs and more morpheme-like subwords for agglutinative, conjunctively written Nguni languages?

## Method

- **Approach:** segmental LM with lexicon/character mixture, Viterbi decoding for segmentation; also word-level segmental models trained on isolated words.
- **Model(s) / architecture:** char-LSTM encoder; baselines: char/BPE/ULM with LSTM and Transformer LMs.
- **PEFT method (if any):** none.
- **Languages covered:** isiXhosa, isiZulu, isiNdebele, Siswati.
- **Datasets:** compiled LM corpora (released); NCHLT annotated data for segmentation evaluation.
- **Tasks:** language modelling; unsupervised morphological segmentation.
- **Evaluation metrics:** BPC; morpheme identification and morpheme boundary identification P/R/F1.
- **Compute / hardware:** CHPC cluster; not detailed in what we read.

## Key findings

Test BPC (Table 2):

| Model | xh | zu | nr | ss | avg |
|---|---|---|---|---|---|
| BPE-LSTM | 1.30 | 1.22 | 1.39 | 1.28 | 1.30 |
| ULM-LSTM | 1.25 | 1.27 | 1.39 | 1.31 | 1.31 |
| BPE-Transformer | 1.33 | 1.27 | 1.36 | 1.30 | 1.31 |
| SSLM | 1.27 | 1.21 | 1.35 | 1.28 | 1.28 |

1. SSLM is best on average, but by 0.02 BPC; it is not best on isiXhosa.
2. Word-level segmental models are the best unsupervised segmenters; Morfessor is the weakest of all segmenters on these data (Morfessor trained on a 10k-token subset worked best).

## What we got from it

- Another data point that Morfessor segmentation is poor for Nguni languages, which fits our 0.51 precision.
- Released Nguni LM corpora and an unsupervised segmenter that beats Morfessor, usable if we need a non-supervised alternative for isiZulu.

## Gaps and limitations

- **Stated by the authors:** one language group only; datasets web-sourced with possible noise.
- **Our observations:**
  - No downstream tasks and no pretrained transformers.
  - BPC differences are small; no significance testing reported.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** supports learned, LM-driven segmentation over Morfessor for Nguni.
- **Our results:** does not speak to injecting segmentation into a frozen pretrained encoder; it only confirms that Morfessor is a weak segmenter for isiZulu, a likely cause of our drops.
- **Low-resource / African language angle:** directly isiZulu and its relatives.
- **Efficiency / low-cost hardware angle:** small LSTMs.
- **Baseline for us?** No (possible alternative segmenter for isiZulu if the CRF is not available).

## Quotes and figures worth citing

> "We propose a subword segmental language model (SSLM) that learns how to segment words while being trained for autoregressive language modelling." (p. 6636)

- Table 2: BPC. Tables 4-5: segmentation metrics (garbled in our text extraction; read from the PDF before citing numbers).

## Related papers to follow up

- [ ] Moeng et al. (2021), supervised Nguni segmentation.
- [ ] Kawakami et al. (2019), segmental LMs.
- [ ] Mzamo et al. (2019), entropy-based isiXhosa segmentation.

## Open questions / discussion points

- Would SSLM segments, used as inner-word cuts on AfroXLMR, behave better than Morfessor cuts?
