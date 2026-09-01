---
name: dockerfile-cache-xp
description: Turn a CI Dockerfile into a Dockerfile.local that maximizes BuildKit layer-cache reuse for local builds, plus the nerdctl build command.
disable-model-invocation: true
---

# dockerfile-cache-xp

Push BuildKit layer-cache reuse to the limit: turn a CI `Dockerfile` into a
`Dockerfile.local` that survives source-only edits in minutes instead of
rebuilding from scratch — and hand over the nerdctl command that runs it.

The CI Dockerfile is built for reproducibility from a clean state, not for
iteration. A local build pays that full cost every time. The local version keeps
the CI stage structure and rewrites each `RUN` to ride cache mounts across
builds.

## Output

Two artifacts, placed next to the original:

1. **`<name>.local`** — the optimized Dockerfile (same directory as the source,
   `.local` suffix). Preserves the original's stage structure; only changes how
   each stage caches.
2. **The nerdctl build command** — printed to the user, ready to run.

## Process

### 1. Identify the build language

Read the CI Dockerfile end to end. Identify the build language(s): Rust (cargo /
maturin), Go (go mod), or other. The language decides which reference governs
the rewrite. A multi-language Dockerfile (e.g. a Go service with a Rust sidecar)
applies each language's rules to its own stage.

### 2. Load common.md, then the language reference

- [`references/common.md`](references/common.md) — language-agnostic cache
  rules, loaded every run.
- **Rust** → [`references/rust.md`](references/rust.md)
- **Go** → [`references/go.md`](references/go.md)
- **Other** (Python/Node/C++…) → common.md alone; tell the user it's best-effort.

### 3. Rewrite each stage

For every `RUN` in every build stage, apply common.md's cache-mount rules, then
the language reference's COPY ordering and mount partitioning. The local version
inherits the original's stage topology — never restructure.

### 4. Write the Dockerfile.local

Write `<original-name>.local` in the same directory. Header comment states what
changed vs the CI version, the usage command, and expected first/subsequent
build times.

### 5. Produce the build command

Reach [`references/build-command.md`](references/build-command.md) and assemble
the nerdctl command: resolve the proxy address from AGENTS.md or memory
(do not hardcode), four-case proxy `--build-arg` + `NO_PROXY`/`no_proxy`, harbor
registry tag, `-f <path>.local`. Print the command to the user.

## Completion checklist

Each item is a lever that, if missed, collapses the cache benefit:

- [ ] Every `RUN` that downloads or compiles has a matching `--mount=type=cache`.
- [ ] Cache mounts have explicit `id=` prefixed with the project name.
- [ ] Compile-output mount (`target`/`go-build`) has `sharing=locked`.
- [ ] No `cargo clean`, `go clean`, or `rm -rf /root/.cache` remains.
- [ ] COPY ordering follows the language rules: Go layers manifests → source;
      Rust uses full COPY (no manifest pre-fetch layer).
- [ ] Proxy `ARG`s declared per stage and `export`ed inside each networked `RUN`.
- [ ] The original stage structure is preserved — no flattening.
- [ ] The `.local` file sits beside the original; header has usage + timing.
- [ ] The nerdctl command uses four-case proxy args and includes `NO_PROXY`.
- [ ] Proxy address comes from the environment, not hardcoded in the Dockerfile.
