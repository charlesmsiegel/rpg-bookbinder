import os, sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers"))
from _lib import config


class TestPrismConfig(unittest.TestCase):
    def setUp(self):
        os.environ.pop("BOOKBINDER_CONFIG", None)
        config.load(force_reload=True)

    def test_system_identity(self):
        self.assertEqual(config.get("system.name"), "PRISM")
        self.assertEqual(config.get("system.project_type"), "core rulebook")

    def test_dice_are_sum_based(self):
        self.assertEqual(config.get("mechanics.dice.sides"), 6)
        self.assertEqual(config.get("mechanics.dice.count"), 2)
        self.assertEqual(config.get("mechanics.dice.default_target"), 9)

    def test_legacy_pool_difficulty_stays_within_its_own_validator(self):
        # calculate_dice_probability rejects difficulty > sides. PRISM does not
        # use that tool, but leaving it broken on its own defaults is not on.
        sides = config.get("mechanics.dice.sides")
        self.assertLessEqual(config.get("mechanics.dice.default_difficulty"), sides)
        self.assertGreaterEqual(config.get("mechanics.dice.default_difficulty"), 3)

    def test_terminology(self):
        self.assertEqual(config.get("terminology.gamemaster"), "Showrunner")
        self.assertEqual(config.get("terminology.player_character"), "Star")

    def test_art_profile_is_ideogram_with_sizes(self):
        self.assertEqual(config.get("art.active_generator"), "ideogram-v4")
        self.assertEqual(config.get("art.density_words_per_illustration"), 2000)
        sizes = config.get("art.generators.ideogram-v4.sizes")
        self.assertIsNotNone(sizes, "art-direction.md requires a sizes map")
        for key in ("portrait", "landscape", "column", "full_page"):
            self.assertIn(key, sizes)
            self.assertEqual(len(sizes[key]), 2)

    def test_prompt_style_is_a_value_the_art_tool_recognizes(self):
        # art.py selects its natural-language builder only on exactly "natural";
        # anything else silently falls back to tag mode.
        self.assertEqual(config.get("art.generators.ideogram-v4.prompt_style"), "natural")

    def test_text_is_not_negated_in_a_profile_chosen_for_lettering(self):
        neg = config.get("art.generators.ideogram-v4.negative_prompt", "")
        self.assertNotIn("text", neg)

    def test_layout_keys_move_together(self):
        style_file = config.get("layout.style_file")
        self.assertEqual(config.get("layout.docx_theme"), "prism")
        self.assertEqual(style_file, "styles/layout/prism.md")
        self.assertTrue(Path(style_file).exists(), f"{style_file} must exist; /compile checks")
        self.assertTrue(Path("styles/layout/prism.theme.json").exists())

    def test_voice_points_at_the_prism_guide(self):
        wsf = config.get("voice.writing_style_file")
        self.assertEqual(wsf, "styles/writing/prism.md")
        self.assertTrue(Path(wsf).exists())

    def test_transform_as_a_verb_is_banned(self):
        banned = " ".join(config.get("voice.banned_phrases"))
        self.assertIn("transforms", banned)


if __name__ == "__main__":
    unittest.main()
