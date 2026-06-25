# Claude

Local Codex plugin for using Claude Code as a collaborator.

Codex owns this wrapper as a stewardship layer: prompts, logs, verification, and final shipping judgment stay under Codex control. The plugin is not a fixed "collaboration mode"; it is a way to choose the right Claude workflow for the task and preserve the feedback loop.

For app UI and frontend implementation work, Claude must own the implementation pass. Codex should invoke Claude with the frontend implementation workflow before making UI edits, then constrain scope, inspect the diff, clean up mistakes, verify behavior, and decide what ships. A handoff-only or critique-only pass is only acceptable when the user explicitly asks for planning, critique, or no code changes.

This project is unofficial and is not affiliated with Anthropic.

## Workflow rule of thumb

- Use an implementation pass for app UI and frontend implementation work. Claude owns the UI edit pass; Codex stewards it.
- Use a handoff pass only when the user explicitly wants planning, critique, or a second opinion before code changes.
- Treat user feedback on the output as specification discovery. Update the prompt/workflow so the same failure is less likely next time.
- Codex remains responsible for checking diffs, fixing breakage, verifying in-browser behavior, and deciding what is ready.

## Model selection

The wrapper passes `--model claude-opus-4-8` by default so Claude runs use Opus 4.8 unless a specific model is explicitly provided with `--model`.

## Included surfaces

- `skills/frontend-ui` is the mandatory workflow for app UI and frontend implementation work: Claude edits the UI directly, while Codex stewards and verifies.
- `skills/explainer` produces polished standalone HTML explainers through the Claude visual-artifact workflow.
- `scripts/run_design_pass.py` runs Claude in streamed JSON mode and writes raw logs so Codex can inspect progress.
- `templates/frontend-implementation.md` is the default frontend workflow: Claude edits the UI directly, while Codex stewards and cleans up.
- `templates/frontend-handoff.md` remains available for explicit read-only critique or planning.
- `assets/claude-mobile-app-icon.jpg` is sourced from the Claude by Anthropic App Store listing.

## Claude Code compatibility

This plugin is intentionally Codex-first. It does not ship a Claude Code plugin manifest because its purpose is to let Codex invoke and steward Claude Code, not to teach Claude how to call itself.
