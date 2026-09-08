# Scan evidence

Empirical backing for the rules in this skill, from a scan of the 200 most recent pi sessions (one week, 2026-09-02 → 2026-09-08). Method: a one-off script parsed each session's bash tool calls, kept every command containing `ssh`/`scp`/`sshpass`, classified it (inline vs scp-first vs upload/download, quoting density, heredoc, length), and joined each to its tool result to extract the exit status. Node names, IPs, and credentials are sanitized; the counts are real.

## Totals

287 remote commands across 9 sessions (most sessions touch no remote node at all).

## Pattern vs failure rate

| Pattern | Count | Fail rate |
|---|---|---|
| Inline command (`ssh '...'`) | 253 | 13% |
| scp + remote script execution | 12 | **0%** |
| Pure scp transfer | 43 | 2% |
| Inline heredoc | 11 | 27% |
| Inline command > 1200 chars | 3 | **100%** |
| Inline quote-heavy commands | 95 | 17% (survived but fragile) |

The scp-first pattern never failed once in the scan window; inline failed roughly every eighth command. Length alone is a predictor: every >1200-char inline command failed, all with quoting/parsing errors.

## Failure taxonomy (33 failures)

| Cause | Count | Feeds rule |
|---|---|---|
| Remote file missing | 12 | (probing — expected) |
| Auth failure (`Permission denied`) | 7 | first-contact probe |
| Local timeout killed the ssh session | 5 | time-bound every remote command |
| Quoting/parsing error | 4 | quoting hell / escalate on first failure |
| Other remote error | 3 | — |
| Connection refused | 2 | — |

All 5 timeout failures were the same two shapes: long remote waits (`kubectl rollout status` polling) with no remote-side `timeout`, and a background `nohup` launch bundled with `sleep` + follow-up checks in one ssh string.

## Credential anti-pattern is universal

`sshpass -p <inline password>`: 129 occurrences. `sshpass -e` (env var): **0**. During the scan itself, a regex accidentally recovered the plaintext password from session logs — direct confirmation that inline passwords persist in transcripts and leak to anything that reads them.

## Escalation lag

Only 2 of 9 sessions escalated from inline failure to scp-first; the rest kept retrying inline. This is why the skill's trigger description includes "an inline ssh command failed — escalate instead of retrying inline" as an explicit branch.
