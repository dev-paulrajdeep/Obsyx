"""Comprehensive test suite for the Obsyx official theme collection and theme switcher."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_BIN = os.path.join(REPO_ROOT, "bin", "obsyx")
sys.path.insert(0, os.path.join(REPO_ROOT, "tools"))

import build_tokens

OFFICIAL_THEMES = ["noctis_amethyst", "obsidian", "frost", "aurora", "ember"]


def _run_cli(*args):
    """Execute bin/obsyx with specified arguments."""
    cmd = [CLI_BIN] + list(args)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    return proc.returncode, proc.stdout, proc.stderr


def _run_lua(script, env_override=None):
    """Execute a Lua script snippet with package.path configured."""
    cmd = [
        "lua",
        "-e",
        f'package.path = "{REPO_ROOT}/hypr/?.lua;{REPO_ROOT}/hypr/?/init.lua;" .. package.path\n'
        + script,
    ]
    env = os.environ.copy()
    if env_override:
        env.update(env_override)
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, env=env)
    return proc.returncode, proc.stdout, proc.stderr


class TestThemeTokenDefinitions(unittest.TestCase):
    """Verify that all five canonical token definitions exist and strictly adhere to schema."""

    def test_all_five_theme_tokens_exist(self):
        for slug in OFFICIAL_THEMES:
            token_path = os.path.join(REPO_ROOT, "core", "tokens", f"{slug}.json")
            self.assertTrue(os.path.isfile(token_path), f"Missing token file: {token_path}")

    def test_all_five_themes_validate(self):
        for slug in OFFICIAL_THEMES:
            token_path = os.path.join(REPO_ROOT, "core", "tokens", f"{slug}.json")
            with open(token_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Should not raise TokenError
            build_tokens.validate_tokens(data)

    def test_theme_specific_identities(self):
        identities = {
            "noctis_amethyst": {"accent": "#9b7ede", "void": "#121018", "passes": 3},
            "obsidian":        {"accent": "#a0a5ad", "void": "#0b0b0e", "passes": 2},
            "frost":           {"accent": "#4fc3f7", "void": "#0b1017", "passes": 3},
            "aurora":          {"accent": "#26a69a", "void": "#071315", "passes": 3},
            "ember":           {"accent": "#ff7043", "void": "#120c0c", "passes": 3},
        }

        for slug, expected in identities.items():
            token_path = os.path.join(REPO_ROOT, "core", "tokens", f"{slug}.json")
            with open(token_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.assertEqual(data["palette"]["accent"], expected["accent"], f"Wrong accent for {slug}")
            self.assertEqual(data["palette"]["void"], expected["void"], f"Wrong void for {slug}")
            self.assertEqual(data["blur"]["passes"], expected["passes"], f"Wrong blur passes for {slug}")


class TestThemeInheritance(unittest.TestCase):
    """Verify deterministic theme inheritance and cycle detection."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="obsyx_inheritance_")

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_single_level_inheritance(self):
        base_path = os.path.join(self.tmpdir, "base.json")
        child_path = os.path.join(self.tmpdir, "child.json")

        base_data = {
            "name": "Base Theme",
            "version": "1.0.0",
            "palette": {
                "void": "#000000",
                "surface": "#111111",
                "accent": "#ff0000",
            },
            "geometry": {
                "rounding": 10,
                "border_size": 2,
            },
            "blur": {
                "size": 12,
                "passes": 3,
            },
        }
        child_data = {
            "name": "Child Theme",
            "inherits": "base.json",
            "palette": {
                "accent": "#00ff00",
            },
            "geometry": {
                "rounding": 4,
            },
        }

        with open(base_path, "w", encoding="utf-8") as f:
            json.dump(base_data, f)
        with open(child_path, "w", encoding="utf-8") as f:
            json.dump(child_data, f)

        resolved = build_tokens.resolve_inheritance(child_data, child_path)
        self.assertEqual(resolved["name"], "Child Theme")
        self.assertEqual(resolved["palette"]["accent"], "#00ff00")
        self.assertEqual(resolved["palette"]["void"], "#000000")
        self.assertEqual(resolved["geometry"]["rounding"], 4)
        self.assertEqual(resolved["geometry"]["border_size"], 2)
        self.assertEqual(resolved["blur"]["passes"], 3)

    def test_circular_inheritance_raises_error(self):
        a_path = os.path.join(self.tmpdir, "a.json")
        b_path = os.path.join(self.tmpdir, "b.json")

        a_data = {"name": "A", "extends": "b.json"}
        b_data = {"name": "B", "extends": "a.json"}

        with open(a_path, "w", encoding="utf-8") as f:
            json.dump(a_data, f)
        with open(b_path, "w", encoding="utf-8") as f:
            json.dump(b_data, f)

        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.resolve_inheritance(a_data, a_path)
        self.assertIn("Circular inheritance detected", str(ctx.exception))

    def test_missing_parent_raises_error(self):
        orphan_path = os.path.join(self.tmpdir, "orphan.json")
        orphan_data = {"name": "Orphan", "extends": "does_not_exist.json"}

        with open(orphan_path, "w", encoding="utf-8") as f:
            json.dump(orphan_data, f)

        with self.assertRaises(build_tokens.TokenError) as ctx:
            build_tokens.resolve_inheritance(orphan_data, orphan_path)
        self.assertIn("Parent theme not found", str(ctx.exception))


class TestThemeCompilation(unittest.TestCase):
    """Verify that compiling each theme generates valid Lua, CSS, RASI, and conf artifacts."""

    def test_compiled_lua_tables_syntax(self):
        if not shutil.which("luac"):
            self.skipTest("luac compiler not found")

        for slug in OFFICIAL_THEMES:
            lua_file = os.path.join(REPO_ROOT, "hypr", "themes", f"{slug}.lua")
            self.assertTrue(os.path.isfile(lua_file), f"Compiled lua table missing: {lua_file}")
            proc = subprocess.run(["luac", "-p", lua_file], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, f"Lua syntax error in {lua_file}:\n{proc.stderr}")

    def test_compile_theme_artifacts_helper(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            token_path = os.path.join(REPO_ROOT, "core", "tokens", "frost.json")
            tokens = build_tokens.load_and_resolve_theme(token_path)

            lua_out = os.path.join(tmpdir, "theme.lua")
            css_out = os.path.join(tmpdir, "theme.css")
            rofi_out = os.path.join(tmpdir, "theme.rasi")
            conf_out = os.path.join(tmpdir, "theme.conf")

            build_tokens.compile_theme_artifacts(
                tokens,
                lua_out=lua_out,
                css_out=css_out,
                rofi_out=rofi_out,
                hypr_conf_out=conf_out,
            )

            self.assertTrue(os.path.isfile(lua_out))
            self.assertTrue(os.path.isfile(css_out))
            self.assertTrue(os.path.isfile(rofi_out))
            self.assertTrue(os.path.isfile(conf_out))

            with open(css_out, "r", encoding="utf-8") as f:
                css_content = f.read()
            self.assertIn("@define-color amethyst", css_content)
            self.assertIn("#4fc3f7", css_content)


class TestThemeLoaderRuntime(unittest.TestCase):
    """Verify runtime theme loader behavior and XDG override detection."""

    @classmethod
    def setUpClass(cls):
        if shutil.which("lua") is None:
            raise unittest.SkipTest("lua interpreter not available")

    def test_loader_loads_all_five_themes(self):
        for slug in OFFICIAL_THEMES:
            rc, stdout, stderr = _run_lua(f"""
                require("config.variables")
                Registry.Theme.name = "{slug}"
                package.loaded["config.theme"] = nil
                local theme = require("config.theme")
                assert(theme ~= nil, "theme is nil")
                assert(Registry.Theme.slug == "{slug}", "slug mismatch")
                print("OK")
            """)
            self.assertEqual(rc, 0, f"Failed loading {slug}:\n{stderr}")
            self.assertIn("OK", stdout)

    def test_xdg_persisted_theme_override(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            obsyx_dir = os.path.join(tmpdir, "obsyx")
            os.makedirs(obsyx_dir, exist_ok=True)
            theme_file = os.path.join(obsyx_dir, "theme")
            with open(theme_file, "w", encoding="utf-8") as f:
                f.write("ember\n")

            rc, stdout, stderr = _run_lua("""
                require("config.variables")
                package.loaded["config.theme"] = nil
                local theme = require("config.theme")
                assert(theme.name == "Ember", "expected Ember from override file, got: " .. tostring(theme.name))
                assert(Registry.Theme.slug == "ember", "expected ember slug")
                print("OVERRIDE_OK")
            """, env_override={"XDG_CONFIG_HOME": tmpdir})

            self.assertEqual(rc, 0, f"Override test failed:\n{stderr}")
            self.assertIn("OVERRIDE_OK", stdout)


class TestThemeCli(unittest.TestCase):
    """Verify obsyx theme CLI subcommands (list, show, apply)."""

    def test_theme_list_human(self):
        rc, stdout, stderr = _run_cli("theme", "list")
        self.assertEqual(rc, 0, f"theme list failed:\n{stderr}")
        self.assertIn("Obsyx Official Themes", stdout)
        for slug in OFFICIAL_THEMES:
            self.assertIn(slug, stdout)

    def test_theme_list_json(self):
        rc, stdout, stderr = _run_cli("theme", "list", "--json")
        self.assertEqual(rc, 0, f"theme list --json failed:\n{stderr}")
        data = json.loads(stdout)
        self.assertEqual(data.get("status"), "ok")
        theme_slugs = [t["slug"] for t in data.get("themes", [])]
        for slug in OFFICIAL_THEMES:
            self.assertIn(slug, theme_slugs)

    def test_theme_show_details(self):
        for slug in OFFICIAL_THEMES:
            rc, stdout, stderr = _run_cli("theme", "show", slug)
            self.assertEqual(rc, 0, f"theme show {slug} failed:\n{stderr}")
            self.assertIn("Key Palette Tokens:", stdout)
            self.assertIn("Geometry & Materials:", stdout)

    def test_theme_show_json(self):
        rc, stdout, stderr = _run_cli("theme", "show", "aurora", "--json")
        self.assertEqual(rc, 0, f"theme show aurora --json failed:\n{stderr}")
        data = json.loads(stdout)
        self.assertEqual(data.get("name"), "Aurora")
        self.assertEqual(data["palette"]["accent"], "#26a69a")

    def test_theme_show_unknown_error(self):
        rc, stdout, stderr = _run_cli("theme", "show", "nonexistent_theme")
        self.assertNotEqual(rc, 0)
        self.assertIn("Unknown theme", stderr)

    def test_theme_apply_dry_run(self):
        rc, stdout, stderr = _run_cli("theme", "apply", "frost", "--dry-run")
        self.assertEqual(rc, 0, f"theme apply --dry-run failed:\n{stderr}")
        self.assertIn("DRY RUN SIMULATION", stdout)
        self.assertIn("Frost", stdout)

    def test_theme_apply_sandbox_dest(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            rc, stdout, stderr = _run_cli("theme", "apply", "obsidian", "--dest", tmpdir, "--json")
            self.assertEqual(rc, 0, f"theme apply sandbox failed:\n{stderr}")
            data = json.loads(stdout)
            self.assertEqual(data.get("status"), "ok")
            self.assertEqual(data.get("theme"), "obsidian")

            # Check that files exist in destination
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "obsyx", "theme")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, ".obsyx_theme")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "hypr", "themes", "obsidian.lua")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "waybar", "generated", "theme-tokens.css")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "rofi", "generated", "theme-tokens.rasi")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "swaync", "generated", "theme-tokens.css")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "hypr", "generated", "theme-tokens.conf")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "kitty", "generated", "theme-tokens.conf")))
            self.assertTrue(os.path.isfile(os.path.join(tmpdir, "wlogout", "generated", "theme-tokens.css")))

            # Check that theme list recognizes the active theme in this destination
            rc_list, stdout_list, _ = _run_cli("theme", "list", "--dest", tmpdir, "--json")
            self.assertEqual(rc_list, 0)
            list_data = json.loads(stdout_list)
            self.assertEqual(list_data.get("active_theme"), "obsidian")


class TestThemeSwitcherScript(unittest.TestCase):
    """Verify the interactive Rofi theme switcher script."""

    def test_switcher_script_exists_and_executable(self):
        script_path = os.path.join(REPO_ROOT, "rofi", "scripts", "theme-switcher.sh")
        self.assertTrue(os.path.isfile(script_path), f"Missing script: {script_path}")
        self.assertTrue(os.access(script_path, os.X_OK), f"Script not executable: {script_path}")

    def test_switcher_script_bash_syntax(self):
        script_path = os.path.join(REPO_ROOT, "rofi", "scripts", "theme-switcher.sh")
        proc = subprocess.run(["bash", "-n", script_path], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, f"Bash syntax error in switcher script:\n{proc.stderr}")


if __name__ == "__main__":
    unittest.main()
