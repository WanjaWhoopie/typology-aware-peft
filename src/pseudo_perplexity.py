#!/usr/bin/env python3
"""How well does the encoder know each language? Masked-LM pseudo-log-likelihood on parallel text.

Scores the SIB-200 sentences (the same sentences translated into every language, from FLORES)
with the masked-LM head of the encoder, one masked position at a time:
  token     = classic pseudo-log-likelihood (mask one subword, predict it)
  word_l2r  = mask the subword and the rest of its word, predict it (Kauf & Ivanova, 2023).
              Fairer across languages, because a fragmented word cannot be guessed from its own pieces.
Because the sentences are parallel, the total NLL per sentence is comparable across languages
(same content), unlike per-token perplexity, which depends on how finely the tokenizer splits.

    python src/pseudo_perplexity.py                    # SIB-200 test split, 6 languages
    python src/pseudo_perplexity.py --split validation

Writes results/pppl/sentences.jsonl and results/pppl/summary.md. If results/sib200/results.jsonl
exists, also correlates sentence NLL with how often the SIB-200 models classified that sentence correctly.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import torch
from datasets import load_dataset
from transformers import AutoModelForMaskedLM, AutoTokenizer

LANGS = {"amh": "amh_Ethi", "hau": "hau_Latn", "kin": "kin_Latn",
         "lug": "lug_Latn", "swa": "swh_Latn", "zul": "zul_Latn"}


def masked_inputs(enc, mask_id, variant):
    """One copy of the sentence per scored subword; returns (input_ids list, target positions, gold ids)."""
    ids, wids = enc["input_ids"], enc.word_ids()
    seqs, pos, gold = [], [], []
    for i, w in enumerate(wids):
        if w is None:  # <s>, </s>
            continue
        x = list(ids)
        x[i] = mask_id
        if variant == "word_l2r":
            for j in range(i + 1, len(ids)):
                if wids[j] != w:
                    break
                x[j] = mask_id
        seqs.append(x); pos.append(i); gold.append(ids[i])
    return seqs, pos, gold


@torch.no_grad()
def sentence_nll(model, seqs, pos, gold, device, bs):
    total = 0.0
    for k in range(0, len(seqs), bs):
        x = torch.tensor(seqs[k:k + bs], device=device)
        h = model.base_model(input_ids=x).last_hidden_state  # logits only at the scored position (saves memory)
        h = h[torch.arange(len(x), device=device), torch.tensor(pos[k:k + bs], device=device)]
        logp = torch.log_softmax(model.lm_head(h).float(), dim=-1)
        total -= logp[torch.arange(len(x), device=device), torch.tensor(gold[k:k + bs], device=device)].sum().item()
    return total


def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Davlan/afro-xlmr-large-76L")
    ap.add_argument("--langs", nargs="+", default=list(LANGS), choices=list(LANGS))
    ap.add_argument("--split", default="test")
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--out", default="results/pppl")
    ap.add_argument("--sib_results", default="results/sib200/results.jsonl")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForMaskedLM.from_pretrained(
        args.model, dtype=torch.float16 if device.type == "cuda" else torch.float32).to(device).eval()

    rows = []
    for l in args.langs:
        d = load_dataset("Davlan/sib200", LANGS[l])[args.split]
        for n, (iid, text) in enumerate(zip(d["index_id"], d["text"])):
            enc = tok(text, truncation=True, max_length=256)
            r = {"lang": l, "item": n, "index_id": iid, "n_words": len(text.split()),
                 "n_tokens": len(enc["input_ids"]) - 2}
            for variant in ("token", "word_l2r"):
                r[f"nll_{variant}"] = sentence_nll(model, *masked_inputs(enc, tok.mask_token_id, variant),
                                                   device, args.bs)
            rows.append(r)
        print(f"{l}: {len(d)} sentences scored", flush=True)
    with open(out / "sentences.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    # item accuracy from the SIB-200 runs (all methods, sources and seeds), if available
    item_acc = {}
    sib = Path(args.sib_results)
    if sib.exists() and args.split == "test":
        res = [json.loads(x) for x in sib.read_text(encoding="utf-8").splitlines() if x.strip()]
        for l in args.langs:
            c = [r["correct"] for r in res if r["tgt"] == l]
            if c:
                item_acc[l] = np.mean(c, axis=0)

    lines = ["# Masked-LM pseudo-log-likelihood", "",
             f"Model: {args.model}. SIB-200 {args.split} split ({len(rows) // len(args.langs)} parallel sentences "
             "per language). Lower NLL = the model predicts the text better.", "",
             "NLL per sentence is the fairest comparison across languages (same content). "
             "PPPL per token depends on how finely each language is split into subwords.", ""]
    table = []
    for l in args.langs:
        rr = [r for r in rows if r["lang"] == l]
        toks = sum(r["n_tokens"] for r in rr)
        nll_t = np.array([r["nll_token"] for r in rr])
        nll_w = np.array([r["nll_word_l2r"] for r in rr])
        rho = f"{spearman(nll_w, item_acc[l]):+.2f}" if l in item_acc else "n/a"
        table.append([l, f"{np.mean(nll_w):.1f}", f"{np.mean(nll_t):.1f}", f"{np.exp(nll_w.sum() / toks):.2f}",
                      f"{np.exp(nll_t.sum() / toks):.2f}", f"{toks / sum(r['n_words'] for r in rr):.2f}", rho])
    lines += ["| lang | NLL/sentence word_l2r | NLL/sentence token | PPPL word_l2r | PPPL token | tokens/word "
              "| Spearman(NLL, SIB item acc) |", "|---|---|---|---|---|---|---|"]
    lines += ["| " + " | ".join(r) + " |" for r in table]
    lines += ["", "Spearman is computed per language over sentences, using word_l2r NLL. A negative value means "
              "sentences the model predicts poorly are also classified wrongly more often.", ""]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
