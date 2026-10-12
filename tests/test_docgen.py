"""Tests for Obsyx keybinding parser, documentation generator, and Rofi search script (obsyx docgen)."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_BIN = os.path.join(REPO_ROOT, 'bin', 'obsyx')


def _run_cli(*args):
    """Run bin/obsyx with specified arguments."""
    cmd = [CLI_BIN] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout, proc.stderr


class TestDocgenCliInterface(unittest.TestCase):
    """Verify that obsyx docgen is registered and accessible via CLI."""

    def test_docgen_help(self):
        rc, stdout, stderr = _run_cli('docgen', '--help')
        self.assertEqual(rc, 0, f'docgen --help failed:\n{stderr}')
        self.assertIn('docgen', stdout.lower())
        self.assertIn('--output', stdout)
        self.assertIn('--rofi-script', stdout)
        self.assertIn('--json', stdout)

    def test_docgen_json_output(self):
        rc, stdout, stderr = _run_cli('docgen', '--json')
        self.assertEqual(rc, 0, f'docgen --json failed:\n{stderr}')
        try:
            data = json.loads(stdout)
        except Exception as e:
            self.fail(f'Failed to parse JSON output: {e}\nOutput was:\n{stdout}')

        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('keybindings', data)
        self.assertIn('categories', data)
        self.assertGreater(len(data['keybindings']), 35)

        # Check essential keybindings
        keys = [b['key'] for b in data['keybindings']]
        self.assertTrue(any('Return' in k for k in keys), 'Missing Return bind')
        self.assertTrue(any('Space' in k for k in keys), 'Missing Space bind')
        self.assertTrue(any('Q' in k for k in keys), 'Missing Q bind')
        self.assertTrue(any('Escape' in k for k in keys), 'Missing Escape bind')


class TestDocgenFileGeneration(unittest.TestCase):
    """Verify that docgen generates valid KEYBINDINGS.md and rofi/scripts/keybindings.sh."""

    def test_generate_custom_destinations(self):
        with tempfile.TemporaryDirectory() as sandbox:
            out_md = os.path.join(sandbox, 'KEYBINDINGS.md')
            out_rofi = os.path.join(sandbox, 'keybindings.sh')

            rc, stdout, stderr = _run_cli('docgen', '--output', out_md, '--rofi-script', out_rofi)
            self.assertEqual(rc, 0, f'docgen failed:\n{stdout}\n{stderr}')

            # Verify KEYBINDINGS.md
            self.assertTrue(os.path.isfile(out_md), 'KEYBINDINGS.md was not created')
            with open(out_md, 'r', encoding='utf-8') as f:
                md_content = f.read()

            self.assertIn('# Obsyx Keybindings Cheatsheet', md_content)
            self.assertIn('| Shortcut | Description | Action / Command |', md_content)
            self.assertIn('Terminal Emulator', md_content)
            self.assertIn('Close Window', md_content)
            self.assertIn('Power Menu', md_content)
            self.assertIn('Workspace 1', md_content)

            # Verify rofi/scripts/keybindings.sh
            self.assertTrue(os.path.isfile(out_rofi), 'keybindings.sh was not created')
            self.assertTrue(os.access(out_rofi, os.X_OK), 'keybindings.sh is not executable')

            with open(out_rofi, 'r', encoding='utf-8') as f:
                sh_content = f.read()

            self.assertTrue(sh_content.startswith('#!/usr/bin/env bash'), 'Missing shebang')
            self.assertIn('rofi -dmenu', sh_content)
            self.assertIn('Terminal Emulator', sh_content)

            # Verify bash syntax
            if shutil.which('bash'):
                syntax_check = subprocess.run(['bash', '-n', out_rofi], capture_output=True, text=True)
                self.assertEqual(syntax_check.returncode, 0, f'Bash syntax error in generated script:\n{syntax_check.stderr}')

    def test_check_mode(self):
        """Verify that --check validates whether files are up to date."""
        with tempfile.TemporaryDirectory() as sandbox:
            out_md = os.path.join(sandbox, 'KEYBINDINGS.md')
            out_rofi = os.path.join(sandbox, 'keybindings.sh')

            # Initial generation
            rc, _, _ = _run_cli('docgen', '--output', out_md, '--rofi-script', out_rofi)
            self.assertEqual(rc, 0)

            # Check should pass
            rc_chk, stdout_chk, stderr_chk = _run_cli('docgen', '--output', out_md, '--rofi-script', out_rofi, '--check')
            self.assertEqual(rc_chk, 0, f'Check mode failed when files match:\n{stderr_chk}')

            # Corrupt the file and check should fail
            with open(out_md, 'w', encoding='utf-8') as f:
                f.write('Outdated content')

            rc_fail, _, _ = _run_cli('docgen', '--output', out_md, '--rofi-script', out_rofi, '--check')
            self.assertNotEqual(rc_fail, 0, 'Check mode should fail when files are outdated')


if __name__ == '__main__':
    unittest.main()
