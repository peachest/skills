# rolling-ocr — Skill Impact

| date | proposal | commit | verification |
|---|---|---|---|
| 2026-10-30 | 新建 skill：编排"本地评审循环"（修完意见先 commit → 全量首评 → H/M fix-or-reject → 窄轮 low 复核 → 同题 3 轮上限 → 回扩全量终审 → 闸门过才 push）。职责卡位：ocr owns 单轮评审怎么跑，rolling-ocr owns 循环与 push 时机；CLI 细节经 read 指针落 ocr 第 3/4 章（skill-dependencies read-material 形态）。判据全部来自 2026-10-28 session-mining 六 lane 报告 | feat: add rolling-orchestration skill (rolling-ocr) and ocr exit pointer | 依赖前校验（fix/ocr/triage-mr/pi-events-daemon 均在装）；npx skills add -g 安装成功；判据与六 lane 报告逐条对账 |
| 2026-10-30 | doc-reviewer 噪声审计（对象=上条新建 commit，裁决清单 9 条）落 6 条：①公开仓 ledger 删 ~/tmp 个人路径（高危）②首段动机铺陈压缩③步骤 0/4 轶事句删（含写死计数）④"轮次参数指纹"表删——参数已内联步骤正文，消双写⑤四坑压成标题+步骤指针，概念留步骤 4 一处⑥OCR_LLM_TIMEOUT 改"取 ocr ch3 推荐值"防漂移；N2-1 软候选按审计备注保守保留一行动机 | fix(skills): rolling-ocr noise audit — trim restatements, drop anecdotes, sanitize ledger path | diff 复读：四坑仍完整覆盖 4 类（坑 3 正文唯一处保留）；卡位句/完成判据/同题上限/工具故障边界未动 |
