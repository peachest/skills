#!/usr/bin/env bash
# install.sh — 一次性安装：core.hooksPath 指向本目录。
# hook 内容随分支文件走（旧分支没有本目录时 hook 自动不生效，fail-open），
# 配置写 clone 级共享配置——配一次，主检出与全部 worktree 同时生效。
# 撤销：git config --unset core.hooksPath
# 信任模型（r15 no134）：hook 内容随检出分支变化——检出不受信分支（外部 PR/fork）后
# 其自带钩子会在下次 commit/push 自动执行。WT_NO_HOOKS=1 仅为安装开关（含本脚本、
# wt pre-start、make setup 透传），不影响已写入的 core.hooksPath——停用已装钩子需
# git config --unset core.hooksPath；单次跳过校验用 --no-verify（r17 no161）。
# 详见 README "Git hooks" 一节
# 最低 git 版本（r16 no149）：相对 core.hooksPath 按各 worktree 根解析是本方案前提，
# 以 CI 镜像 git 版本为实测基线；--porcelain 逐块解析在更旧版本上行为未定义
set -euo pipefail

# kill-switch（r16 no150）：与 wt pre-start 同口径（仅字面 1），三条安装路径语义统一
[ "${WT_NO_HOOKS:-}" = "1" ] && { echo "提示: WT_NO_HOOKS=1，跳过钩子安装" >&2; exit 0; }

root="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "错误: 当前目录不在 git 工作树内（bare 仓/无工作树），钩子安装不适用" >&2; exit 1; }   # 可读诊断替代 git 原生 fatal（r17 no162）
cd "$root"

HOOKS_DIR="tools/git-hooks"   # 必须相对路径：core.hooksPath 相对值按各 worktree 根解析，
                               # 这是"hook 内容随分支走、旧分支 fail-open"的前提；改绝对路径会全 worktree 共享一份
# 不变式固化（r9 no e9dd）：绝对路径会静默改变语义（全 worktree 共享一份、旧分支 fail-open 失效）
case "$HOOKS_DIR" in /*) echo "错误: HOOKS_DIR 必须为相对路径（见上方注释），得到: $HOOKS_DIR" >&2; exit 1 ;; esac

# 目录缺失在旧分支是 fail-open 设计内场景（exit 0 + 提示）；
# 真实错误（hooksPath 写失败）才 exit 1
[ -d "$HOOKS_DIR" ] || { echo "提示: $HOOKS_DIR 不存在（旧分支无钩子目录属预期），跳过安装" >&2; exit 0; }

# 先授权钩子文件再写任何配置：chmod 失败不改动 hooksPath（r15 no133）。已知部分
# 原子性边界（r17 no163）：迁移清理先于 clone 级写入执行，后者失败时已清除的
# worktree 级值仅能按 stdout 记录手工恢复（清理提示带原值，可接受）

# 否则 chmod 失败后配置已落盘，git 会静默跳过无执行位的钩子（检查反而被关闭），
# 且提前退出会短路末尾的聚合诊断报告。保留 chmod 错误输出便于诊断（只读挂载/EACCES）
# 遍历目录（钩子目录即事实源，新增钩子自动纳入）；仅排除 *.sh/*.md。
# 不变式（r21 no231 措辞对齐）：目录内应只放钩子与 *.sh/*.md 辅助文件——其他
# 无扩展名文件也会被 chmod +x（git 按精确文件名识别钩子，无扩展名是钩子约定）
for hook in "$HOOKS_DIR"/*; do
    [ -f "$hook" ] || continue   # 跳过子目录（glob 字面量已被上方 -d 拦，防御空目录场景）
    case "${hook##*/}" in
        *.sh|*.md) continue ;;   # *.sh 辅助脚本；*.md 文档（r9 no 6b3a：文档不应被 chmod +x）
    esac
    chmod +x "$hook" || { echo "错误: chmod +x $hook 失败，钩子不会生效" >&2; exit 1; }   # 真实错误 exit 1（r13 no103）
    [ -x "$hook" ] || { echo "错误: $hook 不可执行，该钩子不会生效" >&2; exit 1; }
done

if old="$(git config --show-origin --get core.hooksPath 2>/dev/null)"; then
    origin="${old%%$'\t'*}"; old="${old#*$'\t'}"
    if [ "$old" != "$HOOKS_DIR" ]; then
        # worktree 级来源将被下方迁移清理而非覆盖（r12 no87 口径区分）
        case "$origin" in
            *config.worktree*) echo "注意: 发现 worktree 级 core.hooksPath（来自 ${origin#file:}）: $old——将随迁移清理" >&2 ;;
            *)                 echo "注意: 覆盖已有 core.hooksPath（来自 ${origin#file:}）: $old -> $HOOKS_DIR" >&2 ;;
        esac
    fi
fi
# porcelain 每块以空行结尾；先落盘再循环：进程替换的退出码不传播，pipefail 下 git 失败
# 会静默空循环（r9 no 9e3e）。清理与校验两个循环共用同一快照。快照边界（r23 no270）：
# 快照后并发增删的 worktree 不在处理范围——新增 worktree 读共享配置天然生效、
# 悬空场景有警告兜底、幂等重跑可收敛；clean_wt 探测与 unset 间亦有 TOCTOU 窗口
wts=$(git worktree list --porcelain) || { echo "错误: git worktree list 失败" >&2; exit 1; }

# porcelain 共享解析：attached 块以 branch 行收尾，detached 块以 detached 行收尾，空行即块界。
# 块边界处理而非行特征触发（r8 no30a9）；末块 flush 非边角而是主路径（r11 no74）。
# 清理与校验两循环共用，防解析口径分叉（r12 no89）。回调返回非零不中断遍历，
# 由调用方聚合（CALLBACK_FAILED）；进程替换退出码不传播，故先落盘 wts（r9 no 9e3e）
CALLBACK_FAILED=0
each_wt() {  # $1 = 回调函数名（接受 worktree 路径参数）
    local wt_dir="" line
    while IFS= read -r line; do
        case "$line" in
            worktree\ *) wt_dir="${line#worktree }" ;;
            bare)        wt_dir="" ;;
            "")          [ -n "$wt_dir" ] && { "$1" "$wt_dir" || CALLBACK_FAILED=1; }; wt_dir="" ;;
        esac
    done <<< "$wts"
    if [ -n "$wt_dir" ]; then "$1" "$wt_dir" || CALLBACK_FAILED=1; fi
    return 0   # 显式 0：&& 短路状态不得成为函数返回值（set -e 会吞掉聚合，r14 no118）
}

# 迁移清理：旧 install-hooks.sh 是单 worktree 作用域——每个跑过旧脚本的
# worktree 都写了各自的 worktree 级 hooksPath（指向已悬空的 gitdir hooks），
# 优先级高于 clone 级配置。遍历全部 worktree 统一清理
if [ "$(git config --bool extensions.worktreeConfig 2>/dev/null)" = "true" ]; then
    clean_wt() {  # $1 = worktree 路径：旧 install-hooks.sh 残留则清除
        local old_val
        if old_val=$(git -C "$1" config --worktree --get core.hooksPath 2>/dev/null); then   # 单次调用探测+取值（r15 no135：消竞态）
            # 收窄清理范围（r23 no266·medium）：仅清旧脚本残留形态（gitdir hooks 路径）。
            # pre-start 使本脚本每次建仓都跑——"一律清除"会让用户自意的 worktree 级
            # 配置无感知丢失（恢复线索只在触发者终端）。非残留形态仅警告跳过
            case "$old_val" in
                */.git/worktrees/*/hooks|*/.git/worktrees/*/hooks/)
                    if git -C "$1" config --worktree --unset-all core.hooksPath; then
                        echo "✓ 已清除 $1 的旧 worktree 级 hooksPath（原值: $old_val）" >&2   # 原值可恢复线索，走 stderr（r22 no247）
                    else
                        echo "警告: $1 清理失败" >&2
                        return 1   # 显式失败：否则赋值 return 0，each_wt 聚合永远不触发（r13 no102·high）
                    fi
                    ;;
                *)
                    echo "警告: $1 存在非迁移残留的 worktree 级 hooksPath（原值: $old_val）——保留不动；如需统一请手动 unset" >&2
                    ;;
            esac
        fi
    }
    each_wt clean_wt
    clean_fail=$CALLBACK_FAILED   # 共享遍历器的失败聚合（r12 no89）；未进本分支时由 ${clean_fail:-0} 兜底（r23 no268）
    CALLBACK_FAILED=0
fi

git config --replace-all core.hooksPath "$HOOKS_DIR" || { echo "错误: core.hooksPath 写入失败（配置只读/损坏/并发锁？）" >&2; exit 1; }   # --replace-all 消除存量多值失败模式（r21 no230），键不存在时等同普通写入
# 写入后校验各 worktree 的实际生效值（worktree 级优先于 clone 级）：
# 清理失败或存量覆盖（extensions.worktreeConfig 未启用而 worktree config 已有值）都会让
# clone 级写入对个别 worktree 无效——逐仓校验并显式暴露，不做静默降级（r8 no8548）。
# porcelain 每块以空行结尾——空行即块主路径，末块 flush 并非边角兼容（r11 no74）
check_wt() {  # $1 = worktree 路径：校验实际生效值（悬空跳过并提示，r10 no e1a4）
    if [ ! -d "$1" ]; then
        echo "警告: $1 已不存在（悬空 worktree 元数据），跳过校验，建议 git worktree prune" >&2
        return 0
    fi
    # 显式容错（r22 no245·medium）：git 失败时按 mismatch 聚合而非依赖
    # "恒经 each_wt 调用所以 errexit 被抑制"的隐式前提
    if ! actual="$(git -C "$1" config core.hooksPath 2>/dev/null)"; then
        echo "警告: $1 的 hooksPath 读取失败（元数据损坏？）" >&2
        return 1
    fi
    while [ "${actual%/}" != "$actual" ]; do actual="${actual%/}"; done   # 剥全部尾斜杠（r22 no248/r23 no269：tools/git-hooks// 等语义等价不误报）
    if [ "$actual" != "$HOOKS_DIR" ]; then
        # 打印实际生效值（r19 no202）：mismatch 成因多样（worktree 级残留/local include/
        # 环境级 GIT_CONFIG_* 覆盖/尾部斜杠差异），实测值帮助定位
        echo "警告: $1 的 hooksPath 校验未通过（实际生效值: ${actual:-<空>}，期望 $HOOKS_DIR——常见为 worktree 级覆盖残留），该 worktree 钩子不生效" >&2
        return 1
    fi
}
each_wt check_wt   # wt_mismatch 直取聚合值（原 0 初始化为死赋值，r17 no164）
wt_mismatch=$CALLBACK_FAILED   # 共享遍历器的失败聚合（r12 no89）
CALLBACK_FAILED=0
# 按行解析无法表示含换行的路径（git ≥2.36 才有 --porcelain -z）：此类极端路径不受支持（已文档化）

# 清理失败/校验不匹配 = 真实错误（与头部边界声明一致：仅目录缺失属 fail-open），exit 1
# 让 wt pre-start / Makefile setup 调用方能感知（r9 no 3627/5b6d）
if [ "${clean_fail:-0}" = 1 ] || [ "${wt_mismatch:-0}" = 1 ]; then
    echo "错误: 存在 worktree 级 hooksPath 覆盖未被清除，或实际生效值仍非 $HOOKS_DIR（成因：worktree 级残留 / 环境级 GIT_CONFIG_* 覆盖 / local include 链 / 值格式差异，见上方各 worktree 校验警告的实际值）——worktree 级残留请修复权限后重跑本脚本（幂等）或手动 git -C <worktree> config --worktree --unset-all core.hooksPath；其余成因请检查对应配置源" >&2   # 按成因区分（r21 no229：wt_mismatch 不止清理失败一种）
    exit 1
fi
echo "✓ core.hooksPath = $HOOKS_DIR（本 clone 主检出与全部 worktree 生效）"
echo "  队友 clone 后跑一次 bash $HOOKS_DIR/install.sh；wt 用户由仓内 .config/wt.toml [pre-start] 自动装。"
echo "  注意: pre-start 仅在 worktree 首次创建时执行——已存在的 worktree 需手动跑一次本脚本。"
