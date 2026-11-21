# Experiment: NER and POS baselines, LoRA

| Field | Details |
|---|---|
| **Date** | 2026-11-14 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done (to be retrained to convergence with a tuned LoRA) |
| **Code / commit** | `notebooks/token_colab.ipynb`; commit 809d7cd |

## Hypothesis

LoRA matches full fine-tuning on word-level tasks, as it does on SIB-200.

## Setup

- **Base model:** Davlan/afro-xlmr-large-76L
- **PEFT method:** LoRA r=8, alpha 16, query and value, lr 3e-4
- **Languages:** amh, hau, kin, lug, swa, zul
- **Task(s):** NER (5 epochs), POS (10 epochs), 3 seeds
- **Hardware / runtime / memory:** 0.14% trainable; NER 3.8 to 5.3 GB, about 3.4 times faster than full

## Results

| Language | Metric | LoRA minus full |
|---|---|---|
| pooled | NER entity F1 | −3.3, 95% CI [−3.9, −2.8] |
| per language | NER | −1.0 (swa) to −5.4 (lug) |
| pooled | POS accuracy | −0.8, 95% CI [−1.0, −0.7] |

## Observations

- The gap is larger on NER than POS, so it does not follow word structure. Two candidate explanations: undertraining (NER ran 5 epochs) and training-set size (PEFT tends to lag on 1k to 10k examples). Within NER the gap does not follow data size (amh, smallest, −4.7).

## Next steps

- [ ] LoRA sweep on Swahili dev (`notebooks/sweep_colab.ipynb`)
- [ ] Converged baselines and low-data runs (`notebooks/baselines_colab.ipynb`, blocks A and C)
