--------------------------------------------------------------------------------
-- Obsyx
-- Core Plugin & Lifecycle Architecture
--
-- Manages plugin registration, event hooks, and lifecycle state dispatch.
-- Provides isolated execution (pcall) so plugin faults never crash the desktop.
--------------------------------------------------------------------------------

local Plugins = {}

--------------------------------------------------------------------------------
-- Canonical Lifecycle Events
--------------------------------------------------------------------------------

Plugins.EVENTS = {
    INIT             = "on_init",
    THEME_CHANGE     = "on_theme_change",
    PROFILE_CHANGE   = "on_profile_change",
    WORKSPACE_CHANGE = "on_workspace_change",
}

--------------------------------------------------------------------------------
-- Internal Registry State
--------------------------------------------------------------------------------

Plugins._plugins = {}
Plugins._hooks = {}
Plugins._next_id = 1

--------------------------------------------------------------------------------
-- State Management
--------------------------------------------------------------------------------

--- Clear all registered plugins and lifecycle hooks.
function Plugins.clear()
    Plugins._plugins = {}
    Plugins._hooks = {}
    Plugins._next_id = 1
end

--------------------------------------------------------------------------------
-- Hook Management
--------------------------------------------------------------------------------

--- Register a listener callback for a lifecycle event.
-- @param event (string) Event name (e.g. "on_init", "on_theme_change")
-- @param fn (function) Callback function
-- @param opts (table|nil) Optional options: { once = bool, plugin = string, priority = number }
-- @return (function) Unsubscribe function that removes this hook
function Plugins.on(event, fn, opts)
    if type(event) ~= "string" or event == "" then
        error("Plugins.on: event must be a non-empty string", 2)
    end
    if type(fn) ~= "function" then
        error("Plugins.on: callback must be a function", 2)
    end

    opts = opts or {}
    local hook_id = Plugins._next_id
    Plugins._next_id = Plugins._next_id + 1

    local entry = {
        id = hook_id,
        fn = fn,
        once = opts.once or false,
        plugin = opts.plugin or nil,
        priority = opts.priority or 0,
    }

    if not Plugins._hooks[event] then
        Plugins._hooks[event] = {}
    end
    table.insert(Plugins._hooks[event], entry)

    -- Return unsubscription handle
    return function()
        Plugins.off(event, hook_id)
    end
end

--- Register a one-time listener callback for a lifecycle event.
-- @param event (string) Event name
-- @param fn (function) Callback function
-- @param opts (table|nil) Optional options
-- @return (function) Unsubscribe function
function Plugins.once(event, fn, opts)
    opts = opts or {}
    opts.once = true
    return Plugins.on(event, fn, opts)
end

--- Unregister a listener by callback function or hook ID.
-- @param event (string) Event name
-- @param fn_or_id (function|number) Callback function or ID
-- @return (boolean) True if a listener was removed
function Plugins.off(event, fn_or_id)
    if not Plugins._hooks[event] then
        return false
    end

    local list = Plugins._hooks[event]
    for i, entry in ipairs(list) do
        if entry.id == fn_or_id or entry.fn == fn_or_id then
            table.remove(list, i)
            return true
        end
    end
    return false
end

--- Check if an event has any registered hooks.
-- @param event (string) Event name
-- @return (boolean)
function Plugins.has_hook(event)
    return Plugins._hooks[event] ~= nil and #Plugins._hooks[event] > 0
end

--- Dispatch a lifecycle event with arbitrary arguments to all registered listeners.
-- Listeners are called safely using pcall so one failure does not abort the sequence.
-- @param event (string) Event name
-- @param ... Arguments forwarded to each callback
-- @return (table) Result table: { ok = bool, fired = number, errors = table }
function Plugins.emit(event, ...)
    local result = {
        ok = true,
        fired = 0,
        errors = {},
    }

    if not Plugins._hooks[event] or #Plugins._hooks[event] == 0 then
        return result
    end

    -- Snapshot listeners to allow mutations (e.g. unregistering inside callback)
    local listeners = {}
    for _, entry in ipairs(Plugins._hooks[event]) do
        table.insert(listeners, entry)
    end

    local indices_to_remove = {}

    for _, entry in ipairs(listeners) do
        result.fired = result.fired + 1

        local ok, err = pcall(entry.fn, ...)
        if not ok then
            result.ok = false
            local err_msg = tostring(err)
            table.insert(result.errors, {
                hook_id = entry.id,
                plugin = entry.plugin,
                error = err_msg,
            })
            if io and io.stderr then
                io.stderr:write(string.format(
                    "[Obsyx Plugins] Error in hook '%s'%s: %s\n",
                    event,
                    entry.plugin and (" from plugin '" .. entry.plugin .. "'") or "",
                    err_msg
                ))
            end
        end

        if entry.once then
            table.insert(indices_to_remove, entry.id)
        end
    end

    -- Clean up once listeners
    for _, hook_id in ipairs(indices_to_remove) do
        Plugins.off(event, hook_id)
    end

    return result
end

--------------------------------------------------------------------------------
-- Plugin Registration
--------------------------------------------------------------------------------

--- Register a plugin module.
-- Automatically wires declarative lifecycle hooks (on_init, on_theme_change, etc.)
-- and invokes plugin.init(Plugins) if provided.
-- @param name (string) Unique plugin name
-- @param def (table) Plugin definition table
-- @return (table) Registered plugin table
function Plugins.register(name, def)
    if type(name) ~= "string" or name == "" then
        error("Plugins.register: plugin name must be a non-empty string", 2)
    end
    if type(def) ~= "table" then
        error("Plugins.register: plugin definition must be a table", 2)
    end

    def.name = def.name or name

    -- Auto-bind declarative lifecycle hooks
    local hook_keys = {
        "on_init",
        "on_theme_change",
        "on_profile_change",
        "on_workspace_change",
    }

    for _, hook_name in ipairs(hook_keys) do
        if type(def[hook_name]) == "function" then
            Plugins.on(hook_name, def[hook_name], { plugin = name })
        end
    end

    Plugins._plugins[name] = def

    -- Invoke init hook if present
    if type(def.init) == "function" then
        local ok, err = pcall(def.init, Plugins)
        if not ok then
            if io and io.stderr then
                io.stderr:write(string.format(
                    "[Obsyx Plugins] Error initializing plugin '%s': %s\n",
                    name,
                    tostring(err)
                ))
            end
        end
    end

    return def
end

--- Unregister a plugin and remove all its registered hooks.
-- @param name (string) Plugin name
-- @return (boolean) True if plugin existed and was removed
function Plugins.unregister(name)
    if not Plugins._plugins[name] then
        return false
    end

    Plugins._plugins[name] = nil

    -- Clean up all hooks belonging to this plugin
    for event, list in pairs(Plugins._hooks) do
        local i = 1
        while i <= #list do
            if list[i].plugin == name then
                table.remove(list, i)
            else
                i = i + 1
            end
        end
    end

    return true
end

--- Retrieve a registered plugin by name.
-- @param name (string)
-- @return (table|nil)
function Plugins.get(name)
    return Plugins._plugins[name]
end

--- Retrieve the map of all registered plugins.
-- @return (table)
function Plugins.list()
    return Plugins._plugins
end

return Plugins
