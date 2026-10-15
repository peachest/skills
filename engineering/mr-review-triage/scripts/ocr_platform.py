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


# CI statuses meaning "still in flight" — union of GitLab pipeline and
# GitHub check-run states. Terminal states (success, failed, skipped,
# canceled, completed, ...) and unknown values let the gate proceed.
_IN_FLIGHT_STATUSES = {
    "created", "waiting_for_resource", "preparing", "pending",
    "running", "queued", "in_progress",
}


def pipeline_in_flight(status):
    """True while a CI pipeline / check-run status is still in flight."""
    return str(status).strip().lower() in _IN_FLIGHT_STATUSES


def run_pipeline_gate(platform, mr_or_pr_id, skip=False):
    """Re-pull timing gate (spec #57 Amendment R2, 修订 B), script-executed.

    pull/verify query the head-ref CI status (GitLab head_pipeline /
    GitHub check runs) and exit 2 while it is in flight — the completion
    gate becomes "gate exit 0 AND last re-pull happened after CI completed",
    with --skip-pipeline-check as the explicit escape hatch. No CI on the
    head ref (or an undeterminable status) is a stderr note, not an error —
    the thread-state check downstream still fails closed on real problems.
    """
    if skip:
        return
    if platform == "github":
        from ocr_github import check_runs_status
        status = check_runs_status(mr_or_pr_id)
        kind = "check runs"
    else:
        from ocr_gitlab import head_pipeline_status
        status = head_pipeline_status(mr_or_pr_id)
        kind = "pipeline"
    if not status:
        print(f"note: no CI {kind} status found on head (no CI configured, or "
              f"status fetch failed) — proceeding without the timing gate",
              file=sys.stderr)
        return
    if pipeline_in_flight(status):
        print(f"ERROR: CI {kind} on head not finished (status: {status}) — "
              f"acting now would read a stale review state; re-run after it "
              f"completes or pass --skip-pipeline-check to override",
              file=sys.stderr)
        sys.exit(2)


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
