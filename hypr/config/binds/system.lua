--------------------------------------------------------------------------------
-- Noctis Amethyst
-- System Keybindings
--
-- Session management and power controls.
--------------------------------------------------------------------------------

local MOD = "SUPER"

--------------------------------------------------------------------------------
-- Session
--------------------------------------------------------------------------------

local SystemBindings = {

    ------------------------------------------------------------------------
    -- Primary
    ------------------------------------------------------------------------

    {
        key = MOD .. " + Escape",
        command = Registry.Session.powerMenu,
        description = "Power Menu",
    },

    {
        key = MOD .. " + L",
        command = Registry.Session.lock,
        description = "Lock Session",
    },

    ------------------------------------------------------------------------
    -- Direct Actions
    ------------------------------------------------------------------------

    {
        key = MOD .. " + CTRL + L",
        command = Registry.Session.logout,
        description = "Logout",
    },

    {
        key = MOD .. " + CTRL + S",
        command = Registry.Session.suspend,
        description = "Suspend",
    },

    {
        key = MOD .. " + CTRL + R",
        command = Registry.Session.reboot,
        description = "Reboot",
    },

    {
        key = MOD .. " + CTRL + H",
        command = Registry.Session.hibernate,
        description = "Hibernate",
    },

    {
        key = MOD .. " + CTRL + P",
        command = Registry.Session.shutdown,
        description = "Power Off",
    },

    ------------------------------------------------------------------------
    -- Display
    ------------------------------------------------------------------------

    {
        key = MOD .. " + CTRL + O",
        command = Registry.Session.monitorOff,
        description = "Turn Monitor Off",
    },

}

--------------------------------------------------------------------------------
-- Register Bindings
--------------------------------------------------------------------------------

for _, bind in ipairs(SystemBindings) do

    hl.bind(

        bind.key,

        hl.dsp.exec_cmd(bind.command),

        {

            locked = true,

            description = bind.description,

        }

    )

end