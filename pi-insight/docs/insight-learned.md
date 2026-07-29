# Pi Insight 扩展学习报告

> 从 6 个第三方 pi insight 扩展中提取的可复用模式、设计约定和最佳实践。
> 分析对象：`@observal/pi-insights`、`@mrclrchtr/supi-insights`、`@ygncode/pi-insights`、`pi-session-insights` (diwu)、`@2008muyu/pi-stats-insight`、`pi-session-insight` (halrixx)

---

## 1. 核心模式（跨仓库复现的结构/流程模式）

### 1.1 五阶段流水线 — 已成行业事实标准

**observal** 和 **supi-insights** 都采用完全相同的五阶段流水线，顺序一致：

```
Scan → Extract Meta → Extract Facets (LLM) → Aggregate → Generate Insights (LLM) → Render
```

| 阶段 | observal (`index.ts:2582+`) | supi-insights (`insights.ts:147+`) |
|------|------|------|
| Scan | `SessionManager.listAll()` | `scanAllSessions()` (scanner.ts) |
| Meta | `extractSessionStats()` 逐条解析 JSONL entries | `extractSessionMeta()` (parser.ts) |
| Facets | `callModel()` + 50 并发 | `extractFacets()` + 50 并发 (extractor.ts) |
| Aggregate | `aggregateData()` 含衰减加权 | `aggregateData()` (aggregator.ts) |
| Insights | 8 个并行 LLM prompt + 1 synthesis | `generateInsights()` (generator.ts) |

**关键洞察**：两个独立团队独立演化出了相同的架构。这证明了该流水线是 session analytics 领域的自然解法——**确定性统计先于 LLM 分析，两者分离缓存**。

### 1.2 确定性 Meta + LLM Facet 双层缓存

所有成熟实现都将数据分为两层，分别缓存：

| 层 | 内容 | 计算方式 | 缓存键 |
|----|------|---------|--------|
| **Meta** | 消息数、Token、工具调用、文件变更、语言分布 | 纯解析 JSONL，无 LLM | `session_id` (observal) 或 `session_id + path_hash + mtime_hash` (supi) |
| **Facets** | 目标分类、达成度、摩擦点、满意度 | LLM 调用 | 同上，但可 `--refresh` 强制刷新 |

**supi-insights 的缓存键更健壮**（`cache.ts` 的 `makeCacheKey`）：

```typescript
// supi-insights: cache.ts
function makeCacheKey(sessionId, path, modifiedMs) {
  // 包含路径哈希和修改时间哈希，防止 branched/resumed session 冲突
}
```

vs **observal 仅用 sessionId**，会在 session 文件被 fork/resume 时缓存过期数据。

**最佳实践**：缓存键应包含 `sessionId + 文件路径哈希 + 修改时间哈希`。

### 1.3 Session JSONL 解析模式

所有实现都面临相同的数据格式，但解析策略不同：

| 实现 | 解析方式 | 优点 | 缺点 |
|------|---------|------|------|
| observal | `SessionManager.open()` + `getEntries()` | 使用 pi 内置 API，最可靠 | 依赖 pi 版本 |
| supi-insights | `parseSessionFile()` 自行解析 | 独立可控 | 需跟踪格式变化 |
| ygncode | `createReadStream` + `readline` 逐行 | 内存友好，适合大文件 | 手动 JSON.parse |
| diwu | `createReadStream` + `createInterface` 逐行 + 并发 8 | 最高效，支持 mtime 过滤 | 代码复杂 |

**diwu 的扫描层最成熟**（`session-scan.ts`）：
- 并发 8 个文件扫描（`SCAN_CONCURRENCY = 8`）
- 支持 `modifiedSince` 增量扫描
- 串行化锁（`scanTail`）防止并发扫描冲突
- 容错解析：坏行跳过并记录错误，不中断

### 1.4 会话过滤管道

成熟实现都有多层过滤：

```
全部 sessions → 排除当前 session → 排除 meta-session（自己产生的）→ ≥2 user messages → ≥1 min duration → 非 warmup-only
```

**observal 的 meta-session 检测**（`index.ts:isMetaSession`）很巧妙——检测自身 LLM 调用产生的 session：

```typescript
function isMetaSession(entries) {
  // 检查前3条 user 消息是否包含 "RESPOND WITH ONLY A VALID JSON OBJECT"
  // 或 "record_facets" 或 "extract structured facets"
}
```

### 1.5 LLM 并发控制

| 实现 | 并发数 | 批量大小 | 策略 |
|------|--------|---------|------|
| observal | 50 (`FACET_CONCURRENCY`) | 10 (`LOAD_BATCH_SIZE`) | Promise.all 批处理 |
| supi-insights | 50 | 10 | 同上 |
| diwu | 8 | N/A | 文件扫描并发 |

**长 transcript 处理**：observal 和 supi 都用相同策略——超过 30K 字符时分块摘要再合并：

```typescript
if (transcript.length > 30000) {
  const chunks = splitInto(transcript, 25000);
  const summaries = await Promise.all(chunks.map(summarize));
  transcript = summaries.join("\n\n---\n\n");
}
```

---

## 2. 关键差异（实现分歧及其原因）

### 2.1 架构定位：Extension vs Skill vs Hybrid

| 实现 | 类型 | 触发方式 | LLM 调用 |
|------|------|---------|---------|
| observal | Extension | `/pi-insights` 命令 | ✅ 8+1 并行 |
| supi-insights | Extension | `/supi-insights` 命令 | ✅ 多 prompt |
| ygncode | Extension + React SPA | `/insights` 命令 | ❌ 纯统计 |
| diwu | Extension | `/insights` 命令 | ✅ 可选 AI 日报 |
| 2008muyu | Extension (hooks) | `/stats` 命令 + 实时 footer | ❌ 纯统计 |
| halrixx | Extension | `/insight` 命令 | ✅ 发送 prompt 到当前会话 |

**halrixx 最独特**——它不自己调 LLM，而是通过 `pi.sendMessage()` 把分析 prompt 注入当前会话，让 agent 自己执行：

```typescript
pi.sendMessage(
  { content: PROMPT + note, display: true },
  { triggerTurn: true }
);
```

这是一种 **"skill-like extension"** 模式——用 extension 注册命令，但执行逻辑交给 agent session。

### 2.2 输出格式：HTML vs Markdown vs TUI

| 实现 | 输出 | 自包含 | 交互性 |
|------|------|--------|--------|
| observal | HTML + Markdown | ✅ 内联 CSS/JS | 复制按钮、checkbox |
| supi-insights | HTML | ✅ | 自定义消息类型 |
| ygncode | HTML (React SPA) | ✅ 内联 JS bundle | 图表交互 |
| diwu | Markdown + TUI 面板 | ✅ | L2 overlay 面板，1/2 切换 |
| 2008muyu | 实时 footer + /stats | N/A | 状态栏 |
| halrixx | 会话内文本 | N/A | 直接在对话中输出 |

**observal 的 HTML 最精致**——暗色主题、stat card、bar chart、response time chart、time-of-day chart、copyable prompts、checkbox 选择配置项。

**ygncode 的 React SPA 最工程化**——Vite 构建、React 组件、Contribution Calendar、独立前端代码库。

**diwu 的 TUI 面板最 pi-native**——使用 `@earendil-works/pi-tui` 的 `Container`、`matchesKey`、`visibleWidth` 等原生组件：

```typescript
// diwu: panel.ts
import { matchesKey, truncateToWidth, visibleWidth } from "@earendil-works/pi-tui";
```

### 2.3 时间感知与趋势分析

**只有 observal 做了完整的时间感知**：

| 特性 | observal | 其他 |
|------|----------|------|
| 周环比 diff | ✅ `computeTemporalData()` | ❌ |
| 衰减加权（10天半衰期） | ✅ `decayWeight()` | ❌ |
| 轨迹检测（上升/下降/稳定） | ✅ | ❌ |
| 异常检测（3σ 成本/错误尖峰） | ✅ | ❌ |
| 重大转换检测（模型切换） | ✅ | ❌ |
| 已解决 vs 持续摩擦 | ✅ 14天窗口 | ❌ |

**observal 的衰减加权是核心创新**——让近期 session 对图表有更大影响：

```typescript
const HALF_LIFE_MS = 10 * 86400000;
const LAMBDA = Math.log(2) / HALF_LIFE_MS;
function decayWeight(meta) {
  const age = latestTs - new Date(meta.start_time).getTime();
  return Math.exp(-LAMBDA * age);
}
```

### 2.4 用户上下文感知

**只有 observal 读取用户现有配置**来避免重复建议：

```typescript
async function gatherUserContext() {
  // 读取 AGENTS.md 规则
  // 读取 settings.json 中的 packages
  // 读取 installed skills 目录
  // 读取 installed extensions 目录
}
```

然后在 suggestion prompt 中明确要求：
> "DO NOT suggest what's already present"

### 2.5 模型效率分析

**observal 独有的模型花费分析**——区分 PAYG 和订阅制：

| 检测 | 策略 |
|------|------|
| overspend | 高价模型用于简单任务且成功 |
| underspend | 低价模型用于复杂任务且失败 |
| quota_pressure | 订阅制重型模型用于琐事 |

模型 tier 自动分类：
```typescript
// 按 cost-per-token 分位数自动分 high/mid/low/subscription
const cptMedian = cptValues.sort(...)[Math.floor(cptValues.length / 2)];
if (cpt > cptMedian * 3) tier = "high";
else if (cpt < cptMedian * 0.4) tier = "low";
```

### 2.6 独特维度

| 实现 | 独特维度 | 代码位置 |
|------|---------|---------|
| ygncode | **Rage detection**（脏话检测） | `rage.ts` — 30 词的词表，按 model/hour/project 分组 |
| ygncode | **Thinking level 分布** | 解析 `thinking_level_change` event |
| ygncode | **Stop reason 分布** | 解析 `msg.stopReason` |
| ygncode | **Cache token 分离** | input/output/cacheRead/cacheWrite 四维 |
| diwu | **Context health**（压缩频率/量） | 解析 `compaction` entry 的 `tokensBefore` |
| diwu | **Dteam usage**（子 agent 用量） | 独立扫描 dteam-usage 记录 |
| diwu | **Audit usage** | 独立扫描 audit-usage 记录 |
| diwu | **i18n**（11 种语言） | `locale.ts` + 本地化标签 |
| diwu | **Obsidian sync** | `obsidian-sync.ts` |
| diwu | **日报归档** | `daily-archive.ts` + 自适应日界 |
| 2008muyu | **实时 footer** | hooks 驱动，debounce 500ms |
| 2008muyu | **工具耗时** | `tool_execution_start/end` 计时 |
| 2008muyu | **HTTP 错误监控** | `after_provider_response` 4xx+ |
| halrixx | **语用学分析** | Grice maxims + SBI + Relevance Theory |
| observal | **Multi-clauding**（并行会话检测） | 30分钟窗口内的会话重叠 |

---

## 3. 最佳实践与陷阱

### ✅ 最佳实践

1. **Meta 和 Facet 分离缓存** — Meta 永久缓存（纯确定性），Facet 可刷新（LLM 结果可能变）
2. **限制 facet 提取数量** — observal 和 supi 都设 `MAX_FACET_EXTRACTIONS = 50`，避免对 500+ session 全量调 LLM
3. **并发控制** — 50 并发 facet 提取 + 10 并发文件加载，平衡速度和 API 限流
4. **长 transcript 分块摘要** — 超过 30K 字符时分 25K 块摘要再合并
5. **排除自身产生的 session** — 检测 facet 提取 prompt 的特征文本
6. **文件权限 0o600** — `writeFile(path, data, { mode: 0o600 })` 保护用户数据
7. **容错解析** — 每行独立 JSON.parse，坏行跳过并记录，不中断整体扫描
8. **增量缓存** — diwu 支持 `modifiedSince` 只扫描新文件
9. **UI 进度反馈** — `ctx.ui.setWidget()` / `ctx.ui.setStatus()` 实时显示进度
10. **多语言支持** — diwu 支持 11 种语言的本地化标签

### ❌ 常见陷阱

1. **缓存键不含文件修改时间** — observal 仅用 `sessionId`，session 被 fork/resume 后缓存过期
2. **未处理 branched sessions** — 同一 sessionId 可能对应多个文件（分支），需要去重并选择"最佳"分支
3. **LLM 调用无超时** — diwu 设了 90s 超时，其他实现大多依赖 pi 的默认行为
4. **无 fallback 模型** — diwu 支持 `fallbackModel`，其他实现失败即跳过
5. **HTML 文件过大** — observal 单文件 ~2811 行 TypeScript 生成 HTML，可维护性差
6. **ygncode 首次运行需 npm install + build** — 用户体验差，需要预构建
7. **工具调用 ID 去重** — observal 用 `seenToolCallIds` 去重，其他实现未考虑 branched entries 的重复问题

---

## 4. 接口与契约

### 4.1 pi Extension API 使用

所有实现都通过 `pi.registerCommand()` 注册斜杠命令：

```typescript
export default function (pi: ExtensionAPI) {
  pi.registerCommand("insight", {
    description: "...",
    handler: async (args: string, ctx: ExtensionCommandContext) => {
      // ctx.model — 当前模型
      // ctx.ui.notify() — 通知
      // ctx.ui.setStatus() — 状态栏
      // ctx.ui.setWidget() — 自定义 widget
      // ctx.ui.confirm() — 确认对话框
      // ctx.sessionManager — 会话管理
      // ctx.modelRegistry — 模型注册表
      // ctx.cwd — 当前工作目录
    }
  });
}
```

### 4.2 LLM 调用方式

| 方式 | 使用者 | 代码 |
|------|--------|------|
| `@earendil-works/pi-ai` 的 `complete()` | observal, supi, diwu | 直接调底层 API |
| `ctx.modelRegistry.getApiKeyAndHeaders()` | observal, supi | 获取认证 |
| `pi.sendMessage({ triggerTurn: true })` | halrixx | 注入到当前会话 |
| `@mrclrchtr/supi-core/llm` 的 `callWithJsonResponse()` | supi | 封装+TypeBox schema 验证 |

**supi 的 `callWithJsonResponse` 最健壮**——用 TypeBox schema 验证 LLM 返回的 JSON：

```typescript
const FacetSchema = Type.Object({
  underlyingGoal: Type.String(),
  goalCategories: Type.Record(Type.String(), Type.Number()),
  // ...
});
const result = await callWithJsonResponse(ctx, { prompt, maxTokens: 4096, retries: 2 }, FacetSchema);
```

### 4.3 事件 Hooks（仅 2008muyu）

```typescript
pi.on('session_start', ...)
pi.on('message_end', ...)           // 提取 usage
pi.on('tool_execution_start', ...)  // 工具计时开始
pi.on('tool_execution_end', ...)    // 工具计时结束 + 错误记录
pi.on('session_before_compact', ...) // 压缩前 token 数
pi.on('after_provider_response', ...) // HTTP 4xx+ 错误
pi.on('turn_end', ...)              // 每轮工具调用数
pi.on('session_shutdown', ...)      // 清理
```

### 4.4 SessionMeta 字段对比

| 字段 | observal | supi | ygncode | diwu | 2008muyu |
|------|----------|------|---------|------|----------|
| session_id | ✅ | ✅ | ✅ | ✅ | ✅ |
| project_path | ✅ | ✅ | ✅ | ✅ | ❌ |
| duration | ✅ | ✅ | ✅ | ✅ | ❌ |
| user/assistant msg count | ✅ | ✅ | ✅ | ✅ | ❌ |
| tool_counts | ✅ | ✅ | ✅ | ✅ | ✅ |
| tool_errors | ✅ | ✅ | ✅ | ✅ | ✅ |
| input/output tokens | ✅ | ✅ | ✅ | ✅ | ✅ |
| cache tokens | ❌ | ❌ | ✅ | ✅ | ✅ |
| cost | ✅ | ❌ | ✅ | ✅ | ✅ |
| model_usage | ✅ | ❌ | ✅ | ✅ | ✅ |
| languages | ✅ | ✅ | ❌ | ❌ | ❌ |
| lines_added/removed | ✅ | ✅ | ❌ | ❌ | ❌ |
| files_modified | ✅ | ✅ | ❌ | ❌ | ❌ |
| git_commits/pushes | ✅ | ✅ | ❌ | ❌ | ❌ |
| user_interruptions | ✅ | ✅ | ❌ | ❌ | ❌ |
| user_response_times | ✅ | ✅ | ❌ | ❌ | ❌ |
| message_hours | ✅ | ✅ | ✅ | ❌ | ❌ |
| user_message_timestamps | ✅ | ✅ | ❌ | ❌ | ❌ |
| uses_subagent/mcp | ✅ | ✅ | ❌ | ❌ | ❌ |
| thinking_levels | ❌ | ❌ | ✅ | ❌ | ❌ |
| stop_reasons | ❌ | ❌ | ✅ | ❌ | ❌ |
| compaction | ❌ | ❌ | ❌ | ✅ | ✅ |
| tool_duration | ❌ | ❌ | ❌ | ❌ | ✅ |

### 4.5 SessionFacets 字段对比（LLM 提取）

| 字段 | observal | supi | halrixx |
|------|----------|------|---------|
| underlying_goal | ✅ | ✅ | ❌ |
| goal_categories | ✅ | ✅ | ❌ |
| outcome | ✅ | ✅ | ❌ |
| user_satisfaction | ✅ | ✅ | ❌ |
| assistant_helpfulness | ✅ | ✅ | ❌ |
| session_type | ✅ | ✅ | ❌ |
| friction_counts | ✅ | ✅ | ❌ |
| friction_detail | ✅ | ✅ | ❌ |
| primary_success | ✅ | ✅ | ❌ |
| brief_summary | ✅ | ✅ | ❌ |
| user_instructions | ✅ | ❌ | ❌ |
| unspoken_rules | ❌ | ❌ | ✅ (核心) |

### 4.6 存储路径

| 实现 | 数据目录 |
|------|---------|
| observal | `~/.pi/agent/usage-data/{meta,facets,report.html}` |
| supi-insights | `~/.pi/agent/supi/insights/{meta,facets,report-*.html}` |
| ygncode | `~/.pi/agent/insights-reports/pi-insights.html` |
| diwu | `~/.pi/agent/extensions/pi-session-insights/` |
| 2008muyu | 内存（不持久化） |

---

## 5. 文件地图

### @observal/pi-insights
```
pi-insights/
├── index.ts          # 全部逻辑——2811行单文件（解析+聚合+LLM+HTML+MD）
├── package.json      # 依赖 @earendil-works/pi-ai, pi-coding-agent
└── README.md
```
**特点**：单文件架构，无模块拆分，无测试。功能最完整但可维护性最差。

### @mrclrchtr/supi-insights
```
supi-insights/
├── src/
│   ├── insights.ts    # 命令注册 + 报告生成编排
│   ├── scanner.ts     # 会话扫描
│   ├── parser.ts      # JSONL 解析 + Meta 提取
│   ├── extractor.ts   # LLM Facet 提取
│   ├── aggregator.ts  # 跨会话聚合
│   ├── generator.ts   # LLM 叙事生成
│   ├── html.ts        # HTML 报告渲染
│   ├── cache.ts       # 双层缓存（Meta + Facet）
│   ├── types.ts       # 共享类型
│   ├── api.ts         # Extension API 封装
│   └── utils.ts       # 工具函数
├── __tests__/         # 单元测试（aggregator, utils）
├── CLAUDE.md          # 项目上下文
├── CONTEXT.md         # 领域模型
└── package.json       # 依赖 supi-core（配置/设置/LLM 封装）
```
**特点**：模块化最好，有测试，有领域文档。依赖 SuPi 生态。

### @ygncode/pi-insights
```
pi-insights/
├── index.ts           # Extension 入口（扫描+解析+生成报告）
├── lib/
│   ├── parser.ts      # JSONL 逐行流式解析
│   ├── analytics.ts   # 聚合引擎（日/项目/模型/工具/ragg）
│   ├── rage.ts        # 脏话检测（30词词表）
│   └── types.ts       # 类型定义
├── src/               # React SPA 前端
│   ├── App.tsx        # 主组件
│   ├── components/
│   │   └── ContributionCalendar.tsx
│   └── utils.ts
├── dist/              # 预构建产物
└── tests/             # 测试（parser, analytics, rage, utils）
```
**特点**：前后端分离，React SPA 前端，纯统计无 LLM。首次运行需 build。

### pi-session-insights (diwu)
```
pi-session-insights/
├── index.ts            # Extension 入口
├── src/
│   ├── insights.ts     # 命令编排（扫描→聚合→渲染）
│   ├── session-scan.ts # 会话扫描（并发8，增量，串行锁）
│   ├── usage-rollup.ts # K0 量纲聚合（纯函数）
│   ├── dimensions.ts   # K1-K5 多维聚合（纯函数）
│   ├── format.ts       # 格式化输出
│   ├── panel.ts        # TUI L2 overlay 面板
│   ├── report-*.ts     # 报告生成（markdown/ai-summary/redact/session-extract）
│   ├── daily-*.ts      # 日报（archive/command/config/options/orchestrator）
│   ├── time-range.ts   # 时间范围解析（LLM 优先 + 规则回退）
│   ├── obsidian-sync.ts # Obsidian 同步
│   ├── locale.ts       # i18n（11种语言）
│   └── types.ts        # 类型定义（最完整的类型系统）
├── doc/                # 设计文档（PRD/决策档案/术语表/路线图）
└── package.json
```
**特点**：文档最完善（7份决策档案），类型系统最完整，纯函数聚合层可测试，支持 TUI 面板。

### @2008muyu/pi-stats-insight
```
pi-stats-insight/
├── src/
│   ├── index.ts       # Extension 入口（hooks 注册）
│   ├── collector.ts   # 事件收集器（message_end/tool/compaction/error/turn）
│   ├── store.ts       # 内存存储
│   ├── footer.ts      # 状态栏更新
│   ├── commands.ts    # /stats 命令
│   ├── format.ts      # 格式化
│   └── types.ts       # 类型定义
└── package.json
```
**特点**：唯一实时监控方案，hooks 驱动，内存存储不持久化。最轻量。

### pi-session-insight (halrixx)
```
pi-session-insight/
├── index.ts           # Extension 入口（4行核心逻辑）
├── prompt.md          # 分析 prompt（Gricean pragmatics）
└── package.json
```
**特点**：极简——只发一条 prompt 给当前会话。不解析 JSONL，不调 LLM API。

---

## 6. 依赖与技术栈

| 实现 | 构建 | 测试 | LLM 调用 | UI | 特殊依赖 |
|------|------|------|---------|-----|---------|
| observal | 无构建（直接 .ts） | 无 | `@earendil-works/pi-ai` complete() | ctx.ui | 无 |
| supi | tsc | vitest | `supi-core/llm` callWithJsonResponse() | ctx.ui | supi-core, typebox |
| ygncode | Vite + React + tsc | vitest | 无 LLM | React SPA | React, Vite |
| diwu | 无构建（.ts 直接） | 无（有类型） | `@earendil-works/pi-ai` complete() | pi-tui | pi-tui |
| 2008muyu | tsup | 无 | 无 LLM | ctx.ui footer | 无 |
| halrixx | 无构建 | 无 | pi.sendMessage() | 会话内文本 | 无 |

**趋势**：大多数 pi insight 扩展不做编译，直接用 TypeScript 源码（pi 支持 jiti 运行时加载 .ts）。仅 ygncode 因 React SPA 需要 Vite 构建。

---

## 7. 跨仓库综合——给实现者的建议

### 7.1 如果做纯统计报告（无 LLM）

参考 **diwu** 的架构：
- `session-scan.ts` 的并发扫描 + 增量 + 串行锁
- `usage-rollup.ts` 的纯函数聚合
- `dimensions.ts` 的多维分析（项目/工具/错误/健康）
- `format.ts` 的格式化输出

### 7.2 如果做 LLM 增强报告

参考 **observal** 的流水线 + **supi** 的模块化：
- 五阶段流水线（Scan → Meta → Facets → Aggregate → Insights）
- 双层缓存（Meta 永久 + Facet 可刷新）
- 缓存键用 `sessionId + path_hash + mtime_hash`（supi 模式）
- LLM 调用用 schema 验证（supi 的 `callWithJsonResponse`）
- 衰减加权让近期数据更重要（observal 独创）
- 并发 50 facet 提取 + 8 并行 insight prompt

### 7.3 如果做实时监控

参考 **2008muyu** 的 hooks 架构：
- `message_end` → token/cost 收集
- `tool_execution_start/end` → 工具计时
- `session_before_compact` → 上下文健康
- `after_provider_response` → HTTP 错误
- debounce 500ms 更新 footer

### 7.4 如果做"从会话中学习规则"

参考 **halrixx** 的极简模式：
- 用 `pi.sendMessage({ triggerTurn: true })` 把 prompt 注入当前会话
- 让 agent 自己分析，不自己调 LLM API
- 适合 "unspoken rules extraction" 这类需要 agent 推理能力的场景

### 7.5 独特功能清单（可选择性吸收）

| 功能 | 来源 | 实现难度 | 价值 |
|------|------|---------|------|
| 衰减加权图表 | observal | 中 | ⭐⭐⭐ |
| 周环比 diff | observal | 低 | ⭐⭐⭐ |
| 异常检测 | observal | 中 | ⭐⭐ |
| 模型效率分析（PAYG vs 订阅） | observal | 高 | ⭐⭐⭐ |
| Multi-clauding 检测 | observal | 中 | ⭐ |
| 用户上下文感知（不重复建议） | observal | 低 | ⭐⭐⭐ |
| "Stop doing" 负面建议 | observal | 低 | ⭐⭐⭐ |
| Rage detection | ygncode | 低 | ⭐ |
| Thinking level 分布 | ygncode | 低 | ⭐ |
| Cache token 分离 | ygncode/diwu | 低 | ⭐⭐ |
| Context health（压缩频率） | diwu | 低 | ⭐⭐ |
| TUI L2 overlay 面板 | diwu | 高 | ⭐⭐ |
| 日报归档 + 自适应日界 | diwu | 中 | ⭐⭐ |
| i18n | diwu | 中 | ⭐⭐ |
| LLM 时间范围解析 | diwu | 中 | ⭐⭐ |
| 实时 footer | 2008muyu | 低 | ⭐⭐ |
| 工具耗时 | 2008muyu | 低 | ⭐⭐ |
| Schema 验证 LLM JSON | supi | 低 | ⭐⭐⭐ |
| Unspoken rules extraction | halrixx | 低 | ⭐⭐ |
| 可复制的 prompt 建议 | observal | 低 | ⭐⭐⭐ |
| Checkbox 选择配置项 | observal | 低 | ⭐⭐ |

### 7.6 Facet Extraction Prompt 最佳实践

observal 和 supi 的 facet prompt 几乎相同，核心要点：

1. **明确区分用户请求 vs agent 自主行为**："Count ONLY what the USER explicitly asked for"
2. **满意度基于显式信号**："Yay!" → happy, "thanks" → satisfied, "try again" → dissatisfied
3. **摩擦点要具体分类**：misunderstood_request, wrong_approach, buggy_code, user_rejected_action, excessive_changes
4. **warmup session 标记**：`warmup_minimal` 用于过滤无意义 session
5. **要求纯 JSON 输出**："RESPOND WITH ONLY A VALID JSON OBJECT"
6. **一句话摘要**：`brief_summary` — "what user wanted and whether they got it"

---

## 附录：仓库链接

| 包名 | 仓库 | 下载/月 |
|------|------|---------|
| @observal/pi-insights | https://github.com/BlazeUp-AI/pi-insights | 233 |
| @mrclrchtr/supi-insights | https://github.com/mrclrchtr/supi | 3,397 |
| @ygncode/pi-insights | https://github.com/ygncode/pi-insights | 133 |
| pi-session-insights (diwu) | npm: pi-session-insights | 279 |
| @2008muyu/pi-stats-insight | https://github.com/2008muyu/pi-stats-insight | 119 |
| pi-session-insight (halrixx) | https://github.com/halrixx/pi-session-insight | 474 |
