--------------------------------------------------------------------------------
-- Obsyx
-- Laptop Profile Overrides
--
-- Power-conservative, low-overhead settings for mobile and battery operation:
-- • Single blur pass with reduced size to minimize GPU compositing load.
-- • Shadows disabled to conserve rendering power.
-- • VFR (variable frame rate) enabled and VRR disabled for power efficiency.
--------------------------------------------------------------------------------

hl.config({

    decoration = {

        shadow = {

            enabled = false,

        },

        blur = {

            enabled = true,

            size = 4,

            passes = 1,

            vibrancy = 0.15,

        },

    },

    misc = {

        vfr = true,

        vrr = 0,

    },

})
