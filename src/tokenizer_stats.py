#!/usr/bin/env python3
"""Fragmentation study: how finely do existing tokenizers split our six languages? No GPU, no training.

Text: SIB-200 sentences (train + validation + test, 1,004 per language). They are FLORES sentences, so every
language has the same content, which makes tokens per sentence comparable across languages. English is
included as the reference for the token premium.

Per tokenizer and language:
  fertility        subword tokens per whitespace word
  continued_words  share of words split into 2 or more tokens (Rust et al., 2021)
  chars_per_token  characters (without spaces) per token
  unk_rate         share of tokens that are the unknown token
  premium          tokens per sentence / English tokens per sentence, same tokenizer (Petrov et al., 2023)
  renyi_eff        Renyi efficiency, alpha 2.5, of the token distribution (Zouhar et al., 2023)
Morpheme boundaries, for languages with gold surface segmentations (isiZulu only so far: NCHLT annotations as
prepared by Moeng et al., 2021, 11k unique words; none found for swa, kin, lug):
  boundary_p/r/f1  token boundaries inside a word vs gold morpheme boundaries, micro-averaged over words
  exact_match      share of words whose token boundaries equal the gold boundaries exactly

    python src/tokenizer_stats.py
    python src/tokenizer_stats.py --tokenizers Davlan/afro-xlmr-large-76L UBC-NLP/serengeti

Gated tokenizers (Llama, Gemma, InkubaLM) need `huggingface-cli login` and accepted terms; the ones that
fail to load are listed in the summary and skipped.
Writes results/tokenizers/{stats.csv,boundaries.csv,summary.md}.
"""
import argparse
import csv
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np
from datasets import load_dataset
from transformers import AutoTokenizer

LANGS = {"amh": "amh_Ethi", "hau": "hau_Latn", "kin": "kin_Latn", "lug": "lug_Latn",
         "swa": "swh_Latn", "zul": "zul_Latn", "eng": "eng_Latn"}
TOKENIZERS = {  # name -> (repo, note)
    "AfroXLMR-76L": ("Davlan/afro-xlmr-large-76L", "same vocabulary as XLM-R"),
    "Serengeti": ("UBC-NLP/serengeti", ""),
    "AfriBERTa": ("castorini/afriberta_large", ""),
    "BantuBERTa": ("dsfsi/BantuBERTa", ""),
    "mBERT": ("google-bert/bert-base-multilingual-cased", ""),
    "mT5": ("google/mt5-base", ""),
    "InkubaLM": ("lelapa/InkubaLM-0.4B", "gated"),
    "Llama-3.1": ("meta-llama/Llama-3.1-8B", "gated"),
    "Gemma-2": ("google/gemma-2-2b", "gated"),
}
GOLD = {"zul": "https://raw.githubusercontent.com/TumiMoeng/MORPH_SEGMENT/main/Sequence%20to%20Sequence/Data/zulu/"
               "zulu.clean.{}.conll"}  # word | surface segmentation (a-se-duz-an-e) | ... ; MIT, data from NCHLT


def load_gold(lang, raw):
    """Unique words with their gold boundary offsets, e.g. 'aseduzane' -> {1, 3, 6, 8}."""
    words = {}
    for split in ("train", "dev", "test"):
        f = raw / f"morph_{lang}" / f"{lang}.{split}.conll"
        if not f.exists():
            f.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(GOLD[lang].format(split), f)
        for line in f.read_text(encoding="utf-8").splitlines():
            word, seg = line.split(" | ")[:2]
            if word.lower() != seg.replace("-", "").lower() or word in words:
                continue  # 1 to 2% of entries do not join back to the word
            cuts = np.cumsum([len(m) for m in seg.split("-")])[:-1]
            words[word] = set(cuts.tolist())
    return words


def token_cuts(tok, word):
    """Boundary offsets between the tokens of a word, or None if the pieces do not spell the word."""
    pieces = [p.lstrip("▁Ġ").removeprefix("##") for p in word_pieces(tok, word)]
    pieces = [p for p in pieces if p]
    if "".join(pieces) != word:
        return None
    return set(np.cumsum([len(p) for p in pieces])[:-1].tolist())


def load_tokenizer(repo):
    try:
        return AutoTokenizer.from_pretrained(repo)
    except Exception:  # some sentencepiece tokenizers only load as the slow version
        return AutoTokenizer.from_pretrained(repo, use_fast=False)


def word_pieces(tok, word):
    """Tokens for one word as it appears after a space inside a sentence."""
    byte_bpe = "Ġ" in "".join(tok.tokenize(" a"))  # GPT-2 style tokenizers mark the leading space
    return tok.tokenize(" " + word if byte_bpe else word)


def renyi_efficiency(counts, vocab_size, alpha=2.5):
    p = np.array(list(counts.values()), dtype=float)
    p /= p.sum()
    return float(np.log((p ** alpha).sum()) / (1 - alpha) / np.log(vocab_size))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokenizers", nargs="+", default=list(TOKENIZERS),
                    help="names from the list above or Hugging Face repos")
    ap.add_argument("--out", default="results/tokenizers")
    ap.add_argument("--raw", default="data/raw")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    gold = {l: load_gold(l, Path(args.raw)) for l in GOLD}
    brows = []

    text = {}
    for l, cfg in LANGS.items():
        d = load_dataset("Davlan/sib200", cfg)
        text[l] = [s for split in ("train", "validation", "test") for s in d[split]["text"]]

    rows, failed = [], []
    for name in args.tokenizers:
        repo, note = TOKENIZERS.get(name, (name, ""))
        try:
            tok = load_tokenizer(repo)
        except Exception as e:
            failed.append((name, repo, type(e).__name__))
            print(f"{name}: could not load ({type(e).__name__})", flush=True)
            continue
        cache = {}
        per_lang = {}
        for l, sents in text.items():
            n_tok = n_words = n_cont = n_chars = n_unk = 0
            counts = Counter()
            for s in sents:
                for w in s.split():
                    if w not in cache:
                        cache[w] = word_pieces(tok, w)
                    p = cache[w]
                    n_tok += len(p); n_words += 1; n_cont += len(p) > 1; n_chars += len(w)
                    n_unk += sum(x == tok.unk_token for x in p)
                    counts.update(p)
            per_lang[l] = dict(tokens=n_tok, words=n_words, sentences=len(sents),
                               fertility=n_tok / n_words, continued_words=n_cont / n_words,
                               chars_per_token=n_chars / n_tok, unk_rate=n_unk / n_tok,
                               renyi_eff=renyi_efficiency(counts, len(tok)))
        eng = per_lang["eng"]["tokens"] / per_lang["eng"]["sentences"]
        for l, r in per_lang.items():
            rows.append(dict(tokenizer=name, repo=repo, algorithm=type(tok).__name__, vocab=len(tok), lang=l,
                             premium=r["tokens"] / r["sentences"] / eng, note=note, **r))
        for l, words in gold.items():
            tp = n_tok = n_gold = exact = used = 0
            for w, g in words.items():
                t = token_cuts(tok, w)
                if t is None:
                    continue
                used += 1; tp += len(t & g); n_tok += len(t); n_gold += len(g); exact += t == g
            p, r_ = tp / max(n_tok, 1), tp / max(n_gold, 1)
            chance = sum(len(g) for g in words.values()) / sum(len(w) - 1 for w in words)
            brows.append(dict(tokenizer=name, lang=l, words=len(words), words_scored=used, chance_p=chance, boundary_p=p,
                              boundary_r=r_, boundary_f1=2 * p * r_ / max(p + r_, 1e-9), exact_match=exact / max(used, 1),
                              tokens_per_word=(n_tok + used) / max(used, 1),
                              morphemes_per_word=(n_gold + used) / max(used, 1)))
        print(f"{name}: done", flush=True)

    fields = ["tokenizer", "repo", "algorithm", "vocab", "lang", "sentences", "words", "tokens", "fertility",
              "continued_words", "chars_per_token", "unk_rate", "premium", "renyi_eff", "note"]
    with open(out / "stats.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    with open(out / "boundaries.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(brows[0]))
        w.writeheader()
        w.writerows(brows)

    names = list(dict.fromkeys(r["tokenizer"] for r in rows))
    langs = list(LANGS)
    get = {(r["tokenizer"], r["lang"]): r for r in rows}
    lines = ["# Tokenizer fragmentation study", "",
             "Text: SIB-200 (FLORES) sentences, 1,004 per language, the same content in every language. "
             "Words are whitespace-separated; each word is tokenized as it appears after a space.", ""]
    for key, label, fmt in [("fertility", "Fertility (tokens per word, lower = less splitting)", "{:.2f}"),
                            ("continued_words", "Continued words (% of words split into 2+ tokens)", "{:.0%}"),
                            ("premium", "Token premium (tokens per sentence / English, same tokenizer)", "{:.2f}"),
                            ("renyi_eff", "Renyi efficiency (alpha 2.5, higher = more even use of the vocabulary)",
                             "{:.3f}"),
                            ("unk_rate", "Unknown-token rate", "{:.2%}")]:
        lines += [f"## {label}", "", "| tokenizer | vocab | " + " | ".join(langs) + " |",
                  "|---|---|" + "---|" * len(langs)]
        for n in names:
            lines.append(f"| {n} | {get[(n, 'eng')]['vocab']:,} | " +
                         " | ".join(fmt.format(get[(n, l)][key]) for l in langs) + " |")
        lines.append("")
    lines += ["## Morpheme boundaries (gold surface segmentation)", "",
              "| tokenizer | lang | words scored | boundary precision | boundary recall | boundary F1 | exact match "
              "| tokens/word | morphemes/word |", "|---|---|---|---|---|---|---|---|---|"]
    lines += [f"| {b['tokenizer']} | {b['lang']} | {b['words_scored']:,} of {b['words']:,} | {b['boundary_p']:.2f} | "
              f"{b['boundary_r']:.2f} | {b['boundary_f1']:.2f} | {b['exact_match']:.0%} | {b['tokens_per_word']:.2f} | "
              f"{b['morphemes_per_word']:.2f} |" for b in brows]
    lines += ["", "Precision: share of token boundaries that are morpheme boundaries. Recall: share of morpheme "
              "boundaries the tokenizer also cuts at. Words whose pieces do not spell the word (byte-level pieces, "
              "unknown tokens) are not scored.", ""]
    lines += [f"Chance precision ({b['lang']}): {b['chance_p']:.2f}, the share of positions inside a word that are "
              "morpheme boundaries, i.e. the precision of cutting at random." for b in brows if b["tokenizer"] == names[0]]
    lines += [""]
    if failed:
        lines += ["Not loaded (gated or broken): " + ", ".join(f"{n} (`{r}`, {e})" for n, r, e in failed), ""]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
