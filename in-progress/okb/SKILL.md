---
name: okb
description: Manage OKB, a bronze → silver → gold knowledge base (source snapshot → distilled note → verified note). Use when ingesting a source, distilling a note, fact-checking knowledge, querying the knowledge base, auditing a claim's provenance, or auditing the knowledge base's health (stale notes, broken links, taxonomy, topology).
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

**Only silver touches content.** Distill writes silver from bronze; factcheck writes a gold *verification overlay* (see §gold note).

## Directory layout

Layer paths are as in the table above. Two more files live at the okb root:

**index.md** — one section per topic: layer note counts and `ingests_since_status: <n>`. The counter is load-bearing — Ingest increments it, Status watches it.

**log.md** — the append-only operation record, one line per curation step:
`<ISO 8601> | <op> | <topic> | <what>`, e.g.
`2026-09-12T09:00Z | distill | llm-wiki-pattern | merged 'compiled-knowledge' into silver/concept.md`.
Ops: `ingest | route | distill | factcheck | status`. Append a line when a step's done-criterion is met, not before. log.md answers "what happened when" without walking frontmatter.

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
conflicts_with: []       # slugs of notes contradicting this note; both versions kept
verified: []             # empty ⇒ unverified
stale_after: <ISO 8601>  # distill sets it: evergreen sources ~12mo, fast-moving topics 1-3mo
sources:                 # derivation edge; [^id] footnotes key into these ids
  - id: <source-slug>    # globally unique across the okb; the overlap audit depends on it
    resource: ../bronze/<topic>/<source-slug>.md
    title: ...
---
```

**gold note** — no body content. It is a **verification overlay** on silver: `verified` events (machine-confirmed, or human-reviewed once a `human:` actor verifies), optional claim-level `verdicts`, `status: stable`, and `sources[].resource` pointing at the silver note. The knowledge lives in silver; gold only records that it was verified.

```yaml
---
status: stable
verified:
  - { by: process:okb-factcheck, at: <ISO 8601>, method: source-walk }
  - { by: human:<name>, at: <ISO 8601>, method: user-confirmation }
verdicts: []              # optional, claim-level: { claim: <quote>, verdict: confirmed|refuted|unverifiable }
sources:
  - id: <concept-slug>
    resource: ../silver/<topic>/<concept>.md
---
```

*Legacy corpus:* an okb created before this schema may carry gold bodies or non-slug `sources[].id`s — on the next factcheck, strip the gold body to the overlay and normalize the id.

**type** — `concept` (a mechanism or idea; default) or `reference` (compressed reference: glossary, algorithm, syntax, checklist).

## Curation

Build knowledge for a topic by running these in order. Each step is done on its completion criterion. An empty okb starts as the three directories plus empty `index.md` and `log.md`; a topic is named at first ingest — kebab-case, confirmed with the user when the boundary is ambiguous.

1. **Ingest** a source — fetch it and save a bronze snapshot. `scripts/okb_snapshot.py` does the mechanical part (arXiv id/URL → bronze file with frontmatter + sha256 dedup; content fetched elsewhere goes via `--from-file`).
   `<source-slug>` derives from the source title, kebab-case; `author` falls back to the account/publisher, else `unknown`; `sha256` hashes the saved snapshot body — the bytes under the frontmatter.
   **Fidelity floor:** the snapshot must cover the passages the distilled claims will cite. When the core claims live in the body (algorithms, theorems, tables) an abstract alone is not enough — fetch the full text and snapshot that; factcheck evidence must reach the origin, and an abstract-only bronze caps the chain short.
   Mirror check first: an existing bronze with the same `author` + `title` is the same work syndicated on another channel — add the URL to its `mirrors:` and skip the fetch (the script also skips on sha256 match).
   Done when `bronze/<topic>/<source-slug>.md` exists with `source`, `author`, `title`, `fetched_at`, `sha256` set, the verbatim content saved, and the topic's `ingests_since_status` counter in `index.md` incremented.

2. **Distill** — build silver from the bronze snapshot in two passes. **Silver is the only rewrite layer.**
   **Pass A — route, no writing.** Scan the topic's existing silver notes and produce a routing decision for every concept in the source: merge into an existing note (name the slug) or open a new one. The invariant is **one concept, one slug**. Append the route to log.md (one `route` line per concept) before any write — the route line survives a crash and claims the slugs against concurrent sessions. Done when every concept has a route: merge (slug named) or open.
   **Pass B — write.** Re-validate the route against current silver (concurrent sessions share this tree), then apply it. `scripts/okb_new.py` opens skeleton notes (silver always `status: draft`, `verified` empty). Merge appends to `sources[]`, folds the new facts into the body, refreshes `updated`, and rewrites inbound links to a retired slug; new opens a note. In every note written, link directly related silver notes using Markdown hyperlinks in the body — same topic `[concept](./<concept>.md)`, cross-topic `[concept](../<topic>/<concept>.md)` — **never `[[wikilink]]`**. A link is a navigation edge, not decoration.
   When the new source contradicts an existing note, keep both versions in the body and set `conflicts_with` on each side — resolution belongs to the user.
   Distill always writes `status: draft`. Only the factcheck step (or a one-line user confirmation, recorded as a `human:` verified event in gold) writes `status: stable` or a non-empty `verified` on silver — distill never touches either field.
   Done when every concept from the bronze snapshot is merged or newly opened, `silver/<topic>/<concept>.md` carries a non-empty `type` and `description`, `sources` lists the bronze snapshot, every fact is preserved (`reference` notes may compress — that is their job), and any note with a genuinely related sibling links to it. Attribute body claims with `[^id]` footnotes keyed to `sources[].id`.

3. **Fact-check** — verify the silver note and write a gold **verification overlay** (not content).
   Verify against the transitive sources (walk the chain to bronze/origin), not parametric memory. Every `verified` event's evidence cites bronze content (or the origin itself) — evidence pointing at a derived document (lesson, addendum, another note) does not close the chain.
   Done when `gold/<topic>/<concept>.md` exists, its `sources[].resource` points at the silver note, and every claim in the silver note is covered by a `verified` event or a `verdicts` entry.
   Verification promotes the silver note `draft → stable`; a one-line user confirmation promotes it too — record it as a `human:` verified event in gold.

4. **Query** — read notes back out, filtered by `topic`, `status`, or `verified`. If the matched note is gold, descend to its silver note first (gold has no body), then follow body Markdown hyperlinks one hop to pull linked notes in — the link graph is the recall mechanism, bronze is never re-read at query time.
   Done when the matching notes plus their one-hop linked notes are returned, each labeled with `status` and `verified`.

5. **Status** — report layer distribution plus the stale (`now >= stale_after`) and broken-link list (body hyperlinks and `sources[].resource` edges both count), a **taxonomy health audit** over all three directories (judgment-based: same-level distinguishable / same-level related / parent covers children / distance reflects relevance / structure serves retrieval, not itself), and a **topology audit** over silver notes (mechanical — computable from frontmatter and body links):
   - *isolated notes*: no link in or out — first candidates for linking or retirement;
   - *thinly linked notes*: exactly one distinct linked peer, in ∪ out;
   - *unlinked source-overlap pairs*: two silver notes sharing ≥2 `sources[]` ids but not linking each other — missed links or merge candidates.
   A *link* is a Markdown hyperlink between silver notes (`./<concept>.md` or `../<topic>/<concept>.md`); `[^id]` footnotes and external URLs don't count. Audit per topic, plus cross-topic links.
   Done when every report lists every note violating its check. `scripts/okb_index_regen.py` regenerates index.md from the tree (counters carried forward) and `--check-links` mechanically verifies the link list. Run it whenever a topic's `ingests_since_status` counter in `index.md` reaches ten, then reset the counter.

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
