---
name: then-what
description: The user can see the options but can't predict what happens after choosing. Explore the real consequences of each option and re-present them as user stories.
disable-model-invocation: true
---

The user is staring at options you presented — A, B, C — and cannot tell what life looks like after picking each one. Your job is to make the consequences concrete.

For each option, **explore the real consequences** before writing anything. Read the code, check the docs, load `/skill:prototype` and build a throwaway if a behavior is uncertain. Do not write a story from assumptions — a story the user cannot trust is worse than the raw option list.

If exploration reveals an option is infeasible, or surfaces an option the original set is missing, **fix the option set first** — drop the dead one, add the missing one — then write stories for the corrected set. Do not present a story for an option you already know is broken.

Write one **user story** per option: a short narrative paragraph tracing the timeline after the choice — what happens next, what the user does, what they notice. Concrete and temporal, not abstract. Show cause and effect, not a trade-off table.

After the stories, give your **recommendation** — which option to pick, and why — then wait for the user's choice. When they pick, carry the answer back to wherever the options came from and continue.
