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
