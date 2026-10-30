# skill-impact — create-mr

提案台账：每次 skill 编辑一行，**被拒提案也记录**（含拒绝理由，防止同形状提案原样重提）。
状态：proposed / accepted（已落地）/ rejected / verified（下轮 diagnose 确认 pattern 消失）。

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-09-09 | S1 preflight.sh：预检信息收集包（remote/平台/分支状态/已有 MR/target 候选/标题/assignee），结构化输出，含 404 甄别与分支一致性节（落点: engineering/create-mr/scripts/preflight.sh） | 落地 commit 见 git log | feat(create-mr): sediment S1/S2/S3 from two diagnose rounds；结果: accepted 2026-09-10 |
| 2026-09-09 | S2 create-draft-mr.sh：create 命令收编（-R URL 归一化 + title 清洗拒 Draft:/WIP: 前缀 + --desc-file 文件化描述 + 瞬时失败重试一次；exit 3 = glab 静默失败短路）（落点: engineering/create-mr/scripts/create-draft-mr.sh） | 落地 commit 见 git log | feat(create-mr): sediment S1/S2/S3 from two diagnose rounds；结果: accepted 2026-09-10 |
| 2026-09-09 | S3 怪癖入 SKILL.md：URL 归一化规则与跨实例 -R 形式（step 2）、404 甄别 + tos/* 静默失败短路（step 5）（落点: engineering/create-mr/SKILL.md） | 落地 commit 见 git log | feat(create-mr): sediment S1/S2/S3 from two diagnose rounds；结果: accepted 2026-09-10 |
| 2026-09-09 | S4 独立 glab-json.py 脚本 | — | —；结果: rejected: 环境已有 jq，按仓库"文档优先于新脚本"惯例，文档化一条 jq 规范命令即可 |
| 2026-09-09 | S5 job-trace ANSI 剥离一行命令（`sed 's/\x1b\[[0-9;]*m//g'` 再 grep）归并 glab-api skill（落点: in-progress/glab-api/SKILL.md） | — | feat(glab-api): glab CLI/GitLab API decision table + verified quirks；结果: proposed |
| 2026-09-10 | S6 step 0 陈旧度规则（二次执行/隔日 session 必重读 SKILL.md）+ step 1 多 remote 必问强化 + step 8 确认门定义（仅本 session 显式用户输入算确认）——对应 diagnose#2 遵循度结论（落点: engineering/create-mr/SKILL.md） | 落地 commit 见 git log | feat(create-mr): sediment S1/S2/S3 from two diagnose rounds；结果: accepted 2026-09-10 |
| 2026-10-14 | S7 标题风格固定为行为变更式：step 6 删除 commit-subject / 分支名转换备选，仅允许行为变更（前后变化/症状修复）式标题；TITLE_CANDIDATE 降为措辞素材（落点: engineering/create-mr/SKILL.md） | feat(create-mr): MR 标题风格固定为行为变更式 | feat(create-mr): MR 标题风格固定为行为变更式；结果: accepted 2026-10-14 |
| 2026-10-15 | S8 preflight.sh 直读 `OCR_REMOTE` env 覆盖 primary remote 推导（非法值 exit 2 并列可用 remote，fork 仓防呆对齐 triage-mr #63）；SKILL.md step 1 注明 ask 显式选择优先于 OCR_REMOTE（env 是无问答时的默认），MULTI_REMOTE ask 契约不变（落点: engineering/create-mr/scripts/preflight.sh + SKILL.md） | feat(mr-review-triage): OCR_REMOTE env override + startup auth probe (#63) | feat(mr-review-triage): OCR_REMOTE env override + startup auth probe (#63)；结果: accepted |
| 2026-10-15 | S9 preflight gh pr list 加 `--repo owner/repo`（取自 OCR_REMOTE 选中 remote 的归一化 URL path；gh 自身 remote 解析在 fork 检出会查错仓）；glab 侧不变（--hostname 已管 host）（落点: engineering/create-mr/scripts/preflight.sh） | fix(create-mr): preflight gh pr list targets the OCR_REMOTE-selected repo (ocr r1 F2) | fix(create-mr): preflight gh pr list targets the OCR_REMOTE-selected repo (ocr r1 F2) |
| 2026-10-26 | S11 step 10「MR 闭环（CI 订阅 + 评审循环）」：MR 建好后 opt-in 闭环——pi-events-daemon 订阅 CI 终态（gitlab-pipeline 模板 ci 形态，需先取 head_pipeline.id；MR 页 URL 会路由到 mr 形态）→ 红：失败按类型路由 gitlab-security-job / diagnose-ocr-ci，2 轮不绿或非 agent 权限即停上报 → 绿：triage-mr pull + challenge-audit 审报告（杀掉的落 ❌ FP/🔵 OOS）→ fix triage 模式（闭环确认计为 batch instruction）→ post+verify 循环至 gate exit 0；闭环确认覆盖同分支评审修复 push，超范围回 step 8（落点: engineering/create-mr/SKILL.md） | feat(create-mr): MR 建好后接 CI 订阅+评审闭环 | feat(create-mr): MR 建好后接 CI 订阅+评审闭环 |

备注：harbor registry 鉴权脚本的重复内联（诊断报告中有记录）属部署诊断域，超出
create-mr 范围——若未来出现 harbor-api skill，其 skill-impact 首条从这里引用。

