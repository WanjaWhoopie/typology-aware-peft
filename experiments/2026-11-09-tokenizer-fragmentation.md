# Experiment: Tokenizer fragmentation and isiZulu morpheme boundaries

| Field | Details |
|---|---|
| **Date** | 2026-11-09 |
| **Run by** | Wanjiru (Colab L4), analysis with Claude |
| **Status** | Done |
| **Code / commit** | `src/tokenizer_stats.py`, `src/morfessor_silver.py`; commits 8398cbf, 53317c9 |

## Hypothesis

Subword tokenizers break up morphologically rich words, and token boundaries rarely fall on morpheme boundaries (RQ1 premise).

## Setup

- **Base model:** tokenizers only (AfroXLMR, Serengeti, AfriBERTa, BantuBERTa, mBERT, others)
- **Languages:** amh, hau, kin, lug, swa, zul, eng
- **Dataset(s):** SIB-200 parallel text (1,004 sentences); NCHLT isiZulu gold segmentations
- **Metrics:** fertility, continued words, token premium, Renyi efficiency, unknown rate; boundary precision / recall / F1

## Results

| Language | Metric | Result |
|---|---|---|
| swa to zul | AfroXLMR tokens per word | 1.65 to 3.01 |
| all | Serengeti tokens per word | 1.25 to 2.19 (lowest for every language) |
| zul | boundary F1 across tokenizers | 0.32 to 0.41 (AfroXLMR 0.38), chance precision 0.30 |
| zul | Morfessor boundary F1 (held-out gold) | 0.45, precision 0.51 at the chosen weight |

## Observations

- Token boundaries are barely above chance on isiZulu morpheme boundaries.
- Morfessor is not a good stand-in for gold (about half its cuts are wrong).
- Fertility measurement alone overlaps recent preprints; the gold-boundary analysis is the more distinctive part.

## Next steps

- [ ] Supervised segmenter on the NCHLT gold (awaiting supervisor)
