--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Permissions
--
-- Explicitly grants Hyprland ecosystem permissions to trusted applications.
--
-- NOTE:
-- Permission changes require a full Hyprland restart.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Ecosystem Security
--------------------------------------------------------------------------------

hl.config({

    ecosystem = {

        -- Require explicit permission for privileged ecosystem actions.
        enforce_permissions = true,

    },

})

--------------------------------------------------------------------------------
-- Screen Capture
--------------------------------------------------------------------------------

-- Hyprshot
hl.permission(
    "/usr/(bin|local/bin)/hyprshot",
    "screencopy",
    "allow"
)

-- XDG Desktop Portal
hl.permission(
    "/usr/(lib|libexec|lib64)/xdg-desktop-portal-hyprland",
    "screencopy",
    "allow"
)

--------------------------------------------------------------------------------
-- Plugin Management
--------------------------------------------------------------------------------

hl.permission(
    "/usr/(bin|local/bin)/hyprpm",
    "plugin",
    "allow"
)