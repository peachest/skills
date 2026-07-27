# Review — `/fix` against `writing-great-skills`

**Overall verdict:** A well-structured, mostly-predictable step skill that fails on one architectural axis (Invocation) and carries several Single-Source-of-Truth / Duplication leaks between `SKILL.md` and `CLASSIFICATION.md`; fixable in a focused pass.

Reference framework: `writing-great-skills` (`SKILL.md` + `GLOSSARY.md`). Bold terms below are **GLOSSARY.md** terms, used by name.

---

## 1. Predictability — WARN

The skill wrangles determinism well at the macro level: a fixed seven-step **Steps** sequence, a stated defining failure ("Verify before grill, grill before fix — inverting this order is the skill's defining failure", `SKILL.md:11`), enumerated verdicts, and a disclosed decision tree. The ordered triad *verify → grill → fix* is a strong **Leading Word** anchor on execution order.

Two variance leaks:

- **Step 3 offers three undated reproduction options** (`SKILL.md:69`): "reproduce it — run the code path, write a quick test, or trace the logic by hand." These are presented as a flat OR with no gating, so the agent picks whichever it reaches first run-to-run. A **Branch** this central to the skill's identity (verify-before-fix) should be gated: e.g. "Run the code path if reachable; otherwise write a test; if neither applies, trace by hand." That makes the *process* the same every run even when the *technique* must vary.
- **Step 6 is Go-default with a soft adapt clause** (`SKILL.md:121-124`): `go vet ./... && go build ./... && go test ./...` then "Adapt the command to the project's language if not Go." The adaptation is unguided, so the verify step is predictably Go-shaped and unpredictably everything else. Either disclose a small per-language command table (a **Reference** peer-set) or state the detection rule ("detect from `go.mod` / `package.json` / `Cargo.toml`…").

Not a failure of **Predictability** at the process level, but the two soft branches above are where run-to-run behaviour diverges.

---

## 2. Invocation — FAIL (headline)

`disable-model-invocation: true` (`SKILL.md:4`) is inconsistent with how the skill is consumed.

- `triage-mr/SKILL.md` is itself `disable-model-invocation: true` (i.e. **User-Invoked**) and its Step 2 says "Pass `/tmp/issues.json` to `/fix`. The `/fix` skill runs its full process" (`triage-mr/SKILL.md`, Step 2), with a Checkpoints table whose rows 2–5 are all "During `/fix` Step N". So `/triage-mr` (another skill) must reach `/fix`.
- Per **GLOSSARY.md** → **User-Invoked**: "nothing but the human can reach it: no other skill can fire it"; and **Model-Invoked**: "reachable by other skills, because the **Description** that makes it agent-discoverable makes it invocable." A skill that another skill delegates to must be **Model-Invoked**. The framework's own test — "Pick model-invocation only when… another skill must reach it" — is met here. `/fix` is reached by `/triage-mr`; therefore `/fix` should keep its **Description** and drop `disable-model-invocation`.

The internal inconsistency is visible right in the frontmatter: the `description` (`SKILL.md:3`) is written *as a model-facing trigger* ("Use when review comments, bug reports, or static analysis findings need triage…") — trigger phrasing that, per **GLOSSARY.md** → **Description**, only belongs on a **Model-Invoked** skill ("set `disable-model-invocation: true`; the `description` becomes human-facing — a one-line summary, trigger lists stripped"). So the flag says user-invoked, the description is authored for model-invocation. They disagree.

**Suggestion:** set `disable-model-invocation: false` (or remove the line) and keep a model-facing description. The **Context Load** cost is justified because `/triage-mr` reaches `/fix` on its own — exactly the case the framework licenses model-invocation for.

If the intent is genuinely that `/fix` only ever fires by hand and `/triage-mr` merely stages the input file for a *separate* human `/fix` invocation, then keep the flag but (a) strip the "Use when…" trigger clause from the description, and (b) rewrite `/triage-mr` Step 2 so it does not claim to delegate. The current state — flag says user-invoked, description says model-invoked, consumer says it delegates — satisfies none of the three cleanly.

---

## 3. Information Hierarchy — WARN

Tiering is mostly right: **Steps** (Process, `SKILL.md:46-132`) are the primary tier in-file; the decision tree is **Progressive Disclosure** behind a **Context Pointer** to `CLASSIFICATION.md` (`SKILL.md:44`); the report template is disclosed to `REPORT.md` (`SKILL.md:130`); the `classified.json` schema is inlined as **Reference** (`SKILL.md:142-156`), which is fine — it is compact, single-output, and needed at Step 7.

Three concerns:

1. **The decision tree is must-have material behind a pointer.** `CLASSIFICATION.md` opens "Consulted during Step 2 (recommend) and Step 3 (verify)" — i.e. every classification run needs it. Per **GLOSSARY.md** → **Context Pointer**: "A must-have target behind a weakly worded pointer is a variance bug… pull it back inline only if [sharpening] fails." The pointer wording ("Full decision tree and verdict definitions", `SKILL.md:44`) is clear enough that this is defensible as a sprawl control, but it is the one disclosure most at risk of not firing. At minimum, keep the pointer; consider inlining the 8-line decision tree since it is the skill's core and is short.
2. **The `classified.json` field-requiredness is defined in two rungs.** The schema annotations (`SKILL.md:150-152`: "fix_plan … (TP required)", "priority … (TP required)", "adr … (FP optional)") duplicate the "Required fields / Optional fields" bullets inside every verdict section of `CLASSIFICATION.md`. See §9.
3. **Nothing disclosed that should be inline** beyond the above; nothing inline that obviously belongs behind a pointer (the input schema at `SKILL.md:17-26` is needed every run, correctly inlined).

---

## 4. Completion Criteria — WARN

Most criteria are both *checkable* and *exhaustive* (the two properties from **GLOSSARY.md** → **Completion Criterion**), but three are leaky:

- **Step 1 (`SKILL.md:57`): "every finding has a file read and a scope check recorded."** The step body requires *two* checks — **Scope** (line 54) *and* **Prior FP** (line 55) — but the criterion names only "file read and a scope check." The Prior-FP check is unbound: an agent reading the criterion as the done-bar can skip it. **Fix:** "every finding has a file read, a scope check, and a prior-FP check recorded."
- **Step 3 (`SKILL.md:75`): "every ✅ TP and 🟡 Edge finding has been verified — confirmed or refuted with evidence."** The step body (`SKILL.md:69,73`) allows a third outcome — "insufficient detail" → ⏸️ Question. The criterion's enumeration "confirmed or refuted" omits it, so an insufficient-detail finding has no recognised done-state. **Fix:** "every ✅ TP and 🟡 Edge finding is resolved as confirmed, refuted (with evidence), or reclassified ⏸️ Question (with the uncertainty stated)."
- **Step 6 (`SKILL.md:124,126`):** the body introduces a new verdict-ish state — "A failed build marks the finding ❌ fix failed" — but "fix failed" is not one of the five verdicts, and the criterion ("build + tests pass, or failures are documented") does not capture the reclassification. Either "fix failed" is a *status* (then say so and add it to the report template) or it is a verdict (then it belongs in the verdict table / `CLASSIFICATION.md`). Right now it is an orphan.

Steps 2, 4, 5, 7 have sharp, exhaustive criteria. The Step 1 gap is the most consequential — it is the step whose **Legwork** (reading ADRs, review-knowledge) the whole downstream quality depends on.

---

## 5. Leading Words — WARN

Strong points: the *verify → grill → fix* triad (`SKILL.md:11`) is a textbook **Leading Word** cluster — compact, pretrained, repeated, anchoring both execution order and the defining failure. "A finding is a claim, not a fact" (`SKILL.md:11`) recruits the skepticism prior with *claim*.

Two issues:

- **The description's leading word is orphaned from the body.** The description front-loads "Classify" (`SKILL.md:3`), but the body uses "classification" only once (`SKILL.md:32`) and never "classify" as a working token; the body's anchors are *verify/grill/fix*. Per **GLOSSARY.md** → **Leading Word**, the description should use "the leading words you actually use when you want the skill," and the shared language is what makes invocation reliable. "Classify" recruits no priors the body reinforces.
- **Synonym duplication in the description.** "Classify code review findings… Use when … findings need **triage** into…" (`SKILL.md:3`). "Classify" and "triage" rename the same **Branch** — exactly the "synonyms that rename a single branch are **Duplication**" case from `writing-great-skills/SKILL.md`. Collapse to one. Also "fix/skip/FP verdicts" in the same sentence is a partial restatement of the five-verdict table (`SKILL.md:34-40`) and is incomplete (lists 3 of 5); cut it.

**Suggested description** (assuming the §2 fix to model-invocation): "Verify, grill, and fix code-review findings. Use when review comments, bug reports, or static-analysis findings need verdicts and action." — leading words *verify/grill/fix* now match the body, "triage"/"Classify" collapsed, partial verdict list removed.

---

## 6. Pruning — WARN

**Duplication** (**GLOSSARY.md** → **Duplication**, violation of **Single Source of Truth**):

- Verdict table + priority spread restated in both `SKILL.md:34-42` and `CLASSIFICATION.md` (Verdicts headings + Priority-assignment table). See §9.
- `resolved` defaults stated at `SKILL.md:158` *and* per-verdict inside `CLASSIFICATION.md`. See §9.
- Source enumeration twice in the same file: `SKILL.md:9` ("from a remote MR review, a local `/code-review` run, `/diagnosing-bugs`, or any source") and `SKILL.md:28` ("Remote MR review comments arrive pre-formatted from `/triage-mr`. Local session findings — from `/code-review`, `/diagnosing-bugs`, or ad-hoc…"). One home.
- Skip-annotation prefixes defined at `SKILL.md:95` ("annotate with `// FIXME:` (real, deferred) or `// NOTE:` (design intent)") *and* restated as a table at `SKILL.md:111-114`. The table adds nothing over the inline line; keep one.
- "Delegate to `/code-review`" appears at `SKILL.md:79`, `:101`, `:105`. The three contexts differ, but the delegation itself is restated; the Step-4 line could defer the *how* to the Step-5 sub-paths.

**No-Op** (**GLOSSARY.md** → **No-Op**):

- `SKILL.md:28` "The skill does not care where they came from." — uniformity is already implied by "uniform format, regardless of source" (`SKILL.md:15`). Says nothing the model doesn't already infer.
- `SKILL.md:67` "This is the step that separates this skill from 'just fix everything the bot says.'" — borderline. As pure exposition it is a no-op; but it does double as a light **Premature-Completion** defence weighting Step 3 against rushing (see §7). Keep *only if* you want that weighting; otherwise cut. Lean toward keeping but moving the sentiment into the completion criterion's demand.

**Sediment / Relevance:** low. The skill is lean; no stale layers found.

**Negation** (**GLOSSARY.md** → **Negation**): essentially clean. "inverting this order is the skill's defining failure" (`SKILL.md:11`) is a prohibition-adjacent line, but it is paired with the positive "Verify before grill, grill before fix" and functions as a hard guardrail — the framework's allowed form. No "don't do X" prose without a positive target. PASS on negation.

---

## 7. Premature Completion — WARN

All seven steps are visible inline, so every step's **Post-Completion Steps** are in view — the structural risk the framework warns about. The primary defence in use is sharp **Completion Criteria**, which is the correct first lever ("sharpen the bound first — it is local and cheap").

The highest-risk junction is **Step 2 → Step 3**: Step 2 already produces a verdict + reason and gets user confirmation, so the agent can feel "done" with a finding before Step 3's verification — which is the exact inversion the skill exists to prevent. Defences present: the *verify-before-grill* leading word (`SKILL.md:11`) and the motivational line at `:67`. These are adequate but soft.

The secondary risk is **Step 1 → Step 2**: Step 1's criterion omits the Prior-FP check (§4), so the agent can clear Step 1 and rush to recommending verdicts without the review-knowledge legwork — and a finding that *should* be ❌ FP gets recommended as ✅ TP, which Step 3 then has to unwind.

No sequence split is warranted yet — the criteria are mostly sharp and the steps share the findings list as state — but the §4 criterion fixes are what actually hold the line here. Fix the criteria before considering a **Granularity** sequence cut.

---

## 8. Co-location — WARN (minor)

Within `CLASSIFICATION.md`, each verdict's definition / action / required fields / `resolved` default are well **Co-located** under one heading — good. Within `SKILL.md`, the verdict table and priority sit together (`SKILL.md:30-42`) — good.

Two **Co-location** gaps:

- The `resolved` default for a verdict lives in `CLASSIFICATION.md` (under that verdict) *and* in `SKILL.md:158` (Output section, far from the verdict table). A reader at the verdict table does not get the default; a reader at the Output block does not get the verdict context. Pick one home (see §9).
- "fix failed" (`SKILL.md:124`) is a verdict-adjacent state defined in Step 6, divorced from the verdict table (`SKILL.md:34-40`) and from `CLASSIFICATION.md`. If it stays, co-locate it with verdicts.

---

## 9. Single Source of Truth — FAIL

**GLOSSARY.md** → **Single Source of Truth**: "each meaning lives in exactly one authoritative place." Four meanings currently have two:

1. **Verdict definitions + priority.** `SKILL.md:34-42` (compact table + priority line) *and* `CLASSIFICATION.md` (per-verdict sections + Priority-assignment table). Change the priority mapping → edit two files.
2. **`resolved` defaults.** `SKILL.md:158` ("`resolved` defaults: TP=false, FP=true, Edge=false, OOS=true, Question=false") *and* the per-verdict `resolved` bullets in `CLASSIFICATION.md`.
3. **Per-verdict required/optional fields.** `classified.json` schema annotations (`SKILL.md:150-152`) *and* `CLASSIFICATION.md` "Required fields / Optional fields" per verdict.
4. **Input sources.** `SKILL.md:9` *and* `SKILL.md:28` (within-file duplication, but still two statements of the same meaning).

**Recommended resolution** — make `CLASSIFICATION.md` the single home for *verdict semantics* (definition, sub-types, decision tree, priority, required fields, `resolved` default), and make `SKILL.md` carry only the compact verdict *marks* table (Mark → Verdict → Action) needed to read the Process, plus the pointer. Specifically:

- In `SKILL.md`, drop the priority line (`:42`) — it lives in `CLASSIFICATION.md`.
- In `SKILL.md`, drop the `resolved` defaults sentence (`:158`) — each verdict's default is in `CLASSIFICATION.md`; keep only the *post-Step-5 transition rule* ("After Step 5, processed TP and Edge are set to `true`"), which is process, not a per-verdict definition.
- In `SKILL.md`, drop the "(TP required)" / "(FP optional)" annotations from the schema (`:150-152`); they are in `CLASSIFICATION.md`.
- In `SKILL.md:9` *or* `:28`, keep one source enumeration.

This collapses four two-source meanings into one each, with no loss of inline legibility (the compact mark table stays in `SKILL.md`).

---

## Prioritized concrete changes

1. **[Invocation, blocker for the stated consumption model]** Decide `/fix`'s invocation axis. Given `/triage-mr` delegates to it, set `disable-model-invocation: false` and keep a model-facing description. If instead `/fix` is hand-only, strip the "Use when…" trigger clause from the description and stop `/triage-mr` claiming to delegate. (`SKILL.md:3-4`; `triage-mr/SKILL.md` Step 2.)
2. **[Single Source of Truth]** Make `CLASSIFICATION.md` the sole home for verdict semantics; from `SKILL.md` remove the priority line (`:42`), the `resolved` defaults sentence (`:158`), and the `(TP required)/(FP optional)` schema annotations (`:150-152`). Keep only the compact mark table + the post-Step-5 transition rule.
3. **[Completion Criterion — Step 1]** `SKILL.md:57` → add the Prior-FP check to the criterion: "every finding has a file read, a scope check, and a prior-FP check recorded."
4. **[Completion Criterion — Step 3]** `SKILL.md:75` → add the insufficient-detail outcome: "…resolved as confirmed, refuted (with evidence), or reclassified ⏸️ Question (uncertainty stated)."
5. **[Completion Criterion — Step 6]** `SKILL.md:124,126` → either make "fix failed" a named *status* (and add it to `REPORT.md`) or a verdict (and add it to the table / `CLASSIFICATION.md`). State the choice in the criterion.
6. **[Leading Words / Description]** Rewrite the description to lead with the body's actual anchors and collapse the classify/triage synonym: e.g. "Verify, grill, and fix code-review findings. Use when review comments, bug reports, or static-analysis findings need verdicts and action." Drop the partial "fix/skip/FP" verdict list. (`SKILL.md:3`.)
7. **[Pruning — Duplication]** Remove one of the two source enumerations (`SKILL.md:9` vs `:28`); remove the no-op "The skill does not care where they came from" (`:28`); collapse the skip-prefix table (`:111-114`) into the inline line (`:95`) or vice versa.
8. **[Predictability — Step 3 branch]** `SKILL.md:69` → gate the three reproduction options ("run if reachable; else test; else trace") so the process is the same every run.
9. **[Predictability — Step 6 branch]** `SKILL.md:121-124` → state the language-detection rule or disclose a small per-language command **Reference** table, instead of the unguided "Adapt … if not Go."
10. **[Information Hierarchy — decision tree]** Consider inlining the 8-line decision tree from `CLASSIFICATION.md` (it is must-have on every classification run); if kept disclosed, leave the pointer as-is — it is clearly worded.
