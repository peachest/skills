# Go (modules) layer-cache rules

Delta on top of [`common.md`](common.md). Loaded when the target Dockerfile
builds Go.

## Layered COPY — the core lever

Go is the language where layered COPY *works*. `go mod download` resolves the
module graph from `go.mod`/`go.sum` alone — it never touches `.go` source — so
deps download as an isolated cached layer that only invalidates when deps change:

```dockerfile
WORKDIR /<pkg>

# Step 1: manifests only → go mod download (cached layer).
COPY ./go.mod ./go.sum ./
RUN --mount=type=cache,id=<pkg>-gomodcache,target=${GOMODCACHE} go mod download

# Step 2: source. Only this layer invalidates on source edits.
COPY ./<src-dirs> ./
RUN --mount=type=cache,id=<pkg>-gomodcache,target=${GOMODCACHE} go build -o bin/<pkg> .
```

This is the key difference from Rust (see `rust.md`): Go can split the dependency
layer from the source layer; Rust workspaces cannot.

## GOMODCACHE

Set the mount target explicitly via `ARG`:

```dockerfile
ARG GOMODCACHE=/root/go/pkg/mod
```

`~/.cache/go-build` is a secondary, smaller win — mount it if present.

## Cross-architecture: BUILDPLATFORM

For multi-arch builds, run `go build` on the build host platform (faster,
especially on arm64 hosts) and cross-compile to the target:

```dockerfile
FROM --platform=${BUILDPLATFORM} <golang-builder> AS build
ARG TARGETARCH
ARG ARCH=${TARGETARCH}
ENV ARCH=${ARCH}

# ... layered COPY + go build with GOARCH=${TARGETARCH} ...
```

Preserve `BUILDPLATFORM` — it keeps arm64 builds fast.

## GOPROXY

CI Dockerfiles often pin a corporate goproxy mirror via `ENV GOPROXY=...`. Keep
that ENV in the local version — it composes with the `--build-arg` proxy
passthrough and routes `go mod download` to the fast internal mirror.

## Verified reference

`~/projects/kube-nodexpu-manager/dev/Dockerfile.local` — Go project, layered
COPY (`go.mod`/`go.sum` → `go mod download` → source), GOMODCACHE cache mount,
BUILDPLATFORM cross-arch. Read it when the target Dockerfile is Go and you need
a concrete shape to mirror.
