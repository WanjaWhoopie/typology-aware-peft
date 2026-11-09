# Tokenizer fragmentation study

Text: SIB-200 (FLORES) sentences, 1,004 per language, the same content in every language. Words are whitespace-separated; each word is tokenized as it appears after a space.

## Fertility (tokens per word, lower = less splitting)

| tokenizer | vocab | amh | hau | kin | lug | swa | zul | eng |
|---|---|---|---|---|---|---|---|---|
| AfroXLMR-76L | 250,002 | 2.35 | 1.69 | 2.56 | 2.67 | 1.65 | 3.01 | 1.39 |
| Serengeti | 250,004 | 1.58 | 1.27 | 1.78 | 1.99 | 1.25 | 2.19 | 1.27 |
| AfriBERTa | 70,005 | 1.71 | 1.37 | 1.92 | 2.76 | 1.47 | 3.73 | 1.62 |
| BantuBERTa | 70,000 | 12.91 | 1.87 | 1.86 | 2.19 | 1.42 | 1.94 | 1.39 |
| mBERT | 119,547 | 1.15 | 1.89 | 2.76 | 2.84 | 2.06 | 3.57 | 1.31 |
| mT5 | 250,100 | 3.33 | 1.82 | 2.49 | 2.66 | 1.96 | 2.99 | 1.53 |

## Continued words (% of words split into 2+ tokens)

| tokenizer | vocab | amh | hau | kin | lug | swa | zul | eng |
|---|---|---|---|---|---|---|---|---|
| AfroXLMR-76L | 250,002 | 62% | 44% | 76% | 77% | 42% | 88% | 27% |
| Serengeti | 250,004 | 37% | 19% | 45% | 56% | 20% | 67% | 20% |
| AfriBERTa | 70,005 | 40% | 22% | 49% | 77% | 29% | 96% | 35% |
| BantuBERTa | 70,000 | 99% | 51% | 38% | 60% | 29% | 55% | 26% |
| mBERT | 119,547 | 12% | 60% | 79% | 78% | 59% | 97% | 21% |
| mT5 | 250,100 | 94% | 58% | 75% | 78% | 65% | 96% | 40% |

## Token premium (tokens per sentence / English, same tokenizer)

| tokenizer | vocab | amh | hau | kin | lug | swa | zul | eng |
|---|---|---|---|---|---|---|---|---|
| AfroXLMR-76L | 250,002 | 1.36 | 1.42 | 1.73 | 1.56 | 1.17 | 1.57 | 1.00 |
| Serengeti | 250,004 | 1.00 | 1.16 | 1.32 | 1.26 | 0.97 | 1.25 | 1.00 |
| AfriBERTa | 70,005 | 0.85 | 0.98 | 1.11 | 1.38 | 0.90 | 1.67 | 1.00 |
| BantuBERTa | 70,000 | 7.48 | 1.56 | 1.25 | 1.27 | 1.01 | 1.01 | 1.00 |
| mBERT | 119,547 | 0.71 | 1.67 | 1.97 | 1.75 | 1.55 | 1.98 | 1.00 |
| mT5 | 250,100 | 1.76 | 1.39 | 1.53 | 1.41 | 1.26 | 1.42 | 1.00 |

## Renyi efficiency (alpha 2.5, higher = more even use of the vocabulary)

| tokenizer | vocab | amh | hau | kin | lug | swa | zul | eng |
|---|---|---|---|---|---|---|---|---|
| AfroXLMR-76L | 250,002 | 0.384 | 0.369 | 0.405 | 0.412 | 0.374 | 0.431 | 0.354 |
| Serengeti | 250,004 | 0.443 | 0.349 | 0.384 | 0.414 | 0.348 | 0.417 | 0.355 |
| AfriBERTa | 70,005 | 0.459 | 0.393 | 0.426 | 0.439 | 0.402 | 0.442 | 0.402 |
| BantuBERTa | 70,000 | 0.167 | 0.414 | 0.390 | 0.449 | 0.398 | 0.427 | 0.394 |
| mBERT | 119,547 | 0.008 | 0.387 | 0.418 | 0.419 | 0.403 | 0.434 | 0.374 |
| mT5 | 250,100 | 0.302 | 0.293 | 0.303 | 0.320 | 0.313 | 0.327 | 0.271 |

## Unknown-token rate

| tokenizer | vocab | amh | hau | kin | lug | swa | zul | eng |
|---|---|---|---|---|---|---|---|---|
| AfroXLMR-76L | 250,002 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| Serengeti | 250,004 | 0.27% | 0.09% | 0.01% | 0.01% | 0.00% | 0.01% | 0.01% |
| AfriBERTa | 70,005 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| BantuBERTa | 70,000 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |
| mBERT | 119,547 | 94.70% | 2.48% | 2.77% | 1.47% | 0.17% | 0.13% | 0.17% |
| mT5 | 250,100 | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% | 0.00% |

## Morpheme boundaries (gold surface segmentation)

| tokenizer | lang | words scored | boundary precision | boundary recall | boundary F1 | exact match | tokens/word | morphemes/word |
|---|---|---|---|---|---|---|---|---|
| AfroXLMR-76L | zul | 11,392 of 11,392 | 0.41 | 0.36 | 0.38 | 5% | 3.23 | 3.51 |
| Serengeti | zul | 11,392 of 11,392 | 0.49 | 0.25 | 0.33 | 5% | 2.28 | 3.51 |
| AfriBERTa | zul | 11,392 of 11,392 | 0.39 | 0.44 | 0.41 | 4% | 3.85 | 3.51 |
| BantuBERTa | zul | 10,251 of 11,392 | 0.58 | 0.22 | 0.32 | 4% | 1.98 | 3.57 |
| mBERT | zul | 11,392 of 11,392 | 0.31 | 0.35 | 0.33 | 3% | 3.80 | 3.51 |
| mT5 | zul | 11,392 of 11,392 | 0.43 | 0.32 | 0.37 | 5% | 2.87 | 3.51 |

Precision: share of token boundaries that are morpheme boundaries. Recall: share of morpheme boundaries the tokenizer also cuts at. Words whose pieces do not spell the word (byte-level pieces, unknown tokens) are not scored.

Chance precision (zul): 0.30, the share of positions inside a word that are morpheme boundaries, i.e. the precision of cutting at random.

Not loaded (gated or broken): InkubaLM (`lelapa/InkubaLM-0.4B`, OSError), Llama-3.1 (`meta-llama/Llama-3.1-8B`, OSError), Gemma-2 (`google/gemma-2-2b`, OSError)

