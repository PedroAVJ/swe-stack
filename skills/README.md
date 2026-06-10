# Skills

Pedro-authored standalone agent skills (one folder per skill, `SKILL.md`
inside). Skills that belong to a plugin live under that plugin's `skills/`
directory instead; this directory is for skills that stand alone.

All skills here are client-agnostic instructions usable by any agent that
reads the [Agent Skills](https://agentskills.io) format. Per-agent targeting
(codex-only, Claude-only, everything) happens at install time, not in the
repo.

| Skill | What it does |
| --- | --- |
| `agent-ledger` | Agent-owned operational state in a local SQLite ledger (IOUs, follow-ups, agent todos) |
| `agents-md-index` | Keep AGENTS.md an index, not a manual; migration walkthrough for bloated files |
| `anger-defusal` | Context-gap check before responding to user frustration; verdict-first defusal shape |
| `bdd-test` | Minimal BDD contracts (Given/When/Then Markdown) paired with Playwright automation |
| `codex-app-hacking` | Inspect/patch/restore the local macOS Codex desktop app bundle (ASAR, codesigning) |
| `mac-health-triage` | Diagnose macOS CPU heat, memory pressure, swap, and stale agent processes |
| `publish-file` | Publish local files to durable URLs via the publish-file CLI (Vercel Blob) |
| `sentry-logs` | Sentry Logs vs issues/events/traces; query the right surface |
| `sqlite-cache-cli-pattern` | Durable CLIs that sync API/connector data into a local SQLite cache |

Install into local agents with the skills CLI:

```bash
npx skills add PedroAVJ/swe-stack --list
npx skills add PedroAVJ/swe-stack --skill <name> -a claude-code -a codex -g -y
```

Always install by explicit `--skill` name. Do not use `-s '*'` / `--all` on
this repo: the CLI discovers every SKILL.md in the tree, including
plugin-internal skills under `plugins/*/skills/`, which are delivered via the
plugin marketplaces and must not be double-installed as standalone skills.

Workflow: edit skills here (upstream) first, push, then sync local installs —
see `.agents/skills/swe-stack-release` for the full release procedure,
including the Claude Code symlink bridge (Claude does not read
`~/.agents/skills`; each skill needs `ln -sfn ~/.agents/skills/<name>
~/.claude/skills/<name>`). Local skill directories are install targets, not
sources of truth. OpenAI curated/system skills and third-party skills are
never vendored into this repo.
