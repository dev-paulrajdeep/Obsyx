--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Hyprland Configuration
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Core Architecture & Plugins
--------------------------------------------------------------------------------

local ok_plugins, Plugins = pcall(require, "core.plugins")
if ok_plugins and Plugins then
    _G.Plugins = Plugins
end

--------------------------------------------------------------------------------
-- Registry
--------------------------------------------------------------------------------

require("config.variables")

--------------------------------------------------------------------------------
-- Theme
--------------------------------------------------------------------------------

require("config.theme")

--------------------------------------------------------------------------------
-- Environment
--------------------------------------------------------------------------------

require("config.env")

--------------------------------------------------------------------------------
-- Hardware
--------------------------------------------------------------------------------

require("config.monitors")
require("config.input")

--------------------------------------------------------------------------------
-- Core Configuration
--------------------------------------------------------------------------------

require("config.general")
require("config.misc")

--------------------------------------------------------------------------------
-- Appearance
--------------------------------------------------------------------------------

require("config.appearance.decoration")
require("config.appearance.animations")

--------------------------------------------------------------------------------
-- Layouts
--------------------------------------------------------------------------------

require("config.layouts.dwindle")
require("config.layouts.master")

--------------------------------------------------------------------------------
-- Workspace & Window Policy
--------------------------------------------------------------------------------

require("config.rules.workspaces")
require("config.rules.windows")
require("config.rules.layers")

--------------------------------------------------------------------------------
-- Keybindings
--------------------------------------------------------------------------------

require("config.binds.apps")
require("config.binds.windows")
require("config.binds.workspaces")
require("config.binds.system")
require("config.binds.media")
require("config.binds.screenshots")

--------------------------------------------------------------------------------
-- Profile Specialization (Optional form-factor overrides)
--------------------------------------------------------------------------------

local ok_profile = pcall(require, "config.profile")
if not ok_profile then
    local xdg = os.getenv("XDG_CONFIG_HOME")
    if not xdg or xdg == "" then
        xdg = (os.getenv("HOME") or "") .. "/.config"
    end
    local prof_file = xdg .. "/obsyx/profile.lua"
    local f = io.open(prof_file, "r")
    if f then
        f:close()
        pcall(dofile, prof_file)
    end
end

if _G.Plugins and type(_G.Plugins.emit) == "function" then
    local current_prof = (Registry and Registry.Profile and Registry.Profile.name) or "default"
    _G.Plugins.emit("on_profile_change", current_prof)
end

--------------------------------------------------------------------------------
-- User Overrides (Git-Clean Local Customization)
--------------------------------------------------------------------------------

local function load_user_overrides()
    local custom_user_dir = os.getenv("OBSYX_USER_DIR")
    local xdg = os.getenv("XDG_CONFIG_HOME")
    if not xdg or xdg == "" then
        xdg = (os.getenv("HOME") or "") .. "/.config"
    end

    local candidates = {}
    if custom_user_dir and custom_user_dir ~= "" then
        table.insert(candidates, custom_user_dir .. "/hyprland.lua")
        table.insert(candidates, custom_user_dir .. "/user/hyprland.lua")
    end
    table.insert(candidates, xdg .. "/obsyx/user/hyprland.lua")
    table.insert(candidates, xdg .. "/hypr/user/hyprland.lua")
    table.insert(candidates, "user/hyprland.lua")
    table.insert(candidates, "../user/hyprland.lua")

    local ok_req = pcall(require, "user.hyprland")
    if not ok_req then
        for _, path in ipairs(candidates) do
            local f = io.open(path, "r")
            if f then
                f:close()
                local ok_run, err = pcall(dofile, path)
                if not ok_run and io and io.stderr then
                    io.stderr:write(string.format("[Obsyx User Override] Error loading '%s': %s\n", path, tostring(err)))
                end
                break
            end
        end
    end

    local waybar_candidates = {}
    if custom_user_dir and custom_user_dir ~= "" then
        table.insert(waybar_candidates, custom_user_dir .. "/waybar.jsonc")
    end
    table.insert(waybar_candidates, xdg .. "/obsyx/user/waybar.jsonc")
    table.insert(waybar_candidates, xdg .. "/waybar/user/waybar.jsonc")
    table.insert(waybar_candidates, "user/waybar.jsonc")
    table.insert(waybar_candidates, "../user/waybar.jsonc")

    for _, wb_path in ipairs(waybar_candidates) do
        local f = io.open(wb_path, "r")
        if f then
            f:close()
            if Registry and Registry.Startup and Registry.Startup.statusBar == "waybar" then
                Registry.Startup.statusBar = "waybar -c " .. wb_path
            end
            if Registry and Registry.Desktop and Registry.Desktop.statusBar == "waybar" then
                Registry.Desktop.statusBar = "waybar -c " .. wb_path
            end
            break
        end
    end
end

load_user_overrides()

--------------------------------------------------------------------------------
-- Runtime
--------------------------------------------------------------------------------

require("config.autostart")

--------------------------------------------------------------------------------
-- Lifecycle Initialization
--------------------------------------------------------------------------------

if _G.Plugins and type(_G.Plugins.emit) == "function" then
    _G.Plugins.emit("on_init")
end
