# Data access report

datasets 4.4.1, HF_TOKEN not set

| Resource | Status | Note |
|---|---|---|
| SIB-200 amh_Ethi | PASS | train=701, validation=99, test=204 |
| SIB-200 hau_Latn | PASS | train=701, validation=99, test=204 |
| SIB-200 kin_Latn | PASS | train=701, validation=99, test=204 |
| SIB-200 lug_Latn | PASS | train=701, validation=99, test=204 |
| SIB-200 swh_Latn | PASS | train=701, validation=99, test=204 |
| SIB-200 zul_Latn | PASS | train=701, validation=99, test=204 |
| MasakhaNEWS swa | PASS | train=1658, validation=237, test=476 |
| MasakhaNEWS lug | PASS | train=771, validation=110, test=223 |
| MasakhaNEWS amh | PASS | train=1311, validation=188, test=376 |
| MasakhaNEWS hau | PASS | train=2219, validation=317, test=637 |
| MasakhaNER 2.0 kin | FAIL | RuntimeError: Dataset scripts are no longer supported, but found masakhaner2.py |
| MasakhaNER 2.0 lug | FAIL | RuntimeError: Dataset scripts are no longer supported, but found masakhaner2.py |
| MasakhaNER 2.0 swa | FAIL | RuntimeError: Dataset scripts are no longer supported, but found masakhaner2.py |
| MasakhaNER 2.0 zul | FAIL | RuntimeError: Dataset scripts are no longer supported, but found masakhaner2.py |
| MasakhaNER 2.0 hau | FAIL | RuntimeError: Dataset scripts are no longer supported, but found masakhaner2.py |
| MasakhaNER 1.0 amh | FAIL | RuntimeError: Dataset scripts are no longer supported, but found masakhaner.py |
| MasakhaPOS kin | PASS | train=757, validation=151, test=604 |
| MasakhaPOS lug | PASS | train=733, validation=146, test=586 |
| MasakhaPOS swa | PASS | train=693, validation=138, test=553 |
| MasakhaPOS zul | PASS | train=753, validation=150, test=601 |
| MasakhaPOS hau | PASS | train=753, validation=150, test=601 |
| FLORES+ repo | WARN | gated=auto; accept terms on the dataset page and set HF_TOKEN |
| FLORES+ amh_Ethi | FAIL | DatasetNotFoundError: Dataset 'openlanguagedata/flores_plus' is a gated dataset on the Hub. Visit the dataset page at https://huggingface.co/d (config name may differ; check the dataset page) |
| FLORES+ hau_Latn | FAIL | DatasetNotFoundError: Dataset 'openlanguagedata/flores_plus' is a gated dataset on the Hub. Visit the dataset page at https://huggingface.co/d (config name may differ; check the dataset page) |
| FLORES+ kin_Latn | FAIL | DatasetNotFoundError: Dataset 'openlanguagedata/flores_plus' is a gated dataset on the Hub. Visit the dataset page at https://huggingface.co/d (config name may differ; check the dataset page) |
| FLORES+ lug_Latn | FAIL | DatasetNotFoundError: Dataset 'openlanguagedata/flores_plus' is a gated dataset on the Hub. Visit the dataset page at https://huggingface.co/d (config name may differ; check the dataset page) |
| FLORES+ swh_Latn | FAIL | DatasetNotFoundError: Dataset 'openlanguagedata/flores_plus' is a gated dataset on the Hub. Visit the dataset page at https://huggingface.co/d (config name may differ; check the dataset page) |
| FLORES+ zul_Latn | FAIL | DatasetNotFoundError: Dataset 'openlanguagedata/flores_plus' is a gated dataset on the Hub. Visit the dataset page at https://huggingface.co/d (config name may differ; check the dataset page) |
| WURA amh | PASS | 4 files matching 'amh' |
| WURA hau | PASS | 4 files matching 'hau' |
| WURA kin | PASS | 4 files matching 'kin' |
| WURA lug | FAIL | no file matching 'lug' (language may be missing) |
| WURA swa | PASS | 4 files matching 'swa' |
| WURA zul | PASS | 4 files matching 'zul' |
| MADLAD-400 repo | PASS | gated=False (fallback corpus; 6 languages: am, ha, rw, lg, sw, zu) |
| Glot500-c repo | PASS | gated=False (second fallback) |
| AfroXLMR-large-76L tokenizer | PASS | amh: 3 tokens; swa: 6 tokens; zul: 5 tokens |
| UD_Amharic-ATT | WARN | am_att-ud-test.conllu; only a test file, so you must make your own train/dev/test split |
| UniMorph amh | PASS | exists |
| UniMorph zul | PASS | exists |
| UniMorph swa | FAIL | repo not found (resource may not exist for this language) |
| UniMorph kin | FAIL | repo not found (resource may not exist for this language) |
| UniMorph hau | FAIL | repo not found (resource may not exist for this language) |
| HornMorpho | PASS | exists |
| Morfessor | PASS | exists |
| KinyaBERT repo | WARN | exists; the analyser inside is closed-source and provided on request |
| DeepKIN (analyser release?) | PASS | exists |
| Masakhane NER 2.0 repo | PASS | exists |
| Masakhane POS repo | PASS | exists |
| SADiLaR NCHLT isiZulu POS+lemma | WARN | page reachable; open it to check the licence, whether download needs login, and whether it contains MORPHEME boundaries |
| SADiLaR ZulMorph | WARN | page reachable; open it to check the licence, whether download needs login, and whether it contains MORPHEME boundaries |
