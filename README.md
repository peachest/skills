# Skills

个人 agent skills 集合，用于 [pi agent](https://github.com/peachest/skills)。同时通过 git subtree 引入了 [mattpocock/skills](https://github.com/mattpocock/skills) 并改造成 pi 的 `/skill:<name>` 引用格式。

## 为什么有这个仓库

日常开发中我需要两类 skill：

1. **自己写的 skill** —— 针对具体工作流（MR review、fact-check、Go 重构等），扁平放在根目录
2. **社区 skill** —— [mattpocock/skills](https://github.com/mattpocock/skills) 提供了一套完整的工程 skill（grilling → spec → tickets → implement → code-review），但它的 skill 互相引用用的是 `/<name>` 格式，pi agent 要求 `/skill:<name>`。通过 git subtree 引入后用脚本批量改写

## 目录结构

```
skills/
├── fact-check/              ← 自定义 skill（扁平）
├── mr-review-triage/        ← 自定义 skill
├── fix/                     ← 自定义 skill
├── ...                      ← 其它自定义 skill
├── scripts/
│   └── rewrite-skill-refs.py  ← skill 引用格式化脚本
└── vendor/
    └── mattpocock/          ← git subtree, 整个上游仓库
        └── skills/
            ├── engineering/
            ├── personal/
            └── productivity/
```

## 自定义 Skills

### 工程开发

- **[commit-buddy](./commit-buddy/SKILL.md)** — 分析变更、规划拆分、按 Conventional Commits 提交
- **[conventional-commits](./conventional-commits/SKILL.md)** — 用 Conventional Commits 规范格式化 commit message
- **[gopls-refactor](./gopls-refactor/SKILL.md)** — 基于 gopls 的 Go 符号重命名（rename、命名对齐、私有化）
- **[write-gomega-matcher](./write-gomega-matcher/SKILL.md)** — 编写自定义 Gomega matcher（gcustom.MakeMatcher）
- **[k8s-dra](./k8s-dra/SKILL.md)** — Kubernetes DRA（动态资源分配）概念、API 参考和示例
- **[vscode-extension](./vscode-extension/SKILL.md)** — VS Code 扩展开发辅助
- **[ci-pipeline-profiler](./ci-pipeline-profiler/SKILL.md)** — GitLab CI pipeline 耗时分析：拉取 job 数据、下钻日志、关联配置文件，产出结构化报告 + 优化建议

### 代码审查与修复

- **[mr-review-triage](./mr-review-triage/SKILL.md)** — 从 GitLab MR / GitHub PR 拉取 OCR review 评论，分类打标，解决线程
- **[triage-mr](./triage-mr/SKILL.md)** — 拉取未解决 review 评论，委托 /fix 分类修复，回贴标签并 resolve
- **[fix](./fix/SKILL.md)** — 验证、grill、修复 code-review 发现的问题
- **[html-review](./html-review/SKILL.md)** — 验证 HTML 文件结构完整性（DOCTYPE、charset、标签闭合、重复 id、资源引用）

### 项目规划

- **[to-epic](./to-epic/SKILL.md)** — 将产品研究文档拆解为里程碑级 epic 和 feature 级 spec
- **[to-backlog](./to-backlog/SKILL.md)** — 向项目 backlog 追加小任务或标记完成
- **[setup-to-epic](./setup-to-epic/SKILL.md)** — 为 to-epic 配置 local-markdown issue tracker 的两级目录结构
- **[stuck-callout](./stuck-callout/SKILL.md)** — agent 卡住时生成结构化摘要（已试什么、失败什么、需要什么帮助）

### 内容与工具

- **[fact-check](./fact-check/SKILL.md)** — 从文档提取可验证声明，路由到规则引擎或 web search，产出有证据支撑的判定
- **[fetch-article](./fetch-article/SKILL.md)** — 通用文章抓取器，路由 URL 到适配器，输出 Markdown（微信公众号、Bilibili 视频、通用 URL）
- **[bilibili-transcriber](./bilibili-transcriber/SKILL.md)** — 通过 whisper-asr 服务转录 Bilibili 视频音频为文本
- **[learn-from-examples](./learn-from-examples/SKILL.md)** — 分析示例项目/源码仓库，提取可复用模式、最佳实践、接口契约
- **[pi-package-development](./pi-package-development/SKILL.md)** — pi 包开发全流程（extension、skill、theme、prompt 的 scaffold/test/publish）
- **[my-coffee](./my-coffee/SKILL.md)** — 瑞幸咖啡点单（搜索门店/商品、查询取餐码/订单状态、取消订单）

## Vendor: mattpocock/skills

`vendor/mattpocock/` 是通过 `git subtree add --squash` 引入的 [mattpocock/skills](https://github.com/mattpocock/skills) 仓库。所有文件直接存在于本仓库中，可以原地修改，不需要 submodule 的 init/push 流程。

### 包含的 skills

上游 skill 按 engineering / productivity / personal / misc 分类，引用格式已全部改写为 `/skill:<name>`。完整列表见 [vendor/mattpocock/README.md](./vendor/mattpocock/README.md)。

### 安装到 Pi

见 [`docs/agents/install-skills.md`](./docs/agents/install-skills.md)。

```bash
# 自定义 skill
npx skills add ~/skills/ --global --all -a pi -y

# 引入的 mattpocock skill
npx skills add ~/skills/vendor/mattpocock --global --all -a pi -y
```

### 更新上游

```bash
git subtree pull --prefix=vendor/mattpocock \
  https://github.com/mattpocock/skills.git main --squash
```

拉取后重新安装：

```bash
python3 scripts/rewrite-skill-refs.py
npx skills add ~/skills/vendor/mattpocock --global --all -y
```

脚本幂等，重复运行不会产生多余改动。

### 引用格式化脚本

`scripts/rewrite-skill-refs.py` 将 mattpocock 的 skill 引用从 `/<name>` 改写为 pi agent 格式 `/skill:<name>`。

```bash
# 预览（不写文件）
python3 scripts/rewrite-skill-refs.py --dry-run

# 执行替换
python3 scripts/rewrite-skill-refs.py

# 指定其它目录
python3 scripts/rewrite-skill-refs.py /path/to/other/vendor
```

脚本自动发现 skill 名（扫描含 `SKILL.md` 的目录名），上游新增 skill 时无需修改脚本。正则排除了 URL、文件路径等非引用场景，替换后再次运行结果为 0（幂等）。
