#!/usr/bin/env python3
"""Morpheme pre-segmentation tables for the NER and POS data (WP1 method b: split words, keep the vocabulary).

For each language, train Morfessor Baseline on raw text (same recipe as src/morfessor_silver.py) and segment the
words of MasakhaNER / MasakhaPOS / UD Amharic. Corpus weight 0.1: on isiZulu gold it has the same F1 as the best
weight (0.444 vs 0.451 on test words) but higher precision (0.51 vs 0.42), and wrong cuts matter more than missed
ones when the model has to read the pieces; 0.03 cut most words into syllables. No gold exists to tune the other
languages. Only words seen in Morfessor's training word list are split; unseen words (mostly names, e.g.
'bi-ra-zi-l') would otherwise be cut into syllables. Output: results/morfessor_seg/<lang>.json, mapping a
lowercased word to its morpheme cut offsets ('aseduzane' -> [1, 3, 6, 8]); unsplit words are left out.
src/token_baseline.py --segment results/morfessor_seg then feeds each morpheme to the tokenizer separately.

    python src/morfessor_segment.py

Also writes results/morfessor_seg/stats.csv: morphemes per word, and AfroXLMR tokens per word with and without
pre-segmentation (on the NER + POS training words).
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import morfessor
from transformers import AutoTokenizer

from morfessor_silver import WORD, cuts, train, word_counts
from token_baseline import LANGS, load_ner, load_pos, split_word


def task_words(lang, raw):
    """Every word in the NER and POS data of one language, with the training-split words counted separately."""
    words, train_words = set(), []
    for loader in (load_ner, load_pos):
        for split, sents in loader(lang, raw).items():
            for ws, _ in sents:
                words.update(ws)
                if split == "train":
                    train_words += ws
    return words, train_words


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--langs", nargs="+", default=LANGS)
    ap.add_argument("--weight", type=float, default=0.1)
    ap.add_argument("--max_types", type=int, default=100_000)
    ap.add_argument("--model", default="Davlan/afro-xlmr-large-76L", help="tokenizer for the before/after counts")
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--processed", default="data/processed")
    ap.add_argument("--out", default="results/morfessor_seg")
    args = ap.parse_args()
    raw, proc, out = Path(args.raw), Path(args.processed), Path(args.out)
    proc.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(args.model)
    io = morfessor.MorfessorIO()

    stats = []
    for lang in args.langs:
        f = proc / f"morfessor_seg_{lang}_{args.weight}.bin"
        full, counts = word_counts(lang, raw, args.max_types)
        if f.exists():
            m = io.read_binary_model_file(str(f))
        else:
            m = train(counts, args.weight)
            io.write_binary_model_file(str(f), m)
        words, train_words = task_words(lang, raw)
        table = {}
        for w in sorted({w.lower() for w in words}):
            if WORD.fullmatch(w) and w in counts:  # unseen words (mostly names) would be cut into syllables
                c = sorted(cuts(m, w))
                if c:
                    table[w] = c
        (out / f"{lang}.json").write_text(json.dumps(table, ensure_ascii=False, sort_keys=True), encoding="utf-8")

        n_morph = sum(len(table.get(w.lower(), [])) + 1 for w in train_words)
        before = sum(len(tok.tokenize(w)) for w in train_words)
        after = sum(len(tok.tokenize(p)) for w in train_words for p in split_word(w, table.get(w.lower(), [])))
        row = dict(lang=lang, corpus_words=sum(full.values()), train_types=len(counts), weight=args.weight,
                   task_word_types=len(words), types_split=len(table), train_tokens=len(train_words),
                   morphs_per_word=n_morph / len(train_words), tokens_per_word_before=before / len(train_words),
                   tokens_per_word_after=after / len(train_words))
        stats.append(row)
        print(f"{lang}: corpus {row['corpus_words']:,} words; {len(table):,} of {len(words):,} task word types split; "
              f"{row['morphs_per_word']:.2f} morphemes/word; AfroXLMR tokens/word {row['tokens_per_word_before']:.2f}"
              f" -> {row['tokens_per_word_after']:.2f}", flush=True)

    with open(out / "stats.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(stats[0]))
        w.writeheader()
        w.writerows(stats)


if __name__ == "__main__":
    main()
