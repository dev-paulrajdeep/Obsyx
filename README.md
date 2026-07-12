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

# Design Philosophy

Obsyx follows a simple principle:

> Every configuration file should have one responsibility.

Instead of hundreds of unrelated settings inside a single file, the desktop is composed of independent modules.

```
Variables
      │
      ▼
Environment
      │
      ▼
Appearance
      │
      ▼
Layouts
      │
      ▼
Rules
      │
      ▼
Keybindings
      │
      ▼
Runtime
```

Each layer only depends on the layers above it.

---

# Project Structure

```
hypr/

├── config/
│
├── appearance/
│   ├── animations.lua
│   └── decoration.lua
│
├── binds/
│   ├── apps.lua
│   ├── media.lua
│   ├── screenshots.lua
│   ├── system.lua
│   ├── windows.lua
│   └── workspaces.lua
│
├── layouts/
│   ├── dwindle.lua
│   └── master.lua
│
├── rules/
│   ├── windows.lua
│   └── workspaces.lua
│
├── autostart.lua
├── env.lua
├── general.lua
├── input.lua
├── misc.lua
├── monitors.lua
└── variables.lua
```

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

Obsyx is evolving toward a complete desktop framework featuring:

- Theme engine
- Design token system
- Component library
- Automated installer
- Configuration validation
- Documentation generator
- Multiple desktop variants
- Plugin support

---

# Technologies

- Hyprland
- Lua
- Wayland
- Kitty
- Waybar
- Rofi
- SwayNC
- Hyprlock
- Hyprshot
- awww

---

# Philosophy

Obsyx values:

- Simplicity over complexity
- Consistency over novelty
- Architecture over shortcuts
- Performance over decoration
- Maintainability over convenience

Every module should be understandable in isolation and reusable without modification.

---

# Status

Current development stage:

**Foundation Complete**

The core architecture is implemented and actively evolving toward a fully documented desktop framework.

See:

- ROADMAP.md
- CHANGELOG.md

---

# License

Released under the MIT License.

---

<div align="center">

Built with Hyprland, Lua, and an appreciation for well-structured software.

</div>