# Limited-Resource Adapters Are Regularizers, Not Linguists

## Reference

| Field | Details |
|---|---|
| **Title** | Limited-Resource Adapters Are Regularizers, Not Linguists |
| **Authors** | Marcell Fekete, Nathaniel R. Robinson, Ernests Lavrinovics, E. Djeride Jean-Baptiste, Raj Dabre, Johannes Bjerva, Heather Lent |
| **Year** | 2025 |
| **Venue** | ACL 2025 (Volume 2: Short Papers), pp. 222-237 |
| **DOI / URL** | https://doi.org/10.18653/v1/2025.acl-short.19 |
| **PDF (online)** | https://aclanthology.org/2025.acl-short.19.pdf |
| **Code / data** | not checked |

**Citation (APA):**
> Fekete, M., Robinson, N. R., Lavrinovics, E., Jean-Baptiste, E. D., Dabre, R., Bjerva, J., & Lent, H. (2025). Limited-resource adapters are regularizers, not linguists. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)* (pp. 222-237). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.acl-short.19

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{fekete-etal-2025-limited,
  title     = {Limited-Resource Adapters Are Regularizers, Not Linguists},
  author    = {Fekete, Marcell and Robinson, Nathaniel R. and Lavrinovics, Ernests and Jean-Baptiste, E. Djeride and Dabre, Raj and Bjerva, Johannes and Lent, Heather},
  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)},
  year      = {2025},
  pages     = {222--237},
  doi       = {10.18653/v1/2025.acl-short.19}
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
| **Tags** | #adapters #typology #controls #regularization #creoles #MT #low-resource |

## Summary

For MT from three Creoles (Haitian, Papiamento, Sango) into English with NLLB-200 600M, the authors train denoising language adapters, "soup" (weight-average) the Creole adapter with adapters of transfer languages, and fine-tune only decoder cross-attention on 10k parallel sentences. Transfer languages are chosen by phylogeny, Creole group, lang2vec typology, NLLB embeddings or subword evenness. All choices improve BLEU over baselines, but so do unrelated languages (Uralic, Dravidian, CJK) and a randomly initialised untrained adapter, often by as much or more. They conclude the adapters act as regularisers, supported by lower parameter variance and lower dev loss and gradient norms.

## Review claim check

- **Claim:** "typology-conditioned approach found equally effective with randomly initialized adapters".
- **Verdict:** partly holds.
- **Evidence:** the method is adapter souping with transfer languages selected by several criteria, one of which is lang2vec typology; it is not a typology-conditioned adapter generator. With that correction, the core finding holds: untrained-adapter souping gave mean BLEU gains of +3.49 / +7.98 / +2.51 vs +2.70 / +7.74 / +1.86 for principled transfer (hat / pap / sag, Table 2, p. 225).

## The control, exactly (for our shuffled-typology control)

- **Unrelated-language controls:** soup the Creole adapter with adapters of Uralic, Dravidian, or CJK languages (no phylogenetic or significant typological relation; two also differ in script).
- **Random adapter control ("init"):** a randomly initialised, untrained adapter, used two ways: (a) replacing the Creole source adapter; (b) souped with the Creole adapter at weight 1:3 (Creole : init), to mimic souping with three other adapters.
- All adapters, trained and untrained, start from the same random seed (needed for souping to work).
- Everything else fixed: same CA-FT on 10k NLLB-OPUS pairs, 1 epoch with early stopping, FLORES-200 evaluation.
- Main text reports means; no seed variance shown in the main paper.

## Research question / problem

- Which transfer-language criterion works best for adapter-based low-resource MT, and is the gain from linguistic transfer at all?

## Method

- **Approach:** denoising language adapters (MADLAD-400 data), adapter souping, cross-attention fine-tuning (following Üstün et al. 2021).
- **Model(s) / architecture:** NLLB-200 distilled 600M.
- **PEFT method (if any):** bottleneck adapters (trained 10k samples, up to 100k steps, early stopping).
- **Languages covered:** Haitian, Papiamento, Sango; Catalan as a sanity case with close relatives.
- **Datasets:** MADLAD-400, NLLB-OPUS (10k), FLORES-200.
- **Tasks:** MT into English (main).
- **Evaluation metrics:** BLEU, chrF; small native-speaker error analysis for Haitian.
- **Compute / hardware:** not reported as a focus.

## Key findings

| Creole -> English BLEU (Table 2) | hat | pap | sag |
|---|---|---|---|
| Base model (CA-FT) | 33.37 | 38.97 | 10.89 |
| lang2vec-selected souping | 36.54 | 47.04 | 13.07 |
| Untrained-adapter souping | 37.42 | 46.34 | 13.41 |
| Untrained adapter replacing source adapter | 37.07 | 45.01 | 14.91 |

1. Transfer-language choice does not matter; unrelated languages and noise do as well.
2. For Catalan (close relatives clearly known), no adapter method beats the base model, and the random adapter comes closest.
3. Souping lowers parameter variance; unregularised runs show higher gradient norms and dev loss.

## What we got from it

- A ready-made control design: random/untrained module and unrelated-language module, all else equal. Our shuffled-typology control (permute typology vectors across languages) plus a random-gate control fits this pattern.
- Warns that any gain from adding modules in a small-data regime may be regularisation, not linguistics.

## Gaps and limitations

- **Stated by the authors:** only three Creoles; limited typology coverage (Grambank covers only Haitian); religious-domain data issues.
- **Our observations:** MT and decoder cross-attention, a different setting from encoder sequence labelling; likely single runs; souping is weight averaging, not a learned gate.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** direct negative evidence that typology-based selection may carry no information beyond regularisation.
- **Low-resource / African language angle:** Sango (Central African Republic) is the only African-lexified case.
- **Efficiency / low-cost hardware angle:** small modules, cheap.
- **Baseline for us?** Yes, as controls: (1) random-init LoRA expert(s) in the mixture, (2) shuffled typology vectors, (3) a uniform (averaged) mixture. Our typology gate must beat all three.

## Quotes and figures worth citing

> "Surprisingly, our cross-attention fine-tuning approach appears equally effective with randomly initialized adapters" (abstract, p. 222)

- Table 2 (p. 225): BLEU per transfer criterion and controls.
- Figure 2: parameter variance of souped vs pretrained adapters.

## Related papers to follow up

- [ ] Üstün, Berard, Besacier & Gallé 2021, "Multilingual unsupervised neural machine translation with denoising adapters" (EMNLP 2021).
- [ ] Chronopoulou et al. 2023, AdapterSoup.

## Open questions / discussion points

- If our mixture helps on SIB-200 (701 items) or POS (about 750 sentences), is it regularisation? Compare against a regularisation-only baseline (e.g. stronger dropout or weight decay on single LoRA).
