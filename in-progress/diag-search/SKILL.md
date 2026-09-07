---
name: diag-search
description: Search the ops diagnosis vault (~/ops) for prior diagnoses relevant to a current bug — labels, keywords, and cluster index. Use before or during a diagnosis run (prior root causes feed hypotheses), or when the user asks to look up past 诊断/排查记录.
---

# Diag Search

Find what the vault already knows about a bug before diagnosing from zero. Pure ripgrep over `~/ops` — frontmatter labels first, then symptom keywords, then the cluster index.

## Step 1 — Form the query

From the bug at hand, extract: component(s) (hami, nodexpu, dcu, k3s, …), failure type (调度失败, OOM, …), vendor (hygon, nvidia, …), and 2–3 distinctive symptom keywords.

## Step 2 — Search by labels, then keywords

```bash
# label hits — frontmatter only
rg -l 'labels:.*<component>' ~/ops/*.md
# keyword hits — symptom terms across body
rg -il -e '<keyword1>' -e '<keyword2>' ~/ops/*.md
```

Union both sets. Zero hits on labels alone means broaden to keywords; zero on both means the vault has nothing — say so and stop.

## Step 3 — Read the index for the cluster

`~/ops/index.md` — the cluster matching the bug's theme (调度链路, webhook 链路, …) lists its entries with one-line gists; scan for adjacency the keyword search missed.

## Step 4 — Report ranked, then read

Rank the union: label match + keyword match > either alone. Read the full notes of the top few (their 排查过程 carries the repro commands and probes). Report each hit as: title, labels, one-line gist, path.

A prior note's 根本原因 is the prize — feed it into the current hypothesis list; its red-loop command may shorten the current Phase 1.

## Done when

- [ ] Every vault note matching the bug's labels has been considered (not just the first hit)
- [ ] Report states either the ranked hits with paths, or explicitly that the vault has nothing
