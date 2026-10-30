#!/usr/bin/env bash
# ci-parity.sh — local CI parity: rerun the tests.yml two-tier loop in a
# STRIPPED environment (nix tooling removed from PATH), so environment-probe
# test failures surface locally BEFORE push instead of one GitHub Actions
# round trip each.
#
# Motivation (2026-10-28): three consecutive CI failures (yt-dlp / ffmpeg /
# herdr probes) were all invisible on the dev box because nix provides them;
# each was only discovered by pushing.
#
# Usage:
#   bash scripts/ci-parity.sh                 # full two-tier loop
#   bash scripts/ci-parity.sh <path-filter>   # only dirs containing <filter>
#   bash scripts/ci-parity.sh <test-dir>      # single test dir (tier-1 fast path)
#
# Exit codes mirror tests.yml: 0 = green, other = last failing rc
# (5 = no tests collected is treated as pass).

set -uo pipefail

if [ "${CI_PARITY_STRIPPED:-}" != "1" ]; then
    UV_BIN=$(command -v uv) || { echo "ci-parity: uv not found" >&2; exit 1; }
    NODE_BIN=$(command -v node || true)
    exec env -i PATH="$HOME/.local/bin:/usr/bin:/bin" HOME="$HOME" \
        CI_PARITY_STRIPPED=1 UV_BIN="$UV_BIN" NODE_BIN="$NODE_BIN" bash "$0" "$@"
fi

# Align with the CI runner, not with a bare box: ubuntu-latest preinstalls
# tools that env -i loses. aria2c → no-op stub (tests only need it to RESOLVE
# via which(); invocations are mocked). node → real binary symlink (tests run
# it for real). Extend this list when CI images change.
STUBS=$(mktemp -d)
printf '#!/bin/sh\nexit 0\n' > "$STUBS/aria2c" && chmod +x "$STUBS/aria2c"
[ -n "${NODE_BIN:-}" ] && ln -s "$NODE_BIN" "$STUBS/node"
export PATH="$STUBS:$HOME/.local/bin:/usr/bin:/bin"

cd "$(git rev-parse --show-toplevel)" || exit 1
FILTER="${1:-}"
rc=0

# Tier 2 skills: own pyproject → own venv (same loop as .github/workflows/tests.yml)
for pyproj in $(find . -name pyproject.toml -not -path "./.venv/*" -not -path "*/.venv/*" | sort); do
    d=$(dirname "$pyproj")
    [ -d "$d/tests" ] || continue
    if [ -n "$FILTER" ] && [[ "$d" != *"$FILTER"* ]]; then continue; fi
    echo "::tier2 $d"
    (cd "$d" && "$UV_BIN" run pytest tests -q) || rc=$?
    [ "$rc" -eq 5 ] && rc=0
done

# Tier 1: pytest-only → shared root venv
for tdir in $(find . -type d -name tests -not -path "./.venv/*" -not -path "*/.venv/*" \
              -not -path "*/site-packages/*" -not -path "*/fixtures/*" \
              -not -path "*/golden/*" | sort); do
    [ -f "$(dirname "$tdir")/pyproject.toml" ] && continue  # tier 2, done above
    ls "$tdir"/test_*.py >/dev/null 2>&1 || continue        # shell/fixture-only dirs
    if [ -n "$FILTER" ] && [[ "$tdir" != *"$FILTER"* ]]; then continue; fi
    echo "::tier1 $tdir"
    ("$UV_BIN" run --project . pytest "$tdir" -q) || rc=$?
    [ "$rc" -eq 5 ] && rc=0
done

exit "$rc"
