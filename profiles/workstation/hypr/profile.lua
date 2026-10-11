--------------------------------------------------------------------------------
-- Obsyx
-- Workstation Profile Overrides
--
-- High-fidelity, multi-monitor, high-refresh desktop performance:
-- • Triple blur passes with extended radius and vibrancy.
-- • Full ambient drop shadows with extended range.
-- • Variable refresh rate (VRR) enabled for high-Hz gaming and fluid displays.
--------------------------------------------------------------------------------

hl.config({

    decoration = {

        shadow = {

            enabled = true,

            range = 24,

            render_power = 3,

        },

        blur = {

            enabled = true,

            size = 8,

            passes = 3,

            vibrancy = 0.35,

        },

    },

    misc = {

        vrr = 1,

    },

})
