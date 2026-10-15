#!/bin/bash
# hooks/common.sh — shared logging, validation, and utility functions
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Validate Conventional Commits format: type(scope)!: description
validate_commit_msg() {
    local msg_file="$1"
    local first_line
    first_line=$(head -n1 "$msg_file" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

    if [ -z "$first_line" ]; then
        log_error "提交信息不能为空。"
        return 1
    fi

    if ! echo "$first_line" | grep -qE '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-zA-Z0-9/_,-]+\))?!?: [^[:space:]].*'; then
        log_error "提交信息不符合 Conventional Commits 格式："
        log_error "  <type>(optional scope)(optional !): <description>"
        log_error "  例如: feat(auth): add login"
        log_error "  type 可选: build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"
        return 1
    fi
    return 0
}

cd_to_repo_root() {
    local repo_root
    repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || {
        log_error "无法确定 Git 仓库根目录。"
        exit 1
    }
    cd "$repo_root" || exit 1
}

auto_update_hooks() {
    local hooks_dir="$1"  # absolute path to hooks/ directory
    local prev_commit
    prev_commit=$(git reflog -1 --format="%H" HEAD@{1} 2>/dev/null) || return 0

    if ! git cat-file -t "$prev_commit" >/dev/null 2>&1; then
        return 0
    fi

    if git diff --name-only --diff-filter=ACMR "$prev_commit" HEAD 2>/dev/null | grep -q "^hooks/.*\.sh$"; then
        log_info "检测到 hooks 变更，正在重新安装..."
        if [ -x "$hooks_dir/install-hooks.sh" ]; then
            "$hooks_dir/install-hooks.sh" && log_info "hooks 已更新。"
        fi
    fi
}