---
name: learn-from-examples
description: |
  Analyze example projects or source repositories to extract reusable patterns,
  best practices, interface contracts, key differences, file maps, and dependency
  choices. Outputs structured knowledge as a Markdown report or an installable
  skill package. Use when user says "从...学习" / "从这些...中学习" / "学一下..." / "从这些源码中..."
  / "学习...的开发方式" / "学习如何使用" / "学习使用" / "提取模式" / "归纳最佳实践" / "learn from" / "study
  these repos" / "extract patterns from" / "看看这些项目是怎么做..." / "分析一下这些仓库" / "分析这些仓库"
---

# Learn from Examples

Extract reusable patterns, design conventions, and best practices from example source repos. Meta-skill: output is structured knowledge you can use immediately.

## Step 1 — Gather inputs

Identify repos from user's request. Each entry: **source** (`local` path or `git` URL + optional ref), **what to learn** (user-specified aspect, e.g. "pi-tui component system"). Git repos clone to a temp dir.

- [ ] Repos recorded with source type and target aspect. Git repos cloned.

## Step 2 — Choose output format

Ask user: **A) Markdown report** (self-contained `.md`) or **B) Skill package** (`SKILL.md` + `references/`) or custom.

## Step 3 — Choose analysis strategy

Ask user: **Default** (N ≤ 2 holistic, N ≥ 3 parallel-analyze then synthesize) or custom override.

## Step 4 — Discover file scope

Two-phase: **(4a) Structural survey** — README + directory listings for repo structure. **(4b) Focused zoom** — guided by "what to learn", identify specific files to deep-read. Use `codegraph` when available for fast symbol search.

- [ ] Structural survey done. Focused files identified per aspect.

## Step 5 — Extract knowledge (6 dimensions)

For each repo, extract with code references (file + line#):

| # | Dimension | Key questions |
|---|-----------|---------------|
| 1 | **Core patterns** | What structural/flow patterns recur across repos? |
| 2 | **Key differences** | Where do implementations diverge and why? |
| 3 | **Best practices & pitfalls** | What works? What are common mistakes? |
| 4 | **Interfaces & contracts** | APIs, config formats, type signatures |
| 5 | **File map** | Key files and their responsibilities |
| 6 | **Dependencies & stack** | Tools, libraries, versions used |

- [ ] All 6 dimensions covered per repo with code references.

## Step 6 — Synthesize

N ≥ 3 (parallel): combine per-repo analyses into cross-repo synthesis — compare patterns, contrast differences, highlight best practices. N ≤ 2: holistic analysis IS the synthesis.

- [ ] Cross-repo patterns identified with consistent terminology.

## Step 7 — Ask output path and build output

Ask user for output directory (default to current working directory). Write artifacts to that path.

**Report (A)**: write `<aspect>-learned.md` with sections per dimension, code blocks with source annotation.

**Skill (B)**: write `SKILL.md` (~60 lines Quick Start + Workflow) plus:

| File | Content |
|------|---------|
| `references/patterns.md` | Core patterns & key differences |
| `references/practices.md` | Best practices, pitfalls, interface contracts |
| `references/files.md` | File maps per repo |
| `references/stack.md` | Dependencies & tech stack |

## Do NOT

- Modify source repos — analysis is read-only.
- Include full file contents — only key snippets with line refs.
- Guess architectures — read code to verify.
- Hardcode package names or versions in output.