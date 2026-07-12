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

local Permissions = {

    --------------------------------------------------------------------------
    -- Screen Capture
    --------------------------------------------------------------------------

    {
        executable = "/usr/(bin|local/bin)/hyprshot",
        permission = "screencopy",
        policy = "allow",
    },

    {
        executable = "/usr/(lib|libexec|lib64)/xdg%-desktop%-portal%-hyprland",
        permission = "screencopy",
        policy = "allow",
    },

    --------------------------------------------------------------------------
    -- Plugin Management
    --------------------------------------------------------------------------

    {
        executable = "/usr/(bin|local/bin)/hyprpm",
        permission = "plugin",
        policy = "allow",
    },

}

for _, spec in ipairs(Permissions) do
    hl.permission(spec)
end