# Effects of sub-word segmentation on performance of transformer language models

## Reference

| Field | Details |
|---|---|
| **Title** | Effects of sub-word segmentation on performance of transformer language models |
| **Authors** | Jue Hou, Anisia Katinskaia, Anh-Duc Vu, Roman Yangarber |
| **Year** | 2023 |
| **Venue** | Proceedings of EMNLP 2023, pp. 7413-7425 |
| **DOI / URL** | https://doi.org/10.18653/v1/2023.emnlp-main.459 |
| **PDF (online)** | https://aclanthology.org/2023.emnlp-main.459.pdf |
| **Code / data** | No code link found in the text we read |

**Citation (APA):**
> Hou, J., Katinskaia, A., Vu, A.-D., & Yangarber, R. (2023). Effects of sub-word segmentation on performance of transformer language models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 7413-7425). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.emnlp-main.459

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{hou2023effects,
  title     = {Effects of sub-word segmentation on performance of transformer language models},
  author    = {Hou, Jue and Katinskaia, Anisia and Vu, Anh-Duc and Yangarber, Roman},
  year      = {2023},
  booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  pages     = {7413--7425},
  doi       = {10.18653/v1/2023.emnlp-main.459}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | Low |
| **Tags** | #segmentation #morphology #morfessor #pretraining #finnish #russian #POS |

## Summary

Trains GPT and BERT from scratch on Finnish and Russian (plus English and Turkish GPT) with BPE versus two unsupervised morphological segmenters, Morfessor and StateMorph, at matched vocabulary sizes and two model sizes. Morphological segmentation gives lower perplexity and faster convergence in most settings, and downstream scores (topic classification, POS, linguistic acceptability, paraphrase) that are equal or slightly better. Smaller models with morphological segmentation can match larger BPE models.

## Review claim check

- **Claim:** "gains from morphology-aware segmentation, but pretrained from scratch with it".
- **Verdict:** holds (with weak downstream gains).
- **Evidence:** all GPT/BERT models are pretrained from scratch with each segmentation. Perplexity and convergence gains are clear, but downstream differences are small and mostly not significant (Finnish POS t-test p about 0.42 to 0.45); BERT with Morfessor is about 1% worse on Finnish POS.

## Research question / problem

- Compared to BPE, does unsupervised morphological segmentation give lower perplexity, faster convergence, equal or better downstream scores, and allow smaller models?

## Method

- **Approach:** same vocab size per comparison (StateMorph lexicon pruned to match); pretrain BERT and GPT; fine-tune on downstream tasks.
- **Model(s) / architecture:** BERT and GPT, base-like and medium-like sizes (instance length 256).
- **PEFT method (if any):** none.
- **Languages covered:** Finnish, Russian (full study); English, Turkish (GPT only).
- **Datasets:** Finnish news (HS, YLE), Russian Taiga, English Wikipedia + news, Turkish OSCAR; UD POS; Lenta.ru; RuCoLa; Finnish paraphrase.
- **Tasks:** topic classification, POS, linguistic acceptability, paraphrase generation.
- **Evaluation metrics:** perplexity, steps to convergence, accuracy/F1/MCC, chrF++.
- **Compute / hardware:** limited; smaller instance size and batch due to resources.

## Key findings

1. Morphological segmentation gives lower perplexity in almost all models; exceptions involve Morfessor.
2. BPE needs more steps to converge, sometimes several times more.
3. Downstream: POS differences under 1% (Russian under 0.1%); Morfessor BERT about 1% worse on Finnish POS; StateMorph slightly best.

## What we got from it

- Morfessor is the weakest morphological segmenter here too, and it slightly hurt POS; consistent with our Morfessor POS drop.

## Gaps and limitations

- **Stated by the authors:** two architectures, two main languages, limited segmenters and lexicon sizes, few downstream tasks.
- **Our observations:**
  - Perplexities are compared across different segmentations; token-level perplexity is not directly comparable across tokenizations unless normalised (we did not see such a normalisation).
  - From-scratch pretraining is outside our budget and setting.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** morphology helps when the model is built around it from the start; this does not transfer to a frozen pretrained model with a fixed tokenizer.
- **Our results:** our RQ1 asks whether morphology helps a frozen model via PEFT; this paper's positive result relies on pretraining from scratch, so it neither supports nor contradicts our negative results directly.
- **Low-resource / African language angle:** none.
- **Efficiency / low-cost hardware angle:** faster convergence is a sustainability argument, but only for pretraining.
- **Baseline for us?** No.

## Quotes and figures worth citing

> "achieve equivalent or better evaluation scores on downstream tasks." (p. 7413, abstract)

- Tables 1-2: perplexity and convergence. Table 6: Finnish/Russian POS.

## Related papers to follow up

- [ ] Park et al. (2021), morphology and LM surprisal across 92 languages.
- [ ] Toraman et al. (2022), Turkish tokenization study.
- [ ] Nouri and Yangarber (2017), StateMorph.

## Open questions / discussion points

- Is StateMorph available and usable for Bantu languages as a third segmenter?
