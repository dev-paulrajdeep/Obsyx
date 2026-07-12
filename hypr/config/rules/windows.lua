--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Window Rules
--
-- Philosophy:
-- Define behaviors, not exceptions.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Global Behaviour
--------------------------------------------------------------------------------

-- Ignore maximize requests from applications.
hl.window_rule({

    name = "ignore-maximize",

    match = {

        class = ".*",

    },

    suppress_event = "maximize",

})

--------------------------------------------------------------------------------
-- XWayland Compatibility
--------------------------------------------------------------------------------

-- Temporary XWayland drag windows.
hl.window_rule({

    name = "xwayland-drag",

    match = {

        class      = "^$",
        title      = "^$",

        xwayland   = true,
        float      = true,

        fullscreen = false,
        pin        = false,

    },

    no_focus = true,

})

--------------------------------------------------------------------------------
-- Floating Utilities
--------------------------------------------------------------------------------

-- NOTE: class/title are matched against Hyprland's own regex engine, not Lua
-- patterns. Hyphens and dots are not special here and should NOT be escaped
-- with '%' -- that's a Lua-pattern habit that doesn't apply to this field.
local FloatingUtilities = {

    "^blueman-manager$",
    "^nm-connection-editor$",
    "^pavucontrol$",
    "^qalculate-gtk$",
    "^org.gnome.Calculator$",

}

for _, class in ipairs(FloatingUtilities) do

    hl.window_rule({

        name = "floating-" .. class,

        match = {

            class = class,

        },

        float = true,
        center = true,

    })

end

--------------------------------------------------------------------------------
-- Modal Dialogs
--------------------------------------------------------------------------------

hl.window_rule({

    name = "modal",

    match = {

        modal = true,

    },

    float = true,

    center = true,

    dim_around = true,

})

--------------------------------------------------------------------------------
-- Authentication
--------------------------------------------------------------------------------

hl.window_rule({

    name = "authentication",

    match = {

        class = ".*[Pp]olkit.*",

    },

    float = true,

    center = true,

})

--------------------------------------------------------------------------------
-- File Choosers
--------------------------------------------------------------------------------

hl.window_rule({

    name = "file-dialog",

    match = {

        title = "Open File|Save File|Choose Files?|Select.*",

    },

    float = true,

    center = true,

})

--------------------------------------------------------------------------------
-- Picture in Picture
--------------------------------------------------------------------------------

hl.window_rule({

    name = "pip",

    match = {

        title = "Picture-in-Picture",

    },

    float = true,

    pin = true,

})

--------------------------------------------------------------------------------
-- Hyprland Utilities
--------------------------------------------------------------------------------

local HyprUtilities = {

    "^hyprland-run$",
    "^hyprpicker$",

}

for _, class in ipairs(HyprUtilities) do

    hl.window_rule({

        name = "hypr-" .. class,

        match = {

            class = class,

        },

        float = true,

        center = true,

    })

end

--------------------------------------------------------------------------------
-- Notifications
--------------------------------------------------------------------------------

hl.window_rule({

    name = "notifications",

    match = {

        class = "^swaync-control-center$",

    },

    float = true,

})

--------------------------------------------------------------------------------
-- Fullscreen
--------------------------------------------------------------------------------

hl.window_rule({

    name = "fullscreen",

    match = {

        fullscreen = true,

    },

    rounding = 0,

    border_size = 0,

    no_shadow = true,

    dim_around = false,

})

--------------------------------------------------------------------------------
-- Floating Style
--------------------------------------------------------------------------------

hl.window_rule({

    name = "floating-style",

    match = {

        float = true,

    },

    rounding = 10,

    dim_around = true,

})