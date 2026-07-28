# teach assets — 模板源

teach skill 的 **canonical assets 模板**。每个教学工作区创建时,从此目录复制到工作区的 `assets/` 目录。

## 架构决策 (Closes #5)

- **每工作区自包含**:各工作区存自己的 `assets/` 副本,不依赖外部路径
- **模板源**:此目录为 canonical source
- **路径约定**:lesson 通过 `../assets/` 引用(相对路径,双击 HTML 即开)
- **内部结构**:flat——不分 css/js 子目录
- **更新**:修改此模板后,手动同步到各现有工作区的 `assets/`

## 预期文件(待后续 ticket 确定内容)

| 文件 | 用途 | 来源 ticket |
|---|---|---|
| `base.css` | 统一 CSS 基底 | #7 |
| `quiz.js` | 声明式 quiz 组件 | #8 |
| `katex.min.css` | KaTeX 公式渲染样式 | #6 |
| `katex.min.js` | KaTeX 公式渲染 JS | #6 |
| `fonts/` | KaTeX 字体文件 | #6 |

参见 [Map #4](https://github.com/peachest/skills/issues/4)。
