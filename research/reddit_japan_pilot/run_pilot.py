#!/usr/bin/env python3
"""Reddit-as-Japan pilot: 4 prompts × Llama 70B + Gemma 27B."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from itertools import cycle
from pathlib import Path

BASE = "https://www.neuronpedia.org"
OUT = Path(__file__).resolve().parent / "run.json"

MODELS = [
    {"modelId": "llama3.3-70b-it", "nlaSourceId": "kitft-l53", "name": "llama70b"},
    {"modelId": "gemma-3-27b-it", "nlaSourceId": "kitft-l41", "name": "gemma27b"},
]

PROMPTS = {
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

SLOT_NEEDLES = (
    "community",
    "website",
    "according",
    "people",
    "talk",
    "{",
    "}",
    "where",
    "choose",
)


def key_cycle():
    raw = os.environ.get("NEURONPEDIA_API_KEYS", "").strip()
    keys = [k.strip() for k in raw.split(",") if k.strip()]
    if not keys:
        raise SystemExit("set NEURONPEDIA_API_KEYS")
    return cycle(keys)


KEYS = key_cycle()


def headers() -> dict[str, str]:
    h = {"Content-Type": "application/json", "Accept": "application/json"}
    h["x-api-key"] = next(KEYS)
    return h


def post(path: str, payload: dict, timeout: int = 240) -> dict:
    last = None
    for attempt in range(3):
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
            if e.code in (429, 500, 502, 503):
                continue
            raise last from e
        except TimeoutError as e:
            last = e
    raise last  # type: ignore[misc]


def complete(model: dict, prompt: str) -> dict:
    return post(
        "/api/nla/completion",
        {
            "modelId": model["modelId"],
            "nlaSourceId": model["nlaSourceId"],
            "messages": [{"role": "user", "content": prompt}],
            "completion_tokens": 128,
            "temperature": 0.4,
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
            "temperature": 0.7,
        },
    )


def is_special(tok: str) -> bool:
    t = tok or ""
    if t.startswith("<|") or t.startswith("<"):
        return True
    return t in {"assistant", "user", "system", "model", "bos", "start_of_turn", "end_of_turn"}


def first_assistant_content(tokens: list[dict]) -> int | None:
    last_header = None
    for i, t in enumerate(tokens):
        tok = t.get("token") or ""
        if tok in {"assistant", "model"}:
            last_header = i
    if last_header is None:
        return None
    for t in tokens[last_header + 1 :]:
        tok = t.get("token") or ""
        if is_special(tok) or not (tok or "").strip():
            continue
        return t["position"]
    return None


def user_span_positions(tokens: list[dict]) -> list[dict]:
    """User message tokens: after the *first* 'user' header, until assistant/model."""
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


def pick_positions(prompt_id: str, tokens: list[dict]) -> list[dict]:
    """Return list of {label, position, token} to explain."""
    user = user_span_positions(tokens)
    picked: list[dict] = []

    def add(label: str, t: dict) -> None:
        pos = t["position"]
        if any(p["position"] == pos for p in picked):
            return
        picked.append(
            {"label": label, "position": pos, "token": t.get("token")}
        )

    if prompt_id != "p3_bare_laptop":
        for t in user:
            low = (t.get("token") or "").lower()
            if any(n in low for n in SLOT_NEEDLES):
                add("user_slot", t)
    else:
        content = [
            t
            for t in user
            if not is_special(t.get("token") or "")
            and (t.get("token") or "").strip()
        ]
        for t in content[-4:]:
            add("user_tail", t)

    asst = first_assistant_content(tokens)
    if asst is not None:
        by_pos = {t["position"]: t for t in tokens}
        t = by_pos.get(asst)
        if t:
            add("assistant_first", t)

    return picked[:16]


def main() -> None:
    run = {
        "models": MODELS,
        "prompts": PROMPTS,
        "cells": [],
    }
    for model in MODELS:
        for pid, prompt in PROMPTS.items():
            print(f"=== {model['name']} {pid} complete ===", flush=True)
            body = complete(model, prompt)
            full_text = body.get("full_text") or body.get("text") or ""
            tokens = body.get("tokens") or []
            completion = body.get("completion") or ""
            print(completion[:350], flush=True)
            probes = pick_positions(pid, tokens)
            positions = [p["position"] for p in probes]
            print("probes", probes, flush=True)
            explained = {"results": []}
            if positions:
                explained = explain(model, full_text, positions)
            by_pos = {row["position"]: row for row in explained.get("results") or []}
            nla = []
            for p in probes:
                row = by_pos.get(p["position"]) or {}
                nla.append(
                    {
                        "label": p["label"],
                        "position": p["position"],
                        "token_picked": p["token"],
                        "token_api": row.get("token"),
                        "mse": row.get("mse"),
                        "cosine_similarity": row.get("cosine_similarity"),
                        "description": row.get("description"),
                    }
                )
            run["cells"].append(
                {
                    "model": model["name"],
                    "modelId": model["modelId"],
                    "nlaSourceId": model["nlaSourceId"],
                    "prompt_id": pid,
                    "prompt": prompt,
                    "completion": completion,
                    "probes": nla,
                }
            )
            OUT.write_text(json.dumps(run, indent=2, ensure_ascii=False))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
