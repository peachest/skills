# Work Remaining — Fact-Check Skill

> 状态: 设计阶段完成 (DD-01 ~ DD-31)，进入实现阶段。
> 更新: 2026-07-09（DD-06 吸收 5 个参考项目亮点完成修订；DD-02 规则引擎扩展为 25 条 authority 规则，覆盖 5 类平台 + 4 种包管理器 + 6 种学术标识符 + SPDX License；Phase 2 改为双通道路由；DD-28~DD-31 完成 CLI 精简 + 子 agent 并行化设计）

---

## 必须实现（skill 可运行）

### R1 · SKILL.md workflow 步骤细化

**当前状态:** Phase 概览已有，但 agent 需要逐步骤的具体指令

**需要补充的内容:**
- Phase 0: 增量检测逻辑的伪代码（DD-30 自动检测：ledger+git→full/incremental，subagent capability 检测）
- Phase 0: 文档域自动检测逻辑（关键词 → 扩展层类型启用，增量新增不删除）
- Phase 1: 提取 prompt 的调用方式（读 `prompts/extract-claims.md`，含 catalog 7 模式拆解 + `decomposition_mode`/`compound_flag`，拼合文档内容，产出 `claims.json`）
- Phase 1: 四级 validator loop（DD-22 A JSON 语法 / B Schema 符合 / C1 location 有效 / C2 text 匹配 / C3 hash 一致 / D 原子性，per-claim diff 修补，max 3 轮，失败保留 validation_errors.json）
- Phase 2: 双通道路由（读 `references/regex-rules.json`，25 条 authority 规则 regex 优先匹配 + LLM `expected_verifier` fallback）
- Phase 3a: rule-engine.sh 的调用参数和预期输出格式
- Phase 3b: triage 的 LLM 调用策略（不同 provider，单次调用，分流逃逸/搜索）
- Phase 4: 检查点 UI 模板（展示：规则引擎已验证 + triage-escaped + 需深度搜索 + `compound_embedded` 警告；支持 triage override）
- Phase 5: anysearch 搜索策略（batch_search、提取策略、交叉验证指令）
- Phase 6: 文件写入清单和格式
- Phase 7: 交付摘要格式
- Phase 8: A/M/V 路径的选择 UI 和 fix loop

**建议:** 每个 phase 写成独立的 checklist 块即可，不用写在 SKILL.md 主文件中（已在 60 行）。

### R2 · rule-engine.sh 接入 claims.json

**当前状态:** 验证函数骨架（arXiv/DOI/PR/Issue/repo/URL）已编写，但 Main 部分是 stub

**需要补充的内容:**
- 读取 `claims.json`，过滤 `expected_verifier == "rule_engine"` 的行（含双通道 LLM fallback 路由进来的 claim）
- 根据 regex-rules.json 中的 25 条 authority 规则 dispatch 到对应 verifier（code_platform_pr/issue/repo 为抽象 verifier，内部按平台 dispatch 到 `gh`/`glab`/Gitee API）
- 新增 verifier: `rule_engine.cargo` / `go_module` / `nuget`（包管理器扩展，`curl -sI` 模式）
- 新增 verifier: `rule_engine.pmid` / `patent` / `ietf_draft`（学术/标准扩展，`curl -sI` 模式）
- 新增 verifier: `rule_engine.spdx_license`（SPDX 标识符验证：先校验 SPDX license list 有效性，再查项目 metadata）
- 调用验证函数，收集输出格式：`{ "vid": "...", "verdict": "...", "evidence": "...", "evidence_url": "..." }`
- 写回 `claims.json` 更新对应 entry
- 错误处理：`gh` CLI 缺失时的 fallback 提示

### R3 · Agent 调用 skill 与子 agent 入口协定

**当前状态:** SKILL.md 已简化为 3 命令 CLI（`/fact-check <path>` / `--full` / `--status`），DD-31 定义子 agent 能力检测 + 并行分发，`references/subagent-tasks.md` 定义各阶段 task prompt 模板

**需要补充的内容:**
- Phase 0 的策略：项目根目录检测、`fact-check/` 目录初始化
- Phase 1 的 prompt 拼接规则 + subagent per-document 并行分发：读 `prompts/extract-claims.md` + 文档全文 → 子 agent 并行提取 → 校验器 loop
- claims.json 的写入路径：`<project>/fact-check/run-{datetime}-{tag}/claims.json`
- 每个 phase 的"完成条件"和"异常退出条件"

### R4 · 检查点的 UI 交互描述

**当前状态:** design.md DD-05 已更新，但 phase 实现细节待补充

**需要补充的内容:**
- 检查点暂停时，agent 对用户输出的 UI 文本模板（分区展示：规则引擎已验证 / triage-escaped / 需深度搜索 / compound_embedded 警告 / INFERRED 声明）
- 用户输入 `y / n / skip C001 / view C001 / edit C001 / search C001`（search → override triage，将该 claim 拉入 Phase 5 深度搜索）
- 跳过阈值检测伪代码（≤ 3 条新 claim + 全部 SUPPORTED → 自动跳过；severity:high + CONTRADICTED → 必须打断）
- 检查点后 `claims.json` 重新读取的确认

### R5 · Phase 5 搜索验证策略（子 agent 并行优先，anysearch CLI 作为 fallback）

**当前状态:** 可通过 `anysearch-researcher` / `researcher` 子 agent 并行执行（DD-31），也可 fallback 到 anysearch CLI

**需要补充的内容:**
- 子 agent 模式：claim batch 分组 → 从 `subagent-tasks.md` 动态生成 task → 并行调用搜索 agent（≤ 4 concurrency）
- CLI fallback 模式：不同类型 claim 的搜索 query 生成策略
- batch_search 的并发量控制
- 交叉验证的判断规则（多源 vs 单源、出现矛盾时如何升级 verdict）
- extract 命令的使用时机（需要读原始页面内容时）

---

## 可实现（首次实测后再定）

### R6 · 非 markdown 文档处理

- PDF 文档的 claim 提取（需要 pdftotext 或类似工具）
- HTML 文档的净化和分段
- 纯文本的无结构文档处理

### R7 · 超大文档分片

- 超过 50 条 claim 的文档分段策略
- 分片后的 vid 去重和 atomicity_parent 跨段关联
- 单次 LLM 提取的内容窗口管理

### R8 · Phase 8 Agent Fix 的逐项交互

- agent 生成 diff 的格式
- 用户 `y/n/e` 的解析
- 编辑后 `claims.json` 状态更新
- 修正完成后的增量 recheck 触发

### R9 · handoff.md 规范

- 待修项的机器可读格式（agent 能读取并执行修正）
- 与 `documents/<key>.ledger.jsonl` 的关联
- bug/issue 的优先级排序

### R10 · total-stats.json 自动聚合

- 每次 run 结束后的统计更新逻辑
- `verdict_distribution`、`evidence_tier_distribution`、`total_claims` 等字段
- 多项目间的统计隔离

---

### R11 · validate-claims.sh（Phase 1 四级校验器）

**当前状态:** 不存在。Phase 1 校验当前设计为 LLM retry 循环，应改由脚本只读校验。

**需要实现的内容（确定性，无 LLM 调用）：**
- A 级：验证 JSON 语法合法可 parse
- B 级：验证 Schema 字段存在 + 类型 + 枚举值合法
- C1 级：验证 `source_location` 行/区间/精确位置在源文档中存在
- C2 级：从 source_location 定位原文，trim/compress 后与 `claim_text` 逐字对比
- C3 级：重新计算 `content_hash`（SHA256 + cut -c1-12 + sha256: 前缀）并对比
- D 级：**仅验证**（不再强制执行拆解——拆解由 R23 check-atomicity.sh 在提取阶段即时处理）。检测 claim 的 decomposition_mode 是否符合 catalog 模式，不一致时输出 warning
- 输出格式：`{ "passed": N, "failed": [{ "claim_id": "...", "errors": [...] }], "auto_fixes": [...] }`
- 只读脚本，不修改 claims.json

### R12 · route-claims.sh（Phase 2 确定性正则路由）

**当前状态:** 不存在。Phase 2 的路由逻辑在 agent 内存中处理。

**需要实现的内容：**
- 读取 `claims.json` + `references/regex-rules.json`
- 对每个 claim 的 `claim_text` + `normalized_claim` 双字段匹配 25 条 authority 规则
- 3 条 judgment 规则（纯价值/社区归因/hedging_factual）+ 2 条 interpretation 规则
- 产出 JSON：`{ "claims": [...], "stats": { authority_hit, judgment_refused, judgment_community, judgment_hedging, interpretation, unmatched }}`
- 未匹配的 claim 标记为 `unmatched`，留给 agent LLM fallback

### R13 · grade-evidence.sh（Phase 5 证据分级）

**当前状态:** 不存在。证据 Tier 分级 + 交叉验证 + 时效性标记当前由 LLM 在搜索 prompt 中判断。

**需要实现的内容：**
- 从 verify-batch JSON 的 `evidence_url` 域名推导 Tier（T1: github/arxiv/doi/docs; T2: blog/tutorial; T3: reddit/HN/discussion; T4: none）
- 交叉验证：同 batch 内多源同 verdict → confidence: high；同 batch 内矛盾 → CONTRADICTED/NUANCED
- 时效性：`evidence_date < now - 6mo` → `staleness_warning: true`

### R14 · generate-report.sh（Phase 6 报告生成）

**当前状态:** 不存在。报告/ledger/统计当前由 agent 手写。

**需要实现的内容：**
- 从 claims.json 生成 report.md（Summary 表格 + 按 verdict 分组的 claim 清单）
- 从 claims.json 过滤 CONTRADICTED/NUANCED 生成 handoff.md（含 `<!-- handoff-claim C001 -->` 机器可读标记）
- append ledger.jsonl（`jq -c` 提取 vid/claim_text/verdict/evidence_tier/evidence_url/timestamp/run）
- 更新 total-stats.json（读旧文件 + 合并本次）
- 补全 run.json 的统计字段（total_claims, verdict_distribution, duration_seconds）
- **写一致性自检**（零 LLM 成本，确定性）：report.md summary 表格 vs claims.json verdict 分布 → 不一致则自动修正 report；ledger 行数 vs claims.json checked count → 不一致写 warning 到 run.json；report 中 evidence_url 全非空

### R15 · init.sh（Phase 0 初始化）

**当前状态:** 不存在。Phase 0 的 git 操作/路径检测/incremental 判断由 agent 逐个执行。

**需要实现的内容：**
- git rev-parse + remote + branch + diff + rename detection（DD-30）
- realpath → document_key
- 文件/目录检测，目录→扫描直接子 `*.md`
- 输出：JSON `{ document_key, mode: full|incremental, repo, session_tag, is_directory }`

### R16 · profile.jsonl / profile-summary.json（运行可观测性）

**当前状态:** 不存在。长运行任务无性能数据，无法定位瓶颈。

**需要实现的内容：**
- `run-{...}/profile.jsonl`：7 种事件类型（phase_start/end、llm_call、script、network、retry、subagent）
- `run-{...}/profile-summary.json`：Phase 6 由 `generate-report.sh` 聚合生成
- agent 在每个 Phase 开始/结束时记录毫秒时间戳
- 脚本调用用 `time` 前缀捕获耗时
- LLM 调用后从 API 响应读取 token 计数
- 写入方式：shell `>>` 追加到 profile.jsonl
- 聚合：total_duration、phases 占比、LLM token 统计、重试计数

### R17 · Phase 5 搜索精炼 Loop（已决策，待实现）

**当前状态:** 设计完成（5 个决策已 grill 确认），DD 待写入 design.md。

**决策摘要:**
- Q1 查询生成：纯 LLM 改写，用 multi-query + step-back 手段
- Q2 搜索策略：两阶段 C——R0 用 normalized_claim，失败 → LLM 生成 2 并行 query
- Q3 降级上限：质量驱动——零结果 vs 仅 T3 走不同 R1 策略，max 2 轮
- Q4 证据合并：全量合并，最高 tier 定 verdict，低 tier 保留在 evidence 数组
- Q5 批处理适配：混合编排 C——R0 batch → 父 agent 收集 → 一次 LLM 生成所有 R1 query → 重新 batch

**需要实现的内容:**
- R0 batch 搜索后，子 agent 返回结果 + `needs_refinement: true/false` + `fallback_reason: "no_results"|"t3_only"`
- 父 agent 收集所有 R1 候选 → 一次 LLM 调用生成所有 R1 query（multi-query 或 step-back）
- R1 重新 batch 分组 + 子 agent 搜索
- 全量证据合并：所有轮次结果按 tier 合并，低 tier 保留为 supplementary
- R1 仍失败 → 零结果 case → UNVERIFIABLE；仅 T3 case → NUANCED（confidence=low）

### R18 · 跨 Phase 内部一致性 Loop（待 grill 细节）

**当前状态:** Q1 已决（混合筛选 C），其余细节待 grill。

**已定:** 先按 claim type 分组 → 同组内文本相似度筛选候选对 → 批量送 LLM 判断矛盾

**待定:**
- 矛盾确认后的处理策略（双降级？溯源澄清？标记 SUSPECT？）
- SUSPECT 对的 sub-loop 设计
- 一致性检查的触发条件（全量？仅新 claim？）

### R19 · Phase 3a 跨 Verifier 回退链（已跳过）

**决策:** 不做。确权型验证的实际失败全是 ID 不存在（非网络抖动），回退链无实际痛点。现有 DD-12 的 2 次指数退避已足够覆盖网络抖动。

### R20 · Phase 2 孤儿 Claim 恢复 Loop（已跳过）

**决策:** 不做。regex 全失配 + LLM fallback 无法归类的概率极低（现有 ~270 条 claim 无一 orphan）。此类 claim → 默认 `web_search`，Phase 5 搜索自然判定 UNVERIFIABLE 或其他。

### R21 · Phase 6 写一致性校验（已合并到 R14）

**决策:** 不做独立 loop，作为 generate-report.sh（R14）的最后一步自检。脚本自己生成报告数据，自己验证一致性，零 LLM 成本。

### R22 · locate-claim.sh（Claim 文本定位器）

**当前状态:** 设计完成（grill Q1-Q5 全部确认）。

**核心设计:** 仿照 pi 的 edit 工具——精确子串匹配（非逐行 grep），多行文本直接做子串扫描。agent 逐条调用，即时获得反馈。

**设计决策:**
- Q1 normalize：不做。索引严格原文，失败直接标记 TEXT_MISMATCH 进 retry loop
- Q2 前缀长度：80 字符，短行用完整内容，≤20 字符冲突 → AMBIGUOUS
- Q3 性能：O(n) 子串扫描（n=~80KB 文档），单次 <1ms
- Q4 字符级定位：行号 + indexOf 算出 col 范围
- Q5 形态：独立 shell 脚本，agent 通过 bash 调用

**需要实现的内容:**
- `locate-claim "<claim_text>" <doc_path>` → JSON `{ ok, location, hash }` 或 `{ error: TEXT_NOT_FOUND, closest_match }` 或 `{ error: AMBIGUOUS, candidates }`
- 多行文本精确子串匹配（edit 风格的 oldText 匹配逻辑）
- 找到后计算 `source_location`（DD-25 四种格式）和 `content_hash`（SHA256 前 12 字符）
- agent 重试循环（max 3）：TEXT_NOT_FOUND → 看 closest_match → 修正 claim_text → 重试

### R23 · check-atomicity.sh（原子性检查器）

**当前状态:** 设计完成。从 validate-claims.sh 的 D 级分离出来的独立脚本。

**需要实现的内容:**
- 接收 claim_text → 按 7 种 catalog 模式做 regex 匹配
- 返回：`{ match: true/false, pattern: "and_enum"|"..."|"none", sub_items: ["...", ...], word_count }`
- 匹配且 >1 子项 → agent 生成 sub_claims[]（派生，不需要 locate）
- 匹配只有 1 项 → 不需拆
- 不匹配 + >25 词 → compound_embedded
- Phase 1 即时调用，给 agent 即时反馈

### R24 · analyze-run.sh（运行质量分析）

**当前状态:** 设计完成（grill Q1-Q3 确认）。

**设计决策:**
- Q1 分析范围：单次 run（A），未来扩展跨 run
- Q2 报告格式：双输出——analysis.json（机器读）+ analysis.md（人读）
- Q3 分析方式：全确定性脚本（jq/count/ratio），零 LLM；analysis.md 用模式匹配模板生成

**分析的 10 个指标：**

| # | 指标 | 数据源 | 阈值 |
|---|------|--------|------|
| 1 | TEXT_MISMATCH 率 | validation_errors.json | >50% → 🔴 |
| 2 | Rule Engine 误匹配率 | claims.json（verdict+matched_rule） | >20% → 🔴 |
| 3 | Verdict 分布 | claims.json | SUPPORTED <10% → 🟡 |
| 4 | Phase 完成度 | profile.jsonl（phase events） | P5-P8 未达 → 🟡 |
| 5 | 声明密度 | claims.json count / doc bytes | >3/KB → 🟡 |
| 6 | locate 重试次数 | validation_errors.json | >5 → 🔴 |
| 7 | 正则路由覆盖率 | claims.json（route vs matched_rule） | <30% → 🟡 |
| 8 | Triage 跳过率 | claims.json（triage_result 缺失） | >0% → 🟡 |
| 9 | Subagent 使用率 | profile.jsonl（subagent events） | 预期全用→实际未用 → 🟡 |
| 10 | 总耗时 | profile.jsonl | >10min → 🟡 |
| 11 | 非标准 verdict 率 | claims.json vs DD-03 合法列表 | >0% → 🔴 |
| 12 | 证据 tier 缺失率 | claims.json evidence_tier | >50% → 🔴 |
| 13 | verify-batch ↔ claims 一致性 | verify-batch-N.json vs claims.json | 不一致 → 🟡 |
| 14 | ad-hoc 脚本数 | session log（临时 Python 脚本版本迭代） | >3 → 🟡 |

> 指标 11-14 基于 e2e coldstart session 完整 P0-P7 实践补充。
- 读取 run dir 下所有 JSON 文件 → `jq` 聚合计算
- 输出 analysis.json（10 个指标 + 阈值判断）
- 输出 analysis.md（含执行摘要 + 阶段分析 + 改进建议 + 模板化根因）
- 模式匹配模板（如 CONTRADICTED>20% → "Rule engine false-positive rate high. Check regex-rules.json."）
- Phase 6 generate-report.sh 结束后可选自动调用

**与 R16（profile）的区别:** profile 是"发生了什么"（性能观测），analysis 是"哪里出问题了"（质量诊断）。analysis 使用 profile-summary.json 作为数据源之一。

---

## 验收标准

- [ ] 对 `04-llama.cpp框架.md` 跑一次完整 Phase 0–8（含 Phase 3b triage）/fact-check
- [ ] 对 `kvcache/research/01_分层存储架构.md` 跑一次增量
- [ ] R1-R5 所有 gaps 填补完毕
- [ ] 发现至少一次 CONTRADICTED/NUANCED/INFERRED 并自动生成 handoff.md
- [ ] Phase 8 完成至少一次 agent fix + 用户确认 + 增量 recheck 的完整 loop
- [ ] catalog 7 模式拆解成功（至少触发 3 种模式）
- [ ] hedging_factual guard 正确路由（含可验证原子的"可能"类 claim → web_search，非 REFUSED）
- [ ] 扩展层类型自动检测工作（含定价/合规关键词的文档启用对应类型）
- [ ] analysis.md 自动生成（含 10 个质量指标，零 LLM）
