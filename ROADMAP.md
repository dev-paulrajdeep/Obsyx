# Obsyx Roadmap

> Building a luxury, modular Wayland desktop engineered with the same principles used in modern software systems:
>
> - Modular architecture
> - Separation of concerns
> - Design tokens
> - Declarative configuration
> - Reusable components
> - Hardware-aware optimization

# Obsyx Roadmap

This roadmap outlines the long-term vision for **Obsyx**, a modular desktop framework built on **Hyprland** and **Lua**.

> **Current Status:** Phase 1 Complete ✅

---

# Phase 1 — Foundation ✅

**Objective:** Build a stable, modular, production-grade architecture.

## Core Architecture

- [x] Modular Lua configuration hierarchy
- [x] Layered configuration loading
- [x] Production-grade file organization
- [x] Central configuration registry
- [x] Shared variables system

## Runtime

- [x] Environment management
- [x] Autostart framework
- [x] Monitor abstraction
- [x] Input abstraction
- [x] System configuration

## Desktop Core

- [x] Window management
- [x] Workspace management
- [x] Layout modules
- [x] Window rules
- [x] Workspace rules

## Visual Engine

- [x] Animation engine
- [x] Decoration engine
- [x] Blur system
- [x] Border system
- [x] Glass styling

## Interaction

- [x] Application keybindings
- [x] System keybindings
- [x] Media keybindings
- [x] Screenshot workflow
- [x] Window navigation

---

# Phase 2 — Desktop Components

**Objective:** Replace individual desktop utilities with a cohesive desktop experience.

## Status Bar

- [ ] Modular Waybar architecture
- [ ] Workspace indicators
- [ ] Active window title
- [ ] Media controls
- [ ] Volume widget
- [ ] Brightness widget
- [ ] Battery widget
- [ ] Network widget
- [ ] Bluetooth widget
- [ ] VPN widget
- [ ] CPU monitor
- [ ] RAM monitor
- [ ] GPU monitor
- [ ] Temperature monitor
- [ ] Clock
- [ ] Calendar popup
- [ ] System tray

## Launcher

- [ ] Application launcher
- [ ] File launcher
- [ ] Power menu
- [ ] Calculator mode
- [ ] Clipboard browser
- [ ] Emoji picker
- [ ] Theme-aware styling
- [ ] Icon support
- [ ] Blur integration

## Notifications

- [ ] Notification center
- [ ] Control center
- [ ] Volume OSD
- [ ] Brightness OSD
- [ ] Screenshot preview

## Lock Screen

- [ ] Custom lock screen
- [ ] Background blur
- [ ] Media widget
- [ ] User profile
- [ ] Time & date
- [ ] Battery indicator
- [ ] Idle integration

## Logout Menu

- [ ] Themed logout interface
- [ ] Animated transitions
- [ ] Icon redesign

## Wallpaper Engine

- [ ] Wallpaper daemon integration
- [ ] Automatic preload
- [ ] Wallpaper cache
- [ ] Multi-monitor support
- [ ] Dynamic wallpaper switching

## Desktop Theme

- [ ] GTK theme
- [ ] Qt theme
- [ ] Cursor theme
- [ ] Icon theme
- [ ] Font stack
- [ ] Terminal theme
- [ ] VS Code theme
- [ ] Browser theme

---

# Phase 3 — Design System

**Objective:** Transform Obsyx from a single desktop into a reusable desktop framework.

## Theme Engine

- [ ] Theme registry
- [ ] Theme loader
- [ ] Theme metadata
- [ ] Theme inheritance
- [ ] Theme validation

## Design Tokens

- [ ] Color tokens
- [ ] Accent palette
- [ ] Surface colors
- [ ] Typography tokens
- [ ] Radius tokens
- [ ] Blur tokens
- [ ] Shadow tokens
- [ ] Animation tokens
- [ ] Opacity tokens
- [ ] Spacing tokens

## Component Library

- [ ] Window styling
- [ ] Panel styling
- [ ] Menu styling
- [ ] Notification styling
- [ ] Dialog styling
- [ ] Widget styling
- [ ] Overlay styling

## Motion System

- [ ] Shared animation presets
- [ ] Shared bezier curves
- [ ] Shared spring physics
- [ ] Transition library

## Official Themes

Obsyx ships with **Noctis Amethyst** as its default reference theme. Future official themes will build upon the same architecture and design system.

- [ ] Noctis Amethyst *(Reference Theme)*
- [ ] Obsidian
- [ ] Frost
- [ ] Aurora
- [ ] Ember

---

# Phase 4 — Developer Experience

**Objective:** Make Obsyx simple to install, maintain, and contribute to.

## Installer

- [ ] Interactive installer
- [ ] Minimal installation
- [ ] Full installation
- [ ] Package detection
- [ ] Existing configuration backup

## Tooling

- [ ] Dependency checker
- [ ] Configuration validator
- [ ] Theme validator
- [ ] Health diagnostics
- [ ] System compatibility checker

## Command Line Interface

- [ ] `obsyx install`
- [ ] `obsyx update`
- [ ] `obsyx doctor`
- [ ] `obsyx theme`
- [ ] `obsyx backup`
- [ ] `obsyx restore`

## Documentation

- [ ] Architecture guide
- [ ] Configuration reference
- [ ] Theme development guide
- [ ] Plugin guide
- [ ] Lua API documentation
- [ ] Screenshots
- [ ] GIF demonstrations

---

# Phase 5 — Extensibility

**Objective:** Transform Obsyx into an extensible desktop platform.

## Plugin Framework

- [ ] Plugin loader
- [ ] Plugin registry
- [ ] Plugin lifecycle
- [ ] Event hooks
- [ ] Permission model

## APIs

- [ ] Theme API
- [ ] Widget API
- [ ] Animation API
- [ ] Layout API
- [ ] Rule API

## Widgets

- [ ] Dashboard widgets
- [ ] Weather widget
- [ ] Music widget
- [ ] Calendar widget
- [ ] Notes widget
- [ ] System monitor widget

## Extensions

- [ ] Third-party plugins
- [ ] Community widgets
- [ ] Optional desktop modules

---

# Phase 6 — Distribution

**Objective:** Make Obsyx easy to install, package, test, and release.

## Packaging

- [ ] PKGBUILD
- [ ] AUR package
- [ ] Binary releases
- [ ] Semantic versioning
- [ ] Release notes

## Automation

- [ ] GitHub Actions
- [ ] Lua linting
- [ ] Code formatting
- [ ] Build verification
- [ ] Dependency validation
- [ ] Automatic screenshots
- [ ] Documentation deployment

## Quality Assurance

- [ ] Configuration regression tests
- [ ] Theme validation tests
- [ ] Startup verification
- [ ] Performance benchmarks
- [ ] Memory profiling

---

# Phase 7 — ObsyxOS Vision

**Objective:** Build a complete desktop ecosystem around Obsyx.

## Desktop Experience

- [ ] First-boot wizard
- [ ] Welcome application
- [ ] Settings application
- [ ] Theme manager
- [ ] Wallpaper browser
- [ ] Extension manager

## Ecosystem

- [ ] Official website
- [ ] Documentation portal
- [ ] Showcase gallery
- [ ] Community themes
- [ ] Community plugins
- [ ] User handbook

## Long-Term Vision

- [ ] Stable release channel
- [ ] Beta release channel
- [ ] Nightly builds
- [ ] LTS editions
- [ ] Multi-distribution support
- [ ] Complete desktop framework

---

# Future Ideas

These ideas are intentionally kept outside the main roadmap until the core framework reaches maturity.

- AI-powered wallpaper recommendations
- Dynamic color extraction
- Per-monitor themes
- Automatic day/night themes
- Workspace templates
- Session restoration
- Desktop profiles
- Remote synchronization
- Cloud backup
- Mobile companion application

Obsyx is intended to evolve from a personal Hyprland configuration into a modular desktop framework focused on clean architecture, consistency, and performance.