"""Shared GitHub API client for OCR review pipeline scripts.

Mirrors the ocr_gitlab.py interface: provides `curl()` and `get_project_id()`
so that ocr-pull-discussions.py and ocr-post-labels.py can use the same
calling convention across platforms.

Uses the `gh` CLI under the hood (subprocess), which handles auth, pagination,
and owner/repo inference automatically.
"""

import json
import os
import random
import re
import subprocess
import sys
import time

from ocr_platform import _git_remote_url

MAX_RETRY_DELAY = 60.0

_OWNER_REPO_CACHE = None


def _local_owner_repo():
    """Parse owner/repo from the configured remote URL ('' if not GitHub).

    git@github.com:owner/repo.git → owner/repo
    https://github.com/owner/repo.git → owner/repo
    """
    m = re.search(r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?$", _git_remote_url())
    return f"{m.group(1)}/{m.group(2)}" if m else ""


def get_project_id():
    """Resolve GitHub owner/repo.

    Priority: GITHUB_REPOSITORY env > parse from git remote.
    Returns "owner/repo" string (cached).
    """
    global _OWNER_REPO_CACHE
    if _OWNER_REPO_CACHE is not None:
        return _OWNER_REPO_CACHE

    repo = os.environ.get("GITHUB_REPOSITORY", "") or _local_owner_repo()
    _OWNER_REPO_CACHE = repo
    return repo


def probe_auth():
    """Auth probe: one repo lookup, compared against the local remote's path.

    Skipped when GITHUB_REPOSITORY env takes precedence — the project id then
    comes from env and there is no local remote path to compare (no error).
    Exits 2 naming OCR_REMOTE on mismatch; returns silently when the local
    remote yields no owner/repo to compare.
    """
    if os.environ.get("GITHUB_REPOSITORY", "").strip():
        return
    local_repo = _local_owner_repo()
    if not local_repo:
        return
    status, body, _ = curl(f"/repos/{local_repo}", retries=0)
    returned = body.get("full_name", "") if isinstance(body, dict) else ""
    if status == 200 and returned.casefold() == local_repo.casefold():
        return
    remote_name = os.environ.get("OCR_REMOTE", "").strip() or "origin"
    detail = f"HTTP {status}" if status else "request failed"
    got = f" (got full_name '{returned}')" if returned else ""
    print(f"AUTH PROBE FAILED: GET /repos/{local_repo} via gh → {detail}{got}",
          file=sys.stderr)
    print("gh's token does not serve this repo's project. Check OCR_REMOTE "
          f"(current: '{remote_name}') points at the remote hosting the "
          "review instance, and gh auth status.", file=sys.stderr)
    sys.exit(2)


def _resolve_token():
    """Resolve GitHub auth token.

    Priority: GITHUB_TOKEN > GH_TOKEN
    """
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN", "")


def _is_retryable(status):
    return status == 0 or status == 429 or (500 <= status < 600) or status == 408


def _sleep_for_retry(attempt, headers):
    retry_after = headers.get("retry-after", "")
    if retry_after:
        try:
            delay = float(retry_after)
        except (ValueError, TypeError):
            delay = 2 ** attempt
    else:
        delay = 2 ** attempt
    delay = min(delay, MAX_RETRY_DELAY)
    delay *= 0.75 + random.uniform(0, 0.5)
    time.sleep(delay)


def _parse_response(stdout_text):
    """Parse `gh api -i` output into (status, headers, body_text).

    gh api with -i flag emits HTTP headers + blank line + body.
    """
    # Split headers and body
    parts = stdout_text.split("\r\n\r\n", 1)
    if len(parts) != 2:
        parts = stdout_text.split("\n\n", 1)
    if len(parts) != 2:
        return 0, {}, ""

    header_text, body_text = parts
    header_lines = header_text.replace("\r", "").split("\n")

    status = 0
    if header_lines:
        parts_status = header_lines[0].split()
        if len(parts_status) >= 2:
            try:
                status = int(parts_status[1])
            except ValueError:
                pass

    headers = {}
    for line in header_lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    return status, headers, body_text


def curl(endpoint, *, method="GET", data=None, retries=2):
    """Make a GitHub API request via `gh api` with retry.

    Args:
        endpoint: API path, e.g. "/repos/owner/repo/pulls/42/comments"
                  (without /api prefix; gh api handles it).
                  For GraphQL, use "graphql" with method="graphql".
        method: HTTP method ("GET", "POST", "PUT", "PATCH", "DELETE").
        data: Body dict for non-GET, None for GET.
        retries: Max retry attempts on transient failures.

    Returns:
        (status: int, body: any, headers: dict)
        status=0  → failure after all retries
        body=None → JSON decode failure
    """
    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return (0, None, {})

    token = _resolve_token()

    for attempt in range(retries + 1):
        # Build gh api command
        # gh api automatically injects auth and handles the API base URL.
        # For REST endpoints, pass the path directly.
        if endpoint.startswith("http"):
            url = endpoint
        elif endpoint == "graphql":
            url = "graphql"
        else:
            url = endpoint

        cmd = ["gh", "api", "-i", "--method", method, url]

        if data is not None:
            if method == "GET":
                # Query params for GET
                for k, v in data.items():
                    cmd += ["-f", f"{k}={v}"]
            else:
                # JSON body for POST/PUT/PATCH
                cmd += ["--input", "-"]

        try:
            if data is not None and method != "GET":
                result = subprocess.run(
                    cmd, capture_output=True, text=True,
                    input=json.dumps(data), timeout=35,
                )
            else:
                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=35,
                )
        except Exception:
            result = subprocess.CompletedProcess(args=[], returncode=1)

        if result.returncode != 0:
            if attempt < retries:
                _sleep_for_retry(attempt, {})
                continue
            print(f"ERROR: gh api failed: {result.stderr.strip()}", file=sys.stderr)
            return (0, None, {})

        status, headers, body_text = _parse_response(result.stdout)

        if _is_retryable(status) and attempt < retries:
            _sleep_for_retry(attempt, headers)
            continue

        if not body_text:
            return (status, None, headers)

        try:
            body = json.loads(body_text)
        except json.JSONDecodeError:
            return (status, None, headers)

        return (status, body, headers)

    return (0, None, {})


def graphql(query, variables=None, retries=2):
    """Execute a GraphQL query via gh api.

    Args:
        query: GraphQL query string.
        variables: Dict of variables (optional).
        retries: Max retry attempts.

    Returns:
        (status: int, body: dict, headers: dict)
        body is the parsed GraphQL response (contains "data" and/or "errors").
    """
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(retries + 1):
        cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
        for k, v in (variables or {}).items():
            cmd += ["-F", f"{k}={v}"]

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=35,
            )
        except Exception:
            result = subprocess.CompletedProcess(args=[], returncode=1)

        if result.returncode != 0:
            if attempt < retries:
                _sleep_for_retry(attempt, {})
                continue
            print(f"ERROR: gh api graphql failed: {result.stderr.strip()}", file=sys.stderr)
            return (0, None, {})

        try:
            body = json.loads(result.stdout)
        except json.JSONDecodeError:
            return (0, None, {})

        return (200, body, {})

    return (0, None, {})
