# SWE Stack Oracle Plugin

A Codex-first plugin for getting a second opinion from the user's logged-in ChatGPT Pro session.

Oracle is intentionally not an API wrapper. It packages the existing Oracle skill as a plugin and preserves the live workflow: gather verified local context, use Computer Use to operate Chrome, select a Pro or extended-thinking Pro model in ChatGPT, send one focused prompt, wait for the answer, and bring the useful guidance back into Codex.

This project is unofficial and is not affiliated with OpenAI. ChatGPT, GPT, OpenAI, and related marks are trademarks of OpenAI.

## What You Get

- One canonical `oracle` skill.
- Computer Use + Chrome as the default path.
- A prompt shape for second-opinion engineering and product decisions.
- Guardrails against using logged-out, free, in-app-browser, or non-Pro surfaces.
- Legacy static dossier scripts preserved only for explicit bundle requests.

## Use With Codex

Install SWE Stack as a Codex marketplace, then install the `oracle` plugin from the Plugins screen.

```bash
codex plugin marketplace add PedroAVJ/swe-stack --ref main --sparse .agents/plugins --sparse plugins/oracle
codex plugin marketplace upgrade
```

In the Codex app, the equivalent Add marketplace values are:

```text
Source: PedroAVJ/swe-stack
Git ref: main
Sparse paths:
.agents/plugins
plugins/oracle
```

If you already installed SWE Stack for another plugin, add `plugins/oracle` to the sparse paths or leave sparse paths blank, then run `codex plugin marketplace upgrade`.

## Oracle Flow

Use Oracle when you want a high-quality second opinion:

```text
Ask Oracle to sanity-check this architecture decision.
Use Oracle for a second opinion on this bug.
Run this implementation plan by ChatGPT Pro.
```

The skill requires the user's logged-in ChatGPT session in Chrome and will not automate login challenges, CAPTCHAs, credential prompts, or account setup.

## Privacy And Source Checks

Oracle is a reasoning surface, not a replacement for local source-of-truth checks. The skill instructs agents to inspect local files, diffs, logs, docs, tickets, messages, or deployment state first, then send only the verified context needed for the second opinion.

If the prompt would transmit sensitive private data to ChatGPT and that transmission has not been approved, the agent should ask before sending.

## Claude Code

This plugin includes a Claude-compatible manifest, but the primary browser automation workflow is Codex-specific because it depends on Codex Computer Use controlling the local Chrome app.
