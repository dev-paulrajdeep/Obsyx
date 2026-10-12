# Changelog

All notable changes to **Obsyx** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-10-12

### Overview
First major feature release of Obsyx as a complete, modular Wayland desktop framework built with Hyprland and Lua. Ships with **Noctis Amethyst** as the reference theme.

### Added

#### 🎨 Design Token Engine & Themes
- Centralized canonical token dictionary in `core/tokens/noctis_amethyst.json`.
- Deterministic token compiler in `tools/build_tokens.py` compiling to:
  - Hyprland Lua theme table (`hypr/themes/noctis_amethyst.lua`)
  - Waybar GTK3 CSS tokens (`waybar/generated/theme-tokens.css`)
  - Rofi RASI tokens (`rofi/generated/theme-tokens.rasi`)
  - SwayNC GTK3 CSS tokens (`swaync/generated/theme-tokens.css`)
  - Hyprland & Hyprlock conf tokens (`hypr/generated/theme-tokens.conf`)
  - Kitty terminal emulator colors (`kitty/generated/theme-tokens.conf`)
  - Wlogout GTK3 CSS tokens (`wlogout/generated/theme-tokens.css`)
- Dynamic theme loader (`hypr/config/theme.lua`) and reactive decoration binding (`hypr/config/appearance/decoration.lua`).
- Token verification mode (`python3 tools/build_tokens.py --check`) for CI and pre-commit checks.

#### 🖥 Desktop Component Library
- **Rofi:** Glass application launcher (`drun`), power menu overlay (`powermenu.sh`), and clipboard manager (`cliphist.sh`).
- **SwayNC:** Notification daemon and control center styled with translucent glass and accent highlights.
- **Hyprlock:** Screen locker with dynamic blurred wallpaper backgrounds, clock widgets, and password prompts.
- **Kitty:** Terminal configuration importing Noctis Amethyst palette tokens.
- **Wlogout:** Full-screen logout, reboot, and power action menu.
- **Wallpaper Daemon:** Canonical wallpaper asset structure and `hyprpaper` autostart configuration.
- **Waybar Telemetry:** Portable telemetry scripts (`waybar/scripts/runner.sh`) for CPU, GPU, memory, network, media, and VPN with dynamic path resolution.

#### 🛠 Obsyx CLI Suite (`bin/obsyx`)
- `obsyx doctor`: Comprehensive system diagnostic checking required, recommended, and optional binaries with `--json` output.
- `obsyx validate`: Syntax and schema validator across Lua (`luac -p`), JSON/JSONC stylesheets, shell scripts (`bash -n`), and design tokens.
- `obsyx install`: Non-destructive symlink installer with `--dry-run`, automatic timestamped backups (`~/.config/hypr.backup.<timestamp>`), selective component linking, and sandbox destination overrides.
- `obsyx docgen`: Automated keybindings parser generating markdown cheatsheets (`KEYBINDINGS.md`) and interactive executable Rofi search modal.
- `obsyx profile`: Hardware and form-factor profile manager supporting `list`, `show`, and `apply` with live compositor reload signals.

#### ⚙️ Hardware Profiles
- **Laptop Profile (`profiles/laptop/`):** Battery-saving profile with single blur pass, disabled window shadows, and compact 32px Waybar.
- **Workstation Profile (`profiles/workstation/`):** High-performance profile with triple blur passes, ambient shadows, VRR enabled, and expanded 40px telemetry bar.

#### 🔌 Plugin Architecture & User Overrides
- Lifecycle hook engine (`hypr/core/plugins.lua`) with `on_init`, `on_theme_change`, `on_profile_change`, and `on_workspace_change`.
- Protected call (`pcall`) execution isolating plugin faults from compositor startup.
- Git-clean user overrides framework in `user/` (`user/hyprland.lua`, `user/waybar.jsonc`) excluded from git tracking while tracking templates.

#### 📦 Distribution & Packaging
- Arch Linux PKGBUILD and `.SRCINFO` in `packaging/arch/`.
- Automated AUR synchronization script (`packaging/arch/publish_aur.sh`).
- Headless Wayland integration test runner (`tools/test_headless.sh`).
- Release packaging script (`tools/package_release.py`).
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) matrix-testing Python 3.10–3.13 and Lua 5.4.