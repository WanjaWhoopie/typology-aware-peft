#!/usr/bin/env python3
"""SIB-200 baseline: in-language fine-tuning plus the 6x6 zero-shot transfer matrix.

For every method, seed and source language the script
  1. fine-tunes AfroXLMR on the source-language SIB-200 train split,
  2. picks the epoch with the best source-language dev accuracy,
  3. evaluates that model on the test split of ALL six languages
     (diagonal = in-language score, off-diagonal = zero-shot transfer).
So the 30-pair transfer matrix comes from the same runs as the in-language baselines.

Setup (once):
    pip install torch transformers datasets peft scikit-learn numpy

Quick test (a few minutes, use the base model first):
    python src/sib200_baseline.py --smoke --model Davlan/afro-xlmr-base

Full run (from the repo root):
    python src/sib200_baseline.py
    python src/sib200_report.py

Methods: "full" = full fine-tuning, "lora" = LoRA (PEFT reference).
Runs are appended to results/sib200/runs.jsonl and results/sib200/results.jsonl,
so an interrupted run resumes where it stopped (finished combinations are skipped).
"""
import argparse
import gc
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
from datasets import load_dataset
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

# short code -> SIB-200 config name
LANGS = {"amh": "amh_Ethi", "hau": "hau_Latn", "kin": "kin_Latn",
         "lug": "lug_Latn", "swa": "swh_Latn", "zul": "zul_Latn"}


def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def load_all(langs, tok, max_len, limit=None):
    """Load and tokenise train/validation/test for each language; shared label ids."""
    raw = {l: load_dataset("Davlan/sib200", LANGS[l]) for l in langs}
    labels = sorted({c for l in langs for c in raw[l]["train"]["category"]})
    l2i = {c: i for i, c in enumerate(labels)}
    data = {}
    for l in langs:
        data[l] = {}
        for split in ("train", "validation", "test"):
            d = raw[l][split]
            if limit:  # splits are sorted by category, so shuffle before truncating
                d = d.shuffle(seed=0).select(range(min(limit, len(d))))
            enc = tok(list(d["text"]), truncation=True, max_length=max_len)
            cats = list(d["category"])
            data[l][split] = [{"input_ids": enc["input_ids"][i],
                               "attention_mask": enc["attention_mask"][i],
                               "labels": l2i[cats[i]]} for i in range(len(d))]
    return data, labels


def make_collate(tok):
    def collate(batch):
        labels = torch.tensor([b["labels"] for b in batch])
        out = tok.pad([{"input_ids": b["input_ids"], "attention_mask": b["attention_mask"]} for b in batch],
                      return_tensors="pt")
        out["labels"] = labels
        return out
    return collate


@torch.no_grad()
def evaluate(model, examples, collate, device, amp_dtype, bs=64):
    model.eval()
    preds = []
    for batch in DataLoader(examples, batch_size=bs, collate_fn=collate):
        batch = {k: v.to(device) for k, v in batch.items()}
        batch.pop("labels")
        with torch.autocast(device_type=device.type, dtype=amp_dtype, enabled=amp_dtype is not None):
            logits = model(**batch).logits
        preds += logits.argmax(-1).cpu().tolist()
    gold = [e["labels"] for e in examples]
    correct = [int(p == g) for p, g in zip(preds, gold)]
    return {"acc": float(np.mean(correct)),
            "macro_f1": float(f1_score(gold, preds, average="macro", zero_division=0)),
            "correct": correct}


def build_model(name, method, num_labels, args):
    model = AutoModelForSequenceClassification.from_pretrained(name, num_labels=num_labels)
    if method == "lora":
        from peft import LoraConfig, TaskType, get_peft_model
        cfg = LoraConfig(task_type=TaskType.SEQ_CLS, r=args.lora_r, lora_alpha=2 * args.lora_r,
                         lora_dropout=0.1, target_modules=["query", "value"])
        model = get_peft_model(model, cfg)  # classifier head stays trainable automatically
    return model


def train_one(src, seed, method, data, labels, tok, args, device, amp_dtype):
    set_seed(seed)
    collate = make_collate(tok)
    model = build_model(args.model, method, len(labels), args).to(device)
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
    best_acc, best_epoch, best_state = -1.0, 0, None
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
        dev = evaluate(model, data[src]["validation"], collate, device, amp_dtype)
        print(f"    epoch {epoch:2d}  loss {loss.item():.3f}  dev acc {dev['acc']:.3f}", flush=True)
        if dev["acc"] > best_acc:
            best_acc, best_epoch = dev["acc"], epoch
            best_state = {n: p.detach().cpu().clone() for n, p in model.named_parameters() if n in trainable}
    model.load_state_dict(best_state, strict=False)
    seconds = time.time() - t0
    peak = torch.cuda.max_memory_allocated() / 1e9 if device.type == "cuda" else None

    rows = []
    for tgt in data:
        r = evaluate(model, data[tgt]["test"], collate, device, amp_dtype)
        rows.append({"task": "sib200", "model": args.model, "method": method, "seed": seed,
                     "src": src, "tgt": tgt, **r})
    run = {"task": "sib200", "model": args.model, "method": method, "seed": seed, "src": src,
           "n_params": n_all, "n_trainable": n_train, "trainable_pct": 100 * n_train / n_all,
           "peak_mem_gb": peak, "seconds": seconds, "best_epoch": best_epoch, "best_dev_acc": best_acc,
           "collapsed": best_acc < 0.3, "lr": lr, "epochs": args.epochs, "bs": args.bs}
    if run["collapsed"]:
        print("    WARNING: dev accuracy below 0.3 (model likely collapsed to one class). "
              "Try a lower learning rate or another seed.", flush=True)
    del model, opt, best_state
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return run, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="Davlan/afro-xlmr-large-76L")
    ap.add_argument("--methods", nargs="+", default=["full", "lora"], choices=["full", "lora"])
    ap.add_argument("--langs", nargs="+", default=list(LANGS), choices=list(LANGS))
    ap.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3])
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--max_len", type=int, default=128)
    ap.add_argument("--lr_full", type=float, default=2e-5)
    ap.add_argument("--lr_lora", type=float, default=3e-4)
    ap.add_argument("--lora_r", type=int, default=8)
    ap.add_argument("--out", default="results/sib200")
    ap.add_argument("--smoke", action="store_true", help="tiny run to test the pipeline")
    args = ap.parse_args()

    limit = None
    if args.smoke:
        args.langs, args.seeds, args.epochs, args.methods = ["swa", "zul"], [1], 1, ["lora"]
        args.out = "results/sib200_smoke"
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
    data, labels = load_all(args.langs, tok, args.max_len, limit)
    print(f"{len(labels)} labels: {labels}")
    print({l: {s: len(v) for s, v in d.items()} for l, d in data.items()})

    jobs = [(m, s, l) for m in args.methods for s in args.seeds for l in args.langs]
    todo = [j for j in jobs if (args.model, *j) not in done]
    print(f"{len(todo)} runs to do ({len(jobs) - len(todo)} already finished)\n", flush=True)
    t_start = time.time()
    for i, (method, seed, src) in enumerate(todo, 1):
        print(f"[{i}/{len(todo)}] method={method} seed={seed} source={src}", flush=True)
        run, rows = train_one(src, seed, method, data, labels, tok, args, device, amp_dtype)
        with open(res_f, "a", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        with open(runs_f, "a", encoding="utf-8") as f:  # written last, so a crash re-runs this job
            f.write(json.dumps(run) + "\n")
        diag = next(r for r in rows if r["tgt"] == src)
        elapsed = time.time() - t_start
        print(f"    test acc in-language {diag['acc']:.3f}; {run['seconds']:.0f}s; "
              f"elapsed {elapsed / 60:.1f} min, about {elapsed / i * (len(todo) - i) / 60:.0f} min left\n", flush=True)
    print("Done. Now run: python src/sib200_report.py")


if __name__ == "__main__":
    main()
