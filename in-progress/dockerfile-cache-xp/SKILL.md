---
name: dockerfile-cache-xp
description: Audit and optimize a repo's Dockerfile.local for local build speed — cache mounts (GOCACHE/GOMODCACHE), kill -a full recompiles, CGO, ldflags dummy values, runtime base parity. Use when local image rebuilds are slow (改代码后重建镜像要几分钟), when writing/reviewing a Dockerfile.local, or when the user says 提速本地构建 / dockerfile cache / 本地打包优化.
---

# Dockerfile Cache XP

Speed up the "edit code → rebuild image locally" loop. The measured prize (<node-a>, 2026-10-23): warm rebuild 20.2s → 2.3s (Go service) and 19.9s → 4.7s (CGO service). Full playbook and provenance: <platform-wiki> `silver/local-image-build/`.

## Step 0 — Scope check

This skill targets **Dockerfile.local** (the local iteration path), never the CI Dockerfile or `.gitlab-ci.yml`. Confirm the repo has a Dockerfile.local; if only a CI Dockerfile exists, clone its runtime stage into a new Dockerfile.local first (see wiki silver/local-image-build for the 4-rule template).

## Step 1 — Audit (read the Dockerfile.local + the makefile target it calls)

Check for these cost killers in order of impact:

| # | Killer | Look for | Fix |
|---|--------|----------|-----|
| 1 | **`-a` full recompile** | `go build -a` anywhere in the called makefile target (e.g. `build:`) | Dockerfile.local calls `go build` directly, bypassing make |
| 2 | **Missing GOCACHE mount** | `--mount=type=cache` only on GOMODCACHE | Add `--mount=type=cache,target=/root/.cache/go-build` to the build RUN |
| 3 | **Version ARG churn** | `ARG VERSION/TIME/COMMIT` consumed inside build RUN | Dummy-value them (`${VERSION:-dev}`) so layer cache survives |
| 4 | **CGO when not needed** | `CGO_ENABLED=1` (or unset) for a pure-Go service | `CGO_ENABLED=0` if the binary doesn't dlopen anything — verify against what CI/Makefile does first |
| 5 | **Non-hermetic build step** | build RUN without `GOPROXY=off` | `go mod download all` (plain download leaves zips missing → warm builds silently hit the network) + `env GOPROXY=off` in the build RUN. Passing = cache complete; failing = missing (fails fast instead of mysterious +45s) |
| 6 | **Runtime base drift** | final FROM on a base that's 404/unreachable on this node (e.g. `golang-runner:1.20-alpine3.19`) | `ARG RUNTIME_IMAGE` declared **before the first FROM** (global scope), default = CI base for ADR-0007 parity; alpine-only `apk` steps get a `command -v apk` guard so ubuntu overrides also build. For a CGO_ENABLED=0 binary, `<ns>/base/alpine-runner:3.19` halves image size vs ubuntu-runner (163MB vs 329MB measured) |

Rules of thumb from the measurement runs:
- `go mod download` as a separate RUN costs ~0 in steady state (layer only re-runs when go.mod changes) — don't bother merging it.
- Cold start (first build on a node) is dominated by module download (~45s); internal goproxy is NOT reliably faster than the company proxy — don't churn on it.
- Steady-state floor is ~2-3s: buildkit overhead + COPY layers + link. If you're there, stop.

## Step 2 — Measure (no cheating)

Benchmark = **warm rebuild after a one-line real source change** (append a comment to a mid-level package file), with buildkit cache mounts in steady state:

```bash
# warmup build (untimed, fills cache mounts) — only needed once per Dockerfile variant
sudo nerdctl -n buildkit build -f Dockerfile.local -t xp:bench . > /tmp/build.log 2>&1
echo "// xp $(date +%s)" >> internal/<mid-level-pkg>/<file>.go
T0=$(date +%s.%N); sudo nerdctl -n buildkit build -f Dockerfile.local -t xp:bench . > /tmp/build.log 2>&1 || { tail -30 /tmp/build.log; exit 1; }; T1=$(date +%s.%N)
python3 -c "print(f'{$T1-$T0:.1f}s')"
# smoke: binary exists & executable at ENTRYPOINT path
sudo nerdctl -n buildkit run --rm --entrypoint /bin/sh xp:bench -c 'test -x <bin-path>' && echo SMOKE-OK
```

Integrity rules:
- The timed build must run the full pipeline (mod download + compile + image assembly). Never pre-bake artifacts into the context.
- Run the variant **twice** — report the second number (first run after any Dockerfile edit re-runs all layers).
- Proxy builds need all four build-args (`http_proxy https_proxy HTTP_PROXY HTTPS_PROXY`) or DNS fails inside buildkit.
- buildkit on these nodes rejects `--network host` (entitlement) — don't pass it.
- `nerdctl` needs `-n buildkit` for build/run/push namespace consistency.

## Step 3 — Apply & verify

Apply the winning combination, run the timed build twice, run the smoke. Keep the runtime stage byte-compatible with the CI Dockerfile unless an ARG override is explicitly documented (ADR-0007 pattern: local and CI images must give the same trivy verdict).

Commit as `ci: ...` with the before/after numbers in the message, and write the measured numbers back to <platform-wiki> `silver/local-image-build/README.md`.

## Known traps

- **export data version mismatch**: a golangci-lint binary built with go≤1.27.2 fails typecheck (v5>v4) against a GOCACHE written by go1.27.3+. Fixed 2026-10-23 on <node-a> by building golangci-lint v2.15.0 from source with the host toolchain. New lint versions also carry rule drift (revive magic-number etc.) — check `.golangci.yml` pinning before blaming code.
- **Bare repos + extensions.worktreeConfig**: enabling it on a bare repo breaks worktree detection ("must be run in a work tree"). To bypass hooks in one worktree of a bare repo, point `core.hooksPath` at a directory that doesn't exist in that branch instead.
- **`git reset --hard` wipes uncommitted experiment state** — commit before any reset during measurement loops.
