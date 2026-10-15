#!/bin/bash
# pre-push: run full CI checks before pushing.
# Two modes:
#   simple — runs make lint && make test in the current repo
#   isolated — checks out pushed SHA in a temp worktree (simulates CI)
# Use isolated for critical repos; simple is fine for most projects.

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd_to_repo_root

zero=0000000000000000000000000000000000000000
checked=""
tmp=""
trap '[ -n "$tmp" ] && { git worktree remove --force "$tmp" >/dev/null 2>&1; rm -rf "$tmp"; }' EXIT

while read -r _local_ref local_sha _remote_ref _remote_sha; do
    [ -z "$local_sha" ] || [ "$local_sha" = "$zero" ] && continue
    case " $checked " in *" $local_sha "*) continue ;; esac
    checked="$checked $local_sha"

    log_info "检查 ${local_sha:0:8}..."
    # Simple mode: just run make in the current repo
    if ! make lint test; then
        log_error "make lint / test 失败。"
        exit 1
    fi
done

log_info "pre-push 检查通过。"