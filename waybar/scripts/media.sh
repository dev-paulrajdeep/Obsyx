#!/usr/bin/env bash
#
# Waybar media module — supports multi-player cycling, safe JSON output,
# per-status CSS classes, and richer tooltips.
#
# BUGFIX (the one causing the live parse-error spam): with
# "return-type": "json", Waybar tries to JSON-parse the script's stdout on
# EVERY interval — including when there's nothing to show. The previous
# version handled "no players" and "player stopped" with a bare `exit 0`,
# printing zero bytes. Feeding an empty string to a JSON parser produces
# exactly the "Missing '}' or object member name" error seen in the log,
# repeating every interval for as long as the player stays paused/stopped.
# Fixed: every exit path now prints a complete, valid JSON object — an
# empty one (`"text":""`) when there's nothing playing, which still
# collapses the module visually, but never hands Waybar invalid JSON.
#
# BUGFIX (from the previous round, confirmed still correct): reading the
# saved player index via `$(< "$STATE_FILE" 2>/dev/null || echo 0)` doesn't
# actually read the file — only the bare `$(< file)` form does. Reading via
# `cat` instead.

STATE_FILE="/tmp/waybar-media-player-index"
MAX=32

empty_output() {
    echo '{"text":"","tooltip":"","class":"none","alt":"none"}'
    exit 0
}

# --- player selection --------------------------------------------------

mapfile -t PLAYERS < <(playerctl -l 2>/dev/null)

if [[ ${#PLAYERS[@]} -eq 0 ]]; then
    empty_output
fi

# Allow middle-click to cycle through active players.
# (No JSON needed here — this invocation is on-click-middle, not the
# periodic exec, so Waybar isn't expecting parseable output from it.)
if [[ "$1" == "--next-player" ]]; then
    IDX=""
    [[ -f "$STATE_FILE" ]] && IDX=$(cat "$STATE_FILE" 2>/dev/null)
    IDX=${IDX:-0}
    IDX=$(( (IDX + 1) % ${#PLAYERS[@]} ))
    echo "$IDX" > "$STATE_FILE"
    exit 0
fi

IDX=""
[[ -f "$STATE_FILE" ]] && IDX=$(cat "$STATE_FILE" 2>/dev/null)
IDX=${IDX:-0}
(( IDX >= ${#PLAYERS[@]} )) && IDX=0

PLAYER="${PLAYERS[$IDX]}"

# Prefer a Playing player if the "selected" one isn't active
if [[ "$(playerctl -p "$PLAYER" status 2>/dev/null)" != "Playing" ]]; then
    for p in "${PLAYERS[@]}"; do
        if [[ "$(playerctl -p "$p" status 2>/dev/null)" == "Playing" ]]; then
            PLAYER="$p"
            break
        fi
    done
fi

STATUS=$(playerctl -p "$PLAYER" status 2>/dev/null)
[[ -z "$STATUS" || "$STATUS" == "Stopped" ]] && empty_output

# --- metadata ------------------------------------------------------------

TITLE=$(playerctl -p "$PLAYER" metadata title 2>/dev/null)
ARTIST=$(playerctl -p "$PLAYER" metadata artist 2>/dev/null)
ALBUM=$(playerctl -p "$PLAYER" metadata album 2>/dev/null)

TITLE=${TITLE:-Unknown title}
ARTIST=${ARTIST:-Unknown artist}
ALBUM=${ALBUM:-}

TEXT="${TITLE} — ${ARTIST}"
if (( ${#TEXT} > MAX )); then
    TEXT="${TEXT:0:$((MAX-1))}…"
fi

case "$STATUS" in
    Playing) ICON="" CLASS="playing" ;;
    Paused)  ICON="" CLASS="paused"  ;;
    *)       ICON="󰏤" CLASS="stopped" ;;
esac

# --- JSON-safe escaping ---------------------------------------------------
# Waybar's own JSON parser will silently misbehave on raw quotes/backslashes,
# so escape backslashes first, then quotes, then swap real newlines for \n.

json_escape() {
    local s="$1"
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\n'/\\n}
    printf '%s' "$s"
}

TEXT_ESC=$(json_escape "$ICON $TEXT")
TITLE_ESC=$(json_escape "$TITLE")
ARTIST_ESC=$(json_escape "$ARTIST")
ALBUM_ESC=$(json_escape "$ALBUM")
PLAYER_ESC=$(json_escape "$PLAYER")

TOOLTIP="<b>${TITLE_ESC}</b>\nArtist   ${ARTIST_ESC}"
[[ -n "$ALBUM" ]] && TOOLTIP="${TOOLTIP}\nAlbum    ${ALBUM_ESC}"
TOOLTIP="${TOOLTIP}\nPlayer   ${PLAYER_ESC}\nStatus   ${STATUS}"
(( ${#PLAYERS[@]} > 1 )) && TOOLTIP="${TOOLTIP}\n\n(${#PLAYERS[@]} players active — middle-click to switch)"

cat <<EOF
{
    "text": "${TEXT_ESC}",
    "tooltip": "${TOOLTIP}",
    "class": "${CLASS}",
    "alt": "${STATUS}"
}
EOF