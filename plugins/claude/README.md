# Claude

Local Codex plugin for using Claude Code to guide polished visual explainers.

Codex owns this wrapper as a stewardship layer: prompts, logs, implementation,
verification, and final shipping judgment stay under Codex control. Claude
provides visual-artifact direction for the included explainer workflow.

This project is unofficial and is not affiliated with Anthropic.

## Workflow rule of thumb

- Use the explainer skill for a standalone designed HTML explanation.
- Claude supplies visual direction; Codex implements and verifies the artifact.

## Model selection

The wrapper passes `--model claude-opus-4-8` by default so Claude runs use Opus 4.8 unless a specific model is explicitly provided with `--model`.

## Included surfaces

- `skills/explainer` produces polished standalone HTML explainers through the Claude visual-artifact workflow.
- `scripts/run_design_pass.py` runs Claude in streamed JSON mode and writes raw logs so Codex can inspect progress.
- `templates/visual-handoff.md` provides the read-only visual-direction prompt.
- `assets/claude-mobile-app-icon.jpg` is sourced from the Claude by Anthropic App Store listing.

## Claude Code compatibility

This plugin is intentionally Codex-first. It does not ship a Claude Code plugin manifest because its purpose is to let Codex invoke and steward Claude Code, not to teach Claude how to call itself.
