#!/usr/bin/env python3
"""NER and POS baselines: in-language fine-tuning plus the 6x6 zero-shot transfer matrix.

Same design as src/sib200_baseline.py: for every task, method, seed and source language the script
fine-tunes AfroXLMR on the source train split, picks the epoch with the best source dev score, and
evaluates that model on the test split of ALL six languages (diagonal = in-language, off-diagonal = zero-shot).

Data (downloaded once into data/raw/, which is not committed):
  NER  MasakhaNER 2.0 (hau, kin, lug, swa, zul) and MasakhaNER 1.0 (amh), CoNLL files from GitHub
       (the Hugging Face copies use loading scripts, which datasets>=4 no longer runs).
       Metric: entity-level F1 (exact span and type, as conlleval).
  POS  MasakhaPOS from Hugging Face (hau, kin, lug, swa, zul) and UD_Amharic-ATT (amh). Metric: accuracy.
       UD_Amharic-ATT has only a test file (1,074 sentences), so it is split 70/10/20 with a fixed seed.
       Its tokens are UD syntactic words (clitics split off, e.g. one surface word -> NOUN DET PART),
       unlike MasakhaPOS, which tags surface words. Footnote this whenever Amharic POS is reported.

    python src/token_baseline.py --task ner --smoke --model Davlan/afro-xlmr-base
    python src/token_baseline.py --task ner
    python src/token_baseline.py --task pos
    python src/token_report.py --task ner

Runs are appended to results/<task>/runs.jsonl and results/<task>/results.jsonl, so an interrupted
run resumes where it stopped (finished combinations are skipped).
"""
import argparse
import gc
import json
import random
import time
import urllib.request
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader
from transformers import AutoModelForTokenClassification, AutoTokenizer, get_linear_schedule_with_warmup

LANGS = ["amh", "hau", "kin", "lug", "swa", "zul"]
NER_URL = "https://raw.githubusercontent.com/masakhane-io/masakhane-ner/main/"
UD_AMH_URL = "https://raw.githubusercontent.com/UniversalDependencies/UD_Amharic-ATT/master/am_att-ud-test.conllu"
SPLITS = ("train", "validation", "test")


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def fetch(url, path):
    path = Path(path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return path.read_text(encoding="utf-8")


def read_conll(text):
    """'word tag' lines, blank line between sentences -> list of (words, tags)."""
    sents, words, tags = [], [], []
    for line in text.splitlines():
        if not line.strip():
            if words:
                sents.append((words, tags))
                words, tags = [], []
            continue
        p = line.split()
        words.append(p[0])
        tags.append(p[-1])
    if words:
        sents.append((words, tags))
    return sents


def load_ner(lang, raw):
    base = f"{NER_URL}data/amh/" if lang == "amh" else f"{NER_URL}MasakhaNER2.0/data/{lang}/"
    files = {"train": "train.txt", "validation": "dev.txt", "test": "test.txt"}
    return {s: read_conll(fetch(base + f, raw / "masakhaner" / lang / f)) for s, f in files.items()}


def load_pos(lang, raw):
    if lang != "amh":
        from datasets import load_dataset
        d = load_dataset("masakhane/masakhapos", lang)
        names = d["train"].features["upos"].feature.names
        return {s: [(x["tokens"], [names[i] for i in x["upos"]]) for x in d[s]] for s in SPLITS}
    sents, words, tags = [], [], []
    for line in fetch(UD_AMH_URL, raw / "ud_amharic_att" / "am_att-ud-test.conllu").splitlines():
        if not line.strip():
            if words:
                sents.append((words, tags))
                words, tags = [], []
            continue
        if line.startswith("#"):
            continue
        p = line.split("\t")
        if p[0].isdigit():  # syntactic words only; skips multiword-token ranges (1-3) and empty nodes (1.1)
            words.append(p[1])
            tags.append(p[3])
    if words:
        sents.append((words, tags))
    order = np.random.default_rng(0).permutation(len(sents))
    n_tr, n_dev = int(0.7 * len(sents)), int(0.1 * len(sents))
    pick = lambda idx: [sents[i] for i in sorted(idx)]
    return {"train": pick(order[:n_tr]), "validation": pick(order[n_tr:n_tr + n_dev]),
            "test": pick(order[n_tr + n_dev:])}


def encode(sents, tok, l2i, max_len):
    """Label the first subword of each word; other subwords get -100 (ignored)."""
    out = []
    for words, tags in sents:
        enc = tok(words, is_split_into_words=True, truncation=True, max_length=max_len)
        labels, prev = [], None
        for w in enc.word_ids():
            labels.append(-100 if w is None or w == prev else l2i[tags[w]])
            prev = w
        out.append({"input_ids": enc["input_ids"], "attention_mask": enc["attention_mask"],
                    "labels": labels, "tags": tags})
    return out


def load_all(task, langs, tok, max_len, raw, limit=None):
    loader = load_ner if task == "ner" else load_pos
    raw_data = {l: loader(l, raw) for l in langs}
    labels = sorted({t for l in langs for _, tags in raw_data[l]["train"] for t in tags})
    l2i = {c: i for i, c in enumerate(labels)}
    data = {}
    for l in langs:
        data[l] = {}
        for split in SPLITS:
            sents = raw_data[l][split]
            if limit:
                sents = [sents[i] for i in np.random.default_rng(0).permutation(len(sents))[:limit]]
            # a tag seen only in another split or language would have no id: map it to "O" / "X"
            fallback = "O" if task == "ner" else "X"
            sents = [(w, [t if t in l2i else fallback for t in tags]) for w, tags in sents]
            data[l][split] = encode(sents, tok, l2i, max_len)
    return data, labels


def make_collate(tok):
    def collate(batch):
        out = tok.pad([{"input_ids": b["input_ids"], "attention_mask": b["attention_mask"]} for b in batch],
                      return_tensors="pt")
        n = out["input_ids"].shape[1]
        out["labels"] = torch.tensor([b["labels"] + [-100] * (n - len(b["labels"])) for b in batch])
        return out
    return collate


def spans(tags):
    """IOB2 tags -> set of (type, start, end). An I- tag without a matching B- starts a new entity."""
    out, start, typ = set(), None, None
    for i, t in enumerate(list(tags) + ["O"]):
        if start is not None and not (t.startswith("I-") and t[2:] == typ):
            out.add((typ, start, i))
            start = None
        if t.startswith("B-") or (t.startswith("I-") and start is None):
            start, typ = i, t[2:]
    return out


def score(task, gold_tags, pred_tags):
    """Per-sentence counts, so the report can bootstrap over sentences."""
    if task == "pos":
        items = [[sum(g == p for g, p in zip(gs, ps)), len(gs)] for gs, ps in zip(gold_tags, pred_tags)]
        return {"score": sum(c for c, _ in items) / sum(n for _, n in items), "items": items}
    items = []
    for gs, ps in zip(gold_tags, pred_tags):
        g, p = spans(gs), spans(ps)
        items.append([len(g & p), len(p - g), len(g - p)])  # tp, fp, fn
    tp, fp, fn = (sum(x[k] for x in items) for k in range(3))
    return {"score": 2 * tp / (2 * tp + fp + fn) if tp else 0.0, "items": items}


@torch.no_grad()
def evaluate(task, model, examples, labels, collate, device, amp_dtype, bs=64):
    model.eval()
    preds = []
    for batch in DataLoader(examples, batch_size=bs, collate_fn=collate):
        batch = {k: v.to(device) for k, v in batch.items()}
        gold = batch.pop("labels")
        with torch.autocast(device_type=device.type, dtype=amp_dtype, enabled=amp_dtype is not None):
            logits = model(**batch).logits
        for row_pred, row_gold in zip(logits.argmax(-1).cpu().tolist(), gold.cpu().tolist()):
            preds.append([labels[p] for p, g in zip(row_pred, row_gold) if g != -100])
    gold_tags = [e["tags"] for e in examples]
    fill = "O" if task == "ner" else "X"  # words cut off by truncation count as wrong
    pred_tags = [p + [fill] * (len(g) - len(p)) for p, g in zip(preds, gold_tags)]
    return score(task, gold_tags, pred_tags)


def build_model(name, method, labels, args):
    model = AutoModelForTokenClassification.from_pretrained(
        name, num_labels=len(labels), id2label=dict(enumerate(labels)), label2id={c: i for i, c in enumerate(labels)})
    if method == "lora":
        from peft import LoraConfig, TaskType, get_peft_model
        cfg = LoraConfig(task_type=TaskType.TOKEN_CLS, r=args.lora_r, lora_alpha=2 * args.lora_r,
                         lora_dropout=0.1, target_modules=["query", "value"])
        model = get_peft_model(model, cfg)  # classifier head stays trainable automatically
    return model


def train_one(src, seed, method, data, labels, tok, args, device, amp_dtype):
    set_seed(seed)
    collate = make_collate(tok)
    model = build_model(args.model, method, labels, args).to(device)
    trainable = {n for n, p in model.named_parameters() if p.requires_grad}
    n_train = sum(p.numel() for n, p in model.named_parameters() if n in trainable)
    n_all = sum(p.numel() for p in model.parameters())
    lr = args.lr_full if method == "full" else args.lr_lora
    opt = torch.optim.AdamW([p for n, p in model.named_parameters() if n in trainable],
                            lr=lr, weight_decay=0.01)
    loader = DataLoader(data[src]["train"], batch_size=args.bs, shuffle=True, collate_fn=collate,
                        generator=torch.Generator().manual_seed(seed))
    total = len(loader) * args.epochs
    sched = get_linear_schedule_with_warmup(opt, int(0.1 * total), total)
    scaler = torch.amp.GradScaler(device.type, enabled=(amp_dtype == torch.float16))
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats()
    t0 = time.time()
    best, best_epoch, best_state = -1.0, 0, None
    for epoch in range(1, args.epochs + 1):
        model.train()
        for batch in loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            with torch.autocast(device_type=device.type, dtype=amp_dtype, enabled=amp_dtype is not None):
                loss = model(**batch).loss
            scaler.scale(loss).backward()
            scaler.unscale_(opt)
            torch.nn.utils.clip_grad_norm_([p for n, p in model.named_parameters() if n in trainable], 1.0)
            scaler.step(opt)
            scaler.update()
            opt.zero_grad(set_to_none=True)
            sched.step()
        dev = evaluate(args.task, model, data[src]["validation"], labels, collate, device, amp_dtype)
        print(f"    epoch {epoch:2d}  loss {loss.item():.3f}  dev {args.metric} {dev['score']:.3f}", flush=True)
        if dev["score"] > best:
            best, best_epoch = dev["score"], epoch
            best_state = {n: p.detach().cpu().clone() for n, p in model.named_parameters() if n in trainable}
    model.load_state_dict(best_state, strict=False)
    seconds = time.time() - t0
    peak = torch.cuda.max_memory_allocated() / 1e9 if device.type == "cuda" else None

    rows = []
    for tgt in data:
        r = evaluate(args.task, model, data[tgt]["test"], labels, collate, device, amp_dtype)
        rows.append({"task": args.task, "model": args.model, "method": method, "seed": seed,
                     "src": src, "tgt": tgt, "metric": args.metric, **r})
    run = {"task": args.task, "model": args.model, "method": method, "seed": seed, "src": src,
           "n_params": n_all, "n_trainable": n_train, "trainable_pct": 100 * n_train / n_all,
           "peak_mem_gb": peak, "seconds": seconds, "best_epoch": best_epoch, "best_dev": best,
           "collapsed": best < args.collapse, "lr": lr, "epochs": args.epochs, "bs": args.bs}
    if run["collapsed"]:
        print(f"    WARNING: dev {args.metric} below {args.collapse} (model likely collapsed). "
              "Try a lower learning rate or another seed.", flush=True)
    del model, opt, best_state
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return run, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True, choices=["ner", "pos"])
    ap.add_argument("--model", default="Davlan/afro-xlmr-large-76L")
    ap.add_argument("--methods", nargs="+", default=["full", "lora"], choices=["full", "lora"])
    ap.add_argument("--langs", nargs="+", default=LANGS, choices=LANGS)
    ap.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3])
    ap.add_argument("--epochs", type=int, default=None, help="default: 5 for NER (5k-8k sentences), 10 for POS")
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--max_len", type=int, default=256)
    ap.add_argument("--lr_full", type=float, default=2e-5)
    ap.add_argument("--lr_lora", type=float, default=3e-4)
    ap.add_argument("--lora_r", type=int, default=8)
    ap.add_argument("--raw", default="data/raw")
    ap.add_argument("--out", default=None, help="default: results/<task>")
    ap.add_argument("--smoke", action="store_true", help="tiny run to test the pipeline")
    args = ap.parse_args()
    args.metric = "f1" if args.task == "ner" else "acc"
    args.collapse = 0.2 if args.task == "ner" else 0.5
    args.epochs = args.epochs or (5 if args.task == "ner" else 10)
    args.out = args.out or f"results/{args.task}"

    limit = None
    if args.smoke:
        args.langs, args.seeds, args.epochs, args.methods = ["swa", "amh"], [1], 1, ["lora"]
        args.out = f"results/{args.task}_smoke"
        limit = 64

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    runs_f, res_f = out / "runs.jsonl", out / "results.jsonl"
    done = set()
    if runs_f.exists():
        for line in runs_f.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done.add((r["model"], r["method"], r["seed"], r["src"]))

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cuda":
        amp_dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
    else:
        amp_dtype = None
        print("WARNING: no GPU found, training will be very slow.")
    (out / "meta.json").write_text(json.dumps({
        "args": vars(args), "torch": torch.__version__,
        "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None}, indent=2), encoding="utf-8")

    tok = AutoTokenizer.from_pretrained(args.model)
    data, labels = load_all(args.task, args.langs, tok, args.max_len, Path(args.raw), limit)
    print(f"{len(labels)} labels: {labels}")
    print({l: {s: len(v) for s, v in d.items()} for l, d in data.items()})

    jobs = [(m, s, l) for m in args.methods for s in args.seeds for l in args.langs]
    todo = [j for j in jobs if (args.model, *j) not in done]
    print(f"{len(todo)} runs to do ({len(jobs) - len(todo)} already finished)\n", flush=True)
    t_start = time.time()
    for i, (method, seed, src) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] task={args.task} method={method} seed={seed} source={src}", flush=True)
        run, rows = train_one(src, seed, method, data, labels, tok, args, device, amp_dtype)
        with open(res_f, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        with open(runs_f, "a", encoding="utf-8") as f:  # written last, so a crash re-runs this job
            f.write(json.dumps(run) + "\n")
        diag = next(r for r in rows if r["tgt"] == src)
        elapsed = time.time() - t_start
        print(f"    test {args.metric} in-language {diag['score']:.3f}; {run['seconds']:.0f}s; "
              f"elapsed {elapsed / 60:.1f} min, about {elapsed / i * (len(todo) - i) / 60:.0f} min left\n", flush=True)
    print(f"Done. Now run: python src/token_report.py --task {args.task}")


if __name__ == "__main__":
    main()
