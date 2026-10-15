"""CLI-level tests for OCR_REMOTE env override + startup auth probe (spec #57 / ticket #63).

Single test seam per spec: real CLI invocation, platform API mocked offline via
fake curl/gh/glab executables + git ls-remote shim on PATH. Synthetic hostnames
only (gitlab.blue.example / github.com) — no internal names (pre-push sanitize).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

FORKEE_HOST = "gitlab.blue.example"
# Env that must never leak from the outer shell into a test run.
SCRUB = {
    "OCR_REMOTE", "OCR_PLATFORM", "CI_SERVER_URL", "CI_PROJECT_ID",
    "GITHUB_REPOSITORY", "GITLAB__PERSONAL_ACCESS_TOKEN", "GITLAB_API_TOKEN",
    "CI_JOB_TOKEN", "GITHUB_TOKEN", "GH_TOKEN", "OCR_BOT_LOGIN",
}


# ── offline fakes ────────────────────────────────────────────────────────

FAKE_CURL = """#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
url = args[-1]
method = args[args.index("-X") + 1] if "-X" in args else "GET"
log, routes = os.environ["FAKE_API_LOG"], json.load(open(os.environ["FAKE_ROUTES"]))
with open(log, "a") as f:
    f.write(f"curl {method} {url}\\n")
for r in routes:
    if r["match"] in url and r.get("method", method) == method:
        body = r["body"] if isinstance(r["body"], str) else json.dumps(r["body"])
        sys.stdout.write(f"HTTP/2 {r['status']}\\r\\ncontent-type: application/json\\r\\n\\r\\n{body}")
        sys.exit(0)
sys.stdout.write('HTTP/2 404\\r\\n\\r\\n{"message": "404 Not Found"}')
"""

FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
if args[:2] == ["api", "user"]:
    print(json.dumps({"login": "tester"})); sys.exit(0)
if args[0] == "pr":
    print("[]"); sys.exit(0)
url = args[-1]
log, routes = os.environ["FAKE_API_LOG"], json.load(open(os.environ["FAKE_ROUTES"]))
with open(log, "a") as f:
    f.write(f"gh GET {url}\\n")
for r in routes:
    if r["match"] in url and r.get("method", "GET") == "GET":
        body = r["body"] if isinstance(r["body"], str) else json.dumps(r["body"])
        sys.stdout.write(f"HTTP/2 {r['status']}\\r\\ncontent-type: application/json\\r\\n\\r\\n{body}")
        sys.exit(0)
sys.stdout.write('HTTP/2 404\\r\\n\\r\\n{"message": "Not Found"}')
"""

FAKE_GLAB = """#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
if args[:2] == ["auth", "status"]:
    print("Logged in as tester"); sys.exit(0)
joined = " ".join(args)
log, routes = os.environ["FAKE_API_LOG"], json.load(open(os.environ["FAKE_ROUTES"]))
with open(log, "a") as f:
    f.write(f"glab GET {joined}\\n")
for r in routes:
    if r["match"] in joined:
        body = r["body"] if isinstance(r["body"], str) else json.dumps(r["body"])
        print(body)
        sys.exit(0)
print("[]")
"""

FAKE_GIT = """#!/usr/bin/env bash
# ls-remote shim: keep preflight offline (refs mimic a normal remote);
# everything else delegates to real git.
if [ "$1" = "ls-remote" ]; then
  echo "ref: refs/heads/main	HEAD"
  echo "abc123\trefs/heads/main"
  echo "def456\trefs/heads/feature/x"
  exit 0
fi
exec {real_git} "$@"
"""


def _which_git():
    return subprocess.run(["sh", "-c", "command -v git"], capture_output=True,
                          text=True).stdout.strip() or "/usr/bin/git"


def fake_bin(tmp_path, routes):
    """Write fake curl/gh/glab + git ls-remote shim; returns (bin dir, call log)."""
    bin_dir = tmp_path / "fakebin"
    bin_dir.mkdir()
    for name, body in (("curl", FAKE_CURL), ("gh", FAKE_GH), ("glab", FAKE_GLAB),
                       ("git", FAKE_GIT.replace("{real_git}", _which_git()))):
        (bin_dir / name).write_text(body)
        (bin_dir / name).chmod(0o755)
    (tmp_path / "routes.json").write_text(json.dumps(routes))
    log = tmp_path / "api.log"
    log.write_text("")
    return bin_dir, log


def make_repo(tmp_path, remotes):
    """git init + remotes; returns repo dir."""
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args):
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

    git("init", "-q")
    git("-c", "user.email=t@example.com", "-c", "user.name=t",
        "commit", "--allow-empty", "-qm", "init")
    for name, url in remotes.items():
        git("remote", "add", name, url)
    return repo


def base_env(tmp_path, bin_dir, log):
    env = {k: v for k, v in os.environ.items() if k not in SCRUB}
    env.update({
        "PATH": f"{bin_dir}{os.pathsep}{env.get('PATH', '')}",
        "HOME": str(tmp_path / "home"),
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/bin/true",
        "FAKE_ROUTES": str(tmp_path / "routes.json"),
        "FAKE_API_LOG": str(log),
    })
    os.makedirs(env["HOME"], exist_ok=True)
    return env


def run_cli(repo, script, env, *args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        cwd=repo, capture_output=True, text=True, env=env,
        input=stdin, timeout=60,
    )


def log_lines(log):
    return (log.read_text()).splitlines()


FORK_REMOTES = {
    "origin": "git@github.com:fork-owner/app.git",
    "review": f"git@{FORKEE_HOST}:team/app.git",  # sorts after origin in `git remote`
}

PROBE_OK_ROUTE = {
    "match": "projects/team%2Fapp", "status": 200,
    "body": {"id": 7, "path_with_namespace": "team/app"},
}
GITLAB_DISCUSSIONS = [{
    "id": "abc123def",
    "notes": [{
        "id": 1, "body": "use fmt.Errorf instead of errors.New",
        "author": {"username": "ocr-bot"}, "system": False,
        "resolvable": True, "resolved": False,
        "position": {"new_path": "a.go", "new_line": 3, "old_path": "a.go"},
    }],
}]


def gitlab_env(tmp_path, extra_routes=(), mr="1", discussions=GITLAB_DISCUSSIONS):
    routes = [
        PROBE_OK_ROUTE,
        {"match": "merge_requests/1/discussions", "status": 200, "body": discussions},
        {"match": "merge_requests/1", "status": 200, "body": {
            "title": "Fix thing", "state": "opened",
            "web_url": f"https://{FORKEE_HOST}/team/app/-/merge_requests/{mr}",
        }},
        *extra_routes,
    ]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env.update({
        "OCR_REMOTE": "review",
        "CI_PROJECT_ID": "42",
        "GITLAB__PERSONAL_ACCESS_TOKEN": "test-token",
    })
    return env, log


# ── OCR_REMOTE override across the three scripts ────────────────────────


def test_ocr_remote_override_pull(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    env, log = gitlab_env(tmp_path)
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 0, r.stderr
    assert "Detected platform: gitlab" in r.stderr
    issues = json.loads(r.stdout)
    assert issues == [{
        "discussion_id": "abc123def", "file": "a.go", "line": 3,
        "body": "use fmt.Errorf instead of errors.New", "author": "ocr-bot",
    }]
    joined = "\n".join(log_lines(log))
    assert f"https://{FORKEE_HOST}/api/v4/projects/team%2Fapp" in joined  # probe
    assert "github.com" not in joined  # origin (upstream fork) never consulted


def test_ocr_remote_override_post(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    extra = [
        {"match": "discussions/abc123def/notes/1", "method": "PUT", "status": 200, "body": {}},
        {"match": "discussions/abc123def/notes", "method": "POST", "status": 201, "body": {"id": 9}},
        {"match": "discussions/abc123def", "method": "GET", "status": 200,
         "body": {"id": "abc123def", "notes": GITLAB_DISCUSSIONS[0]["notes"]}},
        {"match": "discussions/abc123def", "method": "PUT", "status": 200, "body": {}},
    ]
    env, log = gitlab_env(tmp_path, extra_routes=extra)
    item = json.dumps([{"discussion_id": "abc123def", "classification": "FP",
                        "reason": "not a real issue"}])
    r = run_cli(repo, "ocr-post-labels.py", env, "1", stdin=item)
    assert r.returncode == 0, r.stderr
    assert "Detected platform: gitlab" in r.stderr
    assert "[OK]" in r.stderr and "0 failed" in r.stderr
    assert f"https://{FORKEE_HOST}/api/v4/projects/team%2Fapp" in "\n".join(log_lines(log))


def test_ocr_remote_override_verify(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    resolved = [{**GITLAB_DISCUSSIONS[0], "notes":
                 [{**GITLAB_DISCUSSIONS[0]["notes"][0], "resolved": True}]}]
    env, _ = gitlab_env(tmp_path, discussions=resolved)
    r = run_cli(repo, "ocr-verify-resolved.py", env, "1")
    assert r.returncode == 0, r.stderr
    assert "Detected platform: gitlab" in r.stderr
    assert "All resolvable review threads resolved" in r.stderr


def test_ocr_remote_nonexistent_remote_loud_failure(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    env, _ = gitlab_env(tmp_path)
    env["OCR_REMOTE"] = "nope"
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 2, r.stderr
    assert "OCR_REMOTE" in r.stderr
    assert "nope" in r.stderr


# ── auth probe failure paths (exit 2 before first business API call) ─────


def test_probe_failure_pull_404(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    routes = [{"match": "projects/team%2Fapp", "status": 404,
               "body": {"message": "404 Project Not Found"}}]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env.update({"OCR_REMOTE": "review", "CI_PROJECT_ID": "42",
                "GITLAB__PERSONAL_ACCESS_TOKEN": "test-token"})
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 2, r.stderr
    assert "AUTH PROBE FAILED" in r.stderr
    assert "OCR_REMOTE" in r.stderr
    assert r.stdout == ""  # no findings JSON ever emitted
    assert "discussions" not in "\n".join(log_lines(log))  # no business call


def test_probe_failure_verify_path_mismatch(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    routes = [{"match": "projects/team%2Fapp", "status": 200,
               "body": {"id": 7, "path_with_namespace": "other/app"}}]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env.update({"OCR_REMOTE": "review", "CI_PROJECT_ID": "42",
                "GITLAB__PERSONAL_ACCESS_TOKEN": "test-token"})
    r = run_cli(repo, "ocr-verify-resolved.py", env, "1")
    assert r.returncode == 2, r.stderr
    assert "AUTH PROBE FAILED" in r.stderr and "OCR_REMOTE" in r.stderr
    assert "other/app" in r.stderr


def test_probe_failure_post_404(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    routes = [{"match": "projects/team%2Fapp", "status": 404,
               "body": {"message": "404 Project Not Found"}}]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env.update({"OCR_REMOTE": "review", "CI_PROJECT_ID": "42",
                "GITLAB__PERSONAL_ACCESS_TOKEN": "test-token"})
    item = json.dumps([{"discussion_id": "abc123def", "classification": "FP",
                        "reason": "x"}])
    r = run_cli(repo, "ocr-post-labels.py", env, "1", stdin=item)
    assert r.returncode == 2, r.stderr
    assert "OCR_REMOTE" in r.stderr


def test_github_probe_failure_404(tmp_path):
    repo = make_repo(tmp_path, {"origin": "git@github.com:owner/app.git"})
    routes = [{"match": "repos/owner/app", "status": 404, "body": {"message": "Not Found"}}]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env["GITHUB_TOKEN"] = "test-token"
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 2, r.stderr
    assert "AUTH PROBE FAILED" in r.stderr and "OCR_REMOTE" in r.stderr


# ── GITHUB_REPOSITORY env precedence: probe skipped, no error ────────────


def test_github_repository_env_skips_probe(tmp_path):
    repo = make_repo(tmp_path, {"origin": "git@github.com:owner/app.git"})
    routes = [
        {"match": "repos/other/repo/pulls/1/comments", "status": 200, "body": []},
        {"match": "repos/other/repo/pulls/1", "status": 200,
         "body": {"title": "T", "state": "open", "html_url": "https://github.com/other/repo/pull/1"}},
    ]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env.update({"GITHUB_REPOSITORY": "other/repo", "GITHUB_TOKEN": "test-token"})
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == []
    lines = log_lines(log)
    assert lines, "gh should have been called for business endpoints"
    assert all("/pulls/" in ln for ln in lines)  # no bare repo probe lookup
    assert "repos/owner/app" not in "\n".join(lines)  # local remote never consulted


# ── 0-findings stderr hint ────────────────────────────────────────────────


def test_zero_findings_stderr_hint(tmp_path):
    repo = make_repo(tmp_path, FORK_REMOTES)
    env, _ = gitlab_env(tmp_path, discussions=[])
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout) == []
    assert "0 findings" in r.stderr
    assert "platform=gitlab" in r.stderr
    assert FORKEE_HOST in r.stderr
    assert "OCR_REMOTE" in r.stderr


# ── happy-path regressions (default derivation unchanged) ────────────────


def test_github_happy_path_regression(tmp_path):
    repo = make_repo(tmp_path, {"origin": "git@github.com:owner/app.git"})
    routes = [
        {"match": "repos/owner/app/pulls/1/comments", "status": 200, "body": [{
            "id": 99, "path": "src/a.go", "line": 5,
            "body": "off-by-one in loop bound",
            "user": {"login": "human-1", "type": "User"},
            "in_reply_to_id": None,
        }]},
        {"match": "repos/owner/app/pulls/1", "status": 200,
         "body": {"title": "Fix thing", "state": "open",
                  "html_url": "https://github.com/owner/app/pull/1"}},
        {"match": "repos/owner/app", "status": 200,
         "body": {"id": 1, "full_name": "owner/app", "node_id": "PR_x"}},
    ]
    bin_dir, log = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, log)
    env["GITHUB_TOKEN"] = "test-token"
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 0, r.stderr
    issues = json.loads(r.stdout)
    assert issues == [{
        "discussion_id": "99", "file": "src/a.go", "line": 5,
        "body": "off-by-one in loop bound", "author": "human-1",
    }]
    assert "Detected platform: github" in r.stderr


def test_gitlab_default_origin_regression(tmp_path):
    repo = make_repo(tmp_path, {"origin": f"git@{FORKEE_HOST}:team/app.git"})
    env, log = gitlab_env(tmp_path)
    env.pop("OCR_REMOTE")  # default origin derivation
    r = run_cli(repo, "ocr-pull-discussions.py", env, "1")
    assert r.returncode == 0, r.stderr
    assert len(json.loads(r.stdout)) == 1
    assert "Detected platform: gitlab" in r.stderr


# ── create-mr preflight (bash side) ──────────────────────────────────────


def run_preflight(tmp_path, remotes, env_extra):
    repo = make_repo(tmp_path, remotes)
    routes = [{"match": "merge_requests?", "status": 200, "body": []}]
    bin_dir, _ = fake_bin(tmp_path, routes)
    env = base_env(tmp_path, bin_dir, tmp_path / "api.log")
    env.update(env_extra)
    preflight = SCRIPTS.parents[1] / "create-mr" / "scripts" / "preflight.sh"
    return subprocess.run(["bash", str(preflight)],
                          cwd=repo, capture_output=True, text=True, env=env, timeout=60)


def test_preflight_ocr_remote_override(tmp_path):
    r = run_preflight(tmp_path, FORK_REMOTES, {"OCR_REMOTE": "review"})
    assert r.returncode == 0, r.stderr
    assert "primary=review  platform=glab" in r.stdout
    assert "MULTI_REMOTE=true" in r.stdout  # ask contract still surfaces


def test_preflight_default_origin(tmp_path):
    r = run_preflight(tmp_path, FORK_REMOTES, {})
    assert r.returncode == 0, r.stderr
    assert "primary=origin  platform=gh" in r.stdout


def test_preflight_ocr_remote_nonexistent(tmp_path):
    r = run_preflight(tmp_path, FORK_REMOTES, {"OCR_REMOTE": "nope"})
    assert r.returncode == 2
    assert "OCR_REMOTE" in r.stderr
