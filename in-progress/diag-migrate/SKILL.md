---
name: diag-migrate
description: Rewrite a legacy or external ops note into the ~/ops diagnosis vault schema — frontmatter, labels, status re-derived from content, assets copied in. Use when backfilling the old obsidianNote/运维 notes or importing any external markdown diagnosis doc.
---

# Diag Migrate

Bring one external diagnosis note into the vault, one note per pass. Same vault as `/skill:diag-write` (`~/ops`, self-describing) — the schema lives there, this skill adds the rewrite rules.

## Step 1 — Derive frontmatter from content

- `status`: root cause confirmed **and** fix verified in the body → `resolved`; everything else → `undetermined`. The source folder's name is a hint, not a verdict — legacy 已解决 notes without a confirmed root cause migrate as `undetermined`.
- `source`: `Oops` prefix → `oops`, `Ops` → `ops`, anything else → `ops`. Strip the prefix from the title.
- `date`: from the note's content if present; otherwise the migration date.

## Step 2 — Rewrite the body

- Fill `~/ops/template.md` sections from the source: 排查过程 keeps the original trail verbatim (fenced outputs, trimmed to the lines that carry the signal); a 复现方法/稳定复现 section folds into 排查过程 as the red loop.
- 环境 missing in the source → write 未记录 (required only for fresh diagnoses, never invent it).
- Screenshots and referenced assets: copy into `~/ops/assets/`, fix the paths — the vault stays self-contained. Links leaving the vault (external notes, docs) stay as-is with their original targets.
- Preserve the original's cross-note links as relative paths to the migrated entries.

## Step 3 — Labels, index, commit

Steps 3–5 of `/skill:diag-write` apply unchanged: one pass per axis from `~/ops/labels.md`, index cluster (or 未归类) in `~/ops/index.md`, grouped commit via `/skill:commit-buddy`.

## Step 4 — Leave the source untouched

The legacy original stays where it is, byte-identical — a frozen copy. The vault holds the living version.

## Done when

- [ ] Frontmatter valid per labels.md; status reflects the body's actual conclusions
- [ ] No template comments, no leftover Oops/Ops prefix, no 复现方法 heading
- [ ] All referenced assets inside `~/ops/assets/`, paths resolve
- [ ] Index updated; grouped commit made; source file unchanged
