---
name: diag-write
description: Write a finished bug diagnosis into the ops diagnosis vault (~/ops) — template fill, labels from labels.md, index update, grouped commit. Reached at the end of a diagnosing-bugs run (Phase 6 handoff), or when the user asks to 记录/沉淀 a diagnosis.
---

# Diag Write

Turn a finished diagnosis into a vault entry that outlives the session. The vault is `~/ops` — self-describing: `template.md` (note skeleton), `labels.md` (frontmatter schema + label table + new-label protocol), `index.md` (cluster index). This skill adds only the process; the vault holds the rules.

## Step 1 — Gather the diagnosis

From the diagnosis run (or the user's account), collect: the symptom as the user stated it, the environment (nodes, cluster, component versions), the feedback-loop command with its red and green outputs, the ranked hypotheses and which one survived, the fix, and how it was verified. Every line the entry cites comes from this material.

## Step 2 — Find or create the entry

Search the vault before creating — symptom keywords and component names across it:

```bash
rg -il '<keywords>' ~/ops/*.md
```

A hit that covers this issue means an earlier entry exists: update it in place — fill empty sections, refine labels and index — never fork a second trail. (Extraction and migration routes converge here: many sessions, or a session plus a legacy note, on one issue yield one entry.)

Otherwise create `~/ops/<title>.md` from `~/ops/template.md` (delete the template comments). Title = the symptom in one Chinese line, no prefix. Body in Chinese, terse. `source: diagnosis`.

## Step 3 — Assign labels

Read `~/ops/labels.md` and run **one pass per axis** — component (what broke, family-level), failure-type (how it broke), vendor (whose hardware). Multi-value axes take all that apply.

A label absent from the table may only enter through the new-label protocol: propose it, get the user's approval, register it in `labels.md` (axis + meaning + when-to-apply) — then use it.

## Step 4 — Update the index

Open `~/ops/index.md`, add the entry to its cluster — title link, labels, one-line gist. No fitting cluster → 未归类 (entries graduate as clusters emerge).

## Step 5 — Commit via /skill:commit-buddy

In `~/ops`, commit through `/skill:commit-buddy` — grouped so this entry and nothing else ride the commit. The vault is local-only; no remote exists.

## Done when

- [ ] Vault searched before creation; an existing entry on this issue was updated, not forked
- [ ] Frontmatter valid per labels.md (status derived from content, not optimism)
- [ ] Every label present in labels.md, or registered through user approval this run
- [ ] index.md updated; entry sits in a cluster or 未归类
- [ ] `~/ops` working tree clean (entry committed)
- [ ] Every claim in 结论 traces to evidence quoted in 排查过程
