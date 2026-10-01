#!/usr/bin/env bash
# check-env — verify to-peer runtime assumptions.
set -uo pipefail
FAIL=0
say() { echo "$1"; }

SKILL_DIR=$(cd "$(dirname "$0")/.." && pwd)

if command -v herdr >/dev/null 2>&1; then
  say "PASS herdr CLI: $(command -v herdr)"
else
  say "FAIL herdr CLI not found in PATH — install herdr"
  FAIL=1
fi

if [ "${HERDR_ENV:-}" = 1 ]; then
  say "PASS HERDR_ENV=1 (inside herdr pane)"
else
  say "WARN HERDR_ENV!=1 — tab create / agent start will refuse at runtime; run check from inside a herdr pane"
fi

if bash -n "$SKILL_DIR/scripts/herdr-tab-peer.sh" 2>/dev/null; then
  say "PASS herdr-tab-peer.sh syntax"
else
  say "FAIL herdr-tab-peer.sh has syntax errors"
  FAIL=1
fi

exit $FAIL
