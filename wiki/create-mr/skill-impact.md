# skill-impact — create-mr

提案台账：每次 skill 编辑一行，**被拒提案也记录**（含拒绝理由，防止同形状提案原样重提）。
状态：proposed / accepted（已落地）/ rejected / verified（下轮 diagnose 确认 pattern 消失）。

| 日期 | 提案 | 落点 | commit | 验证 | 结果 |
|------|------|------|--------|------|------|
| 2026-09-09 | S1 preflight.sh：预检信息收集包（remote/平台/分支状态/已有 MR/target 候选/标题/assignee），结构化输出，含 404 甄别与分支一致性节 | engineering/create-mr/scripts/preflight.sh | 落地 commit 见 git log | bash -n + 实跑于 ~/skills（gh 侧）验证；下轮 diagnose 验证 P-001/P-003 absent-this-run | accepted 2026-09-10 |
| 2026-09-09 | S2 create-draft-mr.sh：create 命令收编（-R URL 归一化 + title 清洗拒 Draft:/WIP: 前缀 + --desc-file 文件化描述 + 瞬时失败重试一次；exit 3 = glab 静默失败短路） | engineering/create-mr/scripts/create-draft-mr.sh | 落地 commit 见 git log | bash -n + --dry-run 冒烟（ssh URL 归一化、Draft:/WIP: 剥离、--no-push）；下轮 diagnose 验证 P-004/P-005/P-006 absent | accepted 2026-09-10 |
| 2026-09-09 | S3 怪癖入 SKILL.md：URL 归一化规则与跨实例 -R 形式（step 2）、404 甄别 + tos/* 静默失败短路（step 5） | engineering/create-mr/SKILL.md | 落地 commit 见 git log | 下轮 diagnose 验证 P-002 absent | accepted 2026-09-10 |
| 2026-09-09 | S4 独立 glab-json.py 脚本 | — | — | — | rejected: 环境已有 jq，按仓库"文档优先于新脚本"惯例，文档化一条 jq 规范命令即可 |
| 2026-09-09 | S5 job-trace ANSI 剥离一行命令（`sed 's/\x1b\[[0-9;]*m//g'` 再 grep）归并 glab-api skill | in-progress/glab-api/SKILL.md | — | 下轮 diagnose 验证 P-007 相关场景 absent | proposed |
| 2026-10-14 | S7 标题风格固定为行为变更式：step 6 删除 commit-subject / 分支名转换备选，仅允许行为变更（前后变化/症状修复）式标题；TITLE_CANDIDATE 降为措辞素材 | engineering/create-mr/SKILL.md | a146aa3 | 下轮 diagnose 验证 title 风格漂移 absent | accepted 2026-10-14 |
| 2026-09-10 | S6 step 0 陈旧度规则（二次执行/隔日 session 必重读 SKILL.md）+ step 1 多 remote 必问强化 + step 8 确认门定义（仅本 session 显式用户输入算确认）——对应 diagnose#2 遵循度结论 | engineering/create-mr/SKILL.md | 落地 commit 见 git log | 下轮 diagnose 验证 step1/step8 违规与 draft 漂移 absent | accepted 2026-09-10 |
| 2026-10-15 | S8 preflight.sh 直读 `OCR_REMOTE` env 覆盖 primary remote 推导（非法值 exit 2 并列可用 remote，fork 仓防呆对齐 triage-mr #63）；SKILL.md step 1 注明 ask 显式选择优先于 OCR_REMOTE（env 是无问答时的默认），MULTI_REMOTE ask 契约不变 | engineering/create-mr/scripts/preflight.sh + SKILL.md | 0908dab | pytest 3 例（override/default/非法值 exit 2）+ bash -n；下轮 diagnose 验证 fork 仓 platform 误判 absent | accepted |

备注：harbor registry 鉴权脚本的重复内联（诊断报告中有记录）属部署诊断域，超出
create-mr 范围——若未来出现 harbor-api skill，其 skill-impact 首条从这里引用。
| 2026-10-15 | S9 preflight gh pr list 加 `--repo owner/repo`（取自 OCR_REMOTE 选中 remote 的归一化 URL path；gh 自身 remote 解析在 fork 检出会查错仓）；glab 侧不变（--hostname 已管 host） | engineering/create-mr/scripts/preflight.sh | 6dbb8d7 | pytest 参数化 3 例（scp/https/ssh:// 三种 remote 形式，fake gh journal 断言 --repo team/app）；对应 P-002 远端形式矩阵收口 |
