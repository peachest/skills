# Skills

个人 agent skills 集合，用于 [pi coding agent](https://github.com/earendil-works/pi-coding-agent)。同时通过 git subtree 引入了 [mattpocock/skills](https://github.com/mattpocock/skills) 并改造成 pi 的 `/skill:<name>` 引用格式。

## 为什么有这个仓库

日常开发中我需要两类 skill：

1. **自己写的 skill** —— 针对具体工作流（commit、code review、fact-check、Go 重构等），按用途分类放在 `engineering/`、`productivity/`、`research/`、`devtools/`、`misc/` 下；仍在打磨的放在 `in-progress/`，不再维护的归入 `deprecated/`
2. **社区 skill** —— [mattpocock/skills](https://github.com/mattpocock/skills) 提供了一套完整的工程 skill（grilling → spec → tickets → implement → code-review），但它的 skill 互相引用用的是 `/<name>` 格式，pi agent 要求 `/skill:<name>`。通过 git subtree 引入后用脚本批量改写

## 目录结构

```
skills/
├── engineering/             ← 工程开发：commit、review、spec、重构
├── productivity/            ← 效能工具：日报、CI 分析、博客、session 诊断
├── research/                ← 研究/内容：文章抓取、视频转录、论文翻译、fact-check
├── devtools/                ← 开发辅助：gopls 重构、Gomega matcher、VS Code 扩展、pi 包
├── misc/                    ← 杂项：HTML 校验、K8s DRA、瑞幸咖啡
├── in-progress/             ← 打磨中：架构巡视、变异测试、OKB、Python 设计模式…
├── deprecated/              ← 已废弃
├── docs/
│   ├── adr/                 ← 架构决策记录
│   └── agents/              ← agent 规范（安装、issue tracker、triage labels、domain）
├── scripts/
│   ├── rewrite-skill-refs.py  ← skill 引用格式化脚本
│   └── check-skill-invocation.py
├── vendor/
│   └── mattpocock/          ← git subtree, 整个上游仓库
│       └── skills/
│           ├── engineering/
│           ├── personal/
│           └── productivity/
├── AGENTS.md                ← agent 项目规范
├── CONTEXT.md               ← 术语表（导航隐喻系统）
└── LICENSE
```

## 自定义 Skills

### 工程开发（engineering/）

- **[commit-buddy](./engineering/commit-buddy/SKILL.md)** — 分析变更、规划拆分、按 Conventional Commits 提交
- **[conventional-commits](./engineering/conventional-commits/SKILL.md)** — 用 Conventional Commits 规范格式化 commit message
- **[fix](./engineering/fix/SKILL.md)** — 验证、grill、修复 code-review 发现的问题
- **[learn-from-examples](./engineering/learn-from-examples/SKILL.md)** — 分析示例项目/源码仓库，提取可复用模式、最佳实践、接口契约
- **[mr-review-triage](./engineering/mr-review-triage/SKILL.md)** — 从 GitLab MR / GitHub PR 拉取 OCR review 评论，分类打标，解决线程
- **[triage-mr](./engineering/triage-mr/SKILL.md)** — 拉取未解决 review 评论，委托 /skill:fix 分类修复，回贴标签并 resolve
- **[orient](./engineering/orient/SKILL.md)** — 出发前先读地形：survey 项目现状，让规划基于已有内容
- **[project-wiki](./engineering/project-wiki/SKILL.md)** — 一次性 survey 代码库地形，用 SHA 漂移检测保持地图最新
- **[review-spec](./engineering/review-spec/SKILL.md)** — traverse 前检查路线：找出 spec 与 ground truth 的偏差并路由到修复 skill
- **[then-what](./engineering/then-what/SKILL.md)** — 探索每个选项的真实后果，以用户故事重呈现
- **[hail](./engineering/hail/SKILL.md)** — agent 迷路时生成 distress signal（已试什么、当前位置、需要什么救援）

> `orient` → `project-wiki` → `review-spec` → `then-what` → `hail` 共享一套[导航隐喻](./CONTEXT.md)，每个 skill 名本身就是一个导航动作。

### 效能工具（productivity/）

- **[daily-recap](./productivity/daily-recap/SKILL.md)** — 将当天 pi sessions 汇总为结构化日报
- **[ci-pipeline-profiler](./productivity/ci-pipeline-profiler/SKILL.md)** — GitLab CI pipeline 耗时分析：拉取 job 数据、下钻日志、关联配置，产出报告 + 优化建议
- **[blog](./productivity/blog/SKILL.md)** — Blog pipeline：draft → de-slop → review，触发于写/改/导出博客
- **[pi-insight](./productivity/pi-insight/SKILL.md)** — 诊断 pi 使用：分析 system prompt 组成、tool/skill 使用频率、给精简建议
- **[guardrail-optimizer](./productivity/guardrail-optimizer/SKILL.md)** — 找出触发 guardrail 的路径/命令，推荐 allowlist 并更新配置

### 研究与内容（research/）

- **[fact-check](./research/fact-check/SKILL.md)** — 从文档提取可验证声明，路由到规则引擎或 web search，产出有证据支撑的判定
- **[fetch-article](./research/fetch-article/SKILL.md)** — 通用文章抓取器，路由 URL 到适配器，输出 Markdown（微信公众号、Bilibili、通用 URL）
- **[bilibili-transcriber](./research/bilibili-transcriber/SKILL.md)** — 通过 whisper-asr 服务转录 Bilibili 视频音频为文本
- **[paper-translate](./research/paper-translate/SKILL.md)** — 将 LaTeX 论文源文件翻译为中文 Markdown 文档
- **[paper-summarize](./research/paper-summarize/SKILL.md)** — 根据翻译后的中文 MD 和 TeX 原文，生成章节摘要到 brief.md

### 开发辅助（devtools/）

- **[gopls-refactor](./devtools/gopls-refactor/SKILL.md)** — 基于 gopls 的 Go 符号重命名（rename、命名对齐、私有化）
- **[write-gomega-matcher](./devtools/write-gomega-matcher/SKILL.md)** — 编写自定义 Gomega matcher（gcustom.MakeMatcher）
- **[vscode-extension](./devtools/vscode-extension/SKILL.md)** — VS Code 扩展开发辅助
- **[pi-package-development](./devtools/pi-package-development/SKILL.md)** — pi 包开发全流程（extension、skill、theme、prompt 的 scaffold/test/publish）

### 杂项（misc/）

- **[html-review](./misc/html-review/SKILL.md)** — 验证 HTML 文件结构完整性（DOCTYPE、charset、标签闭合、重复 id、资源引用）
- **[k8s-dra](./misc/k8s-dra/SKILL.md)** — Kubernetes DRA（动态资源分配）概念、API 参考和示例
- **[my-coffee](./misc/my-coffee/SKILL.md)** — 瑞幸咖啡点单（搜索门店/商品、查询取餐码/订单状态、取消订单）

### 打磨中（in-progress/）

这些 skill 已可使用，但仍在迭代，行为可能变化。

- **[architecture-explorer](./in-progress/architecture-explorer/SKILL.md)** — 用 CodeGraph 引导式逐层巡视代码库架构
- **[mutation-testing](./in-progress/mutation-testing/SKILL.md)** — 变异测试验证测试质量，找出存活 mutant 揭示测试盲区
- **[okb](./in-progress/okb/SKILL.md)** — 开放知识库（bronze → silver → gold），管理 agent 所知的真相来源
- **[python-design](./in-progress/python-design/SKILL.md)** — Python 项目设计模式（data model、validation、pipeline、plugin、序列化、state context）
- **[multi-arch-harbor-push](./in-progress/multi-arch-harbor-push/SKILL.md)** — nerdctl 构建多架构镜像并 fan-out 推送到 Harbor，不产生单架构 tag 噪音
- **[pi-session-cleanup](./in-progress/pi-session-cleanup/SKILL.md)** — 清理 trivial/陈旧 pi session 文件，回收磁盘空间
- **session-profile**（[设计阶段](./productivity/session-profile/)，尚无 SKILL.md，见 issue #18 #28）— pi session 画像分析底座

### 已废弃（deprecated/）

不再维护，保留供参考：[to-epic](./deprecated/to-epic/SKILL.md)、[to-backlog](./deprecated/to-backlog/SKILL.md)、[setup-to-epic](./deprecated/setup-to-epic/SKILL.md)。

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

## License

[MIT](./LICENSE)
