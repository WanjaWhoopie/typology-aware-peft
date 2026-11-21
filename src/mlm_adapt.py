#!/usr/bin/env python3
"""Short masked-LM pass that trains only the input embeddings (the adaptation step FVT prescribes after a vocabulary
swap; Gee et al. 2022). Everything else in the model stays frozen.

Used twice, with the same text, steps and settings:
  1. on the Serengeti-vocabulary model from src/vocab_transfer.py (new tokens start as averages of AfroXLMR pieces);
  2. on plain AfroXLMR as a control, so a gain can be credited to the vocabulary rather than to extra masked-LM
     training on the four languages' text.

Text: the raw corpora Morfessor was trained on (WURA for kin, swa, zul; MADLAD-400 for lug; see
src/morfessor_silver.py), the same number of 128-token blocks per language.

    python src/mlm_adapt.py --model /content/afroxlmr_serengeti_fvt --out /content/serengeti_fvt_mlm
    python src/mlm_adapt.py --model Davlan/afro-xlmr-large-76L --out /content/afroxlmr_mlm

Writes the adapted model (and tokenizer) to --out, plus mlm_stats.json with the loss before and after.
"""
import argparse
import json
import random
import time
from pathlib import Path

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer, DataCollatorForLanguageModeling

from morfessor_silver import lines


def blocks(lang, tok, raw, n_blocks, block=128, seed=0):
    """n_blocks token blocks of one language, cut from consecutive non-empty lines."""
    out, buf = [], []
    for line in lines(lang, raw):
        line = line.strip()
        if len(line) < 20:
            continue
        buf += tok(line, add_special_tokens=False)["input_ids"]
        while len(buf) >= block - 2:
            out.append([tok.cls_token_id] + buf[:block - 2] + [tok.sep_token_id])
            buf = buf[block - 2:]
            if len(out) >= 3 * n_blocks:  # read a bit more than needed, then sample
                random.Random(seed).shuffle(out)
                return out[:n_blocks]
    random.Random(seed).shuffle(out)
    return out[:n_blocks]


def amp_dtype(device):
    """bf16 on GPUs with native support (A100, L4), fp16 on older ones (T4), none on CPU."""
    if device.type != "cuda":
        return None
    return torch.bfloat16 if torch.cuda.get_device_capability(0)[0] >= 8 else torch.float16


def mean_loss(model, data, collate, device, bs=32, n=20):
    model.eval()
    g = torch.Generator().manual_seed(0)
    tot = 0.0
    with torch.no_grad(), torch.autocast(device_type=device.type, dtype=amp_dtype(device) or torch.float32, enabled=amp_dtype(device) is not None):
        for i in range(n):
            torch.manual_seed(i)  # same masks every time
            batch = collate(data[i * bs:(i + 1) * bs])
            tot += model(**{k: v.to(device) for k, v in batch.items()}).loss.item()
    model.train()
    return tot / n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--langs", nargs="+", default=["kin", "lug", "swa", "zul"])
    ap.add_argument("--blocks_per_lang", type=int, default=20_000)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=5e-4)
    ap.add_argument("--raw", default="data/raw")
    args = ap.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    random.seed(0)
    torch.manual_seed(0)

    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForMaskedLM.from_pretrained(args.model).to(device)
    for p in model.parameters():
        p.requires_grad = False
    emb = model.get_input_embeddings().weight  # tied to the output layer, so that moves with it
    emb.requires_grad = True

    data = {l: blocks(l, tok, Path(args.raw), args.blocks_per_lang) for l in args.langs}
    print({l: len(v) for l, v in data.items()}, flush=True)
    held = {l: v[:640] for l, v in data.items()}  # held-out blocks for the before/after loss
    train = [b for l in args.langs for b in data[l][640:]]
    random.shuffle(train)
    collate = DataCollatorForLanguageModeling(tok, mlm_probability=0.15)
    collate_ids = lambda xs: collate([{"input_ids": x} for x in xs])

    before = {l: mean_loss(model, held[l], collate_ids, device) for l in args.langs}
    opt = torch.optim.AdamW([emb], lr=args.lr, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 200) * max(0.0, 1 - s / args.steps))
    scaler = torch.amp.GradScaler(device.type, enabled=amp_dtype(device) == torch.float16)
    t0, i = time.time(), 0
    model.train()
    for step in range(args.steps):
        if i + args.bs > len(train):
            random.shuffle(train)
            i = 0
        batch = collate_ids(train[i:i + args.bs])
        i += args.bs
        with torch.autocast(device_type=device.type, dtype=amp_dtype(device) or torch.float32, enabled=amp_dtype(device) is not None):
            loss = model(**{k: v.to(device) for k, v in batch.items()}).loss
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_([emb], 1.0)
        scaler.step(opt)
        scaler.update()
        sched.step()
        opt.zero_grad(set_to_none=True)
        if step % 250 == 0 or step == args.steps - 1:
            print(f"step {step:5d}  loss {loss.item():.3f}  {time.time() - t0:.0f}s", flush=True)
    after = {l: mean_loss(model, held[l], collate_ids, device) for l in args.langs}

    out = Path(args.out)
    model.save_pretrained(out)
    tok.save_pretrained(out)
    cfg = json.loads((out / "config.json").read_text(encoding="utf-8"))
    cfg.pop("transformers_version", None)  # see src/vocab_transfer.py (transformers 4.57.2 local-load bug)
    (out / "config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    stats = dict(model=args.model, steps=args.steps, bs=args.bs, lr=args.lr, blocks_per_lang=args.blocks_per_lang,
                 trained="input embeddings only (tied output layer)", seconds=time.time() - t0,
                 gpu=torch.cuda.get_device_name(0) if device.type == "cuda" else None, amp=str(amp_dtype(device)),
                 heldout_loss_before=before, heldout_loss_after=after)
    (out / "mlm_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
