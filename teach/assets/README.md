# teach assets — 模板源

teach skill 的 **canonical assets 模板**。每个教学工作区创建时,从此目录复制到自己需要的文件到工作区的 `assets/` 目录。

## 架构决策

- **每工作区自包含**:各工作区存自己的 `assets/` 副本 (#5)
- **路径约定**:lesson 通过 `../assets/` 引用(相对路径,双击 HTML 即开)
- **内部结构**:flat——不分 css/js 子目录
- **更新**:修改此模板后,手动同步到各现有工作区的 `assets/`

## 文件清单

| 文件 | 用途 | 来源 ticket | 必需? |
|---|---|---|---|
| `base.css` | 统一 CSS 基底 | #7 (待定) | ✅ 所有工作区 |
| `quiz.js` | 声明式 quiz 组件 | #8 (待定) | 可选 |
| `katex.min.css` | KaTeX 公式渲染样式 | #6 | 可选(有公式时) |
| `katex.min.js` | KaTeX 公式渲染核心 | #6 | 可选(有公式时) |
| `auto-render.min.js` | KaTeX 自动扫描渲染 | #6 | 可选(有公式时) |
| `render.js` | KaTeX 定界符配置($ 和 $$) | #6 | 可选(有公式时) |
| `fonts/*.woff2` | KaTeX 字体(20 个 woff2) | #6 | 可选(有公式时) |

## KaTeX 引入方式 (#6)

在 lesson `<head>` 中加入:

```html
<link rel="stylesheet" href="../assets/katex.min.css">
<script src="../assets/katex.min.js" defer></script>
<script src="../assets/auto-render.min.js" defer></script>
<script src="../assets/render.js" defer></script>
```

正文中用 `$...$` (行内) 或 `$$...$$` (块级) 包裹 LaTeX 公式即可自动渲染。

- **本地 vendored**:离线完全可用,总大小 ~600KB(仅 woff2 字体)
- **opt-in**:不需要公式的工作区(如 ocr-image)不复制 KaTeX 文件
- **定界符**:`$...$` 行内 + `$$...$$` 块级

参见 [Map #4](https://github.com/peachest/skills/issues/4)。
