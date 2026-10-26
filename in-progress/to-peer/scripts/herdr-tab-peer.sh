#!/usr/bin/env bash
# herdr-tab-peer — create a peer agent in a NEW herdr tab (no pane split),
# with fused verify and identity registration (SPEC .agents/agents).
#   herdr-tab-peer.sh <name> [repo-cwd] [--workspace W] [--prompt-file F|-]
#     [--label L] [--focus] [--runtime R] [--machine M] [--caller-ws]
#     [--description D]
# repo-cwd defaults to $PWD. --workspace accepts a workspace id (w3) or label
# (exact match first, then fragment; ambiguity = error listing candidates).
# --caller-ws: resolve the CALLER pane's workspace from $HERDR_PANE_ID and pin
# the tab there (used by the herdr_peer tool for its "current ws" default).
# --prompt-file - reads the prompt from stdin. --runtime R targets another herdr
# session (herdr --session R ...). --machine M creates the peer on a SAVED SSH
# MACHINE (herdr >= 0.9.5); mutually exclusive with --runtime; cwd is a REMOTE
# path. --description fills AGENT.json (default: "to-peer created peer").
# Prints JSON: {name, machine, tab_id, pane_id, workspace_id, cwd, status,
# prompt, identity, session_id?}. identity ∈ registered | needs-workspace-init
# | skipped-remote-machine | skipped-no-session-id.
# Exit: 0 ok · 1 usage/validation · 2 herdr/verify error · 3 name/identity
# conflict (JSON on stdout names the existing holder; reuse needs user decision)
# · 4 peer created but identity workspace missing — ASK the user whether to
# initialize .agents/agents/ (SPEC §2: user confirms new workspaces; never
# create silently, never skip silently).
set -euo pipefail

HERDR="${HERDR_BIN:-herdr}"
usage() { echo "usage: herdr-tab-peer.sh <name> [repo-cwd] [--workspace W] [--prompt-file F|-] [--label L] [--focus] [--runtime R | --machine M] [--caller-ws] [--description D]" >&2; exit 1; }
jqget() { python3 -c "import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }
now_iso() { date -u +%Y-%m-%dT%H:%M:%SZ; }

[ $# -ge 1 ] || usage
NAME="$1"; shift
CWD=""; WORKSPACE=""; PROMPT_FILE=""; LABEL=""; FOCUS=""; RUNTIME=""; MACHINE=""; CALLER_WS=""; DESC=""
hr() { "$HERDR" ${MACHINE:+--machine "$MACHINE"} ${RUNTIME:+--session "$RUNTIME"} "$@"; }
while [ $# -gt 0 ]; do
  case "$1" in
    --machine) MACHINE="${2:?--machine needs a saved machine label (herdr machine list)}"; shift 2 ;;
    --runtime) RUNTIME="${2:?--runtime needs a herdr session name}"; shift 2 ;;
    --workspace) WORKSPACE="${2:?--workspace needs an id or label}"; shift 2 ;;
    --prompt-file) PROMPT_FILE="${2:?--prompt-file needs a path or -}"; shift 2 ;;
    --label) LABEL="${2:?--label needs text}"; shift 2 ;;
    --description) DESC="${2:?--description needs text}"; shift 2 ;;
    --caller-ws) CALLER_WS=1; shift ;;
    --focus) FOCUS=1; shift ;;
    *) if [ -z "$CWD" ]; then CWD="$1"; shift; else usage; fi ;;
  esac
done
[ -z "$MACHINE" ] || [ -z "$RUNTIME" ] || { echo "--machine and --runtime are mutually exclusive" >&2; exit 1; }

# validate before touching herdr so offline tests can run
echo "$NAME" | grep -qE '^[a-z][a-z0-9_-]{0,31}$' || { echo "name must match [a-z][a-z0-9_-]{0,31}" >&2; exit 1; }
CWD="${CWD:-$PWD}"; CWD="${CWD%/}"
# --machine: cwd is a REMOTE path, uncheckable locally — only require non-empty
if [ -z "$MACHINE" ] && [ ! -d "$CWD" ]; then echo "cwd not a directory: $CWD" >&2; exit 1; fi
if [ -n "$MACHINE" ] && [ -z "$CWD" ]; then echo "empty cwd" >&2; exit 1; fi
[ -z "$PROMPT_FILE" ] || [ "$PROMPT_FILE" = "-" ] || [ -f "$PROMPT_FILE" ] || { echo "prompt file not found: $PROMPT_FILE" >&2; exit 1; }
# HERDR_ENV gate: required for local creation; --machine forwards over SSH and
# works from any shell (verified 2026-10-15 — the probe ran from a plain shell)
if [ -z "$MACHINE" ] && [ -z "${HERDR_ENV:-}" ]; then
  echo "HERDR_ENV=1 missing: run inside a herdr pane, or pass --machine for cross-machine creation" >&2; exit 1
fi
[ -n "$LABEL" ] || LABEL="$NAME"

# --- workspace resolution -----------------------------------------------------
# --caller-ws: pin to the caller pane's own ws (from $HERDR_PANE_ID).
# Else with no --workspace: infer from cwd — the workspace whose label equals
# the cwd's tail segment (e.g. /…/skills → "skills" ws). The daemon's bare
# `tab create` default is the most-recently-active ws, NOT the cwd's project ws
# (2026-10-19: three skills peers landed in the pi-mypackage ws despite correct
# cwd), so an inference failure must be loud, never silent. Ambiguous label
# (two ws sharing a label) → ask via stderr, no guess.
if [ -n "$CALLER_WS" ] && [ -z "$WORKSPACE" ] && [ -z "$MACHINE" ]; then
  if [ -n "${HERDR_PANE_ID:-}" ]; then
    WORKSPACE=$(hr agent list 2>/dev/null | python3 -c "
import json,sys
pane=sys.argv[1]
try: d=json.load(sys.stdin)
except Exception: sys.exit()
for a in d.get('result',{}).get('agents',[]):
    if a.get('pane_id')==pane and a.get('workspace_id'):
        print(a['workspace_id']); break
" "$HERDR_PANE_ID") || WORKSPACE=""
    [ -n "$WORKSPACE" ] && echo "note: --caller-ws resolved caller pane $HERDR_PANE_ID → ws $WORKSPACE" >&2
  fi
fi
if [ -z "$WORKSPACE" ] && [ -z "$MACHINE" ]; then
  WS_JSON=$(hr workspace list)
  CWD_TAIL=$(printf '%s' "$CWD" | sed 's:/*$::' | awk -F/ '{print $NF}')
  WS_ID=$(printf '%s' "$WS_JSON" | python3 -c "
import json,sys
ws=json.load(sys.stdin)['result']['workspaces']
tail=sys.argv[1]
m=[w for w in ws if w.get('label')==tail]
if len(m)==1: print(m[0]['workspace_id'])
" "$CWD_TAIL") || exit 2
  if [ -n "$WS_ID" ]; then
    WORKSPACE="$WS_ID"
    echo "note: --workspace omitted — inferred $WS_ID from cwd tail '$CWD_TAIL'; pass --workspace explicitly to override" >&2
  else
    CANDIDATES=$(printf '%s' "$WS_JSON" | python3 -c "
import json,sys
ws=json.load(sys.stdin)['result']['workspaces']
print(', '.join(w['workspace_id']+'='+w['label'] for w in ws))")
    echo "WARN: no --workspace and cwd tail '$CWD_TAIL' matches no workspace label; the tab will land in the daemon default ws (often the last-active one). Candidates: $CANDIDATES" >&2
  fi
fi
# resolve workspace: bare id passes through; otherwise match against workspace list
if [ -n "$WORKSPACE" ]; then
  if ! echo "$WORKSPACE" | grep -qE '^w[0-9A-Za-z]+$'; then
    WS_JSON=$(hr workspace list)
    WS_ID=$(printf '%s' "$WS_JSON" | python3 -c "
import json,sys
ws=json.load(sys.stdin)['result']['workspaces']
q=sys.argv[1]
exact=[w for w in ws if w['label']==q]
if len(exact)==1: print(exact[0]['workspace_id']); sys.exit()
if exact: sys.stderr.write('ambiguous workspace label %r: %s\n' % (q, ', '.join(w['workspace_id']+'='+w['label'] for w in exact))); sys.exit(2)
frag=[w for w in ws if q.lower() in w['label'].lower() or q==w['workspace_id']]
if len(frag)==1: print(frag[0]['workspace_id']); sys.exit()
sys.stderr.write('no %r workspace; candidates: %s\n' % (q, ', '.join(w['workspace_id']+'='+w['label'] for w in ws))); sys.exit(2)
" "$WORKSPACE") || exit 2
    WORKSPACE="$WS_ID"
  fi
fi

# --- identity pre-flight (before creating anything, so abort leaves no litter) --
# SPEC workspace resolution: prefer the MAIN CHECKOUT when cwd is a git
# worktree (wt dirs are disposable; identity is a persistent asset — user
# ruling 2026-10-26), then walk cwd upward. First dir containing
# .agents/agents/ wins. Machine peers: remote fs is out of reach → skip (v1).
IDENTITY_DIR=""; IDENTITY_WS=""; NEEDS_INIT=0
if [ -n "$MACHINE" ]; then
  IDENTITY=skipped-remote-machine
else
  read -r IDENTITY_WS IDENTITY_DIR < <(python3 - "$CWD" <<'PYEOF'
import os, sys
cwd = sys.argv[1]
def wt_main(d):
    g = os.path.join(d, ".git")
    if os.path.isfile(g):
        try: line = open(g).read().strip()
        except Exception: return None
        if line.startswith("gitdir:"):
            gd = os.path.abspath(os.path.normpath(os.path.join(d, line[len("gitdir:"):].strip())))
            parts = gd.split(os.sep)
            if "worktrees" in parts:
                i = len(parts) - 1 - parts[::-1].index("worktrees")
                return os.sep.join(parts[:i - 1])  # strip /worktrees/<name> and /.git
    return None
def chain(d):
    while True:
        yield d
        home = os.path.expanduser("~")
        parent = os.path.dirname(d)
        if d == home or parent == d: return
        d = parent
starts = [s for s in [wt_main(cwd), cwd] if s]
seen = set()
for start in starts:
    for d in chain(start):
        a = os.path.join(d, ".agents", "agents")
        if a in seen: continue
        seen.add(a)
        if os.path.isdir(a):
            print(d, a); sys.exit()
print("", "")
PYEOF
) || { echo "identity ws resolution failed" >&2; exit 2; }
  if [ -z "$IDENTITY_DIR" ]; then
    NEEDS_INIT=1
  elif [ -e "$IDENTITY_DIR/$NAME" ]; then
    # identity name conflict (Q7): abort BEFORE creating the tab; reuse/takeover
    # is the user's call, same contract as the herdr agent-name conflict
    python3 -c 'import json,sys; print(json.dumps({"error":"identity_conflict","name":sys.argv[1],"existing_identity":sys.argv[2],"advice":"reuse via multi-agent-collab (user must supply session id/name), pick another name, or explicitly take over the identity — user decides"}))' "$NAME" "$IDENTITY_DIR/$NAME"
    echo "identity conflict: $IDENTITY_DIR/$NAME already exists; nothing created. Ask the user." >&2
    exit 3
  fi
fi

# --- create the tab ------------------------------------------------------------
TAB_ARGS=(--cwd "$CWD" --label "$LABEL")
[ -n "$WORKSPACE" ] && TAB_ARGS+=(--workspace "$WORKSPACE")
[ -z "$FOCUS" ] && TAB_ARGS+=(--no-focus)

TAB_JSON=$(hr tab create "${TAB_ARGS[@]}")
TAB_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['tab']['tab_id']")
PANE_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['root_pane']['pane_id']")
# actual ws of the created tab (daemon prefix migration can rewrite ids — read back, never echo the input)
WS_ACTUAL=$(printf '%s' "$TAB_JSON" | jqget "d['result']['tab']['workspace_id']")

# --- ws assertion: correct cwd does NOT imply correct ws (2026-10-19/10-26) ----
# mismatch → close the tab and fail loudly, unless it's an id migration
# (requested id vanished from the list while the actual one exists).
if [ -n "$WORKSPACE" ] && [ "$WS_ACTUAL" != "$WORKSPACE" ]; then
  MIGRATED=$(hr workspace list | python3 -c "
import json,sys
ws=json.load(sys.stdin)['result']['workspaces']
ids={w['workspace_id'] for w in ws}
req,act=sys.argv[1],sys.argv[2]
print('yes' if req not in ids and act in ids else 'no')
" "$WORKSPACE" "$WS_ACTUAL") || MIGRATED=no
  if [ "$MIGRATED" = "yes" ]; then
    echo "note: workspace id migrated $WORKSPACE → $WS_ACTUAL (daemon prefix rewrite)" >&2
  else
    hr tab close "$TAB_ID" >/dev/null 2>&1 || true
    echo "WS MISMATCH: asked for $WORKSPACE, tab landed in $WS_ACTUAL — closed the tab, nothing left behind. Resolve the target ws explicitly (herdr workspace list) and retry." >&2
    exit 2
  fi
fi

# --- agent start + name-conflict report ----------------------------------------
START_JSON=$(hr agent start "$NAME" --kind pi --pane "$PANE_ID")
if printf '%s' "$START_JSON" | grep -q '"error"'; then
  # report the existing holder so the caller can ask the user (reuse vs rename)
  EXISTING=$(printf '%s' "$START_JSON" | python3 -c "
import json,sys
d=json.load(sys.stdin)
e=d.get('error') or d.get('result',{}).get('error') or {}
print(json.dumps(e))" 2>/dev/null || printf '%s' "$START_JSON")
  hr tab close "$TAB_ID" >/dev/null 2>&1 || true
  python3 -c 'import json,sys; print(json.dumps({"error":"agent_name_taken","name":sys.argv[1],"herdr_error":json.loads(sys.argv[2]) if sys.argv[2].startswith("{") else sys.argv[2],"advice":"reuse via multi-agent-collab (user must supply session id/name), or pick another name — user decides"}))' "$NAME" "$EXISTING" 2>/dev/null \
    || { echo "agent name conflict: $NAME already used. Tab closed. Ask the user." >&2; }
  exit 3
fi

# --- fused verify: bounded liveness poll + session UUID grab --------------------
# agent list output has no name field — match by pane id (unique)
SESSION_ID=""
VERIFIED=false
STATUS="?"
for _ in 1 2 3 4 5 6; do
  LINE=$(hr agent list 2>/dev/null | python3 -c "
import json,sys
pane=sys.argv[1]
try: d=json.load(sys.stdin)
except Exception: sys.exit()
for a in d.get('result',{}).get('agents',[]):
    if a.get('pane_id')==pane:
        sess=(a.get('agent_session') or {}).get('value','')
        import re
        m=re.search(r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', sess)
        print(a.get('agent_status','?'), m.group(1) if m else '')
        break
" "$PANE_ID") || LINE=""
  if [ -n "$LINE" ]; then
    STATUS=$(printf '%s' "$LINE" | awk '{print $1}')
    SESSION_ID=$(printf '%s' "$LINE" | awk '{print $2}')
    VERIFIED=true
    break
  fi
  sleep 2
done
if [ "$VERIFIED" != "true" ]; then
  hr tab close "$TAB_ID" >/dev/null 2>&1 || true
  echo "VERIFY FAILED: agent $NAME not alive in agent list after start (pane $PANE_ID). Tab closed." >&2
  exit 2
fi

PROMPT_STATE=none
if [ -n "$PROMPT_FILE" ]; then
  if [ "$PROMPT_FILE" = "-" ]; then
    hr agent prompt "$NAME" "$(cat)" >/dev/null
  else
    hr agent prompt "$NAME" "$(cat "$PROMPT_FILE")" >/dev/null
  fi
  PROMPT_STATE=sent
fi

# --- identity registration ------------------------------------------------------
if [ "$NEEDS_INIT" = "1" ]; then
  IDENTITY=needs-workspace-init
elif [ -n "$MACHINE" ]; then
  IDENTITY=skipped-remote-machine
else
  D="$IDENTITY_DIR/$NAME"
  mkdir -p "$D"
  [ -n "$DESC" ] || DESC="to-peer created peer; charter filled by on-duty session"
  python3 - "$D" "$NAME" "$IDENTITY_WS" "$DESC" <<'PYEOF'
import json, os, sys, datetime
d, name, ws, desc = sys.argv[1:5]
agent = {
    "name": name, "workspace": ws, "description": desc,
    "charter": "charter.md", "peers": [],
    "created": datetime.date.today().isoformat(),
}
json.dump(agent, open(os.path.join(d, "AGENT.json"), "w"), indent=2, ensure_ascii=False)
PYEOF
  cat > "$D/charter.md" <<EOF2
# $NAME

身份由 to-peer 派发创建（$(date -u +%F)）。职责以派发 bootstrap prompt 为准；
当值 session 上岗后补写本文件与 STATE.md / peers.md。
EOF2
  # sessions.log row per SPEC schema; sessionId from the verify step (never
  # hand-written). Missing session id → leave registration to the on-duty
  # session rather than write a broken row.
  if [ -n "$SESSION_ID" ]; then
    printf '{"sessionId": "%s", "startedAt": "%s", "endedAt": null, "note": "to-peer dispatch (tab %s, pane %s)"}\n' \
      "$SESSION_ID" "$(now_iso)" "$TAB_ID" "$PANE_ID" >> "$D/sessions.log"
    IDENTITY=registered
  else
    IDENTITY=skipped-no-session-id
    echo "WARN: session UUID not found in agent list; sessions.log row not written — on-duty session should register itself (agent-session-id tool)" >&2
  fi
fi

python3 -c 'import json,sys; print(json.dumps(dict(zip(sys.argv[1::2], sys.argv[2::2]))))' \
  machine "${MACHINE:-local}" name "$NAME" tab_id "$TAB_ID" pane_id "$PANE_ID" workspace_id "$WS_ACTUAL" cwd "$CWD" status "$STATUS" prompt "$PROMPT_STATE" identity "$IDENTITY" session_id "${SESSION_ID:-}"

[ "$IDENTITY" = "needs-workspace-init" ] && {
  echo "peer created and verified, but no identity workspace (.agents/agents/) found for $CWD. ASK the user whether to initialize one (SPEC §2: user confirms new workspaces) — do not create silently, do not skip silently." >&2
  exit 4
}
exit 0
