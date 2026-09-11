#!/usr/bin/env python3
"""Gemma 27B: same 11 Free Chat prompts; NLA on last user content token."""

from __future__ import annotations

import json
import re
from pathlib import Path

import run_pilot as rp

rp.OUT = Path(__file__).resolve().parent / "gemma_freechat11.json"
rp.MODELS = [
    {"modelId": "gemma-3-27b-it", "nlaSourceId": "kitft-l41", "name": "gemma27b"},
]
rp.PROMPTS = {
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
}


def last_user_content_token(tokens: list[dict]) -> dict | None:
    user = rp.user_span_positions(tokens)
    content = [
        t
        for t in user
        if not rp.is_special(t.get("token") or "") and (t.get("token") or "").strip()
    ]
    return content[-1] if content else None


def pick_positions(_prompt_id: str, tokens: list[dict]) -> list[dict]:
    last = last_user_content_token(tokens)
    if last is None:
        return []
    return [
        {
            "label": "user_last",
            "position": last["position"],
            "token": last.get("token"),
        }
    ]


def mentions_reddit(text: str | None) -> bool:
    return bool(re.search(r"reddit", text or "", flags=re.I))


rp.pick_positions = pick_positions  # type: ignore[method-assign]


def summarize(run: dict) -> dict:
    rows = []
    for cell in run["cells"]:
        probe = (cell.get("probes") or [{}])[0]
        desc = probe.get("description") or ""
        completion = cell.get("completion") or ""
        rows.append(
            {
                "prompt_id": cell["prompt_id"],
                "prompt": cell["prompt"],
                "last_token": probe.get("token_api") or probe.get("token_picked"),
                "mse": probe.get("mse"),
                "reddit_in_av": mentions_reddit(desc),
                "reddit_in_completion": mentions_reddit(completion),
                "av_preview": desc[:280],
            }
        )
    n = len(rows)
    n_av = sum(1 for r in rows if r["reddit_in_av"])
    n_out = sum(1 for r in rows if r["reddit_in_completion"])
    return {
        "n": n,
        "reddit_in_av": n_av,
        "reddit_in_av_frac": (n_av / n) if n else None,
        "reddit_in_completion": n_out,
        "reddit_in_completion_frac": (n_out / n) if n else None,
        "rows": rows,
    }


if __name__ == "__main__":
    rp.main()
    run = json.loads(rp.OUT.read_text())
    run["summary"] = summarize(run)
    rp.OUT.write_text(json.dumps(run, indent=2, ensure_ascii=False))
    s = run["summary"]
    print(
        f"Gemma last-user-token Reddit in AV: {s['reddit_in_av']}/{s['n']} "
        f"({s['reddit_in_av_frac']:.0%})",
        flush=True,
    )
    print(
        f"Reddit in completion: {s['reddit_in_completion']}/{s['n']}",
        flush=True,
    )
