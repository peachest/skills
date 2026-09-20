# Effort wiki (okb tree + CONTEXT-MAP) — bootstrap reference

For a multi-repo, multi-session engineering effort whose decisions live scattered across per-repo ADRs, ticket trackers, and research docs. The trigger symptom: **parallel sessions re-deriving each other's context** — the effort wiki exists so they read and write one place instead.

Provenance: this design was validated on a real effort (llmops-wiki, 2026-09: 7 repos, 14 bronze / 11 silver in one sitting, peer-audited). This file is the generalization of that run's blueprint.

## 1. Mission doc → `~/handoff/<name>.md`

Write it before touching the filesystem. Sections (this structure is the template):

```md
# Handoff: <name> — cross-repo knowledge base for <effort>
Written <date> by <session/repo>.
## Mission
<effort spans N repos. Decisions live scattered in X/Y/Z. Pain: <concrete misjudgment or re-derivation that already happened>.>
Build a shared OKB so every project/session reads and writes one place, and <reuse goal>.
## User directives
<already-given constraints: which skill, which map pattern, audience>
## Source inventory (all already written, nothing to re-derive)
| Repo | Location (worktree/branch!) | Artifacts to ingest |
## Distill targets
<the unified contracts, numbered, one line each — verified across sessions, with dates>
## Component map
<producer → consumer chain, if the domain has one>
## Open items
<context, NOT this session's job unless asked>
```

The inventory table must pin the **exact checkout** per repo (worktree + branch, or a commit) — "read from the worktree, not dev" class mistakes are the classic bootstrap failure.

## 2. Scaffold

```
<name>/
├── CONTEXT-MAP.md     # hybrid: contexts (each = one okb topic) + repo index + glossary
├── bronze/<topic>/  silver/<topic>/  gold/<topic>/
├── index.md           # per-topic note counts + ingests_since_status counters
├── log.md             # append-only op record
└── RESOURCES.md       # the consumption entry peers point at
```

- **Contexts are domain-based** (one per okb topic: resource-names, units, billing…), not repo-based — repos appear in the CONTEXT-MAP repo-index table, which maps each repo's ADRs/artifacts to the contexts they feed.
- **Glossary** lives in CONTEXT-MAP: canonical term + _avoid_ list per alias (a glossary without an avoid-list lets the banned name back in).
- git init; internal-only wikis never get a public remote.

## 3. Build order

1. **Ingest** — one bronze snapshot per artifact in the inventory. Use the okb skill's `scripts/okb_snapshot.py --from-file` (verbatim copy + frontmatter + sha256). Increment each topic's counter.
2. **Distill, two passes** — Pass A writes a `route` line to log.md per concept *before any write* (crash-safe, claims slugs against concurrent sessions); Pass B writes silver per the route. Silver frontmatter: `status: draft`, empty `verified` — only factcheck touches those. `sources[].resource` points at `../../bronze/<topic>/<slug>.md`; body claims carry `[^id]` footnotes; sibling notes link via Markdown hyperlinks.
3. **Link check** — every hyperlink and every `sources[].resource` resolves; `okb_index_regen.py --check-links` mechanizes this.

## 4. Peer protocol

- Notify peer sessions (herdr/orca per multi-agent-collab) with RESOURCES.md as the single entry pointer — one line, not a tour.
- Audit loop that worked: reviewer sends machine-checked findings as a task list; the builder **verifies each against the repo before editing** and pushes back on wrong claims with evidence (line numbers); receipts close the loop in both directions.

## 5. Handover

Owning skill: **`okb`** — all subsequent curation (re-ingest on ADR revisions, factcheck 择机, Status audits) runs through it. The wiki is live when the first post-bootstrap change (an ADR update, a new contract) is ingested as a new bronze and distilled into the existing silver rather than re-deriving from scratch.
