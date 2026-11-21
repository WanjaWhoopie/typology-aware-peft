# LGSE: Lexically Grounded Subword Embedding Initialization for Low-Resource Language Adaptation

## Reference

| Field | Details |
|---|---|
| **Title** | LGSE: Lexically Grounded Subword Embedding Initialization for Low-Resource Language Adaptation |
| **Authors** | Hailay Kidu Teklehaymanot, Dren Fazlija, Wolfgang Nejdl |
| **Year** | 2026 |
| **Venue** | arXiv preprint 2603.22629 (no venue stated in the PDF) |
| **DOI / URL** | https://doi.org/10.48550/arXiv.2603.22629 |
| **PDF (online)** | https://arxiv.org/pdf/2603.22629 |
| **Code / data** | Project page: https://hailaykidu.github.io/LGSE-Project-/ (new Amharic/Tigrinya educational-quality dataset promised) |

**Citation (APA):**
> Teklehaymanot, H. K., Fazlija, D., & Nejdl, W. (2026). LGSE: Lexically grounded subword embedding initialization for low-resource language adaptation. *arXiv preprint arXiv:2603.22629*. https://doi.org/10.48550/arXiv.2603.22629

<details>
<summary>BibTeX</summary>

```bibtex
@article{teklehaymanot2026lgse,
  title   = {{LGSE}: Lexically Grounded Subword Embedding Initialization for Low-Resource Language Adaptation},
  author  = {Teklehaymanot, Hailay Kidu and Fazlija, Dren and Nejdl, Wolfgang},
  year    = {2026},
  journal = {arXiv preprint arXiv:2603.22629},
  doi     = {10.48550/arXiv.2603.22629}
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
| **Tags** | #morphology #embeddings #vocabulary-transfer #amharic #tigrinya #LAPT #low-resource |

## Summary

LGSE adds morpheme-based tokens (from the supervised MoVoC morphology-aware BPE tokenizer) to XLM-R base and initialises each new token as the average of fastText character n-gram embeddings of its morphemes, mapped into XLM-R space by a learned linear projection; unanalysable tokens are sampled from a Gaussian fit to existing embeddings. A regulariser keeps new embeddings near their init during LAPT. Encoder layers are kept frozen during LAPT; only embeddings adapt. On Amharic and Tigrinya QA, NER and a new educational-quality classification set, LGSE + LAPT beats FOCUS + LAPT, random + LAPT and plain LAPT.

## Review claim check

- **Claim:** "morpheme-based embedding initialisation for Amharic and Tigrinya; updates the new embeddings".
- **Verdict:** holds, with a caveat about inconsistency.
- **Evidence:** the abstract says they "update only the new embeddings during adaptation", and Section 5 says encoder parameters are preserved and only the embedding layer E is adapted. But the paper is inconsistent: the abstract says the original vocabulary and tokenizer are retained, while Section 5 speaks of a language-specific vocabulary V_morph and Section 6.1 of a hybrid BPE + morpheme vocabulary.

## Research question / problem

- Does initialising new-token embeddings from morphemes (rather than arbitrary BPE pieces) give better adaptation for Ge'ez-script, morphologically rich languages?

## Method

- **Approach:** MoVoC tokenizer (supervised morphological analysis, then BPE inside morphemes, no merges across morpheme boundaries); LGSE init via fastText n-grams + linear projection; L2 regulariser to init; LAPT with MLM (10 epochs, LR 5e-5, seq 256), encoder frozen; then task fine-tuning.
- **Model(s) / architecture:** XLM-R base (about 125M parameters as stated).
- **PEFT method (if any):** effectively embedding-only adaptation during LAPT.
- **Languages covered:** Amharic, Tigrinya.
- **Datasets:** LAPT: CC100 Amharic (133M tokens), Tigrinya corpus (about 0.5 GB). Tasks: MasakhaNER (1.0) Amharic, Tigrinya NER (random 80/10/10), AmQA, TIGQA, new 2,500-item educational-quality dataset.
- **Tasks:** QA, NER, text classification.
- **Evaluation metrics:** F1 (QA, NER), accuracy (TC); 5 seeds.
- **Compute / hardware:** single Ampere GPU, up to 24 GPU-hours per run.

## Key findings

NER F1 (Table 2, mean of 5 seeds):

| Model | Tigrinya | Amharic |
|---|---|---|
| XLM-R off-the-shelf | 66.4 | 70.2 |
| XLM-R + LAPT | 69.8 | 75.0 |
| Random init + LAPT | 70.3 | 74.0 |
| FOCUS + LAPT | 77.5 | 78.1 |
| LGSE + LAPT | 79.0 | 79.4 |

1. LAPT alone adds about 2 to 5 F1 on NER.
2. FOCUS already captures most of the gain; LGSE adds about 1.3 to 1.5 F1 over FOCUS on NER.
3. Morpheme-aware tokenization lowers fertility (one Tigrinya example: 21 BPE tokens vs 6).

## What we got from it

- A morpheme-aware init recipe that could be applied to our Morfessor or CRF segments when adding tokens.
- Evidence that, when the embeddings are allowed to adapt by LAPT, morpheme-informed vocab can help NER.

## Gaps and limitations

- **Stated by the authors:** needs morphologically annotated resources; encoder-only; extra compute.
- **Our observations:**
  - Internal inconsistencies (vocab retained vs replaced; FOCUS described as not modifying the tokenizer, which is not what FOCUS does; "off-the-shelf zero-shot" baseline that still reports fine-tuned task scores).
  - No ablation separating morpheme tokenizer from morpheme-based init, and no scrambled control.
  - Ge'ez script is an unseen-script-like case for XLM-R, so gains may not carry to Latin-script Bantu languages.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** the closest "morpheme-aware embeddings + frozen encoder" study to our RQ1, and it reports gains. The key difference from our failed variants: their new embeddings are trained during LAPT; ours stayed frozen.
- **Our results:** suggests our Morfessor-cut (NER -3.9) and Serengeti (NER -5.8) arms might recover with an embedding-update MLM step; it does not tell us whether morphology or LAPT is doing the work, which needs a scrambled-cut control.
- **Low-resource / African language angle:** Amharic is a language we used earlier; Tigrinya is new; no Bantu languages.
- **Efficiency / low-cost hardware angle:** single GPU, 24 h budget.
- **Baseline for us?** No (needs a supervised analyser; Ge'ez only). Cite as supporting evidence for an embedding-update rung.

## Quotes and figures worth citing

> "we retain the original pre-trained model vocabulary and tokenizer and update only the new embeddings during adaptation." (p. 1, abstract)

- Table 2: QA/TC/NER results for all baselines.

## Related papers to follow up

- [ ] Teklehaymanot et al. (2025a), MoVoC tokenizer.
- [ ] Pham et al. (2024), UniBridge.
- [ ] Nag et al. (2023), EVALM.

## Open questions / discussion points

- Would a FOCUS-vs-LGSE gap of about 1.5 F1 survive a scrambled-morpheme init?
