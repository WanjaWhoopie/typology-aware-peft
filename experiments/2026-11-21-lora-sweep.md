# Experiment: LoRA sweep on Swahili dev

| Field | Details |
|---|---|
| **Date** | 2026-11-21 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done (2026-11-22) |
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

Full tables: `results/sweep/summary.md`; chosen settings: `results/sweep/chosen.json`.

| Task | Chosen | Dev | Runner-up | Old setting (r=8, qv) |
|---|---|---|---|---|
| NER | r=32, query+value (0.56% trainable) | 94.48 entity F1 | r=8, all layers 94.00 | 93.37 |
| POS | r=8, query+value (0.14% trainable) | 93.90 accuracy | best r=16, qv 94.18 (tied, more parameters) | 93.90 |

## Observations

- POS: all qv settings and r=32 all tie within 0.3 points, so the old setting stays.
- NER: the old setting was about 1.1 points below the best on dev. r=32 qv is the only config that kept improving past epoch 6 (best epoch 14 of 17); r=8 and r=16 qv stopped at epoch 8. With one seed, part of the 0.5-point lead over r=8 all may be noise; the rule was fixed in advance, so it stands.
- The tuned NER LoRA could close part of the 3.3-point LoRA gap; block A measures that.

## Next steps

- [x] Push `results/sweep/chosen.json`
- [x] Run `notebooks/baselines_colab.ipynb` and `notebooks/vocab_mlm_colab.ipynb` (2026-11-22)
