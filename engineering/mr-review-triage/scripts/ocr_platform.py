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
    # gitlab.com or self-hosted GitLab (gitlab.blue.example, etc.)
    # Default: anything non-github is treated as gitlab
    return "gitlab"


def triage_state_dir(mr_id=None):
    """Resolve the .triage state directory against cwd via realpath.

    State paths are always derived from the working directory — never
    expanduser($HOME): peer sessions can run the same checkout under
    different $HOME values (/home/x vs /mnt/disk1/x), and $HOME-derived
    paths split state across two locations and FileNotFoundError later.
    With mr_id, returns the per-MR state dir .triage/<mr_id>/; without,
    the flat .triage/ working dir. Pure path computation — callers make
    the directory when writing. Shared by post-labels and verdict.py.
    """
    base = os.path.realpath(os.path.join(os.getcwd(), ".triage"))
    return os.path.join(base, str(mr_id)) if mr_id is not None else base
