---
name: pdf
description: Unified PDF toolkit — export Markdown/HTML to PDF, extract text, split/merge/rotate/delete pages, PDF↔image conversion, and OCR. Use when the user asks to 导出 PDF / md 转 pdf / export to PDF / generate a PDF, 提取 PDF 文本 / PDF 文字识别 / parse a PDF, 合并/拆分/旋转/删除 PDF 页面 / split merge rotate PDF pages, PDF 转图片 / 图片转 PDF / pdf to images, or PDF OCR / 扫描件识别. All Python deps run through `uv run --with` — no venv to maintain. Carries vetted toolchain facts (the `uv tool run` pandoc trap, Chinese font strategy, markitdown[pdf] as the verified text-extraction path) so the agent does not re-derive them.
---

# PDF Toolkit

One skill for the whole PDF surface: **export → extract → manipulate → convert → OCR**.
`<SKILL_DIR>` is this skill's directory. `<PROJECT_DIR>` is the directory of the
file being processed.

## Environment

All Python dependencies run ephemerally via `uv run --with <pkg>` (uv-managed
cache, no venv, nothing committed to the repo). The md→PDF export chain is the
one exception: it needs **system pandoc** (a Haskell CLI — Python "pandoc"
packages from uv are a trap, see Key Facts) plus `uv tool install weasyprint`.

Before first use in a session: `bash <SKILL_DIR>/scripts/check-env.sh` —
every FAIL line is its own setup command; fix and re-run until green.

## Scenario routing

| Scenario | Toolchain | How |
|---|---|---|
| md → PDF (single file or directory) | pandoc + weasyprint | `bash <SKILL_DIR>/scripts/export-pdf.sh <file.md\|dir>` |
| HTML → PDF | weasyprint CLI | `weasyprint page.html out.pdf` |
| PDF → Markdown（保标题/结构，首选） | markitdown | `uv run --with 'markitdown[pdf]' markitdown in.pdf > out.md` |
| PDF → 纯文本（快，无结构） | pypdf | `uv run --with pypdf python -c '...'`（snippet below） |
| split / merge / rotate / delete pages | pypdf | `uv run --with pypdf python -c '...'` (snippets below) |
| docx/xlsx/pptx → Markdown | markitdown | 同上，markitdown 自动按扩展名路由转换器 |
| PDF → images, page rendering, metadata | pymupdf | `uv run --with pymupdf python -c '...'` |
| images → PDF | img2pdf | `uv run --with img2pdf img2pdf *.png -o out.pdf` |
| scanned PDF OCR | tesseract (system) + pytesseract/pymupdf | see OCR section |

Snippets are copy-paste starting points — adapt paths, don't re-derive APIs.

## md → PDF export (pandoc + weasyprint)

```bash
bash <SKILL_DIR>/scripts/export-pdf.sh <PROJECT_DIR>/input.md          # single file
bash <SKILL_DIR>/scripts/export-pdf.sh <PROJECT_DIR>                   # every top-level *.md
bash <SKILL_DIR>/scripts/export-pdf.sh <PROJECT_DIR> --recursive       # incl. subdirs
```

Options: `-o/--outdir DIR`, `--css FILE` (default: skill's `references/style.css`),
`--no-toc`, `--toc-depth N`, `--title-prefix P`, `--exclude GLOB`.
Output: `<outdir>/<basename>.pdf`; report path, size, page count to the user.

Bootstrap (when check-env FAILs):

```bash
# weasyprint (uv tool, with pymupdf extra for page counts)
uv tool install weasyprint --with pymupdf

# Chinese font (weasyprint renders CJK as tofu without one) — light fallback:
mkdir -p ~/.fonts && curl -sL --retry 3 -o ~/.fonts/NotoSansSC.ttf \
  "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf" && fc-cache -f

# preferred body font (Maple Mono Normal NF CN, ~20MB×2, not the whole 152MB zip):
cd ~/tmp && gh release download v7.9 --repo subframe7536/maple-font \
    --pattern 'MapleMonoNormal-NF-CN.zip'
unzip -o -q MapleMonoNormal-NF-CN.zip \
    'MapleMonoNormal-NF-CN-Regular.ttf' 'MapleMonoNormal-NF-CN-Bold.ttf' -d ~/.fonts
fc-cache -f
```

## Text extraction

**首选 markitdown**（微软“万物转 Markdown”，保住标题层级/结构，直接产出可投喂 LLM 的 md）：

```bash
uv run --with 'markitdown[pdf]' markitdown input.pdf > input.md
```

**备选 pypdf 纯文本**（更快、依赖更轻，只要文字不要结构时用）：

```bash
uv run --with pypdf python -c '
from pypdf import PdfReader
r = PdfReader("input.pdf")
text = "\n\n".join((p.extract_text() or "") for p in r.pages)
open("input.txt", "w").write(text)
print(f"{len(r.pages)} pages, {len(text)} chars")
'
```

For layout-aware extraction (tables, columns), upgrade to
`uv run --with pymupdf` (`page.get_text("blocks")` or `"words"`) — pymupdf's
extractor is stronger on multi-column PDFs than pypdf's.

## Page manipulation (pypdf)

```bash
# merge
uv run --with pypdf python -c '
from pypdf import PdfWriter
w = PdfWriter()
for f in ["a.pdf", "b.pdf"]: w.append(f)
w.write("merged.pdf")'

# split: keep pages 3-5 (1-based inclusive); rotate: 90/180/270
uv run --with pypdf python -c '
from pypdf import PdfReader, PdfWriter
r = PdfReader("input.pdf"); w = PdfWriter()
for i in range(2, 5): w.add_page(r.pages[i])
# w.pages[0].rotate(90)  # rotate instead, if that is the task
w.write("out.pdf"); print(f"{len(w.pages)} pages written")'
```

## PDF ↔ images (pymupdf / img2pdf)

```bash
# PDF → PNG per page (200 dpi)
uv run --with pymupdf python -c '
import pymupdf
doc = pymupdf.open("input.pdf")
for i, page in enumerate(doc):
    page.get_pixmap(dpi=200).save(f"page-{i+1:03d}.png")
print(f"{doc.page_count} pages rendered")'

# images → PDF (lossless, one page per image)
uv run --with img2pdf img2pdf *.png -o out.pdf
```

## OCR (scanned PDFs — optional chain)

Only when the PDF has no text layer. Requires system `tesseract` with
`chi_sim` + `eng` language packs (`apt install tesseract-ocr tesseract-ocr-chi-sim`),
then:

```bash
uv run --with pymupdf pytesseract python -c '
import pymupdf, pytesseract
from PIL import Image
import io
doc = pymupdf.open("input.pdf")
with open("input.txt", "w") as out:
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        out.write(pytesseract.image_to_string(img, lang="chi_sim+eng") + "\n\n")
'
```

## Key facts (do not re-derive)

- **`uv tool run --with weasyprint pandoc` is a trap**: it installs the
  *Python* `pandoc` package, which shadows the system pandoc CLI and behaves
  differently. Always use system pandoc, with weasyprint provided separately
  via `uv tool install weasyprint`.
- **markitdown 必须 `[pdf]` extra**：裸 `markitdown` 遇到 PDF 抛
  MissingDependencyException（PdfConverter 缺 pdfminer-six 等依赖）。且 CLI
  转换失败时**退出码仍为 0**——脚本里要检查输出文件非空，不能只看 exit code。
- **markitdown via `uv run --with 'markitdown[pdf]'` 是已验证的文本提取路径**
  （底层 pdfminer-six；本节点 pdftotext 不存在、python3 无 pip，uv-run 是唯一
  正道）。pypdf 仍用于纯文本提取和页操作（拆/合/旋转）。
- **`--embed-resources` is a no-op for PDF** output. Image self-containment
  is handled by pandoc's internal MediaBag. Do not add the flag.
- **Do not add `--number-sections`** when the source already hand-numbers
  headings (e.g. blog posts); it duplicates the numbering.
- **weasyprint cannot jump to CJK anchors** and logs `ERROR ... anchor` /
  "Links are not available" lines for internal links. Harmless — the export
  script filters them.
- **weasyprint ≥ 70 logs `Using fontTools instead of HarfBuzz-Subset`** per
  embedded CJK font. Cosmetic — filtered by the export script.
- **Font family names differ per Maple variant**: the *Normal* build
  registers as `Maple Mono Normal NF CN`, not `Maple Mono NF CN` — check with
  `fc-list | grep -i maple` before writing CSS.
- **`--resource-path=<source dir>`** must point at the directory containing
  the markdown (and its images) so relative image paths resolve.

## Custom styling

The default stylesheet (`<SKILL_DIR>/references/style.css`) provides: 2cm/1.5cm
margins with page-number footer, 10.5pt body at line-height 1.7, styled
headings, dark rounded code blocks, zebra-striped tables, and blockquote
accents. Font chain: "Maple Mono Normal NF CN" → "Noto Sans SC" →
"WenQuanYi Zen Hei" → sans-serif. Override per-run with `--css`, or edit the
file for a project-wide look.
