---
name: okb
description: Manage OKB — the open-knowledge-base that is the source of truth for what the agent knows, organized as bronze → silver → gold (source snapshot → distilled note → fact-checked note). Use when ingesting a source, distilling a note, fact-checking knowledge, querying the knowledge base, or auditing a claim's provenance.
---

# OKB (open-knowledge-base)

OKB is the **source of truth** for knowledge. What the agent learns worth keeping lands here — layered, sourced, and traceable — instead of being re-read from raw sources each session. A teaching skill consumes OKB through `RESOURCES.md` pointers.

## Three layers

Three **distinct directories**, linked by `sources[].resource` (the derivation edge):

| Layer | Directory | Holds |
|---|---|---|
| **Bronze** | `bronze/<topic>/<source-slug>.md` | a raw source snapshot (URL + fetched_at + sha256) |
| **Silver** | `silver/<topic>/<concept>.md` | a distilled note — structured, sourced, unverified |
| **Gold** | `gold/<topic>/<concept>.md` | a fact-checked note — verified, stable |

**Promotion writes a new file** — distill writes silver from bronze, factcheck writes gold from silver.

## Directory layout

```
okb/
├── bronze/<topic>/<source-slug>.md
├── silver/<topic>/<concept>.md
├── gold/<topic>/<concept>.md
└── index.md
```

`<topic>`, `<concept>`, and `<source-slug>` are kebab-case.

## Frontmatter

**bronze snapshot**

```yaml
---
source: <original URL>
title: <label>
fetched_at: <ISO 8601>
sha256: <content hash>
---
<verbatim fetched content>
```

**silver note**

```yaml
---
type: concept            # concept | reference
title: ...
description: ...
tags: [ ... ]
status: draft            # draft | stable | deprecated
generated: { by: process:okb-distill, at: <ISO 8601> }
verified: []             # empty ⇒ unverified
stale_after: <ISO 8601>
sources:                 # derivation edge; [^id] footnotes key into these ids
  - id: <source-slug>
    resource: ../bronze/<topic>/<source-slug>.md
    title: ...
---
```

**gold note** — same shape as silver, with three differences: `sources[].resource` points at the silver note it was fact-checked from; `verified` is non-empty (`machine-confirmed`, or `human-reviewed` once a `human:` actor verifies); `status: stable`.

**type** — `concept` (a mechanism or idea; default) or `reference` (compressed reference: glossary, algorithm, syntax, checklist).

## Curation

Build knowledge for a topic by running these in order. Each step is done on its completion criterion.

1. **Ingest** a source — fetch it and save a bronze snapshot.
   Done when `bronze/<topic>/<source-slug>.md` exists with `source`, `fetched_at`, `sha256` set and the verbatim content saved.

2. **Distill** — write a silver note from the bronze snapshot.
   Done when `silver/<topic>/<concept>.md` exists with a non-empty `type` and `sources` listing the bronze snapshot. Attribute body claims with `[^id]` footnotes keyed to `sources[].id`.

3. **Fact-check** — verify the silver note and write the gold note.
   Done when `gold/<topic>/<concept>.md` exists, its `sources[].resource` points at the silver note, and `verified` is non-empty. Verify against the transitive sources (walk the chain to bronze/origin), not parametric memory.

4. **Query** — read notes back out, filtered by `topic`, `status`, or `verified`.
   Done when the matching notes are returned.

5. **Status** — report layer distribution plus the stale (`now >= stale_after`) and broken-link list.

## Evidence chain (invariant)

Every claim in a lesson traces back to its origin in four hops:

```
lesson ──▶ gold ──▶ silver ──▶ bronze ──▶ origin URL
 (OKB sources)  (sources→silver)  (sources→bronze)  (source=URL)
```

Each hop is a `sources[].resource` derivation edge. The chain is a **forcing function**: a claim carries its source or it is not written.

## Consuming OKB from another skill

A teaching workspace reads knowledge through `RESOURCES.md`, pointing into OKB:

```md
## Knowledge
- [micro-batch event loop](../../okb/gold/<topic>/micro-batch-event-loop.md)
```

Point Knowledge entries at `gold/`, falling back to `silver/` when gold is absent. When a topic's knowledge is missing from OKB, run curation first, then read from OKB.
