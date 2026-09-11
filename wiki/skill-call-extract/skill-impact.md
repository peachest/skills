# skill-impact — skill-call-extract

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| 提案 | 落点 | commit | 验证命令与结果 |
|------|------|--------|----------------|
| S1 版本锚定：injection body / read-load toolResult 内容哈希 → 源仓库 git 历史逐 blob 解析 → commit / uncommitted（含幽灵版本检测 matches_current_file:false）/ third-party 三态裁决。不在 SKILL.md 加 version 字段（共享 checkout 下手动 bump 必漂移；内容哈希是"实际跑的字节"的 ground truth，版本字段只是声称） | scripts/version-anchor.py + SKILL.md 步骤 5 + 交付物 4 + Done-when 第 4 条 | 6f98eeb | `uv run pytest`：29 passed（8 新测试 + 真实形态收敛测试）；真实 session 冒烟（<project> 会话锚定 to-intent）：17:47 注入正确解析到 48df71d，17:26 注入正确判为幽灵版本（未提交的集成前版本，仅存于 session log） |
| R1 SKILL.md frontmatter 加 version 字段——被否：多 session 共享 checkout（本仓库现实）下靠人记得 bump 必然漂移；git blob 哈希已是无歧义版本源，字段是对环境的冗余 cache（skill-authoring 规范：cache 只存环境查不到的东西） | —（采纳 S1 替代） | — | 本 session 论证：version 字段只告诉"声称是 v3"，无法回答"该 session 当时实际生效哪版"——后者只有内容哈希能答 |
