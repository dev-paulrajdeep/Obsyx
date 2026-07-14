#!/usr/bin/env bash

########################################
# Obsyx Memory Module
########################################
#
# BUGFIXES:
#  1. Raw newlines were embedded directly in the JSON tooltip string —
#     invalid JSON (RFC 8259). Rebuilt using explicit "\n" escapes.
#  2. The old version called `free -b` AND `free -h` separately, a moment
#     apart — two independent snapshots that could disagree with each
#     other under memory pressure. Consolidated into a single `free -b`
#     call as the one source of truth for every figure shown.
#
# UPGRADE: percentage now rounds (was truncating), and a "class" field
# (normal/warning/critical) is exposed for style.css to hook into.

read -r TOTAL USED AVAILABLE SWAP_TOTAL SWAP_USED CACHE_B <<< "$(
    free -b | awk '
        /^Mem:/  {total=$2; used=$3; avail=$7; cache=$6}
        /^Swap:/ {swtotal=$2; swused=$3}
        END {print total, used, avail, swtotal+0, swused+0, cache}
    '
)"

to_gib() { awk "BEGIN{printf \"%.1f\", $1/1024/1024/1024}"; }

USED_GB=$(to_gib "$USED")
TOTAL_GB=$(to_gib "$TOTAL")
AVAILABLE_GB=$(to_gib "$AVAILABLE")
SWAP_USED_GB=$(to_gib "$SWAP_USED")
SWAP_TOTAL_GB=$(to_gib "$SWAP_TOTAL")
CACHE_GB=$(to_gib "$CACHE_B")

PERCENT=$(awk "BEGIN{printf \"%.0f\", ($USED/$TOTAL)*100}")

CLASS="normal"
(( PERCENT >= 90 )) && CLASS="critical"
(( PERCENT >= 75 && PERCENT < 90 )) && CLASS="warning"

TOOLTIP="Memory\n\nUsage        ${PERCENT}%\nUsed         ${USED_GB} GiB\nAvailable    ${AVAILABLE_GB} GiB\nTotal        ${TOTAL_GB} GiB\nCache        ${CACHE_GB} GiB\nSwap         ${SWAP_USED_GB} / ${SWAP_TOTAL_GB} GiB"

printf '{"text":"󰍛 %s/%s","tooltip":"%s","class":"%s"}\n' "$USED_GB" "$TOTAL_GB" "$TOOLTIP" "$CLASS"
