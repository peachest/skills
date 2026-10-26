#!/bin/bash
# pre-push: 两段检查
#   1. base-branch drift：当前分支落后基分支（默认 remote HEAD / branch.<name>.merge）
#      时阻断 push，提示先 pull+rebase——避免在 MR 阶段才发现冲突（实证：基于旧 dev
#      的分支会撞上已修复问题的旧版本）。绕过单次 push：HOOKS_ALLOW_BASE_DRIFT=1
#   2. CI 模拟：对将要推送的 commit 跑 make lint + make test。
#      simple 模式直接在当前仓跑；isolated 模式在临时 worktree 检出推送 SHA
#      （模拟干净 CI，适合有 go.mod replace ../xxx 相对依赖的仓）。

SCRIPT_PATH="$(readlink -f "$0" 2>/dev/null || echo "$0")"
source "$(dirname "$SCRIPT_PATH")/common.sh" || { echo "无法加载 common.sh"; exit 1; }

# ── 配置块 ─────────────────────────────────────────────────────────
CHECK_BASE_DRIFT=1        # 0 关闭落后检查
SIM_MODE="simple"         # simple | isolated（isolated 需按仓改 clone_replace_deps 逻辑）
SIM_MAKE_TARGETS="lint test"
# ─────────────────────────────────────────────────────────────────

cd_to_repo_root

zero=0000000000000000000000000000000000000000
checked=""

# --- 1. base-branch drift 检查 ---
if [ "$CHECK_BASE_DRIFT" = "1" ] && [ "${HOOKS_ALLOW_BASE_DRIFT:-0}" != "1" ]; then
    branch=$(git branch --show-current)
    # 基分支探测：branch.<name>.merge（wt/VSCode 等会写）优先，回退 remote HEAD
    base_branch=$(git config --get "branch.${branch}.merge" 2>/dev/null | sed 's|^refs/heads/||')
    [ -z "$base_branch" ] && base_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')
    if [ -n "$base_branch" ] && [ "$base_branch" != "$branch" ]; then
        git fetch --quiet origin "$base_branch" 2>/dev/null || log_warn "fetch origin $base_branch 失败，跳过 drift 检查"
        behind=$(git rev-list --count "HEAD..origin/${base_branch}" 2>/dev/null || echo 0)
        if [ "${behind:-0}" -gt 0 ]; then
            log_error "当前分支基于的 ${base_branch} 已前进 ${behind} 个提交——先 rebase 再 push："
            log_error "  git fetch origin && git rebase origin/${base_branch}"
            log_error "（单次绕过: HOOKS_ALLOW_BASE_DRIFT=1 git push ...）"
            exit 1
        fi
    fi
fi

# --- 2. CI 模拟 ---
tmp=""
trap '[ -n "$tmp" ] && { git worktree remove --force "$tmp" >/dev/null 2>&1; rm -rf "$tmp"; }' EXIT

while read -r _local_ref local_sha _remote_ref _remote_sha; do
    [ -z "$local_sha" ] || [ "$local_sha" = "$zero" ] && continue
    case " $checked " in *" $local_sha "*) continue ;; esac
    checked="$checked $local_sha"

    log_info "检查 ${local_sha:0:8}..."
    if [ "$SIM_MODE" = "isolated" ]; then
        # isolated：临时 worktree 检出推送 SHA（干净树模拟 CI）。
        # 有 go.mod replace => ../xxx 相对依赖的仓需自行克隆依赖到 worktree 同级
        # （参考 <device-plugin-repo> hooks/pre-push.sh 的 clone_replace_deps）。
        tmp=$(mktemp -d)
        git worktree add --detach "$tmp/worktree" "$local_sha" >/dev/null || exit 1
        if ! make -C "$tmp/worktree" $SIM_MAKE_TARGETS; then
            log_error "make $SIM_MAKE_TARGETS 失败（针对 ${local_sha:0:8}）。"
            exit 1
        fi
    else
        if ! make $SIM_MAKE_TARGETS; then
            log_error "make $SIM_MAKE_TARGETS 失败。"
            exit 1
        fi
    fi
done

log_info "pre-push 检查通过。"
