---
name: export-pdf
description: Export Markdown documents to self-contained PDF via pandoc + weasyprint (images inlined, fonts embedded). Use when the user asks to 导出 PDF / export to PDF / md 转 pdf / generate a PDF from markdown, whether a single file or a whole directory. Carries the vetted toolchain facts (weasyprint via uv tool, the `uv tool run` pandoc trap, Chinese font strategy, harmless anchor warnings) so the agent does not re-derive them.
---

# Export Markdown → PDF

Converts one or more Markdown files into self-contained PDFs (images inlined,
fonts embedded) using system pandoc + weasyprint, with a Chinese-friendly
stylesheet.

`<SKILL_DIR>` is this skill's directory. `<PROJECT_DIR>` is the directory
containing the markdown being exported.

## Workflow

1. Run `bash <SKILL_DIR>/scripts/check-env.sh`. If it FAILs, fix per the FAIL
   message (see "Environment bootstrap" below) and re-run until green.
2. Export:
   - Single file: `bash <SKILL_DIR>/scripts/export-pdf.sh <PROJECT_DIR>/input.md`
   - Whole directory: `bash <SKILL_DIR>/scripts/export-pdf.sh <PROJECT_DIR>`
     (every top-level `*.md`; pass `--recursive` to include subdirectories)
3. Report output path(s), size, and page count to the user.

## Script reference

```
bash <SKILL_DIR>/scripts/export-pdf.sh [options] <file.md | dir> [more paths...]

Options:
  -o, --outdir DIR    output directory (default: <source dir>/pdf/)
  --css FILE          custom stylesheet (default: <SKILL_DIR>/references/style.css)
  --no-toc            skip table of contents
  --toc-depth N       TOC depth (default 2)
  --title-prefix P    prefix for --metadata title (title itself = first H1)
  --recursive         with a directory arg, also descend into subdirs
  --exclude GLOB      basename glob to skip (repeatable; STYLE-GUIDE.md,
                      README.md always skipped in directory mode)
```

Per-file output goes to `<outdir>/<basename>.pdf`.

## Environment bootstrap (when check-env FAILs)

- **weasyprint missing** — one command, installs to the uv tool standard
  location with the optional pymupdf extra for page counts:

  ```bash
  uv tool install weasyprint --with pymupdf
  ```

- **No Chinese font** — download Noto Sans SC variable font (16.9MB) into
  `~/.fonts` and refresh the cache:

  ```bash
  mkdir -p ~/.fonts && cd ~/.fonts
  curl -sL --retry 3 -o NotoSansSC.ttf \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"
  fc-cache -f
  ```

  The full "Maple Mono NF CN" family is 159MB; Noto Sans SC is the light
  option and the default stylesheet falls back to it automatically.

## Key facts (do not re-derive)

- **`uv tool run --with weasyprint pandoc` is a trap**: it installs the
  *Python* `pandoc` package, which shadows the system pandoc CLI and behaves
  differently. Always use system pandoc, with weasyprint provided separately
  via `uv tool install weasyprint`.
- **`--embed-resources` is a no-op for PDF** output. Image self-containment
  for PDF is handled by pandoc's internal MediaBag (HTML-family engines go
  through `makeSelfContained` → data URIs; LaTeX-family via `\includegraphics`
  + temp files). Do not add the flag.
- **Do not add `--number-sections`** when the source already hand-numbers
  headings (e.g. blog posts); it duplicates the numbering.
- **weasyprint cannot jump to CJK anchors** and logs `ERROR ... anchor` /
  "Links are not available" lines for internal links like `§` references.
  These are harmless — content renders fine. The export script filters them.
- **weasyprint ≥ 70 logs `Using fontTools instead of HarfBuzz-Subset`** per
  embedded CJK font (unless system libharfbuzz-subset is installed). Cosmetic
  — subsetting still works via fontTools. Filtered by the export script.
- **`--resource-path=<source dir>`** must point at the directory containing
  the markdown (and its images) so relative image paths resolve.

## Custom styling

The default stylesheet (`<SKILL_DIR>/references/style.css`) provides: 2cm/1.5cm
margins with page-number footer, 10.5pt body at line-height 1.7, styled
H1/H2/H3, dark rounded code blocks, zebra-striped tables, and blockquote
accents. Font-family is a fallback chain ("Maple Mono NF CN" → "Noto Sans SC"
→ "WenQuanYi Zen Hei" → sans-serif), so it adapts to whichever CJK font the
node has. Override per-run with `--css`, or edit the file for a project-wide
look.

Source of the toolchain facts: pandoc manual + pandoc source
(`src/Text/Pandoc/PDF.hs`) + weasyprint docs. Full research report:
`~/research/.pi-subagents/artifacts/outputs/be7be2a8-02ac-4317-b5da-91dc3bcd33f8/research.md`
