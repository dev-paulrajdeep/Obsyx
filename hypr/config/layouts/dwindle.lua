--------------------------------------------------
---------------- DWINDLE LAYOUT -------------------
--------------------------------------------------

hl.config({

    dwindle = {

        --------------------------------------------------
        -- Window Splitting
        --------------------------------------------------

        -- Follow cursor when creating splits.
        -- 0 = Smart (recommended)
        -- 1 = Always left / top
        -- 2 = Always right / bottom
        force_split = 0,

        -- Preserve tree orientation after windows
        -- are closed. Required for togglesplit.
        preserve_split = true,

        -- Cursor-aware split direction.
        -- Automatically enables preserve_split.
        smart_split = true,

        --------------------------------------------------
        -- Resizing
        --------------------------------------------------

        -- Resize based on nearest corner.
        smart_resizing = true,

        --------------------------------------------------
        -- Split Behaviour
        --------------------------------------------------

        -- Preselect directions are one-shot.
        permanent_direction_override = false,

        -- Always split relative to focused window.
        use_active_for_splits = true,

        -- Equal 50 / 50 split.
        default_split_ratio = 1.08,

        -- Give the active window the split.
        split_bias = 1,

        --------------------------------------------------
        -- Special Workspace
        --------------------------------------------------

        -- Scratchpad windows slightly smaller.
        special_scale_factor = 0.88,

        --------------------------------------------------
        -- Wide Monitor Behaviour
        --------------------------------------------------

        -- Default works perfectly on laptops.
        split_width_multiplier = 1.0,

        --------------------------------------------------
        -- Mouse Behaviour
        --------------------------------------------------

        -- Keep classic dragging.
        precise_mouse_move = true,

    },

})