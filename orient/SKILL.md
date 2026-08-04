---
name: orient
description: Orient before you wayfind — read the project's glossary, ADRs, docs, and codebase to establish where "here" is, so planning starts grounded in what already exists.
disable-model-invocation: true
---

Before you **wayfind**, **orient**. Wayfinding charts a way from *here* to a destination, but you can't chart from here if you don't know where here is. **Orienting** reads the **terrain** the requirement lands on, so every subsequent plan is grounded in what already exists.

The pull to jump straight to planning is the signal to orient. A requirement that feels ready to decompose usually isn't — the ADRs that constrain it, the glossary terms that must be precise, the seams it should follow haven't been read yet.

## Read the terrain

The requirement is your compass — it points the direction. Survey the terrain between here and where it points, not the whole project.

1. **Glossary.** Read `CONTEXT.md`, or `CONTEXT-MAP.md` if the repo carries multiple contexts — follow it to the one the requirement touches. Extract the **ubiquitous language**: terms the project has already agreed on. A term in the requirement that the glossary defines is now precise; one it doesn't is a **gap**.

2. **Decisions.** Read `docs/adr/` — the architectural decisions already locked. Each narrows what the plan can propose without re-opening a settled question. Extract those in the requirement's area.

3. **Docs.** Read the project's documentation — `README.md`, `docs/`, and any local knowledge base (`knowledge_search`, `kb_read`). Extract what's already written about the area.

4. **Codebase.** Survey the code the requirement will touch. Use `codegraph` for fast symbol search where available; otherwise read directory structure and key files. Map the **seams** — existing interfaces, modules, and patterns the work should follow rather than invent.

A terrain layer that doesn't exist — no `CONTEXT.md`, no ADRs, no docs — is itself a gap; note it. Don't create anything; that's `/skill:domain-modeling`'s job, reached when grilling resolves a term or decision.

- [ ] Glossary read; ubiquitous language extracted; gaps flagged.
- [ ] ADRs read; relevant constraints extracted.
- [ ] Docs read; area-specific knowledge extracted.
- [ ] Codebase surveyed; seams mapped.

## Produce the bearing

Synthesize the terrain into a **bearing** — a compact grounding summary the next skill consumes:

| Section | Holds |
|---------|-------|
| **Terms** | Glossary vocabulary relevant to the requirement, each with its agreed meaning. |
| **Constraints** | ADRs that bound the decision space, each gist'd to its ruling. |
| **Seams** | Codebase structure, interfaces, and patterns the work lands on. |
| **Gaps** | What the terrain doesn't cover but the requirement needs — undefined terms, missing decisions, undocumented areas. The first questions a grilling or wayfinding session should raise. |

The bearing lives in the session context and carries into the next skill. If wayfinding, feed the bearing's terms and constraints into the map's **Notes**; let the gaps seed the first grilling.

- [ ] Bearing produced: terms, constraints, seams, gaps each covered.
