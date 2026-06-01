---
name: android-phone
description: "Inspect, test, debug, and control Android phones through ADB from Codex. Use when the user asks to inspect, screenshot, tap, swipe, type, or otherwise control their Android phone."
---

# Android Phone

Use this skill when the user explicitly invokes Android Phone or asks to
inspect, control, test, debug, screenshot, navigate, type on, or automate their
Android phone.

Android Phone is the Android analogue of Computer / Browser:

- Computer controls macOS apps.
- Browser controls Codex's in-app browser.
- Android Phone controls a developer-authorized Android phone through ADB.

## Source Of Truth

Prefer the Android Phone MCP tools over clicking a scrcpy mirror window. The
mirror is useful for human visual feedback, but ADB is the control layer.

Use the tools in this order:

1. `list_devices` or `get_device_info` to confirm the target device.
2. `screenshot` for visual state.
3. `dump_ui` when structured UI text, bounds, or package/activity context is
   useful.
4. `tap`, `swipe`, `type_text`, `press_key`, `press_back`, or `press_home` for
   actions.
5. Re-observe with `screenshot` or `dump_ui` after meaningful actions.

If no device is connected but Wireless debugging is already paired, ask the
user for the current `IP address & Port` from the Wireless debugging screen and
use `connect_wifi`.

Do not ask the user for a wireless pairing code unless pairing is actually
needed. Pairing grants persistent debug access and should be handled explicitly.

## Safety

Treat the phone as the user's real local environment.

Before filling any form on the phone, check whether fields request credentials,
financial information, medical/legal information, contact details, precise
location, authorization codes, or activity/history-derived data. Typing
sensitive data into a phone app or web form counts as transmission if the app or
site can receive it.

Confirm at action time before:

- typing sensitive data into an app or form;
- sending messages, emails, DMs, comments, or posts;
- submitting forms;
- making purchases or financial actions;
- changing sharing, permissions, account settings, or system security settings;
- deleting local or cloud data;
- creating persistent access such as new debug pairing unless the user has
  specifically asked for that exact pairing action.

Do not solve CAPTCHAs or bypass browser/web safety barriers on the phone.

## Xiaomi / Redmi Notes

On Xiaomi, Redmi, MIUI, or HyperOS devices:

- Wireless ADB pairing can work normally.
- Standard scrcpy mirroring is useful for human visual feedback.
- Raw ADB input may be blocked until extra developer security settings are
  enabled.
- Do not default to scrcpy HID mode unless the user asks; it can behave
  differently and may be unstable.

If `tap`, `swipe`, or `press_key` returns an `INJECT_EVENTS` security error,
tell the user the phone is blocking ADB input. On Xiaomi/MIUI/HyperOS, the fix
is usually Developer Options -> `USB debugging (Security settings)`, which may
require signing into a Xiaomi account.
