# Canonical and Surface Morphological Segmentation for Nguni Languages

## Reference

| Field | Details |
|---|---|
| **Title** | Canonical and Surface Morphological Segmentation for Nguni Languages |
| **Authors** | Tumi Moeng, Sheldon Reay, Aaron Daniels, Jan Buys |
| **Year** | 2021 |
| **Venue** | arXiv preprint 2104.00767 (the PDF itself names no venue) |
| **DOI / URL** | https://doi.org/10.48550/arXiv.2104.00767 |
| **PDF (online)** | https://arxiv.org/pdf/2104.00767 |
| **Code / data** | Code: https://github.com/DarkPr0digy/MORPH_SEGMENT ; data: NCHLT annotated corpora, https://repo.sadilar.org/handle/20.500.12185/7 |

**Citation (APA):**
> Moeng, T., Reay, S., Daniels, A., & Buys, J. (2021). Canonical and surface morphological segmentation for Nguni languages. *arXiv preprint arXiv:2104.00767*. https://doi.org/10.48550/arXiv.2104.00767

<details>
<summary>BibTeX</summary>

```bibtex
@article{moeng2021canonical,
  title   = {Canonical and Surface Morphological Segmentation for Nguni Languages},
  author  = {Moeng, Tumi and Reay, Sheldon and Daniels, Aaron and Buys, Jan},
  year    = {2021},
  journal = {arXiv preprint arXiv:2104.00767},
  doi     = {10.48550/arXiv.2104.00767}
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
| **Tags** | #morphology #segmentation #zulu #nguni #low-resource #CRF #morfessor |

## Summary

Supervised and unsupervised morphological segmentation for isiZulu, isiXhosa, isiNdebele and siSwati using the NCHLT annotated corpora. Canonical segmentation (underlying morphemes) is treated as character-level seq2seq; surface segmentation (pure split of the written word) as BMES character labelling with CRFs. A feature-based CRF reaches 97.1% average morpheme F1 on surface segmentation; the Transformer reaches 72.5% on canonical segmentation. Unsupervised methods (Morfessor, entropy-based LSTM) are far worse and sometimes barely above a random baseline.

## Review claim check

- **Claim:** "feature-based CRFs reach about 97.1% F1 on surface segmentation".
- **Verdict:** holds.
- **Evidence:** Abstract and Table 4 give a 97.14 average F1 for the feature-based CRF (isiZulu 97.35). Small inconsistency inside the paper: the text says the Bi-LSTM CRF averages 93.81 while Table 4 and the abstract say 94.83 / 94.8.

## Research question / problem

- Can supervised models produce accurate morpheme segmentations for conjunctively written Nguni languages, and how far behind are unsupervised methods?

## Method

- **Approach:** canonical segmentation as seq2seq (LSTM, Bi-LSTM+attention, Transformer); surface segmentation as BMES sequence labelling (feature-based CRF via sklearn-crfsuite; Bi-LSTM CRF); unsupervised Morfessor-Baseline, entropy-based char-LSTM, random baseline.
- **CRF features:** character n-grams (n 0 to 6), vowel/consonant, upper/lower case; epsilon 1e-7, max 160 iterations.
- **Surface gold:** derived heuristically from canonical annotations by Levenshtein alignment (45% of words differ between canonical and surface forms on average).
- **Model(s) / architecture:** small task-specific models (hidden 256), no pretrained LM.
- **PEFT method (if any):** none.
- **Languages covered:** isiZulu, isiXhosa, isiNdebele, siSwati.
- **Datasets:** NCHLT annotated text corpora (Eiselen and Puttkammer, 2014).
- **Tasks:** canonical and surface morphological segmentation.
- **Evaluation metrics:** morpheme-level precision, recall, micro-F1 (set of morphemes per word), not boundary accuracy.
- **Compute / hardware:** CRF is cheap (CPU); not reported in detail.

## Key findings

| Model | Avg P | Avg R | Avg F1 | isiZulu F1 |
|---|---|---|---|---|
| Surface, feature-based CRF | 97.54 | 96.74 | 97.14 | 97.35 |
| Surface, Bi-LSTM CRF | 94.68 | 94.99 | 94.83 | 96.64 |
| Canonical, Transformer | 75.58 | 69.76 | 72.54 | 74.06 |
| Canonical, rule-based NCHLT (upper bound) | 60.26 | 43.97 | 50.72 | 54.42 |
| Unsupervised, Morfessor | 28.06 | 27.57 | 27.69 | 21.69 (P 20.37) |
| Unsupervised, random | 24.83 | 14.76 | 18.51 | 18.48 |

1. Supervised surface segmentation is close to solved for isiZulu with a plain CRF.
2. Morfessor on isiZulu is barely above random on morpheme-level F1.
3. Under boundary accuracy Morfessor looks much better (they reproduce about 77% from prior work), so the metric matters a lot.

## Data and splits (we use their isiZulu data)

- Source: NCHLT annotated corpora (SADiLaR repo above), which come with a train/test split; morpheme labels exist but the paper ignores them.
- Processing: punctuation, numbers and unsegmented words removed; any word in both train and test removed from train; dev split carved from train the same way (so test words are unseen types).
- Sizes after processing (words): isiZulu 17,778 / 1,777 / 3,298 (train/dev/test); isiXhosa 16,879 / 1,688 / 3,004; isiNdebele 12,929 / 1,119 / 2,553; siSwati 13,278 / 1,080 / 1,347.
- The paper does not itself state that the processed splits are released; check the GitHub repo before citing them as "their splits".

## What we got from it

- A ready supervised segmenter recipe (feature-based CRF) for isiZulu surface segmentation, trainable in minutes.
- A reference number for how bad Morfessor is on the same gold (morpheme F1 21.7 for isiZulu).

## Gaps and limitations

- **Stated by the authors:** small datasets; future work on semi-supervised and multilingual training.
- **Our observations:**
  - Surface gold is derived heuristically from canonical annotation, so "97%" is against an approximate surface target.
  - Test set is word types out of context; no downstream use of the segmentations.
  - No Kinyarwanda, Luganda or Swahili.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** our Morfessor segmentation has precision 0.51 against isiZulu gold; this paper shows a supervised CRF gets about 97 F1 on the same kind of gold. That makes "bad segmentation" the first suspect for our NER -7.0 / -3.9 and POS -3.4 / -0.5 drops, and a supervised segmenter is the obvious next arm. Make sure our 0.51 uses the same metric (morpheme-level vs boundary) before comparing.
- **Low-resource / African language angle:** only Nguni; transfer of a Zulu CRF to Kinyarwanda/Luganda is not possible, so the supervised arm is isiZulu-only (maybe isiXhosa).
- **Efficiency / low-cost hardware angle:** CRF training is CPU-cheap.
- **Baseline for us?** Yes: train their feature-based CRF on the isiZulu split and rerun our inner-word-cut variant with CRF cuts instead of Morfessor cuts.

## Quotes and figures worth citing

> "Feature-based CRFs outperform bidirectional LSTM-CRFs to obtain an average of 97.1% F1 on surface segmentation." (p. 1, abstract)

- Table 1: dataset sizes. Table 4: surface segmentation results. Table 5: unsupervised results (Morfessor near random for isiZulu).

## Related papers to follow up

- [ ] Eiselen and Puttkammer (2014), NCHLT annotated corpora.
- [ ] Cotterell et al. (2015/2016), semi-Markov CRF and canonical segmentation.
- [ ] Mzamo et al. (2019), entropy-based isiXhosa segmentation.

## Open questions / discussion points

- Does a 97-F1 segmenter fix our drop, or does the drop come from frozen embeddings regardless of cut quality? (The scrambled-cut control answers this.)
