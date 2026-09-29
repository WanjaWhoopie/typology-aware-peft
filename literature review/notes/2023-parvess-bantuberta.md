# BantuBERTa: Using Language Family Grouping in Multilingual Language Modeling for Bantu Languages

## Reference

| Field | Details |
|---|---|
| **Title** | BantuBERTa: Using Language Family Grouping in Multilingual Language Modeling for Bantu Languages |
| **Authors** | Jesse Parvess (supervisors: Vukosi Marivate, Verrah Akinyi) |
| **Year** | 2023 |
| **Venue** | MSc mini-dissertation (Big Data Science), University of Pretoria |
| **DOI / URL** | https://repository.up.ac.za/handle/2263/92766 |
| **PDF (online)** | [UPSpace repository (open access PDF)](https://repository.up.ac.za/bitstream/handle/2263/92766/BantuBERTa__Using_Language_Family_Grouping_in_Multilingual_Language_Modeling_for_Bantu_Languages.pdf?isAllowed=y&sequence=1) |
| **Code / data** | [dsfsi/BantuBERTa on Hugging Face](https://huggingface.co/dsfsi/BantuBERTa) |

**Citation (APA):**
> Parvess, J. (2023). *BantuBERTa: Using language family grouping in multilingual language modeling for Bantu languages* [Master's mini-dissertation, University of Pretoria]. https://repository.up.ac.za/handle/2263/92766

<details>
<summary>BibTeX</summary>

```bibtex
@mastersthesis{parvess2023bantuberta,
  title  = {BantuBERTa: Using Language Family Grouping in Multilingual Language Modeling for Bantu Languages},
  author = {Parvess, Jesse},
  school = {University of Pretoria},
  year   = {2023},
  url    = {https://repository.up.ac.za/handle/2263/92766}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | Claude (AI-drafted; to be checked) |
| **Date read** | 2026-09-29 |
| **Status** | Read |
| **Relevance to our work** | Medium |
| **Tags** | #bantu #language-family #pretraining #typology #NER #topic-classification #low-resource |

## Summary

Pretrains a 125M-parameter RoBERTa-style model from scratch on Bantu languages only (3.8M sentences, mostly mC4 and CC100 web text). The question: does training only on one language family transfer better to that family than training on many unrelated languages? It loses to XLM-R, mBERT and AfriBERTa on NER, but roughly ties the best models on news topic classification. Conclusion: family grouping helps simple tasks; harder tasks also need more and cleaner data.

## Method

- **Model:** XLM-RoBERTa architecture, 10 layers, 6 heads, 70k BPE vocab, MLM only, batch size 8
- **Data:** 11 free datasets (CC100, mC4, NCHLT, OPUS-100, XL-Sum, WiLI, etc.), 15 languages; Swahili is 45%
- **Tuning:** 16 short runs varying data filtering, vocab size, heads and depth, then a regression to pick settings
- **Evaluation:** MasakhaNER (Swahili, Kinyarwanda, Luganda) and African News Topic Classification (Zulu, Lingala); F1
- **PEFT:** none
- **Compute:** not reported; batch size and search space limited by "resource constraints"

## Key findings

| NER F1 | Swahili | Kinyarwanda | Luganda |
|---|---|---|---|
| BantuBERTa | 0.850 | 0.694 | 0.730 |
| XLM-R base | 0.874 | 0.739 | 0.807 |
| AfriBERTa | 0.880 | 0.732 | 0.793 |

| News F1 | Lingala | Zulu |
|---|---|---|
| BantuBERTa | 0.589 | 0.797 |
| XLM-R + MAFT | 0.586 | 0.796 |

- More data beat cleaner data: the larger, noisier corpus gave better NER.
- Vocab size (70k vs 100k) and heads (6 vs 8) made no significant difference; depth helped slightly.

## What we got from it

- Pretraining from scratch fails with little data, which supports adapting an existing model with PEFT.
- Family grouping helps classification, so it's worth testing typology-based parameter sharing with adapters (WP3).
- Zulu writes prefixes into one word (*bangazifunda*), Northern Sotho writes them separately (*ba ka bala*). Fragmentation metrics must account for this (WP1).
- Guthrie's Bantu zones can serve as an extra static similarity baseline (WP2).
- Clean text sources: NCHLT, KINNEWS/KIRNEWS, XL-Sum, WiLI, English–Luganda parallel corpus.

## Gaps and limitations

- **Stated by the author:** small, mostly web-scraped data; skewed to Swahili/Zulu/Xhosa; only BPE tried; only 2 tasks; narrow hyperparameter search.
- **Our observations:**
  - Oromo is included as "Bantu" but is Cushitic (Afroasiatic), about 5% of the corpus.
  - Says "topographically similar" where it means typologically.
  - The cleaner dataset is also smaller, so size and quality effects can't be separated.
  - Baselines copied from other papers; single runs; the news "win" (+0.001–0.003) is within noise.
  - Discusses BPE fragmenting morphemes but never measures it.

## Relevance to typology-aware PEFT

- **Typology:** treats typology as family membership only, the static view RQ2 replaces.
- **African languages:** useful map of Bantu data on Hugging Face; BantuBERTa is a possible baseline.
- **Low cost:** a cautionary example of pretraining on limited compute.

## Related papers to follow up

- [ ] Ogueji et al. (2021). AfriBERTa: *Small Data? No Problem!* https://aclanthology.org/2021.mrl-1.11
- [ ] Alabi et al. (2022). *Adapting Pre-trained Language Models to African Languages via Multilingual Adaptive Fine-Tuning.* https://aclanthology.org/2022.coling-1.382
- [ ] Lauscher et al. (2020). *From Zero to Hero.* https://aclanthology.org/2020.emnlp-main.363
- [ ] Nzeyimana & Rubungo (2022). *KinyaBERT: a Morphology-aware Kinyarwanda Language Model.* https://arxiv.org/abs/2203.08459
- [ ] Park et al. (2021). *Morphology Matters.* https://doi.org/10.1162/tacl_a_00365

## Open questions

- Would a LoRA trained on Bantu-only languages transfer better to an unseen Bantu language than one trained on mixed families?
- Fragmentation per orthographic word or per morpheme, given conjunctive vs disjunctive spelling?
