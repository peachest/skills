# argocd-ops — skill impact log

## 2026-09-22 — Troubleshooting playbook restructure

- **Proposal**: session diagnosis (tool-call-extract + tool-call-diagnose over a peer session, 42 argocd bash calls vs 1246 total). Two persistent gaps surfaced twice each in the trace; routed as skill-doc.
- **Changes** (commit 159b8d2):
  - `Pitfalls` → `Troubleshooting`, entries reframed symptom → forensics → fix (writing-for-agents negation lever: positive framing over prohibition).
  - New entry "Stale manifest cache: escalation ladder" — hard refresh → repo-server restart → Redis purge (`mfst|*` keys, auth via pod env) → `operation.sync` CR patch. Trace evidence: 6 improvised calls in two identical rounds for the redis-clearing sequence.
  - New entry "Editing helm parameters on the Application CR" — JSON Patch can't match array elements by name; read-modify-write whole array; automated-sync revert warning. Trace evidence: rejected pseudo-path json-patch, then two rounds of re-patching after sync rollback.
  - Playbook §3 pointer to the ladder when a post-refresh cycle doesn't converge (5 refresh calls all used `normal` where `hard` was documented).
  - §2: CLI availability via `command -v`; CLI-absent path via `operation` patch.
- **Verification**: sanitize-check CLEAN; no internal identifiers in new content; no tests in skill dir (exempt).
- **Rejected**: none.
