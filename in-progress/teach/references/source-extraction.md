# Source Extraction Reference

Reference for the Source Extraction workflow in SKILL.md. Read when doing code
archaeology, adjudicating a paper-vs-code divergence, or writing/validating a
source anchor. Definitions only — the steps live in SKILL.md; layer
arbitration order lives in the okb skill.

## Anchor formats

Every claim carried from a source layer into a lesson cites its origin in one
of three anchor shapes:

| Layer | Anchor | Example |
|---|---|---|
| paper | `tex:<line>` | `tex:287` |
| code | `<commit>:<file>:<line>` | `2320d52:eagle/model/choices.py:1` |
| interpretation | article locator (id + paragraph/figure) | `p/839661630#fig2` |

Rules that apply across all three:

- **Figure numbers cite the local tex, verbatim.** Different published
  versions of the same paper renumber figures; the lesson's "Fig. 7" must be
  the local `source/` copy's "Figure 7". Verify by grepping the tex for the
  literal caption before citing the number.
- **A code anchor pins a commit.** Repositories evolve; a bare
  `file:line` without a commit hash describes a moving target. Clone with
  full history (`--unshallow` before archaeology — a shallow clone hides the
  commit a historical claim needs).
- **An interpretation anchor names the article, not the platform.** The
  locator must survive the article being re-fetched or mirrored; platform
  chrome (layout, section index) is not stable across mirrors.
- **Anchors are verbatim-checkable.** A fact-check pass re-reads the cited
  line and expects the quoted claim there. Write anchors you would accept
  being re-read.

## Code archaeology traps

Recurring failure shapes when extracting facts from a repository. Each was
hit in real sessions; the general form is listed so the next search starts
past it.

1. **Star-imported symbols hide consumption.** A symbol may be defined in
   one file and consumed everywhere via `from x import *` — grep for the
   symbol across the repo, never just the defining file, and grep the import
   lines to find the consumers.
2. **A variable is not a file.** Searching by identifier with
   `find -name "*foo*"` misses a variable defined inside a module. Locate
   definitions with grep over contents, not filename search.
3. **Misspelled identifiers break grep.** A function named with a typo
   (`genrate` for `generate`) is invisible to correctly-spelled searches.
   When a symbol fails to resolve, grep a fragment of it (4-5 chars) rather
   than the full word.
4. **Near-duplicate files double every hit.** Variant copies (`cnets1.py`
   beside `cnets.py`, a `testbug/` scratch dir) return search results from
   dead code. Determine which file production actually imports before
   reading any hit.
5. **Dead entry points masquerade as configuration.** A CLI flag or
   constructor argument that exists but is never read (a flag with a default
   that no caller overrides, an import no module reaches) describes nothing
   about runtime behavior. Confirm consumption: grep the symbol repo-wide
   and check the consumers are on the live import path.
6. **Defaults live on three tiers.** A "hardcoded" value may be the
   constructor default, the config file value, or the CLI default — three
   different numbers for the same knob, and all three can differ from what
   production uses. When citing a config value, name the tier:
   code-default, config-file, or invocation-CLI.
7. **History and HEAD are different systems.** A repo's current source may
   have removed what an earlier version relied on. Claims about "how it
   worked" at a named era need the commit that era maps to — use `git log`
   archaeology and cite the commit, not HEAD.

## Divergence patterns: labeling paper-vs-code

Four shapes recur when paper text and released code disagree. The label goes
in the lesson next to the claim, so the learner can see which authority the
statement rests on.

1. **Paper silent → code arbitrates.** The paper omits a concrete detail
   (a topology, a threshold) that the lesson needs. State the fact with the
   code anchor and note the paper carries no specific claim. Resolve this at
   extraction time, not during fact-check — an unanchored number written
   early becomes a defended position later.
2. **Implementation differs from the paper's description.** The code does
   X where the paper describes Y (a simplified knob shared between two
   parameters, an acceptance rule that skips a textbook step). Label the
   lesson text as *implementation difference* and describe what the code
   does; do not silently harmonize the lesson to the paper.
3. **Historical implementation vs current HEAD.** The behavior existed in
   one era and was removed or replaced later. Write both layers — "in the
   <era> design X; as of <commit/era>, Y" — and cite the commit for each.
   A single-layer description is wrong for whichever era the reader checks.
4. **Same name, different object.** An identifier inherited between
   projects names different structures in each (a tree config of the same
   name with different node counts). State both, with each side's anchor,
   before drawing any comparison.

**Recorded ruling.** Whichever pattern applies, the resolution is one line
in the fact base (ruling + anchors + which layer won), produced with the
OKB arbitration order (see the okb skill). The lesson then carries the
outcome — the ruling itself stays in the fact base, not in learner-facing
text.
