"""Tests for Waybar design token integration and stylesheet consistency."""

import glob
import json
import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WAYBAR_DIR = os.path.join(REPO_ROOT, 'waybar')


def _strip_jsonc_comments(text):
    """Remove single-line (//) and multi-line (/* */) comments from JSONC text."""
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )

    def replacer(match):
        s = match.group(0)
        return ' ' if s.startswith('/') else s

    return re.sub(pattern, replacer, text)


class TestWaybarTokenIntegration(unittest.TestCase):
    """Verifies Waybar stylesheet import chain and design token coverage."""

    def test_style_css_imports_generated_tokens(self):
        """style.css imports generated/theme-tokens.css."""
        style_path = os.path.join(WAYBAR_DIR, 'style.css')
        with open(style_path, 'r') as f:
            content = f.read()
        self.assertIn('@import url("generated/theme-tokens.css");', content)

    def test_theme_css_forwards_to_generated_tokens(self):
        """theme.css forwards to generated/theme-tokens.css without duplicating definitions."""
        theme_path = os.path.join(WAYBAR_DIR, 'theme.css')
        with open(theme_path, 'r') as f:
            content = f.read()
        self.assertIn('@import url("generated/theme-tokens.css");', content)
        self.assertNotIn('@define-color noctis-void', content)

    def test_only_generated_stylesheet_defines_colors(self):
        """Only waybar/generated/theme-tokens.css defines @define-color rules."""
        css_files = glob.glob(os.path.join(WAYBAR_DIR, '**', '*.css'), recursive=True)
        generated_css = os.path.join(WAYBAR_DIR, 'generated', 'theme-tokens.css')

        for css_file in css_files:
            if os.path.abspath(css_file) == os.path.abspath(generated_css):
                continue
            with open(css_file, 'r') as f:
                content = f.read()
            self.assertNotIn('@define-color', content,
                             f'Unexpected @define-color in {os.path.relpath(css_file, REPO_ROOT)}')

    def test_all_used_tokens_are_defined(self):
        """Every @token referenced in waybar/styles/*.css exists in generated/theme-tokens.css."""
        generated_css = os.path.join(WAYBAR_DIR, 'generated', 'theme-tokens.css')
        defined_tokens = set()
        with open(generated_css, 'r') as f:
            for line in f:
                m = re.search(r'@define-color\s+([a-zA-Z0-9_-]+)', line)
                if m:
                    defined_tokens.add(m.group(1))

        self.assertTrue(len(defined_tokens) > 0, 'No tokens found in generated stylesheet')

        styles_dir = os.path.join(WAYBAR_DIR, 'styles')
        used_tokens = set()
        for css_file in glob.glob(os.path.join(styles_dir, '*.css')):
            with open(css_file, 'r') as f:
                for line in f:
                    for m in re.finditer(r'@([a-zA-Z0-9_-]+)', line):
                        token = m.group(1)
                        if token not in ('import', 'define-color'):
                            used_tokens.add(token)

        missing = used_tokens - defined_tokens
        self.assertEqual(missing, set(), f'Undefined tokens used in styles: {missing}')

    def test_no_hardcoded_hex_in_modules(self):
        """waybar/modules/*.jsonc files must not contain hardcoded hex colors."""
        modules_dir = os.path.join(WAYBAR_DIR, 'modules')
        hex_pattern = re.compile(r'#[0-9a-fA-F]{3,8}\b')

        for jsonc_file in glob.glob(os.path.join(modules_dir, '*.jsonc')):
            with open(jsonc_file, 'r') as f:
                content = f.read()
            matches = hex_pattern.findall(content)
            self.assertEqual(
                matches, [],
                f'Hardcoded hex color found in {os.path.relpath(jsonc_file, REPO_ROOT)}: {matches}',
            )

    def test_all_jsonc_files_are_valid(self):
        """All JSONC files in waybar/ must parse cleanly after stripping comments."""
        for jsonc_file in glob.glob(os.path.join(WAYBAR_DIR, '**', '*.jsonc'), recursive=True):
            with open(jsonc_file, 'r') as f:
                raw = f.read()
            clean = _strip_jsonc_comments(raw)
            try:
                data = json.loads(clean)
                self.assertIsInstance(data, dict, f'{jsonc_file} did not parse as a dict')
            except Exception as e:
                self.fail(f'Failed to parse JSONC in {os.path.relpath(jsonc_file, REPO_ROOT)}: {e}')


class TestWaybarModulePortability(unittest.TestCase):
    """Verifies that Waybar telemetry modules do not hardcode paths and support portable execution."""

    TELEMETRY_MODULES = [
        'cpu.jsonc',
        'gpu.jsonc',
        'media.jsonc',
        'memory.jsonc',
        'network.jsonc',
        'vpn.jsonc',
    ]

    def test_no_hardcoded_script_paths_in_modules(self):
        """waybar/modules/*.jsonc files must not hardcode ~/.config/waybar/scripts/."""
        modules_dir = os.path.join(WAYBAR_DIR, 'modules')
        hardcoded_re = re.compile(r'~/\.config/waybar/scripts/')

        for filename in self.TELEMETRY_MODULES:
            path = os.path.join(modules_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            matches = hardcoded_re.findall(content)
            self.assertEqual(
                matches, [],
                f'Hardcoded script path found in {filename}: {matches}',
            )

    def test_telemetry_modules_use_dynamic_resolution(self):
        """Telemetry modules must dynamically resolve scripts via WAYBAR_SCRIPTS_DIR and relative paths."""
        modules_dir = os.path.join(WAYBAR_DIR, 'modules')

        for filename in self.TELEMETRY_MODULES:
            path = os.path.join(modules_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertIn('WAYBAR_SCRIPTS_DIR', content, f'{filename} does not reference WAYBAR_SCRIPTS_DIR')
            self.assertIn('./scripts', content, f'{filename} does not check ./scripts')
            self.assertIn('./waybar/scripts', content, f'{filename} does not check ./waybar/scripts')

    def test_runner_script_exists_and_executable(self):
        """waybar/scripts/runner.sh must exist, be executable, pass syntax checks, and execute scripts."""
        runner_path = os.path.join(WAYBAR_DIR, 'scripts', 'runner.sh')
        self.assertTrue(os.path.isfile(runner_path), f'Missing: {runner_path}')
        self.assertTrue(os.access(runner_path, os.X_OK), f'{runner_path} is not executable')

        import subprocess
        rc = subprocess.run(['bash', '-n', runner_path], capture_output=True, text=True)
        self.assertEqual(rc.returncode, 0, f'Syntax error in runner.sh:\n{rc.stderr}')


if __name__ == '__main__':
    unittest.main()
