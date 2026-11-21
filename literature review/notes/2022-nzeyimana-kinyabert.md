# KinyaBERT: a Morphology-aware Kinyarwanda Language Model

## Reference

| Field | Details |
|---|---|
| **Title** | KinyaBERT: a Morphology-aware Kinyarwanda Language Model |
| **Authors** | Antoine Nzeyimana, Andre Niyongabo Rubungo |
| **Year** | 2022 |
| **Venue** | Proceedings of the 60th Annual Meeting of the ACL (Volume 1: Long Papers), pp. 5347-5363 |
| **DOI / URL** | https://doi.org/10.18653/v1/2022.acl-long.367 |
| **PDF (online)** | https://aclanthology.org/2022.acl-long.367.pdf |
| **Code / data** | https://github.com/anzeyimana/kinyabert-acl2022 (code and data; the morphological analyser itself is described as closed source) |

**Citation (APA):**
> Nzeyimana, A., & Niyongabo Rubungo, A. (2022). KinyaBERT: A morphology-aware Kinyarwanda language model. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 5347-5363). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.acl-long.367

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{nzeyimana2022kinyabert,
  title     = {{KinyaBERT}: a Morphology-aware {K}inyarwanda Language Model},
  author    = {Nzeyimana, Antoine and Niyongabo Rubungo, Andre},
  year      = {2022},
  booktitle = {Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages     = {5347--5363},
  doi       = {10.18653/v1/2022.acl-long.367}
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
| **Tags** | #morphology #kinyarwanda #bantu #pretraining #NER #two-tier-encoder #low-resource |

## Summary

KinyaBERT is a two-tier BERT for Kinyarwanda. A finite-state morphological analyser (plus a heuristic POS tagger) turns each word into a stem, affixes and POS tags; a small morphology encoder (no positional encoding) combines POS, stem, affix-set and affix embeddings per word, and its outputs plus a stem embedding feed a standard BERT-base sentence encoder. Pretrained from scratch with a morphology-aware MLM (predict stem and affixes) on 2.4 GB of Kinyarwanda text. It beats a same-corpus BPE BERT, a same-corpus BERT fed flat morpheme sequences, and XLM-R base on MasakhaNER (1.0) Kinyarwanda NER, machine-translated GLUE, and news classification ties with BPE BERT.

## Research question / problem

- BPE fails to recover Kinyarwanda morphemes; even with an analyser, feeding morphemes as a flat sequence into BERT does not capture word-level compositionality. Can a two-tier architecture do better?

## Method (details)

- **Morphological analyser:** finite-state two-level morphology, morphotactics DAG for all inflectable word types (verbs, nouns, adjectives, pronouns, numerals, quantifiers), hand-written morphographemic rules; built and calibrated by native speakers before this work; disambiguation by a classifier trained on a stemming dataset plus phrase-level POS context. BPE is used only for words the analyser cannot parse (misspellings, names, foreign words).
- **POS tagger:** unsupervised, greedy bidirectional decoding with emission scores from (i) morphological disambiguation, (ii) hand-set precedence weights per tag, (iii) Bantu class-agreement rules within a 7-word window.
- **Morphology encoder:** small transformer over {3 POS-related embeddings (one spans an affix-set vocabulary), stem, each affix}; outputs for POS and stem (4 vectors) are concatenated with another stem embedding as the word input to the main encoder.
- **Main encoder:** BERT-base dimensions (12 layers, 12 heads, hidden 768, FFN 3072), untied positional encoding with relative bias (TUPE); stem embedding size 256.
- **Pretraining objective:** MLM on 15% of words; when masked, affixes are dropped 70% of the time; predict stem plus either an affix distribution (ADR, KL loss) or an affix-set class (ASC, cross-entropy).
- **Variants:** KinyaBERT-ADR (101M params), KinyaBERT-ASC (105M); vocab: 34K stems and BPE tokens, 0.3K affixes, 0.2K POS tags, 34K affix sets for ASC.
- **Baselines:** BERT-BPE (120M, 43K BPE vocab, same corpus and steps), BERT-MORPHO (127M, flat morpheme + BPE sequence, 51K vocab, 30% masking worked better), XLM-R base (270M, 250K vocab, no Kinyarwanda in pretraining).
- **Pretraining data:** 2.4 GB, 390M tokens, 16M sentences, 840K documents from 370 websites (2011-2021).
- **Pretraining budget:** 32K steps, batch 2,560 sequences of up to 512 tokens, peak LR 4e-4 after 2,000 warm-up steps; KinyaBERT on RTX 3090 / 2080Ti desktop GPUs (about 22 h per 1,000 steps on one 3090), baselines on TPU v3-8. Parsing the corpus took 20 hours on a 12-core machine.
- **PEFT method (if any):** none; full fine-tuning with a 2-layer feed-forward head.
- **Languages covered:** Kinyarwanda.
- **Datasets:** MasakhaNER 1.0 Kinyarwanda (2.1K train sentences); machine-translated GLUE subset (MRPC, QNLI, RTE, SST-2, STS-B, WNLI) via Google Translate with human quality scores; new NEWS classification set (25.7K articles, 12 classes, 70/5/25 split).
- **Evaluation metrics:** NER micro-F1, GLUE accuracy/F1/correlation, NEWS accuracy; 10 fine-tuning runs each.

## Key findings

NER, MasakhaNER 1.0 Kinyarwanda, micro-F1 (Table 4, mean of 10 runs):

| Model | Dev | Test |
|---|---|---|
| XLM-R (base) | 80.3 | 71.8 |
| BERT-BPE | 83.4 | 74.8 |
| BERT-MORPHO (flat morphemes) | 83.2 | 72.8 |
| KinyaBERT-ADR | 87.1 | 77.2 |
| KinyaBERT-ASC | 86.2 | 76.3 |

Other test results:

| Model | MRPC acc/F1 | QNLI | RTE | SST-2 | STS-B | NEWS |
|---|---|---|---|---|---|---|
| XLM-R | 82.6/76.0 | 78.1 | 56.4 | 76.3 | 69.5/68.9 | 84.0 |
| BERT-BPE | 82.8/76.2 | 81.1 | 55.6 | 79.1 | 68.9/67.8 | 88.3 |
| BERT-MORPHO | 82.7/75.4 | 80.8 | 56.7 | 80.7 | 68.9/67.8 | 86.9 |
| KinyaBERT-ASC | 84.6/78.4 | 82.2 | 58.8 | 81.4 | 74.5/73.5 | 88.0 |

1. Two-tier morphology encoding beats BPE by +2.4 test F1 on NER (+3.7 dev); the abstract says "2%" and the text says "about 3.2%", so quote numbers from Table 4.
2. Feeding morphemes as a flat sequence (BERT-MORPHO) is worse than BPE on NER test (-2.0 F1) and NEWS (-1.4): having an analyser is not enough.
3. On NEWS, KinyaBERT does not beat BPE BERT on test (88.0 vs 88.3).
4. Ablation (Table 6): removing affixes (stem only) hurts high-resource GLUE tasks (QNLI, SST-2) but NER test barely moves (76.4 vs 76.3 to 77.2), so for NER the gain may come mostly from stems and POS rather than affixes.
5. KinyaBERT converges faster in fine-tuning and has 12%+ fewer parameters than BERT-BPE because of smaller vocabularies.

## What it needs (cost of the approach)

- A high-quality, hand-built morphological analyser and disambiguator (not open source per the paper).
- A hand-tuned POS tagger with language-specific agreement rules.
- Pretraining from scratch on 2.4 GB of in-language text (32K large-batch steps).
- Architecture changes, so it cannot be dropped into an existing XLM-R/AfroXLMR checkpoint.

## What we got from it

- The closest prior evidence that morphology helps Bantu NER, but only with an analyser, a custom architecture and pretraining from scratch.
- Independent confirmation of our result (a): flat morpheme sequences hurt NER even when the segmentation is high quality.

## Gaps and limitations

- **Stated by the authors:** analyser and POS tagger noise not quantified; design space (POS embeddings, affix-set size, morphology encoder type) not explored.
- **Our observations:**
  - MasakhaNER 1.0, not 2.0; XLM-R baseline is base size and never saw Kinyarwanda, so it is a weak multilingual baseline compared to AfroXLMR-large.
  - GLUE is machine-translated with noticeable noise (quality scores 2.7 to 3.1 out of 4).
  - Baselines trained on TPU, KinyaBERT on GPU; same steps and batch, so likely fine, but not identical stacks.
  - No significance tests; std over 10 runs given.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** shows the gain from morphology depends on how it enters the model: a separate word-level morphology encoder works, a flat morpheme stream does not. Our frozen-encoder PEFT setting is the flat-stream case (Morfessor words, NER -7.0), and our inner-word cuts (NER -3.9) are a softer version of it. A KinyaBERT-like idea compatible with PEFT would be a small trainable morphology module whose output is added to the frozen word-piece embeddings.
- **Our results:** supports the honest reading that our negative results are expected for input-level injection into a frozen model; it does not show that morphology cannot help via PEFT.
- **Low-resource / African language angle:** Kinyarwanda is one of our four languages.
- **Efficiency / low-cost hardware angle:** pretraining fits desktop GPUs but takes weeks of GPU time; not feasible for our four languages.
- **Baseline for us?** No as something to run (analyser, pretraining). Cite as the reference point; note that its NER numbers are on MasakhaNER 1.0 and not comparable with our MasakhaNER 2.0 results.

## Quotes and figures worth citing

> "naive sequencing of morphemes into a standard BERT architecture is inefficient at capturing morphological compositionality" (p. 5347, abstract)

> "It is also shown that having just a morphological analyzer is not enough" (p. 5352)

- Figure 1: two-tier architecture. Table 4: NER. Table 6: ablation. Table 8: vocab sizes and parameters.

## Related papers to follow up

- [ ] Nzeyimana (2020), Kinyarwanda morphological analysis.
- [ ] Mohseni and Tebbifakhr (2019), flat morpheme input to BERT.
- [ ] Ke et al. (2020), TUPE positional encoding.
- [ ] Later KinyaBERT follow-ups by the same author (not checked here).

## Open questions / discussion points

- Can a small trainable morphology encoder (stems + affix sets from an analyser or CRF) be bolted onto frozen AfroXLMR as an additive embedding, trained with LoRA?
- How would KinyaBERT compare with AfroXLMR-large on MasakhaNER 2.0 Kinyarwanda?
