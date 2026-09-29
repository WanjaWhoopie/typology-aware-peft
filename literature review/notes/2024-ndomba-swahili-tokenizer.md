# Effects of Swahili Monolingual Tokenizer on Downstream Tasks

## Reference

| Field | Details |
|---|---|
| **Title** | Effects of Swahili Monolingual Tokenizer on Downstream Tasks |
| **Authors** | Goodwill Erasmo Ndomba, Young-Seob Jeong |
| **Year** | 2024 |
| **Venue** | IEEE BigComp 2024, pp. 357–358 (2-page extended abstract) |
| **DOI / URL** | https://doi.org/10.1109/BIGCOMP60711.2024.00067 |
| **PDF (online)** | [IEEE Xplore (via DOI, paywalled)](https://doi.org/10.1109/BIGCOMP60711.2024.00067) |
| **Code / data** | None released |

**Citation (APA):**
> Ndomba, G. E., & Jeong, Y.-S. (2024). Effects of Swahili monolingual tokenizer on downstream tasks. In *2024 IEEE International Conference on Big Data and Smart Computing (BigComp)* (pp. 357–358). IEEE. https://doi.org/10.1109/BIGCOMP60711.2024.00067

<details>
<summary>BibTeX</summary>

```bibtex
@inproceedings{ndomba2024swahili,
  title     = {Effects of Swahili Monolingual Tokenizer on Downstream Tasks},
  author    = {Ndomba, Goodwill Erasmo and Jeong, Young-Seob},
  booktitle = {2024 IEEE International Conference on Big Data and Smart Computing (BigComp)},
  pages     = {357--358},
  year      = {2024},
  doi       = {10.1109/BIGCOMP60711.2024.00067}
}
```
</details>

## Reading log

| Field | Details |
|---|---|
| **Read by** | Claude (AI-drafted; to be checked) |
| **Date read** | 2026-09-29 |
| **Status** | Read |
| **Relevance to our work** | Low |
| **Tags** | #tokenization #swahili #low-resource |

## Summary

Trains a 30k-token Swahili SentencePiece tokenizer and compares it with the mBERT and English BERT tokenizers on Swahili sentiment and news classification. Tokens are fed to classic classifiers (SVM, random forest). The Swahili tokenizer **loses** to both; the authors blame its small training set (23M words). Superseded by the same group's 2025 IEEE Access paper, which reaches the opposite conclusion.

## Method

- **Tokenizers:** Swahili SentencePiece (trained on 23M words from the SwahBERT corpus) vs mBERT and English BERT tokenizers
- **Tasks:** news classification (1,895 headlines, 5 classes) and sentiment (7,107 texts, 3 classes)
- **Classifiers:** SVM and random forest, scikit-learn defaults; 8:1:1 split; accuracy
- **PEFT / neural models:** none

## Key findings

| Tokenizer | Sentiment (SVM / RF) | News (SVM / RF) |
|---|---|---|
| mBERT | 0.83 / 0.29 | **0.67** / 0.45 |
| English BERT | **0.86** / 0.34 | 0.65 / 0.45 |
| Swahili (theirs) | 0.67 / 0.30 | 0.62 / 0.44 |

- The English tokenizer does well on Swahili, which the authors put down to shared Latin script and loanwords.

## What we got from it

- Early evidence that tokenizer training-data size matters as much as being language-specific.

## Gaps and limitations

- **Stated by the authors:** small tokenizer corpus; classic classifiers instead of language models.
- **Our observations:**
  - Random forest scores (~0.30 on 3-class sentiment) are at chance level, so half the results are uninformative.
  - The text says the sentiment gap is smaller than the news gap; the table shows the opposite.
  - Single run, no variance, no tokenizer metrics (fertility, morpheme alignment).

## Relevance to typology-aware PEFT

- Only as background for RQ1. Cite the 2025 paper instead.

## Related papers to follow up

- [ ] Martin et al. (2022). *SwahBERT: Language Model of Swahili.* NAACL. https://aclanthology.org/2022.naacl-main.23
