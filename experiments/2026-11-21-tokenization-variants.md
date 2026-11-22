# Experiment: Morfessor cuts inside words, and Serengeti vocabulary (FVT, frozen embeddings) (RQ1)

| Field | Details |
|---|---|
| **Date** | 2026-11-21 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done |
| **Code / commit** | `src/token_baseline.py --seg_mode inner`, `src/vocab_transfer.py`, `notebooks/variants_colab.ipynb`; commits e887ae4, 2de6adf |

## Hypothesis

(a) Morpheme-aligned subword cuts help if words are not broken into extra words. (b) A vocabulary that splits less (Serengeti) helps once moved into AfroXLMR.

## Setup

- **Base model:** Davlan/afro-xlmr-large-76L, embeddings frozen
- **PEFT method:** LoRA r=8
- **Languages:** amh, hau, kin, lug, swa, zul
- **(a)** subword pieces forced to stop at Morfessor cuts, one word stays one word
- **(b)** Serengeti tokenizer; shared tokens keep AfroXLMR vectors, new tokens get the mean of their AfroXLMR pieces; no masked-LM step

## Results

| Variant | Metric | Difference vs plain LoRA |
|---|---|---|
| (a) cuts inside words | NER / POS | −3.9 [−4.9, −2.8] / −0.5 [−0.6, −0.3] |
| (b) Serengeti vocabulary | NER / POS | −5.8 [−6.6, −5.1] / −2.3 [−2.5, −2.1] |

## Observations

- Neither beats plain LoRA, with embeddings frozen.
- (b) skipped the masked-LM step that FVT prescribes, so it is not yet a fair test.
- Lead: with (b), NER transfer into isiZulu rises (lug→zul +7.9, swa→zul +7.5). A third of isiZulu entity words are prefix + capital (uKaunda); no other language has any.

## Next steps

- [x] Serengeti vocabulary + masked-LM step, with an AfroXLMR + masked-LM control (`2026-11-22-vocab-mlm.md`) (`notebooks/vocab_mlm_colab.ipynb`)
- [ ] isiZulu capital split (`notebooks/baselines_colab.ipynb`, block B)
- [ ] Scrambled-cut control (block D, awaiting supervisor)
