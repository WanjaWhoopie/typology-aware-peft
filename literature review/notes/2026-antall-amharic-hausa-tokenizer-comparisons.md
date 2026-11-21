# What Do Tokenizer Comparisons Measure? Disentangling Granularity, Root Assignment, and Word-Level Readout across Amharic and Hausa

## Reference

| Field | Details |
|---|---|
| **Title** | What Do Tokenizer Comparisons Measure? Disentangling Granularity, Root Assignment, and Word-Level Readout across Amharic and Hausa |
| **Authors** | Abdul Rehman Antall, Baidya Nath Saha |
| **Year** | 2026 |
| **Venue** | arXiv preprint 2611.14818 (v1, 10 Nov 2026) |
| **DOI / URL** | https://doi.org/10.48550/arXiv.2611.14818 |
| **PDF (online)** | https://arxiv.org/pdf/2611.14818 |
| **Code / data** | No code link found in the main text; data: MasakhaNER 1.0, OPUS-100, UniMorph, HornMorpho |

**Citation (APA):**
> Antall, A. R., & Saha, B. N. (2026). What do tokenizer comparisons measure? Disentangling granularity, root assignment, and word-level readout across Amharic and Hausa. *arXiv preprint arXiv:2611.14818*. https://doi.org/10.48550/arXiv.2611.14818

<details>
<summary>BibTeX</summary>

```bibtex
@article{antall2026tokenizercomparisons,
  title   = {What Do Tokenizer Comparisons Measure? Disentangling Granularity, Root Assignment, and Word-Level Readout across {A}mharic and {H}ausa},
  author  = {Antall, Abdul Rehman and Saha, Baidya Nath},
  year    = {2026},
  journal = {arXiv preprint arXiv:2611.14818},
  doi     = {10.48550/arXiv.2611.14818}
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
| **Tags** | #tokenization #morphology #scrambled-control #amharic #hausa #NER #methodology |

## Summary

A morphology-aware tokenizer changes three things at once compared with BPE: granularity (finer segmentation), root assignment (forms of one root share a token), and, for token-level tasks, how much the word-level readout (first sub-token vs mean pool) matters. The paper separates them with controls that change one factor at a time, using a lossless root-and-pattern tokenizer for Amharic (Ge'ez) and Hausa as a Latin-script contrast, in two independent implementations. Real roots beat scrambled roots on Amharic NER in both (+4.9 and +4.7 F1); readout choice can reverse every tokenizer-vs-BPE comparison in tiny from-scratch models but matters under 1 F1 in XLM-R and AfroXLM-R; the granularity effect changes sign across languages and implementations.

## Review claim check

- **Claim:** "real roots beat scrambled roots for Amharic NER".
- **Verdict:** holds, within a narrow scope.
- **Evidence:** Study I +4.86 F1 [3.14, 6.69] and Study II +4.65 [3.01, 6.33], positive in all five seeds (p. 6). But this is in about 1M to 2M-parameter models trained from scratch on 1,750 sentences with absolute F1 around 16 to 29; the root effect was not tested in pretrained encoders.

## The scrambled-control design (to copy)

- **Decomposition:** S(T) - S(B) = [S(T') - S(B)] (granularity) + [S(T) - S(T')] (root assignment), where T' is a trained reference with the same vocabulary and fertility as T but morphology-blind roots. A two-arm study (T vs B) cannot identify the split (their Proposition 1).
- **What every root control keeps fixed:** prefix, template and suffix tokens of every word; only the root token is replaced. So token inventory size, tokens per word, fertility, parameter count and token positions are identical to the real tokenizer.
- **Scrambled control:** each analysable word TYPE gets a root identifier drawn uniformly at random (consistent per type across the corpus). Breaks the link between related words; identifiers end up with roughly equal numbers of word types.
- **Permuted control:** shuffle the real root assignments among word types, so each identifier keeps its exact type count (preserves the skewed real root frequency profile) but the word-root link is destroyed.
- **Stratified permuted control:** shuffle only within corpus-frequency deciles, so frequent words keep frequent identifiers.
- **Reading the contrasts:** real minus scrambled = root effect; permuted minus scrambled = how much frequency profile alone could explain.
- **Granularity sweep:** BPE at five vocab sizes reaching about 1.0, 1.3, 1.6, 2.0 and 2.3-2.4x baseline fertility; all embedding tables padded to the largest, so parameter counts are equal.
- **Readout crossing:** every tokenizer run with both first-sub-token and mean-pool word readout; readout gain Delta(X) = S_pool - S_first; the readout part of a comparison is Delta(T) - Delta(B).
- **Other matching:** non-embedding parameters identical; sequence budgets equalise words, not sub-tokens; shared positional table.
- **Replication:** Study II re-implements with a different root analyser (induced from paradigm lists), new code, new training setup; only results that hold in both are claimed.
- **Statistics:** 5 seeds; paired bootstrap over test sentences (2,000 resamples, recomputing corpus F1); Holm correction within pre-specified families; equivalence verdicts at pre-set margins (1 or 2 F1, TOST at alpha 0.05); seed-level paired t-tests; dev-score-zero runs dropped before aggregation; a "replication ledger" of every failed prediction.

## Method

- **Model(s) / architecture:** 2-layer pre-LN Transformer NER encoders from scratch (0.97M Study I; 1.95M Study II); small encoder-decoder for MT; in Study II, fine-tuned XLM-R base and AfroXLM-R base (3 seeds) for the readout question only.
- **PEFT method (if any):** none.
- **Languages covered:** Amharic, Hausa.
- **Datasets:** MasakhaNER 1.0 (Amharic 1,750/250/500 sentences; Hausa 1,912/276/552), OPUS-100 for MT, UniMorph paradigms, HornMorpho analyser.
- **Tasks:** NER (main), English-to-X MT.
- **Evaluation metrics:** entity-level micro-F1, chrF++.

## Key findings

| Contrast (Amharic NER, pooled readout) | Study I | Study II |
|---|---|---|
| Total: real roots minus BPE | +9.11 | +1.25 (inconclusive) |
| Granularity: scrambled minus BPE | +4.25 | -3.39 |
| Root: real minus scrambled | +4.86 | +4.65 |
| Real minus permuted | n/a | +2.92 |
| Real minus stratified permuted | n/a | +5.21 |

1. Root effect replicates; frequency structure explains little of it (stratified permuted minus scrambled -0.56, equivalent to zero at 2 F1).
2. Readout: in from-scratch models the pooled-vs-first gain grows from +2.0 (BPE) to +13.4 (analyser arm), reversing every comparison; in AfroXLM-R the gain is +0.54 (equivalent to zero), XLM-R +0.72 (inconclusive).
3. Granularity alone: finer BPE helps Amharic up to about 2x fertility (+7.7 F1) and hurts Hausa at every level (to -10.7 F1).
4. MT: finer target segmentation hurts both languages; no root effect detected.
5. About 78% of the analyser-backed NER gain was reachable from paradigm lists alone.

## What we got from it

- A full blueprint for our scrambled-cut control, including the permutation variants and the statistics.
- Warning: our results must report the readout (first sub-token vs pooled) and match parameters and word-level sequence budgets.

## Gaps and limitations

- **Stated by the authors:** one language for the root result; tiny models from scratch; root effect not tested with pretrained models or continued pretraining; seed-sensitive permutation contrasts.
- **Our observations:**
  - Amharic is non-concatenative; Bantu morphology is concatenative, closer to the Hausa or Tagalog-free case, so the root result may not carry over.
  - Absolute F1 is very low, far from our AfroXLMR-large regime.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** the cleanest available test of "does correct morphology matter" and it says yes for Amharic roots, in tiny models.
- **Our results:** our Morfessor variants mix granularity and morphology (and perhaps readout). A scrambled-cut arm (same number of cuts per word type, same fertility, random positions, consistent per type) would tell whether our NER -3.9 is from wrong cuts or from cutting at all. Their pretrained-encoder result suggests readout is a minor issue for AfroXLMR, but we should still log it.
- **Low-resource / African language angle:** MasakhaNER Amharic and Hausa, languages we used earlier.
- **Efficiency / low-cost hardware angle:** controls are cheap to build; same cost as any extra tokenizer arm.
- **Baseline for us?** Yes: copy the scrambled and permuted controls, plus a granularity-matched BPE arm.

## Quotes and figures worth citing

> "a gain over BPE is evidence for linguistic structure only after granularity and readout have been controlled." (p. 2)

- Figure 1: design. Figure 2: decomposition in both studies. Table 1: replication ledger.

## Related papers to follow up

- [ ] Hatch and Richardson (2025), root and template tokens for Semitic MT (nearest precedent for the scrambled control).
- [ ] Ács et al. (2021), sub-token pooling for morphological tasks.
- [ ] Gazit et al. (2025), non-concatenative tokenization.

## Open questions / discussion points

- In a frozen AfroXLMR with LoRA, is there any morphology signal left to detect, or does the pretrained tokenizer dominate?
