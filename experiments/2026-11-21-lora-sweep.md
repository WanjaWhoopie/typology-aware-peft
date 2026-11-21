# Experiment: LoRA sweep on Swahili dev

| Field | Details |
|---|---|
| **Date** | 2026-11-21 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Running |
| **Code / commit** | `notebooks/sweep_colab.ipynb`, `src/sweep_report.py`; commit c2e39a4 |

## Hypothesis

The untuned LoRA (r=8, query and value) understates LoRA; a small sweep fixes one setting per task before the converged baselines.

## Setup

- **Base model:** Davlan/afro-xlmr-large-76L
- **PEFT method:** LoRA, rank 8 / 16 / 32 x targets query+value or all linear layers
- **Languages:** swa only, seed 1, dev only (test never evaluated)
- **Task(s):** NER and POS
- **Hyperparameters:** up to 20 epochs, early stopping after 3 epochs without dev gain
- **Selection rule (fixed in advance):** best dev; configs within 0.3 points tie; among ties the fewest trainable parameters wins

## Results

Pending.

## Observations

-

## Next steps

- [ ] Push `results/sweep/chosen.json`, then run `notebooks/baselines_colab.ipynb` and `notebooks/vocab_mlm_colab.ipynb`
