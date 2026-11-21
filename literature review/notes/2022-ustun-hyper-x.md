# Hyper-X: A Unified Hypernetwork for Multi-Task Multilingual Transfer

## Reference

| Field | Details |
|---|---|
| **Title** | Hyper-X: A Unified Hypernetwork for Multi-Task Multilingual Transfer |
| **Authors** | Ahmet Üstün, Arianna Bisazza, Gosse Bouma, Gertjan van Noord, Sebastian Ruder |
| **Year** | 2022 |
| **Venue** | EMNLP 2022, pp. 7934-7949 |
| **DOI / URL** | https://doi.org/10.18653/v1/2022.emnlp-main.541 |
| **PDF (online)** | https://aclanthology.org/2022.emnlp-main.541.pdf |
| **Code / data** | https://github.com/ahmetustun/hyperx (announced in paper) |

**Citation (APA):**
> Üstün, A., Bisazza, A., Bouma, G., van Noord, G., & Ruder, S. (2022). Hyper-X: A unified hypernetwork for multi-task multilingual transfer. In *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing* (pp. 7934-7949). Association for Computational Linguistics. https://doi.org/10.18653/v1/2022.emnlp-main.541

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{ustun-etal-2022-hyper,
  title     = {Hyper-{X}: A Unified Hypernetwork for Multi-Task Multilingual Transfer},
  author    = {{\"U}st{\"u}n, Ahmet and Bisazza, Arianna and Bouma, Gosse and van Noord, Gertjan and Ruder, Sebastian},
  booktitle = {Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing},
  year      = {2022},
  pages     = {7934--7949},
  doi       = {10.18653/v1/2022.emnlp-main.541}
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
| **Tags** | #adapters #hypernetwork #multi-task #zero-shot #few-shot #NER #POS |

## Summary

Hyper-X is one hypernetwork that generates adapter weights for every transformer layer from the concatenation of a task embedding, a language embedding and a layer embedding. Task and language embeddings are learned (MLM on Wikipedia is an auxiliary task so every language gets an embedding). On mBERT, with NER (WikiANN) and POS (UD 2.7) over 15 zero-shot languages, it is on par with MAD-X when only English is available (NER 52.7 vs 52.8 F1) and better when a mix of task-language data is available, while training once (about 18 hours vs about 116 for MAD-X). It is also competitive in few-shot (5 to 50 examples).

## Review claim check

- **Claim:** "generates adapters from language embeddings".
- **Verdict:** holds.
- **Evidence:** adapters are "conditioned on both tasks and language embeddings" (abstract, p. 7934); the embeddings are "learned together with the parameters of the hypernetwork" (p. 7937). Note: unlike UDapter and MAD-G, these are learned embeddings, not typological feature vectors.

## Research question / problem

- How to use heterogeneous supervision (different tasks available in different languages) and transfer to unseen task-language pairs.

## Method

- **Approach:** hypernetwork(task emb, language emb, layer emb) -> adapter weights; MLM as auxiliary task.
- **Model(s) / architecture:** mBERT; Hyper-X Base (76M trainable params) and Small (13M).
- **PEFT method (if any):** generated bottleneck adapters.
- **Languages covered:** typologically diverse set incl. English, Arabic, Breton, Chinese, Icelandic, Kazakh, Tamil, Turkish, Yoruba, Faroese, Guarani, Upper Sorbian, Maltese, Sanskrit, Uyghur, Cantonese (appendix list).
- **Datasets:** UD 2.7, WikiANN (Rahimi splits), Wikipedia (100K sentences per language for MLM).
- **Tasks:** NER, POS.
- **Evaluation metrics:** F1, accuracy; 3 runs.
- **Compute / hardware:** one training run of about 18 hours.

## Key findings

1. English-only source: Hyper-X Base about equal to MAD-X on NER (52.7 vs 52.8), behind on POS (63.5 vs 65.4).
2. With mixed task-language sources it beats mBERT and parameter space factorisation, especially on languages unseen by mBERT.
3. Few-shot (5, 10, 20, 50 examples, 50 epochs): competitive or better than baselines.

## What we got from it

- Shows a hypernetwork over learned language embeddings is a strong alternative to typology vectors when each language has some data, which is our in-training case.

## Gaps and limitations

- **Stated by the authors:** only two tasks; few-shot only for languages with MLM data; no completely new tasks.
- **Our observations:** no typology input, so it cannot place a language without MLM data; mBERT; one African language (Yoruba).

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none directly; it is the "learned language embedding" contrast to typology.
- **Low-resource / African language angle:** weak.
- **Efficiency / low-cost hardware angle:** single model for many task-language pairs.
- **Baseline for us?** No as a full system. Its idea gives a control: replace typology features in our gate with learned language IDs.

## Quotes and figures worth citing

> "This model generates weights for adapter modules conditioned on both tasks and language embeddings." (abstract, p. 7934)

## Related papers to follow up

- [ ] Ponti et al. 2021, parameter space factorisation.
- [ ] Mahabadi et al. 2021, HyperFormer.

## Open questions / discussion points

- For our four in-training languages, will a learned language ID gate match a typology gate (as UDapter found for seen languages)? Typology should only be expected to win on held-out languages.
