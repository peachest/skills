# Report structure

**Leading words:** _What_, _How_, _So What_, _Now What_ — the four layers of a research report. Each answers one question and builds on the layer before; skipping one leaves facts without a path to action.

A report that dumps findings without structure forces the reader to do the synthesis themselves. The four layers move the reader from understanding → capability → relevance → action. Not every report needs all four at full depth — a tool survey leans on _How_, a cost model on _What_ — but every report touches all four. A missing layer is a gap to flag, not a section to skip silently; match depth to the question, never drop a layer without a one-line reason.

## Two report kinds

The research skill produces two kinds of report:

- **Direction report** (`NN-slug.md`) — one per research direction. Covers only **What**, **How**, and key findings, each claim cited to its source. It stops before **So What** / **Now What**: those layers need the commissioning context (audience, constraints, success criteria) that only the main session holds, and a direction subagent writing them in isolation would hallucinate.
- **Synthesis** (`00-summary.md`) — one per research topic. Covers **all four layers**, reconciling contradictions across directions, and opens with a direction index.

The four layers below apply in full to the synthesis; a direction report touches the first two and flags findings without leaping to team impact or action.

---

## 1. What — model & modeling

The model, framework, or quantitative relationship that describes the problem.

- Problem definition + mathematical model / formulas
- Quantitative data (metrics, benchmarks, cost figures)
- Comparison with alternative approaches

**⚠️ Assumptions & constraints** — state them explicitly. Every model hides premises: a queueing formula may assume steady-state arrival, a forecasting model may assume historical patterns continue, a capacity model may assume a known service-time distribution. Unstated assumptions read as truth. Name the premise, then note when it holds and when it breaks.

**Sensitivity analysis** — which variable is most dangerous? If a key input moves 20%, does the conclusion flip? Test the one or two variables whose uncertainty could reverse the finding; a model that survives a sensitivity test is worth acting on, one that doesn't is worth hedging.

## 2. How — methodology & tools

How to measure, build, or apply the model in practice.

- Tool selection & comparison
- Installation, configuration, code examples
- Best practices

## 3. So What — team impact

What the findings mean for the team that commissioned the research.

- Relevance to the team's context — their infrastructure, workflows, constraints
- Current state vs target state — where are we, where should we be
- Risks & opportunities

## 4. Now What — next steps

What to do about it.

- Action items, prioritized
- **Dependency chain** — A → B → C ordering. Some actions can't start until another finishes: can't price by goodput without first measuring goodput; can't do chargeback without per-request token metering. Make the ordering explicit so no one blocks on a missing prerequisite.
- **Success criteria** — KPI + threshold for each action, so done is distinguishable from not-done.
- Implementation roadmap (Crawl → Walk → Run)
