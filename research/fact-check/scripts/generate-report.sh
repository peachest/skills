#!/bin/bash
# generate-report.sh — Phase 6 report generation (DD-16, DD-17, run-output.md)
# Usage: bash generate-report.sh <claims.json> <run.json> <run-dir>
# Writes: report.md, handoff.md, updates ledger.jsonl, total-stats.json, run.json

set -euo pipefail

CLAIMS_FILE="${1:-}"
RUN_FILE="${2:-}"
RUN_DIR="${3:-}"

if [ -z "$CLAIMS_FILE" ] || [ -z "$RUN_FILE" ] || [ -z "$RUN_DIR" ]; then
  echo '{"error":"usage: generate-report.sh <claims.json> <run.json> <run-dir>"}' >&2
  exit 1
fi

exec python3 - "$CLAIMS_FILE" "$RUN_FILE" "$RUN_DIR" << 'PYEOF'
import hashlib, json, os, sys
from datetime import datetime, timezone

claims_file, run_file, run_dir = sys.argv[1], sys.argv[2], sys.argv[3]

with open(claims_file) as f:
    claims = json.load(f)

with open(run_file) as f:
    run_meta = json.load(f)

# ---------------------------------------------------------------------------
# Verdict icons and ordering
# ---------------------------------------------------------------------------
ICONS = {
    "CONTRADICTED": "🔴", "NUANCED": "🟡", "OUTDATED": "🕐",
    "UNVERIFIABLE": "⚪", "SUPPORTED": "🟢", "REFUSED": "⛔", "INFERRED": "💡",
}
ORDER = ["CONTRADICTED", "NUANCED", "OUTDATED", "UNVERIFIABLE", "SUPPORTED", "REFUSED", "INFERRED"]

# ---------------------------------------------------------------------------
# Computations
# ---------------------------------------------------------------------------
verdict_counts = {}
for c in claims:
    v = c.get("verdict", "UNKNOWN")
    verdict_counts[v] = verdict_counts.get(v, 0) + 1

now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
doc_name = run_meta.get("document_key", "document")
run_id = os.path.basename(run_dir)
document_path = run_meta.get("documents", [doc_name])[0]

def generate_vid(claim_text):
    return hashlib.sha256(claim_text.strip().lower().encode()).hexdigest()[:12]

# ---------------------------------------------------------------------------
# report.md
# ---------------------------------------------------------------------------
report_lines = []
report_lines.append(f"# Fact-Check Report: {document_path}")
report_lines.append(f"**Run:** {run_id} | **Checked:** {now_utc[:10]}")
report_lines.append("")
report_lines.append("## Summary")
report_lines.append("| | Count |")
report_lines.append("|---|-------|")
for v in ORDER:
    c = verdict_counts.get(v, 0)
    report_lines.append(f"| {ICONS.get(v, '  ')} {v} | {c} |")
report_lines.append("")

# Items to fix / attention
fixable = [c for c in claims if c.get("verdict") in ("CONTRADICTED",)]
needs_attention = [c for c in claims if c.get("verdict") in ("NUANCED", "OUTDATED", "UNVERIFIABLE")]
carried = [c for c in claims if c.get("verdict") in ("SUPPORTED", "REFUSED", "INFERRED")]

report_lines.append(f"## Items to Fix ({len(fixable)})")
report_lines.append(f"## Items Needing Attention ({len(needs_attention)})")
report_lines.append(f"## Carried Forward ({len(carried)})")
report_lines.append("")
report_lines.append("---")

# Claim detail cards, grouped by verdict
for verdict_type in ORDER:
    group = [c for c in claims if c.get("verdict") == verdict_type]
    if not group:
        continue
    for c in group:
        cid = c.get("claim_id", "?")
        ct = c.get("claim_text", "")
        loc = c.get("source_location", "")
        v = c.get("verdict", "?")
        sev = c.get("severity", "medium")
        conf = c.get("confidence", "medium")
        tier = c.get("evidence_tier", "?")
        url = c.get("evidence_url", "")
        evidence = c.get("evidence", "")
        vid = generate_vid(ct)

        icon = ICONS.get(v, "")
        report_lines.append(f"### {cid} — {v} {icon} severity:{sev} confidence:{conf}")
        report_lines.append(f"- **Claim:** \"{ct}\"")
        report_lines.append(f"- **Location:** `{loc}`")
        if url:
            report_lines.append(f"- **Evidence Tier:** {tier} — {url}")
        if evidence:
            report_lines.append(f"- **Finding:** {evidence}")
        report_lines.append(f"- **Verdict ID:** `sha256:{vid}`")
        report_lines.append("")

report_path = os.path.join(run_dir, "report.md")
with open(report_path, "w") as f:
    f.write("\n".join(report_lines))

# ---------------------------------------------------------------------------
# handoff.md
# ---------------------------------------------------------------------------
handoff = [c for c in claims if c.get("verdict") in ("CONTRADICTED", "NUANCED")]
handoff_lines = []
handoff_lines.append(f"# Handoff: Items to Review — {document_path}")
handoff_lines.append(f"**Run:** {run_id} | **Generated:** {now_utc[:10]}")
handoff_lines.append("")
handoff_lines.append("> Mark items as `verdict wrong, counter evidence: <url>` to trigger re-evaluation.")
handoff_lines.append("")

for c in handoff:
    cid = c.get("claim_id", "?")
    ct = c.get("claim_text", "")
    v = c.get("verdict", "?")
    url = c.get("evidence_url", "")
    evidence = c.get("evidence", "")
    icon = ICONS.get(v, "")
    handoff_lines.append(f"<!-- handoff-claim {cid} -->")
    handoff_lines.append(f"### {cid} — {v} {icon}")
    handoff_lines.append(f"- **Claim:** \"{ct}\"")
    handoff_lines.append(f"- **Evidence:** {evidence}")
    if url:
        handoff_lines.append(f"- **Source:** {url}")
    handoff_lines.append(f"- **Verdict ID:** `sha256:{generate_vid(ct)}`")
    handoff_lines.append("")

handoff_path = os.path.join(run_dir, "handoff.md")
with open(handoff_path, "w") as f:
    f.write("\n".join(handoff_lines))

# ---------------------------------------------------------------------------
# ledger.jsonl append
# ---------------------------------------------------------------------------
doc_key = run_meta.get("document_key", "document")
# ledger lives beside claims.json in documents/<key>/
ledger_dir = os.path.dirname(claims_file)
ledger_path = os.path.join(ledger_dir, "ledger.jsonl")

# total-stats.json lives at fact-check/total-stats.json (2 levels up from documents/<key>)
fact_check_dir = os.path.dirname(os.path.dirname(ledger_dir))
stats_path = os.path.join(fact_check_dir, "total-stats.json")
run_seq = 1
if os.path.exists(stats_path):
    try:
        with open(stats_path) as f:
            stats = json.load(f)
        run_seq = stats.get("total_runs", 0) + 1
    except:
        pass

timestamp = now_utc
ledger_entries = []
for c in claims:
    vid = generate_vid(c.get("claim_text", ""))
    entry = {
        "vid": vid,
        "claim_text": c.get("claim_text", ""),
        "verdict": c.get("verdict", ""),
        "evidence_tier": c.get("evidence_tier", ""),
        "evidence_url": c.get("evidence_url", ""),
        "run_seq": run_seq,
        "timestamp": timestamp,
        "run": run_id,
    }
    ledger_entries.append(json.dumps(entry, ensure_ascii=False))

os.makedirs(os.path.dirname(ledger_path), exist_ok=True)
with open(ledger_path, "a") as f:
    for entry in ledger_entries:
        f.write(entry + "\n")

# ---------------------------------------------------------------------------
# total-stats.json update
# ---------------------------------------------------------------------------
if os.path.exists(stats_path):
    with open(stats_path) as f:
        stats = json.load(f)
else:
    stats = {
        "total_runs": 0,
        "total_claims_verified": 0,
        "verdict_distribution": {},
        "outstanding_fixes": 0,
        "unresolved_claims": 0,
    }

stats["total_runs"] = run_seq
stats["total_claims_verified"] = stats.get("total_claims_verified", 0) + len(claims)
for v, c in verdict_counts.items():
    stats["verdict_distribution"][v] = stats["verdict_distribution"].get(v, 0) + c
stats["outstanding_fixes"] = len(fixable)
stats["unresolved_claims"] = len([c for c in claims if c.get("verdict") == "UNVERIFIABLE"])
stats["latest_run"] = run_id

os.makedirs(os.path.dirname(stats_path), exist_ok=True)
with open(stats_path, "w") as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# run.json update
# ---------------------------------------------------------------------------
run_meta["completed_at"] = now_utc
run_meta["total_claims"] = len(claims)
run_meta["verdict_distribution"] = verdict_counts

with open(run_file, "w") as f:
    json.dump(run_meta, f, ensure_ascii=False, indent=2)

# ---------------------------------------------------------------------------
# profile-summary.json (T10) — aggregate profile.jsonl if it exists
# ---------------------------------------------------------------------------
profile_path = os.path.join(run_dir, "profile.jsonl")
summary_path = os.path.join(run_dir, "profile-summary.json")
if os.path.exists(profile_path):
    summary = {"total_duration_ms": 0, "phases": {}, "llm_calls": {"total": 0, "total_duration_ms": 0,
        "total_input_tokens": 0, "total_output_tokens": 0}, "scripts": {"total": 0, "total_duration_ms": 0},
        "network_requests": {"total": 0, "total_duration_ms": 0}, "retries": {"total": 0}}
    with open(profile_path) as pf:
        for line in pf:
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except:
                continue
            ev = e.get("event", "")
            dur = e.get("duration_ms", 0)
            if ev == "phase_start":
                summary["phases"][e.get("phase", "?")] = {"start_ms": e.get("timestamp_ms", 0)}
            elif ev == "phase_end":
                ph = e.get("phase", "?")
                summary["phases"].setdefault(ph, {})["duration_ms"] = dur
                summary["total_duration_ms"] += dur
            elif ev == "llm_call":
                summary["llm_calls"]["total"] += 1
                summary["llm_calls"]["total_duration_ms"] += dur
                summary["llm_calls"]["total_input_tokens"] += e.get("input_tokens", 0)
                summary["llm_calls"]["total_output_tokens"] += e.get("output_tokens", 0)
            elif ev == "script":
                summary["scripts"]["total"] += 1
                summary["scripts"]["total_duration_ms"] += dur
            elif ev == "network":
                summary["network_requests"]["total"] += 1
                summary["network_requests"]["total_duration_ms"] += dur
            elif ev == "retry":
                summary["retries"]["total"] += 1
    with open(summary_path, "w") as sf:
        json.dump(summary, sf, ensure_ascii=False, indent=2)

print(json.dumps({
    "report": report_path,
    "handoff": handoff_path,
    "ledger": ledger_path,
    "total_stats": stats_path,
    "total_claims": len(claims),
    "verdict_distribution": verdict_counts,
}, ensure_ascii=False))
PYEOF
