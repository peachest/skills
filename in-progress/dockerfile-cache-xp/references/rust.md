# Rust (cargo) layer-cache rules

Delta on top of [`common.md`](common.md). Loaded when the target Dockerfile
builds Rust via `cargo` / `maturin`.

## The single hard lesson: no manifest-layered COPY

**Rust workspaces cannot layer COPY the way Go does.** A `cargo fetch --locked`
step resolves every workspace member's manifest, and `[lib]` sections reference
`src/lib.rs`. Cargo checks those target files during resolution, so copying only
`Cargo.toml`/`Cargo.lock` without source fails `cargo fetch`. Proven on the SMG
project: the manifest-layered-COPY approach built fine in theory and broke at
`cargo fetch` in practice.

The proven shape is **full source COPY + cache mounts** — no manifest pre-fetch
layer:

```dockerfile
COPY . .

RUN --mount=type=cache,id=<pkg>-cargo-registry,target=${CARGO_HOME}/registry \
    --mount=type=cache,id=<pkg>-cargo-git,target=${CARGO_HOME}/git \
    --mount=type=cache,id=<pkg>-cargo-target,target=/opt/<pkg>/target,sharing=locked \
    <build command>
```

First build downloads deps into the cache mounts; subsequent builds skip the
download and reuse incremental compilation. You lose the "deps download as an
isolated layer" but the cache mounts already cover that case.

## Cargo cache mount partitioning

Set `CARGO_HOME` and `RUSTUP_HOME` as `ENV`, then mount each separately:

| Mount target | Purpose |
|---|---|
| `${CARGO_HOME}/registry` | crates.io index + downloaded crate tarballs |
| `${CARGO_HOME}/git` | git checkout of git deps |
| `${CARGO_HOME}/bin` | cargo/rustc binaries (if installed via rustup) |
| `${RUSTUP_HOME}` | toolchain + components |
| `<workdir>/target` | incremental build artifacts — the big one |

## Toolchain install

If the base image doesn't preinstall Rust, mount the toolchain caches during
install:

```dockerfile
RUN --mount=type=cache,target=${RUSTUP_HOME} \
    --mount=type=cache,target=${CARGO_HOME}/bin \
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
```

If the CI flow already has a toolchain-base image, `FROM` it — the install is
cached at the registry layer.

## Verified reference

`~/projects/smg/transwarp/docker/Dockerfile.smg.local` — Rust workspace (maturin
build), full COPY + cache mounts, no cargo clean. Read it when the target
Dockerfile is Rust and you need a concrete shape to mirror.
