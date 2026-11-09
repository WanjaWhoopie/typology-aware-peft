#!/usr/bin/env python3
"""Build results/results.xlsx: every number in the project in one workbook, one tab per topic.

    python src/build_workbook.py

Rebuild after any new run; the workbook is generated, so never edit it by hand. Hand-curated content
(tokenizer availability, literature numbers) lives in the lists below. The .md files stay as interpretation.
Tabs: README, Tokenizer availability, Tokenizer stats, SIB-200, NER, POS, Luganda diagnostics, Literature, Runs.
"""
import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from sib200_report import BANTU, ORDER, read
from token_report import boot

R = Path("results")
FONT, BOLD, TITLE = Font(name="Arial", size=10), Font(name="Arial", size=10, bold=True), Font(name="Arial", size=12, bold=True)
HEAD = PatternFill("solid", start_color="D9E1F2")

# --- hand-curated: which languages each tokenizer was trained for -------------------------------------------
AVAILABILITY = [  # tokenizer, repo, algorithm, vocab, trained for, amh, hau, kin, lug, swa, zul, source, checked
    ["AfroXLMR-76L (our model)", "Davlan/afro-xlmr-large-76L", "SentencePiece Unigram", 250002,
     "XLM-R's 100 languages (CC100). Vocabulary identical to XLM-R: the model was further trained on 76 languages "
     "incl. all six, but the tokenizer was not changed", "yes", "yes", "no", "no", "yes", "no",
     "tokenizer_config + vocabulary compared with FacebookAI/xlm-roberta-large; XLM-R language list from memory",
     "2026-11-09"],
    ["Serengeti", "UBC-NLP/serengeti", "SentencePiece (XLM-R format)", 250004,
     "517 African languages; own vocabulary (59k of 250k pieces shared with XLM-R)",
     "yes", "yes", "yes", "yes", "yes", "yes", "model card (tags am ha lg sw zu; Kinyarwanda in card text)", "2026-11-09"],
    ["AfriBERTa", "castorini/afriberta_large", "SentencePiece Unigram", 70005,
     "11 African languages: Oromo, Amharic, Gahuza (Kinyarwanda + Kirundi), Hausa, Igbo, Pidgin, Somali, Swahili, "
     "Tigrinya, Yoruba", "yes", "yes", "yes (Gahuza)", "no", "yes", "no", "model card", "2026-11-09"],
    ["BantuBERTa", "dsfsi/BantuBERTa", "byte-level BPE", 70000, "15 Bantu languages (+ Oromo)",
     "no", "no", "yes", "yes", "yes", "yes", "model card (tags sw rw zu lg); Parvess 2023", "2026-11-09"],
    ["mBERT", "google-bert/bert-base-multilingual-cased", "WordPiece", 119547, "104 Wikipedia languages",
     "no (95% unknown tokens)", "no", "no", "no", "yes", "no",
     "Wikipedia language list from memory; Amharic confirmed by unknown-token rate", "2026-11-09"],
    ["mT5", "google/mt5-base", "SentencePiece Unigram", 250100, "101 mC4 languages",
     "yes", "yes", "no?", "no", "yes", "yes", "mC4 language list from memory: verify", ""],
    ["InkubaLM", "lelapa/InkubaLM-0.4B", "not loaded (gated)", None,
     "Swahili, isiZulu, Hausa, Yoruba, Igbo + English, French (from memory)",
     "no?", "yes?", "no?", "no?", "yes?", "yes?", "from memory; accept terms on Hugging Face to measure", ""],
    ["Llama-3.1", "meta-llama/Llama-3.1-8B", "byte-level BPE", 128256, "general multilingual",
     "", "", "", "", "", "", "gated: accept terms on Hugging Face to measure", ""],
    ["Gemma-2", "google/gemma-2-2b", "SentencePiece BPE", 256000, "general multilingual",
     "", "", "", "", "", "", "gated: accept terms on Hugging Face to measure", ""],
    ["KinyaBERT", "anzeyimana/kinyabert-acl2022", "morphological analyser + BPE", None,
     "Kinyarwanda only (morpheme-aware)", "no", "no", "yes", "no", "no", "no",
     "Nzeyimana & Rubungo 2022; analyser availability not checked", ""],
]

# --- hand-curated: numbers reported in papers (state of the art) -------------------------------------------
# paper, year, language, tokenizer, algorithm, vocab, model / classifier, task, dataset, metric, score,
# intrinsic metrics reported, comparable to ours, where in paper, checked
P23 = ("Parvess 2023 (BantuBERTa)", 2023)
P24 = ("Ndomba & Jeong 2024", 2024)
P25 = ("Ndomba, Mswahili & Jeong 2025", 2025)
LIT = [
    [*P23, "swa", "BantuBERTa", "BPE", 70000, "BantuBERTa (fine-tuned)", "NER", "MasakhaNER", "F1", 85.0, "none", "partly (same task, older data, single run)", "results table", "AI-drafted"],
    [*P23, "kin", "BantuBERTa", "BPE", 70000, "BantuBERTa (fine-tuned)", "NER", "MasakhaNER", "F1", 69.4, "none", "partly", "results table", "AI-drafted"],
    [*P23, "lug", "BantuBERTa", "BPE", 70000, "BantuBERTa (fine-tuned)", "NER", "MasakhaNER", "F1", 73.0, "none", "partly", "results table", "AI-drafted"],
    [*P23, "swa", "XLM-R", "SentencePiece Unigram", 250002, "XLM-R base (fine-tuned)", "NER", "MasakhaNER", "F1", 87.4, "none", "partly", "results table (copied from other papers)", "AI-drafted"],
    [*P23, "kin", "XLM-R", "SentencePiece Unigram", 250002, "XLM-R base (fine-tuned)", "NER", "MasakhaNER", "F1", 73.9, "none", "partly", "results table (copied from other papers)", "AI-drafted"],
    [*P23, "lug", "XLM-R", "SentencePiece Unigram", 250002, "XLM-R base (fine-tuned)", "NER", "MasakhaNER", "F1", 80.7, "none", "partly", "results table (copied from other papers)", "AI-drafted"],
    [*P23, "swa", "AfriBERTa", "SentencePiece Unigram", 70005, "AfriBERTa (fine-tuned)", "NER", "MasakhaNER", "F1", 88.0, "none", "partly", "results table (copied from other papers)", "AI-drafted"],
    [*P23, "kin", "AfriBERTa", "SentencePiece Unigram", 70005, "AfriBERTa (fine-tuned)", "NER", "MasakhaNER", "F1", 73.2, "none", "partly", "results table (copied from other papers)", "AI-drafted"],
    [*P23, "lug", "AfriBERTa", "SentencePiece Unigram", 70005, "AfriBERTa (fine-tuned)", "NER", "MasakhaNER", "F1", 79.3, "none", "partly", "results table (copied from other papers)", "AI-drafted"],
    [*P23, "zul", "BantuBERTa", "BPE", 70000, "BantuBERTa (fine-tuned)", "news topic", "ANTC", "F1", 79.7, "none", "no (different dataset)", "results table", "AI-drafted"],
    [*P23, "zul", "XLM-R", "SentencePiece Unigram", 250002, "XLM-R + MAFT (fine-tuned)", "news topic", "ANTC", "F1", 79.6, "none", "no", "results table", "AI-drafted"],
    [*P24, "swa", "mBERT", "WordPiece", 119547, "SVM on tokens", "sentiment", "SwahBERT sentiment (7,107 texts)", "accuracy", 83.0, "none", "no (bag of tokens, no neural model)", "results table", "AI-drafted"],
    [*P24, "swa", "English BERT", "WordPiece", 30522, "SVM on tokens", "sentiment", "SwahBERT sentiment", "accuracy", 86.0, "none", "no", "results table", "AI-drafted"],
    [*P24, "swa", "Swahili SentencePiece (theirs)", "SentencePiece", 30000, "SVM on tokens", "sentiment", "SwahBERT sentiment", "accuracy", 67.0, "none", "no", "results table", "AI-drafted"],
    [*P24, "swa", "mBERT", "WordPiece", 119547, "SVM on tokens", "news topic", "Swahili headlines (1,895)", "accuracy", 67.0, "none", "no", "results table", "AI-drafted"],
    [*P24, "swa", "English BERT", "WordPiece", 30522, "SVM on tokens", "news topic", "Swahili headlines", "accuracy", 65.0, "none", "no", "results table", "AI-drafted"],
    [*P24, "swa", "Swahili SentencePiece (theirs)", "SentencePiece", 30000, "SVM on tokens", "news topic", "Swahili headlines", "accuracy", 62.0, "none", "no", "results table", "AI-drafted"],
]
for lang, task, ds, own, best_name, best, eng, xlmr in [
        ("swa", "sentiment", "SwahBERT sentiment", 88.9, "Serengeti", 89.4, 84.5, 88.7),
        ("swa", "news topic", "Mwananchi news", 57.5, "Serengeti", 56.8, 53.4, 54.4),
        ("hau", "sentiment", "NaijaSenti", 72.1, "AfriBERTa", 72.9, 71.9, 71.7),
        ("hau", "news topic", "MasakhaNEWS", 80.9, "Swahili tokenizer", 81.1, 78.9, 80.7),
        ("yor", "sentiment", "NaijaSenti", 65.8, "word-level", 67.3, 63.6, 64.3),
        ("yor", "news topic", "MasakhaNEWS", 82.8, "word-level", 83.9, 76.6, 74.2)]:
    for tok, alg, vocab, score in [(f"{lang} WordPiece (theirs)", "WordPiece", 30000, own), (best_name, "", None, best),
                                   ("English", "WordPiece", None, eng), ("XLM-R", "SentencePiece Unigram", 250002, xlmr)]:
        LIT.append([*P25, lang, tok, alg, vocab, "TF-IDF + SVM/RF/LR (mean of 3)", task, ds, "accuracy", score,
                    "none", "no (bag of tokens, no neural model)", "Tables 3 to 6", "AI-drafted"])
for paper, year, lang, what in [
        ("Goel & Sadat 2025 (IndoNLP)", 2025, "hin", "monolingual Hindi tokenizers for BERT; intrinsic + downstream"),
        ("Dwivedi & Gopalan 2026 (ACL)", 2026, "hin, mar", "fertility, Renyi efficiency, percentile frequency vs QA, POS"),
        ("Pattnayak et al. 2025 (arXiv 2504.16977)", 2025, "Indic (asm, ben, mar, ori, sat, mni, snd)", "BPE vs SentencePiece vs character for zero-shot NER"),
        ("Gren & Kurfali 2026 (EACL SRW)", 2026, "6 languages", "tokenizer transfer (OMP, FVT) on Goldfish models"),
        ("Nzeyimana & Rubungo 2022 (KinyaBERT)", 2022, "kin", "morphology-aware tokenization; NER, GLUE-MT"),
        ("Nakashole 2025 (ACL)", 2025, "10 Bantu", "MoI-MoE, typology-guided adaptation")]:
    LIT.append([paper, year, lang, "", "", None, "", what, "", "", None, "", "", "to extract from the PDF", "not yet"])


def lit_best():
    """Literature cells to bold: the top score (and its tokenizer) within each paper, language and dataset."""
    groups = defaultdict(list)
    for i, x in enumerate(LIT):
        if x[10] is not None:
            groups[(x[0], x[2], x[8])].append(i)
    return {(max(g, key=lambda i: LIT[i][10]), j) for g in groups.values() if len(g) > 1 for j in (3, 10)}


def style_sheet(ws, widths=None):
    for row in ws.iter_rows():
        for c in row:
            if c.font != BOLD and c.font != TITLE:
                c.font = FONT
    for i, col in enumerate(ws.columns, 1):
        w = max((len(str(c.value)) for c in col if c.value is not None), default=8)
        ws.column_dimensions[get_column_letter(i)].width = min(max(w + 2, 8), (widths or {}).get(i, 45))


def best(rows, cols, pick=max):
    """Cells to bold: the best value in each of the given columns, as (row index, column index) pairs."""
    out = set()
    for j in cols:
        vals = [(row[j], i) for i, row in enumerate(rows) if isinstance(row[j], (int, float)) and not np.isnan(row[j])]
        if vals:
            out.add((pick(vals)[1], j))
    return out


def table(ws, r, header, rows, fmts=None, title=None, note=None, bold=()):
    """Write a table at row r; returns the next free row (one blank row after).
    bold: (row index, column index) pairs, both 0-based within the data rows, to show in bold."""
    if title:
        ws.cell(r, 1, title).font = TITLE
        r += 1
    if note:
        ws.cell(r, 1, note).font = Font(name="Arial", size=9, italic=True)
        r += 1
    for j, h in enumerate(header, 1):
        c = ws.cell(r, j, h)
        c.font, c.fill = BOLD, HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, row in enumerate(rows):
        r += 1
        for j, v in enumerate(row, 1):
            if isinstance(v, (np.floating, np.integer)):
                v = v.item()
            if isinstance(v, float) and np.isnan(v):
                v = None
            c = ws.cell(r, j, v)
            if fmts and j - 1 < len(fmts) and fmts[j - 1]:
                c.number_format = fmts[j - 1]
            if (i, j - 1) in bold:
                c.font = BOLD
    return r + 2


def task_sheet(wb, name, task, folder):
    """In-language table, transfer matrices and LoRA vs full for one task. Scores in % (1 decimal)."""
    res, runs = read(folder / "results.jsonl"), read(folder / "runs.jsonl")
    if task == "sib200":  # per-item correct -> [correct, 1] so the same bootstrap works
        for x in res:
            x["score"], x["items"] = x["acc"], [[c, 1] for c in x["correct"]]
        for x in runs:
            x["best_dev"] = x["best_dev_acc"]
    btask = "ner" if task == "ner" else "pos"
    metric = {"sib200": "accuracy", "ner": "entity F1", "pos": "accuracy"}[task]
    ws = wb.create_sheet(name)
    r = table(ws, 1, ["source of these numbers", f"results/{folder.name}/results.jsonl and runs.jsonl"], [
        ["model", res[0]["model"]], ["metric", f"{metric} (%)"], ["seeds", ", ".join(map(str, sorted({x['seed'] for x in res})))],
        ["methods finished", ", ".join(sorted({x["method"] for x in res}))],
        ["runs finished", f"{len(runs)} of 36"]], title=f"{name} baseline")
    langs = [l for l in ORDER if any(x["src"] == l for x in res)]
    methods = sorted({x["method"] for x in res})
    sc, it = {}, {}
    for m in methods:
        sc[m], it[m] = defaultdict(list), defaultdict(list)
        for x in res:
            if x["method"] == m:
                sc[m][(x["src"], x["tgt"])].append(x["score"]); it[m][(x["src"], x["tgt"])].append(x["items"])
    for m in methods:
        rows = []
        for l in langs:
            a = np.array(sc[m][(l, l)]) * 100
            lo, hi = np.percentile(boot(btask, it[m][(l, l)]), [2.5, 97.5]) * 100
            rr = [x for x in runs if x["method"] == m and x["src"] == l]
            rows.append([l, a.mean(), a.std(), lo, hi, np.mean([x["trainable_pct"] for x in rr]),
                         np.mean([x["peak_mem_gb"] for x in rr]), np.mean([x["seconds"] for x in rr]) / 60,
                         np.mean([x["best_epoch"] for x in rr]), len(it[m][(l, l)][0]), len(a)])
        r = table(ws, r, ["lang", f"{metric} % (mean)", "sd over seeds", "95% CI low", "95% CI high", "trainable %",
                          "peak GPU GB", "minutes/run", "best epoch (mean)", "test items", "seeds"], rows,
                  [None, "0.0", "0.0", "0.0", "0.0", "0.00", "0.0", "0.0", "0.0", "0", "0"],
                  title=f"Method: {m}. In-language (train and test on the same language)",
                  note="CI: bootstrap over test items (2,000 resamples), same resampled items for every seed. "
                       "Bold: best and weakest language.",
                  bold={(i, j) for i, _ in best(rows, [1]) | best(rows, [1], min) for j in (0, 1)})
        M = np.array([[np.mean(sc[m][(s, t)]) * 100 if (s, t) in sc[m] else np.nan for t in langs] for s in langs])
        r = table(ws, r, ["source \\ target"] + langs, [[s] + list(M[i]) for i, s in enumerate(langs)],
                  [None] + ["0.0"] * len(langs), title=f"Method: {m}. Zero-shot transfer matrix, {metric} %",
                  note="Rows = training (source) language, columns = test (target) language. Diagonal (bold) = in-language.",
                  bold={(i, i + 1) for i in range(len(langs))})
        Rm = M / np.diag(M)[None, :]
        off = ~np.eye(len(langs), dtype=bool)
        rows = [[s] + list(Rm[i]) + [np.nanmean(Rm[i][off[i]])] for i, s in enumerate(langs)]
        rows.append(["mean as target"] + [np.nanmean(Rm[:, j][off[:, j]]) for j in range(len(langs))] + [None])
        n = len(langs)
        tgt = rows[-1][1:n + 1]
        src = [x[n + 1] for x in rows[:-1]]
        r = table(ws, r, ["source \\ target"] + langs + ["mean as source"], rows, [None] + ["0.00"] * (n + 1),
                  title=f"Method: {m}. Relative transfer (zero-shot / target's in-language score)",
                  note="Bold: best and worst source (last column), easiest and hardest target (last row).",
                  bold={(n, 1 + int(np.nanargmax(tgt))), (n, 1 + int(np.nanargmin(tgt))),
                        (int(np.nanargmax(src)), n + 1), (int(np.nanargmin(src)), n + 1)})
        X = np.where(off, M, np.nan)
        tot = np.nanvar(X)
        col = np.nanvar(np.where(off, np.nanmean(X, 0)[None, :], np.nan))
        row = np.nanvar(np.where(off, np.nanmean(X, 1)[:, None], np.nan))
        bi = [i for i, l in enumerate(langs) if l in BANTU]
        oi = [i for i, l in enumerate(langs) if l not in BANTU]
        r = table(ws, r, ["measure", "value"], [
            ["share of off-diagonal variance explained by the target", col / tot],
            ["share of off-diagonal variance explained by the source", row / tot],
            [f"Bantu -> Bantu, mean {metric} %", np.mean([M[i, j] for i in bi for j in bi if i != j])],
            [f"amh/hau -> Bantu, mean {metric} %", np.mean([M[i, j] for i in oi for j in bi])],
            ["collapsed runs", ", ".join(f"{x['src']} seed {x['seed']}" for x in runs if x["method"] == m and x["collapsed"]) or "none"]],
            [None, None], title=f"Method: {m}. Structure of the transfer matrix",
            bold={(0, 1), (1, 1), (2, 1), (3, 1)})
        for rr in range(r - 6, r - 4):
            ws.cell(rr, 2).number_format = "0%"
        for rr in range(r - 4, r - 2):
            ws.cell(rr, 2).number_format = "0.0"
    if len(methods) == 2:
        a_m, b_m = methods
        rows, diffs = [], []
        for l in langs:
            rows.append([l, (np.mean(sc[b_m][(l, l)]) - np.mean(sc[a_m][(l, l)])) * 100])
            diffs.append(boot(btask, it[b_m][(l, l)]) - boot(btask, it[a_m][(l, l)]))
        lo, hi = np.percentile(np.mean(diffs, axis=0), [2.5, 97.5]) * 100
        rows.append(["pooled (6 languages, all seeds)", np.mean([x[1] for x in rows])])
        rows.append(["pooled 95% CI low", lo]); rows.append(["pooled 95% CI high", hi])
        r = table(ws, r, ["lang", "difference (points)"], rows, [None, "+0.0;-0.0;0.0"],
                  title=f"{b_m} minus {a_m}, in-language {metric}",
                  note="CI: paired bootstrap over test items. Bold: the pooled answer (a CI that spans 0 = no real difference).",
                  bold={(len(rows) - k, j) for k in (1, 2, 3) for j in (0, 1)})
    else:
        ws.cell(r, 1, "LoRA runs not finished yet: the LoRA tables and LoRA minus full appear here after the rerun.").font = FONT
    style_sheet(ws, {1: 50})
    ws.freeze_panes = "B2"


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    tabs = [["Tokenizer availability", "Which of our 6 languages each tokenizer was trained for (hand-curated, with source)"],
            ["Tokenizer stats", "Fragmentation study: fertility, continued words, token premium, Renyi efficiency, unknown rate"],
            ["SIB-200", "Topic classification baseline: in-language, 6x6 transfer matrices, LoRA vs full"],
            ["NER", "MasakhaNER baseline, same layout"], ["POS", "MasakhaPOS / UD Amharic baseline, same layout"],
            ["Luganda diagnostics", "Masked-LM pseudo-perplexity per language (why is Luganda weak on SIB-200?)"],
            ["Literature", "Numbers reported in papers: state-of-the-art comparison table for the literature review"],
            ["Runs", "Every training run: settings, best dev score, GPU memory, time"]]
    r = table(ws, 1, ["tab", "contents"], tabs, title="Typology-aware PEFT: results workbook",
              note=f"Built {date.today().isoformat()} by src/build_workbook.py from the files in results/. "
                   "Generated: rebuild instead of editing. Interpretation lives in the .md files.")
    defs = [["fertility", "subword tokens per whitespace word (lower = less splitting)"],
            ["continued words", "share of words split into 2 or more tokens"],
            ["token premium", "tokens per sentence divided by English tokens per sentence, same tokenizer (parallel text)"],
            ["Renyi efficiency", "Renyi entropy (alpha 2.5) of the token distribution / log(vocabulary size)"],
            ["entity F1", "MasakhaNER span-level F1 (conlleval style)"],
            ["relative transfer", "zero-shot score / the target language's in-language score"],
            ["NLL per sentence", "masked-LM negative log-likelihood of a sentence, whole-word masking; parallel text, so comparable"],
            ["full / lora", "full fine-tuning / LoRA r=8, alpha 16, query and value matrices"],
            ["bold numbers", "the ones to read first; the note above each table says what its bold marks"]]
    table(ws, r, ["term", "definition"], defs, title="Definitions")
    style_sheet(ws, {1: 30, 2: 110})

    ws = wb.create_sheet("Tokenizer availability")
    table(ws, 1, ["tokenizer", "repo", "algorithm", "vocab", "tokenizer trained for", "amh", "hau", "kin", "lug", "swa",
                  "zul", "source", "checked on"], AVAILABILITY, [None, None, None, "#,##0"],
          title="Which languages each tokenizer was trained for",
          note="'?' = from memory, not yet checked. Model coverage can differ from tokenizer coverage (see AfroXLMR).")
    style_sheet(ws, {5: 60, 12: 60})
    ws.freeze_panes = "B4"

    ws = wb.create_sheet("Tokenizer stats")
    stats = list(csv.DictReader(open(R / "tokenizers" / "stats.csv", encoding="utf-8")))
    names = list(dict.fromkeys(s["tokenizer"] for s in stats))
    langs = list(dict.fromkeys(s["lang"] for s in stats))
    get = {(s["tokenizer"], s["lang"]): s for s in stats}
    r = 1
    for key, label, fmt, pick in [("fertility", "Fertility (tokens per word)", "0.00", min),
                                  ("continued_words", "Continued words (share of words split)", "0%", min),
                                  ("premium", "Token premium vs English", "0.00", min),
                                  ("renyi_eff", "Renyi efficiency (alpha 2.5)", "0.000", max),
                                  ("unk_rate", "Unknown-token rate", "0.00%", None)]:
        rows = [[n, int(get[(n, "eng")]["vocab"])] + [float(get[(n, l)][key]) for l in langs] for n in names]
        cols = range(2, 2 + len(langs))
        if pick:  # best tokenizer per language (not English, not where it is mostly unknown tokens), plus our model
            ok = [[x[0], x[1]] + [v if float(get[(x[0], l)]["unk_rate"]) < 0.01 else np.nan for v, l in zip(x[2:], langs)]
                  for x in rows]
            hl = best(ok, [2 + k for k, l in enumerate(langs) if l != "eng"], pick) | \
                {(i, 0) for i, x in enumerate(rows) if x[0].startswith("AfroXLMR")}
            how = ("Bold: best tokenizer for each of our languages (ignoring 1% or more unknown tokens); "
                   "AfroXLMR-76L is our model.")
        else:  # unknown tokens: only problems are worth seeing
            hl = {(i, j) for i, x in enumerate(rows) for j in cols if x[j] >= 0.01}
            how = "Bold: 1% or more unknown tokens (the tokenizer cannot represent that language)."
        r = table(ws, r, ["tokenizer", "vocab"] + langs, rows, [None, "#,##0"] + [fmt] * len(langs), title=label,
                  note=("Source: results/tokenizers/stats.csv (src/tokenizer_stats.py). Text: SIB-200, 1,004 parallel "
                        "sentences per language. " if r == 1 else "") + how, bold=hl)
    bnd = list(csv.DictReader(open(R / "tokenizers" / "boundaries.csv", encoding="utf-8")))
    rows = [[b["tokenizer"], b["lang"], int(b["words_scored"]), int(b["words"])] +
            [float(b[k]) for k in ("chance_p", "boundary_p", "boundary_r", "boundary_f1", "exact_match",
                                   "tokens_per_word", "morphemes_per_word")] for b in bnd]
    r = table(ws, r, ["tokenizer", "lang", "words scored", "words in gold set", "chance precision", "boundary precision",
                      "boundary recall", "boundary F1", "exact match", "tokens/word", "morphemes/word"], rows,
              [None, None, "#,##0", "#,##0", "0.00", "0.00", "0.00", "0.00", "0%", "0.00", "0.00"],
              title="Morpheme boundaries vs gold segmentation (isiZulu only: no gold set found for swa, kin, lug)",
              note="Source: results/tokenizers/boundaries.csv. Gold: NCHLT isiZulu surface segmentations as prepared by "
                   "Moeng et al. 2021 (github.com/TumiMoeng/MORPH_SEGMENT). Chance precision = precision of random cuts. "
                   "Bold: the chance baseline, the best boundary F1, and our model's F1.",
              bold={(0, 4)} | best(rows, [7]) | {(i, j) for i, x in enumerate(rows) if x[0].startswith("AfroXLMR")
                                                 for j in (0, 7)})
    morf = list(csv.DictReader(open(R / "tokenizers" / "morfessor.csv", encoding="utf-8")))
    chosen = max(range(len(morf)), key=lambda i: float(morf[i]["dev_boundary_f1"]))
    rows = [[m["lang"], float(m["corpus_weight"]), "yes" if i == chosen else "", int(m["train_types"])] +
            [float(m[k]) for k in ("dev_boundary_f1", "test_boundary_p", "test_boundary_r", "test_boundary_f1",
                                   "test_exact_match", "test_morphs_per_word", "all_boundary_f1")]
            for i, m in enumerate(morf)]
    r = table(ws, r, ["lang", "corpus weight (Morfessor setting: lower = more cuts)", "chosen (best dev F1)",
                      "training word types", "dev F1", "test precision", "test recall", "test F1", "test exact match",
                      "test pieces/word", "all gold words F1"], rows,
              [None, "0.00", None, "#,##0", "0.000", "0.00", "0.00", "0.000", "0%", "0.00", "0.000"],
              title="Morfessor (unsupervised segmenter) vs isiZulu gold: can it serve as silver for swa, kin, lug?",
              note="Every row is the same method (Morfessor Baseline, same isiZulu text); only the corpus weight differs. "
                   "Source: results/tokenizers/morfessor.csv (src/morfessor_silver.py). Trained on WURA isiZulu "
                   "(3.3M words, top 100k types). Weight chosen on gold dev words, scored on held-out gold test words. "
                   "Gold: 3.51 morphemes per word. Compare 'all gold words F1' with the tokenizer table above. "
                   "Bold: the chosen setting.",
              bold={(chosen, j) for j in (1, 2, 4, 7, 10)})
    cols = ["tokenizer", "repo", "algorithm", "vocab", "lang", "sentences", "words", "tokens", "fertility",
            "continued_words", "chars_per_token", "unk_rate", "premium", "renyi_eff"]
    table(ws, r, cols, [[s[c] if i < 3 or c == "lang" else float(s[c]) for i, c in enumerate(cols)] for s in stats],
          [None, None, None, "#,##0", None, "#,##0", "#,##0", "#,##0", "0.00", "0%", "0.00", "0.00%", "0.00", "0.000"],
          title="All measurements (long format, for filtering)")
    style_sheet(ws, {1: 30, 2: 40})

    for name, task in [("SIB-200", "sib200"), ("NER", "ner"), ("POS", "pos")]:
        if (R / task / "results.jsonl").exists():
            task_sheet(wb, name, task, R / task)

    ws = wb.create_sheet("Luganda diagnostics")
    sent = read(R / "pppl" / "sentences.jsonl")
    sib = read(R / "sib200" / "results.jsonl")
    rows = []
    for l in ORDER:
        s = [x for x in sent if x["lang"] == l]
        toks, words = sum(x["n_tokens"] for x in s), sum(x["n_words"] for x in s)
        nw, nt = np.array([x["nll_word_l2r"] for x in s]), np.array([x["nll_token"] for x in s])
        acc = np.mean([x["acc"] for x in sib if x["tgt"] == l and x["src"] == l]) * 100
        rows.append([l, len(s), nw.mean(), nt.mean(), np.exp(nw.sum() / toks), np.exp(nt.sum() / toks), toks / words, acc])
    table(ws, 1, ["lang", "sentences", "NLL/sentence (whole-word)", "NLL/sentence (token)", "PPPL whole-word",
                  "PPPL token", "tokens/word", "SIB-200 in-language acc % (both methods)"], rows,
          [None, "0", "0.0", "0.0", "0.00", "0.00", "0.00", "0.0"],
          title="Masked-LM pseudo-perplexity of AfroXLMR-76L on the SIB-200 test sentences",
          note="Source: results/pppl/sentences.jsonl (src/pseudo_perplexity.py). Lower NLL = model predicts the text better. "
               "Same 204 sentences in every language. Bold: Luganda, the outlier.",
          bold={(i, j) for i, x in enumerate(rows) if x[0] == "lug" for j in (0, 2, 4, 7)})
    style_sheet(ws, {1: 12})

    ws = wb.create_sheet("Literature")
    table(ws, 1, ["paper", "year", "language", "tokenizer", "algorithm", "vocab", "model / classifier", "task", "dataset",
                  "metric", "score (%)", "intrinsic metrics reported", "comparable to ours", "where in paper", "checked"],
          LIT, [None, "0", None, None, None, "#,##0", None, None, None, None, "0.0"],
          title="Numbers reported in papers (state of the art)",
          note="One row per reported number. 'AI-drafted' rows come from the reading notes and must be checked against "
               "the PDF. Numbers from different papers are not directly comparable (setups differ): see the comparable column. "
               "Bold: best tokenizer within each paper, language and dataset.",
          bold=lit_best())
    style_sheet(ws, {1: 38, 7: 32, 8: 40, 13: 36})
    ws.freeze_panes = "B4"

    ws = wb.create_sheet("Runs")
    rows = []
    for task in ("sib200", "ner", "pos"):
        f = R / task / "runs.jsonl"
        if f.exists():
            for x in read(f):
                rows.append([task, x["method"], x["seed"], x["src"], x.get("best_dev", x.get("best_dev_acc")) * 100,
                             x["best_epoch"], x["epochs"], x["lr"], x["bs"], x["trainable_pct"], x["n_trainable"],
                             x["peak_mem_gb"], x["seconds"] / 60, "yes" if x["collapsed"] else ""])
    table(ws, 1, ["task", "method", "seed", "source", "best dev score %", "best epoch", "epochs", "learning rate",
                  "batch size", "trainable %", "trainable params", "peak GPU GB", "minutes", "collapsed"], rows,
          [None, None, "0", None, "0.0", "0", "0", "0.0E+00", "0", "0.00", "#,##0", "0.0", "0.0"],
          title="Every training run", note="Source: results/<task>/runs.jsonl. GPU: NVIDIA L4 (Colab). Bold: collapsed runs.",
          bold={(i, j) for i, x in enumerate(rows) if x[-1] for j in range(len(x))})
    style_sheet(ws)
    ws.freeze_panes = "A4"

    wb.save(R / "results.xlsx")
    print(f"Wrote {R / 'results.xlsx'}: {', '.join(wb.sheetnames)}")


if __name__ == "__main__":
    main()
