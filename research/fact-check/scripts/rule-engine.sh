#!/bin/bash
# rule-engine.sh — Deterministic verifier for authority claims (DD-02, DD-12)
# Usage: bash rule-engine.sh <claims.json> [--repo <owner/repo>]
# Wrapper around python3 for HTTP verification of 20+ P0/P1 authority claim types.

set -euo pipefail

CLAIMS_FILE="${1:-}"
REPO=""

shift || true
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$CLAIMS_FILE" ] || [ ! -f "$CLAIMS_FILE" ]; then
  echo '{"error":"usage: rule-engine.sh <claims.json> [--repo owner/repo]"}' >&2
  exit 1
fi

exec python3 - "$CLAIMS_FILE" "$REPO" << 'PYEOF'
import hashlib, json, re, sys, urllib.request, urllib.error, ssl
from datetime import datetime, timezone

claims_file, repo = sys.argv[1], sys.argv[2]

# Ignore SSL errors for public API calls
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

def http_status(url):
    """Return HTTP status code, 0 on failure."""
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0

def verify_url(url):
    s = http_status(url)
    if s in (200, 301, 302, 303): return ("SUPPORTED", url, f"HTTP {s}")
    if s == 0: return ("UNVERIFIABLE", url, "connection failed")
    return ("CONTRADICTED", url, f"HTTP {s}")

def verify_arxiv(ident):       return verify_url(f"https://arxiv.org/abs/{ident}")
def verify_doi(ident):         return verify_url(f"https://doi.org/{ident}")
def verify_npm(ident):         return verify_url(f"https://registry.npmjs.org/{ident}")
def verify_pypi(ident):        return verify_url(f"https://pypi.org/project/{ident}/")
def verify_cargo(ident):       return verify_url(f"https://crates.io/api/v1/crates/{ident}")
def verify_go_module(ident):   return verify_url(f"https://pkg.go.dev/{ident}")
def verify_nuget(ident):       return verify_url(f"https://www.nuget.org/packages/{ident}/")
def verify_rfc(ident):         return verify_url(f"https://datatracker.ietf.org/doc/html/rfc{ident}")
def verify_pmid(ident):        return verify_url(f"https://pubmed.ncbi.nlm.nih.gov/{ident}/")
def verify_patent(ident):      return verify_url(f"https://patents.google.com/patent/{ident}/en")
def verify_spdx(ident):
    s = http_status(f"https://spdx.org/licenses/{ident}.json")
    return ("SUPPORTED", f"https://spdx.org/licenses/{ident}", "SPDX: valid") if s == 200 \
      else ("CONTRADICTED", f"https://spdx.org/licenses/{ident}", "SPDX: invalid")
def verify_ietf_draft(ident):  return verify_url(f"https://datatracker.ietf.org/doc/{ident}/")

def verify_docker(ident):
    ns, _, name = ident.partition("/")
    if not name: ns, name = "library", ns
    return verify_url(f"https://hub.docker.com/v2/repositories/{ns}/{name}/tags/")

# ---------------------------------------------------------------------------
# Extract identifier from claim_text per matched_rule (case-insensitive)
# ---------------------------------------------------------------------------
PATTERNS = {
    "arxiv_id":           r'arxiv:(\d+\.\d+(?:v\d+)?)',
    "doi":                r'(10\.\d{4,}/[^\s]+)',
    "github_pr_slash":    r'github\.com/[\w.-]+/[\w.-]+/pull/(\d+)',
    "github_pr_symbol":   r'(?:pr|pull request|拉取请求)\s*#?(\d+)',
    "code_platform_symbol_pr": r'[!#](\d+)',
    "github_issue":       r'(?:issue|问题|议题)\s*#?(\d+)',
    "github_repo":        r'github\.com/([\w.-]+/[\w.-]+)',
    "gitlab_repo":        r'gitlab\.com/([\w.-]+/[\w.-]+)',
    "gitlab_mr":          r'gitlab\.com/[\w.-]+/[\w.-]+/-/merge_requests/(\d+)',
    "gitlab_issue":       r'gitlab\.com/[\w.-]+/[\w.-]+/-/issues/(\d+)',
    "gitee_repo":         r'gitee\.com/([\w.-]+/[\w.-]+)',
    "url":                r'(https?://[^\s)]+)',
    "npm_package":        r'(?:install|i|安装|装)\s+(?:-g\s+)?[\'\"]?(@?[\w@./-]+)',
    "pypi_package":       r'(?:install|download|安装|装)\s+[\'\"]?([\w.-]+)',
    "cargo_crate":        r'(?:install|add|安装|添加|装)\s+[\'\"]?([\w-]+)',
    "go_module":          r'(?:go\s+get\s+(?:拉取|获取|安装)?\s*["\']?|pkg\.go\.dev/)([\w.-]+/[\w./-]+)',
    "nuget_package":      r'(?:install-package|dotnet\s+add\s+package|nuget\s*(?:安装|装))\s+[\'\"]?([\w.-]+)',
    "git_commit":         r'(?:commit|提交)\s+#?([0-9a-f]{7,40})',
    "rfc":                r'rfc\s*#?(\d+)',
    "pmid":               r'pmid:\s*(\d+)',
    "patent":             r'\b((?:us|cn|wo|ep|jp|kr)\d{6,12}(?:b\d|a\d)?)',
    "ietf_draft":         r'(draft-(?:ietf-)?[\w-]+-\d{2})',
    "docker_image":       r'(?:pull|run|拉取|运行|启动)\s+(?:--[\w.=-]+\s+)*[\'\"]?([\w.-]+(?:/[\w.-]+)?)',
    "spdx_license":       r'(?:licensed\s+under|license[d]?\s+under|released\s+under|许可证)\s*[为：:|]?\s*[\'\"]?([a-za-z0-9.\-+]+)',
    "git_tag":            r'(v?\d[\w.]{1,30})',
}

VERIFIERS = {
    "arxiv_id": verify_arxiv, "doi": verify_doi,
    "github_pr_slash": lambda x: ("UNVERIFIABLE", "", "requires gh CLI"),
    "github_pr_symbol": lambda x: ("UNVERIFIABLE", "", "requires gh CLI"),
    "code_platform_symbol_pr": lambda x: ("UNVERIFIABLE", "", "requires gh CLI"),
    "github_issue": lambda x: ("UNVERIFIABLE", "", "requires gh CLI"),
    "github_repo": lambda x: verify_url(f"https://github.com/{x}"),
    "gitlab_repo": lambda x: verify_url(f"https://gitlab.com/{x}"),
    "gitlab_mr": verify_url, "gitlab_issue": verify_url,
    "gitee_repo": lambda x: verify_url(f"https://gitee.com/{x}" if not x.startswith("http") else x),
    "url": verify_url,
    "npm_package": verify_npm, "pypi_package": verify_pypi,
    "cargo_crate": verify_cargo, "go_module": verify_go_module,
    "nuget_package": verify_nuget, "rfc": verify_rfc,
    "pmid": verify_pmid, "patent": verify_patent,
    "ietf_draft": verify_ietf_draft, "docker_image": verify_docker,
    "spdx_license": verify_spdx,
    "git_commit": lambda x: ("UNVERIFIABLE", "", "requires gh CLI + repo context"),
    "git_tag": lambda x: ("UNVERIFIABLE", "", "requires git + repo context"),
}

# ---------------------------------------------------------------------------
with open(claims_file) as f:
    claims = json.load(f)

results = []
for claim in claims:
    route = claim.get("route", "")
    matched_verifier = str(claim.get("matched_verifier", ""))
    if route != "rule_engine" and "rule_engine" not in matched_verifier:
        if claim.get("expected_verifier") != "rule_engine":
            continue

    cid = claim.get("claim_id", "?")
    text = claim.get("claim_text", "")
    rule = claim.get("matched_rule", "")

    # Extract identifier
    ident = ""
    pat = PATTERNS.get(rule)
    if pat:
        m = re.search(pat, text, re.IGNORECASE)
        ident = m.group(1) if (m and m.lastindex) else (m.group(0) if m else "")
    if not ident:
        m = re.search(r'(https?://[^\s)]+)', text)
        ident = m.group(1) if m else ""

    verdict, evidence_url, evidence = "UNVERIFIABLE", "", "no identifier extracted"
    if ident and rule in VERIFIERS:
        try:
            verdict, evidence_url, evidence = VERIFIERS[rule](ident)
        except Exception as e:
            verdict, evidence = "UNVERIFIABLE", str(e)

    claim["verdict"] = verdict
    claim["evidence"] = evidence
    claim["evidence_url"] = evidence_url
    claim["checked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    results.append({"claim_id": cid, "verdict": verdict, "evidence": evidence, "evidence_url": evidence_url})

with open(claims_file, "w") as f:
    json.dump(claims, f, ensure_ascii=False, indent=2)

print(json.dumps({"verified": len(results), "results": results}, ensure_ascii=False))
PYEOF
