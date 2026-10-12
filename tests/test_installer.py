"""Tests for the Obsyx automated safe installer (bin/obsyx install and tools/install.sh)."""

import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_BIN = os.path.join(REPO_ROOT, 'bin', 'obsyx')
INSTALL_SH = os.path.join(REPO_ROOT, 'tools', 'install.sh')


def _run_cli(*args, input_data=None):
    """Run bin/obsyx with specified arguments."""
    cmd = [CLI_BIN] + list(args)
    proc = subprocess.run(cmd, input=input_data, capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def _run_install_sh(*args, input_data=None):
    """Run tools/install.sh with specified arguments."""
    cmd = [INSTALL_SH] + list(args)
    proc = subprocess.run(cmd, input=input_data, capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout, proc.stderr


class TestInstallerDryRun(unittest.TestCase):
    """Verify that --dry-run simulates actions without touching the filesystem."""

    def test_dry_run_makes_no_filesystem_changes(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_cli('install', '--dest', sandbox, '--dry-run')
            self.assertEqual(rc, 0, f'Installer dry-run failed:\n{stderr}')
            self.assertIn('DRY RUN', stdout)
            # The sandbox must remain completely empty
            entries = os.listdir(sandbox)
            self.assertEqual(entries, [], f'Dry-run modified sandbox directory: {entries}')

    def test_dry_run_json_output(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_cli('install', '--dest', sandbox, '--dry-run', '--json')
            self.assertEqual(rc, 0, f'Installer dry-run --json failed:\n{stderr}')
            try:
                data = json.loads(stdout)
            except Exception as e:
                self.fail(f'Failed to parse JSON: {e}\nOutput was: {stdout}')

            self.assertTrue(data.get('dry_run'))
            self.assertEqual(data.get('status'), 'ok')
            self.assertIn('actions', data)
            self.assertGreaterEqual(len(data['actions']), 6)


class TestInstallerRealExecution(unittest.TestCase):
    """Verify actual installation in an isolated sandbox directory."""

    def test_install_all_components(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_cli('install', '--dest', sandbox)
            self.assertEqual(rc, 0, f'Installer failed:\n{stdout}\n{stderr}')

            # Check that all expected component symlinks were created
            for comp in ('hypr', 'waybar', 'rofi', 'swaync', 'kitty', 'wlogout'):
                dest_path = os.path.join(sandbox, comp)
                self.assertTrue(os.path.islink(dest_path), f'Expected symlink at {dest_path}')
                target = os.path.realpath(dest_path)
                expected_target = os.path.realpath(os.path.join(REPO_ROOT, comp))
                self.assertEqual(target, expected_target, f'Symlink target mismatch for {comp}')

    def test_install_is_idempotent(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # First run
            rc1, _, stderr1 = _run_cli('install', '--dest', sandbox)
            self.assertEqual(rc1, 0, f'First install failed:\n{stderr1}')

            # Second run
            rc2, stdout2, stderr2 = _run_cli('install', '--dest', sandbox)
            self.assertEqual(rc2, 0, f'Second install failed:\n{stderr2}')
            self.assertIn('already linked', stdout2.lower())


class TestInstallerBackupExisting(unittest.TestCase):
    """Verify non-destructive timestamped backups of existing dotfiles."""

    def test_backup_preexisting_config(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # Create a pre-existing config directory with user data
            pre_existing_hypr = os.path.join(sandbox, 'hypr')
            os.makedirs(pre_existing_hypr)
            canary_file = os.path.join(pre_existing_hypr, 'user_custom.conf')
            with open(canary_file, 'w') as f:
                f.write('# User canary file')

            # Run installer
            rc, stdout, stderr = _run_cli('install', '--dest', sandbox)
            self.assertEqual(rc, 0, f'Installer failed with existing config:\n{stdout}\n{stderr}')

            # Check that hypr is now a symlink to Obsyx
            self.assertTrue(os.path.islink(pre_existing_hypr), 'hypr is not a symlink after install')

            # Check that backup directory was created and contains the canary file
            backup_matches = glob.glob(os.path.join(sandbox, 'hypr.backup.*'))
            self.assertEqual(len(backup_matches), 1, f'Expected 1 backup directory, found: {backup_matches}')
            backup_canary = os.path.join(backup_matches[0], 'user_custom.conf')
            self.assertTrue(os.path.isfile(backup_canary), f'Missing canary file in backup: {backup_canary}')
            with open(backup_canary, 'r') as f:
                self.assertIn('User canary file', f.read())


class TestInstallerSelectiveComponents(unittest.TestCase):
    """Verify selective component filtering (--components and --skip)."""

    def test_install_selected_components_only(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_cli('install', '--dest', sandbox, '--components', 'waybar,kitty')
            self.assertEqual(rc, 0, f'Selective install failed:\n{stderr}')

            self.assertTrue(os.path.islink(os.path.join(sandbox, 'waybar')))
            self.assertTrue(os.path.islink(os.path.join(sandbox, 'kitty')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'hypr')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'rofi')))

    def test_install_with_skip(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_cli('install', '--dest', sandbox, '--skip', 'wlogout,swaync')
            self.assertEqual(rc, 0, f'Install with skip failed:\n{stderr}')

            self.assertTrue(os.path.islink(os.path.join(sandbox, 'hypr')))
            self.assertTrue(os.path.islink(os.path.join(sandbox, 'waybar')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'wlogout')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'swaync')))


class TestInstallShWrapper(unittest.TestCase):
    """Verify tools/install.sh wrapper script."""

    def test_install_sh_exists_and_executable(self):
        self.assertTrue(os.path.isfile(INSTALL_SH), f'Missing: {INSTALL_SH}')
        self.assertTrue(os.access(INSTALL_SH, os.X_OK), f'{INSTALL_SH} is not executable')

    def test_install_sh_dry_run(self):
        with tempfile.TemporaryDirectory() as sandbox:
            rc, stdout, stderr = _run_install_sh('--dest', sandbox, '--dry-run')
            self.assertEqual(rc, 0, f'tools/install.sh --dry-run failed:\n{stderr}')
            self.assertIn('DRY RUN', stdout)
            self.assertEqual(os.listdir(sandbox), [])



class TestInstallerInteractive(unittest.TestCase):
    """Verify interactive wizard mode (bin/obsyx install --interactive)."""

    @classmethod
    def tearDownClass(cls):
        # Restore repository to default reference theme (noctis_amethyst) so subsequent tests see clean tokens
        subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, "tools", "build_tokens.py")],
            cwd=REPO_ROOT,
            capture_output=True,
        )

    def test_interactive_full_install(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # Inputs:
            # Step 2: dest -> sandbox
            # Step 3: preset -> 1 (full)
            # Step 4: theme -> 1 (noctis_amethyst)
            # Step 5: profile -> 1 (default)
            # Step 6: confirm -> 1 (install)
            inputs = f"{sandbox}\n1\n1\n1\n1\n"
            rc, stdout, stderr = _run_cli('install', '--interactive', input_data=inputs)
            self.assertEqual(rc, 0, f"Interactive full install failed:\n{stdout}\n{stderr}")

            # Verify components
            for comp in ('hypr', 'waybar', 'rofi', 'swaync', 'kitty', 'wlogout'):
                dest_path = os.path.join(sandbox, comp)
                self.assertTrue(os.path.islink(dest_path), f"Expected symlink at {dest_path}")
                target = os.path.realpath(dest_path)
                expected_target = os.path.realpath(os.path.join(REPO_ROOT, comp))
                self.assertEqual(target, expected_target)

            # Verify active theme state
            state_file = os.path.join(sandbox, '.obsyx_theme')
            self.assertTrue(os.path.isfile(state_file))
            with open(state_file, 'r') as f:
                state = json.load(f)
            self.assertEqual(state.get('active_theme'), 'noctis_amethyst')

            # Verify Next Steps banner
            self.assertIn('Next Steps & Quick Start', stdout)

    def test_interactive_minimal_install(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # Inputs:
            # Step 2: dest -> sandbox
            # Step 3: preset -> 2 (minimal)
            # Step 4: theme -> 2 (obsidian)
            # Step 5: profile -> 1 (default)
            # Step 6: confirm -> 1 (install)
            inputs = f"{sandbox}\n2\n2\n1\n1\n"
            rc, stdout, stderr = _run_cli('install', '-i', input_data=inputs)
            self.assertEqual(rc, 0, f"Interactive minimal install failed:\n{stdout}\n{stderr}")

            # Verify hypr and waybar linked
            self.assertTrue(os.path.islink(os.path.join(sandbox, 'hypr')))
            self.assertTrue(os.path.islink(os.path.join(sandbox, 'waybar')))

            # Verify other components NOT linked and directories NOT created
            for excluded in ('rofi', 'swaync', 'kitty', 'wlogout'):
                self.assertFalse(os.path.exists(os.path.join(sandbox, excluded)), f"{excluded} should not exist in minimal preset")

            # Verify theme tokens were scoped
            self.assertTrue(os.path.isfile(os.path.join(sandbox, 'hypr', 'themes', 'obsidian.lua')))
            self.assertTrue(os.path.isfile(os.path.join(sandbox, 'waybar', 'generated', 'theme-tokens.css')))

            # Verify state
            state_file = os.path.join(sandbox, '.obsyx_theme')
            self.assertTrue(os.path.isfile(state_file))
            with open(state_file, 'r') as f:
                state = json.load(f)
            self.assertEqual(state.get('active_theme'), 'obsidian')

    def test_interactive_custom_install(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # Inputs:
            # Step 2: dest -> sandbox
            # Step 3: preset -> 3 (custom)
            # Components prompt:
            #   hypr -> y
            #   waybar -> n
            #   rofi -> y
            #   swaync -> n
            #   kitty -> y
            #   wlogout -> n
            # Step 4: theme -> 3 (frost)
            # Step 5: profile -> 1 (default)
            # Step 6: confirm -> 1 (install)
            inputs = f"{sandbox}\n3\ny\nn\ny\nn\ny\nn\n3\n1\n1\n"
            rc, stdout, stderr = _run_cli('install', '-i', input_data=inputs)
            self.assertEqual(rc, 0, f"Interactive custom install failed:\n{stdout}\n{stderr}")

            self.assertTrue(os.path.islink(os.path.join(sandbox, 'hypr')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'waybar')))
            self.assertTrue(os.path.islink(os.path.join(sandbox, 'rofi')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'swaync')))
            self.assertTrue(os.path.islink(os.path.join(sandbox, 'kitty')))
            self.assertFalse(os.path.exists(os.path.join(sandbox, 'wlogout')))

            # Check theme
            state_file = os.path.join(sandbox, '.obsyx_theme')
            with open(state_file, 'r') as f:
                state = json.load(f)
            self.assertEqual(state.get('active_theme'), 'frost')

    def test_interactive_dry_run_simulation(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # Inputs:
            # Step 2: dest -> sandbox
            # Step 3: preset -> 1 (full)
            # Step 4: theme -> 1 (noctis_amethyst)
            # Step 5: profile -> 1 (default)
            # Step 6: confirm -> 2 (dry_run)
            inputs = f"{sandbox}\n1\n1\n1\n2\n"
            rc, stdout, stderr = _run_cli('install', '--interactive', input_data=inputs)
            self.assertEqual(rc, 0, f"Interactive dry-run failed:\n{stdout}\n{stderr}")
            self.assertIn('DRY RUN', stdout)
            self.assertEqual(os.listdir(sandbox), [], f"Sandbox modified in dry-run: {os.listdir(sandbox)}")

    def test_interactive_cancellation(self):
        with tempfile.TemporaryDirectory() as sandbox:
            # Inputs:
            # Step 2: dest -> sandbox
            # Step 3: preset -> 1 (full)
            # Step 4: theme -> 1 (noctis_amethyst)
            # Step 5: profile -> 1 (default)
            # Step 6: confirm -> 3 (cancel)
            inputs = f"{sandbox}\n1\n1\n1\n3\n"
            rc, stdout, stderr = _run_cli('install', '--interactive', input_data=inputs)
            self.assertEqual(rc, 0, f"Interactive cancel failed:\n{stdout}\n{stderr}")
            self.assertIn('aborted by user', stdout)
            self.assertEqual(os.listdir(sandbox), [], f"Sandbox modified upon cancel: {os.listdir(sandbox)}")


if __name__ == '__main__':
    unittest.main()
