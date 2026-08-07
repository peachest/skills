# Report Template

The profiler produces a markdown report with adaptive depth: always-on sections plus drill-down sections that appear only when significant bottlenecks are detected.

## Drill-down trigger

A job gets deep analysis when **either** condition is met:
- Its `step_script` section exceeds **60 seconds**
- Its duration exceeds **30%** of the pipeline wall-clock

If no job meets either threshold, the report stays at the overview level — no deep analysis, no suggestion table.

## Report skeleton

```markdown
## Pipeline #<ID> 耗时分析

**触发**: <commit message> (`<short sha>`)
**触发时间**: <created_at>
**状态**: ✅/❌ <succeeded>/<total> 成功
**总 wall-clock**: <duration>

### Job 耗时明细

| Stage | Job | 状态 | 允许失败 | 执行时长 | 排队时长 | 启动 → 完成 |
|---|---|---|---|---|---|---|
| <stage> | `<job name>` | ✅/❌ | 是/否 | <duration>s | <queued>s | <start> → <finish> |

<!-- 按启动顺序排列。最慢的 job 标记 🔴最长 / 🟡次长。 -->

### 关键路径

<stage A longest job> (<duration>) → <stage B longest job> (<duration>) = <total>s
（占 wall-clock 的 <percentage>%）

<!-- 关键路径是串行 stage 链上每个 stage 最慢 job 的耗时之和。 -->
<!-- 如果只有一个 stage，关键路径就是该 stage 的最慢 job。 -->

<!-- ↓ 以下 section 仅在触发 drill-down 时出现 ↓ -->

### 慢 Job 深度分析: `<job name>` (<duration>s)

#### Section 拆解

| Section | 耗时 | 占比 | 说明 |
|---|---|---|---|
| `prepare_script` | <n>s | <%> | Pod 调度 |
| `get_sources` | <n>s | <%> | git fetch + checkout |
| `restore_cache` | <n>s | <%> | 缓存恢复 |
| `step_script` | <n>s | <%> | 核心执行 |
| `archive_cache` | <n>s | <%> | 缓存保存 |
| ... | | | |

#### Sub-step 信号

<!-- LLM 从 signals JSON 中提炼的子步骤拆解。 -->
<!-- 数据来源: commands（执行了什么）、downloads（下载数量）、buildx_steps（构建步骤）、tool_timings（工具自报告计时）、sleep_occurrences（硬编码等待）、cache_operations（缓存行为） -->

| 子步骤 | 估计耗时 | 占 step_script | 说明 |
|---|---|---|---|
| <step name> | <n>s | <%> | <what it does> |

#### 瓶颈识别

1. 🔴 <bottleneck> — <why it's slow>
2. 🟡 <bottleneck> — <why it's slow>
3. 🟢 <minor issue> — <note>

<!-- 🔴 = 关键路径上的大瓶颈 -->
<!-- 🟡 = 有改善空间但非关键路径 -->
<!-- 🟢 = minor，记录但不紧急 -->

### 优化建议

| Job | 优化项 | 预估节省 | 优先级 | 方案 |
|---|---|---|---|---|
| `<job>` | <what to optimize> | ~<n>s | 🔴 | <how to fix> |

<!-- 预估节省标注为 "~" 表示粗略估计，基于经验而非精确测量。 -->
<!-- 按优先级排序：🔴 → 🟡 → 🟢。 -->
```

## Notes for the agent

- The report is always in Chinese (matching the reference session and user preference).
- Job table is sorted by start time, not by duration — the agent should identify the longest and mark it with 🔴最长 / 🟡次长 inline.
- The "关键路径" section should be one or two lines — just the chain of longest jobs per stage and the total.
- Sub-step timings in the deep analysis are **estimates** — the agent derives them from signals (command lines, tool timings, download counts) and section timestamps, not from precise per-command profiling. Mark them as "估计" in the table header.
- Suggestions should be specific and actionable: name the file and line if possible (e.g., "移除 `.gitlab-ci.yml` 第 198 行的 `sleep 10`"), not vague ("优化构建步骤").
- If the pipeline failed, note the failure but still analyze durations of successful jobs — the user may want to optimize before fixing the failure.
