# skill-impact

| 日期 | 提案 | 落点 | commit | 验证 |
|---|---|---|---|---|
| 2026-10-09 | 首次实战（peer session 01a11aa5 复测 speculative-training 20 文档）：skill 推翻 peer ad-hoc 脚本的 3 个"假有用"误判（其脚本漏 python 单行读/heredoc 读侧/grep 上下文读）；流程 adherence 完整（targets.tsv→matrix×5 轮含 pattern 放宽→escape 按建账日分桶→echo×3→完整契约）。peer 发现 self-pollution 坑（审计 session 自身计入矩阵） | SKILL.md matrix 步骤补 self-pollution pitfall 段 | (本次) | peer 手动剔除当天 session 后 verdict 不变（echo 26/27/27 个历史文件触及） |
