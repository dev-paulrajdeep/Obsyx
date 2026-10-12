#!/usr/bin/env bash
# Obsyx Clipboard Manager
# Noctis Amethyst cliphist + rofi integration

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROFI_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
THEME="${ROFI_DIR}/clipboard.rasi"

if ! command -v cliphist >/dev/null 2>&1; then
    notify-send "Obsyx Clipboard" "cliphist is not installed" --urgency=critical || true
    exit 1
fi

SELECTION="$(cliphist list | rofi -dmenu -i -p "󰅌" -theme "${THEME}" || true)"

if [[ -n "${SELECTION}" ]]; then
    echo "${SELECTION}" | cliphist decode | wl-copy
fi
