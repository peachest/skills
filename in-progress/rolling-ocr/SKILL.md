---
name: rolling-ocr
description: >
  编排"本地评审循环"：修复评审意见后不立即 push——先 commit，再本地 ocr 评审 → 修复 →
  窄轮复核，通过收敛闸门后才 push，push 后等 CI 下一轮 bot 评审。Use when 修复完
  CI/评审 findings 准备 push、用户说 本地评审/迭代评审/先收敛再推/rolling review、
  triage-mr 修完当前轮意见之后、或要判断 本轮评审是否收敛/能不能推。只编排循环与
  push 时机；单轮评审怎么跑（命令、参数、排障）由 /skill:ocr 承接。
---

# rolling-ocr — 本地评审循环

CI bot 评审慢：修复意见后立即 push，要等很久才拿到下一轮意见。本 skill 把这一整段
等待换成本地循环——**每轮意见都在本地评审、修复、复核，收敛后才 push 一次**，CI 的
下一轮 bot 评审消费的是已经收敛的 diff。

卡位：`ocr` owns 单轮评审怎么跑（命令构造、参数、结果校验、排障）；this owns 循环——
什么时候跑评审、跑什么范围、什么时候算收敛、什么时候 push。

## 流程

```
修完当前轮意见 → commit → 首评(全量) → verdict(修/驳) → 窄轮复核(修复面)
      ↑                                              │
      └────── 仍有 H/M findings ←────────────────────┘
                                                     │ H/M 全部有去向
                                                     ↓
                              回扩确认(全量终审) → 闸门过 → push → 等 CI 下轮
```

### 0. 先 commit 再评

评审对象是 commit 区间，工作区未 commit 时 `--from/--to` 审到的是旧快照（实证事故：
修复停在工作区，本地评了个寂寞）。**每轮修复落地即 commit，然后才发评审**。
完成判据：`git status` 干净，`git log -1` 是刚修的内容。

### 1. 首评（全量）

`--from <MR基点> --to HEAD --effort medium`（高危面/单票深审用 high）。范围必须覆盖
全部改动——窄范围是假收敛的头号来源。
命令构造、`-b` 背景串写法、concurrency 选择：read /skill:ocr 的 SKILL.md 第 3 章
（参数规则）与第 4 章（场景路由）。评审发后台（bg_run），完成判据：结果 JSON 落盘。

### 2. Verdict：行动项清空

逐条核对 findings（LLM 结论先按 ocr 第 5 章对源码验证再采信）：

- **critical/high/medium**：每条给去向——修（Delegate to /skill:fix with findings 列表）
  或驳回（写明理由，如"按 spec 该行为是故意的"）。
- **low**：丢弃，不阻塞。

完成判据：没有一条 H/M 悬空——每条都处于"已修"或"已驳回"。这就是**收敛**的主判据；
0 findings 单独出现反而要警惕（见"假收敛四坑"）。

### 3. 窄轮复核（修复面）

每轮修复后：`--from <修复起点> --to HEAD` 或 `-c <fix-commit>`，`--effort low`——只验证
"修对了、没修出新问题"。复核 findings 回到步骤 2。

**同题上限**：同一主题的 finding 最多修 3 轮；第 3 轮修完仍出同题，停止响应，如实上报
已尝试的每轮修复与剩余分歧，由用户裁决。不为凑绿改判或压低 effort 再跑。

### 4. 回扩确认（全量终审）

窄轮的结构性盲区：它看不见修复过程自己引入的、落在修复文件之外的问题（实证：收尾
全量轮抓出 agent 刚写的 critical；另一实例里逐票评审全收口后，全仓 scan 在同一批
已评审代码上扫出 9 项实锤）。所以 H/M 清空后，**末轮必须回到全量**：

- 修的是 ocr 自己的 findings 且 TDD 红绿留痕（失败测试→修→转绿）→ 本轮可豁免，
  修复证据即确认。
- 其余一律跑：全量 diff（`--effort low` 起步，收尾确认可用 high）。

完成判据：全量轮无新增 critical/high/medium。

### 5. Push

闸门通过（步骤 2 + 步骤 4 都过）才 push。push 后本轮结束——CI bot 的下一轮意见是新的
输入，回到步骤 0。MR 场景的 verdict 落盘与线程回复由 triage-mr 流程承接；等 CI 终态用
pi-events-daemon 订阅，本地循环不空转轮询。

## 轮次参数指纹

| 阶段 | 范围 | effort |
|---|---|---|
| 首评 | `--from <MR基点> --to HEAD` 全量 | medium（高危面 high） |
| 窄轮复核 | `--from <修复起点>` 或 `-c <fix>` | low |
| 回扩确认 | 回到全量 | low 起步（可 high） |

稳定的习惯：每轮真跑前 `--preview` 定范围（范围判定以 diff 为准，preview 只做参考）；
`-b` 写成轮次台账（复核轮枚举上轮修了什么）；`OCR_LLM_TIMEOUT=300` 恒定。其余 flag
细节以 ocr 第 3 章为准。

## 假收敛四坑

1. **窄轮盲区**：修复面干净 ≠ 全量干净——窄轮只证明修复没引入新问题，不证明别处干净。
   首评与终审必须全量，只有中间轮允许窄（步骤 1/4）。
2. **审错快照**：未 commit 就评审，审到旧内容（步骤 0）。
3. **降档绿灯**：时延压力下把 effort 降档后通过的轮，不是同 effort 下的收敛证据——
   降档轮的"干净"降权处理，终审恢复标准 effort。
4. **基线选错**：`--from origin/main` 会把他人 commit 卷进双向 diff——基点取 MR 实际
   分叉 commit。

工具故障的边界：网关持续超时、重试阶梯（缩范围→升超时→降并发→`--resume`，见 ocr
第 8 章）走完仍跑不成时，停下上报"本地评审未完成"，把 push 决策交还用户——此时
判据已经退化，push 不再经过闸门。
