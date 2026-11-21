#!/usr/bin/env python3
"""Scrambled-cut control for the Morfessor variants: same words, same number of cuts per word, random positions.

If Morfessor's cuts help (or hurt) because they fall on morpheme boundaries, the scrambled tables should behave
differently; if it is only the number of pieces that matters, they should behave the same. Design follows the
scrambled-control preprints (Antall & Saha 2026, Amharic/Hausa and Tagalog).

For every word in results/morfessor_seg/<lang>.json with k cuts, k distinct cut positions are drawn uniformly from
1 .. len(word) - 1, seeded per word, so the tables are reproducible. Words Morfessor left whole stay whole.

    python src/scramble_segment.py
    python src/token_baseline.py --task ner --methods lora --segment results/morfessor_scrambled_seg \\
        --seg_mode inner --out results/ner_morfessor_scrambled

Writes results/morfessor_scrambled_seg/<lang>.json and stats.csv (with the share of scrambled cuts that happen to
coincide with Morfessor's, i.e. chance agreement).
"""
import argparse
import csv
import json
import random
import zlib
from pathlib import Path


def scramble(word, cuts, seed=0):
    n = len(word)
    k = min(len(cuts), n - 1)
    rng = random.Random(zlib.crc32(f"{seed}:{word}".encode("utf-8")))
    return sorted(rng.sample(range(1, n), k))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default="results/morfessor_seg")
    ap.add_argument("--out", default="results/morfessor_scrambled_seg")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    src, out = Path(args.src), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stats = []
    for f in sorted(src.glob("*.json")):
        table = json.loads(f.read_text(encoding="utf-8"))
        new = {w: scramble(w, c, args.seed) for w, c in table.items()}
        same = sum(len(set(c) & set(new[w])) for w, c in table.items())
        total = sum(len(c) for c in table.values())
        (out / f.name).write_text(json.dumps(new, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        stats.append(dict(lang=f.stem, words=len(table), cuts=total, cuts_matching_morfessor=same,
                          share_matching=round(same / max(total, 1), 4)))
        print(f"{f.stem}: {len(table):,} words, {total:,} cuts, {same / max(total, 1):.0%} land on a Morfessor cut by chance")
    with open(out / "stats.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(stats[0]))
        w.writeheader()
        w.writerows(stats)


if __name__ == "__main__":
    main()
