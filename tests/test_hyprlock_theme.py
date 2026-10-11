"""Tests for Obsyx Hyprlock configuration and design token integration."""

import os
import re
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HYPR_DIR = os.path.join(REPO_ROOT, 'hypr')
CONF_FILE = os.path.join(HYPR_DIR, 'hyprlock.conf')
TOKEN_CONF_FILE = os.path.join(HYPR_DIR, 'generated', 'theme-tokens.conf')

VARIABLE_DEF_RE = re.compile(r'^\$([a-zA-Z0-9_-]+)\s*=', re.MULTILINE)
VARIABLE_USAGE_RE = re.compile(r'\$([a-zA-Z0-9_-]+)')
HEX_COLOR_RE = re.compile(r'#[0-9a-fA-F]{3,8}\b')


def _extract_defined_hypr_tokens():
    """Extract all variable names defined in hypr/generated/theme-tokens.conf."""
    if not os.path.isfile(TOKEN_CONF_FILE):
        return set()
    with open(TOKEN_CONF_FILE, 'r') as f:
        content = f.read()
    return {m.group(1) for m in VARIABLE_DEF_RE.finditer(content)}


class TestHyprlockFiles(unittest.TestCase):
    """Verify that Hyprlock configuration and token files exist."""

    def test_generated_tokens_exists(self):
        self.assertTrue(os.path.isfile(TOKEN_CONF_FILE), f'Missing: {TOKEN_CONF_FILE}')

    def test_hyprlock_conf_exists(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')


class TestHyprlockStructure(unittest.TestCase):
    """Verify hyprlock.conf structure, widget blocks, and syntax balance."""

    def test_balanced_brackets(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        # Strip comments
        lines = [line.split('#')[0] for line in content.splitlines()]
        cleaned = '\n'.join(lines)
        open_braces = cleaned.count('{')
        close_braces = cleaned.count('}')
        self.assertEqual(
            open_braces, close_braces,
            f'Mismatched braces: {open_braces} open vs {close_braces} close'
        )

    def test_required_widgets_present(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        self.assertIn('background {', content, 'Missing background widget block')
        self.assertIn('input-field {', content, 'Missing input-field widget block')
        self.assertIn('label {', content, 'Missing label widget block')

    def test_background_uses_blur_and_screenshot(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        self.assertIn('path = screenshot', content)
        self.assertIn('blur_passes', content)
        self.assertIn('blur_size', content)

    def test_input_field_uses_token_variables(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        # Find input-field block
        input_block = re.search(r'input-field\s*\{(.*?)\}', content, flags=re.DOTALL)
        self.assertIsNotNone(input_block, 'Could not find input-field block')
        block_text = input_block.group(1)
        self.assertIn('inner_color', block_text)
        self.assertIn('outer_color', block_text)
        self.assertIn('check_color', block_text)
        self.assertIn('fail_color', block_text)
        self.assertIn('font_color', block_text)


class TestHyprlockTokens(unittest.TestCase):
    """Verify hyprlock.conf imports and uses generated theme tokens."""

    def test_sources_generated_tokens(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        self.assertTrue(
            'source = generated/theme-tokens.conf' in content or
            'source = ~/.config/hypr/generated/theme-tokens.conf' in content or
            'source = $XDG_CONFIG_HOME/hypr/generated/theme-tokens.conf' in content,
            'hyprlock.conf does not source generated/theme-tokens.conf'
        )

    def test_no_hardcoded_hex_colors(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        lines = [line.split('#')[0] for line in content.splitlines()]
        cleaned = '\n'.join(lines)
        hexes = HEX_COLOR_RE.findall(cleaned)
        self.assertEqual(
            hexes, [],
            f'Hardcoded hex colors found in hyprlock.conf: {hexes}'
        )

    def test_used_theme_tokens_are_defined(self):
        self.assertTrue(os.path.isfile(CONF_FILE), f'Missing: {CONF_FILE}')
        defined = _extract_defined_hypr_tokens()
        self.assertTrue(bool(defined), 'No tokens defined in generated/theme-tokens.conf')
        with open(CONF_FILE, 'r') as f:
            content = f.read()
        # Exclude comments and hyprlock format variables like $TIME, $USER, $FAIL, $ATTEMPTS
        HYPRLOCK_BUILTINS = {
            'TIME', 'TIME12', 'USER', 'FAIL', 'ATTEMPTS', 'LAYOUT',
            'PAMFAIL', 'PAMPROMPT', 'FPRINTFAIL', 'FPRINTPROMPT', 'DESC',
            'XDG_CONFIG_HOME', 'HOME'
        }
        lines = [line.split('#')[0] for line in content.splitlines()]
        cleaned = '\n'.join(lines)
        for match in VARIABLE_USAGE_RE.finditer(cleaned):
            var_name = match.group(1)
            if var_name in HYPRLOCK_BUILTINS:
                continue
            self.assertIn(
                var_name, defined,
                f'Undefined token ${var_name} used in hypr/hyprlock.conf'
            )


if __name__ == '__main__':
    unittest.main()
