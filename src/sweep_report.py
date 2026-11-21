#!/usr/bin/env python3
"""LoRA sweep on Swahili dev: pick one LoRA setting per task before any further runs.

Reads results/sweep/<task>/<config>/runs.jsonl (from src/token_baseline.py with --no_test, so the test sets are never
looked at). Configs: rank r = 8, 16, 32 crossed with targets qv (attention query and value, the current baseline) or
all (every linear layer). Seed 1, Swahili only, up to 20 epochs with early stopping on dev.

Selection rule, fixed before the sweep: the highest dev score wins, but any config within TOL points of it counts as
a tie, and among ties the one with the fewest trainable parameters is chosen (cheaper is better for G7).

    python src/sweep_report.py [--dir results/sweep]

Writes results/sweep/summary.md and results/sweep/chosen.json.
"""
import argparse
import json
from pathlib import Path

from sib200_report import md_table, read

TOL = 0.3  # points of dev F1 / accuracy; one seed cannot separate smaller differences


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="results/sweep")
    d = Path(ap.parse_args().dir)
    lines = ["# LoRA sweep (Swahili dev, seed 1)", "",
             f"Rule: highest dev score; configs within {TOL} points count as tied, and the tie with the fewest trainable "
             "parameters wins. Test sets were not evaluated.", ""]
    chosen = {}
    for task in ("ner", "pos"):
        runs = [r for f in sorted((d / task).glob("*/runs.jsonl")) for r in read(f)]
        if not runs:
            continue
        top = max(r["best_dev"] for r in runs)
        ties = [r for r in runs if r["best_dev"] >= top - TOL / 100]
        pick = min(ties, key=lambda r: r["n_trainable"])
        chosen[task] = dict(lora_r=pick["lora_r"], lora_targets=pick["lora_targets"], dev=pick["best_dev"],
                            best_epoch=pick["best_epoch"], epochs_run=pick["epochs_run"])
        rows = [[f"r={r['lora_r']}", r["lora_targets"], f"{100 * r['best_dev']:.2f}", f"{r['trainable_pct']:.2f}",
                 r["best_epoch"], r["epochs_run"], f"{r['seconds'] / 60:.1f}", f"{r['peak_mem_gb'] or 0:.1f}",
                 "chosen" if r is pick else ("tied" if r in ties else "")]
                for r in sorted(runs, key=lambda r: (r["lora_targets"], r["lora_r"]))]
        metric = "entity F1" if task == "ner" else "accuracy"
        lines += [f"## {task.upper()}", "",
                  md_table(["rank", "targets", f"dev {metric} %", "trainable %", "best epoch", "epochs run", "minutes",
                            "peak GPU GB", ""], rows), ""]
        late = [r for r in runs if r["best_epoch"] == r["epochs_run"] and r["epochs_run"] == r["epochs"]]
        if late:
            lines += [f"Warning: {len(late)} config(s) were still improving at the last allowed epoch.", ""]
    (d / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (d / "chosen.json").write_text(json.dumps(chosen, indent=2), encoding="utf-8")
    print("\n".join(lines))
    print(json.dumps(chosen, indent=2))


if __name__ == "__main__":
    main()
