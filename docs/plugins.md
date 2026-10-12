# Plugin guide

Obsyx plugins are Lua tables registered with `require("core.plugins")`. They run inside the Hyprland Lua process with the same privileges as that process. The current framework has no permission sandbox; only load code you trust.

Place local plugin registration in `user/hyprland.lua` or another file loaded by that override. For example:

```lua
local Plugins = require("core.plugins")

Plugins.register("session_notes", {
    description = "Example lifecycle observer",

    init = function(plugin_api)
        print("session_notes initialized", plugin_api == Plugins)
    end,

    on_theme_change = function(theme, theme_name)
        print("Theme selected:", theme_name)
    end,

    on_profile_change = function(profile_name)
        print("Profile selected:", profile_name)
    end,

    on_workspace_change = function(workspace_id)
        print("Workspace selected:", workspace_id)
    end,
})
```

## Lifecycle events

| Event | Current dispatch point | Arguments |
|---|---|---|
| `on_init` | End of Hyprland configuration bootstrap | none |
| `on_theme_change` | Theme loader | theme table, theme name |
| `on_profile_change` | After profile override loading | profile name (`default` when unset) |
| `on_workspace_change` | Available event name; no dispatch is wired in the current tracked configuration | emitter-defined |

Declarative callbacks are registered automatically by `Plugins.register`. The event names are also exposed as `Plugins.EVENTS` constants.

## Listener API

- `Plugins.on(event, callback, options)` registers a callback and returns an unsubscribe function.
- `Plugins.once(event, callback, options)` registers a one-time callback.
- `Plugins.off(event, callback_or_id)` removes a matching listener.
- `Plugins.has_hook(event)` reports whether listeners are present.
- `Plugins.emit(event, ...)` calls a snapshot of listeners and returns `{ ok, fired, errors }`.
- `Plugins.unregister(name)` removes a plugin and its plugin-tagged hooks.
- `Plugins.get(name)` and `Plugins.list()` expose registered plugin definitions.
- `Plugins.clear()` resets plugin and listener state; primarily useful in tests/reloads.

Callbacks are invoked with `pcall`; a callback error is recorded and logged without stopping later listeners. `priority` can be passed in options but the current dispatcher does not sort callbacks by it, so ordering is registration order. The `once` option is removed after dispatch even if the callback errors.

See [Lua API](lua-api.md) for the surrounding configuration globals and external `hl` calls used by the configuration.
