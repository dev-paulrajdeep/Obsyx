<div align="center">

# Obsyx

### A modular Wayland desktop framework built with Hyprland and Lua.

Elegant by design. Engineered for maintainability.

---

![Platform](https://img.shields.io/badge/Platform-Linux-1793D1?style=for-the-badge)
![Wayland](https://img.shields.io/badge/Wayland-Hyprland-6E4AFF?style=for-the-badge)
![Language](https://img.shields.io/badge/Language-Lua-2C2D72?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-7ED957?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)

</div>

---

## Overview

Obsyx is a modular desktop framework for Hyprland that treats desktop configuration as software engineering rather than a collection of configuration files.

The framework currently ships with **Noctis Amethyst**, its default reference theme, which showcases the design language, architecture, and interaction model that future themes will build upon.

Instead of one large monolithic configuration, every subsystem is isolated into reusable modules with clearly defined responsibilities.

The project focuses on:

- Clean architecture
- Modular configuration
- Consistent visual language
- Smooth interaction design
- Hardware-aware optimization
- Long-term maintainability

---

# Current Features

## Architecture

- Modular Lua configuration
- Central command registry
- Layered configuration loading
- Reusable modules
- Production-oriented file hierarchy

## Desktop

- Activity-oriented workspaces
- Advanced window management
- Comprehensive keybinding system
- Dynamic layouts
- Floating window rules
- Scratchpad workspace

## Visuals

- Glass-inspired desktop
- Blur and transparency
- Custom animation curves
- Workspace transitions
- Dynamic borders
- Rounded window geometry

## System Integration

- Wallpaper daemon
- Clipboard history
- Notifications
- Audio controls
- Brightness controls
- Screenshot workflow
- Bluetooth integration
- Network integration

---

# Goals

Obsyx provides a complete modular desktop framework featuring:

- [x] **Theme engine:** Canonical token system, multi-theme compiler, inheritance engine, and live switcher (`bin/obsyx theme`).
- [x] **Design token system:** Single-source-of-truth tokens in `core/tokens/` generating CSS, RASI, Conf, and Lua tables.
- [x] **Component library:** Cohesive Waybar status bar, Rofi menus, SwayNC notification center, Hyprlock, and Wlogout.
- [x] **Automated installer:** `bin/obsyx install` with non-destructive backups, dry-run simulation, and component selection.
- [x] **Configuration validation:** `bin/obsyx validate` verifying Lua, JSONC, Shell, and Design Token syntax.
- [x] **Documentation generator:** `bin/obsyx docgen` compiling markdown cheatsheets and interactive Rofi search.
- [x] **Multiple desktop variants:** `bin/obsyx profile` providing hardware-specific laptop and workstation profiles.
- [x] **Plugin support:** `hypr/core/plugins.lua` lifecycle hooks (`on_init`, `on_theme_change`, `on_profile_change`, `on_workspace_change`) and user overrides.

---

# Status

Current development stage:

**Phases 1–5 Complete (Desktop Framework & Official Themes) / Phase 6 Verified (Packaging & CI)**

- **Phase 1 (Foundation):** Modular Lua architecture, central registry, autostart, window/workspace rules, animations.
- **Phase 2 (Desktop Components):** Waybar status bar, Rofi launcher, SwayNC notifications/OSD, Hyprlock lock screen with idle daemon, and Wlogout.
- **Phase 3 (Design System):** Five official themes (Noctis Amethyst, Obsidian, Frost, Aurora, Ember) with deterministic inheritance.
- **Phase 4 (Developer Experience):** CLI suite (`doctor`, `validate`, `install`, `docgen`, `profile`, `theme`).
- **Phase 5 (Extensibility):** Plugin architecture with lifecycle hooks and git-clean user overrides.
- **Phase 6 (Packaging & Distribution):** PKGBUILD, AUR packaging, headless Wayland test runner, and automated GitHub Actions CI.

See:

- [ROADMAP.md](ROADMAP.md)
- [CHANGELOG.md](CHANGELOG.md)
- [docs/themes.md](docs/themes.md)
- [docs/cli.md](docs/cli.md)
- [docs/profiles.md](docs/profiles.md)

---

# License

Released under the MIT License.

---

<div align="center">

Built with Hyprland, Lua, and an appreciation for well-structured software.

</div>
