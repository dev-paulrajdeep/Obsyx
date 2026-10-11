# Theme Tokens

Obsyx uses a **canonical JSON token source** as the single source of truth for its visual identity. A deterministic compiler generates target-specific configuration from this source.

## Files

| File | Role |
|------|------|
| `core/tokens/noctis_amethyst.json` | Canonical token source — edit this |
| `tools/build_tokens.py` | Deterministic compiler |
| `hypr/themes/noctis_amethyst.lua` | Generated Hyprland Lua theme table |
| `hypr/config/theme.lua` | Hyprland dynamic theme loader |
| `hypr/config/appearance/decoration.lua` | Compositor styling bound to active theme tokens |
| `waybar/generated/theme-tokens.css` | Generated Waybar GTK3 CSS tokens |
| `waybar/style.css` | Waybar stylesheet entry point importing generated tokens |
| `waybar/scripts/runner.sh` | Portable telemetry script runner supporting dynamic and relative discovery |
| `rofi/generated/theme-tokens.rasi` | Generated Rofi RASI tokens |
| `rofi/config.rasi` | Central Rofi configuration importing active theme |
| `rofi/theme.rasi` | Token-driven Noctis Amethyst glass theme for Rofi |
| `rofi/powermenu.rasi` | Token-driven power controls dialog theme |
| `rofi/clipboard.rasi` | Token-driven clipboard manager dialog theme |
| `rofi/scripts/powermenu.sh` | Session management script (lock, suspend, logout, reboot, poweroff) |
| `rofi/scripts/cliphist.sh` | Clipboard history script using `cliphist` and `wl-copy` |
| `swaync/generated/theme-tokens.css` | Generated SwayNC GTK3 CSS tokens |
| `swaync/config.json` | SwayNC notification daemon and control center layout configuration |
| `swaync/style.css` | Token-driven SwayNC stylesheet with urgency states and widget styling |
| `hypr/generated/theme-tokens.conf` | Generated Hyprland / Hyprlock configuration variables |
| `hypr/hyprlock.conf` | Token-driven screen lock configuration with blurred screenshot and input field |
| `kitty/generated/theme-tokens.conf` | Generated Kitty terminal color tokens |
| `kitty/kitty.conf` | Kitty terminal configuration importing generated tokens |
| `wlogout/generated/theme-tokens.css` | Generated Wlogout GTK3 CSS tokens |
| `wlogout/layout` | Wlogout action layout configuration |
| `wlogout/style.css` | Token-driven Wlogout stylesheet importing generated tokens |
| `tests/test_build_tokens.py` | Token compiler automated test suite |
| `tests/test_theme_loader.py` | Theme loader and decoration wiring test suite |
| `tests/test_waybar_tokens.py` | Waybar token integration and consistency test suite |
| `tests/test_rofi_theme.py` | Rofi configuration, theme, and scripts test suite |
| `tests/test_swaync_theme.py` | SwayNC configuration and stylesheet token test suite |
| `tests/test_hyprlock_theme.py` | Hyprlock configuration and token test suite |
| `tests/test_kitty_theme.py` | Kitty terminal configuration and token test suite |
| `tests/test_wlogout_theme.py` | Wlogout layout and token stylesheet test suite |

## Hyprland Theme Loader & Decoration

Hyprland loads themes dynamically through `hypr/config/theme.lua`:

1. `hypr/config/variables.lua` declares the active theme name (e.g. `Registry.Theme.name = "Noctis Amethyst"`).
2. `hypr/config/theme.lua` slugifies the theme name, loads `hypr/themes/<slug>.lua`, validates required sections (`palette`, `geometry`, `blur`), and exposes the theme globally as `Theme` and in `Registry.Theme.current`.
3. `hypr/config/appearance/decoration.lua` dynamically consumes the active theme's geometry (gaps, border size, rounding), palette (active gradient borders, inactive borders), opacity, shadows, and blur passes.

## Waybar Token Integration

Waybar styles are driven by the generated tokens without duplicate definitions:

1. `waybar/style.css` imports `generated/theme-tokens.css` directly as the foundation of its stylesheet import chain.
2. `waybar/theme.css` re-exports `generated/theme-tokens.css` for backwards compatibility while retaining the spatial token reference.
3. Component modules (`waybar/modules/*.jsonc`) use pure semantic markup with zero hardcoded hex colors, delegating state colors (`.notification`, `.dnd-notification`) to `waybar/styles/modules.css`.
4. Telemetry modules (`cpu`, `gpu`, `media`, `memory`, `network`, `vpn`) resolve backend scripts portably via dynamic lookup across `$WAYBAR_SCRIPTS_DIR`, `./scripts`, `./waybar/scripts`, and `${XDG_CONFIG_HOME:-$HOME/.config}/waybar/scripts`, eliminating hardcoded user paths. Standalone script execution is provided via `waybar/scripts/runner.sh`.

## Rofi Component Library Integration

Rofi application launcher, power menu, and clipboard history are styled via generated tokens:

1. `rofi/generated/theme-tokens.rasi` provides the single source of truth for Rofi colors and geometry (`@rounding`, `@border-width`).
2. `rofi/theme.rasi` imports `generated/theme-tokens.rasi` and applies Noctis Amethyst glass styling (`@noctis-surface-raised`, `@hairline-strong`, `@amethyst-fill`, `@amethyst-ink`).
3. `rofi/scripts/powermenu.sh` and `rofi/scripts/cliphist.sh` invoke Rofi with dedicated modal themes (`rofi/powermenu.rasi` and `rofi/clipboard.rasi`) and are wired into `Registry.Desktop` and `Registry.Session`.

## SwayNC Notification Daemon & Control Center

SwayNC notification popups and control center are styled using compiled GTK3 tokens:

1. `swaync/generated/theme-tokens.css` defines the canonical colors as `@define-color` rules.
2. `swaync/style.css` imports `generated/theme-tokens.css` and styles `.control-center`, `.notification`, widgets, and urgency states (`.low`, `.normal`, `.critical`) with zero hardcoded hex values.
3. `swaync/config.json` configures overlay dimensions, layout, margins, and widget list.

## Hyprlock Screen Locker Integration

Hyprlock screen locking is driven by compiled configuration variables:

1. `hypr/generated/theme-tokens.conf` provides `$token = rgb(...)` / `rgba(...)` variables for palette, geometry, and blur parameters.
2. `hypr/hyprlock.conf` sources `generated/theme-tokens.conf` to configure background live screenshot blurring (`$blur_passes`, `$blur_size`), time/date labels (`$amethyst_ink`, `$ink_default`), and the authentication input field (`$amethyst`, `$warning`, `$danger`).

## Kitty Terminal Theming

Kitty terminal colors and configuration are unified through token generation:

1. `kitty/generated/theme-tokens.conf` defines terminal foreground, background (`void`), selection, cursor, window borders, tab bar, and the 16 standard/bright ANSI colors directly from the Noctis Amethyst palette.
2. `kitty/kitty.conf` imports `generated/theme-tokens.conf`, configuring typography (`JetBrainsMono Nerd Font`), padding, opacity, and window rules without hardcoded color values.

## Wlogout Logout Menu Integration

Wlogout session management overlay is styled using compiled GTK3 tokens:

1. `wlogout/generated/theme-tokens.css` defines the canonical colors as `@define-color` rules.
2. `wlogout/layout` specifies session actions (`lock`, `hibernate`, `logout`, `shutdown`, `suspend`, `reboot`) with associated Hyprland and systemd commands.
3. `wlogout/style.css` imports `generated/theme-tokens.css` and provides Noctis Amethyst glass styling (`@noctis-surface-raised`, `@hairline-strong`, `@amethyst-fill`, `@amethyst-line`) with zero hardcoded hex values.

## Running the compiler

From the repository root:

```bash
python3 tools/build_tokens.py
```

This reads `core/tokens/noctis_amethyst.json` and generates all output files. The command accepts optional arguments:

```bash
python3 tools/build_tokens.py \
    --tokens core/tokens/noctis_amethyst.json \
    --lua-out hypr/themes/noctis_amethyst.lua \
    --css-out waybar/generated/theme-tokens.css \
    --rofi-out rofi/generated/theme-tokens.rasi \
    --swaync-out swaync/generated/theme-tokens.css \
    --hypr-conf-out hypr/generated/theme-tokens.conf \
    --kitty-out kitty/generated/theme-tokens.conf \
    --wlogout-out wlogout/generated/theme-tokens.css
```

## Running the tests

```bash
python3 -m unittest discover tests/ -v
```

## Token format

Colors are represented in one of two ways:

- **Opaque:** a plain hex string — `"#9b7ede"`
- **With alpha:** an object — `{ "hex": "#9b7ede", "alpha": 0.16 }`

The compiler translates these to:

| Target | Opaque | With alpha |
|--------|--------|------------|
| Hyprland Lua | `"#9b7ede"` | `"rgba(9B7EDE29)"` |
| Waybar CSS | `#9b7ede` | `rgba(155, 126, 222, 0.16)` |
| Rofi RASI | `#9b7ede` | `rgba(155, 126, 222, 0.16)` |
| SwayNC CSS | `#9b7ede` | `rgba(155, 126, 222, 0.16)` |
| Hypr Conf | `rgb(9b7ede)` | `rgba(9b7ede29)` |
| Kitty Conf | `#9b7ede` | `#9b7ede` |
| Wlogout CSS | `#9b7ede` | `rgba(155, 126, 222, 0.16)` |

## Adding a new token

1. Add the entry to `core/tokens/noctis_amethyst.json` under the appropriate section.
2. If the token should appear in the Waybar CSS output, add a mapping entry to the `CSS_TOKEN_MAP` list in `tools/build_tokens.py`.
3. If the token should appear in the Lua output, add it to the `LUA_PALETTE_ORDER` list in `tools/build_tokens.py`.
4. Run the compiler: `python3 tools/build_tokens.py`
5. Run the tests: `python3 -m unittest discover tests/ -v`

## Important

The generated files (`hypr/themes/noctis_amethyst.lua`, `waybar/generated/theme-tokens.css`, `rofi/generated/theme-tokens.rasi`, `swaync/generated/theme-tokens.css`, `hypr/generated/theme-tokens.conf`, `kitty/generated/theme-tokens.conf`, and `wlogout/generated/theme-tokens.css`) are **committed to the repository** — they are part of the distributable configuration. However, they should never be edited by hand. Always modify the token source and re-run the compiler.
