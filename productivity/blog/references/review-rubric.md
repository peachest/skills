# Subagent Review Rubric

Each subagent receives this rubric alongside the draft and the `technical-writing-best-practices` skill.

## Return format

```
## Review: <Domain>

**File reviewed:** <path>

### Check N: <rule name> — PASS | FAIL | PARTIAL

<evidence: quote the specific passage. If FAIL, state what's wrong and what the fix is.>

### Summary

- Passing: N
- Failing: N
- Partial: N

### Fixes needed (if any)

1. <line/section> — <what to change>
2. ...
```

## Domain: Structure and Flow

Rules to check (from `technical-writing-best-practices` §2):

1. **Thesis spine** — one sentence thesis, every section reinforces it
2. **Directional movement** — each section depends on the previous, pushes forward not sideways
3. **Narrative arc** — problem → pressure → root cause → old model failure → new model → why it works → how to adopt
4. **Transition integrity** — every major handoff answers: why here? loop closed? natural next step?
5. **Architectural integrity** — conclusion resolves the opening tension
6. **Semantic hierarchy** — concept before details, principles before actions
7. **Cognitive pacing** — dense info balanced with simplicity
8. **Signaled level shifts** — mode changes (story→theory, abstract→concrete) explicitly signaled

## Domain: Teaching and Explanation

Rules to check (from `technical-writing-best-practices` §3):

1. **Teaching, not pointing** — every step explains what happens behind it, not just what to do
2. **Decoupled explanation** — concept taught on its own before tool-specific implementation
3. **Mental model anchoring** — new concepts linked to familiar structures
4. **Systemic metaphor** — analogies describe how the system functions, not just what it resembles
5. **Layered insight** — concept → system → implementation, each layer distinct

## Domain: Sentence Craft

Rules to check (from `technical-writing-best-practices` §4):

1. **Reader compression** — one purpose per sentence, no forced rereads
2. **Signal-to-noise density** — no filler ("it's important to note that", "simply", "just")
3. **Parallel logic** — consistent sentence structure when comparing similar ideas
4. **Show, don't stack** — one concrete example beats a list of abstract claims
5. **Fidelity of examples** — real filenames, ports, paths — not hello-world

## Domain: Reasoning and Argument

Rules to check (from `technical-writing-best-practices` §5):

1. **Declarative storytelling** — section headings as outcomes, BLUF opening
2. **Code-backed authority** — claims supported by code, data, or measurable outcomes
3. **Earned solutions** — problem fully established before fix introduced
4. **Thesis integrity** — every section serves the core claim, no interesting tangents

## Blocking vs fix-in-place

- **Blocking** (Structure, Reasoning): the article has a structural or logical defect. Must fix before publishing.
- **Fix-in-place** (Sentence Craft, Teaching): the article is sound but has local issues. Fix at the sentence level.
