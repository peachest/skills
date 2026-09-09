#!/usr/bin/env bash
# create-draft-mr.sh — push + open a draft MR/PR with a clean title and a
# file-based description. Sediments wiki P-004/P-005 (incl. the draft-drift
# consequence: the title scrub lives here, not in the agent's memory).
# Usage:
#   bash <SKILL_DIR>/scripts/create-draft-mr.sh \
#     --remote <name> --source <branch> --target <branch> \
#     --title "<title>" --desc-file <path> [--assignee <user>] [--no-push] \
#     [--dry-run] [repo-dir]
# Exit codes: 0 ok · 2 usage · 3 glab silent failure (tos/* quirk → 走 glab-api
# skill 的 API 路径，先查 existing MR 防重复)
set -euo pipefail

remote= source= target= title= desc= assignee= push=yes dry=no repo=
while [ $# -gt 0 ]; do
  case $1 in
    --remote) remote=$2; shift 2 ;;
    --source) source=$2; shift 2 ;;
    --target) target=$2; shift 2 ;;
    --title) title=$2; shift 2 ;;
    --desc-file) desc=$2; shift 2 ;;
    --assignee) assignee=$2; shift 2 ;;
    --no-push) push=no; shift ;;
    --dry-run) dry=yes; shift ;;
    -h|--help) grep '^#' "$0"; exit 0 ;;
    *) if [ -z "$repo" ]; then repo=$1; shift; else echo "unknown arg: $1" >&2; exit 2; fi ;;
  esac
done
cd "${repo:-.}"
: "${remote:?missing --remote}" "${source:?missing --source}" \
  "${target:?missing --target}" "${title:?missing --title}" "${desc:?missing --desc-file}"
[ -f "$desc" ] || { echo "desc-file not found: $desc" >&2; exit 2; }

# --- title scrub: draft 状态只能由 --draft 表达，前缀一律剥掉 --------------
shopt -s nocasematch
if [[ $title =~ ^(draft|wip)[[:space:]]*:?[[:space:]]*(.+)$ ]]; then
  echo "NOTE: stripped '$(echo "$title" | cut -d' ' -f1)' prefix from title — draft state is expressed by --draft only" >&2
  title=${BASH_REMATCH[2]}
fi

norm_url() {  # keep in sync with preflight.sh
  local u=$1 rest host path
  u=${u%.git}
  case "$u" in
    ssh://git@*) rest=${u#ssh://git@}; host=${rest%%/*}; host=${host%%:*}; path=${rest#*/}
                  echo "https://$host/$path" ;;
    git@*)        rest=${u#git@}; host=${rest%%:*}; path=${rest#*:}
                  echo "https://$host/$path" ;;
    http://*) echo "${u/http:/https:}" ;;
    *) echo "$u" ;;
  esac
}

web=$(norm_url "$(git remote get-url "$remote")")
case "$web" in *github.com*) platform=gh ;; *) platform=glab ;; esac

if [ "$dry" = yes ]; then
  echo "DRY: git push -u $remote $source  $([ $push = no ] && echo '(skipped: --no-push)')"
  case $platform in
    gh)   echo "DRY: gh pr create --head $source --base $target --title '$title' --body-file $desc --draft ${assignee:+--assignee $assignee}" ;;
    glab) echo "DRY: glab mr create -R $web --source-branch $source --target-branch $target --title '$title' --description \"\$(cat $desc)\" --draft --yes ${assignee:+--assignee $assignee}" ;;
  esac
  exit 0
fi

if [ "$push" = yes ]; then
  git push -u "$remote" "$source"
fi

# create with one retry on transient failure (5xx / empty output).
# Retry is safe-cheap: the description lives in a file, nothing is re-emitted.
attempt() {
  case $platform in
    gh) gh pr create --head "$source" --base "$target" --title "$title" \
           --body-file "$desc" --draft ${assignee:+--assignee "$assignee"} ;;
    glab) local args=(glab mr create -R "$web" --source-branch "$source"
           --target-branch "$target" --title "$title"
           --description "$(cat "$desc")" --draft --yes)
          [ -n "$assignee" ] && args+=(--assignee "$assignee")
          "${args[@]}" ;;
  esac
}

rc=0; out=$(attempt 2>&1) || rc=$?
if [ $rc -ne 0 ] && echo "$out" | grep -qiE '50[0-9]|service unavailable'; then
  echo "transient failure (rc=$rc), retrying once in 5s" >&2; sleep 5
  rc=0; out=$(attempt 2>&1) || rc=$?
fi
echo "$out"

if [ $rc -eq 0 ] && [ -z "$out" ]; then
  echo "GLAB_SILENT_FAIL —— glab 静默失败（tos/* 命名空间怪癖）。" \
       "改走 glab-api skill 的 API 路径；重试前先查 existing MR 防重复" >&2
  exit 3
fi
exit $rc
