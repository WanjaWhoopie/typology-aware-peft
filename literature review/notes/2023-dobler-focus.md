# FOCUS: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models

## Reference

| Field | Details |
|---|---|
| **Title** | FOCUS: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models |
| **Authors** | Konstantin Dobler, Gerard de Melo |
| **Year** | 2023 |
| **Venue** | Proceedings of EMNLP 2023, pp. 13440-13454 |
| **DOI / URL** | https://doi.org/10.18653/v1/2023.emnlp-main.829 |
| **PDF (online)** | https://aclanthology.org/2023.emnlp-main.829.pdf |
| **Code / data** | https://github.com/konstantinjdobler/focus (code and checkpoints) |

**Citation (APA):**
> Dobler, K., & de Melo, G. (2023). FOCUS: Effective embedding initialization for monolingual specialization of multilingual models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 13440-13454). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.emnlp-main.829

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{dobler2023focus,
  title     = {{FOCUS}: Effective Embedding Initialization for Monolingual Specialization of Multilingual Models},
  author    = {Dobler, Konstantin and de Melo, Gerard},
  year      = {2023},
  booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  pages     = {13440--13454},
  doi       = {10.18653/v1/2023.emnlp-main.829}
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
| **Tags** | #tokenization #vocabulary-transfer #embeddings #swahili #hausa #xhosa #low-resource #LAPT |

## Summary

FOCUS replaces XLM-R's 250k vocabulary with a 50k language-specific SentencePiece vocabulary. Shared tokens keep their embeddings; each new token is a sparsemax-weighted mean of overlapping tokens' embeddings, with weights from similarity in a small fastText space trained on target text. All models then get language-adaptive pretraining (LAPT, MLM on CC100, 50M samples) before full fine-tuning. FOCUS + LAPT beats random init and WECHSEL and is on par with or slightly above LAPT on the original vocabulary for Swahili, Hausa and isiXhosa NER on MasakhaNER 2.0.

## Review claim check

- **Claim:** "swaps XLM-R's tokenizer for Kiswahili, Hausa and isiXhosa and evaluates on MasakhaNER 2.0, with continued pretraining after initialisation".
- **Verdict:** holds.
- **Evidence:** Section 3 uses XLM-R base with 50k Unigram tokenizers; NER for Swahili, Hausa and isiXhosa uses MasakhaNERv2 (Table 3); every replaced-vocab arm gets LAPT (50M samples, about 390k steps). Note it is XLM-R base, not large, and German/Arabic are also covered.

## Research question / problem

- How to initialise embeddings for a new language-specific tokenizer so that a multilingual encoder can be specialised to one language cheaply.

## Method

- **Approach:** copy overlapping-token embeddings; new tokens = sparsemax-weighted mean of similar overlapping tokens (similarity from auxiliary fastText token embeddings); then LAPT; then task fine-tuning.
- **Baselines:** off-the-shelf XLM-R; LAPT with original vocab; random init + 2-stage LAPT (embeddings-only for an extra 20% of steps first); WECHSEL; vocab extension (+30k tokens) with random or FOCUS init.
- **Model(s) / architecture:** XLM-R base (278M; 124M after vocab replacement).
- **PEFT method (if any):** none; full LAPT and full fine-tuning.
- **Languages covered:** German, Arabic, Kiswahili, Hausa, isiXhosa (downstream); more for MLM loss only.
- **Datasets:** CC100 (LAPT: Swahili 0.3 GB, Hausa 0.06 GB, isiXhosa 0.03 GB); XNLI, TyDiQA, WikiANN, MasakhaNERv2, GermEval14.
- **Tasks:** NLI, QA, NER.
- **Evaluation metrics:** accuracy / F1, 5 seeds, mean and sd.
- **Compute / hardware:** V100/A100/A6000 GPUs, 1 to 4 per run; LAPT is the heavy part.

## Key findings

MasakhaNERv2 test F1 (mean of 5 seeds, Table 3):

| Method | Swahili | Hausa | isiXhosa |
|---|---|---|---|
| XLM-R off-the-shelf | 92.0 | 84.2 | 85.5 |
| LAPT, original vocab | 92.5 | 85.6 | 88.3 |
| Replaced vocab, random + LAPT | 92.3 | 85.0 | 87.4 |
| Replaced vocab, FOCUS + LAPT | 92.6 | 86.0 | 88.5 |
| Extended vocab, random + LAPT | 92.0 | 84.1 | 87.2 |
| Extended vocab, FOCUS + LAPT | 92.1 | 84.9 | 87.7 |

(WECHSEL could not be run for Hausa and isiXhosa: no fastText word vectors.)

1. With LAPT, a new vocabulary does not hurt and FOCUS gives small gains over keeping XLM-R's vocab (+0.1 to +0.4 F1).
2. Keeping the original vocab + LAPT is a strong baseline; most of the gain over off-the-shelf comes from LAPT itself (+0.5 to +2.8 F1).
3. Directly after init (no training), FOCUS gives the lowest MLM loss of all inits (Table 4), but no downstream numbers without LAPT are reported.

## What we got from it

- A better initialiser than FVT to try, and evidence that a swapped vocabulary can match the original only after substantial LAPT.
- Hyperparameters for LAPT on tiny African corpora (isiXhosa 0.03 GB still helped).

## Gaps and limitations

- **Stated by the authors:** need monolingual data for LAPT and fastText; limited downstream languages; limited scripts.
- **Our observations:**
  - No frozen-embedding or PEFT condition, and no "init only, no LAPT" downstream result, which is exactly our setting.
  - LAPT budget (390k steps) is far beyond our hardware; a cheap-LAPT point is missing.
  - XLM-R base, not AfroXLMR-large.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none; tokenizer is plain Unigram.
- **Our results:** our Serengeti + FVT with frozen embeddings lost NER -5.8. FOCUS shows the recovery path is init + LAPT; with LAPT even random init is only about 1 F1 below. So our loss most likely reflects the missing adaptation step, not the vocabulary per se. Also note that the gain from a new vocab, even when it works, is small (under 0.5 F1) on Swahili/Hausa/isiXhosa NER.
- **Low-resource / African language angle:** directly on MasakhaNER 2.0 with two languages close to ours (Swahili; isiXhosa is Nguni like isiZulu).
- **Efficiency / low-cost hardware angle:** vocab replacement shrinks XLM-R by over 55%, useful for small GPUs.
- **Baseline for us?** Yes: FOCUS init as a stronger alternative to FVT inside the masked-LM ladder, plus "original vocab + short MLM" as the control rung.

## Quotes and figures worth citing

> "keeping the original vocabulary intact proves to be a strong baseline" (p. 13444)

- Table 3: NER including MasakhaNERv2. Table 4: MLM loss right after init. Figure 2: LAPT loss curves.

## Related papers to follow up

- [ ] Minixhofer et al. (2022), WECHSEL.
- [ ] de Vries and Nissim (2021), 2-stage embedding-first training.
- [ ] Alabi et al. (2022), multilingual adaptive fine-tuning (AfroXLMR).

## Open questions / discussion points

- Does a short LAPT (for example a few thousand steps, LoRA + embeddings) recover most of the FOCUS/FVT gap on AfroXLMR-large?
