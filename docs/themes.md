# Obsyx Official Theme Collection & Design System

Obsyx provides five official themes built on top of the canonical design-token engine. Each theme defines a complete set of color, geometry, opacity, blur, and shadow tokens that compile consistently across all supported desktop components (Hyprland, Waybar, Rofi, SwayNC, Hyprlock, Kitty, and Wlogout).

---

## The Official Themes

### 1. Noctis Amethyst *(Reference Theme)*
- **Slug**: `noctis_amethyst`
- **Identity**: Regal, nocturnal, luxurious, and technically sophisticated.
- **Palette**:
  - `void`: `#121018`
  - `surface`: `#16131d` (alpha 0.88)
  - `accent`: `#9b7ede` (Amethyst)
  - `accent_ink`: `#dacbff` (Soft Lavender)
- **Materials**: 3-pass glass blur (size 13, vibrancy 0.32), 8px rounding, refined dark plum shadows.

### 2. Obsidian
- **Slug**: `obsidian`
- **Identity**: Monolithic stone, precision-machined dark metal, architectural minimalism. Zero saturated neon.
- **Palette**:
  - `void`: `#0b0b0e`
  - `surface`: `#111114` (alpha 0.90)
  - `accent`: `#a0a5ad` (Cool Silver / Platinum)
  - `accent_ink`: `#e2e4e8` (Polished Titanium)
- **Materials**: 2-pass matte blur (size 10, vibrancy 0.12), 6px rounding, crisp neutral hairlines.

### 3. Frost
- **Slug**: `frost`
- **Identity**: Crystalline winter, sub-zero glacial clarity, polar slate blue.
- **Palette**:
  - `void`: `#0b1017`
  - `surface`: `#0f1722` (alpha 0.86)
  - `accent`: `#4fc3f7` (Ice Blue)
  - `accent_ink`: `#b3e5fc` (Frosted Crystal)
- **Materials**: 3-pass clear glass blur (size 14, vibrancy 0.38, contrast 1.22), 8px rounding.

### 4. Aurora
- **Slug**: `aurora`
- **Identity**: Midnight Arctic sky, ethereal northern lights, deep oceanic teal and emerald luminescence.
- **Palette**:
  - `void`: `#071315`
  - `surface`: `#0b1a1c` (alpha 0.87)
  - `accent`: `#26a69a` (Luminous Emerald)
  - `accent_ink`: `#80cbc4` (Pale Mint)
- **Materials**: 3-pass vibrant glass blur (size 15, vibrancy 0.45), 9px rounding.

### 5. Ember
- **Slug**: `ember`
- **Identity**: Basalt volcanic rock, glowing embers, forge heat, deep charred soot with rich warm terracotta and magma copper.
- **Palette**:
  - `void`: `#120c0c`
  - `surface`: `#171010` (alpha 0.89)
  - `accent`: `#ff7043` (Warm Amber / Burnt Orange)
  - `accent_ink`: `#ffccbc` (Peach Highlight)
- **Materials**: 3-pass warm-toned blur (size 12, vibrancy 0.28), 8px rounding.

---

## Theme Inheritance Engine

Themes can extend or inherit from another theme by specifying `"extends"` or `"inherits"`:

```json
{
    "name": "Custom Variant",
    "inherits": "noctis_amethyst",
    "palette": {
        "accent": "#ff007f"
    }
}
```

The inheritance resolver (`tools/build_tokens.py`):
1. Loads the parent JSON recursively.
2. Performs a deep recursive merge where child tokens override parent tokens.
3. Validates against cyclic inheritance (e.g. A extends B extends A) and raises a descriptive `TokenError`.
4. Ensures missing parent files are reported clearly.

---

## Theme Switching

### CLI Switcher (`obsyx theme`)

```bash
# List available themes and see the active theme
obsyx theme list

# Inspect detailed tokens for a theme
obsyx theme show frost

# Simulate switching to Obsidian
obsyx theme apply obsidian --dry-run

# Switch to Aurora and reload compositor components
obsyx theme apply aurora
```

### Interactive Rofi Switcher

Launch the interactive Rofi menu:

```bash
obsyx theme rofi
# or
~/.config/rofi/scripts/theme-switcher.sh
```

### Generated Artifacts on Switch

When `obsyx theme apply <name>` runs, it compiles and installs:
- `hypr/themes/<name>.lua` (Lua theme table)
- `waybar/generated/theme-tokens.css` (GTK3 CSS definitions)
- `rofi/generated/theme-tokens.rasi` (Rofi stylesheet)
- `swaync/generated/theme-tokens.css` (Notification center styles)
- `hypr/generated/theme-tokens.conf` (Hyprland / Hyprlock variables)
- `kitty/generated/theme-tokens.conf` (Terminal palette)
- `wlogout/generated/theme-tokens.css` (Logout menu styles)

And signals live components:
- `hyprctl reload`
- `pkill -SIGUSR2 waybar`
- `swaync-client -R`
