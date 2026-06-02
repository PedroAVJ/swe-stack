---
name: coverage-pass
description: "Compatibility mode for Symphony Requirements Elicitation. Use when Pedro asks whether stakeholder input, bugs, requirements, or meeting/chat follow-ups are covered in Linear/docs; report coverage gaps first and mutate Linear only when Pedro asks to fix coverage."
metadata:
  author: Pedro
  origin: local-self-authored
  source: hand-written
  provenance: not-openai-curated-not-plugin
---

# Symphony Coverage Pass

Coverage pass is now a mode of `requirements-elicitation`.

Use it when Pedro asks:

- "Are we missing anything?"
- "They sent requirements; make sure we have issues."
- "Cover the bugs from this chat in Linear."
- "Make sure every action-shaped thing has somewhere to live."

## Workflow

1. Read the relevant source of truth.
2. Extract only action-shaped items: bugs, requirements, data dependencies, and
   decisions.
3. Check existing Linear issues/comments/docs before creating anything.
4. Report covered, missing, deferred, and ignored items.
5. If Pedro asked to fix coverage, create/update the smallest useful Linear
   packet using `requirements-elicitation` rules.

Do not treat Linear as the full spec. Do not implement product code from this
skill.

## Output

```markdown
Coverage result:

- Covered already: ITEM -> ISSUE_OR_DOC
- Added comment: ITEM -> ISSUE
- Created issue: ITEM -> ISSUE
- Not tracked: ITEM -> reason

Remaining gaps:
- GAP -> recommended next action
```
