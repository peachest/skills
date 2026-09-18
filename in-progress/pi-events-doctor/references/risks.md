# 风险登记表（risk register）

daemon 已知风险与生产期检查信号。每次诊断回写 status 与日期；新风险当场入行。
裁定来源：#29 收口、#30 增量清单、orca 迁移研究（~/research/orca-migration/）。

| ID | 风险 | 触发信号（生产期可见症状） | 检查方法 | 缓解（已裁定） | status |
|---|---|---|---|---|---|
| R1 | 事件流无界增长 → 归约/FTS5 性能退化 | 单实体事件数 >阈值；states() 延迟上升 | `SELECT entity, COUNT(*) FROM events GROUP BY entity ORDER BY 2 DESC LIMIT 10;` + EXPLAIN QUERY PLAN | 快照机制（#30 裁定，性能触发再上） | design-stage |
| R2 | parked 积压 / 订阅者永久退场 | parked 行平均年龄持续上升；SESSION_START 不清空 | parked 行数与 age 分布；对照 session 启动记录 | dead-letter 即终态 + reckon 对账（#30） | design-stage |
| R3 | dead-letter 积压被遗忘 | dead-letter 行数增长无人处理 | dead-letter 清单按 reason 分组 | reckon 展示 + 本 skill 定期盘点 | design-stage |
| R4 | 采纳率低（agent 继续手写 sleep 轮询不 subscribe） | transcript 中 sleep/轮询模式 vs subscribe 调用比 | 抽样 sessions JSONL 统计两类模式出现频次 | usage examples + 冒烟自检；采纳率为不可验证行为假设，只观测 | design-stage |
| R5 | wake 失败 / 长连接断开未兜住 | accepted 停留时长分布右移；重试日志密集 | accepted→verified 间隔分位数；投递循环日志 | 退避 + parked 兜底（含 orca hibernation 断连场景） | design-stage |
| R6 | transcript adapter 格式漂移（harness-v2 v3→v4、lane 信封） | adapter 自检失败/降级日志；扫描命中率下降 | C1 启动自检结果；notificationId 扫描命中 vs 投递数 | 双形态 + 逐 session 分流 + C1 降级 | design-stage |
| R7 | profile 冲突拒绝误伤（合法订阅被拒） | 用户报告 subscribe 报错"实体属于其他 profile" | 拒绝日志按 profile 对统计 | 报错信息列出冲突 profile 与 key generator 来源（错误信息列选项惯例） | design-stage |
| R8 | op 面误用 / 冗余 op 无人用 | op 调用分布长尾；审计后被砍 op 仍有调用痕迹 | transcript 统计 10 op 各自频次 | op 审计表随 v2 spec 出（#30 B 节） | design-stage |
| R9 | 崩溃恢复缺陷（X1-X5 矩阵外路径） | daemon 重启后状态不一致、重复事件 | 重启后 reconcile：事件 id 唯一性 + appendIfMissing 生效检查 | 崩溃矩阵测试（层级 A/B/C） | design-stage |
| R10 | checker 执行面滥用（超长阻塞/凭证泄漏） | 执行日志中 10s+ 超时占比；token-pattern 拒绝触发 | B3 运行日志审计；拒绝记录复盘 | 超时 10s/并发 8/token-pattern 拒绝/审计走运行日志 | design-stage |

## 环境性风险（非 daemon 自身，迁移相关）

| ID | 风险 | 信号 | 出处 |
|---|---|---|---|
| E1 | orca 迁移后 agent status hooks 与 pi-hooks 注册表冲突 | daemon wake 注入失效/重复 | orca 研究 POC 清单 #2 |
| E2 | harness-v2 迁移改变 daemon 依赖的 transcript 契约 | #27 双维度重启条件触发 | #27、intent Risks |

## 维护规则

- status 取值：`design-stage | healthy | degraded | triggered | fixed(链接)`——进入实现期后首次诊断把 design-stage 逐行落成实测。
- 诊断日期与结论追加在行内 `[YYYY-MM-DD verdict: ...]`，不删历史。
