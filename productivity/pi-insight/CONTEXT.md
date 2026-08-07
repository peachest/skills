# Pi Insight — 领域上下文

通过扫描 session JSONL 和分析 system prompt dump，诊断 pi agent 的配置臃肿问题——哪些 tool/skill 声明了但从未使用，哪些 prompt 段落占用过多空间。

## Language

### 数据采集

**System Prompt Dump**:
通过 `/insight-dump` 命令获取的当前完整 system prompt 文本，写入 `~/.pi/agent/insight/system-prompt-dump.txt`。获取方式见 SKILL.md Key constraint。
_Avoid_: prompt snapshot, prompt export

**Session Meta**:
从 session JSONL 文件中解析出的结构化使用统计。两个关键指标：**total_calls**（调用量——某 tool/skill 被调用了多少次）和 **session_count**（覆盖面——多少个 session 用过它）。分类阈值基于 session_count，不看 total_calls。纯确定性计算，无 LLM 调用。

**Installed Skill**:
`~/.pi/agent/skills/` 目录下的 skill，每个含 `SKILL.md`。扫描逻辑：先扫顶层目录，对没有顶层 `SKILL.md` 的目录递归查找子目录中的 `SKILL.md`（处理嵌套 skill 包，如 `domain-driven-design-skills/skills/ddd-contexts/`）。每个 skill 含 dir_name（目录名）、name（frontmatter 中的 name，可能与 dir_name 不同）、description、line_count（SKILL.md 磁盘行数）。Cross-reference 时按 name 和 dir_name 双向匹配，解决 prompt `<name>` 与磁盘目录名不一致的问题。

### 度量

**Prompt Footprint**:
一个 skill 在 system prompt 的 `<available_skills>` 段落中实际占用的行数和字节数——即其 `<skill>` 块的大小。与 SKILL.md 磁盘行数（line_count）不同：prompt 只携带 name + description + location（通常 5-10 行），而 SKILL.md 可能数百行。精简 prompt 的收益应按 Prompt Footprint 衡量，不是磁盘行数。
_Avoid_: skill size, skill lines（歧义——是 prompt 占用还是磁盘占用？）

### 分析维度

**Declared**:
在 system prompt dump 中声明的 tool 或 skill——出现在 prompt 文本中的。
_Avoid_: registered, configured

**Used**:
在最近 N 个 session 的 JSONL 中实际被调用过的 tool 或 skill。Tool 通过 `toolCall` block 的 name 检测；Skill 通过 `/skill:name` 命令和 `<skill name="...">` 标签检测。

**Zero-use**:
Declared 但未 Used 的 tool 或 skill——声明在 prompt 中占空间，但近期从未使用。是精简的首要目标。
_Avoid_: unused, dead

**Cross-reference**:
将 Declared 集合与 Used 集合做交集/差集，产出三类：used（声明且使用）、zero_use（声明但未使用）、not_declared_but_used（使用但未声明——是内置工具如 grep/ls，或通过 `/skill:` 命令触发的 skill；不占 prompt 空间，不受精简影响）。Zero-use 的节省有两个指标：**zero_use_prompt_lines**（Prompt Footprint 行数之和，是精简收益的真实衡量）和 **zero_use_disk_lines**（SKILL.md 磁盘行数之和，是维护负担指标，非 prompt 节省）。还输出 `detail[]` 数组：每个 declared skill 的 prompt_lines、disk_lines、session_count、cmd_count、tag_count、status，按 session_count 降序排列，直接用于报告。

### 输出

**Insight Report**:
基于 Session Meta + System Prompt Dump + Cross-reference 生成的 Markdown 报告，含结构概览、频率分析、精简建议（按优先级排序）、保留清单。报告由 agent 基于 `analyze.py` 的 JSON 输出生成，不是脚本直接输出的。

### Prompt 结构段

**Skills List**:
System prompt 中 `<available_skills>` 标签包裹的段落，包含所有已加载 skill 的 name + description。通常是 prompt 中占比最大的段落。

**Guidelines**:
System prompt 中 `Guidelines:` 标记后的段落，包含每个 tool 的详细使用规则。

**Tools**:
System prompt 中 `Available tools:` 标记后的段落，包含所有 tool 的 one-liner 描述。
