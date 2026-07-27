# Classification

The verdict definitions and decision tree for `/fix`. Consulted during Step 2 (recommend) and Step 3 (verify).

## Verdicts

### ✅ TP — True Positive

A real defect in the code introduced or touched by this change. The finding accurately describes a problem that should be fixed.

- **Action**: Fix (after grill).
- **Priority**: 🚨 high (security, crash, data loss) / ⚠️ medium (logic error, race condition) / 🟢 low (cleanup, docs, minor style).
- **Required fields**: `fix_plan`, `priority`.
- **`resolved`**: false by default (stays open for tracking until fixed).

### ❌ FP — False Positive

The finding is wrong. Either the code is correct and the bot misread it, or the "defect" is an intentional design decision.

Sub-types:

- **Design intent** — the code does this on purpose. Check `docs/adr/` for a supporting ADR. If no ADR exists but the design is clearly intentional, record the design intent as the reason.
- **Already fixed** — the code has been refactored since the finding was posted; the issue no longer exists.
- **Misjudgment** — the bot misunderstood the code. The logic is correct as written.

- **Action**: Skip.
- **Required fields**: `reason`.
- **Optional fields**: `adr` (link to supporting ADR).
- **`resolved`**: true (close it).

### 🟡 Edge — Real but Low Priority

The finding identifies a real issue, but it's low priority: vendor code, prototype code, style nit, or a minor improvement that isn't worth the risk of changing in this MR.

Sub-types:

- **Vendor** — third-party code, not maintained here.
- **Prototype** — experimental code that will be replaced.
- **Style** — readability or style suggestion, not a defect.

- **Action**: Optional fix (user chooses).
- **Required fields**: `reason`.
- **`resolved`**: false by default.

### 🔵 OOS — Out of Scope

The cited code is pre-existing — not part of this MR/PR's diff. The finding may be valid, but it shouldn't be fixed here.

- **Action**: Skip.
- **Required fields**: `reason`.
- **`resolved`**: true (close it).

### ⏸️ Question — Cannot Determine

Not enough information to classify. The finding is ambiguous, the code path is unclear, or the fix might have side effects that need team discussion.

- **Action**: Pause. Present the uncertainty to the user.
- **Required fields**: `reason` (what's uncertain).
- **`resolved`**: false (stays open).

## Decision tree

Walk down the list in order. First match wins.

1. **Is the cited line in this MR/PR's diff?**
   - No → 🔵 OOS (pre-existing code)

2. **Can you confirm or refute the finding?**
   - Cannot determine → ⏸️ Question

3. **Is the cited code vendor/third-party?**
   - Yes → 🟡 Edge (vendor)

4. **Is the cited code a prototype/experimental?**
   - Yes → 🟡 Edge (prototype)

5. **Has the code been refactored since the finding was posted?**
   - Yes, the issue is gone → ❌ FP (already fixed)

6. **Is there a design decision that explains the "defect"?**
   - ADR in `docs/adr/NNN-xxx.md` → ❌ FP (design intent, cite the ADR)
   - No ADR but clearly intentional → ❌ FP (design intent, explain)

7. **Is the finding about style/readability, not a defect?**
   - Yes → 🟡 Edge (style)

8. **Does the finding describe a real defect?**
   - Yes → ✅ TP (assign priority)

## Priority assignment

For ✅ TP findings, assign priority based on impact:

| Priority | Mark | Criteria |
| -------- | ---- | -------- |
| High | 🚨 | Security vulnerability, crash, data loss, panic |
| Medium | ⚠️ | Logic error, race condition, resource leak, incorrect behavior |
| Low | 🟢 | Cleanup, documentation, minor style, non-blocking improvement |

When unsure between two levels, pick the higher one — it's safer to over-prioritize a real defect than to bury it.
