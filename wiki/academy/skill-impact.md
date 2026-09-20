# academy skill-impact

| Date | Proposal | Landing | Commit | Verification |
|------|----------|---------|--------|--------------|
| 2026-09-14 | Document topic-incubation flow (survey → research → split by direction → batch spawn → N/N receipts → close), distilled from first real run (session 01a09f4f, DeepSeek V1→V4.1 series, 6 courses); fix pane→tab convention in Course session protocol | in-progress/academy/SKILL.md: new "Incubate a topic" section + Create paragraph rewrite | 37937c2 | no tests in skill (exempt); reinstall via npx skills add; behavior verified against the source session trace (99 entries) |
| 2026-09-20 diagnose#1 | P-001 course-content boundary + documented correction path; P-002 drop `--wait` (receipts counted from injected messages) | in-progress/academy/SKILL.md: Roles bullet rewrite, Course session protocol bootstrap note, Incubate steps 6-7 | 3c9d7f4 | passCheck: post-close assistant output carries no course technical analysis; zero `herdr agent prompt --wait` calls |
