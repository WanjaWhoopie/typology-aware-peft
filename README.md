# Typology-Aware Parameter-Efficient Transfer Learning for Morphologically Rich, Low-Resource Languages
Research on typology-aware adapters that help LLMs handle morphologically rich, low-resource African languages (Swahili, Zulu, Amharic, Hausa and more) on low-cost hardware.

Languages: Amharic (amh), Hausa (hau), Kinyarwanda (kin), Luganda (lug), Swahili (swa), isiZulu (zul); the last four are Bantu. Model: [Davlan/afro-xlmr-large-76L](https://huggingface.co/Davlan/afro-xlmr-large-76L). Methods: full fine-tuning and LoRA (r = 8), 3 seeds each, on one Colab L4 GPU.

**All numbers are in one workbook, [`results/results.xlsx`](results/results.xlsx)**, one tab per experiment (rebuilt with `python src/build_workbook.py`). The `summary.md` and `interpretation.md` files in each `results/` folder hold the full tables and the reasoning behind them.

## Results so far

### 1. SIB-200 topic classification (baseline, done)

Details: [`results/sib200/interpretation.md`](results/sib200/interpretation.md), workbook tab "SIB-200".

| question | why it matters | what we found |
|---|---|---|
| 1. How well does the unchanged model do on each language? | This is the reference score every later method (WP1 to WP3) is compared against. | 84 to 89% topic accuracy for five languages; Luganda is clearly weaker at about 70% |
| 2. Does LoRA match full fine-tuning? | The project relies on PEFT. If LoRA lost a lot, it would be a weak base to build on. | Yes: pooled difference +0.7 points, 95% CI [−0.7, +2.0], so no real difference |
| 3. Is it cheap enough? (goal G7) | The project promises methods that run on one 16 GB GPU. | LoRA trains 0.33% of the parameters, peaks at 4.4 GB against 11.3 GB, and takes about 43 s per run against about 140 s |
| 4. How well does a model trained on one language work on the others? (the 6x6 zero-shot transfer matrix) | RQ2 needs to know whether related languages (the four Bantu ones) help each other more than unrelated ones (Amharic, Hausa). | Transfer is almost as good as in-language (92 to 102%). The target language explains about 95% of the variation and the source almost none. No Bantu advantage: Bantu sources reach about 79% on Bantu targets, Amharic and Hausa sources about 80% |

### 2. Named entity recognition, MasakhaNER (baseline, full fine-tuning done, LoRA pending)

Details: [`results/ner/summary.md`](results/ner/summary.md), workbook tab "NER". MasakhaNER 2.0 for five languages, MasakhaNER 1.0 for Amharic.

| question | why it matters | what we found |
|---|---|---|
| 1. How well does the unchanged model do on each language? | Reference score for a task that depends on word forms, where tokenization should matter more than for topic labels. | Entity F1 78% (Amharic) to 92% (Swahili). Luganda is not weak here (89.5%), so its SIB-200 weakness is specific to that task or dataset |
| 2. Does LoRA match full fine-tuning? | Same check as for SIB-200, on a harder task. | Not known yet: the LoRA runs crashed on a Colab library clash (fixed); 18 runs to rerun |
| 3. Is it cheap enough? (goal G7) | Same as SIB-200. | Full fine-tuning peaks at 11.3 GB and takes 3 to 14 minutes per run; LoRA figures follow with the rerun |
| 4. How well does transfer work across languages? | RQ2: do related languages help each other more? | Transfer is much weaker than for topics: 45 to 92% of the in-language score. The target explains 81% of the variation, the source 6%. A small Bantu advantage: Bantu sources reach 65.3 F1 on Bantu targets, Amharic and Hausa sources 60.2. isiZulu and Amharic are the hardest targets (about 50% of in-language) |

### 3. Part-of-speech tagging, MasakhaPOS (baseline, full fine-tuning done, LoRA pending)

Details: [`results/pos/summary.md`](results/pos/summary.md), workbook tab "POS". MasakhaPOS for five languages; UD Amharic-ATT for Amharic, split 70/10/20 by us.

| question | why it matters | what we found |
|---|---|---|
| 1. How well does the unchanged model do on each language? | Reference score for the most morphology-sensitive of our three tasks. | Accuracy 90% (isiZulu) to 98% (Kinyarwanda). Luganda is again not weak (92.3%) |
| 2. Does LoRA match full fine-tuning? | Same check as for SIB-200. | Not known yet: LoRA runs to rerun (18 runs) |
| 3. Is it cheap enough? (goal G7) | Same as SIB-200. | Full fine-tuning peaks at 11.3 GB and takes about 2.5 minutes per run; LoRA figures follow with the rerun |
| 4. How well does transfer work across languages? | RQ2: do related languages help each other more? | Transfer reaches 42 to 80% of the in-language score. The target explains 44% of the variation and the source 30%, so here the source language matters. A clear Bantu advantage: Bantu sources reach 66.1% on Bantu targets, Amharic and Hausa sources 50.0% |

Across the three tasks, the more a task depends on word structure (topics, then entities, then parts of speech), the weaker zero-shot transfer gets and the more language relatedness helps. This is the pattern RQ2 builds on.

### 4. Why is Luganda weak on SIB-200? (diagnostic, done)

Details: [`results/sib200/interpretation.md`](results/sib200/interpretation.md) and [`results/pppl/summary.md`](results/pppl/summary.md), workbook tab "Luganda diagnostics".

| question | why it matters | what we found |
|---|---|---|
| 1. Does the model know Luganda text less well? (masked-LM pseudo-perplexity on the same 204 sentences in every language) | If the model barely knows a language, adapters must make up for missing pretraining, not only for tokenization. | Yes: 173.5 NLL per sentence for Luganda against 88 to 113 for the others; pseudo-perplexity 40 against 8 to 15 |
| 2. Is it the tokenizer? | Fragmentation is what WP1 targets. | No: Kinyarwanda and isiZulu are split as finely or more finely and score normally |
| 3. Is Luganda weak on every task? | Tells us whether the problem is the language or the dataset. | No: Luganda is not weak on NER (89.5 F1, second best) or POS (92.3%). The gap is concentrated on some SIB-200 (FLORES) sentences; the worst 30 sentences account for 62% of it |

### 5. Tokenizer fragmentation (no training, done)

Details: [`results/tokenizers/summary.md`](results/tokenizers/summary.md), workbook tabs "Tokenizer availability" and "Tokenizer stats". Text: the same 1,004 SIB-200 sentences in every language. Each model comes with its own tokenizer; the names below are models.

| question | why it matters | what we found |
|---|---|---|
| 1. How finely does our model split each language? | RQ1 starts from the claim that subword tokenizers break up morphologically rich words. | AfroXLMR-76L (XLM-R's vocabulary, never trained on kin, lug or zul) needs 1.65 tokens per word for Swahili up to 3.01 for isiZulu |
| 2. Do other African models split less? | Shows how much a dedicated vocabulary could save. | Serengeti splits least for every language (1.25 to 2.19 tokens per word). AfriBERTa and BantuBERTa are better on some languages and worse on others; mBERT maps 95% of Amharic to the unknown token |
| 3. Do token boundaries fall on morpheme boundaries? (isiZulu only, the one language with gold segmentations: NCHLT, 11,392 words) | RQ1 is about preserving morphemes, not only about fewer tokens. | Barely above chance. Boundary F1 is 0.32 to 0.41 across tokenizers (AfroXLMR-76L 0.38), against a chance precision of 0.30; only 3 to 5% of words are split exactly into their morphemes |
| 4. Can an unsupervised segmenter (Morfessor) stand in for gold in Swahili, Kinyarwanda and Luganda? | No gold segmentations exist for those three languages. | No: trained on 3.3M words of isiZulu web text, its best setting reaches boundary F1 0.45 on held-out gold words (0.48 on all gold words), only a little above the tokenizers. Boundary preservation is therefore reported for isiZulu only |

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
│   └── build_workbook.py          # builds results/results.xlsx from everything below
├── notebooks/
│   ├── sib200_colab.ipynb         # runs the SIB-200 baseline on Colab
│   └── token_colab.ipynb          # runs the NER and POS baselines on Colab
└── results/
    ├── results.xlsx               # every number in the project, one tab per experiment
    ├── data_access_report.md      # which datasets and models load
    ├── sib200/                    # SIB-200 runs, tables and interpretation
    ├── ner/                       # NER runs and tables
    ├── pos/                       # POS runs and tables
    ├── pppl/                      # pseudo-perplexity per language
    └── tokenizers/                # fragmentation, morpheme boundaries, Morfessor
```

## Tracking papers

1. Copy [`literature review/TEMPLATE.md`](literature%20review/TEMPLATE.md) into `literature review/notes/` as `YYYY-firstauthor-shortname.md`.
2. Add the paper to [`literature review/reading-log.md`](literature%20review/reading-log.md).
3. Copy any gaps or ideas into [`literature review/gaps-and-ideas.md`](literature%20review/gaps-and-ideas.md).

## Planning

See [`docs/work-plan.md`](docs/work-plan.md) for goals, work packages, target venues, datasets and compute.
