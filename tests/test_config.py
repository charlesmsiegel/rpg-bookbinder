import json, os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers"))
from _lib import config

class TestConfig(unittest.TestCase):
    def setUp(self):
        config.load(force_reload=True)

    def test_default_file_loads(self):
        self.assertEqual(config.get("system.project_type"), "supplement")

    def test_dotted_get_with_default(self):
        self.assertEqual(config.get("no.such.key", "fallback"), "fallback")

    def test_missing_file_yields_defaults(self):
        os.environ["BOOKBINDER_CONFIG"] = str(Path(tempfile.gettempdir()) / "nope.json")
        try:
            config.load(force_reload=True)
            self.assertEqual(config.get("system.name"), "Generic RPG")
            self.assertEqual(config.get("mechanics.dice.sides"), 10)
        finally:
            del os.environ["BOOKBINDER_CONFIG"]
            config.load(force_reload=True)

    def test_override_file(self):
        p = Path(tempfile.gettempdir()) / "bb_test_cfg.json"
        p.write_text(json.dumps({"system": {"name": "Test Game"}}), encoding="utf-8")
        os.environ["BOOKBINDER_CONFIG"] = str(p)
        try:
            config.load(force_reload=True)
            self.assertEqual(config.get("system.name"), "Test Game")
            # unspecified keys fall back to built-in defaults
            self.assertEqual(config.get("mechanics.dice.default_difficulty"), 6)
        finally:
            del os.environ["BOOKBINDER_CONFIG"]
            config.load(force_reload=True)

if __name__ == "__main__":
    unittest.main()
