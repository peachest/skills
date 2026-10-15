#!/bin/bash
# pre-commit: staged-file checks (format, whitespace)
# Runs against git-show content (what will actually be committed),
# not working-tree files — works correctly with git add -p.

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd_to_repo_root
fail=0

# 1. Format check — replace with project's formatter (gofmt, prettier, etc.)
while IFS= read -r f; do
    [ -z "$f" ] && continue
    if ! diff -q <(git show ":$f" | tr -d '\n') <(git show ":$f" | gofmt | tr -d '\n') >/dev/null 2>&1; then
        log_error "gofmt 不通过: $f"
        fail=1
    fi
done < <(git diff --cached --name-only --diff-filter=ACM -- '*.go')

# 2. Whitespace check
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    against=$(git hash-object -t tree /dev/null)
fi
if ! git diff-index --check --cached "$against" --; then
    log_error "空白字符错误（行尾空白 / 缩进混用）。"
    fail=1
fi

if [ "$fail" -ne 0 ]; then
    log_error "请修复后重新 git add。"
    exit 1
fi

log_info "pre-commit 检查通过。"