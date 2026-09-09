#!/usr/bin/env bash
# mr-state.sh — open (or specific) MR state for a GitLab repo, via glab api.
# Usage: mr-state.sh <repo-path> [--iid N]
#   no --iid: list OPEN MRs for the current branch's project
# Output per MR (TSV): iid|source_branch|state|merge_status|sha|title|web_url|blocking
#   blocking: best-effort cross-repo dependency — first "Depends on"/"依赖"/"阻塞" + !N match in description
# Uses glab api only (no hand-rolled token auth); JSON parsed with python3 stdlib.
set -uo pipefail
GLAB="${GLAB_BIN:-$HOME/.nix-profile/bin/glab}"
GIT=/usr/bin/git

# Derive GitLab host from the origin remote so `glab api` hits the right instance
# (multi-instance env: bare glab defaults to another instance and gets 401).
host_from_url() {
    case "$1" in
        ssh://*) printf '%s' "$1" | sed -e 's|^ssh://[^@]*@||' -e 's|[:/].*||' ;;
        https://*|http://*) printf '%s' "$1" | sed -e 's|^\(https\?\)://||' -e 's|[:/].*||' ;;
        *) printf '%s' "$1" | sed -e 's|^[^@]*@||' -e 's|[:/].*||' ;;
    esac
}

repo="${1:?usage: mr-state.sh <repo-path> [--iid N]}"; shift || true
iid=""
while [ $# -gt 0 ]; do
    case "$1" in
        --iid) iid="$2"; shift 2 ;;
        *) shift ;;
    esac
done

# Project path from the git remote (gitblue ssh form: host:group/project.git)
remote_url=$($GIT -C "$repo" remote get-url origin 2>/dev/null) || { echo "no origin remote: $repo" >&2; exit 1; }
# strip proto/host, keep group/project
proj_path=$(printf '%s' "$remote_url" | sed -e 's|.*[:/]||; s|\.git$||; s|^.*://[^/]*/||')
# robust: take everything after the first colon (ssh) or after host (https), minus .git
case "$remote_url" in
    ssh://*) proj_path=$(printf '%s' "$remote_url" | sed -e 's|^ssh://[^/]*/||' -e 's/\.git$//') ;;
    *:*) proj_path=$(printf '%s' "$remote_url" | sed -e 's/^[^:]*://' -e 's/\.git$//') ;;
    *)    proj_path=$(printf '%s' "$remote_url" | sed -e 's|^.*://[^/]*/||' -e 's/\.git$//') ;;
esac
proj_enc=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$proj_path")
export GITLAB_HOST=$(host_from_url "$remote_url")

if [ -n "$iid" ]; then
    api="projects/$proj_enc/merge_requests/$iid"
    include_desc=1
else
    api="projects/$proj_enc/merge_requests?state=opened&per_page=20"
    include_desc=""
fi

# glab api with one retry (API 404 jitter is a known quirk).
fetch() { $GLAB api "$1" 2>/dev/null || { sleep 1; $GLAB api "$1" 2>/dev/null; } }
json=$(fetch "$api") || { echo "glab api failed for $proj_path" >&2; exit 1; }

python3 - "$json" "$include_desc" << 'PYEOF'
import json, re, sys
raw, include_desc = sys.argv[1], sys.argv[2] == "1"
mrs = [json.loads(raw)] if include_desc else json.loads(raw)
if isinstance(mrs, dict) and "iid" not in mrs: mrs = []
for mr in mrs:
    desc = mr.get("description") or ""
    m = re.search(r'(?:Depends on|depends on|依赖|阻塞于|blocked by)[^\n]*?(!\d+)', desc)
    blocking = m.group(1) if m else ""
    sha = (mr.get("sha") or "")[:8]
    print("|".join([
        str(mr.get("iid","")), mr.get("source_branch",""), mr.get("state",""),
        mr.get("merge_status",""), sha, (mr.get("title","") or "")[:60],
        mr.get("web_url",""), blocking,
    ]))
if not mrs: print("(no open MRs)")
PYEOF
