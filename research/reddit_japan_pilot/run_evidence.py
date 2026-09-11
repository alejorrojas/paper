#!/usr/bin/env python3
"""Multi-seed Reddit-default evidence for CoNaIISI.

Batteries
  A  community / website / bare slots (completion is the outcome)
  B  no slot; NLA on last user content token (hidden lexeme)

Resume-safe. Writes evidence/cells.jsonl and evidence/summary.json.
"""

from __future__ import annotations

import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://www.neuronpedia.org"
ROOT = Path(__file__).resolve().parent / "evidence"
CELLS = ROOT / "cells.jsonl"
SUMMARY = ROOT / "summary.json"

LLAMA = {"modelId": "llama3.3-70b-it", "nlaSourceId": "kitft-l53", "name": "llama70b"}
GEMMA = {"modelId": "gemma-3-27b-it", "nlaSourceId": "kitft-l41", "name": "gemma27b"}

N_SEEDS_LLAMA = 5
N_SEEDS_GEMMA = 3
COMPLETION_TEMP = 0.4
EXPLAIN_TEMP = 0.7
COMPLETION_TOKENS = 128

REDDIT_RE = re.compile(
    r"(?<![A-Za-z])(reddit(?:\.com)?\b|r/[A-Za-z][A-Za-z0-9_]*)",
    re.I,
)

PROMPTS_A = {
    "p1_community_laptop": (
        "What laptop should a student buy {according to community}?\n"
        "Be brief. Choose yourself where people talk about this."
    ),
    "p2_community_friends": (
        "How do you make friends in a new city {according to community}?\n"
        "Be brief. Choose yourself where people talk about this."
    ),
    "p3_bare_laptop": "What laptop should a student buy?\nBe brief.",
    "p4_website_laptop": (
        "What laptop should a student buy {on website}?\n"
        "Be brief. Choose yourself the website."
    ),
}

# Advice / how-to vs closed factual. Last user token only.
PROMPTS_B = {
    "summarize_for_me": "Summarize this for me",
    "banana_calories": "How many calories does a banana have?",
    "source_of_truth": (
        "Give me a source of truth were I can find information.\n"
        "Respond in one word"
    ),
    "laptop_student": "Recommend a laptop for a student",
    "cook_white_rice": "Explain how to cook white rice",
    "list_10_websites": "Give me a list of 10 websites",
    "ideas_for": "Give me ideas for",
    "email_not_stiff": "Rewrite this email so it sounds professional but not stiff",
    "night_shift_sleep": "How do I get better sleep if I work night shifts?",
    "roth_vs_traditional_ira": (
        "What's the difference between a Roth IRA and a traditional IRA?"
    ),
    "equity_startup_es": 'Qué significa "equity" en una oferta de startup',
    "start_investing": "How should someone start investing?\nBe brief.",
    "friends_new_city": "How do you make friends in a new city?\nBe brief.",
    "learn_python": "I need to learn Python. Help me understand how to start.",
    "cook_pasta": "Explain how to cook spaghetti.",
    "negotiate_salary": "How do I negotiate a salary offer?",
    "running_shoes": "What running shoes should a beginner buy?",
    "cover_letter": "How do I write a cover letter?",
    "study_exams": "How should a student study for final exams?",
    "moved_city": "I just moved to a new city and I don't know anyone.",
    "capital_france": "What is the capital of France?",
    "boiling_water": "At what temperature does water boil at sea level?",
}

ADVICE_IDS = {
    "summarize_for_me",
    "source_of_truth",
    "laptop_student",
    "cook_white_rice",
    "list_10_websites",
    "ideas_for",
    "email_not_stiff",
    "equity_startup_es",
    "start_investing",
    "friends_new_city",
    "learn_python",
    "cook_pasta",
    "negotiate_salary",
    "running_shoes",
    "cover_letter",
    "study_exams",
    "moved_city",
}
FACTUAL_IDS = {
    "banana_calories",
    "night_shift_sleep",
    "roth_vs_traditional_ira",
    "capital_france",
    "boiling_water",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def headers() -> dict[str, str]:
    h = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": BASE,
        "Referer": f"{BASE}/llama3.3-70b-it/nla",
        "User-Agent": "CoNaIISI-reddit-evidence",
    }
    raw = os.environ.get("NEURONPEDIA_API_KEYS", "").strip() or os.environ.get(
        "NEURONPEDIA_API_KEY", ""
    ).strip()
    if raw:
        h["x-api-key"] = raw.split(",")[0].strip()
    return h


def post(path: str, payload: dict, timeout: int = 240) -> dict:
    last: Exception | None = None
    for attempt in range(6):
        req = urllib.request.Request(
            f"{BASE}{path}",
            data=json.dumps(payload).encode(),
            headers=headers(),
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:1500]
            last = RuntimeError(f"HTTP {e.code} {path}: {body}")
            if e.code == 429:
                wait = 65 * 60
                print(f"rate limit hit. sleep {wait}s then retry", flush=True)
                time.sleep(wait)
                continue
            if e.code in (500, 502, 503):
                wait = min(90, 8 * (2**attempt)) + random.random()
                print(f"backoff {e.code} {wait:.0f}s", flush=True)
                time.sleep(wait)
                continue
            raise last from e
        except (TimeoutError, urllib.error.URLError) as e:
            last = e
            time.sleep(min(40, 5 * (attempt + 1)))
    raise last  # type: ignore[misc]


def complete(model: dict, prompt: str) -> dict:
    return post(
        "/api/nla/completion",
        {
            "modelId": model["modelId"],
            "nlaSourceId": model["nlaSourceId"],
            "messages": [{"role": "user", "content": prompt}],
            "completion_tokens": COMPLETION_TOKENS,
            "temperature": COMPLETION_TEMP,
        },
    )


def explain(model: dict, full_text: str, positions: list[int]) -> dict:
    return post(
        "/api/nla/explain",
        {
            "modelId": model["modelId"],
            "nlaSourceId": model["nlaSourceId"],
            "text": full_text,
            "positions": positions,
            "temperature": EXPLAIN_TEMP,
        },
    )


def is_special(tok: str) -> bool:
    t = tok or ""
    if t.startswith("<|") or t.startswith("<"):
        return True
    return t in {
        "assistant",
        "user",
        "system",
        "model",
        "bos",
        "start_of_turn",
        "end_of_turn",
    }


def user_span(tokens: list[dict]) -> list[dict]:
    start = None
    for i, t in enumerate(tokens):
        if (t.get("token") or "") == "user":
            start = i
            break
    if start is None:
        return tokens
    out = []
    for t in tokens[start + 1 :]:
        tok = t.get("token") or ""
        if tok in {"assistant", "model"}:
            break
        out.append(t)
    return out


def last_user_content(tokens: list[dict]) -> dict | None:
    content = [
        t
        for t in user_span(tokens)
        if not is_special(t.get("token") or "") and (t.get("token") or "").strip()
    ]
    return content[-1] if content else None


def mentions_reddit(text: str | None) -> bool:
    return bool(REDDIT_RE.search(text or ""))


def cell_id(model_name: str, battery: str, prompt_id: str, seed: int) -> str:
    return f"{model_name}|{battery}|{prompt_id}|s{seed}"


def load_done() -> set[str]:
    done: set[str] = set()
    if not CELLS.exists():
        return done
    for line in CELLS.read_text().splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        done.add(row["id"])
    return done


def append_cell(row: dict) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    with CELLS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_cell(model: dict, battery: str, prompt_id: str, prompt: str, seed: int) -> dict:
    body = complete(model, prompt)
    full_text = body.get("full_text") or body.get("text") or ""
    tokens = body.get("tokens") or []
    completion = body.get("completion") or ""
    last = last_user_content(tokens)
    nla: dict | None = None
    if last is not None:
        explained = explain(model, full_text, [last["position"]])
        rows = explained.get("results") or explained.get("explanations") or []
        row = rows[0] if rows else {}
        desc = (
            row.get("description")
            or row.get("explanation")
            or row.get("text")
            or row.get("verbalization")
            or ""
        )
        nla = {
            "position": last["position"],
            "token": row.get("token") or last.get("token"),
            "mse": row.get("mse"),
            "cosine_similarity": row.get("cosine_similarity"),
            "description": desc,
        }
    av_text = (nla or {}).get("description") or ""
    return {
        "id": cell_id(model["name"], battery, prompt_id, seed),
        "ts": utc_now(),
        "model": model["name"],
        "modelId": model["modelId"],
        "nlaSourceId": model["nlaSourceId"],
        "battery": battery,
        "prompt_id": prompt_id,
        "prompt": prompt,
        "seed": seed,
        "family": (
            "advice"
            if prompt_id in ADVICE_IDS
            else "factual"
            if prompt_id in FACTUAL_IDS
            else battery
        ),
        "completion": completion,
        "reddit_in_completion": mentions_reddit(completion),
        "reddit_in_av": mentions_reddit(av_text),
        "nla": nla,
    }


def jobs() -> list[tuple[dict, str, str, str, int]]:
    out: list[tuple[dict, str, str, str, int]] = []
    for seed in range(N_SEEDS_LLAMA):
        for pid, prompt in PROMPTS_A.items():
            out.append((LLAMA, "A", pid, prompt, seed))
        for pid, prompt in PROMPTS_B.items():
            out.append((LLAMA, "B", pid, prompt, seed))
    for seed in range(N_SEEDS_GEMMA):
        for pid, prompt in PROMPTS_A.items():
            out.append((GEMMA, "A", pid, prompt, seed))
        for pid, prompt in PROMPTS_B.items():
            out.append((GEMMA, "B", pid, prompt, seed))
    return out


def frac(n: int, d: int) -> float | None:
    return (n / d) if d else None


def summarize() -> dict:
    rows = []
    if CELLS.exists():
        rows = [json.loads(x) for x in CELLS.read_text().splitlines() if x.strip()]

    def slice_rows(model: str, battery: str, family: str | None = None) -> list[dict]:
        s = [r for r in rows if r["model"] == model and r["battery"] == battery]
        if family:
            s = [r for r in s if r.get("family") == family]
        return s

    def pack(label: str, s: list[dict]) -> dict:
        n = len(s)
        n_av = sum(1 for r in s if r.get("reddit_in_av"))
        n_out = sum(1 for r in s if r.get("reddit_in_completion"))
        return {
            "label": label,
            "n": n,
            "reddit_av": n_av,
            "reddit_av_pct": None if not n else round(100 * n_av / n),
            "reddit_completion": n_out,
            "reddit_completion_pct": None if not n else round(100 * n_out / n),
        }

    blocks = []
    for model in ("llama70b", "gemma27b"):
        blocks.append(pack(f"{model} A all", slice_rows(model, "A")))
        for pid in PROMPTS_A:
            s = [r for r in rows if r["model"] == model and r["prompt_id"] == pid]
            blocks.append(pack(f"{model} A {pid}", s))
        blocks.append(pack(f"{model} B all", slice_rows(model, "B")))
        blocks.append(pack(f"{model} B advice", slice_rows(model, "B", "advice")))
        blocks.append(pack(f"{model} B factual", slice_rows(model, "B", "factual")))

    summary = {
        "updated": utc_now(),
        "n_cells": len(rows),
        "n_seeds_llama": N_SEEDS_LLAMA,
        "n_seeds_gemma": N_SEEDS_GEMMA,
        "blocks": blocks,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    done = load_done()
    queue = jobs()
    print(f"queue {len(queue)} done {len(done)}", flush=True)
    for i, (model, battery, pid, prompt, seed) in enumerate(queue, start=1):
        cid = cell_id(model["name"], battery, pid, seed)
        if cid in done:
            continue
        print(f"[{i}/{len(queue)}] {cid}", flush=True)
        try:
            row = run_cell(model, battery, pid, prompt, seed)
        except Exception as e:
            print("FAIL", cid, e, flush=True)
            summarize()
            raise
        append_cell(row)
        done.add(cid)
        print(
            f"  out_reddit={row['reddit_in_completion']} av_reddit={row['reddit_in_av']}",
            flush=True,
        )
        time.sleep(0.4)
        if i % 8 == 0:
            summarize()
    s = summarize()
    print("wrote", CELLS, "n=", s["n_cells"], flush=True)
    for b in s["blocks"]:
        if b["n"] and ("all" in b["label"] or "advice" in b["label"] or "factual" in b["label"]):
            print(
                f"{b['label']}: AV {b['reddit_av']}/{b['n']} ({b['reddit_av_pct']}%) "
                f"out {b['reddit_completion']}/{b['n']} ({b['reddit_completion_pct']}%)",
                flush=True,
            )


if __name__ == "__main__":
    main()
