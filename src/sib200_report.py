#!/usr/bin/env python3
"""Summarise results/sib200 into tables (markdown + CSV). Needs only numpy.

    python src/sib200_report.py [--dir results/sib200]

Writes summary.md and matrix_<method>_{acc,relative}.csv into the same folder.
Accuracy matrix: rows = source (training) language, columns = target (test) language.
Relative transfer = zero-shot accuracy on the target / in-language accuracy on the target.
95% CIs come from bootstrapping the test items (they show how noisy a 204-item test set is).
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ORDER = ["amh", "hau", "kin", "lug", "swa", "zul"]


def read(path):
    return [json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()]


def boot_ci(arr, n=2000, seed=0):
    """arr: seeds x items matrix of 0/1. CI of the seed-averaged accuracy, resampling items."""
    arr = np.asarray(arr, dtype=float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, arr.shape[1], size=(n, arr.shape[1]))
    boots = arr[:, idx].mean(axis=2).mean(axis=0)
    return np.percentile(boots, [2.5, 97.5])


def md_table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="results/sib200")
    args = ap.parse_args()
    d = Path(args.dir)
    res, runs = read(d / "results.jsonl"), read(d / "runs.jsonl")
    langs = [l for l in ORDER if any(r["src"] == l for r in res)]
    methods = sorted({r["method"] for r in res})
    lines = [f"# SIB-200 baseline summary", "", f"Model: {res[0]['model']}. "
             f"Seeds per cell: {sorted({r['seed'] for r in res})}. Test set: 204 items per language.", ""]

    acc, f1, corr = {}, {}, {}
    for m in methods:
        a, f, c = defaultdict(list), defaultdict(list), defaultdict(list)
        for r in res:
            if r["method"] == m:
                k = (r["src"], r["tgt"])
                a[k].append(r["acc"]); f[k].append(r["macro_f1"]); c[k].append(r["correct"])
        acc[m], f1[m], corr[m] = a, f, c

    for m in methods:
        lines += [f"## Method: {m}", "", "### In-language baseline (diagonal)", ""]
        rows = []
        for l in langs:
            k = (l, l)
            if k not in acc[m]:
                continue
            a = np.array(acc[m][k]) * 100
            lo, hi = boot_ci(corr[m][k]) * 100
            rr = [r for r in runs if r["method"] == m and r["src"] == l]
            pct = np.mean([r["trainable_pct"] for r in rr])
            mem = [r["peak_mem_gb"] for r in rr if r["peak_mem_gb"] is not None]
            rows.append([l, f"{a.mean():.1f} ± {a.std():.1f}", f"[{lo:.1f}, {hi:.1f}]",
                         f"{np.mean(f1[m][k]) * 100:.1f}", f"{pct:.2f}",
                         f"{np.mean(mem):.1f}" if mem else "n/a", f"{np.mean([r['seconds'] for r in rr]):.0f}",
                         f"{len(a)}"])
        lines += [md_table(["lang", "acc % (mean ± sd over seeds)", "95% CI (test items)", "macro-F1 %",
                            "trainable %", "peak GPU GB", "seconds/run", "seeds"], rows), ""]

        lines += ["### Zero-shot transfer matrix: accuracy % (rows = source, columns = target)", ""]
        M = np.full((len(langs), len(langs)), np.nan)
        for i, s in enumerate(langs):
            for j, t in enumerate(langs):
                if (s, t) in acc[m]:
                    M[i, j] = np.mean(acc[m][(s, t)]) * 100
        lines += [md_table(["source \\ target"] + langs,
                           [[s] + [f"{M[i, j]:.1f}" for j in range(len(langs))] for i, s in enumerate(langs)]), ""]

        diag = np.diag(M)
        R = M / diag[None, :]  # divide each column (target) by its in-language score
        lines += ["### Relative transfer (zero-shot / in-language score of the target)", ""]
        lines += [md_table(["source \\ target"] + langs + ["mean as source"],
                           [[s] + [f"{R[i, j]:.2f}" for j in range(len(langs))] +
                            [f"{np.nanmean(np.delete(R[i], i)):.2f}"] for i, s in enumerate(langs)]
                           + [["mean as target"] + [f"{np.nanmean(np.delete(R[:, j], j)):.2f}"
                                                    for j in range(len(langs))] + [""]]), ""]
        np.savetxt(d / f"matrix_{m}_acc.csv", M, delimiter=",", header=",".join(langs), fmt="%.2f", comments="")
        np.savetxt(d / f"matrix_{m}_relative.csv", R, delimiter=",", header=",".join(langs), fmt="%.4f", comments="")

        bad = [r for r in runs if r["method"] == m and r["collapsed"]]
        if bad:
            lines += [f"Collapsed runs (best dev acc < 0.3): " +
                      ", ".join(f"{r['src']} seed {r['seed']}" for r in bad), ""]

    if len(methods) == 2:
        a_m, b_m = methods
        lines += [f"## {b_m} minus {a_m}, in-language accuracy (percentage points)", ""]
        rows = []
        for l in langs:
            k = (l, l)
            if k in acc[a_m] and k in acc[b_m]:
                rows.append([l, f"{(np.mean(acc[b_m][k]) - np.mean(acc[a_m][k])) * 100:+.1f}"])
        lines += [md_table(["lang", "difference"], rows), ""]

    (d / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nWrote {d / 'summary.md'}")


if __name__ == "__main__":
    main()
