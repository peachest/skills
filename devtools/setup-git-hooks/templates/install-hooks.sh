#!/bin/bash
# hooks/install-hooks.sh — symlink hooks/*.sh to .git/hooks/
set -e

HOOKS_DIR="$(cd "$(dirname "$0")" && pwd)"

# Worktree-aware: use worktree-level hooksPath when multi-worktree
if [ "$(git config extensions.worktreeConfig 2>/dev/null)" = "true" ]; then
    GIT_HOOKS_DIR="$(git rev-parse --absolute-git-dir)/hooks"
    git config --worktree core.hooksPath "$GIT_HOOKS_DIR"
    echo "✓ worktree core.hooksPath = $GIT_HOOKS_DIR"
else
    GIT_HOOKS_DIR=$(git rev-parse --git-dir)/hooks
fi

mkdir -p "$GIT_HOOKS_DIR"

for src in "$HOOKS_DIR"/*.sh; do
    hook=$(basename "$src" .sh)
    [ "$hook" = "common" ] && continue
    [ "$hook" = "install-hooks" ] && continue
    dest="$GIT_HOOKS_DIR/$hook"
    ln -sf "$src" "$dest"
    chmod +x "$src"
    echo "✓ $hook -> $src"
done

echo "Git hooks 安装完成。"