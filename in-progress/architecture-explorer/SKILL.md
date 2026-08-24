---
name: architecture-explorer
description: Explore a codebase's architecture interactively, layer by layer, using CodeGraph — survey modules, drill into internals, map dependencies, and assess deep/shallow module health. Use when the user says "explore architecture", "巡视架构", "module dependencies", "who calls X", "architecture viewer", or before refactoring, before /skill:improve-codebase-architecture, when you need to understand how modules relate before changing them.
---

# Architecture Explorer

Interactive, layer-by-layer architecture exploration built on CodeGraph. The counterpart to `project-wiki` (which surveys once and persists a static chart) — this skill explores on demand, drilling into any module's internals and dependencies at the level the question needs.

## Prerequisite: CodeGraph initialized

Verify before proceeding:

```bash
# Check via the codegraph_status tool
```

If CodeGraph is not initialized for the project, tell the user and stop — this skill cannot run without it. Direct them to initialize CodeGraph first (the `codegraph_status` tool reports how).

## The three phases

### Phase 1 — Survey

Get the module tree and build a module index with one-line responsibilities.

Use the `codegraph_files` tool (format `tree`) to get the project's file/module structure. For each top-level module, infer a one-line responsibility from its name and the files it contains. If `project-wiki`'s chart exists in the project (`docs/project_wiki/overview.md`), read it for pre-existing responsibility descriptions — don't re-infer what's already written.

Output: a module index — one line per module, `name — responsibility`. Keep it under 30 lines; if there are more modules, group minor ones.

### Phase 2 — Drill

For each module the user picks (or, if none picked, the module most active in recent `git log`), explore its internals and dependencies.

**Internals** — use `codegraph_explore` with the module name or its key symbols to see what's inside: functions, types, methods, and how they group.

**Inbound dependencies** — use `codegraph_callers` on the module's key exported symbols to see who depends on it. This reveals the module's consumers and the coupling surface.

**Outbound dependencies** — use `codegraph_callees` on the module's key symbols to see what it depends on. This reveals the module's suppliers and whether it reaches across layers.

**Impact radius** — if the user is exploring before a change, use `codegraph_impact` on the symbol they plan to touch, to show the blast radius before they commit.

Present findings as a per-module card:

```
## <module name>
Responsibility: <one line>
Internals: <N functions, N types, key groups>
Inbound: <who calls it — modules and count>
Outbound: <what it calls — modules and count>
Depth assessment: <deep / shallow / mixed — see below>
```

### Phase 3 — Synthesize

Produce a markdown architecture map assessing each surveyed module's health using the `codebase-design` vocabulary. Load `codebase-design`'s glossary first (run `/skill:codebase-design` or read its SKILL.md) — use its terms exactly: **module**, **interface**, **depth**, **seam**, **adapter**, **leverage**, **locality**. Do not invent new vocabulary.

For each module, assess:

- **Depth** — Is it a deep module (small interface, lots of behaviour hidden) or a shallow module (wide interface, thin implementation)? Use the deletion test from `codebase-design`: would deleting this module concentrate complexity, or just move it?
- **Seam quality** — Is the interface at a clean seam, or does it leak internals? Do callers reach past the interface into implementation?
- **Coupling** — Does it have too many inbound dependencies (God module) or too many outbound (reaches across layers)?
- **Locality** — Do changes concentrate here, or do they spread across callers?

Output: a markdown file (write to a temp location — `$TMPDIR/architecture-explorer-<timestamp>.md` or `/tmp/` — keep it out of the repo by default). Structure:

```markdown
# Architecture Map — <project>, <date>

## Module index
<from Phase 1>

## Module assessments
<one card per module from Phase 2, with depth/seam/coupling/locality assessment>

## Health summary
- Deep modules: <list>
- Shallow modules (deepening candidates): <list>
- God modules (too many inbound): <list>
- Layer-crossers (too many outbound): <list>
- Next steps: feed shallow modules into /skill:improve-codebase-architecture
```

## When to stop

- The user asked about a specific module → after Phase 2 for that module, ask if they want to drill further or synthesize.
- The user wants a full survey → Phase 1, then Phase 2 for every module (or the top 5-10 by activity), then Phase 3.
- The user is exploring before a refactor → Phase 2 for the modules in the refactor scope + `codegraph_impact` on symbols to be changed, then Phase 3 scoped to those modules.

## Relationship to other skills

- **`project-wiki`** — surveys once, persists a static chart with SHA-based drift detection. This skill explores interactively on demand. They are complements: project-wiki for orientation, this skill for investigation.
- **`codebase-design`** — provides the vocabulary (deep module, seam, leverage, locality) this skill uses in Phase 3. Load it before synthesizing.
- **`improve-codebase-architecture`** — scans for deepening opportunities and grills through them. This skill feeds it candidates: the shallow modules identified in Phase 3 are exactly what `improve-codebase-architecture` works on.
