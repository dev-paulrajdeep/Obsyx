# Obsyx Canonical Wallpapers

This directory provides the canonical wallpaper assets for Obsyx desktop environments, designed specifically to harmonize with the Noctis Amethyst design token system.

## Assets

| File | Resolution | Format | Purpose |
|------|------------|--------|---------|
| `noctis_amethyst_default.svg` | 1920x1080 (Scalable) | Scalable Vector Graphics | Master vector artwork |
| `noctis_amethyst_default.png` | 1920x1080 | 8-bit RGBA Raster | Production wallpaper asset for `swww` / `hyprpaper` |

## Design Tokens & Palette

The artwork incorporates the exact color values defined in `core/tokens/noctis_amethyst.json`:

- **Deep Void / Background**: `#121018`
- **Surface / Elevation Tones**: `#16131d`, `#191623`, `#1f1a2b`
- **Amethyst Gradients**: `#8a63d2` to `#c7a6ff`
- **Vibrant Accent**: `#9b7ede`
- **Hairline / Highlights**: `#dacbff`

## Daemon Integration

- **`swww`**:
  ```bash
  swww img assets/wallpapers/noctis_amethyst_default.png \
      --transition-type fade \
      --transition-duration 1.5 \
      --transition-fps 60
  ```
- **`hyprpaper`**:
  Configured in `hypr/hyprpaper.conf`:
  ```ini
  preload = ~/.config/hypr/assets/wallpapers/noctis_amethyst_default.png
  wallpaper = ,~/.config/hypr/assets/wallpapers/noctis_amethyst_default.png
  ```
- **Wallpaper Manager Script**:
  Dispatched via `hypr/scripts/wallpaper.sh` during compositor startup.
