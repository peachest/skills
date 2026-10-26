#!/usr/bin/env bash
# commit-msg — commit 格式校验（本地钩子 + CI 兜底共用同一实现）
#
# 三种调用形态（同一脚本 = L1 本地钩子与 L2 CI 兜底口径天然一致）：
#   git commit-msg 钩子:  commit-msg <msg文件路径>
#   CI 范围校验:          commit-msg --ci <base-sha> <tip-sha>
#   人工调试:             commit-msg <msg文件路径>（同钩子）
#
# 配置块是本规则的单一事实源（setup-dev-and-contributing 会按 repo posture 回填）。
# 改规则先改这里——L1/L2 消费同一逻辑，无需两处同步。

# ── 配置块（单一事实源）────────────────────────────────────────────
COMMIT_FORMAT="conventional"   # conventional | none
COMMIT_PREFIX=""               # fork 仓填 "[TW]"（或 "[<ORG>]"），否则空串
                               # 内部原创 commit 必带此前缀；上游 cherry-pick 豁免
EXEMPT=(
    "^Merge "                  # git merge 自动生成
    "^Revert "                 # git revert 自动生成
    "^fixup!" "^squash!" "^amend!"  # git 交互式 rebase 自动生成
    "cherry picked from commit"     # 上游同步：git cherry-pick -x 尾注
)
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

validate_one() {
    local first_line="$1"

    if [ -z "$first_line" ]; then
        log_error "提交信息不能为空。"
        return 1
    fi

    # 豁免规则：git 自动生成的提交 + 上游 cherry-pick 同步
    local pattern
    for pattern in "${EXEMPT[@]}"; do
        if echo "$first_line" | grep -qE "$pattern"; then
            return 0
        fi
    done

    # 内部原创 commit 前缀（fork 仓的隔离标记，上游同步时 grep '^[ORG]' 可列出全部内部修改）
    # 有 prefix 时先剥离再校验 conventional——两者叠加而非冲突（[TW] feat(x): x 应通过）
    local check_line="$first_line"
    if [ -n "$COMMIT_PREFIX" ]; then
        if echo "$first_line" | grep -qF "$COMMIT_PREFIX"; then
            # ${var#*"X"} 双引号 pattern 里 * 不生效，改用长度截取
            local plen=${#COMMIT_PREFIX}
            check_line="${first_line:plen}"
            check_line="${check_line# }"   # 去掉 prefix 后的一个空格
        else
            log_error "内部原创 commit 必须带 $COMMIT_PREFIX 前缀："
            log_error "  $COMMIT_PREFIX <type>(scope): <description>"
            log_error "  豁免：merge/revert/fixup! 等自动生成提交、上游 cherry-pick（-x）"
            return 1
        fi
    fi

    if [ "$COMMIT_FORMAT" = "conventional" ]; then
        if ! echo "$check_line" | grep -qE '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-zA-Z0-9/_,-]+\))?!?: [^[:space:]].*'; then
            log_error "提交信息不符合 Conventional Commits 格式："
            log_error "  <type>(optional scope)(optional !): <description>"
            log_error "  例如: feat(auth): add login"
            log_error "  type 可选: build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"
            return 1
        fi
    fi
    return 0
}

validate_range() {
    local base="$1" tip="$2" bad=0
    # CI 兜底：只检查新 push 范围（base..tip），存量历史豁免（否则迁移仓首跑全红）
    local shas
    shas=$(git rev-list "$base..$tip" 2>/dev/null) || { log_warn "无法解析范围 $base..$tip，跳过"; return 0; }
    [ -z "$shas" ] && { log_info "无新 commit，跳过。"; return 0; }
    while read -r sha; do
        local subject
        subject=$(git log -1 --format=%s "$sha")
        if ! validate_one "$subject"; then
            log_error "  ↳ commit $(echo "$sha" | cut -c1-8): $subject"
            bad=1
        fi
    done <<< "$shas"
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
        validate_one "$first_line" || exit 1
        log_info "提交信息格式正确。"
        ;;
esac
