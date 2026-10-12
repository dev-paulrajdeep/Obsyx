"""Tests for Obsyx Wlogout logout menu configuration and design token integration."""

import json
import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WLOGOUT_DIR = os.path.join(REPO_ROOT, 'wlogout')
TOKEN_FILE = os.path.join(WLOGOUT_DIR, 'generated', 'theme-tokens.css')
LAYOUT_FILE = os.path.join(WLOGOUT_DIR, 'layout')
STYLE_FILE = os.path.join(WLOGOUT_DIR, 'style.css')

DEFINE_COLOR_RE = re.compile(r'@define-color\s+([a-zA-Z0-9_-]+)\s+([^;]+);')
TOKEN_USAGE_RE = re.compile(r'@([a-zA-Z0-9_-]+)')
HEX_COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}\b')


def _extract_defined_wlogout_tokens():
    """Extract all token names defined in wlogout/generated/theme-tokens.css."""
    if not os.path.isfile(TOKEN_FILE):
        return set()
    with open(TOKEN_FILE, 'r') as f:
        content = f.read()
    return {m.group(1) for m in DEFINE_COLOR_RE.finditer(content)}


class TestWlogoutFiles(unittest.TestCase):
    """Verify that required Wlogout files exist."""

    def test_generated_tokens_exists(self):
        self.assertTrue(os.path.isfile(TOKEN_FILE), f'Missing: {TOKEN_FILE}')

    def test_layout_file_exists(self):
        self.assertTrue(os.path.isfile(LAYOUT_FILE), f'Missing: {LAYOUT_FILE}')

    def test_style_css_exists(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')


class TestWlogoutLayout(unittest.TestCase):
    """Verify wlogout layout file syntax and action entries."""

    def test_layout_contains_required_actions(self):
        self.assertTrue(os.path.isfile(LAYOUT_FILE), f'Missing: {LAYOUT_FILE}')
        with open(LAYOUT_FILE, 'r') as f:
            content = f.read()

        # Each entry in wlogout layout is a JSON object
        raw_objects = re.findall(r'\{[^{}]*\}', content)
        self.assertGreaterEqual(len(raw_objects), 4, 'Expected at least 4 action blocks in layout')

        labels = set()
        for obj_str in raw_objects:
            entry = json.loads(obj_str)
            self.assertIn('label', entry)
            self.assertIn('action', entry)
            self.assertIn('text', entry)
            labels.add(entry['label'])

        for expected in ('lock', 'logout', 'reboot', 'shutdown'):
            self.assertIn(expected, labels, f'Missing action {expected} in wlogout layout')


class TestWlogoutTokens(unittest.TestCase):
    """Verify wlogout style.css correctly integrates canonical design tokens."""

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
        cleaned = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        hexes = HEX_COLOR_RE.findall(cleaned)
        self.assertEqual(
            hexes, [],
            f'Hardcoded hex colors found in wlogout/style.css: {hexes}'
        )

    def test_all_used_tokens_are_defined(self):
        self.assertTrue(os.path.isfile(STYLE_FILE), f'Missing: {STYLE_FILE}')
        defined = _extract_defined_wlogout_tokens()
        self.assertTrue(bool(defined), 'No tokens defined in generated/theme-tokens.css')
        with open(STYLE_FILE, 'r') as f:
            content = f.read()
        cleaned = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        for match in TOKEN_USAGE_RE.finditer(cleaned):
            token_name = match.group(1)
            if token_name == 'import':
                continue
            self.assertIn(
                token_name, defined,
                f'Undefined token @{token_name} used in wlogout/style.css'
            )


if __name__ == '__main__':
    unittest.main()
