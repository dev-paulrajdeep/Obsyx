"""Tests for headless Wayland compositor integration using Hyprland."""

import os
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNNER_SCRIPT = os.path.join(REPO_ROOT, "tools", "test_headless.sh")


class TestHeadlessWaylandIntegration(unittest.TestCase):
    """Verify that Hyprland executes cleanly in headless mode with Obsyx configs."""

    @classmethod
    def setUpClass(cls):
        if shutil.which("hyprland") is None:
            raise unittest.SkipTest("hyprland binary not available in PATH")

    def test_runner_script_exists_and_executable(self):
        """tools/test_headless.sh must exist, be executable, and pass bash syntax check."""
        self.assertTrue(os.path.isfile(RUNNER_SCRIPT), f"Missing {RUNNER_SCRIPT}")
        self.assertTrue(os.access(RUNNER_SCRIPT, os.X_OK), f"{RUNNER_SCRIPT} is not executable")
        res = subprocess.run(["bash", "-n", RUNNER_SCRIPT], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Syntax error in {RUNNER_SCRIPT}:\n{res.stderr}")

    def test_hyprland_verify_default_config(self):
        """hyprland --verify-config must succeed on hypr/hyprland.lua."""
        hypr_entry = os.path.join(REPO_ROOT, "hypr", "hyprland.lua")
        proc = subprocess.run(
            ["hyprland", "--verify-config", "--config", hypr_entry],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(proc.returncode, 0, f"Hyprland verify failed:\n{proc.stdout}\n{proc.stderr}")
        self.assertIn("config ok", proc.stdout)

    def test_hyprland_verify_profiles(self):
        """hyprland --verify-config must succeed for both laptop and workstation profiles."""
        for profile in ("laptop", "workstation"):
            profile_lua = os.path.join(REPO_ROOT, "profiles", profile, "hypr", "profile.lua")
            self.assertTrue(os.path.isfile(profile_lua), f"Missing profile file: {profile_lua}")

            with tempfile.NamedTemporaryFile("w", suffix=".lua", delete=False) as tmp:
                tmp.write(f"""
                    package.path = "{REPO_ROOT}/hypr/?.lua;" .. package.path
                    require("hyprland")
                    dofile("{profile_lua}")
                """)
                tmp_path = tmp.name

            try:
                proc = subprocess.run(
                    ["hyprland", "--verify-config", "--config", tmp_path],
                    capture_output=True,
                    text=True,
                    cwd=REPO_ROOT,
                )
                self.assertEqual(
                    proc.returncode,
                    0,
                    f"Profile '{profile}' failed verification:\n{proc.stdout}\n{proc.stderr}",
                )
                self.assertIn("config ok", proc.stdout)
            finally:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    def test_headless_session_runner(self):
        """Running tools/test_headless.sh must exit with 0."""
        proc = subprocess.run(
            [RUNNER_SCRIPT],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(proc.returncode, 0, f"Headless test runner failed:\n{proc.stdout}\n{proc.stderr}")
        self.assertIn("PASSED successfully", proc.stdout)


if __name__ == "__main__":
    unittest.main()
