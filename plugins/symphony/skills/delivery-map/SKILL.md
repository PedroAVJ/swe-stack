---
name: delivery-map
description: "Intake for things that were DONE — help Pedro evaluate built-but-unseen work without test-driving it himself. Use when Pedro asks what got built, whether finished work is okay, or how to lazily ingest a delivered feature. Same intake philosophy as requirements-map, pointed backwards."
---

# Symphony Delivery Map

`requirements-map` answers "what do we need to do?"; this answers "what did we
get, and is it okay?" — for a reader who will not test-drive it himself.

## Optimize for evaluation-without-driving

Pedro's questions, in order. Answer them conversationally — one flow per turn,
small inline visuals, let him react before moving on. A monolithic artifact
only if he asks for everything at once.

1. **What changed for me?** Observable product terms, zero prior knowledge:
   which screen, which section, which new buttons. Never lean on branch names,
   commits, or issue IDs as content.
2. **Show me it working.** Show, don't describe. The unit of evidence is a
   short slowed screen recording (30–60s) of the real app doing the real flow,
   with a one-line caption per clip; stills for static states. Recordings are
   the right medium for judging UI behavior; prose is not.
3. **What's actually verified?** Three honest labels, never blurred:
   *machine-tested* (suites/automation passed), *live-verified* (exercised
   against the real external system), *unverified*. Never attribute an
   experience to Pedro he hasn't had ("you saw this work") — he hasn't.
4. **What's still rough?** Defects with provenance on every row — "found in
   code review, file:line", never phrased so it could read as stakeholder
   input. Count + flavor, details on request.
5. **What's the decision?** Approve as-is / fix first / he test-drives it
   himself. One line.

## Evidence honesty

- Captions state what data is real, what was seeded for the demo, and what an
  error on screen means. A live rejection from an external API can be good
  footage — label it, don't hide it.
- If a flow cannot be demonstrated truthfully yet (missing credential, no
  data), say so and show the closest honest thing — never fake the UI state.

## Mechanics

- Record with slowed automated browsing (e.g. Playwright `slowMo` +
  `recordVideo`) against the real app; name clips by flow.
- **Video pipeline (settled empirically, 2026-06-12):** convert the recording
  to H.264 MP4 (`ffmpeg -c:v libx264 -pix_fmt yuv420p -movflags +faststart`),
  publish it with the `publish-file` lane, and deliver the URL as a plain
  markdown link in chat. Do NOT wrap clips in HTML for the inline preview
  panel: its webview chokes on local/webm/data-URI video and cannot
  fullscreen — Pedro clicks the link and watches in his real browser instead.
- HTML files in the preview panel are for text-and-stills documents only;
  in-thread widgets for diagrams, tables, and counters. Never auto-open an
  external browser unless Pedro asks.
- Answers and verdicts go in the turn's final message — text between tool
  calls does not render for Pedro.

## Boundary

- Read-only lane: no Linear writes, no code changes, no deploys.
- If Pedro asks *how* he should evaluate something, answer the question first;
  produce media when he says go.
- Runtime split as with the sibling skills: Claude Code authors directly;
  Codex stewards and delegates artifact work to Claude.
