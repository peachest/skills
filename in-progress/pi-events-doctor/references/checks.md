# 检查项手册（checks）

> ⚠️ 占位状态：daemon 尚未实现，库路径/schema 以 v2 汇总 spec（#30）定稿为准。
> 本文件先固定"每条风险查什么"，SQL 在 schema 冻结后填实（标记 `TODO(schema)`）。
> 约定：`$DB` = daemon SQLite 库路径；`$SESS` = ~/.pi/agent/sessions。

## R1 事件流增长
```sql
-- TODO(schema): events 表名/字段按 v2 spec
SELECT entity_ref, COUNT(*) AS n FROM events GROUP BY entity_ref ORDER BY n DESC LIMIT 10;
SELECT MAX(event_seq) FROM events;  -- 总量趋势，每次诊断记录对比
```
判定：单实体 n > 1000 或总查询 P95 > 200ms → 建议启用快照。

## R2/R3 parked 与 dead-letter
```sql
-- TODO(schema)
SELECT state, COUNT(*), MIN(created_at), MAX(created_at) FROM deliveries GROUP BY state;
SELECT reason, COUNT(*) FROM deliveries WHERE state='dead-letter' GROUP BY reason;
```
判定：parked 平均年龄 > 7d 视为"永久退场"信号（对照 #30 裁定 3）。

## R4 采纳率
```bash
# 抽样近 N 个 session 文件，对比两类模式
grep -l 'subscribe(' $SESS/**/*.jsonl | wc -l
grep -l 'sleep [0-9].*&&.*\(glab\|kubectl\)' $SESS/**/*.jsonl | wc -l
```
判定：比值持续下降 → 采纳问题，升级为 issue。

## R5 wake 健康度
```sql
-- TODO(schema): accepted→verified 间隔分位数（两段式 ack 的黄金指标）
SELECT session_id, accepted_at, verified_at FROM deliveries WHERE state='verified' ORDER BY verified_at DESC LIMIT 100;
```

## R6 adapter 自检
```bash
# daemon 启动日志中 C1 自检行 + 降级标记
journalctl --user -u pi-events-daemon | grep -i 'adapter\|degraded\|self-check'
```

## R9 重启一致性
```sql
-- 事件 id 唯一 + 无重复 notificationId
SELECT COUNT(*) - COUNT(DISTINCT id) FROM events;  -- 期望 0
```

## R10 执行面审计
```bash
# B3 运行日志：超时占比 + token-pattern 拒绝
journalctl --user -u pi-events-daemon | grep -c 'timeout' ; \
journalctl --user -u pi-events-daemon | grep -c 'token-pattern'
```

## 诊断报告模板

每轮诊断输出：登记表逐行 verdict 表 + triggered/degraded 项的证据块 + 已执行动作 +
升级 issue 链接；确诊故障走 diag-write 入 ~/ops（标签建议：`pi-events-daemon`、`daemon-doctor`）。
