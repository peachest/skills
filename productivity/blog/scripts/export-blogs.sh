#!/bin/bash
set -euo pipefail

# <PROJECT_DIR> = blogs/ directory (first arg or default)
PROJECT_DIR="${1:-$HOME/research/infer-cost/blogs}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$PROJECT_DIR/pdf"
CSS_FILE="$SKILL_DIR/references/export-style.css"

mkdir -p "$OUT_DIR"

echo "=========================================="
echo "  批量导出博客 PDF（pandoc + weasyprint）"
echo "  PROJECT_DIR: $PROJECT_DIR"
echo "=========================================="
echo ""

for md_file in "$PROJECT_DIR"/*.md; do
    [ "$(basename "$md_file")" = "STYLE-GUIDE.md" ] && continue
    filename=$(basename "$md_file" .md)
    pdf_file="$OUT_DIR/${filename}.pdf"

    echo "▶ 导出: $filename.md → ${filename}.pdf"

    # 从 md 第一行提取标题（去掉 # 和前后空格）
    title=$(head -1 "$md_file" | sed 's/^#\+ *//' | sed 's/ *$//')

    pandoc "$md_file" \
        -o "$pdf_file" \
        --pdf-engine=weasyprint \
        --css="$CSS_FILE" \
        --resource-path="$PROJECT_DIR" \
        --metadata title="$title" \
        --standalone \
        --toc \
        --toc-depth=2 \
        2>&1 | grep -v 'WARNING: Ignored' || true

    if [ -f "$pdf_file" ]; then
        size=$(du -h "$pdf_file" | cut -f1)
        pages=$(python3 -c "import fitz; print(fitz.open('$pdf_file').page_count)" 2>/dev/null || echo "?")
        echo "  ✅ $size | $pages 页"
    else
        echo "  ❌ 失败"
    fi
    echo ""
done

echo "=========================================="
echo "全部完成！输出目录: $OUT_DIR"
echo "=========================================="
ls -lh "$OUT_DIR"/*.pdf
