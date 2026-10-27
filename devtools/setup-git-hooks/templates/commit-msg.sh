#!/bin/bash
# commit-msg — commit 格式校验（本地钩子 + CI 兜底共用同一实现）
#
# 三种调用形态（同一脚本 = L1 本地钩子与 L2 CI 兜底口径天然一致）：
#   git commit-msg 钩子:  commit-msg <msg文件路径>
#   CI 范围校验:          commit-msg --ci <base-sha> <tip-sha>
#   人工调试:             commit-msg <msg文件路径>（同钩子）
#
# 配置块是本规则的单一事实源。改规则先改这里——L1/L2 消费同一逻辑。

# ── 配置块（单一事实源）────────────────────────────────────────────
COMMIT_FORMAT="conventional"   # conventional | none
COMMIT_PREFIX=""               # 本仓非 fork，纯 conventional；fork 时填 "[TW]" 等
EXEMPT=(
    # 收紧为 git 自动生成形态（r12 no79）：手写 "Merge xxx"/"Revert xxx" 不再豁免。
    # git merge 模板固定为 branch/remote-tracking branch/pull request/commit/tag 开头；
    # git revert 固定为 Revert "<原 subject>"
    # git 模板恒为空格分隔；无空格变体是手写通道（r14 no113）；(es)?/(s)? 覆盖 octopus
    # 复数形态 "Merge branches 'a' and 'b'"/"Merge tags ..."（r15 no127；注意可选组
    # 是 (es)/(s) 而非 branches?——后者的 ? 落在词尾 s 上，单数 branch 反而不匹配）
    "^Merge (branch(es)? |remote-tracking branch(es)? |pull request |commit(s)? |tag(s)? )"
    "^Revert \""   # 豁免仅判 subject（first_line）；若按全文匹配，正文任意 "Revert ..." 行都会劫持豁免（正文绕过实证）
    "^fixup!" "^squash!" "^amend!"  # git 交互式 rebase 自动生成
)
BODY_EXEMPT=(
    # 正文级豁免（fork 场景）：cherry-pick -x 尾注在正文，subject 无特征。
    # 本仓非 fork 留空；fork 仓填 "^\(cherry picked from commit "
)
# ─────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"   # cd+pwd -P 可移植（readlink -f 旧 macOS 缺失，r12 no81/r23 no271）；不解析 $0 符号链接——install.sh 以 hooksPath 直指仓内目录
source "$SCRIPT_DIR/common.sh" || { echo "无法加载 common.sh" >&2; exit 1; }

# 配置块自检：拼错会静默 fail-open（跳过全部格式校验），与"单一事实源"定位不符（r9 no e3d5）
case "$COMMIT_FORMAT" in conventional|none) ;; *) echo "错误: COMMIT_FORMAT 配置非法: $COMMIT_FORMAT" >&2; exit 1 ;; esac

validate_one() {
    local first_line="$1" full_msg="${2:-$1}"

    if [ -z "$first_line" ]; then
        log_error "提交信息不能为空。"
        return 1
    fi

    # 重复 Signed-off-by 查重先于豁免：豁免免的是格式约束，不免全仓查重规则
    # （"Merge branch x" 标题藏重复 signoff 不应放过）。
    # 宽松匹配：键名大小写不敏感（grep -i 命中 + sed 改写为小写字面键）+ 折叠多空格——
    # "Signed-off-by:  A" 与 "signed-off-by: A" 判重；签署人值大小写敏感（r12 no82 刻意取舍，
    # r19 no197 措辞对齐实现：并非"统一小写"）
    # POSIX 可移植：\+ 是 GNU BRE 扩展（BSD 按字面 +，r12 no82）；不整行小写——仅大小写
    # 不同的两个不同签署人会被误判重复（r12 no82）；判重本身对大小写敏感是刻意取舍
    if [ -n "$(printf '%s\n' "$full_msg" | grep -iE '^signed-off-by[[:space:]]*:' | tr -d '\r' | sed 's/^[^:]*:[[:space:]]*/signed-off-by: /;s/[[:space:]][[:space:]]*/ /g;s/[[:space:]]*$//' | sort | uniq -d)" ]; then
        log_error "存在重复的 Signed-off-by 行。"
        return 1
    fi

    # 豁免规则：git 自动生成的提交特征在 subject；cherry-pick 尾注在正文。
    # subject 级豁免只判 first_line（全文匹配会被正文任意 "Merge ..." 行劫持），
    # 正文级豁免（BODY_EXEMPT）独立列表，仅 fork 场景非空
    local pattern
    for pattern in ${EXEMPT[@]+"${EXEMPT[@]}"}; do
        if printf '%s\n' "$first_line" | grep -qE "$pattern"; then
            return 0
        fi
    done
    # ${#BODY_EXEMPT[@]} 判空而非 ${arr[@]:+}——bash<4.4（macOS 3.2）下空数组展开
    # 会报 unbound variable（r14 no116，同 EXEMPT 守卫不同写法的历史原因）
    if [ "${#BODY_EXEMPT[@]}" -gt 0 ]; then
        for pattern in ${BODY_EXEMPT[@]+"${BODY_EXEMPT[@]}"}; do
            if printf '%s\n' "$full_msg" | grep -qE "$pattern"; then
                return 0
            fi
        done
    fi

    # 内部原创 commit 前缀（fork 仓的隔离标记，上游同步时 grep '^\[ORG\]' 可列出全部内部修改）。
    # 行首锚定：case 的 pattern 中变量按字面匹配（[TW] 不作 glob 展开），
    # 剥离用同源字面展开 ${var#\$PREFIX}——不用 grep -qF（全文子串，"xxx feat: add [TW]" 会误命中）
    local check_line="$first_line"
    if [ -n "$COMMIT_PREFIX" ]; then
        case "$first_line" in
            "$COMMIT_PREFIX"*)
                check_line="${first_line#"$COMMIT_PREFIX"}"
                check_line="${check_line#"${check_line%%[! ]*}"}"   # 归一化：去 prefix 后全部前导空格
                ;;
            *)
                log_error "内部原创 commit 必须带 $COMMIT_PREFIX 前缀："
                log_error "  $COMMIT_PREFIX <type>(scope): <description>"
                # ${arr[@]:+} 在 bash<4.4 空数组下 unbound（r16 no145，同 r14 no116）
                local body_exempt_note=""
                [ "${#BODY_EXEMPT[@]}" -gt 0 ] && body_exempt_note="、上游 cherry-pick（-x）"
                log_error "  豁免：merge/revert/fixup! 等自动生成提交$body_exempt_note"
                return 1
                ;;
        esac
    fi

    if [ "$COMMIT_FORMAT" = "conventional" ]; then
        if ! printf '%s\n' "$check_line" | grep -qE '^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-zA-Z0-9/_,-]+\))?!?: [^[:space:]].*'; then
            log_error "提交信息不符合 Conventional Commits 格式："
            log_error "  <type>(optional scope)(optional !): <description>"
            log_error "  例如: feat(hgml): add MIG placement API"
            log_error "  type 可选: build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test"
            return 1
        fi
    fi
    return 0
}

empty_range=0   # 全局标记：validate_range 返回后调用方读取，local 会在 return 后失效（r13 no95）
validate_range() {
    local base="$1" tip="$2" bad=0
    # 两段式取数：rev-list 拿 sha（无歧义），逐 commit 取 %B——
    # 0x1e 单遍记录协议已被两轮绕过（no59e3 伪 40-hex 头、no67 伪造终结+重同步），
    # 消息体可含任意字节时任何行内分隔符都不可信，故彻底放弃行解析（r11 no67）
    local shas
    # 形态预检（r17 no169）：- 开头的值会被 git 当选项解析（如 --all 改变范围语义）
    case "$base" in -*) log_error "base 不可用选项形态: $base"; return 1 ;; esac
    case "$tip" in -*) log_error "tip 不可用选项形态: $tip"; return 1 ;; esac
    # 存在性预检（r15 no131）：先校验两端可解析，给精确错误并消除 crafted 值歧义
    git rev-parse --verify --quiet "$base^{commit}" >/dev/null || { log_error "base 不可解析为提交: $base"; return 1; }
    git rev-parse --verify --quiet "$tip^{commit}" >/dev/null || { log_error "tip 不可解析为提交: $tip"; return 1; }
    shas=$(git rev-list "$base..$tip") \
        || { log_error "无法解析范围 $base..$tip——浅克隆需 fetch-depth: 0，具体原因见上方 git 报错"; return 1; }
    # 空范围（r17 no168·medium）：CI 接线的 diff-base..HEAD 在正常 MR 下必非空，空即
    # base 误配，默认 fail-closed（exit 1）；人工调试的合法空范围（tip 已含于 base，
    # 如 rebase 后旧 diff-base）用 COMMIT_CI_ALLOW_EMPTY=1 显式豁免
    if [ -z "$shas" ]; then
        empty_range=1
        if [ "${COMMIT_CI_ALLOW_EMPTY:-0}" = "1" ]; then
            log_warn "EMPTY_RANGE: 范围 $base..$tip 为空（0 个提交被校验）——COMMIT_CI_ALLOW_EMPTY=1 已豁免"
            return 0
        fi
        log_error "EMPTY_RANGE: 范围 $base..$tip 为空（0 个提交被校验，兜底未生效）——确认 base/tip 是否错配（正常 MR 非空）；人工调试合法空范围请设 COMMIT_CI_ALLOW_EMPTY=1"
        return 1
    fi

    local sha body first_line parents shallow   # parents/shallow 补声明（r26 no23）
    # 规模护栏：范围错配到很远的历史时逐提交校验线性变慢，WARN 提示（r12 no84）
    [ "$(printf '%s\n' "$shas" | wc -l)" -gt 200 ] && log_warn "范围 $base..$tip 提交数超过 200——确认 base 是否错配（校验耗时会线性增长）"
    while IFS= read -r sha; do
        # NUL 截断（r22 no255·security medium，selftest 实证）：含 NUL 的对象
        # rev-parse/rev-list/log 全部正常工作且 log 自身按 NUL 截断——必须读原始
        # cat-file 内容检测；命令替换静默丢 \0，NUL 之后的字节逃过 0x1e/查重/格式
        # 全部校验，且 L1（grep 原文件）能看到，破坏同口径
        git cat-file commit "$sha" > "$msg_tmp" 2>/dev/null \
            || { log_error "commit ${sha:0:8}: 无法读取提交对象"; bad=1; continue; }
        local raw_len nonul_len   # 不泄漏全局（r23 no264）
        raw_len=$(wc -c < "$msg_tmp" | tr -d "[:space:]")
        nonul_len=$(LC_ALL=C tr -d '\000' < "$msg_tmp" | wc -c | tr -d "[:space:]")
        if [ "$raw_len" != "$nonul_len" ]; then
            log_error "commit ${sha:0:8} 提交对象包含 NUL 字节（命令替换会截断校验范围）"
            bad=1
            continue
        fi
        # 头部（git 生成，不含 NUL）后首个空行起为消息体
        body=$(sed '1,/^$/d' "$msg_tmp")
        # 消息含 0x1e 一律拒绝（L1 钩子同口径；攻击者可借此伪造分隔符）
        if [[ "$body" == *$'\x1e'* ]]; then
            log_error "commit ${sha:0:8} 提交信息包含非法控制字符 0x1e"
            bad=1
            continue
        fi
        # sed -n 取首行（SIGPIPE 防护 r12 no83）；剥前导空行同钩子口径（r13 no97）
        first_line=$(printf '%s\n' "$body" | sed '/./,$!d' | sed -n '1{s/[[:space:]]*$//p;}')
        # Merge 豁免反伪造（r17 no170，r18 no182 改用已算的 first_line 省一次子进程）：
        # 真 merge commit 恒有 >=2 parent；手写 "Merge branch 'x'" subject 的普通提交
        # 在此被拒（L2 有 sha 可查，L1 维持 subject 口径）。形态列表须与 EXEMPT 的
        # branch(es)/tag(s)/commit(s) 对齐（r18 no180）
        case "$first_line" in
            "Merge branch "*|"Merge branches "*|"Merge tag "*|"Merge tags "*|"Merge commit "*|"Merge commits "*|"Merge remote-tracking "*|"Merge pull request "*)
                # 显式设防（r18 no179·medium）：|| 列表左支内 set -e 被禁用，赋值失败会
                # 使 -lt 比较报错短路、反伪造被静默跳过——fail-closed 须手动拦截
                if ! parents=$(git rev-list --parents -n1 "$sha" | wc -w) || [ -z "$parents" ] || ! [ "$parents" -eq "$parents" ] 2>/dev/null; then
                    log_error "commit ${sha:0:8}: 无法确定 parent 数（浅克隆截断/仓库损坏？）——merge 主题提交需完整 parent 信息"
                    bad=1
                    continue
                fi
                if [ "$parents" -lt 3 ]; then
                    # 浅克隆 graft 裁剪会让真 merge 也只报 1 parent（r18 no183）：诊断区分
                    # is-shallow-repository 需 git ≥2.15，旧版报错兜底为非浅克隆（r23 no265）
                    shallow=$(git rev-parse --is-shallow-repository 2>/dev/null || echo false)
                    if [ "$shallow" = "true" ]; then
                        log_error "commit ${sha:0:8} 为浅克隆截断的 merge commit（parent 信息不全）——请 fetch-depth: 0 后重试"
                    else
                        log_error "commit ${sha:0:8} 手写 Merge 主题但非 merge commit（parent 数 $((parents-1))）——请改写为 conventional 格式"
                    fi
                    bad=1
                fi
                ;;
            "Revert \""*)
                # Revert 反伪造（r19 no196·medium，与 Merge 反伪造对称）：git revert 模板
                # 恒含 "This reverts commit <40-hex>." 尾注——缺失即手写伪造
                # [.,] 兼容普通 revert（句点）与 merge revert（", reversing" 续行，r26 no20·high 实测）
                if ! printf '%s\n' "$body" | grep -qE '^This reverts commit [0-9a-f]{40,64}[.,]'; then
                    log_error "commit ${sha:0:8} 手写 Revert 主题但正文无 'This reverts commit <sha>.' 尾注——请改写为 conventional 格式或用 git revert 生成"
                    bad=1
                fi
                ;;
        esac
        # 只去尾随空白：不裁前导空白——" Merge branch x"/" feat: x" 前置空格
        # 属格式违规，与 CI 拒绝口径一致（r7 no11）。[[:space:]] 含 \r（r10 no c4be）
        # first_line 已在 0x1e 检查后统一计算（r18 no182：反伪造与格式校验共用）
        if ! validate_one "$first_line" "$body"; then
            log_error "  ↳ commit ${sha:0:8}: $(printf '%s' "$first_line" | tr -d '\000-\013\016-\037')"
            bad=1
        fi
    done <<< "$shas"
    return "$bad"
}

case "${1:-}" in
    --ci)
        [ $# -eq 3 ] || { log_error "用法: commit-msg --ci <base-sha> <tip-sha>"; exit 1; }
        # 消息落临时文件：NUL 检测需字节级读取，命令替换会静默丢弃 \0（r22 no255）
        msg_tmp=$(mktemp) || { log_error "无法创建临时文件"; exit 1; }
        trap 'rm -f "$msg_tmp"' EXIT
        trap 'rm -f "$msg_tmp"; exit 129' HUP
        trap 'rm -f "$msg_tmp"; exit 130' INT
        trap 'rm -f "$msg_tmp"; exit 143' TERM   # 128+N 惯例（r26 no24/no32）   # 信号清理（r23 no262）
        validate_range "$2" "$3" || exit 1
        [ "${empty_range:-0}" = 1 ] || log_info "CI commit 检查通过。"   # 空范围不报"通过"（r12 no78：WARN 与通过矛盾）
        ;;
    *)
        [ -f "${1:-}" ] || { log_error "未提供提交信息文件"; exit 1; }
        # 已知 L1/L2 口径边界（r23 no261）：手写 Merge/Revert 主题在 L1 按 subject 豁免
        # 放行（本地无 sha/尾注可查反伪造）——L2 会拒，本地过 push 后 CI 红属预期
        # commentchar 跟随 core.commentchar 配置（r12 no80；auto 模式取 #）
        comment_char=$(git config core.commentchar || echo '#')
        [ "$comment_char" = "auto" ] && comment_char='#'
        # / 会破坏 sed 地址定界符（转义后仍歧义），显式拒绝而非晦涩报错（r14 no114）
        [ "$comment_char" = "/" ] && { echo "错误: 不支持的 core.commentchar 值: /（请改用其他注释符）" >&2; exit 1; }
        esc_cc=$(printf '%s' "$comment_char" | sed 's/[][\.^$*]/\\&/g')   # 元字符转义再进 BRE（r13 no99）
        # 先截断 scissors（r23 no259/r24 no276·medium）：git commit -v 在
        # "# -------- >8 --------"（wt-status cut_line，两侧各 24 个 -）后附 diff——
        # 截断必须先于注释剥离（分隔线以注释符开头，先 d 会删掉它使范围地址失效）；
        # 通配 --* 兼容任意线长。截断后 0x1e/NUL/查重只作用于真实消息区域（r24 no277）
        hook_tmp=$(mktemp) || { log_error "无法创建临时文件"; exit 1; }
        trap 'rm -f "$hook_tmp"' EXIT
        trap 'rm -f "$hook_tmp"; exit 129' HUP
        trap 'rm -f "$hook_tmp"; exit 130' INT
        trap 'rm -f "$hook_tmp"; exit 143' TERM
        sed -e "/^$esc_cc --* >8 --*/,\$d" "$1" > "$hook_tmp"
        # L1 与 L2 同源：本地钩子也拒 0x1e / NUL（消息文件即将入库，可预检；
        # NUL 同 L2 r22 no255 口径：sed 会丢弃它，其后内容对校验不可见）
        if grep -q $'\x1e' "$hook_tmp"; then
            log_error "提交信息包含非法控制字符 0x1e（与 CI 校验协议冲突）"
            exit 1
        fi
        raw_len=$(wc -c < "$hook_tmp" | tr -d "[:space:]")
        nonul_len=$(LC_ALL=C tr -d '\000' < "$hook_tmp" | wc -c | tr -d "[:space:]")
        if [ "$raw_len" != "$nonul_len" ]; then
            log_error "提交信息包含 NUL 字节（与 CI 校验协议冲突）"
            exit 1
        fi
        # 不裁前导空白（r7 no11，同 --ci 口径）。commentchar 解析在 scissors 截断前已完成
        # （r26 no22/no30：单次解析复用 esc_cc，防两段口径分叉）——此处仅剥注释行。
        msg_clean=$(sed "/^$esc_cc/d" "$hook_tmp" | sed '/./,$!d')
        # 已知 L1/L2 边界（r14 no115）：-m/-F 提交的默认 cleanup=whitespace 不剥注释行，
        # `#` 开头的 subject 会入库；此处按 strip 模拟会误删该行——多行 -m 时本地放行、
        # CI 按 %B 原文拒绝（fail-closed 方向）。按 commit.cleanup 区分属后续增强
        first_line=$(printf '%s\n' "$msg_clean" | sed -n '1{s/[[:space:]]*$//p;}')   # 同上，避 SIGPIPE（r12 no83）
        validate_one "$first_line" "$msg_clean" || exit 1
        log_info "提交信息格式正确。"
        ;;
esac
