#!/usr/bin/env python3
"""Check that every dataset, model and resource in docs/work-plan.md is reachable.

Run once on a machine with internet access (not in a restricted sandbox):

    pip install datasets huggingface_hub transformers
    export HF_TOKEN=hf_...        # optional, needed for gated datasets (e.g. FLORES+)
    python src/check_data_access.py

Writes a table to the terminal and to results/data_access_report.md.
Statuses: PASS (works), WARN (works with a caveat or needs a manual step), FAIL (not reachable).
Nothing large is downloaded: dataset checks load only the small splits listed below,
WURA and MADLAD-400 are checked by listing files only, and the model check loads the tokenizer only.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

TOKEN = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
RESULTS = []  # (resource, status, note)


def add(resource, status, note=""):
    RESULTS.append((resource, status, note))
    print(f"[{status:4}] {resource}: {note}", flush=True)


def http_status(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "peft-data-check"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(200000).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # network down, DNS, timeout
        return None, str(e)


def github_exists(repo):
    code, _ = http_status(f"https://api.github.com/repos/{repo}")
    return code


def github_files(repo, path=""):
    code, body = http_status(f"https://api.github.com/repos/{repo}/contents/{path}")
    if code != 200:
        return code, []
    try:
        return code, [x["name"] for x in json.loads(body)]
    except Exception:
        return code, []


# ---------------------------------------------------------------- environment
try:
    import datasets
    DS_VERSION = datasets.__version__
except Exception:
    datasets = None
    DS_VERSION = None
try:
    from huggingface_hub import HfApi
    API = HfApi(token=TOKEN)
except Exception:
    API = None

print(f"python {sys.version.split()[0]}, datasets {DS_VERSION}, "
      f"huggingface_hub {'ok' if API else 'MISSING'}, HF_TOKEN {'set' if TOKEN else 'not set'}\n")
if datasets is None or API is None:
    add("environment", "FAIL", "install: pip install datasets huggingface_hub transformers")


# ---------------------------------------------------------------- HF datasets
def try_load(repo, config, label, expect_splits=("train", "validation", "test")):
    """Load one config. Tries plain load first, then trust_remote_code for script datasets."""
    if datasets is None:
        return add(label, "FAIL", "datasets library missing")
    err = None
    for kwargs in ({}, {"trust_remote_code": True}):
        try:
            ds = datasets.load_dataset(repo, config, token=TOKEN, **kwargs)
            sizes = {k: len(v) for k, v in ds.items()}
            missing = [s for s in expect_splits if s not in sizes]
            note = ", ".join(f"{k}={v}" for k, v in sizes.items())
            if kwargs:
                note += " (needed trust_remote_code; may break on datasets>=4)"
            if missing:
                return add(label, "WARN", f"missing splits {missing}: {note}")
            return add(label, "WARN" if kwargs else "PASS", note)
        except Exception as e:
            err = e
    short = str(err).replace("\n", " ")[:160]
    add(label, "FAIL", f"{type(err).__name__}: {short}")


SIB = ["amh_Ethi", "hau_Latn", "kin_Latn", "lug_Latn", "swh_Latn", "zul_Latn"]
for c in SIB:
    try_load("Davlan/sib200", c, f"SIB-200 {c}")
for c in ["swa", "lug", "amh", "hau"]:
    try_load("masakhane/masakhanews", c, f"MasakhaNEWS {c}")
for c in ["kin", "lug", "swa", "zul", "hau"]:
    try_load("masakhane/masakhaner2", c, f"MasakhaNER 2.0 {c}")
try_load("masakhane/masakhaner", "amh", "MasakhaNER 1.0 amh")
for c in ["kin", "lug", "swa", "zul", "hau"]:
    try_load("masakhane/masakhapos", c, f"MasakhaPOS {c}")

# FLORES+ (may be gated): report gating, then try one language
if API:
    try:
        info = API.dataset_info("openlanguagedata/flores_plus")
        add("FLORES+ repo", "WARN" if info.gated else "PASS",
            f"gated={info.gated}" + ("; accept terms on the dataset page and set HF_TOKEN" if info.gated else ""))
    except Exception as e:
        add("FLORES+ repo", "FAIL", f"{type(e).__name__}: {str(e)[:140]}")
    for lang in ["amh_Ethi", "hau_Latn", "kin_Latn", "lug_Latn", "swh_Latn", "zul_Latn"]:
        try:
            if datasets is None:
                break
            ds = datasets.load_dataset("openlanguagedata/flores_plus", lang, token=TOKEN)
            add(f"FLORES+ {lang}", "PASS", ", ".join(f"{k}={len(v)}" for k, v in ds.items()))
        except Exception as e:
            add(f"FLORES+ {lang}", "FAIL", f"{type(e).__name__}: {str(e)[:120]} (config name may differ; check the dataset page)")


# ---------------------------------------------------------------- big corpora: list files only
def list_only(repo, label, keys):
    if API is None:
        return add(label, "FAIL", "huggingface_hub missing")
    try:
        files = API.list_repo_files(repo, repo_type="dataset")
        for lang, key in keys.items():
            hits = [f for f in files if key in f.lower()]
            add(f"{label} {lang}", "PASS" if hits else "FAIL",
                f"{len(hits)} files matching '{key}'" if hits else f"no file matching '{key}' (language may be missing)")
    except Exception as e:
        add(label, "FAIL", f"{type(e).__name__}: {str(e)[:140]}")


list_only("castorini/wura", "WURA", {"amh": "amh", "hau": "hau", "kin": "kin", "lug": "lug", "swa": "swa", "zul": "zul"})
if API:
    try:
        info = API.dataset_info("allenai/MADLAD-400")
        add("MADLAD-400 repo", "WARN" if info.gated else "PASS", f"gated={info.gated} (fallback corpus; 6 languages: am, ha, rw, lg, sw, zu)")
    except Exception as e:
        add("MADLAD-400 repo", "FAIL", f"{type(e).__name__}: {str(e)[:140]}")
    try:
        info = API.dataset_info("cis-lmu/Glot500")
        add("Glot500-c repo", "WARN" if info.gated else "PASS", f"gated={info.gated} (second fallback)")
    except Exception as e:
        add("Glot500-c repo", "FAIL", f"{type(e).__name__}: {str(e)[:140]}")

# ---------------------------------------------------------------- model + tokenizer
try:
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Davlan/afro-xlmr-large-76L", token=TOKEN)
    samples = {"amh": "ሰላም ለሁሉም", "swa": "watakujulisha kesho", "zul": "bazobabona kusasa"}
    note = "; ".join(f"{k}: {len(tok.tokenize(v))} tokens" for k, v in samples.items())
    add("AfroXLMR-large-76L tokenizer", "PASS", note)
except Exception as e:
    add("AfroXLMR-large-76L tokenizer", "FAIL", f"{type(e).__name__}: {str(e)[:140]}")

# ---------------------------------------------------------------- GitHub-hosted resources
code, files = github_files("UniversalDependencies/UD_Amharic-ATT")
if code == 200:
    conllu = [f for f in files if f.endswith(".conllu")]
    splits = ", ".join(conllu) or "no .conllu files"
    only_test = conllu and all("test" in f for f in conllu)
    add("UD_Amharic-ATT", "WARN" if only_test or not conllu else "PASS",
        f"{splits}" + ("; only a test file, so you must make your own train/dev/test split" if only_test else ""))
else:
    add("UD_Amharic-ATT", "FAIL", f"GitHub API status {code}")

for name, repo in [("UniMorph amh", "unimorph/amh"), ("UniMorph zul", "unimorph/zul"), ("UniMorph swa", "unimorph/swa"),
                   ("UniMorph kin", "unimorph/kin"), ("UniMorph hau", "unimorph/hau"),
                   ("HornMorpho", "hltdi/HornMorpho"), ("Morfessor", "aalto-speech/morfessor"),
                   ("KinyaBERT repo", "anzeyimana/kinyabert-acl2022"), ("DeepKIN (analyser release?)", "anzeyimana/DeepKIN"),
                   ("Masakhane NER 2.0 repo", "masakhane-io/masakhane-ner"), ("Masakhane POS repo", "masakhane-io/masakhane-pos")]:
    code = github_exists(repo)
    if code == 200:
        extra = ""
        if "kinyabert" in repo:
            extra = "; the analyser inside is closed-source and provided on request"
        add(name, "WARN" if extra else "PASS", f"exists{extra}")
    elif code == 404:
        add(name, "FAIL", "repo not found (resource may not exist for this language)")
    else:
        add(name, "FAIL", f"GitHub API status {code} (rate limit or network)")

# ---------------------------------------------------------------- SADiLaR (needs a manual look at licence/login)
for name, uuid in [("SADiLaR NCHLT isiZulu POS+lemma", "6a64d931-b6d2-4f07-900a-bcd2c7a63670"),
                   ("SADiLaR ZulMorph", "d2e523d3-18b7-410b-b237-694e1f94e535")]:
    code, _ = http_status(f"https://repo.sadilar.org/items/{uuid}")
    add(name, "WARN" if code == 200 else "FAIL",
        "page reachable; open it to check the licence, whether download needs login, and whether it contains MORPHEME boundaries"
        if code == 200 else f"status {code}")

# ---------------------------------------------------------------- report
Path("results").mkdir(exist_ok=True)
lines = ["# Data access report", "", f"datasets {DS_VERSION}, HF_TOKEN {'set' if TOKEN else 'not set'}", "",
         "| Resource | Status | Note |", "|---|---|---|"]
lines += [f"| {r} | {s} | {n.replace('|', '/')} |" for r, s, n in RESULTS]
Path("results/data_access_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
counts = {s: sum(1 for _, x, _ in RESULTS if x == s) for s in ("PASS", "WARN", "FAIL")}
print(f"\nSummary: {counts}. Report written to results/data_access_report.md")
sys.exit(1 if counts["FAIL"] else 0)
