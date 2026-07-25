#!/usr/bin/env bash

STATE_FILE="/tmp/waybar-media-player-index"
MAX=32

empty_output() {
python3 <<'PY'
import json
print(json.dumps({
    "text": "",
    "tooltip": "",
    "class": "none",
    "alt": "none"
}, ensure_ascii=False))
PY
exit 0
}

########################################
# Player discovery
########################################

mapfile -t PLAYERS < <(playerctl -l 2>/dev/null)

(( ${#PLAYERS[@]} == 0 )) && empty_output

########################################
# Cycle player
########################################

if [[ "$1" == "--next-player" ]]; then
    IDX=0
    [[ -f "$STATE_FILE" ]] && IDX=$(<"$STATE_FILE")
    IDX=$(( (IDX + 1) % ${#PLAYERS[@]} ))
    echo "$IDX" > "$STATE_FILE"
    exit 0
fi

IDX=0
[[ -f "$STATE_FILE" ]] && IDX=$(<"$STATE_FILE")
(( IDX >= ${#PLAYERS[@]} )) && IDX=0

PLAYER="${PLAYERS[$IDX]}"

########################################
# Prefer active player
########################################

if [[ "$(playerctl -p "$PLAYER" status 2>/dev/null)" != "Playing" ]]; then
    for p in "${PLAYERS[@]}"; do
        if [[ "$(playerctl -p "$p" status 2>/dev/null)" == "Playing" ]]; then
            PLAYER="$p"
            break
        fi
    done
fi

########################################
# Metadata
########################################

STATUS=$(playerctl -p "$PLAYER" status 2>/dev/null)

[[ -z "$STATUS" || "$STATUS" == "Stopped" ]] && empty_output

TITLE=$(playerctl -p "$PLAYER" metadata title 2>/dev/null)
ARTIST=$(playerctl -p "$PLAYER" metadata artist 2>/dev/null)
ALBUM=$(playerctl -p "$PLAYER" metadata album 2>/dev/null)

TITLE=${TITLE:-Unknown title}
ARTIST=${ARTIST:-Unknown artist}
ALBUM=${ALBUM:-}

########################################
# Display text
########################################

TEXT="${TITLE} — ${ARTIST}"

(( ${#TEXT} > MAX )) && TEXT="${TEXT:0:$((MAX-1))}…"

########################################
# Icons
########################################

case "$PLAYER" in
    spotify*)
        ICON=""
        ;;
    firefox*)
        ICON="󰈹"
        ;;
    chromium*)
        ICON=""
        ;;
    vlc*)
        ICON="󰕼"
        ;;
    mpv*)
        ICON="󰐹"
        ;;
    *)
        ICON="󰎈"
        ;;
esac

########################################
# CSS class
########################################

case "$STATUS" in
    Playing) CLASS="playing" ;;
    Paused)  CLASS="paused" ;;
    *)       CLASS="stopped" ;;
esac

########################################
# Tooltip
########################################

TOOLTIP="${TITLE}
Artist   ${ARTIST}"

[[ -n "$ALBUM" ]] && TOOLTIP="${TOOLTIP}
Album    ${ALBUM}"

TOOLTIP="${TOOLTIP}
Player   ${PLAYER}
Status   ${STATUS}"

(( ${#PLAYERS[@]} > 1 )) &&
TOOLTIP="${TOOLTIP}

${#PLAYERS[@]} players active
Middle-click to switch"

########################################
# JSON
########################################

export TEXT TOOLTIP CLASS STATUS ICON

python3 <<'PY'
import json
import os

print(json.dumps({
    "text": f"{os.environ['ICON']} {os.environ['TEXT']}",
    "tooltip": os.environ["TOOLTIP"],
    "class": os.environ["CLASS"],
    "alt": os.environ["STATUS"]
}, ensure_ascii=False))
PY