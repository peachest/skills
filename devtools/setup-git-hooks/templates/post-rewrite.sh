#!/bin/bash
# post-rewrite: auto-update hooks after rebase / amend

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
SCRIPT_DIR="$(dirname "$SCRIPT_PATH")"
source "$SCRIPT_DIR/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd_to_repo_root

log_info "rebase/amend 后更新..."
auto_update_hooks "$SCRIPT_DIR"

log_info "post-rewrite 完成。"