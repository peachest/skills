# Language-agnostic layer-cache rules

The rules every build stage follows, regardless of language. Loaded for every
run — the language references (`rust.md`, `go.md`) carry only the delta on top
of this.

## Inherit the original structure

The local version keeps the original's stage topology — multi-stage, two-stage
env-base, whatever it is. The optimization is per-`RUN` cache mounts and COPY
ordering, never restructuring. A rewrite that flattens stages has gone wrong.

## Every networked RUN gets a cache mount

Every `RUN` that downloads (apt, apk, uv pip, npm) or compiles (cargo, go,
cmake) gets a `--mount=type=cache` for that tool's cache directory. The mount
survives across builds; without it the step pays the full cost every time.

## Explicit id= on every cache mount

Prefix with the project name:

```dockerfile
--mount=type=cache,id=smg-cargo-target,target=/opt/smg/target,sharing=locked
```

Without an `id=`, buildkit derives one from the target path, which collides
across unrelated projects sharing one buildkitd.

## sharing=locked on build-output mounts

The compile output mount (`target/`, `go-build`, etc.) takes `sharing=locked`.
Concurrent builds writing the same target dir corrupt incremental artifacts;
locked serializes them.

## Preserve incremental artifacts

Keep the compile cache across builds — never `cargo clean`, `go clean`, or
`rm -rf /root/.cache` in a layer. These wipe the cache mount's incremental
state, collapsing the cache benefit to zero. The cache mount content isn't
baked into the image layer, so deleting it only burns time.

## Per-stage proxy ARGs

Args are stage-scoped — each stage that runs networked steps redeclares them,
and each such `RUN` exports them so the tools inside see the proxy:

```dockerfile
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG http_proxy
ARG https_proxy
ARG NO_PROXY
ARG no_proxy

RUN --mount=type=cache,... \
    export HTTP_PROXY HTTPS_PROXY http_proxy https_proxy NO_PROXY no_proxy \
    && <networked step>
```

Four-case (upper + lower) is mandatory: `curl` reads lowercase, `git` reads
uppercase in some paths; one set alone leaves some steps bypassing the proxy.
The proxy address comes from the environment (AGENTS.md / memory), not
hardcoded — see `build-command.md`.
