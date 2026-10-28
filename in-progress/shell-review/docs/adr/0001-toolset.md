# ADR-0001: 工具集只收 bash -n + shellcheck + shfmt，其余实测剔除

日期: 2026-10-28
状态: accepted

## 背景

设计 shell 静态评审 skill 时，对 shell 静态分析全生态做了实测（对一个内部 CI 构建审计项目的 worktree 中的 4 个脚本，共 579 行）：

| 工具 | 实测结果 | 判定 |
|---|---|---|
| bash -n | 4 脚本全过，瞬时 | 收（零依赖语法闸） |
| shellcheck v0.10.0 | 0 warning（基线已清干净）；历史实证抓出 SC2155 真 bug（LLM 八轮评审漏掉） | 收（唯一缺陷检测器） |
| shfmt v3.12.0 -d | 4 文件全部需重排，842 行 diff | 收为 advisory（仅报告） |
| bashate | ~30 条全是 E003 缩进/E006 行宽噪音 | 剔除 |
| checkbashisms | 0 条（bash 脚本无需 POSIX 兼容） | 剔除 |
| shellharden v4.3.2 --check | 4 脚本全 0 条建议（引号问题被 shellcheck SC2086 族覆盖） | 剔除 |
| dash -n | 报 bashism——脚本 shebang=bash 且 CI 用 bash，bashism 是预期 | 剔除 |
| bash-language-server / semgrep / 聚合器 / actionlint / bats | LSP 通道 agent 用不上 / bash 支持实验性 / 内部跑的还是上述工具 / 平台不符 / 行为测试非静态 | 未装即剔 |

## 决策

skill 只集成 bash -n（前置语法闸，失败短路）→ shellcheck -S style（缺陷层）→ shfmt -d（格式 advisory，**仅报告不落盘**）。

shfmt 不落盘的原因：reproducible-build 场景 digest 对脚本内容敏感（见 GLOSSARY「digest 敏感」），`shfmt -w` 自动改写会引起 digest 漂移。

## 后果

- 工具链零 Python 依赖；shfmt/shellcheck 为单二进制，进 runtime.conf.example + check-env.sh。
- 若未来脚本需要兼容 /bin/sh（如容器内 dash），dash -n 可作为可选层捡回。
