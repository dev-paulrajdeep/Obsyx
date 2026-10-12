# Obsyx Desktop architecture

Obsyx is a user-session configuration framework. Hyprland loads a Lua entry point, the entry point builds shared registry/theme state, and focused modules register compositor settings, rules, bindings, and startup services.

## Startup path

`hypr/hyprland.lua` loads the desktop in this order:

1. Plugin module and global `Plugins` reference.
2. `config.variables`, which creates `Registry`.
3. `config.theme`, which loads a theme and publishes `Theme` and `Registry.Theme.current`.
4. Environment, monitor/input, general/misc settings, appearance, layouts, rules, and keybindings.
5. Optional profile override and user overrides.
6. `config.autostart`, followed by the `on_init` lifecycle event.

The sequence is significant: configuration modules consume `Registry` and `Theme`, and profile/user code runs after the core settings have loaded.

## Main boundaries

| Area | Responsibility |
|---|---|
| `hypr/config/variables.lua` | Shared application commands, component commands, startup commands, paths, theme name, media, screenshot, and session commands |
| `hypr/config/appearance/` | Theme-driven decoration and animation settings |
| `hypr/config/layouts/` | Dwindle and master layout configuration |
| `hypr/config/rules/` | Window, workspace, and layer rules |
| `hypr/config/binds/` | Application, window, workspace, media, screenshot, and session bindings |
| `hypr/config/autostart.lua` | Ordered session processes and delayed wallpaper dispatch |
| `hypr/themes/`, `core/tokens/` | Runtime Lua themes and their JSON design-token sources |
| `hypr/core/plugins.lua` | In-process plugin registry and lifecycle callbacks |
| `profiles/` | Explicit laptop/workstation override files and Waybar variants |
| `user/` | Examples and Git-ignored local override extension points |
| `waybar/`, `rofi/`, `swaync/`, `kitty/`, `wlogout/` | Companion user-session applications and their styles |
| `bin/obsyx`, `tools/` | CLI, token generation, validation, packaging, and helper scripts |

## Theme data flow

Theme JSON files in `core/tokens/` are compiled by `tools/build_tokens.py` into runtime Lua and component-specific CSS, RASI, and conf artifacts. Hyprland's theme loader reads the selected runtime Lua table. `obsyx theme apply` stores theme state and regenerates output files in the chosen XDG config root.

Generated files are committed for distribution; edit token sources and regenerate outputs rather than changing generated files manually. See [Theme tokens](theme-tokens.md) and [Theme development](themes.md).

## Product boundary

This architecture configures an already installed desktop session. It does not build an ISO, partition disks, install a base operating system, or provide system update/recovery infrastructure. See [ROADMAP.md](../ROADMAP.md) for the separate Obsyx OS work.
