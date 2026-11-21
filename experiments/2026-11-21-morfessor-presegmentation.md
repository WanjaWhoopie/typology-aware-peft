# Experiment: Morfessor pre-segmentation, morphemes as separate words (RQ1)

| Field | Details |
|---|---|
| **Date** | 2026-11-21 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done |
| **Code / commit** | `src/morfessor_segment.py`, `notebooks/morfessor_colab.ipynb`, `src/variants_report.py`; commits 7d9e860, ca3a251 |

## Hypothesis

Feeding morphemes instead of whole words gives the unchanged tokenizer morpheme-aligned input and helps word-level tasks.

## Setup

- **Base model:** Davlan/afro-xlmr-large-76L, embeddings frozen
- **PEFT method:** LoRA r=8 (same as the LoRA baseline)
- **Languages:** amh, hau, kin, lug, swa, zul
- **Segmentation:** Morfessor Baseline, corpus weight 0.1, seen words only; each morpheme fed as its own word

## Results

| Language | Metric | Difference vs plain LoRA |
|---|---|---|
| pooled | NER entity F1 | −7.0 [−7.8, −6.1] |
| pooled | POS accuracy | −3.4 [−3.6, −3.2] |
| 30 transfer cells | NER / POS | −12.4 / −9.8 |

## Observations

- Lower in every language; not caused by truncation.
- Most of the damage comes from the extra word starts (see the next log).

## Next steps

- [x] Keep the cuts inside words (`2026-11-21-tokenization-variants.md`)
