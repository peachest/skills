# GLOSSARY — shell-review

## 术语

### 静态三件套
skill 的工具链：`bash -n`（语法闸，失败短路）→ `shellcheck -S style`（缺陷层，逐条 SC 码）→ `shfmt -d`（仅格式报告，不自动改文件）。bashate / checkbashisms / shellharden / dash -n 实测剔除（见 ADR-0001）。

### 误报定谳
对 shellcheck 命中逐条归类为三选一：真修 / 白名单（场景性豁免）/ `# shellcheck disable=SCxxxxx` 注解。白名单**不内置**在 skill 里，靠脚本内注解承载（见 ADR-0003）。

### digest 敏感
peer 的 reproducible-build 场景下，脚本内容参与镜像 digest 计算。任何工具自动改写脚本（如 `shfmt -w`）都会引起 digest 漂移——因此 shfmt 只产出报告，永不落盘（见 ADR-0001）。

### 前置机械闸
本 skill 的定位：在 ocr（LLM 评审）之前运行，用静态工具消掉机械层问题（语法、SC 码、格式），把消噪后的残差连同 SC 码证据交给 LLM 评审。不替代 ocr（ADR-0002）。

### 扫描面（diff 感知）
默认只审当前分支相对 base（origin/dev）改动的 `.sh` 文件，与 ocr 评审面对齐；显式传文件路径时按文件审。不做全仓扫描（ADR-0004）。

## 状态语言

### 编排层
skill 的全部职责：按固定顺序调三件套、透传原始输出、按 severity 归类解读。不做结构化报告、不做 CI 模板（ADR-0005）。

### error 级
shellcheck severity=error（如 SC2155）。硬失败，阻塞后续评审。

### warning/style 级
报告但放行，附误报定谳建议。沿用 peer 的分级实践。
