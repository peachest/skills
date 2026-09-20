#!/usr/bin/env bash
# replay-compare environment check. FAIL output = fix instruction.
set -u
FAIL=0
say() { echo "$1"; }
fail() { echo "FAIL  $1"; FAIL=1; }

command -v python3 >/dev/null 2>&1 && say "PASS  python3: $(command -v python3)" || fail "python3 not on PATH"
command -v node >/dev/null 2>&1 && say "PASS  node: $(node --version 2>/dev/null)" || fail "node not on PATH"
command -v npx >/dev/null 2>&1 && say "PASS  npx: $(command -v npx)" || fail "npx not on PATH (needed to run tsx runner)"
npx --no-install tsx --version >/dev/null 2>&1 \
  && say "PASS  tsx available" \
  || say "WARN  tsx not cached yet — first runner run downloads it via npx (needs network/proxy)"

[ "$FAIL" -eq 0 ] && echo "ALL OK" || echo "FIX FAILURES ABOVE"
exit "$FAIL"
