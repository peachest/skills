# skill-impact — reckon

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| 提案 | 落点 | commit | 验证命令与结果 |
|------|------|--------|----------------|
| S1 position.sh：逐 worktree TSV 采集（upstream 链解析、/usr/bin/git、单调用覆盖全 worktree） | scripts/position.sh | 899ea13 | 冒烟：项目A 19 worktree + 项目B 9 worktree 全对，detached/双 remote/临时 worktree 均正确 |
| S2 mr-state.sh：glab api MR 状态（host 从 remote 推导，多实例 401 免疫；blocking 字段提取 Depends on） | scripts/mr-state.sh | 899ea13 | 冒烟：项目A MR open ✓、项目B MR merged ✓、项目C open 列表 ✓ |
| S3 frontier.sh：map→open/pending limbo 闭环态（map iid 过滤、Closes 提取） | scripts/frontier.sh | 899ea13 | 冒烟：项目A 双 map + pending limbo ✓、项目B #1 pending ✓、项目C 空输出（正确沉默）✓ |
| D1 注入即查询硬 gate + 三分支触发（首注/长隔/compaction→全量；新鲜位置→查询必做、输出按 diff 比例） | SKILL.md Cold start | 899ea13 | 待下轮 diagnose 验证 |
| D2 compaction 检测操作化（摘要在场/近期 turn 缺失即信号） | SKILL.md rule 4 | 899ea13 | 待下轮 diagnose 验证 |
| D3 map 行两结果正向表述（空结果→直接查下一数据源） | SKILL.md map 段 | 899ea13 | 待下轮 diagnose 验证 |
| D4 删 step n/m 模板字段 → 状态描述符 | SKILL.md rule 1 | 899ea13 | 待下轮 diagnose 验证 |
| D5 rule 3 锚行内容要求（项目+分支+待合并数） | SKILL.md rule 3 | 899ea13 | 待下轮 diagnose 验证 |
| R1 评审修订：三分支+rule4 坍缩为二元新鲜度测试（上一条位置陈述是否还在 context）；删 position.sh/mr-state.sh 死代码；修 frontier.sh 多号 Closes 只捕获首号 bug | SKILL.md + scripts | 921f910 | 单元回归：多号捕获 [45,109,110,113] ✓；三脚本重冒烟 ✓（MR merge 后 pending 自动清除=正确） |
