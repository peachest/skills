# skill-impact — setup-matt-pocock-skills

| 日期 | 提案/落点 | commit | 验证 |
|---|---|---|---|
| 2026-10-19 | issue-tracker-gitlab.md 同步三层规则（97bc905）：问题 A 命令形态适配 glab；问题 B 不适用——GitLab 扫描全部 closing pattern 逐一关闭。local 版不适用——文件编辑走 edit 工具，未命中显式报错且强制唯一，工具语义已覆盖 | | |
| 2026-10-19 | issue-tracker-github.md 两处 retro 修复：①新增「Issue body 编辑三层规则」（结构改动整篇重写 --body-file；str-replace 仅限微调且 replace 前必 grep 验证唯一存在；未命时报错列上下文，禁静默跳过）②关闭规则补例外 3：merge commit 携带多个 Closes 引用时 GitHub 只处理第一个，其余票 `gh issue close -c 'Closed by <merge-sha>'` 补关 | docs(setup-matt-pocock-skills): issue-tracker-github 两处 retro 修复——①issue body 编辑三层规则（大改整篇重写 --body-file、微调 str-replace 前必 grep 验证、未命时报错不静默，实跑 11 次 MISS 实证）②多 Closes 引用平台行为例外：merge commit 只处理第一个 Closes，其余票 gh issue close -c 补关（实跑 9 票滞留 8 票实证） | 已装安装副本（post-commit hook 重装），sanitize-check 本文件 0 命中 |
| 2026-10-26 | merge 后验证接入 tracker close-verify 首选工具：tracker CLI 新增 --backend github\|gitlab 与 `ticket close-verify --ref <PR/MR号或SHA>`（dry-run 默认、--apply 补关、扫描述+全部 commit message 的 closing pattern，覆盖非默认分支合并/多 Closes 滞留/squash 丢引用三类盲区）；两份 issue-tracker 文档的 merge 后验证节、例外 2/3、默认分支变更追补同步改指该工具，手动路径降为回退。动机：历史 session 挖掘 481 次手动关票调用，HAMi #50-54 五票实证遗漏。实现侧 pi-packages feat/tracker-remote-backends ba8927d（peer 交付，父 session 独立真实 smoke 验证 PR #148 链路通过） | 9c91508 | go build+test 全绿（+27 测试）；真实验证 peachest/pi-packages（list/view/close-verify）；post-commit hook 已重装安装副本 |
