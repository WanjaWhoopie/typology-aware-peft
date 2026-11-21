# IFCLoRA: Topology-Aware Rank Allocation for Parameter-Efficient Fine-Tuning

## Reference

| Field | Details |
|---|---|
| **Title** | IFCLoRA: Topology-Aware Rank Allocation for Parameter-Efficient Fine-Tuning |
| **Authors** | Wei Zhang, Xinwu Liu, Yihang Cheng |
| **Year** | 2026 |
| **Venue** | arXiv preprint (cs.LG), arXiv:2607.22251 (v2, 7 Aug 2026) |
| **DOI / URL** | https://arxiv.org/abs/2607.22251 |
| **PDF (online)** | https://arxiv.org/pdf/2607.22251 |
| **Code / data** | not linked in the main text (supplementary material mentioned) |

**Citation (APA):**
> Zhang, W., Liu, X., & Cheng, Y. (2026). *IFCLoRA: Topology-aware rank allocation for parameter-efficient fine-tuning* (arXiv:2607.22251). arXiv. https://arxiv.org/abs/2607.22251

<details>
<summary>BibTeX</summary>

```bibtex
@misc{zhang-2026-ifclora,
  title         = {{IFCLoRA}: Topology-Aware Rank Allocation for Parameter-Efficient Fine-Tuning},
  author        = {Zhang, Wei and Liu, Xinwu and Cheng, Yihang},
  year          = {2026},
  eprint        = {2607.22251},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | Low (Medium for the planned layer-wise rank allocation) |
| **Tags** | #LoRA #rank-allocation #layer-wise #controls |

## Summary

IFCLoRA allocates LoRA ranks across modules before fine-tuning. On a small calibration set it traces interventions in the frozen model, builds a graph whose nodes are LoRA target modules, and scores each by Information-Flow Centrality (graph reachability fused with gradient sensitivity). Ranks are then allocated once under a total budget, and adapters are initialised in traced response directions (FlowInit). On LLaMA-3.1-8B and LLaMA-2-7B, at r = 8, it beats standard LoRA on GSM8K (+4.75 and +13.54 points), MT-Bench and HumanEval, with similar time and memory (3h32m vs 3h29m on an A800).

## Review claim check

- **Claim:** "topology-aware (information-flow graph), not typology-aware; evaluated on tasks such as GSM8K; not a linguistic baseline".
- **Verdict:** holds.
- **Evidence:** "topology" refers to the module interaction graph of the network; evaluation is GSM8K, MT-Bench and HumanEval on LLaMA models, 3 seeds; no languages or linguistic features involved.

## Research question / problem

- How to distribute a limited LoRA rank budget across modules using global, task-conditioned structure rather than local statistics.

## Method

- **Approach:** intervention tracing -> sparse interaction graph -> IFC score -> one-shot discrete rank allocation; FlowInit initialisation.
- **Model(s) / architecture:** LLaMA-3.1-8B, LLaMA-2-7B (decoder LLMs).
- **PEFT method (if any):** LoRA with non-uniform ranks; compared with AdaLoRA, PiSSA, OLoRA, LoRA-GA, GoRA.
- **Languages covered:** English only.
- **Datasets:** MetaMathQA / GSM8K, instruction following (MT-Bench), code (HumanEval).
- **Tasks:** maths reasoning, instruction following, code generation.
- **Evaluation metrics:** accuracy, MT-Bench score, pass@1; mean and std over 3 seeds.
- **Compute / hardware:** A800 GPUs; about 44 GB peak memory.

## Key findings

1. GSM8K at r = 8: +4.75 (LLaMA-3.1-8B) and +13.54 (LLaMA-2-7B) points over LoRA.
2. Topology-only allocation beats sensitivity-only; fused score best.
3. Shuffling the learned ranks across modules (topology permutation control) lowers accuracy: 71.14 vs 68.84 (LLaMA-3.1-8B) and 51.66 vs 46.37 (LLaMA-2-7B), p. 6.
4. Learned rank profiles differ by layer, projection, task and base model.

## What we got from it

- The permutation control (same rank multiset, shuffled placement) is the right control for our layer-wise rank allocation work.
- Evidence that q/k/v/o and layers deserve different ranks, relevant to our fixed r = 8 on query/value.

## Gaps and limitations

- **Stated by the authors:** needs an offline calibration stage; r = 16 experiments only on GSM8K.
- **Our observations:** decoder LLMs, English, generation tasks; nothing about encoders, sequence labelling or multilingual transfer. Preprint, not peer reviewed.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none.
- **Low-resource / African language angle:** none.
- **Efficiency / low-cost hardware angle:** pre-fine-tuning allocation with near-zero training overhead; useful for later layer-wise rank allocation.
- **Baseline for us?** No for RQ3. Possibly for the later rank-allocation study (with AdaLoRA as the simpler standard baseline).

## Quotes and figures worth citing

> "the original placement achieves higher means than the shuffled placement" (p. 6)

- Figure 5: per-layer, per-projection rank profiles.

## Related papers to follow up

- [ ] Zhang et al. 2023, AdaLoRA.

## Open questions / discussion points

- Would task-conditioned rank profiles for NER differ between Bantu languages? Could typology predict rank profiles? (Speculative.)
