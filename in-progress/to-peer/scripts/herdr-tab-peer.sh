#!/usr/bin/env bash
# herdr-tab-peer — create a peer agent in a NEW herdr tab (no pane split).
#   herdr-tab-peer.sh <name> <repo-cwd> [--prompt-file F] [--label L] [--focus]
# Prints JSON: {name, tab_id, pane_id, cwd, status, prompt}.
# Exit: 0 ok · 1 usage/validation · 2 herdr error.
set -euo pipefail

HERDR="${HERDR_BIN:-herdr}"
usage() { echo "usage: herdr-tab-peer.sh <name> <repo-cwd> [--prompt-file F] [--label L] [--focus]" >&2; exit 1; }
jqget() { python3 -c "import json,sys; d=json.load(sys.stdin); print(eval(sys.argv[1]))" "$1"; }

[ $# -ge 2 ] || usage
NAME="$1"; CWD="$2"; shift 2
PROMPT_FILE=""; LABEL=""; FOCUS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --prompt-file) PROMPT_FILE="${2:?--prompt-file needs a path}"; shift 2 ;;
    --label) LABEL="${2:?--label needs text}"; shift 2 ;;
    --focus) FOCUS=1; shift ;;
    *) usage ;;
  esac
done

# validate before touching herdr so offline tests can run
echo "$NAME" | grep -qE '^[a-z][a-z0-9_-]{0,31}$' || { echo "name must match [a-z][a-z0-9_-]{0,31}" >&2; exit 1; }
[ -d "$CWD" ] || { echo "cwd not a directory: $CWD" >&2; exit 1; }
[ -z "$PROMPT_FILE" ] || [ -f "$PROMPT_FILE" ] || { echo "prompt file not found: $PROMPT_FILE" >&2; exit 1; }
[ -n "${HERDR_ENV:-}" ] || { echo "HERDR_ENV=1 missing: run inside a herdr pane (see herdr skill)" >&2; exit 1; }

CWD="${CWD%/}"
[ -n "$LABEL" ] || LABEL="$NAME"

TAB_ARGS=(--cwd "$CWD" --label "$LABEL")
[ -z "$FOCUS" ] && TAB_ARGS+=(--no-focus)

TAB_JSON=$("$HERDR" tab create "${TAB_ARGS[@]}")
TAB_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['tab']['tab_id']")
PANE_ID=$(printf '%s' "$TAB_JSON" | jqget "d['result']['root_pane']['pane_id']")

START_JSON=$("$HERDR" agent start "$NAME" --kind pi --pane "$PANE_ID")
STATUS=$(printf '%s' "$START_JSON" | jqget "d['result']['agent'].get('agent_status','?')")

PROMPT_STATE=none
if [ -n "$PROMPT_FILE" ]; then
  "$HERDR" agent prompt "$NAME" "$(cat "$PROMPT_FILE")" >/dev/null
  PROMPT_STATE=sent
fi

python3 -c 'import json,sys; print(json.dumps(dict(zip(sys.argv[1::2], sys.argv[2::2]))))' \
  name "$NAME" tab_id "$TAB_ID" pane_id "$PANE_ID" cwd "$CWD" status "$STATUS" prompt "$PROMPT_STATE"
