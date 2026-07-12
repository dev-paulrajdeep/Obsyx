--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Application Keybindings
--------------------------------------------------------------------------------

local MOD = "SUPER"

--------------------------------------------------------------------------------
-- Application Launchers
--------------------------------------------------------------------------------

local Applications = {

    { "Return", Registry.Apps.terminal      },
    { "Space",  Registry.Desktop.launcher   },
    { "B",      Registry.Apps.browser       },
    { "E",      Registry.Apps.fileManager   },
    { "L",      Registry.Desktop.lock       },

}

--------------------------------------------------------------------------------
-- Register Keybindings
--------------------------------------------------------------------------------

for _, app in ipairs(Applications) do

    hl.bind(
        MOD .. " + " .. app[1],
        hl.dsp.exec_cmd(app[2])
    )

end