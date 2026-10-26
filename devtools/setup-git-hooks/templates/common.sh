#!/bin/bash
# tools/git-hooks/common.sh — 日志工具（commit 校验已移至同目录 commit-msg）
# 仅提供函数，不设置 shell 选项——set -euo pipefail 由各入口脚本自行声明
# （库文件携带 set -e 会隐式改变 pre-commit/pre-push 的错误处理语义：
#   如 pre-push 对 wiki.py check 的 rc=$? 捕获在 -e 下直接终止钩子）。

# 颜色：两流均为 TTY 才着色（交叉重定向如 2>err.log 时任一"或"判断都会
# 让转义符漏进非 TTY 流）；遵循 NO_COLOR 约定
if [[ -t 1 && -t 2 ]] && [[ -z "${NO_COLOR:-}" ]]; then
    RED=$'\033[0;31m'
    GREEN=$'\033[0;32m'
    YELLOW=$'\033[1;33m'
    NC=$'\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    NC=''
fi

# printf 而非 echo -e：消息含外部输入（commit subject、clone 报错），
# echo -e 会解释其中的反斜杠序列
log_info()  { printf '%s\n' "[INFO] ${GREEN}$*${NC}"; }
log_warn()  { printf '%s\n' "[WARN] ${YELLOW}$*${NC}" >&2; }
log_error() { printf '%s\n' "[ERROR] ${RED}$*${NC}" >&2; }
