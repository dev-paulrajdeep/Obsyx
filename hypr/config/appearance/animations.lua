--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Animations
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Curves
--------------------------------------------------------------------------------

-- Primary UI motion.
hl.curve("executive", {

    type = "bezier",

    points = {

        {0.25, 1.00},
        {0.50, 1.00},

    },

})

-- Used for fades.
hl.curve("glass", {

    type = "bezier",

    points = {

        {0.16, 1.00},
        {0.30, 1.00},

    },

})

-- Soft spring for window movement.
hl.curve("inertia", {

    type = "spring",

    mass = 1.0,

    stiffness = 95,

    dampening = 18,

})

--------------------------------------------------------------------------------
-- Global
--------------------------------------------------------------------------------

hl.animation({

    leaf = "global",

    enabled = true,

    speed = 1.90,

    bezier = "executive",

})

--------------------------------------------------------------------------------
-- Windows
--------------------------------------------------------------------------------

hl.animation({

    leaf = "windows",

    enabled = true,

    speed = 2.00,

    spring = "inertia",

})

hl.animation({

    leaf = "windowsIn",

    enabled = true,

    speed = 1.90,

    spring = "inertia",

    style = "popin 95%",

})

hl.animation({

    leaf = "windowsOut",

    enabled = true,

    speed = 1.30,

    bezier = "glass",

    style = "popin 98%",

})

hl.animation({

    leaf = "windowsMove",

    enabled = true,

    speed = 1.80,

    spring = "inertia",

})

--------------------------------------------------------------------------------
-- Borders
--------------------------------------------------------------------------------

hl.animation({

    leaf = "border",

    enabled = true,

    speed = 1.10,

    bezier = "glass",

})

--------------------------------------------------------------------------------
-- Fade
--------------------------------------------------------------------------------

hl.animation({

    leaf = "fade",

    enabled = true,

    speed = 1.25,

    bezier = "glass",

})

hl.animation({

    leaf = "fadeIn",

    enabled = true,

    speed = 1.10,

    bezier = "glass",

})

hl.animation({

    leaf = "fadeOut",

    enabled = true,

    speed = 1.00,

    bezier = "glass",

})

--------------------------------------------------------------------------------
-- Layers
--------------------------------------------------------------------------------

hl.animation({

    leaf = "layers",

    enabled = true,

    speed = 1.70,

    bezier = "executive",

})

hl.animation({

    leaf = "layersIn",

    enabled = true,

    speed = 1.50,

    bezier = "glass",

    style = "fade",

})

hl.animation({

    leaf = "layersOut",

    enabled = true,

    speed = 1.20,

    bezier = "glass",

    style = "fade",

})

--------------------------------------------------------------------------------
-- Workspaces
--------------------------------------------------------------------------------

hl.animation({

    leaf = "workspaces",

    enabled = true,

    speed = 1.90,

    bezier = "executive",

    style = "slidefade 12%",

})

hl.animation({

    leaf = "workspacesIn",

    enabled = true,

    speed = 1.90,

    bezier = "executive",

    style = "slidefade 12%",

})

hl.animation({

    leaf = "workspacesOut",

    enabled = true,

    speed = 1.90,

    bezier = "executive",

    style = "slidefade 12%",

})