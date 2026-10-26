# Triage MR 评审轮次挖掘：diff 大小 vs 最佳 review 次数

- 日期：2026-10-26 ｜ 执行 session：herdr:agent w1:p2P（peer-fix-loop-cap worktree 内派发）
- 路由：session-mining script 路由（find-skill-sessions + find-tool-calls）→ GitLab API ground truth
- 数据文件：`~/tmp/triage-rounds/`（`mr-stats.json` 逐 MR 轮次、`findings.json` 逐 finding、`data/*.json` 原始 discussions、`resolve-log.json` 项目解析）
- 复跑：`~/tmp/extract-triage-mrs.py` → `triage-rounds-collect.py` → `triage-rounds-diffsize.py` → `triage-rounds-analyze.py`

## 方法与口径

1. **候选 MR**：全库 5284 个 pi session 中 155 个命中 triage-mr 注入；tool 路由过滤出 **143 个 session 真实调用过 `ocr-pull-discussions.py`**，771 次 pull 调用，去重出 **60 个 distinct MR iid**。
2. **项目归属**：iid 跨项目撞车严重（小 iid 多项目并存），以 session cwd→git remote 投票定向探查解析，59/60 解析成功（`!2966` 未解析，剔除）。残余风险：无 remote 证据、fallback 扫描解析的少数 MR（!34 等）可能错配项目，涉及量 <10 次 pull。
3. **Finding 定义**：镜像 `ocr-pull-discussions.py` 的正典口径——讨论根注释、过滤 system/junk/🔍✅⚠️ summary。共 **1221 findings**（810 带 diff 锚点、411 无锚点的 fallback/general）。
4. **轮次**：finding 按 `position.head_sha` 分组 = 一次评审轮（bot 对该 commit 的评审）。triage verdict 取线程内最后一条 `### ✅/❌/🟡/🔵` 回帖。优先级取 finding 头 `[category · priority]`（仅新格式 OCR 有）。
5. **verdict 覆盖**：1221 中 811 条有线程内 verdict（TP 407 / FP 202 / Edge 91 / OOS 19 / Q 0 / 92 未答），其余为老格式时代或未 triage 轮。

## 核心结果

### 1. 轮次衰减与收敛（810 条 anchored findings，按轮次索引归一）

| 轮 | MR 活跃 | 新 findings | 占比 | 累计捕获 | TP% | FP% | hi/med/low |
|---|---|---|---|---|---|---|---|
| 1 | 44 | 403 | 49.8% | 49.8% | 42% | 39% | 26/88/196 |
| 2 | 33 | 181 | 22.3% | 72.1% | 62% | 20% | 18/55/90 |
| 3 | 20 | 78 | 9.6% | 81.7% | 73% | 16% | 6/23/46 |
| 4 | 15 | 59 | 7.3% | 89.0% | 86% | 10% | 4/17/38 |
| 5 | 13 | 25 | 3.1% | 92.1% | 95% | 0% | 3/7/14 |
| 6 | 8 | 34 | 4.2% | 96.3% | 55%* | 3% | 4/10/20 |
| 7-13 | ≤5 | 32 | 4.0% | 100% | ~90% | ~10% | 少量 low |

\* round 6 的 OOS 12 条来自单个 MR 的一批范围外改判，非普遍现象。

**收敛结论**：
- **数量收敛成立**：新 findings 逐轮近似减半（403→181→78→59→25），42% 的多轮 MR 严格单调递减；轮次中位数 2-3。
- **质量纯度收敛**：TP 占比 42%→86%+ 单调上升，FP 占比 39%→10%→0 单调下降。**后期轮次产出更少但更真**——剩下的基本是真缺陷或 fix 引入的回归，不是噪音。
- **优先级后移**：high 类集中在 round 1-2（44/233）；round 3 起 low 占比 >55%。高价值问题前置，符合预期。

### 2. diff 大小 vs 评审轮次（59 MR）

| 改动行数 (+/-) | #MR | 轮次中位 | 轮次均值 | findings 中位 | 文件数中位 | commits 中位 |
|---|---|---|---|---|---|---|
| 0-50 | 9 | 0 | 0.6 | 1 | 2 | 2 |
| 50-150 | 7 | 2 | 2.6 | 8 | 3 | 4 |
| 150-400 | 15 | 2 | 2.5 | 5 | 5 | 4 |
| 400-1000 | 12 | 3 | 3.0 | 16 | 9 | 8 |
| 1000-3000 | 8 | 2 | 3.6 | 17 | 13 | 11 |
| 3000+ | 8 | 2 | 2.9 | 24 | 32 | 23 |

```
轮次均值（▲）按 diff 行数分桶：
0-50      ▏0.6
50-150    ██▏2.6
150-400   ██▏2.5
400-1000  ██▌3.0
1000-3000 ███▋3.6
3000+     ██▉2.9   ← 中位被"一轮清完"的大 MR 拉低，均值与 commits 高度耦合
```

**相关系数**（n=59）：diff 行数 r=0.165，文件数 r=0.275，**commits r=0.576，pipelines r=0.667**。

**结论：diff 大小是弱预测变量，churn（push/commit 数）才是强预测变量。** 大 MR 常见两种形态：一轮爆出 20+ findings 后收敛（3000+ 桶的中位=2），或修一点推一轮拖 10+ 轮（internal MR example：54 commits → 11 轮有产出）。

### 3. 逐 MR 收敛速度（rounds-to-90%-own-findings）

15 个 MR 零 findings（OCR 一轮全绿）｜12 个 1 轮捕获 90%｜15 个 2 轮｜3 个 3 轮｜6 个 4 轮｜5 个 5 轮｜长尾 6-11 轮 3 个。

### 4. "最佳 review 次数" 操作建议（拟合）

- **目标 90% 捕获**：3 轮（累计 82%）不够，**4 轮（89%）是拐点**；5 轮后每轮新增 <4%。
- **边际收益视角**：每轮 review 的边际产出 = 上一轮的 ~50%；第 4 轮后边际 <8%，继续 push-review 的主要收益是抓自己 fix 引入的回归（TP 纯度 ~90%+），而非新问题。
- **经验公式**：review 轮次 ≈ max(2, min(4, ⌈commits ÷ 3⌉))——按 pipelines r=0.667 的强相关性，大约每 2-3 个 push 安排一轮有效评审；diff 大小只影响单轮 findings 数，不影响需要的轮数。
- **与 2 轮上限规则的关系**：本次统计的是 **MR 级评审轮次**；fix/triage-mr 新加的 2 轮上限是**单 finding 修复-复审往复**，两者不同层。数据支持单 finding 层面 2 轮上限（round 3+ 的同 finding 复现属于长尾回归拉锯），但不支持 MR 级 4 轮封顶——MR 级第 3-4 轮仍有 ~17% 的新发现产出。

## 数据质量注意

- 老格式时代（~2026-08 前）OCR finding 无 `[cat · pri]` 头 → 这些 finding 的 priority 统计缺失（占比集中在 round 1 的 unanswered 桶）。
- 411 条 unanchored（fallback/general findings）不参与轮次切分，避免污染轮次索引；它们多数是老格式全文评审。
- 109 条 round-1 findings 无 verdict：多为老格式时代未走 triage 或 diff 过期无法回帖（SKILL.md 已知场景）。
- 仓库分布偏置：三个高频使用 triage 的内部仓（占位：A/B/C） 三个仓贡献了绝大多数轮次重的 MR（正是 triage 高频使用仓）。
