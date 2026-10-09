# patterns — challenge-audit

诊断史条目沉淀于此。来源为知识提取（challenger 实战），非 diagnose 产物。

## P-001 评审员三类系统性缺陷 → 四轴设计依据

- 状态: absorbed-into-skill
- 根因: 知识提取
- 现象: 三个实战 session 观察到的评审报告缺陷形态——①虚报收口（声明"已修复"但 same-file sibling 同病行漏改，verified-but-unlanded 的藏身处；01a0aeb3 的 A1 prober 三态残留）②集体漏检的结构性原因（评审员逐文件扫描，缺跨文件认领者视角，跨文件归属洞成为盲区——once/readyCheck 零认领案例，7/9 战果来自漏检轴）③过度升级（terrain vs terrain 可机械对齐却拿去问用户，SQLite 裁定案例）
- 方案: 轴 A 特核 closure claims + same-file siblings；轴 B 以"source of truth 逐节扫无人认领"为方法；轴 C 以"权威来源声明可机械裁决"为判据——全部落入 SKILL.md
- 触发条件: 人工判定
- passCheck: SKILL.md 四轴各自携带对应缺陷形态的核查方法
- 证据: 01a0aeb3#2007,#2016-2017（四轴任务书+9/9 核实）; 01a11f50#282,#366（裁决论证证伪+流程过度设计审计）; 01a12025#198（challenger 裁定规则）
- 出现: 2026-10-10 知识提取（challenger 实战回写 review-spec 后独立成 skill）
