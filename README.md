# CoNaIISI 2026 — NLAs & Code Assistants

Student research workspace for a paper on whether LLM coding assistants change implementation rigor under contextual signals (user/environment), with **Natural Language Autoencoders (NLAs)** as an optional interpretability layer.

An AI helping humans understand AI — carefully.

## Start here

| File | What it is |
|------|------------|
| [SOUL.md](SOUL.md) | Assistant identity (research vibe, epistemic rules) |
| [memory.md](memory.md) | Living lab notebook — findings, claims, Neuronpedia notes |
| [AGENTS.md](AGENTS.md) | Project map, sources, how agents should work |

## Layout

```
.
├── AGENTS.md / SOUL.md / memory.md / README.md
├── research/          # idea notes & CoNaIISI planning
├── sources/nla/       # primary literature (local copies)
└── conference/        # titles & proceedings dumps
```

## Core idea

Keep functional requirements fixed. Vary only contextual signals (junior vs senior, academic vs production, etc.). Measure code quality with a rubric. Optionally compare black-box outputs with NLA verbalizations of internal activations.

**Governing claim style:** NLAs produce interpretable *signals*, not proof of what a model “knows.”

## Key sources

- Paper: https://transformer-circuits.pub/2026/nla/index.html (local: [`sources/nla/nla_transformer_circuits_2026.md`](sources/nla/nla_transformer_circuits_2026.md))
- Blog: https://www.anthropic.com/research/natural-language-autoencoders
- Code/checkpoints: https://github.com/kitft/natural_language_autoencoders
- Demo: https://www.neuronpedia.org/nla

## Conference

[CoNaIISI 2026](https://conaiisi2026.frre.utn.edu.ar/) — student paper track; submission closes ~28 Aug 2026.

See [`conference/`](conference/) for prior-year titles and proceedings.

## Repo notes

- Idea/context drafts in `research/` may still be in Spanish; agent continuity docs at the root are in English.
- `conference/memorias*.md` are large — don’t load them whole unless searching.
