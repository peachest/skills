---
name: province-chain
description: 'Force every concrete factual claim to carry a locatable source anchor, and audit a finished conclusion''s evidence chain on demand. Invoke with /province-chain for writing-time citation (stays on until "stop province-chain"); say "审计证据链" / "audit this conclusion''s sources" to run a one-shot audit. Use when writing research reports, citing data or papers, giving conclusions about a codebase, or producing any claim a reader will trust on the source''s authority.'
license: MIT
metadata:
  hermes:
    tags: [Citation, Evidence-Chain, Research, Audit, Provenance]
    category: quality
    related_skills: [okb, fact-check, research]
---

# province-chain

A claim without a locatable source is a guess wearing a claim''s clothes. province-chain makes the source a forcing function: every concrete factual claim carries an anchor pointing back to where it came from, or it is not written. After a conclusion lands, an audit retraces the chain — anchors that exist raise confidence; anchors that are missing drop it and force a re-derivation.

Two modes share one invariant — **no source, no claim**:

- **citing** — writing-time, persistent. `/province-chain` turns it on; it stays on for the session until "stop province-chain". Every concrete factual claim written while on must carry an anchor.
- **audit** — one-shot, on demand. The user says "审计证据链" / "audit this conclusion''s sources" / names a conclusion to check. Retrace its chain, score confidence, re-derive what is missing.

## The invariant

Every concrete factual claim traces to a **locatable anchor** — a point in the agent''s context where the raw fact lives: a tool result (a `read` file span, a `bash` output line, a `grep` hit), a cited document section, or a measured datum with a timestamp. "I read something once" is not an anchor; the file:line / output line / §heading is. A claim whose anchor cannot be pointed to is unsourceed, and unsourceed concrete claims are not written.

## citing mode

### Persistence

These rules apply to every response for the rest of the session. They do not expire after a few turns and do not lapse when the topic changes. Turn them off only when the reader says "stop province-chain" or "停止证据链模式" — confirm in one line, then return to default.

### What must carry an anchor

A **concrete factual claim** — a statement asserting a fact about the world rather than a step of reasoning — carries an anchor. Six shapes, each a place fabrication hides when unsourceed:

1. **Numbers** — percentages, counts, ratios, magnitudes ("90% of context", "44-minute P99").
2. **Versions / identifiers** — version numbers, release tags, model IDs ("EAGLE-2", "v1.7.0").
3. **URLs** — any link asserted to exist or to say something.
4. **API / system behaviour assertions** — "this function does Z", "the endpoint returns Y", "sglang emits usage only when …".
5. **Citation conclusions** — "X shows …", "Y reports …", "per the paper …" attributing a finding to a source.
6. **Measured facts** — "latency is 200ms", "acceptance rate hits 70% on code".

### What does not carry an anchor

Pure reasoning — derivations, method suggestions, logic steps, restatements of the user''s instruction. These are the agent''s own work, not facts borrowed from a source; anchoring them manufactures a source where there is none.

### Anchor formats

Four source kinds, one format each. The anchor names **where in the context the fact lives**, not the source''s title.

- **code** — `[code: <PROJECT_DIR>/path/to/file.go:42-58]`
- **paper / doc** — `[doc: arXiv:2402.xxxx §3.2]` or `[doc: <URL> §<heading>]`
- **measured** — `[measured: <query or command> @ 2026-09-01]`
- **tool result** — `[tool: <read|bash|grep> <what output, e.g. `bash: kubectl get pods` line N>]`

A concrete factual claim is immediately followed by its anchor. One anchor per claim; if a claim rests on two sources, both appear.

Bad: "Tools consume 90% of the context window."  ← number, no anchor; fabrication enters here.
Good: "Tools consume 12–28% of the context window [doc: arXiv:2608.00101 §4]."

Bad: "User thinking P99 reaches 44 minutes."  ← metric, no anchor; metric confusion enters here.
Good: "User thinking P99 reaches 13.9 hours [doc: arXiv:TraceLab Table 7]; the 44-minute figure is request-response P99, a different metric [doc: arXiv:TraceLab Table 7]."

Bad: "NVIDIA Dynamo docs describe disaggregated serving."  ← URL asserted, no anchor; a 404 hides here.
Good: "TensorRT-LLM disaggregated serving splits prefill from decode [doc: https://nvidia.com/.../tensorrt-llm-disaggregated §disaggregated]."

### No anchor, no claim

If a concrete factual claim cannot be given an anchor from the current context, it is not written. Options, in order:

1. **Fetch the source** — run the tool that produces the anchor (`read` the file, `grep` the line, fetch the doc). Then write the claim with the fresh anchor.
2. **Mark it unverified** — if the reader asked for a quick read and the source is reachable but not yet in context, write the claim tagged `[未审计]` and note what to source it from. These are debt: an audit will flag them low-confidence until paid.
3. **Drop the claim** — if the source is the agent''s parametric memory or training knowledge and cannot be reached by any tool, do not assert it as fact. Say instead "I have no source in context for this; it would need <where to look>."

## audit mode

Triggered only when the user explicitly asks — "审计证据链", "audit this conclusion''s sources", or names a conclusion to check. It does not fire on its own and does not persist: one pass, then done.

### Locatability is the test

For each audited conclusion, ask: can the fact it rests on be pointed to a raw anchor in the current context? An anchor is a concrete locus — file:line, output line, §heading, measured query — not "I recall reading this." The answer places the conclusion on one of three rungs:

- **anchored** — the anchor exists in context and supports the conclusion. ✅ high confidence.
- **partial** — the anchor exists but supports only part, or supports it with a caveat (a version mix-up, an optimistic bound). ⚠️ medium — name the deviation.
- **unsourceed** — no anchor can be pointed to; the conclusion rests on parametric memory, a guess, or a source no longer in context. ❌ low confidence.

### Graded handling

- **anchored** → keep. List the anchor.
- **partial** → keep with the caveat written out ("direction right, magnitude estimated — needs production validation").
- **unsourceed, sourceable** → the agent fetches the source now (run the tool, get the anchor), re-derives the conclusion, and returns it anchored. No need to stop the user.
- **unsourceed, not sourceable** → stop. Report `[无源·低置信] 此结论来自模型内部知识/推断，上下文无对应原始锚点：<conclusion>` and give 2–3 concrete ways to source it (which file to read, which command to run, which URL to fetch). Wait for the reader to supply the source or accept the low-confidence claim.
- **before an irreversible action** (drop data, migrate schema, force push) → even anchored conclusions are audited, and unsourceed ones halt: do not act on a guess before an irreversible step, emergency or not.

### Output

A table — one row per audited conclusion — plus a re-derivation note. The table goes to the conversation; if the audit covers a persistent artifact (a report, a codebase conclusion worth keeping), also write `<artifact>.audit.md` beside it.

```
| 结论 | 锚点 | 置信度 | 处置 |
|------|------|--------|------|
| 工具目录消耗 12-28% 上下文 | doc: arXiv:2608.00101 §4 | ✅ 高 | 保留 |
| 用户思考 P99=44分钟 | (无锚点) | ❌ 低 | 重推：补 TraceLab Table 7 |
| 函数 foo() 做了 Z | code: repo/foo.go:42-58 | ✅ 高 | 保留 |
```

Then a short **re-derivation note**: for each ❌ row, the 2–3 concrete sourcing moves and what re-running the reasoning with that source would change.

## When to break the rules

1. **Pure reasoning / method suggestions / logic steps** carry no anchor — they are excluded from the anchor requirement, not exceptions to it.
2. **Reader says "先别管来源，给个快速判断"** — citing yields, but the claim is tagged `[未审计]`. An audit will score these ❌ until sourced. The debt is named, not hidden.
3. **Emergency / safety scene** (live incident, stop-service decision) — audit yields to action: give the conclusion and the move first, audit after. But an irreversible action (drop data, migrate schema) still forces an audit first, emergency or not.
4. **Harness limit** — a subagent that cannot spawn or fetch still runs citing (it is an output-format rule, independent of tools). Audit degrades to "list the anchors that can be listed; report the missing tool capability explicitly" rather than silently dropping claims.

## Pre-send check (citing)

Before sending, scan the concrete factual claims:

1. Every number, version, URL, behaviour assertion, citation conclusion, and measured fact has an anchor immediately after it.
2. No anchor is a title-only gesture ("per the paper") — it points to a locus (§heading, file:line, output line).
3. `[未审计]` tags are present only where the reader asked for speed, and each names what would source it.

If a claim fails, source it or drop it.

## Relations

- **research** — direction subagents inherit citing via this skill''s description; the research skill may add a one-line cross-link "direction subagents follow province-chain".
- **fact-check** — province-chain is the before/during constraint (carry the source); fact-check is the after verifier (check the source is true). They do not overlap.
- **okb** — an audited, anchored chain may be distilled into OKB by `okb-distill` for persistent storage. province-chain never writes OKB itself; it only notes the option here.
