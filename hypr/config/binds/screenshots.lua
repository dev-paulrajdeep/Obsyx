--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Screenshot Keybindings
--------------------------------------------------------------------------------

local MOD = "SUPER"

--------------------------------------------------------------------------------
-- Screenshot Bindings
--------------------------------------------------------------------------------

local ScreenshotBindings = {

    ------------------------------------------------------------------------
    -- Clipboard
    ------------------------------------------------------------------------

    {
        key = MOD .. " + S",
        command = Registry.Screenshot.regionClipboard,
        description = "Region → Clipboard",
    },

    {
        key = MOD .. " + SHIFT + S",
        command = Registry.Screenshot.regionSave,
        description = "Region → File",
    },

    ------------------------------------------------------------------------
    -- Window
    ------------------------------------------------------------------------

    {
        key = MOD .. " + ALT + S",
        command = Registry.Screenshot.windowClipboard,
        description = "Window → Clipboard",
    },

    {
        key = MOD .. " + ALT + SHIFT + S",
        command = Registry.Screenshot.windowSave,
        description = "Window → File",
    },

    ------------------------------------------------------------------------
    -- Output
    ------------------------------------------------------------------------

    {
        key = "Print",
        command = Registry.Screenshot.outputSave,
        description = "Monitor → File",
    },

    {
        key = "SHIFT + Print",
        command = Registry.Screenshot.outputClipboard,
        description = "Monitor → Clipboard",
    },

}

--------------------------------------------------------------------------------
-- Register
--------------------------------------------------------------------------------

for _, bind in ipairs(ScreenshotBindings) do

    hl.bind(

        bind.key,

        hl.dsp.exec_cmd(bind.command),

        {

            locked = true,

            description = bind.description,

        }

    )

end