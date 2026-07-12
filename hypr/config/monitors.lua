--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Monitor Configuration
--
-- Defines display topology for the entire desktop.
-- Hyprland will automatically use the preferred mode unless overridden.
--------------------------------------------------------------------------------

local Displays = {

    --------------------------------------------------------------------------------
    -- Internal / Primary Display
    --------------------------------------------------------------------------------

    primary = {

        output   = "",
        mode     = "preferred",
        position = "auto",
        scale    = 1,

    },

    --------------------------------------------------------------------------------
    -- Future External Display
    --
    -- Uncomment and modify when needed.
    --------------------------------------------------------------------------------

    -- external = {
    --
    --     output   = "DP-1",
    --     mode     = "2560x1440@165",
    --     position = "1920x0",
    --     scale    = 1,
    --
    -- },

}

--------------------------------------------------------------------------------
-- Register Displays
--------------------------------------------------------------------------------

for _, monitor in pairs(Displays) do
    hl.monitor(monitor)
end