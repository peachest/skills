"""Shared GitLab API client for OCR review pipeline scripts.

Provides a single `curl()` function that handles token resolution,
subprocess curl invocation, -i header/body parsing, JSON decoding,
and retry with jitter + Retry-After support on transient failures.

Multi-instance aware: the GitLab host is derived from `git remote get-url origin`
(not hardcoded), the token is read from glab config for that host, and the `glab`
fallback passes `--hostname <host>` so self-hosted instances resolve correctly
(e.g. `internal.example.com` alongside `internal.example.com`).
"""

import json
import os
import random
import re
import subprocess
import time

# ponytail: global lock, per-account limits if throughput matters
MAX_RETRY_DELAY = 60.0

_PROJECT_ID_CACHE = None
_CONTEXT_CACHE = None


def _git_remote_url():
    """Return the origin remote URL, or '' on failure."""
    try:
        r = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=10,
        )
        return r.stdout.strip()
    except Exception:
        return ""


def _parse_host(url):
    """Derive (host, scheme) from a git remote or API URL.

    Handles:
      https://internal.example.com/ns/proj.git          -> ('internal.example.com', 'https')
      http://internal.example.com/ns/proj.git           -> ('internal.example.com', 'http')
      git@internal.example.com:ns/proj.git              -> ('internal.example.com', None)
      ssh://git@internal.example.com:10022/ns/proj.git  -> ('internal.example.com', None)

    The ssh port is dropped (the API host never carries the ssh port); the
    scheme is None for ssh remotes and is filled from glab config later.
    """
    url = (url or "").strip()
    if not url:
        return None, None
    m = re.match(r"^(https?)://([^/:]+)(?::\d+)?(?:/|$)", url)
    if m:
        return m.group(2), m.group(1)
    m = re.match(r"^(?:ssh://)?[^@/]+@([^/:]+)(?::\d+)?", url)
    if m:
        return m.group(1), None
    return None, None


def _glab_config():
    """Load glab CLI config YAML (hosts -> {token, api_host, api_protocol})."""
    try:
        import yaml  # PyYAML — used for multi-instance token resolution
    except ImportError:
        return {}
    for path in (
        os.path.expanduser("~/.config/glab-cli/config.yml"),
        os.path.expanduser("~/.config/glab-cli/config.yaml"),
    ):
        if os.path.exists(path):
            try:
                with open(path) as f:
                    cfg = yaml.safe_load(f)
                return cfg if isinstance(cfg, dict) else {}
            except Exception:
                return {}
    return {}


def resolve_gitlab_context():
    """Resolve (base_url, host, token, header_name) for the GitLab instance.

    Multi-instance aware. Priority:
      1. CI_SERVER_URL env (explicit override; host parsed from it)
      2. git remote host, with scheme / api_host / token read from glab config
         for that host — glab config is the canonical token source when several
         GitLab instances are configured (a stale generic env token from a
         different instance would otherwise 401)
      3. env token fallback (GITLAB__PERSONAL_ACCESS_TOKEN > GITLAB_API_TOKEN > CI_JOB_TOKEN)

    Cached in module-level _CONTEXT_CACHE.
    """
    global _CONTEXT_CACHE
    if _CONTEXT_CACHE is not None:
        return _CONTEXT_CACHE

    glab = _glab_config()
    hosts = glab.get("hosts", {}) or {}

    env_url = os.environ.get("CI_SERVER_URL", "").strip()
    if env_url:
        host, scheme = _parse_host(env_url)
        base_url = env_url.rstrip("/")
    else:
        host, scheme = _parse_host(_git_remote_url())
        if not host:
            host = "gitlab.com"
        hcfg = hosts.get(host)
        hcfg = hcfg if isinstance(hcfg, dict) else {}
        api_host = hcfg.get("api_host") or host
        if scheme is None:
            scheme = hcfg.get("api_protocol") or "https"
        base_url = f"{scheme}://{api_host}"

    # Token: prefer the glab config token for the specific host.
    hcfg = hosts.get(host)
    hcfg = hcfg if isinstance(hcfg, dict) else {}
    token = hcfg.get("token", "")
    header_name = "PRIVATE-TOKEN"
    if not token:
        env_pat = os.environ.get("GITLAB__PERSONAL_ACCESS_TOKEN") \
            or os.environ.get("GITLAB_API_TOKEN")
        token = env_pat or os.environ.get("CI_JOB_TOKEN", "")
        if token and not env_pat:
            header_name = "JOB-TOKEN"

    _CONTEXT_CACHE = (base_url, host, token, header_name)
    return _CONTEXT_CACHE


def get_project_id():
    """Resolve GitLab project ID.

    Priority: CI_PROJECT_ID > glab from git remote (with --hostname).
    Result cached in module-level _PROJECT_ID_CACHE.
    """
    global _PROJECT_ID_CACHE
    if _PROJECT_ID_CACHE is not None:
        return _PROJECT_ID_CACHE

    pid = os.environ.get("CI_PROJECT_ID", "")
    if pid:
        _PROJECT_ID_CACHE = pid
        return pid

    _base_url, host, _token, _header = resolve_gitlab_context()

    # Local fallback: parse namespace/project from git remote, resolve via glab
    try:
        url = _git_remote_url()
        # Parse path from git URL. Handles:
        #   git@host:ns/proj.git              → ns/proj
        #   ssh://git@host:port/ns/proj.git   → ns/proj
        #   https://host/ns/proj.git          → ns/proj
        from urllib.parse import urlparse, quote_plus
        if "://" in url:
            path = urlparse(url).path
        else:
            path = url.split(":", 1)[-1]
        path = path.strip("/").removesuffix(".git")
        if "/" in path:
            # Encode namespace/project for API: llm/llmops/hami/ppu-device-plugin → llm%2Fllmops%2Fhami%2Fppu-device-plugin
            encoded = quote_plus(path, safe="")
            cmd = ["glab", "api", f"projects/{encoded}"]
            if host:
                # --hostname is required for self-hosted instances; without it
                # glab defaults to gitlab.com and the lookup fails.
                cmd += ["--hostname", host]
            r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
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
    base_url, _host, token, auth_header = resolve_gitlab_context()

    for attempt in range(retries + 1):
        url = endpoint if endpoint.startswith("http") else f"{base_url}/api/v4{endpoint}"
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
