# Tokenizers for African Languages

## Reference

| Field | Details |
|---|---|
| **Title** | Tokenizers for African Languages |
| **Authors** | Goodwill Erasmo Ndomba, Medard Edmund Mswahili, Young-Seob Jeong |
| **Year** | 2025 (published online Dec 2024) |
| **Venue** | IEEE Access, vol. 13, pp. 1046–1054 (CC BY 4.0) |
| **DOI / URL** | https://doi.org/10.1109/ACCESS.2024.3522285 |
| **PDF (online)** | [IEEE Access (open access, CC BY 4.0)](https://doi.org/10.1109/ACCESS.2024.3522285) |
| **Code / data** | None released |

**Citation (APA):**
> Ndomba, G. E., Mswahili, M. E., & Jeong, Y.-S. (2025). Tokenizers for African languages. *IEEE Access, 13*, 1046–1054. https://doi.org/10.1109/ACCESS.2024.3522285

<details>
<summary>BibTeX</summary>

```bibtex
@article{ndomba2025tokenizers,
  title   = {Tokenizers for African Languages},
  author  = {Ndomba, Goodwill Erasmo and Mswahili, Medard Edmund and Jeong, Young-Seob},
  journal = {IEEE Access},
  volume  = {13},
  pages   = {1046--1054},
  year    = {2025},
  doi     = {10.1109/ACCESS.2024.3522285}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | Claude (AI-drafted; to be checked) |
| **Date read** | 2026-09-29 |
| **Status** | Read |
| **Relevance to our work** | Medium |
| **Tags** | #tokenization #swahili #hausa #yoruba #multilingual-tokenizers #low-resource |

## Summary

Trains 30k-token WordPiece tokenizers for Swahili, Hausa and Yoruba and compares them with tokenizers for English, Spanish, Arabic and French, and with multilingual tokenizers (AfroXLMR, AfriBERTa, Serengeti, XLM-R, mBERT). Tokenizers are judged by how well a TF-IDF bag-of-tokens classifier (SVM, random forest, logistic regression) does on sentiment and news classification. Language-specific tokenizers generally win, and African multilingual tokenizers beat global ones.

## Method

- **Tokenizers:** WordPiece, 30k vocab, trained on 560k–810k sentences per language (SwahBERT corpus; MasakhaNEWS raw text)
- **Tasks:** sentiment (Swahili data from SwahBERT; NaijaSenti for Hausa/Yoruba) and news classification (Mwananchi; MasakhaNEWS)
- **Classifiers:** tokens → bag-of-words → TF-IDF → SVM / random forest / logistic regression, scikit-learn defaults; accuracy averaged over 5 runs
- **PEFT / neural models:** none (deliberately excluded)

## Key findings

Average accuracy across the three classifiers (Tables 3–6):

| | Swahili SC | Swahili NC | Hausa SC | Hausa NC | Yoruba SC | Yoruba NC |
|---|---|---|---|---|---|---|
| Own tokenizer | 88.9 | **57.5** | 72.1 | 80.9 | 65.8 | 82.8 |
| Best other | Serengeti **89.4** | Serengeti 56.8 | AfriBERTa **72.9** | Swahili tok. **81.1** | Word-level **67.3** | Word-level **83.9** |
| English | 84.5 | 53.4 | 71.9 | 78.9 | 63.6 | 76.6 |
| XLM-R | 88.7 | 54.4 | 71.7 | 80.7 | 64.3 | 74.2 |

- African multilingual tokenizers beat XLM-R/mBERT on average (+1.70 points sentiment, +1.41 news).
- The Yoruba-specific tokenizer beats all multilingual tokenizers on Yoruba news by 6–9 points; the authors link this to few loanwords and tone marks.
- **Their advice:** start with an African multilingual tokenizer (e.g. Serengeti); build a language-specific one only for languages like Yoruba.

## What we got from it

- Supports choosing an **African** base model (AfroXLMR, Serengeti) over XLM-R/mBERT for our experiments.
- Tokenizer choice alone moves accuracy by several points, even without a neural model.
- Candidate tokenizers for our WP0 fragmentation study: AfroXLMR, AfriBERTa, Serengeti, XLM-R, mBERT.

## Gaps and limitations

- **Stated by the authors:** small task datasets; only 2 tasks; classic classifiers instead of neural models.
- **Our observations:**
  - Bag-of-tokens TF-IDF says little about how a tokenizer behaves inside a transformer.
  - No intrinsic metrics (fertility, morpheme-boundary F1), although the paper claims the tokenizers capture affixes and vowel harmony.
  - A word-level tokenizer built from the task data wins on Yoruba, so the setup rewards vocabulary overlap rather than morphology.
  - The "novel tokenizer" is standard WordPiece.
  - Own-tokenizer scores differ between tables (Swahili SC 88.9 in Table 3 vs 88.3 in Table 5; Hausa NC 80.9 vs 82.1).
  - Standard deviations of ±0.01 over 5 runs of mostly deterministic classifiers suggest little real variation was tested.
  - Linguistic claims are shaky: Hausa is described as polysynthetic (it isn't), and "linguistic bonds" are claimed between languages from three different families (Bantu, Chadic, Yoruboid).
  - No Zulu, Xhosa or Amharic.

## Relevance to typology-aware PEFT

- **RQ1 (tokenization):** it shows the gap we fill. Nobody here measures morpheme preservation or tests tokenizers inside a transformer.
- **Base model choice:** backs AfroXLMR/Serengeti as starting points.
- **Typology:** attributes results to linguistic traits (loanwords, tone) but never measures them, so there's room for our data-driven typology (RQ2).

## Related papers to follow up

- [ ] Rust et al. (2021). *How Good is Your Tokenizer? On the Monolingual Performance of Multilingual Language Models.* ACL. https://aclanthology.org/2021.acl-long.243
- [ ] Petrov et al. (2023). *Language Model Tokenizers Introduce Unfairness Between Languages.* NeurIPS. https://arxiv.org/abs/2305.15425
- [ ] Chang et al. (2023). *When Is Multilinguality a Curse?* https://arxiv.org/abs/2311.09205
- [ ] Adebara et al. (2023). *SERENGETI: Massively Multilingual Language Models for Africa.* Findings of ACL. https://aclanthology.org/2023.findings-acl.97
- [ ] Dossou & Emezue (2021). *Crowdsourced Phrase-Based Tokenization for Low-Resourced NMT: The Case of Fon.* https://arxiv.org/abs/2103.08052
