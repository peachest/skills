#!/usr/bin/env bash
# position.sh — per-repo position line for reckon baselines.
# Usage: position.sh [repo-path ...]   (no args = current repo, all its worktrees)
# Output: one TSV line per checked worktree:
#   worktree-path|branch|upstream|ahead|dirty|untracked|last-commit
# upstream: the tracking branch actually used for ahead counting, resolved by chain:
#   @{u} -> origin/<default-branch> -> internal/<default-branch> -> "(none)"
# All git invocations use /usr/bin/git (PATH git may be intercepted by a wrapper).
set -uo pipefail
GIT=/usr/bin/git
GLAB="${GLAB_BIN:-$HOME/.nix-profile/bin/glab}"

# Default-branch guess for a repo: remote HEAD if set, else first of main/master/dev.
default_branch_at() {  # in the context of worktree $1
    local wt="$1" d
    d=$($GIT -C "$wt" symbolic-ref --short "refs/remotes/origin/HEAD" 2>/dev/null | sed 's|^origin/||')
    [ -n "$d" ] && { echo "$d"; return; }
    for d in main master dev; do
        if $GIT -C "$wt" show-ref --verify --quiet "refs/remotes/origin/$d" 2>/dev/null; then echo "$d"; return; fi
    done
    echo main
}

pos_line() {
    local wt="$1" branch up ahead dirty untracked last
    branch=$($GIT -C "$wt" symbolic-ref --short HEAD 2>/dev/null) || branch="(detached $($GIT -C "$wt" rev-parse --short HEAD 2>/dev/null))"
    up=$($GIT -C "$wt" rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
    if [ -z "$up" ]; then
        local db; db=$(default_branch_at "$wt")
        for cand in "origin/$db" "internal/$db"; do
            if $GIT -C "$wt" show-ref --verify --quiet "refs/remotes/$cand" 2>/dev/null; then up="$cand"; break; fi
        done
    fi
    [ -n "$up" ] || up="(none)"
    if [ "$up" = "(none)" ]; then
        ahead="?"
    else
        ahead=$($GIT -C "$wt" rev-list --count "$up..HEAD" 2>/dev/null) || ahead="?"
    fi
    dirty=$($GIT -C "$wt" status --porcelain 2>/dev/null | grep -cv '^??')
    untracked=$($GIT -C "$wt" status --porcelain 2>/dev/null | grep -c '^??')
    last=$($GIT -C "$wt" log -1 --format='%h %s' 2>/dev/null | cut -c1-60)
    printf '%s|%s|%s|%s|%s|%s|%s\n' "$wt" "$branch" "$up" "$ahead" "$dirty" "$untracked" "$last"
}

if [ $# -eq 0 ]; then
    set -- "$PWD"
fi

for repo in "$@"; do
    # Accept either a worktree path or the bare/main repo path; enumerate worktrees once.
    common_dir=$($GIT -C "$repo" rev-parse --git-common-dir 2>/dev/null) || { echo "not a git repo: $repo" >&2; continue; }
    common_dir=$(cd "$repo" && cd "$common_dir" && pwd)   # absolute
    $GIT -C "$repo" worktree list --porcelain 2>/dev/null | awk '/^worktree /{print $2}'
done | sort -u | while read -r wt; do
    pos_line "$wt"
done
