---
name: requirements-map
description: "Render a WHOLE-SOURCE requirements map — everything a meeting, chat thread, or document demands, on one designed HTML page — so Pedro can re-anchor without replaying the source. Use when Pedro asks what a meeting requires overall, says he lost the thread of the work, or wants the full picture rather than one issue. For a single packet decision, use issue-explainer instead."
---

# Symphony Requirements Map

One source in, one page out: the complete picture of what that source demands,
with current status. This is Pedro's re-orientation document — he reads it when
the meeting has faded from working memory and he needs the whole board back in
his head in under two minutes.

## Optimize for intake, not completeness theater

The reader is re-anchoring, not auditing. Every element earns its place by
answering one of his five questions, in this order:

1. **What is this all about?** One-sentence thesis at the top — the meeting's
   ask compressed to its essence, in plain language.
2. **Why did it turn into this much work?** A short narrative paragraph
   connecting the stakeholder's framing (e.g. "a script and some UI") to the
   actual work map. This bridges his memory to reality — it is the most
   important prose on the page.
3. **What are the pieces and where do they stand?** The work map in dependency
   order, each piece: plain-language outcome, one supporting sentence, source
   anchor (timestamp/message id), and an honest status. Status vocabulary:
   done / on a branch awaiting review / in progress / not started / blocked,
   plus what blocks it.
4. **What's unresolved?** Open questions (with who owes the answer) kept
   visually separate from deliberately-deferred items (with the deferral
   quote/anchor). Never blend these — "waiting on Jorge" and "parked on
   purpose" are different mental shelves.
5. **What's the one decision in front of me?** End with it, singular if at all
   possible.

Known defects/risks on in-flight work get one honest block — count, flavor,
severity — not a bug tracker dump.

## Grounding

Same source-of-truth rules as `requirements-elicitation`: read the actual
transcript/thread, check Linear and the repo/branches for real status before
labeling anything done, and include source pointers in a colophon (transcript
path, timestamp ranges, branch/commits, the status evidence). Do not guess
status from memory of prior conversation turns — verify against git/Linear at
build time.

## Artifact contract

- Single self-contained HTML file; Google Fonts allowed; no build step; light
  AND dark mode via `prefers-color-scheme`; every color a CSS variable; no
  inline color styles; mobile-first responsive.
- **Design before markup.** Commit to a visual direction first — type pairing,
  palette, layout rhythm — chosen for a re-orientation brief: strong
  typographic hierarchy, generous whitespace, one accent color, restraint.
  Avoid badge/card/box soup; prefer typography over chrome. No house style;
  do not reuse the previous artifact's design system. Skip Inter/Roboto/Arial.
- Save to `/tmp/<source-slug>-requirements-map.html` and open it.
- Chat narration: a few lines — direction chosen, sections, path.

## Runtime

Same split as `issue-explainer`: in Claude Code, Claude designs and writes the
HTML directly; in Codex, Codex stewards and delegates the artifact to Claude
(the `claude` plugin's design pass), with no handcrafted fallback.

## Boundary

- Build only when Pedro asks for the artifact. If he asks *whether* one should
  exist or what it would contain, answer in chat first.
- Read-only lane: no Linear writes, no code changes, no dispatch. Zoom-ins go
  through `issue-explainer`; implementation approval through
  `requirements-elicitation` rules.
