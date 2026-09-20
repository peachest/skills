# herdr CLI ops mining — evidence baseline (2026-09-20)

Full-scan audit by `mine-herdr-ops.py` (same dir). Next re-run diffs against these
numbers; material drift (>2× error rate, new subcommand in top-5) means the bundled
tools' coverage needs review.

## Baseline numbers

- Scope: 2609 pi sessions, **1117 paired herdr bash calls** (call→result pairs, ~146 sessions)
- Top ops: `agent prompt` 315 (8% err) · `agent get` 139 (5%) · `agent list` 117 (7%) · `agent read` 66 (5%) · `workspace create` 8 (**50%**)
- `agent list` shapes: 68 piped-to-parser, 64 other/complex, **6 bare** — its dominant use is parsing addresses out of the envelope, not listing

## Failure classes (the load-bearing conclusions)

1. **Envelope/output parsing crashes dominate**: `KeyError: 'result'` / `KeyError: 'agents'`
   / `JSONDecodeError` across prompt/list/read/create — ~40+ crashes over 4 months.
   Documented in pitfalls #5/#7/#8 yet still recurring; pitfalls.md had exactly **1
   direct read-load** in 29 marker-injected sessions → documentation alone cannot stop
   this class; deterministic wrappers can (herdr-resolve.py / herdr-send.py).
2. **Direct sends rarely fail**: bare `herdr agent prompt` ~1% error; the 8% headline
   was inflated by python-wrapper parse crashes wrapping the send. Quoting
   (`unknown option`) is real but rare (2 mined).
3. **"Command aborted" pollutes error stats**: user aborts counted as tool errors —
   7/138 of `agent get`'s "errors" (pitfalls #25). Exclude before drawing conclusions.
4. **Session-UUID → address** was rare as a literal pattern (1 hit) but is the
   motivation behind most `agent list` parsing — the resolve flow is multi-step and
   every step is a parse crash opportunity (→ herdr-resolve.py).
5. **Stale addressing is rare but blocking**: `pane_not_found`, wait timeout (pitfalls
   #11/#16). No tool needed; pitfalls coverage is enough.

## Method notes (for re-runs)

- Pair `assistant.toolCall` (bash, contains `herdr`) with the later `toolResult` message
  by `toolCallId`; `isError: true` marks failures. A call whose result never arrived is
  NOT an error (session cut short).
- `"Command aborted"` in result text = user abort — bucket separately before claiming
  failure rates.
- Subcommand extraction regex stops at shell separators; heredoc-heavy multi-command
  cells fragment (cosmetic, does not affect the top-line conclusions).
- Reference read-load audits (was pitfalls.md ever opened?) are a different signal —
  use skill-call-extract's `find-skill-sessions.py` (marker + read-load modes), not this
  script.
