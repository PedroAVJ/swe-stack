#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time


PLUGIN_ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATES = {
    "handoff": PLUGIN_ROOT / "templates" / "frontend-handoff.md",
    "implement": PLUGIN_ROOT / "templates" / "frontend-implementation.md",
}
DEFAULT_LOG_ROOT = pathlib.Path.home() / ".local" / "share" / "claude-plugin" / "design-logs"


def extract_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if not isinstance(item, dict):
                continue
            if item.get("type") in {"text", "text_delta"} and item.get("text"):
                parts.append(item["text"])
            elif item.get("delta", {}).get("text"):
                parts.append(item["delta"]["text"])
        return "".join(parts)
    return ""


def print_event(event):
    event_type = event.get("type") or event.get("event")

    if event_type in {"assistant", "message"}:
        message = event.get("message", event)
        text = extract_text(message.get("content") or event.get("content"))
        if text:
            print(text, end="", flush=True)
        return

    if event_type in {"content_block_delta", "text_delta"}:
        text = event.get("delta", {}).get("text") or event.get("text")
        if text:
            print(text, end="", flush=True)
        return

    if event_type in {"tool_use", "tool_result"}:
        name = event.get("name") or event.get("tool_name") or event.get("id") or "tool"
        print(f"\n[claude:{event_type}] {name}", flush=True)
        return

    if event_type in {"error", "result"}:
        print(f"\n[claude:{event_type}] {event.get('subtype') or event.get('message') or ''}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Run a streamed Claude frontend collaboration pass.")
    parser.add_argument("--repo", required=True, help="Repo path Claude may read.")
    parser.add_argument(
        "--mode",
        choices=sorted(DEFAULT_TEMPLATES),
        default="implement",
        help="Pass type. 'implement' lets Claude own the UI edit pass; 'handoff' is read-only guidance.",
    )
    parser.add_argument("--prompt-file", default="", help="Base prompt/template file.")
    parser.add_argument("--prompt", default="", help="Extra prompt appended after the prompt file.")
    parser.add_argument("--log-root", default=str(DEFAULT_LOG_ROOT), help="Directory for raw stream and debug logs.")
    parser.add_argument("--model", default="", help="Optional Claude model alias/name.")
    parser.add_argument("--effort", default="medium", help="Claude effort level.")
    parser.add_argument("--allow-edits", action="store_true", help="Allow edit/write tools. Default is read-only handoff.")
    args = parser.parse_args()

    repo = pathlib.Path(args.repo).expanduser().resolve()
    prompt_file = args.prompt_file or str(DEFAULT_TEMPLATES[args.mode])
    prompt_path = pathlib.Path(prompt_file).expanduser().resolve()
    log_root = pathlib.Path(args.log_root).expanduser().resolve()
    log_root.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y%m%d-%H%M%S")
    raw_log = log_root / f"{stamp}-stream.jsonl"
    debug_log = log_root / f"{stamp}-debug.log"

    prompt = prompt_path.read_text()
    if args.prompt:
        prompt = f"{prompt}\n\nProject-specific request:\n{args.prompt}\n"

    tools = "Read,Glob,Grep,LS"
    permission_mode = "plan"
    if args.mode == "implement" or args.allow_edits:
        tools = "Read,Glob,Grep,LS,Edit,MultiEdit,Write"
        permission_mode = "acceptEdits"

    cmd = [
        "claude",
        "-p",
        "--output-format=stream-json",
        "--include-partial-messages",
        "--verbose",
        "--debug-file",
        str(debug_log),
        "--add-dir",
        str(repo),
        "--permission-mode",
        permission_mode,
        "--tools",
        tools,
        "--effort",
        args.effort,
    ]
    if args.model:
        cmd.extend(["--model", args.model])
    cmd.append(prompt)

    print(f"[claude-run] repo: {repo}")
    print(f"[claude-run] codex plugin: {PLUGIN_ROOT}")
    print(f"[claude-run] mode: {args.mode}")
    print(f"[claude-run] stream log: {raw_log}")
    print(f"[claude-run] debug log: {debug_log}")
    print()

    process = subprocess.Popen(
        cmd,
        cwd=str(repo),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=os.environ.copy(),
    )

    with raw_log.open("w") as raw:
        assert process.stdout is not None
        for line in process.stdout:
            raw.write(line)
            raw.flush()
            stripped = line.strip()
            if not stripped:
                continue
            try:
                event = json.loads(stripped)
            except json.JSONDecodeError:
                print(stripped, flush=True)
                continue
            print_event(event)

    return_code = process.wait()
    print(f"\n[claude-run] exit code: {return_code}")
    return return_code


if __name__ == "__main__":
    sys.exit(main())
