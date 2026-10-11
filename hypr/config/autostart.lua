--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Autostart
--
-- Launches desktop services in a deterministic order.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Startup Queue
--------------------------------------------------------------------------------

local Startup = {

    ------------------------------------------------------------------------
    -- Authentication Agent
    ------------------------------------------------------------------------

    Registry.Startup.authAgent,

    ------------------------------------------------------------------------
    -- Core Services
    ------------------------------------------------------------------------

    Registry.Startup.notificationDaemon,

    Registry.Startup.wallpaperDaemon,

    Registry.Startup.clipboardText,

    Registry.Startup.clipboardImage,

    ------------------------------------------------------------------------
    -- System Applets
    ------------------------------------------------------------------------

    Registry.Startup.networkApplet,

    Registry.Startup.bluetoothApplet,

    ------------------------------------------------------------------------
    -- Desktop
    ------------------------------------------------------------------------

    Registry.Startup.statusBar,

}

--------------------------------------------------------------------------------
-- Startup
--------------------------------------------------------------------------------

hl.on("hyprland.start", function()

    ------------------------------------------------------------------------
    -- Launch Services
    ------------------------------------------------------------------------

    for _, command in ipairs(Startup) do
        if command and command ~= "" then
            hl.exec_cmd(command)
        end
    end

    ------------------------------------------------------------------------
    -- Delay Wallpaper
    ------------------------------------------------------------------------

    if Registry.Startup.wallpaper and Registry.Startup.wallpaper ~= "" then
        hl.timer(function()

            hl.exec_cmd(Registry.Startup.wallpaper)

        end, {

            timeout = 500,

            type = "oneshot",

        })
    end

end)

return Startup