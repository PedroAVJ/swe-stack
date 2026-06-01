# SWE Stack

Agentic SDK for prosumers.

SWE Stack is a collection of local-first tools, plugins, CLIs, skills, and agent workflows for people who want software-engineering agents to operate real personal and business systems without handing everything to a hosted SaaS.

The stack is intentionally practical:

- Agent-facing CLIs with stable JSON output.
- Local SQLite-backed state where durability matters.
- Codex and Claude Code plugin shells.
- Reviewable drafts before side effects.
- Explicit confirmation gates for live writes.
- Small composable tools that can be inspected, forked, and run locally.

## Modules

| Module | Status | Description |
| --- | --- | --- |
| [`plugins/oracle`](./plugins/oracle) | Open | Codex-first second-opinion workflow through the user's logged-in ChatGPT Pro session (GPT-5.5 Pro) in Chrome. |
| [`plugins/whatsapp`](./plugins/whatsapp) | Open | WhatsApp bridge, SQLite-backed reads, media/context tools, reviewable drafts, and guarded sends for Codex and Claude Code. |

More modules will land here as the custom stack gets cleaned up for public use.

## Principles

1. Local-first by default.
2. Agent-readable interfaces before UI gloss.
3. Human approval before irreversible side effects.
4. Durable state over ad-hoc process memory.
5. Bring-your-own-agent: Codex first, Claude Code compatible.

## Quick Start

### Install In Codex

In the Codex app, open Plugins -> Manage -> Add marketplace:

```text
Source: PedroAVJ/swe-stack
Git ref: main
Sparse paths:
.agents/plugins
plugins/whatsapp
plugins/oracle
```

Or from the CLI:

```bash
codex plugin marketplace add PedroAVJ/swe-stack --ref main --sparse .agents/plugins --sparse plugins/whatsapp --sparse plugins/oracle
codex plugin marketplace upgrade
```

Leave sparse paths blank if you want Codex to fetch the whole marketplace repo. The sparse paths above are the minimal set for the marketplace manifest plus the current plugins.

### Develop Locally

```bash
git clone https://github.com/PedroAVJ/swe-stack.git
cd swe-stack
pnpm test
```

Use the first plugin:

```bash
cd plugins/whatsapp
./bin/whatsapp --json doctor
```

## Status

This is an early open-source extraction of a real working local agent stack. Expect the repo shape to evolve as more custom modules become public.

## License

MIT. See [`LICENSE`](./LICENSE).
