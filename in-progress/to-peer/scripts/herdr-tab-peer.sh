#!/usr/bin/env bash
# herdr-tab-peer — create a peer agent in a NEW herdr tab (no pane split).
#   herdr-tab-peer.sh <name> [repo-cwd] [--workspace W] [--prompt-file F|-] [--label L] [--focus] [--runtime R]
# repo-cwd defaults to $PWD. --workspace accepts a workspace id (w3) or label
# (exact match first, then fragment; ambiguity = error listing candidates).
# --prompt-file - reads the prompt from stdin. --runtime R targets another herdr
# session (herdr --session R ...), e.g. creating in the dev runtime from elsewhere.
# Prints JSON: {name, tab_id, pane_id, workspace_id, cwd, status, prompt}.
# Exit: 0 ok · 1 usage/validation · 2 herdr error.
set -euo pipefail

HERDR="${HERDR_BIN:-herdr}"
usage() { echo "usage: herdr-tab-peer.sh <name> [repo-cwd] [--workspace W] [--prompt-file F|-] [--label L] [--focus]" >&2; exit 1; }
jqget() { python3 -c "import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }

[ $# -ge 1 ] || usage
NAME="$1"; shift
CWD=""; WORKSPACE=""; PROMPT_FILE=""; LABEL=""; FOCUS=""; RUNTIME=""
hr() { "$HERDR" ${RUNTIME:+--session "$RUNTIME"} "$@"; }
while [ $# -gt 0 ]; do
  case "$1" in
    --runtime) RUNTIME="${2:?--runtime needs a herdr session name}"; shift 2 ;;
    --workspace) WORKSPACE="${2:?--workspace needs an id or label}"; shift 2 ;;
    --prompt-file) PROMPT_FILE="${2:?--prompt-file needs a path or -}"; shift 2 ;;
    --label) LABEL="${2:?--label needs text}"; shift 2 ;;
    --focus) FOCUS=1; shift ;;
    *) if [ -z "$CWD" ]; then CWD="$1"; shift; else usage; fi ;;
  esac
done

# validate before touching herdr so offline tests can run
echo "$NAME" | grep -qE '^[a-z][a-z0-9_-]{0,31}$' || { echo "name must match [a-z][a-z0-9_-]{0,31}" >&2; exit 1; }
CWD="${CWD:-$PWD}"; CWD="${CWD%/}"
[ -d "$CWD" ] || { echo "cwd not a directory: $CWD" >&2; exit 1; }
[ -z "$PROMPT_FILE" ] || [ "$PROMPT_FILE" = "-" ] || [ -f "$PROMPT_FILE" ] || { echo "prompt file not found: $PROMPT_FILE" >&2; exit 1; }
[ -n "${HERDR_ENV:-}" ] || { echo "HERDR_ENV=1 missing: run inside a herdr pane (see herdr skill)" >&2; exit 1; }
[ -n "$LABEL" ] || LABEL="$NAME"

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

TAB_ARGS=(--cwd "$CWD" --label "$LABEL")
[ -n "$WORKSPACE" ] && TAB_ARGS+=(--workspace "$WORKSPACE")
[ -z "$FOCUS" ] && TAB_ARGS+=(--no-focus)

TAB_JSON=$(hr tab create "${TAB_ARGS[@]}")
TAB_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['tab']['tab_id']")
PANE_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['root_pane']['pane_id']")
# actual ws of the created tab (daemon prefix migration can rewrite ids — read back, never echo the input)
WS_ACTUAL=$(printf '%s' "$TAB_JSON" | jqget "d['result']['tab']['workspace_id']")
[ -n "$WORKSPACE" ] && [ "$WS_ACTUAL" != "$WORKSPACE" ] && echo "note: workspace resolved to $WS_ACTUAL" >&2

START_JSON=$(hr agent start "$NAME" --kind pi --pane "$PANE_ID")
STATUS=$(printf '%s' "$START_JSON" | jqget "d['result']['agent'].get('agent_status','?')")

PROMPT_STATE=none
if [ -n "$PROMPT_FILE" ]; then
  if [ "$PROMPT_FILE" = "-" ]; then
    hr agent prompt "$NAME" "$(cat)" >/dev/null
  else
    hr agent prompt "$NAME" "$(cat "$PROMPT_FILE")" >/dev/null
  fi
  PROMPT_STATE=sent
fi

python3 -c 'import json,sys; print(json.dumps(dict(zip(sys.argv[1::2], sys.argv[2::2]))))' \
  name "$NAME" tab_id "$TAB_ID" pane_id "$PANE_ID" workspace_id "$WS_ACTUAL" cwd "$CWD" status "$STATUS" prompt "$PROMPT_STATE"
