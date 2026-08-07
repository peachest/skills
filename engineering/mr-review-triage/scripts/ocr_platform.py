"""Platform detection and dispatch for OCR review pipeline scripts.

Detects whether the current repo is GitLab or GitHub based on git remote,
and provides a unified `detect_platform()` function used by both
ocr-pull-discussions.py and ocr-post-labels.py.
"""

import os
import subprocess


def detect_platform():
    """Detect the platform from git remote URL.

    Returns:
        "gitlab" if remote points at a GitLab instance,
        "github" if remote points at github.com.

    Override with env var OCR_PLATFORM=gitlab|github.
    """
    override = os.environ.get("OCR_PLATFORM", "").strip().lower()
    if override in ("gitlab", "github"):
        return override

    try:
        r = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10,
        )
        url = r.stdout.strip().lower()
    except Exception:
        url = ""

    if "github.com" in url:
        return "github"
    # gitlab.com or self-hosted GitLab (internal.example.com, etc.)
    # Default: anything non-github is treated as gitlab
    return "gitlab"
