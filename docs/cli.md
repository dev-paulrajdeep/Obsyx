# Obsyx CLI

The CLI is `bin/obsyx`, a Python 3 program that uses the standard library. When installed from the Arch package, it is exposed as `obsyx`.

```bash
./bin/obsyx --help
./bin/obsyx --version
```

Commands that accept a destination use `$XDG_CONFIG_HOME`, falling back to `~/.config`, unless `--dest` is supplied. Use a disposable directory such as `/tmp/obsyx-preview` when inspecting write behavior.

## `doctor`

Checks for required, recommended, and optional executable dependencies. `--json` prints the report as JSON. Exit status is `1` if any required command is missing; recommended and optional misses are reported but do not fail the command. This checks command availability only.

```bash
./bin/obsyx doctor
./bin/obsyx doctor --json
```

## `validate`

Walks the target directory and performs static checks:

- Parses Lua files with `luac -p`, or falls back to `lua`'s `loadfile` if `luac` is unavailable.
- Parses `.json` and `.jsonc` after stripping comments.
- Requires `.sh` files to be executable and checks them with `bash -n`.
- Checks a small set of required keys in token JSON and the presence of expected generated token artifacts. This is not the full validation performed by the token compiler.

It does not run Hyprland, validate every component's native configuration semantics, or prove that a desktop session works. Without `--path`, the current working directory is checked. Exit status is `1` when a check fails.

```bash
./bin/obsyx validate
./bin/obsyx validate --path /path/to/config --json
```

## `install`

Creates symlinks for the supported component directories under the destination. Existing target entries are moved to a timestamped backup before linking. The installer does not install system packages. See [installer details](installer.md) for component names and consequences.

```bash
./bin/obsyx install --dry-run
./bin/obsyx install --components hypr,waybar
./bin/obsyx install --skip wlogout
./bin/obsyx install --interactive
./bin/obsyx install --dest /tmp/obsyx-preview --json
```

Options: `--dest`/`--target`, `--dry-run`, `--components`/`-c`, `--skip`/`-s`, `--interactive`/`-i`, and `--json`. The default component set is `hypr`, `waybar`, `rofi`, `swaync`, `kitty`, and `wlogout`.

## `update`

Updates the Obsyx source checkout using Git. It refuses to run if the working tree has tracked or untracked changes, if the branch has no upstream, or if the branch has diverged. Updates are fast-forward only. Package-managed copies without a Git checkout must be updated through the package manager.

```bash
./bin/obsyx update --check
./bin/obsyx update
./bin/obsyx update --json
```

`--check` fetches the upstream and compares commit counts without changing tracked files; it does update local Git remote-tracking metadata and needs network access. Running without `--check` fast-forwards the checkout when the local branch has no unique commits. Exit status is nonzero for dirty trees, unsupported installs, fetch/compare errors, or divergence.

## `backup`

Creates a compressed archive of selected Obsyx config directories and state (`obsyx/`, `.obsyx_theme`, `.obsyx_profile` when present). By default, the source is `$XDG_CONFIG_HOME` or `~/.config`, and the archive is saved under `$XDG_STATE_HOME/obsyx/backups` or `~/.local/state/obsyx/backups`.

```bash
./bin/obsyx backup
./bin/obsyx backup --source /tmp/obsyx-config --components hypr,waybar
./bin/obsyx backup --output /tmp/before-change.tar.gz --json
```

Options: `--source`, `--output`/`-o`, `--components`/`-c`, and `--json`. Existing output paths are never overwritten. Config symlinks at the selected top level are backed up by content; nested symlinks are omitted and listed in `manifest.json` so they are not followed outside the config tree.

## `restore`

Restores an archive created by `obsyx backup`. The archive is validated before writing; absolute paths, traversal paths, links, special files, unlisted entries, oversized archives, and unsupported formats are rejected. Existing target entries are first captured in a safety archive, then moved aside as `.pre-restore.<timestamp>` before the restored entries are installed.

```bash
./bin/obsyx restore ~/.local/state/obsyx/backups/obsyx-config-20261013_120000.tar.gz --dry-run
./bin/obsyx restore /path/to/backup.tar.gz
./bin/obsyx restore /path/to/backup.tar.gz --dest /tmp/obsyx-restore --json
```

The command requires a readable `obsyx-config-backup` archive and refuses malformed inputs. `--dry-run` validates and prints target paths without creating the destination or safety backup. Restore always creates a pre-restore archive when any target already exists.

## `theme`

Lists and displays the five official themes or compiles one into files under the destination. Applying a theme writes marker/state files and generated theme artifacts, then attempts reload signals for running components. Reload commands are best-effort; a successful CLI exit does not prove that each application accepted the result.

```bash
./bin/obsyx theme list
./bin/obsyx theme show obsidian --json
./bin/obsyx theme apply frost --dry-run
./bin/obsyx theme apply ember --dest /tmp/obsyx-preview
./bin/obsyx theme rofi
```

Actions: `list`, `show <name>`, `apply <name>`, and `rofi`. `apply` accepts `--dest`/`--target`, `--dry-run`, and `--json`; `list` and `show` accept `--dest` and `--json`. A theme apply targets generated paths for all components even if those component directories are not linked or installed.

## `profile`

Lists, displays, and applies the `laptop` and `workstation` profiles. Applying writes Hyprland profile overrides, Waybar configuration/style overrides, and `.obsyx_profile` state. It may send reload signals when run inside a Hyprland session. Profile application is not a package or hardware detection operation.

```bash
./bin/obsyx profile list
./bin/obsyx profile show laptop
./bin/obsyx profile apply laptop --dry-run
./bin/obsyx profile apply workstation --dest /tmp/obsyx-preview
```

Actions: `list`, `show <name>`, and `apply <name>`. `apply` accepts `--dest`/`--target`, `--dry-run`, and `--json`.

## `docgen`

Reads configured Hyprland keybindings and generates `KEYBINDINGS.md` and `rofi/scripts/keybindings.sh` by default. `--check` compares generated content without writing and returns nonzero if either output is stale. `--json` emits the parsed keybinding data.

```bash
./bin/obsyx docgen
./bin/obsyx docgen --check
./bin/obsyx docgen --json
```

Options: `--output`/`-o`, `--rofi-script`/`-r`, `--check`, and `--json`.

## Static checks and tests

```bash
./bin/obsyx validate
python3 -m unittest discover tests/ -v
```

The Python suite includes static checks and a headless Wayland test runner. Neither command establishes successful ISO boot or installation on a target machine.
