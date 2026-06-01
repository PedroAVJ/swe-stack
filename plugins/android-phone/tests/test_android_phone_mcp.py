#!/usr/bin/env python3
"""Tiny smoke tests for the Android Phone MCP server."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "scripts" / "android_phone_mcp.py"


def request(process: subprocess.Popen[bytes], message: dict) -> dict:
    process.stdin.write(json.dumps(message).encode("utf-8") + b"\n")
    process.stdin.flush()
    line = process.stdout.readline()
    assert line, "server produced no response"
    return json.loads(line)


def main() -> int:
    process = subprocess.Popen(
        [sys.executable, str(SERVER)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None
    assert process.stdout is not None

    init = request(
        process,
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05"}},
    )
    assert init["result"]["serverInfo"]["name"] == "android-phone"

    tools = request(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    names = {tool["name"] for tool in tools["result"]["tools"]}
    assert "screenshot" in names
    assert "tap" in names
    assert "type_text" in names
    assert "connect_wifi" in names

    process.stdin.close()
    process.terminate()
    process.wait(timeout=5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
