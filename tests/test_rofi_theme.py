"""Tests for Obsyx Rofi configuration, theme stylesheets, and scripts."""

import os
import shutil
import stat
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROFI_DIR = os.path.join(REPO_ROOT, 'rofi')


class TestRofiFileStructure(unittest.TestCase):
    """Verify all required Rofi files exist with proper permissions."""

    def test_generated_tokens_exists(self):
        path = os.path.join(ROFI_DIR, 'generated', 'theme-tokens.rasi')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')

    def test_config_rasi_exists(self):
        path = os.path.join(ROFI_DIR, 'config.rasi')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')

    def test_theme_rasi_exists(self):
        path = os.path.join(ROFI_DIR, 'theme.rasi')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')

    def test_powermenu_rasi_exists(self):
        path = os.path.join(ROFI_DIR, 'powermenu.rasi')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')

    def test_clipboard_rasi_exists(self):
        path = os.path.join(ROFI_DIR, 'clipboard.rasi')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')

    def test_powermenu_script_exists_and_executable(self):
        path = os.path.join(ROFI_DIR, 'scripts', 'powermenu.sh')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')
        st = os.stat(path)
        self.assertTrue(bool(st.st_mode & stat.S_IXUSR), f'Not executable: {path}')

    def test_cliphist_script_exists_and_executable(self):
        path = os.path.join(ROFI_DIR, 'scripts', 'cliphist.sh')
        self.assertTrue(os.path.isfile(path), f'Missing: {path}')
        st = os.stat(path)
        self.assertTrue(bool(st.st_mode & stat.S_IXUSR), f'Not executable: {path}')


class TestRofiThemeSyntax(unittest.TestCase):
    """Verify all Rofi .rasi files pass syntax validation via rofi -dump-theme."""

    @classmethod
    def setUpClass(cls):
        cls.rofi = shutil.which('rofi')

    def _validate_rasi(self, rel_path):
        if not self.rofi:
            self.skipTest('rofi not installed')
        abs_path = os.path.join(ROFI_DIR, rel_path)
        self.assertTrue(os.path.isfile(abs_path), f'File not found: {abs_path}')
        res = subprocess.run(
            [self.rofi, '-no-config', '-theme', abs_path, '-dump-theme'],
            capture_output=True,
            text=True,
            cwd=ROFI_DIR,
        )
        if "Failed to open display" in res.stderr:
            self.skipTest("rofi needs X11/Wayland display to run syntax validation")
        self.assertEqual(res.returncode, 0, f'rofi syntax error in {rel_path}:\n{res.stderr}')

    def test_theme_tokens_syntax(self):
        self._validate_rasi(os.path.join('generated', 'theme-tokens.rasi'))

    def test_theme_rasi_syntax(self):
        self._validate_rasi('theme.rasi')

    def test_config_rasi_syntax(self):
        self._validate_rasi('config.rasi')

    def test_powermenu_rasi_syntax(self):
        self._validate_rasi('powermenu.rasi')

    def test_clipboard_rasi_syntax(self):
        self._validate_rasi('clipboard.rasi')


class TestRofiScriptsSyntax(unittest.TestCase):
    """Verify Rofi shell scripts pass bash -n syntax checks."""

    def _validate_shell_script(self, rel_path):
        abs_path = os.path.join(ROFI_DIR, rel_path)
        self.assertTrue(os.path.isfile(abs_path), f'File not found: {abs_path}')
        res = subprocess.run(
            ['bash', '-n', abs_path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f'Bash syntax error in {rel_path}:\n{res.stderr}')

    def test_powermenu_script_syntax(self):
        self._validate_shell_script(os.path.join('scripts', 'powermenu.sh'))

    def test_cliphist_script_syntax(self):
        self._validate_shell_script(os.path.join('scripts', 'cliphist.sh'))


class TestRofiTokenIntegration(unittest.TestCase):
    """Verify that Rofi files import and use canonical theme tokens."""

    def test_theme_imports_generated_tokens(self):
        theme_path = os.path.join(ROFI_DIR, 'theme.rasi')
        with open(theme_path, 'r') as f:
            content = f.read()
        self.assertIn('@import "generated/theme-tokens.rasi"', content)

    def test_theme_uses_amethyst_tokens(self):
        theme_path = os.path.join(ROFI_DIR, 'theme.rasi')
        with open(theme_path, 'r') as f:
            content = f.read()
        self.assertIn('@noctis-surface', content)
        self.assertIn('@hairline', content)
        self.assertIn('@amethyst', content)
        self.assertIn('@rounding', content)

    def test_powermenu_imports_or_uses_theme(self):
        pm_path = os.path.join(ROFI_DIR, 'powermenu.rasi')
        with open(pm_path, 'r') as f:
            content = f.read()
        self.assertTrue('@import' in content or '@theme' in content)

    def test_clipboard_imports_or_uses_theme(self):
        cb_path = os.path.join(ROFI_DIR, 'clipboard.rasi')
        with open(cb_path, 'r') as f:
            content = f.read()
        self.assertTrue('@import' in content or '@theme' in content)


class TestRofiRegistryWiring(unittest.TestCase):
    """Verify that variables.lua exposes Rofi desktop components."""

    def test_registry_contains_desktop_rofi_entries(self):
        var_path = os.path.join(REPO_ROOT, 'hypr', 'config', 'variables.lua')
        with open(var_path, 'r') as f:
            content = f.read()
        self.assertIn('Registry.Desktop', content)
        self.assertIn('clipboard', content)
        self.assertIn('powerMenu', content)
        self.assertIn('Registry.Session', content)


if __name__ == '__main__':
    unittest.main()
