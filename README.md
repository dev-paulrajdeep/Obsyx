<div align="center">

# Obsyx

### A modular Wayland desktop framework built on Hyprland and Lua.

*Elegant. Performant. Engineered.*

---

![Platform](https://img.shields.io/badge/Platform-Linux-blue)
![Wayland](https://img.shields.io/badge/Wayland-Hyprland-purple)
![Language](https://img.shields.io/badge/Language-Lua-blueviolet)
![Status](https://img.shields.io/badge/Status-Active%20Development-success)

</div>

---

# Overview

Obsyx is a modular desktop framework that transforms Hyprland into a cohesive operating environment.

Rather than treating desktop configuration as a collection of unrelated dotfiles, Obsyx organizes every subsystem into reusable modules with clear responsibilities.

The project applies software engineering principles—including modular architecture, separation of concerns, configuration abstraction, and reusable design systems—to desktop customization.

---

# Design Goals

Obsyx is built around five principles.

- **Modularity** — every subsystem lives independently.
- **Consistency** — appearance, interaction, and behavior follow shared rules.
- **Performance** — smooth animations and low overhead.
- **Maintainability** — scalable project architecture.
- **Extensibility** — new features should integrate without restructuring the project.

---

# Current Features

## Desktop Architecture

- Modular Lua configuration
- Registry-driven configuration
- Production-grade project hierarchy
- Environment abstraction
- Component separation

## Window Management

- Advanced window rules
- Workspace rules
- Floating policies
- Smart fullscreen behavior
- Scratch workspace
- Directional navigation
- Keyboard-first workflow

## Appearance

- Glassmorphism
- Blur pipeline
- Dynamic opacity
- Gradient borders
- Rounded geometry
- Modern animation system

## Layouts

- Dwindle
- Master
- Workspace policies
- Independent monitor workspaces

## Input

- Mouse
- Keyboard
- Touchpad
- Gesture support

---

# Project Structure

```
Obsyx
│
├── config
│   ├── appearance
│   ├── binds
│   ├── layouts
│   ├── rules
│   ├── autostart.lua
│   ├── env.lua
│   ├── general.lua
│   ├── input.lua
│   ├── misc.lua
│   ├── monitors.lua
│   └── variables.lua
│
├── themes
│
├── scripts
│
└── hyprland.lua
```

Each directory owns a single concern, making the configuration easier to extend and maintain.

---

# Philosophy

Obsyx is designed as a desktop framework rather than a collection of configuration files.

Every module should answer exactly one question.

Examples:

- How should windows behave?
- How should workspaces behave?
- How should animations feel?
- Which applications belong to the system?
- What does the visual language look like?

This architecture keeps complexity localized while allowing the desktop to evolve without becoming difficult to maintain.

---

# Technology

- Hyprland (Lua configuration)
- Wayland
- Lua
- Kitty
- Waybar
- Rofi
- SwayNC
- Hyprlock
- Hyprshot
- awww

---

# Roadmap

### Phase 1 — Foundation

- Modular architecture
- Window policies
- Workspace policies
- Animation engine
- Decoration engine

### Phase 2 — Desktop

- Waybar
- Notification center
- Lock screen
- Launcher
- Theme engine

### Phase 3 — Design System

- Shared color tokens
- Typography system
- Material presets
- Theme variants

### Phase 4 — Developer Experience

- Installer
- Dependency checker
- Configuration validation
- Documentation generator

### Phase 5 — Ecosystem

- Community themes
- Plugin support
- Package distribution
- Continuous integration

---

# Contributing

Contributions are welcome.

When contributing, prioritize:

- Readability
- Maintainability
- Consistency
- Performance
- Simplicity

---

# License

MIT License.

---

<div align="center">

**Obsyx is an exploration of what desktop configuration looks like when treated as software engineering rather than scripting.**

</div>