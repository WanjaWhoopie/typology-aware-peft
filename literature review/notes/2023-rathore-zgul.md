# ZGUL: Zero-shot Generalization to Unseen Languages using Multi-source Ensembling of Language Adapters

## Reference

| Field | Details |
|---|---|
| **Title** | ZGUL: Zero-shot Generalization to Unseen Languages using Multi-source Ensembling of Language Adapters |
| **Authors** | Vipul Rathore, Rajdeep Dhingra, Parag Singla, Mausam |
| **Year** | 2023 |
| **Venue** | EMNLP 2023, pp. 6969-6987 |
| **DOI / URL** | https://doi.org/10.18653/v1/2023.emnlp-main.431 |
| **PDF (online)** | https://aclanthology.org/2023.emnlp-main.431.pdf |
| **Code / data** | https://github.com/dair-iitd/ZGUL |

**Citation (APA):**
> Rathore, V., Dhingra, R., Singla, P., & Mausam. (2023). ZGUL: Zero-shot generalization to unseen languages using multi-source ensembling of language adapters. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 6969-6987). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.emnlp-main.431

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{rathore-etal-2023-zgul,
  title     = {{ZGUL}: Zero-shot Generalization to Unseen Languages using Multi-source Ensembling of Language Adapters},
  author    = {Rathore, Vipul and Dhingra, Rajdeep and Singla, Parag and Mausam},
  booktitle = {Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing},
  year      = {2023},
  pages     = {6969--6987},
  doi       = {10.18653/v1/2023.emnlp-main.431}
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
| **Tags** | #adapters #AdapterFusion #lang2vec #typology #MasakhaNER #kinyarwanda #luganda #swahili #zero-shot #few-shot |

## Summary

ZGUL combines frozen language adapters (LAs) of several related source languages at train and test time. Each layer has a FUSION network (token-level attention over LAs, as in AdapterFusion) and a LANG2VEC network (attention over LAs using lang2vec syntax features of the input language), whose outputs are concatenated and fed to a task adapter; entropy minimisation tunes the attention weights at test time. On 15 languages unseen by mBERT in four groups, it beats baselines on 10 of 15. For the African NER group it gains +0.9 F1 average over plain multi-source fine-tuning (SFT-M), but loses to SFT-M on Kinyarwanda and Luganda. It also helps with some unlabeled target data and in few-shot (10 to 100 examples).

## Review claim check

- **Claim:** "ensembles adapters from related source languages, with an African group on MasakhaNER and a few-shot setting".
- **Verdict:** holds.
- **Evidence:** African group: sources English, Amharic, Swahili, Wolof; targets Hausa, Igbo, Kinyarwanda, Luganda, Luo, Nigerian Pidgin on MasakhaNER (Table 1, p. 6973); few-shot bins of 10, 30, 70, 100 target examples (p. 6976). Note the gain is modest (+0.9 avg) and negative for Kinyarwanda and Luganda.

## Research question / problem

- Zero-shot transfer to languages unseen by the PLM and without unlabeled data, by leveraging multiple related source LAs at train and test time.

## Method

- **Approach:** FUSION + LANG2VEC attention over frozen source LAs in every layer, a task adapter on top, entropy-minimisation (EM) tuning of attention at inference.
- **Model(s) / architecture:** mBERT; pretrained LAs from AdapterHub.
- **PEFT method (if any):** bottleneck language adapters (frozen) + trainable task adapter and fusion modules.
- **Languages covered:** Germanic and Slavic (POS), African and Indo-Aryan (NER); 15 targets.
- **Datasets:** MasakhaNER (v1), WikiANN, UD 2.5.
- **Tasks:** NER, POS.
- **Evaluation metrics:** F1, mean of 3 seeds; McNemar tests.
- **Compute / hardware:** not a focus. NER trained up to 10 epochs.

## Key findings

African NER zero-shot F1 (Table 3, p. 6974):

| Method | hau | ibo | kin | lug | luo | pcm | avg |
|---|---|---|---|---|---|---|---|
| SFT-En (English only) | 43.2 | 47.1 | 49.1 | 47.5 | 29.0 | 64.4 | 46.7 |
| SFT-M (multi-source fine-tuning) | 51.3 | 55.7 | 57.9 | 56.0 | 36.0 | 65.0 | 53.7 |
| CPG (UDapter-style generator) | 49.0 | 51.1 | 55.1 | 54.0 | 34.2 | 65.7 | 51.5 |
| ZGUL | 53.6 | 56.8 | 56.2 | 54.2 | 40.2 | 66.5 | 54.6 |
| ZGUL w/o LANG2VEC | 49.0 | 54.7 | 57.3 | 53.5 | 35.5 | 65.5 | 52.6 |

1. Multi-source training is the biggest single factor (English-only is 7 points lower on average for African NER).
2. Removing the lang2vec part costs 2.0 F1 on average (54.6 -> 52.6), but helps Kinyarwanda without it.
3. Plain multi-source fine-tuning (SFT-M) beats the CPG typology generator on NER; the authors attribute this to CPG's large parameter count and small NER data.
4. Few-shot: ZGUL stays ahead of baselines up to 100 examples; curves have not plateaued. Exact few-shot numbers are only in figures/appendix.

## What we got from it

- SFT-M (fine-tune on pooled related source languages) is a strong, cheap baseline that typology-aware methods barely beat; we must include it.
- Learned attention over source adapters correlates with syntactic/genetic similarity (Table 4: lang2vec network r = 0.61 for the African group), a useful interpretability check for our gate.

## Gaps and limitations

- **Stated by the authors:** needs pretrained LAs (Wikipedia-based); unseen scripts not handled; only token-level tasks tested.
- **Our observations:** mBERT base; MasakhaNER v1; zero-shot setting, while we have in-language data. No random or shuffled lang2vec control; "w/o LANG2VEC" removes the module rather than corrupting its input.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** typology (lang2vec syntax) used as gate input over adapters, the closest architecture to our gated mixture among adapter papers.
- **Low-resource / African language angle:** includes Kinyarwanda and Luganda as targets, Swahili as source.
- **Efficiency / low-cost hardware angle:** frozen LAs, light trainable parts.
- **Baseline for us?** Yes. SFT-M (pooled multi-source full fine-tuning and pooled multi-source LoRA) is mandatory; a ZGUL-style fusion over our per-language LoRAs is a reasonable stronger baseline.

## Quotes and figures worth citing

> "For NER, ZGUL achieves decent gains of 3.2 points and 0.9 points for the Indo-Aryan and the African groups respectively over the closest baseline" (p. 6973)

- Table 3 (p. 6974): African NER per language.
- Table 4: correlation of learned attention with language similarity.

## Related papers to follow up

- [ ] Wang et al. 2021, EMEA (entropy-minimised ensembling of adapters).
- [ ] Pfeiffer et al. 2021, AdapterFusion.

## Open questions / discussion points

- Gains over SFT-M are small and uneven; a typology gate for Bantu must beat pooled multi-source LoRA, not just single-language LoRA.
