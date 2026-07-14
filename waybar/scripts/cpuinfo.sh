#!/usr/bin/env bash

########################################
# Obsyx CPU Monitor
########################################
#
# BUGFIXES:
#  1. Raw newlines embedded directly in the JSON tooltip string — invalid
#     JSON (RFC 8259). Rebuilt using explicit "\n" escapes.
#  2. MODEL was a hardcoded placeholder string ("AMD Ryzen 7 250") that
#     doesn't correspond to any real Ryzen model — it always displayed the
#     same wrong text regardless of the actual CPU. Now read live from
#     /proc/cpuinfo.
#  3. Temperature and power were read via a bare glob over
#     /sys/class/hwmon/hwmon*, with no guarantee hwmon0 is the CPU sensor —
#     hwmon numbering is assigned by driver load order, so on a system with
#     an NVMe drive, GPU, or Wi-Fi chip also exposing hwmon data, this could
#     silently report a completely different device's numbers as "CPU
#     temp". Now scoped explicitly to the k10temp (AMD) / coretemp (Intel)
#     hwmon by name.
#
# UPGRADE: added a "class" (normal/warning/critical) field for style.css.

CACHE="/tmp/obsyx_cpu.cache"

json_escape() {
    local s="$1"
    s=${s//\\/\\\\}
    s=${s//\"/\\\"}
    s=${s//$'\n'/\\n}
    printf '%s' "$s"
}

# Finds the hwmon directory whose "name" file matches $1 — avoids relying on
# glob order, since hwmon0 is not guaranteed to be any particular device.
find_hwmon() {
    local target="$1" f
    for f in /sys/class/hwmon/hwmon*/name; do
        [[ -f "$f" ]] || continue
        grep -qi "$target" "$f" 2>/dev/null && { dirname "$f"; return 0; }
    done
    return 1
}

############################################
# CPU Model (live, not hardcoded)
############################################

MODEL=$(awk -F': ' '/model name/ {print $2; exit}' /proc/cpuinfo)
MODEL=${MODEL:-"Unknown CPU"}

############################################
# CPU Usage (delta since last poll, via cache)
############################################

usage=$(grep 'cpu ' /proc/stat | awk '
{
idle=$5
total=0
for(i=2;i<=NF;i++) total+=$i
print idle,total
}')

read -r idle total <<< "$usage"

if [[ -f "$CACHE" ]]; then
    source "$CACHE"
else
    old_idle=$idle
    old_total=$total
fi

diff_idle=$((idle-old_idle))
diff_total=$((total-old_total))

if (( diff_total > 0 )); then
    cpu_usage=$((100*(diff_total-diff_idle)/diff_total))
else
    cpu_usage=0
fi

############################################
# Frequency
############################################

freq=$(awk '{sum+=$1} END {if (NR>0) printf "%.2f",sum/NR/1000000}' \
/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq 2>/dev/null)
freq=${freq:-"--"}

############################################
# Temperature — scoped to the correct sensor by name
############################################

CPU_HWMON=$(find_hwmon "k10temp")
[[ -z "$CPU_HWMON" ]] && CPU_HWMON=$(find_hwmon "coretemp")

temp="--"
[[ -n "$CPU_HWMON" && -f "$CPU_HWMON/temp1_input" ]] && \
    temp=$(awk '{printf "%.0f",$1/1000}' "$CPU_HWMON/temp1_input")

############################################
# Package Power — same sensor scope as temperature
############################################

power="--"
[[ -n "$CPU_HWMON" && -f "$CPU_HWMON/power1_average" ]] && \
    power=$(awk '{printf "%.1f",$1/1000000}' "$CPU_HWMON/power1_average")

############################################
# Governor
############################################

gov=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null)
gov=${gov:-"unknown"}

############################################
# Save usage cache
############################################

cat > "$CACHE" <<CACHE_EOF
old_idle=$idle
old_total=$total
CACHE_EOF

############################################
# Class for CSS state hooks
############################################

CLASS="normal"
if [[ "$temp" != "--" ]]; then
    (( temp >= 85 )) && CLASS="critical"
    (( temp >= 75 && temp < 85 )) && CLASS="warning"
fi

############################################
# Output JSON
############################################

TOOLTIP="$(json_escape "$MODEL")\n\nUsage        ${cpu_usage}%\nFrequency    ${freq} GHz\nTemperature  ${temp}°C\nPower        ${power} W\nGovernor     ${gov}"

printf '{"text":"󰍛 %s%%","tooltip":"%s","class":"%s"}\n' "$cpu_usage" "$TOOLTIP" "$CLASS"
