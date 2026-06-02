---
name: symphony-review-handoff
description: Use when Pedro wants a Symphony human-review handoff artifact for a UI fix, especially a slower browser video that clearly shows the relevant behavior using existing auth/setup helpers instead of a full test-suite style demo.
metadata:
  author: Pedro
  origin: local-self-authored
  source: hand-written
  provenance: not-openai-curated-not-plugin
---

# Symphony Review Handoff

Create human-readable review artifacts for UI changes. Prefer short, focused browser recordings or screenshots over fast regression-test videos.

## When to use

Use this skill when the user asks for:

- a handoff video
- a review video
- a slower demo for humans
- a clear visual proof of a fix

This skill is for demonstration, not broad regression coverage. The review unit is the user-facing issue or bug, not the branch or PR.

## Core rules

1. Reuse existing auth/setup helpers when the repo already has them.
2. When the repo already has Playwright config, global setup, fixtures, storage state, or passing specs for the target flow, build the handoff artifact on top of that existing Playwright test harness instead of bypassing it with a standalone script.
3. Prefer a one-off Playwright spec inside the repo's existing Playwright runner over a standalone script. Only use a standalone script when there is no viable in-repo Playwright setup to reuse.
4. Reusing the runner means reusing the repo's real config, global setup, fixtures, env loading, and authentication/storage-state flow unless the user explicitly asks for something different.
5. Show only the relevant behavior. Skip unrelated setup whenever you can safely redirect, seed, deep-link, or reuse saved auth state.
6. Start the recording on the closest stable route or screen to the behavior being reviewed. If a stable deep link exists, use it.
7. Do not include upstream navigation through unrelated routes just because an existing helper already does that navigation.
8. Slow the recording down so a human can follow it.
9. Run browser automation headless by default. Do not launch a headed browser window or steal desktop focus unless the user explicitly asks to watch the flow live.
10. In the final response, embed the video directly in the thread whenever the client supports local video rendering. Do not default to plain file links when an embeddable local video path is available.
11. End with the exact local video path and a one-line note about what to watch.
12. Off-camera setup is mandatory whenever possible. Login, app boot, blank loading time, and unrelated form setup should not appear in the delivered handoff video unless the user explicitly asked to review those steps.
13. Deliver a dense video. If a recording contains dead time because Playwright recorded the whole browser context, trim the artifact before handing it off.
14. Treat leading dead time as a hard failure, not a suggestion. If the delivered video starts with more than about 2 seconds of blank, loading, or irrelevant setup, trim it or redo the recording before responding.
15. Using the Playwright test runner does not remove your ability to control when the delivered recording begins. Do off-camera setup in unrecorded steps or trim the recorded artifact afterward so the first useful frame is the reviewed UI.
16. Produce review artifacts per issue, bug, or user-facing workflow. A giant PR may have a summary artifact only in addition to issue-level handoffs, not instead of them.
17. For bug fixes, include reproduction evidence and fixed-state evidence whenever feasible. The reproduction can be a screenshot, video, trace excerpt, or terminal/app error capture, and the fixed-state artifact should use the same or comparable scenario so a reviewer can see what changed.
18. Review handoffs should show the app, fix, or workflow being reviewed. Do not include meeting clips, transcript excerpts, stakeholder-source evidence, issue-proposal context, or provenance material unless the user explicitly asks for source-context evidence in the handoff.
19. For UI improvements, default the fixed-state artifact to a short app video that starts on the relevant screen and shows the visible outcome. A still image is acceptable only for non-interactive visual proof when video adds no review value.
20. Name artifacts by issue or workflow so they can be mapped back without reading the PR, for example `ped-92-selector-labels-fixed.webm` or `ped-91-authorized-carrier-before.webm`.
21. In the final response, group handoff artifacts by plain-English issue name first, with tracker IDs secondary.
22. For click-triggered runtime bugs, a screenshot is not enough unless video is impossible. Record the triggering click path and the resulting error for reproduction evidence, then record the same click path in the fixed build.
23. Distinguish evidence types precisely when source-context evidence is explicitly requested:
    - **Report evidence**: stakeholder meeting recording, transcript quote, support clip, screenshot, or external bug report.
    - **Reproduction evidence**: the agent independently triggers the bug in the app, test harness, browser, terminal, or trace.
    - **Fixed evidence**: the same or closest comparable path on the fixed build.
    A meeting recording clip can be useful report evidence, but it is not a review handoff by itself and should not be included by default.
24. For fixed videos, start on the closest stable screen before the failing interaction. If the reported failure happened while editing a POE leg, the video should begin on the relevant route/trip screen and click into the POE-leg editor as the first reviewed action; customer setup, fixture creation, login, route creation, and unrelated navigation must stay off-camera.

## Recording workflow

1. List the issues or user-facing workflows covered by the change.
2. Decide the artifact type per issue:
   - bug: reproduction evidence plus fixed-state evidence when feasible
   - click-triggered runtime bug: repro video plus fixed-path video whenever feasible
   - meeting-only bug report: fixed-path app video by default; include the meeting clip only if the user explicitly asks for source-context evidence
   - meeting-derived UI improvement: fixed-state app video by default; include meeting/transcript context only when explicitly requested
   - interactive fix: video
   - static visual/data fix: video by default when it came from a meeting/demo; screenshot only when video is unnecessary and the user did not ask for recording context
   - backend-only fix: terminal/app output is acceptable only when there is no meaningful UI surface
3. Find existing auth, seed, and navigation helpers in the repo.
4. Do as much setup as possible off-camera:
   - seed data before recording
   - prepare auth state before recording
   - prefer opening the recorded context already authenticated
   - start at the closest stable screen to the behavior under review
   - if the app supports a stable deep link to that screen, use it instead of walking through higher-level navigation
5. Prefer creating a one-off spec inside the existing Playwright suite for the specific review task so the repo's runner performs setup for you.
6. Record video with visible pacing:
   - add pauses before and after key interactions
   - move the cursor intentionally before clicking when practical
   - leave a final pause on the fixed state
   - keep the browser headless unless the user explicitly requested a visible run
7. Keep the flow short and dense:
   - the first meaningful frame should already be on the target UI or one step away from it
   - do not show login unless login is the thing being reviewed
   - do not show empty waits, blank screens, unrelated setup, or category/dashboard traversal that is not part of the reviewed behavior
8. If context-scoped recording still captures setup, trim the final artifact before delivery.
   - do not hand off the raw artifact if trimming is required
   - the trimmed artifact is the deliverable
9. Save the artifact under `output/playwright/` when practical, or return the generated `test-results/.../video.webm` path if that is the cleanest result.
10. If you also include a clickable file reference, treat it as secondary to the embedded video, not a replacement for it.

## Pacing defaults

- Short pause after navigation: `800-1200ms`
- Pause before important click: `300-500ms`
- Pause after important click: `800-1500ms`
- Final hold on the fixed state: `2000-3000ms`

Favor slightly too slow over too fast.

## Implementation preference

- First choice: a focused Playwright spec executed through the repo's existing Playwright test runner, reusing the same config, global setup, fixtures, and auth flow as the passing suite.
- Second choice: adapt an existing focused regression spec, slowing it down and trimming it to the essential flow.
- Last choice: a standalone script, and only when no viable in-repo Playwright harness exists.
- Avoid pointing the user at a fast CI-style artifact when they explicitly asked for a human-review handoff.

## Output checklist

- Each covered issue has its own handoff entry.
- Bugs have reproduction evidence plus fixed-state evidence when feasible.
- Meeting clips or transcript excerpts are omitted unless explicitly requested as source-context evidence.
- The video is understandable without narration.
- The bug/fix behavior is visible in one pass.
- The video starts on the closest stable relevant UI, not at app boot, login, or unrelated higher-level routes.
- The delivered artifact has no obvious dead time.
- The final response embeds the video in-thread when possible, using the absolute local path.
- The artifact path is returned as an absolute path.
- The final response says what changed on screen in plain English.
