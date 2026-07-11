# AGENTS.md — CoNaIISI 2026 Paper / NLAs + Code Assistants

Instructions for any agent (human or AI) working in this workspace.

## What this project is

Preparation of a **student paper for CoNaIISI 2026** (submission window closes ~28 Aug 2026).

**Core idea (Line C):** study whether LLM-based coding assistants change the **rigor / completeness / security / tests** of their implementations given **contextual signals** about the user or environment (junior vs senior, academic vs production, low vs high review), while keeping **functional requirements constant**.

**Optional / novelty layer:** use **Natural Language Autoencoders (NLAs)** (Anthropic, May 2026) as an exploratory tool to surface assumptions, shortcuts, or omissions in internal activations that do not appear in the final output.

Cautious formulation (avoid attributing intent):

> The model may show patterns of simplification, omission, or greater technical rigor depending on contextual signals that do not explicitly change the functional requirements.

Do not say: “the model decides to be lazy” / “the model *knows* X”.

## Governing principle for NLAs

Working phrase:

> An NLA does not establish the model’s beliefs; it produces **interpretable signals** that, read for **themes** and validated by **behavior** or other tests, support **hypotheses** the output alone does not show.

Operational detail, valid/invalid claims, metrics, and Neuronpedia exploration findings: see **[memory.md](memory.md)** (living document — keep it updated).

## Files to read (suggested order)

| File | Role |
|---|---|
| **[SOUL.md](SOUL.md)** | **Who you are.** Personality, vibe, boundaries. Read every session; tell the user if you change it. |
| **[memory.md](memory.md)** | **What you've learned.** Accumulated knowledge, inferences, how to read AVs, progress. Update when substantive work lands. |
| **[AGENTS.md](AGENTS.md)** | **The job.** This file: project map and working rules. |
| **[research/idea_paper_nla_asistentes_codigo.md](research/idea_paper_nla_asistentes_codigo.md)** | Detailed experimental idea: hypotheses, prompts, rubric, NLA use, titles, CoNaIISI version. (Currently in Spanish.) |
| **[research/contexto_conaiisi_2026_paper.md](research/contexto_conaiisi_2026_paper.md)** | Conference context, lines A/B/C, preliminary decision, next steps, references. (Currently in Spanish.) |
| **[sources/nla/nla_transformer_circuits_2026.md](sources/nla/nla_transformer_circuits_2026.md)** | Local copy of Anthropic’s technical paper (Transformer Circuits). Primary source for citations. |
| **[conference/titulos_estudiantiles_conaiisi_2024.md](conference/titulos_estudiantiles_conaiisi_2024.md)** | 2024 student paper titles (benchmark of what CoNaIISI accepts). |
| `conference/memorias2023.md` / `conference/memorias2024.md` | Full conference proceedings (heavy; use only for targeted precedent search). |

Do not read the full proceedings unless searching for something specific.

## Repo layout

```
.
├── AGENTS.md / SOUL.md / memory.md / README.md   # agent continuity (root)
├── research/     # paper idea & CoNaIISI planning notes
├── sources/nla/  # primary literature (local copies)
└── conference/   # CoNaIISI titles & proceedings dumps
```

## Canonical NLA sources

1. **Paper:** https://transformer-circuits.pub/2026/nla/index.html  
   Local: `sources/nla/nla_transformer_circuits_2026.md`
2. **Anthropic blog:** https://www.anthropic.com/research/natural-language-autoencoders
3. **Code / checkpoints:** https://github.com/kitft/natural_language_autoencoders  
   GitHub handle `kitft`: **Kit Fraser-Taliente** (first author).
4. **HF models:** https://huggingface.co/collections/kitft/nla-models
5. **Demo / API:** https://www.neuronpedia.org/nla (Anthropic + Neuronpedia collaboration; real inference, not a mock)

Related (not a successor): *Cycle-Consistent Activation Oracles* — Sviatoslav Chalnev, LessWrong, March 2026 (concurrent, smaller scale).

## Viable paper scope

- **Safe version:** black-box experiment + software-quality rubric (no NLA runtime).
- **Novel version:** black-box + NLA extension (Neuronpedia and/or open checkpoint, e.g. Qwen 7B; training from scratch is typically out of scope).
- Local hardware (MacBook M4): fine for coding-assistant prototyping; official NLA stack is NVIDIA/SGLang — use cloud or Neuronpedia for the NLA piece.

## How an agent should work here

1. Read `SOUL.md`, then `memory.md`, then this file. Do not reinvent agreed interpretations.
2. Prefer weak, defensible claims (Anthropic style: *suggest*, *NLA-measured*, hypothesis + validation). Strong opinions on process and paper strategy are fine; strong metaphysical claims about model beliefs are not.
3. Do not train NLAs from scratch unless explicitly requested with clear resources.
4. Do not claim verbalizations are literal “thoughts” or beliefs.
5. If the user explores Neuronpedia or other results: log useful findings in `memory.md`.
6. Commits / PRs only when the user asks.
7. Keep **AGENTS.md**, **memory.md**, and **SOUL.md** in **English**. Other idea/context notes may still be Spanish until migrated. Final paper language follows the conference when decided.

## memory.md — living document (continuity across chats)

`memory.md` is the project’s **accumulated memory**: findings, inferences, interpretation criteria, decisions, and knowledge built across agent conversations.

- **Not** a raw dump of every message; a durable synthesis.
- **Every agent that advances the work must update it** when:
  - an important formulation or claim is agreed;
  - an experimental result is interpreted (Neuronpedia, runs, rubric);
  - paper scope changes (black-box only vs +NLA);
  - a useful limit, citation, or precedent is found;
  - a session ends with substantive progress.
- Goal: a new chat **inherits** the intellectual state instead of rediscovering it.
- When updating: date the entry, be concrete, mark **fact / hypothesis / open**.

This is the continuity mechanism across generations of agents.
