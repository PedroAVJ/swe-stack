#!/bin/zsh

set -euo pipefail

source "$(cd "$(dirname "$0")" && pwd)/common_env.sh"

require_command go

if bridge_healthcheck || [[ -n "$(bridge_listener_pid || true)" ]]; then
  echo "Stop the durable WhatsApp bridge first with 'pnpm stop' before running setup." >&2
  exit 1
fi

if [[ "${WHATSAPP_USE_PHONE_PAIRING:-}" == "1" ]]; then
  resolve_pair_phone
fi

export WHATSAPP_MCP_EXIT_AFTER_AUTH=1
export WHATSAPP_MCP_EXIT_AFTER_AUTH_WAIT_SECS=35

if [[ -n "${WHATSAPP_MCP_PAIR_PHONE:-}" ]]; then
  echo "Phone-number pairing fallback enabled. In WhatsApp, use Linked devices -> Link with phone number instead, then enter the code shown below."
else
  echo "QR pairing enabled. In WhatsApp, use Linked devices -> Link a device, then scan the QR code shown below."
fi

cd "$BRIDGE_DIR"
exec go run main.go
