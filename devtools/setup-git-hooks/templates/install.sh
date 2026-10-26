#!/usr/bin/env bash
# install.sh — 一次性安装：core.hooksPath 指向本目录。
# hook 内容随分支文件走（旧分支没有本目录时 hook 自动不生效，fail-open），
# 配置写 clone 级共享配置——配一次，主检出与全部 worktree 同时生效。
# 撤销：git config --unset core.hooksPath
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

HOOKS_DIR="tools/git-hooks"   # 放在其他目录（如 hack/git-hooks）的仓改这里

[ -d "$HOOKS_DIR" ] || { echo "error: hook 目录不存在: $HOOKS_DIR（请检查 HOOKS_DIR 设置）" >&2; exit 1; }

if old="$(git config --show-origin --get core.hooksPath 2>/dev/null)"; then
    origin="${old%%$'\t'*}"; old="${old#*$'\t'}"
    if [ "$old" != "$HOOKS_DIR" ]; then
        echo "注意: 覆盖已有 core.hooksPath（来自 ${origin#file:}）: $old -> $HOOKS_DIR" >&2
    fi
fi
# 迁移清理：旧 install-hooks.sh（symlink 方案）留下的 worktree 级 hooksPath
# 指向已悬空的 gitdir hooks——它优先于 clone 级配置，不清则钩子静默失效
if [ "$(git config extensions.worktreeConfig 2>/dev/null)" = "true" ] \
   && git config --worktree --get core.hooksPath >/dev/null 2>&1; then
    # 显式 if-then：set -e 下 'A && echo' 链中 A 失败被静默吞
    if git config --worktree --unset core.hooksPath; then
        echo "✓ 已清除旧 worktree 级 hooksPath 覆盖"
    else
        echo "警告: 旧 worktree 级 hooksPath 清理失败" >&2
    fi
fi

git config core.hooksPath "$HOOKS_DIR"
# 遍历目录（钩子目录即事实源，新增钩子自动纳入）；非钩子文件跳过。
# exec 位校验同循环：部分文件系统 chmod 静默失败，git 只执行带 exec 位钩子
for hook in "$HOOKS_DIR"/*; do
    # 排除清单与目录内容耦合：新增非钩子文件时记得同步此处
    case "${hook##*/}" in
        common.sh|selftest.sh|install.sh) continue ;;
    esac
    chmod +x "$hook" 2>/dev/null || true
    [ -x "$hook" ] || echo "警告: $hook 不可执行，该钩子不会生效" >&2
done

echo "✓ core.hooksPath = $HOOKS_DIR（本 clone 主检出与全部 worktree 生效）"
echo "  队友 clone 后跑一次 bash $HOOKS_DIR/install.sh；wt 用户由仓内 .config/wt.toml [pre-start] 自动装。"
echo "  注意: pre-start 仅在 worktree 首次创建时执行——已存在的 worktree 需手动跑一次本脚本。"
