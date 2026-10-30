# skill-impact — shell-review

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-28 | 诞生（grill-with-docs 会话，Q1-Q9 全量拍板）：静态 shell 评审 skill，定位=LLM 评审（ocr）的前置机械闸。工具集经 8 类全生态实测定夺（对 peer 正在修复的内部构建审计项目 4 脚本实测）：收 bash 语法闸 + shellcheck + shfmt（仅报告不落盘——digest 敏感）；剔除 bashate（纯缩进噪音）、checkbashisms（bash 脚本无需 POSIX）、shellharden（0 增量，SC2086 族已覆盖）、dash 语法层（bashism 是预期）及 5 类未装工具（LSP 底层同 shellcheck / semgrep bash 实验性 / 聚合器内部同工具 / 平台不符 / 行为测试）。关键设计：error 阻塞 + warning/style 三选一定谳（真修/场景误报/disable 注解）；白名单不内置不引 .shellcheckrc；diff 感知扫描无全仓模式；文档型只编排透传原始输出（YAGNI：不做结构化报告/CI 模板/脚本入口，行为漂移实证 ≥2 次再脚本化）（落点: SKILL.md、GLOSSARY.md、docs/adr/0001-0005） | feat(shell-review): 新增静态 shell 评审 skill（grill-with-docs，5 ADR + GLOSSARY） | npx skills add -g 安装成功；diff 源仓=安装副本一致；gitleaks clean；结果: npx skills add -g 安装成功；diff 源仓=安装副本一致；gitleaks clean |
