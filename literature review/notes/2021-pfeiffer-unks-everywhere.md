# UNKs Everywhere: Adapting Multilingual Language Models to New Scripts

## Reference

| Field | Details |
|---|---|
| **Title** | UNKs Everywhere: Adapting Multilingual Language Models to New Scripts |
| **Authors** | Jonas Pfeiffer, Ivan Vulić, Iryna Gurevych, Sebastian Ruder |
| **Year** | 2021 |
| **Venue** | Proceedings of EMNLP 2021, pp. 10186-10203 |
| **DOI / URL** | https://doi.org/10.18653/v1/2021.emnlp-main.800 |
| **PDF (online)** | https://aclanthology.org/2021.emnlp-main.800.pdf |
| **Code / data** | https://github.com/Adapter-Hub/UNKs_everywhere |

**Citation (APA):**
> Pfeiffer, J., Vulić, I., Gurevych, I., & Ruder, S. (2021). UNKs everywhere: Adapting multilingual language models to new scripts. In *Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing* (pp. 10186-10203). Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.emnlp-main.800

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{pfeiffer2021unks,
  title     = {{UNKs} Everywhere: Adapting Multilingual Language Models to New Scripts},
  author    = {Pfeiffer, Jonas and Vuli{\'c}, Ivan and Gurevych, Iryna and Ruder, Sebastian},
  year      = {2021},
  booktitle = {Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing},
  pages     = {10186--10203},
  doi       = {10.18653/v1/2021.emnlp-main.800}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | Medium |
| **Tags** | #embeddings #vocabulary-transfer #adapters #MAD-X #unseen-scripts #amharic #low-resource |

## Summary

mBERT fails on languages whose script it never saw (Amharic, Tibetan, Khmer, Divehi, Sinhala): most tokens become UNK. The paper learns a new 10k WordPiece vocabulary and a new embedding matrix per target language, initialised either randomly, from lexically overlapping tokens, or through a low-dimensional matrix factorisation of mBERT's embeddings (with optional token clusters). New embeddings are trained jointly with MAD-X language adapters by MLM while the transformer is frozen; then a task adapter is trained on source-language data for zero-shot transfer. Largest gains are for unseen scripts; for Latin-script unseen languages the new-vocab methods are only competitive.

## Review claim check

- **Claim:** "learns new embedding matrices under frozen adapters".
- **Verdict:** partly holds (the wording is wrong).
- **Evidence:** new embedding matrices are learned, but jointly with the language adapters, not under frozen ones; what is frozen is the pretrained transformer (p. 10191: language adapters and embeddings trained "jointly while keeping the rest of the model fixed"). Adapters are frozen only later, when the task adapter is trained.

## Research question / problem

- How to adapt a multilingual model to low-resource languages, especially unseen scripts, by learning new embeddings that reuse knowledge in the pretrained embedding matrix.

## Method

- **Approach:** EL-RAND / EL-LEX (full new embeddings, random or lexical-overlap init); MF1 / MF10 (low-dim embeddings F times shared up-projections G from Semi-NMF of mBERT embeddings, with k-means or learned Gumbel-softmax clusters), each with RAND or LEX init.
- **Model(s) / architecture:** mBERT; MAD-X 2.0 (drops the adapter in the last layer).
- **PEFT method (if any):** language, invertible and task adapters; transformer frozen.
- **Languages covered:** 17 NER targets (incl. Amharic, Wolof, Maori, Guarani...), 6 DP targets; sources English, Chinese, Japanese, Arabic.
- **Datasets:** WikiANN NER, UD dependency parsing; Wikipedia for MLM (up to 100k steps).
- **Tasks:** zero-shot cross-lingual NER and DP.
- **Evaluation metrics:** F1, UAS/LAS, 5 runs.
- **Compute / hardware:** not detailed.

## Key findings

1. Zero-shot mBERT F1 correlates strongly with proportion of UNKs (Pearson -0.798) and less with lexical overlap (0.443) (p. 10188).
2. Lexical-overlap init helps for most languages; matrix factorisation helps most for unseen languages with seen scripts.
3. For Latin-script unseen languages (Maori, Ilokano, Guarani, Wolof) the new-vocab methods are only competitive with MAD-X 2.0, since Latin script is already well covered.
4. Alternating freeze/fine-tune of embeddings and transformer (Artetxe et al. 2020 style) largely underperforms the adapter route.

## What we got from it

- The idea of training new embeddings plus a language adapter by MLM while the body stays frozen: a PEFT-compatible version of LAPT.
- Overlap-based init is a cheap fallback when no fastText data exists.

## Gaps and limitations

- **Stated by the authors:** focus on unseen scripts; MF helps less for unseen scripts.
- **Our observations:**
  - mBERT only; zero-shot only; no in-language fine-tuning.
  - Our languages are Latin-script and seen by AfroXLMR, the regime where this paper reports little gain.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none; tokenizers are plain WordPiece.
- **Our results:** supports the view that a new vocabulary pays off mainly when the old one fails badly (UNKs). For Kinyarwanda, Luganda, Swahili and isiZulu on AfroXLMR there are no UNKs, so a vocab swap (our Serengeti arm, NER -5.8) has little to gain and much to lose unless embeddings are trained.
- **Low-resource / African language angle:** Amharic and Wolof only, zero-shot.
- **Efficiency / low-cost hardware angle:** adapter + embedding MLM with frozen body is cheap.
- **Baseline for us?** No.

## Quotes and figures worth citing

> "this empirically confirms that the Latin script is adequately represented in the original vocabulary." (p. 10193)

- Table 1: UNK and overlap rates. Figure 2: F1 vs UNK rate. Table 3: main NER/DP results.

## Related papers to follow up

- [ ] Artetxe et al. (2020), new embeddings for a frozen transformer.
- [ ] Pfeiffer et al. (2020), MAD-X.
- [ ] Rust et al. (2021), tokenizer quality and monolingual performance.

## Open questions / discussion points

- Could their "embeddings + language adapter via MLM" be our rung 2 (with LoRA in place of adapters)?
