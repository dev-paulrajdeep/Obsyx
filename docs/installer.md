# Obsyx Automated Safe Installer

Obsyx includes an automated, non-destructive installation framework designed to safely deploy configuration files into user dotfile environments without risk of configuration loss.

## Installation Architecture

The installer is invoked either via the central CLI or the dedicated shell wrapper:

```bash
# Using the Obsyx CLI
./bin/obsyx install [OPTIONS]

# Using the companion wrapper script
./tools/install.sh [OPTIONS]
```

## Safety Features

### 1. Dry-Run Simulation Mode (`--dry-run`)
Allows inspecting all proposed filesystem changes before applying them. Zero modifications are made when `--dry-run` is active.

```bash
./bin/obsyx install --dry-run
```

### 2. Automatic Timestamped Backups
If a destination directory or file already exists (for example `~/.config/hypr` or `~/.config/waybar`), the installer never overwrites it. Instead, it moves the existing directory to a timestamped backup:

```
~/.config/hypr.backup.20261011_200300
~/.config/waybar.backup.20261011_200300
```

If the destination is already a symlink pointing to the current Obsyx repository, the installer recognizes it as already linked and safely skips it without redundant backups.

### 3. Destination Overrides (`--dest` / `--target`)
By default, the installer targets `${XDG_CONFIG_HOME:-$HOME/.config}`. You can override the target destination to preview or test Obsyx in an isolated sandbox:

```bash
./bin/obsyx install --dest /tmp/test-config
```

### 4. Selective Component Deployment (`--components` / `--skip`)
Install only specific components or exclude unwanted ones:

```bash
# Install only Waybar and Kitty
./bin/obsyx install --components waybar,kitty

# Install all components except Wlogout
./bin/obsyx install --skip wlogout
```

---

## Supported Components

| Component | Target Directory | Description |
|-----------|------------------|-------------|
| `hypr` | `<dest>/hypr` | Hyprland compositor, themes, autostart, hyprlock, and wallpapers |
| `waybar` | `<dest>/waybar` | Waybar status bar, layouts, GTK3 CSS, and telemetry scripts |
| `rofi` | `<dest>/rofi` | Rofi app launcher, power menu, clipboard manager, and glass theme |
| `swaync` | `<dest>/swaync` | SwayNC notification daemon and control center stylesheet |
| `kitty` | `<dest>/kitty` | Kitty terminal emulator configuration and theme tokens |
| `wlogout` | `<dest>/wlogout` | Wlogout logout dialog layout and CSS styling |

---

## Command Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--dry-run` | | `false` | Simulate installation without modifying the filesystem |
| `--dest` | `--target` | `~/.config` | Target configuration directory |
| `--components` | `-c` | all | Comma-separated list of components to install |
| `--skip` | `-s` | none | Comma-separated list of components to skip |
| `--json` | | `false` | Emit structured JSON output |
