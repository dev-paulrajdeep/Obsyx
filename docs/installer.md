# Desktop configuration installer

`obsyx install` deploys Obsyx configuration directories into a user's XDG config directory. It does not install Linux packages, create a bootable system, or configure system services.

## Preview first

```bash
./bin/obsyx install --dry-run
./bin/obsyx install --dest /tmp/obsyx-preview --components hypr,waybar --dry-run
```

The normal destination is `$XDG_CONFIG_HOME`, or `~/.config` if that variable is unset. `--dest` and `--target` override it.

## What the installer changes

The installer creates symlinks from the destination to the matching directories in the Obsyx repository. The repository must remain at its current path for those links to keep working. The six supported components are:

| Component | Target | Contents |
|---|---|---|
| `hypr` | `<dest>/hypr` | Hyprland configuration, themes, lock/idle/wallpaper settings, scripts |
| `waybar` | `<dest>/waybar` | Bar configuration, styles, modules, telemetry scripts |
| `rofi` | `<dest>/rofi` | Launcher, menus, styles, scripts |
| `swaync` | `<dest>/swaync` | Notification daemon configuration and styles |
| `kitty` | `<dest>/kitty` | Terminal configuration and generated colors |
| `wlogout` | `<dest>/wlogout` | Logout layout and styles |

By default all six are selected. `--components` selects a comma-separated subset; `--skip` removes components from the default or selected set. Unknown names are currently ignored by the CLI, so check the printed plan before applying.

When a target already exists, the installer renames it to `<target>.backup.YYYYMMDD_HHMMSS` and then creates the symlink. An existing symlink to the same repository directory is left in place. These backups are not automatic merges: changes in the moved directory are not copied into Obsyx. Preserve and review the backup before removing it.

## Interactive mode

```bash
./bin/obsyx install --interactive
# The wrapper also starts interactive mode when run in a terminal with no arguments.
./tools/install.sh
```

The wizard checks a small set of commands, asks for the destination, offers Full/Minimal/Custom component presets, selects a theme and optional profile, then asks whether to install, simulate, or cancel. The Minimal preset installs `hypr` and `waybar`. Its dependency check reports availability; it does not fetch or install dependencies.

## Options

| Option | Behavior |
|---|---|
| `--dest PATH`, `--target PATH` | Destination config directory |
| `--dry-run` | Print planned links without filesystem changes |
| `--components LIST`, `-c LIST` | Select component names, comma-separated |
| `--skip LIST`, `-s LIST` | Exclude component names, comma-separated |
| `--interactive`, `-i` | Start the guided wizard |
| `--json` | Emit a JSON plan/result |

For an isolated installation, use a new temporary directory and inspect its links. Do not point the command at system directories. The CLI makes no promise that other tools or running sessions will accept the selected configuration.

## Theme and profile selection

The interactive flow applies the selected theme and optional profile after linking. The theme compiler writes generated theme files and state under the destination. Profile application writes override files and profile state. These operations have their own path and overwrite behavior; see [CLI reference](cli.md), [themes](themes.md), and [profiles](profiles.md) before selecting them for an existing configuration.
