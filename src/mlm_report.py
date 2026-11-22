#!/usr/bin/env python3
"""Serengeti vocabulary + masked-LM step against its control, AfroXLMR + the same masked-LM step (RQ1, option B).

Both models get the same embedding-only masked-LM pass (src/mlm_adapt.py: same text, steps and settings) and are
then fine-tuned with the tuned LoRA from the sweep (results/sweep/chosen.json), seeds 1-3, kin lug swa zul. The
only difference is the vocabulary, so their difference is the effect of the vocabulary once its embeddings have
been trained. If the converged LoRA baseline (results/<task>_conv) exists, the control is also compared with it,
which isolates the masked-LM pass itself.

    python src/mlm_report.py

Writes results/<task>_serengeti_mlm/comparison.md and .csv and results/mlm_summary.md.
CIs bootstrap test sentences (paired) and seeds, as in src/variants_report.py.
"""
import csv
import json
from pathlib import Path

from sib200_report import md_table
from variants_report import METRIC, compare

R = Path("results")
PAIRS = [("serengeti_mlm", "afroxlmr_mlm", "Serengeti vocabulary + MLM vs AfroXLMR + MLM (vocabulary effect)"),
         ("afroxlmr_mlm", "conv", "AfroXLMR + MLM vs converged LoRA baseline (masked-LM effect)")]


def section(task, variant, base, title):
    c = compare(task, variant, base=f"{task}_{base}")
    langs, (point, lo, hi) = c["langs"], c["pooled"]
    zs_all, zs_bantu = c["zero_shot"][0], c["zero_shot"][1]
    lines = [f"## {task.upper()}: {title}", "",
             md_table(["lang", base, variant, "difference", "95% CI (sentences + seeds)"],
                      [[r["lang"], f"{r['lora']:.1f}", f"{r['variant_score']:.1f}", f"{r['difference']:+.1f}",
                        f"[{r['ci_lo']:+.1f}, {r['ci_hi']:+.1f}]"] for r in c["rows"]]), "",
             f"Pooled over {len(langs)} languages: {point:+.1f} points, 95% CI [{lo:+.1f}, {hi:+.1f}].", "",
             f"Zero-shot, all {len(langs) * (len(langs) - 1)} transfer cells: {zs_all[1]:.1f} -> {zs_all[2]:.1f} "
             f"({zs_all[3]:+.1f}).", "",
             "Difference per transfer cell (rows = source, columns = target):", "",
             md_table(["source \\ target"] + langs,
                      [[a] + ["" if i == j else f"{c['diff'][i, j]:+.1f}" for j in range(len(langs))]
                       for i, a in enumerate(langs)]), ""]
    return lines, c, [task.upper(), title, f"{point:+.1f}", f"[{lo:+.1f}, {hi:+.1f}]", f"{zs_all[3]:+.1f}"]


def main():
    chosen = json.loads((R / "sweep" / "chosen.json").read_text())
    out = ["# Serengeti vocabulary with the masked-LM step (NER and POS)", "",
           "Tuned LoRA from the sweep (NER r={} {}, POS r={} {}), seeds 1-3, kin lug swa zul, up to 20 epochs with "
           "early stopping. Differences in points; CIs bootstrap test sentences (paired) and seeds.".format(
               chosen["ner"]["lora_r"], chosen["ner"]["lora_targets"], chosen["pos"]["lora_r"],
               chosen["pos"]["lora_targets"]), ""]
    pooled, body = [], []
    for task in ("ner", "pos"):
        for variant, base, title in PAIRS:
            if not all((R / f"{task}_{x}" / "results.jsonl").exists() for x in (variant, base)):
                continue
            lines, c, row = section(task, variant, base, title)
            body += lines
            pooled.append(row)
            if variant == "serengeti_mlm":
                d = R / f"{task}_{variant}"
                (d / "comparison.md").write_text("\n".join([f"# {task.upper()}: {title}", "",
                                                            f"Metric: {METRIC[task]} (%).", ""] + lines[2:]) + "\n",
                                                 encoding="utf-8")
                with open(d / "comparison.csv", "w", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=list(c["rows"][0]))
                    w.writeheader()
                    w.writerows({k: round(x, 3) if isinstance(x, float) else x for k, x in r.items()} for r in c["rows"])
    mlm = []
    for m in ("serengeti_mlm", "afroxlmr_mlm"):
        f = R / f"ner_{m}" / "mlm_stats.json"
        if f.exists():
            s = json.loads(f.read_text())
            mlm.append([m] + [f"{s['heldout_loss_before'][l]:.2f} -> {s['heldout_loss_after'][l]:.2f}"
                              for l in s["heldout_loss_after"]])
            langs = list(s["heldout_loss_after"])
    out += ["## Pooled", "", md_table(["task", "comparison", "in-language difference", "95% CI",
                                       "zero-shot difference"], pooled), "",
            "## Masked-LM pass: held-out loss before -> after (embedding-only, 3,000 steps of 32 blocks)", "",
            md_table(["model"] + langs, mlm), "",
            "Losses are per predicted token, and the two vocabularies cut text differently, so the two rows are not "
            "directly comparable; the gap is still large.", ""] + body
    notes = R / "mlm_interpretation.md"
    if notes.exists():
        out += ["## Interpretation", "", notes.read_text(encoding="utf-8").strip(), ""]
    (R / "mlm_summary.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("wrote", R / "mlm_summary.md")


if __name__ == "__main__":
    main()
