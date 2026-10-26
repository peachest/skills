#!/usr/bin/env bash
# install.sh — 一次性安装：core.hooksPath 指向本目录。
# hook 内容随分支文件走（旧分支没有本目录时 hook 自动不生效，fail-open），
# 配置写 clone 级共享配置——配一次，主检出与全部 worktree 同时生效。
# 撤销：git config --unset core.hooksPath
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

HOOKS_DIR="tools/git-hooks"   # 必须相对路径：core.hooksPath 相对值按各 worktree 根解析，
                               # 这是"hook 内容随分支走、旧分支 fail-open"的前提；改绝对路径会全 worktree 共享一份

# 目录缺失在旧分支是 fail-open 设计内场景（exit 0 + 提示）；
# 真实错误（hooksPath 写失败）才 exit 1
[ -d "$HOOKS_DIR" ] || { echo "提示: $HOOKS_DIR 不存在（旧分支无钩子目录属预期），跳过安装" >&2; exit 0; }

if old="$(git config --show-origin --get core.hooksPath 2>/dev/null)"; then
    origin="${old%%$'\t'*}"; old="${old#*$'\t'}"
    if [ "$old" != "$HOOKS_DIR" ]; then
        echo "注意: 覆盖已有 core.hooksPath（来自 ${origin#file:}）: $old -> $HOOKS_DIR" >&2
    fi
fi
# 迁移清理：旧 install-hooks.sh 是单 worktree 作用域——每个跑过旧脚本的
# worktree 都写了各自的 worktree 级 hooksPath（指向已悬空的 gitdir hooks），
# 优先级高于 clone 级配置。遍历全部 worktree 统一清理
if [ "$(git config --bool extensions.worktreeConfig 2>/dev/null)" = "true" ]; then
    wt_dir=""
    clean_fail=0
    while IFS= read -r line; do
        case "$line" in
            worktree\ *) wt_dir="${line#worktree }" ;;
            bare)        wt_dir="" ;;
            detached|\ *)
                if [ -n "$wt_dir" ] && git -C "$wt_dir" config --worktree --get core.hooksPath >/dev/null 2>&1; then
                    if git -C "$wt_dir" config --worktree --unset core.hooksPath; then
                        echo "✓ 已清除 $wt_dir 的旧 worktree 级 hooksPath"
                    else
                        echo "警告: $wt_dir 清理失败" >&2
                        clean_fail=1
                    fi
                fi
                wt_dir=""
                ;;
        esac
    done < <(git worktree list --porcelain)
fi

git config core.hooksPath "$HOOKS_DIR"
# 遍历目录（钩子目录即事实源，新增钩子自动纳入）；非钩子文件跳过。
# git 只按精确文件名识别钩子（均无扩展名），*.sh 必为辅助脚本——排除即不变式，
# 新增辅助脚本无需维护清单
for hook in "$HOOKS_DIR"/*; do
    [ -f "$hook" ] || continue   # 跳过子目录（glob 字面量已被上方 -d 拦，防御空目录场景）
    case "${hook##*/}" in
        *.sh) continue ;;
    esac
    chmod +x "$hook" 2>/dev/null || true
    [ -x "$hook" ] || echo "警告: $hook 不可执行，该钩子不会生效" >&2
done

if [ "${clean_fail:-0}" = 1 ]; then
    echo "警告: 部分 worktree 级 hooksPath 清理失败——这些 worktree 的钩子不会指向 $HOOKS_DIR（worktree 级优先），请手动：git -C <worktree> config --worktree --unset core.hooksPath" >&2
else
    echo "✓ core.hooksPath = $HOOKS_DIR（本 clone 主检出与全部 worktree 生效）"
fi
echo "  队友 clone 后跑一次 bash $HOOKS_DIR/install.sh；wt 用户由仓内 .config/wt.toml [pre-start] 自动装。"
echo "  注意: pre-start 仅在 worktree 首次创建时执行——已存在的 worktree 需手动跑一次本脚本。"
