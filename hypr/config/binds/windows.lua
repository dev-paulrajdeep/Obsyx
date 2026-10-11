--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Window Management
--
-- Stable, production-grade window controls.
--------------------------------------------------------------------------------

local MOD = "SUPER"

--------------------------------------------------------------------------------
-- Direction Map
--------------------------------------------------------------------------------

local Directions = {

    { "left",  "left" },
    { "down",  "down" },
    { "up",    "up" },
    { "right", "right" },

}


--------------------------------------------------------------------------------
-- Window Actions
--------------------------------------------------------------------------------

hl.bind(

    MOD .. " + Q",

    hl.dsp.window.close(),

    {

        description = "Close Window",

    }

)

hl.bind(

    MOD .. " + V",

    hl.dsp.window.float({

        action = "toggle",

    }),

    {

        description = "Toggle Floating",

    }

)

hl.bind(

    MOD .. " + F",

    hl.dsp.window.fullscreen(),

    {

        description = "Toggle Fullscreen",

    }

)

hl.bind(

    MOD .. " + P",

    hl.dsp.window.pseudo(),

    {

        description = "Toggle Pseudo",

    }

)

hl.bind(

    MOD .. " + SHIFT + P",

    hl.dsp.window.pin({

        action = "toggle",

    }),

    {

        description = "Toggle Pin",

    }

)

--------------------------------------------------------------------------------
-- Layout
--------------------------------------------------------------------------------

hl.bind(

    MOD .. " + J",

    hl.dsp.layout("togglesplit"),

    {

        description = "Toggle Split",

    }

)

--------------------------------------------------------------------------------
-- Focus
--------------------------------------------------------------------------------

for _, item in ipairs(Directions) do

    local key, direction = item[1], item[2]

    hl.bind(

        MOD .. " + " .. key,

        hl.dsp.focus({

            direction = direction,

        }),

        {

            description = "Focus " .. direction,

        }

    )

end

--------------------------------------------------------------------------------
-- Mouse Controls
--------------------------------------------------------------------------------

hl.bind(

    MOD .. " + mouse:272",

    hl.dsp.window.drag(),

    {

        mouse = true,

        description = "Drag Window",

    }

)

hl.bind(

    MOD .. " + mouse:273",

    hl.dsp.window.resize(),

    {

        mouse = true,

        description = "Resize Window",

    }

)