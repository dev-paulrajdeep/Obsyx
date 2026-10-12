#!/usr/bin/env python3
"""Obsyx Theme Token Compiler.

Reads a canonical JSON token source and generates:
  - Hyprland-compatible Lua theme table
  - Waybar-compatible GTK3 CSS token stylesheet
  - Rofi-compatible RASI token stylesheet
  - SwayNC-compatible GTK3 CSS token stylesheet
  - Hyprland/Hyprlock-compatible conf variable file
  - Kitty-compatible terminal color configuration
  - Wlogout-compatible GTK3 CSS token stylesheet

Usage:
    python3 tools/build_tokens.py [OPTIONS]

Options:
    --tokens PATH         Token source (default: core/tokens/noctis_amethyst.json)
    --lua-out PATH        Lua output   (default: hypr/themes/noctis_amethyst.lua)
    --css-out PATH        CSS output   (default: waybar/generated/theme-tokens.css)
    --rofi-out PATH       Rofi output  (default: rofi/generated/theme-tokens.rasi)
    --swaync-out PATH     SwayNC CSS   (default: swaync/generated/theme-tokens.css)
    --hypr-conf-out PATH  Hypr conf    (default: hypr/generated/theme-tokens.conf)
    --kitty-out PATH      Kitty conf   (default: kitty/generated/theme-tokens.conf)
    --wlogout-out PATH    Wlogout CSS  (default: wlogout/generated/theme-tokens.css)
"""

import argparse
import json
import os
import re
import sys
import tempfile

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')

REQUIRED_SECTIONS = ('name', 'palette', 'geometry', 'blur')

# Ordered mapping: (json palette key) -> (CSS @define-color name).
# Only palette entries that belong in the Waybar CSS output are listed here.
# Hyprland-only entries (gradient endpoints, border_inactive) are omitted.
CSS_TOKEN_MAP = [
    ('void',            'noctis-void'),
    ('surface',         'noctis-surface'),
    ('surface_raised',  'noctis-surface-raised'),
    ('surface_focus',   'noctis-surface-focus'),
    ('overlay',         'noctis-overlay'),
    ('ink_strong',      'ink-strong'),
    ('ink_default',     'ink-default'),
    ('ink_muted',       'ink-muted'),
    ('ink_quiet',       'ink-quiet'),
    ('hairline',        'hairline'),
    ('hairline_strong', 'hairline-strong'),
    ('shadow',          'shadow'),
    ('accent',          'amethyst'),
    ('accent_ink',      'amethyst-ink'),
    ('accent_wash',     'amethyst-wash'),
    ('accent_fill',     'amethyst-fill'),
    ('accent_line',     'amethyst-line'),
    ('warning',         'warning'),
    ('danger',          'danger'),
    ('danger_wash',     'danger-wash'),
]

# Ordered mapping: (json palette key) -> (Hyprland / Hyprlock conf variable name).
HYPR_CONF_TOKEN_MAP = [
    ('void',                  'noctis_void'),
    ('surface',               'noctis_surface'),
    ('surface_raised',        'noctis_surface_raised'),
    ('surface_focus',         'noctis_surface_focus'),
    ('overlay',               'noctis_overlay'),
    ('ink_strong',            'ink_strong'),
    ('ink_default',           'ink_default'),
    ('ink_muted',             'ink_muted'),
    ('ink_quiet',             'ink_quiet'),
    ('hairline',              'hairline'),
    ('hairline_strong',       'hairline_strong'),
    ('shadow',                'shadow'),
    ('accent',                'amethyst'),
    ('accent_ink',            'amethyst_ink'),
    ('accent_wash',           'amethyst_wash'),
    ('accent_fill',           'amethyst_fill'),
    ('accent_line',           'amethyst_line'),
    ('accent_gradient_start', 'accent_gradient_start'),
    ('accent_gradient_end',   'accent_gradient_end'),
    ('warning',               'warning'),
    ('danger',                'danger'),
    ('danger_wash',           'danger_wash'),
    ('border_inactive',       'border_inactive'),
]

# Ordered list of all palette keys for Lua output (controls emission order).
LUA_PALETTE_ORDER = [
    'void',
    'surface',
    'surface_raised',
    'surface_focus',
    'overlay',
    'ink_strong',
    'ink_default',
    'ink_muted',
    'ink_quiet',
    'hairline',
    'hairline_strong',
    'shadow',
    'accent',
    'accent_ink',
    'accent_wash',
    'accent_fill',
    'accent_line',
    'accent_gradient_start',
    'accent_gradient_end',
    'warning',
    'danger',
    'danger_wash',
    'border_inactive',
]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class TokenError(Exception):
    """Raised when token validation fails."""


def _validate_hex(value, path):
    """Validate a hex color string."""
    if not isinstance(value, str) or not HEX_RE.match(value):
        raise TokenError(f'{path}: invalid hex color {value!r} '
                         f'(expected #rrggbb)')


def _validate_alpha(value, path):
    """Validate an alpha value."""
    if not isinstance(value, (int, float)):
        raise TokenError(f'{path}: alpha must be a number, got {type(value).__name__}')
    if not (0.0 <= value <= 1.0):
        raise TokenError(f'{path}: alpha {value} out of range [0.0, 1.0]')


def _validate_color_entry(value, path):
    """Validate a palette entry: either "#rrggbb" or {"hex": "...", "alpha": ...}."""
    if isinstance(value, str):
        _validate_hex(value, path)
    elif isinstance(value, dict):
        if 'hex' not in value:
            raise TokenError(f'{path}: color object missing "hex" field')
        if 'alpha' not in value:
            raise TokenError(f'{path}: color object missing "alpha" field')
        _validate_hex(value['hex'], f'{path}.hex')
        _validate_alpha(value['alpha'], f'{path}.alpha')
    else:
        raise TokenError(f'{path}: expected hex string or {{hex, alpha}} object, '
                         f'got {type(value).__name__}')


def _validate_numeric(value, path, allow_negative=False):
    """Validate a numeric value."""
    if not isinstance(value, (int, float)):
        raise TokenError(f'{path}: expected number, got {type(value).__name__}')
    if not allow_negative and value < 0:
        raise TokenError(f'{path}: value {value} must be non-negative')


def validate_tokens(tokens):
    """Validate the complete token structure. Raises TokenError on failure."""
    # Required top-level keys.
    for key in REQUIRED_SECTIONS:
        if key not in tokens:
            raise TokenError(f'missing required top-level key: {key!r}')

    if not isinstance(tokens['name'], str) or not tokens['name'].strip():
        raise TokenError('name: must be a non-empty string')

    # Palette.
    palette = tokens['palette']
    if not isinstance(palette, dict) or not palette:
        raise TokenError('palette: must be a non-empty object')
    for key, value in palette.items():
        _validate_color_entry(value, f'palette.{key}')

    # Geometry.
    geometry = tokens['geometry']
    if not isinstance(geometry, dict):
        raise TokenError('geometry: must be an object')
    for key, value in geometry.items():
        _validate_numeric(value, f'geometry.{key}')

    # Blur.
    blur = tokens['blur']
    if not isinstance(blur, dict):
        raise TokenError('blur: must be an object')
    for key, value in blur.items():
        _validate_numeric(value, f'blur.{key}')

    # Optional sections.
    if 'opacity' in tokens:
        opacity = tokens['opacity']
        if not isinstance(opacity, dict):
            raise TokenError('opacity: must be an object')
        for key, value in opacity.items():
            _validate_numeric(value, f'opacity.{key}')
            _validate_alpha(value, f'opacity.{key}')

    if 'shadow' in tokens:
        shadow = tokens['shadow']
        if not isinstance(shadow, dict):
            raise TokenError('shadow: must be an object')
        for key, value in shadow.items():
            if key == 'color':
                _validate_color_entry(value, 'shadow.color')
            else:
                _validate_numeric(value, f'shadow.{key}')


# ---------------------------------------------------------------------------
# Color conversion
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_str):
    """Convert '#rrggbb' to (r, g, b) integers."""
    h = hex_str.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _alpha_to_hex_byte(alpha):
    """Convert alpha float [0.0, 1.0] to two-char uppercase hex byte."""
    return format(int(alpha * 255 + 0.5), '02X')


def _color_to_hypr(entry):
    """Convert a palette entry to Hyprland format.

    Opaque hex  -> "#rrggbb"
    With alpha  -> "rgba(RRGGBBAA)"
    """
    if isinstance(entry, str):
        return entry
    hex_upper = entry['hex'].lstrip('#').upper()
    alpha_hex = _alpha_to_hex_byte(entry['alpha'])
    return f'rgba({hex_upper}{alpha_hex})'


def _color_to_css(entry):
    """Convert a palette entry to GTK3 CSS format.

    Opaque hex  -> #rrggbb;
    With alpha  -> rgba(R, G, B, A);
    """
    if isinstance(entry, str):
        return entry
    r, g, b = _hex_to_rgb(entry['hex'])
    alpha = f"{entry['alpha']:.2f}"
    return f'rgba({r}, {g}, {b}, {alpha})'


# ---------------------------------------------------------------------------
# Lua generation
# ---------------------------------------------------------------------------

def _lua_string(value):
    """Format a string as a Lua string literal."""
    return f'"{value}"'


def _lua_number(value):
    """Format a number as a Lua numeric literal."""
    if isinstance(value, float):
        # Emit minimal representation, avoiding unnecessary trailing zeros
        # but preserving at least one decimal for floats.
        s = f'{value:.10g}'
        if '.' not in s:
            s += '.0'
        return s
    return str(value)


def generate_lua(tokens, output_path):
    """Generate the Hyprland Lua theme table."""
    lines = []
    token_slug = tokens["name"].lower().replace(" ", "_")
    lines.append('--------------------------------------------------------------------------------')
    lines.append('-- AUTO-GENERATED by tools/build_tokens.py')
    lines.append(f'-- Source: core/tokens/{token_slug}.json')
    lines.append('-- DO NOT EDIT — modify the token source and re-run the compiler.')
    lines.append('--------------------------------------------------------------------------------')
    lines.append('')
    lines.append('local Theme = {}')
    lines.append('')
    lines.append(f'Theme.name = {_lua_string(tokens["name"])}')
    if 'version' in tokens:
        lines.append(f'Theme.version = {_lua_string(tokens["version"])}')
    lines.append('')

    # Palette.
    palette = tokens['palette']
    lines.append('Theme.palette = {')
    # Calculate alignment width from the keys we will emit.
    keys_to_emit = [k for k in LUA_PALETTE_ORDER if k in palette]
    max_key_len = max(len(k) for k in keys_to_emit) if keys_to_emit else 0
    for key in keys_to_emit:
        value = _color_to_hypr(palette[key])
        padded_key = key.ljust(max_key_len)
        lines.append(f'    {padded_key} = {_lua_string(value)},')
    lines.append('}')
    lines.append('')

    # Geometry.
    geometry = tokens['geometry']
    lines.append('Theme.geometry = {')
    geo_keys = list(geometry.keys())
    max_geo_len = max(len(k) for k in geo_keys) if geo_keys else 0
    for key in geo_keys:
        padded_key = key.ljust(max_geo_len)
        lines.append(f'    {padded_key} = {_lua_number(geometry[key])},')
    lines.append('}')
    lines.append('')

    # Opacity.
    if 'opacity' in tokens:
        opacity = tokens['opacity']
        lines.append('Theme.opacity = {')
        opa_keys = list(opacity.keys())
        max_opa_len = max(len(k) for k in opa_keys) if opa_keys else 0
        for key in opa_keys:
            padded_key = key.ljust(max_opa_len)
            lines.append(f'    {padded_key} = {_lua_number(opacity[key])},')
        lines.append('}')
        lines.append('')

    # Blur.
    blur = tokens['blur']
    lines.append('Theme.blur = {')
    blur_keys = list(blur.keys())
    max_blur_len = max(len(k) for k in blur_keys) if blur_keys else 0
    for key in blur_keys:
        padded_key = key.ljust(max_blur_len)
        lines.append(f'    {padded_key} = {_lua_number(blur[key])},')
    lines.append('}')
    lines.append('')

    # Shadow.
    if 'shadow' in tokens:
        shadow = tokens['shadow']
        lines.append('Theme.shadow = {')
        shadow_keys = list(shadow.keys())
        max_shd_len = max(len(k) for k in shadow_keys) if shadow_keys else 0
        for key in shadow_keys:
            padded_key = key.ljust(max_shd_len)
            value = shadow[key]
            if key == 'color':
                lines.append(f'    {padded_key} = {_lua_string(_color_to_hypr(value))},')
            else:
                lines.append(f'    {padded_key} = {_lua_number(value)},')
        lines.append('}')
        lines.append('')

    lines.append('return Theme')
    lines.append('')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# CSS generation
# ---------------------------------------------------------------------------

def generate_css(tokens, output_path):
    """Generate the Waybar GTK3 CSS token stylesheet."""
    lines = []
    lines.append('/* AUTO-GENERATED by tools/build_tokens.py')
    lines.append(f'   Source: core/tokens/{tokens["name"].lower().replace(" ", "_")}.json')
    lines.append('   DO NOT EDIT — modify the token source and re-run the compiler. */')
    lines.append('')

    palette = tokens['palette']

    # Calculate alignment width from CSS token names.
    max_name_len = max(len(css_name) for _, css_name in CSS_TOKEN_MAP)

    for json_key, css_name in CSS_TOKEN_MAP:
        if json_key not in palette:
            continue
        value = _color_to_css(palette[json_key])
        padded_name = css_name.ljust(max_name_len)
        lines.append(f'@define-color {padded_name} {value};')

    lines.append('')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# Rofi generation
# ---------------------------------------------------------------------------

def generate_rofi(tokens, output_path):
    """Generate the Rofi RASI token stylesheet."""
    lines = []
    lines.append('/* AUTO-GENERATED by tools/build_tokens.py')
    lines.append(f'   Source: core/tokens/{tokens["name"].lower().replace(" ", "_")}.json')
    lines.append('   DO NOT EDIT — modify the token source and re-run the compiler. */')
    lines.append('')
    lines.append('* {')

    palette = tokens['palette']
    geometry = tokens.get('geometry', {})

    all_keys = [name for _, name in CSS_TOKEN_MAP] + ['rounding', 'border-width', 'gaps-in', 'gaps-out']
    max_name_len = max(len(k) for k in all_keys) + 1

    for json_key, rofi_name in CSS_TOKEN_MAP:
        if json_key not in palette:
            continue
        value = _color_to_css(palette[json_key])
        padded_name = f'{rofi_name}:'.ljust(max_name_len + 1)
        lines.append(f'    {padded_name} {value};')

    lines.append('')
    if 'rounding' in geometry:
        padded = 'rounding:'.ljust(max_name_len + 1)
        lines.append(f'    {padded} {geometry["rounding"]}px;')
    if 'border_size' in geometry:
        padded = 'border-width:'.ljust(max_name_len + 1)
        lines.append(f'    {padded} {geometry["border_size"]}px;')
    if 'gaps_in' in geometry:
        padded = 'gaps-in:'.ljust(max_name_len + 1)
        lines.append(f'    {padded} {geometry["gaps_in"]}px;')
    if 'gaps_out' in geometry:
        padded = 'gaps-out:'.ljust(max_name_len + 1)
        lines.append(f'    {padded} {geometry["gaps_out"]}px;')

    lines.append('}')
    lines.append('')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# Hyprland / Hyprlock conf generation
# ---------------------------------------------------------------------------

def generate_hypr_conf(tokens, output_path):
    """Generate the Hyprland / Hyprlock conf token file."""
    lines = []
    token_slug = tokens["name"].lower().replace(" ", "_")
    lines.append('################################################################################')
    lines.append('# AUTO-GENERATED by tools/build_tokens.py')
    lines.append(f'# Source: core/tokens/{token_slug}.json')
    lines.append('# DO NOT EDIT — modify the token source and re-run the compiler.')
    lines.append('################################################################################')
    lines.append('')

    palette = tokens['palette']
    geometry = tokens.get('geometry', {})
    blur = tokens.get('blur', {})

    # Palette
    lines.append('# Palette')
    max_key_len = max(len(f'${conf_name}') for _, conf_name in HYPR_CONF_TOKEN_MAP)

    for json_key, conf_name in HYPR_CONF_TOKEN_MAP:
        if json_key not in palette:
            continue
        entry = palette[json_key]
        if isinstance(entry, str):
            hex_clean = entry.lstrip('#')
            val = f'rgb({hex_clean})'
        else:
            hex_clean = entry['hex'].lstrip('#')
            alpha_hex = _alpha_to_hex_byte(entry['alpha']).lower()
            val = f'rgba({hex_clean}{alpha_hex})'
        var_name = f'${conf_name}'.ljust(max_key_len)
        lines.append(f'{var_name} = {val}')

    # Aliases for compatibility
    lines.append('')
    lines.append('# Semantic aliases')
    lines.append('$void                  = $noctis_void')
    lines.append('$surface               = $noctis_surface')
    lines.append('$surface_raised        = $noctis_surface_raised')
    lines.append('$surface_focus         = $noctis_surface_focus')
    lines.append('$accent                = $amethyst')
    lines.append('$accent_ink            = $amethyst_ink')

    lines.append('')
    lines.append('# Geometry')
    if 'rounding' in geometry:
        lines.append(f'$rounding = {geometry["rounding"]}')
    if 'border_size' in geometry:
        lines.append(f'$border_size = {geometry["border_size"]}')
    if 'gaps_in' in geometry:
        lines.append(f'$gaps_in = {geometry["gaps_in"]}')
    if 'gaps_out' in geometry:
        lines.append(f'$gaps_out = {geometry["gaps_out"]}')

    lines.append('')
    lines.append('# Blur')
    if 'passes' in blur:
        lines.append(f'$blur_passes = {blur["passes"]}')
    if 'size' in blur:
        lines.append(f'$blur_size = {blur["size"]}')

    lines.append('')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# Kitty conf generation
# ---------------------------------------------------------------------------

def generate_kitty_conf(tokens, output_path):
    """Generate the Kitty terminal color theme configuration."""
    lines = []
    token_slug = tokens["name"].lower().replace(" ", "_")
    lines.append('################################################################################')
    lines.append('# AUTO-GENERATED by tools/build_tokens.py')
    lines.append(f'# Source: core/tokens/{token_slug}.json')
    lines.append('# DO NOT EDIT — modify the token source and re-run the compiler.')
    lines.append('################################################################################')
    lines.append('')

    palette = tokens['palette']

    def _hex(key, fallback='#000000'):
        entry = palette.get(key, fallback)
        if isinstance(entry, dict):
            return entry['hex']
        return entry

    # Special colors
    lines.append('# Special colors')
    lines.append(f'background            {_hex("void")}')
    lines.append(f'foreground            {_hex("accent_ink")}')
    lines.append(f'selection_background  {_hex("accent")}')
    lines.append(f'selection_foreground  {_hex("void")}')
    lines.append(f'cursor                {_hex("accent_ink")}')
    lines.append(f'cursor_text_color     {_hex("void")}')
    lines.append(f'url_color             {_hex("accent")}')
    lines.append('')
    lines.append('# Kitty window borders')
    lines.append(f'active_border_color   {_hex("accent")}')
    lines.append(f'inactive_border_color {_hex("border_inactive")}')
    lines.append(f'bell_border_color     {_hex("warning")}')
    lines.append('')
    lines.append('# Tab bar colors')
    lines.append(f'active_tab_foreground   {_hex("void")}')
    lines.append(f'active_tab_background   {_hex("accent")}')
    lines.append(f'inactive_tab_foreground {_hex("accent_ink")}')
    lines.append(f'inactive_tab_background {_hex("surface")}')
    lines.append('')
    lines.append('# 16 terminal colors')
    lines.append('# Black')
    lines.append(f'color0  {_hex("surface")}')
    lines.append(f'color8  {_hex("surface_focus")}')
    lines.append('')
    lines.append('# Red')
    lines.append(f'color1  {_hex("danger")}')
    lines.append(f'color9  {_hex("danger")}')
    lines.append('')
    lines.append('# Green')
    lines.append(f'color2  {_hex("accent_gradient_start")}')
    lines.append(f'color10 {_hex("accent_gradient_end")}')
    lines.append('')
    lines.append('# Yellow')
    lines.append(f'color3  {_hex("warning")}')
    lines.append(f'color11 {_hex("warning")}')
    lines.append('')
    lines.append('# Blue')
    lines.append(f'color4  {_hex("accent_gradient_start")}')
    lines.append(f'color12 {_hex("accent")}')
    lines.append('')
    lines.append('# Magenta')
    lines.append(f'color5  {_hex("accent_gradient_end")}')
    lines.append(f'color13 {_hex("accent_ink")}')
    lines.append('')
    lines.append('# Cyan')
    lines.append(f'color6  {_hex("accent")}')
    lines.append(f'color14 {_hex("accent_ink")}')
    lines.append('')
    lines.append('# White')
    lines.append(f'color7  {_hex("accent_ink")}')
    lines.append(f'color15 {_hex("ink_strong", "#ffffff")}')
    lines.append('')

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', newline='\n') as f:
        f.write('\n'.join(lines))


# ---------------------------------------------------------------------------
# Inheritance
# ---------------------------------------------------------------------------

def deep_merge(target, source):
    """Deep merge source dict into target dict."""
    for key, value in source.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            deep_merge(target[key], value)
        else:
            if key not in target:
                target[key] = value
    return target

def resolve_inheritance(tokens, token_file_path, visited=None):
    """Resolve theme inheritance if the 'extends' key is present."""
    if visited is None:
        visited = set()

    real_path = os.path.realpath(token_file_path)
    if real_path in visited:
        raise TokenError(f"Circular inheritance detected: {real_path}")
    visited.add(real_path)

    if 'extends' not in tokens:
        return tokens

    parent_file = tokens['extends']
    parent_path = os.path.join(os.path.dirname(token_file_path), parent_file)

    try:
        with open(parent_path, 'r') as f:
            parent_tokens = json.load(f)
    except FileNotFoundError:
        raise TokenError(f"Parent theme not found: {parent_path}")
    except json.JSONDecodeError as e:
        raise TokenError(f"Malformed JSON in parent theme {parent_path}: {e}")

    # Recursively resolve parent inheritance
    parent_tokens = resolve_inheritance(parent_tokens, parent_path, visited)

    # Merge parent into child (child overrides parent)
    merged_tokens = deep_merge(tokens, parent_tokens)
    return merged_tokens


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Obsyx Theme Token Compiler',
    )
    parser.add_argument(
        '--tokens',
        default='core/tokens/noctis_amethyst.json',
        help='Path to the canonical token JSON source',
    )
    parser.add_argument(
        '--lua-out',
        default='hypr/themes/noctis_amethyst.lua',
        help='Path for the generated Lua theme table',
    )
    parser.add_argument(
        '--css-out',
        default='waybar/generated/theme-tokens.css',
        help='Path for the generated CSS token stylesheet',
    )
    parser.add_argument(
        '--rofi-out',
        default='rofi/generated/theme-tokens.rasi',
        help='Path for the generated Rofi token stylesheet',
    )
    parser.add_argument(
        '--swaync-out',
        default='swaync/generated/theme-tokens.css',
        help='Path for the generated SwayNC CSS token stylesheet',
    )
    parser.add_argument(
        '--hypr-conf-out',
        default='hypr/generated/theme-tokens.conf',
        help='Path for the generated Hyprland/Hyprlock conf tokens',
    )
    parser.add_argument(
        '--kitty-out',
        default='kitty/generated/theme-tokens.conf',
        help='Path for the generated Kitty terminal tokens',
    )
    parser.add_argument(
        '--wlogout-out',
        default='wlogout/generated/theme-tokens.css',
        help='Path for the generated Wlogout CSS token stylesheet',
    )
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check whether generated artifacts match current files without modifying them',
    )
    args = parser.parse_args()

    # Load.
    try:
        with open(args.tokens, 'r') as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print(f'error: token source not found: {args.tokens}', file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f'error: malformed JSON in {args.tokens}: {e}', file=sys.stderr)
        sys.exit(1)

    # Resolve Inheritance.
    try:
        tokens = resolve_inheritance(tokens, args.tokens)
    except TokenError as e:
        print(f'error: theme inheritance failed: {e}', file=sys.stderr)
        sys.exit(1)

    # Validate.
    try:
        validate_tokens(tokens)
    except TokenError as e:
        print(f'error: token validation failed: {e}', file=sys.stderr)
        sys.exit(1)

    if args.check:
        with tempfile.TemporaryDirectory() as tmpdir:
            targets = [
                (args.lua_out, generate_lua),
                (args.css_out, generate_css),
                (args.rofi_out, generate_rofi),
                (args.swaync_out, generate_css),
                (args.hypr_conf_out, generate_hypr_conf),
                (args.kitty_out, generate_kitty_conf),
                (args.wlogout_out, generate_css),
            ]
            mismatches = []
            for target_path, gen_func in targets:
                tmp_target = os.path.join(tmpdir, os.path.basename(target_path))
                gen_func(tokens, tmp_target)
                if not os.path.isfile(target_path):
                    mismatches.append(f"{target_path} (missing)")
                    continue
                with open(tmp_target, "r", encoding="utf-8") as f1, open(target_path, "r", encoding="utf-8") as f2:
                    if f1.read() != f2.read():
                        mismatches.append(f"{target_path} (outdated content mismatch)")

            if mismatches:
                print(f"Error: {len(mismatches)} token artifact(s) are outdated or missing:", file=sys.stderr)
                for m in mismatches:
                    print(f"  - {m}", file=sys.stderr)
                print("Run 'python3 tools/build_tokens.py' to regenerate compiled tokens.", file=sys.stderr)
                sys.exit(1)

            print("All token artifacts are up to date.")
            sys.exit(0)

    # Generate.
    generate_lua(tokens, args.lua_out)
    generate_css(tokens, args.css_out)
    generate_rofi(tokens, args.rofi_out)
    generate_css(tokens, args.swaync_out)
    generate_hypr_conf(tokens, args.hypr_conf_out)
    generate_kitty_conf(tokens, args.kitty_out)
    generate_css(tokens, args.wlogout_out)

    print(f'Generated: {args.lua_out}')
    print(f'Generated: {args.css_out}')
    print(f'Generated: {args.rofi_out}')
    print(f'Generated: {args.swaync_out}')
    print(f'Generated: {args.hypr_conf_out}')
    print(f'Generated: {args.kitty_out}')
    print(f'Generated: {args.wlogout_out}')


if __name__ == '__main__':
    main()
