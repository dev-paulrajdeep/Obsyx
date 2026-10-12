"""Safety and behavior tests for Obsyx update, backup, and restore commands."""

import json
import glob
import os
import shutil
import subprocess
import tarfile
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_BIN = os.path.join(REPO_ROOT, "bin", "obsyx")


def run_cli(*args, env=None, cwd=REPO_ROOT, binary=CLI_BIN):
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    return subprocess.run([binary, *args], cwd=cwd, env=merged_env, capture_output=True, text=True)


class TestBackupRestore(unittest.TestCase):
    def test_backup_and_restore_preserves_old_target(self):
        with tempfile.TemporaryDirectory() as root:
            config = os.path.join(root, "config")
            os.makedirs(os.path.join(config, "hypr"))
            with open(os.path.join(config, "hypr", "hyprland.conf"), "w") as stream:
                stream.write("restored config\n")
            state_home = os.path.join(root, "state")
            archive = os.path.join(root, "backup.tar.gz")

            backup = run_cli("backup", "--source", config, "--output", archive, "--json")
            self.assertEqual(backup.returncode, 0, backup.stderr)
            self.assertEqual(json.loads(backup.stdout)["status"], "ok")

            dest = os.path.join(root, "restore")
            os.makedirs(os.path.join(dest, "hypr"))
            with open(os.path.join(dest, "hypr", "local.conf"), "w") as stream:
                stream.write("keep before restore\n")
            restored = run_cli("restore", archive, "--dest", dest, "--json", env={"XDG_STATE_HOME": state_home})
            self.assertEqual(restored.returncode, 0, restored.stderr)
            result = json.loads(restored.stdout)
            self.assertEqual(result["status"], "ok")
            self.assertTrue(os.path.isfile(result["pre_restore_backup"]))
            with open(os.path.join(dest, "hypr", "hyprland.conf")) as stream:
                self.assertEqual(stream.read(), "restored config\n")
            previous = glob.glob(os.path.join(dest, "hypr.pre-restore.*"))
            self.assertEqual(len(previous), 1)
            with open(os.path.join(previous[0], "local.conf")) as stream:
                self.assertEqual(stream.read(), "keep before restore\n")

    def test_restore_dry_run_and_archive_overwrite_refusal(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "source")
            os.makedirs(os.path.join(source, "waybar"))
            with open(os.path.join(source, "waybar", "config.jsonc"), "w") as stream:
                stream.write("{}\n")
            archive = os.path.join(root, "backup.tar.gz")
            first = run_cli("backup", "--source", source, "--output", archive)
            self.assertEqual(first.returncode, 0, first.stderr)
            second = run_cli("backup", "--source", source, "--output", archive)
            self.assertNotEqual(second.returncode, 0)
            dest = os.path.join(root, "dest")
            preview = run_cli("restore", archive, "--dest", dest, "--dry-run", "--json")
            self.assertEqual(preview.returncode, 0, preview.stderr)
            self.assertFalse(os.path.exists(dest))

    def test_restore_rejects_path_traversal_before_writing(self):
        with tempfile.TemporaryDirectory() as root:
            archive_path = os.path.join(root, "malicious.tar.gz")
            manifest = {"format": "obsyx-config-backup", "format_version": 1,
                        "created_at": "test", "source": "test", "entries": ["hypr"],
                        "skipped_symlinks": []}
            with tarfile.open(archive_path, "w:gz") as archive:
                raw = json.dumps(manifest).encode()
                info = tarfile.TarInfo("manifest.json")
                info.size = len(raw)
                import io
                archive.addfile(info, io.BytesIO(raw))
                bad = tarfile.TarInfo("hypr/../../outside")
                bad.size = 4
                archive.addfile(bad, io.BytesIO(b"oops"))
            dest = os.path.join(root, "dest")
            result = run_cli("restore", archive_path, "--dest", dest)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(os.path.exists(dest))
            self.assertFalse(os.path.exists(os.path.join(root, "outside")))

    def test_backup_skips_nested_symlinks_and_records_them(self):
        with tempfile.TemporaryDirectory() as root:
            source = os.path.join(root, "source")
            os.makedirs(os.path.join(source, "hypr"))
            with open(os.path.join(source, "hypr", "settings.conf"), "w") as stream:
                stream.write("safe content\n")
            os.symlink("/etc/passwd", os.path.join(source, "hypr", "external.conf"))
            archive = os.path.join(root, "backup.tar.gz")
            result = run_cli("backup", "--source", source, "--output", archive, "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(result.stdout)["manifest"]
            self.assertIn("hypr/external.conf", manifest["skipped_symlinks"])
            with tarfile.open(archive, "r:gz") as tar:
                self.assertNotIn("hypr/external.conf", tar.getnames())

    def test_restore_rejects_symlink_members(self):
        with tempfile.TemporaryDirectory() as root:
            archive_path = os.path.join(root, "linked.tar.gz")
            manifest = {"format": "obsyx-config-backup", "format_version": 1,
                        "created_at": "test", "source": "test", "entries": ["hypr"],
                        "skipped_symlinks": []}
            with tarfile.open(archive_path, "w:gz") as archive:
                raw = json.dumps(manifest).encode()
                info = tarfile.TarInfo("manifest.json")
                info.size = len(raw)
                import io
                archive.addfile(info, io.BytesIO(raw))
                link = tarfile.TarInfo("hypr/external.conf")
                link.type = tarfile.SYMTYPE
                link.linkname = "/etc/passwd"
                archive.addfile(link)
            dest = os.path.join(root, "dest")
            result = run_cli("restore", archive_path, "--dest", dest)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(os.path.exists(dest))


class TestUpdate(unittest.TestCase):
    def setUp(self):
        if not shutil.which("git"):
            self.skipTest("git not available")
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = self.temp.name
        self.checkout = os.path.join(self.root, "checkout")
        os.makedirs(os.path.join(self.checkout, "bin"))
        shutil.copy2(CLI_BIN, os.path.join(self.checkout, "bin", "obsyx"))
        self.remote = os.path.join(self.root, "remote.git")
        self._git("init", "--bare", "--initial-branch=main", self.remote)
        self._git("init", "--initial-branch=main", self.checkout)
        self._git("-C", self.checkout, "config", "user.name", "Obsyx Tests")
        self._git("-C", self.checkout, "config", "user.email", "tests@example.invalid")
        self._git("-C", self.checkout, "add", "bin/obsyx")
        self._git("-C", self.checkout, "commit", "-m", "initial")
        self._git("-C", self.checkout, "remote", "add", "origin", self.remote)
        self._git("-C", self.checkout, "push", "-u", "origin", "main")

    def _git(self, *args):
        result = subprocess.run(["git", *args], capture_output=True, text=True)
        if result.returncode:
            self.fail(f"git {' '.join(args)} failed: {result.stderr}")

    def _publish_commit(self):
        publisher = os.path.join(self.root, "publisher")
        self._git("clone", self.remote, publisher)
        self._git("-C", publisher, "config", "user.name", "Obsyx Tests")
        self._git("-C", publisher, "config", "user.email", "tests@example.invalid")
        with open(os.path.join(publisher, "next.txt"), "w") as stream:
            stream.write("new version\n")
        self._git("-C", publisher, "add", "next.txt")
        self._git("-C", publisher, "commit", "-m", "next")
        self._git("-C", publisher, "push", "origin", "main")

    def test_check_and_fast_forward_update(self):
        self._publish_commit()
        cli = os.path.join(self.checkout, "bin", "obsyx")
        check = run_cli("update", "--check", "--json", cwd=self.checkout, binary=cli)
        self.assertEqual(check.returncode, 0, f"stdout={check.stdout}\nstderr={check.stderr}")
        check_data = json.loads(check.stdout)
        self.assertEqual(check_data["status"], "available")
        self.assertEqual(check_data["behind"], 1)
        update = run_cli("update", "--json", cwd=self.checkout, binary=cli)
        self.assertEqual(update.returncode, 0, update.stderr)
        self.assertEqual(json.loads(update.stdout)["status"], "updated")
        self.assertTrue(os.path.isfile(os.path.join(self.checkout, "next.txt")))

    def test_dirty_checkout_is_refused(self):
        with open(os.path.join(self.checkout, "untracked.txt"), "w") as stream:
            stream.write("local data\n")
        cli = os.path.join(self.checkout, "bin", "obsyx")
        result = run_cli("update", "--json", cwd=self.checkout, binary=cli)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "dirty")
        self.assertTrue(os.path.isfile(os.path.join(self.checkout, "untracked.txt")))

    def test_diverged_checkout_is_refused(self):
        self._publish_commit()
        with open(os.path.join(self.checkout, "local.txt"), "w") as stream:
            stream.write("local commit\n")
        self._git("-C", self.checkout, "add", "local.txt")
        self._git("-C", self.checkout, "commit", "-m", "local")
        cli = os.path.join(self.checkout, "bin", "obsyx")
        result = run_cli("update", "--json", cwd=self.checkout, binary=cli)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["status"], "diverged")
        self.assertFalse(os.path.exists(os.path.join(self.checkout, "next.txt")))

    def test_non_git_install_is_directed_to_package_manager(self):
        install_root = os.path.join(self.root, "installed", "share", "obsyx")
        os.makedirs(os.path.join(install_root, "bin"))
        cli = os.path.join(install_root, "bin", "obsyx")
        shutil.copy2(CLI_BIN, cli)
        result = run_cli("update", "--json", cwd=install_root, binary=cli)
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "unsupported")
        self.assertIn("package manager", payload["message"])


if __name__ == "__main__":
    unittest.main()
