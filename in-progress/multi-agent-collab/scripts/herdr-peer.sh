#!/usr/bin/env bash
# herdr-peer — bootstrap a named peer agent in one step.
#   herdr-peer.sh <name> <repo-cwd> [right|down] [--wait-ready MS]
# name: [a-z][a-z0-9_-]{0,31} (pitfall #18). Prints JSON: {pane_id, ...}.
# Exit: 0 ok · 1 usage · 2 herdr error.
set -euo pipefail

HERDR="${HERDR_BIN:-herdr}"
usage() { echo "usage: herdr-peer.sh <name> <repo-cwd> [right|down] [--wait-ready MS]" >&2; exit 1; }
[ $# -ge 2 ] || usage
NAME="$1"; CWD="$2"; shift 2
DIR="right"
while [ $# -gt 0 ]; do
  case "$1" in
    right|down) DIR="$1"; shift ;;
    --wait-ready) WAIT="${2:?--wait-ready needs a value}"; shift 2 ;;
    *) usage ;;
  esac
done
echo "$NAME" | grep -qE '^[a-z][a-z0-9_-]{0,31}$' || { echo "name must match [a-z][a-z0-9_-]{0,31} (pitfall #18)" >&2; exit 1; }
[ -d "$CWD" ] || { echo "cwd not a directory: $CWD" >&2; exit 1; }

# wide caller pane → split right; tall → down (herdr skill geometry rule)
SPLIT_OUT=$("$HERDR" pane split --current --direction "$DIR" --cwd "$CWD" --no-focus)
PANE_ID=$(printf '%s' "$SPLIT_OUT" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if 'error' in d: sys.stderr.write('herdr error: '+json.dumps(d['error'])+'\n'); sys.exit(2)
print(d['result']['pane']['pane_id'])")

"$HERDR" agent start "$NAME" --kind pi --pane "$PANE_ID" >/dev/null

if [ -n "${WAIT:-}" ]; then
  "$HERDR" agent wait "$PANE_ID" --until idle --timeout "$WAIT" >/dev/null 2>&1 || true
fi

python3 -c 'import json,sys; print(json.dumps({"pane_id":sys.argv[1],"name":sys.argv[2],"cwd":sys.argv[3]}))' "$PANE_ID" "$NAME" "$CWD"
