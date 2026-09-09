#!/usr/bin/env bash
# frontier.sh — wayfinder map + open tickets + limbo (pending-MR-closure) state for a repo.
# Usage: frontier.sh <repo-path>
# Output: one line per open map, then limbo lines:
#   map: #<map-iid> <title> | open: #<n>,#<n> | pending: #<n>-#<n> (await !<mr>)
#   pending = open ticket whose closer MR is still open (Closes #n in an open MR's commits/description)
#   — the zero-frontier limbo the label query cannot see.
# No open maps → no output (silence is correct for "no map here").
set -uo pipefail
GLAB="${GLAB_BIN:-$HOME/.nix-profile/bin/glab}"
GIT=/usr/bin/git

host_from_url() {
    case "$1" in
        ssh://*) printf '%s' "$1" | sed -e 's|^ssh://[^@]*@||' -e 's|[:/].*||' ;;
        https://*|http://*) printf '%s' "$1" | sed -e 's|^\(https\?\)://||' -e 's|[:/].*||' ;;
        *) printf '%s' "$1" | sed -e 's|^[^@]*@||' -e 's|[:/].*||' ;;
    esac
}

repo="${1:?usage: frontier.sh <repo-path>}"
remote_url=$($GIT -C "$repo" remote get-url origin 2>/dev/null) || { echo "no origin remote: $repo" >&2; exit 1; }
case "$remote_url" in
    ssh://*) proj_path=$(printf '%s' "$remote_url" | sed -e 's|^ssh://[^/]*/||' -e 's/\.git$//') ;;
    *:*) proj_path=$(printf '%s' "$remote_url" | sed -e 's/^[^:]*://' -e 's/\.git$//') ;;
    *)    proj_path=$(printf '%s' "$remote_url" | sed -e 's|^.*://[^/]*/||' -e 's/\.git$//') ;;
esac
proj_enc=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$proj_path")
export GITLAB_HOST=$(host_from_url "$remote_url")

fetch() { $GLAB api "$1" 2>/dev/null || { sleep 1; $GLAB api "$1" 2>/dev/null; } }

# Open maps (label wayfinder:map). Note: some instances miss labels on old issues;
# zero maps here is a query-method signal, not proof — the caller may widen the query.
maps_json=$(fetch "projects/$proj_enc/issues?labels=wayfinder%3Amap&state=opened&per_page=20") || exit 1
open_issues_json=$(fetch "projects/$proj_enc/issues?state=opened&per_page=100") || exit 1
open_mrs_json=$(fetch "projects/$proj_enc/merge_requests?state=opened&per_page=50") || exit 1

python3 - "$maps_json" "$open_issues_json" "$open_mrs_json" << 'PYEOF'
import json, re, sys
maps, issues, mrs = (json.loads(a) for a in sys.argv[1:4])
if not maps: sys.exit(0)
map_iids = {m["iid"] for m in maps}
# ponytail: Closes in MR description/title only; commit-message Closes (the wayfinder
# convention) needs the /closes_issues endpoint per MR — add when limbo under-detects.
closing = set()
for mr in mrs:
    text = (mr.get("description") or "") + " " + (mr.get("title") or "")
    for chunk in re.findall(r'Closes?\s+((?:#\d+[,\s]*)+)', text):
        closing.update(int(n) for n in re.findall(r'\d+', chunk))
for m in maps:
    mid = m["iid"]
    opens = [i["iid"] for i in issues if i["iid"] not in map_iids]
    pending = [i for i in opens if i in closing]
    frontier = [i for i in opens if i not in closing]
    parts = [f"map: #{mid} {(m.get('title') or '')[:40]}"]
    parts.append("open: " + (",".join(f"#{i}" for i in frontier) if frontier else "none"))
    if pending:
        parts.append("pending: " + ",".join(f"#{i}" for i in pending) + " (await open MR)")
    print(" | ".join(parts))
PYEOF
