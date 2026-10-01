#!/usr/bin/env bash
# Offline tests for herdr-tab-peer.sh: usage/validation paths only (no herdr calls).
set -uo pipefail
S=$(cd "$(dirname "$0")/../scripts" && pwd)
pass=0; fail=0
t() { # t <desc> <expected-exit> <args...>
  local desc="$1" want="$2"; shift 2
  if bash "$S/herdr-tab-peer.sh" "$@" >/dev/null 2>&1; then got=0; else got=$?; fi
  if [ "$got" = "$want" ]; then pass=$((pass+1)); echo "PASS $desc";
  else fail=$((fail+1)); echo "FAIL $desc (exit $got, want $want)"; fi
}

t "no args → usage(1)"            1
t "one arg → usage(1)"            1 foo
t "bad name chars → 1"            1 BadName /tmp
t "name too long → 1"             1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa /tmp
t "nonexistent cwd → 1"           1 okname /nonexistent-dir-xyz
t "prompt-file missing → 1"       1 okname /tmp --prompt-file /nonexistent-f.txt

# assert the script refuses before touching herdr when HERDR_ENV unset
t "HERDR_ENV unset → 1 (no herdr call)" 1 okname /tmp
# rerun that case with HERDR_ENV actually scrubbed from the child env
if env -u HERDR_ENV bash "$S/herdr-tab-peer.sh" okname /tmp >/dev/null 2>&1; then got=0; else got=$?; fi
if [ "$got" = "1" ]; then pass=$((pass+1)); echo "PASS HERDR_ENV scrubbed → 1"; else fail=$((fail+1)); echo "FAIL HERDR_ENV scrubbed (exit $got, want 1)"; fi

# if we happen to be in a herdr env, smoke-test against the real session (skip otherwise)
if [ "${HERDR_ENV:-}" = 1 ] && command -v herdr >/dev/null 2>&1; then
  OUT=$(bash "$S/herdr-tab-peer.sh" to-peer-smoke /tmp --label to-peer-smoke 2>&1)
  if echo "$OUT" | grep -q '"pane_id"'; then pass=$((pass+1)); echo "PASS live smoke (tab created)";
  else fail=$((fail+1)); echo "FAIL live smoke: $OUT"; fi
  herdr tab close "$(echo "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tab_id"])')" >/dev/null 2>&1 || true
else
  echo "SKIP live smoke (not in herdr env)"
fi

echo "----"; echo "pass=$pass fail=$fail"; exit $fail
