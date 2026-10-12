# Obsyx — Arch Linux & AUR Packaging

This directory contains the official Arch Linux packaging specifications for Obsyx (`obsyx-git`).

---

## Files

- `PKGBUILD`: Arch Linux package build recipe.
- `.SRCINFO`: Machine-readable package metadata generated via `makepkg --printsrcinfo`.
- `publish_aur.sh`: Automated synchronization and publishing script for AUR maintainers.

---

## 1. Local Testing & Building

To test-build the package locally on an Arch Linux system:

```bash
cd packaging/arch
makepkg -sf
```

To install the locally built package:
```bash
sudo pacman -U obsyx-git-*.pkg.tar.zst
```

---

## 2. Publishing to the AUR

### Prerequisites
1. Create an account on the [Arch User Repository (AUR)](https://aur.archlinux.org/).
2. Add your SSH public key to your AUR account profile (`My Account` → `SSH Public Key`).
3. Verify SSH connection:
   ```bash
   ssh -T aur@aur.archlinux.org
   # Expected output: Interactive shell is disabled.
   ```

### Publishing Steps
Run the automated publishing script:
```bash
# Verify files without pushing:
./packaging/arch/publish_aur.sh --dry-run

# Publish to AUR:
./packaging/arch/publish_aur.sh
```

### Manual Publishing (Alternative)
```bash
git clone ssh://aur@aur.archlinux.org/obsyx-git.git /tmp/aur-obsyx
cp packaging/arch/PKGBUILD packaging/arch/.SRCINFO /tmp/aur-obsyx/
cd /tmp/aur-obsyx
git add PKGBUILD .SRCINFO
git commit -m "Update obsyx-git to latest release"
git push origin master
```
