#!/bin/bash
# commit-msg: validate Conventional Commits format + duplicate Signed-off-by

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

[ -f "$1" ] || { log_error "未提供提交信息文件"; exit 1; }

validate_commit_msg "$1" || exit 1

if [ -n "$(grep '^Signed-off-by: ' "$1" | sort | uniq -d)" ]; then
    log_error "存在重复的 Signed-off-by 行。"
    exit 1
fi

log_info "提交信息格式正确。"