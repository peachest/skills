#!/usr/bin/env bash
# create-mr preflight — one command, the six info blocks skill steps 1-6 need.
# Read-only: never pushes, never creates.
# Usage: bash <SKILL_DIR>/scripts/preflight.sh [repo-dir]   (default: cwd)
# Requires: git, python3; gh or glab per detected platform.
# Sediments wiki P-001/P-003 (and the 404-discrimination half of P-002).
set -euo pipefail
cd "${1:-.}"

norm_url() {  # any remote URL form → https://host/path (port dropped, .git stripped)
  local u=$1 rest host path
  u=${u%.git}
  case "$u" in
    ssh://git@*)
      rest=${u#ssh://git@}; host=${rest%%/*}; host=${host%%:*}; path=${rest#*/}
      echo "https://$host/$path" ;;
    git@*)  # scp form git@host:group/project
      rest=${u#git@}; host=${rest%%:*}; path=${rest#*:}
      echo "https://$host/$path" ;;
    http://*) echo "${u/http:/https:}" ;;
    *) echo "$u" ;;
  esac
}

# --- REMOTES / PLATFORM -------------------------------------------------
echo "== REMOTES =="
git remote -v | awk '!seen[$2]++ {print $1, $2}'
if [ "$(git remote | wc -l)" -gt 1 ]; then
  echo "MULTI_REMOTE=true —— 必须 ask 用户选择，上下文再明确也不自判"
fi
primary=$(git remote | head -1)   # 多 remote 时仅作信息块基准，最终由用户定
url=$(git remote get-url "$primary")
web=$(norm_url "$url")
case "$url" in *github.com*) platform=gh ;; *) platform=glab ;; esac
echo "primary=$primary  platform=$platform  web=$web"

host=${web#https://}; host=${host%%/*}
path=${web#https://$host/}
enc=${path//\//%2F}

# --- BRANCH (含分支一致性) -----------------------------------------------
branch=$(git rev-parse --abbrev-ref HEAD)
echo "== BRANCH =="
echo "current=$branch  dirty_files=$(git status --porcelain | wc -l)"
default=$(git ls-remote --symref "$primary" HEAD 2>/dev/null \
          | awk '/^ref:/ {sub(/refs\/heads\//, "", $2); print $2}' | head -1)
echo "default_branch=${default:-unknown}"
if git rev-parse -q --verify "remotes/$primary/$branch" >/dev/null 2>&1; then
  echo "unpushed_commits=$(git rev-list --count "remotes/$primary/$branch..HEAD")"
  echo "-- local ahead of remote (branch consistency, check for foreign commits) --"
  git log --oneline "remotes/$primary/$branch..HEAD" | head -5
else
  echo "no remote tracking branch for '$branch' — nothing pushed yet"
fi

# --- TITLE_CANDIDATE ------------------------------------------------------
echo "== TITLE_CANDIDATE =="
if [ -n "${default:-}" ] && mb=$(git merge-base HEAD "remotes/$primary/$default" 2>/dev/null); then
  git log --reverse --format=%s "$mb..HEAD" | head -1
else
  git log --format=%s -3
fi

# --- ASSIGNEE -------------------------------------------------------------
echo "== ASSIGNEE =="
case $platform in
  gh)
    gh api user --jq .login 2>/dev/null || echo "gh auth 未就绪" ;;
  glab)
    users=$(glab auth status 2>&1 | sed -n 's/.*[Ll]ogged in as \([^ ]*\).*/\1/p' | sort -u)
    [ -n "$users" ] && echo "$users" || echo "glab auth 未就绪" ;;
esac

# --- EXISTING_MR (API-first，404 甄别) -------------------------------------
echo "== EXISTING_MR =="
case $platform in
  gh)
    gh pr list --head "$branch" --json number,title,isDraft 2>&1 | head -20 ;;
  glab)
    if out=$(glab api --hostname "$host" "projects/$enc/merge_requests?source_branch=$branch&state=opened" 2>&1); then
      echo "$out" | python3 -c "import json,sys
for r in json.load(sys.stdin): print(f\"!{r['iid']} [{r['state']}] {r['title']}\")" 2>/dev/null \
        || { echo "raw (parse failed):"; echo "$out" | head -20; }
    else
      echo "PROJECT_RESOLVE_FAILED —— 404/失败是 URL 或项目路径形式问题，不是\"无 MR\""
      echo "复核: glab api --hostname $host projects/$enc"
      echo "$out" | head -3
    fi ;;
esac

# --- TARGET_CANDIDATES ------------------------------------------------------
echo "== TARGET_CANDIDATES =="
[ -n "${default:-}" ] && echo "$default (default)"
git ls-remote --heads "$primary" 2>/dev/null \
  | awk '{sub(/refs\/heads\//, "", $2); print $2}' | grep -v "^${branch}$" | head -10
