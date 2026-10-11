# Obsyx Roadmap

> Building a luxury, modular Wayland desktop—and evolving it into a reproducible Arch-based operating system—using the same principles as modern software systems:
>
> - Modular architecture
> - Separation of concerns
> - Design tokens
> - Declarative configuration
> - Reusable components
> - Hardware-aware optimization

This roadmap covers two related but distinct products:

- **Obsyx Desktop:** a modular, configurable desktop framework built around Hyprland, Lua, and a cohesive ecosystem of Wayland tools.
- **Obsyx OS:** a bootable, installable **Arch-based Linux distribution** that integrates Obsyx Desktop with the base operating system, hardware support, installation, updates, security, and recovery.

> **Current status:** Phase 1 of the desktop framework is marked complete in this roadmap. The remaining desktop phases are still tracked below. **Distro-specific engineering has not started** and is planned as a separate workstream; completing dotfiles alone does not produce an operating system.

## Scope Boundary — Desktop Framework vs Operating System

Obsyx Desktop owns the user-session experience: Hyprland and Lua configuration, Waybar/Rofi/notifications/lock screen styling, design tokens, themes, desktop profiles, plugins, and user-space diagnostic tools.

Obsyx OS additionally needs the system layers that dotfiles do not provide:

- A versioned base-package manifest and a defined relationship with Arch Linux upstream.
- A bootable live image, kernel/initramfs/boot configuration, and live-session defaults.
- A safe installation path that partitions/formats disks, installs packages, configures the bootloader, creates users, and generates a bootable target system.
- System-level integration: networking, audio, graphics/drivers, firmware, power management, login/session startup, portals, and service defaults.
- Release artifacts, signature/checksum verification, testing across clean installations and hardware, documentation, update policy, and recovery guidance.
- Long-term maintenance for upstream changes, security fixes, installer failures, and user support.

**Initial strategy:** build a focused Arch-based distribution using Arch's packages and existing image-building infrastructure. Do not fork the kernel, package manager, or the entire package ecosystem for the first release.

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

# Phase 6 — Desktop Framework Packaging & Distribution

**Objective:** Make the Obsyx desktop framework easy to install on an existing Arch system, package, test, and release. This phase does not by itself create a bootable operating-system distribution.

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

# Phase 7 — ObsyxOS Product Experience & Ecosystem

**Objective:** Build the user-facing desktop experience and community ecosystem that will ship with Obsyx OS.

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

# Phase 8 — Base Operating System & Architecture

**Objective:** Define the system Obsyx OS ships, what it inherits from Arch Linux, and what Obsyx itself is responsible for maintaining.

## Product Scope & Support Policy

- [ ] Define the initial audience and product promise
- [ ] Set initial architecture scope: x86_64 PCs and laptops
- [ ] Choose and document the initial boot target (UEFI-first; legacy BIOS support is a separate decision)
- [ ] Document the relationship to Arch Linux upstream and its rolling-release model
- [ ] Define a support window and update expectations appropriate for an Arch-based rolling release
- [ ] Publish an initial supported-hardware matrix and explicit non-goals
- [ ] Decide which components are upstream packages, AUR packages, Obsyx configuration, or Obsyx-maintained packages

## Base System Manifest

- [ ] Maintain a version-controlled list of packages installed in the live image and target system
- [ ] Separate base, boot, network, audio, graphics, firmware, desktop, accessibility, and optional development packages
- [ ] Define systemd service defaults and explain why each enabled service is needed
- [ ] Define defaults for users/groups, sudo or privilege escalation, hostname, locale, timezone, keyboard layout, and time synchronization
- [ ] Define pacman configuration, package-signature policy, keyring handling, mirror configuration, and update behavior
- [ ] Keep live-session configuration separate from installed-system configuration
- [ ] Document proprietary/optional driver choices and licensing implications
- [ ] Avoid maintaining a custom kernel or package manager for the initial release

## System Integration Decisions

- [ ] Choose and document the supported filesystem and partitioning layouts
- [ ] Decide the default swap strategy and whether hibernation is in scope
- [ ] Decide whether disk encryption is supported by the first installer release
- [ ] Choose the supported login/session-start path for Hyprland
- [ ] Define recovery access when the graphical session fails (TTY and documented rescue procedure)
- [ ] Document how configuration defaults coexist with user-owned configuration after installation

---

# Phase 9 — Bootable ISO & Live Environment

**Objective:** Produce a reproducible image that boots on supported hardware and presents a usable Obsyx live session.

## Image Build

- [ ] Build a maintained `archiso` profile rather than hand-assembling an ISO
- [ ] Keep image profile, package lists, boot configuration, and live-session overlays in version control
- [ ] Build the ISO reproducibly in a clean environment and record build inputs
- [ ] Include kernel, initramfs, required firmware, microcode where appropriate, and boot configuration
- [ ] Configure UEFI boot and document any unsupported boot modes
- [ ] Configure the live user/session without exposing unnecessary privileges or credentials
- [ ] Provide working networking in the live environment
- [ ] Provide a TTY/rescue path if Hyprland or the display stack fails
- [ ] Set sensible defaults for logs, temporary files, and live-session cleanup

## Image Validation

- [ ] Boot the ISO in a virtual machine using a clean UEFI configuration
- [ ] Test boot, login, networking, audio, display resolution, shutdown, and reboot
- [ ] Test the image on representative physical hardware before public alpha
- [ ] Publish release version, build date, architecture, package manifest, checksum, and known issues
- [ ] Sign release artifacts where supported and publish verification instructions
- [ ] Automate ISO build and smoke tests in CI where practical

---

# Phase 10 — Installer & First Boot

**Objective:** Safely turn the live environment into a bootable, usable installed system.

## Installer Strategy & Storage

- [ ] Evaluate reusing an established Arch installer versus maintaining a custom installer
- [ ] Document the installer decision and its maintenance implications
- [ ] Support a clearly defined UEFI/GPT installation path
- [ ] Detect disks and show the target device clearly before destructive operations
- [ ] Require explicit confirmation before partitioning or formatting
- [ ] Define supported filesystem, root layout, EFI System Partition, and swap options
- [ ] Decide whether optional full-disk encryption is included in the initial release
- [ ] Handle insufficient disk space, missing network, unavailable mirrors, and interrupted installation safely

## System Installation

- [ ] Install the version-controlled package set to the target system
- [ ] Generate and validate `fstab`
- [ ] Configure bootloader and verify that the installed system can boot independently of the ISO
- [ ] Create the user account and configure administrator privileges safely
- [ ] Apply locale, timezone, keyboard, hostname, networking, and system-time configuration
- [ ] Enable only the required system services
- [ ] Apply Obsyx desktop defaults without overwriting unrelated user data silently
- [ ] Write useful installation logs and provide actionable error messages
- [ ] Provide a recovery/retry path for common installation failures

## First-Run Experience

- [ ] Build a first-boot/welcome flow with hardware and network status
- [ ] Confirm that the desktop starts correctly after a fresh installation
- [ ] Explain update behavior, backups, support scope, and known limitations
- [ ] Test the full install from a clean virtual disk, including reboot into the installed system

---

# Phase 11 — Hardware & System Integration

**Objective:** Make the distribution behave like a coherent operating system across its supported hardware, not only on the development machine.

## Essential System Services

- [ ] Reliable wired and Wi-Fi networking
- [ ] Audio through PipeWire and the required session services
- [ ] Bluetooth support, with pairing tested on supported hardware
- [ ] Desktop portals, polkit integration, D-Bus, and session/logind integration
- [ ] Removable storage and filesystem mounting behavior
- [ ] Font rendering, emoji, language/input support, and accessibility basics
- [ ] Printer/scanner support documented as included, optional, or out of scope
- [ ] Correct suspend, resume, lid-switch, brightness, and power-button behavior on supported laptops

## Graphics & Device Support

- [ ] Validate AMD and Intel graphics paths where supported
- [ ] Define NVIDIA driver support and installation/update behavior separately from the generic graphics path
- [ ] Handle firmware packages and CPU microcode appropriately
- [ ] Verify multi-monitor, hot-plug, scaling, and common display resolutions
- [ ] Verify hardware keys, touchpads, trackpoints, and battery reporting on supported laptops
- [ ] Publish known limitations and tested device models rather than implying universal compatibility
- [ ] Keep optional workstation/developer packages separate from the minimal installation

## Resilience

- [ ] Ensure the system remains diagnosable from a TTY if the desktop fails
- [ ] Add `obsyx doctor` checks for distro-specific services, boot state, drivers, networking, and package consistency where feasible
- [ ] Confirm that user overrides survive framework updates
- [ ] Test shutdown, reboot, sleep/wake, display reconnect, and failed-session recovery

---

# Phase 12 — Security, Updates & Recovery

**Objective:** Make installation, daily updates, and failure recovery understandable and reasonably safe for users.

## Security Baseline

- [ ] Document the threat model and security responsibilities inherited from Arch Linux versus maintained by Obsyx
- [ ] Verify package and image signatures/checksums using the relevant upstream mechanisms
- [ ] Use least-privilege service and user defaults
- [ ] Avoid hard-coded passwords, private keys, tokens, or machine-specific secrets in the image and repository
- [ ] Review enabled services, default file permissions, sudo policy, and installer privilege boundaries
- [ ] Document firewall options and provide a sensible recommendation without promising that a firewall alone makes the system secure
- [ ] Establish a process for responding to security-related reports and upstream advisories
- [ ] Treat Secure Boot as an explicit compatibility/security project; do not claim support until it is tested end to end

## Updates & Recovery

- [ ] Define how users update the system using the supported Arch package-management workflow
- [ ] Explain rolling-release update expectations and the need to read relevant upstream announcements
- [ ] Test package updates and upgrades in clean virtual machines before promoting a release image
- [ ] Document recovery from a failed graphical login, broken boot configuration, and interrupted upgrade
- [ ] Provide backup guidance and clarify what Obsyx backup/restore does and does not cover
- [ ] Evaluate filesystem snapshots/rollback as an optional later feature, not an assumed guarantee
- [ ] Define how user configuration is preserved across Obsyx updates
- [ ] Publish a disaster-recovery guide and a known-issues page

---

# Phase 13 — Release Engineering & Maintenance

**Objective:** Establish a sustainable process for building, validating, publishing, and maintaining Obsyx OS releases.

## Package & Repository Strategy

- [ ] Start with official Arch repositories wherever possible
- [ ] Track AUR dependencies explicitly and document their trust/maintenance implications
- [ ] Create an Obsyx package repository only when independent versioning or release control justifies the operational burden
- [ ] If a custom repository is introduced, establish package signing, repository metadata generation, mirroring/availability, and key-rotation procedures
- [ ] Version and release Obsyx-specific packages independently where appropriate
- [ ] Publish package manifests and build provenance for each ISO release

## CI & Release Pipeline

- [ ] Automate ISO build jobs with pinned/recorded build inputs where practical
- [ ] Run package-list, configuration, boot-image, and installer validation
- [ ] Boot-test the ISO in virtual machines in CI
- [ ] Test fresh installation and post-install boot on a documented hardware matrix
- [ ] Generate checksums, release notes, package manifest, and installation documentation
- [ ] Publish signed or otherwise verifiable release artifacts
- [ ] Maintain alpha, beta, and stable release criteria
- [ ] Document rollback of a bad Obsyx image release and removal of broken Obsyx packages

## Maintenance & Support

- [ ] Define a realistic release cadence and maintenance ownership
- [ ] Track Arch upstream changes that affect the image, installer, desktop, or package selection
- [ ] Define issue templates for installation, boot, hardware, update, and desktop problems
- [ ] Publish support boundaries and a contribution process
- [ ] Establish a policy for unmaintained packages, security fixes, and end-of-support notices
- [ ] Avoid promising an LTS edition until there is capacity to maintain one

## Licensing, Attribution & Privacy

- [ ] Audit redistribution obligations for all shipped packages, fonts, icons, wallpapers, themes, and other assets
- [ ] Include required license texts, notices, attribution, and source-code offers where applicable
- [ ] Review use of third-party names and logos, including Arch Linux and upstream projects
- [ ] Publish a privacy and telemetry policy; document what the system sends over the network
- [ ] Keep telemetry off by default unless there is a clear, documented, opt-in reason to enable it

---

# Obsyx OS Alpha — Release Gate

Do not call Obsyx OS an installable alpha until all required checks below pass:

- [ ] A versioned ISO builds successfully from a clean environment
- [ ] The ISO boots in a clean UEFI virtual machine
- [ ] Networking works in the live environment
- [ ] The installer clearly identifies the target disk and protects against accidental destructive actions
- [ ] A fresh installation completes and boots without relying on the live ISO
- [ ] User creation, administrator access, network, audio, graphics, and the Hyprland session work on the declared supported test system
- [ ] A TTY/rescue route exists for graphical-session failure
- [ ] Update, backup, recovery, and known-limitations documentation is published
- [ ] Checksums, release notes, package manifest, and artifact verification instructions are available
- [ ] Clean-install and smoke-test results are recorded; no unsupported hardware claims are made

## Explicit Non-Goals for the First Release

- No independent kernel fork
- No replacement package manager
- No attempt to mirror or fork the entire Arch package ecosystem
- No promise of universal hardware compatibility
- No LTS guarantee or long-term support window beyond what the project can maintain
- No custom desktop applications unless they materially improve the core install/use/update experience
- No assumption that passing dotfile/configuration tests proves the complete OS works

---

# Future Ideas

These ideas are intentionally outside the initial OS release scope. Revisit them once the desktop framework and distribution pipeline are stable.

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

Obsyx is intended to evolve from a personal Hyprland configuration into a modular desktop framework and, eventually, a reproducible Arch-based operating system. The desktop framework defines the user experience; Obsyx OS adds the boot, installation, base-system integration, hardware support, security, release, update, and recovery engineering required to ship that experience as a maintained distribution.