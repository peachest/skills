#!/bin/bash
# tools/git-hooks/common.sh — 日志工具（commit 校验已移至同目录 commit-msg）
# 仅提供函数，不设置 shell 选项——set -euo pipefail 由各入口脚本自行声明
# （库文件携带 set -e 会隐式改变 pre-commit/pre-push 的错误处理语义：
#   如 pre-push 对 wiki.py check 的 rc=$? 捕获在 -e 下直接终止钩子）。

# 颜色：两流均为 TTY 才着色（且 TERM≠dumb，r12 no77）；NO_COLOR 约定优先；
# FORCE_COLOR 显式开色（供 selftest 在非 TTY 管道环境注入验证着色路径，r7 no19；
# 0/false 视为未开，r9 no 6e4b/r12 no77 社区约定）
force_color_on=false
case "${FORCE_COLOR:-}" in ""|0|[Ff]alse|[Nn]o|[Oo][Ff][Ff]) ;; *) force_color_on=true ;; esac   # 关断值大小写不敏感（r17 no160；不用 ${,,}——macOS bash 3.2）
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
# printf 而非 echo -e：消息含外部输入，echo -e 会解释反斜杠序列。剥除 \t/\n 外的全部
# C0（含 \r 行首改写，r15 no125）与 DEL（r16 no143）；UTF-8 编码的 C1（C2 80–9F，
# xterm/VTE 视 U+009B/U+009D 为 CSI/OSC 起始符）定点剥 CSI/OSC 两个起始符——
# 不能按字节区间 0x80-0x9F 删（会破坏中文等合法 UTF-8 续字节）。本层是 pre-commit
# 文件名回显等外部输入的唯一防线。|| true 吞写失败：日志故障不改变钩子判定（r13 no100）
sanitize_log() {
    local IFS=' '   # 与包装层一致："$*" 拼接受调用方 IFS 动态作用域影响（r17 no159）
    local m
    m=$(printf '%s' "$*" | tr -d '\000-\010\013\014\015\016-\037\177') || true
    # UTF-8 编码的 C1（C2 80–9F）中可承载/扰动终端序列的定点剥除（r16 no143/r17 no157）：
    # CSI/OSC/DCS/SOS/PM/APC 起始符 + NEL/RI 行为扰动符；均固定两字节序列，UTF-8 自
    # 同步保证定点删除不误伤多字节字符
    m=${m//$'\xc2\x85'/}   # NEL
    m=${m//$'\xc2\x8d'/}   # RI
    m=${m//$'\xc2\x90'/}   # DCS
    m=${m//$'\xc2\x98'/}   # SOS
    m=${m//$'\xc2\x9b'/}   # CSI
    m=${m//$'\xc2\x9d'/}   # OSC
    m=${m//$'\xc2\x9e'/}   # PM
    m=${m//$'\xc2\x9f'/}   # APC
    printf '%s' "$m"
}
log_info()  { local IFS=' '; local m; m=$(sanitize_log "$*") || true; printf '%s\n' "[INFO] ${GREEN}${m}${NC}" || true; }
log_warn()  { local IFS=' '; local m; m=$(sanitize_log "$*") || true; printf '%s\n' "[WARN] ${YELLOW}${m}${NC}" >&2 || true; }
log_error() { local IFS=' '; local m; m=$(sanitize_log "$*") || true; printf '%s\n' "[ERROR] ${RED}${m}${NC}" >&2 || true; }
