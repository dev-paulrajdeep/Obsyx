--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Input Configuration
--
-- Defines keyboard, pointer, touchpad and gesture behavior.
--------------------------------------------------------------------------------

hl.config({

    input = {

        ------------------------------------------------------------------------
        -- Keyboard
        ------------------------------------------------------------------------

        kb_layout  = "us",
        kb_variant = "",
        kb_model   = "",
        kb_options = "",
        kb_rules   = "",

        ------------------------------------------------------------------------
        -- Mouse
        ------------------------------------------------------------------------

        -- Follow the cursor when changing focus.
        follow_mouse = 1,

        -- Raw sensitivity modifier.
        -- Range: -1.0 → 1.0
        sensitivity = 0,

        ------------------------------------------------------------------------
        -- Touchpad
        ------------------------------------------------------------------------

        touchpad = {

            -- macOS-style scrolling.
            natural_scroll = true,

            -- Tap to click.
            tap_to_click = true,

            -- Disable accidental input while typing.
            disable_while_typing = true,

            -- Clicking with two fingers performs right-click.
            clickfinger_behavior = true,

        },

    },

})

--------------------------------------------------------------------------------
-- Gestures
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Workspace Navigation
--
-- Three-finger horizontal swipe
-- cycles between workspaces.
--------------------------------------------------------------------------------

hl.gesture({

    fingers = 3,

    direction = "horizontal",

    action = "workspace",

})

--------------------------------------------------------------------------------
-- Scratchpad
--
-- Four-finger swipe down
-- toggles the terminal scratchpad.
--------------------------------------------------------------------------------

hl.gesture({

    fingers = 4,

    direction = "down",

    action = "special",

    workspace_name = "terminal",

})

--------------------------------------------------------------------------------
-- Cursor Zoom
--
-- Two-finger pinch
-- activates the accessibility magnifier.
--------------------------------------------------------------------------------

hl.gesture({

    fingers = 2,

    direction = "pinch",

    action = "cursorZoom",

    mode = "live",

    zoom_level = 1,

})