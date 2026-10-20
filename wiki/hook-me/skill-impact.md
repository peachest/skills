# skill-impact — hook-me

| 日期 | 提案 | 落点 | commit | 验证 |
|------|------|------|--------|------|
| 2026-10-20 | 初版创建：模仿 vendor/mattpocock in-progress/loop-me 的结构（lens + definition of done + workspace，frontmatter 带 disable-model-invocation + argument-hint）。内容沉淀自 2026-10-20 两阶段挖掘实跑（908 session 粗扫 + ppu-device-plugin/kube-nodexpu-manager 双 worker 深挖）：hook lens 三问审计（命名事件→hook / 编码判断→规则 / 都不是→删）、guard/nudge/ritual 三动作分类、六类挖掘信号及 hook 事件映射、四条方法律（denominator / human adjudication / cross-repo consensus / reject ledger——均来自本次实跑翻车与验证：bigram 当覆盖率、纠错计数 465→55 人工定标、双仓独立提名互证、rm-rf 与 session_start 候选否决须记账）、多仓并行派 worker 的 dispatch 契约（线索标 hypothesis 防锚定、脚本留 ~/tmp 可重放、session cwd 字段分组防 wt 目录回收、rtk 前缀剥离、compaction 重放去重） | in-progress/hook-me/SKILL.md | 见 git log | sanitize-check CLEAN；npx skills add -g 安装成功；diff 源仓 vs ~/.agents/skills/hook-me 一致 |
