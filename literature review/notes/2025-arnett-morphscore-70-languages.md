# Evaluating Morphological Alignment of Tokenizers in 70 Languages

## Reference

| Field | Details |
|---|---|
| **Title** | Evaluating Morphological Alignment of Tokenizers in 70 Languages |
| **Authors** | Catherine Arnett, Marisa Hudspeth, Brendan O'Connor |
| **Year** | 2025 |
| **Venue** | Proceedings of the ICML 2025 Tokenization Workshop (TokShop), Vancouver; PMLR 267. arXiv 2507.06378 |
| **DOI / URL** | https://doi.org/10.48550/arXiv.2507.06378 |
| **PDF (online)** | https://arxiv.org/pdf/2507.06378 |
| **Code / data** | Data: https://huggingface.co/datasets/catherinearnett/morphscore ; code: https://github.com/catherinearnett/morphscore ; results: https://osf.io/eqy64/ |

**Citation (APA):**
> Arnett, C., Hudspeth, M., & O'Connor, B. (2025). Evaluating morphological alignment of tokenizers in 70 languages. In *Proceedings of the ICML 2025 Tokenization Workshop (TokShop)*. arXiv:2507.06378. https://doi.org/10.48550/arXiv.2507.06378

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{arnett2025morphscore,
  title     = {Evaluating Morphological Alignment of Tokenizers in 70 Languages},
  author    = {Arnett, Catherine and Hudspeth, Marisa and O'Connor, Brendan},
  year      = {2025},
  booktitle = {Proceedings of the ICML 2025 Tokenization Workshop (TokShop)},
  doi       = {10.48550/arXiv.2507.06378}
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
| **Tags** | #tokenization #morphology #MorphScore #evaluation #typology |

## Summary

Extends MorphScore from 22 to 70 languages using UD (and UniMorph) data, and changes scoring to boundary and subword precision/recall (precision penalises over-segmentation, which inflates accuracy-based alignment). Tests whether frequency scaling and inclusion of one-token words change scores. Then correlates alignment with downstream scores (XCOPA, XNLI, SIB-200, MultiBLiMP) for BLOOM, Llama 2/3, Gemma 3 and XGLM. Alignment explains very little variance, and the small correlation is negative.

## Review claim check

- **Claim:** "morphological alignment does not explain very much variance in model performance". Which venue/workshop?
- **Verdict:** holds. Venue: ICML 2025 Tokenization Workshop (TokShop), PMLR 267.
- **Evidence:** the abstract says alignment "does not explain very much variance"; the full mixed model reaches only R² = 0.024 (recall) and 0.005 (precision), and recall adds significant but tiny variance while precision adds none (p. 5).

## Research question / problem

- How should morphological alignment be scored, and does it predict model performance across many languages?

## Method

- **Approach:** gold segmentations derived from UD lemma/form pairs (concatenative only; Semitic and isolating languages drop out); boundary precision/recall and subword P/R/F1; parameter study (frequency scaling, one-token words); linear mixed-effects models with model size and training-data share as covariates.
- **Model(s) / architecture:** BLOOM (560M to 7.1B), Llama 2, Llama 3, Gemma 3, XGLM tokenizers and reported scores.
- **PEFT method (if any):** none.
- **Languages covered:** 70 (86 built, filtered at 100 items); Semitic languages incl. Amharic excluded for lack of usable items.
- **Datasets:** UD treebanks; task scores from XCOPA, XNLI, SIB-200, MultiBLiMP.
- **Tasks:** none trained; correlational.
- **Evaluation metrics:** MorphScore precision/recall, R².
- **Compute / hardware:** analysis only.

## Key findings

| Tokenizer | Recall | Precision |
|---|---|---|
| BLOOM | 0.33 | 0.11 |
| Gemma3 | 0.35 | 0.12 |
| Llama2 | 0.56 | 0.13 |
| Llama3 | 0.45 | 0.12 |
| XGLM | 0.52 | 0.23 |

1. Over-segmentation drives up recall/accuracy; precision is the more honest alignment score.
2. Alignment explains 0.5% to 2.4% of variance in task performance, with a negative sign.
3. Frequency-scaled, one-token-excluded scoring is chosen as default.

## What we got from it

- A ready tool and metric to score our segmenters and tokenizers; use precision, as they recommend, since our Morfessor cuts likely over-segment.

## Gaps and limitations

- **Stated by the authors:** few tasks per language; tasks mostly cover high-resource languages; frequency from small treebanks.
- **Our observations:**
  - Decoder LLMs with prompting-style evaluations; no fine-tuned encoder or token-level task.
  - Likely little or no coverage of our Bantu languages through UD (not verified per language).

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** second strong null for alignment as a predictor; consistent with our negative RQ1 results.
- **Low-resource / African language angle:** weak.
- **Our results:** if we report "morphology-aware input hurt", this paper plus Arnett and Bergen (2025) show the field also lacks evidence that alignment helps; our contribution would be the encoder + PEFT + token-level setting they do not cover.
- **Baseline for us?** No; use MorphScore (precision) as a diagnostic for our tokenizers.

## Quotes and figures worth citing

> "morphological alignment does not explain very much variance in model performance" (p. 1, abstract)

- Table 1: alignment of five pretrained tokenizers. Figure 2: alignment vs task scores.

## Related papers to follow up

- [ ] Batsuren et al. (2024), morphemic vs non-morphemic tokenization evaluation.
- [ ] MultiBLiMP (Jumelet et al., 2025).

## Open questions / discussion points

- Can we build MorphScore-style gold for Kinyarwanda/Luganda from available resources, or only for isiZulu (NCHLT)?
