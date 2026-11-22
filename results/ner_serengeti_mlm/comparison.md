# NER: Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect)

Metric: entity F1 (%).

| lang | afroxlmr_mlm | serengeti_mlm | difference | 95% CI (sentences + seeds) |
|---|---|---|---|---|
| kin | 86.1 | 84.9 | -1.2 | [-2.9, +0.8] |
| lug | 89.5 | 88.2 | -1.3 | [-2.8, +0.1] |
| swa | 92.2 | 91.4 | -0.8 | [-1.3, -0.3] |
| zul | 88.9 | 86.4 | -2.5 | [-4.3, -0.9] |

Pooled over 4 languages: -1.5 points, 95% CI [-2.2, -0.7].

Zero-shot, all 12 transfer cells: 65.1 -> 66.5 (+1.4).

Difference per transfer cell (rows = source, columns = target):

| source \ target | kin | lug | swa | zul |
|---|---|---|---|---|
| kin |  | -1.4 | +1.1 | +0.4 |
| lug | -4.7 |  | -0.6 | +9.5 |
| swa | -1.7 | -1.2 |  | +12.4 |
| zul | -0.6 | +1.0 | +2.2 |  |

