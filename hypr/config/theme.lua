--------------------------------------------------------------------------------
-- Obsyx
-- Theme Loader
--
-- Dynamically loads the active theme table based on Registry.Theme.name.
-- Exposes the active theme globally as `Theme` and in `Registry.Theme.current`.
--------------------------------------------------------------------------------

local function slugify(name)
    if not name or type(name) ~= "string" then
        return "noctis_amethyst"
    end
    return (name:lower():gsub("%s+", "_"):gsub("[^%w_]", ""))
end

local theme_name = (Registry and Registry.Theme and Registry.Theme.name) or "Noctis Amethyst"
local theme_slug = slugify(theme_name)

local ok, loaded_theme = pcall(require, "themes." .. theme_slug)

if not ok or type(loaded_theme) ~= "table" then
    error(string.format(
        "Obsyx Theme Loader: failed to load theme '%s' (module 'themes.%s'): %s",
        tostring(theme_name),
        tostring(theme_slug),
        tostring(loaded_theme)
    ))
end

-- Validate critical structures
local required_sections = { "palette", "geometry", "blur" }
for _, section in ipairs(required_sections) do
    if not loaded_theme[section] or type(loaded_theme[section]) ~= "table" then
        error(string.format(
            "Obsyx Theme Loader: theme '%s' is missing required table '%s'",
            theme_name,
            section
        ))
    end
end

-- Fallback tables if optional sections are missing
loaded_theme.opacity = loaded_theme.opacity or {
    active = 0.75,
    inactive = 0.64,
    fullscreen = 0.95,
}

loaded_theme.shadow = loaded_theme.shadow or {
    range = 18,
    render_power = 4,
    color = "rgba(00000088)",
}

-- Publish globally and in Registry
Theme = loaded_theme

if Registry and Registry.Theme then
    Registry.Theme.current = loaded_theme
    Registry.Theme.slug = theme_slug
end

return loaded_theme
