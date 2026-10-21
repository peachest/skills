# verdict.py — classified.json sole writer

Records one triage verdict into the MR's `classified.json`. The agent-facing
interface: a finding ordinal (`no`) from the pull state file plus the verdict
semantic fields. The script — never the agent — copies the full
`discussion_id` byte-exact from `.triage/<MR>/issues.json`, computes the body
anchor (`sha256(body)[:16]`), and appends or replaces exactly one schema-2
entry per invocation (atomic read-modify-write via tmp + `os.replace`).

## Invocation

```bash
python3 <SCRIPTS_DIR>/verdict.py <MR> <no> --class TP|FP|Edge|OOS|Q \
    --reason "..." [--fix-plan "..."] [--priority high|medium|low] \
    [--resolved true|false] [--force]
```

- `--class` stores `Q` in the state file; consumers normalize (`Q` → `Question`
  before consulting label/resolved maps).
- `--fix-plan` is required for TP.
- `--priority` is the string enum `high|medium|low`; consumed only for TP
  (other classes ignore it).
- `--force` replaces an existing entry (matched by `discussion_id` + anchor,
  never ordinal — ordinals reshuffle across pulls; the dedup key survives
  ordinal reshuffling and re-reports under new ids).

## Per-item `resolved` semantics (spec #57 Amendment R2, 修订 A)

The close-after-verification decision is made **at verdict time** and stored
per item — post only executes it:

| class | default | override |
|-------|---------|----------|
| Edge | `resolved: true` | `--resolved false` keeps it open |
| Q | open (field unset/false) | explicit `--resolved true` closes it |
| TP / FP / OOS | field unset | post applies its mode map (standalone /fix vs triage) |

## Feedback and exit codes

Success echoes `no` + author + first body line — check it against the finding
you meant before proceeding. Display discipline: the `discussion_id` never
reaches human-readable output (no full or truncated id shapes).

- `0` — recorded.
- `1` — state error: missing pull file, unknown `no` (stderr lists the valid
  range), existing verdict without `--force`, corrupt/non-schema-2 state files.
- `2` — usage error (argparse).

## Contract invariants

- `classified.json` schema 2: `{"schema": 2, "entries": [...]}`; entries carry
  `discussion_id` (byte-exact from pull), `no`, `anchor`, classification,
  reason, `fix_plan`, `priority`, `resolved`, `posted: false`.
- Sole writer of verdict semantic fields; `posted` is post's declared-exception
  write.
- Paths via `triage_state_dir()` (cwd/realpath, never `$HOME`).
