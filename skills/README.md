# Skills

Pedro-authored standalone agent skills (one folder per skill, `SKILL.md`
inside). Skills that belong to a plugin live under that plugin's `skills/`
directory instead; this directory is for skills that stand alone.

Install into local agents (Claude Code, Codex, and others) with the skills
CLI:

```bash
npx skills add PedroAVJ/swe-stack --list
npx skills add PedroAVJ/swe-stack --skill <name> -a claude-code -a codex
```

Workflow: edit skills here (upstream) first, push, then upgrade local
installs. Local `~/.claude/skills` and `~/.codex/skills` are install targets,
not sources of truth. OpenAI curated/system skills (installed via
`$skill-installer`) stay local-only and are never vendored into this repo.
