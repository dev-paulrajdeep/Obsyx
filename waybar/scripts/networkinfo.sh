#!/usr/bin/env bash

########################################
# Obsyx Network Module
########################################
#
# BUGFIXES:
#  1. Raw newlines were embedded directly inside JSON string values in the
#     Wi-Fi/Ethernet/offline heredocs — invalid JSON (RFC 8259), would break
#     Waybar's parser. Rebuilt using explicit "\n" escape sequences.
#  2. Throughput was measured by `sleep 1`-ing INSIDE the script on every
#     single poll — with a 2s interval, that's the exec blocking for a full
#     second every other cycle. Replaced with a timestamped cache file (same
#     pattern cpuinfo.sh already uses) so the rate is the delta between
#     polls, not a blocking measurement.
#
# UPGRADE: falls back to interface-name heuristics (wl*/en*/eth*) if
# NetworkManager isn't managing the connection and nmcli reports nothing.

json_escape() {
    local s="$1"
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\n'/\\n}
    printf '%s' "$s"
}

rate_calc() {
    # Sets DOWN / UP (MB/s) in the caller's scope based on the byte-counter
    # delta since the last poll, keyed per-interface so switching between
    # Wi-Fi and Ethernet never mixes stale counters.
    local iface="$1"
    local cache="/tmp/obsyx_network_${iface}.cache"
    local now rx_now tx_now prev_time prev_rx prev_tx elapsed d u

    now=$(date +%s.%N)
    rx_now=$(cat "/sys/class/net/${iface}/statistics/rx_bytes" 2>/dev/null || echo 0)
    tx_now=$(cat "/sys/class/net/${iface}/statistics/tx_bytes" 2>/dev/null || echo 0)

    if [[ -f "$cache" ]]; then
        source "$cache"
    else
        prev_time=$now
        prev_rx=$rx_now
        prev_tx=$tx_now
    fi

    elapsed=$(awk "BEGIN{e=$now-$prev_time; print (e>0.1)?e:1}")
    d=$(awk "BEGIN{v=($rx_now-$prev_rx)/1024/1024/$elapsed; print (v>0)?v:0}")
    u=$(awk "BEGIN{v=($tx_now-$prev_tx)/1024/1024/$elapsed; print (v>0)?v:0}")
    DOWN=$(awk "BEGIN{printf \"%.1f\", $d}")
    UP=$(awk "BEGIN{printf \"%.1f\", $u}")

    cat > "$cache" <<CACHE_EOF
prev_time=$now
prev_rx=$rx_now
prev_tx=$tx_now
CACHE_EOF
}

INTERFACE=$(ip route 2>/dev/null | awk '/^default/ {print $5; exit}')

if [[ -z "$INTERFACE" ]]; then
    echo '{"text":"󰖪","tooltip":"<b>Network</b>\n\nDisconnected","class":"disconnected"}'
    exit 0
fi

TYPE=$(nmcli -t -f DEVICE,TYPE device status 2>/dev/null | awk -F: -v dev="$INTERFACE" '$1==dev {print $2}')

# Fallback when NetworkManager isn't managing the connection (e.g. systemd-networkd)
if [[ -z "$TYPE" ]]; then
    case "$INTERFACE" in
        wl*)       TYPE="wifi" ;;
        en*|eth*)  TYPE="ethernet" ;;
    esac
fi

case "$TYPE" in

wifi)
    SSID=$(nmcli -t -f ACTIVE,SSID dev wifi 2>/dev/null | awk -F: '$1=="yes"{print $2; exit}')
    SSID=${SSID:-"Unknown"}
    FREQ=$(iw dev "$INTERFACE" link 2>/dev/null | awk '/freq:/ {printf "%.1f GHz",$2/1000}')
    FREQ=${FREQ:-"N/A"}
    rate_calc "$INTERFACE"

    TOOLTIP="Wi-Fi\n\nSSID         $(json_escape "$SSID")\nFrequency    ${FREQ}\nDownload     ${DOWN} MB/s\nUpload       ${UP} MB/s"
    printf '{"text":"󰖩","tooltip":"%s","class":"wifi"}\n' "$TOOLTIP"
    ;;

ethernet)
    rate_calc "$INTERFACE"
    TOOLTIP="Ethernet\n\nDownload     ${DOWN} MB/s\nUpload       ${UP} MB/s"
    printf '{"text":"󰈀","tooltip":"%s","class":"ethernet"}\n' "$TOOLTIP"
    ;;

*)
    echo '{"text":"󰖪","tooltip":"<b>Network</b>\n\nDisconnected","class":"disconnected"}'
    ;;
esac
