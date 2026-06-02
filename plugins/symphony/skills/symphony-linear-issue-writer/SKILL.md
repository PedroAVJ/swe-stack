---
name: symphony-linear-issue-writer
description: Steward Symphony's Linear issue-writing workflow from grounded evidence. Use when Pedro wants WhatsApp messages, call/audio transcripts, meeting transcripts, Drive recordings, Gmail, repo docs, screenshots, PDFs, or mixed source bundles turned into Todo Linear issues, reviewed issue drafts, duplicate checks, Symphony pickup-ready issues, or feedback-driven changes to how these issues should be written.
---

# Symphony Linear Issue Writer

Use this skill when evidence should become Linear work. The Linear plugin is the
tool surface; this skill is the policy layer for issue shape, source grounding,
mutation gates, and Symphony pickup.

## Stewardship Contract

Codex is the steward of this skill. Pedro owns the desired outcomes and gives
feedback on the issues, PRs, and Symphony behavior that result from it; Codex
owns translating that feedback into durable workflow rules here.

Treat the skill as a living implementation detail of Pedro's Linear-to-Symphony
system:

- If Pedro says an issue was confusing, over-scoped, under-scoped, mislabeled,
  badly titled, hard for Symphony to implement, or otherwise wrong, update this
  skill unless the feedback is clearly one-off.
- Prefer changing the skill over repeatedly explaining the same mistake in chat.
- Preserve the workflow's intent, not its current wording. Rewrite sections,
  examples, and defaults when better rules emerge.
- Keep changes grounded in observed failures or explicit Pedro feedback.
- Do not ask Pedro to design the skill mechanics unless his preference is
  genuinely needed. He should be able to critique the output while Codex evolves
  the machinery.
- If a requested skill change would make issue creation unsafe, too broad, or
  conflict with higher-priority instructions, explain the boundary and make the
  safest narrower update.

## Doctrine

- Linear issues are evidence pointers plus Pedro-approved specification, not
  transcript summaries or implementation plans.
- Requirements elicitation is a distinct lane from implementation. When Pedro
  asks to elicit, extract the implementable requirement from the real source
  evidence into a Symphony-ready Linear issue; do not write product code, open a
  PR, or mark work review-ready as part of that same step unless he explicitly
  asks for implementation too.
- Do not create Linear bookmark cards for unresolved meeting topics, vague
  future discussions, or "remember to decide later" items unless Pedro
  explicitly asks for parking/meeting-prep artifacts. Linear should track
  implementable work, real `Needs Info` blockers for near-term work, or
  explicitly requested backlog parking.
- A Linear issue is a Symphony work packet. It must make the work type, primary
  product surface, and ownership boundary clear enough that the implementation
  agent does not infer neighboring work from the evidence.
- Read or verify the source of truth before interpreting scope, intent, tone,
  work status, or stakeholder asks.
- Mixed evidence is normal. A single issue may cite a WhatsApp message range, a
  call/audio transcript, a Drive recording, a repo doc, and a local file when
  all of them are needed to ground the same pickable work bucket.
- Mixed evidence is dangerous. If one transcript or chat covers multiple
  requests, identify which parts are operative evidence for this issue and which
  parts are background only.
- Keep the issue body small enough that the implementation agent must reread
  the source before planning.
- Do not expect the title to carry scope by itself. When a source mentions
  adjacent work, add explicit `Scope` and `Out of scope` sections.
- Use singular/plural words that match the real artifact: `corte print` for one
  print/PDF surface, `PDFs` only when multiple distinct PDFs are in scope.
- Todo is the default state for issues this skill writes. Pedro expects Codex to
  steward the issue-writing process; if an issue is wrong, he will give feedback
  and Codex will update this skill for future runs.
- Use Backlog only when Pedro explicitly asks for a draft, backlog parking, or
  review buffer instead of Symphony pickup.
- `Pedro-reviewed specification` is opt-in. Add it only when Pedro explicitly
  supplies or approves exact wording, constraints, or decisions for the issue
  body.
- Never put transcript-derived details, message summaries, agent inferences, or
  stakeholder quotes in `Pedro-reviewed specification` unless Pedro explicitly
  adopts that wording as his own reviewed specification.
- If Pedro asks to capture/create/add an issue without approving issue-body
  wording, create an evidence-pointer card only.
- Do not prescribe file-level changes, architecture, step-by-step execution,
  acceptance criteria, tests, or PR sequencing unless Pedro explicitly asks to
  include that level of direction.
- When Pedro specifies the canonical data model or relationship, do not smuggle
  current workaround logic into the card as fallback behavior. Mention the
  workaround only as out of scope or background evidence.

## Evidence Intake Boundary

This skill consumes stable evidence. It does not own evidence preservation.

Use or require intake first when source artifacts are missing or unstable:

- call recordings / voice notes: `audio-note-evidence-intake`
- Google Meet or formal meeting artifacts: `meeting-evidence-intake`
- WhatsApp messages: use the WhatsApp skill/plugin to read exact message IDs
- Gmail/Drive/docs/sheets: use the appropriate source skill/plugin

If Pedro explicitly asks for a weaker card from memory or an unrecorded
conversation, say the source is unrecorded in the issue body.

## Visual Evidence Coverage

Screenshots, photos, PDFs, and annotated images are source evidence, not just
attachments. When a WhatsApp message, transcript, or issue cites visual media:

- Download/open every cited image or PDF page needed to understand the ask
  before writing or updating the issue.
- Treat each visible annotation, red mark, arrow, circled field, highlighted
  row, or verbally referenced area as its own required evidence item.
- Add a `Visual coverage` section to the issue body before creating Todo work.
  The section must list each marked field or area in plain language and give a
  disposition for it: `In this issue`, `Split to ISSUE_ID/TITLE`,
  `Already shipped in ISSUE_ID/PR`, `Out of scope because ...`, or
  `Needs Info`.
- Do not compress several marked fields into a generic phrase like "show pesos"
  if the image points at separate rows, columns, cards, totals, or print
  sections.
- Do not mark the source as fully handled until every visual item has a
  disposition. If any visual item is unresolved or ambiguous, create a
  `Needs Info`/Backlog card or keep it explicitly out of scope with the reason;
  do not silently drop it.
- When later reporting that a visual-evidence request is fixed, recheck the
  original visual coverage list against the PR, production, or preview. Issue
  status and deploy status are not enough.

## Workflow

1. Identify all evidence sources needed for the requested work bucket:
   - messages with stable IDs and timestamps
   - media IDs and downloaded/opened image or PDF evidence when messages cite
     screenshots, photos, annotated images, or documents
   - transcript path or Doc link
   - recording/audio link when available
   - timestamp ranges for audio/meeting evidence
   - repo/doc/file paths when applicable
2. Classify the work before writing the issue:
   - `Feature`: add missing capability, field, report, print detail, workflow,
     or user-visible behavior where the existing system is not shown to be
     wrong.
   - `Bug`: existing promised behavior is wrong, broken, regressed, or produces
     incorrect results. Bugs need a bounded reproduction/source check.
   - `Research` / `Needs Info`: the requested behavior or correctness claim is
     not yet clear enough to implement.
   - If stakeholder language assumes a future data source, integration, or
     persistence path that the repo does not currently have, write a decision
     card (`Research` / `Needs Info`) instead of a build card.
   - If the only output would be a bookmark for a later meeting decision, do
     not create the issue unless Pedro explicitly asked to park that topic in
     Linear.
3. Name the primary surface and artifact:
   - Examples: `corte print`, `entrega de pan print`, `mobile route form`,
     `production backup job`.
   - If the same evidence also discusses another surface, quarantine that other
     surface under `Out of scope` or split it into another issue.
   - When follow-up chat clarifies which part of a meeting is "start with this"
     versus "we will discuss this next meeting", treat the chat clarification as
     operative evidence for issue boundaries. Split concrete start-now work from
     next-meeting filter/design/research work, and put the deferred work in
     Backlog or `Needs Info` when Pedro asks for a review buffer.
   - Avoid vague decision-card titles like `Clarify ...`. Prefer `Decide ...`,
     `Choose ...`, or `Define ...` so Pedro can see at a glance that the card is
     not ready for implementation.
4. For visual evidence, write the `Visual coverage` disposition list before
   deciding the final split. The list is the guardrail against losing marked
   fields during scope compression.
5. Search Linear before proposing or mutating. Include inactive states such as
   Done, Duplicate, Obsolete, Canceled, Could Not Reproduce, and Needs Info
   when the tool supports it.
6. Check repo/PR/deploy state only enough to avoid duplicate or already-shipped
   work.
7. Split work only into independently reviewable outcomes. Do not split helper
   concepts, internal query rules, or plumbing into separate cards unless they
   produce a PR Pedro can review on its own merits.
8. Choose the mutation mode from Pedro's request:
   - If Pedro asks to triage or suggest, draft cards in chat only.
   - If Pedro asks to create/add/write issues, create exactly the requested
     issue(s) in Todo by default.
   - If Pedro explicitly asks for drafts, backlog cards, or review-only cards,
     create them in Backlog.
   - If Pedro asks to update an existing issue, update only that issue.
   - If Pedro asks to clean up, replace, or redo an issue, it is allowed to
     close/obsolete the contaminated issue or PR after verifying the overlap.
   - If Pedro says the card looks good or should go to Symphony/Todo/Do after a
     draft, move only that named/current card into Todo.
9. For meeting/audio evidence, preserve chronological order unless Pedro
   explicitly asks for a specific topic or multiple cards.
10. Use `Agent: xhigh` when interpreting source evidence is the hard part. Use
   `Agent: high` for clear features and clear bugs once the scope is explicit.

## Mutation Rules

Allowed when Pedro explicitly asks to create/capture/add/write issues:

- create one or more Todo issues matching the requested count/scope
- create Backlog issues only when Pedro explicitly asks for drafts or backlog
  parking
- update a named existing issue with evidence pointers
- attach Drive/source links
- report duplicate/obsolete findings instead of creating new work
- close or obsolete contaminated duplicate work when Pedro asks to redo, clean
  up, or replace the issue and the overlap has been verified

When materially rewriting an existing issue body, title, or scope:

- First check whether a Symphony worker, local worktree, branch, or PR already
  exists for that issue.
- If no worker has started, update the issue normally.
- If a worker has started, treat the existing implementation prompt as stale.
  Do not assume the runner will reread the changed issue body.
- Move the corrected issue back to `Todo` so the implementation lane restarts
  from the rewritten body instead of continuing from the stale prompt.
- If a PR already exists for the stale prompt, close or supersede it when
  permitted before restart, or explicitly report that the new run must ignore
  the stale PR. Do not leave two plausible PRs competing for the same rewritten
  work without saying which one owns the corrected scope.
- If the stale implementation has no useful reviewable work, close or discard
  the old PR/worktree when permitted, then restart from the corrected issue.
- If the stale implementation has useful partial work, preserve it only as
  reference material and make the corrected issue body the source of truth.
- After a material rewrite of an active issue, explicitly report whether any
  active worker/PR/worktree was found and whether it must be restarted.

Not allowed without explicit Pedro approval:

- assigning/delegating an issue to an agent
- adding `Pedro-reviewed specification`
- creating extra issues beyond the requested count
- summarizing evidence as if it were the source pointer
- adding implementation plans, acceptance criteria, caveats, or inferred
  requirements

Pedro can approve a draft/backlog issue for pickup with language like "looks
good", "move it to Do", "send it to Symphony", or another explicit instruction
naming the current issue.

## Issue Shape

Use only sections that have real pointers. Keep labels short and literal.

```markdown
TITLE_AS_FIRST_LINE_OPTIONAL

Type:
Feature | Bug | Research | Needs Info

Source:
WhatsApp · PERSON_OR_GROUP

Messages:
`START_MESSAGE_ID` at YYYY-MM-DD HH:mm -> `END_MESSAGE_ID` at YYYY-MM-DD HH:mm

Visual coverage:
- `MESSAGE_OR_MEDIA_ID`: MARKED_FIELD_OR_AREA -> In this issue
- `MESSAGE_OR_MEDIA_ID`: MARKED_FIELD_OR_AREA -> Split to ISSUE_ID/TITLE

Transcript:
`PATH_OR_LINK_TO_TRANSCRIPT`

Recording:
PATH_OR_LINK_TO_RECORDING

Timestamps:
- HH:MM:SS-HH:MM:SS

Files:
`PATH_OR_LINK`

Scope:
PRIMARY_SURFACE only. ONE_OR_TWO_SENTENCES_NAMING_THE_USER_VISIBLE_OUTCOME.

Out of scope:
NEIGHBORING_WORK_OR_SURFACES_DISCUSSED_BY_THE_SAME_EVIDENCE.

Pedro-reviewed specification:
- Only exact wording Pedro explicitly approved for this issue.
```

Omit `Pedro-reviewed specification` unless Pedro explicitly supplied or approved
that text. Omit empty source sections. If an issue has both messages and audio,
include both pointers.

Use `Scope` and `Out of scope` whenever:

- the title cannot carry every important boundary
- the evidence mentions multiple screens, PDFs, reports, or workflows
- another Linear issue or PR already owns adjacent work
- a prior issue/PR was contaminated by broad transcript ranges

Avoid:

- meeting/date banners
- pickup notes
- context paragraphs
- long transcript or message summaries
- broad "related sources" sections
- invented acceptance criteria
- implementation plans
- file lists unless those files are source evidence
- quoting more than is needed to relocate or disambiguate the source
- vague nouns like `detail` without naming the detail in either title or scope

## Source-Specific Notes

WhatsApp:
- Read the real chat before interpreting.
- Use stable message IDs, timestamps, sender/contact, and media IDs.
- Quote only short snippets needed to identify the message.

Audio/calls:
- Require transcript plus recording/audio pointer when available.
- Include the narrowest timestamp ranges that cover the relevant work bucket.
- Do not include broad ranges that also cover adjacent requests unless the
  adjacent request is explicitly marked out of scope.
- Do not treat transcript excerpts as a replacement for the audio pointer.

Meetings:
- Work chronologically through the transcript/recording unless Pedro directs a
  specific topic.
- If multiple meeting topics exist and Pedro did not ask for bulk creation,
  handle one Todo issue at a time.

Repo/Gmail/Drive/docs:
- Cite exact file paths, URLs, email subjects/IDs, or document links.
- Verify current state when it is cheap and could affect duplicate/obsolete
  decisions.

## Titles

Use short plain-English product outcome titles. Titles are routing labels, not
implementation plans and not research chores.

Title pattern:

- Feature: `Show/Add/Carry/Include OUTCOME on SURFACE`
- Bug: `Fix WRONG_BEHAVIOR when CONDITION`
- Research/Needs Info: `Clarify QUESTION about SURFACE`

Before creating an issue, ask:

- Does the title name the primary surface?
- Does it name every critical data concept, or does the body name the missing
  one under `Scope`?
- Did I use singular/plural correctly?
- Would a different agent accidentally touch a neighboring issue from this
  title plus evidence?

Good:

- `Show carga nueva, prior saldo, and total pieces on entrega de pan print`
- `Show venta total and camioneta detail on corte print`
- `Carry camioneta balance into the next remision`

Bad:

- `Luis follow-up`
- `Ground WhatsApp and audio evidence`
- `Implement query and PDF refactor for remision calculations`
- `Show Excel-style venta total and saldo detail on corte PDFs`

## Weak Sources

If the source is unavailable or only remembered, say that directly in the issue:

```markdown
Source:
Pedro memory of in-person conversation, not independently recorded.
```

Do not create implementation-ready cards from weak sources unless Pedro
explicitly asks for that tradeoff.
