#!/usr/bin/env python3
"""Small stdio MCP server for controlling Android phones through ADB."""

from __future__ import annotations

import base64
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Callable


ADB_PATH = os.environ.get("ADB_PATH", "adb")
DEFAULT_TIMEOUT = float(os.environ.get("ANDROID_PHONE_ADB_TIMEOUT", "20"))


class ToolError(Exception):
    pass


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    input_schema: dict[str, Any]
    handler: Callable[[dict[str, Any]], list[dict[str, Any]]]


def text_content(text: str) -> list[dict[str, Any]]:
    return [{"type": "text", "text": text}]


def image_content(data: bytes, mime_type: str = "image/png") -> list[dict[str, Any]]:
    return [{"type": "image", "data": base64.b64encode(data).decode("ascii"), "mimeType": mime_type}]


def adb_base(serial: str | None = None) -> list[str]:
    command = [ADB_PATH]
    if serial:
        command.extend(["-s", serial])
    return command


def run_adb(
    args: list[str],
    *,
    serial: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
    binary: bool = False,
) -> str | bytes:
    command = adb_base(serial) + args
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise ToolError(f"adb not found at {ADB_PATH!r}. Set ADB_PATH in the plugin MCP config.") from exc
    except subprocess.TimeoutExpired as exc:
        raise ToolError(f"adb command timed out: {shlex.join(command)}") from exc

    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        stdout = result.stdout.decode("utf-8", errors="replace").strip()
        detail = stderr or stdout or f"exit code {result.returncode}"
        raise ToolError(detail)

    if binary:
        return result.stdout

    return result.stdout.decode("utf-8", errors="replace").strip()


def parse_devices(output: str) -> list[dict[str, str]]:
    devices: list[dict[str, str]] = []
    for raw_line in output.splitlines()[1:]:
        line = raw_line.strip()
        if not line:
            continue
        fields = line.split()
        serial = fields[0]
        state = fields[1] if len(fields) > 1 else "unknown"
        details: dict[str, str] = {"serial": serial, "state": state}
        for field in fields[2:]:
            if ":" in field:
                key, value = field.split(":", 1)
                details[key] = value
        devices.append(details)
    return devices


def connected_device_serial(args: dict[str, Any] | None = None) -> str | None:
    if args:
        serial = args.get("serial")
        if isinstance(serial, str) and serial.strip():
            return serial.strip()

    env_serial = os.environ.get("ADB_SERIAL")
    if env_serial:
        return env_serial

    devices = [device for device in parse_devices(run_adb(["devices", "-l"])) if device.get("state") == "device"]
    if not devices:
        raise ToolError("No authorized ADB device is connected. Use connect_wifi or check Wireless debugging.")
    if len(devices) > 1:
        serials = ", ".join(device["serial"] for device in devices)
        raise ToolError(f"Multiple ADB devices are connected. Pass serial explicitly. Devices: {serials}")
    return devices[0]["serial"]


def optional_serial_schema() -> dict[str, Any]:
    return {
        "serial": {
            "type": "string",
            "description": "Optional ADB serial. Leave empty when exactly one device is connected.",
        }
    }


def tool_list_devices(args: dict[str, Any]) -> list[dict[str, Any]]:
    output = run_adb(["devices", "-l"])
    return text_content(json.dumps(parse_devices(output), indent=2))


def tool_connect_wifi(args: dict[str, Any]) -> list[dict[str, Any]]:
    address = require_string(args, "address")
    output = run_adb(["connect", address])
    return text_content(output)


def tool_disconnect(args: dict[str, Any]) -> list[dict[str, Any]]:
    address = args.get("address")
    if isinstance(address, str) and address.strip():
        output = run_adb(["disconnect", address.strip()])
    else:
        output = run_adb(["disconnect"])
    return text_content(output)


def get_prop(serial: str, prop: str) -> str:
    return run_adb(["shell", "getprop", prop], serial=serial)


def tool_get_device_info(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    props = {
        "serial": serial,
        "manufacturer": get_prop(serial, "ro.product.manufacturer"),
        "brand": get_prop(serial, "ro.product.brand"),
        "model": get_prop(serial, "ro.product.model"),
        "device": get_prop(serial, "ro.product.device"),
        "product": get_prop(serial, "ro.product.name"),
        "android_version": get_prop(serial, "ro.build.version.release"),
        "sdk": get_prop(serial, "ro.build.version.sdk"),
        "build_fingerprint": get_prop(serial, "ro.build.fingerprint"),
        "screen_size": run_adb(["shell", "wm", "size"], serial=serial),
        "screen_density": run_adb(["shell", "wm", "density"], serial=serial),
        "battery": run_adb(["shell", "dumpsys", "battery"], serial=serial),
    }
    return text_content(json.dumps(props, indent=2))


def tool_screenshot(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    data = run_adb(["exec-out", "screencap", "-p"], serial=serial, binary=True)
    return image_content(data)


def tool_dump_ui(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    run_adb(["shell", "uiautomator", "dump", "/sdcard/window.xml"], serial=serial)
    xml = run_adb(["exec-out", "cat", "/sdcard/window.xml"], serial=serial)
    return text_content(xml)


def tool_tap(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    x = require_int(args, "x")
    y = require_int(args, "y")
    output = run_adb(["shell", "input", "tap", str(x), str(y)], serial=serial)
    return text_content(output or f"Tapped {x},{y}")


def tool_long_press(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    x = require_int(args, "x")
    y = require_int(args, "y")
    duration_ms = int(args.get("duration_ms", 650))
    output = run_adb(
        ["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms)],
        serial=serial,
    )
    return text_content(output or f"Long-pressed {x},{y} for {duration_ms}ms")


def tool_swipe(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    x1 = require_int(args, "x1")
    y1 = require_int(args, "y1")
    x2 = require_int(args, "x2")
    y2 = require_int(args, "y2")
    duration_ms = int(args.get("duration_ms", 300))
    output = run_adb(
        ["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration_ms)],
        serial=serial,
    )
    return text_content(output or f"Swiped {x1},{y1} -> {x2},{y2} for {duration_ms}ms")


def encode_adb_text(value: str) -> str:
    # `adb shell input text` uses %s for spaces and has a limited character set.
    value = value.replace("%", "%25")
    return value.replace(" ", "%s")


def tool_type_text(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    value = require_string(args, "text")
    output = run_adb(["shell", "input", "text", encode_adb_text(value)], serial=serial)
    return text_content(output or "Typed text into the focused field")


KEY_ALIASES = {
    "back": "KEYCODE_BACK",
    "home": "KEYCODE_HOME",
    "enter": "KEYCODE_ENTER",
    "delete": "KEYCODE_DEL",
    "backspace": "KEYCODE_DEL",
    "space": "KEYCODE_SPACE",
    "tab": "KEYCODE_TAB",
    "escape": "KEYCODE_ESCAPE",
    "power": "KEYCODE_POWER",
    "wake": "KEYCODE_WAKEUP",
    "menu": "KEYCODE_MENU",
    "app_switch": "KEYCODE_APP_SWITCH",
}


def normalize_key(value: str) -> str:
    key = value.strip()
    if not key:
        raise ToolError("key must not be empty")
    lowered = key.lower()
    if lowered in KEY_ALIASES:
        return KEY_ALIASES[lowered]
    if key.isdigit():
        return key
    if key.startswith("KEYCODE_"):
        return key
    return "KEYCODE_" + key.upper()


def tool_press_key(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    key = normalize_key(require_string(args, "key"))
    output = run_adb(["shell", "input", "keyevent", key], serial=serial)
    return text_content(output or f"Pressed {key}")


def tool_press_back(args: dict[str, Any]) -> list[dict[str, Any]]:
    args = dict(args)
    args["key"] = "back"
    return tool_press_key(args)


def tool_press_home(args: dict[str, Any]) -> list[dict[str, Any]]:
    args = dict(args)
    args["key"] = "home"
    return tool_press_key(args)


def tool_current_app(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    focus = run_adb(["shell", "dumpsys", "window"], serial=serial, timeout=30)
    matches = [
        line.strip()
        for line in focus.splitlines()
        if "mCurrentFocus" in line or "mFocusedApp" in line or "topResumedActivity" in line
    ]
    return text_content("\n".join(matches) or "No focused app line found")


def tool_launch_app(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    package = require_string(args, "package")
    output = run_adb(
        ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"],
        serial=serial,
    )
    return text_content(output)


def tool_list_apps(args: dict[str, Any]) -> list[dict[str, Any]]:
    serial = connected_device_serial(args)
    include_system = bool(args.get("include_system", False))
    flags = ["packages"] if include_system else ["packages", "-3"]
    output = run_adb(["shell", "cmd", "package", "list", *flags], serial=serial, timeout=40)
    packages = [line.removeprefix("package:") for line in output.splitlines() if line.strip()]
    return text_content(json.dumps(packages, indent=2))


def require_string(args: dict[str, Any], key: str) -> str:
    value = args.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ToolError(f"{key} must be a non-empty string")
    return value.strip()


def require_int(args: dict[str, Any], key: str) -> int:
    value = args.get(key)
    if isinstance(value, bool):
        raise ToolError(f"{key} must be an integer")
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    raise ToolError(f"{key} must be an integer")


def object_schema(properties: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required or [],
        "additionalProperties": False,
    }


def number_property(description: str) -> dict[str, Any]:
    return {"type": "integer", "description": description}


TOOLS: dict[str, Tool] = {
    "list_devices": Tool(
        "list_devices",
        "List Android devices visible to ADB.",
        object_schema({}),
        tool_list_devices,
    ),
    "connect_wifi": Tool(
        "connect_wifi",
        "Connect to an already-paired Wireless debugging endpoint such as 192.168.1.144:36853.",
        object_schema({"address": {"type": "string", "description": "ADB connect endpoint, host:port."}}, ["address"]),
        tool_connect_wifi,
    ),
    "disconnect": Tool(
        "disconnect",
        "Disconnect one ADB endpoint, or all TCP endpoints if no address is provided.",
        object_schema({"address": {"type": "string", "description": "Optional ADB endpoint, host:port."}}),
        tool_disconnect,
    ),
    "get_device_info": Tool(
        "get_device_info",
        "Read Android model, build, display, and battery metadata for the connected device.",
        object_schema(optional_serial_schema()),
        tool_get_device_info,
    ),
    "screenshot": Tool(
        "screenshot",
        "Take a PNG screenshot of the connected Android device.",
        object_schema(optional_serial_schema()),
        tool_screenshot,
    ),
    "dump_ui": Tool(
        "dump_ui",
        "Dump the current Android UIAutomator XML tree, including visible text and element bounds.",
        object_schema(optional_serial_schema()),
        tool_dump_ui,
    ),
    "tap": Tool(
        "tap",
        "Tap the Android screen at pixel coordinates.",
        object_schema({**optional_serial_schema(), "x": number_property("X coordinate."), "y": number_property("Y coordinate.")}, ["x", "y"]),
        tool_tap,
    ),
    "long_press": Tool(
        "long_press",
        "Long-press the Android screen at pixel coordinates.",
        object_schema({**optional_serial_schema(), "x": number_property("X coordinate."), "y": number_property("Y coordinate."), "duration_ms": number_property("Duration in milliseconds.")}, ["x", "y"]),
        tool_long_press,
    ),
    "swipe": Tool(
        "swipe",
        "Swipe between Android screen coordinates.",
        object_schema(
            {
                **optional_serial_schema(),
                "x1": number_property("Start X coordinate."),
                "y1": number_property("Start Y coordinate."),
                "x2": number_property("End X coordinate."),
                "y2": number_property("End Y coordinate."),
                "duration_ms": number_property("Duration in milliseconds."),
            },
            ["x1", "y1", "x2", "y2"],
        ),
        tool_swipe,
    ),
    "type_text": Tool(
        "type_text",
        "Type literal text into the focused Android field. Sensitive-data confirmations apply before use.",
        object_schema({**optional_serial_schema(), "text": {"type": "string", "description": "Text to type into the focused field."}}, ["text"]),
        tool_type_text,
    ),
    "press_key": Tool(
        "press_key",
        "Press an Android key by alias, keycode name, or numeric keycode.",
        object_schema({**optional_serial_schema(), "key": {"type": "string", "description": "Examples: back, home, enter, KEYCODE_APP_SWITCH, 187."}}, ["key"]),
        tool_press_key,
    ),
    "press_back": Tool(
        "press_back",
        "Press Android Back.",
        object_schema(optional_serial_schema()),
        tool_press_back,
    ),
    "press_home": Tool(
        "press_home",
        "Press Android Home.",
        object_schema(optional_serial_schema()),
        tool_press_home,
    ),
    "current_app": Tool(
        "current_app",
        "Read the currently focused Android app/activity from dumpsys window.",
        object_schema(optional_serial_schema()),
        tool_current_app,
    ),
    "launch_app": Tool(
        "launch_app",
        "Launch an Android app by package name.",
        object_schema({**optional_serial_schema(), "package": {"type": "string", "description": "Android package name, for example com.android.settings."}}, ["package"]),
        tool_launch_app,
    ),
    "list_apps": Tool(
        "list_apps",
        "List installed Android packages. Defaults to third-party packages only.",
        object_schema({**optional_serial_schema(), "include_system": {"type": "boolean", "description": "Include system packages."}}),
        tool_list_apps,
    ),
}


def tool_metadata() -> list[dict[str, Any]]:
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "inputSchema": tool.input_schema,
        }
        for tool in TOOLS.values()
    ]


def handle_request(message: dict[str, Any]) -> dict[str, Any] | None:
    request_id = message.get("id")
    method = message.get("method")
    params = message.get("params") or {}

    if request_id is None:
        return None

    try:
        if method == "initialize":
            requested_version = params.get("protocolVersion") if isinstance(params, dict) else None
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": requested_version or "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "android-phone", "version": "0.1.0"},
                },
            }
        if method == "ping":
            return {"jsonrpc": "2.0", "id": request_id, "result": {}}
        if method == "tools/list":
            return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": tool_metadata()}}
        if method == "tools/call":
            if not isinstance(params, dict):
                raise ToolError("tools/call params must be an object")
            name = params.get("name")
            arguments = params.get("arguments") or {}
            if not isinstance(name, str) or name not in TOOLS:
                raise ToolError(f"Unknown tool: {name}")
            if not isinstance(arguments, dict):
                raise ToolError("tool arguments must be an object")
            content = TOOLS[name].handler(arguments)
            return {"jsonrpc": "2.0", "id": request_id, "result": {"content": content, "isError": False}}
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }
    except Exception as exc:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": text_content(str(exc)), "isError": True},
        }


def read_message(stdin: Any) -> dict[str, Any] | None:
    line = stdin.readline()
    if not line:
        return None
    line = line.rstrip(b"\r\n")
    if not line:
        return {}
    if line.lower().startswith(b"content-length:"):
        length = int(line.split(b":", 1)[1].strip())
        while True:
            header = stdin.readline()
            if not header or header in (b"\n", b"\r\n"):
                break
        payload = stdin.read(length)
        return json.loads(payload.decode("utf-8"))
    return json.loads(line.decode("utf-8"))


def write_message(stdout: Any, message: dict[str, Any]) -> None:
    encoded = json.dumps(message, separators=(",", ":")).encode("utf-8")
    stdout.write(encoded + b"\n")
    stdout.flush()


def main() -> int:
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    while True:
        try:
            message = read_message(stdin)
        except Exception as exc:
            print(f"android-phone: failed to read message: {exc}", file=sys.stderr)
            return 1
        if message is None:
            return 0
        if not message:
            continue
        response = handle_request(message)
        if response is not None:
            write_message(stdout, response)


if __name__ == "__main__":
    raise SystemExit(main())
