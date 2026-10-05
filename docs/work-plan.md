# Work Plan: Typology-Aware PEFT for Morphologically Rich, Low-Resource Languages

|                  |                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Period**       | October 2026 – January 2027 (4 months)                                                                                                            |
| **Last updated** | 2026-10-05                                                                                                                                        |
| **Status**       | Month 0: setup and literature review                                                                                                              |
| **Languages**    | Core (all work packages): Kiswahili, Kinyarwanda, Luganda, isiZulu (Bantu). Contrast for RQ2 and the baselines only: Amharic, Hausa (Afroasiatic) |

> Venue dates marked **(expected)** have not been announced yet and are based on earlier editions. Check the linked pages before planning around them. Venue links and dates were last checked on 2026-09-29. Dataset coverage marked ✓ was checked against the Hugging Face dataset cards (and the UD page for Amharic) on 2026-10-05.

**How the 4 months are used.** RQ1 (tokenisation) is answered in full. RQ2, RQ3 and RQ4 are each answered with a small pilot that gives a preliminary, honestly reported result (positive or negative). Everything that does not fit in the window is listed in Section 9 as future work.

---

## 1. Goals

### Overall aim

Build PEFT modules that use a language's structure (agglutination, prefixing, noun-class systems) to adapt multilingual models to Bantu morphologically rich languages, and to **transfer** what is learned in one language to others with little or no target data. They should train **under 2% of the base model's parameters** and have **final configurations that train on one 16–24 GB GPU**.

Every work package reports two settings: **in-language** (train and test on the same language) and **cross-lingual transfer** (train on source language(s), test on a different target; protocol in WP0).

### Goals mapped to the research questions

| RQ (from the proposal)                                                                                                                         | Goal                                        | Target (hypothesis to test)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Scope by Jan 2027 |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| **RQ1 (Tokenisation):** How can we adapt tokenization to preserve word parts (morphemes) in low-resource languages without breaking the model? | G1 Preserve morphemes                       | ≥15% lower fertility (tokens per word) and higher morpheme-boundary F1 than the base tokenizer on all 4 core languages, **without changing the vocabulary**                                                                                                                                                                                                                                                                                                                                                                                                                    | **Full**          |
|                                                                                                                                                | G2 Do not break the model                   | Task scores on NER, POS and SIB-200 are not worse than the base model with standard LoRA (no significant drop over 3 seeds), and the adapter beats it by **+2 F1 on NER/POS** at the same parameter budget                                                                                                                                                                                                                                                                                                                                                                     | **Full**          |
|                                                                                                                                                | G3 Morpheme preservation transfers          | Cross-lingual transfer (shared protocol, Section 3 WP0): an adapter trained on one source language scores higher on the other three target languages than standard LoRA, zero-shot and with 100 and 1k target examples (+1 F1 average over the 12 source → target pairs)                                                                                                                                                                                                                                                                                                       | **Full**          |
| **RQ2 (Typology):** Can we automatically discover a language's structural traits from raw text instead of relying on static databases?         | G4 Data-driven typology that helps transfer | Pilot on 6 languages (4 Bantu + Amharic, Hausa), three checks: (a) **transfer prediction (main):** distance between latent vectors predicts the 30-pair zero-shot transfer matrix (Spearman ρ) better than URIEL/WALS vectors and a genealogy baseline; (b) **sanity:** the vectors separate the Bantu cluster from Amharic and Hausa as linguists expect; (c) **plug-in:** used as the gate in the RQ3 pilot, they do at least as well as static URIEL vectors. Controls: a script control (romanised Amharic) and a simple-statistics baseline (fertility, type-token ratio) | **Pilot**         |
| **RQ3 (Adapters):** How can we combine modular adapters to maximize cross-lingual learning with very little data?                              | G5 Low-data transfer                        | Pilot: with several source languages and a held-out target (leave-one-language-out), typology-gated Mixture-of-LoRA beats single LoRA and MAD-X-style stacking at 100 and 1k target examples on NER/POS. A small test also checks whether layer-wise rank allocation beats uniform rank at the same parameter budget                                                                                                                                                                                                                                                           | **Pilot**         |
| **RQ4 (Generative models):** How do these typology-aware methods perform in large generative language models?                                  | G6 Generative LLMs                          | Pilot: the G2 and G3 gains (and the G5 gain if ready) are measured on one small decoder trained with QLoRA, on SIB-200 and FLORES subsets. A 7–8B model is future work                                                                                                                                                                                                                                                                                                                                                                                                         | **Pilot**         |
| All (constraints from the problem statement)                                                                                                   | G7 Low-cost claim is real                   | Final methods train on a single 16 GB GPU (Kaggle/Colab T4 or P100). Peak memory and time are reported for every run                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Full              |
|                                                                                                                                                | G8 Open science                             | Release code, trained adapters (Hugging Face), latent typology vectors and evaluation scripts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Full              |

### Main outputs (by end of January 2027)

1. **Paper 1 (WP1, RQ1):** morpheme-preserving embeddings/adapters, in-language and cross-lingual. Submitted to ARR January 2027 cycle for ACL 2027.
2. **Project report:** one section per RQ with the result and its limits (RQ2 to RQ4 as pilots), plus the plan for the full studies.
3. Open-source release: code, adapters, typology vectors and evaluation scripts.

---

## 2. Languages

The four core languages are Bantu and concatenative (prefixing, noun-class agreement, long verb-prefix chains). They differ in orthography (isiZulu is conjunctive, Kiswahili and Luganda are more disjunctive), in resource level and in how much morphological annotation exists. Amharic and Hausa are added only as **contrast languages** so RQ2 has a real typological difference to detect; they are used in the WP0 baselines, the transfer matrix and the RQ2 pilot, not in the WP1 ablations, the WP3 held-out targets or WP4.

| Language    | Code | Role                                                                                                        | Morphology resources                                                              |
| ----------- | ---- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Kiswahili   | swa  | Core. Highest-resource; development language                                                                | UniMorph, Morfessor                                                               |
| isiZulu     | zul  | Core. Conjunctive orthography, longest words; the only core language with gold segmentation                 | NCHLT (SADiLaR), UniMorph                                                         |
| Kinyarwanda | kin  | Core. Rich verbal morphology; closest prior work (KinyaBERT)                                                | Morphological analyser from KinyaBERT (check availability and licence), Morfessor |
| Luganda     | lug  | Core. Lowest-resource of the four                                                                           | Morfessor only                                                                    |
| Amharic     | amh  | Contrast. Semitic, root-and-pattern; Ge'ez script                                                           | UD_Amharic-ATT (manually segmented clitics), UniMorph amh and HornMorpho (check)  |
| Hausa       | hau  | Contrast. Chadic; the easiest Afroasiatic data (NER, POS and news all exist) but not templatic like Semitic | none checked; use Morfessor if needed                                             |

**Limitations to state in every paper:** the core results cover one family. The RQ2 pilot has two families and 6 languages (30 transfer pairs), so it can support "this works on a clear contrast", not general typology discovery. Amharic differs from the Bantu languages in script, corpus size and domain as well as in morphology, so every RQ2 result needs the script control (see Risks).

### Benchmark coverage

✓ = checked on the dataset card on 2026-10-05. ✓\* = carried over from the earlier version of this plan, not rechecked. ? = not checked yet. ✗ = not in the dataset.

| Language    | NER                                                  | POS                                                   | MasakhaNEWS      | SIB-200 / FLORES | AfriSenti | IrokoBench | UniMorph |
| ----------- | ---------------------------------------------------- | ----------------------------------------------------- | ---------------- | ---------------- | --------- | ---------- | -------- |
| Kiswahili   | MasakhaNER 2.0 ✓                                     | MasakhaPOS ✓                                          | ✓                | ✓\*              | ✓\*       | ✓\*        | ✓\*      |
| Kinyarwanda | MasakhaNER 2.0 ✓                                     | MasakhaPOS ✓                                          | ✗ (Kirundi only) | ✓\*              | ?         | ?          | ?        |
| Luganda     | MasakhaNER 2.0 ✓                                     | MasakhaPOS ✓                                          | ✓                | ✓\*              | ?         | ✓\*        | ?        |
| isiZulu     | MasakhaNER 2.0 ✓                                     | MasakhaPOS ✓                                          | ✗                | ✓\*              | ✗\*       | ✓\*        | ✓\*      |
| Amharic     | MasakhaNER **1.0** ✓ (1,750 / 250 / 500; not in 2.0) | UD_Amharic-ATT ✓ (1,074 sentences; not in MasakhaPOS) | ✓                | ✓\*              | ✓\*       | ✓\*        | ✓\*      |
| Hausa       | MasakhaNER 2.0 ✓                                     | MasakhaPOS ✓                                          | ✓                | ✓\*              | ✓\*       | ✓\*        | ?        |

**Task choice follows from this table:** NER and POS (all six languages) are the main tasks. Topic classification uses SIB-200 for all six, because MasakhaNEWS lacks Kinyarwanda and isiZulu. MasakhaNEWS is an extra for Kiswahili, Luganda, Amharic and Hausa only.

**Data caveats:** Amharic NER comes from MasakhaNER 1.0 and the others from 2.0, so annotation and splits differ (footnote it in results tables). Amharic POS is small (about 1k sentences), so POS scores for Amharic will be noisy; give them less weight in the transfer matrix and report NER-only and POS-only matrices as well as the pooled one.

---

## 3. Work packages and tasks

### WP0: Setup and literature review (Oct – Nov 2026)

- [ ] Read and take notes on 15–20 priority papers (see `literature review/reading-log.md`), in this order:
  - [Typology-Guided Adaptation in Multilingual Models (Nakashole, ACL 2025)](https://aclanthology.org/2025.acl-long.1059/). **Closest prior work for WP3:** MoI-MoE routes on morphology over 10 Bantu languages, the same family as our core languages. Our pilot must be clearly different from it
  - [KinyaBERT (Nzeyimana & Rubungo, ACL 2022)](https://aclanthology.org/2022.acl-long.367): morphology-aware Kinyarwanda model with a two-tier encoder. **Closest prior work for RQ1**, so read it before claiming novelty for WP1
  - [IFCLoRA: Topology-Aware Rank Allocation for PEFT (arXiv 2607.22251)](https://arxiv.org/abs/2607.22251): the "topology-aware" baseline cited in the proposal
  - [LoRA (Hu et al., 2021)](https://arxiv.org/abs/2106.09685), [QLoRA (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314), [AdaLoRA (Zhang et al., 2023)](https://arxiv.org/abs/2303.10512), [MAD-X (Pfeiffer et al., 2020)](https://arxiv.org/abs/2005.00052)
  - [URIEL+ (Khan et al., COLING 2025)](https://aclanthology.org/2025.coling-main.463.pdf), [IrokoBench (Adelani et al., 2024)](https://arxiv.org/abs/2406.03368)
  - The 3 tokenizer papers already read; the rest of the 30–40 target moves to background reading after January
- [ ] Set up the environment: PyTorch, Hugging Face `transformers`, [`peft`](https://github.com/huggingface/peft), [`adapters`](https://github.com/adapter-hub/adapters), `bitsandbytes`, [`lm-evaluation-harness`](https://github.com/EleutherAI/lm-evaluation-harness)
- [ ] Set up experiment tracking (Weights & Biases or MLflow) and a shared results table
- [ ] Write data loaders for every dataset in Section 6 and record them in `data/README.md`
- [ ] **Baselines:** standard LoRA, AdaLoRA and MAD-X adapters on AfroXLMR-large for NER, POS and SIB-200 on all 6 languages (the 4 Bantu core languages plus Amharic and Hausa). This is the reference table every WP compares against, and it also supplies the 30-pair zero-shot transfer matrix for the RQ2 pilot
- [ ] **Shared cross-lingual transfer protocol** (used by every WP so results are comparable):
  - Core pairs (G3, WP1, WP3, WP4): all 12 ordered source → target pairs among swa, kin, lug, zul
  - Settings: zero-shot, then 100 and 1k target training examples (same sampled subsets for every method, 3 seeds)
  - RQ2 matrix: zero-shot only, all 30 ordered pairs among the 6 languages (train 6 source models per task; evaluating the other 5 targets is cheap)
  - Tasks: NER and POS, SIB-200 for zero-shot only
  - Metric: F1 (NER), accuracy (POS), and the average gain over standard LoRA with the same source training
  - Output: the 12-pair core matrix and the 30-pair RQ2 matrix
- [ ] **Tokenizer fragmentation study:** fertility, continued-word ratio and morpheme-boundary F1 for XLM-R, AfroXLMR, Llama 3.x, Gemma and InkubaLM tokenizers on all 6 languages (for Amharic report fertility per character as well as per word, since the script differs). Gives early material for a workshop paper

**Deliverables:** reading log with ≥15 notes, baseline results table, fragmentation analysis.

### WP1: Morpheme-preserving embeddings (RQ1, full) (Nov 2026 – Jan 2027)

Core languages only (swa, kin, lug, zul).

- [ ] Build gold or silver morpheme segmentations:
  - isiZulu: NCHLT annotated corpora ([SADiLaR](https://repo.sadilar.org/)) as gold
  - Kinyarwanda: KinyaBERT morphological analyser if usable, otherwise Morfessor
  - Kiswahili and Luganda: unsupervised [Morfessor](https://github.com/aalto-speech/morfessor) (check [UniMorph swa](https://github.com/unimorph/swa) for Kiswahili evaluation)
- [ ] Design soft-token / embedding adapters that add morphological priors (root, prefix and affix embeddings pooled into subword embeddings), keeping the vocabulary unchanged
- [ ] Ablations: segmentation source (gold or analyser, Morfessor, none; gold only possible for isiZulu and maybe Kinyarwanda); adapter placement (embedding layer only, or embedding plus lower layers)
- [ ] Evaluate intrinsically (fertility, boundary F1) and on tasks (MasakhaNER 2.0, MasakhaPOS, SIB-200) at matched parameter budgets, 3 seeds, including the no-regression check for G2
- [ ] **Cross-lingual transfer (G3, December):** take the best adapter, the main ablation and standard LoRA, train on each source language, and evaluate on the other three with the WP0 protocol (zero-shot, 100 and 1k examples). Check whether preserving morphemes helps transfer, and whether it helps more for nearby targets (e.g. swa → kin)
- [ ] Measure peak GPU memory and throughput for every setting (goal G7)
- [ ] Freeze main results by 15 Dec 2026, then write and submit Paper 1 to ARR (January 2027 cycle, for ACL 2027)

### WP2: Dynamic latent typology (RQ2, pilot) (Dec 2026 – early Jan 2027)

RQ2 is judged by whether the discovered typology **helps parameter-efficient transfer**, which keeps it tied to the project title.

- [ ] Train a small unsupervised encoder on raw text (WURA, with MADLAD-400 or Glot500 as fallback for any of the 6 languages WURA lacks; equal-size samples per language) that outputs a continuous typology vector per language. Signals: morpheme statistics from WP1, subword co-occurrence, adapter weight similarity
- [ ] **Check (a), transfer prediction (main):** Spearman ρ between vector distance and the 30-pair zero-shot transfer matrix from WP0, compared with URIEL+/lang2vec vectors, WALS/Grambank features for these 6 languages, and a genealogy baseline (same family or not). Report NER-only, POS-only and pooled matrices
- [ ] **Check (b), sanity:** do the vectors separate the Bantu cluster from Amharic and Hausa the way linguists expect, and are they stable across different text samples of the same language? Quick check on 6 languages, no large probing study
- [ ] **Check (c), plug-in:** use the vectors as the gate in the WP3 Mixture-of-LoRA pilot and compare with static URIEL vectors
- [ ] **Controls:** (1) script: repeat with a romanised copy of the Amharic text so the vectors cannot be driven by Ge'ez script alone; (2) simple-statistics baseline (fertility, type-token ratio, word-length distribution); if it matches the learned encoder, report that as the result
- [ ] Report what 6 languages and 2 families can and cannot show (30 pairs, one family contrast)
- Not in the pilot: probing against Grambank across many languages, within-language variation (dialect, domain, code-switching), more than 6 languages (see Section 9)

### WP3: Typology-guided Mixture-of-Adapters (RQ3, pilot) (late Nov 2026 – early Jan 2027)

- [ ] Build a small Mixture-of-LoRA (2–3 experts) with a gate conditioned on typology vectors. **Start with static URIEL vectors so WP3 is not blocked on WP2**, then swap in the WP2 vectors if they are ready by mid-December
- [ ] Cross-lingual low-data setting: source languages drawn from the 6-language pool (so the gate has a real contrast to route between), a held-out target among the 4 Bantu core languages (leave-one-language-out), 100 and 1k target examples, NER and POS, using the shared WP0 transfer protocol
- [ ] **Layer-wise rank allocation (small test):** probe each layer for morphological information (e.g. morpheme-boundary probe from WP1), allocate more LoRA rank to the layers that carry it, and compare with uniform rank and with AdaLoRA at the same total parameter budget. One configuration only, on the same transfer setting. This tests the abstract's claim that layers specialise in different levels of abstraction
- [ ] Baselines: single LoRA, MAD-X-style stacking. Add AdaLoRA and MoI-MoE (Nakashole 2025) only if their code is available and cheap to run; otherwise compare conceptually and say so
- Not in the pilot: 10k setting, a full study of rank allocation (searching several allocation signals), zero-shot to other families as targets, AfriXNLI

### WP4: Generative LLMs (RQ4, pilot) (mid Dec 2026 – early Jan 2027)

- [ ] Port the WP1 adapter (and the WP3 gate if ready) to one small decoder-only model with QLoRA (4-bit). Candidate: InkubaLM-0.4B (I recall it covers Kiswahili and isiZulu but not Kinyarwanda or Luganda; check) or a 1–3B model that covers all four core languages
- [ ] Evaluate on SIB-200 and a FLORES subset (chrF++) in the languages the model covers, using `lm-evaluation-harness`
- [ ] Include one transfer test (train on one language, test zero-shot on another the model covers)
- [ ] Confirm the configuration trains on a single 16 GB GPU (goal G7)
- Not in the pilot: 7–8B models, IrokoBench full suite, AfriQA/TyDi QA

### WP5: Write-up and release (Jan 2027)

- [ ] Paper 1 submitted to ARR (check the exact January date as soon as it is announced; there is no buffer after it)
- [ ] Project report: one section per RQ with result, limits and what a full study needs
- [ ] Release code on GitHub, adapters and typology vectors on Hugging Face, and a model card for each adapter

---

## 4. Timeline

| Month                               | Oct 26 | Nov         | Dec      | Jan 27     |
| ----------------------------------- | ------ | ----------- | -------- | ---------- |
| WP0 Setup + lit review + baselines  | ■      | ■           |          |            |
| WP1 Morpheme embeddings (RQ1)       |        | ■           | ■        | □ write-up |
| WP2 Latent typology pilot (RQ2)     |        | □ data prep | ■        | ■          |
| WP3 Mixture-of-Adapters pilot (RQ3) |        | ■ (late)    | ■        | ■ (early)  |
| WP4 Generative LLM pilot (RQ4)      |        |             | ■ (late) | ■ (early)  |
| WP5 Write-up and release            |        |             |          | ■          |
| Literature review (ongoing)         | ■      | ■           | □        | □          |

■ main focus · □ background or write-up only

### Key milestones

| Date                        | Milestone                                                                                                                                       |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| 30 Nov 2026                 | Baselines on all 6 languages and fragmentation study done; 30-pair zero-shot transfer matrix ready for the RQ2 pilot; ≥15 papers in reading log |
| 4 Dec 2026                  | Raw-text samples for the 6 languages prepared and the RQ2 encoder training started (WP2 needs this early to finish in the window)               |
| 15 Dec 2026                 | WP1 in-language results frozen (G1, G2); adapter ready for the RQ4 pilot                                                                        |
| 22 Dec 2026                 | WP1 cross-lingual transfer results frozen (G3); the baseline matrix from 30 Nov is already enough for the RQ2 pilot                             |
| 8 Jan 2027                  | All pilot experiments frozen (RQ2, RQ3, RQ4)                                                                                                    |
| Mid Jan 2027 (ARR date TBA) | Paper 1 submitted (ARR January cycle, for ACL 2027)                                                                                             |
| 31 Jan 2027                 | Project report answering RQ1 to RQ4, code and adapters released                                                                                 |

---

## 5. Target venues

| Venue                                                                     | When / where                                                      | Deadline                                                                      | Fit                                                               | Plan                                                                                                |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [ACL 2027](https://2027.aclweb.org/)                                      | 17–22 Aug 2027, Kyoto, Japan                                      | [ARR](https://aclrollingreview.org/dates) January 2027 cycle (exact date TBA) | Top-tier main conference; Multilinguality and Low-resource tracks | **Paper 1 (WP1, RQ1)**                                                                              |
| [AfricaNLP Workshop](https://africanlp.masakhane.io/)                     | 2027 edition **(expected)**; 2026 was at EACL, Rabat, 28 Mar 2026 | Usually ~2–3 months before the host conference                                | Main African NLP venue; Masakhane community                       | Optional early paper from the WP0 fragmentation study, only if the deadline falls inside the window |
| [SIGTYP Workshop](https://sigtyp.github.io/workshop.html)                 | 2027 edition **(expected)**                                       | TBA                                                                           | Computational typology: exact fit for RQ2                         | Future: full RQ2 paper (Section 9)                                                                  |
| EMNLP 2027 (site not live yet; see [EMNLP 2026](https://2026.emnlp.org/)) | Early Nov 2027, Mexico / Central America (tentative)              | ARR ~May 2027 cycle **(expected)**                                            | Top-tier; PEFT                                                    | Future: full RQ3 paper (Section 9)                                                                  |
| [MRL Workshop](https://sigtyp.github.io/ws2026-mrl.html)                  | Usually co-located with EMNLP; 2026 edition 28 Oct 2026, Budapest | TBA for 2027                                                                  | Multilingual representation learning                              | Fallback if Paper 1 is rejected                                                                     |
| [NAACL 2027](https://2027.naacl.org/calls/main_conference_papers/)        | 1–5 Jun 2027, San Francisco                                       | ARR 12 Oct 2026; commit 23 Dec 2026                                           | Low-resource and multilinguality tracks                           | Not usable: results are not ready by 12 Oct                                                         |
| [EACL 2027](https://2027.eacl.org/)                                       | 9–14 Mar 2027, Athens                                             | Passed (ARR 3 Aug 2026)                                                       | n/a                                                               | Watch for its workshops (AfricaNLP/SIGTYP may be co-located)                                        |
| [Deep Learning Indaba](https://deeplearningindaba.com/)                   | 2027 TBA; 2026 was 2–7 Aug, Lagos                                 | Usually applications open early in the year                                   | African ML community, posters, mentorship                         | Outside the window; apply with Paper 1 results                                                      |
| [TACL](https://transacl.org/)                                             | Journal, rolling submissions                                      | Any time                                                                      | Longer consolidated paper                                         | Future: consolidated paper (Section 9)                                                              |

---

## 6. Data sources

### Task datasets (evaluation and fine-tuning)

| Dataset              | Task                                                    | Languages (relevant)                                          | Link                                                                                                                 | Licence               |
| -------------------- | ------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------------------- |
| MasakhaNER 2.0       | Named entity recognition                                | kin, lug, swa, zul, hau (20 languages in total)               | [HF: masakhane/masakhaner2](https://huggingface.co/datasets/masakhane/masakhaner2)                                   | Check dataset card    |
| MasakhaNER 1.0       | Named entity recognition, **Amharic only** (not in 2.0) | amh (1,750 / 250 / 500 train / dev / test)                    | [HF: masakhane/masakhaner](https://huggingface.co/datasets/masakhane/masakhaner)                                     | Check dataset card    |
| MasakhaPOS           | Part-of-speech tagging                                  | kin, lug, swa, zul, hau (20 languages in total; no Amharic)   | [HF: masakhane/masakhapos](https://huggingface.co/datasets/masakhane/masakhapos)                                     | CC BY-NC 4.0 per card |
| UD_Amharic-ATT       | Part-of-speech tagging, **Amharic only**                | amh (1,074 sentences; manual UPOS, clitics segmented)         | [universaldependencies.org](https://universaldependencies.org/treebanks/am_att/index.html)                           | CC BY-SA 4.0          |
| SIB-200              | Topic classification (main topic task for all 6)        | 205 languages incl. all 6                                     | [HF: Davlan/sib200](https://huggingface.co/datasets/Davlan/sib200)                                                   | CC BY-SA 4.0          |
| MasakhaNEWS          | News topic classification (extra)                       | swa, lug, amh, hau (has Kirundi, not Kinyarwanda; no isiZulu) | [HF: masakhane/masakhanews](https://huggingface.co/datasets/masakhane/masakhanews)                                   | CC BY-NC 4.0 per card |
| FLORES-200 / FLORES+ | Machine translation eval (RQ4 pilot)                    | incl. all 6                                                   | [HF: openlanguagedata/flores_plus](https://huggingface.co/datasets/openlanguagedata/flores_plus)                     | CC BY-SA 4.0          |
| AfriSenti            | Sentiment, only if needed                               | swa, amh, hau, possibly kin (check)                           | [HF: shmuhammad/AfriSenti-twitter-sentiment](https://huggingface.co/datasets/shmuhammad/AfriSenti-twitter-sentiment) | Check dataset card    |

Moved to future work: IrokoBench, TyDi QA, other Universal Dependencies treebanks (thin for Bantu). Oromo and Tigrinya have only topic classification in MasakhaNEWS, so they cannot join the NER/POS transfer matrix.

### Morphology and typology resources

| Resource                                                               | Use                                                         | Link                                                                                                                                |
| ---------------------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| NCHLT corpora (SADiLaR)                                                | Gold morphology for isiZulu                                 | [repo.sadilar.org](https://repo.sadilar.org/)                                                                                       |
| KinyaBERT morphological analyser                                       | Kinyarwanda segmentation (check availability and licence)   | [GitHub: anzeyimana/kinyabert-acl2022](https://github.com/anzeyimana/kinyabert-acl2022)                                             |
| UniMorph (Kiswahili, isiZulu, Amharic; Kinyarwanda and Hausa to check) | Morphological paradigms; WP1 evaluation                     | [unimorph.github.io](https://unimorph.github.io/) · [zul](https://github.com/unimorph/zul) · [amh](https://github.com/unimorph/amh) |
| HornMorpho                                                             | Amharic morphological analyser (RQ2 sanity check, optional) | [GitHub: hltdi/HornMorpho](https://github.com/hltdi/HornMorpho)                                                                     |
| Morfessor                                                              | Unsupervised morpheme segmentation (default for swa, lug)   | [GitHub: aalto-speech/morfessor](https://github.com/aalto-speech/morfessor)                                                         |
| URIEL+ / lang2vec                                                      | Static typology vectors (WP2/WP3 baseline)                  | [URIEL+](https://github.com/LeeLanguageLab/URIELPlus) · [lang2vec](https://github.com/antonisa/lang2vec)                            |
| WALS, Grambank                                                         | Typological features                                        | [wals.info](https://wals.info/) · [grambank.clld.org](https://grambank.clld.org/)                                                   |

### Unlabelled text (WP1 segmentation, WP2 typology)

| Corpus     | Notes                                                                                                        | Link                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| WURA       | Cleaned mC4 for 16 African languages, ~29 GB. Confirm that all 6 languages (especially Luganda) are included | [HF: castorini/wura](https://huggingface.co/datasets/castorini/wura)         |
| MADLAD-400 | Fallback for any language missing from WURA                                                                  | [HF: allenai/MADLAD-400](https://huggingface.co/datasets/allenai/MADLAD-400) |
| Glot500-c  | Second fallback                                                                                              | [GitHub: cisnlp/Glot500](https://github.com/cisnlp/Glot500)                  |

### Base models

| Model                       | Size  | Use                                                                                   | Link                                                                                |
| --------------------------- | ----- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| AfroXLMR-large (76L)        | 560M  | Main encoder for WP1–WP3 (confirm all 6 languages are covered)                        | [HF: Davlan/afro-xlmr-large-76L](https://huggingface.co/Davlan/afro-xlmr-large-76L) |
| Serengeti                   | ~500M | Second African encoder baseline                                                       | [HF: UBC-NLP/serengeti](https://huggingface.co/UBC-NLP/serengeti)                   |
| BantuBERTa                  | base  | Bantu-family baseline (confirm language coverage)                                     | [HF: dsfsi/BantuBERTa](https://huggingface.co/dsfsi/BantuBERTa)                     |
| InkubaLM                    | 0.4B  | Small African decoder for the WP4 pilot (check which of the core languages it covers) | [HF: lelapa/InkubaLM-0.4B](https://huggingface.co/lelapa/InkubaLM-0.4B)             |
| A 1–3B multilingual decoder | 1–3B  | Alternative WP4 model if InkubaLM misses kin/lug                                      | Hugging Face (gated; accept licence)                                                |

Moved to future work: Lugha-Llama-8B and Llama 3.x / Gemma 7–9B for the full RQ4 study. Llama 3.x and Gemma tokenizers are still used in the WP0 fragmentation study.

---

## 7. Compute and time

### Strategy

- **Development and debugging:** free GPUs, [Kaggle](https://www.kaggle.com/docs/efficient-gpu-usage) (about 30 GPU-hours/week on P100 16 GB or 2×T4, up to 12 h per session) plus Google Colab. Working on 16 GB cards from the start is itself a test of the low-cost claim (G7).
- **Main runs and pilots:** with 4 months, a compute-grant or HPC application may not be approved in time. Apply in Month 1 anyway ([CHPC](https://www.chpc.ac.za/) or a university cluster), and budget for renting an A100 80 GB as the fallback.
- A P100 is several times slower than an A100, so the Kaggle quota alone will not cover the numbers below. Treat the free tier as covering WP0 and most of WP1 only.

### Estimated GPU hours (A100-80GB equivalent, planning figures)

| WP                | What runs                                                                                                                                                                                               | Rough count | Hours per run | Total GPU-h         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ------------- | ------------------- |
| WP0               | Baselines: 3 PEFT methods × 6 langs × 3 tasks × 3 seeds (AfroXLMR-large); the 30-pair zero-shot matrix is evaluation only                                                                               | ~160        | 0.3           | ~50                 |
| WP1 in-language   | ~10 adapter configs (segmentation source, placement) × 4 core langs × 2 tasks × 3 seeds                                                                                                                 | ~240        | 0.3           | ~70                 |
| WP1 transfer (G3) | 3 configs × 12 source → target pairs × 2 sizes (100, 1k) × 2 tasks × 3 seeds; zero-shot is evaluation only                                                                                              | ~430        | ~0.06         | ~25                 |
| WP2 pilot         | Typology encoder training (6 languages), script control (romanised Amharic), simple-statistics baseline, plus the plug-in check (latent-vector gate at 100 and 1k, ~50 runs). The matrix comes from WP0 | ~130        | 0.3–1         | ~60                 |
| WP3 pilot         | 5 methods (incl. layer-wise rank allocation) × 4 held-out languages × 3 data sizes (100, 1k, plus full for reference) × 2 tasks × 3 seeds                                                               | ~360        | 0.4           | ~145                |
| WP4 pilot         | QLoRA on one small decoder: ~12 fine-tuning runs + evaluation                                                                                                                                           | ~12 + eval  | 1.5–3         | ~40                 |
| Buffer            | Failed runs, reruns (+30%)                                                                                                                                                                              |             |               | ~115                |
| **Total**         |                                                                                                                                                                                                         |             |               | **~500 A100-hours** |

- **Cloud cost if everything were rented:** about USD 750–1,250 at USD 1.5–2.5/h for an A100 80 GB. Check current prices. Adding Amharic and Hausa only to the baselines and RQ2 adds about 50 hours over a 4-language plan; adding them to every work package would have cost about 240 more.
- **Storage:** ~120 GB (WURA subset for the 6 languages, base-model weights ~10 GB, checkpoints/adapters). Adapters are small (MBs), so keep only final adapters and delete intermediate checkpoints.
- **Minimum local machine:** 16 GB RAM laptop for writing and analysis. Training happens remotely.

### Effort estimate (one full-time researcher)

| Phase          | Weeks                                | Main effort                                                        |
| -------------- | ------------------------------------ | ------------------------------------------------------------------ |
| WP0            | 8                                    | Reading (~30%), engineering setup and baselines (~70%)             |
| WP1            | 8 (overlaps WP0 from November)       | Method design, experiments, Paper 1 writing (last 2–3 weeks)       |
| WP2–WP4 pilots | 6 in parallel (late Nov – early Jan) | Three small experiments sharing one codebase and the WP0 baselines |
| WP5            | 3                                    | Paper 1, report, release                                           |

The schedule is tight: the three pilots overlap with the WP1 write-up. If time runs short, cut in this order: the RQ4 pilot first, then the layer-wise rank allocation test, then the rest of the RQ3 pilot. Keep RQ2 because it reuses the WP0 baselines and shares the RQ3 gate. If WP2 itself must shrink, drop check (c), the plug-in test, before (a) or (b). The G3 cross-lingual transfer test in WP1 is not cut: it is part of RQ1 and the title.

---

## 8. Risks and mitigations

| Risk                                                                                                                     | Likelihood | Impact | Mitigation                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------ | ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nakashole (2025) MoI-MoE overlaps with WP3, and the core languages are the same family                                   | High       | High   | State the difference explicitly: PEFT/LoRA experts rather than full MoE, data-driven latent typology rather than a hand-designed index. Include MoI-MoE as a baseline only if code is available; otherwise compare conceptually |
| KinyaBERT (2022) already preserves morphology for Kinyarwanda, which challenges the novelty of RQ1                       | Medium     | High   | Position WP1 as a drop-in adapter on an existing multilingual model that keeps its vocabulary and works across 4 languages, versus a model trained from scratch for one language. Read the paper in Week 1                      |
| RQ2 pilot has only 6 languages and 2 families (30 transfer pairs), so it cannot show general typology discovery          | High       | Medium | Report it as a pilot on a clear contrast; claim only "works or does not work here". Future work adds more languages and Grambank probing (Section 9)                                                                            |
| Amharic differs in script, corpus size and domain as well as morphology, so the vectors may only detect script           | High       | High   | Script control with romanised Amharic; simple-statistics baseline; report NER-only and POS-only matrices; if the vectors collapse to script, report that as the RQ2 result                                                      |
| Amharic data is thin and mixed (NER from MasakhaNER 1.0, ~1k-sentence POS treebank), so its rows in the matrix are noisy | Medium     | Medium | Footnote the sources; give Amharic POS less weight; add Hausa (clean NER, POS, news) as the second contrast language                                                                                                            |
| Pilots do not fit in 6 weeks alongside Paper 1                                                                           | High       | High   | Fixed cut order (RQ4 pilot, then rank allocation, then rest of RQ3); all pilots share the WP0 baselines and data loaders; freeze experiments on 8 Jan                                                                           |
| Gold morphology missing for most languages                                                                               | High       | Medium | Use unsupervised Morfessor as the default; gold segmentation (NCHLT, maybe the KinyaBERT analyser) only for evaluation and one ablation                                                                                         |
| Dataset gaps: no MasakhaNEWS for kin/zul; some coverage entries unchecked                                                | Medium     | Low    | Use SIB-200 for topic classification; finish the benchmark table by checking every `?` cell in Week 1                                                                                                                           |
| Not enough compute in 4 months                                                                                           | Medium     | High   | Smallest model that works, 3 seeds, apply for HPC in Month 1, budget a rented A100 as fallback                                                                                                                                  |
| ARR January date arrives before results are final                                                                        | Medium     | High   | Freeze WP1 results on 15 Dec; write the paper from the WP0 fragmentation study and WP1 results only. Fallback: next ARR cycle or MRL workshop                                                                                   |
| Improvements are small or not significant                                                                                | Medium     | High   | 3 seeds, significance tests, report negative results; the fragmentation study alone is publishable                                                                                                                              |
| Dataset licences (non-commercial)                                                                                        | Low        | Low    | Research use only; record licences in `data/README.md`                                                                                                                                                                          |

---

## 9. Future work (does not fit in Oct 2026 – Jan 2027)

| Item           | Extends | What the full study adds                                                                                                                                                                                |
| -------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full WP2       | RQ2     | More languages (Oromo, Tigrinya, Dholuo, Xhosa), probing against Grambank features, within-language variation (dialect, domain, code-switching in Kiswahili–English), workshop paper (SIGTYP/AfricaNLP) |
| Full WP3       | RQ3     | 10k setting, full study of morphology-driven rank allocation (several allocation signals), AdaLoRA and MoI-MoE baselines, more tasks (AfriXNLI), Paper 3 (EMNLP 2027)                                   |
| Full WP4       | RQ4     | 7–8B models (Lugha-Llama-8B, Llama 3.x), IrokoBench, AfriQA / TyDi QA, A100 sweeps                                                                                                                      |
| More languages | All     | Contrast languages (Amharic, Hausa) in every work package, not only RQ2; Xhosa, Oromo, Tigrinya, Dholuo; low-data languages (Kanuri, Maasai, Nama) where data exists                                    |
| Consolidation  | All     | TACL or ACL/EACL 2028 paper, thesis chapters, Indaba poster                                                                                                                                             |

---

## 10. Next actions (this month)

- [ ] Write notes for KinyaBERT (already in the reading log) and Nakashole (2025) first
- [ ] Write the "how we differ" paragraph for Nakashole (2025) and KinyaBERT in `literature review/gaps-and-ideas.md`
- [ ] Check every `?` cell in the benchmark table (Section 2) against the dataset cards, including SIB-200 and WURA coverage for Amharic and Hausa
- [ ] Load MasakhaNER 1.0 (Amharic) and UD_Amharic-ATT with the same label scheme as the other NER and POS sets, and write down the differences in `data/README.md`
- [ ] Check KinyaBERT analyser availability and licence; check InkubaLM and BantuBERTa language coverage
- [ ] Look up the exact ARR January 2027 deadline and put it in Section 4
- [ ] Create Kaggle and Hugging Face accounts; accept licences for gated models
- [ ] Apply for HPC / cloud compute
- [ ] Download MasakhaNER 2.0, MasakhaPOS and SIB-200 and run the first LoRA baseline on Kiswahili
