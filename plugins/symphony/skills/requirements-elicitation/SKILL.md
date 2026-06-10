---
name: requirements-elicitation
description: "Use when Pedro wants Symphony to turn messy stakeholder input, WhatsApp messages, meeting/email evidence, screenshots, docs, or repo context into an agreed Linear work packet before implementation. This skill talks through meaning and scope first, creates/updates Linear only after approval, and does not write product code."
---

# Symphony Requirements Elicitation

Use this as Symphony's canonical first lane: messy source evidence in, clear
approved work packet out. Implementation happens later, usually through
`implementation-dispatch`.

## Contract

- Ground the requirement in the real source before interpreting it.
- Talk through what the requirement means and where the boundaries are.
- Create or update Linear only after Pedro approves the requirement or asks to
  capture it.
- Do not write product code, open a PR, merge, deploy, or mark work review-ready
  from this skill.
- Do not dispatch an implementation thread until Pedro says to implement, pick
  it up, send it to an agent, or otherwise approves implementation.

## Source Order

1. Resolve and read the source of truth: WhatsApp, Gmail, meeting transcript,
   Drive doc, screenshots/media, Linear, repo docs, or code.
2. Use metadata-only discovery first for private chats; read the narrow message
   window needed to understand the ask.
3. Download/open cited screenshots, PDFs, photos, or annotated images when they
   affect scope.
4. Check Linear for existing coverage before proposing a new issue. Include
   inactive states such as Done, Duplicate, Obsolete, Canceled, and Needs Info
   when available.
5. Inspect repo docs/code only enough to avoid wrong or duplicate scope.

## Elicitation

Extract only action-shaped items:

- `Requirement`: a missing capability, field, report, workflow, print detail, or
  user-visible behavior.
- `Bug`: promised/current behavior is wrong, broken, regressed, or producing
  incorrect results.
- `Needs Info`: the desired behavior, data source, owner, or correctness rule is
  not clear enough to implement.
- `Deferred`: explicitly later, future-meeting, design/open discussion, or not
  concrete enough for near-term work.
- `Non-actionable`: status, scheduling, thanks, jokes, or background.

Prefer one independently reviewable work packet at a time. Split only when two
outcomes can be implemented and reviewed separately.

## Ordering

When one source yields multiple candidate issues, propose them in dependency
order — foundations first, consumers last — not in the chronological order
they came up in the source. Meetings tend to discuss problems top-down;
implementation goes bottom-up. State the dependency rationale so Pedro can see
why the order differs from the conversation. When an explicit stakeholder
"start here" signal conflicts with dependency order, surface the conflict
instead of silently picking one.

## Plain Language First

Phrase each requirement as what the user or system can do after the issue is
done, before any technical scope detail. Pedro should be able to approve the
packet without decoding implementation vocabulary. When a packet bundles
foundation work with a proving consumer (for example "store the token and make
one verified call"), say why the bundle exists and offer the split.

## Linear Rules

- If Pedro only asks what something means, what is missing, or whether it is
  covered, answer the question first and do not mutate Linear.
- If Pedro approves a requirement for implementation, create/update a Todo issue
  unless he asks for a different state.
- If Pedro asks to capture or park something without implementation, use Backlog
  or Needs Info as appropriate.
- If an existing issue already covers the work, update/comment on that issue
  instead of creating a duplicate.
- A Linear issue is a source-linked work packet, not a transcript summary or
  implementation plan.
- Include source pointers: person/thread/document, message IDs or timestamp
  range, media IDs/paths, transcript timestamps, repo paths, and Linear links
  when available.
- Include compact `Scope` and `Out of scope` sections whenever adjacent work is
  present in the same source.
- Add `Pedro-reviewed specification` only when Pedro explicitly supplies or
  approves exact wording/constraints as his specification.
- Do not add file-level implementation steps, test plans, acceptance criteria,
  architecture, or PR sequencing unless Pedro explicitly asks for that level of
  direction.

## Visual Evidence

When source media contains annotations, red marks, arrows, highlighted fields,
or verbally referenced areas:

- inspect each relevant visual item before writing the issue;
- list each marked area in plain language;
- give each area a disposition: `In this issue`, `Covered by ISSUE`, `Split to
  ISSUE`, `Out of scope because ...`, or `Needs Info`.

Do not say visual evidence is fully covered until each marked item has a
disposition.

## Output

When Pedro asks which issue to work on next or for a packet proposal he can
green-light, run the elicitation and coverage work silently and present ONE
packet through the `issue-explainer` lane (a standalone HTML decision
artifact) instead of a multi-issue list in chat. Keep chat narration to a few
lines. Surface the full candidate list only when Pedro asks for it.

For other elicitation-only turns, end with a compact result:

```markdown
Elicitation result:

- Requirement / bug: PLAIN ENGLISH WORK
- Covered already: ISSUE_OR_REASON
- Proposed Linear packet: TITLE, state, scope
- Open questions: QUESTION_OR_NONE
- Recommended next step: create/update issue, dispatch implementation, or wait
```

When Pedro approves implementation, create/update Linear first, then use
`implementation-dispatch` in a separate step to create the fresh agent
thread.
