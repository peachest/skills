# skill-impact — hook-me

| 日期 | 提案 | 落点 | commit | 验证 |
|------|------|------|--------|------|
| 2026-10-20 | 初版创建：模仿 vendor/mattpocock in-progress/loop-me 的结构（lens + definition of done + workspace，frontmatter 带 disable-model-invocation + argument-hint）。内容沉淀自 2026-10-20 两阶段挖掘实跑（908 session 粗扫 + <device-plugin-repo>/<repo-c> 双 worker 深挖）：hook lens 三问审计（命名事件→hook / 编码判断→规则 / 都不是→删）、guard/nudge/ritual 三动作分类、六类挖掘信号及 hook 事件映射、四条方法律（denominator / human adjudication / cross-repo consensus / reject ledger——均来自本次实跑翻车与验证：bigram 当覆盖率、纠错计数 465→55 人工定标、双仓独立提名互证、rm-rf 与 session_start 候选否决须记账）、多仓并行派 worker 的 dispatch 契约（线索标 hypothesis 防锚定、脚本留 ~/tmp 可重放、session cwd 字段分组防 wt 目录回收、rtk 前缀剥离、compaction 重放去重） | in-progress/hook-me/SKILL.md | 见 git log | sanitize-check CLEAN；npx skills add -g 安装成功；diff 源仓 vs ~/.agents/skills/hook-me 一致 |
| 2026-10-20 | 层级判定补全：用户拍板 pi hook 与 git hook 两层都需要。SKILL.md hook lens 增 layer 段（判定问句"这个保证覆盖谁"：仅 agent 行为→pi hook；不得入仓内容→git hook gitleaks pre-commit 硬闸，凭证类双层叠加）；Definition of done 的 spec 必带字段增加 layer (pi/git/both)。动因：第三轮挖掘只产出 harness hook，glpat 泄漏显示缺的是入库闸 | in-progress/hook-me/SKILL.md | 见 git log | sanitize 单文件 CLEAN（wiki 行内部仓名属存量基线模式）；重装 diff 一致 |
