--------------------------------------------------------------------------------
-- Noctis Amethyst
-- Media Keys
--
-- Hardware multimedia and brightness controls.
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
-- Repeating Controls
--------------------------------------------------------------------------------

local Repeating = {

    { "XF86AudioRaiseVolume", Registry.Media.volumeUp,       "Volume Up" },
    { "XF86AudioLowerVolume", Registry.Media.volumeDown,     "Volume Down" },
    { "XF86AudioMute",        Registry.Media.volumeMute,     "Toggle Volume Mute" },
    { "XF86AudioMicMute",     Registry.Media.microphoneMute, "Toggle Mic Mute" },

    { "XF86MonBrightnessUp",   Registry.Media.brightnessUp,   "Brightness Up" },
    { "XF86MonBrightnessDown", Registry.Media.brightnessDown, "Brightness Down" },

}

--------------------------------------------------------------------------------
-- Media Playback
--------------------------------------------------------------------------------

local Playback = {

    { "XF86AudioNext",  Registry.Media.next,      "Next Track" },
    { "XF86AudioPrev",  Registry.Media.previous,  "Previous Track" },
    { "XF86AudioPause", Registry.Media.playPause, "Toggle Play/Pause" },
    { "XF86AudioPlay",  Registry.Media.playPause, "Toggle Play/Pause" },

}

--------------------------------------------------------------------------------
-- Register Repeating Keys
--------------------------------------------------------------------------------

for _, bind in ipairs(Repeating) do

    hl.bind(

        bind[1],

        hl.dsp.exec_cmd(bind[2]),

        {

            locked = true,

            repeating = true,

            description = bind[3],

        }

    )

end

--------------------------------------------------------------------------------
-- Register Playback Keys
--------------------------------------------------------------------------------

for _, bind in ipairs(Playback) do

    hl.bind(

        bind[1],

        hl.dsp.exec_cmd(bind[2]),

        {

            locked = true,

            description = bind[3],

        }

    )

end