#!/usr/bin/env bash
# Obsyx - Interactive Keybinding Search & Launcher
# Search all configured shortcuts and optionally execute their action.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROFI_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
THEME="${ROFI_DIR}/app-launcher.rasi"

if ! command -v rofi >/dev/null 2>&1; then
    echo "Error: rofi is not installed or not in PATH" >&2
    exit 1
fi

ROFI_ARGS=(-i -p "Shortcuts" -format i)
if [[ -f "${THEME}" ]]; then
    ROFI_ARGS+=(-theme "${THEME}")
fi

declare -a ENTRIES=(
    "SUPER + Return             │ Terminal Emulator            │ Applications & Launchers"
    "SUPER + Space              │ Application Launcher         │ Applications & Launchers"
    "SUPER + B                  │ Web Browser                  │ Applications & Launchers"
    "SUPER + E                  │ File Manager                 │ Applications & Launchers"
    "SUPER + L                  │ Lock Screen                  │ Applications & Launchers"
    "SUPER + C                  │ Code Editor                  │ Applications & Launchers"
    "SUPER + M                  │ Music Player                 │ Applications & Launchers"
    "SUPER + V                  │ Clipboard History            │ Applications & Launchers"
    "SUPER + Q                  │ Close Window                 │ Window Management"
    "SUPER + V                  │ Toggle Floating              │ Window Management"
    "SUPER + F                  │ Toggle Fullscreen            │ Window Management"
    "SUPER + P                  │ Toggle Pseudo                │ Window Management"
    "SUPER + SHIFT + P          │ Toggle Pin                   │ Window Management"
    "SUPER + J                  │ Toggle Split                 │ Window Management"
    "SUPER + left               │ Focus left                   │ Window Management"
    "SUPER + down               │ Focus down                   │ Window Management"
    "SUPER + up                 │ Focus up                     │ Window Management"
    "SUPER + right              │ Focus right                  │ Window Management"
    "SUPER + mouse:272          │ Drag Window                  │ Window Management"
    "SUPER + mouse:273          │ Resize Window                │ Window Management"
    "SUPER + 1                  │ Workspace 1                  │ Workspace Navigation"
    "SUPER + SHIFT + 1          │ Move Window → Workspace 1    │ Workspace Navigation"
    "SUPER + 2                  │ Workspace 2                  │ Workspace Navigation"
    "SUPER + SHIFT + 2          │ Move Window → Workspace 2    │ Workspace Navigation"
    "SUPER + 3                  │ Workspace 3                  │ Workspace Navigation"
    "SUPER + SHIFT + 3          │ Move Window → Workspace 3    │ Workspace Navigation"
    "SUPER + 4                  │ Workspace 4                  │ Workspace Navigation"
    "SUPER + SHIFT + 4          │ Move Window → Workspace 4    │ Workspace Navigation"
    "SUPER + 5                  │ Workspace 5                  │ Workspace Navigation"
    "SUPER + SHIFT + 5          │ Move Window → Workspace 5    │ Workspace Navigation"
    "SUPER + 6                  │ Workspace 6                  │ Workspace Navigation"
    "SUPER + SHIFT + 6          │ Move Window → Workspace 6    │ Workspace Navigation"
    "SUPER + 7                  │ Workspace 7                  │ Workspace Navigation"
    "SUPER + SHIFT + 7          │ Move Window → Workspace 7    │ Workspace Navigation"
    "SUPER + 8                  │ Workspace 8                  │ Workspace Navigation"
    "SUPER + SHIFT + 8          │ Move Window → Workspace 8    │ Workspace Navigation"
    "SUPER + 9                  │ Workspace 9                  │ Workspace Navigation"
    "SUPER + SHIFT + 9          │ Move Window → Workspace 9    │ Workspace Navigation"
    "SUPER + 0                  │ Workspace 10                 │ Workspace Navigation"
    "SUPER + SHIFT + 0          │ Move Window → Workspace 10   │ Workspace Navigation"
    "SUPER + Grave              │ Toggle Terminal Scratchpad   │ Workspace Navigation"
    "SUPER + SHIFT + Grave      │ Move Window → Terminal Scratchpad │ Workspace Navigation"
    "SUPER + mouse_down         │ Next Workspace               │ Workspace Navigation"
    "SUPER + mouse_up           │ Previous Workspace           │ Workspace Navigation"
    "SUPER + S                  │ Region → Clipboard           │ Screenshots"
    "SUPER + SHIFT + S          │ Region → File                │ Screenshots"
    "SUPER + ALT + S            │ Window → Clipboard           │ Screenshots"
    "SUPER + ALT + SHIFT + S    │ Window → File                │ Screenshots"
    "Print                      │ Monitor → File               │ Screenshots"
    "SHIFT + Print              │ Monitor → Clipboard          │ Screenshots"
    "XF86AudioRaiseVolume       │ Volume Up                    │ Media & Hardware Controls"
    "XF86AudioLowerVolume       │ Volume Down                  │ Media & Hardware Controls"
    "XF86AudioMute              │ Toggle Volume Mute           │ Media & Hardware Controls"
    "XF86AudioMicMute           │ Toggle Mic Mute              │ Media & Hardware Controls"
    "XF86MonBrightnessUp        │ Brightness Up                │ Media & Hardware Controls"
    "XF86MonBrightnessDown      │ Brightness Down              │ Media & Hardware Controls"
    "XF86AudioNext              │ Next Track                   │ Media & Hardware Controls"
    "XF86AudioPrev              │ Previous Track               │ Media & Hardware Controls"
    "XF86AudioPause             │ Toggle Play/Pause            │ Media & Hardware Controls"
    "XF86AudioPlay              │ Toggle Play/Pause            │ Media & Hardware Controls"
    "SUPER + Escape             │ Power Menu                   │ System & Session Controls"
    "SUPER + L                  │ Lock Session                 │ System & Session Controls"
    "SUPER + CTRL + L           │ Logout                       │ System & Session Controls"
    "SUPER + CTRL + S           │ Suspend                      │ System & Session Controls"
    "SUPER + CTRL + R           │ Reboot                       │ System & Session Controls"
    "SUPER + CTRL + H           │ Hibernate                    │ System & Session Controls"
    "SUPER + CTRL + P           │ Power Off                    │ System & Session Controls"
    "SUPER + CTRL + O           │ Turn Monitor Off             │ System & Session Controls"
)

declare -a ACTIONS=(
    "kitty"
    "rofi -show drun"
    "vivaldi"
    "thunar"
    "hyprlock"
    "code"
    "spotify"
    "~/.config/rofi/scripts/cliphist.sh"
    "dsp.window.close()"
    "dsp.window.float({action=toggle})"
    "dsp.window.fullscreen()"
    "dsp.window.pseudo()"
    "dsp.window.pin({action=toggle})"
    "dsp.layout(togglesplit)"
    "dsp.focus({direction=left})"
    "dsp.focus({direction=down})"
    "dsp.focus({direction=up})"
    "dsp.focus({direction=right})"
    "dsp.window.drag()"
    "dsp.window.resize()"
    "dsp.focus({workspace=1})"
    "dsp.window.move({workspace=1})"
    "dsp.focus({workspace=2})"
    "dsp.window.move({workspace=2})"
    "dsp.focus({workspace=3})"
    "dsp.window.move({workspace=3})"
    "dsp.focus({workspace=4})"
    "dsp.window.move({workspace=4})"
    "dsp.focus({workspace=5})"
    "dsp.window.move({workspace=5})"
    "dsp.focus({workspace=6})"
    "dsp.window.move({workspace=6})"
    "dsp.focus({workspace=7})"
    "dsp.window.move({workspace=7})"
    "dsp.focus({workspace=8})"
    "dsp.window.move({workspace=8})"
    "dsp.focus({workspace=9})"
    "dsp.window.move({workspace=9})"
    "dsp.focus({workspace=10})"
    "dsp.window.move({workspace=10})"
    "dsp.workspace.toggle_special(terminal)"
    "dsp.window.move({workspace=special:terminal})"
    "dsp.focus({workspace=e+1})"
    "dsp.focus({workspace=e-1})"
    "hyprshot -m region --clipboard-only"
    "hyprshot -m region"
    "hyprshot -m window --clipboard-only"
    "hyprshot -m window"
    "hyprshot -m output"
    "hyprshot -m output --clipboard-only"
    "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"
    "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"
    "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"
    "wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"
    "brightnessctl -e4 -n2 set 5%+"
    "brightnessctl -e4 -n2 set 5%-"
    "playerctl next"
    "playerctl previous"
    "playerctl play-pause"
    "playerctl play-pause"
    "~/.config/rofi/scripts/powermenu.sh"
    "hyprlock"
    "hyprctl dispatch exit"
    "systemctl suspend"
    "systemctl reboot"
    "systemctl hibernate"
    "systemctl poweroff"
    "hyprctl dispatch dpms off"
)

# Render menu and capture selection index
INDEX="$(printf "%s\n" "${ENTRIES[@]}" | rofi -dmenu "${ROFI_ARGS[@]}" || true)"

if [[ -z "${INDEX}" ]]; then
    exit 0
fi

ACTION="${ACTIONS[INDEX]:-}"
if [[ -z "${ACTION}" ]]; then
    exit 0
fi

# Dispatch or execute action
if [[ "${ACTION}" == dsp.* ]]; then
    if command -v notify-send >/dev/null 2>&1; then
        notify-send "Obsyx Keybinding" "${ENTRIES[INDEX]}"
    fi
else
    # Shell command execution
    eval "${ACTION} &"
fi
