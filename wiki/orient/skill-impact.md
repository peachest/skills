# skill-impact — orient

| 日期 | 提案 | 落点 | commit | 验证 |
|------|------|------|--------|------|
| 2026-09-24 | 导航词防泄漏：bearing/waymark/seams/calibration 是本 skill 的过程词，实测会渗入用户可见输出（session 01a0ce0a 的"地形重查/Bearing 如下/裁决 landscape"报告被用户打回要求大白话）。SKILL.md 末尾新增 User-facing output 节：导航词留在过程内，用户可读文本走项目输出规则（大白话/完整因果句/一物一名），并给出两个翻译示例 | engineering/orient/SKILL.md | 见 git log | 已重装 npx skills add；grep 'User-facing output' 已装副本命中 |
