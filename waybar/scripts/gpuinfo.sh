#!/usr/bin/env bash

########################################
# Obsyx GPU Monitor
########################################
#
# NVIDIA telemetry is queried once per refresh. Its CSV fields are parsed by
# Bash itself, preserving GPU names containing spaces without an awk process.
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
    local target="${1,,}" f name
    for f in /sys/class/hwmon/hwmon*/name; do
        [[ -f "$f" ]] || continue
        IFS= read -r name < "$f" || continue
        if [[ "${name,,}" == *"$target"* ]]; then
            HWMON_DIR="${f%/name}"
            return 0
        fi
    done
    return 1
}

trim() {
    REPLY="$1"
    REPLY="${REPLY#"${REPLY%%[![:space:]]*}"}"
    REPLY="${REPLY%"${REPLY##*[![:space:]]}"}"
}

format_microwatts() {
    local microwatts="$1" tenths
    tenths=$(( (microwatts + 50000) / 100000 ))
    printf -v REPLY '%d.%d' "$((tenths / 10))" "$((tenths % 10))"
}

NVIDIA_DATA=""
if command -v nvidia-smi >/dev/null 2>&1; then
    NVIDIA_DATA=$(nvidia-smi \
        --query-gpu=name,utilization.gpu,temperature.gpu,power.draw,clocks.current.graphics,memory.used,memory.total \
        --format=csv,noheader,nounits 2>/dev/null)
fi

AMD_BUSY_FILE=""
for busy_file in /sys/class/drm/card*/device/gpu_busy_percent; do
    [[ -r "$busy_file" ]] || continue
    AMD_BUSY_FILE="$busy_file"
    break
done

############################################
# NVIDIA discrete GPU
############################################

if [[ -n "$NVIDIA_DATA" ]]; then

    # Waybar displays the first GPU, matching the previous read behavior.
    IFS= read -r NVIDIA_DATA <<< "$NVIDIA_DATA"
    IFS=',' read -r NAME UTIL TEMP POWER CLOCK MEM_USED MEM_TOTAL <<< "$NVIDIA_DATA"
    for field in NAME UTIL TEMP POWER CLOCK MEM_USED MEM_TOTAL; do
        trim "${!field}"
        printf -v "$field" '%s' "$REPLY"
    done

    CLASS="normal"
    if [[ "$TEMP" =~ ^[0-9]+$ ]]; then
        (( TEMP >= 85 )) && CLASS="critical"
        (( TEMP >= 75 && TEMP < 85 )) && CLASS="warning"
    fi

    TOOLTIP="<b>$(json_escape "$NAME")</b>\n\nUsage        ${UTIL}%\nClock        ${CLOCK} MHz\nTemperature  ${TEMP}°C\nPower        ${POWER} W\nVRAM         ${MEM_USED} / ${MEM_TOTAL} MiB"

    printf '{"text":"󰢮 %s%%","tooltip":"%s","class":"%s"}\n' "$UTIL" "$TOOLTIP" "$CLASS"

############################################
# AMD integrated GPU fallback (amdgpu)
############################################

elif [[ -n "$AMD_BUSY_FILE" ]]; then

    UTIL=0
    IFS= read -r UTIL < "$AMD_BUSY_FILE" || UTIL=0

    HWMON_DIR=""
    find_hwmon "amdgpu" || true
    TEMP="--"
    POWER="--"
    if [[ -n "$HWMON_DIR" && -r "$HWMON_DIR/temp1_input" ]]; then
        IFS= read -r temp_millicelsius < "$HWMON_DIR/temp1_input"
        [[ "$temp_millicelsius" =~ ^[0-9]+$ ]] && TEMP=$(( (temp_millicelsius + 500) / 1000 ))
    fi
    if [[ -n "$HWMON_DIR" && -r "$HWMON_DIR/power1_average" ]]; then
        IFS= read -r power_microwatts < "$HWMON_DIR/power1_average"
        if [[ "$power_microwatts" =~ ^[0-9]+$ ]]; then
            format_microwatts "$power_microwatts"
            POWER="$REPLY"
        fi
    fi

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
