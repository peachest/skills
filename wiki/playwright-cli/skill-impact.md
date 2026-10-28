# skill-impact ledger — playwright-cli

| date | change | commit | verification |
|------|--------|--------|--------------|
| 2026-10-28 | Added "Ref & retry discipline" section (6 rules distilled from a cua-repl teardown article + live AX verification): refs are not persistent IDs / timeout ≠ action not applied / screenshot coords vs refs are independent systems / DOM-only pages have no named roles / tab-binding side effects / partial failure ≠ tool broken. | playwright-cli: add ref and retry discipline section | Live: AX snapshot + ref click verified end-to-end on an internal React SPA (login → navigate → table); rules cross-checked against Playwright locator/strict-mode/autowaiting semantics |
