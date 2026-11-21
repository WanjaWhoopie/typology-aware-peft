# MasakhaPOS: Part-of-Speech Tagging for Typologically Diverse African Languages

## Reference

| Field | Details |
|---|---|
| **Title** | MasakhaPOS: Part-of-Speech Tagging for Typologically Diverse African languages |
| **Authors** | Cheikh M. Bamba Dione, David Ifeoluwa Adelani, Peter Nabende, Jesujoba O. Alabi, et al. (Masakhane NLP) |
| **Year** | 2023 |
| **Venue** | ACL 2023 (61st Annual Meeting, Vol. 1: Long Papers), Toronto, pp. 10883-10900 |
| **DOI / URL** | https://doi.org/10.18653/v1/2023.acl-long.609 |
| **PDF (online)** | [arXiv 2305.13989](https://arxiv.org/pdf/2305.13989) (read: v1) |
| **Code / data** | MasakhaPOS (Masakhane GitHub; link in paper) |

**Citation (APA):**
> Dione, C. M. B., Adelani, D. I., Nabende, P., Alabi, J. O., et al. (2023). MasakhaPOS: Part-of-speech tagging for typologically diverse African languages. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 10883-10900). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.acl-long.609

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{dione-etal-2023-masakhapos,
  title     = {{MasakhaPOS}: Part-of-Speech Tagging for Typologically Diverse {A}frican languages},
  author    = {Dione, Cheikh M. Bamba and Adelani, David Ifeoluwa and Nabende, Peter and Alabi, Jesujoba O. and others},
  booktitle = {Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  year      = {2023},
  pages     = {10883--10900},
  publisher = {Association for Computational Linguistics},
  doi       = {10.18653/v1/2023.acl-long.609}
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
| **Tags** | #benchmark #POS #transfer #adapters #MAD-X #LT-SFT #bantu #hausa #swahili #zulu #kinyarwanda #luganda |

## Summary

Releases UD-style POS data for 20 African languages (news domain) and benchmarks CRF and multilingual PLMs; AfroXLMR-large is best (89.4 average accuracy). Zero-shot transfer uses seven non-target sources with UD training data (afr, ara, eng, fra, pcm, ron, wol), plus chiShona (sna) in the appendix, all on AfroXLMR-base, with plain fine-tuning (FT-Eval) and two parameter-efficient methods (MAD-X adapters, LT-SFT). PEFT methods with target language adapters/SFTs beat FT-Eval by over 10 points on average. Wolof transfers best to non-Bantu Niger-Congo targets; chiShona transfers best to Bantu targets.

## Review claim check

No external claim was given for this paper. Task: record AfroXLMR POS numbers and transfer findings (done below). Note: MasakhaPOS has no Amharic.

## Research question / problem

- No large POS dataset across African languages; unclear which source language and which transfer method work for unseen African targets.

## Method

- **Approach:** annotation under UD guidelines; in-language baselines; single and multi-source zero-shot transfer.
- **Model(s) / architecture:** CRF, mBERT, XLM-R base/large, RemBERT, AfroLM, AfriBERTa-large, AfroXLMR base/large. Transfer: AfroXLMR-base only.
- **PEFT method (if any):** MAD-X 2.0 (language + task adapters), LT-SFT (sparse fine-tuning).
- **Languages covered:** bam, bbj, ewe, fon, hau, ibo, kin, lug, luo, mos, nya, pcm, sna, swa, tsn, twi, wol, xho, yor, zul. Sources: afr, ara, eng, fra, pcm, ron, wol, sna.
- **Datasets:** MasakhaPOS; UD treebanks for sources.
- **Tasks:** POS tagging.
- **Evaluation metrics:** accuracy.
- **Compute / hardware:** not detailed in sections read; language adapters trained on small news corpora (433KB-50.2MB).

## Key findings

1. AfroXLMR-large in-language accuracy (Table 2, 5 runs):

| hau | kin | lug | swa | zul | avg (20) |
|---|---|---|---|---|---|
| 93.0 | 98.4 | 91.6 | 93.2 | 90.1 | 89.4 |

2. Zero-shot FT-Eval (plain fine-tuning, AfroXLMR-base) from selected sources (Table 9):

| source | hau | kin | lug | swa | zul |
|---|---|---|---|---|---|
| sna (Bantu) | 60.5 | 73.7 | 75.0 | 63.4 | 67.9 |
| wol (Atlantic) | 55.1 | 49.2 | 51.8 | 42.9 | 45.5 |
| eng | 67.1 | 63.9 | 57.8 | 56.9 | 48.8 |
| ron | 67.3 | 73.3 | 56.9 | 61.0 | 56.3 |

3. sna (Bantu) gives the best transfer to Bantu targets; wol is best for non-Bantu Niger-Congo targets (bbj, ewe, fon, ibo, mos, twi, yor) despite small data. The authors attribute this to shared family and morphology.
4. Average over 20 targets: eng and ron best single sources; eng-ron-wol-sna multi-source gives the best result (LT-SFT 72.1, MAD-X 71.8 average).
5. MAD-X is sensitive to language adapter corpus size: wol news-only adapter gave very poor transfer; adding Wikipedia fixed it.

## What we got from it

- Reference numbers for our POS baselines (no Amharic in MasakhaPOS, so our 6-language POS set must differ or use another source for amh).
- Independent support for our POS Bantu advantage: sna beats wol on all four of our Bantu targets by 18-25 points under FT-Eval.
- But note ron matches sna on kin (73.3 vs 73.7): a non-African source can match a Bantu source for some targets.

## Gaps and limitations

- **Stated by the authors:** one Afro-Asiatic (hau) and one Nilo-Saharan (luo) language only; news domain; POS only, so best sources may differ for other tasks.
- **Our observations:** no African-to-African transfer matrix among MasakhaPOS languages except from sna and wol; no hau, kin, lug, swa or zul as sources; transfer only with AfroXLMR-base; no seeds or CIs on transfer; source data come from UD (different domain and annotators) so source effects are confounded with treebank quality and domain.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** explicit claim that matching family and morphosyntax helps POS transfer, but evidence rests on two African sources (sna, wol); same thin-contrast problem as our Hausa-only non-Bantu contrast.
- **Low-resource / African language angle:** same dataset and target languages as ours.
- **Efficiency / low-cost hardware angle:** shows PEFT (adapters, sparse FT) improves zero-shot POS transfer by more than 10 points over full FT-Eval when target language modules exist. Relevant to our LoRA r=8 vs full FT comparison (LoRA is a task module only, no language module).
- **Baseline or control for us:** **Baseline** (Table 2 numbers; FT-Eval transfer rows for sna, wol, eng, ron).

## Quotes and figures worth citing

> "transferring knowledge from a language that matches the language family and morphosyntactic properties seems more effective for POS tagging" (Abstract)

- Table 2: in-language accuracy per PLM.
- Table 4 / Table 9: zero-shot transfer per source and method (Bantu vs non-Bantu highlighting).
- Fig. 1: average transfer by source and method.

## Related papers to follow up

- [ ] Pfeiffer et al. (2020, 2021) MAD-X
- [ ] Ansell et al. (2022) LT-SFT
- [ ] Alabi et al. (2022) AfroXLMR (MAFT)

## Open questions / discussion points

- Would a LoRA-based analogue of MAD-X (language LoRA + task LoRA) close the Bantu vs non-Bantu POS gap we see?
- Could we add sna and xho as POS sources to get more than one non-Bantu vs Bantu contrast?
