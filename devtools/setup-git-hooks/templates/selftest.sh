#!/bin/bash
# selftest.sh — hook 脚本自测（纯 bash assert，零依赖，GNU/BSD sed 兼容）。
# 全部断言对临时目录的副本执行，源文件只读；CI 可选跑：bash tools/git-hooks/selftest.sh
set -uo pipefail
cd "$(dirname "$0")"
HDIR="$PWD"                    # hooks 目录绝对路径（后续测试段会 cd 走）
HOOK="$PWD/commit-msg"          # 供临时仓内调用的绝对路径
pass=0; fail=0
T=$(mktemp -d)
MSG=$(mktemp)
D=""   # 先初始化防 trap 引用未赋值（set -u）；IT/IT2/WT 同理由 :- 守护（r8 no8577）
trap 'rm -rf "$T" "$MSG" "${D:-}" "${IT:-}" "${IT2:-}" "${WT:-}"' EXIT
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
# 根提交占位：BAD~1 必须存在，否则 --ci BAD~1 走 fail-closed 恒 1，断言空转（r7 no14）
c "feat: initial"
c "seed bad"
BAD=$(git rev-parse HEAD)   # bad 定位后后续 seed 让范围可达
c "feat: good"
c "feat: seed3"
c "feat: seed4"
bash "$HOOK" --ci "$BAD~1" HEAD >/dev/null 2>&1   # bad~1..HEAD 含 bad（范围含左端点后第一条起）
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 范围报 bad"; }
GOOD=$(git rev-list --all --grep="feat: good" -n1)   # 按 subject 定位，不依赖 commit 序数
[ -n "$GOOD" ] || { echo "FAIL: GOOD 定位失败（--grep 落空，后续断言无意义）"; exit 1; }   # r8 no cb55
bash "$HOOK" --ci "$GOOD~1" "$GOOD" >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 合法 commit 应过"; }
# --ci 空范围（rebase 后 diff-base 含于 tip 的合法场景，期望 0）
bash "$HOOK" --ci HEAD HEAD >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 空范围应放行"; }
# fail-closed：不可达范围
bash "$HOOK" --ci 0000000000000000000000000000000000000000 HEAD >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: fail-closed 不可达范围"; }
# --ci 范围内含 0x1e 的 commit → fail-closed（用 printf 写 0x1e 进 commit message，
# -m "$'\x1e'" 双引号不展开；此前的字面文本 seed 无 0x1e，已删——误导性死代码 r7 no15）
git commit -q --allow-empty -m "feat: clean after bad" || { echo "FAIL: clean seed 失败"; exit 1; }
LC_ALL=C git commit -q --allow-empty -m "$(printf 'feat: evil \x1e tail')" || { echo "FAIL: 0x1e commit 失败"; exit 1; }
EVIL=$(git rev-parse HEAD)
bash "$HOOK" --ci "$EVIL~1" "$EVIL" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 应拒 0x1e 提交"; }
# 颜色路径：非 TTY 管道下用 FORCE_COLOR 注入验证着色可达，NO_COLOR 优先压过（r7 no19）；
# 开色用例显式 NO_COLOR=（清空）——CI 环境若全局导出 NO_COLOR 会让断言假红（r8 no c819）
out=$(NO_COLOR= FORCE_COLOR=1 bash -c "source $T/common.sh 2>/dev/null; log_warn x" 2>&1)
[[ "$out" == *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: FORCE_COLOR 未生效"; }
out=$(NO_COLOR=1 FORCE_COLOR=1 bash -c "source $T/common.sh 2>/dev/null; log_warn x" 2>&1)
[[ "$out" != *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: NO_COLOR 未压过 FORCE_COLOR"; }
out_w=$(bash -c "source $T/common.sh; log_warn w" 2>/dev/null); out_e=$(bash -c "source $T/common.sh; log_warn w" 2>&1 >/dev/null)
[[ -z "$out_w" && -n "$out_e" ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: log_warn 未走 stderr"; }
# install.sh：hooksPath 写入断言（临时主仓 = 当前 clone 之外的测试 clone 语义）。
# cp 不接 2>/dev/null：环境准备失败必须显式暴露而非让断言假阳性（r7 no17）
IT=$(mktemp -d) && git init -q "$IT" && mkdir -p "$IT/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,commit-msg,pre-commit,pre-push,common.sh} "$IT/tools/git-hooks/" \
    || { echo "FAIL: install 测试环境准备失败"; exit 1; }
(cd "$IT" && bash tools/git-hooks/install.sh >/dev/null 2>&1 && [ "$(git -C "$IT" config --get core.hooksPath)" = "tools/git-hooks" ])
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: install.sh hooksPath 写入"; }
rm -rf "$IT"
# 迁移清理分支：worktree 级 hooksPath 覆盖应被 install.sh 清除（r7 no7，本迁移核心逻辑）。
# 用 attached worktree（带 branch 行）——正是 r8 no30a9 暴露的、旧解析永不触发的形态
IT2=$(mktemp -d) && git init -q "$IT2" && mkdir -p "$IT2/tools/git-hooks" "$IT2/.hooks" \
    && cp "$HDIR"/{install.sh,commit-msg,common.sh} "$IT2/tools/git-hooks/" \
    || { echo "FAIL: 迁移用例环境准备失败"; exit 1; }
git -C "$IT2" config core.hooksPath "$IT2/.hooks"   # 种子提交隔离外部钩子（r8 no4bbd，同 $D 段口径）
git -C "$IT2" -c user.name=t -c user.email=t@t commit -q --allow-empty -m "init" || { echo "FAIL: 迁移用例 seed 失败"; exit 1; }
git -C "$IT2" config extensions.worktreeConfig true
WT=$(mktemp -d)
git -C "$IT2" worktree add -q -b tmp-mig-wt "$WT" HEAD >/dev/null 2>&1 || { echo "FAIL: 迁移用例 worktree 创建失败"; exit 1; }
git -C "$WT" config --worktree core.hooksPath "/stale/hooks"   # 模拟旧 install-hooks.sh 残留
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    || { fail=$((fail+1)); echo "FAIL: 迁移用例 install.sh 非零退出（r8 no34ab）"; }
[ -z "$(git -C "$WT" config --worktree --get core.hooksPath 2>/dev/null)" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: install.sh 未清除 worktree 级 hooksPath"; }
rm -rf "$IT2" "$WT"
# 伪造终止符重同步（r8 no59e3）：body 内嵌独立 \t\x1e 行把重复 signoff 拆到两个伪记录
# 里逃过单记录查重——记录头 40-hex 校验应 fail-closed
IT3=$(mktemp -d) && git init -q "$IT3" && mkdir -p "$IT3/tools/git-hooks" "$IT3/.hooks" \
    && cp "$HDIR"/{commit-msg,common.sh} "$IT3/tools/git-hooks/" \
    || { echo "FAIL: 重同步用例环境准备失败"; exit 1; }
git -C "$IT3" config core.hooksPath "$IT3/.hooks" && mkdir -p "$IT3/.hooks"
git -C "$IT3" config user.name t && git -C "$IT3" config user.email t@t
printf 'feat: x\nSigned-off-by: A <a@t>\n\t\x1e\nfeat: y\nSigned-off-by: A <a@t>\n' > "$IT3/forged.msg"
git -C "$IT3" commit -q --allow-empty --no-verify -F "$IT3/forged.msg" || { echo "FAIL: 重同步用例 seed 失败"; exit 1; }
EVIL=$(git -C "$IT3" rev-parse HEAD)
bash "$HDIR/commit-msg" --ci "$EVIL~1" "$EVIL" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 伪造终止符重同步应拒"; }
rm -rf "$IT3"
echo "selftest: $pass pass, $fail fail"
exit $fail
