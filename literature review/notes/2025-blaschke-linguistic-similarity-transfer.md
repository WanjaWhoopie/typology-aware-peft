# Analyzing the Effect of Linguistic Similarity on Cross-Lingual Transfer: Tasks and Experimental Setups Matter

## Reference

| Field | Details |
|---|---|
| **Title** | Analyzing the Effect of Linguistic Similarity on Cross-Lingual Transfer: Tasks and Experimental Setups Matter |
| **Authors** | Verena Blaschke, Masha Fedzechkina, Maartje ter Hoeve |
| **Year** | 2025 |
| **Venue** | Findings of the Association for Computational Linguistics: ACL 2025, pp. 8653-8684 |
| **DOI / URL** | https://aclanthology.org/2025.findings-acl.454 |
| **PDF (online)** | [ACL Anthology](https://aclanthology.org/2025.findings-acl.454.pdf) |
| **Code / data** | UD 2.14, UDPipe 2 models, SIB-200 (code availability not checked) |

**Citation (APA):**
> Blaschke, V., Fedzechkina, M., & ter Hoeve, M. (2025). Analyzing the effect of linguistic similarity on cross-lingual transfer: Tasks and experimental setups matter. In *Findings of the Association for Computational Linguistics: ACL 2025* (pp. 8653-8684). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{blaschke-etal-2025-analyzing,
  title     = {Analyzing the Effect of Linguistic Similarity on Cross-Lingual Transfer: Tasks and Experimental Setups Matter},
  author    = {Blaschke, Verena and Fedzechkina, Masha and ter Hoeve, Maartje},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2025},
  year      = {2025},
  pages     = {8653--8684},
  publisher = {Association for Computational Linguistics},
  url       = {https://aclanthology.org/2025.findings-acl.454}
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
| **Tags** | #transfer #typology #Grambank #lang2vec #SIB-200 #POS #parsing #mixed-effects #controls |

## Summary

Zero-shot transfer across 263 languages from 33 families for POS tagging, dependency parsing (UD 2.14, UDPipe 2 with mBERT embeddings) and topic classification (SIB-200, MLPs on character n-grams, transliterated n-grams, or frozen mBERT features). They correlate transfer with structural (Grambank, lang2vec syntax/phonology/inventory), lexical (ASJP), phylogenetic (Glottolog), geographic, overlap and data-size measures. Syntactic similarity is the best predictor for parsing and POS; trigram overlap for n-gram topic models; nothing predicts mBERT-based topic classification well, where pre-training inclusion of the target dominates. The best predictor depends on task and input representation.

## Review claim check

No external claim was given for this paper. Its abstract says the effect of linguistic similarity "depends on a range of factors: the NLP task, the (mono- or multilingual) input representations, and the definition of linguistic similarity" (p. 8653), which I confirmed in Sec. 5.

## Research question / problem

- How do findings on which similarity predicts transfer generalize across many languages, several tasks and input representations, and how should correlated similarity measures be interpreted?

## Method

- **Approach:** full source x target matrices; Pearson r between each measure and transfer **computed per test language and then averaged** (non-significant set to 0); linear mixed-effects models (lme4) with random source and target; simulated source selection (top-1, top-3 by each measure).
- **Model(s) / architecture:** UDPipe 2 (mBERT-based) for POS/parsing; scikit-learn MLPs for SIB-200 (n-gram, uroman transliteration, frozen mBERT [CLS]).
- **PEFT method (if any):** none.
- **Languages covered:** 263 (70 UD source, 153 UD target, 194 SIB-200).
- **Datasets:** UD 2.14 (test), UDPipe models trained on UD 2.12; SIB-200.
- **Tasks:** POS, dependency parsing (LAS/UAS), topic classification.
- **Evaluation metrics:** accuracy, LAS, UAS; Pearson r; performance loss vs best source.
- **Compute / hardware:** lightweight MLPs chosen to keep runs cheap.

## Key findings

1. Parsing: syntactic similarity (lang2vec syn) r_avg = 0.57, Grambank 0.42; higher (0.69, 0.60) for targets in mBERT pre-training.
2. POS: syn r_avg = 0.37; word overlap 0.33.
3. Topic, n-gram models: trigram overlap 0.65, character overlap 0.49, lexical 0.49. Topic, mBERT: no strong predictor (max 0.27).
4. SIB-200 mBERT accuracy: 68.3% if both languages in pre-training, 46.5% target only, 36.1% source only, 33.2% neither.
5. Measures are correlated: lexical vs phylogenetic r = 0.87; Grambank vs lang2vec syntax 0.61. Mixed models find several measures significant at once.
6. Picking the most similar source by the right measure gives small losses; top-3 candidates are much safer than top-1.
7. Their POS results with UDPipe correlate with de Vries et al. (2022) at r = 0.73.
8. lang2vec's precomputed geographic distances return the maximum distance for some languages (a bug), so they recompute distances.

## What we got from it

- Controls to copy: per-target correlations (removes target difficulty), random source and target effects, a report of inter-measure correlations, a minimum coverage rule for typology features (at least half of features present), and recomputing lang2vec distances.
- Expectation for our SIB-200 with AfroXLMR: target pre-training coverage, not typology, will dominate (matches our 95% target share).

## Gaps and limitations

- **Stated by the authors:** only 263 of about 7,000 languages; high-resource languages over-represented; confounds cannot be fully removed; UD treebanks differ in domain and size.
- **Our observations:** models are mBERT-based or small MLPs, not AfroXLMR; no fine-tuned large encoder for SIB-200; morphological typology is only indirectly covered (Grambank includes some).

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** typology (syntax) does predict transfer for grammatical tasks; for topic classification with a multilingual encoder it does not. Supports splitting RQ2 by task: expect typology signal on POS, not on SIB-200.
- **Low-resource / African language angle:** SIB-200 covers our languages; UD coverage of Bantu is thin.
- **Efficiency / low-cost hardware angle:** shows analyses with cheap models can be informative.
- **Baseline or control for us:** **Control to adopt** (per-target correlation, mixed effects, inter-measure correlation table, top-k selection loss).

## Quotes and figures worth citing

> "the effect of linguistic similarity on transfer performance depends on a range of factors" (p. 8653)

- Fig. 3: mean correlations by measure and experiment.
- Table 3: performance loss from picking sources by each measure.
- Table 8 (App. B): correlations between similarity measures.

## Related papers to follow up

- [ ] Philippy et al. (2023), survey of factors in cross-lingual transfer
- [ ] Samardžić et al. (2022), parsing transfer across 47 x 62 languages
- [ ] Toossi et al. (2024) and Khan et al. (2025), problems in URIEL/lang2vec

## Open questions / discussion points

- Report our RQ2 as top-k selection loss, not just correlation: with 3 candidate sources per target, how much F1 is lost by picking by typology?
