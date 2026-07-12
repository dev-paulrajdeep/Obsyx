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

    { "XF86AudioRaiseVolume", Registry.Media.volumeUp       },
    { "XF86AudioLowerVolume", Registry.Media.volumeDown     },
    { "XF86AudioMute",        Registry.Media.volumeMute     },
    { "XF86AudioMicMute",     Registry.Media.microphoneMute },

    { "XF86MonBrightnessUp",   Registry.Media.brightnessUp   },
    { "XF86MonBrightnessDown", Registry.Media.brightnessDown },

}

--------------------------------------------------------------------------------
-- Media Playback
--------------------------------------------------------------------------------

local Playback = {

    { "XF86AudioNext",  Registry.Media.next       },
    { "XF86AudioPrev",  Registry.Media.previous   },
    { "XF86AudioPause", Registry.Media.playPause  },
    { "XF86AudioPlay",  Registry.Media.playPause  },

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

        }

    )

end