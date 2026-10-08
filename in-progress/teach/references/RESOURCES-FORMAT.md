# RESOURCES.md Format

`RESOURCES.md` is the single interface into OKB for this topic. **Knowledge** entries point into OKB notes (`gold/` when available, `silver/` otherwise) — knowledge for lessons is drawn from those notes, not from parametric guesses. **Wisdom** entries keep community links.

## Structure

```md
# {Topic} Resources

## Knowledge

- [Periodisation fundamentals](../../okb/gold/strength-training/periodisation.md)
  How programming and adaptation interact. Use for: periodisation, recovery, intensity zones.
- [Volume landmarks](../../okb/gold/strength-training/volume-landmarks.md)
  Weekly set targets per muscle group, from the evidence. Use for: programme design.

## Wisdom (Communities)

- [r/weightroom](https://reddit.com/r/weightroom)
  High-signal subreddit, moderated against bro-science. Use for: programme critique, plateau troubleshooting.
- Local: Tuesday strength class at {gym name}
  Use for: real-time coaching feedback on lifts.
```

## Rules

- **Knowledge points into OKB.** Each Knowledge entry is a relative pointer to an OKB note (`okb/gold/...` when verified, `okb/silver/...` otherwise). The note carries sources and verification; the pointer carries one line on what it covers and when to reach for it.
- **Wisdom stays high-trust.** Prefer communities with strong moderation. If a community is marketing dressed as education, leave it out.
- **Annotate every entry.** A bare pointer is useless in three months. Add one line: what it covers and when to reach for it.
- **Group by Knowledge / Wisdom.** Knowledge = OKB pointers; Wisdom = community links. It is fine for a resource to appear in only one group.
- **Surface gaps explicitly.** When a mission needs knowledge that OKB does not yet hold, write a `## Gaps` section listing it, then run OKB curation to fill it and point at the new note.
- **Prune ruthlessly.** A note that turned out wrong, shallow, or off-mission should be removed from OKB, and its pointer dropped here. Better five sharp notes than thirty mediocre ones.
- **Record community preferences.** If the user has opted out of joining communities, note it here so future sessions don't keep proposing them.
