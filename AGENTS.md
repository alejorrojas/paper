# AGENTS.md — CoNaIISI 2026 Paper / NLAs

Instructions for any agent (human or AI) working in this workspace.

## Lab culture

This is an **exploration lab**, not a pre-review committee.

- Follow interesting ideas. Sketch titles, analogies, experiments. Count later.
- Punchy framing is welcome (*Obsessed with Japanese Culture* is the energy).
- Don't make us ridiculous: no invented numbers, no “we proved Reddit trained every LLM” from three AVs, no leaking keys.
- Don't open a new idea by explaining why CoNaIISI would reject it.
- Read AVs for **themes**, not isolated magic words. Curiosity first; honesty about the instrument is how we stay serious without being small.

## What this project is

Preparation of a **student paper for CoNaIISI 2026** (student/research submission closes **14 Sep 2026**; official dates extended).

**Live idea (2026-09-11):** **NLASmith** — LangSmith-style experiment harness for public NLAs (Neuronpedia API + LLM judge on AVs, token policy, compare). **User-final student paper:** [`research/NLASmith_conaiisi_2026.md`](research/NLASmith_conaiisi_2026.md). Reddit/forums-as-default is lab history / optional demo, not the claim. Previous Line C / ladder / lookahead stay in `memory.md` as history.

## Governing principle for NLAs

Working phrase:

> An NLA does not establish the model’s beliefs; it produces **interpretable signals** that, read for **themes** and validated by **behavior** or other tests, support **hypotheses** the output alone does not show.

That is a rule about **not lying**. It is not a rule against bold hypotheses or loud titles.

Operational detail, metrics, and past runs: **[memory.md](memory.md)**.

## Files to read (suggested order)

| File | Role |
|---|---|
| **[SOUL.md](SOUL.md)** | **Who you are.** Personality, vibe. Read every session; tell the user if you change it. |
| **[memory.md](memory.md)** | **What you've learned.** Lab notebook. |
| **[AGENTS.md](AGENTS.md)** | **The job.** This file. |
| **[research/NLASmith_conaiisi_2026.md](research/NLASmith_conaiisi_2026.md)** | **User-final CoNaIISI paper (NLASmith).** |
| **[sources/nla/nla_transformer_circuits_2026.md](sources/nla/nla_transformer_circuits_2026.md)** | Anthropic NLA paper. |
| **[sources/japan_culture_bias_llms_2026.mdx](sources/japan_culture_bias_llms_2026.mdx)** | Japan-default paper (local extract). Lab analog / history. |
| **[research/contexto_conaiisi_2026_paper.md](research/contexto_conaiisi_2026_paper.md)** | Conference context (Spanish; partly stale vs live idea). |
| **[research/paper_nla_eval_conaiisi_2026.md](research/paper_nla_eval_conaiisi_2026.md)** | Older NLA Eval draft (superseded by NLASmith). |
| **[research/idea_paper_nla_asistentes_codigo.md](research/idea_paper_nla_asistentes_codigo.md)** | Old Line C idea (history). |
| **[conference/titulos_estudiantiles_conaiisi_2024.md](conference/titulos_estudiantiles_conaiisi_2024.md)** | What CoNaIISI student tracks have looked like. |

Do not read the full `conference/memorias*.md` unless searching for something specific.

## Repo layout

```
.
├── AGENTS.md / SOUL.md / memory.md / README.md   # agent continuity (root)
├── research/     # paper idea & CoNaIISI planning notes
├── sources/      # literature extracts (NLA, Japan-bias paper)
└── conference/   # CoNaIISI titles & proceedings dumps
```

## Canonical NLA sources

1. **Paper:** https://transformer-circuits.pub/2026/nla/index.html  
   Local: `sources/nla/nla_transformer_circuits_2026.md`
2. **Anthropic blog:** https://www.anthropic.com/research/natural-language-autoencoders
3. **Code / checkpoints:** https://github.com/kitft/natural_language_autoencoders  
   GitHub handle `kitft`: **Kit Fraser-Taliente** (first author).
4. **HF models:** https://huggingface.co/collections/kitft/nla-models
5. **Demo / API:** https://www.neuronpedia.org/nla

Related (not a successor): *Cycle-Consistent Activation Oracles* — Sviatoslav Chalnev, LessWrong, March 2026.

Japan analog: arXiv:2604.21751 — local `sources/japan_culture_bias_llms_2026.mdx`.

## Scope notes

- Neuronpedia (Llama 70B L53, Gemma 27B, …) is the default NLA instrument. Don't train NLAs from scratch unless asked with clear resources.
- MacBook M4 is fine for scripts and writing; the official NLA stack is NVIDIA/SGLang.
- Keep probes short enough to look at. Diversify prompts when testing a “default” (not only SQLi).

## How an agent should work here

1. Read `SOUL.md`, then `memory.md`, then this file.
2. Explore. Log hunches as hunches. Don't wait for a locked design to get curious.
3. Don't pretend AVs are literal thoughts. Don't shrink a live hypothesis into a methods footnote before we try it.
4. Commits / PRs only when the user asks.
5. Keep **AGENTS.md**, `memory.md`, and `SOUL.md` in **English**. Other notes may stay Spanish. Final paper language follows the conference when decided.
6. If you change `SOUL.md`, tell the user.

## memory.md — living document

`memory.md` is accumulated memory: findings, inferences, decisions — not a dump of every chat.

Update it when a formulation is agreed, a run is interpreted, scope shifts, or a session actually moved the work. Date entries. Mark **fact / hypothesis / open**.

This is how a new chat inherits the intellectual state.
