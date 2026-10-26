#!/bin/bash
# selftest.sh — hook 脚本自测（纯 bash assert，零依赖，GNU/BSD sed 兼容）。
# 全部断言对临时目录的副本执行，源文件只读；CI 可选跑：bash tools/git-hooks/selftest.sh
set -uo pipefail
cd "$(dirname "$0")"
HOOK="$PWD/commit-msg"          # 供临时仓内调用的绝对路径
pass=0; fail=0
T=$(mktemp -d)
MSG=$(mktemp)
D=""   # 先初始化防 trap 引用未赋值（set -u）
trap 'rm -rf "$T" "$MSG" "${D:-}"' EXIT
cp commit-msg common.sh "$T/" || { echo "FAIL: 副本复制失败"; exit 1; }

t() { # t <期望exit> <描述> <msg文件内容>
    local want="$1" desc="$2" msg="$3"
    printf '%s' "$msg" > "$MSG"
    bash "$T/commit-msg" "$MSG" >/dev/null 2>&1
    local got=$?
    if [ "$got" = "$want" ]; then pass=$((pass+1)); else
        fail=$((fail+1)); echo "FAIL: $desc (want=$want got=$got)"; fi
}
# 钩子形态边界
t 0 "conventional 通过"        $'feat(x): ok\n'
t 1 "非 conventional 拦截"     $'updated stuff\n'
t 0 "merge 豁免（subject）"    $'Merge branch a\n'
t 1 "正文含 Merge 行不豁免"    $'updated stuff\n\nMerge the config before deploy.\n'
t 1 "空 subject 拦截"          $'\n'
# 重复 Signed-off-by
t 1 "重复 signoff 拦截"        $'feat(x): ok\n\nSigned-off-by: A <a@t>\nSigned-off-by: A <a@t>\n'
t 0 "单个 signoff 通过"        $'feat(x): ok\n\nSigned-off-by: A <a@t>\n'
# 前缀（fork 语义，对副本临时开启）
sed 's/^COMMIT_PREFIX=""/COMMIT_PREFIX="[TW]"/' commit-msg > "$T/commit-msg"
grep -q '^COMMIT_PREFIX="\[TW\]"' "$T/commit-msg" || { echo "FAIL: 前缀 sed 未命中"; exit 1; }
t 1 "缺前缀拦截"               $'feat(x): no\n'
t 0 "[TW]+conventional 通过"   $'[TW] feat(x): ok\n'
t 1 "前缀子串注入拦截"         $'xxx feat: add [TW]\n'
t 0 "前缀后多空格归一化"       $'[TW]  feat(x): ok\n'
t 0 "Revert 豁免优先于前缀"    $'Revert "[TW] feat(x): ok"\n'
sed 's/^COMMIT_PREFIX="\[TW\]"/COMMIT_PREFIX=""/' commit-msg > "$T/commit-msg"
grep -q '^COMMIT_PREFIX=""' "$T/commit-msg" || { echo "FAIL: 前缀还原 sed 未命中"; exit 1; }
# --ci 批量形态（临时仓，身份用本地假值即可——commit-msg 不校验作者）
D=$(mktemp -d)
git init -q "$D" || { echo "FAIL: git init"; exit 1; }
cd "$D" || exit 1
git config user.name t && git config user.email t@t
mkdir -p .hooks && git config core.hooksPath "$D/.hooks"   # 隔离外部全局/系统级钩子
c() { git commit -q --allow-empty -m "$1" || { echo "FAIL: seed commit 失败: $1"; exit 1; }; }
c "seed bad"
c "feat: good"
c "feat: seed3"   # HEAD~2 需要至少 3 个 commit
bash "$HOOK" --ci HEAD~3 HEAD >/dev/null 2>&1   # 含 seed bad 的范围
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 范围报 bad"; }
GOOD=$(git rev-list --all --grep="feat: good" -n1)   # 按 subject 定位，不依赖 commit 序数
bash "$HOOK" --ci "$GOOD~1" "$GOOD" >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 合法 commit 应过"; }
# --ci 空范围（rebase 后 diff-base 含于 tip 的合法场景，期望 0）
bash "$HOOK" --ci HEAD HEAD >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 空范围应放行"; }
# fail-closed：不可达范围
bash "$HOOK" --ci 0000000000000000000000000000000000000000 HEAD >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: fail-closed 不可达范围"; }
# --ci 范围内含 0x1e 的 commit → fail-closed（前置拒绝路径）
git commit -q --allow-empty -m "feat: with $'\x1e' embedded" 2>/dev/null || git commit -q --allow-empty -m "feat: with control char"
bash "$HOOK" --ci HEAD~4 HEAD >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 应拒 0x1e 提交"; }
# log 行为：NO_COLOR 下无 ESC；warn 走 stderr
out=$(NO_COLOR=1 bash -c "source $PWD/common.sh 2>/dev/null; log_warn x" 2>&1)
[[ "$out" != *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: NO_COLOR 未生效"; }
out_w=$(bash -c "source $PWD/common.sh; log_warn w" 2>/dev/null); out_e=$(bash -c "source $PWD/common.sh; log_warn w" 2>&1 >/dev/null)
[[ -z "$out_w" && -n "$out_e" ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: log_warn 未走 stderr"; }
echo "selftest: $pass pass, $fail fail"
exit $fail
