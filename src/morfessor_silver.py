#!/usr/bin/env python3
"""Silver morpheme boundaries: train Morfessor Baseline on raw text and check it against isiZulu gold.

Morfessor is unsupervised (it never sees a morpheme), so its segmentations are "silver". Before using it for
Swahili, Kinyarwanda and Luganda (no gold segmentations exist), we measure how well it does where gold exists:
isiZulu (NCHLT, as prepared by Moeng et al., 2021; loaded by src/tokenizer_stats.py).

Raw text: WURA passages (castorini/wura, eval split) for zul, swa, kin. Training uses the most frequent
word types with log-dampened counts. The corpus weight (Morfessor's one hyperparameter: higher = fewer cuts)
is picked on the isiZulu gold dev words and scored on the gold test words, so the test score is held out.

    python src/morfessor_silver.py                 # isiZulu: grid over corpus weights, dev/test scores
    python src/morfessor_silver.py --langs zul swa kin --weights 1.0

Writes results/tokenizers/morfessor.csv and models to data/processed/morfessor_<lang>_<weight>.bin.
"""
import argparse
import csv
import math
import random
import re
import sys
from collections import Counter
from pathlib import Path

import morfessor
import numpy as np
from huggingface_hub import hf_hub_download

from tokenizer_stats import load_gold

WORD = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)*")  # letters only, no digits or punctuation


def word_counts(lang, raw, max_types):
    f = hf_hub_download("castorini/wura", f"passages-v1.0/eval/{lang}.txt", repo_type="dataset",
                        local_dir=raw / "wura")
    c = Counter()
    with open(f, encoding="utf-8") as fh:
        for line in fh:
            c.update(w.lower() for w in WORD.findall(line))
    return c, dict(c.most_common(max_types))


def train(counts, weight, seed=0):
    random.seed(seed)  # Morfessor shuffles with the random module
    m = morfessor.BaselineModel(corpusweight=weight)
    # integer log-dampened counts (fractional counts break Morfessor's bookkeeping)
    m.load_data([(n, w) for w, n in counts.items()], count_modifier=lambda x: int(round(math.log(x + 1, 2))))
    m.train_batch()
    return m


def cuts(model, word):
    segs = model.viterbi_segment(word.lower())[0]
    return set(np.cumsum([len(s) for s in segs])[:-1].tolist())


def score(model, gold):
    tp = n_pred = n_gold = exact = 0
    for w, g in gold.items():
        t = cuts(model, w)
        tp += len(t & g); n_pred += len(t); n_gold += len(g); exact += t == g
    p, r = tp / max(n_pred, 1), tp / max(n_gold, 1)
    return dict(boundary_p=p, boundary_r=r, boundary_f1=2 * p * r / max(p + r, 1e-9), exact_match=exact / len(gold),
                morphs_per_word=(n_pred + len(gold)) / len(gold))


def gold_split(raw, split):
    """Gold words of one split only (load_gold merges all three)."""
    allw = load_gold("zul", raw)
    names = {l.split(" | ")[0] for l in (raw / "morph_zul" / f"zul.{split}.conll").read_text(encoding="utf-8").splitlines()}
    return {w: c for w, c in allw.items() if w in names}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--langs", nargs="+", default=["zul"])
    ap.add_argument("--weights", nargs="+", type=float, default=[0.1, 0.3, 1.0, 3.0])
    ap.add_argument("--max_types", type=int, default=100_000)
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--processed", default="data/processed")
    ap.add_argument("--out", default="results/tokenizers")
    args = ap.parse_args()
    raw, proc = Path(args.raw), Path(args.processed)
    proc.mkdir(parents=True, exist_ok=True)
    gold = {s: gold_split(raw, s) for s in ("dev", "test")} | {"all": load_gold("zul", raw)}

    rows = []
    for lang in args.langs:
        full, counts = word_counts(lang, raw, args.max_types)
        print(f"{lang}: {sum(full.values()):,} words, {len(full):,} types, training on {len(counts):,}", flush=True)
        for wgt in args.weights:
            m = train(counts, wgt)
            morfessor.MorfessorIO().write_binary_model_file(str(proc / f"morfessor_{lang}_{wgt}.bin"), m)
            row = dict(lang=lang, corpus_weight=wgt, train_types=len(counts), corpus_words=sum(full.values()))
            if lang == "zul":
                for s, g in gold.items():
                    row |= {f"{s}_{k}": v for k, v in score(m, g).items()}
                print(f"  weight {wgt}: dev F1 {row['dev_boundary_f1']:.3f}, test F1 {row['test_boundary_f1']:.3f} "
                      f"(P {row['test_boundary_p']:.2f}, R {row['test_boundary_r']:.2f}, "
                      f"morphs/word {row['test_morphs_per_word']:.2f})", flush=True)
            rows.append(row)

    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(Path(args.out) / "morfessor.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    zul = [r for r in rows if r["lang"] == "zul"]
    if zul:
        best = max(zul, key=lambda r: r["dev_boundary_f1"])
        print(f"\nBest weight on isiZulu dev: {best['corpus_weight']}. Held-out test: F1 {best['test_boundary_f1']:.3f}, "
              f"P {best['test_boundary_p']:.3f}, R {best['test_boundary_r']:.3f}, exact {best['test_exact_match']:.1%}. "
              f"All gold words: F1 {best['all_boundary_f1']:.3f}")


if __name__ == "__main__":
    main()
