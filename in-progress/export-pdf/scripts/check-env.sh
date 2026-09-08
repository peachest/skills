#!/bin/bash
# check-env.sh — verify every runtime assumption of export-pdf skill.
# PASS/WARN/FAIL per item; any FAIL → exit 1 (the FAIL lines are the setup guide).

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
RUNTIME_CONF="${RUNTIME_CONF:-$SKILL_DIR/runtime.conf}"

[ -f "$RUNTIME_CONF" ] && . "$RUNTIME_CONF"
WEASYPRINT_VENV="${WEASYPRINT_VENV:-$HOME/.venvs/weasyprint}"

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

# 2. weasyprint (global CLI or dedicated venv)
if command -v weasyprint >/dev/null 2>&1; then
    echo "PASS weasyprint (PATH) $(weasyprint --version 2>/dev/null || echo '')"
elif [ -x "$WEASYPRINT_VENV/bin/weasyprint" ]; then
    echo "PASS weasyprint (venv $WEASYPRINT_VENV) $("$WEASYPRINT_VENV/bin/weasyprint" --version 2>/dev/null || echo '')"
else
    echo "FAIL weasyprint not found (neither PATH nor $WEASYPRINT_VENV) — bootstrap: uv venv $WEASYPRINT_VENV && uv pip install --python $WEASYPRINT_VENV/bin/python weasyprint"
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

# 4. pymupdf (optional — page count in the report; lives in the weasyprint venv)
if [ -x "$WEASYPRINT_VENV/bin/python" ] && "$WEASYPRINT_VENV/bin/python" -c 'import pymupdf' >/dev/null 2>&1; then
    echo "PASS pymupdf (in $WEASYPRINT_VENV)"
elif python3 -c "import fitz" >/dev/null 2>&1; then
    echo "PASS pymupdf (system python3)"
else
    echo "WARN pymupdf missing — page count will show '?'. Optional: uv pip install --python $WEASYPRINT_VENV/bin/python pymupdf"
fi

# 5. runtime.conf (optional; only carries WEASYPRINT_VENV override)
if [ -f "$RUNTIME_CONF" ]; then
    echo "PASS runtime.conf loaded"
else
    echo "WARN runtime.conf absent — using defaults (WEASYPRINT_VENV=$WEASYPRINT_VENV). Copy runtime.conf.example to runtime.conf to override."
fi

[ "$fails" -eq 0 ] || exit 1
