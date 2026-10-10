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
| `rofi/generated/theme-tokens.rasi` | Generated Rofi RASI tokens |
| `rofi/config.rasi` | Central Rofi configuration importing active theme |
| `rofi/theme.rasi` | Token-driven Noctis Amethyst glass theme for Rofi |
| `rofi/powermenu.rasi` | Token-driven power controls dialog theme |
| `rofi/clipboard.rasi` | Token-driven clipboard manager dialog theme |
| `rofi/scripts/powermenu.sh` | Session management script (lock, suspend, logout, reboot, poweroff) |
| `rofi/scripts/cliphist.sh` | Clipboard history script using `cliphist` and `wl-copy` |
| `tests/test_build_tokens.py` | Token compiler automated test suite |
| `tests/test_theme_loader.py` | Theme loader and decoration wiring test suite |
| `tests/test_waybar_tokens.py` | Waybar token integration and consistency test suite |
| `tests/test_rofi_theme.py` | Rofi configuration, theme, and scripts test suite |

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

## Rofi Component Library Integration

Rofi application launcher, power menu, and clipboard history are styled via generated tokens:

1. `rofi/generated/theme-tokens.rasi` provides the single source of truth for Rofi colors and geometry (`@rounding`, `@border-width`).
2. `rofi/theme.rasi` imports `generated/theme-tokens.rasi` and applies Noctis Amethyst glass styling (`@noctis-surface-raised`, `@hairline-strong`, `@amethyst-fill`, `@amethyst-ink`).
3. `rofi/scripts/powermenu.sh` and `rofi/scripts/cliphist.sh` invoke Rofi with dedicated modal themes (`rofi/powermenu.rasi` and `rofi/clipboard.rasi`) and are wired into `Registry.Desktop` and `Registry.Session`.

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
    --rofi-out rofi/generated/theme-tokens.rasi
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

## Adding a new token

1. Add the entry to `core/tokens/noctis_amethyst.json` under the appropriate section.
2. If the token should appear in the Waybar CSS output, add a mapping entry to the `CSS_TOKEN_MAP` list in `tools/build_tokens.py`.
3. If the token should appear in the Lua output, add it to the `LUA_PALETTE_ORDER` list in `tools/build_tokens.py`.
4. Run the compiler: `python3 tools/build_tokens.py`
5. Run the tests: `python3 -m unittest discover tests/ -v`

## Important

The generated files (`hypr/themes/noctis_amethyst.lua` and `waybar/generated/theme-tokens.css`) are **committed to the repository** — they are part of the distributable configuration. However, they should never be edited by hand. Always modify the token source and re-run the compiler.
