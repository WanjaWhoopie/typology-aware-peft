# Typology-Aware Parameter-Efficient Transfer Learning for Morphologically Rich, Low-Resource Languages

Research on typology-aware adapters that help LLMs handle morphologically rich, low-resource African languages (Swahili, Zulu, Amharic, Hausa and more) on low-cost hardware.

Languages: Amharic (amh), Hausa (hau), Kinyarwanda (kin), Luganda (lug), Swahili (swa), isiZulu (zul); the last four are Bantu.

**All numbers are in one workbook, [`results/results.xlsx`](results/results.xlsx)**, one tab per experiment (rebuilt with `python src/build_workbook.py`). The `summary.md` and `interpretation.md` files in each `results/` folder hold the full tables and the reasoning behind them.

## Results so far

### 1. SIB-200 topic classification (baseline, done)

Details: [`results/sib200/interpretation.md`](results/sib200/interpretation.md), workbook tab "SIB-200".

| question                                                                                                 | why it matters                                                                                                               | what we found                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. How well does the unchanged model do on each language?                                                | This is the reference score every later method (WP1 to WP3) is compared against.                                             | 84 to 89% topic accuracy for five languages; Luganda is clearly weaker at about 70%                                                                                                                                                                 |
| 2. Does LoRA match full fine-tuning?                                                                     | The project relies on PEFT. If LoRA lost a lot, it would be a weak base to build on.                                         | Yes: pooled difference +0.7 points, 95% CI [−1.1, +2.4], so no real difference                                                                                                                                                                      |
| 3. Is it cheap enough? (goal G7)                                                                         | The project promises methods that run on one 16 GB GPU.                                                                      | LoRA trains 0.33% of the parameters, peaks at 4.4 GB against 11.3 GB, and takes about 43 s per run against about 140 s                                                                                                                              |
| 4. How well does a model trained on one language work on the others? (the 6x6 zero-shot transfer matrix) | RQ2 needs to know whether related languages (the four Bantu ones) help each other more than unrelated ones (Amharic, Hausa). | Transfer is almost as good as in-language (92 to 102%). The target language explains about 95% of the variation and the source almost none. No Bantu advantage: Bantu sources reach about 79% on Bantu targets, Amharic and Hausa sources about 80% |

### 2. Named entity recognition, MasakhaNER (baseline, done)

Details: [`results/ner/summary.md`](results/ner/summary.md), workbook tab "NER". MasakhaNER 2.0 for five languages, MasakhaNER 1.0 for Amharic.

| question                                                  | why it matters                                                                                                      | what we found                                                                                                                                                                                                                                                                                                                                                            |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. How well does the unchanged model do on each language? | Reference score for a task that depends on word forms, where tokenization should matter more than for topic labels. | Entity F1 78% (Amharic) to 92% (Swahili). Luganda is not weak here (89.5%), so its SIB-200 weakness is specific to that task or dataset                                                                                                                                                                                                                                  |
| 2. Does LoRA match full fine-tuning?                      | Same check as for SIB-200, on a harder task.                                                                        | Not quite: LoRA is 3.3 points lower, 95% CI [−3.9, −2.8], a small but real gap. It is lower on every language, from −1.0 (Swahili) to −5.4 (Luganda). 16 of 18 runs per method peaked in epoch 4 or 5 of 5 and LoRA settings were not tuned, so both are probably undertrained and the gap may shrink once trained to convergence                                                                                                                          |
| 3. Is it cheap enough? (goal G7)                          | Same as SIB-200.                                                                                                    | Yes: LoRA trains 0.14% of the parameters, peaks at 3.8 to 5.3 GB against 11.3 GB, and runs about 3.4 times faster (1 to 4 minutes against 3 to 14)                                                                                                                                                                                                                       |
| 4. How well does transfer work across languages?          | RQ2: do related languages help each other more?                                                                     | Full fine-tuning shown; LoRA gives the same pattern. Transfer is much weaker than for topics: 45 to 92% of the in-language score. The target explains 81% of the variation, the source 6%. No clear Bantu advantage: Bantu sources reach 65.3 F1 on Bantu targets, but Hausa alone reaches 66.3; only Amharic is lower (54.1), and Amharic differs in script and dataset version (MasakhaNER 1.0). isiZulu and Amharic are the hardest targets (about 50% of in-language) |

### 3. Part-of-speech tagging, MasakhaPOS (baseline, done)

Details: [`results/pos/summary.md`](results/pos/summary.md), workbook tab "POS". MasakhaPOS for five languages; UD Amharic-ATT for Amharic, split 70/10/20 by us.

| question                                                  | why it matters                                                        | what we found                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. How well does the unchanged model do on each language? | Reference score for the most morphology-sensitive of our three tasks. | Accuracy 90% (isiZulu) to 98% (Kinyarwanda). Luganda is again not weak (92.3%)                                                                                                                                                                                                                                                                                        |
| 2. Does LoRA match full fine-tuning?                      | Same check as for SIB-200.                                            | Almost: LoRA is 0.8 points lower, 95% CI [−1.0, −0.7]. The gap is real but small, largest for Amharic (−1.8)                                                                                                                                                                                                                                                          |
| 3. Is it cheap enough? (goal G7)                          | Same as SIB-200.                                                      | Yes: LoRA trains 0.14% of the parameters, peaks at 3.4 to 4.8 GB against 11.3 GB, and takes about 45 s per run against about 155 s                                                                                                                                                                                                                                    |
| 4. How well does transfer work across languages?          | RQ2: do related languages help each other more?                       | Full fine-tuning shown; LoRA gives the same pattern (Bantu sources 65.2% on Bantu targets against 47.2%). Transfer reaches 42 to 80% of the in-language score. The target explains 44% of the variation and the source 30%, so here the source language matters. A Bantu advantage: Bantu sources reach 66.1% on Bantu targets, Amharic and Hausa sources 50.0%. It holds for Hausa alone (49.6%), but Hausa is the only clean non-Bantu contrast |

Across the three tasks, zero-shot transfer gets weaker from topics to entities to parts of speech, and the source language matters more (target explains 95%, 81% and 44% of the variation). Whether related languages help more is clear only for POS, and rests on one non-Bantu contrast (Hausa). LoRA costs nothing on topics, 0.8 points on POS and 3.3 on NER. That order does not follow word structure (POS, the most word-form-sensitive task, has the smaller gap), and NER ran half as many epochs as POS (5 against 10), so the gap may reflect training budget rather than morphology. It is re-measured after the baselines are trained to convergence.

### 4. Why is Luganda weak on SIB-200? (diagnostic, done)

Details: [`results/sib200/interpretation.md`](results/sib200/interpretation.md) and [`results/pppl/summary.md`](results/pppl/summary.md), workbook tab "Luganda diagnostics".

| question                                                                                                                 | why it matters                                                                                                  | what we found                                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Does the model know Luganda text less well? (masked-LM pseudo-perplexity on the same 204 sentences in every language) | If the model barely knows a language, adapters must make up for missing pretraining, not only for tokenization. | Yes: 173.5 NLL per sentence for Luganda against 88 to 113 for the others; pseudo-perplexity 40 against 8 to 15                                                                 |
| 2. Is it the tokenizer?                                                                                                  | Fragmentation is what WP1 targets.                                                                              | No: Kinyarwanda and isiZulu are split as finely or more finely and score normally                                                                                              |
| 3. Is Luganda weak on every task?                                                                                        | Tells us whether the problem is the language or the dataset.                                                    | No: Luganda is not weak on NER (89.5 F1, second best) or POS (92.3%). The gap is concentrated on some SIB-200 (FLORES) sentences; the worst 30 sentences account for 62% of it |

### 5. Tokenizer fragmentation (no training, done)

Details: [`results/tokenizers/summary.md`](results/tokenizers/summary.md), workbook tabs "Tokenizer availability" and "Tokenizer stats". Text: the same 1,004 SIB-200 sentences in every language. Each model comes with its own tokenizer; the names below are models.

| question                                                                                                                          | why it matters                                                                         | what we found                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. How finely does our model split each language?                                                                                 | RQ1 starts from the claim that subword tokenizers break up morphologically rich words. | AfroXLMR-76L (XLM-R's vocabulary, never trained on kin, lug or zul) needs 1.65 tokens per word for Swahili up to 3.01 for isiZulu                                                                                                          |
| 2. Do other African models split less?                                                                                            | Shows how much a dedicated vocabulary could save.                                      | Serengeti splits least for every language (1.25 to 2.19 tokens per word). AfriBERTa and BantuBERTa are better on some languages and worse on others; mBERT maps 95% of Amharic to the unknown token                                        |
| 3. Do token boundaries fall on morpheme boundaries? (isiZulu only, the one language with gold segmentations: NCHLT, 11,392 words) | RQ1 is about preserving morphemes, not only about fewer tokens.                        | Barely above chance. Boundary F1 is 0.32 to 0.41 across tokenizers (AfroXLMR-76L 0.38), against a chance precision of 0.30; only 3 to 5% of words are split exactly into their morphemes                                                   |
| 4. Can an unsupervised segmenter (Morfessor) stand in for gold in Swahili, Kinyarwanda and Luganda?                               | No gold segmentations exist for those three languages.                                 | No: trained on 3.3M words of isiZulu web text, its best setting reaches boundary F1 0.45 on held-out gold words (0.48 on all gold words), only a little above the tokenizers. Boundary preservation is therefore reported for isiZulu only |

### 6. RQ1: changing how words reach the model, with embeddings frozen (Morfessor cuts and Serengeti's vocabulary, done)

Details: [`results/variants_summary.md`](results/variants_summary.md) and [`results/variants_interpretation.md`](results/variants_interpretation.md), workbook tab "Tokenization variants". All three variants use the model, LoRA settings, seeds and trainable parameters of the LoRA baseline; only the input differs, and the embeddings stay frozen. Differences are against plain LoRA, pooled over 6 languages and 3 seeds (CIs resample test sentences and seeds).

| question | why it matters | what we found |
| --- | --- | --- |
| 1. Does feeding Morfessor morphemes as separate words help? | Cheapest morphology-aware input: no new vocabulary, no new model. | No: NER −7.0 [−7.8, −6.1], POS −3.4 [−3.6, −3.2], lower in every language; zero-shot −12.4 and −9.8. Not truncation: no test word is cut off |
| 2. Does it help if the word stays one word and only its subword pieces stop at Morfessor's cuts? | Separates the effect of the morpheme cuts from the extra word starts. | Much less harmful, still not better: NER −3.9 [−4.9, −2.8], POS −0.5 [−0.6, −0.3] (Amharic POS +0.1). Same cuts and almost the same token counts as question 1, so the extra word starts did most of that damage. Whether *better* cuts would help is untested: Morfessor's precision on isiZulu gold is 0.51 |
| 3. Option B: does Serengeti's vocabulary, moved into AfroXLMR, help? | Serengeti splits least for all six languages (Tokenizer stats tab). | Not with frozen embeddings: NER −5.8 [−6.6, −5.1], POS −2.3 [−2.5, −2.1], although words get about a third shorter. A third to a half of the tokens carry averaged vectors that LoRA cannot change. Hypothesis (chosen after the fact, 6 languages): the NER loss grows with the share of new tokens in entity words. Lead: transfer into isiZulu rises (lug→zul +7.9, swa→zul +7.5) |
| 4. What does this mean for RQ1? | Decides the next experiments. | Without adaptation, input changes cost accuracy, least when the input stays close to pretraining. Whether morpheme-aligned input helps once the model can adapt is still open. Next: an adaptation ladder (frozen, trainable embeddings, short masked-LM pass), a scrambled-cut control, and converged baselines |

## Repository structure

```
.
├── README.md                      # this file: project summary and results so far
├── literature review/             # papers we have read, with notes
│   ├── TEMPLATE.md                # notes template for each paper
│   ├── reading-log.md             # index of all papers (start here)
│   ├── gaps-and-ideas.md          # research gaps and ideas from the literature
│   ├── notes/                     # one note per paper
│   └── papers/                    # local PDF copies (not pushed; notes link online)
├── docs/
│   ├── work-plan.md               # goals, timeline, venues, data and compute
│   └── proposal/                  # research proposal (local only, not pushed)
├── experiments/                   # experiment logs (one file per run, see TEMPLATE.md)
├── data/                          # datasets (local only, listed in data/README.md)
├── src/
│   ├── check_data_access.py       # checks every dataset and model in the work plan is reachable
│   ├── sib200_baseline.py         # SIB-200: in-language fine-tuning and 6x6 transfer matrix
│   ├── sib200_report.py           # SIB-200 tables
│   ├── token_baseline.py          # NER and POS: in-language fine-tuning and 6x6 transfer matrix
│   ├── token_report.py            # NER and POS tables
│   ├── pseudo_perplexity.py       # how well the model knows each language (Luganda diagnostic)
│   ├── tokenizer_stats.py         # fragmentation and morpheme-boundary scores per tokenizer
│   ├── morfessor_silver.py        # Morfessor segmenter scored against isiZulu gold
│   ├── morfessor_segment.py       # Morfessor morpheme splits for the NER and POS words (pre-segmentation)
│   ├── variants_report.py         # tokenization variants vs plain LoRA, NER and POS
│   ├── sweep_report.py            # LoRA sweep on Swahili dev: picks one LoRA setting per task
│   ├── vocab_transfer.py          # option B: Serengeti's vocabulary moved into AfroXLMR (FVT)
│   └── build_workbook.py          # builds results/results.xlsx from everything below
├── notebooks/
│   ├── sib200_colab.ipynb         # runs the SIB-200 baseline on Colab
│   ├── token_colab.ipynb          # runs the NER and POS baselines on Colab
│   ├── morfessor_colab.ipynb      # NER and POS with Morfessor pre-segmentation (LoRA) on Colab
│   ├── variants_colab.ipynb       # follow-ups: Morfessor cuts inside words, Serengeti vocabulary (LoRA)
│   └── sweep_colab.ipynb          # LoRA sweep (rank, target layers) on Swahili dev; no Drive needed
└── results/
    ├── results.xlsx               # every number in the project, one tab per experiment
    ├── data_access_report.md      # which datasets and models load
    ├── sib200/                    # SIB-200 runs, tables and interpretation
    ├── ner/                       # NER runs and tables
    ├── pos/                       # POS runs and tables
    ├── pppl/                      # pseudo-perplexity per language
    ├── <task>_morfessor/          # NER / POS LoRA, Morfessor morphemes as separate words
    ├── <task>_morfessor_inner/    # NER / POS LoRA, Morfessor cuts inside words
    ├── <task>_serengeti_fvt/      # NER / POS LoRA, Serengeti's vocabulary moved into AfroXLMR
    ├── variants_summary.md        # all tokenization variants against plain LoRA, with interpretation
    ├── tokenizers/                # fragmentation, morpheme boundaries, Morfessor
    └── morfessor_seg/             # Morfessor word splits per language, used by the pre-segmentation runs
```

## Tracking papers

1. Copy [`literature review/TEMPLATE.md`](literature%20review/TEMPLATE.md) into `literature review/notes/` as `YYYY-firstauthor-shortname.md`.
2. Add the paper to [`literature review/reading-log.md`](literature%20review/reading-log.md).
3. Copy any gaps or ideas into [`literature review/gaps-and-ideas.md`](literature%20review/gaps-and-ideas.md).

## Planning

See [`docs/work-plan.md`](docs/work-plan.md) for goals, work packages, target venues, datasets and compute.
