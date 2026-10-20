---
name: hook-me
description: Mine a workspace's past sessions for deterministic behaviors that should become hooks, then spec each candidate for implementation.
disable-model-invocation: true
argument-hint: "A repo or directory to mine, or nothing for the current workspace"
---

Mine the given repo's past agent sessions for behaviors worth turning into **hooks**, and run each survivor of the audit into a hook spec. For multiple repos, dispatch one mining subagent per repo in parallel and cross-check their findings.

## The hook lens

A **hook** is a deterministic action bound to a lifecycle event: it always runs, and its exit code gates the agent (exit 2 + stderr = block; other exits = inject). A **rule** is guidance the agent may or may not follow. Rules direct; hooks guarantee. Every candidate is an attempted migration of a rule-shaped behavior from memory into mechanism.

The **audit** sorts each mined behavior by one question: is this rule naming an event, or encoding a judgment?

- **Names an event** ("after implementing, run the tests"; "never push without approval") → the behavior is a fixed action on a lifecycle moment → migrate to a hook.
- **Encodes a judgment** ("amounts must be integers"; "target branch is X here") → context-dependent constraint → stays a rule.
- **Neither** → the agent already does it by default → delete.

A candidate that names an event also picks a **layer**. Ask who the guarantee must cover: a pi hook gates only this machine's agent lifecycle; a git hook gates every path into the repo — human commits, other sessions, other agents. Agent-only behavior (turn_end validation, kubectl deletes, polling) is pi-hook territory; anything that must never enter the repository (credentials, leaked tokens) belongs at a git hook — a gitleaks-style pre-commit — because the agent-side guard only stops one path of many. The layers stack: credentials run both, the pi guard as the earlier cheaper stop, the git hook as the last-resort gate. Git-hook conventions per repo live in that repo's `tools/git-hooks/` + wt `pre-start` install pattern.

An event-named candidate then splits by action shape:

- **Guard**: block the action (exit 2) when a match condition fires. For danger: destructive commands, unapproved pushes, leaked credentials. Guards must carry a whitelist for legitimate flows that share the same command shape.
- **Nudge**: inject a reminder without blocking, for verification gaps the agent can still fix in-turn ("claimed done, zero validation ran").
- **Ritual**: inject context at session start. Highest false-positive risk — most "opening ceremonies" are minority habits, not laws.

## Definition of done

A candidate spec is done when an implementer could write the hook script without asking a single question. Every spec carries: layer (pi hook / git hook / both), hook event, match condition (pseudocode), action (guard/nudge/ritual), evidence (raw count, denominator, human-adjudicated true count), false-positive risk with its whitelist, and a coverage check against what already guards or skills already enforce. Nothing is done while a question remains.

## Mining reference

Session data lives under `~/.pi/agent/sessions/<slug>/<timestamp>_<uuid>.jsonl`. First line is `{"type":"session","cwd":...,"id":...}`; entries after are `{"type":"message","message":{"role":"user|assistant|toolResult","content":[...]}}` with text blocks and `toolCall` blocks (`name`, `arguments`; bash commands in `arguments.command`). Group sessions by the `cwd` field, never by slug directory — worktree directories get recycled while their sessions survive. Strip the local `rtk ` command-rewrite prefix before clustering. Compaction replays inflate counts by ~10%; dedup before quoting numbers.

Six signals, each mapped to its hook event:

1. **SessionStart ritual**: the first bash/read commands per session. Count coverage (sessions with the pattern ÷ all sessions), not raw frequency.
2. **Edit→check pairing** (tool_result): bash that follows an edit/write within the same turn (`go build`, `make`, lint). Missing pairs after source edits are nudge candidates.
3. **Claim-done → correction** (turn_end): assistant text claiming completion (`完成/done/全绿`) followed by a user correction (`不对/错了/没验证`). Keyword clusters misfire — adjudicate every sample by hand.
4. **Dangerous commands** (guard): agent-issued `git push` (especially `--force`), `rm -rf` outside temp dirs, `kubectl delete`, plaintext credentials in commands.
5. **Repeated oral rules**: the same operational instruction the user gives in ≥3 distinct sessions. Each gets its own audit verdict.
6. **Post-edit mechanics** (tool_result): deterministic follow-ups like gofmt after `.go` edits, `make manifests` after CRD type edits. Coverage ratio decides nudge vs noise.

Four method laws, learned from a two-stage mining run (coarse scan over 908 sessions, then per-repo deep dives):

- **Denominator**: a frequency without its denominator is a minority habit dressed as a rule. `×11 sessions` means nothing until divided by the repo's session count — a 15% coverage "ritual" is not a ritual.
- **Human adjudication**: machine clustering finds candidates; only hand-read samples produce counts. Expect keyword clusters to shrink 5-8× after filtering misfires.
- **Cross-repo consensus**: a candidate independently nominated by two repos' miners outweighs any single-repo frequency; a single-repo-only candidate with purely preventive evidence ranks last.
- **Reject ledger**: record every rejected candidate with its reason in `NOTES.md`. Unrecorded rejections get re-proposed by the next mining run.

## Parallel mining (multi-repo)

One worker subagent per repo. Write the workflow script to `~/tmp/hook-mining/workflow-<date>.js` (absolute path), fan out with `runs.all`, and give each worker: the mining reference above verbatim, its repo's session slugs, and the coarse-scan clues **labeled as hypotheses to re-verify, never as conclusions**. Each worker writes python scanners (replayable, kept in `~/tmp/hook-mining/<repo>/`) and a full report to a fixed path, returning the path plus one line per top candidate. The parent then cross-checks consensus, merges specs, and owns the reject ledger.

## The workspace

- `hooks/*.md`: one spec per candidate, in the repo under review.
- `NOTES.md`: raw counts, sample quotes, the reject ledger with reasons, and open questions. Thin notes mean the mining was skipped — run it before speccing anything.
