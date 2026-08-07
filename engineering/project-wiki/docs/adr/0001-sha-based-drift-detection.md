# SHA-based drift detection, not AST or git diff

Drift between code and wiki is detected by comparing each file's SHA1
against a stored baseline (`.review_cache.json`), refreshed explicitly by
`update`. We rejected two alternatives: git diff (only shows changes since
last commit, not since last wiki review — the two cadences are
independent) and AST-based structural comparison (language-specific,
fragile, and overkill — we need to know *that* a file changed, not *what*
changed inside it). SHA is language-agnostic, trivially portable, and
makes the review boundary explicit: the baseline is the snapshot at the
moment the human/AI said "I've looked at this."
