# PDF 导出机制

pandoc + weasyprint 把 `<PROJECT_DIR>/` 下的 Markdown 导出为自包含 PDF（图片内联、字体嵌入）。

## 环境检查

导出前验证：

```bash
pandoc --version | head -1        # ≥ 3.0
weasyprint --version              # ≥ 60
fc-list :lang=zh | head -1        # 至少 1 个中文字体
```

缺 weasyprint：`pip install weasyprint`
缺中文字体：`apt install fonts-wqy-zenhei` 或手动安装 Maple Mono NF CN

## 命令

单篇：

```bash
pandoc <PROJECT_DIR>/input.md -o <PROJECT_DIR>/pdf/output.pdf \
  --pdf-engine=weasyprint \
  --css=<SKILL_DIR>/references/export-style.css \
  --resource-path=<PROJECT_DIR> \
  --metadata title="标题" \
  --toc --toc-depth=2 \
  --standalone
```

批量：`bash <SKILL_DIR>/scripts/export-blogs.sh`（脚本遍历 `<PROJECT_DIR>/*.md`，输出到 `<PROJECT_DIR>/pdf/`）

## 关键事实

- **`--embed-resources` 对 PDF 是空操作。** 它只对 HTML 输出生效。PDF 的图片自包含由 pandoc 内部 MediaBag 机制自动处理（HTML 系引擎走 `makeSelfContained` 转 data URI，LaTeX 系走 `\includegraphics` + 临时文件，最终图片数据都嵌入 PDF）。
- **不要加 `--number-sections`。** 博客正文已手写编号，叠加自动编号会重复。
- **weasyprint 不支持中文锚点跳转。** TL;DR 里的 `§` 内部链接会报 ERROR，不影响内容渲染，忽略即可。
- **CSS 控制字体。** `<SKILL_DIR>/references/export-style.css` 里 `font-family: "Maple Mono NF CN"` 指定正文字体，按需修改。

## 排版参数

`<SKILL_DIR>/references/export-style.css` 定义了：

- 页边距 2cm/1.5cm，页脚页码
- 正文 10.5pt，行高 1.7
- H1 20pt 带下划线，H2 15pt 带左侧色条
- 代码块深色背景圆角，表格斑马纹
- blockquote 左侧色条 + 浅底

来源：pandoc 官方手册 + pandoc 源码 `src/Text/Pandoc/PDF.hs` + weasyprint 官方文档。完整调研报告：`~/research/.pi-subagents/artifacts/outputs/be7be2a8-02ac-4317-b5da-91dc3bcd33f8/research.md`
