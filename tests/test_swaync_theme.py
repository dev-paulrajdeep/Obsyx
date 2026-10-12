"""Tests for Obsyx SwayNC notification daemon and control center styling."""

import json
import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAYNC_DIR = os.path.join(REPO_ROOT, 'swaync')
TOKEN_FILE = os.path.join(SWAYNC_DIR, 'generated', 'theme-tokens.css')
STYLE_FILE = os.path.join(SWAYNC_DIR, 'style.css')
CONFIG_FILE = os.path.join(SWAYNC_DIR, 'config.json')

DEFINE_COLOR_RE = re.compile(r'@define-color\s+([a-zA-Z0-9_-]+)\s+([^;]+);')
TOKEN_USAGE_RE = re.compile(r'@([a-zA-Z0-9_-]+)')
HEX_COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}\b')


def _extract_defined_tokens():
    """Extract all token names defined in swaync/generated/theme-tokens.css."""
    if not os.path.isfile(TOKEN_FILE):
        return set()
    with open(TOKEN_FILE, 'r') as f:
        content = f.read()
    return {m.group(1) for m in DEFINE_COLOR_RE.finditer(content)}


class TestSwayNCFiles(unittest.TestCase):
    """Verify that required SwayNC files exist."""

    def test_generated_tokens_exists(self):
        self.assertTrue(os.path.isfile(TOKEN_FILE), f'Missing: {TOKEN_FILE}')

    def test_config_json_exists(self):
        self.assertTrue(os.path.isfile(CONFIG_FILE), f'Missing: {CONFIG_FILE}')

    def test_style_css_exists(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')


class TestSwayNCConfig(unittest.TestCase):
    """Verify SwayNC config.json is valid and contains expected structure."""

    def test_config_is_valid_json(self):
        self.assertTrue(os.path.isfile(CONFIG_FILE), f'Missing: {CONFIG_FILE}')
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_config_structure(self):
        self.assertTrue(os.path.isfile(CONFIG_FILE), f'Missing: {CONFIG_FILE}')
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
        self.assertIn('positionX', data)
        self.assertIn('positionY', data)
        self.assertIn('control-center-width', data)
        self.assertIn('widgets', data)
        self.assertIn('widget-config', data)


class TestSwayNCTokens(unittest.TestCase):
    """Verify SwayNC style.css correctly integrates canonical design tokens."""

    def test_style_imports_generated_tokens(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')
        with open(STYLE_FILE, 'r') as f:
            content = f.read()
        self.assertTrue(
            '@import "generated/theme-tokens.css";' in content or
            "@import 'generated/theme-tokens.css';" in content or
            '@import url("generated/theme-tokens.css");' in content,
            'style.css does not import generated/theme-tokens.css'
        )

    def test_only_generated_stylesheet_defines_colors(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')
        with open(STYLE_FILE, 'r') as f:
            content = f.read()
        definitions = DEFINE_COLOR_RE.findall(content)
        self.assertEqual(
            definitions, [],
            f'style.css defines duplicate colors: {definitions}'
        )

    def test_no_hardcoded_hex_in_style(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')
        with open(STYLE_FILE, 'r') as f:
            content = f.read()
        # Comments stripped
        cleaned = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        hexes = HEX_COLOR_RE.findall(cleaned)
        self.assertEqual(
            hexes, [],
            f'Hardcoded hex colors found in swaync/style.css: {hexes}'
        )

    def test_all_used_tokens_are_defined(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')
        defined = _extract_defined_tokens()
        self.assertTrue(bool(defined), 'No tokens defined in generated/theme-tokens.css')
        with open(STYLE_FILE, 'r') as f:
            content = f.read()
        cleaned = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        for match in TOKEN_USAGE_RE.finditer(cleaned):
            token_name = match.group(1)
            # Skip @import
            if token_name == 'import':
                continue
            self.assertIn(
                token_name, defined,
                f'Undefined token @{token_name} used in swaync/style.css'
            )


if __name__ == '__main__':
    unittest.main()
