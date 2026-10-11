"""Tests for Obsyx wallpaper daemon configuration, wallpaper assets, and autostart framework."""

import os
import shutil
import subprocess
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(REPO_ROOT, 'assets', 'wallpapers')
WALLPAPER_PNG = os.path.join(ASSETS_DIR, 'noctis_amethyst_default.png')
WALLPAPER_SVG = os.path.join(ASSETS_DIR, 'noctis_amethyst_default.svg')
WALLPAPER_README = os.path.join(ASSETS_DIR, 'README.md')

HYPR_DIR = os.path.join(REPO_ROOT, 'hypr')
HYPRPAPER_CONF = os.path.join(HYPR_DIR, 'hyprpaper.conf')
WALLPAPER_SCRIPT = os.path.join(HYPR_DIR, 'scripts', 'wallpaper.sh')
AUTH_AGENT_SCRIPT = os.path.join(HYPR_DIR, 'scripts', 'auth-agent.sh')
VARIABLES_LUA = os.path.join(HYPR_DIR, 'config', 'variables.lua')
AUTOSTART_LUA = os.path.join(HYPR_DIR, 'config', 'autostart.lua')


def _run_lua(script):
    """Execute a Lua script snippet with the repo's hypr directory in package.path.

    Returns (returncode, stdout, stderr).
    """
    cmd = [
        'lua',
        '-e',
        f'package.path = "{REPO_ROOT}/hypr/?.lua;{REPO_ROOT}/hypr/?/init.lua;" .. package.path\n'
        + script,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    return result.returncode, result.stdout, result.stderr


class TestWallpaperAssets(unittest.TestCase):
    """Verify that canonical Noctis Amethyst wallpaper assets exist and are valid."""

    def test_wallpaper_directory_exists(self):
        self.assertTrue(os.path.isdir(ASSETS_DIR), f'Missing: {ASSETS_DIR}')

    def test_wallpaper_png_exists_and_valid(self):
        self.assertTrue(os.path.isfile(WALLPAPER_PNG), f'Missing: {WALLPAPER_PNG}')
        self.assertGreater(os.path.getsize(WALLPAPER_PNG), 1000, 'Wallpaper PNG is suspiciously small')
        with open(WALLPAPER_PNG, 'rb') as f:
            header = f.read(8)
        self.assertEqual(header, b'\x89PNG\r\n\x1a\n', 'File is not a valid PNG')

    def test_wallpaper_svg_exists_and_contains_tokens(self):
        self.assertTrue(os.path.isfile(WALLPAPER_SVG), f'Missing: {WALLPAPER_SVG}')
        with open(WALLPAPER_SVG, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('<svg', content)
        self.assertIn('</svg>', content)
        # Check canonical Noctis Amethyst colors are used
        self.assertIn('#121018', content)  # void / background
        self.assertTrue('#9b7ede' in content or '#8a63d2' in content, 'Missing amethyst accent colors in SVG')

    def test_wallpaper_readme_exists(self):
        self.assertTrue(os.path.isfile(WALLPAPER_README), f'Missing: {WALLPAPER_README}')


class TestHyprpaperConfig(unittest.TestCase):
    """Verify hyprpaper configuration file structure and directives."""

    def test_hyprpaper_conf_exists(self):
        self.assertTrue(os.path.isfile(HYPRPAPER_CONF), f'Missing: {HYPRPAPER_CONF}')

    def test_hyprpaper_conf_directives(self):
        with open(HYPRPAPER_CONF, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('preload', content)
        self.assertIn('wallpaper', content)
        self.assertIn('noctis_amethyst_default', content)


class TestShellScripts(unittest.TestCase):
    """Verify helper shell scripts exist, are executable, and pass syntax checks."""

    def test_wallpaper_script_exists_and_executable(self):
        self.assertTrue(os.path.isfile(WALLPAPER_SCRIPT), f'Missing: {WALLPAPER_SCRIPT}')
        self.assertTrue(os.access(WALLPAPER_SCRIPT, os.X_OK), f'{WALLPAPER_SCRIPT} is not executable')

    def test_wallpaper_script_syntax_and_daemon_support(self):
        result = subprocess.run(['bash', '-n', WALLPAPER_SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f'Syntax error in wallpaper.sh:\n{result.stderr}')

        with open(WALLPAPER_SCRIPT, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('swww', content, 'wallpaper.sh should support swww')
        self.assertIn('hyprpaper', content, 'wallpaper.sh should support hyprpaper')

    def test_auth_agent_script_exists_and_executable(self):
        self.assertTrue(os.path.isfile(AUTH_AGENT_SCRIPT), f'Missing: {AUTH_AGENT_SCRIPT}')
        self.assertTrue(os.access(AUTH_AGENT_SCRIPT, os.X_OK), f'{AUTH_AGENT_SCRIPT} is not executable')

    def test_auth_agent_script_syntax(self):
        result = subprocess.run(['bash', '-n', AUTH_AGENT_SCRIPT], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f'Syntax error in auth-agent.sh:\n{result.stderr}')

        with open(AUTH_AGENT_SCRIPT, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('hyprpolkitagent', content, 'auth-agent.sh should support hyprpolkitagent')
        self.assertIn('polkit-gnome', content, 'auth-agent.sh should support polkit-gnome')


class TestVariablesAndRegistry(unittest.TestCase):
    """Verify variable definitions and typo corrections in hypr/config/variables.lua."""

    @classmethod
    def setUpClass(cls):
        if shutil.which('lua') is None:
            raise unittest.SkipTest('lua interpreter not available')

    def test_no_awww_typos_in_variables(self):
        with open(VARIABLES_LUA, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertNotIn('awww', content, 'Typo "awww" found in variables.lua')

    def test_startup_registry_keys(self):
        rc, stdout, stderr = _run_lua("""
            local Registry = require("config.variables")
            assert(Registry.Startup ~= nil, "Registry.Startup missing")
            assert(Registry.Startup.authAgent ~= nil, "authAgent missing")
            assert(Registry.Startup.notificationDaemon == "swaync", "notificationDaemon mismatch")
            assert(Registry.Startup.wallpaperDaemon == "swww-daemon", "wallpaperDaemon mismatch: " .. tostring(Registry.Startup.wallpaperDaemon))
            assert(Registry.Startup.statusBar == "waybar", "statusBar mismatch")
            assert(Registry.Startup.clipboardText ~= nil, "clipboardText missing")
            assert(Registry.Startup.clipboardImage ~= nil, "clipboardImage missing")
            assert(Registry.Startup.wallpaper ~= nil, "wallpaper command missing")
            assert(Registry.Desktop.wallpaper == "swww", "Registry.Desktop.wallpaper mismatch: " .. tostring(Registry.Desktop.wallpaper))
            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)


class TestAutostartQueue(unittest.TestCase):
    """Verify Startup queue sequence and hl.on("hyprland.start") behavior."""

    @classmethod
    def setUpClass(cls):
        if shutil.which('lua') is None:
            raise unittest.SkipTest('lua interpreter not available')

    def test_startup_queue_ordering(self):
        """Auth agent must be first; wallpaper/notifications before status bar."""
        rc, stdout, stderr = _run_lua("""
            hl = {
                on = function() end,
                timer = function() end,
                exec_cmd = function() end,
            }
            require("config.variables")
            local Startup = require("config.autostart")
            assert(type(Startup) == "table", "Startup queue is not a table")
            assert(#Startup >= 6, "Startup queue is too short: " .. tostring(#Startup))

            -- Auth agent should be at the very front
            assert(Startup[1] == Registry.Startup.authAgent, "authAgent must be first in startup queue")

            -- Notification and wallpaper daemons before statusBar
            local notif_idx, wall_idx, bar_idx = nil, nil, nil
            for i, cmd in ipairs(Startup) do
                if cmd == Registry.Startup.notificationDaemon then notif_idx = i end
                if cmd == Registry.Startup.wallpaperDaemon then wall_idx = i end
                if cmd == Registry.Startup.statusBar then bar_idx = i end
            end
            assert(notif_idx ~= nil, "notificationDaemon not in queue")
            assert(wall_idx ~= nil, "wallpaperDaemon not in queue")
            assert(bar_idx ~= nil, "statusBar not in queue")
            assert(notif_idx < bar_idx, "notificationDaemon should start before statusBar")
            assert(wall_idx < bar_idx, "wallpaperDaemon should start before statusBar")

            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)

    def test_autostart_execution_and_delayed_wallpaper(self):
        """hl.on registers startup handler and executes commands via hl.exec_cmd."""
        rc, stdout, stderr = _run_lua("""
            local executed_cmds = {}
            local registered_events = {}
            local timer_callbacks = {}

            hl = {
                on = function(event, callback)
                    registered_events[event] = callback
                end,
                timer = function(callback, opts)
                    table.insert(timer_callbacks, { fn = callback, opts = opts })
                end,
                exec_cmd = function(cmd)
                    table.insert(executed_cmds, cmd)
                end,
            }

            require("config.variables")
            require("config.autostart")

            assert(registered_events["hyprland.start"] ~= nil, "hyprland.start event handler not registered")

            -- Trigger the startup handler
            registered_events["hyprland.start"]()

            -- Verify core commands were launched
            assert(#executed_cmds >= 6, "Expected at least 6 commands executed, got " .. tostring(#executed_cmds))
            assert(executed_cmds[1] == Registry.Startup.authAgent, "First executed command should be authAgent")

            -- Trigger delayed wallpaper timer
            assert(#timer_callbacks >= 1, "Delayed timer not registered")
            assert(timer_callbacks[1].opts.timeout == 500, "Timer timeout mismatch")
            timer_callbacks[1].fn()

            -- Last executed command should be wallpaper command
            assert(executed_cmds[#executed_cmds] == Registry.Startup.wallpaper, "Last executed command should be wallpaper")

            print("OK")
        """)
        self.assertEqual(rc, 0, f'Lua error:\n{stderr}')
        self.assertIn('OK', stdout)


if __name__ == '__main__':
    unittest.main()
