# Experiment: NER and POS baselines, full fine-tuning

| Field | Details |
|---|---|
| **Date** | 2026-11-09 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done; retrained to convergence in `2026-11-22-converged-baselines.md` |
| **Code / commit** | `src/token_baseline.py`, `src/token_report.py`, `notebooks/token_colab.ipynb`; commit 8398cbf |

## Hypothesis

Reference scores for word-level tasks, where tokenization should matter more than for topics.

## Setup

- **Base model:** Davlan/afro-xlmr-large-76L
- **PEFT method:** full fine-tuning
- **Languages:** amh, hau, kin, lug, swa, zul
- **Dataset(s):** MasakhaNER 2.0 (1.0 for amh), MasakhaPOS (UD_Amharic-ATT for amh)
- **Task(s):** NER, POS, in-language and zero-shot 6x6
- **Hyperparameters:** lr 2e-5, NER 5 epochs, POS 10 epochs, 3 seeds
- **Hardware / runtime / memory:** L4, 11.3 GB

## Results

| Language | Metric | Full |
|---|---|---|
| hau / kin / lug / swa / zul | NER entity F1 | 86.2 / 87.6 / 89.5 / 92.4 / 89.2 (MasakhaNER 2.0 reports 87.4 / 87.5 / 89.6 / 92.7 / 90.6) |
| amh | NER entity F1 | about 78 |
| all | POS accuracy | 90 (zul) to 98 (kin) |

## Observations

- Reproduces published AfroXLMR-large NER within about a point.
- 16 of 18 NER runs per method peaked in epoch 4 or 5 of 5, and POS runs in epoch 9 to 10 of 10: probably undertrained.
- NER: no clear Bantu advantage once Hausa is separated from Amharic. POS: Bantu advantage, resting on Hausa as the one clean contrast.

## Next steps

- [x] Retrain to convergence with early stopping (`notebooks/baselines_colab.ipynb`, block A)
