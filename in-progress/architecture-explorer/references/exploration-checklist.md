# Exploration Checklist

What to look for at each layer of exploration. Not a rigid script — a menu of signals. Pick the ones relevant to the question being explored.

## Phase 1 — Survey signals

While building the module index, flag:

- **Orphaned modules** — modules with no inbound dependencies (nothing calls them). Either dead code, an entry point (main, CLI), or a gap in CodeGraph's index.
- **God modules** — modules with disproportionately many files or symbols compared to peers. Candidates to split.
- **Naming mismatches** — module name doesn't match what its files actually do. A `utils` module containing business logic is a smell.
- **Missing layering** — no visible separation between API, domain, data layers (if the project type expects one).

## Phase 2 — Drill signals

While drilling into a module's internals and dependencies, look for:

### Internals

- **Shallow module** — interface surface (exported symbols) is nearly as large as the implementation (few private helpers). The module adds indirection without hiding complexity. Deepening candidate.
- **Leaked internals** — callers import private/unexported symbols (visible in `codegraph_callers` results that reference internal paths). The seam is not holding.
- **Mixed responsibilities** — the module's exported symbols serve unrelated concerns. Candidate to split into two deep modules.
- **Dead code** — exported symbols with zero inbound callers (unless they're an entry point or public API).

### Inbound dependencies (who calls this module)

- **Too many callers** — a module everyone depends on is either a true shared foundation (good, if deep) or a God module (bad, if shallow). Check depth to distinguish.
- **Cross-layer callers** — a data-layer module called directly by API-layer code, bypassing the domain layer. Layering violation.
- **Single caller** — a module with only one consumer may be better inlined, unless it's a deliberate seam for testing or future reuse.

### Outbound dependencies (what this module calls)

- **Layer crossing** — a domain module calling data-layer or infrastructure modules directly. The dependency direction should follow the architecture's layering (domain ← data ← infra, or whatever the project uses).
- **Fan-out** — a module calling many unrelated modules. It may be a coordinator (legitimate) or a module with mixed responsibilities (smell).
- **Circular dependency** — module A calls module B which calls back to A. CodeGraph's `codegraph_callers` on A's symbols will show B, and B's will show A. Flag explicitly — these are hard to break.

### Impact radius (before a change)

- **High blast radius** — `codegraph_impact` shows 10+ callers across multiple modules. The symbol is load-bearing. Consider whether the change can be made at the seam (new method, deprecate old) rather than in-place.
- **Low blast radius** — 1-3 callers. Safe to change in place.

## Phase 3 — Synthesize signals

While assessing module health with `codebase-design` vocabulary:

- **Depth assessment** — apply the deletion test: if this module disappeared, would complexity concentrate (it was hiding real complexity = deep) or just move (it was thin pass-through = shallow)?
- **Seam quality** — can you change the implementation without touching callers? If yes, the seam holds. If callers break on every internal change, the seam leaks.
- **Leverage** — how many call sites and tests does one implementation pay back across? High leverage = deep module doing real work. Low leverage = shallow module adding overhead.
- **Locality** — when a bug is found here, do you fix it in one place, or does the fix spread to callers? Good locality = changes concentrate. Poor locality = changes ripple.

## Red flags to always report

- **Circular dependencies** — always flag, always name both directions.
- **Leaked internals** — callers reaching past the interface. Always flag with the caller and the internal path they reference.
- **God modules** — always flag with symbol/file count vs peers, and whether the depth justifies the size.
- **Dead exported symbols** — always list, unless the module is a declared public API/entry point.
