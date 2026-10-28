# ADR-0005: 文档型 skill，只编排，透传原始工具输出

日期: 2026-10-28
状态: accepted

## 决策

三个关联决策：

1. **skill 形态 = 文档型**（SKILL.md 教 agent 按序跑三件套并解读结果），不写 review.sh 脚本入口。暂时文档型，后续使用多了再根据实际情况判断是否改造为脚本型（届时需遵循本仓 skill-authoring.md 的 Pipeline discipline 硬要求）。

2. **报告 = 原始工具输出透传**。skill 不做结构化报告、不做 --out 落盘、不对接 verdict.py——输出就是 bash -n / shellcheck / shfmt 各自的原始输出，由 agent 按 SKILL.md 的解读指引归类（error 阻塞 / warning 定谳建议）。

3. **不附 CI 软闸模板**。shellcheck CI 闸是使用方的工程决策（peer 曾自行在自己的 MR 上加过），不属于本 skill 交付物。

## 理由

- skill 的价值在「编排顺序 + severity 语义 + 误报定谳指引」这三样知识，工具输出本身已足够好，加工层（格式化报告）是没人要的灵活性（YAGNI）。
- 文档型启动成本最低，且 agent 每次跑都重新执行编排，天然灵活；等出现「多轮执行行为漂移」的实证再固化成脚本。

## 后果

- 同一批脚本重跑时输出格式可能因工具版本略有差异——可接受。
- 未来脚本化改造的触发信号：agent 跳步/漏跑某个工具、severity 判读不一致的实证 ≥2 次。
