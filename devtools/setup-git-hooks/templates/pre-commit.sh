#!/bin/bash
# pre-commit: staged-file checks (format, whitespace, git identity)
# Runs against git-show content (what will actually be committed),
# not working-tree files — works correctly with git add -p.
# 重检查（lint/test）在 pre-push，见 hooks/pre-push.sh。

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd_to_repo_root
fail=0

# 0. Git 身份校验（损坏的 user.name/email 会静默带错误作者进仓库，
#    事后只能 filter-branch 重写——实证：user.name 被写成字符串 "user.email"）
name=$(git config user.name || true)
email=$(git config user.email || true)
case "$name" in
    "" | "user.email" | "user.name" | "$(git config user.email 2>/dev/null || true)")
        log_error "git user.name 配置损坏: '$name'。修复: git config user.name '<名字>'"
        fail=1 ;;
esac
case "$email" in
    "" | *@* ) ;;  # 空或不含 @ 视为损坏
    *)
        log_error "git user.email 配置损坏: '$email'。修复: git config user.email '<邮箱>'"
        fail=1 ;;
esac

# 1. Format check — replace with project's formatter (gofmt, prettier, etc.)
#    只查不写：自动 -w 写回会破坏 git add -p 的部分暂存场景
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
