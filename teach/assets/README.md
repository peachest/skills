# teach assets — 模板源

teach skill 的 **canonical assets 模板**。每个教学工作区创建时,从此目录复制需要的文件到工作区的 `assets/` 目录。

## 架构决策

- **每工作区自包含**:各工作区存自己的 `assets/` 副本 (#5)
- **路径约定**:lesson 通过 `../assets/` 引用(相对路径,双击 HTML 即开)
- **内部结构**:flat——不分 css/js 子目录
- **更新**:修改此模板后,手动同步到各现有工作区的 `assets/`

## 文件清单

| 文件 | 用途 | 来源 ticket | 必需? |
|---|---|---|---|
| `base.css` | 统一 CSS 基底 | #7 | ✅ 所有工作区 |
| `quiz.js` | 声明式 quiz 组件 (data-quiz JSON + radio button, a11y) | #8 | 可选 |
| `katex.min.css` | KaTeX 公式渲染样式 | #6 | 可选(有公式时) |
| `katex.min.js` | KaTeX 公式渲染核心 | #6 | 可选(有公式时) |
| `auto-render.min.js` | KaTeX 自动扫描渲染 | #6 | 可选(有公式时) |
| `render.js` | KaTeX 定界符配置($ 和 $$) | #6 | 可选(有公式时) |
| `fonts/*.woff2` | KaTeX 字体(20 个 woff2) | #6 | 可选(有公式时) |

## CSS 统一策略 (#7)

**选优扩展**:以 mtp `style.css`(最完整)为基底,吸收 llm-rl 和 ocr-image 的有用部分。

### 设计决策

- **字体**:serif body(Georgia / Songti SC)+ sans-serif heading(系统)+ mono(SF Mono)。系统字体,无需 web font
- **色板**:mtp 色值(accent `#0366d6`,bg `#ffffff`,text `#1a1a1a`)
- **变量命名**:mtp 命名 + `--radius`(from llm-rl)。`--accent-light` 改为 `--accent-bg`
- **Callout**:5 种,Obsidian 命名 — `.callout-note`(蓝)、`.callout-tip`(紫)、`.callout-warning`(橙)、`.callout-success`(绿)、`.callout-danger`(红)
- **吸收的组件**:`.tag`、`.src-ref`、`.sidenote`(from llm-rl);`figure/figcaption`、`.meta`(from ocr-image)
- **移除**:`.math-block`、`.math-inline`、`.formula`(KaTeX 接管)
- **新增**:`.katex-display` margin 样式

### 迁移映射(现有 → 新)

| 旧 class | 新 class | 工作区 |
|---|---|---|
| `.callout-note` | `.callout-note` | mtp (不变) |
| `.callout-warn` | `.callout-warning` | mtp, ocr-image |
| `.callout-key` | `.callout-tip` | mtp |
| `.callout.info` | `.callout-note` | llm-rl |
| `.callout.warn` | `.callout-warning` | llm-rl |
| `.callout.green` | `.callout-success` | llm-rl |
| `.callout.red` | `.callout-danger` | llm-rl |
| `.callout-success` | `.callout-success` | ocr-image (不变) |
| `.callout-info` | `.callout-note` | ocr-image |
| `--accent-light` | `--accent-bg` | mtp |
| `--max-w` / `--measure` | `--max-width` | llm-rl, ocr-image |

## KaTeX 引入方式 (#6)

在 lesson `<head>` 中加入:

```html
<link rel="stylesheet" href="../assets/katex.min.css">
<script src="../assets/katex.min.js" defer></script>
<script src="../assets/auto-render.min.js" defer></script>
<script src="../assets/render.js" defer></script>
```

正文中用 `$...$` (行内) 或 `$$...$$` (块级) 包裹 LaTeX 公式即可自动渲染。

参见 [Map #4](https://github.com/peachest/skills/issues/4)。

## 字体加载策略 (#9)

**系统字体,零 web font**。base.css 已定义系统字体栈:

- body: Georgia, "Songti SC", "Noto Serif SC", serif
- heading: -apple-system, "Segoe UI", "PingFang SC", sans-serif
- mono: "SF Mono", "Fira Code", "Consolas", monospace

迁移时:
- llm-rl: 删除 `@import url('https://fonts.googleapis.com/...')`
- ocr-image: 删除 "Source Serif 4" 引用(未本地化,fallback 到 Georgia)
- mtp: 无需改动
