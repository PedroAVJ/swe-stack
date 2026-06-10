---
name: issue-explainer
description: "Render ONE proposed Symphony work packet as a polished standalone HTML explainer Pedro can green-light at a glance. Use when Pedro asks which issue to work on next, asks for an issue proposal or packet explanation, or wants elicitation output he can approve quickly — instead of a multi-issue list in chat."
---

# Symphony Issue Explainer

Turn the winning packet from requirements elicitation into a single decision
artifact: one HTML page that explains one issue well enough for Pedro to say
yes or no without reading chat prose.

## Contract

- **One issue per page.** Never render a multi-issue dump. If elicitation
  produced several candidates, pick the dependency-first packet, show the rest
  only as a compact chain strip, and offer the next packet after a decision.
- The page answers, in order: what the user/system can do after the issue is
  done (plain language first), why this packet is first (dependency rationale,
  with the stakeholder's own words and a timestamp when a "start here" signal
  exists), what is in and out of scope, where it sits in the dependency chain,
  what Linear coverage was checked, and the explicit decision ask.
- Source pointers (transcript path, timestamp range, message IDs) belong in a
  colophon/footer, not in the narrative.
- Chat narration stays to a few lines: verdict, file path, decision ask.
- This lane explains; it does not mutate. No Linear writes, no product code,
  no dispatch. Approval still flows through `requirements-elicitation` rules,
  then `implementation-dispatch`.

## Artifact contract

- Single self-contained HTML file. No external JS frameworks; Google Fonts is
  fine. No build step.
- Light **and** dark mode via `@media (prefers-color-scheme: dark)`. Every
  color is a CSS variable defined in `:root` and overridden in the dark block.
  No inline `style="color: ..."` attributes, no JS theme toggle.
- Distinctive type pairing; skip Inter, Roboto, Arial, and generic system
  stacks. Commit to an aesthetic direction; avoid the generic docs-page or
  centered-card-on-white look.
- No house style: decide a fresh design system per explainer (palette, type,
  layout language). Do not carry over the previous artifact's design system.
- Readable on Pedro's iPhone and MacBook: mobile-first CSS, no fixed-width
  content, no horizontal scroll.
- Save to `/tmp/<issue-slug>-explainer.html` and open it.

## Runtime

The symphony plugin is installed in both Codex and Claude Code. The lane is
the same; who holds the brush differs:

- **Claude Code**: Claude owns the design judgment directly and writes the
  HTML itself, following the artifact contract above.
- **Codex**: Codex stewards scope, grounding, saving, opening, and final
  verification, and delegates the visual artifact to Claude (the `claude`
  plugin's `explainer` skill / design pass is the vehicle). Do not handcraft
  fallback HTML in Codex; if Claude fails or times out, report the failure
  with logs and stop the lane.

## Order of operations

1. Run elicitation/coverage work first (`requirements-elicitation` source
   order: ground, check Linear, dependency-order the candidates). Do it
   silently; the explainer is the deliverable, not the audit trail.
2. Render the one packet per the artifact contract.
3. End the chat turn with the decision ask. On green light, create/update the
   Linear issue per `requirements-elicitation` rules, then use
   `implementation-dispatch` separately.
