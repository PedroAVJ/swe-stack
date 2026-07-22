---
name: analysis
description: Analyze captured elicitation evidence into a classified, allocated candidate-requirements table plus conflicts to negotiate. Use when Pedro asks to analyze meeting/call/chat evidence, classify or chunk requirements, find conflicts or duplicates against the backlog, or update a prior analysis with verdicts or new evidence. In-thread artifact only — never writes to Linear.
---

# Symphony Analysis

Requirements analysis over evidence Pedro names: segment the sources into
candidate requirements, classify and allocate each one, detect conflicts and
duplicates, and present the result in-thread for negotiation. Specification
(writing Linear issues) is a separate downstream skill; this one never writes
to Linear.

Of SWEBOK's analysis facets, this skill performs classification, allocation,
and negotiation support. Conceptual modeling stays a by-hand instrument
outside this skill.

## Inputs

- The sources Pedro names: repo meeting transcripts and metadata, evidence
  bundles from the `elicitation` skill, WhatsApp threads, emails, docs,
  screenshots. Read them fully and chronologically before segmenting.
- The existing Linear backlog for the relevant project/team — read-only, for
  duplicate detection and conflicts with already-tracked work.
- When updating: the prior candidate table from this or an earlier thread.

If a named source cannot be read, stop and say which one; do not analyze
around a missing source.

## Chunking Rule

Individuate candidates per ISO/IEC/IEEE 29148 well-formed requirements:

- **Singular**: one capability, constraint, or quality factor per candidate.
  Split compound statements until each piece is independently verifiable.
  Test: if one acceptance criterion cannot fully cover the stub, it is more
  than one candidate.
- **Appropriate**: state the need, not the implementation. When a stakeholder
  dictates a solution, record the underlying need as the candidate and keep
  the stated solution in the note.
- **Correct**: the stub must accurately represent what the source said. Mark
  each candidate as stated (with a quotable source location) or inferred
  (Claude's reading between lines). Never present an inferred candidate as
  stated; ambiguous lines are marked ambiguous, not resolved silently.
- **Verifiable**: the stub must be checkable against the running product.

Requirements are singular; work packets are valuable. Several singular
candidates that are only valuable together stay separate rows with a note
naming the bundle, so specification can merge them into one issue.

## Candidate Table

One row per candidate:

| # | Candidate | Type | Area | Verdict | Note |
| --- | --- | --- | --- | --- | --- |

- **Type**: `feature` / `bug` / `decision` / `constraint`.
- **Area**: the product area the candidate lands on (for TradeInCode:
  `trips` / `monitoring` / `operations` / cross-cutting). This is allocation
  as a label. When the home is itself contested, the candidate becomes a
  `decision` row and the contest goes to the conflicts section.
- **Verdict**: `actionable` / `needs-info` / `conflict → Cn` /
  `duplicate = <ISSUE-ID>` / `excluded`.
- **Note**: bundle names, stated-vs-inferred marker when inferred, the
  stakeholder's proposed solution when one was dictated, or the reason for
  exclusion.

Every candidate carries a source pointer (file + location, or chat/message
reference), rendered per row or as a numbered footnote list under the table.

Do not add priority, volatility, or functional/non-functional columns unless
Pedro asks; extra dimensions are opt-in add-backs.

## Conflicts

Conflicts span rows and sources, so they live in their own section, each with
an ID (`C1`, `C2`, ...) and its flavor:

1. **Source vs source** — two stakeholder statements disagree. Attach a quote
   from each side. Resolution needs a human tiebreak.
2. **Candidate vs candidate** — two candidates in this batch are incompatible.
   Flag only genuine incompatibility, not sequencing.
3. **Candidate vs existing decision** — a candidate contradicts shipped
   behavior, a documented product decision, or an open tracked issue. Name the
   doc or issue. When Pedro says the existing behavior makes no sense,
   challenge the behavior rather than defending it.
4. **Candidate vs resource** — cost or capacity collision; usually resolves to
   defer, explicitly.

For each conflict list the resolution options:

- **escalate** — becomes a needs-info verdict plus a ready-to-ask agenda
  question for the named stakeholder.
- **decide** — Pedro picks; the verdict becomes actionable and the note
  records the decision as a documented assumption: what was chosen, why, and
  who can veto it. A self-made call must never end up looking like something
  a stakeholder asked for.
- **defer** — parked with an explicit note that it blocks nothing.

## Entry Points

- **Fresh analysis**: Pedro names sources; produce the full table and
  diagnostics.
- **Verdict update**: Pedro replies with resolutions ("C1 escalate, C2 decide
  ±8"). Update the affected rows and re-emit the settled table; carry decided
  conflicts into notes as documented assumptions.
- **Evidence update**: new evidence arrives (a new call, a Jorge reply).
  Re-analyze against the existing table; emit the updated table marking
  changed and added rows, without renumbering existing candidates.

## Boundaries

Do not:

- create, edit, close, or comment on Linear issues — the backlog is read-only
  here
- write issue bodies or acceptance criteria — that is specification
- invent requirements or citations; every stated candidate must trace to a
  readable source location
- resolve a conflict silently or present an inferred candidate as stated
- drop candidates without an `excluded` row and reason

The artifact is a markdown table in the final chat message. Offer an HTML
render only when the batch exceeds ~30 candidates or Pedro asks.

## Preferred Output

Final message contains, in order:

1. One-line result summary (counts by verdict).
2. The candidate table.
3. Source pointer footnotes, when not inline.
4. Conflicts with flavors, quotes, and resolution options.
5. Open questions as a ready-to-ask agenda grouped by stakeholder.

The settled table (all conflicts resolved, verdicts final) is the input the
specification skill consumes.
