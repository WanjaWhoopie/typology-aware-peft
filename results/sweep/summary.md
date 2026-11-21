# LoRA sweep (Swahili dev, seed 1)

Rule: highest dev score; configs within 0.3 points count as tied, and the tie with the fewest trainable parameters wins. Test sets were not evaluated.

## NER

| rank | targets | dev entity F1 % | trainable % | best epoch | epochs run | minutes | peak GPU GB |  |
|---|---|---|---|---|---|---|---|---|
| r=8 | all | 94.00 | 0.63 | 6 | 9 | 10.4 | 6.7 |  |
| r=16 | all | 93.96 | 1.25 | 6 | 9 | 10.5 | 6.8 |  |
| r=32 | all | 93.36 | 2.47 | 4 | 7 | 8.2 | 6.9 |  |
| r=8 | qv | 93.37 | 0.14 | 5 | 8 | 5.0 | 5.2 |  |
| r=16 | qv | 93.21 | 0.28 | 5 | 8 | 5.0 | 5.2 |  |
| r=32 | qv | 94.48 | 0.56 | 14 | 17 | 10.8 | 5.2 | chosen |

## POS

| rank | targets | dev accuracy % | trainable % | best epoch | epochs run | minutes | peak GPU GB |  |
|---|---|---|---|---|---|---|---|---|
| r=8 | all | 93.61 | 0.63 | 4 | 7 | 0.9 | 5.7 |  |
| r=16 | all | 93.84 | 1.25 | 4 | 7 | 0.9 | 5.7 |  |
| r=32 | all | 93.97 | 2.47 | 11 | 14 | 1.8 | 5.9 | tied |
| r=8 | qv | 93.90 | 0.14 | 14 | 17 | 1.2 | 4.5 | chosen |
| r=16 | qv | 94.18 | 0.28 | 10 | 13 | 0.9 | 4.6 | tied |
| r=32 | qv | 94.05 | 0.56 | 10 | 13 | 0.9 | 4.6 | tied |

