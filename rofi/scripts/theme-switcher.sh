#!/usr/bin/env bash
# Obsyx Theme Switcher
# Interactive theme switcher using Rofi and obsyx theme apply

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROFI_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_DIR="$(cd "${ROFI_DIR}/.." && pwd)"
OBSYX_BIN="${REPO_DIR}/bin/obsyx"

THEMES=(
    "󰏘  Noctis Amethyst|noctis_amethyst|Regal nocturnal purple & soft lavender glass (Reference)"
    "󰏘  Obsidian|obsidian|Monolithic dark stone, matte graphite & platinum"
    "󰏘  Frost|frost|Crystalline polar slate & ice-blue sub-zero clarity"
    "󰏘  Aurora|aurora|Midnight oceanic teal & emerald luminescence"
    "󰏘  Ember|ember|Volcanic basalt rock & warm magma copper"
)

MENU_ENTRIES=""
for entry in "${THEMES[@]}"; do
    display_title="$(echo "${entry}" | cut -d'|' -f1)"
    desc="$(echo "${entry}" | cut -d'|' -f3)"
    if [ -z "${MENU_ENTRIES}" ]; then
        MENU_ENTRIES="${display_title} — ${desc}"
    else
        MENU_ENTRIES="${MENU_ENTRIES}\n${display_title} — ${desc}"
    fi
done

CHOSEN="$(echo -e "${MENU_ENTRIES}" | rofi -dmenu -i -p "Theme" || true)"

if [ -z "${CHOSEN}" ]; then
    exit 0
fi

SELECTED_SLUG=""
for entry in "${THEMES[@]}"; do
    display_title="$(echo "${entry}" | cut -d'|' -f1)"
    if [[ "${CHOSEN}" == "${display_title}"* ]]; then
        SELECTED_SLUG="$(echo "${entry}" | cut -d'|' -f2)"
        break
    fi
done

if [ -n "${SELECTED_SLUG}" ]; then
    if [ -x "${OBSYX_BIN}" ]; then
        "${OBSYX_BIN}" theme apply "${SELECTED_SLUG}"
    else
        obsyx theme apply "${SELECTED_SLUG}"
    fi
    if command -v notify-send >/dev/null 2>&1; then
        notify-send -a "Obsyx Desktop" "Theme Applied" "Active theme switched to ${SELECTED_SLUG}."
    fi
fi
