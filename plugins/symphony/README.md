# Symphony

Local Codex plugin for Pedro's explicit Symphony meta-workflow loops.

Codex owns stewardship: grounding, source boundaries, issue lifecycle judgment,
and final reporting. Symphony owns repeatable workflow shape. Claude may be
invoked as a collaborator for design, HTML, presentation, or UI implementation
passes, but Claude should not become the source of truth for work status.

## Current Role

- Coordinate source-of-truth intake from WhatsApp, meetings, Linear, git, and
  repo docs when Pedro explicitly asks for a Symphony workflow.
- Preserve meeting/call/audio evidence before issue extraction.
- Keep implementable Linear work separate from bookmarks, vague future topics,
  and canceled/obsolete scope.
- Run coverage passes so stakeholder input has issue/comment/doc tracking
  without making Linear the full spec.
- Treat issue/spec rewrites as a restart boundary for stale work.
- Run explicit Codex review, merge, release-proof, and Azure DevOps lifecycle
  lanes when Pedro asks for shipping work.
- Generate sprint-review and stakeholder-facing artifacts from grounded issue
  and repo state.
- Surface concise completion/status updates to Pedro after the workflow has
  actually finished.

## Repo-Specific Boundary

Individual product repos are not Symphony-owned implementation lanes by default.
Ordinary repo work should use normal Codex repo behavior: read the repo, answer
from the source of truth, implement the issue directly, and handle chats one at
a time.

Do not use Symphony to automatically intake, create, rewrite, restart, merge,
or monitor implementation issues. Use Symphony for a repo only when Pedro
explicitly invokes it for a meta artifact or workflow, such as a grounded review
HTML, a deliberately scoped intake audit, or a status summary.

## Skills

- `symphony`
- `symphony-evidence-intake`
- `symphony-linear-issue-writer`
- `symphony-issue-intake`
- `symphony-coverage-pass`
- `symphony-codex-review`
- `symphony-review-handoff`
- `symphony-change-preview`
- `symphony-sprint-review`
- `symphony-merge`
- `symphony-azure-publish-changes`
- `symphony-azure-merge`

## Boundary

This plugin is a product-style workflow plugin, not an MCP server. Add
MCP tools only when there is a concrete runtime action that cannot be handled
cleanly by Codex skills, existing app connectors, the Symphony CLI, or local
scripts.
