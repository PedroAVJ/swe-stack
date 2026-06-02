---
name: symphony-coverage-pass
description: Audit WhatsApp chats, meeting transcripts, docs, or other stakeholder input for Symphony/Linear follow-up coverage without turning Linear into the full spec. Use when Pedro wants requirements, bug reports, decisions, or meeting/chat follow-ups represented as issues or comments so work is not lost.
metadata:
  author: Pedro
  origin: local-self-authored
  source: hand-written
  provenance: not-openai-curated-not-plugin
---

# Symphony Coverage Pass

Use this skill when the user wants to make sure messy stakeholder input is covered by actionable follow-up tracking.

Typical triggers:

- "Do a coverage pass on this WhatsApp thread."
- "They sent a bunch of requirements; make sure we have issues."
- "Look at the transcript and tell me if we missed anything."
- "Cover the bugs from this chat in Linear."
- "Make sure every action-shaped thing has somewhere to live."

## Mental Model

Linear is not the spec home. Linear owns follow-up coverage.

The goal is not to fully specify every detail in an issue. The goal is to avoid losing work.

Use this split:

- **Linear**: action-shaped follow-up coverage, issue pointers, small work buckets, blockers, bugs, and "do not forget this exists."
- **Notion/docs**: domain explanation, durable knowledge, decisions, and fuller spec context.
- **Repo/PR**: implementation decisions and exact behavior once the code is being changed.
- **Drive/raw files**: source evidence such as transcripts, recordings, screenshots, PDFs, and exports.
- **WhatsApp/email/chat**: source-of-truth stakeholder wording and timing.

Good language:

- coverage pass
- follow-up coverage
- work coverage
- coverage gap
- covered by
- not covered yet

Avoid framing this as "complete specification" unless the user explicitly asks for a spec.

## Default Contract

Do:

- Read the relevant source of truth before interpreting requirements or bugs.
- Extract action-shaped items, not every conversational nuance.
- Check existing Linear issues before creating new ones.
- Prefer concise issue comments when an existing issue already covers the work.
- Create a new issue only when there is a real uncovered work item.
- Put domain/spec explanation in Notion or docs when useful, then link from Linear if needed.
- Report what is covered, missing, deferred, and intentionally ignored.

Do not:

- Treat Linear as the complete spec.
- Create one issue per sentence.
- Create issues for pure context, jokes, coordination, vague anxiety, or already-deferred ideas.
- Turn a stakeholder's broad comment into a large implementation plan unless the user asked for planning.
- Read broad private chat history when a narrow message window is enough.
- Send WhatsApp messages, emails, or stakeholder replies from this skill.
- Make repo/code changes unless the user explicitly asks to implement.

## Source Order

Ground the pass in the actual source.

For WhatsApp:

1. Use the WhatsApp skill/plugin.
2. Check bridge health only when needed.
3. Resolve the chat with metadata first.
4. Read the relevant date/message window.
5. Use message context around quoted replies or ambiguous replies.
6. Download media only when the media content affects the coverage decision.
7. Use Google Contacts if a person, phone number, company, or identity is unclear.

For meetings:

1. Prefer the canonical `transcript.txt` artifact when one exists.
2. Use the Google Doc only as a readable view or link target.
3. Use the recording only when transcript quality or missing context matters.
4. Keep raw transcripts in Drive; do not paste full transcripts into Linear.

For issue tracking:

1. Fetch the parent issue if one exists.
2. Fetch likely existing child issues or search by topic.
3. Read relevant comments before deciding something is uncovered.
4. Preserve existing labels/statuses/parent relationships where possible.

For repo grounding:

- Inspect repo docs/code only when needed to avoid duplicate or wrong issues.
- Do not turn a coverage pass into implementation.

## Extract Candidates

Build a short candidate list from the source. Classify each item as one of:

- **Bug report**: someone observed wrong behavior, broken UI, data mismatch, crash, missing save, etc.
- **Requirement**: someone asked the product to support a behavior or workflow.
- **Data dependency**: someone must provide data, codes, files, examples, access, or decisions.
- **Decision**: the group chose naming, direction, scope, or ownership.
- **Domain knowledge**: reusable context that should be documented but may not be work.
- **Deferred idea**: explicitly "later", "not now", "we can see later", or not concrete yet.
- **Non-actionable context**: status, scheduling, compliments, general explanation, or background.

Only the first four usually need Linear coverage.

Domain knowledge usually goes to Notion/docs. It may get a Linear comment only when it prevents misunderstanding of an existing issue.

Deferred ideas get noted only when they are likely to be forgotten and the user wants future tracking.

## Coverage Test

For each candidate, ask:

1. Is there an existing issue that would cause someone to handle this?
2. If yes, does the issue need only a short comment or source link?
3. If no, is the item concrete enough for a small backlog issue?
4. If it is not concrete, should it be captured in Notion/docs instead?
5. Is there a source link, timestamp, message ID, screenshot, or file that future work can trace back to?

An item is covered when a future worker can find it and know that work may be needed.

An item is not necessarily covered just because related words appear in an issue. It must be covered in the correct work bucket.

## Linear Writing Style

Keep Linear concise.

For a new issue:

```markdown
Coverage note from SOURCE:

Stakeholder said/observed SHORT FACT. This is being tracked so it does not get lost; fuller domain/spec context lives in DOC_OR_NOTION_LINK if applicable.

Source:
- WhatsApp: CHAT/PERSON, DATE, MESSAGE_ID_OR_WINDOW
- Transcript: MEETING, TIMESTAMP
- Drive/Doc/Repo: LINK_OR_PATH

Expected coverage:
- Small action-shaped outcome
- Any hard constraint or blocker
- What not to assume, if important
```

For an existing issue comment:

```markdown
Coverage clarification from SOURCE:

This issue should also account for SHORT FACT. Full details are in DOC_OR_NOTION_LINK if applicable.

Source: TIMESTAMP_OR_MESSAGE_WINDOW.
```

Avoid long acceptance criteria unless the issue already needs them or the user explicitly asks.

## When To Create vs Comment

Create a new issue when:

- No existing issue would naturally cause the work to happen.
- The item can be worked independently.
- The issue prevents a real bug/requirement from being forgotten.
- The source describes a concrete workflow, broken behavior, missing field, data dependency, or customer-visible need.

Comment on an existing issue when:

- The work bucket already exists but a nuance/source link is missing.
- The item changes the interpretation of an existing issue.
- The item is a caution like "do not assume X" or "this term means Y."
- The detail belongs in docs/Notion but the issue needs a pointer.

Use Notion/docs only when:

- The item is domain knowledge or a durable explanation.
- It is useful context but not clearly shippable work.
- The issue would become a spec dump if the detail were pasted there.

Do nothing when:

- The source is pure coordination or scheduling.
- The item was explicitly deferred and is not yet concrete.
- The item is already clearly covered.
- The item is too vague and no reasonable tracking action exists.

## Output Format

End with a compact coverage report:

```markdown
Coverage result:

- Covered already: ITEM -> ISSUE_OR_DOC
- Added comment: ITEM -> ISSUE
- Created issue: ITEM -> ISSUE
- Captured in docs: ITEM -> NOTION_OR_DOC
- Not tracked: ITEM -> reason

Remaining gaps:
- GAP -> recommended next action
```

When the user asks only "are we missing anything?", answer the coverage question first. Do not create or update issues unless they asked you to fix the coverage or you have clear prior permission in the same thread.

When the user says to "cover them with issues", apply the changes after reading the source and checking existing issues.

## Safety Boundaries

- For WhatsApp, never live-send a message from this skill.
- For private chats, quote minimally and summarize rather than dumping message contents.
- Preserve source links/IDs for traceability, but avoid exposing raw phone/JID/LID identifiers in user-facing summaries unless debugging.
- If the source includes sensitive personal content unrelated to the project, ignore it.
- If the coverage pass spans several projects or clients, keep separate coverage groups instead of mixing issues.
