"""Tests for the Obsyx Hyprland theme loader and decoration wiring."""

import os
import shutil
import subprocess
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_lua(script):
    """Execute a Lua script snippet with the repo's hypr directory in package.path.

    Returns (returncode, stdout, stderr).
    """
    cmd = [
        'lua',
        '-e',
        f'package.path = "{REPO_ROOT}/hypr/?.lua;{REPO_ROOT}/hypr/?/init.lua;" .. package.path\n'
        + script,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.returncode, result.stdout, result.stderr


class TestThemeLoader(unittest.TestCase):
    """Tests for hypr/config/theme.lua."""

    @classmethod
    def setUpClass(cls):
        if shutil.which('lua') is None:
            raise unittest.SkipTest('lua interpreter not available')

    def test_default_theme_loaded(self):
        """Theme loader loads Noctis Amethyst based on Registry.Theme.name."""
        rc, stdout, stderr = _run_lua("""
            require("config.variables")
            local theme = require("config.theme")
            assert(theme ~= nil, "theme is nil")
            assert(theme.name == "Noctis Amethyst", "wrong theme name: " .. tostring(theme.name))
            assert(Theme == theme, "global Theme not set")
            assert(Registry.Theme.current == theme, "Registry.Theme.current not set")
            assert(Registry.Theme.slug == "noctis_amethyst", "slug incorrect")
            assert(theme.palette.accent == "#9b7ede", "accent color mismatch")
            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)

    def test_missing_theme_error_handling(self):
        """Requesting a nonexistent theme raises a descriptive error."""
        rc, stdout, stderr = _run_lua("""
            require("config.variables")
            Registry.Theme.name = "Nonexistent Theme 99"
            local ok, err = pcall(require, "config.theme")
            assert(not ok, "should have failed for nonexistent theme")
            assert(string.find(tostring(err), "failed to load theme"), "error message should mention failure")
            assert(string.find(tostring(err), "nonexistent_theme_99"), "error message should mention slug")
            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)

    def test_theme_table_structure_validation(self):
        """Theme loader validates that required sections exist."""
        rc, stdout, stderr = _run_lua("""
            package.loaded["themes.broken_theme"] = { name = "Broken" } -- missing palette, geometry, blur
            require("config.variables")
            Registry.Theme.name = "Broken Theme"
            local ok, err = pcall(require, "config.theme")
            assert(not ok, "should have failed for missing sections")
            assert(string.find(tostring(err), "missing required table"), "error should mention missing table")
            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)


class TestDecorationWiring(unittest.TestCase):
    """Tests for dynamic decoration wiring in hypr/config/appearance/decoration.lua."""

    @classmethod
    def setUpClass(cls):
        if shutil.which('lua') is None:
            raise unittest.SkipTest('lua interpreter not available')

    def test_decoration_receives_theme_tokens(self):
        """decoration.lua passes exact theme tokens to hl.config."""
        rc, stdout, stderr = _run_lua("""
            local captured = nil
            hl = {
                config = function(tbl)
                    captured = tbl
                end
            }

            require("config.variables")
            require("config.theme")
            require("config.appearance.decoration")

            assert(captured ~= nil, "hl.config was not called")
            local g = captured.general
            local d = captured.decoration

            -- Geometry
            assert(g.gaps_in == 5, "gaps_in mismatch: " .. tostring(g.gaps_in))
            assert(g.gaps_out == 12, "gaps_out mismatch: " .. tostring(g.gaps_out))
            assert(g.border_size == 2, "border_size mismatch: " .. tostring(g.border_size))
            assert(d.rounding == 8, "rounding mismatch: " .. tostring(d.rounding))
            assert(d.rounding_power == 2.4, "rounding_power mismatch: " .. tostring(d.rounding_power))

            -- Borders
            assert(g.col.active_border.colors[1] == "rgba(8A63D2EE)", "active_border[1] mismatch")
            assert(g.col.active_border.colors[2] == "rgba(C7A6FFEE)", "active_border[2] mismatch")
            assert(g.col.active_border.angle == 45, "border angle mismatch")
            assert(g.col.inactive_border == "rgba(26232DCC)", "inactive_border mismatch")

            -- Opacity
            assert(d.active_opacity == 0.75, "active_opacity mismatch")
            assert(d.inactive_opacity == 0.64, "inactive_opacity mismatch")
            assert(d.fullscreen_opacity == 0.95, "fullscreen_opacity mismatch")

            -- Shadow
            assert(d.shadow.enabled == true, "shadow enabled mismatch")
            assert(d.shadow.range == 18, "shadow range mismatch")
            assert(d.shadow.render_power == 4, "shadow render_power mismatch")
            assert(d.shadow.color == "rgba(00000088)", "shadow color mismatch")

            -- Blur
            assert(d.blur.enabled == true, "blur enabled mismatch")
            assert(d.blur.size == 13, "blur size mismatch")
            assert(d.blur.passes == 3, "blur passes mismatch")
            assert(d.blur.vibrancy == 0.32, "blur vibrancy mismatch")
            assert(d.blur.contrast == 1.18, "blur contrast mismatch")
            assert(d.blur.brightness == 1.0, "blur brightness mismatch")

            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)

    def test_decoration_dynamic_adaptation(self):
        """Changing the active theme values reflects dynamically in decoration config."""
        rc, stdout, stderr = _run_lua("""
            local captured = nil
            hl = {
                config = function(tbl)
                    captured = tbl
                end
            }

            require("config.variables")
            local theme = require("config.theme")

            -- Mutate theme geometry and border colors to simulate custom/alternate theme
            theme.geometry.gaps_in = 16
            theme.geometry.rounding = 24
            theme.palette.accent_gradient_start = "rgba(FF0055EE)"

            -- Clear loaded module to re-evaluate decoration with updated theme
            package.loaded["config.appearance.decoration"] = nil
            require("config.appearance.decoration")

            assert(captured.general.gaps_in == 16, "custom gaps_in not reflected")
            assert(captured.decoration.rounding == 24, "custom rounding not reflected")
            assert(captured.general.col.active_border.colors[1] == "rgba(FF0055EE)", "custom border not reflected")

            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)


if __name__ == '__main__':
    unittest.main()
