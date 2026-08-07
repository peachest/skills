---
name: to-backlog
description: >
  Append small tasks to the project backlog or mark them complete.
  The backlog is stored at `.scratch/backlog.md` alongside the epic/feature
  tree and contains unstructured, small-grain tasks that don't belong to any
  specific milestone or Feature. Use when user says "add to backlog" / 
  "put it in the backlog" / "记到 backlog" / "加到待办" / "mark this done" / 
  "check this off" / list backlog items.
  Do NOT write PRDs, epics, or issues — this skill only maintains the backlog.
---

# To Backlog — Zero-item Task Tracker

Maintain `.scratch/backlog.md` — a flat checklist of small tasks that are too
trivial for a Feature but still need tracking. Users add items on the fly and
mark them done incrementally.

## Process

### 1. Identify intent

The user will say something like:

- "把这个加到 backlog" / "put X in the backlog" — **append**
- "这个做完了" / "mark X done" — **check off**
- "看看 backlog 里还有什么" / "show me the backlog" — **list**

### 2. Before first append

If `.scratch/backlog.md` does not exist yet, ask the user what categories they
want. Suggest common ones based on the project (e.g. `## 测试`, `## 文档`,
`## 配置`, `## 代码重构`, `## 测试`).

Do not write the file until the user confirms the category list.

### 3. Append a task

Ask the user:

- Which category does this belong to? If the existing categories don't match,
  offer to create a new one.
- Does this relate to a specific Feature? (e.g. `modal-tui/modal-tui/feature.md`)
- Any implementation notes worth recording? (Keep it 1-2 sentences max.)

Then append to `.scratch/backlog.md`:

```markdown
- [ ] **<task title>**
  来源：用户 YYYY-MM-DD
  关联：<feature path, optional>
  备注：<notes, optional>
```

### 4. Check off a task

Read `.scratch/backlog.md`. Find the matching `- [ ]` line by title
(substring match, ignore case). Replace `- [ ]` with `- [x]`.

If ambiguous (multiple matches), list the candidates and ask which one.

If not found, ask: "I didn't find '{title}' in the backlog. Add it?"

### 5. List backlog

Read `.scratch/backlog.md` and present a summary:

- Pending items grouped by category
- Recently completed items (last 5 checked off, if any)
- Total counts per category

---

## Guiding principles

1. **One job — maintain the backlog.** Do NOT create feature.md, epic.md, PRD,
   or issue files.

2. **Quick append, simple confirm.** Ask the questions together in one message,
   not one at a time. The goal is < 2 rounds per interaction.

3. **Never duplicate.** Check existing entries before appending. If the same
   task already exists (same title, same category), tell the user.

4. **No line numbers.** Backlog.md is a living document — lines shift as items
   are checked off or added. Match by title text, not line position.