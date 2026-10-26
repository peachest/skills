#!/usr/bin/env bash
# 校验 SYNC.md 安装子集与 ~/.agents/skills 实装一致。source of truth = SYNC.md 的 Installed subset 节。
set -u
cd "$(dirname "$0")"
expected=$(grep -m1 '^`how`' SYNC.md | tr -d '`,' )
fail=0
for s in $expected; do
  [ -d ~/.agents/skills/$s ] || { echo "MISSING: $s listed in SYNC.md but not installed"; fail=1; }
  diff -r -x __pycache__ ~/.agents/skills/$s skills/$s >/dev/null 2>&1 || { echo "DRIFT: $s install copy differs from vendor"; fail=1; }
done
for d in ~/.agents/skills/*/; do
  n=$(basename "$d"); [ -f "skills/$n/SKILL.md" ] || continue
  # pstack 出身判定：安装副本与 vendor 逐字节一致才计入（mattpocock 等其他来源的同名 skill 不归本清单管）
  diff -r -x __pycache__ "$d" "skills/$n" >/dev/null 2>&1 || continue
  echo "$expected" | tr ' ' '\n' | grep -qx "$n" || { echo "UNLISTED: $n installed from vendor but not in SYNC.md"; fail=1; }
done
[ $fail -eq 0 ] && echo "pstack subset: OK ($(echo "$expected" | wc -w) skills)"
exit $fail
