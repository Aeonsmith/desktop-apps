"""
Unit and Integration Test Suite for Matrix Neural Terminal
"""

import unittest
import os
import json
import tempfile
import tkinter as tk
from pathlib import Path
from unittest.mock import patch, MagicMock

import matrix_terminal
from matrix_terminal import UnifiedMatrixTerminal, DEFAULT_CONFIG, MOCK_TARGETS, DICTIONARY_WORDS


class TestMatrixTerminalConfigAndHistory(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.custom_config_path = os.path.join(self.test_dir.name, "test_config.json")
        self.custom_history_path = os.path.join(self.test_dir.name, "test_history.json")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_load_or_create_default_config(self):
        with patch.object(matrix_terminal, "CONFIG_FILE", self.custom_config_path):
            root = tk.Tk()
            root.withdraw()
            app = UnifiedMatrixTerminal()
            cfg = app._load_or_create_config()
            self.assertTrue(os.path.exists(self.custom_config_path))
            self.assertEqual(cfg["theme"], "matrix_green")
            self.assertIn("cyber_amber", cfg["themes"])
            self.assertIn("ice_cyan", cfg["themes"])
            self.assertIn("synth_purple", cfg["themes"])
            self.assertIn("blood_red", cfg["themes"])
            app.destroy()
            root.destroy()

    def test_load_and_save_persistent_history(self):
        with patch.object(matrix_terminal, "HISTORY_FILE", self.custom_history_path):
            root = tk.Tk()
            root.withdraw()
            app = UnifiedMatrixTerminal()
            app.history = ["scan mainframe", "status", "philosophy shadow"]
            app._save_persistent_history()
            
            self.assertTrue(os.path.exists(self.custom_history_path))
            loaded = app._load_persistent_history()
            self.assertEqual(loaded, ["scan mainframe", "status", "philosophy shadow"])
            app.destroy()
            root.destroy()


class TestMatrixTerminalCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a hidden root Tk instance for headless testing
        cls.root = tk.Tk()
        cls.root.withdraw()
        cls.app = UnifiedMatrixTerminal()

    @classmethod
    def tearDownClass(cls):
        try:
            cls.app.destroy()
            cls.root.destroy()
        except Exception:
            pass

    def setUp(self):
        self.app._cmd_clear()

    def test_banner_and_clear(self):
        self.app._cmd_clear()
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("OPERATOR", content)
        self.assertIn("Neural link established", content)

    def test_help_command_overview(self):
        self.app._cmd_help()
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("AVAILABLE MATRIX OPERATOR PROTOCOLS", content)
        self.assertIn("scan", content)
        self.assertIn("crack", content)
        self.assertIn("dump", content)
        self.assertIn("philosophy", content)

    def test_help_subcommand(self):
        self.app._cmd_help(["scan"])
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("MANUAL: SCAN", content)

    def test_status_command(self):
        self.app._cmd_status()
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("OPERATOR & TELEMETRY STATUS", content)
        self.assertIn("Quantum 4096-bit Lattice", content)

    def test_philosophy_command_all(self):
        self.app._cmd_philosophy()
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("CARL JUNG // DEPTH PSYCHOLOGY & INDIVIDUATION", content)
        self.assertIn("THE PERSONA & THE SOCIAL MASK", content)
        self.assertIn("INDIVIDUATION & PERSONAL RESPONSIBILITY", content)
        self.assertIn("SYNCHRONICITY", content)
        self.assertIn("CONFRONTING THE SHADOW", content)
        self.assertIn("EGO INFLATION VS. CONSCIOUS HUMILITY", content)

    def test_philosophy_command_topic(self):
        self.app._cmd_philosophy(["shadow"])
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("CONFRONTING THE SHADOW", content)

    def test_theme_switching(self):
        self.app._cmd_theme(["cyber_amber"])
        self.assertEqual(self.app.current_theme_name, "cyber_amber")
        content = self.app.log_text.get("1.0", tk.END)
        self.assertIn("Switched theme to 'cyber_amber'", content)

        # Revert back to matrix_green
        self.app._cmd_theme(["matrix_green"])
        self.assertEqual(self.app.current_theme_name, "matrix_green")

    def test_mock_targets_dictionary(self):
        self.assertIn("mainframe", MOCK_TARGETS)
        self.assertIn("satellite", MOCK_TARGETS)
        self.assertIn("sentinel", MOCK_TARGETS)
        self.assertTrue(len(DICTIONARY_WORDS) >= 5)


if __name__ == "__main__":
    unittest.main()
