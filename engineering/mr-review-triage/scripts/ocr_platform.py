"""Platform detection and dispatch for OCR review pipeline scripts.

Detects whether the current repo is GitLab or GitHub based on git remote,
and provides a unified `detect_platform()` function used by both
ocr-pull-discussions.py and ocr-post-labels.py.

The git remote lookup lives in ONE helper here (`_git_remote_url`); the
GitLab/GitHub clients import it instead of keeping their own copies. The
remote name comes from OCR_REMOTE (default origin) so a fork-type repo —
origin pointing at the upstream GitHub, the review instance on another
remote — can redirect the whole derivation without touching config.
"""

import os
import subprocess
import sys


def _git_remote_url():
    """Return the configured remote's URL, or '' on failure.

    Remote name: OCR_REMOTE env (default origin). An explicit OCR_REMOTE that
    git cannot resolve is a config error → exit 2; a plain origin failure
    (bare/odd checkout) stays silent and yields '' as before.
    """
    remote = os.environ.get("OCR_REMOTE", "").strip() or "origin"
    try:
        r = subprocess.run(
            ["git", "remote", "get-url", remote],
            capture_output=True, text=True, timeout=10,
        )
        if r.returncode == 0:
            return r.stdout.strip()
        if remote != "origin":
            print(f"ERROR: OCR_REMOTE='{remote}' is not a git remote "
                  f"({r.stderr.strip().splitlines()[-1] if r.stderr.strip() else 'git failed'})",
                  file=sys.stderr)
            sys.exit(2)
        return ""
    except Exception:
        return ""


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

    url = _git_remote_url().lower()

    if "github.com" in url:
        return "github"
    # gitlab.com or self-hosted GitLab (gitlab.blue.example, etc.)
    # Default: anything non-github is treated as gitlab
    return "gitlab"


def run_auth_probe(platform):
    """Startup auth probe: verify derived host+token serve this repo's project.

    One project lookup compared against the local remote's path — a valid
    token on the wrong instance would otherwise pass and silently pull
    unrelated data. Exits 2 on mismatch. Skipped (no error) when there is
    no local remote path to compare: GITHUB_REPOSITORY env takes precedence
    over remote parsing on GitHub, and OCR_PLATFORM forces the platform so
    the remote→host derivation the probe validates is bypassed.
    """
    if os.environ.get("OCR_PLATFORM", "").strip().lower() in ("gitlab", "github"):
        return
    if platform == "github":
        from ocr_github import probe_auth
    else:
        from ocr_gitlab import probe_auth
    probe_auth()
