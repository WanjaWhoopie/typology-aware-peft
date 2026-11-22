# POS: Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect)

Metric: accuracy (%).

| lang | afroxlmr_mlm | serengeti_mlm | difference | 95% CI (sentences + seeds) |
|---|---|---|---|---|
| kin | 98.3 | 97.5 | -0.8 | [-1.1, -0.5] |
| lug | 92.0 | 91.0 | -0.9 | [-1.4, -0.5] |
| swa | 92.8 | 92.3 | -0.5 | [-0.8, -0.1] |
| zul | 89.4 | 88.2 | -1.3 | [-1.8, -0.7] |

Pooled over 4 languages: -0.9 points, 95% CI [-1.1, -0.6].

Zero-shot, all 12 transfer cells: 65.3 -> 65.0 (-0.4).

Difference per transfer cell (rows = source, columns = target):

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin |  | +1.4 | -1.0 | +0.3 |
| lug | +0.6 |  | -0.6 | -1.2 |
| swa | -3.4 | +0.8 |  | -0.4 |
| zul | -1.3 | +0.1 | +0.4 |  |

