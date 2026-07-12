--------------------------------------------------------------------------------
-- Noctis Amethyst
-- System Registry
--
-- Single source of truth for executables, commands and global constants.
-- Every module should reference this file instead of hardcoding values.
--------------------------------------------------------------------------------

Registry = {}

--------------------------------------------------------------------------------
-- User Applications
--------------------------------------------------------------------------------

Registry.Apps = {

    terminal       = "kitty",
    browser        = "vivaldi",
    editor         = "code",
    musicPlayer    = "spotify",
    fileManager    = "dolphin",
    terminalFM     = "yazi",

}

--------------------------------------------------------------------------------
-- Desktop Components
--------------------------------------------------------------------------------

Registry.Desktop = {

    launcher       = "rofi -show drun",
    lock           = "hyprlock",
    logout         = "wlogout",
    notification   = "swaync",
    wallpaper      = "awww",
    statusBar      = "waybar",
}

--------------------------------------------------------------------------------
-- Utilities
--------------------------------------------------------------------------------

Registry.Tools = {

    screenshot     = "hyprshot",
    colorPicker    = "hyprpicker",
    calculator     = "qalculate-gtk",
    clipboard      = "wl-copy",
    clipboardStore = "cliphist",

}

--------------------------------------------------------------------------------
-- System Services
--------------------------------------------------------------------------------

Registry.Services = {

    bluetooth      = "blueman-manager",
    network        = "nm-connection-editor",
    media          = "playerctl",

}

--------------------------------------------------------------------------------
-- Startup Commands
--------------------------------------------------------------------------------

Registry.Startup = {

    wallpaperDaemon    = "awww-daemon",
    statusBar          = "waybar",
    notificationDaemon = "swaync",
    wallpaper          = "awww img ~/Pictures/Wallpapers/default.jpg",
    clipboardText      = "wl-paste --type text --watch cliphist store",
    clipboardImage     = "wl-paste --type image --watch cliphist store",
    networkApplet      = "nm-applet",
    bluetoothApplet    = "blueman-applet",

}

--------------------------------------------------------------------------------
-- Filesystem
--------------------------------------------------------------------------------

Registry.Paths = {

    wallpapers = "~/Pictures/Wallpapers",
    defaultWallpaper = "~/Pictures/Wallpapers/default.jpg",

}

--------------------------------------------------------------------------------
-- Noctis Amethyst
--------------------------------------------------------------------------------

Registry.Theme = {

    name = "Noctis Amethyst",

}


--------------------------------------------------------------------------------
-- Media & System Commands
--------------------------------------------------------------------------------

Registry.Media = {

    volumeUp        = "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+",
    volumeDown      = "wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-",
    volumeMute      = "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle",

    microphoneMute  = "wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle",

    brightnessUp    = "brightnessctl -e4 -n2 set 5%+",
    brightnessDown  = "brightnessctl -e4 -n2 set 5%-",

    next            = "playerctl next",
    previous        = "playerctl previous",
    playPause       = "playerctl play-pause",

}

Registry.Screenshot = {

    regionClipboard = "hyprshot -m region --clipboard-only",
    regionSave      = "hyprshot -m region",

    windowClipboard = "hyprshot -m window --clipboard-only",
    windowSave      = "hyprshot -m window",

    outputClipboard = "hyprshot -m output --clipboard-only",
    outputSave      = "hyprshot -m output",

}

--------------------------------------------------------------------------------
-- Session Management
--------------------------------------------------------------------------------

Registry.Session = {

    lock       = Registry.Desktop.lock,
    logout     = "hyprctl dispatch exit",
    powerMenu  = Registry.Desktop.logout,
    suspend    = "systemctl suspend",
    reboot     = "systemctl reboot",
    shutdown   = "systemctl poweroff",
    hibernate  = "systemctl hibernate",
    monitorOff = "hyprctl dispatch dpms off",

}

return Registry
