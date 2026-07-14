--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Permissions
--
-- Explicitly grants privileged Hyprland ecosystem permissions to trusted
-- applications.
--
-- NOTE:
-- Changes require a full Hyprland restart.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Ecosystem Security
--------------------------------------------------------------------------------

hl.config({

    ecosystem = {

        -- Require explicit permission for privileged actions.
        enforce_permissions = true,

    },

})

--------------------------------------------------------------------------------
-- Permission Rules
--------------------------------------------------------------------------------

-- NOTE: binary is matched against Hyprland's own regex engine, not Lua
-- patterns -- hyphens are not special here and should NOT be escaped with
-- '%'. hl.permission expects exactly { binary, type, mode }.
local Permissions = {

    --------------------------------------------------------------------------
    -- Screen Capture
    --------------------------------------------------------------------------

    {
        binary = "/usr/(bin|local/bin)/hyprshot",
        type = "screencopy",
        mode = "allow",
    },

    {
        binary = "/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland",
        type = "screencopy",
        mode = "allow",
    },

    --------------------------------------------------------------------------
    -- Plugin Management
    --------------------------------------------------------------------------

    {
        binary = "/usr/(bin|local/bin)/hyprpm",
        type = "plugin",
        mode = "allow",
    },

}

for _, spec in ipairs(Permissions) do
    hl.permission(spec)
end