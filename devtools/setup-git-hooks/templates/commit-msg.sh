#!/bin/bash
# commit-msg — commit 格式校验（本地钩子 + CI 兜底共用同一实现）
#
# 三种调用形态（同一脚本 = L1 本地钩子与 L2 CI 兜底口径天然一致）：
#   git commit-msg 钩子:  commit-msg <msg文件路径>
#   CI 范围校验:          commit-msg --ci <base-sha> <tip-sha>
#   人工调试:             commit-msg <msg文件路径>（同钩子）
#
# 配置块是本规则的单一事实源。改规则先改这里——L1/L2 消费同一逻辑。

# ── 配置块（单一事实源）────────────────────────────────────────────
COMMIT_FORMAT="conventional"   # conventional | none
COMMIT_PREFIX=""               # 本仓非 fork，纯 conventional；fork 时填 "[TW]" 等
EXEMPT=(
    # 收紧为 git 自动生成形态（r12 no79）：手写 "Merge xxx"/"Revert xxx" 不再豁免。
    # git merge 模板固定为 branch/remote-tracking branch/pull request/commit/tag 开头；
    # git revert 固定为 Revert "<原 subject>"
    "^Merge (branch |remote-tracking branch |pull request |commit |tag |branch')"   # 只对 subject 判定：
    "^Revert \""                                                                     #   正文任意行匹配会动持豁免（正文绕过实证）
    "^fixup!" "^squash!" "^amend!"  # git 交互式 rebase 自动生成
)
BODY_EXEMPT=(
    # 正文级豁免（fork 场景）：cherry-pick -x 尾注在正文，subject 无特征。
    # 本仓非 fork 留空；fork 仓填 "^\(cherry picked from commit "
)
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd -P)"/$(basename "$0")   # cd+pwd -P 可移植（readlink -f 旧 macOS 缺失，r12 no81）；不解析 $0 符号链接——install.sh 以 hooksPath 直指仓内目录
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh" >&2; exit 1; }

# 配置块自检：拼错会静默 fail-open（跳过全部格式校验），与"单一事实源"定位不符（r9 no e3d5）
case "$COMMIT_FORMAT" in conventional|none) ;; *) echo "错误: COMMIT_FORMAT 配置非法: $COMMIT_FORMAT" >&2; exit 1 ;; esac

validate_one() {
    local first_line="$1" full_msg="${2:-$1}"

    if [ -z "$first_line" ]; then
        log_error "提交信息不能为空。"
        return 1
    fi

    # 重复 Signed-off-by 查重先于豁免：豁免免的是格式约束，不免全仓查重规则
    # （"Merge branch x" 标题藏重复 signoff 不应放过）。
    # 宽松匹配：-i 大小写不敏感 + 折叠多空格 + 统一小写——
    # "Signed-off-by:  X"/"signed-off-by: x" 变体与正典行判重（git 自身对 trailer 宽容）
    # POSIX 可移植：\+ 是 GNU BRE 扩展（BSD 按字面 +，r12 no82）；不整行小写——仅大小写
    # 不同的两个不同签署人会被误判重复（r12 no82）；判重本身对大小写敏感是刻意取舍
    if [ -n "$(printf '%s\n' "$full_msg" | grep -iE '^signed-off-by:' | tr -d '\r' | sed 's/^signed-off-by:[[:space:]]*/signed-off-by: /;s/[[:space:]][[:space:]]*/ /g;s/[[:space:]]*$//' | sort | uniq -d)" ]; then
        log_error "存在重复的 Signed-off-by 行。"
        return 1
    fi

    # 豁免规则：git 自动生成的提交特征在 subject；cherry-pick 尾注在正文。
    # subject 级豁免只判 first_line（全文匹配会被正文任意 "Merge ..." 行劫持），
    # 正文级豁免（BODY_EXEMPT）独立列表，仅 fork 场景非空
    local pattern
    for pattern in ${EXEMPT[@]+"${EXEMPT[@]}"}; do
        if printf '%s\n' "$first_line" | grep -qE "$pattern"; then
            return 0
        fi
    done
    for pattern in ${BODY_EXEMPT[@]+"${BODY_EXEMPT[@]}"}; do
        if printf '%s\n' "$full_msg" | grep -qE "$pattern"; then
            return 0
        fi
    done

    # 内部原创 commit 前缀（fork 仓的隔离标记，上游同步时 grep '^\[ORG\]' 可列出全部内部修改）。
    # 行首锚定：case 的 pattern 中变量按字面匹配（[TW] 不作 glob 展开），
    # 剥离用同源字面展开 ${var#\$PREFIX}——不用 grep -qF（全文子串，"xxx feat: add [TW]" 会误命中）
    local check_line="$first_line"
    if [ -n "$COMMIT_PREFIX" ]; then
        case "$first_line" in
            "$COMMIT_PREFIX"*)
                check_line="${first_line#"$COMMIT_PREFIX"}"
                check_line="${check_line#"${check_line%%[! ]*}"}"   # 归一化：去 prefix 后全部前导空格
                ;;
            *)
                log_error "内部原创 commit 必须带 $COMMIT_PREFIX 前缀："
                log_error "  $COMMIT_PREFIX <type>(scope): <description>"
                log_error "  豁免：merge/revert/fixup! 等自动生成提交${BODY_EXEMPT[@]:+、上游 cherry-pick（-x）}"
                return 1
                ;;
        esac
    fi

    if [ "$COMMIT_FORMAT" = "conventional" ]; then
        if ! printf '%s\n' "$check_line" | grep -qE '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-zA-Z0-9/_,-]+\))?!?: [^[:space:]].*'; then
            log_error "提交信息不符合 Conventional Commits 格式："
            log_error "  <type>(optional scope)(optional !): <description>"
            log_error "  例如: feat(hgml): add MIG placement API"
            log_error "  type 可选: build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"
            return 1
        fi
    fi
    return 0
}

validate_range() {
    local base="$1" tip="$2" bad=0 empty_range=0
    # 两段式取数：rev-list 拿 sha（无歧义），逐 commit 取 %B——
    # 0x1e 单遍记录协议已被两轮绕过（no59e3 伪 40-hex 头、no67 伪造终结+重同步），
    # 消息体可含任意字节时任何行内分隔符都不可信，故彻底放弃行解析（r11 no67）
    local shas
    shas=$(git rev-list "$base..$tip") \
        || { log_error "无法解析范围 $base..$tip——浅克隆需 fetch-depth: 0，具体原因见上方 git 报错"; return 1; }
    # 空范围：tip 已含于 base（tip 为 base 祖先或相等，如 rebase 后旧 diff-base）是合法场景（WARN 不 fail），但需可见
    [ -z "$shas" ] && { log_warn "范围 $base..$tip 为空（0 个提交被校验，本次兑底未生效）——确认 base 是否正确（正常 MR 非空）"; empty_range=1; return 0; }

    local sha body first_line
    # 规模护栏：范围错配到很远的历史时逐提交校验线性变慢，WARN 提示（r12 no84）
    [ "$(printf '%s\n' "$shas" | wc -l)" -gt 200 ] && log_warn "范围 $base..$tip 提交数超过 200——确认 base 是否错配（校验耗时会线性增长）"
    while IFS= read -r sha; do
        body=$(git log -1 --format=%B "$sha") \
            || { log_error "commit ${sha:0:8}: 无法读取提交信息"; bad=1; continue; }
        # 消息含 0x1e 一律拒绝（L1 钩子同口径；攻击者可借此伪造分隔符）
        if [[ "$body" == *$'\x1e'* ]]; then
            log_error "commit ${sha:0:8} 提交信息包含非法控制字符 0x1e"
            bad=1
            continue
        fi
        # 只去尾随空白：不裁前导空白——" Merge branch x"/" feat: x" 前置空格
        # 属格式违规，与 CI 拒绝口径一致（r7 no11）。[[:space:]] 含 \r（r10 no c4be）
        # sed -n 替代 head -n1：大消息时 head 提前退出触发 SIGPIPE→141（set -o pipefail，r12 no83）
        first_line=$(printf '%s\n' "$body" | sed -n '1{s/[[:space:]]*$//p;}')
        if ! validate_one "$first_line" "$body"; then
            log_error "  ↳ commit ${sha:0:8}: $(printf '%s' "$first_line" | tr -d '\000-\013\016-\037')"
            bad=1
        fi
    done <<< "$shas"
    return "$bad"
}

case "${1:-}" in
    --ci)
        [ $# -eq 3 ] || { log_error "用法: commit-msg --ci <base-sha> <tip-sha>"; exit 1; }
        validate_range "$2" "$3" || exit 1
        [ "${empty_range:-0}" = 1 ] || log_info "CI commit 检查通过。"   # 空范围不报"通过"（r12 no78：WARN 与通过矛盾）
        ;;
    *)
        [ -f "${1:-}" ] || { log_error "未提供提交信息文件"; exit 1; }
        # L1 与 L2 同源：本地钩子也拒 0x1e（消息文件即将入库，可预检）
        if grep -q $'\x1e' "$1"; then
            log_error "提交信息包含非法控制字符 0x1e（与 CI 校验协议冲突）"
            exit 1
        fi
        # 不裁前导空白（r7 no11，同 --ci 口径）。钩子拿到的是 git cleanup（剥离注释行/
        # 首尾空行）之前的文件——先模拟 cleanup=strip 再取首行，否则模板块首行空行/注释误拦（r9 no 360f）。
        # commentchar 跟随 core.commentchar 配置（r12 no80；auto 模式取 #）
        comment_char=$(git config core.commentchar || echo '#')
        [ "$comment_char" = "auto" ] && comment_char='#'
        msg_clean=$(sed "/^$comment_char/d" "$1" | sed '/./,$!d')
        first_line=$(printf '%s\n' "$msg_clean" | sed -n '1{s/[[:space:]]*$//p;}')   # 同上，避 SIGPIPE（r12 no83）
        validate_one "$first_line" "$msg_clean" || exit 1
        log_info "提交信息格式正确。"
        ;;
esac
