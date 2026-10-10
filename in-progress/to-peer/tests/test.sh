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
t "two positional args → usage(1)"  1 foo /tmp extra
t "bad name chars → 1"            1 BadName /tmp
t "name too long → 1"             1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa /tmp
t "nonexistent cwd → 1"           1 okname /nonexistent-dir-xyz
# cwd now defaults to $PWD — one-arg form is valid validation, only herdr/HERDR_ENV gates it
if env -u HERDR_ENV bash "$S/herdr-tab-peer.sh" okname >/dev/null 2>&1; then got=0; else got=$?; fi
if [ "$got" = "1" ]; then pass=$((pass+1)); echo "PASS one arg (cwd=$PWD) fails on HERDR_ENV"; else fail=$((fail+1)); echo "FAIL one arg (exit $got, want 1)"; fi
# prompt-file stdin marker passes validation too (reads stdin only after herdr calls)
t "--prompt-file - → fails on HERDR_ENV, not usage"  1 okname /tmp --prompt-file -

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
  # cross-ws smoke: resolve an existing workspace by label/id and create there
  WSTEST=$(herdr workspace list | python3 -c "import json,sys; ws=json.load(sys.stdin)['result']['workspaces']; print(ws[0]['workspace_id'] if ws else '')")
  if [ -n "$WSTEST" ]; then
    OUT2=$(bash "$S/herdr-tab-peer.sh" to-peer-ws-smoke /tmp --workspace "$WSTEST" 2>&1)
    if python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d['workspace_id']=='$WSTEST' else 1)" <<< "$OUT2"; then pass=$((pass+1)); echo "PASS ws smoke (created in $WSTEST)";
    else fail=$((fail+1)); echo "FAIL ws smoke: $OUT2"; fi
    herdr tab close "$(echo "$OUT2" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tab_id"])')" >/dev/null 2>&1 || true
  fi
else
  echo "SKIP live smoke (not in herdr env)"
fi

echo "----"; echo "pass=$pass fail=$fail"; exit $fail
