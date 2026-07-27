# Matt Pocock Skills 写作风格分析

## 1. 核心设计哲学

### Predictability 是根 virtue
Skill 的唯一目的是从随机系统中榨取确定性——**同一流程**每次运行，而非同一输出。所有写作技巧都服务于这一目标。

### 两种负载取舍
- **context load** — model-invoked skill 的 description 常驻 context window 的代价
- **cognitive load** — user-invoked skill 需要人类记住它存在的代价
- 拆分 skill 总是花其中一种，所以拆分必须"值回票价"

## 2. 结构模式

### Frontmatter 纪律
```
--- 
name: <skill-name>
description: <一句话：做什么 + 触发条件>
disable-model-invocation: true  # user-invoked only
---
```
- description 对 model-invoked：包含丰富触发短语（"Use when..."）
- description 对 user-invoked：人类面向，一行摘要，剥离触发列表
- 大部分 engineering skill 是 user-invoked（`disable-model-invocation: true`）
- 少数 reference skill（code-review, tdd, diagnosing-bugs, codebase-design, prototype, research）是 model-invoked

### 信息层级（Information Hierarchy）
三档，从上到下：
1. **In-skill step** — SKILL.md 中的有序动作，每步以 completion criterion 结束
2. **In-skill reference** — SKILL.md 中的定义/规则/事实，按需查阅
3. **External reference** — 推到独立文件，通过 context pointer 触达

关键原则：**顶层保持可读**。能推下去的都推下去（progressive disclosure）。

### Step 结构
- 每步有 **completion criterion**：可检查的（agent 能判断 done vs not-done）+ 可穷尽的
- 模糊的 criterion 导致 **premature completion**（agent 跳步）
- 后续步骤可见会"拉"agent 提前结束当前步——解法是拆分（sequence cut）

### 文件组织
```
<skill-name>/
├── SKILL.md          # 主文件，steps + 核心 reference
├── GLOSSARY.md       # 术语表（可选，disclosed reference）
├── TEMPLATE.md       # 模板（可选，disclosed reference）
└── ...               # 其他 disclosed reference
```

## 3. 写作风格特征

### Leading Words（Leitwort）
- 用模型预训练中已有的紧凑概念词锚定行为：_tight_, _red_, _seam_, _tracer bullet_, _fog of war_
- 在文本中重复该 token（不是句子），积累分布式定义
- 在 description 中也用同样的词，使 invocation 更可靠
- 自造词要明确定义，但不招募 priors，代价更高

### 句法特征
- **声明式开头**：直接说是什么，不说"这个 skill 会..."。"A prototype is throwaway code that answers a question."
- **破折号定义**：用 — 给出精确定义。"**Seam** — a place where you can alter behaviour without editing in that place"
- **_Avoid_ 标注**：每个术语后列出应避免的同义词，锁死语言。"Avoid: unit, component, service"
- **正面表述**：说"做什么"，不说"不做什么"（negation failure mode）。prohibition 只用于无法正面表述的硬约束
- **一句话原则**：每句通过 no-op 测试——删掉后行为是否改变？不变就删

### 段落结构
- 开头一句定位（leading word 或核心概念）
- 中间展开约束/规则
- 结尾给出 completion criterion 或行动指令
- 不写过渡句、不写"接下来我们将..."这类填充

### 引用其他 skill
- 用 `/skill-name` 散文式引用："Run the `/grilling` skill"
- **不**用 `../other-skill/FILE.md` 深层交叉引用
- 共享 reference 放在 owning skill 内，其他 skill 通过 invoke 到达

## 4. 流程型 Skill 的模式（triage, diagnosing-bugs, wayfinder）

### 通用骨架
```
1. 定位（一句话说 skill 是什么 + defining constraint）
2. 前置条件 / 参考文档
3. 核心概念/角色定义（reference tier）
4. 流程步骤（step tier，每步有 completion criterion）
5. 模板（disclosed 或 inline）
6. 边界情况 / 恢复模式
```

### triage 的五步流程
```
1. Gather context — 读全量信息 + 探索代码 + 两个检查
2. Recommend — 给建议 + 等指示
3. Verify the claim — 验证再动手
4. Grill (if needed) — 委托其他 skill 细化
5. Apply the outcome — 按结果执行动作
```
关键：**verify 在 grill 之前**——先确认事实成立，再花精力细化。

### diagnosing-bugs 的六阶段
```
1. Build a feedback loop (THE skill)
2. Reproduce + minimise
3. Hypothesise (3-5 ranked, falsifiable)
4. Instrument (one variable at a time)
5. Fix + regression test
6. Cleanup + post-mortem
```
关键：每阶段有 checkbox 形式的 completion criterion，且明确说"不满足则不前进"。

## 5. 参考型 Skill 的模式（codebase-design, writing-great-skills）

- 无 step，全是 reference
- 开头一句话定位
- Glossary 段落，每术语：定义 + _Avoid_
- 原则列表，每条一句话 + 可选示例
- 关系图（"A has exactly one B"）
- Rejected framings（明确说"不用 X，因为 Y"）

## 6. 从风格中提炼的写作清单

写一个新 skill 时检查：

- [ ] description 一行，含 leading word + 触发条件
- [ ] 开头一句话定位 + defining constraint
- [ ] 每步有可检查的 completion criterion
- [ ] 用 leading word 锚定核心行为
- [ ] 正面表述，prohibition 仅用于硬约束
- [ ] 术语后标 _Avoid_ 同义词
- [ ] 引用其他 skill 用 `/name` 散文式
- [ ] 能 disclose 的 reference 推到独立文件
- [ ] 每句通过 no-op 测试
- [ ] 无过渡句、无填充
