# NLA Eval Lab — LangSmith for activation verbalizations

Status: **locked CoNaIISI main line** (2026-09-10). Draft: `research/paper_nla_eval_conaiisi_2026.md`.

**Locked paper sentence (2026-09-10, user):** Anthropic already grades NLA verbalizations with an LLM judge, but only as a method inside their paper. Traditional LLM *outputs* have a formal eval stack (LangSmith: experiment, evaluator, compare charts). NLAs do not. We propose the analogous tool: judge the **AV**, not the completion, and show the same comparison view.

Working English title energy:

> LangSmith for thoughts: an experiment harness for Natural Language Autoencoders

Spanish hook options:

- Un LangSmith para verbalizaciones NLA
- Evaluar lo que el modelo no dice: un laboratorio de experimentos NLA
- Evaluators para Activation Verbalizers

## Problem (fact we already hit)

Neuronpedia Free Chat is a microscope, not a lab.

- One prompt, one model, one tab.
- Explain is capped at 16 token positions per request.
- Comparing Llama vs Gemma, or 11 prompts, meant scripts + JSON + screenshots.
- The interesting claim is never a single AV sentence. It is a **rate**: how often does the last user token mention Reddit, cyber risk, eval, forum, while the completion does not.

The NLA paper already uses **graders on AVs** (eval-awareness: 50 random response tokens, LLM grader, human agreement 97% on 186 items). That is a research one-off. EasyNLA’s optional LLM judges score **training quality** (coherence, uniqueness, writing), not experimental hypotheses.

LangSmith evaluates **completions**. It has code evaluators, LLM-as-judge (reference-free and reference-based), pairwise, comparison view, charts by experiment metadata. It does not know tokens, residual-stream layers, RMSE, or AVs.

## What we would actually ship

Not a new interpretability method. A **run + judge + compare** layer on top of the Neuronpedia NLA API.

### Objects

| LangSmith | Ours |
|---|---|
| Dataset of prompts | Same |
| Target = agent / chain | Target = `completion` + `explain` at a **token policy** |
| Output text | Artifact = `{completion, AVs[], mse[], token_ids}` |
| Golden output | Optional golden **theme labels** or a **rule prompt** (Reddit? risk? eval?) |
| Feedback keys | `reddit_lexeme`, `judge_reddit`, `judge_cyber_risk`, `omission` (AV yes / completion no), mean MSE |
| Compare experiments | Llama L53 vs Gemma L41; register informal vs expert; last-user vs first-assistant |

### Token policy (locked default, overridable)

What we already do by hand:

1. Last **content** token of the user message.
2. First token of the assistant completion.

Optional later: last assistant token, named lexemes (`unauthorized`, `Reddit`).

Filter: drop AVs with MSE above a threshold (~0.5 UI RMSE) so the judge is not scoring garbage reconstructions.

### Evaluator types (v1)

1. **Code / lexeme.** Case-insensitive substring (`reddit`, `sql injection`, `evaluation`). Cheap, honest, not a theme.
2. **LLM-as-judge, reference-free.** Rubric on the AV only: “Does this verbalization mention a forum/Reddit-like community as the implied context?” Boolean + short reason.
3. **LLM-as-judge, reference-based.** Human-labeled golden labels on a small set; judge scores closeness. Or pairwise: which AV is closer to the golden theme.
4. **Omission evaluator (the NLA-specific one).** Code or judge on the pair `(completion, AV)`. Hit = theme in AV, absent in completion. This is the analog of Anthropic’s verbalized vs NLA-measured awareness. LangSmith has no first-class type for this.

### UI (copy LangSmith, thin)

- Dataset: list of prompts + metadata (register, language, community-slot yes/no).
- Run experiment: source (Llama 70B kitft-l53 / Gemma 27B kitft-l41), token policy, N, temperature.
- Experiment table: per example, completion snippet, AV text, MSE, feedback columns.
- Compare: two experiments, bar charts of hit rates per evaluator, thumbs on pairwise judge.
- Drill-down: one row → full AV + Neuronpedia-style token chips.

Backend: Neuronpedia `/api/nla/completion` + `/api/nla/explain`. Judge via any cheap chat API. Rate limits (~120 explain/h) are part of the paper’s methods, not a surprise.

## Demo suite (the paper needs one real run)

The Reddit-as-default prompts we already have **are** the golden-ish suite. The tool is how we stop treating 11 screenshots as a lab.

Minimum figure for CoNaIISI:

- X axis: prompt family (advice / how-to / encyclopedic / Spanish).
- Grouped bars: Llama vs Gemma.
- Two metrics: lexeme Reddit in AV; judge “forum prior”; plus omission vs completion.

Cyber risk / intent-ladder prompts can be a second evaluator on the same harness, not a second paper.

## Claims we can write vs cannot

| Write | Do not |
|---|---|
| Neuronpedia is for inspection; batch hypothesis testing needs an eval loop | We invented NLA evaluation |
| LLM-as-judge on AVs is the same move Anthropic used for eval awareness, productized for open models | The judge reads the model’s beliefs |
| On our suite, Llama last-user AVs hit forum/Reddit at rate X; Gemma at Y | All LLMs are trained on Reddit |
| Omission rate is the extra signal vs black-box | Low MSE ⇒ the sentence is true |

## Scope for 14 Sep 2026

Four days: a **working MVP + one comparison figure**, not a LangSmith clone.

Must have: dataset JSON, runner, two evaluators (lexeme + judge), two models, comparison HTML or Next.js page, methods in the paper.

Nice: pairwise, golden labels, charts by metadata, deploy.

Kill: training NLAs, custom judges for FVE, full-transcript explain.

## Analog honesty

LangSmith is “just an LLM call + charts.” So is this. The contribution is the **evaluation object** (AV @ token + RMSE + omission vs completion) and making that loop runnable on public NLAs.
