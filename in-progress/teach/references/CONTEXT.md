# Glossary — teach skill

教学领域的通用语言。agent 内部对齐导航隐喻（见 `~/skills/CONTEXT.md` Navigation Metaphor），学习者面保留教学词汇。

## 教学循环

- **Probe**: teach 的第一阶段。勘测两种地形——学科地形（要学什么）和理解地形（学习者当前会什么）——产出 `UNDERSTANDING-MAP.md`。两个子阶段：
  - **Intake**: 面对大主题（如整个代码库），先拆成可学的子域让学习者选定。对代码项目，拆解维度含概念、执行路径、代码实现、算法、边界。
  - **Calibration**: 在选定子域上，通过分级单选题+二分搜索测出学习者当前的理解边界。
  _Avoid_: assessment（太窄，只暗示 calibration），quiz（只是 calibration 的工具）
  _导航隐喻对应_: orient（勘测 terrain → 产出 bearing）

- **Plan**: teach 的第二阶段。产出学习依赖图（节点=要学的概念，边=前置依赖），标注 frontier（当前可学的节点）和 fog（能感觉到但还没法精确描述想学什么）。小主题存为 `PLAN.md`（workspace 内 Mermaid 图）；大主题（跨 session）升级为 wayfinder map（issue tracker）。
  _Avoid_: syllabus（太正式），curriculum（太重）
  _导航隐喻对应_: wayfind（画 map → frontier）

- **Teach**: teach 的第三阶段。沿依赖图一次一个节点地教学，每步配测验反馈。AFK 批量是 Teach 的一种执行策略（沿 Plan 一次性生成多课），不是独立模式。
  _Avoid_: lecture（单向），instruct（命令式）
  _导航隐喻对应_: traverse（沿 route 行走）

## 工件

- **UNDERSTANDING-MAP.md**: Probe 产出的结构化快照。记录每个子主题的掌握程度（会/不会/部分）。AFK 场景从笔记推断；交互式场景从测验测出。同一 schema，Plan 不关心来源。每次 Probe 覆盖更新（非追加）。
  _Avoid_: assessment report（太正式），knowledge graph（太重）

- **PLAN.md**: Plan 产出的学习依赖图。Mermaid 格式，含 frontier 标记和 fog 区。workspace 内文件，小主题用。大主题升级为 wayfinder map。
  _Avoid_: syllabus（太正式），roadmap（太宽泛）

- **session-log/**: 每次交互式教学追加一个文件（`0001-YYYYMMDD.md`），记录原始流水：探查了什么、教了什么、测验结果、学习者反馈。Plan 读它来决定下次教什么和何时停。
  _Avoid_: learning-records（那是 ADR 风格的提炼认知，不是流水）

## 双地形

- **Subject terrain**: 要学的代码/概念——对应导航隐喻的 terrain。Probe 的 intake 阶段勘测它。可复用 seam/landmark/waymark/gap 词汇。
  _Avoid_: codebase（太窄，不限于代码）

- **Understanding terrain**: 学习者当前掌握了什么——导航隐喻没有这个概念（代码库不需要"测它会不会"）。Probe 的 calibration 阶段勘测它。
  _Avoid_: knowledge level（太模糊）

## 接入点

- **Fact-check @ A**: lesson 生成后，对 `lessons/*.html` 跑 fact-check skill，产出 `lesson-XXX.factcheck.md`，有问题触发修正。
- **Fact-check @ B**: Plan 产出后，对依赖图和节点描述跑 fact-check——防止计划里藏了错误前提。
- **Viz-check**: lesson 含 `.drawio` 时，跑 drawio-skill 的 validate.py（悬空边/重复 ID/重叠）+ autolayout.py（Graphviz 布局），产出自检报告。不 spawn 读图子代理。
