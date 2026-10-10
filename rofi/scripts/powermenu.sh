#!/usr/bin/env bash
# Obsyx Power Menu
# Noctis Amethyst session management

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROFI_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
THEME="${ROFI_DIR}/powermenu.rasi"

# Options with icons
LOCK="󰌾  Lock"
SUSPEND="󰤄  Suspend"
LOGOUT="󰍃  Logout"
REBOOT="󰑐  Reboot"
SHUTDOWN="󰐥  Shutdown"

OPTIONS="${LOCK}\n${SUSPEND}\n${LOGOUT}\n${REBOOT}\n${SHUTDOWN}"

CHOSEN="$(echo -e "${OPTIONS}" | rofi -dmenu -i -p "Power" -theme "${THEME}" || true)"

case "${CHOSEN}" in
    "${LOCK}")
        if command -v hyprlock >/dev/null 2>&1; then
            hyprlock
        elif command -v swaylock >/dev/null 2>&1; then
            swaylock
        fi
        ;;
    "${SUSPEND}")
        systemctl suspend
        ;;
    "${LOGOUT}")
        if command -v hyprctl >/dev/null 2>&1; then
            hyprctl dispatch exit
        fi
        ;;
    "${REBOOT}")
        systemctl reboot
        ;;
    "${SHUTDOWN}")
        systemctl poweroff
        ;;
esac
