# 消费者视角反推：底座设计是否合理？

> 基于 subagent profiler 和 guardrail-optimizer 两个真实消费者的实现方案分析，
> 反思 session-profile 底座的设计决策。

---

## 消费者 1：Subagent Profiler

### 需求（来自 session 019fc5fb 的真实画像分析）

| 维度 | 具体数据 | 底座能否提供？ |
|------|---------|--------------|
| 模式分布 (SINGLE/PARALLEL/CHAIN/MGMT) | 392 calls: single 97, parallel 89, mgmt 119 | ✅ `ToolProfile.subagentPatterns.modeDistribution` |
| Sync/Async 比率 | sync 187, async 118 | ✅ `ToolProfile.subagentPatterns.asyncVsSync` |
| Agent 类型分布 | researcher 69, worker 15, reviewer 8 | ✅ `ToolProfile.subagentPatterns.agentDistribution` |
| 高级功能采纳 | worktree 0, turnBudget 0, ... | ✅ `ToolProfile.subagentPatterns.advancedFeatureAdoption` |
| **任务粒度** (task text 长度) | avg 1572 chars, median 1499 | ❌ **不在任何聚合中** |
| **通信渠道** (intercom actions) | send 10, reply 3, ask 1 | ❌ **只有 toolCounts，无 action 分布** |
| **通信渠道** (supervisor) | subagent_supervisor 3 calls | ❌ **同上** |
| **输出文件追踪** | 57 output files | ⚠️ 只有计数，无文件路径 |
| **Child session 指标** | 392 calls → 50 sessions, per-child tokens/cost | ❌ **linking 不完整**（见下文） |
| **Per-agent token/cost** | researcher 总 token, worker 总 token | ❌ **底座无此维度** |
| 结果质量 | LLM 语义分析 | ⚠️ Out of scope（正确） |

### 关键问题 1：Child session linking 设计错误

底座当前设计：
- `SessionMetrics.childSessionIds` — 从 subagent toolCall 的 `id` 参数提取
- `scanChildSessions(parentId)` — 遍历文件系统查找包含 parent ID 的目录

**实际数据流（从真实 session 验证）：**

```
1. Parent session 发起 subagent toolCall
   → toolCall.arguments 中没有 `id` 字段（spawn 调用没有 id）
   → `id` 字段只出现在 mgmt 调用上（status/wait/interrupt）

2. ToolResult 文本中包含完整 linking 信息：
   "Run: 1c276a38
    Children: 2 completed
    Sessions:
    - reviewer [completed]: <path>/1c276a38/run-0/session.jsonl
    - reviewer [completed]: <path>/1c276a38/run-1/session.jsonl"

3. 文件系统结构：
   <cwd-hash>/<timestamp>_<parent-id>/<run-id>/run-<n>/session.jsonl
   
4. Child session 有自己的 session ID（不同于 parent ID 和 run ID）
```

**底座的设计错误：**
- `childSessionIds` 从 toolCall `id` 提取 → 实际提取到的是 mgmt 调用的 run ID，不是 spawn 的 child session ID
- `scanChildSessions(parentId)` 遍历文件系统 → 可以工作但慢（O(n) per parent），且依赖目录名匹配 parent ID
- **真正的 linking 数据在 toolResult 文本中**，底座完全不解析

**应该怎样：**
```typescript
interface SubagentSpawnRecord {
  toolCallId: string;        // 关联 toolCall
  runId: string;             // 从 toolResult 解析（如 "1c276a38"）
  agent: string;             // 从 toolCall args
  mode: 'single' | 'parallel' | 'chain';
  async: boolean;
  taskText?: string;         // 从 toolCall args（single mode）
  taskTexts?: string[];      // 从 toolCall args（parallel mode）
  childSessionPaths: string[]; // 从 toolResult 解析
  childSessionIds: string[];   // 从 child session.jsonl header 读取
  outputFiles?: string[];    // 从 toolResult 解析
  intercomTargets?: string[];// 从 toolResult 解析
}
```

### 关键问题 2：Task text 丢失

Subagent profiler 需要分析 task 粒度（长度、内容模式）。底座的 `ToolProfile` 捕获了 mode/agent/async/feature adoption，但 **task text 在计数后即丢弃**。消费者必须 `parseSession()` 重新解析才能拿到 task text。

### 关键问题 3：通信渠道不完整

Subagent profiler 分析 intercom 和 supervisor 通信。底座的 `SessionMetrics.toolCounts` 有 `intercom: 17` 这样的计数，但没有 action 分布（send/ask/reply/list/status）。`ToolProfile.toolArgKeyProfiles` 记录了参数键，但不是值。消费者必须重新解析。

---

## 消费者 2：Guardrail Optimizer

### 需求（来自 scan_paths.ts 现有实现）

| 需求 | 底座能否提供？ |
|------|--------------|
| 按 project (cwd) 过滤 session | ✅ `scanSessions({ project })` |
| 获取每个 session 的 tool calls + arguments | ❌ **SessionMetrics 只有 counts，无 arguments** |
| 提取 bash 命令中的路径 | ❌ **需要原始 toolCall arguments** |
| 提取 read/write/edit 路径参数 | ❌ **同上** |
| Replay guardrail 逻辑判断 outside-cwd | ⚠️ 底座 out of scope（正确） |

### 关键问题 4：Guardrail-optimizer 完全不能用 SessionMetrics

Guardrail-optimizer 需要 **每个 tool call 的 arguments**（路径、命令文本）。`SessionMetrics.toolCounts` 只有 `{ bash: 1424 }` 这样的计数——arguments 在计数后即丢弃。

消费者必须：
1. `scanSessions({ project })` → 得到 SessionMetrics[]（**浪费**：guardrail-optimizer 不需要任何 SessionMetrics 字段）
2. 对每个 session 调用 `parseSession(path)` → 重新解析得到 raw entries
3. 从 raw entries 中提取 toolCall arguments

**步骤 1 完全是浪费。** Guardrail-optimizer 只需要 session 发现 + project 过滤 + raw entries，不需要预计算 metrics。

### Guardrail-optimizer 自己的 session 发现

现有 `scan_paths.ts` 自己实现了 `findSessionFiles()`：
- 按 cwd-hash 目录过滤
- 只扫描 `.jsonl` 文件（不递归子目录）
- 按 mtime 排序 + limit

底座的 `scanSessions({ project })` 做了同样的事，但还额外计算了 28 个 metrics 字段——这些对 guardrail-optimizer 全部无用。

---

## 跨消费者问题

### 关键问题 5：三重解析

当前设计下的解析路径：

```
scanSessions()     → parse each session → compute SessionMetrics → discard entries
toolProfile()      → re-parse each session → extract tool args → compute aggregates
消费者              → parseSession() → re-parse again → custom analysis
```

对于 100 个 session：3 × 100 = 300 次解析。
对于 1000 个 session：3000 次解析。

"不做缓存"的决策让每次调用独立，但代价是重复解析。如果底座在 `scanSessions()` 时保留 tool call 记录（轻量级，不是全量 entries），消费者就不需要重新解析。

### 关键问题 6：parseSession() 成为事实上的主要 API

三个已知消费者：
- **pi-insight**：主要用 SessionMetrics + crossSession（✅ 底座够用）
- **guardrail-optimizer**：必须用 `parseSession()`（SessionMetrics 完全不够）
- **subagent profiler**：必须用 `parseSession()`（SessionMetrics + ToolProfile 不够）

2/3 消费者的主要 API 是 `parseSession()`，不是 `scanSessions()` + `aggregate`。这意味着底座的核心价值（预计算 metrics + 聚合函数）对大多数消费者不是主要入口——`parseSession()` 才是。

---

## 设计反思与建议

### 问题 A：SessionMetrics 丢弃了消费者需要的原始数据

**根因**：SessionMetrics 在 scan 时聚合了 tool counts，但丢弃了 tool call arguments。2/3 消费者需要这些 arguments。

**建议**：`scanSessions()` 应同时返回轻量级 tool call 记录：

```typescript
interface ToolCallRecord {
  toolName: string;
  arguments: Record<string, unknown>;
  isError: boolean;
  timestamp: number;
}

interface SessionScanResult {
  metrics: SessionMetrics;
  toolCalls: ToolCallRecord[];  // 轻量级——只保留 tool calls，不含全量 entries
}
```

这样：
- guardrail-optimizer 直接用 `toolCalls` 提取路径，不需要 `parseSession()`
- subagent profiler 直接用 `toolCalls` 提取 task text / agent / mode，不需要 `parseSession()`
- 消除三重解析（scan 一次，所有消费者共用）
- `parseSession()` 仍然保留，供需要非 tool 数据的消费者使用

### 问题 B：Child session linking 需要重新设计

**根因**：当前从 toolCall `id` 提取 childSessionIds 是错误的——spawn 调用没有 `id`，linking 信息在 toolResult 文本中。

**建议**：新增 `SubagentSpawnRecord` 类型，从 toolCall + toolResult 配对解析：

```typescript
// 在 scanSessions() 中预计算
interface SessionScanResult {
  metrics: SessionMetrics;
  toolCalls: ToolCallRecord[];
  subagentSpawns: SubagentSpawnRecord[];  // 从 toolCall+toolResult 配对提取
}
```

`SubagentSpawnRecord` 包含 runId、agent、mode、taskText、childSessionPaths——消费者不需要自己解析 toolResult 文本。

### 问题 C："不做缓存"需要重新审视

**根因**：不做缓存的决策基于"消费者自己存 SessionMetrics[]"。但如果消费者还需要 toolCalls[] 和 subagentSpawns[]，他们要存三份数据——或者干脆只存 raw entries 自己算。

**建议**：不做缓存的决策可以保留，但 `scanSessions()` 的返回值需要更丰富。消费者存 `SessionScanResult[]`（metrics + toolCalls + spawns），覆盖 95% 的需求。`parseSession()` 只用于剩下 5% 需要 non-tool entry 类型的场景。

### 不需要改的

- **5 类聚合目录**：仍然合理，`aggregate.*()` 函数可以从 `SessionScanResult[]` 计算
- **纯函数 API**：仍然合理，`SessionScanResult` 是值对象
- **CLI 子命令**：仍然合理
- **child session opt-in**：仍然合理
- **时间趋势**：仍然合理
- **pi 类型复用**：仍然合理
- **JSON to stdout**：仍然合理

---

## 总结

| 设计决策 | 评估 | 调整 |
|---------|------|------|
| 5 类聚合 | ✅ 合理 | 不变 |
| 纯函数 API | ✅ 合理 | 不变 |
| 不做缓存 | ✅ 合理 | 不变 |
| pi 类型复用 | ✅ 合理 | 不变 |
| CLI 子命令 | ✅ 合理 | 不变 |
| **SessionMetrics 丢弃 tool call arguments** | ❌ **2/3 消费者需要重新解析** | **新增 ToolCallRecord[]** |
| **Child session linking 从 toolCall id 提取** | ❌ **数据源错误** | **从 toolCall+toolResult 配对提取 SubagentSpawnRecord** |
| **parseSession() 作为扩展点** | ⚠️ 成为主 API 而非补充 | **丰富 scanSessions() 返回值，parseSession() 退回补充角色** |
