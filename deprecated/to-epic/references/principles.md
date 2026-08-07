# Guiding Principles

## One job — produce Epics and Features.

Do NOT group features into PRDs, write PRD documents, or slice issues. Each
step in the pipeline has a single responsibility.

## The user decides, you guide.

Never skip the milestone confirmation step. Present clearly; let the user steer.
Your role is to propose a well-structured decomposition, not to make decisions
for them.

## Derive, don't invent.

Scope and features should trace back to the input document. Flag when you need
to add something the document doesn't cover — that's a signal the document
may need an update.

## Keep feature.md lean.

No current-state analysis, no user-story-level lists — those belong in the PRD
step. feature.md's value is the scope confirmation gate, not the implementation spec.

## Leave a paper trail.

All outputs are persistent Markdown under `.scratch/`. Each feature directory
is ready for to-prd to fill in later. Don't inline decisions into the
conversation — write them down.