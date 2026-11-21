# Modular Monolingual Adaptation using Pretrained Language Models

## Reference

| Field | Details |
|---|---|
| **Title** | Modular Monolingual Adaptation using Pretrained Language Models |
| **Authors** | Nalin Kumar, Ondřej Dušek |
| **Year** | 2026 |
| **Venue** | arXiv preprint 2606.06738 (v1, 4 Jun 2026) |
| **DOI / URL** | https://doi.org/10.48550/arXiv.2606.06738 |
| **PDF (online)** | https://arxiv.org/pdf/2606.06738 |
| **Code / data** | https://github.com/knalin55/MMA-PLM ; CC-100, WikiANN, UD |

**Citation (APA):**
> Kumar, N., & Dušek, O. (2026). Modular monolingual adaptation using pretrained language models. *arXiv preprint arXiv:2606.06738*. https://doi.org/10.48550/arXiv.2606.06738

<details>
<summary>BibTeX</summary>

```bibtex
@article{kumar2026modular,
  title   = {Modular Monolingual Adaptation using Pretrained Language Models},
  author  = {Kumar, Nalin and Du{\v{s}}ek, Ond{\v{r}}ej},
  year    = {2026},
  journal = {arXiv preprint arXiv:2606.06738},
  doi     = {10.48550/arXiv.2606.06738}
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
| **Tags** | #vocabulary-transfer #embeddings #LAPT #LoRA #low-resource #NER #POS |

## Summary

Proposes adapting a pretrained encoder to a low-resource language by training a new 30k WordPiece tokenizer, initialising its embeddings (mean of old sub-token embeddings, FastText, or random), freezing the input and tied output embeddings, and training all non-embedding parameters with MLM on target text. Tested on Scottish Gaelic, Irish and Quechua with BERT, mBERT and mmBERT. Non-embedding training beats full and embedding-only training on mask-filling and roughly matches full training on NER and POS (after full task fine-tuning). It also beats LoRA (r = 64). The custom tokenizer matters a lot; the embedding init matters little.

## Review claim check

- **Claim:** "vocabulary swap where the rest of the model is tuned to absorb the change".
- **Verdict:** holds.
- **Evidence:** p. 1: "we replace the tokens, freeze the corresponding embeddings, and tune the rest of the model". The tuning is MLM on target-language text (adaptation stage), followed by full fine-tuning on the task. Note the embeddings are frozen but the whole transformer body is trained, which is the mirror image of our setup.

## Research question / problem

- Is full-model tuning needed for monolingual adaptation, or does training only the non-embedding parameters (with a new vocabulary) do as well?

## Method

- **Approach:** custom WordPiece (30k); embeddings from model (mean of old pieces, FVT-like), FastText, or random; embeddings frozen and tied; MLM on target corpus for up to 50 epochs; compare full / embedding-only / non-embedding training; LoRA (r = 64, alpha = 128) as comparison.
- **Model(s) / architecture:** BERT-base, mBERT, mmBERT (base), random-init transformer.
- **PEFT method (if any):** frozen embeddings; LoRA as comparison.
- **Languages covered:** Scottish Gaelic, Irish, Quechua (8.5k training instances).
- **Datasets:** CC-100; WikiANN (gd/qu 100/100/100; ga 1000 each); UD gd, ga.
- **Tasks:** mask filling, NER, POS.
- **Evaluation metrics:** accuracy (also for NER); 3 runs.
- **Compute / hardware:** for mBERT, ours 85.6M trainable params, 0.9 GB VRAM, 14 h vs full 178M, 1.3 GB, 32 h (Table 7).

## Key findings

| mBERT, Scottish Gaelic, custom tokenizer + model-init embeddings | Full | Non-emb (theirs) |
|---|---|---|
| Mask filling accuracy | 33.4 | 54.3 |
| Trainable params | 178M | 85.6M |

1. Non-embedding training wins on mask filling across all languages and models; on NER/POS it is comparable to full training and better than embedding-only training.
2. A custom tokenizer beats the multilingual one on mask filling; embedding init (model, FastText, random) matters little once the body is trained.
3. LoRA (r = 64) is comparable to full fine-tuning but below their method on all three tasks (Table 6).

## What we got from it

- A cheap, well-defined rung for our ladder: after a vocab swap, keep the new embeddings frozen but let the body adapt by MLM (or LoRA + MLM), then fine-tune.
- Evidence that random vs averaged init barely matters once the body adapts, which suggests our Serengeti failure is about the body never adapting to the new embeddings.

## Gaps and limitations

- **Stated by the authors:** (not a separate section in what we read) mmBERT underperforms on downstream tasks, possibly over-training.
- **Our observations:**
  - "Accuracy" for NER inflates scores (O tags); not comparable to entity F1.
  - Tiny NER sets for gd/qu (100 test sentences).
  - Downstream gains over full tuning are small and mixed; the clear win is on mask filling.
  - No African languages; base-size models only.

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** none; plain WordPiece.
- **Our results:** our vocab-swap arms froze both embeddings and body (only LoRA trained on the task), so nothing adapted the body to new embeddings before task training. This paper says the body is what should absorb the change. That predicts our NER -5.8 / POS -2.3 should shrink with an MLM stage that updates the body (fully or via LoRA).
- **Low-resource / African language angle:** none directly, but Quechua's 8.5k sentences is a similar data regime to our smaller languages.
- **Efficiency / low-cost hardware angle:** fewer trainable params and less VRAM than full tuning; still needs MLM over the full body.
- **Baseline for us?** Yes: "frozen new embeddings + body adapted by MLM (LoRA or full)" as a ladder rung.

## Quotes and figures worth citing

> "we replace the tokens, freeze the corresponding embeddings, and tune the rest of the model." (p. 1, abstract)

- Table 1: mask filling by strategy. Table 6: LoRA comparison. Table 7: efficiency.

## Related papers to follow up

- [ ] de Vries and Nissim (2021), relearning lexical embeddings with frozen transformer.
- [ ] Alabi et al. (2022), language adaptive fine-tuning.
- [ ] Rust et al. (2021), monolingual tokenizer quality.

## Open questions / discussion points

- Does LoRA during MLM (instead of full body tuning) keep most of the benefit on AfroXLMR-large?
