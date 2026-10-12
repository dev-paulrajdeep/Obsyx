# Configuration reference

This is a map of the tracked user-session configuration. Files under `generated/` are compiler outputs; user-specific overrides should go through the documented override/profile mechanisms where possible.

## Hyprland Lua configuration

The entry point is `hypr/hyprland.lua`. It loads focused files from `hypr/config/`:

| Path | Settings |
|---|---|
| `variables.lua` | `Registry` tables for commands, startup, paths, themes, media, screenshots, and session actions |
| `env.lua`, `monitors.lua`, `input.lua` | Environment, display, and input settings |
| `general.lua`, `misc.lua` | Compositor-wide behavior and miscellaneous settings |
| `appearance/decoration.lua`, `appearance/animations.lua` | Theme-backed geometry, opacity, blur, shadows, borders, and motion |
| `layouts/dwindle.lua`, `layouts/master.lua` | Layout behavior |
| `rules/windows.lua`, `rules/workspaces.lua`, `rules/layers.lua` | Window/workspace/layer policy |
| `binds/*.lua` | Keyboard bindings grouped by activity |
| `autostart.lua` | Session startup sequence |

The `Registry` is the shared command/configuration table; use it for application and service commands rather than repeating strings in modules. The `Theme` global is populated by `config/theme.lua` before appearance modules load.

## User overrides and profiles

- Hyprland Lua customization: `user/hyprland.lua.example`; local `user/hyprland.lua` is Git-ignored.
- Waybar customization: `user/waybar.jsonc.example`; local `user/waybar.jsonc` is Git-ignored.
- `OBSYX_USER_DIR` can point to an alternate override directory.
- `obsyx profile apply laptop|workstation` writes active overrides below the selected XDG config root. Review existing files before applying; profile application can replace profile targets.

See [User overrides](../user/README.md) and [Profiles](profiles.md).

## Theme tokens and generated styles

Edit `core/tokens/<theme>.json` and run `python3 tools/build_tokens.py --theme <theme>` or use `obsyx theme apply <theme>` for a user configuration. Generated outputs include Hyprland Lua/conf, Waybar CSS, Rofi RASI, SwayNC CSS, Kitty conf, and Wlogout CSS. See [Theme tokens](theme-tokens.md).

## Companion components

- `waybar/config.jsonc`, `waybar/modules/`, `waybar/styles/`: bar module arrangement, scripts, and styling.
- `rofi/config.rasi`, `rofi/*.rasi`, `rofi/scripts/`: launcher, clipboard, power, and theme selection interfaces.
- `swaync/config.json`, `swaync/style.css`: notifications and control-center layout/style.
- `hypr/hyprlock.conf`, `hypr/hypridle.conf`, `hypr/hyprpaper.conf`: lock, idle, and wallpaper configuration.
- `kitty/kitty.conf`: terminal defaults and generated theme include.
- `wlogout/layout`, `wlogout/style.css`: session action entries and styling.

Use each application's own validator/runtime to confirm application-specific settings. `obsyx validate` checks syntax/integrity subsets; it is not a semantic validator for every application format.
