# Make the Best of Cross-lingual Transfer: Evidence from POS Tagging with over 100 Languages

## Reference

| Field | Details |
|---|---|
| **Title** | Make the Best of Cross-lingual Transfer: Evidence from POS Tagging with over 100 Languages |
| **Authors** | Wietse de Vries, Martijn Wieling, Malvina Nissim |
| **Year** | 2022 |
| **Venue** | ACL 2022 (60th Annual Meeting, Vol. 1: Long Papers), Dublin, pp. 7676-7685 |
| **DOI / URL** | https://aclanthology.org/2022.acl-long.529 |
| **PDF (online)** | [ACL Anthology](https://aclanthology.org/2022.acl-long.529.pdf) |
| **Code / data** | https://github.com/wietsedv/xpos ; 65 fine-tuned models at https://hf.co/spaces/wietsedv/xpos |

**Citation (APA):**
> de Vries, W., Wieling, M., & Nissim, M. (2022). Make the best of cross-lingual transfer: Evidence from POS tagging with over 100 languages. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 7676-7685). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{de-vries-etal-2022-make,
  title     = {Make the Best of Cross-lingual Transfer: Evidence from {POS} Tagging with over 100 Languages},
  author    = {de Vries, Wietse and Wieling, Martijn and Nissim, Malvina},
  booktitle = {Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2022},
  pages     = {7676--7685},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2022.acl-long.529}
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
| **Tags** | #POS #transfer #mixed-effects #typology #source-selection #UD #XLM-R |

## Summary

Fine-tunes XLM-R base for POS on each of 65 UD source languages and tests on 105 targets (UD 2.8). A linear mixed-effects model with random intercepts for source, target and target family explains transfer accuracy. Target pre-training inclusion is the strongest predictor (+19.2 points), followed by lexical-phonetic distance (LDND), both languages pre-trained, same family, source pre-trained, same writing system type, same writing system and same SOV order. Target language variance is more than three times source variance. Romanian is the best overall source; English ranks 19th of 65.

## Review claim check

- **Claim:** "65 sources, 105 targets; family, writing system and pretraining coverage all matter".
- **Verdict: holds.** 65 source and 105 target languages (Sec. 2). All are significant fixed effects in Table 1 (p < 0.01), along with LDND distance and SOV word order, which the claim leaves out.

## Research question / problem

- Which properties make a language a good source or target for zero-shot transfer, when English is not assumed to be the source?

## Method

- **Approach:** full 65 x 105 accuracy matrix; linear mixed-effects regression (fixed effects added by likelihood-ratio model comparison; random slopes checked).
- **Model(s) / architecture:** XLM-RoBERTa base (large gave no gain in pilot runs).
- **PEFT method (if any):** none.
- **Languages covered:** 105 UD languages; the African languages listed are Afrikaans, Bambara, Naija, Wolof, Yoruba (no Bantu language in the list I saw).
- **Datasets:** Universal Dependencies 2.8.
- **Tasks:** POS tagging.
- **Evaluation metrics:** accuracy.
- **Compute / hardware:** 1,000 batches of 10 samples; sources capped or oversampled to 10K samples; one random seed for all sources.

## Key findings

1. Mixed model coefficients (Table 1): target pre-trained +19.2; LDND distance -12.7 (0-1 scaled); both pre-trained +7.4; same family +6.8; source pre-trained +5.6; same writing system type +3.6; same writing system +1.4; same SOV order +1.3.
2. Marginal R2 = 47.1% (fixed effects); conditional R2 = 91.1%; target random effect variance more than 3x source variance.
3. Mean within-language accuracy 94.1%; mean cross-lingual 57.4% (sd 22.4).
4. Good source: in pre-training with same script, good within-language accuracy, same writing system type as target, more than about 200 training sentences.
5. Best source per target is from a different family for 23 of 30 families; Romanian best overall.

## What we got from it

- The modelling template for RQ2: mixed-effects regression with random intercepts for source and target, typology features as fixed effects.
- Independent replication of our "target explains most variance" finding (our 95% SIB, 81% NER, 44% POS).
- Covariates we must include: pre-training coverage of source and target, script match, lexical distance.

## Gaps and limitations

- **Stated by the authors:** POS only; most low-performing families have few languages, so family conclusions are uncertain; optimal pairs all in pre-training, unclear for unseen languages.
- **Our observations:** single seed; Indo-European heavy target set; no Bantu language; LDND and family are correlated.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** typology-like variables (family, word order, lexical distance) matter, but explain less than target identity and pre-training coverage. Morphological features were not tested.
- **Low-resource / African language angle:** almost no African coverage; we would extend it to Bantu.
- **Efficiency / low-cost hardware angle:** shows source undersampling to about 10K samples is enough; relevant to cheap runs.
- **Baseline or control for us:** **Control to adopt** (mixed-effects design with random source and target intercepts; pre-training and script covariates).

## Quotes and figures worth citing

> "the variance explained by the target language was more than three times as high as the variance explained by the source language" (p. 7678)

- Table 1: fixed-effect coefficients.
- Fig. 2: full source x target heatmap.

## Related papers to follow up

- [ ] Wichmann et al. (2010) LDND / ASJP
- [ ] de Vries et al. (2021), adapting monolingual models to low-resource languages
- [ ] Rice et al. (2025), ranking transfer languages for POS

## Open questions / discussion points

- With only 6 sources and 6 targets we cannot fit random effects for families; can we pool with this dataset or with MasakhaNER 2.0 Fig. 5 to get enough pairs?
