None of the three input-side variants beats plain LoRA. They all keep the model, the LoRA settings and the trainable parameters, and change only how words reach the model. All 72 runs finished; none collapsed. CIs resample test sentences and seeds; with 3 seeds, the seed part is coarse.

**Scope of these results.** Every variant was tested with the embeddings frozen and only LoRA trained. That keeps the trainable parameters equal to the baseline, but it leaves the model no way to absorb an input change. Published vocabulary swaps train the embeddings or the model after the swap. So these results show that the input changes do not help **without adaptation**. They do not show that input changes cannot help. The LoRA baseline itself may also be undertrained (most NER runs peaked in the last of 5 epochs), so all differences should be re-measured once the baselines are trained to convergence.

**1. In the first Morfessor attempt, the extra word starts did most of the damage.**
- The two Morfessor arms use the same cuts and almost the same number of tokens per word (for example hau 2.23 against 2.24, zul 2.77 against 2.84; amh differs, 2.44 against 2.77). The main difference between them is whether each morpheme starts a new word.
- Keeping the cuts inside words roughly halves the NER loss (−3.9 against −7.0) and nearly removes the POS loss (−0.5 against −3.4).
- Zero-shot transfer recovers most of its loss (NER −3.9 against −12.4, POS −2.3 against −9.8).

**2. Cutting inside words still loses a little, and these results cannot say whether better cuts would help.**
- In NER, kin, lug and zul lose 1.0 to 1.8 points, against 7.4 for hau and 9.2 for amh. In POS every language is within 1.2 points, and Amharic is level (+0.1).
- Morfessor is not a morpheme gold standard. On isiZulu gold its precision is 0.51, so about half its cuts are wrong. No gold exists for the other languages.
- Whether cut quality matters is therefore untested. It would need a scrambled-cut control (same number of cuts at random positions) and a supervised segmenter (isiZulu only).

**3. Serengeti's vocabulary (option B) shortens words a lot but costs accuracy with frozen embeddings.**
- Tokens per word drop by about a third (for example zul 2.43 → 1.68, swa 1.51 → 1.08). Yet NER loses 5.8 points and POS 2.3.
- About a third to a half of the tokens are new to AfroXLMR and carry only an average of their AfroXLMR pieces, which LoRA cannot change.
- **Hypothesis, not a finding:** the NER loss rises with the share of new tokens in entity words (amh 44% → −18.5 down to swa 24% → −0.9). This measure was chosen after the all-token share did not line up, and there are only six languages. It needs testing, for example by training the embeddings and checking whether the loss shrinks most where the share is highest.
- **A lead in the other direction:** NER transfer into isiZulu rises with Serengeti's vocabulary (lug→zul +7.9, swa→zul +7.5, hau→zul +3.4). Possible cause: isiZulu capitalises a name after its noun-class prefix (uMandela), and Serengeti keeps `▁uM andela` together where AfroXLMR splits `▁u Man dela`. These cells were noticed after looking at the table, so they are a lead to test, not a result.
- Next step for option B: an adaptation ladder (frozen embeddings, then trainable embeddings, then a short masked-LM pass on raw text) with the same LoRA runs on top.

**4. What this means for RQ1.**
Without adaptation, changing how words reach the model costs accuracy. The cost is smallest when the input stays close to what the model saw in pretraining. Whether morpheme-aligned input helps once the model can adapt to it is still open, and it is the question the next experiments should answer. These results do not yet show that morphology must be handled on the model side.
