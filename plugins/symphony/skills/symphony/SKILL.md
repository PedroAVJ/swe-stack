---
name: symphony
description: "Use only when Pedro explicitly asks for Symphony or a Symphony-owned meta-workflow: evidence intake, source-of-truth audits, Linear lifecycle hygiene, Codex review, merge/release proof, review artifacts, status summaries, or notifications after agent work completes."
---

# Symphony

Use this skill as the orchestration layer for Pedro's explicit meta-workflows.
Codex remains the steward: ground the state, decide the workflow boundary, call
the right tools or collaborators, and report the actual result.

## Repo-Specific Boundary

Individual product repos are not Symphony-owned implementation lanes by
default. For normal repo work, use that repo's AGENTS.md instructions and
ordinary Codex coding flow: inspect the source, implement the requested change,
verify it, and report back. Handle stakeholder chats and implementation details
one request at a time.

Do not use Symphony to automatically create, rewrite, restart, move, merge, or
monitor repo implementation issues. Use this skill for a product repo only when
Pedro explicitly invokes Symphony for a meta-workflow, such as a grounded review
artifact, a deliberately scoped intake audit, or a status summary.

## Core Model

- Symphony owns repeatable meta-workflow shape when explicitly invoked: intake,
  classify, create/update work, lifecycle hygiene, code-review closeout,
  explicit merge/release proof, status review, and notify Pedro.
- Codex owns judgment and source boundaries.
- Claude owns artifact/design/presentation passes when useful, but not the
  canonical interpretation of work status.
- Linear tracks implementable work, real Needs Info blockers, and explicitly
  requested backlog parking. Do not create bookmark cards for vague future
  topics unless Pedro explicitly asks to park them.
- Symphony is not a background deploy daemon. Merge, release, and deploy actions
  happen only when Pedro explicitly asks for that lifecycle step or the current
  task clearly includes it.

## Lifecycle Lanes

Use the narrower Symphony skills when the request names a lane:

- `symphony-evidence-intake`: preserve meetings, calls, audio notes,
  transcripts, Drive/Gmail artifacts, and local media before extraction.
- `symphony-linear-issue-writer`: write or rewrite grounded Linear issue bodies
  for Symphony pickup.
- `symphony-issue-intake`: turn grounded evidence into Linear work.
- `symphony-coverage-pass`: check that stakeholder input has issue/comment/doc
  coverage without making Linear the full spec.
- `symphony-codex-review`: run Codex review as closeout and verify findings.
- `symphony-review-handoff`: produce human-readable UI review videos or
  screenshots.
- `symphony-change-preview`: produce a Pedro-facing HTML preview artifact.
- `symphony-sprint-review`: produce grounded demo/review artifacts.
- `symphony-merge`: run explicit publish/merge/release-proof lifecycle.
- `symphony-azure-publish-changes` and `symphony-azure-merge`: use for
  Azure DevOps style publish and release proof.

## Source-Of-Truth Order

Choose the source before advising:

- What someone said or implied: WhatsApp, Gmail, transcript, or direct document.
- What work exists or is done: Linear plus git/PR/deploy state.
- What changed in code: repo diff/history and relevant tests.
- What should be presented: Done issues and merged/proven work first; in-flight,
  canceled, deferred, and unknown work in separate sections.

## WhatsApp / Meeting To Linear

When Pedro explicitly asks Symphony to turn messages, meetings, or stakeholder
feedback into work:

1. Read the actual source conversation or transcript before classifying intent.
2. Identify implementable work, Needs Info blockers, explicit backlog parking,
   canceled/obsolete items, and future-meeting topics.
3. Use the existing Linear issue-writing workflow for issue bodies and evidence.
4. Put uncertain or review-needed issues in Backlog unless Pedro asks for Todo.
5. Use Todo only when the issue is implementation-ready and Pedro wants agents
   to pick it up.
6. After rewriting a picked-up issue, move it back to Todo only when the new
   body should restart implementation.
7. If a stale PR/workspace exists for rewritten work, report the restart
   boundary clearly. Do not take over repo implementation unless Pedro
   explicitly asks for that separate coding task.

## Status And Completion

When Pedro asks whether something is done:

- Check Linear status, active Symphony workspace/log state, branch/PR state, and
  deploy/proof surfaces when relevant to the explicit Symphony workflow.
- Say plainly what is local, pushed, merged, deployed, canceled, blocked, or
  waiting for review.
- Do not say "done" when the issue is still Merging/HumanReview/In Progress.

## Collaboration With Claude

Invoke Claude through the local Claude plugin/workflow when the task benefits
from visual taste, editorial HTML, design critique, or UI implementation.
Ground the brief first. Claude receives a bounded brief; Codex verifies and
owns the final answer.
