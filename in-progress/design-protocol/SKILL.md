---
name: design-protocol
description: "7-layer machine-readable design protocol (Token→Component→Direction→Scene→Page→Exhibition→Template) with JSON Schema gates, so AI-generated UI decisions are traceable and consistent instead of random. Use when authoring or validating design protocol files (设计协议/协议文件/design/protocol/), or when generating any UI in a project that has a design/protocol/ directory — load enabled layers as context and cite a protocol entry for every design decision. Complements impeccable (craft and review): this skill owns hard constraints."
---

# Design Protocol

A 7-layer machine-readable design protocol with JSON Schema gates. The protocol files are the source of truth; the agent generates UI inside the space they define, and every design decision cites a protocol entry.

## Discover

Look for `design/protocol/protocol.json` in the project.

- Found → note the `layers` map (which of L1–L7 are enabled), then run **Author** to extend or **Consume** to generate.
- Not found → STOP and ask the user whether to bootstrap one. Do not invent a protocol unprompted, and do not proceed as if constraints existed. Bootstrap is Author mode's step 1.

## Author mode (build or extend the protocol)

Layer files live in `design/protocol/<layer>/` — `tokens.json`, `components/*.json`, `direction.json`, `scene.json`, `page.json`, `exhibition.json`, `template.json`. Field specs and one worked example per layer: [reference/layers.md](reference/layers.md).

1. Bootstrap `protocol.json` if missing:
   ```json
   {"name": "<project>", "protocol": "design-protocol/0.1", "layers": {"L1": true, "L2": true, "L3": false, "L4": false, "L5": false, "L6": false, "L7": false}}
   ```
2. Build layers bottom-up, **only the layers the project needs**. Minimum set: L1 + L2. Enable L3 when the user can name a style intent; L4 when one direction behaves differently across business contexts; L5 when a page structure repeats; L6/L7 on explicit need. Update the `layers` map as you go.
3. L1 tokens use W3C DTCG format (`$type` + `$value`). L2 components declare their closed set: variants, props, constraints ("Button has sm/md/lg, no xl" is written down, not remembered).
4. Gate every write: `python3 <skill-dir>/scripts/validate.py design/protocol/` — schema violations mean the file is rejected; fix the file, do not relax the schema mid-task. A layer counts as done when its files pass validation AND it holds at least one real entry (no empty scaffolds).
5. Seeds for a first entry per layer: [templates/](templates/) — copy, fill with project values, validate.

Extract only patterns the project has used 3+ times with the same intent into the protocol; token values are edited in L1 only — upper layers reference, they do not copy values.

## Consume mode (generate UI under the protocol)

1. Load `protocol.json` and every enabled layer's files into context before generating anything.
2. Produce the UI with each design decision — color, spacing, component choice, page structure — traceable to a protocol entry, cited as `protocol:L<n>/<entry>`. Example: `protocol:L2/button#variant=secondary`, `protocol:L1/spacing.md`.
3. A decision with no protocol entry means the protocol is missing something: add the entry in Author mode (with validation), then use it. This closes the "AI felt like it" gap — the reason this skill exists.
4. Re-run `validate.py design/protocol/` after any protocol change made during generation.

Done when: the artifact ships, every decision carries a `protocol:` citation, and validation passes.

## Interface with impeccable

Both installed? `design/protocol/` is the constraint layer, impeccable's DESIGN.md the explanation layer. Tokens extracted by impeccable's extract flow enter the protocol through Author mode (re-keyed to DTCG `$type`/`$value`) — they are the same values, one source of truth. Run impeccable's craft/critique flows as usual; protocol citations replace none of that, they make decisions explainable afterwards.
