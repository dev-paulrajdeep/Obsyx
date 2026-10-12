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

## Interactive Installation Wizard (`--interactive` / `-i`)

Obsyx provides a guided interactive wizard for both first-time installations and configuration re-tuning. When executed in an interactive terminal without arguments, `./tools/install.sh` automatically launches this wizard:

```bash
# Launch interactive installer wizard via CLI
./bin/obsyx install --interactive

# Or using the companion shell wrapper
./tools/install.sh
```

### Guided Setup Workflow

The interactive wizard guides you through 6 setup stages:

1. **Pre-flight Dependency Detection**: Inspects the host environment for core Wayland desktop binaries (`hyprland`, `waybar`, `rofi`, `swaync`, `kitty`, `wlogout`), reporting status (`FOUND` or `MISSING`).
2. **Installation Destination Confirmation**: Confirms target dotfiles directory (defaults to `${XDG_CONFIG_HOME:-~/.config}`) and detects existing configuration directories scheduled for automatic backup.
3. **Installation Preset Selection**:
   - **Full Desktop Experience (Recommended)**: Installs all 6 core components (`hypr`, `waybar`, `rofi`, `swaync`, `kitty`, `wlogout`).
   - **Core Minimal**: Installs only the core Hyprland compositor (`hypr`) and Waybar status bar (`waybar`).
   - **Custom Selection**: Prompts for individual inclusion of each desktop component.
4. **Official Theme Selection**: Selects the active desktop theme (`Noctis Amethyst`, `Obsidian`, `Frost`, `Aurora`, `Ember`).
5. **Hardware Form-Factor Profile**: Configures hardware optimizations (`Default`, `Workstation`, `Laptop`).
6. **Confirmation & Action Review**: Presents a comprehensive summary before taking action:
   - **Proceed**: Applies live installation, automated backups, and generates theme artifacts.
   - **Simulate (Dry Run)**: Simulates the entire deployment without touching the filesystem.
   - **Cancel**: Aborts without making any changes.

---

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
| `--interactive` | `-i` | `false` | Launch interactive guided installation wizard |
| `--dry-run` | | `false` | Simulate installation without modifying the filesystem |
| `--dest` | `--target` | `~/.config` | Target configuration directory |
| `--components` | `-c` | all | Comma-separated list of components to install |
| `--skip` | `-s` | none | Comma-separated list of components to skip |
| `--json` | | `false` | Emit structured JSON output |
