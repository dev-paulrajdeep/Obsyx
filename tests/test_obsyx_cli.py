"""Tests for the Obsyx CLI core and diagnostic validator (bin/obsyx)."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_BIN = os.path.join(REPO_ROOT, 'bin', 'obsyx')


def _run_cli(*args, cwd=REPO_ROOT):
    """Run bin/obsyx with specified arguments.

    Returns (returncode, stdout, stderr).
    """
    cmd = [CLI_BIN] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return proc.returncode, proc.stdout, proc.stderr


class TestCliInterface(unittest.TestCase):
    """Verify general CLI binary properties, help, and version."""

    def test_cli_binary_exists_and_executable(self):
        self.assertTrue(os.path.isfile(CLI_BIN), f'Missing CLI binary: {CLI_BIN}')
        self.assertTrue(os.access(CLI_BIN, os.X_OK), f'{CLI_BIN} is not executable')

    def test_cli_help(self):
        rc, stdout, stderr = _run_cli('--help')
        self.assertEqual(rc, 0, f'CLI --help failed:\n{stderr}')
        self.assertIn('doctor', stdout)
        self.assertIn('validate', stdout)
        for command in ('update', 'backup', 'restore'):
            self.assertIn(command, stdout)

    def test_cli_version(self):
        rc, stdout, stderr = _run_cli('--version')
        self.assertEqual(rc, 0, f'CLI --version failed:\n{stderr}')
        self.assertIn('0.1.0', stdout)

    def test_cli_unknown_command(self):
        rc, stdout, stderr = _run_cli('unknown-subcommand')
        self.assertNotEqual(rc, 0, 'Unknown subcommand should fail')


class TestDoctorCommand(unittest.TestCase):
    """Verify obsyx doctor diagnostic checks."""

    def test_doctor_human_output(self):
        rc, stdout, stderr = _run_cli('doctor')
        # Doctor may exit 0 or 1 depending on whether optional tools are missing,
        # but output must include doctor header and category checks.
        self.assertIn('Obsyx Doctor', stdout)
        self.assertIn('Hyprland', stdout)
        self.assertIn('Waybar', stdout)

    def test_doctor_json_output(self):
        rc, stdout, stderr = _run_cli('doctor', '--json')
        try:
            data = json.loads(stdout)
        except Exception as e:
            self.fail(f'Failed to parse JSON from doctor --json: {e}\nOutput was: {stdout}')

        self.assertIn('status', data)
        self.assertIn('checks', data)
        self.assertIn('summary', data)
        self.assertIsInstance(data['checks'], list)

        check_names = {c['name'].lower() for c in data['checks']}
        for expected in ('hyprland', 'waybar', 'python3', 'bash'):
            self.assertIn(expected, check_names, f'Missing check for {expected}')

        # Python and bash must be found
        found_map = {c['name'].lower(): c['found'] for c in data['checks']}
        self.assertTrue(found_map.get('python3'), 'python3 should be found')
        self.assertTrue(found_map.get('bash'), 'bash should be found')


class TestValidateCommand(unittest.TestCase):
    """Verify obsyx validate checks across Lua, JSONC, Shell, and Design Tokens."""

    def test_validate_clean_repo_passes(self):
        rc, stdout, stderr = _run_cli('validate')
        self.assertEqual(rc, 0, f'obsyx validate failed on repository:\n{stdout}\n{stderr}')
        self.assertIn('Validation Passed', stdout)

    def test_validate_json_output(self):
        rc, stdout, stderr = _run_cli('validate', '--json')
        self.assertEqual(rc, 0, f'obsyx validate --json failed:\n{stderr}')
        try:
            data = json.loads(stdout)
        except Exception as e:
            self.fail(f'Failed to parse JSON from validate --json: {e}\nOutput was: {stdout}')

        self.assertTrue(data.get('passed'), 'Validation should pass for repo')
        self.assertIn('summary', data)
        self.assertIn('lua', data['summary'])
        self.assertIn('jsonc', data['summary'])
        self.assertIn('shell', data['summary'])
        self.assertIn('tokens', data['summary'])

        # Must have checked files in all categories
        self.assertGreater(data['summary']['lua']['total'], 0, 'No Lua files checked')
        self.assertGreater(data['summary']['jsonc']['total'], 0, 'No JSONC files checked')
        self.assertGreater(data['summary']['shell']['total'], 0, 'No Shell files checked')

    def test_validate_detects_broken_lua(self):
        """Validating a directory with syntax errors must fail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a broken Lua file in a mocked hypr structure
            hypr_dir = os.path.join(tmpdir, 'hypr')
            os.makedirs(hypr_dir)
            with open(os.path.join(hypr_dir, 'broken.lua'), 'w') as f:
                f.write('function broken() syntax error end')

            rc, stdout, stderr = _run_cli('validate', '--path', tmpdir)
            self.assertEqual(rc, 1, 'Validation should fail for broken Lua')
            self.assertIn('FAIL', stdout)


if __name__ == '__main__':
    unittest.main()
