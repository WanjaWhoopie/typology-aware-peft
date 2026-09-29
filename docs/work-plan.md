# Work Plan: Typology-Aware PEFT for Morphologically Rich, Low-Resource Languages

| | |
|---|---|
| **Period** | October 2026 – March 2028 (18 months) |
| **Last updated** | 2026-09-29 |
| **Status** | Month 0: setup and literature review |

> Venue dates marked **(expected)** have not been announced yet and are based on earlier editions. Check the linked pages before planning around them. Links and dates were last checked on 2026-09-29.

---

## 1. Goals

### Overall aim
Build PEFT modules that use a language's structure (agglutination, prefixing, root-and-pattern morphology) to adapt multilingual models to African MRLs. They should train **under 2% of the base model's parameters** and have **final configurations that train on one 16–24 GB GPU**.

### Measurable targets

| # | Goal | Target (hypothesis to test) | Linked RQ |
|---|---|---|---|
| G1 | Less subword fragmentation | ≥15% lower fertility (tokens per word) and higher morpheme-boundary F1 than the base tokenizer on Tier 1 languages, **without changing the vocabulary** | RQ1 |
| G2 | Better word-level tasks | +2 F1 on MasakhaNER 2.0 / MasakhaPOS over standard LoRA with the same parameter budget | RQ1 |
| G3 | Data-driven typology | Latent typology vectors predict cross-lingual transfer (Spearman ρ) at least as well as URIEL/WALS vectors | RQ2 |
| G4 | Better low-data transfer | Typology-gated Mixture-of-LoRA beats single LoRA and MAD-X-style stacking in the 100 / 1k / 10k example settings | RQ3 |
| G5 | Scales to generative LLMs | Gains from G2 and G4 still hold on a 7–8B decoder model trained with QLoRA, on IrokoBench and FLORES | RQ4 |
| G6 | Low-cost claim is real | Final methods train on a single 16 GB GPU (Kaggle/Colab T4 or P100). Peak memory and time are reported for every run | All |
| G7 | Open science | Release code, trained adapters (Hugging Face), latent typology vectors and evaluation scripts | All |

### Main outputs
1. **Paper 1 (WP1):** morpheme-preserving embeddings/adapters. Target ACL 2027.
2. **Paper 2 (WP2):** dynamic latent typology. Target SIGTYP 2027 or AfricaNLP 2027 workshop.
3. **Paper 3 (WP3):** typology-guided Mixture-of-Adapters. Target EMNLP 2027.
4. **Paper 4 (WP4 + consolidation):** scaling to generative LLMs. Target TACL or ACL/EACL 2028.
5. Thesis chapters, open-source release, IndabaX / Deep Learning Indaba poster.

---

## 2. Languages (tiered by data available)

The proposal lists 14 languages. Several (Nama, Maasai, Kanuri) have almost no labelled benchmarks. Grouping languages into tiers keeps the scope realistic without dropping the typological spread.

| Tier | Role | Languages | Why |
|---|---|---|---|
| **Tier 1: core** | Training and evaluation in every WP | Kiswahili, isiZulu, isiXhosa, Luganda (Bantu); Amharic, Hausa (Afroasiatic) | Covered by several Masakhane benchmarks and pretraining corpora. Includes both concatenative (Bantu) and non-concatenative (Amharic) morphology |
| **Tier 2: transfer** | Evaluation and low-data transfer | Oromo, Tigrinya (Afroasiatic); Dholuo (Nilotic) | Present in SIB-200 / FLORES plus one or two task datasets |
| **Tier 3: stress test** | Zero-shot only, where data exists | Central Kanuri, Maasai, Nama (Khoekhoe) | Very little data. Kanuri is in FLORES-200/SIB-200. Maasai and Nama depend on finding data (see Risks) |

### Benchmark coverage (Tier 1–2)

Based on the dataset papers. Confirm language codes and splits on each dataset card when downloading.

| Language | MasakhaNER 2.0 | MasakhaPOS | MasakhaNEWS | AfriSenti | IrokoBench | SIB-200 / FLORES | UniMorph |
|---|---|---|---|---|---|---|---|
| Swahili | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| isiZulu | ✓ | ✓ | | | ✓ | ✓ | ✓ |
| isiXhosa | ✓ | ✓ | ✓ | | ✓ | ✓ | |
| Luganda | ✓ | ✓ | ✓ | | ✓ | ✓ | |
| Amharic | (v1.0) | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Hausa | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Oromo | | | ✓ | ✓ | ✓ | ✓ | |
| Tigrinya | | | ✓ | ✓ | | ✓ | |
| Dholuo | ✓ | ✓ | | | | ✓ | |

---

## 3. Work packages and tasks

### WP0: Setup and literature review (Oct – Nov 2026)
- [ ] Read and take notes on 30–40 core papers (see `literature review/reading-log.md`), with priority on:
  - [Typology-Guided Adaptation in Multilingual Models (Nakashole, ACL 2025)](https://aclanthology.org/2025.acl-long.1059/). **This is the closest prior work:** MoI-MoE routes on morphology over 10 Bantu languages. WP3 must be clearly different from it and compared against it.
  - [IFCLoRA: Topology-Aware Rank Allocation for PEFT (arXiv 2607.22251)](https://arxiv.org/abs/2607.22251): the "topology-aware" baseline cited in the proposal.
  - [LoRA (Hu et al., 2021)](https://arxiv.org/abs/2106.09685), [QLoRA (Dettmers et al., 2023)](https://arxiv.org/abs/2305.14314), [AdaLoRA (Zhang et al., 2023)](https://arxiv.org/abs/2303.10512), [MAD-X (Pfeiffer et al., 2020)](https://arxiv.org/abs/2005.00052)
  - [URIEL+ (Khan et al., COLING 2025)](https://aclanthology.org/2025.coling-main.463.pdf), [IrokoBench (Adelani et al., 2024)](https://arxiv.org/abs/2406.03368)
- [ ] Set up the environment: PyTorch, Hugging Face `transformers`, [`peft`](https://github.com/huggingface/peft), [`adapters`](https://github.com/adapter-hub/adapters), `bitsandbytes`, [`lm-evaluation-harness`](https://github.com/EleutherAI/lm-evaluation-harness)
- [ ] Set up experiment tracking (Weights & Biases or MLflow) and a shared results table
- [ ] Write data loaders for every dataset in Section 5 and record them in `data/README.md`
- [ ] **Baselines:** standard LoRA, AdaLoRA and MAD-X adapters on AfroXLMR-large for NER, POS and news classification (Tier 1). This is the reference table every WP compares against
- [ ] **Tokenizer fragmentation study:** fertility, continued-word ratio and morpheme-boundary F1 for XLM-R, AfroXLMR, Llama 3.x, Gemma and InkubaLM tokenizers. This also gives early material for a workshop paper

**Deliverables:** reading log with ≥30 notes, baseline results table, fragmentation analysis.

### WP1: Morpheme-preserving embeddings (RQ1) (Nov 2026 – Jan 2027)
- [ ] Build gold or silver morpheme segmentations:
  - Zulu/Xhosa: NCHLT annotated corpora ([SADiLaR](https://repo.sadilar.org/))
  - Amharic: [HornMorpho](https://github.com/hltdi/HornMorpho) / [UniMorph amh](https://github.com/unimorph/amh)
  - Swahili and others: unsupervised [Morfessor](https://github.com/aalto-speech/morfessor)
- [ ] Design soft-token / embedding adapters that add morphological priors (root, prefix and affix embeddings pooled into subword embeddings)
- [ ] Ablations: segmentation source (gold, Morfessor, none); adapter placement (embedding layer only, or embedding plus lower layers)
- [ ] Evaluate intrinsically (fertility, boundary F1) and on tasks (MasakhaNER 2.0, MasakhaPOS) at matched parameter budgets, 3 seeds
- [ ] Measure peak GPU memory and throughput for every setting (goal G6)
- [ ] **Write and submit Paper 1 to ARR (January 2027 cycle, for ACL 2027)**

### WP2: Dynamic latent typology (RQ2) (Feb – Apr 2027)
- [ ] Train an unsupervised encoder on raw text (WURA, MADLAD-400) that outputs a continuous typology vector per language (and optionally per domain/dialect). Candidate signals: morpheme statistics from WP1, subword co-occurrence, and adapter weight similarity
- [ ] Compare with [URIEL+/lang2vec](https://github.com/LeeLanguageLab/URIELPlus) and [WALS](https://wals.info/) / [Grambank](https://grambank.clld.org/):
  - (a) can the latent vectors recover known typological features (probing)?
  - (b) do they predict transfer success (ρ between vector distance and zero-shot transfer scores from the WP0 baselines)?
- [ ] Test robustness on code-switched text (Swahili–English, e.g. AfriSenti tweets)
- [ ] **Submit Paper 2 to SIGTYP 2027 or AfricaNLP 2027 (workshop)**

### WP3: Typology-guided Mixture-of-Adapters (RQ3) (Mar – Jun 2027)
- [ ] Build Mixture-of-LoRA with a gate conditioned on typology vectors. **Start with static URIEL vectors so WP3 isn't blocked on WP2**, then switch to WP2's latent vectors
- [ ] Try typology-driven rank allocation per layer (building on the IFCLoRA/AdaLoRA idea of uneven rank, but with the signal coming from morphology)
- [ ] Low-data settings: 100 / 1k / 10k training examples per target language; zero-shot to Tier 2–3
- [ ] Baselines: LoRA, AdaLoRA, MAD-X stacking, IFCLoRA (if code is released), MoI-MoE (Nakashole 2025)
- [ ] Tasks: NER, POS, MasakhaNEWS, SIB-200, AfriXNLI
- [ ] **Submit Paper 3 to ARR (expected May 2027 cycle, for EMNLP 2027)**

### WP4: Generative LLMs (RQ4) (Jul – Oct 2027)
- [ ] Port WP1 and WP3 to decoder-only models with QLoRA (4-bit): a small model for development (InkubaLM-0.4B or a 1–3B model), then a 7–8B model (Llama 3.x 8B or Lugha-Llama-8B)
- [ ] Evaluate on IrokoBench (AfriXNLI, AfriMMLU, AfriMGSM) using `lm-evaluation-harness`, FLORES translation (chrF++), and AfriQA / TyDi QA (Swahili)
- [ ] Confirm the final configurations train on a single 16 GB GPU (goal G6)

### WP5: Consolidation and dissemination (Nov 2027 – Mar 2028)
- [ ] Journal paper (TACL) combining WP1–WP4, or ACL/EACL 2028 submission
- [ ] Release: code on GitHub, adapters and typology vectors on Hugging Face, and a model card for each adapter
- [ ] Thesis chapters and final report
- [ ] Present at IndabaX / Deep Learning Indaba 2027 and share with the Masakhane community

---

## 4. Timeline

| Month | Oct 26 | Nov | Dec | Jan 27 | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Jan 28 | Feb | Mar |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WP0 Setup + lit review | ■ | ■ | | | | | | | | | | | | | | | | |
| WP1 Morpheme embeddings | | ■ | ■ | ■ | | | | | | | | | | | | | | |
| WP2 Latent typology | | | | | ■ | ■ | ■ | | | | | | | | | | | |
| WP3 Mixture-of-Adapters | | | | | | ■ | ■ | ■ | ■ | | | | | | | | | |
| WP4 Generative LLMs | | | | | | | | | | ■ | ■ | ■ | ■ | | | | | |
| WP5 Consolidation | | | | | | | | | | | | | | ■ | ■ | ■ | ■ | ■ |
| Literature review (ongoing) | ■ | ■ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ | □ |

■ main focus · □ ongoing in the background

### Key milestones

| Date | Milestone |
|---|---|
| 30 Nov 2026 | Baselines and fragmentation study done; ≥30 papers in reading log |
| Jan 2027 | Paper 1 submitted (ARR January cycle → ACL 2027) |
| Apr 2027 | Paper 2 submitted (SIGTYP / AfricaNLP 2027) |
| May 2027 | Paper 3 submitted (ARR → EMNLP 2027) |
| Oct 2027 | WP4 results; all systems run on a 16 GB GPU |
| Mar 2028 | Journal submission, open-source release, thesis chapters |

---

## 5. Target venues

| Venue | When / where | Deadline | Fit | Plan |
|---|---|---|---|---|
| [ACL 2027](https://2027.aclweb.org/) | 17–22 Aug 2027, Kyoto, Japan | [ARR](https://aclrollingreview.org/dates) January 2027 cycle (exact date TBA) | Top-tier main conference; Multilinguality and Low-resource tracks | **Paper 1 (WP1)** |
| EMNLP 2027 (site not live yet; see [EMNLP 2026](https://2026.emnlp.org/)) | Early Nov 2027, Mexico / Central America (tentative) | ARR ~May 2027 cycle **(expected)** | Top-tier; empirical methods, PEFT | **Paper 3 (WP3)** |
| [AfricaNLP Workshop](https://africanlp.masakhane.io/) | 2027 edition **(expected)**; 2026 was at EACL, Rabat, 28 Mar 2026 | Usually ~2–3 months before the host conference | Main African NLP venue; Masakhane community | **Early paper** (fragmentation study) or Paper 2 |
| [SIGTYP Workshop](https://sigtyp.github.io/workshop.html) | 2027 edition **(expected)**; 2026 was at EACL, Rabat | TBA | Computational typology + multilingual NLP: exact fit for RQ2 | **Paper 2 (WP2)** |
| [MRL Workshop](https://sigtyp.github.io/ws2026-mrl.html) | Usually co-located with EMNLP; 2026 edition 28 Oct 2026, Budapest | TBA for 2027 | Multilingual representation learning; understudied language families | Fallback for Papers 2 or 3 |
| [NAACL 2027](https://2027.naacl.org/calls/main_conference_papers/) | 1–5 Jun 2027, San Francisco | ARR 12 Oct 2026; commit 23 Dec 2026 | Low-resource and multilinguality tracks | Too early for main results; skip unless WP0 gives a strong finding |
| [EACL 2027](https://2027.eacl.org/) | 9–14 Mar 2027, Athens | Passed (ARR 3 Aug 2026) | — | Watch for its workshops (AfricaNLP/SIGTYP may be co-located) |
| [Deep Learning Indaba](https://deeplearningindaba.com/) | 2027 TBA; 2026 was 2–7 Aug, Lagos | Usually applications open early in the year | African ML community, posters, mentorship | Poster + networking |
| [TACL](https://transacl.org/) | Journal, rolling submissions | Any time | Longer consolidated paper | **Paper 4 (WP4 + consolidation)** |

---

## 6. Data sources

### Task datasets (evaluation and fine-tuning)

| Dataset | Task | Languages (relevant) | Link | Licence |
|---|---|---|---|---|
| MasakhaNER 2.0 | Named entity recognition | 20 African languages incl. swa, zul, xho, lug, hau, luo | [HF: masakhane/masakhaner2](https://huggingface.co/datasets/masakhane/masakhaner2) | Check dataset card |
| MasakhaNER 1.0 | NER | incl. Amharic | [HF: masakhane/masakhaner](https://huggingface.co/datasets/masakhane/masakhaner) | Check dataset card |
| MasakhaPOS | Part-of-speech tagging | 20 typologically diverse African languages | [HF: masakhane/masakhapos](https://huggingface.co/datasets/masakhane/masakhapos) | Check dataset card |
| MasakhaNEWS | News topic classification | 16 languages incl. amh, hau, swa, xho, lug, orm, tir | [HF: masakhane/masakhanews](https://huggingface.co/datasets/masakhane/masakhanews) | Non-commercial (check card) |
| AfriSenti | Sentiment (tweets, code-switching) | 14 languages incl. amh, hau, swa, orm, tir | [HF: shmuhammad/AfriSenti-twitter-sentiment](https://huggingface.co/datasets/shmuhammad/AfriSenti-twitter-sentiment) | Check dataset card |
| SIB-200 | Topic classification | 205 languages (all Tier 1–2 + Kanuri) | [HF: Davlan/sib200](https://huggingface.co/datasets/Davlan/sib200) | CC BY-SA 4.0 |
| IrokoBench (AfriXNLI, AfriMMLU, AfriMGSM) | NLI, knowledge QA, maths reasoning | 16 African languages | [HF: Masakhane IrokoBench collection](https://huggingface.co/collections/masakhane/irokobench-665a21b6d4714ed3f81af3b1) | CC BY-SA 4.0 |
| FLORES-200 / FLORES+ | Machine translation eval | 200+ languages | [HF: openlanguagedata/flores_plus](https://huggingface.co/datasets/openlanguagedata/flores_plus) | CC BY-SA 4.0 |
| TyDi QA | Question answering | incl. Swahili | [GitHub: google-research-datasets/tydiqa](https://github.com/google-research-datasets/tydiqa) | Apache 2.0 |
| Universal Dependencies | Dependency parsing, morphology features | Check coverage: thin for Bantu | [universaldependencies.org](https://universaldependencies.org/) | Per treebank |

### Morphology and typology resources

| Resource | Use | Link |
|---|---|---|
| UniMorph (Amharic, Zulu, Swahili…) | Morphological paradigms; WP1 priors and evaluation | [unimorph.github.io](https://unimorph.github.io/) · [amh](https://github.com/unimorph/amh) · [zul](https://github.com/unimorph/zul) |
| NCHLT corpora (SADiLaR) | Annotated morphology for South African languages (Zulu, Xhosa) | [repo.sadilar.org](https://repo.sadilar.org/) |
| HornMorpho | Amharic/Tigrinya morphological analyser | [GitHub: hltdi/HornMorpho](https://github.com/hltdi/HornMorpho) |
| Morfessor | Unsupervised morpheme segmentation | [GitHub: aalto-speech/morfessor](https://github.com/aalto-speech/morfessor) |
| URIEL+ / lang2vec | Static typology vectors (WP2/WP3 baseline) | [URIEL+](https://github.com/LeeLanguageLab/URIELPlus) · [lang2vec](https://github.com/antonisa/lang2vec) |
| WALS | Typological features | [wals.info](https://wals.info/) |
| Grambank | Grammatical features, 2,400+ languages | [grambank.clld.org](https://grambank.clld.org/) |

### Unlabelled text (WP1 segmentation, WP2 typology)

| Corpus | Notes | Link |
|---|---|---|
| WURA | Cleaned mC4 for 16 African languages, ~29 GB, document level | [HF: castorini/wura](https://huggingface.co/datasets/castorini/wura) |
| MADLAD-400 | Web text in 400+ languages; covers Tier 3 better | [HF: allenai/MADLAD-400](https://huggingface.co/datasets/allenai/MADLAD-400) |
| Glot500-c | Corpus for 500+ languages | [GitHub: cisnlp/Glot500](https://github.com/cisnlp/Glot500) |

### Base models

| Model | Size | Use | Link |
|---|---|---|---|
| AfroXLMR-large (76L) | 560M | Main encoder for WP1–WP3 | [HF: Davlan/afro-xlmr-large-76L](https://huggingface.co/Davlan/afro-xlmr-large-76L) |
| Serengeti | ~500M | Second African encoder baseline | [HF: UBC-NLP/serengeti](https://huggingface.co/UBC-NLP/serengeti) |
| BantuBERTa | base | Bantu-family baseline (from our reading list) | [HF: dsfsi/BantuBERTa](https://huggingface.co/dsfsi/BantuBERTa) |
| InkubaLM | 0.4B | Small African decoder, cheap WP4 development | [HF: lelapa/InkubaLM-0.4B](https://huggingface.co/lelapa/InkubaLM-0.4B) |
| Lugha-Llama-8B | 8B | African-adapted Llama for WP4 | [HF: Lugha-Llama/Lugha-Llama-8B-wura](https://huggingface.co/Lugha-Llama/Lugha-Llama-8B-wura) |
| Llama 3.x 8B / Gemma (current release) | 7–9B | General multilingual decoder for WP4 | Hugging Face (gated; accept licence) |

---

## 7. Compute and time

### Strategy
- **Development and debugging:** free GPUs, [Kaggle](https://www.kaggle.com/docs/efficient-gpu-usage) (about 30 GPU-hours/week on P100 16 GB or 2×T4, up to 12 h per session) plus Google Colab. Working on 16 GB cards from the start is itself a test of the low-cost claim (G6).
- **Final sweeps (multiple seeds, 7–8B models):** a university HPC cluster, [CHPC (South Africa)](https://www.chpc.ac.za/) research allocation, or rented A100 80 GB. Apply for compute grants in Month 1.
- This keeps both statements in the proposal true: final methods **train on one consumer GPU**, while the full research sweep needs **1–4 A100s**.

### Estimated GPU hours (A100-80GB equivalent)

| WP | What runs | Rough count | Hours per run | Total GPU-h |
|---|---|---|---|---|
| WP0 | Baselines: 3 PEFT methods × 6 langs × 3 tasks × 3 seeds (AfroXLMR-large) | ~160 | 0.3 | ~50 |
| WP1 | Morpheme adapters + ablations × 6 langs × 2 tasks × 3 seeds | ~600 | 0.3 | ~180 |
| WP2 | Typology encoder training + probing + transfer matrix | ~50 | 1–2 | ~80 |
| WP3 | MoLoRA variants × low-data settings × 9 langs × 3 seeds (+ baselines) | ~700 | 0.4 | ~280 |
| WP4 | QLoRA on 7–8B: ~40 fine-tuning runs + evaluation on IrokoBench/FLORES | ~40 + eval | 6–10 | ~450 |
| Buffer | Failed runs, reruns for reviewers (+30%) | | | ~310 |
| **Total** | | | | **~1,350 A100-hours** |

- **Cloud cost if everything were rented:** about USD 2,000–3,500 at typical 2026 on-demand A100 80 GB prices (~USD 1.5–2.5/h). Check current prices. Free tiers and HPC allocations can cover most of WP0–WP3.
- **Storage:** ~250 GB (WURA ~29 GB, MADLAD subsets, base-model weights ~40 GB, checkpoints/adapters ~100 GB). Adapters are small (MBs), so keep only final adapters and delete intermediate checkpoints.
- **Minimum local machine:** 16 GB RAM laptop for writing and analysis. Training happens remotely.

### Effort estimate (one full-time researcher)

| Phase | Months | Main effort |
|---|---|---|
| WP0 | 2 | Reading (~40%), engineering setup and baselines (~60%) |
| WP1 | 3 | Method design, experiments, Paper 1 writing (last 3–4 weeks) |
| WP2 | 3 | Method + analysis, workshop paper |
| WP3 | 4 (overlaps WP2) | Largest engineering effort, Paper 3 |
| WP4 | 4 | Scaling, evaluation harness, most compute |
| WP5 | 5 | Writing, release, thesis |

About 25% of the total time should go to writing. Start each paper's related-work section from `literature review/gaps-and-ideas.md`.

---

## 8. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Nakashole (2025) MoI-MoE overlaps with WP3 | High | High | Make the difference explicit: PEFT/LoRA experts rather than full MoE, data-driven latent typology rather than a hand-designed index, more language families (Afroasiatic, Nilotic). Include MoI-MoE as a baseline |
| Too little data for Tier 3 (Nama, Maasai) | High | Medium | Keep Tier 3 zero-shot only; search SADiLaR, Masakhane and MADLAD for text; report coverage honestly as a limitation |
| Gold morphology missing for most languages | Medium | Medium | Use unsupervised Morfessor segmentation as the default; use gold data (NCHLT, UniMorph) only for evaluation |
| Not enough compute for WP4 | Medium | High | QLoRA 4-bit, 1–3B development models, apply for HPC/credits in Month 1, cut WP4 down to 1 model if needed |
| ARR reviewing capacity caps / rejection | Medium | Medium | Workshop fallback for every paper (AfricaNLP, SIGTYP, MRL); resubmit to the next ARR cycle |
| Improvements are small or not significant | Medium | High | 3+ seeds, significance tests, report negative results; the fragmentation study and typology probing are publishable on their own |
| Dataset licences (non-commercial) | Low | Low | Research use only; record licences in `data/README.md` |

---

## 9. Next actions (this month)

- [ ] Finish notes for the 3 papers already in the reading log
- [ ] Read Nakashole (2025) and IFCLoRA first, then write the "how we differ" paragraph in `literature review/gaps-and-ideas.md`
- [ ] Create Kaggle and Hugging Face accounts; accept licences for gated models
- [ ] Apply for HPC / cloud compute
- [ ] Download MasakhaNER 2.0, MasakhaPOS, MasakhaNEWS, SIB-200 and run the first LoRA baseline on Swahili
