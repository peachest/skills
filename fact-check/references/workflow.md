# Fact-Check Workflow

Step-by-step agent instructions for the 8-phase pipeline.

---

## Phase 0: Init

**Goal:** Determine run mode, create run directory, detect subagents.

### Steps

1. **Run init.sh:**
   ```bash
   init_json=$(bash scripts/init.sh "<user-provided-path>")
   ```
   Parses git remote/branch, document key (`/→--`), mode (full/incremental), is_directory.

2. **Parse output** into variables: `document_key`, `mode`, `repo`, `session_tag`, `is_directory`.

3. **If is_directory=true:** scan direct child `*.md` files. Each gets its own independent run.
   - Read `prompts/extract-claims.md` — hold it in memory for Phase 1.
   - Auto-detect extension types: scan document for keywords (`$/user→pricing`, `FedRAMP→compliance`, `/api/→route`, `:8080→port`). If found, prepend extension types to the extraction prompt type list.

4. **Detect subagents:**
   ```
   subagent({ action: "list" })
   ```
   → Map to capabilities: extract_worker, web_searcher, model_alt.
   → Record in run.json `capability_map`.

5. **Create run directory and run.json:**
   ```
   fact-check/run-YYYYMMDD-HHMMSS-{session_tag}/
   └── run.json
   ```
   run.json fields: `session_tag`, `mode`, `repo`, `document_key`, `documents`, `started_at`, `subagents_available`, `capability_map`.

6. **Incremental mode** — if mode=incremental:
   - Read `documents/<key>/claims.json` for old claims
   - Run `git diff --unified=0` → hunk ranges
   - Claims whose source_location falls outside all hunks → carry forward
   - Verify carry-forward claims with content_hash → mismatch → add to re-extract queue
   - Claims in changed hunks → add to re-extract queue

**Output:** run.json exists, `fact-check/documents/<key>/` dir ready.

---

## Phase 1: Extract

**Goal:** Extract all verifiable claims from the document using LLM + locate-claim + check-atomicity + validation loop.

### Steps

1. **Pre-extract with mdq** (if available):
   ```bash
   mdq --output json '# *' <doc>    # chapter structure → chunk boundaries
   mdq --output json '[]()' <doc>   # all links → inject into prompt as anchor
   mdq --output json '```' <doc>     # code blocks → code-api claim anchors
   ```
   If mdq unavailable: chunk by line count (~100 lines per chunk).

2. **Chunk document:** split by chapter headings. Large chapters (>100 lines or >4000 tokens) split by paragraph.

3. **LLM extracts claim_text only** — for each chunk:
   - Read `prompts/extract-claims.md` + chunk content
   - LLM outputs claim_text + type + expected_verifier (NO source_location, NO content_hash)
   - **Parallel mode:** if subagents available, dispatch chunks to workers (≤4 concurrency, fresh context)

4. **locate-claim: deterministic positioning** — for each claim_text:
   ```bash
   result=$(bash scripts/locate-claim.sh "<claim_text>" <source-doc>)
   ```
   - `ok: true` → claim gets `source_location` + `content_hash` ✅
   - `error: TEXT_NOT_FOUND` → agent sees `closest_match`, fixes claim_text, retries (max 3)
   - `error: AMBIGUOUS` → short text (≤20 chars) found at multiple locations → agent disambiguates

5. **check-atomicity: decomposition check** — for each claim_text:
   ```bash
   result=$(bash scripts/check-atomicity.sh "<claim_text>")
   ```
   - `match: true` + `sub_items.length > 1` → agent generates sub_claims[] (derived, no locate-claim needed)
   - `match: true` + `sub_items.length == 1` → no decomposition needed
   - `match: false` + `word_count > 25` → mark `compound_flag: "compound_embedded"`
   - `match: false` + `word_count <= 25` → atomic, proceed

6. **Write initial claims.json:**
   ```
   fact-check/documents/<key>/claims.json
   ```
   Claims now have `source_location` + `content_hash` from locate-claim, `decomposition_mode` from check-atomicity.

7. **Validation loop** (max 3 rounds):
   ```bash
   validation=$(bash scripts/validate-claims.sh documents/<key>/claims.json <source-doc>)
   ```
   - A (JSON syntax), B (schema), C1/C2/C3 (location/text/hash), D (atomicity verification only — no enforcement)
   - If `failed > 0` and `retry_count < max_retries`: feed failed claims + errors to LLM for targeted fix
   - If `failed > 0` after 3 rounds: write `validation_errors.json`, continue with partial claims

**Output:** `fact-check/documents/<key>/claims.json` containing all extracted claims with deterministic source_location and content_hash.

---

## Phase 2: Classify

**Goal:** Route each claim to the correct verifier (rule engine / web search / REFUSED / INFERRED).

### Steps

1. **Run route-claims.sh:**
   ```bash
   route_result=$(bash scripts/route-claims.sh documents/<key>/claims.json references/regex-rules.json)
   ```
2. Parse stats: authority_hit, judgment_refused, judgment_community, judgment_hedging, interpretation, unmatched.
3. Each claim now has `route`, `matched_verifier`, `matched_rule` fields.
4. Unmatched claims get LLM fallback based on `expected_verifier`.

**Output:** claims.json updated in-place with routing fields (`route`, `matched_verifier`, `matched_rule`). Script also prints stats JSON to stdout.

---

## Phase 3a: Rule Engine

**Goal:** Deterministic verification of authority claims (arXiv IDs, DOIs, URLs, packages, etc.).

### Steps

1. **Run rule-engine.sh:**
   ```bash
   bash scripts/rule-engine.sh documents/<key>/claims.json --repo <owner/repo>
   ```
2. Claims routed to `rule_engine` get `verdict`, `evidence`, `evidence_url`, `checked_at`.
3. Failed verifications after 2 retries → UNVERIFIABLE.
4. claims.json updated in-place.

**Output:** Authority claims in claims.json now have verdicts.

---

## Phase 3b: Triage

**Goal:** Use alt-provider LLM to assess confidence on web_search claims, skipping confident ones.

### Steps

1. Filter claims where `route == "web_search"` and no verdict yet.
2. If subagent model_alt available: dispatch batches (≤2 concurrency) to alt-model delegate.
3. If not available: skip Phase 3b, all claims proceed to Phase 5.
4. CONFIDENT → triage-escaped (skip Phase 5), UNCERTAIN/SUSPECT → proceed to Phase 5.
5. Write `triage_results.json` to run dir, update claims.json with `triage_result`.

**Output:** triage_results.json, claims.json updated.

---

## Phase 4: Checkpoint 🛑

**Goal:** Show user the claim partition and get confirmation before expensive search.

### Steps

1. Reload claims.json (user may have edited it).
2. Display partition:
   - **[Rule Engine Verified]** — claims with verdicts from Phase 3a
   - **[Triage-Escaped]** — CONFIDENT claims, skipped search
   - **[Needs Deep Search]** — UNCERTAIN/SUSPECT claims
   - **[Compound Embedded]** — claims with compound_flag
   - **[INFERRED]** — interpretation claims

3. **Skip threshold:** ≤3 claims + all SUPPORTED → auto-skip checkpoint.
   **Force break:** severity:high + CONTRADICTED → must show.

4. **User commands:**
   - `y` → continue to Phase 5
   - `n` → abort
   - `skip C001` → skip specific claim
   - `view C001` → show claim detail
   - `search C001` → override triage, force into Phase 5
   - `edit C001` → allow manual edit

**Output:** User decision recorded. claims.json re-read before Phase 5.

---

## Phase 5: Deep Verify

**Goal:** Web search + cross-validation for remaining claims.

### Steps

1. Group claims into batches (4-5 claims/batch).
2. **Parallel search:**
   - Subagent mode: dispatch batches to web_searcher agents (≤4 concurrency, fresh context)
   - CLI fallback: `anysearch batch_search` inline
3. Per batch: write `verify-batch-{N}.json` to run dir.
4. **Grade evidence:**
   ```bash
   cat verify-batch-*.json | bash scripts/grade-evidence.sh
   ```
   → Adds evidence_tier, confidence, staleness_warning.
5. Cross-validation: multi-source agreement → high confidence. Conflict → NUANCED/CONTRADICTED.
6. Update claims.json with final verdicts.

**Output:** verify-batch-*.json, claims.json updated.

---

## Phase 6: Write

**Goal:** Generate all output files.

### Steps

1. **Run generate-report.sh:**
   ```bash
   bash scripts/generate-report.sh documents/<key>/claims.json run.json <run-dir>
   ```
2. **Outputs:**
   - `report.md` — Summary table + grouped claim cards
   - `handoff.md` — CONTRADICTED/NUANCED claims with machine-readable markers
   - `documents/<key>/ledger.jsonl` — append new verdict rows
   - `fact-check/total-stats.json` — cumulative stats updated
   - `run.json` — completed_at, total_claims, verdict_distribution

**Output:** All Phase 6 files written.

---

## Phase 7: Deliver

**Goal:** Show summary and offer fix options.

### Steps

1. Display verdict distribution table with icons.
2. Show counts: Items to fix, Needs attention, Carried forward.
3. Offer choices:
   - **[A] Agent auto-fix** — agent edits source document for CONTRADICTED claims
   - **[M] Manual fix** — output checklist, user handles offline
   - **[V] View report** — open report.md, can switch to A/M anytime

**Output:** User choice recorded.

---

## Phase 8: Fix 🛑

**Goal:** Apply corrections to source document.

### A Path (Agent Fix):
1. For each CONTRADICTED claim: show claim, evidence, suggested fix.
2. User confirms each edit (`y/n`).
3. Edit source document in-place.
4. Update claims.json status: extracted → revised → rechecked.
5. Append fix to ledger.jsonl.

### M Path (Manual):
1. Output checklist of all items to fix.
2. Next run (incremental) will naturally re-check.

### Dispute Path:
1. User marks in handoff.md: `verdict wrong, counter evidence: <url>`.
2. Next run reads handoff → appends overriding vid to ledger.

**Output:** Source doc edited (A path), ledger updated.
