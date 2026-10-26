# skill-impact — setup-gitleaks

| 日期 | 提案/落点 | 验证 | commit |
|---|---|---|---|
| 2026-09-17 | 初版创建：SKILL.md（两层闸门模型：gitleaks 凭证层 + grep identifier pattern 层；六步流程 harvest→gate→placement→pointer→pre-push→verify）+ templates/gitleaks.toml（占位符规则 + self-exclusion allowlist）+ templates/sanitize-check.sh + tests/test_gate.sh（种子密钥 FAIL/清洁 PASS/缺配置 WARN 三断言） | tests/test_gate.sh 3/3 PASS；仓库 sanitize-check CLEAN | 43b2399 |
| 2026-10-12 | SKILL.md 新增 "Triage a finding before acting" 段：gitleaks 命中 ≠ 泄漏，先验证 git ls-files / 提交历史 / 远端分支再定性，防误报驱动误删（GENERAL 审计教训沉淀） | tests/test_gate.sh 3/3 PASS | 74307b4 |
| 2026-10-26 | SKILL.md Step 6 新增 real-repo canary 规程（4 步：真实变体形态 seed / 仓内路径 / 断言正向 rule-id 命中非退出码 / git log 确认拦截生效）。起因=llmops-wiki 装闸门实证：①`\b` 左边界在 `_` 前失效（`REDIS_PASSWORD=` 形态漏检，占位符测试无法暴露）；②rc 误读两连（仓外路径 git 报错冒充拦截、rc=0 假密码入历史靠事后 rebase 摘除）；③skill 原验收只测模板占位符，不测用户定制规则的变体覆盖 | canary 流程本身在 llmops-wiki 抓出规则 bug 并闭环（命中 kv-password-literal → DIRTY） | 见 git log |
