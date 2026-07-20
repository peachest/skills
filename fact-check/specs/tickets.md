# Tickets: Fact-Check Skill Implementation

基于 `specs/design.md`（DD-01~DD-31）、`specs/run-output.md`（8-phase 文件生命周期）、`specs/todos.md`（R1~R16）。

Work the **frontier**: 任何 blocker 全部完成的 ticket 可开始。对于纯线性链，从顶部开始。

## T1: 确定性脚本（wide refactor）

**What to build:** 6 个确定性脚本（JSON I/O，无 LLM），可独立构建和测试。

**Blocked by:** 无

- [ ] `scripts/init.sh` — git rev-parse/remote/branch/diff → JSON `{document_key, mode, repo, session_tag, is_directory}`
- [ ] `scripts/validate-claims.sh` — A/B/C/D 四级校验：JSON parse → schema → source_location → text match → content_hash → 原子性
- [ ] `scripts/route-claims.sh` — 25 条 authority + 3 judgment + 2 interpretation 正则路由
- [ ] `scripts/rule-engine.sh` — 主 dispatch 完成，调度全部 25 个 verifier
- [ ] `scripts/grade-evidence.sh` — 域名 → T1/T2/T3/T4 分级 + 交叉验证 + 时效性
- [ ] `scripts/generate-report.sh` — report.md + handoff.md + ledger append + total-stats.json

## T2: P1 提取管线

**What to build:** 用户运行 `/fact-check <path>`，agent 完成 P0 → P1，产出一份文档的所有 claim。

**Blocked by:** T1（需 init.sh + validate-claims.sh）

- [ ] SKILL.md Phase 0 指令：init.sh → run.json 创建
- [ ] SKILL.md Phase 1 指令：mdq 分片 → LLM 提取 → validate-claims.sh → claims.json
- [ ] mdq 预提取：章节结构 + 链接 + 代码块
- [ ] 提取 prompt 拼接：`prompts/extract-claims.md` + 文档分片内容
- [ ] 4 级校验循环：validate-claims.sh → 失败时 per-claim diff 修补重试（max 3 轮）
- [ ] 验收：对 `公众号_KV_Cache_从显存走向存储层.md` 跑一次，≥5 条合法 claim，校验 0 失败

## T3: P2 正则路由

**What to build:** 提取后 agent 运行 route-claims.sh，每个 claim 获得 route/verifier 字段。

**Blocked by:** T2（需 claims.json 格式和示例数据）

- [ ] agent 调用 route-claims.sh 读取 claims.json + regex-rules.json
- [ ] 未匹配 claim → 走 LLM expected_verifier fallback
- [ ] 验收：URL 类 claim 得 `route: "rule_engine"`，纯价值 claim 得 `route: "refused"`

## T4: P3a 规则引擎

**What to build:** 路由后 agent 运行 rule-engine.sh，Authority 类 claim 获得 verdict/evidence_url。

**Blocked by:** T3（需已路由的 claims）

- [ ] agent 调用 rule-engine.sh：读 claims.json（route=rule_engine）→ 按 verifier dispatch → curl/gh/glab → 更新 verdict
- [ ] 错误处理：2 次指数退避 → UNVERIFIABLE
- [ ] 验收：存在 arXiv ID 的 claim 得 `SUPPORTED`，不存在得 `CONTRADICTED`

## T5: P3b triage + P4 checkpoint

**What to build:** 非路由 claim 经不同 provider LLM triage → checkpoint 展示分区 → 用户确认。

**Blocked by:** T4（需 P2+P3a 完成后的 claims）

- [ ] P3b：读 triage 级别配置，调用不同 provider subagent/LLM
- [ ] P3b：CONFIDENT → triage-escaped；UNCERTAIN/SUSPECT → 入深度搜索
- [ ] P4：展示 4 个分区（规则引擎已验证 / triage-escaped / 需深度搜索 / compound_embedded）
- [ ] P4：跳过阈值（≤3 + 全 SUPPORTED）→ 自动跳过；severity:high + CONTRADICTED → 必须打断
- [ ] 验收：检查点展示正确分区，跳过/打断阈值生效

## T6: P5 deep verify

**What to build:** UNCERTAIN/SUSPECT claim → subagent/anysearch 搜索 → grade-evidence.sh 分级 → 最终 verdict。

**Blocked by:** T5（需 checkpoint 后的 claims）

- [ ] P5：batch 分组（4-5 claims/batch），并行搜索（subagent 优先，anysearch CLI fallback）
- [ ] P5：超时处理 → UNVERIFIABLE + 重试 1 次
- [ ] grade-evidence.sh：域名分级 + 交叉验证 + 时效性标记
- [ ] 验收：搜索结果经分级后写入 claims.json，Tier 正确，矛盾触发 NUANCED

## T7: P6 报告生成

**What to build:** generate-report.sh 运行 → report.md + handoff.md + ledger + total-stats.json。

**Blocked by:** T4（需 claims 数据来测试报告格式，但脚本本身不依赖 T5/T6 的逻辑）

- [ ] generate-report.sh：从 claims.json 生成 report.md（Summary 表格 + verdict 分组明细）
- [ ] generate-report.sh：过滤 CONTRADICTED/NUANCED → handoff.md（含 `<!-- handoff-claim C001 -->` 标记）
- [ ] generate-report.sh：append ledger.jsonl + 更新 total-stats.json + 补全 run.json
- [ ] 验收：对已有 claims.json 的 run dir 运行，产出符合 spec 格式的报告文件

## T8: P7 交付 + P8 修复

**What to build:** agent 展示摘要 → A/M/V 选择 → A 路径逐项编辑 → ledger 追加修正。

**Blocked by:** T7（需报告文件）

- [ ] P7：交付摘要模板（verdict 分布 + 待修项 + 分类计数）
- [ ] P8 A 路径：agent 逐项编辑源文档 + claims.json 状态更新 + ledger append
- [ ] P8 M 路径：输出 checklist 给用户手动处理
- [ ] P8 争议路径：handoff.md 标记 `verdict wrong, counter evidence: <url>`
- [ ] 验收：对 CONTRADICTED 项执行 A 路径，源文档编辑 + ledger 多一行修正

## T9: 增量模式

**What to build:** git diff hunk 匹配 → carry forward 旧 claim → 只 re-extract diff 区域。

**Blocked by:** T2（全量提取必须先工作），T3（路由需能处理 re-extract 的 claim）

- [ ] P0 增量初始化：读旧 claims.json + git diff hunk → 匹配 source_location → carry forward
- [ ] content_hash 验证：carry forward 后 hash 验证，mismatch → re-extract
- [ ] re-extract queue → 只处理 diff 区域 claim
- [ ] 验收：编辑文档一个段落，rerun 后 80%+ 旧 claim carry forward

## T10: Profiling

**What to build:** 每个 phase/脚本/LLM 调用的时间戳 + token 计数写入 profile.jsonl。

**Blocked by:** T1（需 run dir 概念），可伴随其他 tickets 增量添加

- [ ] phase_start/end 事件：每个 Phase 开始和结束时写入毫秒时间戳
- [ ] script 事件：脚本调用时用 time 前缀捕获耗时
- [ ] llm_call 事件：从 API 响应读取 input_tokens/output_tokens
- [ ] profile-summary.json：phase 6 聚合各 phase 耗时占比、LLM token 统计
- [ ] 验收：运行后 profile-summary.json 显示各 phase 耗时占比
