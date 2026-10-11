#!/usr/bin/env bash
# Obsyx - Waybar Telemetry Script Runner
# Resolves and executes Waybar telemetry scripts portably.

set -euo pipefail

SCRIPT_NAME="${1:-}"
shift || true

if [[ -z "${SCRIPT_NAME}" ]]; then
    echo "Usage: runner.sh <script_name> [args...]" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

CANDIDATES=(
    "${WAYBAR_SCRIPTS_DIR:-}/${SCRIPT_NAME}"
    "${SCRIPT_DIR}/${SCRIPT_NAME}"
    "${REPO_ROOT}/waybar/scripts/${SCRIPT_NAME}"
    "${XDG_CONFIG_HOME:-$HOME/.config}/waybar/scripts/${SCRIPT_NAME}"
)

for target in "${CANDIDATES[@]}"; do
    if [[ -n "${target}" && -x "${target}" ]]; then
        exec "${target}" "$@"
    fi
done

echo "Obsyx: Script not found or not executable: ${SCRIPT_NAME}" >&2
exit 127
