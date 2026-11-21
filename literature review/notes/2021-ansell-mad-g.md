# MAD-G: Multilingual Adapter Generation for Efficient Cross-Lingual Transfer

## Reference

| Field | Details |
|---|---|
| **Title** | MAD-G: Multilingual Adapter Generation for Efficient Cross-Lingual Transfer |
| **Authors** | Alan Ansell, Edoardo Maria Ponti, Jonas Pfeiffer, Sebastian Ruder, Goran Glavaš, Ivan Vulić, Anna Korhonen |
| **Year** | 2021 |
| **Venue** | Findings of EMNLP 2021, pp. 4762-4781 |
| **DOI / URL** | https://doi.org/10.18653/v1/2021.findings-emnlp.410 |
| **PDF (online)** | https://aclanthology.org/2021.findings-emnlp.410.pdf |
| **Code / data** | not checked |

**Citation (APA):**
> Ansell, A., Ponti, E. M., Pfeiffer, J., Ruder, S., Glavaš, G., Vulić, I., & Korhonen, A. (2021). MAD-G: Multilingual adapter generation for efficient cross-lingual transfer. In *Findings of the Association for Computational Linguistics: EMNLP 2021* (pp. 4762-4781). Association for Computational Linguistics. https://doi.org/10.18653/v1/2021.findings-emnlp.410

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{ansell-etal-2021-mad-g,
  title     = {{MAD-G}: Multilingual Adapter Generation for Efficient Cross-Lingual Transfer},
  author    = {Ansell, Alan and Ponti, Edoardo Maria and Pfeiffer, Jonas and Ruder, Sebastian and Glava{\v{s}}, Goran and Vuli{\'c}, Ivan and Korhonen, Anna},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2021},
  year      = {2021},
  pages     = {4762--4781},
  doi       = {10.18653/v1/2021.findings-emnlp.410}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | High |
| **Tags** | #adapters #typology #URIEL #hypernetwork #MasakhaNER #kinyarwanda #luganda #swahili #zero-shot |

## Summary

MAD-G trains one contextual parameter generator that outputs a language adapter from a language's URIEL vector, using MLM on Wikipedias of 95 languages. A task adapter is trained on English on top of the generated English adapter; at test time the generated target-language adapter is swapped in. On zero-shot POS, parsing and MasakhaNER (mBERT, English CoNLL-2003 as source), it is competitive with MAD-X at about 50x lower training cost per language. On MasakhaNER, average F1 is 60.7 vs 52.3 for task-adapter-only and 48.7 for mBERT fine-tuning.

## Review claim check

- **Claim:** "generates adapters from typological features; substantial benefits for low-resource languages, particularly on NER in low-resource African languages".
- **Verdict:** partly holds.
- **Evidence:** the first half and the wording are the paper's own abstract (p. 4762). But the large NER gains are on languages whose Wikipedia was in the generator's MLM training (Hausa 77.1 vs 43.4 TA-only, Igbo, Kinyarwanda); on truly unseen languages gains are small or zero (Luganda +6.3, Luo -0.3, Wolof 0.0). Zero-shot only, mBERT, English source.

## Research question / problem

- Language adapters need monolingual data and training per language; can one generator produce adapters for any language from typology, including unseen ones?

## Method

- **Approach:** CPG (hypernetwork) maps URIEL vector -> language embedding -> adapter weights; MLM training over 95 languages; MAD-X-style stacking with a task adapter.
- **Model(s) / architecture:** mBERT (paper notes it can apply to XLM-R).
- **PEFT method (if any):** generated bottleneck language adapters + task adapter (bottleneck 48); MAD-G-LS variant is even smaller.
- **Languages covered:** MasakhaNER: Hausa, Igbo, Kinyarwanda (MAD-G-seen), Luganda, Luo, Wolof (unseen), Nigerian Pidgin, Swahili, Yoruba (mBERT-seen). Amharic excluded (script). Many UD languages for POS/DP.
- **Datasets:** UD 2.7; MasakhaNER (v1, Adelani et al. 2021); English CoNLL-2003 for NER training (MISC mapped to O, DATE excluded from evaluation).
- **Tasks:** POS, dependency parsing, NER; zero-shot cross-lingual.
- **Evaluation metrics:** accuracy, UAS/LAS, F1.
- **Compute / hardware:** about 50x more efficient per target language than MAD-X.

## Key findings

MasakhaNER F1 (Table 3, p. 4768), task trained on English only:

| Method | hau | ibo | kin | lug | luo | pcm | swa | wol | yor | avg |
|---|---|---|---|---|---|---|---|---|---|---|
| MAD-G | 77.1 | 69.9 | 66.1 | 54.2 | 32.5 | 72.6 | 72.6 | 32.1 | 68.8 | 60.7 |
| MAD-G-en (English adapter at test) | 44.9 | 54.5 | 51.4 | 50.6 | 32.9 | 70.4 | 69.2 | 36.4 | 63.9 | 52.7 |
| TA-only | 43.4 | 55.7 | 52.8 | 47.9 | 32.8 | 72.3 | 68.6 | 32.1 | 65.3 | 52.3 |
| mBERT-ft | 43.2 | 45.5 | 49.9 | 49.3 | 31.6 | 70.5 | 65.8 | 28.1 | 54.3 | 48.7 |
| XLM-R-ft (from Adelani et al.) | 66.4 | 45.5 | 36.1 | 34.8 | 31.9 | 68.4 | 74.5 | 21.6 | 33.4 | 45.8 |

1. Generated adapters are competitive with MAD-X across tasks at much lower cost.
2. Gains over English-only transfer concentrate on languages included in the generator's MLM training; for unseen languages benefit appears mainly in NER and depends on having a related genus in training.
3. Generated adapters are a better starting point than random init when fine-tuned on 1k to 100k words of target text.

## What we got from it

- MAD-G-en (use the English adapter instead of the target's generated one) is a clean control for "does the language-specific part do anything", analogous to our shuffled-typology control.
- Kinyarwanda and Luganda NER zero-shot numbers exist here (mBERT, MasakhaNER v1); not comparable to our supervised MasakhaNER 2.0 numbers.

## Gaps and limitations

- **Stated by the authors:** no NER experiment for unseen languages with monolingual fine-tuning (only two such MasakhaNER languages); benefits depend on genus coverage.
- **Our observations:** zero-shot from English only; no in-language supervision; mBERT base; NER data v1 with DATE removed. The "typology" contribution is not separated from "language was in MLM training".

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** URIEL vectors; no morphology-specific features.
- **Low-resource / African language angle:** covers Kinyarwanda, Luganda, Swahili (not Zulu) on NER.
- **Efficiency / low-cost hardware angle:** one generator for many languages, cheap per-language cost.
- **Baseline for us?** Partly. A full MAD-G pipeline (MLM generator over 95 languages) is too costly. A cheap variant is a baseline: LoRA weights or gate inputs generated from URIEL vectors, plus the MAD-G-en style control.

## Quotes and figures worth citing

> "it offers substantial benefits for low-resource languages, particularly on the NER task in low-resource African languages." (abstract, p. 4762)

- Table 3 (p. 4768): MasakhaNER zero-shot F1 by language and seen/unseen group.

## Related papers to follow up

- [ ] Pfeiffer et al. 2020, MAD-X.
- [ ] Ponti et al. 2021, parameter space factorization.

## Open questions / discussion points

- How much of MAD-G's African NER gain is typology vs having those languages' Wikipedia in the generator's MLM data? Our design should keep this separation explicit.
