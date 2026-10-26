#!/bin/bash
# tools/git-hooks/common.sh — 日志工具（commit 校验已移至同目录 commit-msg）
# 仅提供函数，不设置 shell 选项——set -euo pipefail 由各入口脚本自行声明
# （库文件携带 set -e 会隐式改变 pre-commit/pre-push 的错误处理语义：
#   如 pre-push 对 wiki.py check 的 rc=$? 捕获在 -e 下直接终止钩子）。

# 颜色：两流均为 TTY 才着色（且 TERM≠dumb，r12 no77）；NO_COLOR 约定优先；
# FORCE_COLOR 显式开色（供 selftest 在非 TTY 管道环境注入验证着色路径，r7 no19；
# 0/false 视为未开，r9 no 6e4b/r12 no77 社区约定）
force_color_on=false
case "${FORCE_COLOR:-}" in ""|0|false) ;; *) force_color_on=true ;; esac
if [[ -z "${NO_COLOR:-}" ]] && { { [[ -t 1 && -t 2 ]] && [[ "${TERM:-}" != dumb ]]; } || $force_color_on; }; then
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

# local IFS=' '：$* 以空格连接，防调用方误改 IFS 把消息按行拼碎；单参调用不受影响（r8 no126a）。
# printf 而非 echo -e：消息含外部输入，echo -e 会解释反斜杠序列。仅剥 ESC 防终端注入
# （ANSI CSI/OSC；保留 \t/\n 支持多行消息——与 commit-msg 回显的宽 tr 范围刻意不同，
# r14 no110 注释即信任边界声明）。ESC 常量加载期算一次（r14 no110）。
# || true 吞写失败：日志故障不改变钩子判定（set -e 下写失败中止整个钩子，r13 no100）
ESC=$'\033'
log_info()  { local IFS=' '; printf '%s\n' "[INFO] ${GREEN}${*//$ESC/}${NC}" || true; }
log_warn()  { local IFS=' '; printf '%s\n' "[WARN] ${YELLOW}${*//$ESC/}${NC}" >&2 || true; }
log_error() { local IFS=' '; printf '%s\n' "[ERROR] ${RED}${*//$ESC/}${NC}" >&2 || true; }