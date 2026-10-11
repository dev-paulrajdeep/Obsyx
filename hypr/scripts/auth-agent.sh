#!/usr/bin/env bash
# Obsyx - Polkit Authentication Agent Launcher
# Discovers and launches the available Wayland/Hyprland Polkit authentication agent.

set -euo pipefail

# Prevent multiple instances
if pgrep -f "polkit.*agent" >/dev/null 2>&1 || pgrep -f "hyprpolkitagent" >/dev/null 2>&1; then
    exit 0
fi

# 1. Check systemd user service for hyprpolkitagent
if command -v systemctl >/dev/null 2>&1 && systemctl --user is-enabled hyprpolkitagent.service >/dev/null 2>&1; then
    systemctl --user start hyprpolkitagent.service && exit 0
fi

# 2. Candidate agent binaries in priority order
AGENTS=(
    "/usr/lib/hyprpolkitagent/hyprpolkitagent"
    "/usr/libexec/hyprpolkitagent"
    "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1"
    "/usr/libexec/polkit-gnome-authentication-agent-1"
    "/usr/lib/polkit-kde-authentication-agent-1"
    "/usr/libexec/polkit-kde-authentication-agent-1"
    "/usr/bin/lxpolkit"
)

for agent in "${AGENTS[@]}"; do
    if [[ -x "${agent}" ]]; then
        exec "${agent}" &
        exit 0
    fi
done

echo "Obsyx: No Polkit authentication agent found" >&2
exit 1
