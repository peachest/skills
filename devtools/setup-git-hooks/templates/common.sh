#!/bin/bash
# tools/git-hooks/common.sh — 日志工具（commit 校验已移至同目录 commit-msg）
# 仅提供函数，不设置 shell 选项——set -euo pipefail 由各入口脚本自行声明
# （库文件携带 set -e 会隐式改变 pre-commit/pre-push 的错误处理语义：
#   如 pre-push 对 wiki.py check 的 rc=$? 捕获在 -e 下直接终止钩子）。

# 颜色：两流均为 TTY 才着色（且 TERM≠dumb，r12 no77）；NO_COLOR 约定优先；
# FORCE_COLOR 显式开色（供 selftest 在非 TTY 管道环境注入验证着色路径，r7 no19；
# 0/false 视为未开，r9 no 6e4b/r12 no77 社区约定）
force_color_on=false
# FORCE_COLOR 取值约定（r19 no199）：空/0/false/no/off（任意大小写）=不强制；
# 其他任何值（含社区 1/2/3 级别、true、yes）=强制开色；含尾随空白的变体视为开
case "${FORCE_COLOR:-}" in ""|0|[Ff][Aa][Ll][Ss][Ee]|[Nn][Oo]|[Oo][Ff][Ff]) ;; *) force_color_on=true ;; esac
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
    # LC_ALL=C 锁定字节级 tr 语义（r19 no201：多字节 locale 下 GNU tr 按字符处理有实现差异）
    m=$(printf '%s' "$*" | LC_ALL=C tr -d '\000-\010\013\014\015\016-\037\177') || true
    # 非 UTF-8 locale（LANG=C 等）下终端把原始单字节 0x80-0x9F 解释为 C1 控制符（r19 no198）。
    # 收窄为确定危险的裸 C1 字节（r20 no218：整区间剥除会把合法多字节字符的续字节
    # 一并删掉，希腊/西里尔文等文件名乱码）；声明与终端实际编码错配残余风险见注释
    case "${LC_ALL:-${LC_CTYPE:-${LANG:-}}}" in
        *[Uu][Tt][Ff]*) ;;   # UTF-8 终端：仅靠下方 C1 两字节定点替换
        *) m=$(printf '%s' "$m" | LC_ALL=C tr -d '\205\215\220\230\233\234\235\236\237') || true ;;
    esac
    # UTF-8 编码的 C1（C2 80–9F）中可承载/扰动终端序列的定点剥除（r16 no143/r17 no157）：
    # CSI/OSC/DCS/SOS/PM/APC 起始符 + NEL/RI 行为扰动符；均固定两字节序列，UTF-8 自
    # 定点替换不误伤多字节字符。已知取舍（r18/r19 no178，r20 no219 措辞对齐）：
    # ① 保留内部 LF 支持多行消息——外部输入可注入含 [ERROR] 等任意前缀的伪造行
    #  （不止无前缀行），机器解析不应信任日志行；② 命令替换剥结尾全部 LF（尾部空行静默丢失）
    m=${m//$'\xc2\x85'/'?'}   # NEL
    m=${m//$'\xc2\x8c'/'?'}   # PLD
    m=${m//$'\xc2\x8d'/'?'}   # RI
    m=${m//$'\xc2\x8e'/'?'}   # SS2
    m=${m//$'\xc2\x8f'/'?'}   # SS3
    m=${m//$'\xc2\x90'/'?'}   # DCS
    m=${m//$'\xc2\x95'/'?'}   # CMD
    m=${m//$'\xc2\x96'/'?'}   # SPA
    m=${m//$'\xc2\x97'/'?'}   # EPA
    m=${m//$'\xc2\x98'/'?'}   # SOS
    m=${m//$'\xc2\x9a'/'?'}   # SCI
    m=${m//$'\xc2\x9b'/'?'}   # CSI
    m=${m//$'\xc2\x9c'/'?'}   # ST（OSC/DCS 字符串终止符）
    m=${m//$'\xc2\x9d'/'?'}   # OSC
    m=${m//$'\xc2\x9e'/'?'}   # PM
    m=${m//$'\xc2\x9f'/'?'}   # APC
    printf '%s' "$m"
}
# 公共实现（r23 no275 → r24 重构落位）：级别前缀/颜色变量/输出流三参数化，防三份模板口径分叉
_log() { # $1=级别标签 $2=颜色变量名 $3=输出fd，$4+=消息
    local IFS=' ' label="$1" color="$2" fd="$3"
    shift 3
    local m
    m=$(sanitize_log "$*") || true
    # 动态 fd：命令替换内嵌套会丢 || true 语义，故显式分支
    if [ "$fd" = "err" ]; then
        printf '%s\n' "[$label] ${!color}${m}${NC}" >&2 || true
    else
        printf '%s\n' "[$label] ${!color}${m}${NC}" || true
    fi
}
log_info()  { _log INFO GREEN out "$@"; }
log_warn()  { _log WARN YELLOW err "$@"; }
log_error() { _log ERROR RED err "$@"; }
