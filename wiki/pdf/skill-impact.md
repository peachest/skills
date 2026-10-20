# pdf — skill-impact 台账

## 2026-10-20 创建 skill（合并 export-pdf，用户拍板）
- 提案: 新建统一 PDF skill——覆盖 md/HTML→PDF 导出、文本提取（pypdf）、拆分/合并/旋转（pypdf）、PDF↔图片（pymupdf/img2pdf）、OCR（可选 tesseract 链）；环境统一 uv（`uv run --with` 零 venv，md→PDF 链例外走系统 pandoc + `uv tool install weasyprint`，原因=uv 的 python-pandoc 陷阱）；承接并删除原 export-pdf skill（方案 A：删除，pdf 为唯一入口，由编排方转达用户拍板）
- 落点: 新建 `in-progress/pdf/`（SKILL.md 场景路由表 + runtime.conf.example + scripts/check-env.sh 新增 uv/pypdf 检查 + scripts/export-pdf.sh 与 references/style.css 原样承接自 export-pdf）；删除 `in-progress/export-pdf/` 及其 ~/.agents/skills 安装副本（npx skills remove）；productivity/blog/SKILL.md 导出路由 `/skill:export-pdf` → `/skill:pdf`
- 验证: check-env.sh 6 项全绿（uv/pandoc/weasyprint/中文字体/pymupdf/pypdf）；自测 ①md→PDF（中文+表格+图片内联+代码块）24K/1页 ②pypdf 提取同一 PDF 中文正确；源仓 vs 安装副本 diff 一致；全库 grep 无 /skill:export-pdf 残留（lock 已清）
- 状态: accepted
- 关联: export-pdf 原 key facts 全部并入 pdf/SKILL.md（逐项 grep 核对覆盖）；blog skill 的博客 PDF 默认样式说明随之指向 pdf skill

## 2026-10-20 文本提取切换 markitdown（用户指令）
- 提案: PDF→文本首选链从 pypdf 换成 markitdown（保标题/结构，直接产 Markdown，兼收 docx/xlsx/pptx）；pypdf 降级为纯文本备选+页操作（拆/合/旋转）专用
- 落点: SKILL.md 场景路由表+提取节重写+description；runtime.conf.example；check-env.sh 第 5 项改 markitdown[pdf]（FAIL），pypdf 降为 WARN
- 验证: 本机实测 `uv run --with 'markitdown[pdf]' markitdown test.pdf` 成功（底层 pdfminer-six，标题层级保留）；check-env 7 项全绿；源仓 vs 安装副本 diff 一致
- 状态: accepted
- 坑位记录: ①裸 markitdown 缺 [pdf] extra 抛 MissingDependencyException ②转换失败退出码仍为 0——必须检查输出非空而非 exit code
