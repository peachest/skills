#!/usr/bin/env bash
# render.sh — manim 动画渲染封装
#
# 用法: bash render.sh <scene.py> <SceneClass> [output_name]
#   <scene.py>    manim Scene 源文件 (.py)
#   <SceneClass>  Scene 类名
#   [output_name] 输出文件名 (不含扩展名, 默认同 SceneClass)
#
# 输出: ./animations/media/videos/<scene>/<quality>/<output>.mp4
# 画质: -ql (480p, 渲染快, 教学动画够用)
#
# 依赖: manim (ManimCE). 未安装时见下方提示。

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "用法: bash render.sh <scene.py> <SceneClass> [output_name]" >&2
    exit 1
fi

SCENE_FILE="$1"
SCENE_CLASS="$2"
OUTPUT_NAME="${3:-$SCENE_CLASS}"

# 脚本所在目录 (animations/), 无论从哪调用都正确
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 检测 manim 是否可用
if ! command -v manim >/dev/null 2>&1; then
    cat >&2 <<'EOF'
⚠ 未找到 manim 命令。请先安装 Manim Community Edition (ManimCE)。

常见安装方式 (任选其一):
  - nix:   nix profile install nixpkgs#manim
  - pip:   pip install manim
  - uv:    uv tool install manim

注意: 从源码构建 (pip/uv sdist) 需要 cairo/pango/libxcb 系统开发头文件。
nix 或系统包管理器安装的预构建版本无需额外编译依赖。

安装后重试本脚本。
EOF
    exit 1
fi

# -ql: 480p low quality, 渲染最快
# --media_dir: 强制产物落到脚本同级的 media/ (否则 manim 在 CWD 建 media/)
# --format mp4: 输出 MP4
manim -ql "$SCENE_FILE" "$SCENE_CLASS" \
    -o "$OUTPUT_NAME.mp4" --format mp4 \
    --media_dir "$SCRIPT_DIR/media"

echo ""
echo "=== 渲染完成 ==="
# manim 输出到 <media_dir>/videos/<scene_file_basename>/<quality>/<output>.mp4
MP4=$(find "$SCRIPT_DIR/media" -name "${OUTPUT_NAME}.mp4" 2>/dev/null | head -1)
if [ -n "$MP4" ]; then
    SIZE=$(du -h "$MP4" | cut -f1)
    echo "产物: $MP4 ($SIZE)"
    # lesson 在 ./lessons/ 下, 产物在 ./animations/media/ 下
    REL="${MP4#$SCRIPT_DIR/}"
    echo "嵌入 lesson: <video src=\"../animations/$REL\" controls></video>"
else
    echo "⚠ 未找到 $OUTPUT_NAME.mp4 — 检查上方日志" >&2
    exit 1
fi
