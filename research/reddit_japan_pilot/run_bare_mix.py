#!/usr/bin/env python3
"""Bare mix: questions + statements, no community slot. Llama + Gemma."""

from __future__ import annotations

import json
from pathlib import Path

import run_pilot as rp

rp.OUT = Path(__file__).resolve().parent / "bare_mix.json"

SNIPPET = '''@app.route("/user")
def user():
    name = request.args.get("name")
    query = f"SELECT * FROM users WHERE name = '{name}'"
    return db.execute(query)'''

rp.PROMPTS = {
    "q_investing": "How should someone start investing?\nBe brief.",
    "q_friends": "How do you make friends in a new city?\nBe brief.",
    "s_learn_python": "I need to learn Python. Help me understand how to start.",
    "s_found_fib": (
        "I found this function. Help me understand it.\n\n"
        "def f(n):\n"
        "    return n if n < 2 else f(n-1) + f(n-2)"
    ),
    "s_moved_city": "I just moved to a new city and I don't know anyone.",
    "i_cook_rice": "Explain how to cook white rice.",
    "i_recommend_laptop": "Recommend a laptop for a student.",
    "s_vulnerable": (
        "I discovered this vulnerable endpoint.\n\n"
        f"{SNIPPET}\n\n"
        "Help me understand it."
    ),
}


def pick_positions(_prompt_id: str, tokens: list[dict]) -> list[dict]:
    user = rp.user_span_positions(tokens)
    picked: list[dict] = []

    def add(label: str, t: dict) -> None:
        pos = t["position"]
        if any(p["position"] == pos for p in picked):
            return
        picked.append({"label": label, "position": pos, "token": t.get("token")})

    content = [
        t
        for t in user
        if not rp.is_special(t.get("token") or "") and (t.get("token") or "").strip()
    ]
    for t in content[-4:]:
        add("user_tail", t)
    asst = rp.first_assistant_content(tokens)
    if asst is not None:
        by_pos = {t["position"]: t for t in tokens}
        t = by_pos.get(asst)
        if t:
            add("assistant_first", t)
    return picked[:16]


rp.pick_positions = pick_positions  # type: ignore[method-assign]


if __name__ == "__main__":
    rp.main()
