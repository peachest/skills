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
| **Bronze** | `bronze/<topic>/<source-slug>.md` | a raw source snapshot (URL + author + fetched_at + sha256) — the only fidelity layer |
| **Silver** | `silver/<topic>/<concept>.md` | the **only rewrite layer** — distilled note, every fact preserved, sourced, unverified |
| **Gold** | `gold/<topic>/<concept>.md` | a **verification overlay** — verified events pointing back to silver, no rewritten body |

**Only silver touches content.** Distill writes silver from bronze (rewriting content once, preserving every fact); factcheck writes a gold *verification overlay* (verified events + source pointer), never a second content copy.

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
author: <bylined author of the source>
mirrors: [<alternate URL>]   # optional: same work syndicated on another channel
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
description: ...         # one-line factual summary, ≤40 chars, naming the key entity
tags: [ ... ]
status: draft            # draft | stable | deprecated; promoted by factcheck or user confirmation
generated: { by: process:okb-distill, at: <ISO 8601> }
updated: <ISO 8601>      # last concept-aggregation merge
conflicts_with: []       # concepts whose facts contradict this note; both versions kept
verified: []             # empty ⇒ unverified
stale_after: <ISO 8601>
sources:                 # derivation edge; [^id] footnotes key into these ids
  - id: <source-slug>
    resource: ../bronze/<topic>/<source-slug>.md
    title: ...
---
```

**gold note** — no body content. It is a **verification overlay** on silver: `verified` events (machine-confirmed, or human-reviewed once a `human:` actor verifies), optional claim-level `verdicts`, `status: stable`, and `sources[].resource` pointing at the silver note. The knowledge lives in silver; gold only records that it was verified.

**type** — `concept` (a mechanism or idea; default) or `reference` (compressed reference: glossary, algorithm, syntax, checklist).

## Curation

Build knowledge for a topic by running these in order. Each step is done on its completion criterion.

1. **Ingest** a source — fetch it and save a bronze snapshot.
   Mirror check first: an existing bronze with the same `author` + `title` is the same work syndicated on another channel — add the URL to its `mirrors:` and skip the fetch.
   Done when `bronze/<topic>/<source-slug>.md` exists with `source`, `author`, `title`, `fetched_at`, `sha256` set, the verbatim content saved, and the topic's `ingests_since_status` counter in `index.md` incremented.

2. **Distill** — write a silver note from the bronze snapshot. **This is the only rewrite pass.**
   Start with **concept aggregation**: scan the topic's existing silver notes and route every concept in the new source — merge into the matching note (append to `sources[]`, fold the new facts into the body, refresh `updated`) or open a new one. One concept under two slugs is the failure state this step exists to prevent.
   When the new source contradicts an existing note, keep both versions in the body and set `conflicts_with` on each side — resolution belongs to the user.
   Distill always writes `status: draft`.
   Done when every concept from the bronze snapshot is merged or newly opened, `silver/<topic>/<concept>.md` carries a non-empty `type` and `description`, `sources` lists the bronze snapshot, **and every fact in the bronze snapshot is preserved** (no compression, no dropped claims). Attribute body claims with `[^id]` footnotes keyed to `sources[].id`.

3. **Fact-check** — verify the silver note and write a gold **verification overlay** (not content).
   Done when `gold/<topic>/<concept>.md` exists, its `sources[].resource` points at the silver note, and `verified` is non-empty. Verify against the transitive sources (walk the chain to bronze/origin), not parametric memory. The gold note carries no rewritten body — it only records verification + back to silver.
   Verification promotes the silver note `draft → stable`; a one-line user confirmation of a draft promotes it too.

4. **Query** — read notes back out, filtered by `topic`, `status`, or `verified`.
   Done when the matching notes are returned.

5. **Status** — report layer distribution plus the stale (`now >= stale_after`) and broken-link list, and a **taxonomy health audit** over all three directories (same-level distinguishable / same-level related / parent covers children / distance reflects relevance / structure serves retrieval, not itself).
   Run it whenever a topic's `ingests_since_status` counter in `index.md` reaches ten, then reset the counter.

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

Point Knowledge entries at `gold/`, falling back to stable `silver/` when gold is absent. A draft silver is readable but unreviewed — treat its claims as provisional. When a topic's knowledge is missing from OKB, run curation first, then read from OKB.
