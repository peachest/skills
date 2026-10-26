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
    "^Merge "                  # git merge 自动生成——只对 subject 判定：
    "^Revert "                 #   正文任意行以这些词开头会劫持豁免（正文绕过实证）
    "^fixup!" "^squash!" "^amend!"  # git 交互式 rebase 自动生成
)
BODY_EXEMPT=(
    # 正文级豁免（fork 场景）：cherry-pick -x 尾注在正文，subject 无特征。
    # 本仓非 fork 留空；fork 仓填 "^\(cherry picked from commit "
)
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

validate_one() {
    local first_line="$1" full_msg="${2:-$1}"

    if [ -z "$first_line" ]; then
        log_error "提交信息不能为空。"
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

    # 重复 Signed-off-by 查重（本仓既有规则，L1/L2 都查）
    if [ -n "$(printf '%s\n' "$full_msg" | grep '^Signed-off-by: ' | sort | uniq -d)" ]; then
        log_error "存在重复的 Signed-off-by 行。"
        return 1
    fi

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
        if ! echo "$check_line" | grep -qE '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-zA-Z0-9/_,-]+\))?!?: [^[:space:]].*'; then
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
    local base="$1" tip="$2" bad=0
    # fail-closed：L2 兜底解析不出范围必须显式报错（浅克隆 CI 需 fetch-depth: 0），
    # 静默跳过会让绕过本地钩子的提交从服务端逃逸
    local log_out
    log_out=$(git log --format='%H%x09%B%x09%x1e' "$base..$tip") \
        || { log_error "无法解析范围 $base..$tip——浅克隆需 fetch-depth: 0，具体原因见上方 git 报错"; return 1; }
    # 空范围：rebase 后 diff-base 已含于 tip 是合法场景（WARN 不 fail），但需可见
    [ -z "$log_out" ] && { log_warn "范围 $base..$tip 为空——确认 base 是否正确（正常 MR 非空）"; return 0; }

    # 单次 git log 批量取全文（%B），逐 commit 文本拆分校验（避免逐 commit 起子进程取数）
    local sha="" body="" first_line line
    while IFS= read -r line; do
        if [ -z "$sha" ]; then
            sha="${line%%$'\t'*}"
            body="${line#*$'\t'}"
        else
            body+=$'\n'"$line"
        fi
        if [[ "$line" == *$'\x1e' ]]; then
            body="${body%$'\x1e'}"
            first_line="${body%%$'\n'*}"
            first_line=$(printf '%s' "$first_line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            if ! validate_one "$first_line" "$body"; then
                log_error "  ↳ commit ${sha:0:8}: $(printf '%s' "$first_line" | tr -d '\000-\010\013\014\016-\037')"
                bad=1
            fi
            sha=""
            body=""
        fi
    done <<< "$log_out"
    # 残记录兜底：消息内嵌 0x1e 会提前终结记录，剩余行沦为永不校验的残记录
    # （如把重复 Signed-off-by 藏在残记录里绕过查重）——fail-closed
    if [ -n "$sha" ]; then
        log_error "提交信息包含非法控制字符 0x1e（record 未终结，剩余内容未校验）"
        bad=1
    fi
    return "$bad"
}

case "${1:-}" in
    --ci)
        [ $# -eq 3 ] || { log_error "用法: commit-msg --ci <base-sha> <tip-sha>"; exit 1; }
        validate_range "$2" "$3" || exit 1
        log_info "CI commit 检查通过。"
        ;;
    *)
        [ -f "${1:-}" ] || { log_error "未提供提交信息文件"; exit 1; }
        first_line=$(head -n1 "$1" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        validate_one "$first_line" "$(cat "$1")" || exit 1
        log_info "提交信息格式正确。"
        ;;
esac
