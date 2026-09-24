#!/usr/bin/env bash
# check-env.sh — verify the herdr peer tools' runtime assumptions.
# PASS = usable · WARN = usable with caveats (exit 0) · FAIL = exit 1.
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERDR="${HERDR_BIN:-herdr}"

# 0. runtime.conf (node-specific overrides) — sourced if present (authoring-conventions ①)
[ -f "$DIR/runtime.conf" ] && . "$DIR/runtime.conf"
HERDR="${HERDR_BIN:-herdr}"

# 1. python3 must exist — every tool below is python (P1: a missing python3
#    used to produce a false PASS with every tool dead)
if ! command -v python3 >/dev/null 2>&1; then
  echo "FAIL  python3 not found — all peer tools are python and cannot run. Install python3."
  exit 1
fi
echo "PASS  python3 available"

# 2. herdr binary must execute (not just exist — node-recovery lesson)
if command -v "$HERDR" >/dev/null 2>&1 && "$HERDR" --version >/dev/null 2>&1; then
  echo "PASS  herdr binary: $($HERDR --version 2>/dev/null | head -1)"
else
  echo "FAIL  herdr not executable (HERDR_BIN=$HERDR). Install: https://herdr.dev → npm i -g; then rerun."
  exit 1
fi

# 3. server reachable + envelope parseable (the exact thing the tools wrap).
#    NOTE: bare `agent list` only probes the CURRENT runtime (pitfall #27) —
#    per-runtime health is verified by herdr-resolve.py at call time.
LIST=$("$HERDR" agent list 2>&1 || true)
if printf '%s' "$LIST" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'error' not in d, d.get('error')
assert isinstance((d.get('result') or {}).get('agents'), list)
" 2>/dev/null; then
  N=$(printf '%s' "$LIST" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['result']['agents']))")
  echo "PASS  herdr server reachable (current runtime), envelope parses ($N agents visible)"
else
  echo "WARN  herdr server unreachable or envelope changed — resolve/send will exit 2 until fixed (start herdr server?)"
fi

# 4. scripts present and executable
fail=0
for s in herdr-resolve.py herdr-send.py herdr-peer.sh; do
  if [ -x "$DIR/$s" ]; then
    echo "PASS  scripts/$s executable"
  elif [ -f "$DIR/$s" ]; then
    echo "FAIL  scripts/$s exists but not executable: chmod +x"
    fail=1
  else
    echo "FAIL  scripts/$s missing"
    fail=1
  fi
done
[ "$fail" -eq 0 ] || exit 1
echo "check-env: PASS"
