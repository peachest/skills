# Subagent Task Templates

> 运行时动态生成 task prompt，不写死 agent 名称。
> 每个 stage 定义：输入、task 模板、输出格式、失败处理。

---

## Stage 1: Extract (Phase 1)

**Capability:** `extract_worker`

**Input files (reads):**
- `prompts/extract-claims.md` — 提取 prompt 模板
- `references/schema.md` — claim schema 定义
- `<target_document>` — 被核查的文档

**Task template:**

```
你是 claim 提取器。读 prompts/extract-claims.md 了解提取规则，读 references/schema.md 了解输出 schema。

从文档 <target_document> 提取所有可验证的 factual claim。

规则：
- claim_text 必须逐字来自原文档，不改写
- 拆解复合声明为原子 claim（按 catalog 7 种模式）
- 不输出 source_location（由 locate-claim.sh 定位计算）
- 不输出 content_hash（由 validate-claims.sh 校验计算）
- 不输出 claim_id（在合并阶段分配）
- 不提取纯 opinional 内容（"这个方案更好" 之类）

输出：JSON array（格式见 schema.md），写为 <output_file>。
只输出 JSON，不要夹杂解释文字。
```

**Output:** `claims-<doc_key>.json` — JSON array of claim objects (不含 `source_location`、`content_hash`、`claim_id`，这些由后续阶段填充)

**Failure:** 单个 worker 超时或格式错误 → 标记该文档为 extraction_failed，其他文档继续

---

## Stage 2: Triage (Phase 3b)

**Capability:** `model_alt`

**Input:**
- `claims.json` (当前 run 的)
- `references/verdict-policy.json`

**Task template:**

```
你负责 triage（分流评估）。以下 claim 被 regex 路由为 fallback，需要判断是否值得做深度 web 搜索验证。

对每条 claim，评估：
- CONFIDENT：已有足够上下文确认/否定（无需搜索）
- UNCERTAIN：需要 web 搜索才能判断
- SUSPECT：看起来和已知事实矛盾，需要重点验证

输入：
{claims_json_named_lines}

输出：JSON object — 每条 claim 更新 triage_result 字段：
{
  "C003": "UNCERTAIN",
  "C004": "CONFIDENT",
  ...
}
只输出 JSON。
```

**Output:** `triage_results.json`

**Note:** `model_alt` 应使用不同于父 session 的 provider/model（如父 session 用 Claude，triage 用 GPT-5-mini），通过 inline model override 实现。

**Failure:** triage agent 不可用或调用失败 → 跳过 Phase 3b，所有 fallback claim 进入 Phase 5

---

## Stage 3: Deep Verify (Phase 5)

**Capability:** `web_searcher`

**Input:**
- `references/verdict-policy.json` — 证据层级和裁决规则

**Task template:**

```
你是事实核查员。验证以下 claim batch：

<batch_claims_formatted>

对每条 claim：
1. web 搜索找到最相关的来源（优先找官方、arXiv、GitHub 等 T1 来源）
2. 提取来源中的证据文本
3. 判定 verdict（读 verdict-policy.json 了解裁决规则）：
   - SUPPORTED：≥1 T1 source 确认
   - CONTRADICTED：来源明确否认
   - NUANCED：基本正确但缺关键上下文
   - OUTDATED：已被新版本推翻
   - UNVERIFIABLE：找不到任何来源
4. 记录 evidence_tier（T1-T4）、evidence_url、evidence_date、confidence、severity

输出：JSON array — 每条 claim 更新 verdict + evidence 字段：
[
  {
    "claim_id": "C005",
    "verdict": "SUPPORTED",
    "evidence_tier": "T1",
    "evidence_url": "https://...",
    "evidence_text": "...",
    "evidence_date": "2026-03-31",
    "confidence": "high",
    "severity": "low"
  },
  ...
]
只输出 JSON。
```

**Batch size:** 4-5 claims per subagent

**Output:** `verify-batch-<N>.json`

**Failure:** batch 超时 → 标记整批 UNVERIFIABLE + 重试 1 次；仍失败 → 保留 UNVERIFIABLE，handoff 中注明

---

## Stage 4: Fix (Phase 8)

**Capability:** `extract_worker`

**Input:**
- `handoff.md` — 修正指引
- 原始文档

**Task template:**

```
你是文档修正工。按照 handoff.md 中的修正指引逐项修改源文档。

规则：
- 逐项修正，每完成一项报告
- 不修改 handoff.md 中未列出的内容
- 修改后确认文档格式完整

handoff.md 内容：
{handoff_content}

完成后报告：修改了哪些行、是否存在需要用户手动处理的项。
```

**Output:** 修改后的源文档（原地编辑）+ 修正完成报告

**Mode:** `async: true, context: "fork"` — 父 agent 等待 completion notification

**Failure:** 修正失败 → 保留 handoff.md，用户下次调用增量时重新进入 Phase 8
