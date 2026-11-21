# Does Morphological Correctness Matter for Tokenization? A Scrambled Control Study in Tagalog

## Reference

| Field | Details |
|---|---|
| **Title** | Does Morphological Correctness Matter for Tokenization? A Scrambled Control Study in Tagalog |
| **Authors** | Abdul Rehman Antall, Baidya Nath Saha |
| **Year** | 2026 |
| **Venue** | arXiv preprint 2610.20859 (v1, 14 Oct 2026) |
| **DOI / URL** | https://doi.org/10.48550/arXiv.2610.20859 |
| **PDF (online)** | https://arxiv.org/pdf/2610.20859 |
| **Code / data** | https://github.com/AbdulRehmanAntall/morphaustro-tok ; data: OPUS ParaCrawl v9, FLORES+, WikiANN tl |

**Citation (APA):**
> Antall, A. R., & Saha, B. N. (2026). Does morphological correctness matter for tokenization? A scrambled control study in Tagalog. *arXiv preprint arXiv:2610.20859*. https://doi.org/10.48550/arXiv.2610.20859

<details>
<summary>BibTeX</summary>

```bibtex
@article{antall2026tagalog,
  title   = {Does Morphological Correctness Matter for Tokenization? A Scrambled Control Study in {T}agalog},
  author  = {Antall, Abdul Rehman and Saha, Baidya Nath},
  year    = {2026},
  journal = {arXiv preprint arXiv:2610.20859},
  doi     = {10.48550/arXiv.2610.20859}
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
| **Tags** | #tokenization #morphology #scrambled-control #tagalog #infixation #NER #MT #methodology |

## Summary

Tagalog voice infixes (s-um-ulat, s-in-ulat) make the root non-contiguous, so BPE cannot isolate it. MorphAustro-Tok emits the root as a contiguous token plus a positional infix token, then runs BPE constrained not to merge across morph boundaries. It is compared with corpus-matched BPE at three fertility levels and, at two levels, with a scrambled-morpheme control. MorphAustro-Tok improves MT by 0.84, 1.49 and 3.40 chrF++, but the scrambled control captures nearly the same gain, so no contribution of morphological correctness is detected for MT. On NER the only robust result is that scrambled boundaries hurt slightly relative to real ones (0.023 F1 at one level).

## Review claim check

- **Claim:** "no contribution from morphological correctness at this scale".
- **Verdict:** partly holds.
- **Evidence:** true for MT: real minus scrambled is -0.055 (F1 level) and +0.661 chrF++ (F2 level), both below between-seed dispersion (p. 1, Table 2). The authors stress this is non-detection, not equivalence. For NER at one fertility level, real beats scrambled by +0.023 F1 (p = 0.0045), which they call the only non-circular result clearing both floors (it does not replicate at the other level).

## The scrambled-control design (to copy)

- **Fires on exactly the word types the real analyser fires on** (same selection of words to decompose).
- **Always two morphs:** removes a pseudo-infix at an (offset, length) pair chosen uniformly from pairs with offset and length in {1, 2, 3}, excluding the true pair and leaving at least 3 characters.
- **Per-type consistency:** assignment cached per word type, deterministic given the seed, stable across the corpus.
- **Same marker schema** (<INF:string@offset>), so no new marker category; invertible like the real tokenizer.
- **What it preserves:** morph count per line (verified), invertibility, per-type consistency. **What it destroys:** the correct infix, its length/offset and the residue, so paradigm members stop sharing a root unit.
- **Fertility matching:** levels matched on tokens per character (0.319, 0.379, 0.438), tolerance 0.005; this forces different vocab sizes, which they report and treat as a confound (parameters counted exactly: 926,208 + 128|V|).
- **Statistics:** 3 seeds; paired bootstrap over test examples (10,000 resamples) after averaging seeds; Holm correction in two pre-fixed families; a stability rule requiring both example-level significance and an effect larger than one between-seed sd.
- **Threat they flag:** the control inherits which words to decompose, so the conclusion narrows to "correct placement does not matter given correct selection".

## Method

- **Model(s) / architecture:** tiny Transformers from scratch (1.12M to 1.92M inference-path parameters): encoder-decoder MT, encoder NER, encoder voice probe.
- **PEFT method (if any):** none.
- **Languages covered:** Tagalog (main); Indonesian exploratory (classifier probe only).
- **Datasets:** ParaCrawl v9 en-tl/en-id; FLORES+ devtest; WikiANN tl (10,000 train, 1,000 test).
- **Tasks:** MT, NER, voice probe (declared circular and non-evidential).
- **Evaluation metrics:** chrF++, seqeval entity F1; word representation is the mean of all sub-pieces.

## Key findings

| Level | Morph - BPE (chrF++) | Scrambled - BPE | Morph - Scrambled |
|---|---|---|---|
| F1 (0.379) | +1.488 | +1.543 | -0.055 (ns) |
| F2 (0.438) | +3.396 | +2.735 | +0.661 |

1. Gain over BPE grows as segmentation coarsens, so token count does not explain it.
2. Capacity does not explain it: at F2 the scrambled arm has more parameters and scores lower.
3. A morph-constrained tokenizer needs 16% to 33% more vocab entries for the same fertility.
4. MT and NER gains do not correlate across configurations.

## What we got from it

- A second, simpler scrambled-cut recipe, closer to our case (concatenative-style cut positions inside a word, Latin script) than the Amharic root design.
- A plausible mechanism other than correctness: consistent per-type segmentation.

## Gaps and limitations

- **Stated by the authors:** tiny models; not preregistered; register gap (Filipino test vs Tagalog train, 61% unseen test types); n = 3 seeds; selection of infixed types may carry the effect.
- **Our observations:**
  - Infixation is rare (1.63% of words), so effects are small.
  - Nothing on pretrained encoders or PEFT.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** directly tests whether correctness of morphological cuts matters; answer for MT is "not detectably", for NER "maybe a little".
- **Our results:** our Morfessor cuts are only 0.51 precise, so they are partly "scrambled" already. If a scrambled-cut arm scores the same as the Morfessor arm, the loss comes from cutting, not from wrong cuts. Their NER-only sensitivity to wrong boundaries is a reason to run the control on NER and POS, not just one task.
- **Low-resource / African language angle:** none.
- **Efficiency / low-cost hardware angle:** cheap design.
- **Baseline for us?** Yes: the scrambled-cut control (same words, same number of cuts per word, random but type-consistent positions, fertility-matched).

## Quotes and figures worth citing

> "so we detect no contribution from morphological correctness at this scale." (p. 1, abstract)

> "linguistically wrong morpheme boundaries damage sequence labelling, not that morphology-aware boundaries improve it." (p. 7)

- Algorithm 2: the scrambled control. Table 2: Morph vs Scrambled. Table 4: NER.

## Related papers to follow up

- [ ] Antall and Saha (2026), Amharic/Hausa decomposition study.
- [ ] Schmidt et al. (2024), compression is not the whole story.
- [ ] Bostrom and Durrett (2020), BPE vs Unigram.

## Open questions / discussion points

- Is "consistency" the active ingredient? A control that is consistent but cuts at frequency-chosen points would test this.
