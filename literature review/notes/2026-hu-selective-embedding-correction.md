# SEC: Selective Embedding Correction for Cross-Lingual Transfer in Low-Resource Languages

## Reference

| Field | Details |
|---|---|
| **Title** | SEC: Selective Embedding Correction for Cross-Lingual Transfer in Low-Resource Languages |
| **Authors** | Mengting Hu, Wenjie Xue, Peiyu Xu, Xuan Li, Junpeng Huang, Zhiyuan Guang, Xiaoru Zhang, Hang Gao, Sicheng Wei, Bingyang Fan, Tiegang Gao |
| **Year** | 2026 |
| **Venue** | Findings of the Association for Computational Linguistics: EMNLP 2026, pp. 21821-21836 |
| **DOI / URL** | https://aclanthology.org/2026.findings-emnlp.1033 |
| **PDF (online)** | https://aclanthology.org/2026.findings-emnlp.1033.pdf |
| **Code / data** | https://github.com/NLPioneer/SEC-EMNLP26 |

**Citation (APA):**
> Hu, M., Xue, W., Xu, P., Li, X., Huang, J., Guang, Z., Zhang, X., Gao, H., Wei, S., Fan, B., & Gao, T. (2026). SEC: Selective embedding correction for cross-lingual transfer in low-resource languages. In *Findings of the Association for Computational Linguistics: EMNLP 2026* (pp. 21821-21836). Association for Computational Linguistics.

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{hu2026sec,
  title     = {{SEC}: Selective Embedding Correction for Cross-Lingual Transfer in Low-Resource Languages},
  author    = {Hu, Mengting and Xue, Wenjie and Xu, Peiyu and Li, Xuan and Huang, Junpeng and Guang, Zhiyuan and Zhang, Xiaoru and Gao, Hang and Wei, Sicheng and Fan, Bingyang and Gao, Tiegang},
  year      = {2026},
  booktitle = {Findings of the Association for Computational Linguistics: EMNLP 2026},
  pages     = {21821--21836},
  url       = {https://aclanthology.org/2026.findings-emnlp.1033}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | research agent (Claude) |
| **Date read** | 2026-11-21 |
| **Status** | Read (agent) |
| **Relevance to our work** | Medium |
| **Tags** | #embeddings #vocabulary-transfer #low-rank #adapters #low-resource #amharic #NER #POS |

## Summary

SEC adds a learnable correction to new-language token embeddings: e(w) = e_base(w) + (W_A W_B)(w), a rank-8 residual with a group-lasso penalty on the rows of W_A so only some tokens get corrected. The base embeddings come from UniBridge initialisation for a new target-language SentencePiece vocabulary. Training is MLM on small Wikipedia samples (up to 10k target sentences) with a KL penalty and a lower learning rate on the base embeddings, inside a MAD-X style adapter pipeline. In zero-shot multi-source transfer it beats UniBridge, FOCUS and MAD-X on mBERT; on XLM-R gains are small.

## Review claim check

- **Claim:** "sparse low-rank corrections to embeddings for low-resource NER and POS with about 1% additional trainable parameters".
- **Verdict:** partly holds.
- **Evidence:** the sparse low-rank residual and NER/POS (plus AmericasNLI NLI) are correct. But "about 1%" is relative to the embedding matrix (|V| r + r d over |V| d, about 1.05%, p. 21823), not the model; and the base embeddings themselves are also updated (at a scaled learning rate), along with language and invertible adapters.

## Which languages and benchmarks; any Masakhane data?

- NER: 14 WikiANN target languages (amh, ang, cdo, crh, eml, frr, km, kn, lij, ps, sa, sd, si, so).
- POS: 9 UD languages (amh, lij, olo, sa, sd, si, ta, tl, tt).
- NLI: 10 AmericasNLI languages.
- Source languages: English, Chinese, Russian, Arabic, Japanese (zero-shot multi-source transfer).
- No Masakhane data. Only African languages are Amharic and Somali via WikiANN, and Amharic via UD.

## Method

- **Approach:** UniBridge init of new vocab, then SEC residual trained with L = MLM + KL + group-lasso; differential LR (base embeddings slower); proximal update pushes small-norm rows to zero.
- **Model(s) / architecture:** mBERT (main), XLM-R (appendix), Qwen2.5-3B (appendix).
- **PEFT method (if any):** MAD-X style language, invertible and task adapters (reduction factors 2, 2, 16 in Tables 10-11) plus the low-rank embedding residual (r = 8).
- **Languages covered:** see above.
- **Datasets:** WikiANN, UD, AmericasNLI/XNLI; Wikipedia monolingual (up to 10k sentences per target).
- **Tasks:** NER, POS, NLI.
- **Evaluation metrics:** F1, accuracy; five-seed rerun for POS only; paired t-tests for NER/NLI.
- **Compute / hardware:** RTX A6000; 0.5 to 2 hours per language.

## Key findings

| Average | mBERT | MAD-X | FOCUS | UniBridge | SEC |
|---|---|---|---|---|---|
| WikiANN NER F1 (14 langs, mBERT) | 32.08 | 30.23 | 30.44 | 37.35 | 46.92 |
| UD POS acc (9 langs, mBERT) | 43.82 | 42.36 | 46.62 | 58.64 | 62.09 |
| WikiANN NER F1 (XLM-R) | 43.14 | 38.38 | n/a | 45.95 | 47.39 |

1. Large gains on mBERT, small on XLM-R (+1.44 NER, +0.31 POS, -1.47 NLI per the text); authors say XLM-R's vocab already reduces misalignment.
2. Amharic NER on XLM-R: SEC 47.46 vs UniBridge 49.6 (SEC lower).
3. Correction mass is concentrated: top 20% of tokens carry over 70% of correction strength.

## What we got from it

- A concrete PEFT-style way to let new embeddings move without unfreezing the whole matrix: a rank-8 residual on the embedding layer, optionally sparse.
- r = 8 was best in their sweep (4 to 16).

## Gaps and limitations

- **Stated by the authors:** smaller gains on XLM-R; sensitive to sparsity weight and differential LR, especially for morphologically rich or fragmented languages.
- **Our observations:**
  - Zero-shot cross-lingual only, not in-language fine-tuning like ours.
  - Very low absolute scores (WikiANN F1 30 to 60) make gains easy.
  - Main tables single run; robustness only partly checked.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** claims to help "morphologically complex subwords" but there is no morphology-aware segmentation.
- **Our results:** our vocab-swap arms froze the new embeddings entirely (FVT, Serengeti) and lost NER -5.8 / POS -2.3. SEC shows a cheap middle ground between frozen and fully trainable embeddings. In HF PEFT this is roughly LoRA on the embedding layer.
- **Low-resource / African language angle:** weak; no Bantu language, no Masakhane benchmark.
- **Efficiency / low-cost hardware angle:** good; embedding update is about 1% of the embedding matrix.
- **Baseline for us?** No full replication, but borrow the idea: add an "embedding LoRA (r = 8)" rung to the adaptation ladder.

## Quotes and figures worth citing

> "SEC adds only about 1% additional parameters relative to the full embedding matrix." (p. 21823)

- Table 1: WikiANN NER (mBERT). Table 3: UD POS. Table 16: XLM-R NER.

## Related papers to follow up

- [ ] Pham et al. (2024), UniBridge (their init backbone).
- [ ] Accou and Poelman (2026), TIPA.
- [ ] Liu et al. (2024), OFA.

## Open questions / discussion points

- Would a sparse embedding residual on AfroXLMR-large (already Africa-adapted) give anything, given their weak XLM-R gains?
