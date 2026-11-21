#!/usr/bin/env python3
"""Option B: move a donor tokenizer's vocabulary into AfroXLMR (Fast Vocabulary Transfer, Gee et al. 2022).

The model keeps every transformer weight; only the tokenizer and the input embedding matrix change:
  - a donor token that AfroXLMR also has keeps AfroXLMR's trained vector;
  - a new donor token gets the mean of the AfroXLMR vectors of the pieces AfroXLMR splits its string into
    (a word-start token '▁abc' is split as a word start, an inner token 'abc' as the inside of a word);
  - special tokens (<s>, </s>, <pad>, <unk>, <mask>) are matched by role.
Donor: Serengeti (UBC-NLP/serengeti), which splits least for all six languages in the Tokenizer stats tab and
covers isiZulu and Luganda (AfriBERTa does not). Same architecture family (XLM-R, SentencePiece, 250k types).

    python src/vocab_transfer.py --out /content/afroxlmr_serengeti_fvt
    python src/token_baseline.py --task ner --methods lora --model /content/afroxlmr_serengeti_fvt \\
        --out results/ner_serengeti_fvt

The LoRA runs then train exactly the same parameters as plain LoRA (embeddings stay frozen at their FVT values),
so any difference comes from the vocabulary. Also writes transfer_stats.json next to the model.
"""
import argparse
import json
from pathlib import Path

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

from token_baseline import inner_tokens


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Davlan/afro-xlmr-large-76L")
    ap.add_argument("--donor", default="UBC-NLP/serengeti")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    old_tok, new_tok = AutoTokenizer.from_pretrained(args.model), AutoTokenizer.from_pretrained(args.donor)
    model = AutoModelForMaskedLM.from_pretrained(args.model)
    old_emb = model.get_input_embeddings().weight.detach().clone()
    old_vocab = old_tok.get_vocab()
    special = {new_tok.convert_tokens_to_ids(t): old_tok.convert_tokens_to_ids(t)
               for t in ("<s>", "</s>", "<pad>", "<unk>", "<mask>")}

    new_emb = torch.empty(len(new_tok), old_emb.shape[1], dtype=old_emb.dtype)
    n_copy = n_mean = n_unk = 0
    pieces_per_new = []
    for tok, i in new_tok.get_vocab().items():
        if i in special:
            new_emb[i] = old_emb[special[i]]
            n_copy += 1
        elif tok in old_vocab:
            new_emb[i] = old_emb[old_vocab[tok]]
            n_copy += 1
        else:
            if tok.startswith("▁"):
                parts = old_tok.tokenize(tok[1:]) if tok != "▁" else ["▁"]
            else:
                parts = inner_tokens(old_tok, tok, old_vocab)
            ids = [old_vocab.get(p, old_tok.unk_token_id) for p in parts] or [old_tok.unk_token_id]
            n_unk += all(x == old_tok.unk_token_id for x in ids)
            new_emb[i] = old_emb[ids].mean(0)
            pieces_per_new.append(len(ids))
            n_mean += 1

    model.resize_token_embeddings(len(new_tok))
    model.get_input_embeddings().weight.data.copy_(new_emb)
    model.config.vocab_size = len(new_tok)
    for k in ("bos_token_id", "eos_token_id", "pad_token_id"):
        setattr(model.config, k, getattr(new_tok, k))
    out = Path(args.out)
    model.save_pretrained(out)
    new_tok.save_pretrained(out)
    # transformers 4.57.2 fails to load a tokenizer from a local folder whose config.json records a version
    # <= 4.57.2 ('dict' object has no attribute 'model_type'); the field is informational, so drop it
    cfg = json.loads((out / "config.json").read_text(encoding="utf-8"))
    cfg.pop("transformers_version", None)
    (out / "config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    stats = dict(model=args.model, donor=args.donor, vocab=len(new_tok), copied=n_copy, fvt_mean=n_mean,
                 all_unknown=n_unk, mean_pieces_per_new_token=sum(pieces_per_new) / max(len(pieces_per_new), 1))
    (out / "transfer_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
