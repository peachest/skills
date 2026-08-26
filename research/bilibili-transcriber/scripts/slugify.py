#!/usr/bin/env python3
"""
slugify.py — Sanitize a raw title into a filesystem-safe, UTF-8-safe slug.

Why this exists: Bilibili titles can contain characters illegal in file/dir
names (`/ \ : * ? " < > |`), control characters, and whitespace runs. A raw
*byte* truncation (e.g. shell `head -c 60`) can cut a multi-byte UTF-8
character in half, producing **illegal byte sequences** in the resulting
directory name. This helper truncates by *code point* and then verifies the
result round-trips through UTF-8, so the slug is always a valid file name.

Usage (pipe):
    echo "$RAW_TITLE" | python3 <SKILL_DIR>/scripts/slugify.py [max_chars]

Exit: 0 with the slug on stdout (or "unknown" when input is empty).
"""

import re
import sys

ILLEGAL = re.compile(r'[\\/:*?"<>|]')
CONTROL = re.compile(r"[\x00-\x1f\x7f]+")


def slugify(title: str, max_chars: int = 60) -> str:
    """Return a filesystem-safe slug with at most `max_chars` code points."""
    if not title:
        return "unknown"
    # Control characters (incl. newline/CR) become spaces; collapse whitespace
    s = CONTROL.sub(" ", title)
    s = re.sub(r"\s+", " ", s).strip(" .")
    # Replace filename-illegal characters
    s = ILLEGAL.sub("_", s)
    # Truncate by code point — never splits a UTF-8 sequence
    s = s[:max_chars].rstrip(" .")
    # Final safety: must encode to valid UTF-8 (drops lone surrogates)
    s = s.encode("utf-8", errors="ignore").decode("utf-8")
    return s or "unknown"


if __name__ == "__main__":
    raw = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(slugify(raw))