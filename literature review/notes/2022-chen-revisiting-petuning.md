# Revisiting Parameter-Efficient Tuning: Are We Really There Yet?

## Reference

| Field | Details |
|---|---|
| **Title** | Revisiting Parameter-Efficient Tuning: Are We Really There Yet? |
| **Authors** | Guanzheng Chen, Fangyu Liu, Zaiqiao Meng, Shangsong Liang |
| **Year** | 2022 |
| **Venue** | EMNLP 2022, pp. 2612-2626 |
| **DOI / URL** | https://doi.org/10.18653/v1/2022.emnlp-main.168 |
| **PDF (online)** | https://aclanthology.org/2022.emnlp-main.168.pdf |
| **Code / data** | https://github.com/guanzhchen/PETuning |

**Citation (APA):**
> Chen, G., Liu, F., Meng, Z., & Liang, S. (2022). Revisiting parameter-efficient tuning: Are we really there yet? In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing* (pp. 2612-2626). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.emnlp-main.168

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{chen-etal-2022-revisiting,
  title     = {Revisiting Parameter-Efficient Tuning: Are We Really There Yet?},
  author    = {Chen, Guanzheng and Liu, Fangyu and Meng, Zaiqiao and Liang, Shangsong},
  booktitle = {Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing},
  year      = {2022},
  pages     = {2612--2626},
  doi       = {10.18653/v1/2022.emnlp-main.168}
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
| **Tags** | #LoRA #adapters #PEFT-behaviour #evaluation #seeds #training-length #low-resource |

## Summary

The paper re-evaluates Adapter, prefix tuning, LoRA and BitFit against full fine-tuning on 12 GLUE/SuperGLUE tasks with RoBERTa-base, fixing a flawed protocol where the same dev set was used for early stopping and reporting. Under a fair protocol (new dev split from train, original dev as test, 20 seeds for low/medium tasks, 10 for high, up to 50 epochs with early stopping), PEFT beats full fine-tuning only on low-resource tasks (under 1k examples), is at best comparable on medium tasks (1k to 10k), and loses on high-resource tasks. All methods are unstable across seeds; instability is driven by the number of training iterations, not data size per se.

## Review claim check

- **Claim:** "parameter-efficient tuning may be more suitable for low-resource tasks but struggles on medium-resource tasks; low = up to 1k examples, medium = 1k to 10k".
- **Verdict:** holds.
- **Evidence:** Key finding 1 (p. 2613) states this almost verbatim; bands are low (< 1k: CB, COPA, WSC), medium (1k to 10k: RTE, MRPC, WiC, STS-B, BoolQ), high (> 10k). For medium tasks, "only Adapter and BitFit" stay comparable while "LoRA and prefix tuning lags behind substantially".

## Training length, epochs and seed instability (for our NER question)

- **Protocol:** up to 50 epochs, early stop when eval loss does not improve for 10 epochs (p. 2615); 20 seeds (low/medium), 10 seeds (high).
- **Instability:** every PEFT method is unstable across seeds, like full fine-tuning; both weight init and data order contribute.
- **Iterations, not data size:** with steps matched, 1k and 2k training sets give the same std; std falls as training steps grow (Figure 6, p. 2619). With a fixed number of epochs, small datasets get few iterations and stay unstable.
- **Parameters:** fewer trainable parameters gives more stability, but the smallest configuration is not the best; they conjecture small-parameter models "converge quickly" but may underfit.
- **Recommendation implied:** prolong training iterations to stabilise PEFT.
- **Protocol warning:** using the same set for early stopping and testing inflates PEFT scores (RTE example, Table 1).

## Method

- **Approach:** controlled re-benchmark with a clean dev/test split and many seeds; significance tests.
- **Model(s) / architecture:** RoBERTa-base.
- **PEFT method (if any):** Adapter, prefix tuning, LoRA, BitFit.
- **Languages covered:** English.
- **Datasets:** 12 GLUE/SuperGLUE tasks.
- **Tasks:** sentence/pair classification and regression (no token-level tasks).
- **Evaluation metrics:** task metrics; mean and std over seeds; t-tests.
- **Compute / hardware:** not a focus.

## Key findings

1. Low-resource: Adapter, LoRA and BitFit beat full fine-tuning (LoRA about +8% average).
2. Medium-resource: Adapter and BitFit comparable; LoRA and prefix tuning substantially behind.
3. High-resource: full fine-tuning best across the board.
4. Instability is tied to training iterations; prefix tuning needs a longer "ascent stage".

## What we got from it

- Our SIB-200 (701 items, LoRA +0.7) and POS (about 750 sentences, LoRA -0.8) results sit in their low band; our NER (5k to 8k sentences, LoRA -3.3) sits in their medium band where LoRA specifically lagged. Superficially consistent with a data-size story.
- But their gaps are measured after up to 50 epochs with early stopping, and they argue the real driver of instability is iterations. Our NER runs used 5 epochs with most runs peaking in the last epoch, so our gap may partly be undertraining. Our within-NER pattern (Amharic, 1,750 sentences, -4.7; Swahili, 6,593, -1.0) also fits an iterations story better than a data-size story: with fixed epochs, the smallest set gets the fewest steps.
- Action: rerun NER LoRA with step-matched or much longer training plus early stopping on a separate dev set, and at least 3 to 5 seeds.

## Gaps and limitations

- **Stated by the authors:** focus on RoBERTa-base and GLUE/SuperGLUE.
- **Our observations:** English sentence classification only; "examples" are sentences or pairs, not token-labelled sentences, so mapping our NER sentence counts onto their bands is approximate. No multilingual or larger models.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none.
- **Low-resource / African language angle:** indirect; supports PEFT in very small data regimes like SIB-200 and MasakhaPOS.
- **Efficiency / low-cost hardware angle:** warns that PEFT savings come with seed instability; budget for multiple seeds.
- **Baseline for us?** No (methodology paper). Adopt its protocol: separate dev for early stopping, many seeds, report mean and std.

## Quotes and figures worth citing

> "PETuning may be more suitable for low-resource tasks, but struggle on medium-resource tasks and fall behind finetuning across the board on high-resource tasks" (p. 2613)

> "reducing trainable parameters and prolonging training iterations may lead to higher stability in PETuning methods." (abstract, p. 2612)

- Figure 1: relative PEFT vs FT performance by data size.
- Figure 6: std vs training steps for 1k and 2k data.

## Related papers to follow up

- [ ] Mosbach et al. 2021, on the stability of fine-tuning BERT.
- [ ] Dodge et al. 2020, fine-tuning seeds and early stopping.
- [ ] He et al. 2021, effectiveness of adapter-based tuning (low-resource advantage).

## Open questions / discussion points

- Does the NER LoRA gap close when LoRA is trained to convergence (e.g. 20+ epochs, higher learning rate)? This decides whether "data size" or "undertraining" goes in the thesis.
