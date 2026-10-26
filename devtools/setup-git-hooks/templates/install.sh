#!/bin/bash
# install.sh — 一次性安装：core.hooksPath 指向本目录。
# hook 内容随分支文件走（fork/旧分支没有本目录时 hook 自动不生效，fail-open），
# 配置写 clone 级共享配置——配一次，本 clone 主检出与全部 worktree 同时生效。
# 撤销：git config --unset core.hooksPath
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
cd "$root"

HOOKS_DIR="tools/git-hooks"   # 放在其他目录（如 hack/git-hooks）的仓改这里

git config core.hooksPath "$HOOKS_DIR"
chmod +x "$HOOKS_DIR"/* 2>/dev/null || true

echo "✓ core.hooksPath = $HOOKS_DIR（本 clone 主检出与全部 worktree 生效）"
echo "  队友 clone 后跑一次 bash $HOOKS_DIR/install.sh 即可。"
echo "  建议 wt 用户在主检出 .config/wt.toml 配 [pre-start] hooks = \"bash $HOOKS_DIR/install.sh\" 实现检出即装。"
