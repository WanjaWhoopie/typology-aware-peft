Morfessor pre-segmentation lowers POS accuracy in every language: -3.4 points pooled, 95% CI [-3.6, -3.2]. Zero-shot transfer drops more (-9.8 points over the 30 off-diagonal cells), most from Amharic and Hausa as sources into the Bantu languages (-16.2). No test words are lost to truncation in either setting.

- **The pattern matches NER.** Losses are smallest for kin (-2.0), zul (-2.6) and swa (-3.1), and largest for hau (-5.9).
- **The loss is smaller than for NER.** A POS tag depends mostly on the word itself, while NER needs whole names, which the split breaks apart.
- **See results/ner_morfessor/interpretation.md** for the likely cause and the next variant worth testing.
