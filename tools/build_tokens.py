#!/usr/bin/env python3
"""Obsyx Theme Token Compiler.

Reads a canonical JSON token source and generates:
  - Hyprland-compatible Lua theme table
  - Waybar-compatible GTK3 CSS token stylesheet

Usage:
    python3 tools/build_tokens.py [OPTIONS]

Options:
    --tokens PATH    Token source (default: core/tokens/noctis_amethyst.json)
    --lua-out PATH   Lua output  (default: hypr/themes/noctis_amethyst.lua)
    --css-out PATH   CSS output  (default: waybar/generated/theme-tokens.css)
"""

import argparse
import json
import os
import re
import sys

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

    # Validate.
    try:
        validate_tokens(tokens)
    except TokenError as e:
        print(f'error: token validation failed: {e}', file=sys.stderr)
        sys.exit(1)

    # Generate.
    generate_lua(tokens, args.lua_out)
    generate_css(tokens, args.css_out)

    print(f'Generated: {args.lua_out}')
    print(f'Generated: {args.css_out}')


if __name__ == '__main__':
    main()
