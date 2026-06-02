#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path
import selectors
import subprocess
import time


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ask Claude to generate a standalone HTML change preview."
    )
    parser.add_argument("--workspace", default=".", help="Trusted workspace root.")
    parser.add_argument(
        "--target",
        required=False,
        help="PR, issue, commit, branch, or natural-language target to preview.",
    )
    parser.add_argument("--brief", help="Markdown brief produced by the runner.")
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="Evidence artifact path such as a screenshot, video, trace, or note.",
    )
    parser.add_argument(
        "--mode",
        default="change",
        help="Preview mode label for caller bookkeeping; Claude still decides the artifact direction.",
    )
    parser.add_argument("--output", required=True, help="HTML output path.")
    parser.add_argument("--log", help="Claude output log path.")
    parser.add_argument("--jsonl-log", help="Raw Claude stream JSONL log path.")
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=int(os.environ.get("CHANGE_PREVIEW_TIMEOUT_SECONDS", "1800")),
        help="Maximum time to let Claude generate the preview. Defaults to 30 minutes.",
    )
    args = parser.parse_args()
    if not args.target and not args.brief:
        parser.error("one of --target or --brief is required")
    return args


def build_prompt(target, brief_path, evidence_paths, mode, output_path):
    target_text = target or f"the runner brief at {Path(brief_path).resolve()}"
    brief_text = ""
    if brief_path:
        brief_text = f"\nRunner brief: {Path(brief_path).resolve()}\n"
    evidence_text = ""
    if evidence_paths:
        evidence_lines = "\n".join(f"- {Path(path).resolve()}" for path in evidence_paths)
        evidence_text = f"\nAvailable evidence:\n{evidence_lines}\n"

    return f"""Use your `frontend-design` skill.

Generate a standalone HTML change preview for: {target_text}

Output path: {Path(output_path).resolve()}
Mode: {mode}
{brief_text}{evidence_text}

Inspect the workspace, git history/diff, PR metadata, tests, app artifacts, and available evidence yourself.

Rough intent: this is a Pedro-facing comprehension artifact. It is not approval gating and it is not internal verification evidence. Help him quickly understand what changed, why it matters, and what the shipped behavior feels like.

You own the visual/editorial direction. Decide whether to use real screenshots, mockups, diagrams, timelines, examples, small interactions, or any other presentation that makes the change easy to parse. Do not ask the caller to choose sections, media, mockups, or visual direction.

Responsive contract: the generated HTML must look good on both a MacBook-sized viewport and an iPhone-sized viewport. Build mobile-first, include `meta viewport`, use fluid type/spacing, stack multi-column grids on narrow screens, avoid fixed-width panels, prevent horizontal scrolling, and ensure long issue titles, code labels, pills, tables, and diagram text wrap inside their containers.

If the output path already exists, replace it from scratch. Do not patch, preserve, or visually imitate a previous non-responsive preview. Previous preview links in handoff text are historical evidence only, not a design source.

Write the HTML file and return a short completion note.
"""


def summarize_stream_event(event):
    event_type = event.get("type")

    if event_type == "stream_event":
        stream_event = event.get("event") or {}
        stream_type = stream_event.get("type")
        if stream_type == "content_block_start":
            block = stream_event.get("content_block") or {}
            if block.get("type") == "tool_use":
                return f"tool_use started: {block.get('name', 'tool')}"
        return None

    if event_type == "rate_limit_event":
        info = event.get("rate_limit_info") or {}
        status = info.get("status")
        limit_type = info.get("rateLimitType")
        if status:
            return f"rate_limit: {status}" + (f" ({limit_type})" if limit_type else "")
        return None

    if event_type == "system":
        subtype = event.get("subtype")
        session_id = event.get("session_id")
        return f"system: {subtype or 'event'}" + (f" session={session_id}" if session_id else "")

    if event_type == "assistant":
        message = event.get("message") or {}
        parts = []
        for block in message.get("content") or []:
            block_type = block.get("type")
            if block_type == "text" and block.get("text"):
                parts.append(block["text"].strip())
            elif block_type == "tool_use":
                name = block.get("name", "tool")
                tool_input = block.get("input")
                if isinstance(tool_input, dict):
                    detail = tool_input.get("description") or tool_input.get("command") or ""
                    detail = str(detail).replace("\n", " ")[:240]
                    parts.append(f"tool_use: {name}" + (f" - {detail}" if detail else ""))
                else:
                    parts.append(f"tool_use: {name}")
        return "\n".join(part for part in parts if part)

    if event_type == "user":
        message = event.get("message") or {}
        content = message.get("content")
        if isinstance(content, list):
            results = []
            for block in content:
                if block.get("type") == "tool_result":
                    status = "error" if block.get("is_error") else "ok"
                    text = str(block.get("content") or "").replace("\n", " ")[:240]
                    results.append(f"tool_result: {status}" + (f" - {text}" if text else ""))
            return "\n".join(results)
        return None

    if event_type == "result":
        subtype = event.get("subtype")
        duration_ms = event.get("duration_ms")
        cost = event.get("total_cost_usd")
        result = str(event.get("result") or "").strip()
        pieces = [f"result: {subtype or 'done'}"]
        if duration_ms is not None:
            pieces.append(f"{duration_ms / 1000:.1f}s")
        if cost is not None:
            pieces.append(f"${cost:.4f}")
        if result:
            pieces.append(result[:500])
        return " | ".join(pieces)

    if event_type:
        return f"{event_type}: {json.dumps(event, ensure_ascii=False)[:500]}"

    return None


def terminate_process(proc):
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)


def run_claude(workspace, prompt, log_path, jsonl_log_path, timeout_seconds):
    command = [
        "claude",
        "-p",
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "stream-json",
        "--include-partial-messages",
        "--verbose",
        "-",
    ]

    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    Path(jsonl_log_path).parent.mkdir(parents=True, exist_ok=True)

    proc = subprocess.Popen(
        command,
        cwd=workspace,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert proc.stdin is not None
    assert proc.stdout is not None
    proc.stdin.write(prompt)
    proc.stdin.close()

    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ)
    start = time.monotonic()
    last_progress = start
    result_seen_at = None
    terminated_after_result = False

    try:
        with open(log_path, "w", encoding="utf-8") as log_file, open(
            jsonl_log_path, "w", encoding="utf-8"
        ) as jsonl_file:
            def note(message):
                elapsed = time.monotonic() - start
                line = f"[{elapsed:7.1f}s] {message}"
                print(line, flush=True)
                log_file.write(line + "\n")
                log_file.flush()

            note("started Claude preview generation")

            stream_done = False
            while True:
                if timeout_seconds and time.monotonic() - start > timeout_seconds:
                    note(f"timeout after {timeout_seconds}s; terminating Claude")
                    terminate_process(proc)
                    raise SystemExit(
                        f"Claude preview generation timed out after {timeout_seconds}s; "
                        f"see {log_path} and {jsonl_log_path}"
                    )

                events = selector.select(timeout=1)
                if not events:
                    if proc.poll() is not None:
                        break
                    if result_seen_at and time.monotonic() - result_seen_at > 5:
                        note("Claude reported a result but the CLI did not exit; terminating completed session")
                        terminate_process(proc)
                        terminated_after_result = True
                        break
                    now = time.monotonic()
                    if now - last_progress >= 60:
                        note("Claude still running; waiting for stream output or HTML completion")
                        last_progress = now
                    continue

                for key, _ in events:
                    line = key.fileobj.readline()
                    if not line:
                        if proc.poll() is not None:
                            stream_done = True
                            break
                        if result_seen_at and time.monotonic() - result_seen_at > 5:
                            note("Claude reported a result but the stream stayed open; terminating completed session")
                            terminate_process(proc)
                            terminated_after_result = True
                            stream_done = True
                            break
                        continue
                    jsonl_file.write(line)
                    jsonl_file.flush()

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        note(f"raw: {line.rstrip()}")
                        last_progress = time.monotonic()
                        continue

                    summary = summarize_stream_event(event)
                    if summary:
                        for summary_line in summary.splitlines():
                            if summary_line.strip():
                                note(summary_line.strip())
                        last_progress = time.monotonic()
                    if event.get("type") == "result":
                        result_seen_at = time.monotonic()
                if stream_done:
                    break

            returncode = proc.wait()
    finally:
        try:
            selector.close()
        except Exception:
            pass
        if proc.poll() is None:
            terminate_process(proc)

    if returncode != 0 and not terminated_after_result:
        raise SystemExit(
            f"Claude preview generation failed with status {returncode}; "
            f"see {log_path} and {jsonl_log_path}"
        )


def main():
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    output_path = Path(args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(
        args.target,
        args.brief,
        args.evidence,
        args.mode,
        output_path,
    )
    (output_path.parent / "change-preview-prompt.md").write_text(prompt, encoding="utf-8")
    log_path = args.log or str(output_path.parent / "change-preview-claude.log")
    jsonl_log_path = args.jsonl_log or str(
        output_path.parent / "change-preview-claude.stream.jsonl"
    )
    run_claude(workspace, prompt, log_path, jsonl_log_path, args.timeout_seconds)
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise SystemExit(
            f"Claude did not create a non-empty {output_path}; "
            f"see {log_path} and {jsonl_log_path}"
        )
    print(f"change-preview ok: {output_path}")


if __name__ == "__main__":
    main()
