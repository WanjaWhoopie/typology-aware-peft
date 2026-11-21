# A Systematic Analysis of Subwords and Cross-Lingual Transfer in Multilingual Translation

## Reference

| Field | Details |
|---|---|
| **Title** | A Systematic Analysis of Subwords and Cross-Lingual Transfer in Multilingual Translation |
| **Authors** | Francois Meyer, Jan Buys |
| **Year** | 2024 |
| **Venue** | Findings of the Association for Computational Linguistics: NAACL 2024, pp. 2194-2200 |
| **DOI / URL** | https://aclanthology.org/2024.findings-naacl.141 |
| **PDF (online)** | [ACL Anthology](https://aclanthology.org/2024.findings-naacl.141.pdf) |
| **Code / data** | WMT22 African MT data; FLORES for validation/test |

**Citation (APA):**
> Meyer, F., & Buys, J. (2024). A systematic analysis of subwords and cross-lingual transfer in multilingual translation. In *Findings of the Association for Computational Linguistics: NAACL 2024* (pp. 2194-2200). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{meyer-buys-2024-systematic,
  title     = {A Systematic Analysis of Subwords and Cross-Lingual Transfer in Multilingual Translation},
  author    = {Meyer, Francois and Buys, Jan},
  booktitle = {Findings of the Association for Computational Linguistics: NAACL 2024},
  year      = {2024},
  pages     = {2194--2200},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2024.findings-naacl.141}
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
| **Tags** | #tokenization #orthography #transfer #MT #bantu #siswati #setswana #isixhosa #morphology |

## Summary

Short paper on English-to-X translation into four South African languages. Siswati is the low-resource target; isiXhosa (closely related, conjunctive), Setswana (related, agglutinative, disjunctive orthography) and Afrikaans (unrelated, analytic, disjunctive) are paired with it. They compare subword methods (BPE, ULM, SSMT, OBPE, XBPE) in trilingual training (synergy/interference) and in fine-tuning a pretrained bilingual model on a new direction. ULM gives the most synergy in multilingual training; BPE transfers best in fine-tuning. Setswana helps Siswati least, less even than unrelated Afrikaans, which they attribute to its disjunctive orthography.

## Review claim check

- **Claim:** "differences in orthographic word boundary conventions (the morphological granularity of written words) may impede cross-lingual transfer more significantly than linguistic unrelatedness"; Setswana is the disjunctive example.
- **Verdict: holds** (as the authors' hedged claim). The sentence is in the abstract nearly verbatim (p. 2194), and Sec. 5.3 (p. 2197) uses Setswana vs Afrikaans as the evidence. Caveat: it rests on one target (Siswati), one language per condition, chrF++ from single small MT models trained from scratch, with no seeds reported.

## Research question / problem

- Which subword methods promote synergy and cross-lingual transfer in multilingual MT, and how do relatedness, morphology and orthographic word boundaries interact with them?

## Method

- **Approach:** (1) bilingual vs trilingual models, synergy = relative chrF++ change; (2) pretrain en->xh/ts/af, fine-tune on en->ss.
- **Model(s) / architecture:** MT models trained from scratch (no pretrained multilingual encoder).
- **PEFT method (if any):** none.
- **Languages covered:** English to Siswati (ss), isiXhosa (xh), Setswana (ts), Afrikaans (af).
- **Datasets:** WMT22 (training, en->xh/ts/af subsampled to the en->af size), FLORES (dev/test). Removed English sentences shared with en->ss to avoid multi-parallel overlap.
- **Tasks:** machine translation.
- **Evaluation metrics:** chrF++.
- **Compute / hardware:** UCT HPC; details in their appendix.

## Key findings

1. ULM (subword regularisation) gives the most synergy for en->ss in trilingual models.
2. BPE transfers best in cross-lingual fine-tuning; ULM is a barrier there.
3. Synergy for Siswati: isiXhosa > Afrikaans > Setswana, for all subword methods.
4. Trilingual chrF++ on en->ss (Table 3, BPE): with xh 33.4, with af 28.2, with ts 22.5.

## What we got from it

- A concrete, measurable typology-adjacent variable: orthographic word granularity (conjunctive vs disjunctive). It is visible from raw text (e.g. mean word length, morphemes per orthographic word).
- Warns that "Bantu vs non-Bantu" may be the wrong contrast; within Bantu, conjunctive vs disjunctive writing could matter more.

## Gaps and limitations

- **Stated by the authors:** only English to four South African languages; conclusions may not hold for other families or orthographies; did not study languages with several orthographies.
- **Our observations:** one target, one contrast per factor, so relatedness, orthography and morphology are each represented by a single language; no statistical test; MT from scratch, not a pretrained encoder; effects on NER/POS untested.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** supports adding orthographic word granularity as a typology feature or covariate. Our four Bantu languages are all conjunctive, so we cannot test this inside our current set.
- **Low-resource / African language angle:** Southern Bantu languages; Setswana is in MasakhaNER 2.0 and MasakhaPOS (tsn), so it could be added as a disjunctive Bantu contrast.
- **Efficiency / low-cost hardware angle:** none.
- **Baseline or control for us:** **Control / covariate** (orthographic granularity), not a baseline.

## Quotes and figures worth citing

> "differences in orthographic word boundary conventions (the morphological granularity of written words) may impede cross-lingual transfer more significantly than linguistic unrelatedness" (p. 2194)

- Table 1: language selection matrix (family, morphology, orthography).
- Fig. 3: fine-tuning transfer chrF++ per subword method.

## Related papers to follow up

- [ ] Pretorius et al. (2009), Setswana tokenisation and disjunctive orthography
- [ ] Taljard & Bosch (2006), conjunctive vs disjunctive Bantu tagging
- [ ] Shaham et al. (2023), causes of interference in multilingual MT

## Open questions / discussion points

- In MasakhaNER 2.0 Fig. 5, tsn as a source gives 64 F1 on kin and 44 on zul (mDeBERTaV3); is that lower than other Bantu sources once target effects are removed?
