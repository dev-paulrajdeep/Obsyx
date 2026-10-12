--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Application Keybindings
--------------------------------------------------------------------------------

local MOD = "SUPER"

--------------------------------------------------------------------------------
-- Application Launchers
--------------------------------------------------------------------------------

local Applications = {

    { "Return", Registry.Apps.terminal,     "Terminal Emulator" },
    { "Space",  Registry.Desktop.launcher,  "Application Launcher" },
    { "B",      Registry.Apps.browser,      "Web Browser" },
    { "E",      Registry.Apps.fileManager,  "File Manager" },
    { "L",      Registry.Desktop.lock,      "Lock Screen" },
    { "C",      Registry.Apps.editor,       "Code Editor" },
    { "M",      Registry.Apps.musicPlayer,  "Music Player" },
    { "V",      Registry.Desktop.clipboard, "Clipboard History" },
   
}

--------------------------------------------------------------------------------
-- Register Keybindings
--------------------------------------------------------------------------------

for _, app in ipairs(Applications) do

    hl.bind(
        MOD .. " + " .. app[1],
        hl.dsp.exec_cmd(app[2]),
        {
            description = app[3],
        }
    )

end