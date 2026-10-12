<div align="center">

# Obsyx

### A modular Hyprland desktop configuration framework

Lua configuration, themed desktop components, profiles, and command-line tools for Arch-based Linux systems.

[![Platform](https://img.shields.io/badge/Platform-Linux-1793D1?style=for-the-badge)](#requirements)
[![Wayland](https://img.shields.io/badge/Compositor-Hyprland-6E4AFF?style=for-the-badge)](#requirements)
[![Language](https://img.shields.io/badge/Configuration-Lua-2C2D72?style=for-the-badge)](#project-map)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE.md)

</div>

---

Obsyx organizes a Hyprland desktop into maintainable configuration modules. It includes Waybar, Rofi, SwayNC, Hyprlock, Kitty, and Wlogout configuration; five official themes; laptop and workstation profiles; and tools for installing the configuration, switching themes, generating keybinding documentation, and checking configuration syntax.

**Obsyx is desktop configuration software, not an operating system distribution.** This repository does not currently provide a bootable ISO, disk installer, base-system package manifest, or OS update and recovery service. The OS work described in [ROADMAP.md](ROADMAP.md) remains planned work.

## Requirements

The package recipe targets an existing Arch Linux system. The desktop configuration is built around Hyprland and Lua. Components and features require their corresponding applications, including Waybar, Rofi, SwayNC, Hyprlock, Kitty, Wlogout, a wallpaper daemon, and Wayland utilities. `obsyx doctor` reports required, recommended, and optional command-line tools; it does not install packages or prove that the session is configured correctly.

The package recipe is in [`packaging/arch/PKGBUILD`](packaging/arch/PKGBUILD). Review its dependency list and your system before installing. Obsyx does not configure a complete OS or guarantee support for every device.

## Quick start

Clone the repository, inspect the proposed changes, then install the six supported configuration trees. The installer links repository directories into your XDG config directory (normally `~/.config`). If a target already exists, it is moved to a timestamped `.backup.<timestamp>` path before the link is created. Keep the repository in place while using these links.

```bash
git clone https://github.com/dev-paulrajdeep/Obsyx.git
cd Obsyx

# Preview the default install; this makes no filesystem changes.
./bin/obsyx install --dry-run

# Install interactively, or choose a non-interactive component set.
./bin/obsyx install --interactive
# ./bin/obsyx install --components hypr,waybar,rofi

# Check dependencies and configuration syntax.
./bin/obsyx doctor
./bin/obsyx validate
```

The installer manages configuration links; it does not install dependencies. Read [Installation](docs/installer.md) before applying it to an existing `~/.config`.

## Common commands

```bash
./bin/obsyx theme list
./bin/obsyx theme apply frost --dry-run
./bin/obsyx profile list
./bin/obsyx profile apply laptop --dry-run
./bin/obsyx docgen --check
```

Use `./bin/obsyx --help` or see the [CLI reference](docs/cli.md) for all commands. Theme and profile apply commands default to `$XDG_CONFIG_HOME` or `~/.config`; use `--dest` to preview or target another directory.

## Included features

- Modular Hyprland Lua configuration for input, monitors, rules, layouts, appearance, startup, and keybindings.
- Five themes: Noctis Amethyst, Obsidian, Frost, Aurora, and Ember. Canonical JSON tokens generate component-specific styles and configuration.
- Laptop and workstation profile overrides.
- Waybar modules and telemetry scripts, Rofi launcher and utility menus, SwayNC styles, Hyprlock, Kitty, and Wlogout configuration.
- Plugin registration and lifecycle callbacks for initialization, theme changes, profile changes, and workspace changes. Plugins execute Lua code in the desktop process; the framework does not provide a plugin permission sandbox.
- `doctor`, `validate`, `install`, `theme`, `profile`, and `docgen` commands.

See [Themes](docs/themes.md), [Theme tokens](docs/theme-tokens.md), [Profiles](docs/profiles.md), [Autostart and wallpapers](docs/autostart-and-wallpapers.md), and [User overrides](user/README.md).

## Project map

| Path | Purpose |
|---|---|
| `hypr/` | Hyprland entry point, Lua modules, themes, and helper scripts |
| `core/tokens/` | Canonical JSON theme token sources |
| `waybar/`, `rofi/`, `swaync/`, `kitty/`, `wlogout/` | Desktop component configuration |
| `profiles/` | Laptop/workstation overrides and theme-specific assets |
| `bin/obsyx` | Python standard-library CLI |
| `tools/` | Token compiler, installer wrapper, packaging and validation helpers |
| `tests/` | Python unit and static integration checks |
| `docs/` | CLI, installer, theme, profile, and workflow documentation |
| `packaging/arch/` | Arch package recipe and AUR publishing helper |

## Development and checks

Python unit tests can be run with:

```bash
python3 -m unittest discover tests/ -v
```

The test suite includes Python-driven checks and a headless Wayland integration script. The headless script needs a working Hyprland build and is not equivalent to testing a full installed desktop. Syntax validation and passing unit tests do not establish boot, hardware, or installer behavior. See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

## Documentation

- [CLI reference](docs/cli.md)
- [Installer behavior and options](docs/installer.md)
- [Themes](docs/themes.md)
- [Theme token compiler](docs/theme-tokens.md)
- [Hardware profiles](docs/profiles.md)
- [Autostart and wallpapers](docs/autostart-and-wallpapers.md)
- [Keybindings](KEYBINDINGS.md)
- [Roadmap and product scope](ROADMAP.md)

## License

Obsyx is distributed under the [MIT License](LICENSE.md).
