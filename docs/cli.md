# Obsyx CLI (`bin/obsyx`)

The Obsyx command-line interface provides diagnostic health checking, configuration syntax validation, and desktop environment tooling.

## Location & Execution

The CLI executable is located at `bin/obsyx` and requires only Python 3 standard library:

```bash
./bin/obsyx --help
./bin/obsyx --version
```

---

## Commands

### 1. `obsyx doctor`

Checks system dependencies and desktop runtime tooling across three tiers:
- **Required Core Tooling**: `hyprland`, `waybar`, `bash`, `python3`, `lua`, `luac`.
- **Recommended Desktop Components**: `swaync`, `hyprlock`, `rofi`, `wlogout`, wallpaper daemon (`swww` or `hyprpaper`), `kitty`, `wl-copy`, `cliphist`, and Polkit authentication agent.
- **Optional Utilities & Applets**: `playerctl`, `brightnessctl`, `hyprshot`, `hyprpicker`, `nm-applet`, `blueman-applet`, ImageMagick (`magick`/`convert`).

#### Usage

```bash
# Standard formatted diagnostic check
./bin/obsyx doctor

# Machine-readable JSON output
./bin/obsyx doctor --json
```

#### Exit Codes
- `0`: All required dependencies are installed and available.
- `1`: One or more required dependencies are missing.

---

### 2. `obsyx validate`

Automates comprehensive syntax, structure, and integrity checks across the entire desktop configuration repository:
- **Lua Compositor Configurations**: Validates all `*.lua` files in `hypr/` via `luac -p` (or `lua` fallback).
- **JSONC / JSON Module Stylesheets**: Strips comments and validates strict JSON parsing via `json.loads` for Waybar, SwayNC, and tokens.
- **Shell Telemetry & Service Scripts**: Validates all `*.sh` files for execution flags (`chmod +x`) and bash syntax (`bash -n`).
- **Design Tokens & Compiled Artifacts**: Validates canonical design token schema (`core/tokens/noctis_amethyst.json`) and verifies presence of all compiled target artifacts (`hypr`, `waybar`, `rofi`, `swaync`, `hyprlock`, `kitty`, `wlogout`).

#### Usage

```bash
# Validate current repository
./bin/obsyx validate

# Validate custom or isolated configuration directory
./bin/obsyx validate --path /path/to/custom/config

# Machine-readable JSON validation report
./bin/obsyx validate --json
```

#### Exit Codes
- `0`: All configurations, scripts, and design tokens passed validation.
- `1`: One or more syntax errors, permission issues, or missing artifacts were detected.

---

### 3. `obsyx install`

Safely deploys Obsyx configuration components into target user dotfiles directory with automated timestamped backups and dry-run simulation:
- **`--dry-run`**: Simulate deployment without touching filesystem.
- **`--dest PATH`**: Destination target (defaults to `~/.config`).
- **`--components COMP1,COMP2`**: Selectively install components (`hypr`, `waybar`, `rofi`, `swaync`, `kitty`, `wlogout`).
- **`--skip COMP1`**: Exclude specific components.
- **`--json`**: Emit machine-readable installation report.

#### Usage

```bash
# Dry-run preview
./bin/obsyx install --dry-run

# Standard deployment
./bin/obsyx install

# Isolated sandbox deployment
./bin/obsyx install --dest /tmp/test-config
```

---

### 4. `obsyx docgen`

Automated keybinding parser and documentation generator:
- **`--output PATH`** (`-o`): Target markdown cheatsheet path (defaults to `KEYBINDINGS.md`).
- **`--rofi-script PATH`** (`-r`): Target interactive Rofi search script path (defaults to `rofi/scripts/keybindings.sh`).
- **`--check`**: Verify that generated cheatsheet and script files match active configuration without overwriting (exit code `0` if up to date, `1` if outdated).
- **`--json`**: Emit machine-readable JSON structure of all parsed categories and keybindings.

#### Usage

```bash
# Generate KEYBINDINGS.md and rofi/scripts/keybindings.sh
./bin/obsyx docgen

# Verify documentation matches configuration
./bin/obsyx docgen --check

# Output keybindings as JSON
./bin/obsyx docgen --json
```
