# Fast Vocabulary Transfer for Language Model Compression

## Reference

| Field | Details |
|---|---|
| **Title** | Fast Vocabulary Transfer for Language Model Compression |
| **Authors** | Leonidas Gee, Andrea Zugarini, Leonardo Rigutini, Paolo Torroni |
| **Year** | 2022 |
| **Venue** | Proceedings of EMNLP 2022: Industry Track, pp. 419-426 |
| **DOI / URL** | https://aclanthology.org/2022.emnlp-industry.41 |
| **PDF (online)** | https://aclanthology.org/2022.emnlp-industry.41.pdf |
| **Code / data** | No code link in the paper; datasets ADE, LEDGAR, CoNLL03 |

**Citation (APA):**
> Gee, L., Zugarini, A., Rigutini, L., & Torroni, P. (2022). Fast vocabulary transfer for language model compression. In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing: Industry Track* (pp. 419-426). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{gee2022fast,
  title     = {Fast Vocabulary Transfer for Language Model Compression},
  author    = {Gee, Leonidas and Zugarini, Andrea and Rigutini, Leonardo and Torroni, Paolo},
  year      = {2022},
  booktitle = {Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing: Industry Track},
  pages     = {419--426},
  url       = {https://aclanthology.org/2022.emnlp-industry.41}
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
| **Tags** | #tokenization #vocabulary-transfer #embeddings #compression |

## Summary

Proposes Fast Vocabulary Transfer (FVT): train a new in-domain tokenizer, copy embeddings for shared tokens, and initialise each new token as the mean of the old-tokenizer pieces it splits into. After initialisation the model is trained with MLM on in-domain data for one epoch, then fine-tuned on the task. On BERT-base, FVT keeps F1 close to the original tokenizer on medical and legal tasks and loses more on CoNLL03 NER; it always beats partial transfer (random init for new tokens). Combined with distillation it gives up to 2.76x speed-up.

## Review claim check

- **Claim:** "the method requires a masked-LM step on in-domain data after FVT initialisation, before fine-tuning".
- **Verdict:** holds (slightly overstated: it is part of their pipeline in every experiment, not a hard requirement of the initialisation).
- **Evidence:** p. 421 says they adjust the model by MLM on in-domain data before fine-tuning, found it beneficial in preliminary experiments, and "kept such a tuning stage in all our experiments"; MLM runs for one epoch (p. 422). No FVT-without-MLM result is reported.

## Research question / problem

- Can a smaller, domain-specific vocabulary compress and speed up a pretrained LM without large accuracy loss?

## Method

- **Approach:** new WordPiece tokenizer on in-domain data at 100/75/50/25% of BERT's vocab size; FVT init (Eq. 2: mean of old sub-token embeddings); baseline PVT (shared tokens copied, new tokens random); one epoch MLM on in-domain data; full fine-tuning; optional DistilBERT-style distillation before VT.
- **Model(s) / architecture:** BERT-base cased (28,996 wordpieces).
- **PEFT method (if any):** none; full fine-tuning, embeddings trainable.
- **Languages covered:** English only.
- **Datasets:** ADE (medical classification), LEDGAR (legal classification), CoNLL03 (NER).
- **Tasks:** sentence/document classification, NER.
- **Evaluation metrics:** F1, model size, inference speed-up; 3 seeds.
- **Compute / hardware:** not stated in detail.

## Key findings

| Setting | ADE F1 | LEDGAR F1 | CoNLL03 F1 |
|---|---|---|---|
| Original tokenizer (Tgen) | 90.80 | 80.93 | 89.43 |
| T100 + FVT | 90.77 | 80.60 | 87.87 |
| T25 + FVT | 90.27 | 81.03 | 86.17 |
| T100 + PVT | 82.57 | 80.07 | 84.53 |

1. FVT beats PVT everywhere, so averaging old sub-token embeddings is much better than random init.
2. NER on general news loses most (-1.6 to -3.3 F1); the authors link it to the domain being less specialised.
3. Smaller vocab does not always hurt; vocab size behaves like a hyperparameter.

## What we got from it

- The FVT formula we already use for Serengeti embeddings.
- The pipeline we did NOT follow: FVT is always followed by in-domain MLM and full fine-tuning with embeddings trainable.

## Gaps and limitations

- **Stated by the authors:** integrate VT into distillation; unified KPI metric.
- **Our observations:**
  - English only, monolingual BERT, same-language tokenizer swap (domain shift, not language shift).
  - No ablation of the MLM step, so its size of contribution is unknown.
  - The proceedings header in the PDF prints the wrong year for the conference dates (2020); actual venue is EMNLP 2022.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none directly; FVT is a mechanical vocabulary transfer.
- **Our results:** our Serengeti + FVT variant used frozen embeddings, no MLM step, and LoRA only, and lost NER -5.8 / POS -2.3. Even in the easy English domain-shift setting FVT costs NER points with MLM and full tuning, so our drop is not surprising. The missing MLM rung is the first thing to add.
- **Low-resource / African language angle:** none.
- **Efficiency / low-cost hardware angle:** one epoch MLM is cheap; matches our budget.
- **Baseline for us?** Yes: FVT + short MLM (embeddings trainable, or LoRA + embeddings) as the first rung of the masked-LM adaptation ladder.

## Quotes and figures worth citing

> "we kept such a tuning stage in all our experiments." (p. 421, on the MLM step after FVT)

- Table 2: FVT vs PVT F1. Table 5: size and speed-up.

## Related papers to follow up

- [ ] Samenko et al. (2021), VIPI vocabulary transfer (the method FVT simplifies).
- [ ] Gordon and Duh (2020), distillation and domain adaptation.

## Open questions / discussion points

- How much of FVT's recovery comes from the MLM epoch? Our ladder can measure this directly (FVT frozen vs FVT + MLM).
