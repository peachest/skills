#!/bin/bash
# 截图三查自检：宽度 / 完整性 / 一致性
# 用法: shot-verify.sh <screenshots-dir> <expectations-file>
#   expectations-file 每行: <png文件名> <关键UUID出现次数> [更多UUID...] —— podanno 图按申请数核
# 退出码: 0=三查全过, 1=有 FAIL（逐条打印 FAIL/OK）
set -u
DIR="${1:?用法: shot-verify.sh <screenshots-dir> <expectations-file>}"
EXPECT="${2:?用法: shot-verify.sh <screenshots-dir> <expectations-file>}"
S2PNG="$HOME/tools/playwright-runner/svg2png.mjs"
fail=0

for svg in "$DIR"/*.svg; do
  name=$(basename "$svg" .svg)
  png="$DIR/$name.png"

  # 查1: 宽度——SVG width 必须 >= 最长行渲染预算（防 --width 像素误用裁切）
  w=$(grep -o 'width="[0-9.]*"' "$svg" | head -1 | grep -o '[0-9.]*')
  # 经验值: freeze 字符渲染每字符约 6.6px; raw 最宽行 × 6.6 需 <= svg width
  # raw 源在同目录 <name>-raw.txt 或上游 evidence; 无 raw 则跳过本查的精确比对
  raw="$(dirname "$svg")/$name-raw.txt"
  if [ -f "$raw" ]; then
    maxcols=$(awk '{ if (length($0) > m) m = length($0) } END { print m }' "$raw")
    need=$(python3 -c "print(int($maxcols * 6.6))")
    if python3 -c "exit(0 if $w >= $need else 1)"; then
      echo "OK   width  $name: svg=${w}px >= need≈${need}px (maxcol=$maxcols)"
    else
      echo "FAIL width  $name: svg=${w}px < need≈${need}px (maxcol=$maxcols) → 右侧被裁，去掉 --width 重渲染"
      fail=1
    fi
  else
    if python3 -c "exit(0 if $w >= 600 else 1)"; then
      echo "OK   width  $name: svg=${w}px (无 raw，粗检)"
    else
      echo "FAIL width  $name: svg=${w}px < 600px 疑似误传像素宽度"
      fail=1
    fi
  fi

  # 查2: 完整性——按 expectations 核对关键 UUID 数量（防数据段被截）
  if [ -f "$EXPECT" ]; then
    while read -r fname want uuids; do
      [ "$fname" = "$name" ] || continue
      [ -z "$uuids" ] && continue
      for u in $uuids; do
        if grep -q "$u" "$svg"; then
          echo "OK   expect $name: 含 $u"
        else
          echo "FAIL expect $name: 缺 $u → 数据被截或分配错误"
          fail=1
        fi
      done
    done < "$EXPECT"
  fi

  # 查3: 一致性——PNG 必须与当前 SVG 重渲染逐字节一致（防交付包陈旧）
  if [ -f "$png" ]; then
    if node "$S2PNG" "$(realpath "$svg")" /tmp/shot-verify-regen.png >/dev/null 2>&1 \
       && cmp -s "$png" /tmp/shot-verify-regen.png; then
      echo "OK   fresh  $name: png == svg 重渲染"
    else
      echo "FAIL fresh  $name: png 与 svg 重渲染不一致 → 交付包是旧图，重转 PNG"
      fail=1
    fi
  else
    echo "FAIL fresh  $name: 缺 $name.png"
    fail=1
  fi
done
exit $fail
