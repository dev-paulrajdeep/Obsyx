#!/usr/bin/env bash
########################################
# Obsyx VPN Module
########################################

json_escape() {
    local s="$1"
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\n'/\\n}
    printf '%s' "$s"
}

# Find candidate VPN-ish interfaces: wireguard (wg*), tun/tap (OpenVPN, etc)
mapfile -t VPN_IFACES < <(ip -o link show 2>/dev/null | awk -F': ' '{print $2}' | grep -E '^(wg|tun|tap)[0-9]*$')

if [[ ${#VPN_IFACES[@]} -eq 0 ]]; then
    echo '{"text":"","tooltip":"","class":"disconnected"}'
    exit 0
fi

VPN_IF="${VPN_IFACES[0]}"

# Determine type by naming convention, not by grepping our own output
if [[ "$VPN_IF" =~ ^wg ]]; then
    TYPE="WireGuard"
else
    TYPE="OpenVPN"
fi

IP=$(ip -4 addr show "$VPN_IF" 2>/dev/null | awk '/inet / {print $2}' | cut -d/ -f1)

# No IP yet = interface exists but tunnel isn't actually up
if [[ -z "$IP" ]]; then
    ICON="󰦞"
    STATUS="Connecting"
    CLASS="connecting"
else
    ICON="󰦝"
    STATUS="Connected"
    CLASS="connected"
fi

EXTRA=""

# WireGuard gives us live handshake + transfer stats for free
if [[ "$TYPE" == "WireGuard" ]] && command -v wg &>/dev/null; then
    WG_INFO=$(wg show "$VPN_IF" 2>/dev/null)
    if [[ -n "$WG_INFO" ]]; then
        LATEST_HANDSHAKE=$(echo "$WG_INFO" | awk -F': ' '/latest handshake/ {print $2}')
        TRANSFER=$(echo "$WG_INFO" | awk -F': ' '/transfer/ {print $2}')
        ENDPOINT=$(echo "$WG_INFO" | awk -F': ' '/endpoint/ {print $2}')

        [[ -n "$LATEST_HANDSHAKE" ]] && EXTRA="${EXTRA}\nHandshake    ${LATEST_HANDSHAKE}"
        [[ -n "$TRANSFER" ]] && EXTRA="${EXTRA}\nTransfer     ${TRANSFER}"
        [[ -n "$ENDPOINT" ]] && EXTRA="${EXTRA}\nEndpoint     ${ENDPOINT}"
    fi
fi

if (( ${#VPN_IFACES[@]} > 1 )); then
    EXTRA="${EXTRA}\n\n(${#VPN_IFACES[@]} VPN interfaces active)"
fi

TYPE_ESC=$(json_escape "$TYPE")
IF_ESC=$(json_escape "$VPN_IF")
IP_ESC=$(json_escape "${IP:-none}")
EXTRA_ESC=$(json_escape "$EXTRA")

TOOLTIP="<b>VPN</b>\nStatus       ${STATUS}\nType         ${TYPE_ESC}\nInterface    ${IF_ESC}\nIPv4         ${IP_ESC}${EXTRA_ESC}"

cat <<EOF
{
    "text": "${ICON}",
    "tooltip": "${TOOLTIP}",
    "class": "${CLASS}",
    "alt": "${STATUS}"
}
EOF