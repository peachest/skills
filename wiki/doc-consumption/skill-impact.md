# skill-impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-09 | 首次实战（peer session 01a11aa5 复测 <project-a> 20 文档）：skill 推翻 peer ad-hoc 脚本的 3 个"假有用"误判（其脚本漏 python 单行读/heredoc 读侧/grep 上下文读）；流程 adherence 完整（targets.tsv→matrix×5 轮含 pattern 放宽→escape 按建账日分桶→echo×3→完整契约）。peer 发现 self-pollution 坑（审计 session 自身计入矩阵）（落点: SKILL.md matrix 步骤补 self-pollution pitfall 段） | c5a000e | peer 手动剔除当天 session 后 verdict 不变（echo 26/27/27 个历史文件触及） |
| 2026-10-26 | 分析（文章《AI写得快≠真正提效》机制移植评估）后**拒绝**"将捕获层整体前移为常驻 hook"：skill 瓶颈在分析（matrix/escape/echo 是跨 session 批处理逻辑），且 session JSONL 已 100% 记录 hook 能看到的一切，通用全量记录是冗余流式抳贝；hook 同步预算（10s）也装不下完整 READ/WRITE/MENTION 分类器。采纳的分工：pi-bash-guards KB 门禁 guard（同日落地）已对 ops vault + <internal-wiki> 写月度读日志（satisfy/block/pass 三类事件），覆盖当前最重要的目标面；捕获层前移（targets.tsv 喂 doc-touch hook + 轻分类）的触发条件 = KB 读日志观察 1-2 周后跑复审，且审计要季度化时再做，不为"可能有用"预建（落点: 本条目（纯决策记账，无 skill 本体变更）） | 不适用（无代码变更；KB guard 在 pi-packages 仓） | KB readlog 实测：block/satisfy/pass 三事件序列正确（本 session 人工验证） |
