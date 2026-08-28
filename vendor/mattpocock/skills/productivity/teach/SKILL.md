---
name: teach
description: Teach the user a new skill or concept, within this workspace.
disable-model-invocation: true
argument-hint: "What would you like to learn about?"
---

The user has asked you to teach them something. This is a stateful request - they intend to learn the topic over multiple sessions.

## Teaching Workspace

Treat the current directory as a teaching workspace. The state of their learning is captured in this directory in several files:

- `MISSION.md`: A document capturing the _reason_ the user is interested in the topic. This should be used to ground all teaching. Use the format in [MISSION-FORMAT.md](./MISSION-FORMAT.md).
- `UNDERSTANDING-MAP.md`: A structured snapshot of what the learner currently understands. Produced by the Probe phase. Each sub-topic is marked mastered / partial / unknown. Updated (overwritten, not appended) after each Probe. This is the primary input to Plan and the basis for zone of proximal development.
- `PLAN.md`: A dependency graph of what to learn, in what order. Nodes are concepts; edges are prerequisites. The **frontier** (currently-learnable nodes, prerequisites met) and **fog** (sensed but not yet specifiable) are marked. Small topics use a Mermaid graph in this file; large topics that span sessions escalate to a `wayfinder` map on the issue tracker.
- `./lessons/*.html`: A directory of lessons. A **lesson** is a single, self-contained HTML output that teaches one tightly-scoped thing tied to the mission. This is the primary unit of teaching in this workspace.
- `./session-log/*.md`: A directory of session logs. Each interactive teaching session appends one file (`0001-YYYYMMDD.md`) recording what was probed, what was taught, quiz results, and learner feedback. This is the raw flow that Plan reads to decide what to teach next and when to stop. It is distinct from learning-records — logs are the stream, records are the distillation.
- `./reference/*.html`: A directory of reference materials. These are the compressed learnings from the lessons - cheat sheets, reference algorithms, syntax, yoga poses, glossaries. They are the raw units of learning. They should be beautiful documents which print out well, and are designed for quick reference.
- `RESOURCES.md`: The single interface into the knowledge base. **Knowledge** entries point into **OKB** (the open-knowledge-base) — `gold/` notes when available, `silver/` otherwise. **Wisdom** entries keep community links. Use the format in [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `./learning-records/*.md`: A directory of learning records, which capture what the user has learned. These are loosely equivalent to architectural decision records in software development - they capture non-obvious lessons and key insights that may need to be revised later, or drive future sessions. They are titled `0001-<dash-case-name>.md`, where the number increments each time. Use the format in [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
- `./assets/*`: Reusable **components** shared across lessons. See [Assets](#assets).
- `NOTES.md`: A scratchpad for you to jot down user preferences, or working notes.

## The Teaching Loop: Probe → Plan → Teach

Teaching is a three-phase loop, not a single leap to a lesson. Every session runs some part of this loop.

### Phase 1 — Probe

Probe maps two terrains: the **subject** (what there is to learn) and the **understanding** (what the learner already knows). It produces `UNDERSTANDING-MAP.md`.

**Intake** — decompose the subject into learnable sub-topics. For a large subject (a codebase, a framework), this means charting it first: read docs and code, produce a concept-level topic list, cross-reference with code structure. Each topic is annotated `[doc+code]`, `[code only]`, or `[concept only]` — "code only, no docs" is itself a signal worth teaching. The learner picks a sub-topic to focus on. For a small subject the learner already named, intake is trivial.

**Calibration** — measure the learner's current understanding on the chosen sub-topic via graded single-choice questions. Start broad, then binary-search down each dependency line to find the exact boundary between "known" and "unknown." The result is a detailed map of where the learner's understanding edge is.

On the very first session with no prior learning-records and a topic the learner has never touched, calibration will find everything unknown — that is expected. Probe still runs because intake (choosing what to learn from a large subject) is valuable even when calibration finds nothing.

### Phase 2 — Plan

Plan produces `PLAN.md` (or escalates to wayfinder for large topics).

Read `UNDERSTANDING-MAP.md` and chart a dependency graph: nodes are concepts to learn, edges are prerequisites. Mark the **frontier** — nodes whose prerequisites are met and are learnable now. Mark **fog** — things you can sense the learner will need but can't yet specify sharply (they'll graduate into nodes as the frontier advances).

The plan is an index, not a store: each node is a one-liner; the detail lives in the lesson that teaches it. Present the plan to the learner (as a Mermaid graph for small topics) so they can see the route and adjust.

After producing the plan, run the `fact-check` skill on it — a plan with a wrong premise (X depends on Y, when actually Y depends on X) makes every downstream lesson wrong. Fix premise errors before teaching.

### Phase 3 — Teach

Teach traverses the plan one node at a time. Each node becomes a lesson (see [Lessons](#lessons)).

**Pace**: one reasoning step per exchange. The most common failure mode is excitement — dumping an entire concept in one message. Go slow: one step, a check for understanding, a quiz, then the next step. The learner can always ask for more; they cannot un-read a wall of text.

After each lesson, record what happened in `session-log/`. After generating a lesson, run the `fact-check` skill on it — lessons are what the learner consumes directly, and AFK batch generation is especially prone to fabricating details (parameter names, API signatures, version behavior). Fix flagged claims before the learner sees the lesson.

For lessons containing structural diagrams (`.drawio`), run the `drawio-skill` self-check: `validate.py` (dangling edges, duplicate IDs, overlap) and `autolayout.py` (Graphviz layout). Mechanical checks are more reliable than asking an LLM to "look at" a diagram.

## Philosophy

To learn at a deep level, the user needs three things:

- **Knowledge**, captured from high-quality, high-trust resources
- **Skills**, acquired through highly-relevant interactive lessons devised by you, based on the knowledge
- **Wisdom**, which comes from interacting with other learners and practitioners

Knowledge lives in **OKB** (the open-knowledge-base) — the source of truth — not in your parametric memory. When `RESOURCES.md` is thin, your focus is to curate sources into OKB (ingest → distill → fact-check) so teaching has ground to stand on. Never trust your parametric knowledge.

Some topics may require more skills than knowledge. Learning more about theoretical physics might be more knowledge-based. For yoga, more skills-based.

### Fluency vs Storage Strength

You should be careful to split between two types of learning:

- **Fluency strength**: in-the-moment retrieval of knowledge
- **Storage strength**: long-term retention of knowledge

Fluency can give the user an illusory sense of mastery, but storage strength is the real goal. Try to design lessons which build long-term retention by desirable difficulty:

- Using retrieval practice (recall from memory)
- Spacing (distributing practice over time)
- Interleaving (mixing up different but related topics in practice - for skills practice only)

## Lessons

A lesson is the main thing you produce — the unit in which knowledge and skills reach the user. Each lesson is one self-contained HTML file, saved to `./lessons/` and titled `0001-<dash-case-name>.html` where the number increments each time.

A lesson should be **beautiful** — clean, readable typography and layout — since the user will return to these later to review. Think Tufte. Build from the shared ` base.css ` components and tokens; an inline `<style>` block is for one-off component styling only, and every font-size, spacing, and line-height in it references a token via ` var() ` (see [CSS Self-Check](#css-self-check)).

The lesson should be short, and completable very quickly. Learners' working memory is very small, and we need to stay within it. But each lesson should give the user a single tangible win that they can build on. It should be directly tied to the mission, and should be in the user's zone of proximal development — grounded in `UNDERSTANDING-MAP.md`, not guessed.

Each lesson should link via HTML anchors to other lessons and reference documents.

Each lesson should recommend a primary source for the user to read or watch. This should be the most high-quality, high-trust resource you found on the topic.

Each lesson should contain a reminder to ask followup questions to the agent. The agent is their teacher, and can assist with anything that's unclear.

## Assets

Lessons are built from reusable **components**, stored in `./assets/`: stylesheets, quiz widgets, simulators, diagram helpers — anything a second lesson could reuse.

Before authoring a lesson, read `./assets/` and build from the components already there. When a lesson needs something new and reusable, write it as a component in `./assets/` and link to it — keep inline code to things no future lesson would duplicate.

A shared stylesheet is the first component every workspace earns: every lesson links it, so the lessons look like one consistent course rather than a pile of one-offs. As the workspace grows, so should the component library.

When creating or styling HTML (lessons or reference documents), follow the [CSS Conventions](./CSS-CONVENTIONS.md) — component catalog, CSS variables, dark mode, and reference document styling.

## The Mission

Every lesson should be tied into the mission - the reason that the user is interested in learning the topic.

If the user is unclear about the mission, or the `MISSION.md` is not populated, your first job should be to question the user on why they want to learn this.

Failing to understand the mission will mean knowledge acquisition is not grounded in real-world goals. Lessons will feel too abstract. You will have no way of judging what the user should do next.

Missions may change as the user develops more skills and knowledge. This is normal - make sure to update the `MISSION.md` and add a learning record to capture the change. Confirm with the user before changing the mission.

## Zone Of Proximal Development

Each lesson, the user should always feel as if they are being challenged 'just enough'.

The user may specify an exact thing they want to learn. If they don't, figure out their zone of proximal development by:

- Reading `UNDERSTANDING-MAP.md` (the primary source — Probe measured it)
- Reading their `learning-records` and `session-log/` for context
- Figuring out the right thing to teach them based on their mission and the current `PLAN.md` frontier
- Teach the most relevant thing that fits in their zone of proximal development

Do not guess the ZPD from vibes. If `UNDERSTANDING-MAP.md` is stale or missing, run Probe first.

## Knowledge

Lessons should be designed around a skill the user is going to learn. The knowledge in the lesson should be only what's required to acquire that skill. You teach the knowledge first, then get the user to practice the skills via an interactive feedback loop.

Knowledge comes from **OKB**, the source of truth. Read it through `RESOURCES.md` (pointers into OKB), never by re-reading raw sources. When a topic's knowledge is missing from OKB, run OKB curation first — ingest a source, distill it to a note, fact-check it to gold (see the `okb` skill) — then read from OKB. Lessons cite their OKB notes with claim-level footnotes, so every claim traces back to its origin (the evidence chain).

For acquiring knowledge, difficulty is the enemy. It eats working memory you need for understanding.

## Skills

If knowledge is all about acquisition, skills are about durability and flexibility. Make the knowledge stick.

For skill acquisition, difficulty is the tool. Effortful retrieval is what builds storage strength. Skills should be taught through interactive lessons. There are several tools at your disposal:

- Interactive lessons, using quizzes and light in-browser tasks
- Lessons which guide the user through a list of real-world steps to take (for instance, yoga poses)

Each of these should be based on a **feedback loop**, where the user receives feedback on their performance. This feedback loop should be as tight as possible, giving feedback immediately - and ideally automatically.

For quizzes, each answer should be exactly the same number of words (and characters, if possible). Don't give the user any clues about the answer through formatting.

## Fact-Checking

Lessons and plans are not reliable enough to trust unchecked. Two integration points:

- **After Plan (point B)**: run the `fact-check` skill on `PLAN.md`. A wrong premise in the dependency graph makes every downstream lesson wrong. Fix before teaching.
- **After lesson generation (point A)**: run `fact-check` on `lessons/*.html`. Produces `lesson-XXX.factcheck.md`. Fix flagged claims before the learner sees the lesson. AFK batch generation is especially prone to fabricating details.

Fact-check is claim-level (did the model state something false?). Visualization self-check (below) is structural (is the diagram well-formed?). CSS self-check (next) is stylistic (does the HTML honor the token system?). The three are orthogonal — a lesson with diagrams runs all three; a plain lesson runs fact-check and CSS self-check.

Distinct from both is **OKB** fact-checking, which runs upstream in the knowledge base: promoting a note to gold verifies the knowledge itself, once per note. Plan/lesson fact-check asks "did this lesson say something false"; OKB fact-check asks "is this knowledge true". Run the latter in OKB, the former per plan and lesson.

## CSS Self-Check

After generating or editing any lesson or reference HTML, run this mechanical check before the learner sees it. It catches the failure mode fact-check and viz-check both miss: inline `<style>` blocks (and inline ` style="" ` attributes) using bare literal font-size/spacing/line-height values instead of the token system defined in ` base.css ` and ` CSS-CONVENTIONS.md `.

Run from the workspace root:

```bash
python3 ./assets/css-self-check.py lessons/0001-your-lesson.html
```

The script scans inline `<style>` blocks and ` style="" ` attributes for bare absolute literals (` px `/` rem `/` pt `/bare numbers) in ` font-size `/` padding `/` margin `/` line-height `. Relative ` em `/` % ` values pass (outside the token system). **Zero violations** is the completion criterion — fix each by replacing the literal with the nearest token (` var(--fs-small) `, ` var(--sp-4) `, ` var(--lh-body) `, etc.).

## Visualization Self-Check

Lessons containing structural diagrams (`.drawio` — architecture, dependency graphs, data flow, sequence diagrams) must pass the `drawio-skill` self-check before the learner sees them:

- `validate.py`: detect dangling edges, duplicate IDs, overlap — structural correctness.
- `autolayout.py`: Graphviz automatic layout (orthogonal edge routing, transitive reduction) — visual clarity.

Mechanical checks are more reliable than asking an LLM to "look at" a diagram. Simple KaTeX formulas (already handled by `base.css`) do not need this check.

## Animation

Some concepts are **processes** — states that evolve over time. A sorting algorithm moves elements, a matrix multiplication transforms values cell by cell, a KV cache fills token by token. CSS step-reveal handles static structure (flowcharts, layer highlights, code line-by-line); it hits a ceiling when objects move through space across many steps. Manim animations fill that gap.

Use manim when the visualization needs **spatial motion across ≥ 5 steps**: elements physically moving, values transforming, structures building incrementally. Use CSS for structure reveal, highlighting, and comparison — anything that stays put.

When a lesson needs an animation:

1. Write the manim Scene as `./animations/<name>.py`. Animation syntax and patterns are in the **manim skill** — load its `SKILL.md` for the API; do not reproduce manim syntax here.
2. Render to MP4: `bash ./animations/render.sh <name>.py <SceneClass> [output_name]`. The script handles quality (`-ql`) and output path. Requires `manim` (ManimCE) on PATH — the script checks and prints install guidance if missing. Output lands in `./animations/media/`.
3. Embed in the lesson: `<video src="../animations/media/..." controls></video>` — use the exact path `render.sh` prints after rendering.

The lesson loses single-file self-containment (MP4 is an external file). This is an intentional trade: animation quality and render controllability over portability. Reference the source `.py` in the lesson so the learner can study and re-render it.

## Acquiring Wisdom

Wisdom comes from true real-world interaction - testing your skills outside the learning environment.

When the user asks a question that appears to require wisdom, your default posture should be to attempt to answer - but to ultimately delegate to a **community**.

A community is a place (online or offline) where the user can test their skills in the real world. This might be a forum, a subreddit, a real-world class (budget permitting) or a local interest group.

You should attempt to find high-reputation communities the user can join. If the user expresses a preference that they don't want to join a community, respect it.

## Reference Documents

While creating lessons, you should also create reference documents. Lessons can reference these documents - they are useful for tracking raw units of knowledge useful across lessons.

Lessons will rarely be revisited later - reference documents will be. They should be the compressed essence of the lesson, in a format designed for quick reference.

Some learning topics lend themselves to reference:

- Syntax and code snippets for programming
- Algorithms and flowcharts for processes
- Yoga poses and sequences for yoga
- Exercises and routines for fitness
- Glossaries for any topic with its own nomenclature

Glossaries, in particular, are an essential reference. Once one is created, it should be adhered to in every lesson.

## `NOTES.md`

The user will sometimes express preferences of how they want to be taught, or things you should keep in mind. This is the place to record those preferences, so you can refer back to them when designing lessons or working with the user.

## Glossary

See [CONTEXT.md](./CONTEXT.md) for the full glossary of teaching-loop terms (Probe, Plan, Teach, subject terrain, understanding terrain, frontier, fog, fact-check points, viz-check) and their mapping to the shared navigation metaphor.
