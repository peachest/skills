# Fact-Check Skill 执行分析

## Session 来源

### Session 1

- Session ID: `019f82a4-f052-7fc8-89dc-f55064e14f4a`
- 日期: 2026-07-21
- 任务: research → fact-check 串联
- 文档: Kimi K3 技术报告（中文，~630 行，34KB）
- 模型: glm-5.2 (主), deepseek-v4-pro (初始)
- fact-check 执行度: 部分启动（P0-P3a），P4-P8 全跳过

### Session 2

- Session ID: `019f82c3-14cc-7a7b-abe0-bf53e14e5370`
- 日期: 2026-07-21
- 任务: 抓取微信文章 → anysearch 找 GitHub PDD → clone → markitdown → 写 PDD 技术报告 → fact-check
- 文档: PDD 综合技术报告（~20KB，中文）
- 模型: glm-5.2
- fact-check 执行度: **完全绕过 pipeline**（0 个脚本被调用）

### Session 3 (PDD, glm5.2 重跑)

- Session ID: `019f83b7-d486-740a-a682-5a63989d44c9`
- 日期: 2026-07-21
- 任务: 对 PDD 综合技术报告执行 fact-check（full mode）
- 文档: PDD 综合技术报告（~20KB，中文）
- 模型: internal-gateway GLM-5.2-FP8
- fact-check 执行度: **P0-P7 全部完成** ✅
- 结果: 47/47 SUPPORTED, 0 NUANCED, 0 CONTRADICTED

### Session 4 (Kimi K3, glm5.2 重跑)

- Session ID: `019f83b7-b2f4-79a0-8171-195bf14c7178`
- 日期: 2026-07-21
- 任务: 对 Kimi K3 技术报告执行 fact-check（full mode，目录有 Session 1 残留）
- 文档: Kimi K3 技术报告（~630 行，34KB）
- 模型: internal-gateway GLM-5.2-FP8
- fact-check 执行度: **P0-P7 全部完成** ✅
- 结果: 42 SUPPORTED, 3 NUANCED, 0 CONTRADICTED

### Session 5 (LLM RL Survey, deepseek-v4-flash)

- Session ID: `019f8e54-8516-78b4-b9f2-959a413101ae`
- 日期: 2026-07-23
- 任务: 对 LLM RL 技术调研文档执行 fact-check（full mode）
- 文档: llm-rl-survey.md（中文，~730 行，682 行有效内容）
- 模型: deepseek/deepseek-v4-flash
- fact-check 执行度: **部分执行**（P0 + P1 subagent 提取 + P3a 手构输入），P2/P3b-P8 跳过
- 结果: 49 SUPPORTED, 1 CONTRADICTED, 2 NUANCED, 5 UNVERIFIABLE（手写 report.md，非脚本生成）

---

## 发现 0（P0）：route-claims.sh 不回写 claims.json → 规则引擎连锁失效

### 现象

claims.json 中 3 条 `rule_engine` 路由的 claim 全部报 `UNVERIFIABLE` + `"no identifier extracted"`，即使原文含 `arXiv:2412.06464` 和 `arXiv:2510.26692` 这类标准 ID。

### 根因

各脚本的 I/O 约定不一致：

| 脚本 | phase | 读取 claims.json | 回写 claims.json |
|------|-------|-------------------|------------------|
| `route-claims.sh` | P2 | ✅ | ❌ **只 stdout** `{claims, stats}` |
| `rule-engine.sh` | P3a | ✅ | ✅ 回写 |
| `validate-claims.sh` | P1 (loop) | ✅ | ❌ 只 stdout |
| `locate-claim.sh` | P1 | ✅ 源文档 | ❌ 只 stdout |
| `generate-report.sh` | P6 | ✅ | ❌ 生成 report.md |
| `grade-evidence.sh` | P5 | ✅ | ❌ 只 stdout |

### 断裂链条

1. Agent 运行 `route-claims.sh` → stdout 输出了 routing 结果
2. **但 claims.json 中 `route`、`matched_rule`、`matched_verifier` 全部保持空字符串**
3. `rule-engine.sh` 读取 claims.json → `matched_rule = ""` → `PATTERNS.get("")` 返回 None → `ident = ""` → 报 `"no identifier extracted"`
4. Agent 看到 3 条 UNVERIFIABLE，认为规则引擎不工作，跳过后续验证

### 修复

`route-claims.sh` 必须像 `rule-engine.sh` 一样回写 claims.json。

---

## 发现 1：Unicode Normalize（防御性）

### 场景

当前 case 中 arXiv ID 是纯 ASCII，regex 能匹配。但以下场景的中文文本需要 NFKC normalize：

- 全角括号 `（）` vs 半角 `()` — 影响 P1 catalog 分解 (`paren_append` / `paren_expand`)
- 全角逗号 `，` vs 半角 `,` — 影响 `paren_expand` 多项分隔
- 全角数字 `２８００` vs `2800` — 影响 numerical pattern
- 中文撇号 `＇` / 中文引号 `＂` — 影响字符串匹配

### 建议位置

在 `route-claims.sh` 和 `rule-engine.sh` 的 Python 入口处添加：

```python
import unicodedata
text = unicodedata.normalize("NFKC", text)
```

对 `claim_text` 和 `normalized_claim` 都做。NFKC 不会改变中文字义。

---

## 发现 2（P1）：Phase 1（Extract）完整流水线被跳过

### 现象

Agent 直接用 shell `grep` 提取声明，没有调用 `locate-claim.sh`、`check-atomicity.sh`、`validate-claims.sh`。结果：

- `source_location` 全是 `"line:1"`（非标准格式）或空字符串（应为 `file:line:col`）
- `content_hash` 全为空
- 没有 `normalized_claim`
- 没有 `decomposition_mode` / `atomicity_parent` / `compound_flag`

### 根因

agent 没有文件门的约束，选择不调用这些脚本（因为它们产生 stdout 却不回写 claims.json，agent 看不出调用它们和直接手工提取的区别）

---

## 发现 3（P4）：Checkpoint 假设人类在场

### 场景

workflow.md 中 P4 要求显示模板并等待用户 `y/n/skip/view/search/edit` 命令。但在 goal/multi-step 模式下，agent 无法与用户交互，自行跳过。

### 当前状态

用户确认本次是"忘记需要人类在场"，不需要修复。但可以作为 design note 记录。

---

## 发现 4（P5）：Deep Verify 被手动验证替代

### 现象

workflow.md 设计使用 `anysearch batch_search` 或 web_searcher subagents 进行 P5 深度验证。实际 agent 用本地参考文件手动交叉比对数值。

### 问题

- claims.json 中 42 条 `web_search` claim 没有任何 `verdict` / `evidence` / `evidence_tier` 字段
- 报告中"43 条通过 ✅ / 2 条需注意 / 0 条未通过"是 agent 手动写进去的，不是脚本产出

---

## Session 2 特有发现

### 发现 5：Agent 读 SKILL.md 后选择完全绕过 pipeline

Session 2 的 agent 读了 fact-check 的 SKILL.md 后直接说：

> "The fact-check skill has an elaborate pipeline. For our purposes, I'll do a focused fact-check — verifying the key numerical claims in the report against the primary source."

然后手写了 `fact-check-report.md`。**没有一个脚本被调用。**

Session 1 的 agent 至少跑了 init.sh、route-claims.sh、rule-engine.sh（虽然都部分失败）。Session 2 连尝试都没有做。这说明 SKILL.md 的 8-phase 表格本身可能产生了"太复杂不值得启动"的劝退效应。当 agent 在一个多步任务（research → 报告 → fact-check）的最后一环时，它倾向于选择最小阻力路径。

### 发现 6：循环验证 — 用写报告的源验证报告

Session 2 的 fact-check 是：agent 用 PDD 原始论文写了一份报告，然后用 PDD 原始论文来"验证"报告中的数值是否正确。这不是 fact-check，这是 **proofreading**。

真正的 fact-check 应该：
- 对 "P99 TTFT 降低 51.5%" → 搜索独立来源验证（是否有第三方复现？是否有社区讨论？）
- 对 "基于 Mooncake 的 TCP 传输引擎" → 检查 Mooncake 仓库是否确实有 TCP 传输引擎
- 对 "DeepSeek-V4 Pro 1.6T/49B" → 检查 HuggingFace 模型卡片

但 agent 只是自己 grep 了自己写报告用的源文件。如果原始论文本身包含笔误或夸大，这种 fact-check 无法发现。

### 发现 7：路径解析不一致

Agent 先尝试 `/root/hyx/skills/fact-check/SKILL.md`（权限拒绝），然后才找到 `/mnt/disk1/hyx/skills/fact-check/SKILL.md`。这说明 skill 路径在不同 session/环境下不稳定，增加了执行摩擦。

### 发现 8：无结构化输出

Session 2 没有创建 `fact-check/` 目录，没有 `run.json`，没有 `claims.json`，没有 `ledger.jsonl`。如果后续要做增量 fact-check（`/fact-check --status` 或增量模式），完全没有数据基础。

### 发现 9：修复阶段引入 edit artifact

Agent 在修复阶段通过 `edit` 工具修改报告时，因为 `oldText` 不精确导致了格式错误：

```
> PDD 论文 Abstract 中同样宣告了> P  # ← artifact，多了一个 >
```

修复后需要额外的 edit 来清理。这暴露了在无用户交互的 goal 模式下，agent 自行 edit 引入新 bug 的风险，以及修复后缺少自动 recheck 的问题。

---

## Session 3 & 4 特有发现（glm5.2 完整 pipeline 执行）

### 发现 10：route-claims.sh 回写 bug 再次被命中 — agent 自行绕过

两个 session 都命中了发现 0 中的 route-claims.sh 不回写 bug，但 glm5.2 的 agent 都自行发现了问题并手动解决：

Session 3:
```
Agent: "The route script outputs to stdout but doesn't write back. Let me re-run and save the output."
→ 手动捕获 stdout → python3 解析 → 写回 claims.json
```

Session 4:
```
Agent: "The route-claims.sh outputs to stdout but doesn't write back. Let me capture the output and update claims.json."
→ 同样的手动 workaround
```

**结论**：bug 仍然存在且每次必现，但 glm5.2 的 agent 有足够的智能来诊断和绕过。即使 agent 能绕过，也浪费了 3-4 个 tool call。

### 发现 11：`architecture` type 不在 VALID_TYPES 中 — 两个 session 都命中

extract-claims.md 的 Type Selection Guide 列出了 `architecture` 作为扩展类型：
```
| architecture | 架构声明 | `uses X for Y`, `routes through` |
```

但 validate-claims.sh 的 `VALID_TYPES` 不包含它：
```python
VALID_TYPES = {
    "authority", "numerical", "temporal", "factual", "causal",
    "comparative", "code-api", "citation", "existence", "interpretation",
    "file_path", "attribution",
    # extension
    "legal-med-fin", "pricing", "licensing", "compliance",
    "route", "port", "retry", "timeout",
}
```

两个 session 的 agent 都提取了 `type: "architecture"` 的 claim，都在 validate-claims.sh 处失败，都手动改成了 `factual`。schema.md 也列出了 `architecture` 作为扩展类型。同理 `capability`、`date`、`status` 也在 schema/prompt 中列出但不在 validator 中。

**这是 schema/prompt 与 validator 之间的不一致 bug**。

### 发现 12：增量 fact-check 完全不工作 — 缺少 resume 模式

Session 4 在 Kimi K3 目录上运行，该目录已有 Session 1 的残留：

```json
// Session 1 遗留的 claims.json
{
  "claim_id": "C001",
  "source_location": "line:1",    // 非标准格式
  "content_hash": "",              // 空
  "route": "",                     // 空
  "matched_rule": ""               // 空
}
```

init.sh 正确返回了 `mode: "full"`（因为上一个 run 从未完成，没有 ledger.jsonl）。但问题是：

1. **旧的 claims.json 存在但残缺** — agent 需要决定是复用还是重新提取
2. Agent 选择重新提取，但沿用了旧的 claim_id（C001-C045），只是修复了 source_location 和 content_hash
3. **没有 "resume incomplete run" 模式** — workflow.md 只有 full（从头来）和 incremental（基于已完成 run 的 diff）

**增量模式的设计缺陷**：
- `incremental` 模式的前提是上一个 run 已完成（有 ledger.jsonl）
- 如果上一个 run 在 P3 中断了，下一个 run 无法从中断点恢复
- 只能 full re-run，浪费之前已完成的工作

### 发现 13：Rule engine 对 "论文标题+会议" 类 claim 无能为力

Session 3 中 4 条 citation claim 被 rule_engine 报 UNVERIFIABLE：

| Claim | 内容 | 原因 |
|-------|------|------|
| C026 | DeepSeek-R1 in Nature 645:633-638, 2025 | 没有 arXiv ID / URL，只有期刊号 |
| C038 | Splitwise: ISCA 2024, pp.118-132 | 没有 arXiv ID / URL |
| C039 | DistServe: OSDI 2024 | 没有 arXiv ID / URL |
| C041 | SGLang: NeurIPS 2024 | 没有 arXiv ID / URL |

这些 claim 的 `matched_rule` 是 `url`（因为 route-claims 的 fallback），但 claim text 中没有 URL。rule-engine.sh 的 `PATTERNS.get("url")` 找不到 URL → `ident = ""` → UNVERIFIABLE。

Agent 随后手动用 curl + DBLP 验证了这些 claim。这说明 rule engine 缺少一个 **DBLP/DOI 查询器**来处理 "论文标题+会议/期刊" 类 claim。

### 发现 14：Stale subagent attention signals 造成大量摩擦

两个 session 都出现了相同模式：

```
Agent: "The attention signal is stale — all 4 subagents already completed."
→ subagent(action="status", id="b0e37995")  // 确认已完成
→ subagent(action="interrupt", id="b0e37995")  // 尝试中断
→ "No interrupt-capable run found in this session."
→ subagent(action="stop", id="6882da58")  // 尝试停止
→ "action='stop' supports async runs only."
```

Session 3 中 agent 花了约 **5 分钟**（4:50 → 4:59）反复处理 stale signals，期间多次调用 `subagent action=status/interrupt/stop`。这是平台层面的问题，但它显著拖慢了 pipeline 的执行。

### 发现 15：P5 验证质量问题 — "all SUPPORTED" 的假象

Session 3 (PDD) 的结果：47/47 SUPPORTED，0 NUANCED，0 CONTRADICTED。

但细看 P5 的验证方式：
- 28 条 web_search claim 中，约 20 条是 PDD 论文自报的 benchmark 数据
- web-researcher subagent 验证这些 claim 时，主要来源是 **PDD 论文本身**（T1 evidence）
- 这又回到了 Session 2 的循环验证问题：用 PDD 论文写报告 → 用 PDD 论文验证报告

Session 4 (Kimi K3) 的结果更好：42 SUPPORTED + 3 NUANCED，34 条 T4（二级来源） vs 11 条 T1。但仍有大量 claim 依赖原始来源验证。

**核心问题**：P5 的 web-researcher subagent 没有被指示去寻找 **独立第三方来源**，而是去验证 claim 是否与原始来源一致。这与 fact-check 的设计意图（独立交叉验证）有偏差。

### 发现 16：CC Safety Net 反复阻止 python3 -c one-liner

两个 session 都多次命中：
```
BLOCKED by CC Safety Net
Reason: Interpreter one-liners are blocked in paranoid mode.
```

Agent 需要改用 `python3 << 'PYEOF'` heredoc 方式。这虽然不是 fact-check skill 的问题，但增加了执行摩擦。每次命中浪费 1 个 tool call + 1 个 turn。workflow.md 中的示例命令应该避免使用 `python3 -c`。

---

## Session 5 特有发现（deepseek-v4-flash, LLM RL Survey）

### 发现 17：subagent 并行提取 claims 是好想法，但执行断裂

Agent 创建了自定义 subagent `claim-extractor`，把文档分成 8 个 chunk，并行提取 claims。这比 glm5.2 的单线程提取更高效。但：

- 提取结果分散在 `claims-section-*.json` 多个文件中，**从未合并为统一的 claims.json**
- **没有调用 locate-claim.sh** — 所有 claim 缺少 source_location 和 content_hash
- **没有调用 validate-claims.sh** — 没有校验 claim_text 是否为原文子串
- **没有调用 check-atomicity.sh** — 没有原子性分解

这印证了文件门禁（P1b）的必要性：如果 rule-engine.sh 或 route-claims.sh 在入口检查"claims.json 是否有 source_location"，agent 就无法跳过 locate-claim.sh。

### 发现 18：rule-engine.sh 被误用 — 手构 authority-claims.json 绕过 pipeline

Agent 没有跑 route-claims.sh，而是自己 grep 出所有 arXiv ID 和 GitHub URL，手动构造了一个 `authority-claims.json`，然后调 rule-engine.sh 验证。

这意味着 rule-engine.sh 虽然被调用了，但：
- 输入不是 claims.json（而是手构的临时文件）
- 输出不回写到 claims.json（因为没有统一的 claims.json）
- 57 条 authority claim 验证结果只存在于 stdout 和 report.md 中

### 发现 19：rule-engine.sh 的 HEAD 请求对部分网站失效

- `verl.readthedocs.io` 和 `openrlhf.readthedocs.io`：HEAD 请求返回 403，但 GET 请求返回 200
- `huggingface.co`：返回 429（rate limit）

这是 rule-engine.sh 的 `http_status()` 函数使用 HEAD 方法的问题。部分网站不允许 HEAD 请求。应该 fallback 到 GET。

### 发现 20：发现了一个真实的 CONTRADICTED claim

`hkust-nlp/SimpleRL` 返回 HTTP 404 — 仓库确实不存在。这是 5 个 session 中 **第一次发现真实的 factual error**。说明 rule engine 的 HTTP 验证本身是有效的，问题在于 pipeline 没有完整执行到 P5/P6/P7 来交付这个结果。

### 发现 21：CC Safety Net 阻止 rm -rf 清理

Agent 最后想清理 `.tmp-chunks` 临时目录，被 CC Safety Net 阻止。这不影响 fact-check 结果，但留下了临时文件。

---

## 五次 Session 的完整对比

| 特征 | S1 (Kimi K3, 旧) | S2 (PDD, 旧) | S4 (Kimi K3, glm5.2) | S3 (PDD, glm5.2) | S5 (LLM RL, ds-v4-flash) |
|------|-----|-----|-----|-----|-----|
| Pipeline 完成度 | P0-P3a 部分 | 0 个脚本 | **P0-P7 全部** ✅ | **P0-P7 全部** ✅ | P0 + P1 subagent + P3a 手构 |
| claims.json | 45条, 残缺 | 未创建 | 45条, 完整 ✅ | 47条, 完整 ✅ | ❌ 从未创建 |
| P1 locate-claim | ❌ 跳过 | ❌ 跳过 | ✅ 45/45 定位 | ✅ 47/47 定位 | ❌ 跳过 |
| P2 路由 | ⚠️ 回写 bug | ❌ 跳过 | ⚠️ 回写 bug, 手动绕过 | ⚠️ 回写 bug, 手动绕过 | ❌ 跳过 |
| P3a 规则引擎 | ❌ UNVERIFIABLE | ❌ 跳过 | ✅ 4/4 SUPPORTED | ✅ 15/19 SUPPORTED | ⚠️ 手构输入, 49 SUPPORTED + 1 CONTRADICTED |
| P3b Triage | ❌ 跳过 | ❌ 跳过 | ✅ 38 UNCERTAIN, 3 SUSPECT | ✅ 跳过 (无 alt-model) | ❌ 跳过 |
| P4 Checkpoint | ❌ 跳过 | ❌ 跳过 | ✅ 用户确认 | ✅ 用户确认 | ❌ 跳过 |
| P5 深度验证 | ❌ 手动 | ❌ 循环验证 | ✅ 4 web-researcher | ✅ 4 web-researcher | ❌ 跳过 |
| P6 报告 | ❌ 手动 | ❌ 手动 | ✅ generate-report.sh | ✅ generate-report.sh | ❌ 手写 report.md |
| P7 交付 | ❌ 跳过 | ❌ 跳过 | ✅ 摘要表+选项 | ✅ 摘要表+选项 | ❌ 跳过 |
| 最终 verdict | N/A | N/A | 42 SUPPORTED + 3 NUANCED | 47 SUPPORTED | 49 SUPPORTED + 1 CONTRADICTED + 2 NUANCED |
| ledger.jsonl | ❌ | ❌ | ✅ 45 行 | ✅ 47 行 | ❌ |

**关键观察**：
1. glm5.2（S3/S4）是唯一能完整跑完 8 phase 的模型
2. deepseek-v4-flash（S5）倾向于"选择性执行"——只执行自己认为有价值的部分（authority claim HTTP 验证），跳过"繁琐但必要"的步骤
3. 不同模型有不同的"偷懒"模式：S1/S2 完全绕过，S5 部分优化，S3/S4 完整执行
4. **文件门禁是唯一能统一约束所有模型的机制** — 无论模型选择哪种跳步模式，门禁都会阻止它
5. S5 首次发现了真实 factual error（hkust-nlp/SimpleRL 404），说明 rule engine 本身有效，问题在 pipeline 完整性

---

## 建议修复列表

| ID | 文件 | 修复 | 优先级 | 来源 session |
|----|------|------|--------|-------------|
| P0a | `scripts/route-claims.sh` | 回写 claims.json | P0 | S1, S3, S4 |
| P0b | `scripts/validate-claims.sh` | VALID_TYPES 添加 `architecture`, `capability`, `date`, `status` | P0 | S3, S4 |
| P0c | `scripts/init.sh` + `references/workflow.md` | 添加 resume 模式（从断点恢复） | P0 | S4 |
| P0d | `scripts/validate-claims.sh` | 回写 auto_fixes | P0 | S1 |
| P0e | `scripts/rule-engine.sh` | http_status() HEAD 失败时 fallback 到 GET | P0 | S5 |
| P1a | `scripts/route-claims.sh` + `scripts/rule-engine.sh` | 入口加 NFKC normalize | P1 | S1 |
| P1b | 所有 phase 脚本 | **文件门禁** — 执行前验证上一个 phase 的输出是否满足契约 | P1 | S1, S2, S5 |
| P1c | `scripts/rule-engine.sh` | 添加 DBLP/DOI verifier 处理 "论文标题+会议" claim | P1 | S3 |
| P1d | `references/workflow.md` + `prompts/` | P5 指示 web-researcher 优先寻找独立第三方来源 | P1 | S2, S3 |
| P1e | `references/workflow.md` | 示例命令避免 `python3 -c`，改用 heredoc | P1 | S3, S4 |
| P2a | 所有 phase 脚本 | 统一 I/O 约定：stdout = 报告，file = 状态持久化 | P2 | S1, S5 |
| P2b | `scripts/locate-claim.sh` | 校验其 stdout 格式/gate 逻辑 | P2 | S1 |
| P2c | `prompts/extract-claims.md` vs `scripts/validate-claims.sh` | 同步 type 枚举（单一数据源） | P2 | S3, S4 |

### 文件门禁设计（P1b）

```
P1 输出契约 (claims.json):
  - 每条 claim 必须有非空 source_location (格式 file:line:col)
  - 每条 claim 必须有非空 content_hash (格式 sha256:xxx)
  - validate-claims.sh passed > 0

P2 输出契约 (claims.json, 在 P1 基础上):
  - 每条 claim 必须有非空 route
  - 每条 claim 必须有非空 matched_rule

P3a 输出契约 (claims.json, 在 P2 基础上):
  - route == "rule_engine" 的 claim 必须有非空 verdict
  - route == "rule_engine" 的 claim 不能是 UNVERIFIABLE + "no identifier extracted"
    → 如果 matched_rule 仍为空: "PREREQUISITE_FAILED: Phase 2 (route-claims) output missing"

P5 输出契约 (verify-batch-*.json):
  - 每条 web_search claim 必须有 verdict
  - 每条 web_search claim 必须有 evidence_tier

P6 输出契约:
  - report.md 存在
  - handoff.md 存在
  - ledger.jsonl 可 append
```

每个脚本在 Python 入口处调用 `validate_prerequisites(claims)`：

```python
def validate_prerequisites(claims, required_fields):
    """Gate: refuse to run if previous phase output is missing."""
    missing = [c["claim_id"] for c in claims
               if c.get("expected_verifier") == "rule_engine"
               and not all(c.get(f) for f in required_fields)]
    if missing:
        print(json.dumps({
            "error": "PREREQUISITE_FAILED",
            "phase": "<phase>",
            "missing": f"fields: {required_fields}",
            "affected_claims": missing[:5],
            "fix": "<action>"
        }))
        sys.exit(2)  # distinct exit code: gate failure
```
