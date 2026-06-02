---
name: symphony-issue-intake
description: "Use only when Pedro explicitly asks for a Symphony issue-intake pass over WhatsApp/meeting/email evidence to decide do-now work, create/update Linear issues, and report the intake result."
---

# Symphony Issue Intake

Use this skill for an explicit Symphony intake loop: "go read the source, make
the right Linear work, and tell me what happened."

## Repo-Specific Boundary

Repo implementation should not default to Symphony intake. For ordinary product
repo chats, meeting follow-ups, and implementation details, Codex should handle
the request directly with normal repo/source-of-truth workflow. Use this skill
for a product repo only when Pedro explicitly asks for a Symphony intake audit.

## Intake Rules

- Read the actual source-of-truth evidence before classifying.
- Keep "do-now" work separate from future-meeting topics.
- Ask for no clarification when the source and repo state are enough to decide.
- Use Backlog for review-needed issue drafts unless Pedro asks to move them to
  Todo.
- Use Todo only when the issue is implementation-ready and Pedro wants agents to
  pick it up.
- Cancel or mark obsolete cards that were only bookmarks, contaminated, or no
  longer implementable.

## Evidence To Issue Body

Issue bodies should include:

- Source type and exact source path/message IDs/recording links when available.
- Plain-English problem and expected behavior.
- Implementation scope and explicit non-goals.
- Files or modules likely involved when grounded in the repo.
- Caveats when a dependency is not currently implemented.

## After Creation Or Rewrite

- Report issue titles in plain English, with Linear IDs secondary.
- State current status: Backlog, Todo, Done, Canceled, Merging, etc.
- If an issue rewrite invalidates existing work, state the lifecycle boundary.
  Do not restart repo implementation work under Symphony unless Pedro explicitly
  asks for that separate coding task.
