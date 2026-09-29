# Research Gaps and Ideas

A running list of gaps, limitations and ideas pulled from the papers we read. This is where the literature review turns into our research direction.

When you finish a paper's notes, copy any strong gaps or ideas here and link back to the note.

## Research gaps

| Gap | Source paper(s) | How our work could address it | Priority |
|---|---|---|---|
| Tokenizer fragmentation of Bantu words is discussed but never measured (no fertility or morpheme-boundary metrics) | [Parvess 2023](notes/2023-parvess-bantuberta.md) | WP0 fragmentation study and WP1 metrics | High |
| Language-family grouping only tested by pretraining from scratch, which fails with little data | [Parvess 2023](notes/2023-parvess-bantuberta.md) | Test family/typology grouping with adapters on a strong existing model (WP3) | High |
| "Typology" treated as family membership only (static, categorical) | [Parvess 2023](notes/2023-parvess-bantuberta.md) | Learned typology vectors (WP2); Guthrie zones as an extra static baseline | Medium |
| Single runs, copied baselines, no significance tests | [Parvess 2023](notes/2023-parvess-bantuberta.md) | 3+ seeds, same fine-tuning setup for all baselines, significance tests | Medium |

## Recurring themes

<!-- Patterns across several papers, e.g. "most work uses multilingual tokenizers that fragment agglutinative words". -->

- Swahili dominates "Bantu" resources; other Bantu languages get a small share ([Parvess 2023](notes/2023-parvess-bantuberta.md))

## Ideas to try

- [ ] Measure fragmentation per morpheme as well as per orthographic word, so conjunctive (Zulu, Xhosa) and disjunctive (Sotho, Tswana) spelling are comparable. Source: [Parvess 2023](notes/2023-parvess-bantuberta.md)
- [ ] Compare a LoRA trained on Bantu-only languages vs mixed families for transfer to an unseen Bantu language. Source: [Parvess 2023](notes/2023-parvess-bantuberta.md)

## Baselines and datasets mentioned

| Name | Type (model / dataset / benchmark) | Languages | Source paper | Link |
|---|---|---|---|---|
| BantuBERTa | Model (125M encoder) | 15 Bantu (+ Oromo) | [Parvess 2023](notes/2023-parvess-bantuberta.md) | [HF](https://huggingface.co/dsfsi/BantuBERTa) |
| ANTC (African News Topic Classification) | Benchmark | incl. Zulu, Lingala | [Parvess 2023](notes/2023-parvess-bantuberta.md) | [Alabi et al. 2022](https://aclanthology.org/2022.coling-1.382) |
| NCHLT text corpora | Dataset (clean text) | 9 South African Bantu languages | [Parvess 2023](notes/2023-parvess-bantuberta.md) | [SADiLaR](https://repo.sadilar.org/) |
