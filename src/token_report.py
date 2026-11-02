#!/usr/bin/env python3
"""Summarise results/<task> (NER or POS) into tables (markdown + CSV). Needs only numpy.

    python src/token_report.py --task ner [--dir results/ner]

Same layout as src/sib200_report.py. Scores are entity-level F1 (NER) or accuracy (POS), in %.
95% CIs come from bootstrapping test sentences (the same resampled sentences for every seed).
If the folder has an interpretation.md (hand-written notes), it is appended as the last section.
"""
import argparse
from collections import defaultdict
from pathlib import Path

import numpy as np

from sib200_report import BANTU, ORDER, md_table, read


def total(task, items):
    """items: n x k per-sentence counts (k=3 tp/fp/fn for NER, k=2 correct/total for POS) -> score."""
    s = items.sum(axis=-2)
    if task == "ner":
        tp, fp, fn = s[..., 0], s[..., 1], s[..., 2]
        return np.where(tp > 0, 2 * tp / np.maximum(2 * tp + fp + fn, 1), 0.0)
    return s[..., 0] / s[..., 1]


def boot(task, per_seed, n=2000, seed=0):
    """per_seed: seeds x sentences x k. Bootstrap distribution of the seed-averaged score."""
    a = np.asarray(per_seed, dtype=float)
    idx = np.random.default_rng(seed).integers(0, a.shape[1], size=(n, a.shape[1]))
    return np.stack([total(task, s[idx]) for s in a]).mean(axis=0)  # n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True, choices=["ner", "pos"])
    ap.add_argument("--dir", default=None)
    args = ap.parse_args()
    task = args.task
    d = Path(args.dir or f"results/{task}")
    res, runs = read(d / "results.jsonl"), read(d / "runs.jsonl")
    langs = [l for l in ORDER if any(r["src"] == l for r in res)]
    methods = sorted({r["method"] for r in res})
    name = "entity F1" if task == "ner" else "accuracy"
    lines = [f"# {task.upper()} baseline summary", "",
             f"Model: {res[0]['model']}. Metric: {name} (%). Seeds per cell: {sorted({r['seed'] for r in res})}.", ""]
    if task == "ner":
        lines += ["Data: MasakhaNER 2.0 (hau, kin, lug, swa, zul); MasakhaNER 1.0 for amh "
                  "(different annotation round and splits).", ""]
    else:
        lines += ["Data: MasakhaPOS (hau, kin, lug, swa, zul); UD_Amharic-ATT for amh, split 70/10/20 by us. "
                  "Amharic tokens are UD syntactic words (clitics split off), not surface words.", ""]

    sc, items = {}, {}
    for m in methods:
        s, it = defaultdict(list), defaultdict(list)
        for r in res:
            if r["method"] == m:
                s[(r["src"], r["tgt"])].append(r["score"]); it[(r["src"], r["tgt"])].append(r["items"])
        sc[m], items[m] = s, it

    for m in methods:
        lines += [f"## Method: {m}", "", "### In-language baseline (diagonal)", ""]
        rows = []
        for l in langs:
            k = (l, l)
            if k not in sc[m]:
                continue
            a = np.array(sc[m][k]) * 100
            lo, hi = np.percentile(boot(task, items[m][k]), [2.5, 97.5]) * 100
            rr = [r for r in runs if r["method"] == m and r["src"] == l]
            mem = [r["peak_mem_gb"] for r in rr if r["peak_mem_gb"] is not None]
            rows.append([l, f"{a.mean():.1f} ± {a.std():.1f}", f"[{lo:.1f}, {hi:.1f}]",
                         f"{np.mean([r['trainable_pct'] for r in rr]):.2f}",
                         f"{np.mean(mem):.1f}" if mem else "n/a", f"{np.mean([r['seconds'] for r in rr]):.0f}",
                         f"{np.mean([r['best_epoch'] for r in rr]):.1f}", f"{len(items[m][k][0])}", f"{len(a)}"])
        lines += [md_table(["lang", f"{name} % (mean ± sd over seeds)", "95% CI (test sentences)", "trainable %",
                            "peak GPU GB", "seconds/run", "best epoch (mean)", "test sentences", "seeds"], rows), ""]

        M = np.full((len(langs), len(langs)), np.nan)
        for i, s in enumerate(langs):
            for j, t in enumerate(langs):
                if (s, t) in sc[m]:
                    M[i, j] = np.mean(sc[m][(s, t)]) * 100
        lines += [f"### Zero-shot transfer matrix: {name} % (rows = source, columns = target)", "",
                  md_table(["source \\ target"] + langs,
                           [[s] + [f"{M[i, j]:.1f}" for j in range(len(langs))] for i, s in enumerate(langs)]), ""]
        R = M / np.diag(M)[None, :]
        lines += ["### Relative transfer (zero-shot / in-language score of the target)", "",
                  md_table(["source \\ target"] + langs + ["mean as source"],
                           [[s] + [f"{R[i, j]:.2f}" for j in range(len(langs))] +
                            [f"{np.nanmean(np.delete(R[i], i)):.2f}"] for i, s in enumerate(langs)]
                           + [["mean as target"] + [f"{np.nanmean(np.delete(R[:, j], j)):.2f}"
                                                    for j in range(len(langs))] + [""]]), ""]
        np.savetxt(d / f"matrix_{m}_score.csv", M, delimiter=",", header=",".join(langs), fmt="%.2f", comments="")
        np.savetxt(d / f"matrix_{m}_relative.csv", R, delimiter=",", header=",".join(langs), fmt="%.4f", comments="")

        off = ~np.eye(len(langs), dtype=bool)
        X = np.where(off, M, np.nan)
        tot = np.nanvar(X)
        col = np.nanvar(np.where(off, np.nanmean(X, 0)[None, :], np.nan))
        row = np.nanvar(np.where(off, np.nanmean(X, 1)[:, None], np.nan))
        bantu = [i for i, l in enumerate(langs) if l in BANTU]
        other = [i for i, l in enumerate(langs) if l not in BANTU]
        within = [M[i, j] for i in bantu for j in bantu if i != j]
        across = [M[i, j] for i in other for j in bantu]
        lines += ["### Structure of the zero-shot matrix (off-diagonal cells)", "",
                  md_table(["measure", "value"], [
                      ["share of variance explained by the target (column means)", f"{100 * col / tot:.0f}%"],
                      ["share of variance explained by the source (row means)", f"{100 * row / tot:.0f}%"],
                      [f"Bantu -> Bantu, mean {name} %", f"{np.mean(within):.1f}" if within else "n/a"],
                      [f"amh/hau -> Bantu, mean {name} %", f"{np.mean(across):.1f}" if across else "n/a"]]), ""]

        bad = [r for r in runs if r["method"] == m and r["collapsed"]]
        if bad:
            lines += ["Collapsed runs: " + ", ".join(f"{r['src']} seed {r['seed']}" for r in bad), ""]

    if len(methods) == 2:
        a_m, b_m = methods
        lines += [f"## {b_m} minus {a_m}, in-language {name} (percentage points)", ""]
        rows, diffs = [], []
        for l in langs:
            k = (l, l)
            if k in sc[a_m] and k in sc[b_m]:
                rows.append([l, f"{(np.mean(sc[b_m][k]) - np.mean(sc[a_m][k])) * 100:+.1f}"])
                # paired: the same resampled sentences for both methods (same seed in boot)
                diffs.append(boot(task, items[b_m][k]) - boot(task, items[a_m][k]))
        lines += [md_table(["lang", "difference"], rows), ""]
        pooled = np.mean(diffs, axis=0)
        point = np.mean([float(r[1]) for r in rows])
        lo, hi = np.percentile(pooled, [2.5, 97.5]) * 100
        lines += [f"Pooled over {len(rows)} languages and all seeds: {point:+.1f} points, "
                  f"95% CI [{lo:+.1f}, {hi:+.1f}] (paired bootstrap over test sentences).", ""]

    notes = d / "interpretation.md"
    if notes.exists():
        lines += ["## Interpretation", "", notes.read_text(encoding="utf-8").strip(), ""]

    (d / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {d / 'summary.md'}")


if __name__ == "__main__":
    main()
