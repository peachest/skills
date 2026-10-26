#!/bin/bash
# selftest.sh — hook 脚本自测（纯 bash assert，零依赖，GNU/BSD sed 兼容）。
# 单条消息形态断言对临时目录副本执行（t() 对 $T 副本）；--ci 用例对源文件 HOOK 直调
# （CI 消费的就是源文件本身，副本无意义）；CI 接线：make selftest / commit-check job
set -uo pipefail
cd "$(dirname "$0")"
HDIR="$PWD"                    # hooks 目录绝对路径（后续测试段会 cd 走）
HOOK="$PWD/commit-msg"          # 供临时仓内调用的绝对路径
pass=0; fail=0; skipped=0   # skipped：缺工具链的 SKIP 用例计数（r17 no174）
# 配置隔离（r18 no192·medium）：t() 形态矩阵以真实仓库为 cwd 跑钩子副本，钩子会读
# git config core.commentchar——屏蔽全局/系统级配置，防环境相关假红/假绿；
# IT6 等本地配置不受影响
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
T=$(mktemp -d) || { echo "FAIL: mktemp -d 失败"; exit 1; }
MSG=$(mktemp) || { echo "FAIL: mktemp 失败"; exit 1; }
D=""   # 先初始化防 trap 引用未赋值（set -u）；IT/IT2/IT3/WT 同理由 :- 守护（r8 no8577/r9 no8523）
trap 'rm -rf "$T" "$MSG" "${D:-}" "${IT:-}" "${IT2:-}" "${IT3:-}" "${IT4:-}" "${IT5:-}" "${IT6:-}" "${WT:-}"' EXIT   # IT4 同纳入（r15 no140）
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
t 0 "merge 豁免（subject）"    $'Merge branch a\n'   # 模板恒为 "Merge branch 'x'"：branch 后必空格
# octopus 复数形态（r15 no127）
t 0 "octopus branches 豁免"   $'Merge branches \'a\' and \'b\'\n'
t 0 "octopus tags 豁免"       $'Merge tags t1 and t2\n'
t 1 "手写 Merge 不豁免"        $'Merge 手工合并\n'   # 无空格变体/非模板开头不再豁免（r12 no79）
# 交互式 rebase 自动形态豁免 + Revert 豁免（r15 no132）
t 0 "fixup! 豁免"             $'fixup! feat(x): ok\n'
t 0 "squash! 豁免"            $'squash! feat(x): ok\n'
t 0 "amend! 豁免"             $'amend! feat(x): ok\n'
t 0 "Revert 豁免"             $'Revert "feat: x"\n\nThis reverts commit abc.\n'
# CRLF：尾随 \r 并入空白剥离（r10 no 7d2c 回归）
t 0 "CRLF 尾随 \r"            $'feat: x\r\n\nbody\r\n'
t 1 "正文含 Merge 行不豁免"    $'updated stuff\n\nMerge the config before deploy.\n'
t 1 "空 subject 拦截"          $'\n'
# 重复 Signed-off-by
t 1 "重复 signoff 拦截"        $'feat(x): ok\n\nSigned-off-by: A <a@t>\nSigned-off-by: A <a@t>\n'
# 归一化变体判重（r17 no171）：键大小写不敏感、多空格折叠、无空格变体；值大小写敏感
t 1 "signoff 键大小写变体"     $'feat(x): ok\n\nSigned-off-by: A <a@t>\nsigned-off-by: A <a@t>\n'
t 1 "signoff 多空格折叠"       $'feat(x): ok\n\nSigned-off-by:  A <a@t>\nSigned-off-by: A <a@t>\n'
t 1 "signoff 无空格变体"       $'feat(x): ok\n\nSigned-off-by:A <a@t>\nSigned-off-by: A <a@t>\n'
t 0 "不同签署人不误判"          $'feat(x): ok\n\nSigned-off-by: A <a@t>\nSigned-off-by: B <b@t>\n'
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
# --ci 空范围：r17 no168 起 CI 默认 fail-closed；人工调试合法空范围需显式豁免
bash "$HOOK" --ci HEAD HEAD >/dev/null 2>&1
[ $? != 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 空范围应默认拒绝（r17 no168）"; }
COMMIT_CI_ALLOW_EMPTY=1 bash "$HOOK" --ci HEAD HEAD >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 空范围豁免后应放行"; }
# Merge 反伪造（r18 no181·medium）：手写 "Merge branch 'x'" 主题的普通提交 → CI 拒绝
git -C "$D" commit -q --allow-empty --no-verify -m "Merge branch 'fake'" || { echo "FAIL: 反伪造用例 seed 失败"; exit 1; }
FAKE=$(git -C "$D" rev-parse HEAD)
bash "$HOOK" --ci "$FAKE~1" "$FAKE" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 应拒手写 Merge 主题（反伪造）"; }
# 真 merge commit（>=2 parent）→ 放行
git -C "$D" checkout -q -b mbranch HEAD~1 && git -C "$D" commit -q --allow-empty -m "feat: mside" && git -C "$D" checkout -q - >/dev/null 2>&1
git -C "$D" merge -q --no-ff --no-edit mbranch >/dev/null 2>&1 || { echo "FAIL: 反伪造用例 merge seed 失败"; exit 1; }
MERGE=$(git -C "$D" rev-parse HEAD)
bash "$HOOK" --ci "$MERGE~1" "$MERGE" >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: --ci 应放行真 merge commit"; }
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
out=$(NO_COLOR= FORCE_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn x' _ "$T/common.sh" 2>&1)   # 传参形式防 TMPDIR 空格（r15 no142）
[[ "$out" == *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: FORCE_COLOR 未生效"; }
out=$(NO_COLOR=1 FORCE_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn x' _ "$T/common.sh" 2>&1)
[[ "$out" != *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: NO_COLOR 未压过 FORCE_COLOR"; }
out_w=$(bash -c 'source "$1"; log_warn w' _ "$T/common.sh" 2>/dev/null); out_e=$(bash -c 'source "$1"; log_warn w' _ "$T/common.sh" 2>&1 >/dev/null)
[[ -z "$out_w" && "$out_e" == *"[WARN]"* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: log_warn 未走 stderr 或输出非 log_warn（r13 no108）"; }
# ESC 剥离（r14 no111）：消息内嵌 ANSI 序列时输出不得含原始 ESC，正文文本保留
out=$(NO_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn "$2"' _ "$T/common.sh" "$(printf 'x\033[31my')" 2>&1)   # 传参形式（r17 no173 同 no142）
case "$out" in *$'\033'*) fail=$((fail+1)); echo "FAIL: log_warn 未剥离 ESC" ;; *x\[31my*) pass=$((pass+1)) ;; *) fail=$((fail+1)); echo "FAIL: ESC 用例输出异常: $out" ;; esac   # [ 转义（r15 no141：未闭合 [ 按字面是冷门巧合语义）
# UTF-8 C1 定点剥除（r17 no158）：8 位 CSI/OSC 起始符不得透传
out=$(NO_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn "$2"' _ "$T/common.sh" "$(printf 'x\xc2\x9b[31my\xc2\x9d')" 2>&1)
case "$out" in *$'\xc2\x9b'*|*$'\xc2\x9d'*) fail=$((fail+1)); echo "FAIL: log_warn 未剥离 UTF-8 C1" ;; *x\[31my*) pass=$((pass+1)) ;; *) fail=$((fail+1)); echo "FAIL: C1 用例输出异常" ;; esac   # 同 r15 no141 转义口径（r18 no195）
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
git -C "$IT2" config core.hooksPath "$IT2/.hooks" || { echo "FAIL: IT2 钩子隔离配置失败（会退回全局钩子产生非确定结果）"; exit 1; }   # 种子提交隔离外部钩子（r8 no4bbd，同 $D 段口径；r16 no154）
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
[ "$(git -C "$WT" config --worktree --get-all core.hooksPath | grep -c .)" = "2" ] \
    || { echo "FAIL: 多值场景未构造成功（get-all 计数非 2）"; exit 1; }   # 环境断言（r13 no107）；grep -c 而非 wc -l（BSD 前导空格填充，r15 no138）
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 多值清理应成功（--unset-all，r12 no86）"; }
[ -z "$(git -C "$WT" config --worktree --get-all core.hooksPath 2>/dev/null)" ] \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 多值未清空"; }
git -C "$WT" config --worktree --unset-all core.hooksPath 2>/dev/null || true
# 悬空 worktree：目录已删但元数据残留 → 跳过校验 + prune 提示，不置 mismatch（r11 no 75）
rm -rf "$WT"
mig_out=$(cd "$IT2" && bash tools/git-hooks/install.sh 2>&1); mig_rc=$?
{ [ "$mig_rc" = "0" ] && [[ "$mig_out" == *"worktree prune"* ]]; } \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 悬空 worktree 应跳过且输出 prune 提示（r18 no194，got rc=$mig_rc）"; }
rm -rf "$IT2"
# pre-commit 零依赖冒烟（r11 no 72）：空仓上应干净通过（无 staged 文件、无 HEAD）
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
    || { echo "FAIL: pre-commit 冒烟环境准备失败"; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-commit 空仓冒烟失败"; }
# 失败路径（r13 no105）：未 gofmt 的 .go staged → gofmt 拦截 + fail 聚合 → exit 1
# （同时回归 set -e 与循环体交互、fail 聚合两处语义）
if command -v gofmt >/dev/null; then
    printf 'package x\nfunc  y() {}\n' > "$IT/bad.go"
    git -C "$IT" add bad.go || { echo "FAIL: git add 环境准备失败"; exit 1; }
    (cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
    [ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-commit 应拦未 gofmt 文件"; }
else
    echo "SKIP: gofmt 未安装，跳过 gofmt 拦截用例（r17 no174：SKIP 不阻塞无 Go 环境的 make selftest）"
    skipped=$((skipped+1))
fi
rm -rf "$IT"
# clang-format 拦截路径（r16 no166·medium）：未格式化 .c staged → 拦截 + "无法读取
# staged 内容"分支同链路（r16 no153/no165）
# 空白符检查分支（r18 no190）：staged 含行尾空白 → 拦截（覆盖 diff-index --check 路径）
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
    || { echo "FAIL: 空白用例环境准备失败"; exit 1; }
printf 'package x\n// trailing \n' > "$IT/ws.go"
git -C "$IT" add ws.go || { echo "FAIL: 空白用例 git add 失败"; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-commit 应拦行尾空白（r18 no190）"; }
rm -rf "$IT"
if command -v clang-format >/dev/null; then
    IT=$(mktemp -d) && git init -q "$IT" \
        && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
        || { echo "FAIL: clang-format 用例环境准备失败"; exit 1; }
    printf 'int main(){return 0;}\n' > "$IT/bad.c"
    git -C "$IT" add bad.c || { echo "FAIL: clang-format 用例 git add 失败"; exit 1; }
    (cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
    [ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: pre-commit 应拦未 clang-format 文件"; }
    rm -rf "$IT"
else
    echo "SKIP: clang-format 未安装，跳过 clang-format 拦截用例（r17 no174 同口径）"
    skipped=$((skipped+1))
fi
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
# 聚合失败 → 非零（r16 no148·medium）：损坏 config.worktree 使后续 git config 全部 fatal——
# 迁移分支被跳过、配置写入本身也 128 退出；可观测契约是“非零感知”，不锁定具体退出码
# （wt pre-start / make setup 只消费非零信号）
IT5=$(mktemp -d) && git init -q "$IT5" && mkdir -p "$IT5/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,common.sh} "$IT5/tools/git-hooks/" \
    && git -C "$IT5" config user.name t && git -C "$IT5" config user.email t@t \
    || { echo "FAIL: 聚合失败用例环境准备失败"; exit 1; }
git -C "$IT5" commit -q --allow-empty --no-verify -m "init" || { echo "FAIL: 聚合用例 seed 失败"; exit 1; }
git -C "$IT5" config extensions.worktreeConfig true || { echo "FAIL: worktreeConfig 开启失败"; exit 1; }
printf 'this is not valid git-config\x00garbage' > "$IT5/.git/config.worktree"
(cd "$IT5" && bash tools/git-hooks/install.sh >/dev/null 2>&1)
[ $? != 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 清理/写入失败应非零感知（r16 no148）"; }
rm -rf "$IT5"
# wt.toml [pre-start] hooks 包装命令退出码契约（r13 no94）：
#   WT_NO_HOOKS=1 → exit 0（静默跳过）；旧分支无 install.sh → exit 0；install.sh 失败 → 非零传播
# 提取前提（r14 no120）：hooks 行为单行单值、无行尾注释；内层不含 TOML 转义（r14 no112
# 已重写 hooks 行避免 \"），提取后须含 install.sh 关键字方可作为有效命令串
hooks_lines=$(sed -n 's/^hooks = "//p' "$HDIR/../../.config/wt.toml" | grep -c .)   # grep -c 而非 wc -l（BSD 前导空格，r18 no191 同 r15 no138）
[ "$hooks_lines" = "1" ] || { echo "FAIL: wt.toml 存在 $hooks_lines 行 hooks 键（提取契约定为单行，r17 no175）"; exit 1; }
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
# WT_NO_HOOKS=0/false 不跳过（仅字面 1 禁用，r15 no124）
r=$(cd "$IT" && git config --unset core.hooksPath 2>/dev/null; WT_NO_HOOKS=0 sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
{ [ "$r" = "0" ] && git -C "$IT" config --get core.hooksPath | grep -q tools/git-hooks; } \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: WT_NO_HOOKS=0 应正常安装而非跳过"; }
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
# commentchar 路径（r16 no146）：core.commentchar=';' 时钩子按 ';' 剥注释行——
# 模板块首行为注释行应被剥离后正常校验，而非误拦"提交信息不能为空"
IT6=$(mktemp -d) && git init -q "$IT6" && mkdir -p "$IT6/tools/git-hooks" \
    && cp "$HDIR"/{commit-msg,common.sh} "$IT6/tools/git-hooks/" \
    && git -C "$IT6" config user.name t && git -C "$IT6" config user.email t@t \
    && git -C "$IT6" config core.commentchar ';' \
    || { echo "FAIL: commentchar 用例环境准备失败"; exit 1; }
printf '; comment line\nfeat: x\n' > "$IT6/msg"
(cd "$IT6" && bash "$IT6/tools/git-hooks/commit-msg" "$IT6/msg" >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: commentchar=';' 注释行应被剥离"; }
rm -rf "$IT6"
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
git -C "$IT3" config core.hooksPath "$IT3/.hooks" && mkdir -p "$IT3/.hooks" || { echo "FAIL: IT3 钩子隔离配置失败（会退回全局钩子产生非确定结果，r15 no139）"; exit 1; }
git -C "$IT3" config user.name t && git -C "$IT3" config user.email t@t || { echo "FAIL: IT3 git config 失败"; exit 1; }
git -C "$IT3" commit -q --allow-empty -m "feat: initial" || { echo "FAIL: 重同步用例 initial seed 失败"; exit 1; }
printf 'feat: x\nSigned-off-by: A <a@t>\n\t\x1e\nfeat: y\nSigned-off-by: A <a@t>\n' > "$IT3/forged.msg"
git -C "$IT3" commit -q --allow-empty --no-verify -F "$IT3/forged.msg" || { echo "FAIL: 重同步用例 forged seed 失败"; exit 1; }
EVIL=$(git -C "$IT3" rev-parse HEAD)
# 在 IT3 内执行：--ci 的 git log 按 cwd 解析仓，跨仓调用会读错仓 → fail-closed 恒 1、断言空转（r10 no b1e3）
(cd "$IT3" && bash "$HDIR/commit-msg" --ci "$EVIL~1" "$EVIL" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo "FAIL: 伪造终止符重同步应拒"; }
rm -rf "$IT3"
echo "selftest: $pass pass, $fail fail${skipped:+, $skipped skipped}"
exit $fail
