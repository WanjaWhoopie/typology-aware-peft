# Typologically Informed Parameter Aggregation (TIPA)

## Reference

| Field | Details |
|---|---|
| **Title** | Typologically Informed Parameter Aggregation |
| **Authors** | Stef Accou, Wessel Poelman |
| **Year** | 2026 |
| **Venue** | Findings of EACL 2026, pp. 2253-2267 |
| **DOI / URL** | https://aclanthology.org/2026.findings-eacl.119/ |
| **PDF (online)** | https://aclanthology.org/2026.findings-eacl.119.pdf |
| **Code / data** | https://github.com/stefaccou/TIPA |

**Citation (APA):**
> Accou, S., & Poelman, W. (2026). Typologically informed parameter aggregation. In *Findings of the Association for Computational Linguistics: EACL 2026* (pp. 2253-2267). Association for Computational Linguistics. https://aclanthology.org/2026.findings-eacl.119/

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{accou-poelman-2026-tipa,
  title     = {Typologically Informed Parameter Aggregation},
  author    = {Accou, Stef and Poelman, Wessel},
  booktitle = {Findings of the Association for Computational Linguistics: EACL 2026},
  year      = {2026},
  pages     = {2253--2267},
  url       = {https://aclanthology.org/2026.findings-eacl.119/}
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
| **Tags** | #adapters #typology #URIEL #parameter-merging #training-free #SIB-200 #NER #POS #zero-shot |

## Summary

TIPA builds a proxy language adapter for a target language by weight-averaging existing MAD-X language adapters, with weights given by a softmax over URIEL+ typological similarity (1 - distance) to the target. No training is needed; the proxy is plugged into MAD-X with an English-trained task adapter. On XLM-R base, across NER, POS, XCOPA, XQuAD and SIB-200 (234 languages in total), TIPA beats English fine-tuning, MAD-X/closest adapter, "No Train but Gain" and uniform averaging when aggregated over tasks (54.1 vs 50.1 best baseline), with the largest gains on NER and POS and for languages without their own adapter.

## Review claim check

- **Claim:** (question) what it does, languages, results, closeness to a typology-gated LoRA mixture.
- **Verdict:** n/a (descriptive); see below.
- **Evidence:** training-free, typology-weighted, per-language static weighting of bottleneck adapters, not a learned gate and not LoRA. The authors report that preliminary LoRA experiments "did not see strong results" (Limitations, p. 2257).

## Research question / problem

- Can typological similarity be used to construct stand-in language adapters by aggregation, with no language-specific training?

## Method

- **Approach:** URIEL+ distances -> softmax weights -> layer-wise weighted average of adapter weights and biases; optional pruning to top-k or a distance threshold.
- **Model(s) / architecture:** XLM-R base; MAD-X adapters from AdapterHub (pool of 31 languages, Table 6; Swahili is the only Bantu one).
- **PEFT method (if any):** bottleneck language and task adapters (MAD-X).
- **Languages covered:** 234 across tasks; SIB-200 alone 176 languages, including many African ones (e.g. Kinyarwanda, Luganda, Zulu listed in the language tables).
- **Datasets:** WikiANN (NER), UD (POS), XCOPA, XQuAD, SIB-200.
- **Tasks:** NER, POS, COPA, QA, topic classification.
- **Evaluation metrics:** task scores x100, means with std over languages; paired one-tailed t-tests.
- **Compute / hardware:** training-free; inference cost of one adapter.

## Key findings

| Method (Table 2, p. 2255) | ALL (234) | NER (136) | POS (80) | COPA (11) | QA (12) | SIB (176) |
|---|---|---|---|---|---|---|
| English fine-tuning | 45.0 | 39.0 | 38.9 | 55.5 | 53.4 | 61.2 |
| MAD-X / closest adapter | 45.4 | 43.3 | 44.6 | 52.0 | 72.1 | 56.5 |
| No Train but Gain | 50.1 | 49.3 | 46.9 | 50.3 | 72.5 | 61.6 |
| Uniform parameter averaging | 43.1 | 39.5 | 45.4 | 51.5 | 68.6 | 54.3 |
| TIPA | 54.1 | 51.3 | 46.8 | 51.8 | 72.9 | 63.4 |

1. Typology weighting beats uniform averaging by +6.7% (task-aggregated, p < 0.01): the closest thing in this group to a "typology vs no typology" control, and it favours typology.
2. Gains largest on NER and POS; on SIB-200 TIPA is +2.2 over English fine-tuning and +1.8 over No Train but Gain.
3. Morphological URIEL+ features are most informative for NER and POS; all features best overall (Table 7).
4. Standard deviations across languages are large (about 20 points), so aggregate gains hide wide variation.

## What we got from it

- Uniform averaging is a required control for any mixture: it isolates the value of typology-based weights.
- Morphological feature subsets may be better gate inputs for token-level tasks.
- SIB-200 and NER/POS are used, so our task set is comparable in kind.

## Gaps and limitations

- **Stated by the authors:** depends on the adapter pool; hyperparameters tuned heuristically; bibliographic bias; LoRA and decoder LLMs (Gemma, Qwen) did not work well in preliminary tests.
- **Our observations:** zero-shot from English; no in-language data; no shuffled-typology control (uniform averaging removes typology rather than corrupting it); XLM-R base only; aggregate statistics over very different languages.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** very close in spirit: typology decides how modules are mixed. Differences from our plan: static per-language weights vs a learned gate; bottleneck adapters vs LoRA; zero-shot vs supervised plus transfer.
- **Low-resource / African language angle:** SIB-200 includes our languages, but the adapter pool has few African languages (Swahili); Bantu-specific results are not reported separately.
- **Efficiency / low-cost hardware angle:** zero training; ideal cheap baseline.
- **Baseline for us?** Yes. "TIPA for LoRA": average our per-language LoRA modules with URIEL+ softmax weights, training-free. Also run uniform averaging. Their negative LoRA remark is a risk we should test, not assume.

## Quotes and figures worth citing

> "a training-free method that constructs proxy language adapters by aggregating existing ones, weighted by typological similarity." (abstract, p. 2253)

> "preliminary experiments on conditional multilingual language models (Gemma, Qwen) and PEFT methods (LoRa) did not see strong results." (p. 2257)

## Related papers to follow up

- [ ] Klimaszewski et al. 2025, "No Train but Gain: Language arithmetic for training-free language adapters enhancement" (COLING 2025).
- [ ] Khan et al. 2025, URIEL+.
- [ ] Borchert et al. 2025, FLARE (language fusion for PEFT cross-lingual transfer).

## Open questions / discussion points

- Is a learned gate needed at all, or does a training-free typology-weighted LoRA average get most of the benefit? This must be one of our first experiments.
