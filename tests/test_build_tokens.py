"""Tests for the Obsyx theme token compiler."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

# Allow importing the compiler from the tools directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, 'tools'))

import build_tokens


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VALID_TOKENS_PATH = os.path.join(REPO_ROOT, 'core', 'tokens', 'noctis_amethyst.json')


def _load_valid_tokens():
    """Load the canonical token source."""
    with open(VALID_TOKENS_PATH, 'r') as f:
        return json.load(f)


def _run_compiler(*extra_args):
    """Run the compiler as a subprocess, returning (returncode, stdout, stderr)."""
    cmd = [sys.executable, os.path.join(REPO_ROOT, 'tools', 'build_tokens.py')]
    cmd.extend(extra_args)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.returncode, result.stdout, result.stderr


class _TempDirMixin:
    """Mixin providing a temporary directory for generated output."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix='obsyx_test_')

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    @property
    def lua_out(self):
        return os.path.join(self.tmpdir, 'theme.lua')

    @property
    def css_out(self):
        return os.path.join(self.tmpdir, 'theme.css')

    @property
    def rofi_out(self):
        return os.path.join(self.tmpdir, 'theme-tokens.rasi')

    @property
    def swaync_out(self):
        return os.path.join(self.tmpdir, 'swaync-tokens.css')

    @property
    def hypr_conf_out(self):
        return os.path.join(self.tmpdir, 'theme-tokens.conf')


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

class TestValidation(unittest.TestCase):
    """Tests for token validation logic."""

    def test_valid_tokens_pass_validation(self):
        tokens = _load_valid_tokens()
        # Should not raise.
        build_tokens.validate_tokens(tokens)

    def test_missing_name(self):
        tokens = _load_valid_tokens()
        del tokens['name']
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('name', str(ctx.exception))

    def test_missing_palette(self):
        tokens = _load_valid_tokens()
        del tokens['palette']
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('palette', str(ctx.exception))

    def test_missing_geometry(self):
        tokens = _load_valid_tokens()
        del tokens['geometry']
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('geometry', str(ctx.exception))

    def test_missing_blur(self):
        tokens = _load_valid_tokens()
        del tokens['blur']
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('blur', str(ctx.exception))

    def test_invalid_hex_color(self):
        tokens = _load_valid_tokens()
        tokens['palette']['void'] = '#ZZZZZZ'
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('invalid hex color', str(ctx.exception))

    def test_invalid_hex_too_short(self):
        tokens = _load_valid_tokens()
        tokens['palette']['void'] = '#fff'
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('invalid hex color', str(ctx.exception))

    def test_alpha_out_of_range_high(self):
        tokens = _load_valid_tokens()
        tokens['palette']['surface'] = {'hex': '#16131d', 'alpha': 1.5}
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('out of range', str(ctx.exception))

    def test_alpha_out_of_range_negative(self):
        tokens = _load_valid_tokens()
        tokens['palette']['surface'] = {'hex': '#16131d', 'alpha': -0.1}
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('out of range', str(ctx.exception))

    def test_color_object_missing_hex(self):
        tokens = _load_valid_tokens()
        tokens['palette']['surface'] = {'alpha': 0.88}
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('missing "hex"', str(ctx.exception))

    def test_color_object_missing_alpha(self):
        tokens = _load_valid_tokens()
        tokens['palette']['surface'] = {'hex': '#16131d'}
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('missing "alpha"', str(ctx.exception))

    def test_negative_geometry_value(self):
        tokens = _load_valid_tokens()
        tokens['geometry']['gaps_in'] = -1
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('non-negative', str(ctx.exception))

    def test_invalid_opacity_value(self):
        tokens = _load_valid_tokens()
        tokens['opacity']['active'] = 2.0
        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.validate_tokens(tokens)
        self.assertIn('out of range', str(ctx.exception))


# ---------------------------------------------------------------------------
# Generation tests
# ---------------------------------------------------------------------------

class TestLuaGeneration(_TempDirMixin, unittest.TestCase):
    """Tests for Lua output generation."""

    def test_lua_output_contains_expected_values(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_lua(tokens, self.lua_out)
        with open(self.lua_out, 'r') as f:
            content = f.read()

        # Header.
        self.assertIn('AUTO-GENERATED', content)
        self.assertIn('DO NOT EDIT', content)

        # Theme metadata.
        self.assertIn('Theme.name = "Noctis Amethyst"', content)

        # Key palette values that must match existing decoration.lua.
        self.assertIn('rgba(8A63D2EE)', content)   # accent gradient start
        self.assertIn('rgba(C7A6FFEE)', content)   # accent gradient end
        self.assertIn('rgba(26232DCC)', content)    # border inactive
        self.assertIn('rgba(00000088)', content)    # shadow color
        self.assertIn('"#121018"', content)          # void
        self.assertIn('"#9b7ede"', content)          # accent

        # Geometry.
        self.assertIn('gaps_in', content)
        self.assertIn('rounding', content)

        # Structure.
        self.assertIn('return Theme', content)

    def test_lua_syntax_valid(self):
        """Verify generated Lua passes luac syntax check."""
        tokens = _load_valid_tokens()
        build_tokens.generate_lua(tokens, self.lua_out)

        luac = shutil.which('luac')
        if luac is None:
            self.skipTest('luac not available')

        result = subprocess.run(
            [luac, '-p', self.lua_out],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0,
                         f'luac -p failed:\n{result.stderr}')


class TestCssGeneration(_TempDirMixin, unittest.TestCase):
    """Tests for CSS output generation."""

    def test_css_output_contains_expected_values(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_css(tokens, self.css_out)
        with open(self.css_out, 'r') as f:
            content = f.read()

        # Header.
        self.assertIn('AUTO-GENERATED', content)

        # Spot-check token names and values matching existing theme.css.
        self.assertIn('@define-color noctis-void', content)
        self.assertIn('#121018', content)
        self.assertIn('@define-color noctis-surface', content)
        self.assertIn('rgba(22, 19, 29, 0.88)', content)
        self.assertIn('@define-color amethyst', content)
        self.assertIn('#9b7ede', content)
        self.assertIn('@define-color amethyst-ink', content)
        self.assertIn('#dacbff', content)
        self.assertIn('@define-color warning', content)
        self.assertIn('#d8bb82', content)
        self.assertIn('@define-color danger', content)
        self.assertIn('#d28a95', content)
        self.assertIn('@define-color danger-wash', content)
        self.assertIn('rgba(210, 138, 149, 0.16)', content)

    def test_css_does_not_contain_hyprland_only_tokens(self):
        """Gradient endpoints and border_inactive are Hyprland-only."""
        tokens = _load_valid_tokens()
        build_tokens.generate_css(tokens, self.css_out)
        with open(self.css_out, 'r') as f:
            content = f.read()

        self.assertNotIn('gradient', content)
        self.assertNotIn('border_inactive', content)
        self.assertNotIn('border-inactive', content)


# ---------------------------------------------------------------------------
# Rofi generation tests
# ---------------------------------------------------------------------------

class TestRofiGeneration(_TempDirMixin, unittest.TestCase):
    """Tests for Rofi theme token generation."""

    def test_rofi_file_created(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_rofi(tokens, self.rofi_out)
        self.assertTrue(os.path.isfile(self.rofi_out))

    def test_rofi_header(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_rofi(tokens, self.rofi_out)
        with open(self.rofi_out, 'r') as f:
            content = f.read()
        self.assertIn('AUTO-GENERATED by tools/build_tokens.py', content)
        self.assertIn('noctis_amethyst.json', content)

    def test_rofi_contains_root_block(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_rofi(tokens, self.rofi_out)
        with open(self.rofi_out, 'r') as f:
            content = f.read()
        self.assertIn('* {', content)

    def test_rofi_contains_color_tokens(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_rofi(tokens, self.rofi_out)
        with open(self.rofi_out, 'r') as f:
            content = f.read()
        self.assertIn('noctis-void:', content)
        self.assertIn('#121018', content)
        self.assertIn('amethyst:', content)
        self.assertIn('#9b7ede', content)
        self.assertIn('ink-strong:', content)
        self.assertIn('#dacbff', content)
        self.assertIn('noctis-surface-raised:', content)
        self.assertIn('rgba(25, 22, 35, 0.94)', content)

    def test_rofi_contains_geometry_tokens(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_rofi(tokens, self.rofi_out)
        with open(self.rofi_out, 'r') as f:
            content = f.read()
        self.assertIn('rounding:', content)
        self.assertIn('8px;', content)
        self.assertIn('border-width:', content)
        self.assertIn('2px;', content)

    def test_rofi_dump_theme_validates(self):
        """Verify the generated RASI file passes rofi syntax validation."""
        tokens = _load_valid_tokens()
        build_tokens.generate_rofi(tokens, self.rofi_out)
        res = subprocess.run(
            ['rofi', '-no-config', '-theme', self.rofi_out, '-dump-theme'],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f'rofi failed:\n{res.stderr}')


# ---------------------------------------------------------------------------
# Hyprland / Hyprlock conf generation tests
# ---------------------------------------------------------------------------

class TestHyprConfGeneration(_TempDirMixin, unittest.TestCase):
    """Tests for Hyprland / Hyprlock conf token generation."""

    def test_conf_file_created(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_hypr_conf(tokens, self.hypr_conf_out)
        self.assertTrue(os.path.isfile(self.hypr_conf_out))

    def test_conf_header(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_hypr_conf(tokens, self.hypr_conf_out)
        with open(self.hypr_conf_out, 'r') as f:
            content = f.read()
        self.assertIn('AUTO-GENERATED by tools/build_tokens.py', content)
        self.assertIn('noctis_amethyst.json', content)

    def test_conf_contains_palette_variables(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_hypr_conf(tokens, self.hypr_conf_out)
        with open(self.hypr_conf_out, 'r') as f:
            content = f.read()
        self.assertIn('$noctis_void', content)
        self.assertIn('rgb(121018)', content)
        self.assertIn('$amethyst', content)
        self.assertIn('rgb(9b7ede)', content)
        self.assertIn('$amethyst_ink', content)
        self.assertIn('rgb(dacbff)', content)
        self.assertIn('$noctis_surface_raised', content)
        self.assertIn('rgba(191623f0)', content)

    def test_conf_contains_geometry_and_blur_variables(self):
        tokens = _load_valid_tokens()
        build_tokens.generate_hypr_conf(tokens, self.hypr_conf_out)
        with open(self.hypr_conf_out, 'r') as f:
            content = f.read()
        self.assertIn('$rounding = 8', content)
        self.assertIn('$border_size = 2', content)
        self.assertIn('$blur_passes = 3', content)
        self.assertIn('$blur_size = 13', content)


# ---------------------------------------------------------------------------
# Determinism test
# ---------------------------------------------------------------------------

class TestDeterminism(_TempDirMixin, unittest.TestCase):
    """Verify the compiler produces byte-identical output on repeated runs."""

    def test_deterministic_output(self):
        tokens = _load_valid_tokens()

        # First run.
        lua_out_1 = os.path.join(self.tmpdir, 'run1.lua')
        css_out_1 = os.path.join(self.tmpdir, 'run1.css')
        rofi_out_1 = os.path.join(self.tmpdir, 'run1.rasi')
        swaync_out_1 = os.path.join(self.tmpdir, 'run1-swaync.css')
        hypr_conf_out_1 = os.path.join(self.tmpdir, 'run1.conf')

        build_tokens.generate_lua(tokens, lua_out_1)
        build_tokens.generate_css(tokens, css_out_1)
        build_tokens.generate_rofi(tokens, rofi_out_1)
        build_tokens.generate_css(tokens, swaync_out_1)
        build_tokens.generate_hypr_conf(tokens, hypr_conf_out_1)

        with open(lua_out_1, 'rb') as f:
            lua_bytes_1 = f.read()
        with open(css_out_1, 'rb') as f:
            css_bytes_1 = f.read()
        with open(rofi_out_1, 'rb') as f:
            rofi_bytes_1 = f.read()
        with open(swaync_out_1, 'rb') as f:
            swaync_bytes_1 = f.read()
        with open(hypr_conf_out_1, 'rb') as f:
            hypr_conf_bytes_1 = f.read()

        # Second run.
        lua_out_2 = os.path.join(self.tmpdir, 'run2.lua')
        css_out_2 = os.path.join(self.tmpdir, 'run2.css')
        rofi_out_2 = os.path.join(self.tmpdir, 'run2.rasi')
        swaync_out_2 = os.path.join(self.tmpdir, 'run2-swaync.css')
        hypr_conf_out_2 = os.path.join(self.tmpdir, 'run2.conf')

        build_tokens.generate_lua(tokens, lua_out_2)
        build_tokens.generate_css(tokens, css_out_2)
        build_tokens.generate_rofi(tokens, rofi_out_2)
        build_tokens.generate_css(tokens, swaync_out_2)
        build_tokens.generate_hypr_conf(tokens, hypr_conf_out_2)

        with open(lua_out_2, 'rb') as f:
            lua_bytes_2 = f.read()
        with open(css_out_2, 'rb') as f:
            css_bytes_2 = f.read()
        with open(rofi_out_2, 'rb') as f:
            rofi_bytes_2 = f.read()
        with open(swaync_out_2, 'rb') as f:
            swaync_bytes_2 = f.read()
        with open(hypr_conf_out_2, 'rb') as f:
            hypr_conf_bytes_2 = f.read()

        self.assertEqual(lua_bytes_1, lua_bytes_2,
                         'Lua output is not deterministic')
        self.assertEqual(css_bytes_1, css_bytes_2,
                         'CSS output is not deterministic')
        self.assertEqual(rofi_bytes_1, rofi_bytes_2,
                         'Rofi output is not deterministic')
        self.assertEqual(swaync_bytes_1, swaync_bytes_2,
                         'SwayNC output is not deterministic')
        self.assertEqual(hypr_conf_bytes_1, hypr_conf_bytes_2,
                         'Hypr conf output is not deterministic')


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

class TestCLI(_TempDirMixin, unittest.TestCase):
    """Tests for the compiler CLI interface."""

    def test_cli_success(self):
        rc, stdout, stderr = _run_compiler(
            '--tokens', VALID_TOKENS_PATH,
            '--lua-out', self.lua_out,
            '--css-out', self.css_out,
            '--rofi-out', self.rofi_out,
            '--swaync-out', self.swaync_out,
            '--hypr-conf-out', self.hypr_conf_out,
        )
        self.assertEqual(rc, 0, f'Compiler failed:\n{stderr}')
        self.assertTrue(os.path.isfile(self.lua_out))
        self.assertTrue(os.path.isfile(self.css_out))
        self.assertTrue(os.path.isfile(self.rofi_out))
        self.assertTrue(os.path.isfile(self.swaync_out))
        self.assertTrue(os.path.isfile(self.hypr_conf_out))

    def test_cli_missing_token_file(self):
        rc, stdout, stderr = _run_compiler(
            '--tokens', '/nonexistent/tokens.json',
            '--lua-out', self.lua_out,
            '--css-out', self.css_out,
        )
        self.assertNotEqual(rc, 0)
        self.assertIn('not found', stderr)

    def test_cli_malformed_json(self):
        bad_json = os.path.join(self.tmpdir, 'bad.json')
        with open(bad_json, 'w') as f:
            f.write('{invalid json')
        rc, stdout, stderr = _run_compiler(
            '--tokens', bad_json,
            '--lua-out', self.lua_out,
            '--css-out', self.css_out,
        )
        self.assertNotEqual(rc, 0)
        self.assertIn('malformed JSON', stderr)

    def test_cli_invalid_tokens(self):
        bad_tokens = os.path.join(self.tmpdir, 'bad_tokens.json')
        with open(bad_tokens, 'w') as f:
            json.dump({'name': 'Test'}, f)  # Missing palette, geometry, blur.
        rc, stdout, stderr = _run_compiler(
            '--tokens', bad_tokens,
            '--lua-out', self.lua_out,
            '--css-out', self.css_out,
        )
        self.assertNotEqual(rc, 0)
        self.assertIn('validation failed', stderr)


# ---------------------------------------------------------------------------
# Color conversion unit tests
# ---------------------------------------------------------------------------

class TestColorConversion(unittest.TestCase):
    """Unit tests for color format conversion functions."""

    def test_hex_to_hypr_opaque(self):
        self.assertEqual(build_tokens._color_to_hypr('#121018'), '#121018')

    def test_hex_to_hypr_with_alpha(self):
        entry = {'hex': '#8a63d2', 'alpha': 0.933}
        result = build_tokens._color_to_hypr(entry)
        self.assertEqual(result, 'rgba(8A63D2EE)')

    def test_hex_to_hypr_border_inactive(self):
        entry = {'hex': '#26232d', 'alpha': 0.80}
        result = build_tokens._color_to_hypr(entry)
        self.assertEqual(result, 'rgba(26232DCC)')

    def test_hex_to_hypr_shadow(self):
        entry = {'hex': '#000000', 'alpha': 0.533}
        result = build_tokens._color_to_hypr(entry)
        self.assertEqual(result, 'rgba(00000088)')

    def test_hex_to_css_opaque(self):
        self.assertEqual(build_tokens._color_to_css('#9b7ede'), '#9b7ede')

    def test_hex_to_css_with_alpha(self):
        entry = {'hex': '#16131d', 'alpha': 0.88}
        result = build_tokens._color_to_css(entry)
        self.assertEqual(result, 'rgba(22, 19, 29, 0.88)')

    def test_hex_to_css_white_alpha(self):
        entry = {'hex': '#ffffff', 'alpha': 0.92}
        result = build_tokens._color_to_css(entry)
        self.assertEqual(result, 'rgba(255, 255, 255, 0.92)')

    def test_hex_to_css_danger_wash(self):
        entry = {'hex': '#d28a95', 'alpha': 0.16}
        result = build_tokens._color_to_css(entry)
        self.assertEqual(result, 'rgba(210, 138, 149, 0.16)')


if __name__ == '__main__':
    unittest.main()
