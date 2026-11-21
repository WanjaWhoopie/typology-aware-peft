# UDapter: Language Adaptation for Truly Universal Dependency Parsing

## Reference

| Field | Details |
|---|---|
| **Title** | UDapter: Language Adaptation for Truly Universal Dependency Parsing |
| **Authors** | Ahmet Üstün, Arianna Bisazza, Gosse Bouma, Gertjan van Noord |
| **Year** | 2020 |
| **Venue** | EMNLP 2020, pp. 2302-2315 |
| **DOI / URL** | https://doi.org/10.18653/v1/2020.emnlp-main.180 |
| **PDF (online)** | https://aclanthology.org/2020.emnlp-main.180.pdf (also arXiv 2004.14327) |
| **Code / data** | https://github.com/ahmetustun/udapter |

**Citation (APA):**
> Üstün, A., Bisazza, A., Bouma, G., & van Noord, G. (2020). UDapter: Language adaptation for truly universal dependency parsing. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)* (pp. 2302-2315). Association for Computational Linguistics. https://doi.org/10.18653/v1/2020.emnlp-main.180

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{ustun-etal-2020-udapter,
  title     = {{UD}apter: Language Adaptation for Truly Universal Dependency Parsing},
  author    = {{\"U}st{\"u}n, Ahmet and Bisazza, Arianna and Bouma, Gosse and van Noord, Gertjan},
  booktitle = {Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)},
  year      = {2020},
  pages     = {2302--2315},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2020.emnlp-main.180}
}
```
</details>

**Journal follow-up (not read):** Üstün, A., Bisazza, A., Bouma, G., & van Noord, G. (2022). UDapter: Typology-based language adapters for multilingual dependency parsing and sequence labeling. *Computational Linguistics, 48*(3), 555-592. (Found in the reference list of Nakashole 2025; extends to sequence labeling.)

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | High |
| **Tags** | #adapters #typology #hypernetwork #URIEL #zero-shot #parsing |

## Summary

UDapter inserts bottleneck adapters into a frozen mBERT and generates the adapter and biaffine parser weights with a contextual parameter generator (CPG): a linear map from a language embedding. The language embedding is computed by an MLP from URIEL typology features (103 syntax, 28 phonology, 158 phonetic inventory). Trained on 13 high-resource UD treebanks, it beats monolingual and multilingual UDify on high-resource languages (avg LAS 87.3 vs 86.0 mono, 83.0 multi) and slightly improves zero-shot parsing on 30 low-resource languages (36.5 vs 36.3). Typology features matter mainly for zero-shot: with learned-from-scratch embeddings, in-training languages are unchanged (87.1 vs 87.3) but zero-shot collapses (9.0 vs 36.5).

## Review claim check

- **Claim:** "typology-conditioned adapters (contextual parameter generation from URIEL features)".
- **Verdict:** holds.
- **Evidence:** adapters and biaffine weights are generated from a language embedding computed from URIEL syntax, phonology and inventory features (Section 3.3-3.4, p. 2305). A 2022 Computational Linguistics journal version exists.

## Research question / problem

- How to balance cross-language sharing and language-specific capacity in one multilingual parser, and parse unseen languages zero-shot.

## Method

- **Approach:** CPG generates adapter + parser parameters from a typology-based language embedding; only generator, adapters and parser are trained.
- **Model(s) / architecture:** mBERT (frozen) + adapters (size 256) + biaffine parser; language embedding size 32.
- **PEFT method (if any):** bottleneck adapters (generated).
- **Languages covered:** 13 training languages (ar, en, eu, fi, he, hi, it, ja, ko, ru, sv, tr, zh); 30 zero-shot languages incl. Amharic, Bambara, Naija, Yoruba, Wolof (per appendix list).
- **Datasets:** UD 2.3.
- **Tasks:** dependency parsing.
- **Evaluation metrics:** LAS; paired bootstrap significance.
- **Compute / hardware:** not a focus; CPG multiplies adapter parameters by the embedding size.

## Key findings

| Setting | multi-udify | adapter-only | UDapter |
|---|---|---|---|
| High-resource avg LAS (13) | 83.0 | 85.0 | 87.3 |
| Zero-shot avg LAS (30) | 36.3 | 32.9 | 36.5 |

1. Typology-conditioned generation helps in-training languages over plain multilingual training, and gains are larger for smaller treebanks (Figure 2).
2. Zero-shot gains are small (+0.2 avg) and mixed (13 of 18 shown languages improve).
3. Random language embeddings learned from scratch match typology for training languages but fail for unseen ones (centroid embedding: 9.0 LAS).

## What we got from it

- The canonical "typology -> adapter weights" design; a natural parent of a typology-gated LoRA mixture.
- Its ablation (learned embeddings vs URIEL) is the template for our shuffled-typology control.

## Gaps and limitations

- **Stated by the authors:** parameter grouping and low-rank projections untried; why biaffine sharing matters most for low-resource is left open.
- **Our observations:** typology helps mostly as a way to place unseen languages; for seen languages, a learned ID works as well. Zero-shot gains are tiny on average. Single task, mBERT, no African training languages.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** URIEL syntax and phonology features, not morphology-specific; a Bantu-specific feature (e.g. MoI) is absent.
- **Low-resource / African language angle:** African languages only in the zero-shot set.
- **Efficiency / low-cost hardware angle:** adapters on a frozen encoder, but CPG inflates parameters.
- **Baseline for us?** Yes, in spirit: a "URIEL -> LoRA weights" generator (or a single shared LoRA with a language-embedding input) is the obvious competitor to a gated mixture. Re-implementing full CPG for XLM-R-large may be costly; a light version is enough.

## Quotes and figures worth citing

> "Our in-depth analyses show that soft parameter sharing via typological features is key to this success." (abstract, p. 2302)

- Figure 4a: typology vs learned embeddings, high-resource vs zero-shot.

## Related papers to follow up

- [ ] Üstün et al. 2022, Computational Linguistics journal version (adds sequence labeling).
- [ ] Platanios et al. 2018, contextual parameter generation.

## Open questions / discussion points

- Does the "typology only helps for unseen languages" result also hold for LoRA routing on our in-training languages? If so, RQ3 must be evaluated on held-out related languages.
