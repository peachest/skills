#!/bin/bash
# pre-commit: 秒级检查，只看 staged 内容（git show :file，而非工作区文件，
# 保证 git add -p 部分暂存时检查的就是将要提交的内容）。
# 重检查（lint/test）在 pre-push；commit 信息格式校验在 commit-msg——本文件不重复。
# 凭证扫描若需要，装 gitleaks 类工具后在此追加（本仓用 skills 仓的 gitleaks pre-commit，见 AGENTS.md）。

set -euo pipefail   # 入口自行声明（common.sh 不带副作用）；本钩子全部检查为 if/exit 结构，-e 可安全兜住未来新增检查的未防护失败
SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

cd "$(git rev-parse --show-toplevel)" || exit 1

fail=0

# 1. staged Go 文件 → gofmt 检查
while IFS= read -r f; do
    [ -z "$f" ] && continue
    if ! diff -q <(git show ":$f" | tr -d '\n') <(git show ":$f" | gofmt | tr -d '\n') >/dev/null 2>&1; then
        log_error "gofmt 不通过: $f"
        fail=1
    fi
done < <(git diff --cached --name-only --diff-filter=ACM -- '*.go')

# 2. staged C 文件 → clang-format 检查
while IFS= read -r f; do
    [ -z "$f" ] && continue
    if ! git show ":$f" | clang-format --dry-run --Werror --assume-filename="$f" - >/dev/null 2>&1; then
        log_error "clang-format 不通过: $f"
        fail=1
    fi
done < <(git diff --cached --name-only --diff-filter=ACM -- '*.c' '*.h')

if [ "$fail" -ne 0 ]; then
    log_error "请运行 make fmt 后重新 git add。"
    exit 1
fi

# 3. 空白符检查（行尾空白、tab/space 混用等，遵循 core.whitespace 配置）
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    against=HEAD
else
    against=$(git hash-object -t tree /dev/null)
fi
if ! git diff-index --check --cached "$against" --; then
    log_error "存在空白字符错误（行尾空白 / 缩进混用）。"
    exit 1
fi

log_info "pre-commit 检查通过。"
