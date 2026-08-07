"""Tests for markdown report formatting (B-style card + summary).

DD-16: Report format with verdict icons, severity, confidence, evidence tier.

Reference: fact-checker's test_report.py.
"""

from __future__ import annotations


VERDICT_ICONS = {
    "CONTRADICTED": "🔴",
    "NUANCED": "🟡",
    "OUTDATED": "🕐",
    "UNVERIFIABLE": "⚪",
    "SUPPORTED": "🟢",
    "REFUSED": "⛔",
    "INFERRED": "💡",
}


def make_summary_table(claims: list[dict]) -> str:
    """Generate a markdown summary table from verdict distribution."""
    counts = {}
    for c in claims:
        v = c.get("verdict", "UNKNOWN")
        counts[v] = counts.get(v, 0) + 1

    lines = ["## Summary", "", "| | Count |", "|---|-------|"]
    for verdict, icon in VERDICT_ICONS.items():
        if verdict in counts:
            lines.append(f"| {icon} {verdict} | {counts[verdict]} |")
    lines.append("")
    return "\n".join(lines)


def format_claim_card(claim: dict, index: int) -> str:
    """Format a single claim as a B-style card."""
    verdict = claim.get("verdict", "UNKNOWN")
    icon = VERDICT_ICONS.get(verdict, "❓")
    severity = claim.get("severity", "low")
    confidence = claim.get("confidence", "low")
    tier = claim.get("evidence_tier", "T3")
    location = claim.get("source_location", "unknown")
    vid = claim.get("vid", "?")

    lines = [
        f"### {claim['claim_id']} — {verdict} {icon} severity:{severity} confidence:{confidence}",
        f"- **Claim:** {claim['claim_text']}",
        f"- **Location:** `{location}`",
    ]
    if "evidence_url" in claim:
        lines.append(f"- **Evidence Tier:** {tier} — {claim['evidence_url']}")
    if "finding" in claim:
        lines.append(f"- **Finding:** {claim['finding']}")
    if "suggested_fix" in claim:
        lines.append(f"- **Suggested Fix:** {claim['suggested_fix']}")
    lines.append(f"- **Verdict ID:** `{vid}`")
    lines.append("")
    return "\n".join(lines)


def generate_report_header(doc_name: str, run_id: str, date: str) -> str:
    return (
        f"# Fact-Check Report: {doc_name}\n"
        f"**Run:** {run_id} | **Checked:** {date}\n\n"
    )


class TestSummaryTable:
    def test_empty_claims(self):
        table = make_summary_table([])
        assert "## Summary" in table
        assert "| 🔴 CONTRADICTED" not in table

    def test_mixed_verdicts(self):
        claims = [
            {"verdict": "CONTRADICTED"},
            {"verdict": "SUPPORTED"},
            {"verdict": "SUPPORTED"},
            {"verdict": "NUANCED"},
        ]
        table = make_summary_table(claims)
        assert "| 🔴 CONTRADICTED | 1 |" in table
        assert "| 🟢 SUPPORTED | 2 |" in table
        assert "| 🟡 NUANCED | 1 |" in table

    def test_only_shows_present_verdicts(self):
        claims = [{"verdict": "SUPPORTED"}, {"verdict": "SUPPORTED"}]
        table = make_summary_table(claims)
        assert "CONTRADICTED" not in table
        assert "SUPPORTED" in table


class TestClaimCard:
    def test_basic_card(self):
        claim = {
            "claim_id": "C001",
            "claim_text": "arXiv:2605.18071 proposed the method",
            "verdict": "SUPPORTED",
            "severity": "high",
            "confidence": "high",
            "evidence_tier": "T1",
            "source_location": "doc.md:42",
            "vid": "abc123456789",
            "evidence_url": "https://arxiv.org/abs/2605.18071",
            "finding": "arXiv page returns 200",
        }
        card = format_claim_card(claim, 0)
        assert "### C001 — SUPPORTED 🟢" in card
        assert "severity:high confidence:high" in card
        assert "Evidence Tier:" in card
        assert "Verdict ID" in card and "abc123456789" in card

    def test_card_without_evidence_url(self):
        claim = {
            "claim_id": "C002",
            "claim_text": "vLLM is better",
            "verdict": "REFUSED",
            "source_location": "doc.md:46",
            "vid": "def456789abc",
        }
        card = format_claim_card(claim, 1)
        assert "REFUSED ⛔" in card
        assert "Evidence Tier" not in card


class TestReportHeader:
    def test_header_format(self):
        header = generate_report_header("冷启动报告", "run-20260709-120000-main", "2026-07-09")
        assert "# Fact-Check Report: 冷启动报告" in header
        assert "**Run:** run-20260709-120000-main" in header
        assert "**Checked:** 2026-07-09" in header
