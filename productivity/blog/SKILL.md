---
name: blog
description: "Blog pipeline for the blogs/ directory: draft, de-slop, review. Triggers on writing, rewriting, or exporting a blog post (including '导出'/'PDF')."
user-invocable: true
---

# Blog Pipeline

Three phases, each with a hard gate. The gate for each phase is the completion criterion — the agent does not advance until it passes.

`<PROJECT_DIR>` is the user's blogs/ directory.

The pipeline produces one file in `<PROJECT_DIR>/`.

## Phase 1: Draft

Read `<SKILL_DIR>/references/STYLE-GUIDE.md` first.

Run **`/skill:technical-article-writer`**. Follow its workflow.

After the draft is complete, apply the STYLE-GUIDE document skeleton.

**Gate**: draft conforms to STYLE-GUIDE skeleton (title, TL;DR, numbered sections, callout, conclusion, appendix). Missing any → loop back.

## Phase 2: De-slop

Run **`/skill:blog-writing-guide`**'s "AI Writing Patterns to Avoid" section and **`/skill:unslop`**'s rewrite flow.

Run `<SKILL_DIR>/scripts/check-blog.py` first. Fix all programmable failures. Then re-read the draft for the 3 semantic checks: (1) 对比用表格, (2) 引用原文格式, (3) H2 过渡句. Each confirmed present.

**Gate**: `check-blog.py` exits 0. All 3 semantic checks confirmed.

## Phase 3: Review

Spawn parallel subagents — one per dimension of **`/skill:technical-writing-best-practices`**. Four dimensions:

| Subagent | Domain |
|----------|--------|
| structure | Structure and Flow |
| teaching | Teaching and Explanation |
| sentences | Sentence Craft |
| reasoning | Reasoning and Argument |

Each subagent gets: the draft path, the `/skill:technical-writing-best-practices` skill path, and the rubric in `<SKILL_DIR>/references/review-rubric.md`.

Structure and Reasoning fails are blocking. Sentence Craft and Teaching fails are fix-in-place.

**Gate**: zero failing rules in Structure and Reasoning. All fixes applied. If wording changed, re-run Phase 2.

## Export

When the user says "导出"、"export"、"PDF"，read `<SKILL_DIR>/references/export.md`. Then run `<SKILL_DIR>/scripts/export-blogs.sh` with `<SKILL_DIR>/references/export-style.css`.
