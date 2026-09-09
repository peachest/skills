#!/bin/bash
set -euo pipefail

# Export Markdown → self-contained PDF (pandoc + weasyprint).
# Usage: export-pdf.sh [options] <file.md | dir> [more paths...]

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

CSS_FILE="$SKILL_DIR/references/style.css"
TOC_ARGS=(--toc --toc-depth=2)
TITLE_PREFIX=""
RECURSIVE=0
OUTDIR=""
EXCLUDES=()
INPUTS=()

usage() { sed -n '2,25p' "$0"; exit 2; }

while [ $# -gt 0 ]; do
    case "$1" in
        -o|--outdir)      OUTDIR="$2"; shift 2 ;;
        --css)            CSS_FILE="$2"; shift 2 ;;
        --no-toc)         TOC_ARGS=(); shift ;;
        --toc-depth)      TOC_ARGS=(--toc --toc-depth "$2"); shift 2 ;;
        --title-prefix)   TITLE_PREFIX="$2"; shift 2 ;;
        --recursive)      RECURSIVE=1; shift ;;
        --exclude)        EXCLUDES+=("$2"); shift 2 ;;
        -h|--help)        usage ;;
        *)                INPUTS+=("$1"); shift ;;
    esac
done

[ ${#INPUTS[@]} -gt 0 ] || usage
command -v pandoc >/dev/null || { echo "FAIL pandoc not on PATH" >&2; exit 1; }
command -v weasyprint >/dev/null || { echo "FAIL weasyprint not on PATH (see SKILL.md bootstrap)" >&2; exit 1; }

# Page-count python: prefer the python in weasyprint's uv-tool venv (has
# pymupdf via `uv tool install weasyprint --with pymupdf`), fall back to
# system python3.
PAGE_PY="python3"
WP_REAL="$(realpath "$(command -v weasyprint)")"
WP_PY="$(dirname "$WP_REAL")/python"
[ -x "$WP_PY" ] && "$WP_PY" -c 'import pymupdf' >/dev/null 2>&1 && PAGE_PY="$WP_PY"

# Expand inputs: dirs → *.md files (always skipping README.md/STYLE-GUIDE.md)
FILES=()
for input in "${INPUTS[@]}"; do
    if [ -d "$input" ]; then
        if [ "$RECURSIVE" -eq 1 ]; then
            while IFS= read -r -d '' f; do FILES+=("$f"); done \
                < <(find "$input" -name '*.md' -print0)
        else
            for f in "$input"/*.md; do [ -f "$f" ] && FILES+=("$f"); done
        fi
    elif [ -f "$input" ]; then
        FILES+=("$input")
    else
        echo "SKIP not found: $input" >&2
    fi
done
[ ${#FILES[@]} -gt 0 ] || { echo "FAIL no markdown files found" >&2; exit 1; }

ok=0; fail=0
for md_file in "${FILES[@]}"; do
    base=$(basename "$md_file")
    # skip always-excluded + user excludes
    skip=0
    for ex in README.md STYLE-GUIDE.md "${EXCLUDES[@]}"; do
        case "$base" in $ex) skip=1 ;; esac
    done
    [ "$skip" = 1 ] && { echo "SKIP (excluded): $base"; continue; }

    src_dir=$(dirname "$md_file")
    filename="${base%.md}"
    outdir="${OUTDIR:-$src_dir/pdf}"
    mkdir -p "$outdir"
    pdf_file="$outdir/$filename.pdf"

    # Title = first H1 of the md; fall back to filename
    title=$(head -1 "$md_file" | sed 's/^#\+ *//; s/ *$//')
    [ -n "$title" ] || title="$filename"
    [ -n "$TITLE_PREFIX" ] && title="$TITLE_PREFIX$title"

    echo "▶ $base → ${outdir/$HOME/\~}/$filename.pdf"
    # Filter harmless weasyprint noise: CJK-anchor errors (see SKILL.md key
    # facts) and unknown-CSS-property warnings ("WARNING: Ignored ...")
    if pandoc "$md_file" \
        -o "$pdf_file" \
        --pdf-engine=weasyprint \
        --css="$CSS_FILE" \
        --resource-path="$src_dir" \
        --metadata title="$title" \
        --standalone \
        "${TOC_ARGS[@]}" \
        2>&1 | grep -viE 'anchor|Links are not available|WARNING: Ignored|Using fontTools instead of HarfBuzz-Subset'; then
        :
    fi

    if [ -f "$pdf_file" ]; then
        size=$(du -h "$pdf_file" | cut -f1)
        pages=$($PAGE_PY -c "import pymupdf; print(pymupdf.open('$pdf_file').page_count)" 2>/dev/null || echo "?")
        echo "  ✅ $size | $pages 页"
        ok=$((ok+1))
    else
        echo "  ❌ 失败: $base"
        fail=$((fail+1))
    fi
done

echo ""
echo "完成: $ok 成功, $fail 失败"
[ "$fail" -eq 0 ]
