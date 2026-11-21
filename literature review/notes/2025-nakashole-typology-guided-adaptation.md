# Typology-Guided Adaptation in Multilingual Models

## Reference

| Field | Details |
|---|---|
| **Title** | Typology-Guided Adaptation in Multilingual Models |
| **Authors** | Ndapa Nakashole |
| **Year** | 2025 |
| **Venue** | ACL 2025 (63rd Annual Meeting, Vol. 1: Long Papers), Vienna, pp. 21819-21835. Outstanding Paper award |
| **DOI / URL** | https://doi.org/10.18653/v1/2025.acl-long.1059 |
| **PDF (online)** | [ACL Anthology (open access)](https://aclanthology.org/2025.acl-long.1059.pdf) |
| **Code / data** | https://github.com/okalai-ai/moimoe (DictionaryNCR and WikiNCR datasets, per the paper) |

**Citation (APA):**
> Nakashole, N. (2025). Typology-guided adaptation in multilingual models. In *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 21819–21835). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.acl-long.1059

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{nakashole-2025-typology,
  title     = {Typology-Guided Adaptation in Multilingual Models},
  author    = {Nakashole, Ndapa},
  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  month     = jul,
  year      = {2025},
  address   = {Vienna, Austria},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2025.acl-long.1059/},
  doi       = {10.18653/v1/2025.acl-long.1059},
  pages     = {21819--21835}
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
| **Tags** | #typology #mixture-of-experts #routing #bantu #swahili #zulu #luganda #morphology #noun-class #low-resource |

## Summary

The paper defines a Morphological Index (MoI) for Bantu languages: the total number of characters in a language's noun class prefixes (classes 1 to 15), taken from grammar and dictionary prefix tables. It introduces noun class recognition (NCR: predict the noun class of a single dictionary noun, given the noun and its English gloss) and builds two datasets (DictionaryNCR, about 63K nouns, 10 languages; WikiNCR, 2.6K nouns, 3 languages). The model is mT5-XL fine-tuned on "noun + gloss -> class"; MoI-MoE has two experts (High-MoI, Low-MoI) and a fixed, non-learned router that sends each language to an expert by an MoI cutoff of 50. MoI-MoE averages 92.0% accuracy over 8 languages vs 89.9% for one multilingual model and 79.8% for a token-overlap router. MoI correlates with rule-based accuracy (r = 0.75) and negatively with the gain from adding semantics (r = -0.736).

## Review claim check

- **Claim:** "the typology index is hand-computed from grammar-book prefix tables; the model is fully fine-tuned mT5-XL with a non-learned router; the task is noun-class recognition on dictionary entries (pp. 3 to 6)".
- **Verdict:** holds (one small caveat).
- **Evidence:** MoI is the summed character length of prefixes listed in grammar-derived tables (p. 21821; Table 8, p. 21831); the router is "non-learned" (p. 21820) and "nonparametric" (p. 21824); the task is NCR on DictionaryNCR (pp. 21822-21824), i.e. paper pages 3 to 6. Caveat: the paper says "we fine-tune mT5-XL (3.7B parameters)" and mentions no PEFT, so "full" fine-tuning is the natural reading but is not stated in those words.

## Research question / problem

- Can linguistic structure (how strongly noun class is marked by prefixes) guide how a multilingual model shares parameters, instead of genealogy or token overlap?
- Argues that coarse databases (WALS, lang2vec) are too sparse to separate languages inside Bantu.

## Method

- **Approach:** compute MoI per language; split languages into High-MoI and Low-MoI with a cutoff of 50 chosen on validation data; train one expert per regime; route by MoI at inference (hard, per-language routing).
- **Model(s) / architecture:** mT5-XL (3.7B), seq2seq; prompt "Given the Bantu noun [X] whose English meaning is [Y], predict its noun class". Language name in the prompt hurt performance.
- **PEFT method (if any):** none described. How the two experts are built (two separate fine-tuned copies, or shared body) is not spelled out in the main text.
- **Languages covered:** 10 Bantu: Swahili, Ndonga, Xhosa, Zulu, Luganda, Shona, Kwanyama, Umbundu (train and test), Herero and Sotho (zero-shot only). No Kinyarwanda.
- **Datasets:** DictionaryNCR (scanned dictionaries, OCR via MathPix, parsing with GPT-4; classes inferred from prefixes for 5 languages without explicit labels); WikiNCR (Wiktionary; Swahili, Xhosa, Zulu) for out-of-domain test. English glosses expanded by GPT-4.
- **Tasks:** NCR (context-free, single noun); small add-on: Swahili MasakhaPOS with noun-class-specific NP tags.
- **Evaluation metrics:** accuracy; Pearson correlations of MoI with rule-based accuracy and with semantic gain.
- **Compute / hardware:** 4x NVIDIA A40, under 5 hours; lr 5e-5, batch 16, FP16; balanced language sampling (alpha 0.7).

## Key findings

| Model (Table 5, p. 21825) | Swahili | Zulu | Luganda | Avg (8 langs) |
|---|---|---|---|---|
| Rule-based (prefix rules) | 48.73 | 80.00 | 45.13 | 71.20 |
| MORPH (noun only, no gloss) | 80.07 | 92.78 | 77.70 | 87.99 |
| NCR-0 (noun + gloss, one model) | 95.14 | 88.57 | 80.29 | 89.91 |
| TO-MoE (token-overlap router) | 94.13 | 92.48 | 46.91 | 79.8 |
| MoI-MoE | 94.80 | 92.48 | 84.57 | 92.00 |

1. MoI-MoE gives the best average (92.0) but the gain over the single multilingual model is about +2.1 points; the headline "+14 points on Swahili" is vs the morphology-only model, and on Swahili MoI-MoE (94.80) is slightly below NCR-0 (95.14).
2. MoI tracks morphological reliance: rule-based accuracy r = 0.75 with MoI; semantic gain r = -0.736. Removing augments weakens but does not remove the correlations (augmentless MoI-MoE 91.11%).
3. Ablations: no subword tokenization drops average to 24.13; masking prefixes to 34.61 (vs 87.99), so prefix subwords drive the prediction.
4. Zero-shot (Table 11): Sotho 60.56 vs 52.11, Herero 74.12 vs 71.90 (MoE vs single model).
5. Domain shift is large: Swahili 94.8 -> 75.1, Zulu 92.5 -> 76.1 on WikiNCR.
6. Swahili POS with noun-class tags on AfroXLMR-large: 93.5 -> 91.7 accuracy (about 800 sentences); the text calls this "only a 1.0% drop", which does not match the table (1.8 points).

## What we got from it

- A concrete, cheap, Bantu-specific typology feature (MoI) that we could add to our router input next to URIEL/lang2vec vectors; values for Swahili, Zulu and Luganda are derivable from Table 8.
- Their TO-MoE (token-overlap routing) is a useful non-typological routing baseline idea for us.
- Confirms AfroXLMR-large is a reasonable POS backbone for Swahili (93.2 to 93.5 reported).

## Gaps and limitations

- **Stated by the author:** hard routing may miss intermediate cases, soft routing could help; only 10 of 500+ Bantu languages; MoI only covers noun class prefixes; other tasks (parsing, MT, LM) untested.
- **Our observations:**
  - Routing is per language and deterministic, so MoI-MoE is effectively two language-group models; there is no learned gate and no token-level routing.
  - No random-routing or shuffled-MoI control, so the gain over NCR-0 is not attributed to typology versus simply splitting languages into two groups.
  - No seeds or variance reported; differences of 1 to 2 points are untested.
  - Task is word-level classification on dictionary entries with English glosses; it says nothing about sentence-level tasks (NER, POS, SIB-200) beyond a one-language POS add-on.
  - No PEFT and a 3.7B model: not low-cost.

## Relevance to typology-aware PEFT

**Why it is on the list:** closest prior work to our RQ3 (typology-gated mixture of LoRA adapters). It proposes MoI and MoI-MoE, a Mixture-of-Experts model routed by morphological structure, evaluated on 10 Bantu languages.

- **Morphology / typology angle:** shows that a fine-grained morphological index separates Bantu languages better than token overlap for a morphology-heavy task. Our differences: (a) LoRA experts on a frozen AfroXLMR-large-76L instead of fine-tuned mT5-XL; (b) a learned, soft gate conditioned on typological features (and possibly MoI) rather than a fixed cutoff; (c) downstream benchmarks (MasakhaNER 2.0, MasakhaPOS, SIB-200); (d) transfer to related unseen languages with explicit shuffled-typology and random-gate controls. The author states MoI "complements modular approaches such as adapters and LoRA" (p. 21820), but does not test that, which is our gap.
- **Low-resource / African language angle:** covers three of our four languages (Swahili, Zulu, Luganda; not Kinyarwanda). MoI places Swahili as Low-MoI and Zulu/Kwanyama as High-MoI.
- **Efficiency / low-cost hardware angle:** none; full model on 4 A40s. Our LoRA mixture is the efficient counterpart.
- **Baseline for us?** Not directly runnable on our tasks (NCR is a different task). Reuse two ideas as baselines: a hard MoI-cutoff router over our LoRA experts, and a token-overlap router. Use MoI as an extra router feature.

## Quotes and figures worth citing

> "A lightweight, non-learned router uses MoI to select the appropriate expert, enabling typology-driven inference." (p. 21820)

> "MoI requires only a list of noun class prefixes, which are well-documented in grammar books and comparative studies of Bantu languages" (p. 21821)

> "it relies on hard routing based on MoI, which may not fully account for intermediate cases. A soft routing strategy could enhance flexibility." (Limitations, p. 21828)

- Table 5 (p. 21825): per-language NCR accuracy for all baselines and MoI-MoE.
- Table 8 (p. 21831): prefix tables used to compute MoI.
- Figures 6 and 7: MoI vs rule-based accuracy (r = 0.75) and vs semantic gain (r = -0.736).

## Related papers to follow up

- [ ] Üstün et al. 2022, UDapter journal version (Computational Linguistics 48(3)), cited here as the typology-adapter reference.
- [ ] Ogunremi et al. 2023, BantuBERTa / "Mini but mighty" (linguistically informed data selection).
- [ ] Byamugisha et al. 2018, pluralizing nouns across agglutinating Bantu languages.

## Open questions / discussion points

- Does MoI add anything over URIEL features in a learned gate on NER/POS, or is it only informative for noun-class tasks?
- Would a 2-group hard split of our languages (by MoI) already capture most of a learned typology gate's benefit? This is a cheap ablation we should run.
- With only 4 training languages, can any learned gate be trained without overfitting? MoI-MoE sidesteps this by not learning the router.
