#!/usr/bin/env python3
"""Profile wall-clock time for a Codex turn from a rollout JSONL file."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


TERMINAL_EVENT_TYPES = {"task_complete", "turn_aborted"}
CALL_TYPES = {"custom_tool_call", "function_call"}
OUTPUT_TYPES = {"custom_tool_call_output", "function_call_output"}


def parse_timestamp(value: str) -> float:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()


def format_duration(seconds: float) -> str:
    seconds = max(0.0, seconds)
    minutes, remainder = divmod(seconds, 60)
    hours, minutes = divmod(int(minutes), 60)
    if hours:
        return f"{hours}h {minutes:02d}m {remainder:04.1f}s"
    if minutes:
        return f"{minutes}m {remainder:04.1f}s"
    return f"{remainder:.3f}s"


def shorten(text: str, limit: int = 96) -> str:
    normalized = " ".join(text.split())
    return normalized if len(normalized) <= limit else normalized[: limit - 1] + "…"


@dataclass
class Turn:
    turn_id: str
    start_ts: float
    start_iso: str
    end_ts: float | None = None
    end_iso: str | None = None
    status: str = "running"
    duration_ms: int | None = None
    ttft_ms: int | None = None
    prompt: str = ""

    @property
    def duration_seconds(self) -> float:
        if self.duration_ms is not None:
            return self.duration_ms / 1000
        if self.end_ts is not None:
            return self.end_ts - self.start_ts
        return 0.0


@dataclass
class CallInterval:
    call_id: str
    start: float
    end: float
    category: str
    label: str
    tool_name: str

    @property
    def seconds(self) -> float:
        return max(0.0, self.end - self.start)


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number}: {exc}") from exc
            if "timestamp" in event:
                event["_ts"] = parse_timestamp(event["timestamp"])
            events.append(event)
    return events


def collect_turns(events: Iterable[dict[str, Any]]) -> list[Turn]:
    turns: dict[str, Turn] = {}
    order: list[str] = []
    active_turn_id: str | None = None

    for event in events:
        if event.get("type") != "event_msg":
            continue
        payload = event.get("payload", {})
        event_type = payload.get("type")
        turn_id = payload.get("turn_id")

        if event_type == "task_started" and turn_id:
            turns[turn_id] = Turn(
                turn_id=turn_id,
                start_ts=event["_ts"],
                start_iso=event["timestamp"],
            )
            order.append(turn_id)
            active_turn_id = turn_id
        elif event_type == "user_message" and active_turn_id in turns:
            turns[active_turn_id].prompt = payload.get("message", "")
        elif event_type in TERMINAL_EVENT_TYPES and turn_id in turns:
            turn = turns[turn_id]
            turn.end_ts = event["_ts"]
            turn.end_iso = event["timestamp"]
            turn.status = "complete" if event_type == "task_complete" else "aborted"
            turn.duration_ms = payload.get("duration_ms")
            turn.ttft_ms = payload.get("time_to_first_token_ms")
            if active_turn_id == turn_id:
                active_turn_id = None

    return [turns[turn_id] for turn_id in order]


def classify_call(payload: dict[str, Any]) -> tuple[str, str]:
    tool_name = str(payload.get("name") or "tool")
    raw = str(payload.get("input") or payload.get("arguments") or "")
    lowered = raw.lower()

    rules = [
        ("Browser E2E", "Playwright browser", ("playwright_cli.sh", "playwright", "browser__")),
        ("External agent", "Secondary-agent pass", ("run_design_pass.py", "claude -p", " claude ")),
        ("Backend tests", "Backend test run", ("dotnet test",)),
        ("Frontend tests", "Frontend test run", ("vitest", "npm test", "pnpm test", "pnpm --dir nova test")),
        ("Server startup", "Development server", ("dotnet run", "npm run dev", "pnpm dev", "vite --host")),
        ("Deploy/release", "Deployment or release", ("az pipelines", "az repos pr", "zipdeploy", "kudu", "static web app", "vercel deploy", "git push")),
        ("Code edits", "Repository edit", ("tools.apply_patch", "apply_patch")),
        ("Install/setup", "Tool setup", ("install-browser", "npm install", "pnpm install", "npx playwright install")),
        ("Wait/poll", "Process wait", ("tools.wait", "write_stdin", "wait_agent")),
        ("Network/API", "Network or API call", ("tools.web__run", "curl ", "mcp__")),
        ("Source inspection", "Repository inspection", ("rg ", "sed -n", "git diff", "git status", "git log", "find ", "ls ")),
    ]
    for category, label, needles in rules:
        if any(needle in lowered for needle in needles):
            return category, label

    if tool_name in {"wait", "write_stdin"}:
        return "Wait/poll", "Process wait"
    if tool_name in {"request_user_input"}:
        return "Approval/input", "User input"
    return "Other tools", tool_name


def collect_calls(
    events: Iterable[dict[str, Any]], turn: Turn
) -> tuple[list[CallInterval], Counter[str]]:
    starts: dict[str, tuple[float, dict[str, Any]]] = {}
    calls: list[CallInterval] = []
    event_counts: Counter[str] = Counter()
    end_ts = turn.end_ts if turn.end_ts is not None else float("inf")

    for event in events:
        timestamp = event.get("_ts")
        if timestamp is None or timestamp < turn.start_ts or timestamp > end_ts:
            continue
        payload = event.get("payload", {})
        payload_type = payload.get("type")
        if payload_type:
            event_counts[str(payload_type)] += 1
        call_id = payload.get("call_id")
        if payload_type in CALL_TYPES and call_id:
            starts[call_id] = (timestamp, payload)
        elif payload_type in OUTPUT_TYPES and call_id in starts:
            start, call_payload = starts.pop(call_id)
            category, label = classify_call(call_payload)
            calls.append(
                CallInterval(
                    call_id=call_id,
                    start=start,
                    end=timestamp,
                    category=category,
                    label=label,
                    tool_name=str(call_payload.get("name") or "tool"),
                )
            )
    return calls, event_counts


def union_seconds(intervals: Iterable[CallInterval]) -> float:
    ordered = sorted((item.start, item.end) for item in intervals if item.end >= item.start)
    if not ordered:
        return 0.0
    total = 0.0
    start, end = ordered[0]
    for next_start, next_end in ordered[1:]:
        if next_start <= end:
            end = max(end, next_end)
        else:
            total += end - start
            start, end = next_start, next_end
    return total + end - start


def build_profile(events: list[dict[str, Any]], turn: Turn, top: int) -> dict[str, Any]:
    calls, event_counts = collect_calls(events, turn)
    total = turn.duration_seconds
    measured_tool_wall = union_seconds(calls)
    residual = max(0.0, total - measured_tool_wall)
    category_seconds: defaultdict[str, float] = defaultdict(float)
    category_calls: Counter[str] = Counter()
    for call in calls:
        category_seconds[call.category] += call.seconds
        category_calls[call.category] += 1

    categories = [
        {
            "category": category,
            "seconds": round(seconds, 3),
            "percent_of_turn": round((seconds / total * 100) if total else 0.0, 1),
            "calls": category_calls[category],
        }
        for category, seconds in sorted(
            category_seconds.items(), key=lambda item: item[1], reverse=True
        )
    ]
    slowest = [
        {
            "category": call.category,
            "label": call.label,
            "tool": call.tool_name,
            "seconds": round(call.seconds, 3),
        }
        for call in sorted(calls, key=lambda item: item.seconds, reverse=True)[:top]
    ]

    return {
        "turn_id": turn.turn_id,
        "status": turn.status,
        "prompt": shorten(turn.prompt),
        "started_at": turn.start_iso,
        "completed_at": turn.end_iso,
        "total_seconds": round(total, 3),
        "time_to_first_token_seconds": (
            round(turn.ttft_ms / 1000, 3) if turn.ttft_ms is not None else None
        ),
        "paired_tool_calls": len(calls),
        "measured_tool_wall_seconds": round(measured_tool_wall, 3),
        "measured_tool_wall_percent": round(
            (measured_tool_wall / total * 100) if total else 0.0, 1
        ),
        "agent_model_orchestration_residual_seconds": round(residual, 3),
        "agent_model_orchestration_residual_percent": round(
            (residual / total * 100) if total else 0.0, 1
        ),
        "reasoning_items": event_counts.get("reasoning", 0),
        "assistant_messages": event_counts.get("message", 0),
        "categories": categories,
        "slowest_calls": slowest,
        "caveat": (
            "The residual is wall time outside paired local tool calls; it is not "
            "an authoritative server-side model-inference measurement."
        ),
    }


def print_turns(turns: list[Turn]) -> None:
    for turn in turns:
        print(
            f"{turn.turn_id}  {turn.status:8}  "
            f"{format_duration(turn.duration_seconds):>12}  {shorten(turn.prompt, 80)}"
        )


def print_profile(profile: dict[str, Any]) -> None:
    total = profile["total_seconds"]
    print(f"Turn: {profile['turn_id']} ({profile['status']})")
    print(f"Prompt: {profile['prompt']}")
    print(f"Total: {format_duration(total)}")
    if profile["time_to_first_token_seconds"] is not None:
        print(
            "Time to first token: "
            + format_duration(profile["time_to_first_token_seconds"])
        )
    print(
        "Measured tool wall: "
        f"{format_duration(profile['measured_tool_wall_seconds'])} "
        f"({profile['measured_tool_wall_percent']}%) across "
        f"{profile['paired_tool_calls']} calls"
    )
    print(
        "Agent/model/orchestration residual: "
        f"{format_duration(profile['agent_model_orchestration_residual_seconds'])} "
        f"({profile['agent_model_orchestration_residual_percent']}%)"
    )
    print("\nMeasured tool categories:")
    for item in profile["categories"]:
        print(
            f"  {item['category']:<20} {format_duration(item['seconds']):>12}  "
            f"{item['percent_of_turn']:>5.1f}%  {item['calls']:>3} calls"
        )
    print("\nSlowest paired calls:")
    for item in profile["slowest_calls"]:
        print(
            f"  {format_duration(item['seconds']):>12}  "
            f"{item['category']} — {item['label']}"
        )
    print("\nCaveat: " + profile["caveat"])


def choose_turn(turns: list[Turn], args: argparse.Namespace) -> Turn:
    if args.turn_id:
        matches = [turn for turn in turns if turn.turn_id == args.turn_id]
    elif args.contains:
        needle = args.contains.casefold()
        matches = [turn for turn in turns if needle in turn.prompt.casefold()]
    else:
        matches = [turn for turn in turns if turn.status != "running"]
    if not matches:
        raise ValueError("No matching completed or interrupted turn found")
    return matches[-1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile a Codex turn from a rollout JSONL session log."
    )
    parser.add_argument("session", type=Path, help="Path to rollout JSONL")
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument("--turn-id", help="Exact Codex turn ID")
    selector.add_argument("--contains", help="Case-insensitive prompt substring")
    parser.add_argument("--list", action="store_true", help="List turns and exit")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--top", type=int, default=10, help="Number of slow calls")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        events = load_events(args.session.expanduser())
        turns = collect_turns(events)
        if args.list:
            print_turns(turns)
            return 0
        profile = build_profile(events, choose_turn(turns, args), max(0, args.top))
        if args.json:
            print(json.dumps(profile, indent=2))
        else:
            print_profile(profile)
        return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
