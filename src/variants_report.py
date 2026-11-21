#!/usr/bin/env python3
"""Tokenization variants against plain LoRA, NER and POS (WP1 methods b and c).

Every variant is LoRA r=8 on AfroXLMR-76L with the settings, seeds and trainable parameters of the LoRA
baseline in results/<task>; only the input side differs:
  morfessor        words split into Morfessor morphemes, each fed as its own word (extra word starts)
  morfessor_inner  Morfessor cuts kept inside words: subword pieces stop at morpheme boundaries, no extra word starts
  serengeti_fvt    Serengeti's tokenizer, embeddings moved into AfroXLMR by Fast Vocabulary Transfer (frozen)
CIs are paired bootstraps over test sentences (same resampled sentences for both settings), pooled over
languages and seeds.

    python src/variants_report.py

Writes results/<task>_<variant>/comparison.md and comparison.csv, results/variants_summary.md and
results/variants_tokens.csv (tokens per word for each variant; recomputed only if missing, needs the tokenizers).
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from sib200_report import BANTU, ORDER, md_table, read
from token_report import boot

VARIANTS = {"morfessor": "Morfessor, morphemes as separate words",
            "morfessor_inner": "Morfessor, cuts inside words",
            "serengeti_fvt": "Serengeti vocabulary (FVT)"}
METRIC = {"ner": "entity F1", "pos": "accuracy"}


def load(path, method="lora"):
    sc, it = defaultdict(list), defaultdict(list)
    for r in read(path):
        if r["method"] == method:
            sc[(r["src"], r["tgt"])].append(r["score"])
            it[(r["src"], r["tgt"])].append(r["items"])
    return sc, it


def available(task, results=Path("results")):
    return [v for v in VARIANTS if (results / f"{task}_{v}" / "results.jsonl").exists()]


def compare(task, variant, results=Path("results")):
    """In-language rows, pooled difference with CI, zero-shot group means and the per-cell difference matrix."""
    base_sc, base_it = load(results / task / "results.jsonl")
    var_sc, var_it = load(results / f"{task}_{variant}" / "results.jsonl")
    langs = [l for l in ORDER if (l, l) in var_sc]
    rows, diffs = [], []
    for l in langs:
        k = (l, l)
        b, s = np.mean(base_sc[k]) * 100, np.mean(var_sc[k]) * 100
        dist = boot(task, var_it[k]) - boot(task, base_it[k])
        diffs.append(dist)
        lo, hi = np.percentile(dist, [2.5, 97.5]) * 100
        rows.append(dict(task=task, variant=variant, lang=l, lora=b, variant_score=s, difference=s - b, ci_lo=lo, ci_hi=hi))
    plo, phi = np.percentile(np.mean(diffs, axis=0) * 100, [2.5, 97.5])
    pooled = (np.mean([r["difference"] for r in rows]), plo, phi)

    def matrix(sc):
        return np.array([[np.mean(sc[(a, t)]) * 100 for t in langs] for a in langs])
    Mb, Ms = matrix(base_sc), matrix(var_sc)
    off = ~np.eye(len(langs), dtype=bool)
    bantu = [i for i, l in enumerate(langs) if l in BANTU]
    other = [i for i, l in enumerate(langs) if l not in BANTU]

    def groups(M):
        return [M[off].mean(), np.mean([M[i, j] for i in bantu for j in bantu if i != j]),
                np.mean([M[i, j] for i in other for j in bantu])]
    zs = [[name, b, s, s - b] for name, b, s in zip(["all 30 cells", "Bantu -> Bantu", "amh/hau -> Bantu"],
                                                      groups(Mb), groups(Ms))]
    return dict(langs=langs, rows=rows, pooled=pooled, zero_shot=zs, diff=Ms - Mb)


def token_stats(results=Path("results"), raw=Path("data/raw")):
    """Tokens per word on the NER + POS training words for each variant, plus the share of Serengeti tokens (all
    words, and NER test entity words) that AfroXLMR lacks, i.e. whose vectors are FVT averages."""
    f = results / "variants_tokens.csv"
    if f.exists():
        return list(csv.DictReader(open(f, encoding="utf-8")))
    from transformers import AutoTokenizer
    from morfessor_segment import task_words
    from token_baseline import LANGS, inner_tokens, load_ner, split_word
    a = AutoTokenizer.from_pretrained("Davlan/afro-xlmr-large-76L")
    s = AutoTokenizer.from_pretrained("UBC-NLP/serengeti")
    av = a.get_vocab()
    out = []
    for l in LANGS:
        seg = json.loads((results / "morfessor_seg" / f"{l}.json").read_text(encoding="utf-8"))
        _, tw = task_words(l, raw)
        plain = word = inner = ser = new = 0
        for w in tw:
            p = split_word(w, seg.get(w.lower(), []))
            plain += len(a.tokenize(w))
            word += sum(len(a.tokenize(q)) for q in p)
            inner += len(a.tokenize(p[0]) + [t for q in p[1:] for t in inner_tokens(a, q, av)])
            t = s.tokenize(w)
            ser += len(t)
            new += sum(x not in av for x in t)
        ent = [x for ws, ts in load_ner(l, raw)["test"] for w, tag in zip(ws, ts) if tag != "O" for x in s.tokenize(w)]
        n = len(tw)
        out.append(dict(lang=l, afroxlmr=plain / n, morfessor=word / n, morfessor_inner=inner / n,
                        serengeti_fvt=ser / n, fvt_new_share=new / ser,
                        fvt_new_share_entities=sum(x not in av for x in ent) / len(ent)))
    with open(f, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows({k: round(v, 4) if isinstance(v, float) else v for k, v in r.items()} for r in out)
    return list(csv.DictReader(open(f, encoding="utf-8")))


def main():
    toks = {r["lang"]: r for r in token_stats()}
    summary = ["# Tokenization variants vs plain LoRA (NER and POS)", "",
               "All variants: LoRA r=8 on Davlan/afro-xlmr-large-76L, seeds 1-3, the settings and trainable parameters "
               "of the LoRA baseline; only the input differs. Differences in points; CIs are paired bootstraps over "
               "test sentences, pooled over 6 languages and seeds.", ""]
    pooled_rows = []
    per_lang = {}
    for task in ("ner", "pos"):
        name = METRIC[task]
        per_lang[task] = {}
        for v in available(task):
            c = compare(task, v)
            langs, d = c["langs"], Path(f"results/{task}_{v}")
            point, lo, hi = c["pooled"]
            pooled_rows.append([task.upper(), VARIANTS[v], f"{point:+.1f}", f"[{lo:+.1f}, {hi:+.1f}]",
                                f"{c['zero_shot'][0][3]:+.1f}"])
            per_lang[task][v] = c["rows"]
            lines = [f"# {task.upper()}: {VARIANTS[v]} vs plain LoRA", "",
                     "Model Davlan/afro-xlmr-large-76L, LoRA r=8, seeds 1-3, same hyperparameters. "
                     f"Metric: {name} (%). See src/variants_report.py for what the variant changes.", "",
                     "## In-language", "",
                     md_table(["lang", "LoRA", "variant", "difference", "95% CI (paired)", "tokens/word"],
                              [[r["lang"], f"{r['lora']:.1f}", f"{r['variant_score']:.1f}", f"{r['difference']:+.1f}",
                                f"[{r['ci_lo']:+.1f}, {r['ci_hi']:+.1f}]",
                                f"{float(toks[r['lang']]['afroxlmr']):.2f} -> {float(toks[r['lang']][v]):.2f}"]
                               for r in c["rows"]]), "",
                     f"Pooled over {len(langs)} languages and all seeds: {point:+.1f} points, "
                     f"95% CI [{lo:+.1f}, {hi:+.1f}] (paired bootstrap over test sentences).", "",
                     "## Zero-shot transfer (off-diagonal)", "",
                     md_table(["cells", "LoRA", "variant", "difference"],
                              [[g, f"{b:.1f}", f"{s:.1f}", f"{x:+.1f}"] for g, b, s, x in c["zero_shot"]]), "",
                     "### Difference per cell (variant minus LoRA; rows = source, columns = target)", "",
                     md_table(["source \\ target"] + langs,
                              [[a] + [f"{c['diff'][i, j]:+.1f}" for j in range(len(langs))]
                               for i, a in enumerate(langs)]), ""]
            notes = d / "interpretation.md"
            if notes.exists():
                lines += ["## Interpretation", "", notes.read_text(encoding="utf-8").strip(), ""]
            (d / "comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
            with open(d / "comparison.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(c["rows"][0]))
                w.writeheader()
                w.writerows({k: round(x, 3) if isinstance(x, float) else x for k, x in r.items()} for r in c["rows"])

    summary += ["## Pooled", "",
                md_table(["task", "variant", "in-language difference", "95% CI", "zero-shot difference (30 cells)"],
                         pooled_rows), ""]
    for task in ("ner", "pos"):
        vs = list(per_lang[task])
        base = {r["lang"]: r["lora"] for r in per_lang[task][vs[0]]}
        summary += [f"## {task.upper()} per language: plain LoRA {METRIC[task]} and each variant's difference", "",
                    md_table(["lang", "LoRA"] + [VARIANTS[v] for v in vs],
                             [[l, f"{base[l]:.1f}"] + [f"{next(r['difference'] for r in per_lang[task][v] if r['lang'] == l):+.1f}"
                                                        for v in vs] for l in base]), ""]
    summary += ["## Tokens per word (NER + POS training words)", "",
                md_table(["lang", "AfroXLMR", "Morfessor, separate words", "Morfessor, inside words", "Serengeti",
                          "Serengeti tokens new to AfroXLMR", "same, NER test entity words"],
                         [[l, *(f"{float(t[k]):.2f}" for k in ("afroxlmr", "morfessor", "morfessor_inner", "serengeti_fvt")),
                           f"{float(t['fvt_new_share']):.0%}", f"{float(t['fvt_new_share_entities']):.0%}"]
                          for l, t in toks.items()]), ""]
    notes = Path("results/variants_interpretation.md")
    if notes.exists():
        summary += ["## Interpretation", "", notes.read_text(encoding="utf-8").strip(), ""]
    Path("results/variants_summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
