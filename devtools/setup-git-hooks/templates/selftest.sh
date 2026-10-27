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
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_CONFIG_NOSYSTEM=1
# 前提（r20 no226）：GLOBAL/SYSTEM 变量需 git ≥2.32；更旧版本会静默忽略、全局/系统
# 配置仍生效（NOSYSTEM 仅兜住系统级）。运行时探测（r26 no7）：设一个哨兵值，若
# include 链未按预期隔离则 git config 读不到——隔离失效即 fail-loud
env -u GIT_CONFIG_GLOBAL -u GIT_CONFIG_SYSTEM git config --global triage.sentinel "probe-$$" 2>/dev/null || true   # 写真实 ~/.gitconfig（解除上方 export 污染——CI 实证 /dev/null fatal）
if [ "$(GIT_CONFIG_GLOBAL=/dev/null git config --global triage.sentinel 2>/dev/null)" = "probe-$$" ]; then
    echo >&2 "FAIL: git config 全局隔离失效（旧版 git 忽略 GIT_CONFIG_GLOBAL？隔离后仍能读到真实全局值）——形态矩阵会有环境漂移，请升级 git"
    git config --global --unset triage.sentinel 2>/dev/null || true
    exit 1
fi
git config --global --unset triage.sentinel 2>/dev/null || true   # 清理哨兵
T=$(mktemp -d) || { echo >&2 "FAIL: mktemp -d 失败" >&2; exit 1; }
MSG=$(mktemp) || { echo >&2 "FAIL: mktemp 失败" >&2; exit 1; }
D=""   # 先初始化防 trap 引用未赋值（set -u）；IT/IT2/IT3/WT 同理由 :- 守护（r8 no8577/r9 no8523）
trap 'rm -rf "$T" "$MSG" "${D:-}" "${IT:-}" "${IT2:-}" "${IT3:-}" "${IT4:-}" "${IT5:-}" "${IT6:-}" "${IT7:-}" "${WT:-}"' EXIT   # IT4 同纳入（r15 no140）
cp commit-msg common.sh "$T/" || { echo >&2 "FAIL: 副本复制失败" >&2; exit 1; }

t() { # t <期望exit> <描述> <msg文件内容>
    local want="$1" desc="$2" msg="$3"
    printf '%s' "$msg" > "$MSG"
    bash "$T/commit-msg" "$MSG" >/dev/null 2>&1
    local got=$?
    if [ "$got" = "$want" ]; then pass=$((pass+1)); else
        fail=$((fail+1)); echo >&2 "FAIL: $desc (want=$want got=$got)" >&2; fi
}
# 钩子形态边界（矩阵在中性 cwd 执行，r22 no256·medium：commit-msg L1 会读
# core.commentchar——真实仓库本地 .git/config 仍会渗入；$T 非仓目录则只剩已屏蔽
# 的全局/系统级，回落默认 '#'。sed 取数改 HDIR 绝对路径）
cd "$T" || exit 1
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
sed 's/^COMMIT_PREFIX=""/COMMIT_PREFIX="[TW]"/' "$HDIR/commit-msg" > "$T/commit-msg"
grep -q '^COMMIT_PREFIX="\[TW\]"' "$T/commit-msg" || { echo >&2 "FAIL: 前缀 sed 未命中" >&2; exit 1; }
t 1 "缺前缀拦截"               $'feat(x): no\n'
t 0 "[TW]+conventional 通过"   $'[TW] feat(x): ok\n'
t 1 "前缀子串注入拦截"         $'xxx feat: add [TW]\n'
t 0 "前缀后多空格归一化"       $'[TW]  feat(x): ok\n'
t 0 "Revert 豁免优先于前缀"    $'Revert "[TW] feat(x): ok"\n'
# 还原对象是 $T 副本（其 COMMIT_PREFIX 已为 [TW]，r23 no273：读源文件是 no-op）
sed 's/^COMMIT_PREFIX="\[TW\]"/COMMIT_PREFIX=""/' "$T/commit-msg" > "$T/commit-msg.r" \
    && mv "$T/commit-msg.r" "$T/commit-msg"
grep -q '^COMMIT_PREFIX=""' "$T/commit-msg" || { echo >&2 "FAIL: 前缀还原 sed 未命中" >&2; exit 1; }
cd "$HDIR" || exit 1   # 矩阵结束回源目录（r22 no256）
# --ci 批量形态（临时仓，身份用本地假值即可——commit-msg 不校验作者）
D=$(mktemp -d)
git init -q "$D" || { echo >&2 "FAIL: git init" >&2; exit 1; }
cd "$D" || exit 1
git config user.name t && git config user.email t@t || { echo >&2 "FAIL: 环境 git config 失败" >&2; exit 1; }
mkdir -p .hooks && git config core.hooksPath "$D/.hooks" || { echo >&2 "FAIL: 钩子隔离配置失败" >&2; exit 1; }   # 隔离外部全局/系统级钩子
c() { git commit -q --allow-empty -m "$1" || { echo >&2 "FAIL: seed commit 失败: $1" >&2; exit 1; }; }
# 根提交占位：BAD~1 必须存在，否则 --ci BAD~1 走 fail-closed 恒 1，断言空转（r7 no14）
c "feat: initial"
c "seed bad"
BAD=$(git rev-parse HEAD)   # bad 定位后后续 seed 让范围可达
c "feat: good"
c "feat: seed3"
c "feat: seed4"
bash "$HOOK" --ci "$BAD~1" HEAD >/dev/null 2>&1   # bad~1..HEAD 含 bad（范围含左端点后第一条起）
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 范围报 bad" >&2; }
GOOD=$(git rev-list --all --grep="feat: good" -n1)   # 按 subject 定位，不依赖 commit 序数
[ -n "$GOOD" ] || { echo >&2 "FAIL: GOOD 定位失败（--grep 落空，后续断言无意义）" >&2; exit 1; }   # r8 no cb55
bash "$HOOK" --ci "$GOOD~1" "$GOOD" >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 合法 commit 应过" >&2; }
# --ci 空范围：r17 no168 起 CI 默认 fail-closed；人工调试合法空范围需显式豁免
bash "$HOOK" --ci HEAD HEAD >/dev/null 2>&1
[ $? != 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 空范围应默认拒绝（r17 no168）" >&2; }
COMMIT_CI_ALLOW_EMPTY=1 bash "$HOOK" --ci HEAD HEAD >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 空范围豁免后应放行" >&2; }
# Revert 反伪造（r20 no215·medium）：手写 Revert 主题无尾注 → 拒；真 git revert → 放行
git -C "$D" commit -q --allow-empty --no-verify -m 'Revert "feat: fake"' || { echo >&2 "FAIL: revert 伪造 seed 失败"; exit 1; }
FREV=$(git -C "$D" rev-parse HEAD)
bash "$HOOK" --ci "$FREV~1" "$FREV" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 应拒手写 Revert 主题（无尾注，r20 no215）"; }
# git revert 需真实变更（空提交 revert 失败）：先造一个带文件的提交再 revert；
# git revert 无 --no-verify 选项（r20 修正）
printf 'x\n' > "$D/revtmp" && git -C "$D" add revtmp \
    && git -C "$D" commit -q -m "feat: to-revert" \
    || { echo >&2 "FAIL: revert 前置 seed 失败"; exit 1; }
git -C "$D" revert --no-edit HEAD >/dev/null 2>&1 || { echo >&2 "FAIL: revert seed 失败"; exit 1; }
TREV=$(git -C "$D" rev-parse HEAD)
bash "$HOOK" --ci "$TREV~1" "$TREV" >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 应放行真 git revert 提交（r20 no215）"; }
# NUL 截断（r22 no255·security medium）：plumbing hash-object --literally 造含 NUL
# 的提交对象——git 判 bogus、读取命令 128 失败，validate_range 各环节 fail-closed
# bash printf 无法输出 NUL（C 字符串截断）——用 /dev/zero 补 1 字节 NUL
{ printf 'tree %s\nparent %s\nauthor t <t@t> 1700000000 +0800\ncommitter t <t@t> 1700000000 +0800\n\nfeat: nul' \
    "$(git -C "$D" rev-parse HEAD^{tree})" "$(git -C "$D" rev-parse HEAD)" \
    && head -c 1 /dev/zero && printf 'hidden\n'; } > "$T/nul-obj" \
    || { echo >&2 "FAIL: nul 对象构造失败（r26 no6：&& 链全部守卫）"; exit 1; }
[ "$(wc -c < "$T/nul-obj")" -gt 150 ] || { echo >&2 "FAIL: nul-obj 字节数异常（head -c 失败静默截断？r26 no6）"; exit 1; }
NULSHA=$(git -C "$D" hash-object -t commit --literally -w --stdin < "$T/nul-obj") || { echo >&2 "FAIL: nul 对象写入失败"; exit 1; }
bash "$HOOK" --ci "$(git -C "$D" rev-parse HEAD)" "$NULSHA" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 应拒含 NUL 的提交对象（bogus fail-closed，r22 no255）"; }
# Merge 反伪造（r18 no181·medium）：手写 "Merge branch 'x'" 主题的普通提交 → CI 拒绝
git -C "$D" commit -q --allow-empty --no-verify -m "Merge branch 'fake'" || { echo >&2 "FAIL: 反伪造用例 seed 失败" >&2; exit 1; }
FAKE=$(git -C "$D" rev-parse HEAD)
bash "$HOOK" --ci "$FAKE~1" "$FAKE" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 应拒手写 Merge 主题（反伪造）" >&2; }
# 真 merge commit（>=2 parent）→ 放行
git -C "$D" checkout -q -b mbranch HEAD~1 || { echo >&2 "FAIL: mbranch checkout 失败" >&2; exit 1; }
git -C "$D" commit -q --allow-empty -m "feat: mside" || { echo >&2 "FAIL: mside commit 失败" >&2; exit 1; }
git -C "$D" checkout -q - || { echo >&2 "FAIL: 回原分支失败（r19 no210：不再静默重定向）" >&2; exit 1; }
git -C "$D" merge -q --no-ff --no-edit mbranch >/dev/null 2>&1 || { echo >&2 "FAIL: 反伪造用例 merge seed 失败" >&2; exit 1; }
MERGE=$(git -C "$D" rev-parse HEAD)
# 环境断言（r19 no210·medium）：MERGE 必须真为 merge（2 parent），否则断言测的是 conventional 直通
[ "$(git -C "$D" rev-list --parents -n1 "$MERGE" | wc -w | tr -d "[:space:]")" = "3" ] || { echo >&2 "FAIL: MERGE 非 merge commit（环境假阳性防护）" >&2; exit 1; }   # tr 剥空白（BSD wc 前导空格，r21 no241）
bash "$HOOK" --ci "$MERGE~1" "$MERGE" >/dev/null 2>&1
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 应放行真 merge commit" >&2; }
# fail-closed：不可达范围
bash "$HOOK" --ci 0000000000000000000000000000000000000000 HEAD >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: fail-closed 不可达范围" >&2; }
# --ci 范围内含 0x1e 的 commit → fail-closed（用 printf 写 0x1e 进 commit message，
# -m "$'\x1e'" 双引号不展开；此前的字面文本 seed 无 0x1e，已删——误导性死代码 r7 no15）
git commit -q --allow-empty -m "feat: clean after bad" || { echo >&2 "FAIL: clean seed 失败" >&2; exit 1; }
LC_ALL=C git commit -q --allow-empty -m "$(printf 'feat: evil \x1e tail')" || { echo >&2 "FAIL: 0x1e commit 失败" >&2; exit 1; }
EVIL=$(git rev-parse HEAD)
bash "$HOOK" --ci "$EVIL~1" "$EVIL" >/dev/null 2>&1
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: --ci 应拒 0x1e 提交" >&2; }
# 颜色路径：非 TTY 管道下用 FORCE_COLOR 注入验证着色可达，NO_COLOR 优先压过（r7 no19）；
# 开色用例显式 NO_COLOR=（清空）——CI 环境若全局导出 NO_COLOR 会让断言假红（r8 no c819）
out=$(NO_COLOR= FORCE_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn x' _ "$T/common.sh" 2>&1)   # 传参形式防 TMPDIR 空格（r15 no142）
[[ "$out" == *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: FORCE_COLOR 未生效" >&2; }
out=$(NO_COLOR=1 FORCE_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn x' _ "$T/common.sh" 2>&1)
[[ "$out" != *$'\033['* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: NO_COLOR 未压过 FORCE_COLOR" >&2; }
out_w=$(bash -c 'source "$1"; log_warn w' _ "$T/common.sh" 2>/dev/null); out_e=$(bash -c 'source "$1"; log_warn w' _ "$T/common.sh" 2>&1 >/dev/null)
[[ -z "$out_w" && "$out_e" == *"[WARN]"* ]] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: log_warn 未走 stderr 或输出非 log_warn（r13 no108）" >&2; }
# UTF-8 locale 分支（r21 no232·medium）：CI 未设 LANG 恒走字节剥除分支，UTF-8
# 分支在门禁中零覆盖——LC_ALL=C.UTF-8 用例锁定两字节替换 + 多字节字符保留
out=$(LC_ALL=C.UTF-8 bash -c 'source "$1" 2>/dev/null; log_warn "$2"' _ "$T/common.sh" "$(printf 'x\xc2\x9b[31my\xe5\x8d\x81')" 2>&1)
# 期望恰为 "[WARN] x?[31my十"（C1 两字节 → '?'，"十" 原样保留）
case "$out" in *$'\xc2\x9b'*) fail=$((fail+1)); echo >&2 "FAIL: UTF-8 分支未替换 C1 CSI" ;; "[WARN] x?[31my$(printf '\xe5\x8d\x81')") pass=$((pass+1)) ;; *) fail=$((fail+1)); echo >&2 "FAIL: UTF-8 分支输出异常（多字节字符被误伤？）: $(printf '%s' "$out" | od -An -c | head -1)" ;; esac
# ESC 剥离（r14 no111）：消息内嵌 ANSI 序列时输出不得含原始 ESC，正文文本保留
# 非 UTF-8 locale 分支（r24 no274）：显式 LC_ALL=C 锁定裸 C1 字节剥除路径，
# 开发机默认 UTF-8 locale 时该分支无覆盖
out=$(LC_ALL=C LANG=C bash -c 'source "$1" 2>/dev/null; log_warn "$2"' _ "$T/common.sh" "$(printf 'x\x9b[31my')" 2>&1)
# 期望输出恰为 "x[31my"（0x9b 被剥、[31m 文本保留）——唯一通过形态（r26 no28：收紧死模式）
case "$out" in *$'\x9b'*) fail=$((fail+1)); echo >&2 "FAIL: 非 UTF-8 分支未剥裸 C1 字节" ;; "[WARN] x[31my") pass=$((pass+1)) ;; *) fail=$((fail+1)); echo >&2 "FAIL: 非 UTF-8 分支输出异常: $(printf '%s' "$out" | od -An -c | head -1)" ;; esac
# FORCE_COLOR 关断值边界（r21 no233）：0/off/FALSE 不开色
for v in 0 off FALSE; do
    out=$(FORCE_COLOR=$v bash -c 'source "$1" 2>/dev/null; log_warn x' _ "$T/common.sh" 2>&1)
    case "$out" in *$'\033'*) fail=$((fail+1)); echo >&2 "FAIL: FORCE_COLOR=$v 应不强制开色" ;; *) pass=$((pass+1)) ;; esac
done
out=$(NO_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn "$2"' _ "$T/common.sh" "$(printf 'x\033[31my')" 2>&1)   # 传参形式（r17 no173 同 no142）
case "$out" in *$'\033'*) fail=$((fail+1)); echo >&2 "FAIL: log_warn 未剥离 ESC" >&2 ;; *x\[31my*) pass=$((pass+1)) ;; *) fail=$((fail+1)); echo >&2 "FAIL: ESC 用例输出异常: $out" >&2 ;; esac   # [ 转义（r15 no141：未闭合 [ 按字面是冷门巧合语义）
# UTF-8 C1 定点剥除（r17 no158）：8 位 CSI/OSC 起始符不得透传
out=$(NO_COLOR=1 bash -c 'source "$1" 2>/dev/null; log_warn "$2"' _ "$T/common.sh" "$(printf 'x\xc2\x9b[31my\xc2\x9d')" 2>&1)
# locale 无关断言（CI LANG=C 走字节剥除分支，残留孤立 \xc2）：只要 CSI/OSC 起始符
# 不透传、正文 "[31m" 文本保留即可
case "$out" in *$'\xc2\x9b'*|*$'\xc2\x9d'*) fail=$((fail+1)); echo >&2 "FAIL: log_warn 未剥离 UTF-8 C1" ;; *"[31m"*) pass=$((pass+1)) ;; *) fail=$((fail+1)); echo >&2 "FAIL: C1 用例输出异常: $(printf '%s' "$out" | od -c | head -2)" ;; esac   # r19 CI 实测修正
# install.sh：hooksPath 写入断言（临时主仓 = 当前 clone 之外的测试 clone 语义）。
# cp 不接 2>/dev/null：环境准备失败必须显式暴露而非让断言假阳性（r7 no17）
IT=$(mktemp -d) && git init -q "$IT" && mkdir -p "$IT/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,commit-msg,pre-commit,pre-push,common.sh} "$IT/tools/git-hooks/" \
    || { echo >&2 "FAIL: install 测试环境准备失败" >&2; exit 1; }
(cd "$IT" && bash tools/git-hooks/install.sh >/dev/null 2>&1 && [ "$(git -C "$IT" config --get core.hooksPath)" = "tools/git-hooks" ])
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: install.sh hooksPath 写入" >&2; }
rm -rf "$IT"
# fail-open 分支（r9 no 4776）：旧分支无 tools/git-hooks 目录 → exit 0 且不写配置
IT=$(mktemp -d) && git init -q "$IT" || { echo >&2 "FAIL: fail-open 用例环境准备失败" >&2; exit 1; }
(cd "$IT" && bash "$HDIR/install.sh" >/dev/null 2>&1) \
    && [ -z "$(git -C "$IT" config --get core.hooksPath 2>/dev/null)" ] \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: fail-open 应 exit 0 且不写配置" >&2; }
rm -rf "$IT"
# 迁移清理分支：worktree 级 hooksPath 覆盖应被 install.sh 清除（r7 no7，本迁移核心逻辑）。
# 用 attached worktree（带 branch 行）——正是 r8 no30a9 暴露的、旧解析永不触发的形态
IT2=$(mktemp -d) && git init -q "$IT2" && mkdir -p "$IT2/tools/git-hooks" "$IT2/.hooks" \
    && cp "$HDIR"/{install.sh,commit-msg,common.sh} "$IT2/tools/git-hooks/" \
    || { echo >&2 "FAIL: 迁移用例环境准备失败" >&2; exit 1; }
git -C "$IT2" config core.hooksPath "$IT2/.hooks" || { echo >&2 "FAIL: IT2 钩子隔离配置失败（会退回全局钩子产生非确定结果）" >&2; exit 1; }   # 种子提交隔离外部钩子（r8 no4bbd，同 $D 段口径；r16 no154）
git -C "$IT2" -c user.name=t -c user.email=t@t commit -q --allow-empty -m "init" || { echo >&2 "FAIL: 迁移用例 seed 失败" >&2; exit 1; }
git -C "$IT2" config extensions.worktreeConfig true || { echo >&2 "FAIL: extensions.worktreeConfig 开启失败" >&2; exit 1; }
WT=$(mktemp -d)
git -C "$IT2" worktree add -q -b tmp-mig-wt "$WT" HEAD >/dev/null 2>&1 || { echo >&2 "FAIL: 迁移用例 worktree 创建失败" >&2; exit 1; }
STALE="$(git -C "$WT" rev-parse --absolute-git-dir)/hooks"   # 旧 install-hooks.sh 残留 = 自身 gitdir hooks（r23 no266/r26 no34 动态判定）
git -C "$WT" config --worktree core.hooksPath "$STALE" || { echo >&2 "FAIL: worktree 级 hooksPath 写入失败（断言会空转）" >&2; exit 1; }
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    || { fail=$((fail+1)); echo >&2 "FAIL: 迁移用例 install.sh 非零退出（r8 no34ab）" >&2; }
[ -z "$(git -C "$WT" config --worktree --get core.hooksPath 2>/dev/null)" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: install.sh 未清除 worktree 级 hooksPath" >&2; }
# 多值清理用例（r10 no cf09 → r12 no86 修订）：worktree 级同键双值在 --unset 下必败，
# 已改用 --unset-all——本用例验证多值也能清理成功（exit 0），不再走 fail-loud
# 注意首次 install 已把残留清空，需连加两个值才能构成多值场景
STALE="$(git -C "$WT" rev-parse --absolute-git-dir)/hooks"
git -C "$WT" config --worktree --add core.hooksPath "$STALE" \
    || { echo >&2 "FAIL: 多值 --add 1 失败（断言会空转）" >&2; exit 1; }
git -C "$WT" config --worktree --add core.hooksPath "$STALE" \
    || { echo >&2 "FAIL: 多值 --add 2 失败（断言会空转）" >&2; exit 1; }
[ "$(git -C "$WT" config --worktree --get-all core.hooksPath | grep -c .)" = "2" ] \
    || { echo >&2 "FAIL: 多值场景未构造成功（get-all 计数非 2）" >&2; exit 1; }   # 环境断言（r13 no107）；grep -c 而非 wc -l（BSD 前导空格填充，r15 no138）
(cd "$IT2" && bash tools/git-hooks/install.sh >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 多值清理应成功（--unset-all，r12 no86）" >&2; }
[ -z "$(git -C "$WT" config --worktree --get-all core.hooksPath 2>/dev/null)" ] \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 多值未清空" >&2; }
git -C "$WT" config --worktree --unset-all core.hooksPath 2>/dev/null || true
# 非残留形态（r26 no35）：保留原值但聚合计失败（exit 1）——钩子确实不生效，用户显式决策
git -C "$WT" config --worktree core.hooksPath "/my/custom/hooks" \
    || { echo >&2 "FAIL: 非残留形态写入失败"; exit 1; }
keep_out=$(cd "$IT2" && bash tools/git-hooks/install.sh 2>&1); keep_rc=$?
{ [ "$keep_rc" = "1" ] && [[ "$keep_out" == *"保留未清除"* ]] \
    && [ "$(git -C "$WT" config --worktree --get core.hooksPath)" = "/my/custom/hooks" ]; } \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 非残留形态应保留原值且 exit 1（r26 no35，rc=$keep_rc）"; }
git -C "$WT" config --worktree --unset-all core.hooksPath 2>/dev/null || true
# 主检残留形态（r24 no278/r26 no35）：absolute-git-dir/hooks（主检出 gitdir）也应被清
MAIN_HOOKS="$(git -C "$IT2" rev-parse --absolute-git-dir)/hooks"
git -C "$IT2" config --worktree core.hooksPath "$MAIN_HOOKS" \
    || { echo >&2 "FAIL: 主检残留形态写入失败"; exit 1; }
m_out=$(cd "$IT2" && bash tools/git-hooks/install.sh 2>&1); m_rc=$?
{ [ "$m_rc" = "0" ] && [[ "$m_out" == *"已清除"* ]] \
    && [ -z "$(git -C "$IT2" config --worktree --get core.hooksPath 2>/dev/null)" ]; } \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 主检残留形态应被清（r26 no35，rc=$m_rc）"; }
# 悬空 worktree：目录已删但元数据残留 → 跳过校验 + prune 提示，不置 mismatch（r11 no 75）
rm -rf "$WT"
mig_out=$(cd "$IT2" && bash tools/git-hooks/install.sh 2>&1); mig_rc=$?
{ [ "$mig_rc" = "0" ] && [[ "$mig_out" == *"worktree prune"* ]]; } \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 悬空 worktree 应跳过且输出 prune 提示（r18 no194，got rc=$mig_rc）" >&2; }
rm -rf "$IT2"
# pre-commit 零依赖冒烟（r11 no 72）：空仓上应干净通过（无 staged 文件、无 HEAD）
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
    || { echo >&2 "FAIL: pre-commit 冒烟环境准备失败" >&2; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-commit 空仓冒烟失败" >&2; }
# 失败路径（r13 no105）：未 gofmt 的 .go staged → gofmt 拦截 + fail 聚合 → exit 1
# （同时回归 set -e 与循环体交互、fail 聚合两处语义）
if command -v gofmt >/dev/null; then
    printf 'package x\nfunc  y() {}\n' > "$IT/bad.go"
    git -C "$IT" add bad.go || { echo >&2 "FAIL: git add 环境准备失败" >&2; exit 1; }
    (cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
    [ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-commit 应拦未 gofmt 文件" >&2; }
else
    echo >&2 "SKIP: gofmt 未安装，跳过 gofmt 拦截用例（r17 no174：SKIP 不阻塞无 Go 环境的 make selftest）"
    skipped=$((skipped+1))
fi
rm -rf "$IT"
# clang-format 拦截路径（r16 no166·medium）：未格式化 .c staged → 拦截 + "无法读取
# staged 内容"分支同链路（r16 no153/no165）
# symlink 跳过（r24 no282）：staged symlink 命名 *.go → 跳过格式检查不误拦
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
    || { echo >&2 "FAIL: symlink 用例环境准备失败"; exit 1; }
printf 'package x\n' > "$IT/real.go"
ln -s real.go "$IT/link.go"
git -C "$IT" add link.go || { echo >&2 "FAIL: symlink git add 失败"; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-commit 应跳过 symlink（r24 no282）"; }
rm -rf "$IT"
# 空白符检查分支（r18 no190/r26 no4·no45·no8-1a45a824）：用 ws.txt——*.md 已豁免、
# *.go 会先被 gofmt 拦（行尾空白属 gofmt 规范化范围），txt 才能独立触发空白检查
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
    || { echo >&2 "FAIL: 空白用例环境准备失败" >&2; exit 1; }
printf 'text line \n' > "$IT/ws.txt"
git -C "$IT" add ws.txt || { echo >&2 "FAIL: 空白用例 git add 失败" >&2; exit 1; }
(cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-commit 应拦行尾空白（r18 no190）" >&2; }
rm -rf "$IT"
if command -v clang-format >/dev/null; then
    IT=$(mktemp -d) && git init -q "$IT" \
        && cp "$HDIR"/{pre-commit,common.sh} "$IT/" \
        || { echo >&2 "FAIL: clang-format 用例环境准备失败" >&2; exit 1; }
    printf 'int main(){return 0;}\n' > "$IT/bad.c"
    git -C "$IT" add bad.c || { echo >&2 "FAIL: clang-format 用例 git add 失败" >&2; exit 1; }
    (cd "$IT" && bash "$IT/pre-commit" >/dev/null 2>&1)
    [ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-commit 应拦未 clang-format 文件" >&2; }
    rm -rf "$IT"
else
    echo >&2 "SKIP: clang-format 未安装，跳过 clang-format 拦截用例（r17 no174 同口径）"
    skipped=$((skipped+1))
fi
# pre-push 冒烟（r11 no91）：空仓 + </dev/null stdin——验证可解析执行、无 set -u 未绑定；
# 危险路径（worktree/make/网络）仅在非删除推送且有 go 时触发，空仓 stdin 空即跳过
IT=$(mktemp -d) && git init -q "$IT" \
    && cp "$HDIR"/{pre-push,common.sh} "$IT/" \
    || { echo >&2 "FAIL: pre-push 冒烟环境准备失败" >&2; exit 1; }
(cd "$IT" && bash "$IT/pre-push" </dev/null >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-push 空仓冒烟失败" >&2; }
# 回退分支（r13 no106）：env -u PATH -u HOME——path_fallback 与 gopath_prefix 归空边界
(cd "$IT" && env -u PATH -u HOME bash "$IT/pre-push" </dev/null >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: pre-push env -u PATH/HOME 冒烟失败" >&2; }
rm -rf "$IT"
# mismatch 聚合 → exit 1（r23 no267·medium）：环境级 GIT_CONFIG_COUNT 注入 hooksPath
# 覆盖——check_wt 实际生效值非 HOOKS_DIR，聚合后必须 exit 1（wt pre-start 依赖该信号）
IT7=$(mktemp -d) && git init -q "$IT7" && mkdir -p "$IT7/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,common.sh} "$IT7/tools/git-hooks/" \
    || { echo >&2 "FAIL: mismatch 用例环境准备失败"; exit 1; }
mig_out=$(cd "$IT7" && GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.hooksPath GIT_CONFIG_VALUE_0=/other bash tools/git-hooks/install.sh 2>&1); mig_rc=$?
{ [ "$mig_rc" = "1" ] && [[ "$mig_out" == *"hooksPath 校验未通过"* ]]; } \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 环境级覆盖应 mismatch 聚合 exit 1（r23 no267，got rc=$mig_rc）"; }
rm -rf "$IT7"
# 聚合失败 → 非零（r16 no148·medium）：损坏 config.worktree 使后续 git config 全部 fatal——
# 迁移分支被跳过、配置写入本身也 128 退出；可观测契约是“非零感知”，不锁定具体退出码
# （wt pre-start / make setup 只消费非零信号）
IT5=$(mktemp -d) && git init -q "$IT5" && mkdir -p "$IT5/tools/git-hooks" \
    && cp "$HDIR"/{install.sh,common.sh} "$IT5/tools/git-hooks/" \
    && git -C "$IT5" config user.name t && git -C "$IT5" config user.email t@t \
    || { echo >&2 "FAIL: 聚合失败用例环境准备失败" >&2; exit 1; }
git -C "$IT5" commit -q --allow-empty --no-verify -m "init" || { echo >&2 "FAIL: 聚合用例 seed 失败" >&2; exit 1; }
git -C "$IT5" config extensions.worktreeConfig true || { echo >&2 "FAIL: worktreeConfig 开启失败" >&2; exit 1; }
printf 'this is not valid git-config\x00rubbish\n' > "$IT5/.git/config.worktree"   # NUL 经 /dev/zero 无必要——\x00 字面量在 printf 中已生效（r26 no27：去多余 garbage 说明）
(cd "$IT5" && bash tools/git-hooks/install.sh >/dev/null 2>&1)
[ $? != 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 清理/写入失败应非零感知（r16 no148）" >&2; }
rm -rf "$IT5"
# wt.toml [pre-start] hooks 包装命令退出码契约（r13 no94）：
#   WT_NO_HOOKS=1 → exit 0（静默跳过）；旧分支无 install.sh → exit 0；install.sh 失败 → 非零传播
# 提取前提（r14 no120）：hooks 行为单行单值、无行尾注释；内层不含 TOML 转义（r14 no112
# 已重写 hooks 行避免 \"），提取后须含 install.sh 关键字方可作为有效命令串
# 整段依赖 wt.toml——缺失（vendor/独立部署）时整段 SKIP（r20 no225）
if [ -f "$HDIR/../../.config/wt.toml" ]; then
    hooks_lines=$(sed -n 's/^hooks = "//p' "$HDIR/../../.config/wt.toml" | grep -c .)   # grep -c 而非 wc -l（BSD 前导空格，r18 no191）
    [ "$hooks_lines" = "1" ] || { echo >&2 "FAIL: wt.toml 存在 $hooks_lines 行 hooks 键（提取契约定为单行，r17 no175）"; exit 1; }
    HOOKS_WRAP=$(sed -n 's/^hooks = "//p' "$HDIR/../../.config/wt.toml" | sed 's/"$//')
    [ -n "$HOOKS_WRAP" ] && case "$HOOKS_WRAP" in *install.sh*) ;; *) echo >&2 "FAIL: 提取的 hooks 包装命令非法: $HOOKS_WRAP"; exit 1 ;; esac \
        || { echo >&2 "FAIL: 未从 wt.toml 提取 hooks 包装命令"; exit 1; }
    IT=$(mktemp -d) && git init -q "$IT" && mkdir -p "$IT/tools/git-hooks" \
        && cp "$HDIR"/{install.sh,common.sh} "$IT/tools/git-hooks/" \
        || { echo >&2 "FAIL: wt 包装用例环境准备失败"; exit 1; }
    # 用例 1/2：WT_NO_HOOKS 静默 exit 0；正常安装 exit 0
    r=$(cd "$IT" && WT_NO_HOOKS=1 sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
    [ "$r" = "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: WT_NO_HOOKS 应静默 exit 0（got $r）"; }
    r=$(cd "$IT" && sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
    [ "$r" = "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 正常安装应 exit 0（got $r）"; }
    # WT_NO_HOOKS=0/false 不跳过（仅字面 1 禁用，r15 no124）
    r=$(cd "$IT" && git config --unset core.hooksPath 2>/dev/null; WT_NO_HOOKS=0 sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
    { [ "$r" = "0" ] && git -C "$IT" config --get core.hooksPath | grep -q tools/git-hooks; } \
        && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: WT_NO_HOOKS=0 应正常安装而非跳过"; }
    # 用例 3（r14 no119）：install.sh 失败 → 非零传播。chmod -x 无法模拟失败（包装命令是
    # bash 显式调用，不需要执行位）——用非法命令触发 bash 退出码 127
    printf 'fail-marker\n' > "$IT/tools/git-hooks/install.sh"
    r=$(cd "$IT" && sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
    [ "$r" != "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: install.sh 失败应非零传播（got $r）"; }
    # 用例 4（r14 no119）：旧分支无 install.sh → 包装层 exit 0
    rm -rf "$IT/tools/git-hooks"
    r=$(cd "$IT" && sh -c "$HOOKS_WRAP" >/dev/null 2>&1; echo $?)
    [ "$r" = "0" ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 无 hooks 目录应静默 exit 0（got $r）"; }
    rm -rf "$IT"
else
    echo >&2 "SKIP: .config/wt.toml 不存在（独立部署/vendor 场景），跳过 wt 包装契约用例（r19 no212/r20 no225）"
fi

# commentchar 路径（r16 no146）：core.commentchar=';' 时钩子按 ';' 剥注释行——
# 模板块首行为注释行应被剥离后正常校验，而非误拦"提交信息不能为空"
IT6=$(mktemp -d) && git init -q "$IT6" && mkdir -p "$IT6/tools/git-hooks" \
    && cp "$HDIR"/{commit-msg,common.sh} "$IT6/tools/git-hooks/" \
    && git -C "$IT6" config user.name t && git -C "$IT6" config user.email t@t \
    && git -C "$IT6" config core.commentchar ';' \
    || { echo >&2 "FAIL: commentchar 用例环境准备失败" >&2; exit 1; }
printf '; comment line\nfeat: x\n' > "$IT6/msg"
(cd "$IT6" && bash "$IT6/tools/git-hooks/commit-msg" "$IT6/msg" >/dev/null 2>&1) \
    && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: commentchar=';' 注释行应被剥离" >&2; }
rm -rf "$IT6"
# L1 0x1e 文件检查（r14 no123）：钩子模式的 grep 文件路径与 L2 --ci 的 %B 路径实现
# 独立，各补一条防同口径回归。消息文件含 0x1e → commit-msg（钩子形态）exit 1
IT4=$(mktemp -d) && git init -q "$IT4" && mkdir -p "$IT4/tools/git-hooks"     && cp "$HDIR"/{commit-msg,common.sh} "$IT4/tools/git-hooks/"     && git -C "$IT4" config user.name t && git -C "$IT4" config user.email t@t     || { echo >&2 "FAIL: L1 0x1e 用例环境准备失败" >&2; exit 1; }
printf 'feat: x\n\x1e\n' > "$IT4/msg"
printf 'feat: clean\n' > "$IT4/clean.msg"   # 阳性对照（r19 no211）：同环境干净消息应通过
(cd "$IT4" && bash "$IT4/tools/git-hooks/commit-msg" "$IT4/clean.msg" >/dev/null 2>&1)
[ $? = 0 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: L1 干净消息应通过（阳性对照，r19 no211）" >&2; }
(cd "$IT4" && bash "$IT4/tools/git-hooks/commit-msg" "$IT4/msg" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: L1 应拒含 0x1e 的消息文件" >&2; }
# L1 NUL（r23 no260，与 L2 同口径）——bash printf 无法输出 NUL，用 /dev/zero 拼接；
# 构造失败走 SKIP 并收纳断言（r26 no26/no44：防 SKIP 后断言空转假绿）
if { printf 'feat: x'; head -c 1 /dev/zero; printf 'hidden\n'; } > "$IT4/nulmsg" \
    && [ "$(wc -c < "$IT4/nulmsg")" -ge 15 ]; then   # 无 NUL 恰 14 字节，-ge 15 防护栏差一（r26 no5）
    (cd "$IT4" && bash "$IT4/tools/git-hooks/commit-msg" "$IT4/nulmsg" >/dev/null 2>&1)
    [ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: L1 应拒含 NUL 的消息文件（r23 no260）"; }
else
    echo >&2 "SKIP: 无法构造含 NUL 文件，跳过 L1 NUL 用例（r26 no5）"
    skipped=$((skipped+1))
fi
rm -rf "$IT4"
# 0x1e 拒绝回归（body 含独立 \t\x1e 行形态——涵盖伪造终止符攻击的输入特征；
# r11 重写后不再有记录协议，0x1e 一律 fail-closed，r12 no92 注释对齐）。
# 先 seed 一个普通提交：forged 提交不能是根提交，否则 EVIL~1 不存在、断言空转（r9 no aee5）
IT3=$(mktemp -d) && git init -q "$IT3" && mkdir -p "$IT3/tools/git-hooks" "$IT3/.hooks" \
    && cp "$HDIR"/{commit-msg,common.sh} "$IT3/tools/git-hooks/" \
    || { echo >&2 "FAIL: 重同步用例环境准备失败" >&2; exit 1; }
git -C "$IT3" config core.hooksPath "$IT3/.hooks" && mkdir -p "$IT3/.hooks" || { echo >&2 "FAIL: IT3 钩子隔离配置失败（会退回全局钩子产生非确定结果，r15 no139）" >&2; exit 1; }
git -C "$IT3" config user.name t && git -C "$IT3" config user.email t@t || { echo >&2 "FAIL: IT3 git config 失败" >&2; exit 1; }
git -C "$IT3" commit -q --allow-empty -m "feat: initial" || { echo >&2 "FAIL: 重同步用例 initial seed 失败" >&2; exit 1; }
printf 'feat: x\nSigned-off-by: A <a@t>\n\t\x1e\nfeat: y\nSigned-off-by: A <a@t>\n' > "$IT3/forged.msg"
git -C "$IT3" commit -q --allow-empty --no-verify -F "$IT3/forged.msg" || { echo >&2 "FAIL: 重同步用例 forged seed 失败" >&2; exit 1; }
EVIL=$(git -C "$IT3" rev-parse HEAD)
# 在 IT3 内执行：--ci 的 git log 按 cwd 解析仓，跨仓调用会读错仓 → fail-closed 恒 1、断言空转（r10 no b1e3）
(cd "$IT3" && bash "$HDIR/commit-msg" --ci "$EVIL~1" "$EVIL" >/dev/null 2>&1)
[ $? = 1 ] && pass=$((pass+1)) || { fail=$((fail+1)); echo >&2 "FAIL: 伪造终止符重同步应拒" >&2; }
rm -rf "$IT3"
echo "selftest: $pass pass, $fail fail${skipped:+, $skipped skipped}"
exit $fail
