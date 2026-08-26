import json, os, sys, tempfile, unittest
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers"))
from _lib import config, mechanics_ops


class TestSumDistribution(unittest.TestCase):
    """The distribution helper must be exactly right; everything else reads off it."""

    def test_single_die_is_uniform(self):
        dist = mechanics_ops._sum_distribution(1, 6, 1)
        self.assertEqual(dist, {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1})

    def test_two_d6_is_the_known_bell_curve(self):
        dist = mechanics_ops._sum_distribution(2, 6, 2)
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[7], 6)
        self.assertEqual(dist[12], 1)
        self.assertEqual(sum(dist.values()), 36)

    def test_keep_best_two_of_three_matches_brute_force(self):
        expected = {}
        for roll in product(range(1, 7), repeat=3):
            total = sum(sorted(roll, reverse=True)[:2])
            expected[total] = expected.get(total, 0) + 1
        self.assertEqual(mechanics_ops._sum_distribution(3, 6, 2), expected)

    def test_oversized_keep_less_than_dice_pool_is_refused(self):
        # Guard against a hang: enumeration is only used when keep < dice.
        self.assertIsNone(mechanics_ops._sum_distribution(12, 100, 2))


class TestSumProbability(unittest.TestCase):
    def setUp(self):
        os.environ.pop("BOOKBINDER_CONFIG", None)
        config.load(force_reload=True)

    def tearDown(self):
        os.environ.pop("BOOKBINDER_CONFIG", None)
        config.load(force_reload=True)

    def test_reports_flat_fifty_percent_for_one_d6_at_four(self):
        out = mechanics_ops.calculate_sum_probability(dice=1, sides=6, target=4)
        self.assertIn("50.0%", out)

    def test_reports_the_two_d6_seven_or_better_figure(self):
        out = mechanics_ops.calculate_sum_probability(dice=2, sides=6, target=7)
        self.assertIn("58.3%", out)

    def test_publishes_the_all_max_face_statistic(self):
        # PRISM reads this as its Flourish rate; drafting agents need it from the
        # public tool, not from a private test.
        out = mechanics_ops.calculate_sum_probability(dice=2, sides=6, target=7)
        self.assertIn("maximum face", out)
        self.assertIn("2.78%", out)

    def test_all_max_face_rises_with_a_bigger_pool(self):
        out = mechanics_ops.calculate_sum_probability(dice=4, sides=6, target=7, keep=2)
        self.assertIn("13.19%", out)

    def test_notation_names_the_roll(self):
        out = mechanics_ops.calculate_sum_probability(dice=3, sides=6, modifier=1, target=9, keep=2)
        self.assertIn("best 2 of 3d6", out)
        self.assertIn("+1", out)

    def test_falls_back_to_config_when_called_bare(self):
        p = Path(tempfile.gettempdir()) / "bb_prism_cfg.json"
        p.write_text(json.dumps({
            "mechanics": {"dice": {"sides": 6, "count": 2, "default_target": 9}}
        }), encoding="utf-8")
        os.environ["BOOKBINDER_CONFIG"] = str(p)
        config.load(force_reload=True)
        out = mechanics_ops.calculate_sum_probability()
        self.assertIn("2d6", out)
        # Bare call carries no modifier: 2d6 >= 9 is 10/36. The 41.7% figure
        # quoted elsewhere is Trait +1, i.e. 2d6+1 >= 9.
        self.assertIn("27.8%", out)

    def test_rejects_out_of_range_input(self):
        self.assertIn("Error", mechanics_ops.calculate_sum_probability(dice=0, sides=6, target=5))
        self.assertIn("Error", mechanics_ops.calculate_sum_probability(dice=2, sides=1, target=5))
        self.assertIn("Error", mechanics_ops.calculate_sum_probability(dice=2, sides=6, target=5, keep=3))


class TestPrismBalanceTargets(unittest.TestCase):
    """The spec's balance figures are test cases, not aspirations (spec section 9.2)."""

    def pct(self, dice, modifier, target, keep=2):
        dist = mechanics_ops._sum_distribution(dice, 6, keep)
        total = sum(dist.values())
        hits = sum(c for s, c in dist.items() if s + modifier >= target)
        return round(100.0 * hits / total, 1)

    def test_power_of_friendship_curve_at_tricky(self):
        # Trait +1 vs Difficulty 9, zero through three backers.
        self.assertEqual([self.pct(2 + b, 1, 9) for b in range(4)],
                         [41.7, 68.1, 82.6, 90.6])

    def test_dazzling_is_reachable_but_hard(self):
        self.assertEqual(self.pct(2, 2, 11), 27.8)   # Trait +2, unbacked
        self.assertEqual(self.pct(2, 0, 11), 8.3)    # Trait +0, unbacked

    def test_a_hit_at_dazzling_sits_exactly_at_the_ceiling(self):
        # Hit needs to beat 11 by 3, i.e. total 14. Max is 12 + Trait 2 = 14.
        self.assertEqual(self.pct(2, 2, 14), 2.8)    # only double sixes

    def test_flourish_gets_likelier_with_backers(self):
        # Flourish is both kept dice showing 6.
        def flourish(n):
            hits = sum(1 for r in product(range(1, 7), repeat=n)
                       if sorted(r, reverse=True)[:2] == [6, 6])
            return round(100.0 * hits / 6 ** n, 2)
        self.assertEqual([flourish(2 + b) for b in range(4)],
                         [2.78, 7.41, 13.19, 19.62])


if __name__ == "__main__":
    unittest.main()
