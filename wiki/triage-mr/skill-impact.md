# skill-impact — triage-mr

提案台账。被拒提案必须保留并写明拒绝理由——后续提案撞形状时先翻此表。

| 提案 | 落点 | commit | 验证命令与结果 |
|------|------|--------|----------------|
| S1 ocr-verify-resolved.py：GitLab 判定从 notes[0] 改为线程内全部 resolvable note resolved，输出标注 [N/M notes open]（GitHub 侧本为线程级，未动） | mr-review-triage/scripts | 2a46367 | mock 4 例 ✓（head已resolve+reply open→报open；全resolve→closed；单note open 无后缀；非resolvable→跳过）；真实 MR 回归：与旧版在真实 open 线程上判定一致 |
| S2 fix skill"suggested fix is a second, independent claim"段搬回源仓并重装（peer session 只改了安装版） | fix skill | 2a46367 | diff 源仓=安装版 ✓ |
| D1 SKILL.md 正面表述五处：增量写 classified.json（第一条 verdict 即建文件）；script-first 排序+手动 fallback 两类限定；gate-observation 矛盾裁决规则；done 条件与 stale 警告去重；Reflect 降级并入 Wrap-up | triage-mr SKILL.md | 0ec0950 | 待下轮 diagnose 验证（对应 P-001/P-002/P-003） |
| S3 ocr-post-labels.py：线程 resolve 成功后 `_sweep_notes_gitlab` 扫尾剩余 resolvable note；失败降级 WARN（head 已 resolve，gate 兜底） | mr-review-triage/scripts | 0ec0950 | mock ✓：POST 回帖→PUT resolve→GET→扫 stale reply note；验证时序含新回帖 note |
| R1 拒绝：triage-mr frontmatter description 改一行摘要（user-invoked 规范建议） | frontmatter | — | 拒绝理由：流程式描述对人类记忆该 skill 的编排角色有正收益，且 user-invoked 下零 context load，无违规成本 |
| R2 拒绝：post-labels.py 补"独立处理 note 扫尾"子命令（与 S3 二选一） | mr-review-triage/scripts | — | 拒绝理由：S3 顺路扫尾更小 diff，独立子命令引入第二入口徒增维护面 |
