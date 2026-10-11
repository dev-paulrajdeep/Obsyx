"""Tests for Obsyx Kitty terminal configuration and design token integration."""

import os
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITTY_DIR = os.path.join(REPO_ROOT, 'kitty')
TOKEN_CONF_FILE = os.path.join(KITTY_DIR, 'generated', 'theme-tokens.conf')
KITTY_CONF_FILE = os.path.join(KITTY_DIR, 'kitty.conf')


class TestKittyFiles(unittest.TestCase):
    """Verify that required Kitty files exist."""

    def test_generated_tokens_exists(self):
        self.assertTrue(os.path.isfile(TOKEN_CONF_FILE), f'Missing: {TOKEN_CONF_FILE}')

    def test_kitty_conf_exists(self):
        self.assertTrue(os.path.isfile(KITTY_CONF_FILE), f'Missing: {KITTY_CONF_FILE}')


class TestKittyConfig(unittest.TestCase):
    """Verify kitty.conf configuration directives and token integration."""

    def test_includes_generated_tokens(self):
        self.assertTrue(os.path.isfile(KITTY_CONF_FILE), f'Missing: {KITTY_CONF_FILE}')
        with open(KITTY_CONF_FILE, 'r') as f:
            content = f.read()
        self.assertTrue(
            'include generated/theme-tokens.conf' in content or
            'include ./generated/theme-tokens.conf' in content or
            'include ~/.config/kitty/generated/theme-tokens.conf' in content,
            'kitty.conf does not include generated/theme-tokens.conf'
        )

    def test_font_configuration(self):
        self.assertTrue(os.path.isfile(KITTY_CONF_FILE), f'Missing: {KITTY_CONF_FILE}')
        with open(KITTY_CONF_FILE, 'r') as f:
            content = f.read()
        self.assertIn('font_family', content)
        self.assertIn('JetBrainsMono', content)

    def test_window_and_layout_directives(self):
        self.assertTrue(os.path.isfile(KITTY_CONF_FILE), f'Missing: {KITTY_CONF_FILE}')
        with open(KITTY_CONF_FILE, 'r') as f:
            content = f.read()
        self.assertIn('window_padding_width', content)


if __name__ == '__main__':
    unittest.main()
