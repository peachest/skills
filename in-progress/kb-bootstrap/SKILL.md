---
name: kb-bootstrap
description: Bootstrap a persistent knowledge wiki — pick the right wiki type, persist a mission doc, scaffold the tree, land the AGENTS.md pointer. Use when the user asks to 搭建/初始化 a 知识库/wiki/诊断库, starts a multi-repo or multi-session effort that needs shared contracts, or asks "这类知识该放哪".
---

# kb-bootstrap

A **bootstrap** produces one thing: the wiki's **initial state plus its pointer**. Lifetime management belongs to the **owning skill** — bootstrap never curates, diagnoses, or maintains; it hands over.

## 1. Pick the type

| Knowledge | Wiki | Owning skill | Reference |
|---|---|---|---|
| Cross-repo engineering contracts for a multi-session effort (ADRs, decisions, component maps scattered across repos) | effort wiki (okb tree + CONTEXT-MAP) | `okb` | [okb-effort-wiki.md](references/okb-effort-wiki.md) |
| Bug-diagnosis history worth re-consulting | ops diagnosis vault | `diag-write` / `diag-search` | [ops-vault.md](references/ops-vault.md) |
| Skill-execution knowledge (patterns, impact, run logs) | skills wiki | `skill-call-diagnose` | [skills-wiki.md](references/skills-wiki.md) |
| Teaching knowledge for courses | teaching OKB | `academy` | [teaching-okb.md](references/teaching-okb.md) |
| Single-repo code terrain (module maps, file tables) | **no wiki** — use CodeGraph (`codegraph_*` tools, always current) plus a `CONTEXT.md` for hand-curated glossary | — | — |

The last row is a decision, not a gap: a terrain wiki was tried (ppu-device-plugin, 2026-07) and an audit found agents read it only when a gate forced them — CodeGraph serves the same need live. Do not bootstrap one; route the glossary content into the repo's `CONTEXT.md`.

## 2. Three invariants (every type, before scaffolding)

1. **Persist the mission doc.** Write the blueprint to `~/handoff/<wiki-name>.md` — mission, user directives, source inventory, success criteria. `/tmp` loses files; the mission doc is what a later session reconstructs the wiki's *why* from. For effort wikis the template lives in [okb-effort-wiki.md](references/okb-effort-wiki.md).
2. **Land the AGENTS.md pointer.** A wiki without a pointer is unread by design. Add to the consuming scope's AGENTS.md (global for machine-wide wikis, repo-level otherwise) two trigger lines: **read** — when to consult it before acting, and where the entry file is; **write** — what outputs must be recorded back, via which owning skill. Word them as branches, not descriptions ("在上述任一仓做 X 前，先读…" / "产出 Y 后，按 Z 流程回写").
3. **Set the sanitize gate.** Runtime/local state (`runtime.conf`, `.env`, caches) gitignored with an `.example` template committed; internal identifiers (hosts, project names, credentials) follow the public-repo rules of the target repo; run its sanitize check before pushing.

## 3. Scaffold by type

Read the type's reference and follow its build order. Each reference ends with a **handover** section naming the owning skill and the first action that proves the wiki is live.

**Done when**: the tree exists with seed content, the mission doc sits in `~/handoff/`, the AGENTS.md pointer carries both trigger lines, and the owning skill has executed its first action against the wiki (an ingest, a diagnose cold-start, or an academy bootstrap — per reference).
