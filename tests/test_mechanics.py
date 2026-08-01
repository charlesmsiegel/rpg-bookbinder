import json, os, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers"))
from _lib import config, mechanics_ops

class TestMechanics(unittest.TestCase):
    def setUp(self):
        config.load(force_reload=True)

    def test_public_tool_surface(self):
        # Positive allowlist: mechanics_ops exposes exactly these system-neutral
        # calculators. Anything added (or re-added) that is not on this list is a
        # deliberate API change and must be reviewed here first.
        expected = {
            "calculate_dice_probability",
            "calculate_extended_action",
            "calculate_experience_cost",
            "calculate_damage_soak",
            "generate_random_table",
        }
        actual = {
            name for name in vars(mechanics_ops)
            if name.startswith("calculate_") or name.startswith("generate_")
        }
        self.assertEqual(expected, actual)

    def test_dice_uses_config_defaults(self):
        out = mechanics_ops.calculate_dice_probability(5)
        self.assertIn("difficulty 6", out)
        self.assertIn("5d10", out)

    def test_dice_sides_configurable(self):
        p = Path(tempfile.gettempdir()) / "bb_mech_cfg.json"
        p.write_text(json.dumps({"mechanics": {"dice": {"sides": 6, "default_difficulty": 4, "botch_on_ones": False}}}), encoding="utf-8")
        os.environ["BOOKBINDER_CONFIG"] = str(p)
        try:
            config.load(force_reload=True)
            out = mechanics_ops.calculate_dice_probability(4)
            self.assertIn("4d6", out)
            self.assertIn("Botch probability: 0.0%", out)
            # botch_on_ones=False, sides=6, diff=4: each die succeeds on 4-6,
            # p=0.5; expected net successes = 4 * 0.5 = 2.00 exactly. This
            # catches the p_failure bug (probabilities must sum to 1 when
            # ones are plain failures).
            self.assertIn("Expected net successes: 2.00", out)
        finally:
            del os.environ["BOOKBINDER_CONFIG"]
            config.load(force_reload=True)

    def test_xp_unconfigured_guidance(self):
        out = mechanics_ops.calculate_experience_cost("attribute", 2, 3)
        self.assertIn("mechanics.xp_costs", out)

    def test_xp_configured(self):
        p = Path(tempfile.gettempdir()) / "bb_xp_cfg.json"
        p.write_text(json.dumps({"mechanics": {"xp_costs": {"attribute": 4}}}), encoding="utf-8")
        os.environ["BOOKBINDER_CONFIG"] = str(p)
        try:
            config.load(force_reload=True)
            out = mechanics_ops.calculate_experience_cost("attribute", 2, 3)
            self.assertIn("8 XP", out)  # (3-1)*4
        finally:
            del os.environ["BOOKBINDER_CONFIG"]
            config.load(force_reload=True)

if __name__ == "__main__":
    unittest.main()
