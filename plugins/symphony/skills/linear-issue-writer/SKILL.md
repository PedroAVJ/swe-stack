---
name: linear-issue-writer
description: "Internal/compatibility rules for writing grounded Linear issues from Symphony Requirements Elicitation. Use when Pedro explicitly asks to write/rewrite a Linear issue body, or when another Symphony skill needs concise issue-body policy."
---

# Symphony Linear Issue Writer

This skill is now the issue-body policy layer inside
`requirements-elicitation`. Prefer triggering requirements elicitation for
end-to-end source reading, discussion, Linear coverage checks, and approval.

## Issue Body Rules

- A Linear issue is a source-linked work packet, not a transcript summary or an
  implementation plan.
- Lead with the plain-English outcome and source pointers.
- Keep issue bodies concise enough that the implementation agent must reread the
  source before planning.
- Add `Scope` and `Out of scope` whenever adjacent work appears in the same
  source.
- Include visual evidence disposition when screenshots/photos/PDFs contain
  marked fields or annotations.
- Add `Pedro-reviewed specification` only when Pedro explicitly approves exact
  wording or constraints as his spec.
- Do not add architecture, file-level steps, acceptance criteria, test plans, or
  PR sequencing unless Pedro explicitly asks.

## State Rules

- `Todo`: approved for implementation or dispatch.
- `Backlog`: captured for later or review buffer.
- `Needs Info`: real blocker or unclear requirement.
- `Done` / `Canceled` / `Duplicate` / `Obsolete`: only after checking current
  status and overlap.

## Active Work Boundary

Before materially rewriting an existing issue, check for an active worker,
thread, branch, worktree, or PR. If work already started, report that the
implementation prompt is stale and use `implementation-dispatch` for a clean
restart only after Pedro approves.
