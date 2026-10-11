"""Tests for Obsyx desktop profiles architecture and obsyx profile CLI command."""

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


class TestProfileDefinitions(unittest.TestCase):
    """Verify that canonical desktop profiles exist with valid metadata and configurations."""

    def test_canonical_profiles_exist(self):
        for name in ('laptop', 'workstation'):
            p_dir = os.path.join(REPO_ROOT, 'profiles', name)
            self.assertTrue(os.path.isdir(p_dir), f'Missing profile directory: {p_dir}')

            meta_file = os.path.join(p_dir, 'profile.json')
            self.assertTrue(os.path.isfile(meta_file), f'Missing metadata file: {meta_file}')

            hypr_file = os.path.join(p_dir, 'hypr', 'profile.lua')
            self.assertTrue(os.path.isfile(hypr_file), f'Missing Hypr profile file: {hypr_file}')

            waybar_conf = os.path.join(p_dir, 'waybar', 'config.jsonc')
            self.assertTrue(os.path.isfile(waybar_conf), f'Missing Waybar config: {waybar_conf}')

            waybar_style = os.path.join(p_dir, 'waybar', 'style.css')
            self.assertTrue(os.path.isfile(waybar_style), f'Missing Waybar stylesheet: {waybar_style}')

    def test_profile_metadata_schema(self):
        for name in ('laptop', 'workstation'):
            meta_file = os.path.join(REPO_ROOT, 'profiles', name, 'profile.json')
            with open(meta_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.assertEqual(data.get('name'), name)
            self.assertIn('display_name', data)
            self.assertIn('form_factor', data)
            self.assertIn('description', data)
            self.assertIn('features', data)
            self.assertIn('blur_passes', data['features'])
            self.assertIn('shadows_enabled', data['features'])

    def test_profile_lua_syntax(self):
        if not shutil.which('luac'):
            self.skipTest('luac compiler not found')
        for name in ('laptop', 'workstation'):
            lua_file = os.path.join(REPO_ROOT, 'profiles', name, 'hypr', 'profile.lua')
            res = subprocess.run(['luac', '-p', lua_file], capture_output=True, text=True)
            self.assertEqual(res.returncode, 0, f'Lua syntax error in {lua_file}:\n{res.stderr}')


class TestProfileCliListAndShow(unittest.TestCase):
    """Verify obsyx profile list and obsyx profile show commands."""

    def test_profile_list_human(self):
        rc, stdout, stderr = _run_cli('profile', 'list')
        self.assertEqual(rc, 0, f'profile list failed:\n{stderr}')
        self.assertIn('laptop', stdout.lower())
        self.assertIn('workstation', stdout.lower())

    def test_profile_list_json(self):
        rc, stdout, stderr = _run_cli('profile', 'list', '--json')
        self.assertEqual(rc, 0, f'profile list --json failed:\n{stderr}')
        data = json.loads(stdout)
        self.assertEqual(data.get('status'), 'ok')
        self.assertIn('profiles', data)
        names = [p['name'] for p in data['profiles']]
        self.assertIn('laptop', names)
        self.assertIn('workstation', names)

    def test_profile_show_existing(self):
        for name in ('laptop', 'workstation'):
            rc, stdout, stderr = _run_cli('profile', 'show', name)
            self.assertEqual(rc, 0, f'profile show {name} failed:\n{stderr}')
            self.assertIn(name, stdout.lower())

    def test_profile_show_json(self):
        rc, stdout, stderr = _run_cli('profile', 'show', 'laptop', '--json')
        self.assertEqual(rc, 0, f'profile show laptop --json failed:\n{stderr}')
        data = json.loads(stdout)
        self.assertEqual(data.get('name'), 'laptop')
        self.assertEqual(data.get('form_factor'), 'laptop')

    def test_profile_show_unknown(self):
        rc, stdout, stderr = _run_cli('profile', 'show', 'nonexistent_xyz')
        self.assertNotEqual(rc, 0, 'profile show nonexistent must fail')


class TestProfileCliApply(unittest.TestCase):
    """Verify obsyx profile apply command with dry-run and sandbox destination."""

    def test_profile_apply_dry_run(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_cli('profile', 'apply', 'laptop', '--dest', sandbox, '--dry-run')
            self.assertEqual(rc, 0, f'profile apply --dry-run failed:\n{stderr}')
            self.assertIn('DRY RUN', stdout)
            self.assertEqual(os.listdir(sandbox), [], 'Dry-run modified sandbox directory')

    def test_profile_apply_sandbox(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # First, install base configurations into sandbox
            rc_ins, _, _ = _run_cli('install', '--dest', sandbox)
            self.assertEqual(rc_ins, 0)

            # Apply laptop profile
            rc, stdout, stderr = _run_cli('profile', 'apply', 'laptop', '--dest', sandbox)
            self.assertEqual(rc, 0, f'profile apply laptop failed:\n{stdout}\n{stderr}')

            # Check that profile overrides were applied
            hypr_prof = os.path.join(sandbox, 'hypr', 'config', 'profile.lua')
            self.assertTrue(os.path.isfile(hypr_prof), f'Missing {hypr_prof}')
            with open(hypr_prof, 'r') as f:
                self.assertIn('Laptop Profile Overrides', f.read())

            # Check that state tracking file was written
            state_file = os.path.join(sandbox, '.obsyx_profile')
            self.assertTrue(os.path.isfile(state_file), f'Missing {state_file}')
            with open(state_file, 'r') as f:
                state = json.load(f)
            self.assertEqual(state.get('active_profile'), 'laptop')

            # Verify that profile list recognizes active profile
            rc_list, stdout_list, _ = _run_cli('profile', 'list', '--dest', sandbox, '--json')
            self.assertEqual(rc_list, 0)
            list_data = json.loads(stdout_list)
            self.assertEqual(list_data.get('active_profile'), 'laptop')


if __name__ == '__main__':
    unittest.main()
