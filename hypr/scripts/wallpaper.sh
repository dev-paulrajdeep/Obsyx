#!/usr/bin/env bash
# Obsyx - Wallpaper Manager Script
# Detects running wallpaper daemon (swww or hyprpaper) and applies the active wallpaper.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

WALLPAPER="${1:-}"

if [[ -z "${WALLPAPER}" ]]; then
    if [[ -f "${HOME}/Pictures/Wallpapers/default.png" ]]; then
        WALLPAPER="${HOME}/Pictures/Wallpapers/default.png"
    elif [[ -f "${REPO_ROOT}/assets/wallpapers/noctis_amethyst_default.png" ]]; then
        WALLPAPER="${REPO_ROOT}/assets/wallpapers/noctis_amethyst_default.png"
    elif [[ -f "${HOME}/.config/hypr/assets/wallpapers/noctis_amethyst_default.png" ]]; then
        WALLPAPER="${HOME}/.config/hypr/assets/wallpapers/noctis_amethyst_default.png"
    fi
fi

if [[ -z "${WALLPAPER}" || ! -f "${WALLPAPER}" ]]; then
    echo "Obsyx: No valid wallpaper found" >&2
    exit 1
fi

# Apply via swww if running or available
if pgrep -x "swww-daemon" >/dev/null 2>&1 || which swww >/dev/null 2>&1; then
    swww img "${WALLPAPER}" \
        --transition-type fade \
        --transition-duration 1.5 \
        --transition-fps 60 \
        --transition-bezier 0.16,1,0.3,1 2>/dev/null || true
elif pgrep -x "hyprpaper" >/dev/null 2>&1 || which hyprctl >/dev/null 2>&1; then
    hyprctl hyprpaper preload "${WALLPAPER}" 2>/dev/null || true
    hyprctl hyprpaper wallpaper ",${WALLPAPER}" 2>/dev/null || true
fi
