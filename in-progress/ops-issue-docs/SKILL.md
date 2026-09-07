---
name: ops-issue-docs
description: Persist a completed bug diagnosis as an Issue note in the ops knowledge base (~/ops/). Reached at diagnosing-bugs Phase 6 completion, or when the user asks to 记录/沉淀/持久化 a diagnosis or ops issue.
---

# Ops Issue Docs

Turn a finished diagnosis into an Issue note that outlives the session. The vault is `~/ops/` — two live folders, `已解决/` (resolved) and `未确定/` (undetermined) — and the template is `~/obsidianNote/templates/Issue.md`. Earlier issues live in the legacy vault `~/obsidianNote/运维/`; they stay there — do not move them.

## Step 1 — Gather the diagnosis

From the diagnosing-bugs run, collect: the symptom as the user stated it, the environment (nodes, cluster, component versions), the feedback-loop command with its red and green outputs, the ranked hypotheses and which one survived, the fix, and how it was verified. Every line the note cites comes from this material.

## Step 2 — Place and name

Search both vaults before creating — the legacy vault holds the history:

```bash
grep -rl "<keywords from symptom and cause>" ~/ops/ ~/obsidianNote/运维/
```

If a note already covers this issue, update it in place — fill its empty sections, and move it across folders if its status changed. A legacy note (`~/obsidianNote/运维/`) stays where it is; update it there. A sibling note for a known issue splits the trail.

Otherwise create `~/ops/<folder>/<title>.md`:

- `已解决/` — root cause confirmed and the fix verified (loop green)
- `未确定/` — everything else; the note records how far the trail got

Title = the symptom in one Chinese line, e.g. `webhook 阻止删除 finalizer 导致 pod 无法被删除`. Match the style of the neighbouring notes.

## Step 3 — Fill the template

Write the body in Chinese, terse. Map each section:

| Section | Filled from |
| --- | --- |
| 背景 | What triggered the investigation — the task being performed, the report, the related issue. Link related notes here (relative paths). |
| 环境 | Nodes, cluster, and component versions involved |
| 问题描述 | The user's exact symptom, quoted |
| 排查过程 | The trail: the loop command and its red output, then each probe and the hypothesis it killed. Paste outputs verbatim in fenced blocks, trimmed to the lines that carry the signal |
| 根本原因 | The surviving hypothesis, stated as a mechanism. Unknown stays unknown — write 未知 plus the best remaining guess |
| 复现方法 | The minimised repro / loop command |
| 解决方法 | The fix and its verification (loop green, regression test). Unfixed: what is known so far |
| 关联 Solution | Leave the template line as-is |

A ruled-out hypothesis earns a line only when ruling it out took real work — that is exactly the line the next debugger needs.

## Step 4 — Link both ways

When 背景 references another note, open that note and add the return link, so the pair reads connected from either end. Notes in the other vault are reached by relative path across them (e.g. `../../obsidianNote/运维/<note>.md`) — compute the path from the file you are writing, and verify the target exists.

## Done when

- [ ] Every section is filled or explicitly marked 未知
- [ ] Every claim in 结论 traces to evidence quoted in 排查过程
- [ ] The file sits in the folder matching its status
- [ ] Cross-links work from both ends
