# Research Gaps and Ideas

A running list of gaps, limitations and ideas pulled from the papers we read. This is where the literature review turns into our research direction.

When you finish a paper's notes, copy any strong gaps or ideas here and link back to the note.

## Research gaps

| Gap | Source paper(s) | How our work could address it | Priority |
|---|---|---|---|
| Tokenizers for African languages judged only by downstream accuracy; no fertility or morpheme-boundary metrics | [Parvess 2023](notes/2023-parvess-bantuberta.md), [Ndomba 2025](notes/2025-ndomba-tokenizers-african-languages.md), [Ndomba 2024](notes/2024-ndomba-swahili-tokenizer.md) | WP0 fragmentation study and WP1 metrics | High |
| Language-family grouping only tested by pretraining from scratch, which fails with little data | [Parvess 2023](notes/2023-parvess-bantuberta.md) | Test family/typology grouping with adapters on a strong existing model (WP3) | High |
| "Typology" treated as family membership only (static, categorical) | [Parvess 2023](notes/2023-parvess-bantuberta.md) | Learned typology vectors (WP2); Guthrie zones as an extra static baseline | Medium |
| Tokenizers never tested inside a transformer (only bag-of-tokens classifiers) | [Ndomba 2025](notes/2025-ndomba-tokenizers-african-languages.md), [Ndomba 2024](notes/2024-ndomba-swahili-tokenizer.md) | Evaluate tokenization changes inside the model (WP1) | High |
| Single runs, copied baselines, no significance tests | [Parvess 2023](notes/2023-parvess-bantuberta.md), [Ndomba 2024](notes/2024-ndomba-swahili-tokenizer.md) | 3+ seeds, same fine-tuning setup for all baselines, significance tests | Medium |

## Prior work flagged by external reviews (21 Nov 2026), checked by reading

Two external reviews of the repo (not the professor) listed published work that changes what is still open. All rows are in the [reading log](reading-log.md) (rows 6 to 41), each read in full by a research agent on 2026-11-21 with a note in `notes/`.

**What reading changed (21 Nov):**
- **RQ2 is largely taken as framed.** Idris et al. 2026 already test whether embedding similarity predicts transfer for our six languages, with AfroXLMR-large, on MasakhaNER 2.0 and MasakhaPOS (one seed, no LoRA, no overlap covariate). Still open: whether text-derived morphology predicts transfer once entity/token overlap and the target are controlled, and whether LoRA changes which features matter. Four Bantu languages cannot support a correlational claim.
- **Every positive morphology result lets something adapt after the change** (MLM on embeddings or the body: FVT, FOCUS, LGSE, UNKs, Kumar & Dušek) or pretrains from scratch (KinyaBERT, Meyer & Buys, Hou). Our frozen-embedding drops are what the literature predicts. FOCUS also finds the original vocabulary + the same adaptation almost as good, so that control is essential.
- **Several review claims were overstated:** SEC's 1% is relative to the embedding matrix; UNKs Everywhere trains its adapters; MAD-G's African NER gains are mostly on languages its generator saw; Fekete et al. is adapter averaging for Creole MT, not typology; Lauscher's few-shot gains are large for POS, moderate for NER; Meyer & Buys 2022 gains are intrinsic (BPC) only.
- **A clean null is publishable:** three studies find morphological alignment predicts little (all decoder LLMs); our encoder + PEFT + NER/POS setting is untested.
- **Risk for RQ3:** TIPA reports that LoRA "did not see strong results" in preliminary tests; pooled multi-source fine-tuning nearly matched ZGUL on African NER, so it is a mandatory baseline.


| Research question | What is already published | What still looks open | Consequence for us |
|---|---|---|---|
| RQ1: morpheme-aware input or embeddings | Morphology-aware segmentation helps when the model is pretrained with it (KinyaBERT, Meyer & Buys 2022, EMNLP 2023 comparison). Vocabulary swaps work with a training step after initialisation (FVT, FOCUS, which already covers swa, hau, xho on MasakhaNER 2.0). Embedding-side PEFT exists (SEC 2026, UNKs Everywhere 2021). Several papers find morphological alignment explains little (Arnett & Bergen 2025, MorphScore, preprints) | A PEFT-only, cross-lingual Bantu method with a morphological prior on the Masakhane benchmarks | Run the masked-LM rung before concluding on option B; SEC, FOCUS and UNKs Everywhere become baselines; add a scrambled-cut control |
| Fragmentation study | The African Language Tax (20 languages, 11 tokenizers, preprint), MorphScore (70 languages) | Gold-boundary analysis for the Nguni languages | Fertility alone is not publishable; keep the isiZulu boundary analysis |
| RQ2: text-derived typology predicts transfer | Language vectors from BPE statistics (Computational Linguistics, 47 languages), Yu et al. 2021, Entropy2Vec; NN-Rank ranks sources from model representations. Another Computational Linguistics paper warns of false positives | Prediction within Bantu | Use the published vectors as baselines, adopt the false-positive controls, test on POS with token overlap as a covariate (NER transfer follows shared names: IJCNLP-AACL 2023) |
| RQ3: typology-gated adapters | UDapter, MAD-G (gains on African NER), Hyper-X, ZGUL (African group on MasakhaNER), TIPA; Fekete et al. 2025 find random adapters work as well | A gate that beats a shuffled-typology gate | Run cheap baselines and the shuffled control before building the mixture |
| LoRA gap | PEFT keeps up on small training sets (≤1k) but not medium ones (EMNLP 2022) | | Test with the 100 / 1k settings before reading the gap as morphology |
| isiZulu transfer lead | Word-boundary conventions may hurt transfer more than unrelatedness (Findings of NAACL 2024, translation); MasakhaNER 2.0 notes prefix-plus-capital names | Whether this holds for tagging | Setswana (disjunctive) would be the contrast if languages are added |

## Recurring themes

<!-- Patterns across several papers, e.g. "most work uses multilingual tokenizers that fragment agglutinative words". -->

- Swahili dominates "Bantu" resources; other Bantu languages get a small share ([Parvess 2023](notes/2023-parvess-bantuberta.md))
- African multilingual models/tokenizers (AfroXLMR, AfriBERTa, Serengeti) beat global ones (XLM-R, mBERT) on African languages ([Ndomba 2025](notes/2025-ndomba-tokenizers-african-languages.md))
- Linguistic explanations (loanwords, tone, "linguistic bonds") are offered but not measured ([Ndomba 2025](notes/2025-ndomba-tokenizers-african-languages.md), [Parvess 2023](notes/2023-parvess-bantuberta.md))

## Ideas to try

- [ ] Measure fragmentation per morpheme as well as per orthographic word, so conjunctive (Zulu, Xhosa) and disjunctive (Sotho, Tswana) spelling are comparable. Source: [Parvess 2023](notes/2023-parvess-bantuberta.md)
- [ ] Compare a LoRA trained on Bantu-only languages vs mixed families for transfer to an unseen Bantu language. Source: [Parvess 2023](notes/2023-parvess-bantuberta.md)

## Baselines and datasets mentioned

| Name | Type (model / dataset / benchmark) | Languages | Source paper | Link |
|---|---|---|---|---|
| BantuBERTa | Model (125M encoder) | 15 Bantu (+ Oromo) | [Parvess 2023](notes/2023-parvess-bantuberta.md) | [HF](https://huggingface.co/dsfsi/BantuBERTa) |
| ANTC (African News Topic Classification) | Benchmark | incl. Zulu, Lingala | [Parvess 2023](notes/2023-parvess-bantuberta.md) | [Alabi et al. 2022](https://aclanthology.org/2022.coling-1.382) |
| Serengeti | Model / tokenizer | 517 African languages | [Ndomba 2025](notes/2025-ndomba-tokenizers-african-languages.md) | [ACL Anthology](https://aclanthology.org/2023.findings-acl.97) |
| NaijaSenti | Dataset (sentiment) | Hausa, Yoruba, Igbo, Pidgin | [Ndomba 2025](notes/2025-ndomba-tokenizers-african-languages.md) | [LREC 2022](https://aclanthology.org/2022.lrec-1.63) |
| NCHLT text corpora | Dataset (clean text) | 9 South African Bantu languages | [Parvess 2023](notes/2023-parvess-bantuberta.md) | [SADiLaR](https://repo.sadilar.org/) |
| FOCUS | Method (tokenizer swap + embedding init + continued pretraining) | swa, hau, xho (MasakhaNER 2.0) | external review | [DOI](https://doi.org/10.18653/v1/2023.emnlp-main.829) |
| SEC | Method (sparse low-rank embedding corrections) | low-resource NER, POS | external review | [ACL Anthology](https://aclanthology.org/2026.findings-emnlp.1033/) |
| UNKs Everywhere | Method (new embeddings under frozen adapters) | many | external review | [DOI](https://doi.org/10.18653/v1/2021.emnlp-main.800) |
| MAD-G | Method (adapters generated from typology) | incl. African NER | external review | [DOI](https://doi.org/10.18653/v1/2021.findings-emnlp.410) |
| ZGUL | Method (ensemble of related-language adapters) | African group on MasakhaNER | external review | [DOI](https://doi.org/10.18653/v1/2023.emnlp-main.431) |
| Hyper-X | Method (adapters from language embeddings) | many | external review | [DOI](https://doi.org/10.18653/v1/2022.emnlp-main.541) |
| NN-Rank | Method (source-language ranking) | 51 source languages | external review | [DOI](https://doi.org/10.18653/v1/2025.emnlp-main.1650) |
| BPE-statistics language vectors | Baseline (typology from text) | 47 languages | external review | [DOI](https://doi.org/10.1162/coli_a_00489) |
