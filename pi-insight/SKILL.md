---
name: pi-insight
description: "诊断 pi 使用：分析 system prompt 组成、tool/skill 使用频率、给出精简建议。"
disable-model-invocation: true
---

# Pi Insight — 使用诊断

**Leading word:** _diagnose_ — 测量 system prompt 的组成和 tool/skill 的实际使用，找出可精简的部分。

## Prerequisites

- This skill's extension must be installed (provides `/insight-dump` command)
- Python3 available（helper script is stdlib-only）

## Key constraint

System prompt 是**全局共享**的，受 `~/.pi/agent/settings.json` 控制，**不会记录在 session JSONL 中**。因此 prompt 分析必须通过 `/insight-dump` 命令获取当前 system prompt。

## Reference

- 领域术语（Declared, Used, Zero-use, Cross-reference, prompt 结构段）定义在 `CONTEXT.md`
- 报告格式模板在 `REPORT_TEMPLATE.md`

## Flow

### Step 1: 准备诊断数据

让用户执行 `/insight-dump` 命令。该命令通过 extension API 获取当前 system prompt，写入：

```
~/.pi/agent/insight/system-prompt-dump.txt
```

如果用户说已经 dump 过，直接用该路径。

**完成条件：** `~/.pi/agent/insight/system-prompt-dump.txt` 文件存在且非空。确认后进入 Step 2。

### Step 2: 运行完整诊断

**只运行一次** `all` 子命令——它内部已完成 usage 扫描 + prompt 分析 + cross-reference：

```bash
python3 <SKILL_DIR>/scripts/analyze.py all \
  --sessions ~/.pi/agent/sessions \
  --limit 100 \
  --dump ~/.pi/agent/insight/system-prompt-dump.txt \
  --skills-dir ~/.pi/agent/skills
```

输出一个 JSON，包含：
- `usage`：session 统计、tool/skill 调用频率
- `prompt`：prompt 结构分段（行数/占比/字节数）、declared tools/skills、`skill_prompt_footprint`（每个 skill 在 prompt 中的实际行数/字节数）
- `cross_reference`：declared vs used vs zero_use 交叉比对
- `cross_reference.skills.zero_use_prompt_lines`：零使用 skill 的 **prompt 实际占用行数**（直接用于报告的节省估算）
- `cross_reference.skills.zero_use_prompt_kb`：零使用 skill 的 prompt 实际占用 KB
- `cross_reference.skills.zero_use_disk_lines`：零使用 skill 的完整 SKILL.md 磁盘行数之和（维护负担指标，非 prompt 节省）
- `cross_reference.skills.detail`：每个 declared skill 的明细表（prompt_lines, disk_lines, session_count, cmd_count, tag_count, status），已按 session_count 降序排列，直接用于报告

**完成条件：** JSON 输出包含 `usage`、`prompt`、`cross_reference` 三个顶层 key，且 `cross_reference.skills.zero_use_prompt_lines` 和 `cross_reference.skills.detail` 存在。确认后进入 Step 3。

### Step 3: 产出诊断报告

基于 JSON 输出，按 `REPORT_TEMPLATE.md` 的格式生成结构化 Markdown 报告，保存到 `~/.pi/agent/insight/insight-report.md`。填充所有占位符为 JSON 中的实际数据。

按分类阈值划分 tool/skill 级别：

| 级别 | session 覆盖率 | 总调用 | 建议 |
|------|-------------|--------|------|
| 极高 | ≥80% sessions | — | 保留 |
| 高 | ≥30% sessions | — | 保留 |
| 中 | ≥10% sessions | — | 保留 |
| 低 | <10% sessions | — | 精简描述 |
| 零使用 | 0 sessions | — | 移除（历史也 0 则确定移除） |

**完成条件：** 报告包含全部六个章节（结构概览、频率分析、Skills 分析、精简建议、保留清单、注意事项），所有表格填充 JSON 数据，文件已保存到 `~/.pi/agent/insight/insight-report.md`。

## Guardrails

- 只出报告和建议，不修改任何 pi 配置文件
- 功能性必需的工具（如 subagent_wait, goal_complete）即使低频也保留
- MCP 工具不在 system prompt 中声明，不在统计范围内
