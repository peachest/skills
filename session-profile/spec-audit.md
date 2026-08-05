# Spec #28 审计：证据来源与验收覆盖

## 一、证据来源审计

### ❌ 严重问题 1：SubagentSpawnRecord 的 toolResult 格式只覆盖 15% 的真实数据

**Spec 声称：**
> "The toolResult text format (verified from real sessions):"
> ```
> Delivered chain subagent results via intercom.
> Run: 1c276a38
> Children: 2 completed
> Sessions:
> - reviewer [completed]: <path>/1c276a38/run-0/session.jsonl
> ```

**实际数据（200 session, 562 spawn 结果）：**

| 类型 | 数量 | 占比 | 有 `Sessions:` 行？ | 有 `Run:` 行？ |
|------|------|------|---------------------|----------------|
| sync completed | 84 | 15% | ✅ | ✅ |
| async pending | 347 | 62% | ❌ | ❌ |
| error (Unknown agent / validation) | 124 | 22% | ❌ | ❌ |
| isError=true | 7 | 1% | ❌ | ❌ |

**Spec 的 SubagentSpawnRecord 类型声明 `childSessionPaths: string[]`——但 62% 的 spawn 调用（async）的 toolResult 根本没有 child session paths。** async toolResult 只有 `"Async: researcher [uuid]"`，child session paths 出现在后续的 mgmt 调用（status/wait）结果中，格式完全不同。

### ❌ 严重问题 2：Async 子会话是顶层 session，不是 child session

**Spec 声称（来自 CONTEXT.md）：**
> "Stored at `<timestamp>_<parent-id>/<run-id>/run-<n>/session.jsonl`"

**实际数据：**
- **Sync spawns**（single/parallel/chain）：child sessions 确实在 `<parent-dir>/<runId>/run-<n>/session.jsonl` ✅
- **Async spawns**：child sessions 是**顶层 .jsonl 文件**，不在 parent 目录下 ❌

验证：session 019facd0 有 4 个 async 子会话，全部是顶层 .jsonl 文件（通过 mgmt status 结果中的 `"Session: <path>.jsonl"` 确认），文件系统下无 `run-*` 子目录。

**影响：** `scanChildSessions(parentId)` 通过遍历文件系统查找 parent ID 目录——**会完全遗漏 async 子会话**。

### ❌ 严重问题 3：Spec 声称 "28 fields" 但未说明来源

**实际：** Prototype 的 `SessionMetrics` 有 29 个字段（prototype on branch `session-profile-prototype-22`）。#26 移除了 `childSessionIds`，变为 28 个。Spec 直接写 "28 fields" 但没有注明这是修订后的数量，也没有列出具体哪些字段被移除/新增。

### ⚠️ 中等问题 4：Consumer 分析只覆盖 2/3 消费者

Spec 声称 "3 known consumers"，但 `consumer-analysis.md` 只深入分析了 subagent profiler 和 guardrail-optimizer。pi-insight 被提及但没有做等深度的需求分析——只是说 "主要用 SessionMetrics + crossSession（✅ 底座够用）" 而未验证。

### ⚠️ 中等问题 5：toolResult 文本解析被当作可靠数据源

Spec 的 SubagentSpawnRecord 设计依赖从 toolResult **自由文本**中正则提取 `Run:`、`Sessions:`、`Artifacts:` 等信息。这是 pi 的内部输出格式，没有 API 契约保证，任何 pi 版本更新都可能改变格式。Spec 没有提到这个风险，也没有设计降级策略。

---

## 二、验收覆盖审计

### Spec 的 7 个 fixture 场景

1. ✅ Subagent spawn calls (single/parallel/chain) + toolResults
2. ✅ Tool calls (bash/read/write/edit) + toolResults
3. ✅ Compaction entries
4. ✅ Model changes + thinking level changes
5. ✅ User interruptions
6. ✅ No session header (starts with model_change)
7. ✅ Intercom/supervisor calls

### ❌ 缺失的 15 个场景

| # | 场景 | 严重性 | 原因 |
|---|------|--------|------|
| A | **Async spawn call — toolResult 格式不同** | 🔴 严重 | 62% 的 spawn 调用是 async，toolResult 无 Sessions: 行 |
| B | **Subagent error results (isError=true)** | 🔴 严重 | 23% 的 spawn 结果是错误，SubagentSpawnRecord 应如何处理？ |
| C | **Empty session (0 messages)** | 🟡 中等 | 边界条件 |
| D | **Session with no tool calls** | 🟡 中等 | 常见场景（纯对话 session） |
| E | **Malformed JSONL lines** | 🟡 中等 | 容错解析 |
| F | **zod validation failure** | 🟡 中等 | User story 43 要求 zod，但无测试场景 |
| G | **Child session discovery (async)** | 🔴 严重 | Async child sessions 是顶层文件，scanChildSessions 找不到 |
| H | **Parallel spawn with N tasks → N children** | 🟡 中等 | 多 child 验证 |
| I | **scanSessions with --project filter** | 🟡 中等 | 常见使用模式 |
| J | **scanSessions with --limit** | 🟢 低 | 简单截断 |
| K | **aggregate on empty sessions array** | 🟡 中等 | 边界条件 |
| L | **timeTrends with different --bucket values** | 🟢 低 | 参数化 |
| M | **Multiple compaction entries** | 🟢 低 | 累加逻辑 |
| N | **Session with branching (parentId chain)** | 🟡 中等 | pi session 有 tree 结构 |
| O | **Mgmt call results with Session: paths** | 🔴 严重 | Async child session linking 的唯一数据源 |

### ❌ User stories 缺失

| # | 缺失的 user story | 原因 |
|---|-------------------|------|
| ? | 作为消费者，我想获取 async spawn 的 child session paths | async toolResult 没有 child paths，需要从 mgmt 调用结果中提取 |
| ? | 作为消费者，我想处理 spawn 调用失败的情况 | 23% 的 spawn 结果是错误，SubagentSpawnRecord 应标记错误状态 |
| ? | 作为消费者，我想在 scan 结果中区分 sync 和 async spawn | async 的 child session 是顶层文件，linking 逻辑完全不同 |
| ? | 作为消费者，我想扫描空 session 不崩溃 | 边界条件 |
| ? | 作为消费者，我想在 JSONL 有坏行时跳过而非崩溃 | 容错解析 |

---

## 三、总结

### 证据来源评分

| 维度 | 评分 | 说明 |
|------|------|------|
| toolResult 格式 | ❌ 不充分 | 只验证了 1 个 session 的 1 种格式，实际有 4 种格式 |
| Child session 结构 | ❌ 不充分 | 只覆盖 sync child sessions，遗漏 async child sessions（62%） |
| Consumer 需求 | ⚠️ 部分充分 | 2/3 消费者深入分析，pi-insight 未验证 |
| SessionMetrics 字段 | ⚠️ 部分充分 | 数量准确但来源未注明 |
| Aggregate 设计 | ✅ 充分 | 从 6 个第三方扩展 + 真实数据分析提取 |

### 验收覆盖评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 正常路径 | ✅ 覆盖 | 7 个 fixture 覆盖主要场景 |
| 错误/边界 | ❌ 不足 | 缺少 15 个场景，3 个严重 |
| Async 处理 | ❌ 完全缺失 | 62% 的 spawn 调用无测试覆盖 |
| zod 验证 | ❌ 完全缺失 | user story 要求但无测试场景 |

### 建议

**Spec 需要修订才能交付实现：**

1. **SubagentSpawnRecord 需要重新设计**——区分 sync/async spawn，async 的 child session linking 从 mgmt 调用结果提取，不能只依赖 spawn toolResult
2. **scanChildSessions 需要支持 async child sessions**——不能只遍历 `run-*` 目录，还需从 mgmt 调用结果中提取顶层 session paths
3. **测试场景需从 7 个扩展到至少 15 个**——补充 async/error/empty/malformed/child discovery 等
4. **User stories 需补充 5+ 条**——覆盖 async spawn、error handling、empty session、malformed JSONL
5. **toolResult 文本解析需标注风险**——这是 pi 内部格式，无 API 契约，需设计降级策略
