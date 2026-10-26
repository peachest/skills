#!/usr/bin/env bash
# Tests for herdr-tab-peer.sh.
# Offline cases are hermetic: t() always strips HERDR_ENV so no test can touch
# herdr regardless of where it runs. Live smoke cases (only inside a real herdr
# env) cover: creation+verify (exit 4 = needs-workspace-init for a non-workspace
# cwd), ws pinning, and full identity registration against a temp workspace.
set -uo pipefail
S=$(cd "$(dirname "$0")/../scripts" && pwd)
pass=0; fail=0
t() { # t <desc> <expected-exit> <args...>
  local desc="$1" want="$2"; shift 2
  if env -u HERDR_ENV bash "$S/herdr-tab-peer.sh" "$@" >/dev/null 2>&1; then got=0; else got=$?; fi
  if [ "$got" = "$want" ]; then pass=$((pass+1)); echo "PASS $desc";
  else fail=$((fail+1)); echo "FAIL $desc (exit $got, want $want)"; fi
}

t "no args → usage(1)"            1
t "two positional args → usage(1)"  1 foo /tmp extra
t "bad name chars → 1"            1 BadName /tmp
t "name too long → 1"            1 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa /tmp
t "nonexistent cwd → 1"           1 okname /nonexistent-dir-xyz
t "missing prompt-file → 1"       1 okname /tmp --prompt-file /nonexistent-xyz
t "--machine without value → 1"   1 okname /tmp --machine
t "--description without value → 1" 1 okname /tmp --description
t "--machine + --runtime mutually exclusive → 1" 1 okname /tmp --machine m1 --runtime dev
# every HERDR_ENV-sensitive path must fail at the gate when scrubbed (hermetic)
t "HERDR_ENV scrubbed → 1 (no herdr call)" 1 okname /tmp
t "--prompt-file - scrubbed → 1 at HERDR gate" 1 okname /tmp --prompt-file -
t "--caller-ws scrubbed → 1 at HERDR gate" 1 okname /tmp --caller-ws
t "--machine bypasses HERDR_ENV gate (remote cwd ok, fails later at herdr)" 2 okname /tmp --machine nonexistent-machine-xyz

# live smoke: only meaningful inside a real herdr env
if [ "${HERDR_ENV:-}" = 1 ] && command -v herdr >/dev/null 2>&1; then
  # 1. creation + fused verify + needs-workspace-init (cwd /tmp has no identity ws)
  OUT=$(bash "$S/herdr-tab-peer.sh" to-peer-smoke /tmp --label to-peer-smoke 2>/dev/null); RC=$?
  if [ "$RC" = 4 ] && python3 -c "
import json,sys
d=json.loads(sys.argv[1])
assert d['identity']=='needs-workspace-init', d
assert d['status'] in ('idle','working'), d
assert len(d['session_id'])>10, d
assert d['pane_id'] and d['tab_id'], d
" "$OUT"; then pass=$((pass+1)); echo "PASS live smoke: create+verify, exit 4 needs-workspace-init, session_id captured";
  else fail=$((fail+1)); echo "FAIL live smoke (rc=$RC): $OUT"; fi
  TAB1=$(printf '%s' "$OUT" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tab_id"])' 2>/dev/null)
  [ -n "$TAB1" ] && herdr tab close "$TAB1" >/dev/null 2>&1

  # 2. full identity registration against a temp workspace (no --machine)
  T=$(mktemp -d); mkdir -p "$T/.agents/agents"
  OUT2=$(bash "$S/herdr-tab-peer.sh" to-peer-reg-smoke "$T" --label to-peer-reg-smoke --description "test identity" 2>/dev/null); RC2=$?
  if [ "$RC2" = 0 ] && python3 -c "
import json,sys,os
d=json.loads(sys.argv[1])
assert d['identity']=='registered', d
ws=d['workspace_id']; tab=d['tab_id']
assert os.path.isfile(os.path.join(sys.argv[2],'.agents/agents/to-peer-reg-smoke/AGENT.json'))
import json as j
a=j.load(open(os.path.join(sys.argv[2],'.agents/agents/to-peer-reg-smoke/AGENT.json')))
assert a['name']=='to-peer-reg-smoke' and a['description']=='test identity', a
log=open(os.path.join(sys.argv[2],'.agents/agents/to-peer-reg-smoke/sessions.log')).read()
assert d['session_id'] in log and 'to-peer dispatch' in log, log
assert 'endedAt\": null' in log or 'endedAt\":null' in log, log
" "$OUT2" "$T"; then pass=$((pass+1)); echo "PASS live smoke: identity registered (AGENT.json + sessions.log row with sessionId)";
  else fail=$((fail+1)); echo "FAIL registration smoke (rc=$RC2): $OUT2"; fi
  TAB2=$(printf '%s' "$OUT2" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tab_id"])' 2>/dev/null)
  [ -n "$TAB2" ] && herdr tab close "$TAB2" >/dev/null 2>&1
  # re-registration of the same name → identity conflict exit 3, nothing created
  OUT3=$(bash "$S/herdr-tab-peer.sh" to-peer-reg-smoke "$T" 2>/dev/null); RC3=$?
  if [ "$RC3" = 3 ] && printf '%s' "$OUT3" | grep -q '"error": *"identity_conflict"'; then
    pass=$((pass+1)); echo "PASS live smoke: identity re-registration → conflict exit 3 before any tab created"
  else fail=$((fail+1)); echo "FAIL conflict smoke (rc=$RC3): $OUT3"; fi
  rm -rf "$T"

  # 3. ws pinning: create with explicit ws id, read-back must equal it
  WSTEST=$(herdr workspace list | python3 -c "import json,sys; ws=json.load(sys.stdin)['result']['workspaces']; print(ws[0]['workspace_id'] if ws else '')")
  if [ -n "$WSTEST" ]; then
    OUT4=$(bash "$S/herdr-tab-peer.sh" to-peer-ws-smoke /tmp --workspace "$WSTEST" 2>/dev/null); RC4=$?
    if python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d['workspace_id']=='$WSTEST' else 1)" <<< "$OUT4"; then pass=$((pass+1)); echo "PASS ws smoke (created in $WSTEST)";
    else fail=$((fail+1)); echo "FAIL ws smoke (rc=$RC4): $OUT4"; fi
    herdr tab close "$(printf '%s' "$OUT4" | python3 -c 'import json,sys; print(json.load(sys.stdin)["tab_id"])' 2>/dev/null)" >/dev/null 2>&1 || true
  fi
else
  echo "SKIP live smoke (not in herdr env)"
fi

echo "----"; echo "pass=$pass fail=$fail"; exit $fail
