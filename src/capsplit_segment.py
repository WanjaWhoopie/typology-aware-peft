#!/usr/bin/env python3
"""Capital-split tables: cut isiZulu words of the form prefix + Capital (uKaunda, eGoli, ngeSonto) at the capital.

Why: about a third of isiZulu NER entity words have a lowercase noun-class or locative prefix written before a
capitalised name; none of our other languages do (0 of the entity words in the kin, lug, swa, hau test sets). A
model trained on those languages only ever sees names start a word, while AfroXLMR splits uKaunda as '▁u Ka unda',
so in isiZulu the name starts mid-word. Splitting at the capital ('u' + 'Kaunda', each its own word, with
token_baseline.py --seg_mode word) makes isiZulu names look like the names the source languages have.

Keys keep the original case (only words that really contain the prefix-capital pattern are split; token_baseline
looks up the exact form first). Languages with no such words get an empty table.

    python src/capsplit_segment.py
    python src/token_baseline.py --task ner --methods lora --segment results/capsplit_seg --seg_mode word \\
        --out results/ner_capsplit

Writes results/capsplit_seg/<lang>.json and stats.csv.
"""
import argparse
import csv
import json
import re
from pathlib import Path

from token_baseline import LANGS, load_ner, load_pos

PREFIX_CAP = re.compile(r"^([a-z]{1,4})([A-Z])")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--langs", nargs="+", default=LANGS)
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--out", default="results/capsplit_seg")
    args = ap.parse_args()
    raw, out = Path(args.raw), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stats = []
    for lang in args.langs:
        words, ent, ent_split = set(), 0, 0
        for loader in (load_ner, load_pos):
            for split, sents in loader(lang, raw).items():
                for ws, tags in sents:
                    words.update(ws)
                    if loader is load_ner and split == "test":
                        for w, t in zip(ws, tags):
                            if t != "O":
                                ent += 1
                                ent_split += bool(PREFIX_CAP.match(w))
        table = {w: [len(m.group(1))] for w in sorted(words) if (m := PREFIX_CAP.match(w))}
        (out / f"{lang}.json").write_text(json.dumps(table, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        stats.append(dict(lang=lang, word_types_split=len(table), word_types=len(words),
                          ner_test_entity_words=ent, ner_test_entity_words_split=ent_split))
        print(f"{lang}: {len(table):,} word types split; NER test entity words split {ent_split} of {ent}", flush=True)
    with open(out / "stats.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(stats[0]))
        w.writeheader()
        w.writerows(stats)


if __name__ == "__main__":
    main()
