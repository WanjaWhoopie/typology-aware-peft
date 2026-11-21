# Data

- `raw/`: datasets exactly as downloaded
- `processed/`: cleaned or tokenized versions

Dataset files are not committed (see `.gitignore`). List every dataset below so anyone can reproduce the setup.

| Dataset | Languages | Task | Source / link | Licence | Location |
| ------- | --------- | ---- | ------------- | ------- | -------- |
| SIB-200 | amh, hau, kin, lug, swa, zul (+ eng for the tokenizer study) | topic classification; parallel text for tokenizer stats and pseudo-perplexity | [Davlan/sib200](https://huggingface.co/datasets/Davlan/sib200) (Hugging Face) | CC BY-SA 4.0 | Hugging Face cache (downloaded by `src/sib200_baseline.py`) |
| MasakhaNER 2.0 | hau, kin, lug, swa, zul | NER | [masakhane-io/masakhane-ner](https://github.com/masakhane-io/masakhane-ner), `MasakhaNER2.0/data/<lang>/` | Repo LICENSE covers the code (Apache 2.0); data licence not stated there, check the dataset card | `raw/masakhaner/<lang>/` |
| MasakhaNER 1.0 | amh | NER | same repo, `data/amh/` | as above | `raw/masakhaner/amh/` |
| MasakhaPOS | hau, kin, lug, swa, zul | POS tagging | [masakhane/masakhapos](https://huggingface.co/datasets/masakhane/masakhapos) (Hugging Face) | AFL 3.0 | Hugging Face cache |
| UD_Amharic-ATT | amh | POS tagging (test file only, split 70/10/20 by us) | [UniversalDependencies/UD_Amharic-ATT](https://github.com/UniversalDependencies/UD_Amharic-ATT) | CC BY-SA 4.0 | `raw/ud_amharic_att/` |
| NCHLT isiZulu segmentations (as prepared by Moeng et al. 2021) | zul | gold morpheme boundaries | [TumiMoeng/MORPH_SEGMENT](https://github.com/TumiMoeng/MORPH_SEGMENT) | MIT (repo) | `raw/morph_zul/` |
| WURA (eval passages) | amh, hau, kin, swa, zul | raw text for Morfessor and the masked-LM pass | [castorini/wura](https://huggingface.co/datasets/castorini/wura) | Apache 2.0 | `raw/wura/` |
| MADLAD-400 (clean, `lg`) | lug | raw text for Morfessor and the masked-LM pass | [allenai/madlad-400](https://huggingface.co/datasets/allenai/madlad-400) | ODC-BY (dataset card; licence field could not be read automatically, check) | `raw/madlad/` |

Licences checked on 2026-11-21 from the Hugging Face dataset cards and the GitHub repositories.
