# Android Phone

Android Phone is a local Codex plugin for inspecting, testing, debugging, and
controlling developer-authorized Android phones through ADB.

It is intentionally small and inspectable. The MCP server uses only the Python
standard library and the local `adb` binary.

This is an unofficial plugin and is not affiliated with Google or Android.

## Requirements

- Android Developer options enabled.
- USB debugging or Wireless debugging enabled.
- For Xiaomi/Redmi/MIUI/HyperOS devices, `USB debugging (Security settings)`
  may be required for tap, swipe, type, and key-event tools.
- A paired/connected ADB device visible in `adb devices`.

## Tools

- `list_devices`
- `connect_wifi`
- `disconnect`
- `get_device_info`
- `screenshot`
- `dump_ui`
- `tap`
- `long_press`
- `swipe`
- `type_text`
- `press_key`
- `press_back`
- `press_home`
- `current_app`
- `launch_app`
- `list_apps`

## Safety

Typing into a phone can transmit sensitive data if the focused field belongs to
a web page, messaging app, payment app, or account form. Agents must follow the
normal confirmation policy before typing sensitive data, sending messages,
submitting forms, making purchases, changing sharing/access, deleting data, or
performing other irreversible actions.
