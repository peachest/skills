# skill-impact — create-mr

提案台账：每次 skill 编辑一行，**被拒提案也记录**（含拒绝理由，防止同形状提案原样重提）。
状态：proposed / accepted（已落地）/ rejected / verified（下轮 diagnose 确认 pattern 消失）。

| 日期 | 提案 | 落点 | commit | 验证 | 结果 |
|------|------|------|--------|------|------|
| 2026-09-09 | S1 preflight.sh：预检信息收集包（remote/平台/分支状态/已有 MR/target 候选/标题/assignee），结构化输出 | engineering/create-mr/scripts/（待建） | — | 落地后 pytest；下轮 diagnose 验证 P-001/P-003 absent-this-run | proposed |
| 2026-09-09 | S2 create-draft-mr.sh：create 命令收编（含 -R URL 归一化 + --desc-file 文件化描述） | engineering/create-mr/scripts/（待建） | — | 同上，验证 P-004/P-005/P-006 absent | proposed |
| 2026-09-09 | S3 两条怪癖入 SKILL.md step 2/5：ssh remote 的 -R 需原样带 .git 后缀；双实例环境 glab mr list 需 GITLAB_HOST 前缀 | engineering/create-mr/SKILL.md | — | 下轮 diagnose 验证 P-002 absent | proposed |
| 2026-09-09 | S4 独立 glab-json.py 脚本 | — | — | — | rejected: 环境已有 jq，按仓库"文档优先于新脚本"惯例，文档化一条 jq 规范命令即可 |
| 2026-09-09 | S5 job-trace ANSI 剥离一行命令（`sed 's/\x1b\[[0-9;]*m//g'` 再 grep）归并 glab-api skill | glab-api SKILL.md | — | 下轮 diagnose 验证 P-007 相关场景 absent | proposed |

备注：harbor registry 鉴权脚本的重复内联（诊断报告中有记录）属部署诊断域，超出
create-mr 范围——若未来出现 harbor-api skill，其 skill-impact 首条从这里引用。
