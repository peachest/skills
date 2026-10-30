# ocr — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-27 | skill 基线从 v1.11 重对齐到 CLI v1.13.3：新增第 9 章（v1.12→v1.13 新特性面：--background-file、--provider/--model 单次覆盖、--format sarif、delegate preview/rule、viewer、session export/rm、rules check、scan --no-dedup/--no-summary、--max-git-procs、timeout_sec/MCP 配置、新规则包）；修正 3 处过时断言（config 有 unset、timeout_sec 已进白名单且 OCR_LLM_TIMEOUT 优先、WithoutCancel bug 在 v1.13.3 仍未修 loop.go:826） | 9d70514 | 新特性逐条对照 `--help` 实测输出 + 上游 changelog（releases API）；timeout 优先级用 30s 延迟 fake server A/B 实测（env=60 胜 timeout_sec=5）；unset 语义与 WithoutCancel 用沙箱 HOME + v1.13.3 源码 grep 实测 |
| 2026-10-30 | 第 5 章 Re-review hook 追加出口指针：单轮复核属于更大循环，循环级职责（收敛闸门/回扩终审/push 时机）归 rolling-ocr——双向依赖规范（read-material 边的下游入口） | feat: add rolling-orchestration skill (rolling-ocr) and ocr exit pointer | grep 确认 /skill:rolling-ocr 指针落第 5 章；rolling-ocr 已同 commit 建 wiki 配对 |
