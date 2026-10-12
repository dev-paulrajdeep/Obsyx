#!/usr/bin/env bash
# ==============================================================================
# Obsyx — AUR Package Publishing Automation
#
# Automates updating and publishing the obsyx-git package to the Arch User Repository.
# Usage:
#     ./packaging/arch/publish_aur.sh [--dry-run]
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PKG_NAME="obsyx-git"
AUR_REPO_URL="ssh://aur@aur.archlinux.org/${PKG_NAME}.git"
WORK_DIR="/tmp/aur_${PKG_NAME}_$$"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

echo "==> Obsyx AUR Publisher"
echo "    Package: $PKG_NAME"
echo "    Source:  $SCRIPT_DIR/PKGBUILD"

# 1. Verify Arch packaging tools
if ! command -v makepkg >/dev/null 2>&1; then
    echo "[-] Error: 'makepkg' command not found. Run on an Arch Linux system." >&2
    exit 1
fi

# 2. Update .SRCINFO from PKGBUILD
echo "==> Generating latest .SRCINFO..."
cd "$SCRIPT_DIR"
makepkg --printsrcinfo > .SRCINFO
echo "[+] .SRCINFO regenerated successfully."

# 3. Check SSH connectivity to aur.archlinux.org
echo "==> Checking AUR SSH authentication..."
if ! ssh -T aur@aur.archlinux.org 2>&1 | grep -q "Interactive shell is disabled"; then
    echo "[-] Warning: Could not authenticate with aur.archlinux.org via SSH."
    echo "    To publish to the AUR:"
    echo "    1. Register an account at https://aur.archlinux.org/"
    echo "    2. Add your public SSH key (~/.ssh/id_ed25519.pub) to your account profile."
    echo "    3. Test connection with: ssh -T aur@aur.archlinux.org"
    echo ""
    echo "    Local packaging files (PKGBUILD and .SRCINFO) are up to date in packaging/arch/."
    exit 1
fi

if [[ "$DRY_RUN" == true ]]; then
    echo "[+] Dry run complete: PKGBUILD and .SRCINFO verified. Skipping AUR git push."
    exit 0
fi

# 4. Clone AUR repository to temporary workspace
echo "==> Cloning $AUR_REPO_URL into temporary workspace..."
rm -rf "$WORK_DIR"
git clone "$AUR_REPO_URL" "$WORK_DIR" || {
    echo "[-] AUR repository clone failed. If this is the initial package creation,"
    echo "    initialize the repository according to AUR submission guidelines."
    exit 1
}

# 5. Copy updated package files
cp "$SCRIPT_DIR/PKGBUILD" "$WORK_DIR/PKGBUILD"
cp "$SCRIPT_DIR/.SRCINFO" "$WORK_DIR/.SRCINFO"

cd "$WORK_DIR"
git status -s

if git diff --quiet PKGBUILD .SRCINFO; then
    echo "[+] No package changes detected. AUR is already up to date."
    rm -rf "$WORK_DIR"
    exit 0
fi

# 6. Commit and Push
PKG_VER="$(grep '^pkgver=' PKGBUILD | cut -d= -f2)"
PKG_REL="$(grep '^pkgrel=' PKGBUILD | cut -d= -f2)"
COMMIT_MSG="Update to version ${PKG_VER}-${PKG_REL}"

git add PKGBUILD .SRCINFO
git commit -m "$COMMIT_MSG"
git push origin master

echo "[+] Successfully published ${PKG_NAME} ${PKG_VER}-${PKG_REL} to AUR!"
rm -rf "$WORK_DIR"
