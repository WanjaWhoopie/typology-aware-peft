# BantuBERTa: Using Language Family Grouping in Multilingual Language Modeling for Bantu Languages

## Reference

| Field | Details |
|---|---|
| **Title** | BantuBERTa: Using Language Family Grouping in Multilingual Language Modeling for Bantu Languages |
| **Authors** | Jesse Parvess (supervisors: Vukosi Marivate, Verrah Akinyi) |
| **Year** | 2023 |
| **Venue** | MSc mini-dissertation (Big Data Science), University of Pretoria |
| **DOI / URL** | https://repository.up.ac.za/handle/2263/92766 |
| **PDF (online)** | [UPSpace repository (open access PDF)](https://repository.up.ac.za/bitstream/handle/2263/92766/BantuBERTa__Using_Language_Family_Grouping_in_Multilingual_Language_Modeling_for_Bantu_Languages.pdf?isAllowed=y&sequence=1) |
| **Code / data** | [dsfsi/BantuBERTa on Hugging Face](https://huggingface.co/dsfsi/BantuBERTa) |

**Citation (APA):**
> Parvess, J. (2023). *BantuBERTa: Using language family grouping in multilingual language modeling for Bantu languages* [Master's mini-dissertation, University of Pretoria]. https://repository.up.ac.za/handle/2263/92766

<details>
<summary>BibTeX</summary>

```bibtex
@mastersthesis{parvess2023bantuberta,
  title  = {BantuBERTa: Using Language Family Grouping in Multilingual Language Modeling for Bantu Languages},
  author = {Parvess, Jesse},
  school = {University of Pretoria},
  year   = {2023},
  url    = {https://repository.up.ac.za/handle/2263/92766}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | Claude (AI-drafted from the full text; to be checked by the team) |
| **Date read** | 2026-09-29 |
| **Status** | Read |
| **Relevance to our work** | Medium |
| **Tags** | #bantu #language-family #pretraining #typology #tokenization #BPE #swahili #zulu #xhosa #luganda #kinyarwanda #NER #topic-classification #low-resource #data-quality |

## Summary

The dissertation asks whether a multilingual model pretrained only on Bantu languages transfers better to Bantu languages than models pretrained on many unrelated languages. The author collected ~3.8M sentences of "Bantu" text from 11 freely available datasets (mostly from Hugging Face; over 80% from mC4 and CC100). He pretrained a 125M-parameter XLM-RoBERTa-style model from scratch after a small hyperparameter search. On MasakhaNER (Swahili, Kinyarwanda, Luganda), BantuBERTa **underperforms** XLM-R, mBERT and AfriBERTa. On African News Topic Classification (Zulu, Lingala), it scores **about the same as or slightly above** MAFT-adapted XLM-R and AfriBERTa. The author concludes that grouping by language family helps simple tasks like classification, while harder tasks like NER also need more and cleaner pretraining data.

## Research question / problem

Big multilingual models (mBERT, XLM-R) are dominated by high-resource, mostly analytic languages. Swahili is the only Bantu language in either, at 0.04% and 0.07% of pretraining data. Because of the "curse of multilinguality" and negative interference between languages, structurally different low-resource languages get a poor share of model capacity. The two research questions:
1. Can a small multilingual Bantu pretraining corpus be built from freely available online data?
2. Does pretraining only on this Bantu corpus improve transfer to Bantu languages on downstream tasks?

## Method

- **Approach:** Collect and clean Bantu text, then pretrain an XLM-RoBERTa architecture from random initialisation with the MLM objective only (RoBERTa recipe, no next-sentence prediction). A 16-run hyperparameter search (2 epochs each) varied:
  - data cleanliness: fastText language-ID threshold (0.6 vs 0.4) and minimum string length (30 vs 90 characters)
  - BPE vocabulary: 70k vs 100k
  - attention heads: 6 vs 8
  - layers: 8 vs 10

  Each run was scored by fine-tuning on MasakhaNER validation sets. A linear regression of average F1 on the hyperparameters picked the final settings.
- **Model(s) / architecture:** Final BantuBERTa has 10 layers, 6 attention heads and a 70k BPE vocabulary (125M parameters). It was pretrained for 8 epochs with learning rate 1e-4, 40k warm-up steps, batch size 8, 15% masking and max position 514.
- **PEFT method (if any):** None. Full pretraining from scratch plus full fine-tuning.
- **Languages covered:** 15 in pretraining. The biggest shares (dirty set) are Swahili 45%, Zulu 12%, Xhosa 11%, Tswana 7%, Shona 6%, Oromo 5% and Luganda 5%. Kinyarwanda is 1.2%. Evaluation used Swahili, Kinyarwanda and Luganda (NER) and Zulu and Lingala (classification).
- **Datasets:**
  - Pretraining sources: CC100, mC4, NCHLT, OPUS-100, Openslr, XL-Sum, WiLI, KINNEWS/KIRNEWS, SABC News, English–Luganda parallel corpus, Swahili News
  - Evaluation: MasakhaNER 1.0 and ANTC (Alabi et al., 2022). The author excluded Kinyarwanda and Swahili news classification because that text was in the pretraining data (good leakage check).
- **Tasks:** Named entity recognition (a "high-level" task) and news topic classification (a "low-level" task).
- **Evaluation metrics:** F1. Hyperparameter effects were measured with regression p-values and adjusted R².
- **Compute / hardware:** Hardware isn't reported. The author mentions "resource constraints" several times: batch size 8 in pretraining, a small search space and only 2-epoch search runs.

## Key findings

1. **An all-Bantu model can be built from free online data, and it works, but it doesn't beat the baselines on NER.** MasakhaNER test F1:

   | Model | Swahili | Kinyarwanda | Luganda |
   |---|---|---|---|
   | BantuBERTa | 0.850 | 0.694 | 0.730 |
   | XLM-R base | 0.874 | 0.739 | 0.807 |
   | mBERT | 0.864 | 0.710 | 0.806 |
   | AfriBERTa base | 0.880 | 0.732 | 0.793 |

   The biggest gap is on Luganda.
2. **On topic classification, BantuBERTa roughly equals the best models.** ANTC F1:

   | Model | Lingala | Zulu |
   |---|---|---|
   | BantuBERTa | 0.589 | 0.797 |
   | XLM-R base + MAFT | 0.586 | 0.796 |
   | AfriBERTa + MAFT | 0.549 | 0.764 |

   It gets this with about half of XLM-R's parameters. The author calls it state of the art, but the margin over XLM-R is 0.001–0.003 from a single run.
3. **More data mattered more than the model settings.** In the search, only the two data-filtering settings were statistically significant (adjusted R² = 0.91). The larger, "dirtier" dataset (3.79M sentences) gave lower validation loss and better NER than the cleaner one (2.66M). Once data was held fixed, only depth was marginally significant (p ≈ 0.06–0.07; deeper was better). Vocabulary size (70k vs 100k) and number of heads (6 vs 8) made no significant difference, and the 100k vocabulary gave slightly worse pretraining loss.
4. This backs up Lauscher et al. (2020): similarity between languages matters most for simple tasks, while complex tasks like NER need both similarity and a large pretraining corpus.

## What we got from it

- **Evidence that grouping by language family can help**, at least for classification. This supports sharing parameters between related languages. Our version does it with adapters and typology-guided routing rather than a new model trained from scratch.
- **Pretraining from scratch fails when data is scarce.** BantuBERTa's corpus was 30% smaller than AfriBERTa's and was beaten on NER. This is a good argument for our PEFT approach: adapt an existing strong model instead of pretraining.
- **The author's own next steps point toward our approach.** He suggests adapting XLM-R or AfriBERTa with LAFT or MAFT rather than pretraining. PEFT is the cheap version of this.
- **Conjunctive vs disjunctive spelling** (e.g. Zulu *bangazifunda* written as one word vs Northern Sotho *ba ka bala* written as three) changes what counts as a "word". This matters when we measure tokenization fragmentation (fertility, tokens per word) in WP1. We should report it per writing system, or measure against morphemes rather than orthographic words.
- **Guthrie's Bantu zones (A–S)** are a ready-made, geography-based way to measure how similar two Bantu languages are. We can use them as a static typology baseline in WP2, alongside URIEL and WALS.
- **Morphology tools to follow up:** ZulMorph (Bosch & Pretorius, 2017) for Zulu morpheme tagging, and KinyaBERT (morphology-aware Kinyarwanda model). Both are candidate gold-standard segmenters or comparisons for WP1.
- **Useful clean data sources:** NCHLT (9 South African Bantu languages), KINNEWS/KIRNEWS, Openslr TTS text, XL-Sum, WiLI and the English–Luganda parallel corpus.
- **Hyperparameter defaults for small African encoders:** a vocabulary of about 70k is enough, depth matters more than heads, and batch size 8 is too small.

## Gaps and limitations

- **Stated by the author:**
  - Pretraining data is small (30% smaller than AfriBERTa's) and mostly web-scraped (>80% from mC4 and CC100), so likely low quality.
  - Data is skewed toward Swahili, Zulu and Xhosa, and toward Eastern and Southern Bantu.
  - Only BPE tokenization was tried. WordPiece and other methods were not compared.
  - Only two tasks were tested.
  - The hyperparameter search was narrow (8–10 layers, 6–8 heads, 70k–100k vocabulary) and limited by compute (small batch size).
  - Suggested next steps: clean formal-domain text (books, news), smaller monolingual or trilingual Bantu models, and LAFT/MAFT adaptation of existing models.
- **Our observations:**
  - **Oromo is not a Bantu language.** It is Cushitic (Afroasiatic), yet it makes up 4–5% of the "Bantu" corpus. This weakens the language-family claim, because the corpus isn't purely one family.
  - **Probable mix-up of "topographical" with "typological."** The dissertation repeatedly says "topographically similar" where it seems to mean typologically (structurally) similar. Watch for this when citing.
  - **Possible factual slip.** The claim that all collected languages are Eastern Bantu is doubtful: Lingala (Guthrie zone C) is usually grouped with Western Bantu.
  - **Weak language filtering.** The fastText language-ID model it used only knew Swahili among Bantu languages, so filtering the other languages relied on a heuristic.
  - **Data size and quality can't be separated.** The "cleaner" dataset is also the smaller one, so the finding that more data helps can't be told apart from dirty data being fine.
  - **Baselines aren't like-for-like.** Baseline scores were copied from other papers, which used different fine-tuning setups.
  - **One run each.** There are no seeds, variance estimates or significance tests, so the ANTC "win" (+0.001 to +0.003 F1) is within noise.
  - **Tokenization is never measured.** The dissertation argues that BPE only approximates morphemes but never measures fragmentation (tokens per word, morpheme-boundary alignment). This is exactly the gap our RQ1 targets.
  - **No attempt to rebalance languages.** Swahili is 45–56% of the data, and nothing like temperature sampling or upsampling was used to give low-resource languages a fairer share.
  - **Encoder only, 125M parameters.** It says nothing about generative LLMs, parameter-efficient methods or non-Bantu morphologically rich languages (e.g. Amharic's root-and-pattern morphology).

## Relevance to typology-aware PEFT

- **Morphology / typology angle:** It motivates using typological similarity for transfer and gives Guthrie zones as a Bantu-specific similarity measure (WP2 baseline). It also flags the conjunctive vs disjunctive spelling problem for tokenization (WP1). But it treats "typology" as simply belonging to the Bantu family, which is the kind of static, categorical grouping our RQ2 wants to replace with learned, data-driven vectors.
- **Low-resource / African language angle:** Strong. It maps what Bantu data is on Hugging Face, shows which languages dominate (Swahili, Kinyarwanda, Xhosa, Zulu), and gives a BantuBERTa checkpoint we can use as a baseline for Bantu languages.
- **Efficiency / low-cost hardware angle:** Mostly a cautionary tale. Pretraining from scratch on limited compute (batch size 8) and limited data gave weaker NER than existing models. This supports our choice to adapt a strong existing model with PEFT under 2% trainable parameters instead of pretraining.

## Quotes and figures worth citing

> "on lower-order NLP tasks, like classification, pretraining on languages solely within the language family seemed to benefit transfer" (Abstract, p. ii)

- **Table 4.1 (p. 31):** language distribution of the pretraining corpus. Shows the heavy Swahili skew and Oromo mislabelled as Bantu.
- **Table 4.3 (p. 33):** regression of NER F1 on hyperparameters. Only the data-filtering settings are significant.
- **Table 4.6 (p. 35):** MasakhaNER test F1 against XLM-R, mBERT and AfriBERTa.
- **Table 4.8 (p. 36):** ANTC test F1 (Zulu, Lingala) against MAFT-adapted models.
- **Figure 3.2 (p. 17):** Bantu languages on Hugging Face, by number of datasets.
- **Section 2.4.2 (pp. 10–11):** conjunctive vs disjunctive spelling examples (Zulu vs Northern Sotho).

## Related papers to follow up

- [ ] Ogueji, Zhu & Lin (2021). AfriBERTa: *Small Data? No Problem!* MRL workshop. https://aclanthology.org/2021.mrl-1.11
- [ ] Alabi et al. (2022). *Adapting Pre-trained Language Models to African Languages via Multilingual Adaptive Fine-Tuning* (MAFT). COLING. https://aclanthology.org/2022.coling-1.382
- [ ] Lauscher et al. (2020). *From Zero to Hero: On the Limitations of Zero-Shot Language Transfer with Multilingual Transformers.* EMNLP. https://aclanthology.org/2020.emnlp-main.363
- [ ] Wang, Lipton & Tsvetkov (2020). *On Negative Interference in Multilingual Models.* EMNLP. https://aclanthology.org/2020.emnlp-main.359
- [ ] Nzeyimana & Rubungo (2022). *KinyaBERT: a Morphology-aware Kinyarwanda Language Model.* https://arxiv.org/abs/2203.08459
- [ ] Park et al. (2021). *Morphology Matters: A Multilingual Language Modeling Analysis.* TACL. https://doi.org/10.1162/tacl_a_00365
- [ ] Mesham et al. (2021). *Low-Resource Language Modelling of South African Languages.* https://arxiv.org/abs/2104.00772
- [ ] Bosch & Pretorius (2017). *A Computational Approach to Zulu Verb Morphology within the Context of Lexical Semantics.* Lexikos 27 (ZulMorph)
- [ ] Adelani et al. (2021). *MasakhaNER: Named Entity Recognition for African Languages.* TACL. https://aclanthology.org/2021.tacl-1.66

## Open questions / discussion points

- Would the family-grouping result hold with PEFT? For example, would a LoRA trained on several Bantu languages transfer better to an unseen Bantu language than one trained on mixed-family languages? That's a cheap experiment for WP0/WP3.
- Should we evaluate BantuBERTa ourselves under the same fine-tuning setup and multiple seeds, to check whether the ANTC result holds?
- How should we measure fragmentation fairly across conjunctive (Zulu, Xhosa) and disjunctive (Sotho, Tswana) spelling: per orthographic word or per morpheme?
- Are Guthrie zones a better similarity signal than URIEL/WALS for Bantu languages? This is a possible WP2 comparison.
