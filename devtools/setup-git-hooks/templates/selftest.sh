#!/bin/bash
# selftest.sh — hook 脚本自测（纯 bash assert，零依赖，GNU/BSD sed 兼容）。
# 单条消息形态断言对临时目录副本执行（t() 对 $T 副本）；--ci 用例对源文件 HOOK 直调
# （CI 消费的就是源文件本身，副本无意义）；CI 接线：make selftest / commit-check job
set -uo pipefail
cd "$(dirname "$0")"
HDIR="$PWD"                    # hooks 目录绝对路径（后续测试段会 cd 走）
HOOK="$PWD/commit-msg"          # 供临时仓内调用的绝对路径
pass=0; fail=0
T=$(mktemp -d) || { echo "FAIL: mktemp -d 失败"; exit 1; }
MSG=$(mktemp) || { echo "FAIL: mktemp 失败"; exit 1; }
D=""   # 先初始化防 trap 引用未赋值（set -u）；IT/IT2/IT3/WT 同理由 :- 守护（r8 no8577/r9 no8523）
trap 'rm -rf "$T" "$MSG" "${D:-}" "${IT:-}" "${IT2:-}" "${IT3:-}" "${WT:-}"' EXIT
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
git config user.name t && git config user.email t@t || { echo "FAIL: 环境 git config 失败"; exit 1; }
mkdir -p .hooks && git config core.hooksPath "$D/.hooks" || { echo "FAIL: 钩子隔离配置失败"; exit 1; }   # 隔离外部全局/系统级钩子
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
out_w=$(bash -c 'source "$1"; log_warn w' _ "$T/common.sh" 2>/dev/null); out_e=$(bash -c 'source "$1"; log_warn w' _ "$T/common.sh" 2>&1 >/dev/null)
[[ -z "$out_w" && "$out_e" == *"[WARN]"* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: log_warn 未走 stderr 或输出非 log_warn（r13 no108）"; }
# ESC 剥离（r14 no111）：消息内嵌 ANSI 序列时输出不得含原始 ESC，正文文本保留
out=$(NO_COLOR=1 bash -c "source \"$T/common.sh\" 2>/dev/null; log_warn \$(printf 'x\\033[31my')" 2>&1)
case "$out" in *$'\033'*) fail=$((fail+1)); echo "FAIL: log_warn 未剥离 ESC" ;; *x[31my*) pass=$((pass+1)) ;; *) fail=$((fail+1)); echo "FAIL: ESC 用例输出异常: $out" ;; esac
# install.sh：hooksPath 写入断言（临时主仓 = 当前 clone 之外的测试 clone 语义）。
# cp 不接 2>/dev/null：环境准备失败必须显式暴露而非让断言假阳性（r7 no17）
IT=$(mktemp -d) && git init -q "$IT" && mkdir -p "$IT/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,commit-msg,pre-commit,pre-push,common.sh} "$IT/tools/git-hooks/" \
    || { echo "FAIL: install 测试环境准备失败"; exit 1; }
(cd "$IT" && bash tools/git-hooks/install.sh >/dev/null 2>&1 && [ "$(git -C "$IT" config --get core.hooksPath)" = "tools/git-hooks" ])
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: install.sh hooksPath 写入"; }
rm -rf "$IT"
# fail-open 分支（r9 no 4776）：旧分支无 tools/git-hooks 目录 → exit 0 且不写配置
IT=$(mktemp -d) && git init -q "$IT" || { echo "FAIL: fail-open 用例环境准备失败"; exit 1; }
(cd "$IT" && bash "$HDIR/install.sh" >/dev/null 2>&1) \
    && [ -z "$(git -C "$IT" config --get core.hooksPath 2>/dev/null)" ] \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: fail-open 应 exit 0 且不写配置"; }
rm -rf "$IT"
# 迁移清理分支：worktree 级 hooksPath 覆盖应被 install.sh 清除（r7 no7，本迁移核心逻辑）。
# 用 attached worktree（带 branch 行）——正是 r8 no30a9 暴露的、旧解析永不触发的形态
IT2=$(mktemp -d) && git init -q "$IT2" && mkdir -p "$IT2/tools/git-hooks" "$IT2/.hooks" \
    && cp "$HDIR"/{install.sh,commit-msg,common.sh} "$IT2/tools/git-hooks/" \
    || { echo "FAIL: 迁移用例环境准备失败"; exit 1; }
git -C "$IT2" config core.hooksPath "$IT2/.hooks"   # 种子提交隔离外部钩子（r8 no4bbd，同 $D 段口径）
git -C "$IT2" -c user.name=t -c user.email=t@t commit -q --allow-empty -m "init" || { echo "FAIL: 迁移用例 seed 失败"; exit 1; }
git -C "$IT2" config extensions.worktreeConfig true || { echo "FAIL: extensions.worktreeConfig 开启失败"; exit 1; }
WT=$(mktemp -d)
git -C "$IT2" worktree add -q -b tmp-mig-wt "$WT" HEAD >/dev/null 2>&1 || { echo "FAIL: 迁移用例 worktree 创建失败"; exit 1; }
git -C "$WT" config --worktree core.hooksPath "/stale/hooks" || { echo "FAIL: worktree 级 hooksPath 写入失败（断言会空转）"; exit 1; }   # 模拟旧 install-hooks.sh 残留
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    || { fail=$((fail+1)); echo "FAIL: 迁移用例 install.sh 非零退出（r8 no34ab）"; }
[ -z "$(git -C "$WT" config --worktree --get core.hooksPath 2>/dev/null)" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: install.sh 未清除 worktree 级 hooksPath"; }
# 多值清理用例（r10 no cf09 → r12 no86 修订）：worktree 级同键双值在 --unset 下必败，
# 已改用 --unset-all——本用例验证多值也能清理成功（exit 0），不再走 fail-loud
# 注意首次 install 已把残留清空，需连加两个值才能构成多值场景
git -C "$WT" config --worktree --add core.hooksPath /stale/hooks \
    || { echo "FAIL: 多值 --add 1 失败（断言会空转）"; exit 1; }
git -C "$WT" config --worktree --add core.hooksPath /stale/hooks \
    || { echo "FAIL: 多值 --add 2 失败（断言会空转）"; exit 1; }
[ "$(git -C "$WT" config --worktree --get-all core.hooksPath | wc -l)" = "2" ] \
    || { echo "FAIL: 多值场景未构造成功（get-all 计数非 2）"; exit 1; }   # 环境断言（r13 no107）
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 多值清理应成功（--unset-all，r12 no86）"; }
[ -z "$(git -C "$WT" config --worktree --get-all core.hooksPath 2>/dev/null)" ] \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 多值未清空"; }
git -C "$WT" config --worktree --unset-all core.hooksPath 2>/dev/null || true
# 悬空 worktree：目录已删但元数据残留 → 跳过校验 + prune 提示，不置 mismatch（r11 no 75）
rm -rf "$WT"
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 悬空 worktree 应跳过不报错"; }
rm -rf "$IT2"
# pre-commit 零依赖冒烟（r11 no 72）：空仓上应干净通过（无 staged 文件、无 HEAD）
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
    || { echo "FAIL: pre-commit 冒烟环境准备失败"; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-commit 空仓冒烟失败"; }
# 失败路径（r13 no105）：未 gofmt 的 .go staged → gofmt 拦截 + fail 聚合 → exit 1
# （同时回归 set -e 与循环体交互、fail 聚合两处语义）
printf 'package x\nfunc  y() {}\n' > "$IT/bad.go"
git -C "$IT" add bad.go || { echo "FAIL: git add 环境准备失败"; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-commit 应拦未 gofmt 文件"; }
rm -rf "$IT"
# pre-push 冒烟（r11 no91）：空仓 + </dev/null stdin——验证可解析执行、无 set -u 未绑定；
# 危险路径（worktree/make/网络）仅在非删除推送且有 go 时触发，空仓 stdin 空即跳过
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-push,common.sh} "$IT/" \
    || { echo "FAIL: pre-push 冒烟环境准备失败"; exit 1; }
(cd "$IT" && bash "$IT/pre-push" </dev/null >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-push 空仓冒烟失败"; }
# 回退分支（r13 no106）：env -u PATH -u HOME——path_fallback 与 gopath_prefix 归空边界
(cd "$IT" && env -u PATH -u HOME bash "$IT/pre-push" </dev/null >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-push env -u PATH/HOME 冒烟失败"; }
rm -rf "$IT"
# wt.toml [pre-start] hooks 包装命令退出码契约（r13 no94）：
#   WT_NO_HOOKS=1 → exit 0（静默跳过）；旧分支无 install.sh → exit 0；install.sh 失败 → 非零传播
# 提取前提（r14 no120）：hooks 行为单行单值、无行尾注释；内层不含 TOML 转义（r14 no112
# 已重写 hooks 行避免 \"），提取后须含 install.sh 关键字方可作为有效命令串
HOOKS_WRAP=$(sed -n 's/^hooks = "//p' "$HDIR/../../.config/wt.toml" | sed 's/"$//')
[ -n "$HOOKS_WRAP" ] && case "$HOOKS_WRAP" in *install.sh*) ;; *) echo "FAIL: 提取的 hooks 包装命令非法: $HOOKS_WRAP"; exit 1 ;; esac \
    || { echo "FAIL: 未从 wt.toml 提取 hooks 包装命令"; exit 1; }
IT=$(mktemp -d) && git init -q "$IT" && mkdir -p "$IT/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,common.sh} "$IT/tools/git-hooks/" \
    || { echo "FAIL: wt 包装用例环境准备失败"; exit 1; }
# 用例 1/2：WT_NO_HOOKS 静默 exit 0；正常安装 exit 0
r=$(cd "$IT" && WT_NO_HOOKS=1 sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
[ "$r" = "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: WT_NO_HOOKS 应静默 exit 0（got $r）"; }
r=$(cd "$IT" && sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
[ "$r" = "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 正常安装应 exit 0（got $r）"; }
# 用例 3（r14 no119）：install.sh 失败 → 非零传播。chmod -x 无法模拟失败（包装命令是
# bash 显式调用，不需要执行位）——用非法命令触发 bash 退出码 127
printf 'fail-marker\n' > "$IT/tools/git-hooks/install.sh"
r=$(cd "$IT" && sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
[ "$r" != "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: install.sh 失败应非零传播（got $r）"; }
# 用例 4（r14 no119）：旧分支无 install.sh → 包装层 exit 0
rm -rf "$IT/tools/git-hooks"
r=$(cd "$IT" && sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
[ "$r" = "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 无 hooks 目录应静默 exit 0（got $r）"; }
rm -rf "$IT"
# L1 0x1e 文件检查（r14 no123）：钩子模式的 grep 文件路径与 L2 --ci 的 %B 路径实现
# 独立，各补一条防同口径回归。消息文件含 0x1e → commit-msg（钩子形态）exit 1
IT4=$(mktemp -d) && git init -q "$IT4" && mkdir -p "$IT4/tools/git-hooks"     && cp "$HDIR"/{commit-msg,common.sh} "$IT4/tools/git-hooks/"     && git -C "$IT4" config user.name t && git -C "$IT4" config user.email t@t     || { echo "FAIL: L1 0x1e 用例环境准备失败"; exit 1; }
printf 'feat: x\n\x1e\n' > "$IT4/msg"
(cd "$IT4" && bash "$IT4/tools/git-hooks/commit-msg" "$IT4/msg" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: L1 应拒含 0x1e 的消息文件"; }
rm -rf "$IT4"
# 0x1e 拒绝回归（body 含独立 \t\x1e 行形态——涵盖伪造终止符攻击的输入特征；
# r11 重写后不再有记录协议，0x1e 一律 fail-closed，r12 no92 注释对齐）。
# 先 seed 一个普通提交：forged 提交不能是根提交，否则 EVIL~1 不存在、断言空转（r9 no aee5）
IT3=$(mktemp -d) && git init -q "$IT3" && mkdir -p "$IT3/tools/git-hooks" "$IT3/.hooks" \
    && cp "$HDIR"/{commit-msg,common.sh} "$IT3/tools/git-hooks/" \
    || { echo "FAIL: 重同步用例环境准备失败"; exit 1; }
git -C "$IT3" config core.hooksPath "$IT3/.hooks" && mkdir -p "$IT3/.hooks"
git -C "$IT3" config user.name t && git -C "$IT3" config user.email t@t
git -C "$IT3" commit -q --allow-empty -m "feat: initial" || { echo "FAIL: 重同步用例 initial seed 失败"; exit 1; }
printf 'feat: x\nSigned-off-by: A <a@t>\n\t\x1e\nfeat: y\nSigned-off-by: A <a@t>\n' > "$IT3/forged.msg"
git -C "$IT3" commit -q --allow-empty --no-verify -F "$IT3/forged.msg" || { echo "FAIL: 重同步用例 forged seed 失败"; exit 1; }
EVIL=$(git -C "$IT3" rev-parse HEAD)
# 在 IT3 内执行：--ci 的 git log 按 cwd 解析仓，跨仓调用会读错仓 → fail-closed 恒 1、断言空转（r10 no b1e3）
(cd "$IT3" && bash "$HDIR/commit-msg" --ci "$EVIL~1" "$EVIL" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 伪造终止符重同步应拒"; }
rm -rf "$IT3"
echo "selftest: $pass pass, $fail fail"
exit $fail
