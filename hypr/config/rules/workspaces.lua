--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Workspace Rules
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Persistent Activity Workspaces
--------------------------------------------------------------------------------

local Workspaces = {

    { id = "1", name = "Terminal"      },
    { id = "2", name = "Development"   },
    { id = "3", name = "Web"           },
    { id = "4", name = "Files"         },
    { id = "5", name = "Media"         },
    { id = "6", name = "Communication"},
    { id = "7", name = "Laboratory"    },
    { id = "8", name = "Misc"          },
    { id = "9", name = "Scratch"       },

}

for _, ws in ipairs(Workspaces) do

    hl.workspace_rule({

        workspace = ws.id,

        default_name = ws.name,

        persistent = true,

    })

end

--------------------------------------------------------------------------------
-- Smart Gaps
--------------------------------------------------------------------------------

-- Remove outer gaps when only one tiled window exists.

hl.workspace_rule({

    workspace = "w[tv1]",

    gaps_in = 0,

    gaps_out = 2,

})

--------------------------------------------------------------------------------
-- Fullscreen
--------------------------------------------------------------------------------

hl.workspace_rule({

    workspace = "f[1]",

    gaps_in = 0,

    gaps_out = 0,

})