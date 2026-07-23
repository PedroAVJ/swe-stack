---
name: codex-turn-profiler
description: Profile completed or interrupted OpenAI Codex turns from local rollout JSONL logs and explain where wall-clock time went. Use when a user asks why a Codex message, task, implementation, deployment, or tool-heavy turn took so long; wants per-turn duration, time-to-first-token, tool-call latency, slow-call ranking, or a TraceLens flamegraph; or needs to compare latency between Codex turns.
---

# Codex Turn Profiler

Profile the local evidence before explaining latency. Codex rollout files contain
exact event timestamps plus `task_complete.duration_ms` and
`time_to_first_token_ms`; they do not contain authoritative server-side model
inference spans.

## Workflow

1. Locate the relevant `rollout-*.jsonl` under
   `${CODEX_HOME:-$HOME/.codex}/sessions/` or `archived_sessions/`. Prefer the
   thread ID when available; otherwise search for a distinctive prompt phrase.
2. List turns in a candidate file:

   ```bash
   python3 scripts/profile_codex_turn.py SESSION.jsonl --list
   ```

3. Profile by turn ID or prompt text:

   ```bash
   python3 scripts/profile_codex_turn.py SESSION.jsonl --turn-id TURN_ID
   python3 scripts/profile_codex_turn.py SESSION.jsonl --contains "distinctive prompt text"
   ```

   Add `--json` when another tool will consume the result.
4. For a visual call tree or flamegraph, open
   [TraceLens](https://github.com/YuLeo926/tracelens) and load the rollout file
   locally. It supports saved Codex rollouts, waterfalls, slowest-span jumps,
   and duration-weighted flamegraphs. Prefer a local checkout for sensitive
   sessions; never publish or share a rollout without explicit approval.
5. Report the total duration first, then the largest measured tool categories,
   slowest calls, and the residual.

## Interpretation Rules

- Treat total duration, time-to-first-token, event timestamps, and paired tool
  call durations as measured facts.
- Describe `agent/model/orchestration residual` as an attribution boundary, not
  pure model inference. It is total wall time outside paired local tool calls
  and can include model generation, reasoning, message assembly, scheduling,
  approvals, and unpaired/background work.
- Do not add overlapping tool durations and call the result wall time. The
  script unions paired intervals for measured tool wall time.
- Explain high call counts and repeated browser round trips explicitly; many
  individually small calls can dominate a turn through both tool latency and
  reasoning between calls.
- Keep prompts, tool inputs, and outputs private by default. Report sanitized
  categories and timings unless the user asks for raw trace details.

## Output Shape

Lead with a concise verdict such as:

`31m 59.7s total: 11m 51.5s in measured tools and 20m 08.2s in the agent/model/orchestration residual. The largest measured bucket was browser E2E.`

Then distinguish avoidable workflow cost from necessary verification and name
the one or two changes most likely to reduce latency next time.
