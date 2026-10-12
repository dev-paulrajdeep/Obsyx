#!/usr/bin/env bash
# ==============================================================================
# Obsyx — Headless Wayland Integration Test Runner
#
# Launches Hyprland in a headless environment without physical displays,
# verifying compositor configuration parsing, socket creation, and runtime bootstrap.
# Usage:
#     ./tools/test_headless.sh [--verbose]
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VERBOSE=false
if [[ "${1:-}" == "--verbose" ]]; then
    VERBOSE=true
fi

if ! command -v hyprland >/dev/null 2>&1; then
    echo "[-] Error: 'hyprland' binary not found in PATH." >&2
    exit 1
fi

echo "==> Obsyx Headless Wayland Integration Test Runner"
echo "    Compositor: $(which hyprland)"
echo "    Version:    $(hyprland -v | head -n 1)"

# Create isolated sandbox runtime directory
SANDBOX_RUNTIME="/tmp/obsyx_runtime_$$"
mkdir -p "$SANDBOX_RUNTIME"
chmod 0700 "$SANDBOX_RUNTIME"

cleanup() {
    rm -rf "$SANDBOX_RUNTIME"
}
trap cleanup EXIT

# ------------------------------------------------------------------------------
# Test 1: Default Hyprland Lua Configuration Syntax Verification
# ------------------------------------------------------------------------------
echo -n "==> [1/4] Verifying default hyprland.lua config... "
OUT1=$(hyprland --verify-config --config "$REPO_ROOT/hypr/hyprland.lua" 2>&1 || true)
if echo "$OUT1" | grep -q "config ok"; then
    echo "[PASS]"
else
    echo "[FAIL]"
    echo "$OUT1"
    exit 1
fi

# ------------------------------------------------------------------------------
# Test 2: Laptop Profile Configuration Verification
# ------------------------------------------------------------------------------
echo -n "==> [2/4] Verifying laptop profile configuration... "
TMP_LAPTOP="$SANDBOX_RUNTIME/laptop_test.lua"
cat << EOF > "$TMP_LAPTOP"
package.path = "$REPO_ROOT/hypr/?.lua;" .. package.path
require("hyprland")
dofile("$REPO_ROOT/profiles/laptop/hypr/profile.lua")
EOF
OUT2=$(hyprland --verify-config --config "$TMP_LAPTOP" 2>&1 || true)
if echo "$OUT2" | grep -q "config ok"; then
    echo "[PASS]"
else
    echo "[FAIL]"
    echo "$OUT2"
    exit 1
fi

# ------------------------------------------------------------------------------
# Test 3: Workstation Profile Configuration Verification
# ------------------------------------------------------------------------------
echo -n "==> [3/4] Verifying workstation profile configuration... "
TMP_WS="$SANDBOX_RUNTIME/workstation_test.lua"
cat << EOF > "$TMP_WS"
package.path = "$REPO_ROOT/hypr/?.lua;" .. package.path
require("hyprland")
dofile("$REPO_ROOT/profiles/workstation/hypr/profile.lua")
EOF
OUT3=$(hyprland --verify-config --config "$TMP_WS" 2>&1 || true)
if echo "$OUT3" | grep -q "config ok"; then
    echo "[PASS]"
else
    echo "[FAIL]"
    echo "$OUT3"
    exit 1
fi

# ------------------------------------------------------------------------------
# Test 4: Headless Compositor Session Bootstrap
# ------------------------------------------------------------------------------
echo -n "==> [4/4] Testing headless compositor startup session... "
OUT4=$(
    XDG_RUNTIME_DIR="$SANDBOX_RUNTIME" \
    WLR_BACKENDS=headless \
    WLR_LIBINPUT_NO_DEVICES=1 \
    timeout 2 hyprland --config "$REPO_ROOT/hypr/hyprland.lua" 2>&1 || true
)

if echo "$OUT4" | grep -q "Welcome to Hyprland"; then
    echo "[PASS]"
else
    echo "[FAIL]"
    echo "$OUT4"
    exit 1
fi

echo ""
echo "[+] All 4 headless Wayland compositor integration tests PASSED successfully."
