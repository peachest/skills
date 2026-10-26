#!/bin/bash
# common.sh — shared logging and utility functions
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 日志前缀放颜色码外，兼容 VSCode integrated terminal 的高亮检测
log_info()  { echo -e "[INFO] ${GREEN}$1${NC}"; }
log_warn()  { echo -e "[WARN] ${YELLOW}$1${NC}"; }
log_error() { echo -e "[ERROR] ${RED}$1${NC}"; }

# 注：commit 格式校验已迁入 commit-msg.sh 自身（配置块 + --ci 模式），
# 本文件不再持有 validate_commit_msg——规则的正典实现只有一份。

cd_to_repo_root() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || {
        log_error "无法确定 Git 仓库根目录。"
        exit 1
    }
    cd "$repo_root" || exit 1
}
