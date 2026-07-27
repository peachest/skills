# Report Template

The report `fix-plan-<ID>.md` produced by Step 7 of `/fix`.

## Summary table

```markdown
# Review Fix Plan — <ID>

Source: <MR/PR/session>
Branch: <branch>

## Summary

| Verdict | Count | Priority spread |
| ------- | ----- | --------------- |
| ✅ TP   | N     | 🚨 x / ⚠️ x / 🟢 x |
| ❌ FP   | N     | — |
| 🟡 Edge | N     | — |
| 🔵 OOS  | N     | — |
| ⏸️ Q    | N     | — |
```

## Per-finding detail

### ✅ True Positive

Each TP carries a **status** (not a verdict — the verdict stays ✅ TP):

| Status | Mark | Meaning |
| ------ | ---- | ------- |
| Fixed | ✅ | Build + tests pass after the fix |
| Fix failed | ❌ | Build or tests fail; failure output documented |

```markdown
#### #1 <issue summary>
- **File**: `path/file.go:123`
- **Verdict**: ✅ 🚨
- **Fix plan**: <what was changed>
- **Risk**: <affected callers>
- **Status**: ✅ Fixed / ❌ Fix failed
```

### ❌ False Positive

```markdown
#### #1 <issue summary>
- **File**: `path/file.go:456`
- **Verdict**: ❌ FP
- **Reason**: <why it's not a problem>
- **ADR**: docs/adr/0003-xxx.md (if applicable)
```

### 🟡 Edge

```markdown
#### #1 <issue summary>
- **File**: `path/file.go:789`
- **Verdict**: 🟡 Edge (vendor)
- **Action**: Skipped + FIXME / Fixed / Reclassified as FP
```

### 🔵 Out of Scope

```markdown
#### #1 <issue summary>
- **File**: `path/file.go:101`
- **Verdict**: 🔵 OOS
- **Note**: Pre-existing code, not part of this change
```

### ⏸️ Question

```markdown
#### #1 <issue summary>
- **File**: `path/file.go:202`
- **Verdict**: ⏸️ Question
- **Uncertainty**: <what needs clarification>
```

## Checkpoint brief

A condensed version for display at confirmation checkpoints:

```markdown
### Verdict Summary

| Verdict | Count | Priority |
| ------- | ----- | -------- |
| ✅ TP   | N     | 🚨 x / ⚠️ x / 🟢 x |
| ❌ FP   | N     | — |
| 🟡 Edge | N     | — |
| 🔵 OOS  | N     | — |
| ⏸️ Q    | N     | — |

### ✅ True Positives (by priority)

#### 🚨 #1 file.go:29 — <one-line summary>
- Plan: <fix plan>
- Risk: <impact>

#### ⚠️ #2 server.go:46 — <one-line summary>
...
```

High (🚨) first, then medium (⚠️), then low (🟢).
