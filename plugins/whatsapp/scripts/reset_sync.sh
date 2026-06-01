#!/bin/zsh

set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common_env.sh"

"$PLUGIN_ROOT/scripts/stop_bridge.sh" >/dev/null || true

rm -rf "$UPSTREAM_STORE_DIR"
rm -f "$BRIDGE_LOG_FILE" "$QR_TEXT_PATH" "$QR_PNG_PATH"
find "$STATE_ROOT" -maxdepth 1 -type f -name 'upstream-qr*' -delete 2>/dev/null || true
clear_bridge_pid
release_bridge_lock

ensure_state_layout

echo "Reset WhatsApp bridge sync state under $STATE_ROOT"
