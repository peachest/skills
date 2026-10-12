# skill-impact — orient

| 日期 | 提案 | 落点 | commit | 验证 |
|------|------|------|--------|------|
| 2026-09-24 | 导航词防泄漏：bearing/waymark/seams/calibration 是本 skill 的过程词，实测会渗入用户可见输出（session 01a0ce0a 的"地形重查/Bearing 如下/裁决 landscape"报告被用户打回要求大白话）。SKILL.md 末尾新增 User-facing output 节：导航词留在过程内，用户可读文本走项目输出规则（大白话/完整因果句/一物一名），并给出两个翻译示例 | engineering/orient/SKILL.md | 见 git log | 已重装 npx skills add；grep 'User-facing output' 已装副本命中 |
| 2026-10-12 | 补触发词：35 次历史注入中仅 1 次显式说 orient，高频实词是"地形"(8)/"现状"(6)/"先探索先收集"(5)，另有 ~17% 误触发。description 追加 Use when 段：看地形/查看现状/收集现状/先探索/先收集/先看现状 + 久远 session 恢复 + 新仓/新节点进入前摸底 | engineering/orient/SKILL.md | 见 git log | 已重装 npx skills add；~/.agents 与 ~/.pi 两处副本均 grep '看地形' 命中 |
