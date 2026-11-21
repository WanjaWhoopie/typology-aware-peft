None of the three input-side variants beats plain LoRA. They all keep the model, the LoRA settings and the trainable parameters, and change only how words reach the model. All 72 runs finished; none collapsed.

**1. Most of the first Morfessor attempt's loss came from the extra word starts, not from extra tokens.**
- Keeping Morfessor's cuts inside words gives almost the same number of tokens per word (for example hau 2.23 against 2.24, zul 2.77 against 2.84).
- Yet the loss is roughly halved for NER (−3.9 against −7.0) and nearly gone for POS (−0.5 against −3.4).
- Zero-shot transfer recovers most (NER −3.9 against −12.4, POS −2.3 against −9.8).
- Feeding each morpheme as a new word is what moved the input away from what the model knows.

**2. The remaining loss with cuts inside words is small for the Bantu languages and large where Morfessor is least reliable.**
- In NER, kin, lug and zul lose 1.0 to 1.8 points, against 7.4 for hau and 9.2 for amh.
- In POS every language is within 1.2 points, and Amharic is level (+0.1).
- Forcing token boundaries onto morpheme boundaries is close to harmless where the cuts are good, but it does not help either. AfroXLMR's own pieces already carry what the task needs.

**3. Serengeti's vocabulary (option B) shortens words a lot but costs accuracy, because many tokens get averaged vectors.**
- Tokens per word drop by about a third (for example zul 2.43 → 1.68, swa 1.51 → 1.08). Yet NER loses 5.8 points and POS 2.3.
- The NER loss follows how many entity-word tokens are new to AfroXLMR, and so carry an averaged vector: amh 44% → −18.5, zul 37% → −5.9, kin 33% → −4.0, lug 32% → −3.1, hau 27% → −2.6, swa 24% → −0.9. That is a perfect rank order over six languages.
- POS shows the same split: the languages with 46 to 50% new tokens (kin, lug, zul) lose 2.7 to 4.2 points, those with 33% (hau, swa) lose 0.9.
- The vocabulary is not the problem. The averaged vectors are, and LoRA cannot change them because the embeddings stay frozen.
- Tokenizer-transfer papers therefore train the new embeddings briefly before fine-tuning. That is the natural next step for option B: a short embedding-only masked-LM pass on the raw text, then the same LoRA runs.

**4. What this means for the thesis.**
Changing only the input, while the representations stay fixed, costs accuracy. The cost is smallest when the change keeps the input close to what the model saw in pretraining. A morphology-aware method therefore has to adapt the model side as well (adapter weights, or embeddings), not just re-cut the words. This supports moving the morphology into the typology-aware adapter rather than into the tokenizer alone.
