#!/usr/bin/env bash
# check-env.sh — verify the herdr peer tools' runtime assumptions.
# PASS = usable · WARN = usable with caveats · FAIL = exit 1 (fix first).
set -uo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERDR="${HERDR_BIN:-herdr}"
fail=0

# 1. herdr binary must execute (not just exist — node-recovery lesson)
if command -v "$HERDR" >/dev/null 2>&1 && "$HERDR" --version >/dev/null 2>&1; then
  echo "PASS  herdr binary: $($HERDR --version 2>/dev/null | head -1)"
else
  echo "FAIL  herdr not executable (HERDR_BIN=$HERDR). Install: https://herdr.dev → npm i -g; then rerun."
  exit 1
fi

# 2. server reachable + envelope parseable (the exact thing the tools wrap)
LIST=$("$HERDR" agent list 2>&1 | head -c 20000 || true)
if printf '%s' "$LIST" | python3 -c "
import json,sys
d=json.load(sys.stdin)
assert 'error' not in d, d.get('error')
assert isinstance((d.get('result') or {}).get('agents'), list)
" 2>/dev/null; then
  N=$(printf '%s' "$LIST" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['result']['agents']))")
  echo "PASS  herdr server reachable, envelope parses ($N agents visible)"
else
  echo "WARN  herdr server unreachable or envelope changed — resolve/send will exit 2 until fixed (start herdr server?)"
fi

# 3. scripts present and executable
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
