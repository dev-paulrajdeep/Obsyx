--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Workspace Management
--------------------------------------------------------------------------------

local MOD = "SUPER"

--------------------------------------------------------------------------------
-- Workspace Navigation
--------------------------------------------------------------------------------

for workspace = 1, 10 do

    local key = workspace % 10

    ------------------------------------------------------------------------
    -- Switch Workspace
    ------------------------------------------------------------------------

    hl.bind(

        MOD .. " + " .. key,

        hl.dsp.focus({

            workspace = workspace,

        }),

        {

            description = "Workspace " .. workspace,

        }

    )

    ------------------------------------------------------------------------
    -- Move Active Window
    ------------------------------------------------------------------------

    hl.bind(

        MOD .. " + SHIFT + " .. key,

        hl.dsp.window.move({

            workspace = workspace,

        }),

        {

            description = "Move Window → Workspace " .. workspace,

        }

    )

end

--------------------------------------------------------------------------------
-- Scratchpad
--------------------------------------------------------------------------------

hl.bind(

    MOD .. " + Grave",

    hl.dsp.workspace.toggle_special("terminal"),

    {

        description = "Toggle Terminal Scratchpad",

    }

)

hl.bind(

    MOD .. " + SHIFT + Grave",

    hl.dsp.window.move({

        workspace = "special:terminal",

    }),

    {

        description = "Move Window → Terminal Scratchpad",

    }

)

--------------------------------------------------------------------------------
-- Workspace Cycling
--------------------------------------------------------------------------------

hl.bind(

    MOD .. " + mouse_down",

    hl.dsp.focus({

        workspace = "e+1",

    }),

    {

        description = "Next Workspace",

    }

)

hl.bind(

    MOD .. " + mouse_up",

    hl.dsp.focus({

        workspace = "e-1",

    }),

    {

        description = "Previous Workspace",

    }

)