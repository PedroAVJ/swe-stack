---
name: "frontend-ui"
description: "Use when the user asks for app UI, frontend, visual, layout, interaction, customer-facing screen, dashboard, component, CSS, responsive, mobile, or browser-visible implementation work. Claude must own the UI implementation pass; Codex stewards, reviews, cleans up, verifies, and decides what ships."
---

# Frontend UI

This is the mandatory Claude workflow for app UI and frontend implementation work.

If the task changes application UI, visual behavior, layout, styling, interaction, customer-facing screens, dashboards, components, CSS, responsive behavior, mobile UI, or another browser-visible surface, Codex must use Claude for the UI implementation pass before editing those UI files directly.

## Contract

1. Claude owns the UI implementation pass.
2. Codex owns stewardship: scope, prompt quality, logs, diff inspection, cleanup, verification, and final shipping judgment.
3. Do not substitute a read-only critique for implementation unless the user explicitly asks for planning, critique, or no code changes.
4. Do not hand-edit UI first and ask Claude afterward. Claude must get the first implementation attempt for the UI surface.
5. If Claude cannot run, say that plainly before editing UI and treat any Codex-only UI work as a fallback with a named failure reason.

## Workflow

1. Inspect the relevant repo files enough to give Claude a grounded, narrow prompt.
2. Run the plugin implementation pass:

```bash
python3 /path/to/plugins/claude/scripts/run_design_pass.py \
  --repo /path/to/repo \
  --mode implement \
  --model claude-opus-4-8 \
  --prompt "Implement the requested UI change. Keep scope narrow. Match the existing design system. Do not make unrelated changes."
```

Resolve `/path/to/plugins/claude` to the directory containing this skill, then use that plugin's `scripts/run_design_pass.py`.
The wrapper defaults to `claude-opus-4-8`, but the command should keep the model explicit when invoking this workflow.

3. Inspect Claude's raw log and resulting diff.
4. Clean up only what is necessary: broken code, scope drift, formatting, or integration mismatches.
5. Verify the real browser-visible behavior with the repo's appropriate local/dev flow.
6. In the final response, say that Claude performed the UI implementation pass, and mention any Codex cleanup separately.

## Boundaries

- Backend/data/schema changes that merely support UI may be done by Codex, but the visible UI implementation still goes through Claude.
- If a task is purely backend, CLI, data, or documentation with no browser-visible UI, this skill does not apply.
- Standalone educational HTML explainers use the `explainer` skill instead.
