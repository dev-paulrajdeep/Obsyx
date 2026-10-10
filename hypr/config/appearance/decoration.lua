--------------------------------------------------------------------------------
-- Obsyx
-- Decoration
--
-- Dynamically binds window geometry, borders, opacity, shadows, and blur
-- from the active theme tokens.
--------------------------------------------------------------------------------

local theme = Theme or require("config.theme")

hl.config({

    general = {

        ------------------------------------------------------------------------
        -- Layout
        ------------------------------------------------------------------------

        gaps_in  = theme.geometry.gaps_in,

        gaps_out = theme.geometry.gaps_out,

        border_size = theme.geometry.border_size,

        layout = "dwindle",

        resize_on_border = true,

        allow_tearing = false,

        ------------------------------------------------------------------------
        -- Borders
        ------------------------------------------------------------------------

        col = {

            active_border = {

                colors = {

                    theme.palette.accent_gradient_start,

                    theme.palette.accent_gradient_end,

                },

                angle = 45,

            },

            inactive_border =

                theme.palette.border_inactive,

        },

    },

    ------------------------------------------------------------------------
    -- Decoration
    ------------------------------------------------------------------------

    decoration = {

        --------------------------------------------------------------------
        -- Geometry
        --------------------------------------------------------------------

        rounding = theme.geometry.rounding,

        rounding_power = theme.geometry.rounding_power,

        --------------------------------------------------------------------
        -- Opacity
        --------------------------------------------------------------------

        active_opacity   = theme.opacity.active,

        inactive_opacity = theme.opacity.inactive,

        fullscreen_opacity = theme.opacity.fullscreen,

        --------------------------------------------------------------------
        -- Shadow
        --------------------------------------------------------------------

        shadow = {

            enabled = true,

            range = theme.shadow.range,

            render_power = theme.shadow.render_power,

            color = theme.shadow.color,

        },

        --------------------------------------------------------------------
        -- Blur
        --------------------------------------------------------------------

        blur = {

            enabled = true,

            size = theme.blur.size,

            passes = theme.blur.passes,

            vibrancy = theme.blur.vibrancy,

            contrast = theme.blur.contrast,

            brightness = theme.blur.brightness,

        },

    },

    ------------------------------------------------------------------------
    -- Animations
    ------------------------------------------------------------------------

    animations = {

        enabled = true,

    },

})