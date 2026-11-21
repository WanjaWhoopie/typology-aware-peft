# Can Embedding Similarity Predict Cross-Lingual Transfer? A Systematic Study on African Languages

## Reference

| Field | Details |
|---|---|
| **Title** | Can Embedding Similarity Predict Cross-Lingual Transfer? A Systematic Study on African Languages |
| **Authors** | Tewodros Kederalah Idris, Prasenjit Mitra, Roald Eiselen |
| **Year** | 2026 |
| **Venue** | arXiv preprint 2601.03168 (v1, 6 Jan 2026); no peer-reviewed venue stated in the PDF |
| **DOI / URL** | https://arxiv.org/abs/2601.03168 |
| **PDF (online)** | [arXiv](https://arxiv.org/pdf/2601.03168) |
| **Code / data** | "Code released upon publication" (not yet available in v1) |

**Citation (APA):**
> Idris, T. K., Mitra, P., & Eiselen, R. (2026). *Can embedding similarity predict cross-lingual transfer? A systematic study on African languages* (arXiv:2601.03168). arXiv. https://arxiv.org/abs/2601.03168

<details>
<summary>BibTeX</summary>

```bibtex
@misc{idris-etal-2026-embedding,
  title         = {Can Embedding Similarity Predict Cross-Lingual Transfer? A Systematic Study on African Languages},
  author        = {Idris, Tewodros Kederalah and Mitra, Prasenjit and Eiselen, Roald},
  year          = {2026},
  eprint        = {2601.03168},
  archivePrefix = {arXiv},
  primaryClass  = {cs.CL}
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
| **Tags** | #transfer #source-selection #embedding-similarity #URIEL #AfroXLMR #NER #POS #sentiment #bantu #hausa #amharic |

## Summary

Closest prior work to our RQ2. Computes five embedding similarity metrics (cosine mean, cosine gap, P@1, CSLS, CKA) between 12 African languages from mean-pooled FLORES-200 sentence embeddings, and correlates them (Spearman) with zero-shot transfer for NER, POS and sentiment, separately for AfriBERTa, AfroXLM-R (large, 550M) and Serengeti. Cosine gap and retrieval metrics reach rho of about 0.4-0.6; CKA is near zero. Pooling across models reverses the sign (Simpson's paradox). Embedding metrics roughly match URIEL genetic distance, and for AfroXLM-R URIEL is better.

## Review claim check

- **Claim:** "816 transfer runs, 12 African languages, AfroXLMR and Serengeti; compares model-derived similarity with URIEL".
- **Verdict: partly holds.** 816 runs and 12 languages are correct (272 ordered pairs x 3 models). But there are three models, not two: AfriBERTa as well. The URIEL comparison reported in Table 7 is with genetic distance only, though five URIEL distances are described in Sec. 3.3.

## Research question / problem

- Which embedding similarity metrics predict zero-shot transfer between African languages, do findings generalize across models, and how do they compare with typology (URIEL)?

## Method

- **Approach:** per model and task, Spearman rho between each metric and transfer score over all ordered pairs; Simpson's paradox analysis; top-k source selection accuracy vs random.
- **Model(s) / architecture:** AfriBERTa-large (126M), AfroXLM-R-large (Davlan/afro-xlmr-large, 550M), Serengeti (278M).
- **PEFT method (if any):** none (full fine-tuning, linear head).
- **Languages covered:** Bantu kin, lug, swa, xho, zul; Atlantic wol; Volta-Niger ibo, yor; Afro-Asiatic amh, hau; Nilo-Saharan luo; Mande bam.
- **Datasets:** MasakhaNER 2.0 (12 languages, 132 pairs), MasakhaPOS (11, no Amharic, 110 pairs), AfriSenti (6: amh, hau, ibo, kin, swa, yor; 30 pairs); FLORES-200 devtest for embeddings.
- **Tasks:** NER, POS, sentiment.
- **Evaluation metrics:** seqeval micro F1 (NER), accuracy (POS), macro F1 (sentiment); Spearman rho.
- **Compute / hardware:** lr 2e-5, batch 16, max 10 epochs, early stopping patience 3, max length 128; one run per configuration (no seeds).

## Key findings

1. Mean rho over 9 model-task conditions: cosine_gap 0.41, P@1 0.40, CSLS 0.40, cosine_mean 0.34, CKA 0.10.
2. Pooled NER rho = -0.18 vs within-model 0.37 to 0.60 (Simpson's paradox).
3. |rho| with transfer, embedding vs URIEL genetic (Table 7):

| Task | Feature | AfriBERTa | AfroXLM-R | Serengeti |
|---|---|---|---|---|
| NER | cosine_gap | 0.60 | 0.37 | 0.51 |
| NER | URIEL genetic | 0.27 | 0.43 | 0.40 |
| POS | cosine_gap | 0.56 | 0.49 | 0.47 |
| POS | URIEL genetic | 0.45 | 0.65 | 0.45 |

4. AfroXLM-R has the weakest embedding-transfer correlations (mean rho 0.22 vs 0.37-0.39 for the others).
5. Target inclusion in pre-training matters more than source inclusion (+25-27% F1 for seen targets).
6. Sentiment: correlations weak and mostly not significant (n = 30).
7. Best-source top-1 accuracy with cosine_gap: 25-50% vs 9-20% random.

## What we got from it

- **Overlap with our work:** it covers all of our languages (hau, kin, lug, swa, zul, amh), the same model (AfroXLMR-large) and the same NER and POS datasets. Our 6 x 6 NER matrix is a subset of their 12 x 12 AfroXLM-R NER matrix (30 of their 132 pairs), with different hyperparameters (they: lr 2e-5, 10 epochs, length 128, one seed). Our POS matrix overlaps 20 of their 110 pairs (no amh in MasakhaPOS). They do not use SIB-200, LoRA, or multiple seeds, and I did not see per-pair transfer matrices or a Bantu vs non-Bantu analysis in the text.
- A typology result that favours our RQ2 for AfroXLMR: URIEL genetic distance predicts POS transfer at |rho| = 0.65.

## Gaps and limitations

- **Stated by the authors:** encoder-only models; classification tasks only; FLORES-only metrics; correlation not causation (shared vocabulary or pre-training data may drive both); limited families.
- **Our observations:** single run per pair with no CIs, despite known high seed variance in transfer (Beukman & Fokam 2023); pairs are not independent and target effects are not removed (Spearman over all pairs mixes target difficulty with similarity; de Vries et al. 2022 show the target dominates); no token or entity overlap covariate; only genetic URIEL distance reported; Amharic is listed for MasakhaNER 2.0, which does not contain Amharic (it is in MasakhaNER 1.0), and I did not see this explained; AfroXLM-R coverage marks in their Table 9 did not extract cleanly, so check which of the 12 languages they treat as unseen.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** shows the model-derived vs typology comparison has been done for our languages; novelty for RQ2 must come from elsewhere (text-learned morphological typology, controls, PEFT).
- **Low-resource / African language angle:** same languages, datasets and model.
- **Efficiency / low-cost hardware angle:** none (no PEFT).
- **Baseline or control for us:** **Baseline** (cosine_gap and URIEL genetic as the predictors to beat) and **control** (stratify by model and by fine-tuning method; never pool full FT and LoRA correlations).

## Quotes and figures worth citing

> "correlation signs reverse when pooling across models (Simpson's Paradox), so practitioners must validate per-model" (Abstract)

- Table 7: embedding vs URIEL genetic.
- Fig. 1: Simpson's paradox scatter.
- Table 8: top-k source selection accuracy.

## Related papers to follow up

- [ ] Kargaran et al. (2025), MEXA alignment metric (r = 0.90 reported)
- [ ] Muller et al. (2023), language characteristics in mT5 transfer
- [ ] Rice et al. (2025), ranking transfer languages for POS

## Open questions / discussion points

- Contact the authors for per-pair AfroXLM-R scores to compare with our full FT matrix.
- Repeat their analysis per target (or with target random effects) to see whether cosine_gap survives.
