# Typology-Aware Parameter-Efficient Transfer Learning for Morphologically Rich, Low-Resource Languages
Research on typology-aware adapters that help LLMs handle morphologically rich, low-resource African languages (Swahili, Zulu, Amharic, Hausa and more) on low-cost hardware.

## Repository structure

```
.
├── literature review/     # papers we have read, with notes
│   ├── TEMPLATE.md        # notes template for each paper
│   ├── reading-log.md     # index of all papers (start here)
│   ├── gaps-and-ideas.md  # research gaps and ideas from the literature
│   ├── notes/             # one note per paper
│   └── papers/            # local PDF copies (not pushed; notes link online)
├── docs/
│   ├── work-plan.md       # goals, timeline, venues, data and compute
│   ├── proposal/          # research proposal (local only, not pushed)
│   └── meetings/          # meeting notes
├── experiments/           # experiment logs (one file per run)
├── data/                  # datasets (local only, listed in data/README.md)
├── src/                   # source code (adapters, training, evaluation)
├── notebooks/             # exploratory Jupyter notebooks
└── results/               # figures, tables and metrics for the write-up
```

## Tracking papers

1. Copy [`literature review/TEMPLATE.md`](literature%20review/TEMPLATE.md) into `literature review/notes/` as `YYYY-firstauthor-shortname.md`.
2. Add the paper to [`literature review/reading-log.md`](literature%20review/reading-log.md).
3. Copy any gaps or ideas into [`literature review/gaps-and-ideas.md`](literature%20review/gaps-and-ideas.md).

## Planning

See [`docs/work-plan.md`](docs/work-plan.md) for goals, work packages, target venues, datasets and compute.
