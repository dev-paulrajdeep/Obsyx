"""Tests for Obsyx plugin architecture, lifecycle hooks, and git-clean user overrides."""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_lua(script: str, extra_package_path: str = "", env: dict = None):
    """Execute a Lua script snippet with the repo's hypr directory in package.path.

    Returns (returncode, stdout, stderr).
    """
    pkg_path = f"{REPO_ROOT}/hypr/?.lua;{REPO_ROOT}/hypr/?/init.lua;{REPO_ROOT}/?.lua;"
    if extra_package_path:
        pkg_path = extra_package_path + ";" + pkg_path

    cmd = [
        "lua",
        "-e",
        f'package.path = "{pkg_path}" .. package.path\n' + script,
    ]
    proc_env = dict(os.environ)
    if env:
        proc_env.update(env)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT, env=proc_env)
    return result.returncode, result.stdout, result.stderr


def _strip_jsonc_comments(text: str) -> str:
    """Remove single-line and multi-line comments from JSONC."""
    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE,
    )
    def replacer(match):
        s = match.group(0)
        return " " if s.startswith("/") else s
    return re.sub(pattern, replacer, text)


class TestPluginCore(unittest.TestCase):
    """Verify core plugin registration, listener APIs, and lifecycle hook dispatch."""

    @classmethod
    def setUpClass(cls):
        if shutil.which("lua") is None:
            raise unittest.SkipTest("lua interpreter not available")

    def test_plugins_api_structure(self):
        """core.plugins exports all required methods and constants."""
        rc, stdout, stderr = _run_lua("""
            local Plugins = require("core.plugins")
            assert(type(Plugins) == "table", "Plugins module must be a table")
            assert(type(Plugins.register) == "function", "missing register")
            assert(type(Plugins.unregister) == "function", "missing unregister")
            assert(type(Plugins.get) == "function", "missing get")
            assert(type(Plugins.list) == "function", "missing list")
            assert(type(Plugins.on) == "function", "missing on")
            assert(type(Plugins.once) == "function", "missing once")
            assert(type(Plugins.off) == "function", "missing off")
            assert(type(Plugins.emit) == "function", "missing emit")
            assert(type(Plugins.clear) == "function", "missing clear")
            assert(type(Plugins.EVENTS) == "table", "missing EVENTS table")
            assert(Plugins.EVENTS.INIT == "on_init", "missing INIT event")
            assert(Plugins.EVENTS.THEME_CHANGE == "on_theme_change", "missing THEME_CHANGE event")
            assert(Plugins.EVENTS.PROFILE_CHANGE == "on_profile_change", "missing PROFILE_CHANGE event")
            assert(Plugins.EVENTS.WORKSPACE_CHANGE == "on_workspace_change", "missing WORKSPACE_CHANGE event")
            print("OK_API")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_API", stdout)

    def test_register_and_get_plugin(self):
        """Plugins.register records metadata and calls init hook."""
        rc, stdout, stderr = _run_lua("""
            local Plugins = require("core.plugins")
            Plugins.clear()

            local initialized = false
            local plugin = Plugins.register("battery_tweak", {
                name = "battery_tweak",
                description = "Battery optimizer",
                version = "1.0.0",
                init = function(self_plugins)
                    initialized = (self_plugins == Plugins)
                end,
            })

            assert(plugin ~= nil, "plugin definition returned is nil")
            assert(initialized == true, "init callback was not called")
            assert(Plugins.get("battery_tweak") == plugin, "Plugins.get failed")
            assert(Plugins.list()["battery_tweak"] == plugin, "Plugins.list failed")
            print("OK_REGISTER")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_REGISTER", stdout)

    def test_register_declarative_hooks(self):
        """Plugins.register binds lifecycle hooks defined on the plugin table."""
        rc, stdout, stderr = _run_lua("""
            local Plugins = require("core.plugins")
            Plugins.clear()

            local events_heard = {}

            Plugins.register("lifecycle_spy", {
                on_init = function()
                    table.insert(events_heard, "init")
                end,
                on_theme_change = function(theme, theme_name)
                    table.insert(events_heard, "theme:" .. tostring(theme_name))
                end,
                on_profile_change = function(profile_name)
                    table.insert(events_heard, "profile:" .. tostring(profile_name))
                end,
                on_workspace_change = function(ws_id)
                    table.insert(events_heard, "ws:" .. tostring(ws_id))
                end,
            })

            Plugins.emit("on_init")
            Plugins.emit("on_theme_change", {}, "Noctis Amethyst")
            Plugins.emit("on_profile_change", "laptop")
            Plugins.emit("on_workspace_change", 3)

            assert(#events_heard == 4, "expected 4 events, got " .. #events_heard)
            assert(events_heard[1] == "init", "wrong event 1")
            assert(events_heard[2] == "theme:Noctis Amethyst", "wrong event 2")
            assert(events_heard[3] == "profile:laptop", "wrong event 3")
            assert(events_heard[4] == "ws:3", "wrong event 4")
            print("OK_DECLARATIVE")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_DECLARATIVE", stdout)

    def test_hook_error_isolation(self):
        """Errors thrown in one hook do not abort subsequent hooks or crash emit."""
        rc, stdout, stderr = _run_lua("""
            local Plugins = require("core.plugins")
            Plugins.clear()

            local second_called = false

            Plugins.on("on_test", function()
                error("crashing hook test failure")
            end)

            Plugins.on("on_test", function()
                second_called = true
            end)

            local res = Plugins.emit("on_test")
            assert(second_called == true, "second hook was not executed after first crashed")
            assert(res.ok == false, "emit should indicate errors occurred")
            assert(#res.errors == 1, "expected 1 recorded error, got " .. tostring(#res.errors))
            print("OK_ISOLATION")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_ISOLATION", stdout)

    def test_once_and_off(self):
        """Plugins.once fires once and removes itself; unsubscribe function removes listener."""
        rc, stdout, stderr = _run_lua("""
            local Plugins = require("core.plugins")
            Plugins.clear()

            local count_once = 0
            Plugins.once("tick", function()
                count_once = count_once + 1
            end)

            local count_unsub = 0
            local unsub = Plugins.on("tick", function()
                count_unsub = count_unsub + 1
            end)

            Plugins.emit("tick")
            assert(count_once == 1, "once hook did not run first time")
            assert(count_unsub == 1, "unsub hook did not run first time")

            unsub()

            Plugins.emit("tick")
            assert(count_once == 1, "once hook ran a second time")
            assert(count_unsub == 1, "unsub hook ran after unsubscribe")

            print("OK_ONCE_OFF")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_ONCE_OFF", stdout)

    def test_unregister_plugin(self):
        """Plugins.unregister removes plugin and unbinds its registered hooks."""
        rc, stdout, stderr = _run_lua("""
            local Plugins = require("core.plugins")
            Plugins.clear()

            local count = 0
            Plugins.register("temp_plugin", {
                on_init = function()
                    count = count + 1
                end,
            })

            Plugins.emit("on_init")
            assert(count == 1, "plugin hook didn't fire")

            local unreg_ok = Plugins.unregister("temp_plugin")
            assert(unreg_ok == true, "unregister returned false")
            assert(Plugins.get("temp_plugin") == nil, "plugin still exists in registry")

            Plugins.emit("on_init")
            assert(count == 1, "hook fired after plugin was unregistered")
            print("OK_UNREGISTER")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_UNREGISTER", stdout)


class TestHyprlandIntegration(unittest.TestCase):
    """Verify that Hyprland bootstrap integrates Plugins and user overrides."""

    @classmethod
    def setUpClass(cls):
        if shutil.which("lua") is None:
            raise unittest.SkipTest("lua interpreter not available")

    def test_hyprland_bootstraps_plugins_and_emits_lifecycle(self):
        """Requiring hyprland.lua exposes Plugins and fires on_theme_change and on_init."""
        rc, stdout, stderr = _run_lua("""
            local function make_mock()
                local t = {}
                local mt = {
                    __index = function(tbl, key)
                        tbl[key] = make_mock()
                        return tbl[key]
                    end,
                    __call = function(...) return make_mock() end,
                }
                setmetatable(t, mt)
                return t
            end
            hl = make_mock()

            local Plugins = require("core.plugins")
            Plugins.clear()

            local theme_changed = false
            local initialized = false

            Plugins.on("on_theme_change", function(theme, name)
                theme_changed = true
            end)

            Plugins.on("on_init", function()
                initialized = true
            end)

            require("hyprland")

            assert(_G.Plugins ~= nil, "Plugins global was not set")
            assert(theme_changed == true, "on_theme_change was not emitted during startup")
            assert(initialized == true, "on_init was not emitted during startup")
            print("OK_BOOTSTRAP")
        """)
        self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
        self.assertIn("OK_BOOTSTRAP", stdout)

    def test_user_overrides_loaded_if_present(self):
        """When user.hyprland exists, hyprland loads it and applies user customizations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            user_dir = os.path.join(tmpdir, "user")
            os.makedirs(user_dir, exist_ok=True)
            user_file = os.path.join(user_dir, "hyprland.lua")
            with open(user_file, "w", encoding="utf-8") as f:
                f.write("""
                    _G.USER_OVERRIDE_RAN = true
                    if Registry and Registry.Apps then
                        Registry.Apps.customUserApp = "my-custom-app"
                    end
                """)

            script_override = """
                local function make_mock()
                    local t = {}
                    local mt = {
                        __index = function(tbl, key)
                            tbl[key] = make_mock()
                            return tbl[key]
                        end,
                        __call = function(...) return make_mock() end,
                    }
                    setmetatable(t, mt)
                    return t
                end
                hl = make_mock()

                require("hyprland")

                assert(_G.USER_OVERRIDE_RAN == true, "user override did not run")
                assert(Registry.Apps.customUserApp == "my-custom-app", "user override app not applied")
                print("OK_USER_LOADED")
            """
            rc, stdout, stderr = _run_lua(script_override, extra_package_path=f"{tmpdir}/?.lua;{tmpdir}/?/init.lua")
            self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
            self.assertIn("OK_USER_LOADED", stdout)

    def test_user_waybar_config_detected(self):
        """When user/waybar.jsonc is present, Registry.Startup.statusBar uses it."""
        with tempfile.TemporaryDirectory() as tmpdir:
            user_dir = os.path.join(tmpdir, "user")
            os.makedirs(user_dir, exist_ok=True)
            user_waybar = os.path.join(user_dir, "waybar.jsonc")
            with open(user_waybar, "w", encoding="utf-8") as f:
                f.write('{"layer": "top"}')

            script_waybar = """
                local function make_mock()
                    local t = {}
                    local mt = {
                        __index = function(tbl, key)
                            tbl[key] = make_mock()
                            return tbl[key]
                        end,
                        __call = function(...) return make_mock() end,
                    }
                    setmetatable(t, mt)
                    return t
                end
                hl = make_mock()

                require("hyprland")

                assert(string.find(Registry.Startup.statusBar, "waybar %-c"), "statusBar not pointing to user waybar: " .. tostring(Registry.Startup.statusBar))
                assert(string.find(Registry.Startup.statusBar, "waybar%.jsonc"), "statusBar missing user path")
                print("OK_USER_WAYBAR")
            """
            rc, stdout, stderr = _run_lua(script_waybar, env={"OBSYX_USER_DIR": user_dir})
            self.assertEqual(rc, 0, f"Lua error:\n{stderr}")
            self.assertIn("OK_USER_WAYBAR", stdout)


class TestGitCleanOverrides(unittest.TestCase):
    """Verify that user overrides are git-ignored and templates are tracked."""

    def test_user_overrides_ignored_by_git(self):
        """Active user overrides in user/ must be ignored by git."""
        test_files = [
            "user/hyprland.lua",
            "user/waybar.jsonc",
            "user/custom.lua",
        ]
        for fpath in test_files:
            res = subprocess.run(
                ["git", "check-ignore", fpath],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )
            self.assertEqual(res.returncode, 0, f"Expected {fpath} to be ignored by git")

    def test_user_templates_tracked_by_git(self):
        """Documentation and template files in user/ must NOT be ignored by git."""
        template_files = [
            "user/README.md",
            "user/hyprland.lua.example",
            "user/waybar.jsonc.example",
        ]
        for fpath in template_files:
            res = subprocess.run(
                ["git", "check-ignore", fpath],
                capture_output=True,
                text=True,
                cwd=REPO_ROOT,
            )
            self.assertNotEqual(res.returncode, 0, f"Expected template {fpath} to be tracked, but git ignored it")


class TestUserExampleSyntax(unittest.TestCase):
    """Verify syntactic correctness of user example templates."""

    def test_hyprland_lua_example_syntax(self):
        """user/hyprland.lua.example must pass luac -p syntax compilation."""
        if not shutil.which("luac"):
            self.skipTest("luac compiler not found")
        example_path = os.path.join(REPO_ROOT, "user", "hyprland.lua.example")
        self.assertTrue(os.path.isfile(example_path), f"Missing {example_path}")
        res = subprocess.run(["luac", "-p", example_path], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Syntax error in user/hyprland.lua.example:\n{res.stderr}")

    def test_waybar_jsonc_example_syntax(self):
        """user/waybar.jsonc.example must parse as valid JSON after stripping comments."""
        example_path = os.path.join(REPO_ROOT, "user", "waybar.jsonc.example")
        self.assertTrue(os.path.isfile(example_path), f"Missing {example_path}")
        with open(example_path, "r", encoding="utf-8") as f:
            content = f.read()
        stripped = _strip_jsonc_comments(content)
        data = json.loads(stripped)
        self.assertIsInstance(data, dict)
        self.assertIn("layer", data)


if __name__ == "__main__":
    unittest.main()
