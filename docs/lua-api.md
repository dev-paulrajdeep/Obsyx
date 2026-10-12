# Lua API reference

Obsyx configuration runs in the Lua environment provided by the Hyprland integration used by this project. `hl` is supplied by that host runtime; it is not implemented by Obsyx. This page documents the Obsyx globals and the `hl` methods actually used in tracked configuration, not the full external runtime API.

## Obsyx globals

### `Registry`

Created by `hypr/config/variables.lua` and loaded before the other configuration modules. It groups commands and data under:

- `Apps`: `terminal`, `browser`, `editor`, `musicPlayer`, `fileManager`, `terminalFM`.
- `Desktop`: launcher, clipboard, power menu, lock, logout, notifications, wallpaper, and status bar commands.
- `Tools`, `Services`, `Startup`, `Paths`, `Theme`, `Media`, `Screenshot`, and `Session`.

These are project defaults, not capability checks. Changing a command does not install or validate the referenced program.

### `Theme`

Loaded by `hypr/config/theme.lua`. Required tables are `palette`, `geometry`, and `blur`; optional `opacity` and `shadow` receive defaults. The loader also sets `Registry.Theme.current` and `Registry.Theme.slug`.

### `Plugins`

The plugin module is available with `require("core.plugins")`; the entry point exposes it as `_G.Plugins`. See [Plugin guide](plugins.md) for lifecycle and listener methods.

## Host-provided `hl` methods used by Obsyx

The current source calls these host methods:

```lua
hl.config({ general = { gaps_in = 5 } })
hl.bind("SUPER + Return", hl.dsp.exec_cmd(Registry.Apps.terminal), {
    description = "Terminal Emulator",
})
hl.permission({ binary = "/usr/bin/hyprshot", type = "screencopy", mode = "allow" })
hl.on("hyprland.start", function()
    hl.exec_cmd("waybar")
end)
hl.timer(function()
    hl.exec_cmd(Registry.Startup.wallpaper)
end, { timeout = 500, type = "oneshot" })
```

The supported key syntax, config keys, permission types, event names, and timer options are defined by the external Hyprland Lua runtime and the installed Hyprland version. Treat the examples as usage found in this repository, not an exhaustive or version-independent API contract.

## Extending configuration

Use the project override locations and lifecycle API rather than editing generated token files. The [Configuration reference](configuration-reference.md) maps module paths, and [User overrides](../user/README.md) describes discovery behavior.
