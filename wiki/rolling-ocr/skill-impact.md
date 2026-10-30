# rolling-ocr — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-30 | 新建 skill：编排"本地评审循环"（修完意见先 commit → 全量首评 → H/M fix-or-reject → 窄轮 low 复核 → 同题 3 轮上限 → 回扩全量终审 → 闸门过才 push）。职责卡位：ocr owns 单轮评审怎么跑，rolling-ocr owns 循环与 push 时机；CLI 细节经 read 指针落 ocr 第 3/4 章（skill-dependencies read-material 形态）。判据全部来自 2026-10-28 session-mining（124 迭代 session，六 lane 交叉） | feat: add rolling-orchestration skill (rolling-ocr) and ocr exit pointer | 依赖前校验（fix/ocr/triage-mr/pi-events-daemon 均在装）；npx skills add -g 安装成功；判据与六 lane 报告（~/tmp/ocr-loop-mining/lanes/）逐条对账 |
