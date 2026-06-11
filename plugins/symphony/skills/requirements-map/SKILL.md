---
name: requirements-map
description: "Render a WHOLE-SOURCE requirements map — everything a meeting, chat thread, or document demands, on one designed HTML page — so Pedro can re-anchor without replaying the source. Use when Pedro asks what a meeting requires overall, says he lost the thread of the work, or wants the full picture rather than one issue. For a single packet decision, use issue-explainer instead."
---

# Symphony Requirements Map

One source in, one picture out: the complete view of what that source demands,
with current status. This is Pedro's re-orientation surface — he uses it when
the meeting has faded from working memory and he needs the whole board back in
his head in under two minutes.

## Mode: conversational by default

When Pedro is in a dialogue ("what are the things to do, roughly?"), do NOT
produce one monolithic page. Answer his current question with a short reply
plus one small inline visual (a rough-shapes card row, a chain diagram), then
let him steer — he zooms with follow-up questions, one per turn. Map his own
vocabulary to the real shapes ("the robot", "the knobs") and keep using his
words. Mid-conversation visuals are disposable; correctness of status labels
still binds (see verification rules below). Produce the full one-page map only
when he explicitly asks for the whole thing at once.

For work that was already DONE (evaluating built features), use the sibling
`delivery-map` skill instead — same philosophy, pointed backwards.

## Optimize for intake, not completeness theater

The reader is re-anchoring, not auditing. Two hard rules before anything else:

- **Assume zero prior knowledge.** Pedro does not know what was built, what a
  branch contains, or what prior conversation decided. Branch names, commit
  ranges, and issue IDs are colophon material, never load-bearing content.
  Status must be expressed as what is observable in the product: which screen,
  which section, which button now exists.
- **Visual-first, hard prose budget.** The map is a diagram, not an essay.
  Thesis: one sentence. Bridge: at most two sentences. Everything else is
  labels and fragments of five-ish words. If a section is becoming a
  paragraph, restructure it into a visual. Counters (built / defects /
  waiting / parked) beat sentences.

Every element earns its place by answering one of his five questions, in this
order:

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

- **Render inline in the conversation** — that is the primary surface. In
  Claude Code, use the visualize widget surface and follow its design system
  (flat, host CSS variables, dark mode automatic, diagram complexity budget,
  clickable nodes via sendPrompt for drill-down). In Codex, use its inline
  preview surface. Never auto-open an external browser unless Pedro
  explicitly asks for it.
- Optionally also save a standalone HTML copy under
  `/tmp/<source-slug>-requirements-map.html` for archival; when producing the
  standalone file, design before markup, support light and dark via
  `prefers-color-scheme`, and do not reuse the previous artifact's design
  system. The inline rendering always matches the host instead.
- Chat narration around the inline artifact: two or three sentences, no more —
  the artifact carries the content.

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
