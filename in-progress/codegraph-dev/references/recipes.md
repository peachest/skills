# Validated recipes

Each recipe below was proven on a real task (NeMo-Relay MR, 2026-09-14, session `01a09de1`). The evidence line is what it caught that manual review missed.

## 1. Post-change gap check (the core loop)

```bash
cd <repo> && codegraph sync
git diff --name-only origin/main...HEAD | codegraph affected --stdin -q
codegraph impact -d 3 <config/struct symbol you changed>
```

**Evidence — affected catch:** the MR touched 13 files; `affected` listed 7 CLI test files, one of which (`cli_tests.rs`) was *not* in the diff. Root cause: an earlier `git checkout -- crates/cli/tests/` (meant to undo a bad regex edit) had silently rolled back two test assertions added for the change. The diff looked complete; the dependency graph said otherwise.

**Evidence — impact catch:** `impact GatewayConfig` surfaced `apply_env_config` (mod.rs) as a consumer. The change had added the new env var only to the clap flag layer (`env=` on the flag). But `doctor` and `model-pricing` resolve config via `GatewayOverrides::default()` — they never pass through clap, so they read only the `apply_env_config` layer. Without the second layer, `doctor` would print a different effective timeout than the daemon actually used. Symptom class: **config with two application paths** — when adding any config knob, run `impact` on the config type and check *every* consumer reads it from every path.

**Gap rule:** an `affected`/`impact` entry not in your diff and not deliberately untouched is a finding. Verify why before claiming done.

## 2. Spec grounding (to-spec / to-tickets)

```bash
codegraph context "provider passthrough HTTP timeout configuration" --no-code
codegraph callers <resolution fn>          # trace every path a value flows through
```

**Why:** `context` turns a feature sentence into the symbol set a spec's Implementation Decisions must talk about; `callers` enumerates the resolution paths so the spec can require coverage of each. A spec citing the index cannot hallucinate a file name.

**For to-tickets:** slices whose acceptance criteria name real symbols (`resolve_server_config reads http_timeout_secs from apply_env_config`) are passCheck-able; criteria naming only behavior are not.

## 3. Blast radius before the diff exists (implement / fix / wayfinder)

```bash
codegraph node <symbol>          # source + caller/callee trail
codegraph impact -d 2 <symbol>   # what breaks if this changes
```

**Wayfinder use:** a decision ticket's cost-of-reversal is `impact -d 3` on the symbol the decision commits you to. Small radius → cheap to reverse → don't over-deliberate. 164-symbol radius → that's a "Decisions so far" entry with the graph as evidence.

## 4. Reviewer onboarding (code-review / mr-review)

```bash
git diff --name-only <base>...HEAD | codegraph affected --stdin -q   # scope the review
codegraph context "<PR's one-line purpose>"                           # design-context paragraph
```

**Why:** a reviewer (human or subagent) that starts from `affected` + `context` instead of raw diff order enters with the dependency structure in hand — the same two-step the author should have run, so discrepancies between "what the author verified" and "what the graph says" surface immediately.

## Known limits (all observed, don't relearn them)

- **Symbol search misses literals and generated names** — `HTTP_REQUEST_TIMEOUT` (a const, not a function) didn't surface in symbol queries; grep found it. Symbols first, grep for constants.
- **Rust macros/generics are coarse** — `impact GatewayConfig` returned 164 associated symbols across examples/ and Python bindings; those are file-level associations, not call chains. The cli-crate hits were precise; the rest needed manual verification.
- **`affected` is a conservative closure** — it listed 260 test files repo-wide at depth 5; the set that actually executes the changed logic was the 7 in the relevant crate. Filter by crate/module before running anything.
- **Stale index lies quietly** — after heavy edits without `sync`, results silently describe the old tree. `codegraph status -j` before trusting; `sync` after commits.
