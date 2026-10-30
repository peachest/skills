---
name: pi-session-cleanup
description: >
  清理 pi agent 的 session 文件：删除测试/trivial session、陈旧 subagent session、
  旧单轮 session，回收磁盘空间。
disable-model-invocation: true
---

# Pi Session Cleanup

pi session 目录随时间膨胀到上千个文件、GB 级磁盘占用。大部分是两类废物：测试用的 trivial top-level session（`hi`/`hello`/`test`），和后台 subagent 跑完后不会在前台恢复的 session。本工具扫描全部 session，按策略分类，干跑预览后一次性删除。

## 前置

脚本位于本 skill 目录下的 `pi-session-cleanup.py`。

```bash
SCRIPT=~/skills/in-progress/pi-session-cleanup/pi-session-cleanup.py
```

## 步骤

### 1. 查看统计

```bash
python3 $SCRIPT --stats
```

确认 session 总数、磁盘占用、分布特征。判断是否需要清理。

**完成条件**：你看到了 session 总数和磁盘占用，决定是否继续。

### 2. 干跑预览

```bash
python3 $SCRIPT --verbose
```

查看哪些 session 会被清理、按什么策略、共多少个、回收多少空间。

调整参数控制清理范围（见下方参数表），反复干跑直到满意：

```bash
python3 $SCRIPT --age 14 --keep-recent 3 --verbose   # 更保守
python3 $SCRIPT --no-subagent --verbose               # 只清 trivial session
```

**完成条件**：干跑输出中的 "Sessions to clean" 数量和可回收空间符合你的预期。

### 3. 确认清理方案

将干跑结果整理为 summary 展示给用户，用 `ask_user_question` 询问：

- **是否执行删除？**（确认执行 / 调整参数后重新干跑 / 取消）

展示格式：

```
### 清理方案

| 策略 | 数量 | 可回收空间 |
|------|------|-----------|
| <策略名> | N | X.X MB |
| **合计** | **N** | **X.X MB** |

清理后剩余：N 个 session（X.X MB）
```

用户要求调整时，回到步骤 2 重新干跑。

**完成条件**：用户回复确认执行。

### 4. 执行删除

```bash
python3 $SCRIPT --execute
```

删除 session 文件并清理空目录。完成后输出实际删除数量和回收空间。

**完成条件**：终端输出 "Done!"，删除数量与干跑一致。

## 清理策略

| 策略 | 触发条件 | 默认参数 |
|------|---------|---------|
| trivial_top_level | top-level session 且内容为 hi/hello/test/doctor 等关键词，或 ≤5 行且 <5KB | — |
| old_subagent | subagent session 且超过 N 天未活跃 | `--age 7` |
| old_single_msg | top-level session、≤1 条用户消息、超过 N 天、且 <500KB | `--old-single-age 14` |
| tiny_session | 任意 session ≤3 行 | — |

所有策略共用 `--keep-recent` 保护期（默认 1 天）：活跃期内的 session 永不清理。

## 参数

| 参数 | 默认 | 作用 |
|------|------|------|
| `--execute` | 关 | 实际删除；不加则干跑 |
| `--age N` | 7 | subagent 清理的最小年龄（天） |
| `--old-single-age N` | 14 | 旧单轮 top-level 清理的最小年龄（天） |
| `--keep-recent N` | 1 | 保护最近 N 天活跃的 session 不被清理 |
| `--no-subagent` | — | 跳过 subagent 清理 |
| `--no-trivial` | — | 跳过 trivial top-level 清理 |
| `--no-old-single` | — | 跳过旧单轮 top-level 清理 |
| `--no-tiny` | — | 跳过 tiny session 清理 |
| `--stats` | — | 仅显示统计，不分析清理 |
| `--verbose` | — | 列出每个待清理 session 的详情 |
| `--sessions-dir PATH` | 自动检测 | 指定 session 目录 |

## 常用组合

**最安全**——只清 trivial 测试 session：

```bash
python3 $SCRIPT --no-subagent --no-old-single --execute
```

**标准清理**——清 trivial + 7 天+ subagent + 14 天+ 单轮：

```bash
python3 $SCRIPT --execute
```

**激进清理**——3 天+ subagent 全清：

```bash
python3 $SCRIPT --age 3 --execute
```

**保守清理**——14 天+ subagent，保留 3 天内活跃：

```bash
python3 $SCRIPT --age 14 --keep-recent 3 --execute
```
