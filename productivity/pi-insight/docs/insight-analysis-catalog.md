# Pi Insight 扩展分析维度目录

> 6 个第三方 pi insight 扩展提供的完整分析维度清单，按类别分组。
> 每个维度标注来源、计算方式和输出位置。

---

## A. 确定性统计（无 LLM，纯解析）

### A1. 会话基础指标

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| 会话总数 | observal, supi, ygncode, diwu | 计数扫描到的 .jsonl 文件 | 概览卡片 |
| 有效会话数 | observal, supi | 过滤 ≥2 user msg + ≥1 min + 非 warmup-only | 概览卡片 |
| 日期范围 | observal, supi, ygncode, diwu | min/max(session.start_time) | 概览卡片 |
| 活跃天数 | observal, supi | unique(session.start_time.date) | 概览卡片 |
| 总时长 | observal, supi, ygncode, diwu | Σ(session.end_time - session.start_time) | 概览卡片 |
| 平均会话时长 | ygncode | total_duration / total_sessions | 概览卡片 |
| 日均时长 | observal | total_duration_hours / days_active | 概览卡片 |
| 消息总数 | observal, supi, ygncode, diwu | Σ(user_msg + assistant_msg) | 概览卡片 |
| 每会话平均消息数 | observal, ygncode | total_messages / total_sessions | 概览卡片 |
| 日均消息数 | supi | total_messages / days_active | 概览卡片 |
| 用户消息数 | observal, supi, ygncode, diwu | 计数 role=user 且有内容 | 概览卡片 |
| Assistant 消息数 | observal, supi, ygncode, diwu | 计数 role=assistant | 概览卡片 |
| 工具结果数 | diwu | 计数 role=toolResult | 数值视图 |
| 首条 prompt | observal, supi | 第一条 user 消息前 300 字符 | 会话摘要 |
| 末条 prompt | observal | 最后一条 user 消息前 200 字符 | 会话摘要 |

### A2. Token 与成本

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| Input tokens | 全部 | Σ(msg.usage.input) | 概览卡片 |
| Output tokens | 全部 | Σ(msg.usage.output) | 概览卡片 |
| Cache read tokens | ygncode, diwu, 2008muyu | Σ(msg.usage.cacheRead) | 概览/详细 |
| Cache write tokens | ygncode, diwu, 2008muyu | Σ(msg.usage.cacheWrite) | 概览/详细 |
| Total tokens | 全部 | input + output + cacheRead (+ cacheWrite) | 概览卡片 |
| 总成本 | observal, ygncode, diwu, 2008muyu | Σ(msg.usage.cost.total) | 概览卡片 |
| 成本分解 | ygncode, 2008muyu | cost.input / cost.output / cost.cacheRead / cost.cacheWrite | 详细视图 |
| 按模型 token/成本 | observal, supi, ygncode, diwu, 2008muyu | 按 msg.model 分组聚合 | 模型排行 |
| 按 provider 分布 | ygncode, diwu, 2008muyu | 按 msg.provider 分组 | 模型详细 |
| Cache hit rate | 2008muyu | cacheRead / (cacheRead + input + cacheWrite) | footer/详细 |
| 按 provider cache hit rate | 2008muyu | 同上但按 provider 分组 | 详细视图 |
| 模型切换次数 | ygncode | 一个 session 内使用 >1 个模型 | 概览 |
| 今日总成本 | 2008muyu | 跨所有 session 当日 cost 汇总 | 静态方法 |
| 今日总 token | 2008muyu | 跨所有 session 当日 token 汇总 | 静态方法 |

### A3. 工具使用

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| 工具调用频率排行 | 全部 | 计数 toolCall.name | 条形图 |
| 工具错误总数 | observal, supi, ygncode, diwu, 2008muyu | 计数 toolResult.isError | 概览/详细 |
| 工具错误分类 | observal, supi | 按错误文本分类（Command Failed / User Rejected / Edit Failed / File Changed / File Too Large / File Not Found / Other） | 条形图 |
| 按工具错误率 | diwu, 2008muyu | errors / calls per tool | 详细视图 |
| 工具平均耗时 | 2008muyu | (tool_execution_end - tool_execution_start) / count | footer/详细 |
| 按工具平均耗时 | 2008muyu | 同上但按 toolName 分组 | 表格 |
| 工具结果大小 | 2008muyu | JSON.stringify(result).length | 表格 |
| 每轮工具调用数 | 2008muyu | turn_end event 的 toolResults.length | turn 记录 |
| 使用 subagent 的 session 数 | observal, supi | 检测 toolCall.name === "subagent" | 概览卡片 |
| 使用 MCP 的 session 数 | observal, supi | 检测 toolCall.name.startsWith("mcp__") | 概览卡片 |
| 使用 web search | supi | 检测特定工具 | 概览 |
| 使用 web fetch | supi | 检测特定工具 | 概览 |

### A4. 代码产出

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| 新增行数 | observal, supi | Σ(write tool content 的换行数 + edit tool newText 的换行数) | 概览卡片 |
| 删除行数 | observal, supi | Σ(edit tool oldText 的换行数) | 概览卡片 |
| 修改文件数 | observal, supi | unique(write/edit tool 的 path 参数) | 概览卡片 |
| 文件路径列表 | diwu | 从 toolCall 参数和 bash 命令中正则提取 | 日报 |
| 编程语言分布 | observal, supi | 从文件扩展名映射（.ts→TypeScript 等 20+ 映射） | 条形图 |
| Git commits | observal, supi | 检测 bash 命令包含 "git commit" | 概览卡片 |
| Git pushes | observal, supi | 检测 bash 命令包含 "git push" | 概览卡片 |

### A5. 用户行为模式

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| 用户中断次数 | observal, supi | 检测文本 "[Request interrupted by user" | 概览卡片 |
| 用户响应时间分布 | observal, supi | (user_msg.ts - prev_assistant_msg.ts)，2s~3600s 内有效 | 条形图 |
| 用户响应时间中位数 | observal, supi | median(user_response_times) | 数值 |
| 用户响应时间平均值 | observal, supi | mean(user_response_times) | 数值 |
| 消息时段分布（0-23h） | observal, supi, ygncode | 按 user message 的 getHours() 分桶 | 条形图 |
| 并行会话检测 | observal, supi | 30分钟窗口内不同 session 的 user message 重叠 | 概览卡片 |

### A6. 项目分布

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| 项目会话分布 | observal, supi, ygncode, diwu | 按 session.cwd 的 basename 分组 | 条形图/排行 |
| 项目 token/成本排行 | ygncode, diwu | 按 cwd 分组聚合 token/cost | 项目排行 |
| 项目消息数排行 | ygncode | 按 cwd 分组聚合消息数 | 项目排行 |
| 项目时长排行 | ygncode | 按 cwd 分组聚合时长 | 项目排行 |

### A7. 上下文健康

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| 压缩次数 | diwu, 2008muyu | 计数 compaction entry | 数值/详细 |
| 压缩前 token 总量 | diwu | Σ(compaction entry.tokensBefore) | 数值 |
| 压缩前最大 token | diwu | max(compaction entry.tokensBefore) | 数值 |
| 按会话压缩统计 | diwu | 按 session.file 分组 | 详细视图 |
| 当前上下文使用率 | 2008muyu | ctx.getContextUsage().percent | /stats 命令 |
| 当前上下文 token | 2008muyu | ctx.getContextUsage().tokens | /stats 命令 |
| 上下文窗口大小 | 2008muyu | ctx.model.contextWindow | /stats 命令 |

### A8. HTTP 与延迟

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| HTTP 4xx+ 错误数 | 2008muyu | after_provider_response event status≥400 | /stats 命令 |
| HTTP 错误详情 | 2008muyu | 记录 status + timestamp | 详细视图 |
| 工具平均延迟 | 2008muyu | avg(tool_duration_ms) | footer/详细 |

### A9. 独特确定性维度

| 指标 | 来源 | 计算方式 | 输出位置 |
|------|------|---------|---------|
| **Rage detection（脏话检测）** | ygncode | 30词词表正则匹配 user message | 条形图 |
| Rage 按模型分布 | ygncode | 按当前 model 分组 | 条形图 |
| Rage 按小时分布 | ygncode | 按消息小时分组 | 条形图 |
| Rage 按项目分布 | ygncode | 按 projectName 分组 | 条形图 |
| Rage 高频词排行 | ygncode | 按词频排序 top 20 | 条形图 |
| **Thinking level 分布** | ygncode | 解析 thinking_level_change event | 条形图 |
| **Stop reason 分布** | ygncode | 解析 msg.stopReason | 条形图 |
| **日均统计** | ygncode | 按日期分桶 sessions/messages/tokens/cost | 折线图 |
| **Dteam usage（子 agent 用量）** | diwu | 扫描 ~/.pi/agent/dteam-usage.jsonl | 数值视图 |
| Dteam 按 model 分组 | diwu | 按 record.model 分组 token/cost | 详细 |
| Dteam 按 tier 分组 | diwu | 按 record.activeTier 分组 | 详细 |
| Dteam worker 数 | diwu | unique(record.workerId) | 数值 |
| **Audit usage（goal agent 用量）** | diwu | 扫描 ~/.pi/agent/audit-usage.jsonl | 数值视图 |
| Audit 按 model 分组 | diwu | 按 record.model 分组 | 详细 |
| Audit attempt 数 | diwu | 计数 record | 数值 |

---

## B. LLM 语义分析（Facet Extraction）

### B1. 会话级 Facet（per-session LLM 调用）

| Facet | observal | supi | 可能的值 |
|-------|----------|------|---------|
| underlying_goal | ✅ | ✅ | 自由文本：用户本次会话的根本目标 |
| goal_categories | ✅ | ✅ | debug_investigate, implement_feature, fix_bug, write_script_tool, refactor_code, configure_system, create_pr_commit, analyze_data, understand_codebase, write_tests, write_docs, deploy_infra, warmup_minimal |
| outcome | ✅ | ✅ | fully_achieved, mostly_achieved, partially_achieved, not_achieved, unclear_from_transcript |
| user_satisfaction_counts | ✅ | ✅ | frustrated, dissatisfied, likely_satisfied, satisfied, happy, unsure, neutral, delighted |
| assistant_helpfulness | ✅ | ✅ | unhelpful, slightly_helpful, moderately_helpful, very_helpful, essential |
| session_type | ✅ | ✅ | single_task, multi_task, iterative_refinement, exploration, quick_question |
| friction_counts | ✅ | ✅ | misunderstood_request, wrong_approach, buggy_code, user_rejected_action, assistant_got_blocked, user_stopped_early, wrong_file_or_location, excessive_changes, slow_or_verbose, tool_failed, user_unclear, external_issue |
| friction_detail | ✅ | ✅ | 自由文本：一句话描述摩擦 |
| primary_success | ✅ | ✅ | none, fast_accurate_search, correct_code_edits, good_explanations, proactive_help, multi_file_changes, good_debugging |
| brief_summary | ✅ | ✅ | 自由文本：一句话——用户想要什么，是否得到 |
| user_instructions_to_assistant | ✅ | ❌ | 数组：用户给出的可复用指令（如"always show diffs before editing"） |

### B2. 聚合级 Facet（跨会话聚合）

| 聚合指标 | 来源 | 聚合方式 |
|---------|------|---------|
| 目标分类分布 | observal, supi | Σ(goal_categories)，observal 用衰减加权 |
| 达成度分布 | observal, supi | Σ(outcome)，observal 用衰减加权 |
| 满意度分布 | observal, supi | Σ(satisfaction)，observal 用衰减加权 |
| 帮助度分布 | observal, supi | Σ(helpfulness)，observal 用衰减加权 |
| 会话类型分布 | observal, supi | Σ(session_type)，observal 用衰减加权 |
| 摩擦类型分布 | observal, supi | Σ(friction_counts)，observal 用衰减加权 |
| 成功类型分布 | observal, supi | Σ(primary_success)，observal 用衰减加权 |
| 会话摘要列表 | observal, supi | 最近 50 条 {id, date, summary, outcome, helpfulness} |
| 摩擦详情列表 | observal, supi | 前 20 条 friction_detail 文本 |
| 用户指令集合 | observal | 前 15 条 user_instructions |

---

## C. LLM 叙事洞察（Insight Generation）

### C1. observal 的 8 个并行洞察 prompt

| 洞察 | prompt 要求 | JSON schema |
|------|-----------|-------------|
| **Project Areas** | 识别 4-5 个项目领域，每个含名称/会话数/描述 | `{areas: [{name, sessionCount, description}]}` |
| **Interaction Style** | 2-3 段分析用户交互风格（快速迭代 vs 详细规划？频繁中断 vs 放手运行？） | `{narrative, keyPattern}` |
| **What Works** | 3 个令人印象深刻的成功工作流 | `{intro, impressiveWorkflows: [{title, description}]}` |
| **Friction Analysis** | 摩擦分析（已解决 vs 持续），最多 2 已解决 + 3 持续 | `{intro, resolved: [{category, note}], ongoing: [{category, description, examples, severity}]}` |
| **Suggestions** | 配置建议 + 功能推荐 + 使用模式 + **停止做** | `{config_additions, features_to_try, usage_patterns, stop_doing}` |
| **On the Horizon** | 3 个未来工作流机会（自主工作流、并行 agent、自纠流水线） | `{intro, opportunities: [{title, whats_possible, how_to_try, copyable_prompt}]}` |
| **Fun Ending** | 一个 memorable 的人类时刻（不是统计数字） | `{headline, detail}` |
| **Model Efficiency** | 模型花费分析（overspend / underspend / quota_pressure） | `{summary, overspend_pattern, underspend_pattern, quota_pressure, recommendation, potential_savings_note}` |

### C2. observal 的 Synthesis prompt（At a Glance）

在 8 个洞察完成后，顺序调用一次 LLM 生成综合摘要：

| 部分 | 内容 |
|------|------|
| What's working | 用户独特风格 + 有影响力的成果 |
| What's hindering you | (a) assistant 侧失败 (b) 用户侧摩擦 |
| Quick wins to try | 具体的 pi 功能或工作流变更 |
| Ambitious workflows | 随模型进步将变得可行的工作流 |

### C3. supi 的 7 个并行洞察 prompt

与 observal 几乎相同，但用 TypeBox schema 验证返回 JSON：

| 洞察 | schema |
|------|--------|
| projectAreas | `Type.Object({areas: Type.Array({name, sessionCount, description})})` |
| interactionStyle | `Type.Object({narrative, keyPattern})` |
| whatWorks | `Type.Object({intro, impressiveWorkflows: [...]})` |
| frictionAnalysis | `Type.Object({intro, categories: [{category, description, examples}]})` |
| suggestions | `Type.Object({claudeMdAdditions, featuresToTry, usagePatterns})` — 注意没有 `stop_doing` |
| onTheHorizon | `Type.Object({intro, opportunities: [...]})` |
| funEnding | `Type.Object({headline, detail})` |
| atAGlance | 顺序生成，依赖前 7 个结果 |

### C4. diwu 的 AI 日报

diwu 的 AI 叙事不是 per-session facet，而是一个**日报级 LLM 调用**：

| 维度 | 内容 |
|------|------|
| 输入 | 结构化工作事实 JSON（脱敏后的 tasks/completed/outputs/risks/followUps/toolCounts/files） |
| 输出 | 按项目分组的 Markdown 日报，每个项目含 4 个三级标题 |
| 多语言 | 11 种语言的 prompt 和输出 |
| 回退 | AI 失败时用纯算法 Markdown 模板 |
| 缓存 | 日报 markdown 缓存到 DaySummary，历史天秒开 |
| 模型 | 支持配置指定模型 + fallback 模型 |

### C5. halrixx 的语用学分析

halrixx 用 5 个理论框架从当前会话提取"不成文规则"：

| 框架 | 检测内容 |
|------|---------|
| Grice Quality Maxim | 用户是否挑战过无根据的声明？ |
| Grice Quantity Maxim | 用户是否觉得信息太多或太少？ |
| SBI Feedback Model | 每次简短纠正暗示的 Situation-Behavior-Impact |
| Implicit Feedback | 用户的纠正揭示了什么默认期望？ |
| Relevance Theory | 用户的指令实际期望的任务范围 |

输出格式：每条规则含 `[Source Dialogue]` + `[Rule]` + `[Reasoning]` + `[Framework]`

---

## D. 时间感知分析（仅 observal）

### D1. 时间维度

| 分析 | 计算方式 | 输出位置 |
|------|---------|---------|
| **周环比 diff** | 本周 vs 上周的 sessions / avg_cost / errors_per_session / primary_model | "What Changed This Week" 卡片 |
| **轨迹检测** | 最近 10 个 session vs 之前的 avg_cost / avg_errors，判断 increasing/decreasing/stable | 轨迹标注 |
| **异常检测** | 滑动窗口（前 10 个），检测 cost > 3× avg 或 errors > 3× avg 的 session | 异常列表（最多 5 个） |
| **重大转换** | 从后向前扫描，检测 10-session 窗口内的模型切换 | 转换事件卡片 |
| **已解决摩擦** | 14 天前 vs 14 天内的 friction 类型差集 | 摩擦分析"Resolved"部分 |
| **持续摩擦** | 14 天内仍出现的 friction 类型 | 摩擦分析"Ongoing"部分 |
| **衰减加权** | 10 天半衰期的指数衰减，近期 session 权重更高 | 所有 facet-derived 图表 |
| **陈旧度** | |recent_avg_cost - flat_avg_cost| / flat_avg_cost | 内部指标 |

### D2. 模型效率分析（observal 独有）

| 分析 | 计算方式 | 输出位置 |
|------|---------|---------|
| 模型 tier 自动分类 | 按 cost-per-token 分位数分 high/mid/low/subscription | 模型详细 |
| **Overspend 检测** | high-tier 模型用于 simple 任务且成功 → 估算浪费 80% cost | Flagged Sessions |
| **Underspend 检测** | low-tier 模型用于 complex 任务且失败 → 估算浪费 100% cost | Flagged Sessions |
| **Quota pressure 检测** | 订阅制重型模型用于 simple 任务 → 建议用同订阅的轻量模型 | Flagged Sessions |
| **浪费成本估算** | Σ(各 flag 的估算浪费) | 概览卡片 |
| Subscription 检测 | cost < $0.01 且 token > 10K 且 message > 20 → subscription | 内部分类 |
| Cost-per-token 计算 | cost / (input + output) × 1000 | 模型详细 |

---

## E. 用户上下文感知（仅 observal）

| 收集项 | 来源 | 用途 |
|--------|------|------|
| AGENTS.md 规则 | 读 ~/.pi/agent/AGENTS.md，提取含 always/never/must/forbid 的行 | 避免建议已有规则 |
| 已安装 packages | 读 settings.json 的 packages 数组 | 避免建议已安装的包 |
| 已安装 skills | 扫描 ~/.pi/agent/skills/ 目录 | 避免建议已有 skill |
| 已安装 extensions | 扫描 ~/.pi/agent/extensions/ 目录 | 避免建议已有扩展 |
| 默认模型 | 读 settings.json 的 defaultModel | 在建议中引用实际模型名 |

---

## F. 日报与归档（仅 diwu）

| 功能 | 描述 |
|------|------|
| **日报生成** | 按天提取会话活动，生成结构化日报 |
| **自适应日界** | 根据用户时区自动确定日期边界 |
| **日报归档** | 日报 markdown 保存到文件，支持覆盖确认 |
| **日报缓存** | DaySummary 缓存，历史天秒开，今天保留最后一次 |
| **批量日报** | 支持一次生成多天日报 |
| **LLM 时间范围解析** | 用 LLM 解析自然语言时间范围（"上周"、"前三天"），失败回退规则解析 |
| **Obsidian 同步** | 日报同步到 Obsidian vault |
| **会话活动提取** | 从会话中提取任务/完成/产出/错误/阻塞/文件路径/工具调用 |
| **完成检测** | 正则匹配 "已完成/done/fixed/updated" 等完成信号 |
| **阻塞检测** | 正则匹配 "blocked/stuck/error/failed" 等阻塞信号 |
| **文件路径提取** | 从 toolCall 参数和 bash 命令中正则提取文件路径 |

---

## G. 实时监控（仅 2008muyu）

| 监控项 | Hook | 实时性 |
|--------|------|--------|
| Token/cost 累积 | `message_end` | 实时（debounce 500ms） |
| Cache hit rate | `message_end` 计算 | 实时 |
| 工具调用计时 | `tool_execution_start` + `tool_execution_end` | 实时 |
| 工具错误 | `tool_execution_end` 的 isError | 实时 |
| HTTP 错误 | `after_provider_response` status≥400 | 实时 |
| 上下文压缩 | `session_before_compact` | 实时 |
| 每轮工具调用数 | `turn_end` | 实时 |
| Footer 状态栏 | 所有事件汇总 | debounce 500ms |
| /stats 命令 | 5 个子命令 | 按需 |
| 今日跨会话汇总 | 静态方法读所有 .jsonl | 按需 |
| JSONL 持久化 | appendFileSync 每条记录 | 实时 |
| 会话恢复 | 从 JSONL 文件重载 | hot reload 时 |

---

## H. 输出格式与交互

### H1. HTML 报告

| 特性 | observal | supi | ygncode |
|------|----------|------|---------|
| 自包含（无外部依赖） | ✅ 内联 CSS/JS | ✅ | ✅ 内联 JS bundle |
| 暗色主题 | ✅ | ✅ | ✅ |
| Stat card 网格 | ✅ | ✅ | ✅ |
| 条形图 | ✅ barChart() | ✅ | ✅ React |
| 时段分布图 | ✅ timeOfDayChart() | ✅ | ✅ |
| 响应时间分布图 | ✅ responseTimeChart() | ❌ | ❌ |
| Contribution Calendar | ❌ | ❌ | ✅ React |
| 导航栏 | ✅ | ✅ | ✅ |
| 复制按钮 | ✅ copyFromBox() | ❌ | ❌ |
| Checkbox 选择配置 | ✅ copyAllConfig() | ❌ | ❌ |
| 复制全部提示 | ✅ | ❌ | ❌ |

### H2. TUI 面板（仅 diwu）

| 特性 | 描述 |
|------|------|
| L2 overlay 面板 | 使用 pi-tui 的 Container/Theme |
| 双视图切换 | [1] 数字视图 [2] 日报视图 |
| 异步加载 | 面板挂载后异步加载数据 |
| 加载状态 | 显示 loading title + body |
| 错误状态 | 显示 error title + body |
| 日报预览 | 前 12 行 + 提示信息 |
| Esc 退出 | matchesKey(data, "escape") |

### H3. Markdown 报告

| 实现 | 特点 |
|------|------|
| observal | 完整叙事 + 统计表格 + 模型花费表 |
| diwu | 按项目分组 + 四级标题结构 + 脱敏 |
| 2008muyu | /stats 命令的纯文本输出 + 表格 |

### H4. 实时 footer（仅 2008muyu）

```
cache: 45% | tools: 12 (avg 230ms) | errors: 2
```

---

## I. 跨仓库分析维度覆盖矩阵

| 维度类别 | observal | supi | ygncode | diwu | 2008muyu | halrixx |
|---------|----------|------|---------|------|----------|---------|
| 会话基础 | ✅ 完整 | ✅ 完整 | ✅ 完整 | ✅ 完整 | ❌ | ❌ |
| Token/成本 | ✅ | ✅ | ✅ 含cache | ✅ 含cache | ✅ 含cache | ❌ |
| 工具使用 | ✅ | ✅ | ✅ | ✅ | ✅ 含耗时 | ❌ |
| 代码产出 | ✅ 行数/文件/语言 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 用户行为 | ✅ 中断/响应时间 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 项目分布 | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 上下文健康 | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| HTTP/延迟 | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| 时间感知 | ✅ 独有 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 模型效率 | ✅ 独有 | ❌ | ❌ | ❌ | ❌ | ❌ |
| 用户上下文 | ✅ 独有 | ❌ | ❌ | ❌ | ❌ | ❌ |
| LLM Facet | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| LLM 叙事 | ✅ 8+1 | ✅ 7+1 | ❌ | ✅ 日报 | ❌ | ✅ 规则 |
| 日报/归档 | ❌ | ❌ | ❌ | ✅ 独有 | ❌ | ❌ |
| 实时监控 | ❌ | ❌ | ❌ | ❌ | ✅ 独有 | ❌ |
| Rage detection | ❌ | ❌ | ✅ 独有 | ❌ | ❌ | ❌ |
| Thinking/Stop | ❌ | ❌ | ✅ 独有 | ❌ | ❌ | ❌ |
| Dteam/Audit | ❌ | ❌ | ❌ | ✅ 独有 | ❌ | ❌ |
| i18n | ❌ | ❌ | ❌ | ✅ 独有 | ❌ | ❌ |
| 语用学分析 | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ 独有 |
