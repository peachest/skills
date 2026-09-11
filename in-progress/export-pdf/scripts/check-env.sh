#!/bin/bash
# check-env.sh — verify every runtime assumption of export-pdf skill.
# PASS/WARN/FAIL per item; any FAIL → exit 1 (the FAIL lines are the setup guide).

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
fails=0

# 1. pandoc (system CLI, >= 3.0 — must be the real CLI, not a python wrapper)
if command -v pandoc >/dev/null 2>&1; then
    ver=$(pandoc --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
    major=${ver%%.*}
    if [ -n "$major" ] && [ "$major" -ge 3 ]; then
        echo "PASS pandoc $(pandoc --version | head -1 | awk '{print $2}')"
    else
        echo "FAIL pandoc too old ($ver < 3.0) — install pandoc >= 3.0 via system package"
        fails=1
    fi
else
    echo "FAIL pandoc not on PATH — apt install pandoc (>= 3.0 required)"
    fails=1
fi

# 2. weasyprint (uv tool install puts it on PATH)
if command -v weasyprint >/dev/null 2>&1; then
    echo "PASS weasyprint (PATH) $(weasyprint --version 2>/dev/null || echo '')"
else
    echo "FAIL weasyprint not on PATH — bootstrap: uv tool install weasyprint --with pymupdf"
    fails=1
fi

# 3. Chinese font (weasyprint renders CJK as blank/tofu without one)
zh_fonts=$(fc-list :lang=zh 2>/dev/null | wc -l)
if [ "$zh_fonts" -ge 1 ]; then
    echo "PASS Chinese font available ($zh_fonts families via fc-list)"
else
    echo "FAIL no Chinese font — mkdir -p ~/.fonts && curl -sL --retry 3 -o ~/.fonts/NotoSansSC.ttf 'https://raw.githubusercontent.com/google/fonts/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf' && fc-cache -f"
    fails=1
fi

# 4. pymupdf (optional — page count in the report; rides along with the
#    weasyprint uv-tool env when installed via `--with pymupdf`)
PAGE_PY=""
if command -v weasyprint >/dev/null 2>&1; then
    WP_PY="$(dirname "$(realpath "$(command -v weasyprint)")")/python"
    [ -x "$WP_PY" ] && "$WP_PY" -c 'import pymupdf' >/dev/null 2>&1 && PAGE_PY="$WP_PY"
fi
if [ -n "$PAGE_PY" ]; then
    echo "PASS pymupdf (weasyprint uv-tool env)"
elif python3 -c "import pymupdf" >/dev/null 2>&1; then
    echo "PASS pymupdf (system python3)"
else
    echo "WARN pymupdf missing — page count will show '?'. Optional: uv tool install weasyprint --with pymupdf (reinstall with the extra)"
fi

[ "$fails" -eq 0 ] || exit 1
