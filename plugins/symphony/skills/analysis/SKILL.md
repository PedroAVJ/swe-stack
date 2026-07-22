---
name: analysis
description: "Use when Pedro wants Symphony to analyze requirements: apply the SWEBOK definition of a requirement, classify elicited requirements along the kept SWEBOK dimensions, suggest which architecture component each requirement is allocated to, or surface requirement conflicts by SWEBOK's three conflict types."
---

# Symphony Requirements Analysis

This skill covers the SWEBOK definition of a requirement plus three
analysis topics: Requirements Classification, Requirements Allocation, and
Requirements Negotiation. Conceptual modeling and formal analysis are
deliberately dropped — Pedro's call, do not reintroduce either.

## Reference Vocabulary

SWEBOK (Software Requirements knowledge area) is the single reference
vocabulary for Symphony requirements work. Do not merge in other frameworks
— Sommerville's user-vs-system altitudes, Wiegers, ISO/IEC/IEEE 29148
well-formedness checklists — unless Pedro asks. 29148 becomes relevant only
if a formal SRS document is ever contractually required; until then it is
out of scope.

## What Counts as a Requirement

Per SWEBOK: a requirement is "a property that must be exhibited by something
in order to solve some problem in the real world." It must be:

- **Verifiable** — as an individual feature if functional, at system level
  if nonfunctional. If you cannot state how it would be checked, it is a
  wish, not a requirement yet.
- **Unambiguous** — stated as clearly as possible.
- **Quantified where appropriate** — "under 2s for 95% of transactions",
  not "fast".

## Classification

SWEBOK's Requirements Classification topic lists six dimensions. Symphony
uses four. Priority and volatility/stability are deliberately dropped, not
overlooked: both exist to ration scarce implementation effort, and with
agent coding implementation is cheap. Do not ask Pedro for priorities or
stability estimates, and do not record them.

Classify each requirement along:

1. **Functional vs nonfunctional** — behavior the system exhibits vs a
   quality or constraint on it.
2. **Derivation** — where it came from, which fixes where it gets
   validated:
   - *Imposed directly* by a stakeholder → validate with that stakeholder.
   - *Derived* from a parent requirement → validate against the parent and
     keep the trace; if the parent dies, the child dies.
   - *Emergent* — a whole-system property no single component satisfies →
     verifiable only end-to-end.
3. **Product vs process** — does it constrain the artifact, or the activity
   of building it? Nonfunctional product requirements are still product
   requirements; process requirements say nothing about what the software
   does.
4. **Scope** — the extent to which it affects the software: narrow
   (satisfiable by one component) vs global (cannot be allocated to a
   discrete component; constrains architecture and every future change).

## Allocation

For each requirement, suggest which architecture component is responsible
for satisfying it. Components are the named boxes of the target system's
decomposition at feature-area altitude — for TradeInCode: monitoring,
trips, customs, IntegratorAPI, Nova frontend, and so on — never
implementation mechanisms (mutation vs EF hook vs background job is design
inside the box, below this skill).

- State the owning component per requirement; Pedro confirms.
- Surface cross-component dependencies the allocation exposes ("monitoring
  owns auto-close but depends on BOL status owned by trips").
- Record any derived requirements the allocation mints per component, with
  their parent trace — this feeds the derivation dimension.
- A requirement that cannot be allocated to a single component is
  global-scope by definition; say so, and note that emergent properties are
  verified through component interaction, end-to-end only.
- SWEBOK notes this is where analysis overlaps design; keep the overlap to
  picking boxes. Do not design inside them.

## Negotiation

SWEBOK names exactly three conflict types. When requirements conflict,
identify which type it is and surface it:

1. **Stakeholder vs stakeholder** — two stakeholders require mutually
   incompatible features.
2. **Requirements vs resources** — a requirement exceeds what is
   available.
3. **Functional vs nonfunctional** — a functional requirement conflicts
   with a nonfunctional one.

The rest of SWEBOK's negotiation topic — the no-unilateral-decision rule
and the prioritization methods (cost-value, pairwise comparison) — is
deliberately dropped, Pedro's call: conflicts go to him regardless, and
prioritization is effort-rationing. Do not apply or record either.

## Codex Adversarial Pass

Claude and Codex fail in opposite directions on this task: Claude's drift
is loose labels and design decisions recorded as requirements; Codex's
drift is dropped provenance and hedges hardened into false precision. So
after drafting the full analysis and before presenting it, dispatch a
critique to the `codex:codex-rescue` subagent as a single read-only task.

The forwarded task must contain:

- The complete draft analysis verbatim.
- Repo paths to the source evidence (transcripts, meeting notes) so Codex
  can ground the critique instead of reviewing prose in a vacuum.
- An explicit "review only, read-only, make no edits" instruction.
- The critique brief: challenge each row on requirement vs design
  decision, verifiability (was a hedge quantified into a fake number?),
  derivation traced to a named stakeholder, scope (global only when
  genuinely unallocatable), product vs process, missed requirements still
  in the sources, and conflict typing. Findings only — no rewrite.

Then reconcile in-thread: adopt findings that stick, reject the rest with
a stated reason, and present ONE final analysis. Close with a short list
of what the pass changed and what it challenged unsuccessfully, so Pedro
sees the disagreement instead of a silent merge.

Skip the pass — and say so plainly — when the rescue subagent is
unavailable or returns nothing (including when this skill runs inside
Codex itself, where self-review adds nothing). Never fabricate a critique
on Codex's behalf.

## Contract

- Analysis is an in-thread classification and allocation pass over already
  captured or elicited requirements. Answer in chat.
- The Codex adversarial pass is review-only; it inherits this skill's
  no-write contract.
- No Linear writes, no product code, no repo doc writes from this skill.
