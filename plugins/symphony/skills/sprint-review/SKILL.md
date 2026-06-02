---
name: sprint-review
description: "Use when Pedro explicitly asks for a Symphony sprint review, demo agenda, stakeholder-facing HTML review, or grounded presentation artifact."
---

# Symphony Sprint Review

Use this skill for sprint reviews and demo-prep artifacts. Pedro should be able
to ask Codex directly; he should not need to open Claude and ask again.

This is a review/artifact workflow, not an implementation lane. Do not let this
skill pull a repo into Symphony-owned coding or issue lifecycle work. Use it
only to prepare grounded review artifacts when Pedro explicitly asks for that
artifact.

## Workflow

1. Ground the review window.
   - Use Pedro's requested dates, meeting, project, or issue scope.
   - If Pedro says "latest meeting", "last meeting", "newest meeting", or is
     continuing a meeting-review thread, the default scope is that meeting's
     follow-up items only. Do not expand to earlier sprint work unless Pedro
     explicitly asks for a broader sprint/history review.
   - If the latest meeting was mostly debugging, access setup, deployment
     triage, or operations, do not automatically use it as the stakeholder-demo
     anchor. Treat the previous substantive product meeting as the baseline
     when Pedro frames the review as "changes since then"; items already shown
     or accepted in that baseline meeting are excluded from demoable new work.
   - If missing, infer the smallest sensible recent requested window
     and state it.
   - Before rendering, state the chosen window in plain language and verify it
     does not include unrelated previous-meeting foundation work or baseline
     items that were already shown before the review window.
2. Read Linear for the relevant labels/issues.
   - Translate issue IDs into plain-English names.
   - Done/completed items are demoable.
   - In-progress, Merging, HumanReview, Todo, Backlog, Needs Info, canceled,
     obsolete, and deferred items must be separated.
3. Cross-check with repo git history and meeting evidence where cheap.
   - For latest-meeting reviews, cross-check the relevant transcript/WhatsApp
     evidence for what was immediate versus deferred to a next meeting.
   - Supporting earlier foundation may be mentioned as context only, not counted
     as demoable latest-meeting work.
4. Preserve caveats.
   - Do not claim live provider ingestion, deployment, merge, or stakeholder
     approval unless verified.
   - Do not promote bookmark/future-meeting notes into delivered work.
5. Render the artifact.
   - Preferred path in a repo: `docs/sprint-reviews/<review-date>.html`.
   - Scratch path is acceptable for exploratory drafts:
     `.codex-artifacts/sprint-review/sprint-review.html`.
   - Symphony/Codex owns the sprint-review orchestration, evidence gathering,
     issue-status boundaries, and caveats.
   - For polished HTML, delegate only the rendering pass to Claude. Give Claude
     the grounded brief and media, and ask Claude to use its frontend/design
     capabilities to write the HTML. Claude should not be the source-of-truth
     owner for issue intake, scope decisions, or status boundaries.
6. Verify.
   - Open/render the HTML with a browser when feasible.
   - Check mobile width for horizontal overflow.
   - Check that key caveats and issue-status boundaries appear in the page.

## Output Shape

The final chat answer should be short:

- Link the HTML file.
- State the verified window and major counts.
- Name any caveats that matter for presenting.
- Mention whether Claude was used for the rendering pass.
