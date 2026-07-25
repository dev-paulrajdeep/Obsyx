--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Layer Rules
--
-- GTK3 cannot render browser-style backdrop filters. Frosted glass belongs in
-- Hyprland's compositor, scoped to Waybar rather than applied globally.
--------------------------------------------------------------------------------

hl.layer_rule({

    name = "waybar-glass",

    match = {
        namespace = "waybar",
    },

    blur = true,

    -- The bar background is transparent. Blur only the visible surfaces; this
    -- threshold is above the shadow alpha (0.34) and below surface alpha (0.88).
    ignore_alpha = 0.60,

    blur_popups = true,

})
