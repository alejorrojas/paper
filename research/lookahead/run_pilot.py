#!/usr/bin/env python3
"""One-shot lookahead pilot: tenth_fib on Neuronpedia Llama 70B NLA."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://www.neuronpedia.org"
MODEL_ID = "llama3.3-70b-it"
SOURCE_ID = "kitft-l53"
PROMPT = (
    "Write only a Python function tenth_fib() that returns the 10th "
    "Fibonacci number (1-indexed). No comments, no explanation."
)
OUT = Path(__file__).resolve().parent / "pilot_n1.json"


def headers() -> dict[str, str]:
    h = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Origin": BASE,
        "Referer": f"{BASE}/{MODEL_ID}/nla",
        "User-Agent": "CoNaIISI-lookahead-pilot",
    }
    key = os.environ.get("NEURONPEDIA_API_KEY", "").strip()
    if key:
        h["x-api-key"] = key
    return h


def post(path: str, payload: dict, timeout: int, accept: str | None = None) -> str:
    hdrs = headers()
    if accept:
        hdrs["Accept"] = accept
    data = json.dumps(payload).encode()
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=hdrs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:2500]
        raise RuntimeError(f"HTTP {e.code} {path}: {body}") from e


def complete(prompt: str) -> str:
    payload = {
        "modelId": MODEL_ID,
        "nlaSourceId": SOURCE_ID,
        "messages": [{"role": "user", "content": prompt}],
        "completion_tokens": 256,
        "temperature": 0.4,
        "stream": True,
    }
    raw = post("/api/nla/completion", payload, timeout=240, accept="text/event-stream")
    pieces: list[str] = []
    for line in raw.splitlines():
        if not line.startswith("data: "):
            continue
        data = line[6:].strip()
        if data in ("[DONE]", ""):
            continue
        obj = json.loads(data)
        if obj.get("error"):
            raise RuntimeError(f"stream error: {obj['error']}")
        tok = obj.get("token")
        if obj.get("type") == "token" and isinstance(tok, dict):
            pieces.append(tok.get("token") or "")
        elif isinstance(tok, str):
            pieces.append(tok)
    text = "".join(pieces).strip()
    if not text:
        raise RuntimeError(f"empty completion head={raw[:500]!r}")
    return text


def tokenize(messages: list[dict]) -> dict:
    raw = post(
        "/api/nla/completion",
        {
            "modelId": MODEL_ID,
            "nlaSourceId": SOURCE_ID,
            "messages": messages,
            "completion_tokens": 0,
            "add_generation_prompt": False,
        },
        timeout=120,
    )
    return json.loads(raw)


def explain(full_text: str, positions: list[int]) -> dict:
    raw = post(
        "/api/nla/explain",
        {
            "modelId": MODEL_ID,
            "nlaSourceId": SOURCE_ID,
            "text": full_text,
            "positions": positions,
            "temperature": 0.7,
        },
        timeout=240,
    )
    return json.loads(raw)


def assistant_content(tokens: list[dict]) -> list[dict]:
    out = []
    for t in tokens:
        if t.get("role") != "assistant":
            continue
        if t.get("section") not in (None, "content"):
            if t.get("section") != "content":
                continue
        tok = t.get("token") or ""
        if tok.startswith("<|"):
            continue
        out.append(t)
    return out


def pick_probe_positions(asst: list[dict]) -> tuple[list[int], dict]:
    """Probe signature / first body tokens before any '55' appears."""
    first_55 = None
    for t in asst:
        if "55" in (t.get("token") or ""):
            first_55 = t["position"]
            break
    pre = [t for t in asst if first_55 is None or t["position"] < first_55]
    wanted = []
    seen_def = False
    for t in pre:
        tok = t.get("token") or ""
        pos = t["position"]
        if "def" in tok:
            seen_def = True
            wanted.append(pos)
            continue
        if not seen_def:
            continue
        if re.search(r"[A-Za-z0-9:_\n()]", tok) or tok in (":", "\n", ":\n"):
            wanted.append(pos)
        if len(wanted) >= 12:
            break
    if not wanted and pre:
        wanted = [t["position"] for t in pre[:8]]
    meta = {
        "first_55_position": first_55,
        "n_assistant_tokens": len(asst),
        "n_pre_55": len(pre),
        "probed": wanted,
    }
    return wanted, meta


def av_mentions_55(text: str) -> bool:
    return bool(re.search(r"\b55\b", text or ""))


def main() -> None:
    print("=== completion ===", flush=True)
    completion = complete(PROMPT)
    print(completion)
    print("=== tokenize ===", flush=True)
    messages = [
        {"role": "user", "content": PROMPT},
        {"role": "assistant", "content": completion},
    ]
    tokenized = tokenize(messages)
    full_text = tokenized.get("text") or tokenized.get("full_text") or ""
    tokens = tokenized.get("tokens") or []
    asst = assistant_content(tokens)
    preview = [
        {"position": t["position"], "token": t.get("token")}
        for t in asst[:40]
    ]
    print("assistant token preview:", json.dumps(preview, ensure_ascii=False))
    positions, meta = pick_probe_positions(asst)
    print("probe meta:", meta, flush=True)
    if not positions:
        raise SystemExit("no probe positions")
    print("=== explain", positions, "===", flush=True)
    explained = explain(full_text, positions)
    rows = explained.get("explanations") or explained.get("results") or explained
    if isinstance(rows, dict):
        rows = rows.get("explanations") or [rows]
    slim = []
    if isinstance(rows, list):
        for row in rows:
            av = (
                row.get("description")
                or row.get("explanation")
                or row.get("text")
                or row.get("verbalization")
                or ""
            )
            mse = row.get("mse") if "mse" in row else row.get("rmse") or row.get("confidence")
            slim.append(
                {
                    "position": row.get("position"),
                    "token": row.get("token"),
                    "mse": mse,
                    "mentions_55": av_mentions_55(av),
                    "av": av,
                }
            )
    else:
        slim = [{"raw_keys": list(explained)[:30], "sample": str(explained)[:1500]}]
    result = {
        "modelId": MODEL_ID,
        "nlaSourceId": SOURCE_ID,
        "prompt": PROMPT,
        "prompt_contains_55": "55" in PROMPT,
        "completion": completion,
        "completion_contains_55": "55" in completion,
        "probe": meta,
        "assistant_token_preview": preview,
        "nla": slim,
        "explain_keys": list(explained) if isinstance(explained, dict) else type(explained).__name__,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print("wrote", OUT)
    hits = [r for r in slim if isinstance(r, dict) and r.get("mentions_55")]
    print("HIT_55_IN_AV", len(hits), "of", len(slim))


if __name__ == "__main__":
    main()
