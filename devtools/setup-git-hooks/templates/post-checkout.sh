#!/bin/bash
# post-checkout: auto-update hooks + deps on branch switch

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
source "$SCRIPT_DIR/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd_to_repo_root

flag=$3  # 0=file checkout, 1=branch checkout
[ "$flag" = "0" ] && exit 0

log_info "切换分支: $1 -> $2"
auto_update_hooks "$SCRIPT_DIR"

log_info "post-checkout 完成。"