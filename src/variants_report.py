#!/usr/bin/env python3
"""Morfessor pre-segmentation against plain LoRA: in-language and zero-shot differences, NER and POS.

Compares results/<task>_morfessor (LoRA, words split into Morfessor morphemes) with the LoRA rows of
results/<task> (same model, seeds, hyperparameters; words fed whole). CIs are paired bootstraps over test
sentences (the same resampled sentences for both settings), pooled over languages and seeds.

    python src/morfessor_report.py

Writes results/<task>_morfessor/comparison.md and comparison.csv (also used by src/build_workbook.py).
"""
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

from sib200_report import BANTU, ORDER, md_table, read
from token_report import boot


def load(path, method="lora"):
    sc, it = defaultdict(list), defaultdict(list)
    for r in read(path):
        if r["method"] == method:
            sc[(r["src"], r["tgt"])].append(r["score"])
            it[(r["src"], r["tgt"])].append(r["items"])
    return sc, it


def compare(task, results=Path("results")):
    """In-language rows, pooled difference with CI, zero-shot group means and the per-cell difference matrix."""
    base_sc, base_it = load(results / task / "results.jsonl")
    seg_sc, seg_it = load(results / f"{task}_morfessor" / "results.jsonl")
    langs = [l for l in ORDER if (l, l) in seg_sc]
    stats = {r["lang"]: r for r in csv.DictReader(open(results / "morfessor_seg" / "stats.csv", encoding="utf-8"))}
    rows, diffs = [], []
    for l in langs:
        k = (l, l)
        b, s = np.mean(base_sc[k]) * 100, np.mean(seg_sc[k]) * 100
        dist = boot(task, seg_it[k]) - boot(task, base_it[k])
        diffs.append(dist)
        lo, hi = np.percentile(dist, [2.5, 97.5]) * 100
        rows.append(dict(task=task, lang=l, lora=b, lora_morfessor=s, difference=s - b, ci_lo=lo, ci_hi=hi,
                         tokens_per_word_before=float(stats[l]["tokens_per_word_before"]),
                         tokens_per_word_after=float(stats[l]["tokens_per_word_after"])))
    plo, phi = np.percentile(np.mean(diffs, axis=0) * 100, [2.5, 97.5])
    pooled = (np.mean([r["difference"] for r in rows]), plo, phi)

    def matrix(sc):
        return np.array([[np.mean(sc[(a, t)]) * 100 for t in langs] for a in langs])
    Mb, Ms = matrix(base_sc), matrix(seg_sc)
    off = ~np.eye(len(langs), dtype=bool)
    bantu = [i for i, l in enumerate(langs) if l in BANTU]
    other = [i for i, l in enumerate(langs) if l not in BANTU]

    def groups(M):
        return [M[off].mean(), np.mean([M[i, j] for i in bantu for j in bantu if i != j]),
                np.mean([M[i, j] for i in other for j in bantu])]
    zs = [[name, b, s, s - b] for name, b, s in zip(["all 30 cells", "Bantu -> Bantu", "amh/hau -> Bantu"],
                                                      groups(Mb), groups(Ms))]
    return dict(langs=langs, rows=rows, pooled=pooled, zero_shot=zs, diff=Ms - Mb)


def main():
    for task in ("ner", "pos"):
        c = compare(task)
        langs, d = c["langs"], Path(f"results/{task}_morfessor")
        name = "entity F1" if task == "ner" else "accuracy"
        point, lo, hi = c["pooled"]
        lines = [f"# {task.upper()}: Morfessor pre-segmentation vs plain LoRA", "",
                 "Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. "
                 f"Metric: {name} (%). Only the input differs: words split into Morfessor morphemes "
                 "(corpus weight 0.1, seen words only), vocabulary unchanged.", "",
                 "## In-language", "",
                 md_table(["lang", "LoRA", "LoRA + Morfessor", "difference", "95% CI (paired)",
                           "AfroXLMR tokens/word"],
                          [[r["lang"], f"{r['lora']:.1f}", f"{r['lora_morfessor']:.1f}", f"{r['difference']:+.1f}",
                            f"[{r['ci_lo']:+.1f}, {r['ci_hi']:+.1f}]",
                            f"{r['tokens_per_word_before']:.2f} -> {r['tokens_per_word_after']:.2f}"]
                           for r in c["rows"]]), "",
                 f"Pooled over {len(langs)} languages and all seeds: {point:+.1f} points, "
                 f"95% CI [{lo:+.1f}, {hi:+.1f}] (paired bootstrap over test sentences).", "",
                 "## Zero-shot transfer (off-diagonal)", "",
                 md_table(["cells", "LoRA", "LoRA + Morfessor", "difference"],
                          [[g, f"{b:.1f}", f"{s:.1f}", f"{x:+.1f}"] for g, b, s, x in c["zero_shot"]]), "",
                 "### Difference per cell (LoRA + Morfessor minus LoRA; rows = source, columns = target)", "",
                 md_table(["source \\ target"] + langs,
                          [[a] + [f"{c['diff'][i, j]:+.1f}" for j in range(len(langs))] for i, a in enumerate(langs)]),
                 ""]
        notes = d / "interpretation.md"
        if notes.exists():
            lines += ["## Interpretation", "", notes.read_text(encoding="utf-8").strip(), ""]
        (d / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        with open(d / "comparison.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(c["rows"][0]))
            w.writeheader()
            w.writerows({k: round(v, 3) if isinstance(v, float) else v for k, v in r.items()} for r in c["rows"])
        print("\n".join(lines))


if __name__ == "__main__":
    main()
