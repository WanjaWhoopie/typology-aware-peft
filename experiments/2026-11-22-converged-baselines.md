# Experiment: converged baselines, low-data runs and the isiZulu capital split (kin, lug, swa, zul)

| Field | Details |
|---|---|
| **Date** | 2026-11-22 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done |
| **Code / commit** | `notebooks/baselines_colab.ipynb` blocks A, B, C; `src/token_baseline.py`, `src/token_report.py`, `src/build_workbook.py` (tab "Converged and follow-ups"); run on commit 5f24d41 |

## Hypothesis

- **A:** the first NER and POS baselines were undertrained and used an untuned LoRA; trained to convergence with the sweep's LoRA, the NER LoRA gap (−3.3) shrinks.
- **B:** splitting isiZulu prefix + capital words (uKaunda as u + Kaunda) raises NER transfer into isiZulu, since no source language writes names this way.
- **C:** if the LoRA gap is about training-set size, LoRA should keep up with 100 sentences and fall behind with 1,000 or more.

## Setup

- **Base model:** Davlan/afro-xlmr-large-76L
- **Methods:** full fine-tuning (lr 2e-5) and LoRA from the sweep (NER r=32 qv, POS r=8 qv, lr 3e-4)
- **Languages:** kin, lug, swa, zul; seeds 1 to 3; zero-shot 4x4
- **A:** up to 20 epochs, early stopping after 3 epochs without dev gain
- **B:** LoRA only, `--segment results/capsplit_seg --seg_mode word`; the NER label stays on the first piece of the word (the prefix)
- **C:** fixed subsets of 100 and 1,000 training sentences (NER) and 100 (POS), up to 40 epochs, stopping after 5
- **Hardware:** L4, bf16

## Results

| Question | Result |
|---|---|
| A. NER LoRA minus full, in-language (4 languages) | first −3.0 → converged **−0.5 [−1.0, −0.0]** |
| A. POS LoRA minus full | first −0.5 → converged −0.2 [−0.5, −0.0] |
| A. what changed | LoRA rose (NER +2.6 points on average: lug 84.1 → 89.3, kin 84.6 → 86.9); full fine-tuning barely moved (89.7 → 89.8) |
| A. zero-shot, LoRA minus full (12 cells) | NER −0.1, POS −1.2 |
| C. NER LoRA minus full by training size | 100: −0.0 (one collapsed LoRA run left out); 1,000: −1.2 [−1.8, −0.7]; all: −0.5 |
| C. POS LoRA minus full by training size | 100: −0.8 [−1.0, −0.5]; all: −0.2 |
| B. capital split minus converged LoRA, NER | isiZulu in-language −0.3 [−1.2, +0.7]; into isiZulu: kin −4.5, lug −5.0 [−7.5, −2.6], swa −0.3; out of isiZulu: −6.8, −11.7 [−14.8, −8.1], −7.9 |

Convergence: no run hit the epoch limit except one 100-sentence NER LoRA run (best at epoch 40 of 40); one 100-sentence NER LoRA run collapsed (zul, seed 3: best epoch 1, F1 near 0 on isiZulu, which drives the raw −23.6 for isiZulu in `results/ner_n100/summary.md`).

## Observations

- **The NER LoRA gap was mostly undertraining and an untuned LoRA.** Converged, LoRA trails full fine-tuning by 0.5 points on NER and 0.2 on POS, with 0.56% and 0.14% of the parameters. The earlier "−3.3" no longer describes LoRA on this model.
- **Earlier variant comparisons stay valid as paired comparisons** (each variant had exactly the settings of the LoRA baseline it was compared with), but they were made at an undertrained, untuned setting. The masked-LM runs already use the converged settings.
- **No training-size pattern.** The gap is about zero at 100 NER sentences, largest at 1,000 (−1.2) and small with all the data (−0.5); for POS it is largest at 100. The "PEFT lags on 1k to 10k examples" explanation from Chen et al. (2022) is not needed once LoRA is trained to convergence.
- **The capital split, as run, hurts transfer and does not test the hypothesis well.** The NER label stays on the first piece of the word, which is the prefix (u) in both the baseline and the split version, so the model still has to tag a lowercase prefix. Splitting changes what follows the label, not the labelled token. A model trained on split isiZulu text also transfers much worse to unsplit languages (−7 to −12). The cleaner test puts the label on the piece that starts with the capital.
- **Noise floor from a rerun.** The capital split touched almost nothing outside isiZulu (5 of 120,117 Luganda tokens), so its Luganda row is effectively a rerun of the converged baseline: Luganda in-language moved −1.8 [−3.6, −0.2] and lug→swa −4.0 [−6.1, −1.8]. GPU nondeterminism makes the bootstrap CIs (over test sentences and 3 seeds) too narrow for single transfer cells. Differences in single transfer cells below about 5 points should not be read as effects; pooled in-language differences are steadier (Kinyarwanda and Swahili rows moved by 0.5 or less). The Serengeti isiZulu gains (+9.5, +12.4, seen in two setups) are above this floor.

## Next steps

- [ ] Capital split with the label on the capitalised piece (the name), not the prefix
- [ ] Use the converged runs (`results/<task>_conv`) as the baseline for every later comparison
- [ ] Report transfer-cell differences with the rerun noise floor in mind; consider more seeds for the cells a claim rests on
