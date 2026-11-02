# Masked-LM pseudo-log-likelihood

Model: Davlan/afro-xlmr-large-76L. SIB-200 test split (204 parallel sentences per language). Lower NLL = the model predicts the text better.

NLL per sentence is the fairest comparison across languages (same content). PPPL per token depends on how finely each language is split into subwords.

| lang | NLL/sentence word_l2r | NLL/sentence token | PPPL word_l2r | PPPL token | tokens/word | Spearman(NLL, SIB item acc) |
|---|---|---|---|---|---|---|
| amh | 110.5 | 56.1 | 14.65 | 3.91 | 2.36 | +0.14 |
| hau | 98.6 | 52.2 | 10.16 | 3.41 | 1.68 | +0.06 |
| kin | 110.1 | 39.6 | 8.19 | 2.13 | 2.56 | +0.05 |
| lug | 173.5 | 107.1 | 40.04 | 9.75 | 2.71 | +0.12 |
| swa | 88.0 | 49.8 | 12.08 | 4.09 | 1.64 | +0.07 |
| zul | 113.1 | 39.6 | 11.04 | 2.32 | 3.02 | +0.13 |

Spearman is computed per language over sentences, using word_l2r NLL. A negative value means sentences the model predicts poorly are also classified wrongly more often.

