"""Shared GitLab API client for OCR review pipeline scripts.

Provides a single `curl()` function that handles token resolution,
subprocess curl invocation, -i header/body parsing, JSON decoding,
and retry with jitter + Retry-After support on transient failures.
"""

import json
import os
import random
import subprocess
import time

# ponytail: global lock, per-account limits if throughput matters
MAX_RETRY_DELAY = 60.0

_PROJECT_ID_CACHE = None


def get_project_id():
    """Resolve GitLab project ID.

    Priority: CI_PROJECT_ID > glab from git remote.
    Result cached in module-level _PROJECT_ID_CACHE.
    """
    global _PROJECT_ID_CACHE
    if _PROJECT_ID_CACHE is not None:
        return _PROJECT_ID_CACHE

    pid = os.environ.get("CI_PROJECT_ID", "")
    if pid:
        _PROJECT_ID_CACHE = pid
        return pid

    # Local fallback: parse namespace/project from git remote, resolve via glab
    try:
        r = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10,
        )
        url = r.stdout.strip()
        # Parse path from git URL. Handles:
        #   git@host:ns/proj.git  → ns/proj
        #   ssh://git@host:port/ns/proj.git → ns/proj
        #   https://host/ns/proj.git → ns/proj
        from urllib.parse import urlparse, quote_plus
        parsed = urlparse(url)
        path = parsed.path  # e.g. /llm/llmops/hami/ppu-device-plugin.git
        if not path:
            # git@host:ns/proj.git — urlparse puts everything in .path
            path = url.split(":", 1)[-1]
        path = path.strip("/").removesuffix(".git")
        if "/" in path:
            # Encode namespace/project for API: llm/llmops/hami/ppu-device-plugin → llm%2Fllmops%2Fhami%2Fppu-device-plugin
            encoded = quote_plus(path, safe="")
            r2 = subprocess.run(
                ["glab", "api", f"projects/{encoded}"],
                capture_output=True, text=True, timeout=15,
            )
            if r2.returncode == 0:
                try:
                    project = json.loads(r2.stdout)
                    pid = str(project.get("id", ""))
                except json.JSONDecodeError:
                    pid = ""
                if pid:
                    _PROJECT_ID_CACHE = pid
                    return pid
    except Exception:
        pass

    _PROJECT_ID_CACHE = ""
    return ""


def _resolve_auth():
    """Resolve GitLab API token and auth header.

    Priority: GITLAB__PERSONAL_ACCESS_TOKEN (CI + local) > GITLAB_API_TOKEN (legacy) > CI_JOB_TOKEN
    """
    token = os.environ.get("GITLAB__PERSONAL_ACCESS_TOKEN") \
         or os.environ.get("GITLAB_API_TOKEN") \
         or os.environ.get("CI_JOB_TOKEN", "")
    # PAT uses PRIVATE-TOKEN header; CI_JOB_TOKEN uses JOB-TOKEN
    use_pat = bool(os.environ.get("GITLAB__PERSONAL_ACCESS_TOKEN") or os.environ.get("GITLAB_API_TOKEN"))
    header_name = "PRIVATE-TOKEN" if use_pat else "JOB-TOKEN"
    return token, header_name


def _parse_headers_and_body(raw_output):
    """Split curl -i output into status code, headers dict, and body text."""
    parts = raw_output.split("\r\n\r\n", 1)
    if len(parts) != 2:
        parts = raw_output.split("\n\n", 1)
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


def _is_retryable(status):
    """Return True for transient failures worth retrying."""
    return status == 0 or status == 429 or (500 <= status < 600) or status == 408


def _sleep_for_retry(attempt, headers):
    """Compute sleep delay for retry attempt.

    Uses Retry-After header if present, otherwise exponential backoff with jitter.
    """
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


def curl(endpoint, *, method="GET", data=None, retries=2):
    """Make a GitLab API request via subprocess curl with retry.

    Args:
        endpoint: API path, e.g. "/projects/22412/merge_requests/1/notes?per_page=100"
        method: "GET" or "POST"
        data: Body dict for POST, None for GET
        retries: Max retry attempts on transient failures (status=0, 429, 5xx, 408).
                 Set to 0 to disable.

    Returns:
        (status: int, body: any, headers: dict)
        status=0  → curl/network failure after all retries
        body=None → JSON decode failure (including empty response)
        headers keys are always lowercase
    """
    token, auth_header = _resolve_auth()
    gitlab_url = os.environ.get("CI_SERVER_URL", "http://gitblue.transwarp.io")

    for attempt in range(retries + 1):
        url = endpoint if endpoint.startswith("http") else f"{gitlab_url}/api/v4{endpoint}"
        cmd = ["curl", "-s", "-i", "--max-time", "30",
               "-H", f"{auth_header}: {token}",
               "-H", "Content-Type: application/json"]
        if data is not None:
            cmd += ["-X", method, "-d", json.dumps(data)]
        cmd.append(url)

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        except Exception:
            result = subprocess.CompletedProcess(args=[], returncode=1)

        if result.returncode != 0:
            if attempt < retries:
                _sleep_for_retry(attempt, {})
                continue
            return (0, None, {})

        status, headers, body_text = _parse_headers_and_body(result.stdout)

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
