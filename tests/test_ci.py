"""Tests for GitHub Actions CI workflow configuration and token check mode."""

import os
import subprocess
import tempfile
import unittest
import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW_PATH = os.path.join(REPO_ROOT, ".github", "workflows", "ci.yml")
BUILD_TOKENS_BIN = os.path.join(REPO_ROOT, "tools", "build_tokens.py")


class TestWorkflowConfiguration(unittest.TestCase):
    """Verify that .github/workflows/ci.yml exists, is valid YAML, and has all required steps."""

    def test_workflow_file_exists(self):
        """Workflow file .github/workflows/ci.yml must exist."""
        self.assertTrue(
            os.path.isfile(WORKFLOW_PATH),
            f"Missing CI workflow file: {WORKFLOW_PATH}",
        )

    def test_workflow_yaml_is_valid(self):
        """Workflow file must parse as valid YAML without errors."""
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        self.assertIsInstance(data, dict)
        self.assertIn("name", data)
        self.assertIn("jobs", data)

    def test_workflow_triggers(self):
        """Workflow must trigger on push and pull_request."""
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Triggers can be listed under 'on' or True (as boolean in YAML)
        triggers = data.get("on") or data.get(True)
        self.assertIsNotNone(triggers, "Workflow missing 'on' triggers")

        if isinstance(triggers, dict):
            self.assertTrue("push" in triggers or "pull_request" in triggers)
        elif isinstance(triggers, list):
            self.assertTrue("push" in triggers or "pull_request" in triggers)
        else:
            self.fail(f"Unexpected trigger structure: {triggers}")

    def test_workflow_matrix_strategy(self):
        """Workflow jobs must run on ubuntu-latest with a Python matrix."""
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        jobs = data.get("jobs", {})
        self.assertGreater(len(jobs), 0, "No jobs defined in workflow")

        # Find main test job
        test_job = jobs.get("test") or jobs.get("ci") or jobs.get("test-and-validate") or list(jobs.values())[0]
        self.assertEqual(test_job.get("runs-on"), "ubuntu-latest")

        strategy = test_job.get("strategy", {})
        matrix = strategy.get("matrix", {})
        python_versions = matrix.get("python-version", [])
        self.assertIsInstance(python_versions, list)
        self.assertIn("3.11", [str(v) for v in python_versions])
        self.assertIn("3.12", [str(v) for v in python_versions])

    def test_workflow_required_steps_present(self):
        """Workflow steps must include checkout, python setup, lua, token check, validate, and tests."""
        with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        jobs = data.get("jobs", {})
        test_job = jobs.get("test") or jobs.get("ci") or jobs.get("test-and-validate") or list(jobs.values())[0]
        steps = test_job.get("steps", [])
        self.assertGreater(len(steps), 0, "Job has no steps")

        uses_list = [s.get("uses", "") for s in steps if "uses" in s]
        runs_list = [s.get("run", "") for s in steps if "run" in s]
        combined_runs = "\n".join(runs_list)

        # Actions
        self.assertTrue(any("checkout" in u for u in uses_list), "Missing actions/checkout")
        self.assertTrue(any("setup-python" in u for u in uses_list), "Missing actions/setup-python")

        # Commands
        self.assertIn("lua", combined_runs, "Missing Lua installation step")
        self.assertIn("build_tokens.py", combined_runs, "Missing build_tokens.py verification step")
        self.assertIn("obsyx validate", combined_runs, "Missing obsyx validate step")
        self.assertIn("unittest", combined_runs, "Missing unit test runner step")


class TestTokenCompilerCheckMode(unittest.TestCase):
    """Verify that tools/build_tokens.py supports --check flag for CI verification."""

    def test_build_tokens_check_flag_clean(self):
        """Running build_tokens.py --check on the repository must exit 0 when tokens match."""
        proc = subprocess.run(
            ["python3", BUILD_TOKENS_BIN, "--check"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(proc.returncode, 0, f"Expected 0 from --check on clean repo, got:\n{proc.stderr}")
        self.assertIn("up to date", proc.stdout.lower())

    def test_build_tokens_check_detects_outdated_file(self):
        """build_tokens.py --check must exit 1 when a target artifact does not match."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a dummy outdated file
            dummy_out = os.path.join(tmpdir, "outdated.css")
            with open(dummy_out, "w", encoding="utf-8") as f:
                f.write("/* outdated */")

            proc = subprocess.run(
                [
                    "python3",
                    BUILD_TOKENS_BIN,
                    "--check",
                    "--css-out",
                    dummy_out,
                ],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )
            self.assertEqual(proc.returncode, 1, "Expected exit code 1 when target file is outdated")
            self.assertTrue(
                "outdated" in proc.stderr.lower() or "mismatch" in proc.stderr.lower() or "different" in proc.stderr.lower(),
                f"Error message did not mention mismatch/outdated: {proc.stderr}",
            )


if __name__ == "__main__":
    unittest.main()
