"""Post classification verdicts to review threads + resolve them.

Reads a schema 2 classified state file (--classified <path>, or stdin as a
bare transport — validation is identical for both) and for each entry:
  1. Joins it against the pull state file (see below) — hard-fails the whole
     run before any platform call on a mismatch
  2. Posts a reply note with classification label + reason/fix-plan — unless
     the thread already carries this entry's anchor marker + verdict revision
     fingerprint (content dedup, which also covers manual-curl bypass where
     the posted flag is absent); a body-anchor match with a different
     revision is a REVISED verdict (verdict.py --force) → re-post, the
     superseded reply stays as history
  3. Resolves the thread iff the entry's per-item `resolved` field says so —
     post executes the verdict-time decision, it never re-judges

Join + anchor validation (hard-fail BEFORE any platform call):
  - every entry's discussion_id must byte-match an id in the pull state
    file (.triage/<MR>/issues.json, or --pull-file <path>); a mismatch
    exits naming the offending entry's no and the closest real id —
    truncated or forged ids never reach the platform
  - the entry anchor must equal sha256(pull body)[:16] recomputed from the
    SAME pull file; a reviewer editing the live comment mid-run does not
    false-reject, because verdict and post read the same stale snapshot
    (spec #57 Q4)

Resolve semantics (spec #57 Amendment R2 修订 A): the per-item `resolved`
field is authoritative — verdict.py writes it on every entry (Edge defaults
resolved:true, Q defaults open and closes only on an explicit --resolved
true; the close-after-verification judgment happens at verdict time). Entries
without the field (legacy dual-mode) fall back to the mode maps below.
A thread is never resolved when its reply failed — the verdict reason must be
on the wall before a thread closes (--force overrides at the operator's risk);
a reply-failed item counts as fail and exits non-zero.

After the classified entries, post sweeps the remaining resolvable OCR
summary threads itself (spec #57 Q6 AMEND, #62 — the last routine manual-API
path dies). Three template classes off the thread's root-note body:
  🔍 start — confirmation note ("本轮 triage 已启动…"), no statistics;
    resolves only when a ✅ end/LGTM thread exists and completed this run
    (replied/deduped + resolved) AND the classified phase had zero failed
    items — otherwise left open for the closure gate;
  ✅ end/LGTM — statistics template (TP/FP/Edge/OOS/Q counts from the
    classified entries + the TP fix files joined from the pull file),
    then resolve;
  ⚠️ error — fixed escalation note, reply ONLY, never resolved, and its
    presence fails the run (exit non-zero). The closure gate staying red on
    an error round is INTENTIONAL human-in-loop design.
Every sweep reply embeds the anchor marker of the summary thread itself, so
a re-run on an already-swept MR posts nothing (content dedup, #61 ③).

GitHub sweep note (#62 dual-ID-space fix): the REST reply target (comment
databaseId) and the GraphQL resolve target (thread node id) both come from
ONE reviewThreads listing inside this script — no node id ever enters a
REST path, and ocr-verify-resolved.py --json ids (thread node ids) are
never consumed.

Platform is auto-detected from git remote:
  - github.com    → GitHub PR review comment replies + GraphQL resolve
  - anything else → GitLab discussion replies + PUT resolve

Classifications (mode maps apply only to legacy entries without a per-item
resolved field):
    ✅ TP  — label "真阳性" + fix plan
    ❌ FP  — label "假阳性" + reason
    🟡 Edge — label "边缘" + reason
    🔵 OOS  — label "非本 MR 范围" + reason
    ⏸️ Q    — label "需讨论" + question

Classification vocabulary is pinned: state files store the Question verdict
as `Q`; both `Q` and `Question` are accepted and normalized to `Question`
(the canonical key in the label/resolved maps) before any lookup. Unknown or
missing classification values hard-fail the whole run before any platform
call — no silent FP downgrade.

In triage mode (--mode triage), a TP has already been fixed and build-verified
by the time it reaches post-labels, so the triage map resolves it like FP/OOS;
the default map (standalone /fix) leaves it open for tracking. Whether Edge
or Q closes is decided at verdict time via the per-item resolved field —
post only executes it.

Input format (schema 2 — versionless or schema-1 files are rejected loudly
with the filename, the missing-field list, and a rebuild hint):
    {
      "schema": 2,
      "entries": [
        {
          "discussion_id": "...",         # byte-exact copy from the pull file
          "no": 3,                        # finding ordinal in the pull file
          "anchor": "<sha256(body)[:16]>",  # recompute-verified at post time
          "classification": "TP|FP|Edge|OOS|Q",
          "reason": "...",
          "fix_plan": "...",              # TP only
          "priority": "high|medium|low",  # TP only, string enum
          "resolved": true/false,         # verdict-time decision; post executes it
          "posted": false                 # delivery status; this script is the
        },                                # declared exception writer — flips it
        ...                               # to true on a successful reply
      ]
    }

The posted:true flags are written back to the --classified file (atomic
tmp+replace, verdict.py's pattern); the stdin transport has no file to
write back — content dedup is the idempotency net there.

Usage:
    python3 ocr-post-labels.py <MR_OR_PR_ID> [--mode triage] [--classified <path>]
                               [--pull-file <path>] [--force]  [< state.json]

    --pull-file <path>  pull state file to join against (default:
                        .triage/<MR>/issues.json)
    --force             resolve even when the reply failed
"""

import difflib
import hashlib
import json
import os
import re
import sys

from ocr_platform import detect_platform, load_pull_findings, run_auth_probe, triage_state_dir

# ── Templates (platform-agnostic) ──

_SCHEMA_VERSION = 2

# State files store the Question verdict as `Q`; the maps below are keyed by
# the canonical `Question`, so normalize aliases BEFORE any lookup.
_CLASSIFICATION_ALIASES = {"Q": "Question"}

_CLASSIFICATION_LABELS = {
    "TP": "✅ 真阳性",
    "FP": "❌ 假阳性",
    "Edge": "🟡 边缘",
    "OOS": "🔵 非本 MR 范围",
    "Question": "⏸️ 需讨论",
}

_PRIORITY_LABELS = {
    "high": "🚨 高",
    "medium": "⚠️ 中",
    "low": "🟢 低",
}

_BODY_TP = """### {label} {priority}

**修复方案**: {fix_plan}
"""

_BODY_SIMPLE = """### {label}

**原因**: {reason}
"""

_BODY_FP = """### ❌ 假阳性

**原因**: {reason}
{adr_row}"""

_BODY_QUESTION = """### ⏸️ 需讨论

{reason}
"""

# Per-classification resolved fallback — used ONLY by legacy entries without
# a per-item `resolved` field (verdict.py always writes the field).
# `triage` mode (used by /skill:triage-mr): TP is fixed+verified in-run, so it
# resolves. `default` mode (standalone /fix): TP stays open for tracking.
_DEFAULT_RESOLVED = {
    "TP": False,
    "FP": True,
    "Edge": False,
    "OOS": True,
    "Question": False,
}

_TRIAGE_RESOLVED = {
    "TP": True,
    "FP": True,
    "Edge": False,
    "OOS": True,
    "Question": False,
}

_VALID_CLASSIFICATIONS = set(_CLASSIFICATION_LABELS.keys())

# Machine marker embedded in every reply body (invisible HTML comment on both
# platforms). Content dedup (#61 ③) searches threads for it — this is what
# makes a manual-curl bypass (no posted flag) idempotent. Classified replies
# append a verdict revision fingerprint (`rev:`, H2): sha256 over the verdict
# content, so a revised verdict re-posts while the body anchor holds. Sweep
# replies carry the plain anchor form (no verdict content to fingerprint).
_ANCHOR_MARKER = "triage-anchor: {anchor}"


# ── Input parsing (platform-agnostic) ──


def _extract_json(raw):
    text = re.sub(r"```(?:json)?\s*", "", raw)
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return None


def _parse_state_entries(raw, filename):
    """Parse a schema 2 state payload; hard-fail on versionless/schema-1 input.

    Both transports (--classified <path> and stdin) go through this same
    validation. The error carries the filename, the missing/invalid field
    list, and a one-line rebuild hint, then exits non-zero before any
    platform call.
    """
    data = _extract_json(raw)
    if data is None:
        print(f"ERROR: {filename}: no valid JSON found in state input", file=sys.stderr)
        sys.exit(1)

    if isinstance(data, dict):
        problems = []
        if "schema" not in data:
            problems.append("schema")
        elif data["schema"] != _SCHEMA_VERSION:
            problems.append(f"schema={data['schema']!r} (expected {_SCHEMA_VERSION})")
        if not isinstance(data.get("entries"), list):
            problems.append("entries")
        got = ""
    else:
        problems = ["schema", "entries"]
        got = f" (got bare {type(data).__name__})"

    if problems:
        print(
            f"ERROR: {filename}: schema {_SCHEMA_VERSION} state file required — "
            f"missing/invalid field(s): {', '.join(problems)}{got}. "
            f"Rebuild: re-emit as {{\"schema\": {_SCHEMA_VERSION}, \"entries\": [...]}} — older formats are no longer accepted",
            file=sys.stderr,
        )
        sys.exit(1)
    return data["entries"]


def _preflight(entries, filename):
    """Pin the classification vocabulary before any platform call.

    Normalizes `Q` → `Question` (canonical key of the label/resolved maps —
    a legal Q must not KeyError in _build_body), and hard-fails the whole run
    on unknown or missing classification values (no silent FP downgrade) and
    on TP priorities outside the high|medium|low string enum.
    """
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            print(f"ERROR: {filename}: entry {i}: not a JSON object", file=sys.stderr)
            sys.exit(1)
        raw_cls = entry.get("classification")
        cls = _CLASSIFICATION_ALIASES.get(raw_cls, raw_cls)
        if cls not in _VALID_CLASSIFICATIONS:
            kind = "missing classification" if raw_cls is None else f"unknown classification {raw_cls!r}"
            print(
                f"ERROR: {filename}: entry {i}: {kind} (valid: TP|FP|Edge|OOS|Q/Question) — no platform calls made",
                file=sys.stderr,
            )
            sys.exit(1)
        entry["classification"] = cls
        if cls == "TP":
            # ocr r1 F3: omitted priority defaults to medium in _validate_item;
            # a *supplied* priority must be a valid enum string — explicit null
            # and non-string values (incl. collections, which raise TypeError
            # at an `in` check) hard-fail here, before any platform call.
            if "priority" in entry:
                priority = entry["priority"]
                if not isinstance(priority, str) or priority not in _PRIORITY_LABELS:
                    print(
                        f"ERROR: {filename}: entry {i}: priority must be one of high|medium|low, got {priority!r}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
    return entries


def _validate_item(item, idx, resolved_map=None):
    resolved_map = resolved_map or _DEFAULT_RESOLVED
    cleaned = dict(item)

    if "classification" not in cleaned and "_cat" in cleaned:
        cleaned["classification"] = cleaned["_cat"]
    if "reason" not in cleaned and "_reason" in cleaned:
        cleaned["reason"] = cleaned["_reason"]
    if "priority" not in cleaned and "_priority" in cleaned:
        pri_map = {"🚨": "high", "⚠️": "medium", "🟢": "low"}
        cleaned["priority"] = pri_map.get(cleaned["_priority"], "medium")

    disc_id = str(cleaned.get("discussion_id", "")).strip()
    if not disc_id:
        return (False, f"item {idx}: missing discussion_id", None)
    if len(disc_id) < 5:
        return (False, f"item {idx}: discussion_id too short ({len(disc_id)} chars)", None)
    cleaned["discussion_id"] = disc_id

    cls = cleaned.get("classification", "FP")
    if cls not in _VALID_CLASSIFICATIONS:
        print(f"  [WARN] item {idx}: unknown classification '{cls}', using 'FP'", file=sys.stderr)
        cls = "FP"
    cleaned["classification"] = cls

    if cls == "TP":
        fix_plan = str(cleaned.get("fix_plan", "")).strip()
        if not fix_plan:
            return (False, f"item {idx}: TP requires fix_plan", None)
        cleaned["fix_plan"] = fix_plan
        priority = cleaned.get("priority", "medium")
        cleaned["priority"] = priority
    elif cls == "FP":
        reason = str(cleaned.get("reason", "")).strip()
        if not reason:
            return (False, f"item {idx}: missing reason", None)
        cleaned["reason"] = reason
        adr = str(cleaned.get("adr", "")).strip()
        cleaned["adr"] = adr
    else:
        reason = str(cleaned.get("reason", "")).strip()
        if not reason:
            return (False, f"item {idx}: missing reason", None)
        cleaned["reason"] = reason

    resolved = cleaned.get("resolved")
    if resolved is None:
        resolved = resolved_map.get(cls, False)
    if not isinstance(resolved, bool):
        resolved = resolved_map.get(cls, False)
    cleaned["resolved"] = resolved

    return (True, "", cleaned)


def _verdict_rev(cleaned):
    """Verdict revision fingerprint (ocr-r2 H2): sha256 over the verdict
    content — classification|reason|fix_plan — so a `verdict.py --force`
    revision (Q→FP, new reason) changes the marker while the body anchor
    holds. Computed here in post, never in verdict.py: the producer has no
    business knowing the marker's dedup role."""
    payload = "|".join([
        cleaned.get("classification", ""),
        cleaned.get("reason", ""),
        cleaned.get("fix_plan", ""),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _build_body(cleaned):
    cls = cleaned["classification"]

    if cls == "TP":
        pri = _PRIORITY_LABELS.get(cleaned["priority"], "⚠️ 中")
        text = _BODY_TP.format(
            label=_CLASSIFICATION_LABELS[cls],
            priority=pri,
            fix_plan=cleaned["fix_plan"],
        ).strip()
    elif cls == "FP":
        adr_row = ""
        if cleaned.get("adr"):
            adr_row = f"\n**ADR**: {cleaned['adr']}"
        text = _BODY_FP.format(
            reason=cleaned["reason"],
            adr_row=adr_row,
        ).strip()
    elif cls == "Question":
        text = _BODY_QUESTION.format(reason=cleaned["reason"]).strip()
    else:
        text = _BODY_SIMPLE.format(
            label=_CLASSIFICATION_LABELS[cls],
            reason=cleaned["reason"],
        ).strip()

    anchor = cleaned.get("anchor")
    if anchor:
        text += (f"\n\n<!-- {_ANCHOR_MARKER.format(anchor=anchor)} "
                 f"rev:{_verdict_rev(cleaned)} -->")
    return text


# ── Pull-file join + anchor validation (platform-agnostic, pre-call) ──


def _closest_id(bad_id, ids):
    """The real id closest to a rejected one, for the error message.
    Prefix relation first — the canonical failure is a truncated id (the
    8-char id quirk that motivated the byte-match gate) — then fuzzy match."""
    if bad_id:
        for real in ids:
            if real.startswith(bad_id) or bad_id.startswith(real):
                return real
    match = difflib.get_close_matches(bad_id or "", ids, n=1, cutoff=0.5)
    return match[0] if match else None


def _validate_against_pull(entries, pull_path):
    """Join every entry against the pull state file before any platform call
    (spec #57 Q4, #61 ①②). A discussion_id that is not byte-present in the
    pull file, or an anchor that the pull body does not reproduce, exits 1
    naming the entry's no and (for ids) the closest real id. The offending id
    itself is never echoed — its shape must not seed a hand-typed retry."""
    findings = load_pull_findings(pull_path)
    by_id = {}
    for f in findings:
        if isinstance(f, dict) and isinstance(f.get("discussion_id"), str):
            by_id[f["discussion_id"]] = f
    ids = list(by_id)
    for i, entry in enumerate(entries):
        label = f"entry no={entry['no']}" if isinstance(entry.get("no"), int) else f"entry {i}"
        disc_id = entry.get("discussion_id")
        if not isinstance(disc_id, str) or disc_id not in by_id:
            closest = _closest_id(disc_id if isinstance(disc_id, str) else "", ids)
            hint = f"closest real id: {closest}" if closest else "no similar id in pull file"
            print(f"ERROR: {label}: discussion_id not byte-present in {pull_path} "
                  f"({hint}) — ids are copied byte-exact by verdict.py, never hand-typed "
                  f"or truncated; re-run ocr-pull-discussions.py + verdict.py",
                  file=sys.stderr)
            sys.exit(1)
        anchor = entry.get("anchor")
        if isinstance(anchor, str) and anchor:
            body = by_id[disc_id].get("body") or ""
            actual = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]
            if actual != anchor:
                print(f"ERROR: {label}: anchor mismatch — pull file body hashes to "
                      f"{actual}, entry carries {anchor}; the classified entry does not "
                      f"match the pulled comment (stale round or hand-edited state?) — "
                      f"re-run verdict.py against the current pull file",
                      file=sys.stderr)
                sys.exit(1)


def _write_back_posted(classified_path, entries):
    """Persist posted:true delivery flags to the --classified file (atomic,
    verdict.py's tmp+replace pattern). A write-back failure must not fail the
    run — the replies are already on the wall and content dedup is the net."""
    tmp_path = classified_path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump({"schema": _SCHEMA_VERSION, "entries": entries},
                      fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp_path, classified_path)
    except OSError as exc:
        print(f"[WARN] could not write posted flags back to {classified_path}: {exc}",
              file=sys.stderr)


# ── OCR summary-thread sweep (spec #57 Q6 AMEND, #62) ──

_SUMMARY_START = "start"
_SUMMARY_END = "end"
_SUMMARY_ERROR = "error"

# Root-note prefixes that make a thread an OCR status notice. Keep in sync
# with _OCR_SUMMARY_PREFIXES in ocr-verify-resolved.py — the sweep must
# handle exactly the threads the closure gate flags.
_SUMMARY_PREFIXES = (("🔍", _SUMMARY_START),
                     ("✅ OpenCodeReview", _SUMMARY_END),
                     ("⚠️ OpenCodeReview", _SUMMARY_ERROR))

# Fallback notes carry findings (pull parses them into classified entries):
# a lingering unresolved fallback thread needs verdicts, not a status reply.
# Keep in sync with _is_fallback_body in ocr-pull-discussions.py.
_FALLBACK_BODY_RE = re.compile(r"🔍 \*{0,2}OpenCodeReview\*{0,2} — issues")

_SUMMARY_BODY_START = """### 🔍 Triage 已启动

本轮 triage 已启动，结果将回帖于运行汇总处。
"""

_SUMMARY_BODY_END = """### ✅ Triage 汇总

本轮分类裁决统计：TP {tp} / FP {fp} / Edge {edge} / OOS {oos} / Q {q}

修复涉及文件：
{files}
"""

_SUMMARY_BODY_ERROR = """### ⚠️ Triage 受阻

本轮 OpenCodeReview 运行异常，未产出裁决，请人工检查 OCR 运行日志。
"""


def _classify_summary_body(body):
    """Map a root-note body to its summary class (None = not a summary)."""
    text = (body or "").strip()
    if _FALLBACK_BODY_RE.match(text):
        return None
    for prefix, cls in _SUMMARY_PREFIXES:
        if text.startswith(prefix):
            return cls
    return None


def _summary_stats(entries):
    """Verdict counts for the ✅ end template — straight from the classified
    entries post just delivered (canonical classes; Q already normalized)."""
    counts = {c: 0 for c in _VALID_CLASSIFICATIONS}
    for e in entries:
        cls = e.get("classification")
        if cls in counts:
            counts[cls] += 1
    return counts


def _summary_fix_files(entries, findings):
    """TP files in pull-file order — the 修复涉及文件 list. Classified entries
    carry no file field; the same pull file the anchor gate joined against
    supplies it."""
    file_by_id = {f.get("discussion_id"): f.get("file", "")
                  for f in findings if isinstance(f, dict)}
    files = []
    for e in entries:
        if e.get("classification") != "TP":
            continue
        path = file_by_id.get(e.get("discussion_id"), "")
        if path and path not in files:
            files.append(path)
    return files


def _summary_body(cls, stats, fix_files, anchor):
    if cls == _SUMMARY_START:
        text = _SUMMARY_BODY_START
    elif cls == _SUMMARY_END:
        files = "\n".join(f"- {f}" for f in fix_files) or "（无）"
        text = _SUMMARY_BODY_END.format(
            tp=stats["TP"], fp=stats["FP"], edge=stats["Edge"],
            oos=stats["OOS"], q=stats["Question"], files=files)
    else:
        text = _SUMMARY_BODY_ERROR
    return text.strip() + f"\n\n<!-- {_ANCHOR_MARKER.format(anchor=anchor)} -->"


def _sweep_summary_threads(threads, classified_ok, stats, fix_files, reply, resolve):
    """Reply-and-maybe-resolve the listed summary threads (platform mechanics
    injected: reply(thread, body) -> bool, resolve(thread) -> bool; thread
    dicts carry id/cls/anchor/note_bodies).

    Q6 rules: end/LGTM threads always reply+resolve; error threads reply only
    and fail the run; start threads resolve only when an ✅ end thread exists
    AND ended resolved AND the classified phase had zero failed items.
    Replies already on the wall (content dedup) are never repeated, but the
    resolve still executes for non-error threads so a previously
    replied-but-open thread closes on re-run.

    Sweep logs carry no platform ids — summary threads are outside the pull
    file, so there is no ordinal to label them with (display discipline).
    """
    ok = True
    error_seen = False
    end_ok = True
    # H3: already-resolved summary threads ride the listing as closure
    # evidence — a resolved ✅ end counts toward has_end so a start left open
    # by a failed round 1 can still close on run 2.
    has_end = any(t["cls"] == _SUMMARY_END for t in threads)
    # end + error first: the start-thread resolve decision needs their outcome
    ordered = ([t for t in threads if t["cls"] != _SUMMARY_START]
               + [t for t in threads if t["cls"] == _SUMMARY_START])
    for t in ordered:
        cls = t["cls"]
        if t.get("resolved"):
            print(f"[SKIP] summary {cls} thread: already resolved (closure evidence)", file=sys.stderr)
            continue
        marker = _ANCHOR_MARKER.format(anchor=t["anchor"])
        deduped = any(marker in body for body in t["note_bodies"])
        if deduped:
            print(f"[SKIP] summary {cls} thread: sweep note already on wall (content dedup)", file=sys.stderr)
        elif not reply(t, _summary_body(cls, stats, fix_files, t["anchor"])):
            print(f"[FAIL] summary {cls} thread: reply failed — left open", file=sys.stderr)
            ok = False
            if cls == _SUMMARY_ERROR:
                error_seen = True
            elif cls == _SUMMARY_END:
                end_ok = False
            continue
        if cls == _SUMMARY_ERROR:
            error_seen = True
            print("[OK] summary error thread escalated — left open (human-in-loop by design)", file=sys.stderr)
            continue
        if cls == _SUMMARY_START and not (has_end and end_ok and classified_ok):
            print("[OK] summary start thread confirmed — left open (no completed ✅ end thread to take over)", file=sys.stderr)
            continue
        if resolve(t):
            print(f"[OK] summary {cls} thread {'resolved (content dedup)' if deduped else 'replied + resolved'}", file=sys.stderr)
        else:
            print(f"[FAIL] summary {cls} thread: resolve failed — left open for the closure gate", file=sys.stderr)
            ok = False
            if cls == _SUMMARY_END:
                end_ok = False
    if error_seen:
        print("ERROR: ⚠️ OCR error thread on this MR — the review round produced no "
              "verdicts; inspect the OCR run logs by hand. The closure gate stays red "
              "by design (human-in-loop, spec #57 Q6).", file=sys.stderr)
        ok = False
    return ok


# ── GitLab backend ──


def _tid(disc_id):
    """Stable display handle for a thread id in human-facing stderr lines.

    A short hash of the id — never a prefix of the real id, so truncated-id
    shapes cannot flow from display back into state (spec #57 display
    discipline). """
    import hashlib
    return "thread#" + hashlib.sha256(str(disc_id).encode()).hexdigest()[:8]


def _sweep_notes_gitlab(base, disc_id, curl):
    """Resolve every remaining resolvable-unresolved note in a thread.

    GitLab threads carry per-note resolvable/resolved flags, and the
    discussion-level PUT only resolves the thread head — reply notes
    (including the verdict label just posted) stay open and trip the closure
    gate. Called after a successful thread resolve so the script leaves
    nothing for a manual fallback.

    Returns True iff every resolvable note is resolved after this pass —
    also serves as the fallback resolve path for instances where the
    discussion-level PUT fails structurally (e.g. some internal instances
    return 500 on it).
    """
    status, disc, _ = curl(f"{base}/discussions/{disc_id}")
    if status != 200 or not isinstance(disc, dict):
        print(f"[WARN] note sweep {_tid(disc_id)}: fetch HTTP {status} — notes untouched", file=sys.stderr)
        return False
    swept = remaining = 0
    for note in disc.get("notes", []):
        if note.get("resolvable") and not note.get("resolved"):
            note_id = note.get("id")
            st, _, _ = curl(
                f"{base}/discussions/{disc_id}/notes/{note_id}",
                method="PUT",
                data={"resolved": True},
            )
            if 200 <= st < 300:
                swept += 1
            else:
                remaining += 1
                print(f"[WARN] note sweep {_tid(disc_id)}/{note_id}: HTTP {st}", file=sys.stderr)
    if swept:
        print(f"[OK] swept {swept} open reply note(s) in {_tid(disc_id)}", file=sys.stderr)
    return remaining == 0


def _resolve_gitlab_thread(base, disc_id, curl):
    """Resolve one GitLab thread: discussion-level PUT first; when that fails
    structurally (some instances 500 on it), the note sweep is the working
    fallback resolve path. Returns True iff the thread ends up resolved."""
    status, _, _ = curl(
        f"{base}/discussions/{disc_id}",
        method="PUT",
        data={"resolved": True},
    )
    if 200 <= status < 300:
        _sweep_notes_gitlab(base, disc_id, curl)
        return True
    if _sweep_notes_gitlab(base, disc_id, curl):
        print(f"[WARN] discussion PUT {_tid(disc_id)}: HTTP {status} — "
              f"resolved via note-level fallback", file=sys.stderr)
        return True
    print(f"[FAIL] resolve {_tid(disc_id)}: HTTP {status}", file=sys.stderr)
    return False


def _sweep_summaries_gitlab(mr_iid, classified_ok, stats, fix_files):
    """List the MR's still-open OCR summary threads (same discussion listing
    and filtering the closure gate applies) and hand them to the shared
    sweep runner. Fails closed when the listing itself fails — a silently
    empty sweep would look like a done MR."""
    from ocr_gitlab import curl, get_project_id

    project_id = get_project_id()
    if not project_id:
        print("ERROR: could not determine GitLab project ID", file=sys.stderr)
        return False
    base = f"/projects/{project_id}/merge_requests/{mr_iid}"

    threads = []
    for page in range(1, 6):
        status, body, _ = curl(f"{base}/discussions?per_page=100&page={page}")
        if page == 1 and not (200 <= status < 300 and isinstance(body, list)):
            print(f"ERROR: summary sweep: discussions listing failed (HTTP {status}) "
                  f"— summary threads left open", file=sys.stderr)
            return False
        if status == 0 or not isinstance(body, list) or not body:
            break
        for disc in body:
            notes = [n for n in disc.get("notes", []) if isinstance(n, dict)]
            if not notes:
                continue
            resolvable = [n for n in notes if n.get("resolvable", False)]
            if not resolvable:
                continue
            root_body = notes[0].get("body") or ""
            cls = _classify_summary_body(root_body)
            if not cls:
                continue
            threads.append({
                "id": disc.get("id", ""),
                "cls": cls,
                # H3: fully-resolved summary threads stay in the listing as
                # closure evidence instead of vanishing (has_end false forever)
                "resolved": all(n.get("resolved", False) for n in resolvable),
                "anchor": hashlib.sha256(root_body.encode("utf-8")).hexdigest()[:16],
                "note_bodies": [n.get("body") or "" for n in notes],
            })
        if len(body) < 100:
            break

    def reply(t, body):
        st, _, _ = curl(f"{base}/discussions/{t['id']}/notes",
                        method="POST", data={"body": body})
        return 200 <= st < 300

    return _sweep_summary_threads(
        threads, classified_ok, stats, fix_files, reply,
        lambda t: _resolve_gitlab_thread(base, t["id"], curl))


def _post_gitlab(mr_iid, items, resolved_map=None, force=False):
    from ocr_gitlab import curl, get_project_id

    resolved_map = resolved_map or _DEFAULT_RESOLVED
    project_id = get_project_id()
    if not project_id:
        print("ERROR: could not determine GitLab project ID", file=sys.stderr)
        return False

    base = f"/projects/{project_id}/merge_requests/{mr_iid}"
    ok = fail = skip = 0

    for idx, item in enumerate(items):
        valid, err, cleaned = _validate_item(item, idx, resolved_map)
        if not valid:
            print(f"[SKIP] {err}", file=sys.stderr)
            skip += 1
            continue

        disc_id = cleaned["discussion_id"]
        cls = cleaned["classification"]
        do_resolve = cleaned["resolved"]
        label = _CLASSIFICATION_LABELS.get(cls, cls)

        # content dedup (#61 ③, H2): same GET the note sweep uses — a thread
        # whose wall already carries this entry's anchor marker + verdict rev
        # gets no second reply; an anchor-only match is a revised verdict →
        # re-post (the superseded reply stays as history)
        anchor = cleaned.get("anchor")
        deduped = False
        if anchor:
            st, disc, _ = curl(f"{base}/discussions/{disc_id}")
            if st == 200 and isinstance(disc, dict):
                marker = (f"{_ANCHOR_MARKER.format(anchor=anchor)} "
                          f"rev:{_verdict_rev(cleaned)}")
                deduped = any(marker in (n.get("body") or "")
                              for n in disc.get("notes", []) if isinstance(n, dict))
            else:
                print(f"[WARN] dedup probe {_tid(disc_id)}: HTTP {st} — posting anyway", file=sys.stderr)
        if deduped:
            print(f"[SKIP] {label} {_tid(disc_id)}: verdict note already on wall (content dedup)", file=sys.stderr)

        # 1) reply (#61 ④: a failed reply must never lead to a resolve)
        reply_status = None
        posted_now = False
        if not deduped:
            reply_status, _, _ = curl(
                f"{base}/discussions/{disc_id}/notes",
                method="POST",
                data={"body": _build_body(cleaned)},
            )
            posted_now = 200 <= reply_status < 300
            if posted_now:
                item["posted"] = True  # declared exception writer of the delivery-status field

        # 2) resolve per-item (#61 ⑤: execute the verdict-time decision)
        resolved_ok = False
        if do_resolve and (posted_now or deduped):
            resolved_ok = _resolve_gitlab_thread(base, disc_id, curl)
        elif do_resolve and force:
            resolved_ok = _resolve_gitlab_thread(base, disc_id, curl)
            print(f"[WARN] reply {_tid(disc_id)}: HTTP {reply_status} — resolving anyway (--force)", file=sys.stderr)
        elif do_resolve:
            print(f"[FAIL] reply {_tid(disc_id)}: HTTP {reply_status} — NOT resolving "
                  f"(verdict reason not on wall; --force to override)", file=sys.stderr)

        # 3) count + report
        if not posted_now and not deduped:
            fail += 1  # reply failed: the verdict reason never reached the wall
        elif deduped and not do_resolve:
            skip += 1  # dedup line already printed
        elif deduped and not resolved_ok:
            fail += 1  # resolve failed on an already-labeled thread
        elif deduped:
            ok += 1
            print(f"[OK] {label} {_tid(disc_id)}: already labeled — resolved (content dedup)", file=sys.stderr)
        elif do_resolve and not resolved_ok:
            fail += 1
        elif do_resolve:
            ok += 1
            print(f"[OK] {label} resolved {_tid(disc_id)}", file=sys.stderr)
        else:
            ok += 1
            print(f"[OK] {label} labeled {_tid(disc_id)} (open)", file=sys.stderr)

    total = ok + fail
    print(f"Done: {ok} ok, {fail} failed, {skip} skipped ({total}/{len(items)} processed)", file=sys.stderr)
    return fail == 0


# ── GitHub backend ──


def _resolve_github_thread(pr_number, comment_id):
    """Resolve a GitHub PR review thread via GraphQL.

    GitHub's REST API doesn't support resolving review threads. We need to:
    1. Get the PR's node_id
    2. Query review threads to find the thread containing our comment
    3. Call resolveReviewThread mutation

    Returns True if resolved (or already resolved), False on failure.
    """
    from ocr_github import curl, graphql, get_project_id

    owner_repo = get_project_id()
    if not owner_repo:
        return False
    owner, repo = owner_repo.split("/", 1)

    # 1. Get PR node_id
    status, pr_body, _ = curl(f"/repos/{owner}/{repo}/pulls/{pr_number}")
    if status == 0 or not isinstance(pr_body, dict):
        return False
    pr_node_id = pr_body.get("node_id")
    if not pr_node_id:
        return False

    # 2. Query review threads to find the one containing our comment
    #    comment_id is the databaseId; we match against comments[].databaseId
    try:
        comment_id_int = int(comment_id)
    except (ValueError, TypeError):
        return False

    query = """
    query($pr: ID!) {
      node(id: $pr) {
        ... on PullRequest {
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              comments(first: 5) {
                nodes { databaseId }
              }
            }
          }
        }
      }
    }
    """
    status, result, _ = graphql(query, {"pr": pr_node_id})
    if status == 0 or not result or "data" not in result:
        return False

    threads = (
        result.get("data", {})
        .get("node", {})
        .get("reviewThreads", {})
        .get("nodes", [])
    )

    thread_node_id = None
    for thread in threads:
        comment_ids = [c.get("databaseId") for c in thread.get("comments", {}).get("nodes", [])]
        if comment_id_int in comment_ids:
            if thread.get("isResolved"):
                return True  # already resolved — genuinely done
            thread_node_id = thread.get("id")
            break

    if not thread_node_id:
        # #62: not-found is not "already resolved" — the old silent True hid
        # id mismatches (the dual-ID-space family). Report failure; the
        # closure gate catches any thread this leaves open. Note
        # comments(first: 5): a comment buried deeper in a long thread also
        # lands here.
        print(f"ERROR: no open review thread contains comment {comment_id} — not resolving",
              file=sys.stderr)
        return False

    # 3. Resolve the thread
    mutation = """
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { isResolved }
      }
    }
    """
    status, result, _ = graphql(mutation, {"threadId": thread_node_id})
    if status == 0 or not result or "errors" in result:
        return False

    return (
        result.get("data", {})
        .get("resolveReviewThread", {})
        .get("thread", {})
        .get("isResolved", False)
    )


def _resolve_github_thread_node(thread_node_id):
    """resolveReviewThread on a thread node id already in hand from the
    sweep's own GraphQL listing (#62) — no re-matching by comment id needed.
    Returns True iff the thread reports resolved after the mutation."""
    from ocr_github import graphql

    mutation = """
    mutation($threadId: ID!) {
      resolveReviewThread(input: {threadId: $threadId}) {
        thread { isResolved }
      }
    }
    """
    status, result, _ = graphql(mutation, {"threadId": thread_node_id})
    if status == 0 or not result or "errors" in result:
        return False
    return (
        result.get("data", {})
        .get("resolveReviewThread", {})
        .get("thread", {})
        .get("isResolved", False)
    )


def _sweep_summaries_github(pr_number, classified_ok, stats, fix_files):
    """Sweep the PR's open OCR summary review threads. The thread list, the
    REST reply target (root comment databaseId) and the GraphQL resolve
    target (thread node id) all come from ONE reviewThreads listing here —
    the two id spaces never cross call paths, and verify --json ids (thread
    node ids) are never consumed (#62). Fails closed on listing failure."""
    from ocr_github import curl, graphql, get_project_id

    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return False
    owner, repo = owner_repo.split("/", 1)

    status, pr_body, _ = curl(f"/repos/{owner}/{repo}/pulls/{pr_number}")
    if status == 0 or not isinstance(pr_body, dict) or not pr_body.get("node_id"):
        print(f"ERROR: summary sweep: could not fetch PR #{pr_number} — "
              f"summary threads left open", file=sys.stderr)
        return False

    query = """
    query($pr: ID!) {
      node(id: $pr) {
        ... on PullRequest {
          reviewThreads(first: 100) {
            nodes {
              id
              isResolved
              comments(first: 5) { nodes { body databaseId } }
            }
          }
        }
      }
    }
    """
    status, result, _ = graphql(query, {"pr": pr_body["node_id"]})
    threads_raw = (
        result.get("data", {}).get("node", {}).get("reviewThreads", {}).get("nodes", [])
        if status != 0 and result and "data" in result else None
    )
    if threads_raw is None:
        print("ERROR: summary sweep: reviewThreads listing failed — summary threads left open",
              file=sys.stderr)
        return False

    threads = []
    for t in threads_raw:
        comments = [c for c in t.get("comments", {}).get("nodes", []) if isinstance(c, dict)]
        if not comments:
            continue
        root = comments[0]
        cls = _classify_summary_body(root.get("body", ""))
        if not cls:
            continue
        threads.append({
            "id": t.get("id", ""),
            "cls": cls,
            # H3: resolved summary threads stay in the listing as closure
            # evidence (the runner never re-replies or re-resolves them)
            "resolved": bool(t.get("isResolved")),
            "anchor": hashlib.sha256((root.get("body") or "").encode("utf-8")).hexdigest()[:16],
            "note_bodies": [c.get("body") or "" for c in comments],
            "root_comment_id": root.get("databaseId"),
        })

    def reply(t, body):
        st, _, _ = curl(
            f"/repos/{owner_repo}/pulls/{pr_number}/comments/{t['root_comment_id']}/replies",
            method="POST", data={"body": body})
        return 200 <= st < 300

    return _sweep_summary_threads(threads, classified_ok, stats, fix_files,
                                  reply, lambda t: _resolve_github_thread_node(t["id"]))


def _github_thread_has_marker(owner_repo, pr_number, comment_id, anchor, rev, curl):
    """True when the parent comment or any of its replies already carries the
    entry's anchor marker + verdict rev (H2) — the GitHub content-dedup probe
    (#61 ③). An anchor-only match is a revised verdict → re-post.

    H1: GitHub does not serve GET on a comment's /replies endpoint (POST-only,
    no listing there) — the old probe always 404'd and the offline fixture
    masked it, so every retry re-posted the verdict. Replies are listed via
    the PR review-comments listing filtered by in_reply_to, paginated."""
    marker = f"{_ANCHOR_MARKER.format(anchor=anchor)} rev:{rev}"
    status, parent, _ = curl(f"/repos/{owner_repo}/pulls/comments/{comment_id}")
    if status == 200 and isinstance(parent, dict) and marker in (parent.get("body") or ""):
        return True
    page = 1
    while True:
        status, replies, _ = curl(
            f"/repos/{owner_repo}/pulls/{pr_number}/comments"
            f"?in_reply_to={comment_id}&per_page=100&page={page}")
        if status != 200 or not isinstance(replies, list):
            return False
        if any(marker in (r.get("body") or "") for r in replies if isinstance(r, dict)):
            return True
        if len(replies) < 100 or page >= 10:  # shortcut: 1000-reply cap, revisit if a thread ever exceeds it
            return False
        page += 1


def _post_github(pr_number, items, resolved_map=None, force=False):
    from ocr_github import curl, get_project_id

    resolved_map = resolved_map or _DEFAULT_RESOLVED
    owner_repo = get_project_id()
    if not owner_repo:
        print("ERROR: could not determine GitHub owner/repo", file=sys.stderr)
        return False

    ok = fail = skip = 0

    for idx, item in enumerate(items):
        valid, err, cleaned = _validate_item(item, idx, resolved_map)
        if not valid:
            print(f"[SKIP] {err}", file=sys.stderr)
            skip += 1
            continue

        comment_id = cleaned["discussion_id"]
        cls = cleaned["classification"]
        do_resolve = cleaned["resolved"]
        label = _CLASSIFICATION_LABELS.get(cls, cls)

        # content dedup (#61 ③, H2): parent comment or replies already carry
        # the anchor+rev marker
        anchor = cleaned.get("anchor")
        deduped = False
        if anchor and _github_thread_has_marker(owner_repo, pr_number, comment_id,
                                                anchor, _verdict_rev(cleaned), curl):
            deduped = True
            print(f"[SKIP] {label} {_tid(comment_id)}: verdict note already on wall (content dedup)", file=sys.stderr)

        # 1) reply (#61 ④: a failed reply must never lead to a resolve)
        posted_now = False
        if not deduped:
            body = _build_body(cleaned)
            endpoint = f"/repos/{owner_repo}/pulls/{pr_number}/comments/{comment_id}/replies"
            status, resp, _ = curl(endpoint, method="POST", data={"body": body})
            if not (200 <= status < 300):
                # Fallback: post as a regular PR comment
                status2, _, _ = curl(
                    f"/repos/{owner_repo}/issues/{pr_number}/comments",
                    method="POST",
                    data={"body": body},
                )
                posted_now = 200 <= status2 < 300
                if not posted_now:
                    print(f"[FAIL] reply {comment_id}: HTTP {status}, fallback HTTP {status2} — "
                          f"NOT resolving (verdict reason not on wall; --force to override)", file=sys.stderr)
                    if do_resolve and force:
                        if _resolve_github_thread(pr_number, comment_id):
                            print(f"[WARN] {_tid(comment_id)}: resolved anyway (--force)", file=sys.stderr)
                        else:
                            print(f"[WARN] {_tid(comment_id)}: resolve also failed (--force)", file=sys.stderr)
                    fail += 1
                    continue
            else:
                posted_now = True
            if posted_now:
                item["posted"] = True  # declared exception writer of the delivery-status field

        # 2) resolve per-item (#61 ⑤: execute the verdict-time decision)
        if do_resolve and (posted_now or deduped):
            resolved = _resolve_github_thread(pr_number, comment_id)
            if resolved:
                ok += 1
                suffix = " (content dedup)" if deduped else ""
                print(f"[OK] {label} resolved {_tid(comment_id)}{suffix}", file=sys.stderr)
            else:
                print(f"[WARN] reply ok but resolve failed for {_tid(comment_id)}", file=sys.stderr)
                ok += 1  # reply succeeded, just couldn't resolve — verify gate catches open threads
        elif deduped:
            skip += 1
            print(f"[SKIP] {label} {_tid(comment_id)}: already labeled, left open (content dedup)", file=sys.stderr)
        else:
            ok += 1
            print(f"[OK] {label} labeled {_tid(comment_id)} (open)", file=sys.stderr)

    total = ok + fail
    print(f"Done: {ok} ok, {fail} failed, {skip} skipped ({total}/{len(items)} processed)", file=sys.stderr)
    return fail == 0


# ── Main ──


def _parse_args(argv):
    """Return (mr_or_pr_id, mode, classified_path, pull_file, force) from the CLI tail."""
    if not argv or argv[0].startswith("-"):
        return None, None, None, None, False
    mr_or_pr_id = argv[0]
    mode = "default"
    classified_path = None
    pull_file = None
    force = False
    rest = argv[1:]
    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--mode" and i + 1 < len(rest):
            mode = rest[i + 1]
            i += 2
        elif arg == "--classified" and i + 1 < len(rest):
            classified_path = rest[i + 1]
            i += 2
        elif arg == "--pull-file" and i + 1 < len(rest):
            pull_file = rest[i + 1]
            i += 2
        elif arg == "--force":
            force = True
            i += 1
        elif arg in ("--mode", "--classified", "--pull-file"):
            print(f"ERROR: {arg} requires a value", file=sys.stderr)
            sys.exit(1)
        else:
            i += 1
    return mr_or_pr_id, mode, classified_path, pull_file, force


USAGE = ("Usage: python3 ocr-post-labels.py <MR_OR_PR_ID> [--mode triage] [--classified <path>] "
         "[--pull-file <path>] [--force]  [< state.json]")


def main():
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    mr_or_pr_id, mode, classified_path, pull_file, force = _parse_args(sys.argv[1:])
    if mr_or_pr_id is None:
        print(USAGE, file=sys.stderr)
        sys.exit(1)

    if classified_path is not None:
        filename = classified_path
        try:
            with open(classified_path, encoding="utf-8") as fh:
                raw = fh.read()
        except OSError as exc:
            print(f"ERROR: cannot read --classified {classified_path}: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        # stdin is a transport only — the same schema 2 validation applies
        filename = "<stdin>"
        raw = sys.stdin.read()

    entries = _preflight(_parse_state_entries(raw, filename), filename)

    # join + anchor validation gates ALL platform traffic (#61 ①②)
    pull_path = pull_file or os.path.join(triage_state_dir(mr_or_pr_id), "issues.json")
    _validate_against_pull(entries, pull_path)

    # summary-thread sweep inputs (Q6): verdict counts + TP fix files. The
    # pull file is re-read here — the join gate above already hard-failed on
    # a missing/unreadable one, so this cannot diverge.
    findings = load_pull_findings(pull_path)
    stats = _summary_stats(entries)
    fix_files = _summary_fix_files(entries, findings)

    posted_before = sum(1 for e in entries if e.get("posted"))
    resolved_map = _TRIAGE_RESOLVED if mode == "triage" else _DEFAULT_RESOLVED

    platform = detect_platform()
    print(f"Detected platform: {platform}", file=sys.stderr)

    run_auth_probe(platform)

    if platform == "github":
        success = _post_github(mr_or_pr_id, entries, resolved_map, force)
        summary_ok = _sweep_summaries_github(mr_or_pr_id, success, stats, fix_files)
    else:
        success = _post_gitlab(mr_or_pr_id, entries, resolved_map, force)
        summary_ok = _sweep_summaries_gitlab(mr_or_pr_id, success, stats, fix_files)
    success = success and summary_ok

    if classified_path is not None and sum(1 for e in entries if e.get("posted")) > posted_before:
        _write_back_posted(classified_path, entries)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
