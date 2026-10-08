---
name: doc-consumption
description: "Audit whether project docs are actually consumed by agents — from pi session logs, classify every doc touch as READ-like / WRITE-like / MENTION, check escape-rate (actions without doc compliance), and verify consumption by content echo rather than read-call counting alone. Use when the user asks 某文档/机制 agent 有没有真的在用 / 假有用 / 文档消费统计 / doc usage / which docs are sediment, before deleting or merging project docs (AGENTS.md pointers, ledgers, meta-docs), or when a session reported doc-read counts that look implausibly low."
---

# Doc Consumption

**Leading word:** the **consumption matrix** — per-target READ / WRITE / MENTION counts over all session logs (nested included), plus escape-rate and echo verification. Answers "is this doc load-bearing or sediment" with session-log evidence, not with the read-tool call count.

## Why read-call counting is wrong (proven pitfalls)

Every one of these was measured in a real 127-session project:

1. **bash cat/grep outnumbers the read tool ~40:1** (bash 6413 vs read 170). Counting `read` calls misses ~97% of consumption.
2. **Write ≠ read.** A doc written 30× and read 0× is maintenance sediment. Both sides must be counted and compared.
3. **Agents fall back to python one-liners to edit files when `edit` fails** (`python3 -c "...open('f','w').write(src.replace(...))"`), and write via heredocs (`cat > f <<EOF`) / `sed -i`. These are WRITE-like. Python with only read markers (`open().read()`, `json.load`) is READ-like.
4. **Nested session files hold sub-agent populations**: `<session>/forks/*.jsonl`, `<session>/<uuid>/run-0/session.jsonl`. A top-level `*.jsonl` glob misses them; discovery must be recursive.
5. **A read call is weak evidence.** The strong evidence is that the agent's own later reasoning echoes the doc's content.

## Process

### 1. Build the target list

Collect candidate docs/mechanisms from the project: AGENTS.md pointers, ledgers, status files, meta-docs, scripts referenced by rules. Two input forms:

```bash
# inline: pattern = its own name
--patterns 'CONTEXT.md,gpu-reservation-ledger,status.md'

# TSV file (name <TAB> pattern; pattern matched as substring against tool args):
CONSTRAINT.md	CONSTRAINT.md
domain.md	agents/domain.md
```

Distinct mechanisms sharing a filename substring need distinct patterns — `status.md` also matches `campaign-status.md`; narrow the pattern if collisions appear.

### 2. Matrix

```bash
python3 <SKILL_DIR>/scripts/doc-usage.py matrix \
  --sessions-dir ~/.pi/agent/sessions/<cwd-slug>/ \
  --targets targets.tsv
```

Columns: READ / WRITE / MENTION / sessions / read+res (read-like calls whose toolResult was non-empty — a read that returned nothing consumed nothing) / verdict. Verdicts: `consumed` (≥3 reads), `weak-read`, `only-maintained (fake-useful)` (writes, zero reads — deletion candidates), `never-touched`.

### 3. Escape-rate (only when the doc encodes an action rule)

For rules of the form "before doing X, touch doc Y", test the contrapositive — sessions doing X without ever touching Y:

```bash
python3 <SKILL_DIR>/scripts/doc-usage.py matrix ... \
  --escape 'nvidia-smi|torchrun' --escape-min 3
```

`--escape` is a regex of action signatures you pick per project. Any touch (even a write) of any target discharges the session. Escape hits before a rule's adoption date are history, not violations — bucket them by date before reporting.

### 4. Echo verification (for every `only-maintained` target, before recommending deletion)

```bash
python3 <SKILL_DIR>/scripts/doc-usage.py echo \
  --doc /proj/docs/QUESTIONED.md \
  --sessions-dir <dir> --target 'QUESTIONED.md' [--json]
```

Samples distinctive tokens from the doc on disk, then checks whether assistant text/thinking **after the first read-like event** echoes them. Anti-false-positive: the anchor is the first *read-like* event — a write-only session echoing its own just-written content does not count (skipped sessions reported in `sessions_touch_but_no_read`). Caveat: a doc consumed via `bash cat` (not the read tool, not a grep naming the doc) is invisible to the anchor — treat echo as confirmatory, and combine with matrix READ counts.

## Evidence ladder (strongest last)

1. **Touch** — target substring in any tool args (could be mention or maintenance)
2. **Read-like with result** — read-classified call, non-empty toolResult
3. **Echo** — assistant reasoning after a read-like event contains distinctive doc tokens
4. **Action follows the rule** — project-specific; the escape check tests its contrapositive

## Deliverable contract

1. The matrix table (verbatim, with file count and sessions-dir stated)
2. Escape-rate result bucketed by adoption date (when run)
3. For each deletion candidate: echo verdict + the actual echoed-token evidence
4. A recommendation per target: keep (load-bearing) / merge / delete / defer-with-retest-condition (e.g. "designed for a campaign that hasn't started — re-test after it runs")

**Done when**: matrix presented, every `only-maintained` target echo-checked, every target carries a verdict and recommendation.

## Companion skills

- Trace format questions (toolCall/toolResult shapes, entry structure) → `tool-call-extract`'s `references/session-jsonl.md`
- Deciding what to do with a confirmed-dead doc (merge into AGENTS.md vs delete) → the project's own domain docs, not this skill

## Done when

- [ ] Matrix presented with sessions-dir and file count
- [ ] Every `only-maintained` target echo-checked before a deletion recommendation
- [ ] Every target has a verdict and a recommendation
