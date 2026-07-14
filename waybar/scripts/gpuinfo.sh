#!/usr/bin/env bash

########################################
# Obsyx GPU Monitor
########################################
#
# BUGFIX (major): nvidia-smi's --format=csv output delimits fields with
# ", " (comma+space). The previous version read that output with bash's
# default whitespace-splitting `read`. Since GPU names almost always
# contain spaces ("NVIDIA GeForce RTX 5060 Laptop GPU"), every field after
# the first was silently misaligned — utilization, temperature, power,
# clock and VRAM were all reading from the wrong column. Confirmed with a
# side-by-side test: the old parser produced NAME="NVIDIA" TEMP="RTX"
# POWER="5060" — completely garbage. Fixed by re-delimiting with awk
# before the read.
#
# BUGFIX: raw newlines in the JSON tooltip string — invalid JSON, rebuilt
# with explicit "\n".
#
# FEATURE: added an AMD amdgpu sysfs fallback. On a hybrid dGPU/iGPU laptop,
# nvidia-smi failing (no driver loaded, or the dGPU is powered down via
# Optimus/PRIME to save battery) previously meant "GPU information
# unavailable" — even though the AMD iGPU is actively rendering and has its
# own usage/temp data exposed via sysfs.

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

NVIDIA_OK=false
command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi >/dev/null 2>&1 && NVIDIA_OK=true

AMD_BUSY_FILE=$(compgen -G "/sys/class/drm/card*/device/gpu_busy_percent" 2>/dev/null | head -1)

############################################
# NVIDIA discrete GPU
############################################

if $NVIDIA_OK; then

    IFS='|' read -r NAME UTIL TEMP POWER CLOCK MEM_USED MEM_TOTAL <<< "$(
        nvidia-smi \
            --query-gpu=name,utilization.gpu,temperature.gpu,power.draw,clocks.current.graphics,memory.used,memory.total \
            --format=csv,noheader,nounits \
        | awk -F', ' 'BEGIN{OFS="|"} {$1=$1; print}'
    )"

    CLASS="normal"
    (( TEMP >= 85 )) && CLASS="critical"
    (( TEMP >= 75 && TEMP < 85 )) && CLASS="warning"

    TOOLTIP="<b>$(json_escape "$NAME")</b>\n\nUsage        ${UTIL}%\nClock        ${CLOCK} MHz\nTemperature  ${TEMP}°C\nPower        ${POWER} W\nVRAM         ${MEM_USED} / ${MEM_TOTAL} MiB"

    printf '{"text":"󰢮 %s%%","tooltip":"%s","class":"%s"}\n' "$UTIL" "$TOOLTIP" "$CLASS"

############################################
# AMD integrated GPU fallback (amdgpu)
############################################

elif [[ -n "$AMD_BUSY_FILE" ]]; then

    UTIL=$(cat "$AMD_BUSY_FILE" 2>/dev/null || echo 0)

    HWMON_DIR=$(find_hwmon "amdgpu")
    TEMP="--"
    POWER="--"
    [[ -n "$HWMON_DIR" && -f "$HWMON_DIR/temp1_input" ]] && \
        TEMP=$(awk '{printf "%.0f",$1/1000}' "$HWMON_DIR/temp1_input")
    [[ -n "$HWMON_DIR" && -f "$HWMON_DIR/power1_average" ]] && \
        POWER=$(awk '{printf "%.1f",$1/1000000}' "$HWMON_DIR/power1_average")

    CLASS="normal"
    [[ "$TEMP" != "--" ]] && (( TEMP >= 85 )) && CLASS="critical"

    TOOLTIP="AMD Integrated GPU\n\nUsage        ${UTIL}%\nTemperature  ${TEMP}°C\nPower        ${POWER} W"

    printf '{"text":"󰢮 %s%%","tooltip":"%s","class":"%s"}\n' "$UTIL" "$TOOLTIP" "$CLASS"

############################################
# No GPU telemetry available
############################################

else
    echo '{"text":"󰢮 --","tooltip":"GPU information unavailable","class":"unavailable"}'
fi
