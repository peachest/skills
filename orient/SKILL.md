---
name: orient
description: Orient before you wayfind — read the project's terrain so planning starts grounded in what already exists.
disable-model-invocation: true
---

Before you **wayfind**, **orient**. Wayfinding charts a way from *here* to a destination, but you can't chart from here if you don't know where here is. **Orienting** reads the **terrain** the requirement lands on, so every subsequent plan is grounded in what already exists.

## Read the terrain

The requirement is your compass — it points the direction. Survey the terrain between here and where it points, not the whole project.

1. **Glossary.** Read `CONTEXT.md`, or `CONTEXT-MAP.md` if the repo carries multiple contexts — follow it to the one the requirement touches. Extract the **ubiquitous language**: terms the project has already agreed on. A term in the requirement that the glossary defines is now precise; one it doesn't is a **gap**.

2. **Decisions.** Read `docs/adr/` — the architectural decisions already locked. Each narrows what the plan can propose without re-opening a settled question. Extract those in the requirement's area.

3. **Docs.** Read the project's documentation — `README.md`, `docs/`, and any local knowledge base (`knowledge_search`, `kb_read`). Extract what's already written about the area.

4. **Conventions.** Read the project's development conventions — `AGENTS.md`, `DEVELOPMENT.md`, `CONTRIBUTING.md`, `.claude/rules/`, `Makefile` targets, pre-commit config. Extract the rules the work must follow: commit conventions, verification commands, lint policies, code-review patterns, must-read skills before modifying specific components.

5. **Codebase.** Survey the code the requirement will touch. Use `codegraph` for fast symbol search where available; otherwise read directory structure and key files. Map the **seams** — existing interfaces, modules, and patterns the work should follow rather than invent. While surveying, note **landmarks** — existing implementations whose semantics resemble what the requirement asks for. A landmark is not a seam to follow but a point to navigate by: its code encodes behavior, boundaries, and design decisions more precisely than prose, and the plan can migrate semantics from it rather than describing them from scratch.

6. **Waymarks.** Read test files in the requirement's area. Tests are waymarks — markers left by previous travelers on the terrain, indicating paths that pass and boundaries that hold. A test named `test_old_user_compatibility` tells you more about hidden constraints than any README. Extract the behaviors tests assert and the boundary conditions they guard.

A terrain layer that doesn't exist — no `CONTEXT.md`, no ADRs, no docs, no conventions — is itself a gap; note it. This skill is read-only; `/skill:domain-modeling` handles creation, reached when grilling resolves a term or decision.

- [ ] Glossary read; ubiquitous language extracted; gaps flagged.
- [ ] ADRs read; relevant constraints extracted.
- [ ] Docs read; existing area documentation extracted.
- [ ] Conventions read; development rules extracted.
- [ ] Codebase surveyed; seams mapped; landmarks noted.
- [ ] Waymarks read; implicit requirements and boundary conditions extracted.

## Produce the bearing

Synthesize the terrain into a **bearing** — a compact grounding summary the next skill consumes:

| Section | Holds |
|---------|-------|
| **Terms** | Glossary vocabulary relevant to the requirement, each with its agreed meaning and **source** — the file and section it was read from. |
| **Constraints** | ADRs that bound the decision space, each gist'd to its ruling and **source** — the ADR file or doc section that locks it. |
| **Conventions** | Development rules the work must follow — commit conventions, verification commands, lint policies, must-read skills — each with its **source** — the file and section it was read from. |
| **Seams** | Codebase structure, interfaces, and patterns the work lands on, each with its **source** — the file and symbol or line range. |
| **Landmarks** | Existing implementations whose semantics the requirement can migrate from, each with its **source** — the file and symbol, and what it demonstrates. |
| **Waymarks** | Implicit requirements and boundary conditions extracted from test files, each with its **source** — the test file and test name. |
| **Gaps** | What the terrain doesn't cover but the requirement needs — undefined terms, missing decisions, undocumented areas. Each gap is either **surveyed but empty** (you looked and found nothing) or **beyond survey** (you didn't look because it wasn't in scope), and names what's missing and **where you looked** for it. Beyond-survey gaps flow into wayfinding's fog of war; surveyed-but-empty gaps seed the first grilling. |

### Calibrate the requirement against the terrain

The requirement is a compass, not a map — it can be wrong about the terrain. Having read both, calibrate. Where the requirement **over-specifies** — dictating a solution the terrain already handles or closing a decision an ADR has settled — the plan can relax; extra instruction here only binds the agent. Where it **under-specifies** — the terrain is complex, risky, or unsettled but the requirement passes over it in a phrase — that is a gap, and likely the gap that matters most. Name both: what the requirement should let go of, and what it must not leave unsaid.

The bearing lives in the session context and carries into the next skill. If wayfinding, feed the bearing's terms, constraints, and conventions into the map's **Notes**; let the gaps and calibration seed the first grilling.

- [ ] Bearing produced: terms, constraints, conventions, seams, landmarks, waymarks, gaps each covered, every item carrying its source.
- [ ] Calibration produced: over-specified and under-specified points named.
