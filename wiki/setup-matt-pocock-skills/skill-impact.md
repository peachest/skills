# skill-impact — setup-matt-pocock-skills

| 日期 | 提案/落点 | commit | 验证 |
|---|---|---|---|
| 2026-10-19 | issue-tracker-gitlab.md 同步三层规则（97bc905）：问题 A 命令形态适配 glab；问题 B 不适用——GitLab 扫描全部 closing pattern 逐一关闭。local 版不适用——文件编辑走 edit 工具，未命中显式报错且强制唯一，工具语义已覆盖 |
| 2026-10-19 | issue-tracker-github.md 两处 retro 修复：①新增「Issue body 编辑三层规则」（结构改动整篇重写 --body-file；str-replace 仅限微调且 replace 前必 grep 验证唯一存在；未命时报错列上下文，禁静默跳过）②关闭规则补例外 3：merge commit 携带多个 Closes 引用时 GitHub 只处理第一个，其余票 `gh issue close -c 'Closed by <merge-sha>'` 补关 | 80c4ea1 | 已装安装副本（post-commit hook 重装），sanitize-check 本文件 0 命中 |
