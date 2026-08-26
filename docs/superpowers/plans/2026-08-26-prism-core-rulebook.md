# PRISM Core Rulebook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce PRISM — a ~25,000-word core rulebook for an original sugarpop-fantasy one-shot RPG — by configuring Bookbinder for it and running the full authoring pipeline.

**Architecture:** Two halves. Tasks 1–6 are code and configuration: one additive probability function with tests, PRISM's `config/system.json`, the house style assets, and corrections to two shipped drafting prompts that would otherwise point the writing agents at the wrong dice model. Tasks 7–13 run the Bookbinder pipeline (`/init-project` → `/compile`), each gated on the previous phase's quality gate.

**Tech Stack:** Python 3 (stdlib only; `mcp<2` + `httpx` for the servers), `unittest`, Bookbinder MCP servers, Node `docx` for DOCX export, pandoc/weasyprint optional for EPUB/PDF.

**Spec:** `docs/superpowers/specs/2026-08-26-prism-core-rulebook-design.md`

## Global Constraints

- **Traits are +0 to +2. No value above +2 appears anywhere in the book**, including stat blocks and pregenerated characters. There is no Trait advancement.
- **Difficulties are 6 (Easy) / 9 (Tricky) / 11 (Dazzling).** Dazzling is 11, not 12.
- **Outcome ladder:** Miss (under) / Mixed (meets, or beats by 1–2) / Hit (beats by 3+) / **Flourish (both kept dice show 6, on any success)**.
- **Power of Friendship keeps exactly two dice** regardless of pool size. Each backer adds 1d6 and drops 1.
- **Terminology is fixed** (spec §8.1): *Transformation* = noun, *morph* = verb, *transformed* = adjective, named moves are **Solo Morph / Synchronized Morph / Combined Form**, crossing over is **refract**, the two layers are **the everyday** / **the Spectrum**, the fusion gate is **the Chord**. "Transform" as a verb is forbidden outside quoted in-world dialogue.
- **Gamemaster is "Showrunner"; player character is "Star".**
- **No images are generated.** `/art-direction` runs in deferred prompt-manifest mode only.
- **Word target 25,000**, ±25% tolerance per chapter.
- Python: standard library only for new `_lib` code. No new dependencies.

---

## File Structure

**Created:**
- `mcp_servers/_lib/mechanics_ops.py` (modified) — add `calculate_sum_probability` + `_sum_distribution` helper
- `mcp_servers/mechanics.py` (modified) — expose the new tool
- `tests/test_sum_probability.py` — tests for the new function
- `tests/test_mechanics.py` (modified) — update the tool-surface allowlist
- `config/system.json` (modified) — PRISM configuration
- `config/README.md` (modified) — document the two new dice fields
- `styles/writing/prism.md` — house voice
- `styles/templates/core-rulebook.md` — book template
- `styles/layout/prism.md` + `styles/layout/prism.theme.json` — layout language + DOCX theme
- `references/prism/*.md` — PRISM's own canon, for consistency checking
- `.claude/commands/first-draft.md` (modified) — point balance work at the sum tool
- `.claude/agents/book-creation/mechanics-designer.md` (modified) — same, plus replace dice-pool thresholds
- `projects/prism/**` — the book itself (created by the pipeline)

**Already done** (committed earlier on this branch): `.gitignore` now tracks `references/prism/`.

---

### Task 0: Establish a green baseline

`tests/test_art_backends.py` imports `httpx`, which the README lists as a
dependency but which is not installed by default. Without it the suite errors
before you have written a line, and it is easy to mistake that for damage you
caused.

- [ ] **Step 1: Install the runtime dependencies**

Run: `pip install "mcp<2" httpx`

- [ ] **Step 2: Confirm the suite is green before changing anything**

Run: `python -m unittest discover tests`
Expected: `OK`, 25 tests. If anything fails here, fix it before starting Task 1 —
you need a known-good baseline to attribute later failures to.

---

### Task 1: Sum-based dice probability

The existing `calculate_dice_probability` counts successes in a World-of-Darkness dice pool. It cannot express `2d6+1 vs 9` at all, so none of PRISM's numbers are checkable without this.

**Files:**
- Modify: `mcp_servers/_lib/mechanics_ops.py`
- Modify: `tests/test_mechanics.py` (the allowlist at lines 11–24)
- Test: `tests/test_sum_probability.py`

**Interfaces:**
- Consumes: `_lib.config.get(dotted, default)`
- Produces: `mechanics_ops.calculate_sum_probability(dice=None, sides=None, modifier=0, target=None, keep=None) -> str`, and `mechanics_ops._sum_distribution(dice, sides, keep) -> dict[int,int] | None`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_sum_probability.py`:

```python
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
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python -m unittest tests.test_sum_probability -v`
Expected: FAIL — `AttributeError: module '_lib.mechanics_ops' has no attribute '_sum_distribution'`

- [ ] **Step 3: Implement the distribution helper**

Add to `mcp_servers/_lib/mechanics_ops.py`. Add `from collections import defaultdict` and `from itertools import product` to the imports at the top of the file.

```python
def _sum_distribution(dice: int, sides: int, keep: int) -> Optional[dict]:
    """
    Exact distribution over the sum of the best `keep` of `dice` dice of `sides` sides.

    Returns {sum: number_of_outcomes}, or None if the calculation would be too
    large to enumerate. Convolution handles the keep-everything case in linear
    time; dropping dice needs enumeration, which is guarded.
    """
    if keep == dice:
        counts = {0: 1}
        for _ in range(dice):
            nxt = defaultdict(int)
            for running, c in counts.items():
                for face in range(1, sides + 1):
                    nxt[running + face] += c
            counts = dict(nxt)
        return counts

    if sides ** dice > 2_000_000:
        return None

    counts = defaultdict(int)
    for roll in product(range(1, sides + 1), repeat=dice):
        counts[sum(sorted(roll, reverse=True)[:keep])] += 1
    return dict(counts)
```

- [ ] **Step 4: Implement the public function**

Also in `mcp_servers/_lib/mechanics_ops.py`:

```python
def calculate_sum_probability(
    dice: Optional[int] = None,
    sides: Optional[int] = None,
    modifier: int = 0,
    target: Optional[int] = None,
    keep: Optional[int] = None,
) -> str:
    """
    Probability for a sum-based roll: add up the best `keep` of `dice` dice,
    plus a flat modifier, against a target number.

    Every argument falls back to config, so calling this bare answers
    "what are the odds on a standard roll for this game system?"

    Args:
        dice: How many dice to roll. Defaults to mechanics.dice.count.
        sides: Faces per die. Defaults to mechanics.dice.sides.
        modifier: Flat bonus added to the kept sum.
        target: Number the total must reach. Defaults to mechanics.dice.default_target.
        keep: How many of the highest dice to add. Defaults to all of them.

    Returns:
        Success chance, expected value, and a margin table.
    """
    if dice is None:
        dice = config.get("mechanics.dice.count", 2)
    if sides is None:
        sides = config.get("mechanics.dice.sides", 6)
    if target is None:
        target = config.get("mechanics.dice.default_target", 9)
    if keep is None:
        keep = dice

    if not 1 <= dice <= 12:
        return "Error: dice must be between 1 and 12"
    if not 2 <= sides <= 100:
        return "Error: sides must be between 2 and 100"
    if not 1 <= keep <= dice:
        return f"Error: keep must be between 1 and {dice}"

    dist = _sum_distribution(dice, sides, keep)
    if dist is None:
        return "Error: that pool is too large to enumerate exactly (try fewer dice or sides)"

    total = sum(dist.values())
    meets = sum(c for s, c in dist.items() if s + modifier >= target)
    expected = sum((s + modifier) * c for s, c in dist.items()) / total

    notation = f"{dice}d{sides}" if keep == dice else f"best {keep} of {dice}d{sides}"
    if modifier:
        notation += f" {modifier:+d}"

    lines = [
        f"{notation} vs target {target}",
        "",
        f"Chance of meeting the target: {100.0 * meets / total:.1f}%",
        f"Expected total: {expected:.2f}",
        f"Range: {min(dist) + modifier} to {max(dist) + modifier}",
        "",
        "Margin table (chance of beating the target by at least N):",
    ]
    for m in range(0, 6):
        c = sum(cnt for s, cnt in dist.items() if s + modifier >= target + m)
        lines.append(f"  +{m}: {100.0 * c / total:.1f}%")

    # Systems with an "all kept dice showed the best face" special result need this
    # figure, and it cannot be recovered from a sum-only margin table.
    best = keep * sides
    top = dist.get(best, 0)
    lines += [
        "",
        f"Every kept die shows the maximum face ({sides}): {100.0 * top / total:.2f}%",
    ]
    return "\n".join(lines)
```

- [ ] **Step 5: Update the tool-surface allowlist**

`tests/test_mechanics.py` asserts the exact set of public calculators, so it fails by design when one is added. In the `expected` set (around line 14), add the new name:

```python
        expected = {
            "calculate_dice_probability",
            "calculate_extended_action",
            "calculate_experience_cost",
            "calculate_damage_soak",
            "calculate_sum_probability",
            "generate_random_table",
        }
```

The helper `_sum_distribution` starts with an underscore, so it is not picked up by that test's prefix filter and needs no entry.

- [ ] **Step 6: Run the full suite**

Run: `python -m unittest discover tests -v`
Expected: PASS, all tests, including `test_public_tool_surface`.

- [ ] **Step 7: Commit**

```bash
git add mcp_servers/_lib/mechanics_ops.py tests/test_sum_probability.py tests/test_mechanics.py
git commit -m "Add sum-based dice probability to mechanics_ops

The existing calculator counts successes in a dice pool and cannot
express a sum-based xdy+z roll, so none of PRISM's difficulty numbers
were checkable. Adds keep-best-N support, which Power of Friendship
requires, and locks the spec's balance figures as tests."
```

---

### Task 2: Expose the tool on the mechanics MCP server

**Files:**
- Modify: `mcp_servers/mechanics.py`

**Interfaces:**
- Consumes: `mechanics_ops.calculate_sum_probability` from Task 1
- Produces: MCP tool `calculate_sum_probability`, callable by drafting agents

- [ ] **Step 1: Add the tool wrapper**

In `mcp_servers/mechanics.py`, immediately after the existing `calculate_dice_probability` tool function, add:

```python
@mcp.tool()
def calculate_sum_probability(
    dice: Optional[int] = None,
    sides: Optional[int] = None,
    modifier: int = 0,
    target: Optional[int] = None,
    keep: Optional[int] = None,
) -> str:
    """
    Calculate probability for a sum-based roll (add the dice, add a modifier,
    compare to a target). Use this for xdy+z systems.

    Args:
        dice: How many dice to roll. Defaults to mechanics.dice.count from config.
        sides: Faces per die. Defaults to mechanics.dice.sides from config.
        modifier: Flat bonus added to the kept sum.
        target: Number the total must reach. Defaults to mechanics.dice.default_target.
        keep: How many of the highest dice to add. Defaults to all of them.

    Returns:
        Success chance, expected value, and a margin table.
    """
    return mechanics_ops.calculate_sum_probability(
        dice=dice, sides=sides, modifier=modifier, target=target, keep=keep
    )
```

- [ ] **Step 2: Verify the server still imports**

Run: `python -c "import sys; sys.path.insert(0,'mcp_servers'); import mechanics; print('ok')"`
Expected: prints `ok` with no traceback.

- [ ] **Step 3: Verify the delegation works end to end**

Run:
```bash
python -c "
import sys; sys.path.insert(0,'mcp_servers')
from _lib import mechanics_ops
print(mechanics_ops.calculate_sum_probability(dice=3, sides=6, modifier=1, target=9, keep=2))
"
```
Expected: output beginning `best 2 of 3d6 +1 vs target 9` and reporting `68.1%`.

- [ ] **Step 4: Commit**

```bash
git add mcp_servers/mechanics.py
git commit -m "Expose calculate_sum_probability as an MCP tool"
```

---

### Task 3: Configure Bookbinder for PRISM

**Files:**
- Modify: `config/system.json`
- Modify: `config/README.md`
- Test: `tests/test_prism_config.py`

**Interfaces:**
- Produces: config keys `mechanics.dice.count`, `mechanics.dice.default_target`, `art.generators["ideogram-v4"].sizes`, and PRISM's voice/terminology/layout settings

- [ ] **Step 1: Write the failing test**

Create `tests/test_prism_config.py`:

```python
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
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python -m unittest tests.test_prism_config -v`
Expected: FAIL — `system.name` is still `Generic RPG`.

- [ ] **Step 3: Write the config**

Replace `config/system.json` with:

```json
{
  "system": {
    "name": "PRISM",
    "publisher_line": "",
    "project_type": "core rulebook"
  },
  "voice": {
    "writing_style_file": "styles/writing/prism.md",
    "tone_keywords": ["sugarpop", "sincere", "rainbow", "loud", "kind", "unembarrassed"],
    "banned_phrases": [
      "It's not *, it's *",
      "a testament to",
      "little did they know",
      "delve into",
      "transforms",
      "transforming",
      "to transform",
      "whimsical",
      "quirky",
      "adorkable"
    ],
    "banned_names": ["Elara", "Kael", "Lyra", "Seraphina", "Aria"],
    "use_sparingly": [
      { "term": "tapestry", "max_per_10k_words": 1 },
      { "term": "—", "max_per_10k_words": 20 }
    ]
  },
  "terminology": {
    "gamemaster": "Showrunner",
    "player_character": "Star",
    "supplement": "rulebook"
  },
  "citations": {
    "book_map": {},
    "patterns": ["(?P<book>[A-Z][\\w :']+?),?\\s*p\\.\\s*(?P<page>\\d+)"],
    "bibliography": {}
  },
  "mechanics": {
    "xp_costs": {},
    "dice": {
      "sides": 6,
      "count": 2,
      "default_target": 9,
      "default_difficulty": 6,
      "botch_on_ones": false
    }
  },
  "art": {
    "active_generator": "ideogram-v4",
    "density_words_per_illustration": 2000,
    "generators": {
      "stable-diffusion-1.5": {
        "backend": "a1111",
        "endpoint": "http://127.0.0.1:7860",
        "rules_file": "styles/art/stable-diffusion-1.5.md",
        "style_prefix": "black and white ink illustration, ",
        "negative_prompt": "",
        "sampler": "DPM++ 2S a",
        "scheduler": null,
        "steps": 20,
        "cfg_scale": 7.0,
        "prompt_style": "tags",
        "sizes": {
          "portrait": [512, 512],
          "landscape": [768, 512],
          "column": [384, 768],
          "full_page": [512, 768]
        }
      },
      "ideogram-v4": {
        "backend": "comfyui",
        "endpoint": "http://127.0.0.1:8188",
        "rules_file": "styles/art/ideogram-v4.md",
        "workflow_file": "styles/art/example.workflow.json",
        "style_prefix": "hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, ",
        "negative_prompt": "muted colors, desaturated, grimdark, photorealistic, watermark",
        "prompt_style": "natural",
        "sizes": {
          "portrait": [1024, 1024],
          "landscape": [1536, 1024],
          "column": [768, 1536],
          "full_page": [1024, 1536]
        }
      }
    }
  },
  "layout": {
    "style_file": "styles/layout/prism.md",
    "docx_theme": "prism"
  },
  "knowledge_base": {
    "root": "knowledge_base",
    "top_level_dirs": []
  },
  "skills": {
    "toolkit_skill": ""
  }
}
```

Note `default_difficulty` stays at **6**, not 9: `calculate_dice_probability` validates `3 <= difficulty <= sides`, and with `sides: 6` a value of 9 would make that tool error on its own defaults. PRISM's sum target lives in `default_target`.

- [ ] **Step 4: Update the existing config test**

Two existing tests assert the old configuration and will fail. Success criterion 1
requires the whole suite green, so both are in scope.

`tests/test_config.py` line 11 asserts `"supplement"`:

```python
        self.assertEqual(config.get("system.project_type"), "core rulebook")
```

`tests/test_mechanics.py` line 30 (`test_dice_uses_config_defaults`) asserts the
default pool output contains `5d10`. Changing `mechanics.dice.sides` to 6 makes
that `5d6`:

```python
        self.assertIn("5d6", out)
```

Check the same test's `difficulty 6` assertion still holds — it does, because
`default_difficulty` stays at 6.

Run `python -m unittest tests.test_config tests.test_mechanics -v` and confirm both
pass before moving on.

- [ ] **Step 5: Document the new fields**

In `config/README.md`, find the `mechanics.dice` section and add rows for the two new keys:

```markdown
| `mechanics.dice.count` | How many dice a standard roll uses. Read by `calculate_sum_probability`. | `2` |
| `mechanics.dice.default_target` | Target number a summed roll must reach. Read by `calculate_sum_probability`. Distinct from `default_difficulty`, which is the per-die threshold used by the pool-based `calculate_dice_probability` and must satisfy `3 <= difficulty <= sides`. | `9` |
```

- [ ] **Step 6: Run the config test**

Run: `python -m unittest tests.test_prism_config -v`
Expected: the dice, terminology, art, and system tests PASS. The `layout` and `voice` tests still FAIL — they assert files that Task 4 creates. That is expected; Task 4 finishes them.

- [ ] **Step 7: Commit**

```bash
git add config/system.json config/README.md tests/test_config.py tests/test_mechanics.py tests/test_prism_config.py
git commit -m "Configure Bookbinder for PRISM

Sum-based d6 dice, Showrunner/Star terminology, the Ideogram profile with
the sizes map art-direction requires, and both layout keys moved together.
default_difficulty stays within the legacy pool validator's range so that
tool is not left broken on its own defaults."
```

---

### Task 4: House style assets

`/compile` Step 3 reads `layout.style_file` and confirms it names a real file in `styles/layout/`; `/plan-project` Step 2 reads the writing style; `/plan-project` Step 3 looks for a matching book template. All three must exist.

**Files:**
- Create: `styles/writing/prism.md`
- Create: `styles/templates/core-rulebook.md`
- Create: `styles/layout/prism.md`
- Create: `styles/layout/prism.theme.json`

**Interfaces:**
- Consumes: config keys from Task 3
- Produces: the four files those config keys and the pipeline commands point at

- [ ] **Step 1: Write the voice guide**

Create `styles/writing/prism.md`:

```markdown
# PRISM House Voice

## Voice
Warm, direct, unembarrassed. You are talking to someone who is about to have
a good evening with their friends, and you are glad about it.

## Register
Conversational and plain. Rules text is unfussy and says exactly what happens.
Flavor text is sincere and specific. Never academic, never breathless.

## POV
Second person for rules ("you morph", "you keep the best two dice"). The
Showrunner is addressed directly in Chapter 8. Never "the player may".

## Humor
Present, affectionate, never at the genre's expense. The joke is never that
this game is silly. If a line's punchline is "isn't this ridiculous", cut it.

## Sentence length
Mostly short and declarative. Occasional long enthusiastic ones for the big
moments — a morph, a Flourish, the Combined Form. Vary deliberately.

## Hedging
None. State the rule. If something is a judgement call, say who makes it.

## Sincerity rule
This is the load-bearing one. PRISM plays its genre straight. No irony
quotes, no winking, no "yes, really". A rainbow is just a rainbow here.

## Gender
Transformation is self-expression and is open to every character. Examples
use varied pronouns without comment. Never gender a role, a look, a power,
or a register. Do not remark on this in the text; simply write it that way.

## Terminology (binding — see spec section 8.1)
- **Transformation** — the noun, the phenomenon, the chapter.
- **morph** — the verb. Never "transform" as a verb.
- **transformed** — the adjective, the state.
- **Solo Morph / Synchronized Morph / Combined Form** — the named moves, always capitalized.
- **refract** — crossing into the Spectrum. Refracting and morphing are one act.
- **the everyday / the Spectrum** — the two layers. Never "the real world"; both are real.
- **the Chord** — the Combined Form gate. Stars *sound their note*. Never "meter" or "gauge".
- **Showrunner** — the GM. **Star** — a player character. **Number** — a session.

## Banned
- "transform" as a verb (outside quoted in-world dialogue)
- "whimsical", "quirky", "adorkable"
- "It's not X, it's Y" constructions
- Any sentence that apologizes for the genre

## Sample cadence
> You keep the best two dice. Always two, however many your friends throw in.
> That is the whole trick: help makes you likelier, not bigger.
```

- [ ] **Step 2: Write the book template**

Create `styles/templates/core-rulebook.md`:

```markdown
# Template: Core Rulebook

For a complete standalone game. Assumes the reader owns nothing else and may
never have played a tabletop RPG.

## Required elements
- A pitch in the first 300 words that says what you do in this game
- Safety and consent tools, in Chapter 1, before any rules
- A complete worked example of the core roll
- Character creation with a stated time budget
- Pregenerated characters, ready to play
- A starter adventure
- A one-page quick reference
- A character sheet

## Chapter shape (25,000-word build)
| # | Chapter | Words |
|---|---|---|
| 1 | Welcome / what this is | 1,800 |
| 2 | How to play — the core loop | 3,000 |
| 3 | Making a character | 3,200 |
| 4 | The signature subsystem | 2,800 |
| 5 | Conflict and consequences | 3,000 |
| 6 | Pregenerated characters | 1,800 |
| 7 | Setting | 2,500 |
| 8 | Running the game | 3,300 |
| 9 | Antagonists | 1,900 |
| 10 | Starter adventure + reference | 1,700 |

## Rules
- Tolerance is ±25% per chapter.
- Every rule must be stated once, in one chapter, and cross-referenced elsewhere.
- No rule may be introduced in an example. Examples illustrate; they never define.
- Every number that appears in two places must come from the NPC/entity registry.
```

- [ ] **Step 3: Write the layout language**

Create `styles/layout/prism.md`:

```markdown
# PRISM Layout Style

The design language the `prism` DOCX theme implements. Hyper-saturated,
airbrushed, unafraid.

## Palette
- **Body text**: near-black `1A1A1A` on white. Readability is not negotiable;
  the colour lives in the furniture, not the paragraphs.
- **Accent 1** — magenta `FF2D95`. Chapter numbers, headings, rules.
- **Accent 2** — cyan `00C8F0`. Subheadings, callout rules, table headers.
- **Highlight** — sunburst yellow `FFD400`. Used sparingly, for the moments
  the text is shouting: morphs, Flourishes, the Combined Form.
- **Sidebar ground** — deep violet `2B0B4A`, white text. Sidebars are the
  Spectrum bleeding through the page.
- **Alternating table row** — pale rose `FFF0F7`.

## Typography
- **Headings**: a heavy geometric sans. Wide, confident, slightly oversized.
- **Body**: a humanist serif at a generous size. This is a book for reading
  aloud at a table under bad lighting.
- **Sidebars**: the same sans as headings, one step down.

## Rules of thumb
- Chapter openers get a full-width colour band.
- Stat blocks sit in tinted boxes with a 2pt accent rule at the top.
- Never set body text on a saturated ground.
- Every table gets alternating row shading. Every one.
```

- [ ] **Step 4: Write the DOCX theme data**

Create `styles/layout/prism.theme.json`. The key names must match `styles/layout/default.theme.json` exactly, since `scripts/export-docx.js` reads them positionally by name:

```json
{
  "colors": { "body": "1A1A1A", "accent1": "FF2D95", "accent2": "00C8F0", "gold": "FFD400", "sidebarBg": "2B0B4A", "white": "FFFFFF", "altRow": "FFF0F7" },
  "fonts": { "body": "Georgia", "heading": "Trebuchet MS", "toc": "Trebuchet MS", "header": "Trebuchet MS", "sidebar": "Trebuchet MS" },
  "page": { "w": 12240, "h": 15840, "ml": 1080, "mr": 1080, "mt": 1267, "mb": 1440 }
}
```

- [ ] **Step 5: Verify the theme parses and matches the default's shape**

Run:
```bash
python -c "
import json
a=json.load(open('styles/layout/default.theme.json'))
b=json.load(open('styles/layout/prism.theme.json'))
assert a.keys()==b.keys(), (a.keys(), b.keys())
for k in a: assert a[k].keys()==b[k].keys(), (k, a[k].keys(), b[k].keys())
print('theme schema matches default')
"
```
Expected: prints `theme schema matches default`.

- [ ] **Step 6: Run the config test, now complete**

Run: `python -m unittest tests.test_prism_config -v`
Expected: PASS, all tests including `test_layout_keys_move_together` and `test_voice_points_at_the_prism_guide`.

- [ ] **Step 7: Run the whole suite**

Run: `python -m unittest discover tests -v`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add styles/writing/prism.md styles/templates/core-rulebook.md styles/layout/prism.md styles/layout/prism.theme.json
git commit -m "Add PRISM house style, book template, and layout theme

Voice guide carries the binding terminology from spec section 8.1. Theme
key names mirror default.theme.json, which export-docx.js reads by name."
```

---

### Task 5: Correct the drafting prompts

Two shipped prompts route balance work to the dice-pool model. Left alone, the drafting agents would validate PRISM against a tool the spec says cannot express it.

**Files:**
- Modify: `.claude/commands/first-draft.md` (line 41)
- Modify: `.claude/agents/book-creation/mechanics-designer.md` (lines 78 and 111)

- [ ] **Step 1: Fix the first-draft command**

In `.claude/commands/first-draft.md`, replace line 41:

```markdown
  - Balance calculations for new powers, traits, or items (dice math via `calculate_dice_probability`/`calculate_extended_action`, XP cost derivation via `calculate_experience_cost`)
```

with:

```markdown
  - Balance calculations for new powers, traits, or items. Use `calculate_sum_probability` for any sum-based (xdy+z) system; use `calculate_dice_probability`/`calculate_extended_action` only for dice-pool systems that count successes. Check `mechanics.dice` in `config/system.json` to see which this project is. XP cost derivation via `calculate_experience_cost`.
```

- [ ] **Step 2: Fix the mechanics-designer agent's tool recommendation**

In `.claude/agents/book-creation/mechanics-designer.md`, replace line 111:

```markdown
- Use `calculate_dice_probability` for dice pool balance testing rather than guessing
```

with:

```markdown
- Use the probability tools rather than guessing. For sum-based (xdy+z) systems use `calculate_sum_probability`; for dice-pool systems that count successes use `calculate_dice_probability`. `config/system.json` → `mechanics.dice` tells you which this project uses.
```

- [ ] **Step 3: Fix the success-threshold guidance**

In the same file, replace line 78:

```markdown
- **Success Thresholds**: Match complexity to required successes (Simple=1, Complex=3-5, Extreme=10+)
```

with:

```markdown
- **Difficulty**: Match complexity to the system's difficulty bands. For a dice-pool system that is required successes (Simple=1, Complex=3-5, Extreme=10+). For a sum-based system it is the target number — in PRISM, 6 (Easy) / 9 (Tricky) / 11 (Dazzling). Never invent a band that is unreachable at the system's maximum roll; check with the probability tool first.
```

- [ ] **Step 4: Verify no stale pointers remain**

Run:
```bash
grep -rn "calculate_dice_probability" .claude/ | grep -v "calculate_sum_probability"
```
Expected: no output. Every remaining mention sits beside the sum-based alternative.

- [ ] **Step 5: Commit**

```bash
git add .claude/commands/first-draft.md .claude/agents/book-creation/mechanics-designer.md
git commit -m "Point drafting prompts at the right probability model

Both prompts sent balance work to the pool-based calculator, which cannot
express a sum-based roll, and mandated success-count thresholds that are
meaningless in PRISM."
```

---

### Task 6: PRISM's canon documents

The reference-librarian role needs something to check internal consistency against. `.gitignore` was already amended on this branch so `references/prism/` is tracked.

**Files:**
- Create: `references/prism/00-core-rules.md`
- Create: `references/prism/01-terminology.md`
- Create: `references/prism/02-probability.md`

- [ ] **Step 1: Extract the rules reference**

Create `references/prism/00-core-rules.md` containing, verbatim from spec sections 2.1–2.7, 3, 4, and 5: the roll, the Difficulty table, the outcome ladder, Sparkle, Power of Friendship, Shine and Gloom, Mixed costs, beating a Gloom, the six character elements, the three morph gears, the Chord, and the song structure. This is a lookup document, not prose — tables and bullet lists only.

- [ ] **Step 2: Extract the terminology reference**

Create `references/prism/01-terminology.md` containing the terminology table from spec section 8.1 verbatim, plus a glossary of every capitalized game term: Star, Showrunner, Number, Trait, Refrain, Signature, Bond, Look, Radiance, Sparkle, Shine, Gloom, the Chord, the Spectrum, the everyday, Solo Morph, Synchronized Morph, Combined Form, Verse, Chorus, Bridge, Big Finish, Encore, Dimmed, Flourish, Finisher.

- [ ] **Step 3: Generate the probability reference**

Create `references/prism/02-probability.md` from actual tool output rather than by hand:

```bash
python - <<'PY' > references/prism/02-probability.md
import sys; sys.path.insert(0, "mcp_servers")
from _lib import mechanics_ops as m
print("# PRISM Probability Reference\n")
print("Generated from `calculate_sum_probability`. Do not hand-edit.\n")
for label, dc in [("Easy", 6), ("Tricky", 9), ("Dazzling", 11)]:
    print(f"## {label} — Difficulty {dc}\n")
    print("| Trait | 0 backers | 1 | 2 | 3 |")
    print("|---|---|---|---|---|")
    for trait in range(0, 3):
        cells = []
        for b in range(4):
            dist = m._sum_distribution(2 + b, 6, 2)
            tot = sum(dist.values())
            hit = sum(c for s, c in dist.items() if s + trait >= dc)
            cells.append(f"{100.0*hit/tot:.1f}%")
        print(f"| +{trait} | " + " | ".join(cells) + " |")
    print()
PY
```

- [ ] **Step 4: Verify the files are tracked, not ignored**

Run: `git status --porcelain references/prism/`
Expected: three `??` lines. If you see none, `.gitignore` is re-excluding them — check that it reads `references/*` and not `references/**`.

- [ ] **Step 5: Commit**

```bash
git add references/prism/
git commit -m "Add PRISM canon documents for consistency checking"
```

---

### Task 7: Initialize the project (Phase 0)

**Files:**
- Create: `projects/prism/**` (created by the command)

- [ ] **Step 1: Run the command**

Run: `/init-project prism`

When it asks for a title, answer **PRISM**. Accept the default directory layout.

- [ ] **Step 2: Record the natural title**

`initialize_project` stores only the slug, under `project_info.name`. But
`/compile` (line 120) and `build_triple_spaced.py` (line 139) both read a
**root-level `project_title`** to derive the editing PDF's filename. Without it,
compilation is missing a required input. Set it now:

```bash
python - <<'PYEOF'
import json
p = "projects/prism/state/project_state.json"
d = json.load(open(p))
d["project_title"] = "PRISM"
json.dump(d, open(p, "w"), indent=2)
print("project_title:", d["project_title"])
PYEOF
```

- [ ] **Step 3: Verify the skeleton**

Run:
```bash
ls -R projects/prism | head -40
python -c "
import json; d=json.load(open('projects/prism/state/project_state.json'))
print('phase:', d.get('project_info', {}).get('current_phase'))
print('title:', d.get('project_title'))
"
```
Expected: `state/`, `content/`, `development/`, `notes/`, `output/` all present, the
three state files exist, phase prints `initialization` (**not** `None` — the phase
lives under `project_info`, not at the state root), and title prints `PRISM`.

- [ ] **Step 4: Commit**

```bash
git add projects/prism
git commit -m "Initialize PRISM project workspace"
```

---

### Task 8: Plan the book (Phase 1)

**Files:**
- Create: `projects/prism/development/outlines/*`, `projects/prism/development/concepts/*`

- [ ] **Step 1: Run the command**

Run: `/plan-project prism`

At **Step 2 (writing style)**, choose **Path A — pick an existing writing style** and select `styles/writing/prism.md`. Do not re-derive the voice; it is already written and the config points at it.

At **Step 3 (structure)**, use `styles/templates/core-rulebook.md` and the chapter table from spec section 7 exactly:

| # | Chapter | Words |
|---|---|---|
| 1 | Welcome to the Show | 1,800 |
| 2 | How to Play | 3,000 |
| 3 | Making a Star | 3,200 |
| 4 | Transformation | 2,800 |
| 5 | Trouble | 3,000 |
| 6 | Five Stars, Ready to Play | 1,800 |
| 7 | Your Town and the Spectrum | 2,500 |
| 8 | Running the Game | 3,300 |
| 9 | The Gloom | 1,900 |
| 10 | The First Number | 1,700 |

At **Step 5 (reference foundation)**, point the librarian at `references/prism/`.

At **Step 6**, `premise.md` and `themes.md` are gate requirements. Also write `tone.md` (Lisa Frank, ABBA/Aqua, sentai, MLP; sincere not ironic) and `setting.md` (the everyday and the Spectrum; the conversion procedure).

- [ ] **Step 2: Verify the gate requirements exist**

Run:
```bash
ls projects/prism/development/concepts/
ls projects/prism/development/outlines/
```
Expected: `premise.md` and `themes.md` at minimum in `concepts/`; `supplement_outline.md`, `writing_style.md`, `heading_id_registry.md`, `npc_registry.md`, and `forbidden_patterns.md` in `outlines/`.

- [ ] **Step 3: Add the terminology entries to the forbidden-patterns list**

Append to `projects/prism/development/outlines/forbidden_patterns.md`:

```markdown
## Terminology violations (spec section 8.1)
Matched as whole words, so `transformation` and `transformed` — both correct —
are not caught by the `transform` entry.
- `transform`
- `transforms`
- `transforming`
- `combined form` (lowercase — must be `Combined Form`)
- `solo morph` (lowercase — must be `Solo Morph`)
- `synchronized morph` (lowercase — must be `Synchronized Morph`)
- `Gamemaster` (must be `Showrunner`)

## Out-of-range values
- `Difficulty 12` (Dazzling is 11)

## Review flags — not automatic rejections
**These must NOT be added to the hard-reject sections above.** `/final-draft`
treats every entry in this file with zero tolerance and fails the gate on any
match, so a term the book is required to use once cannot be listed as forbidden.
- `+3` — a Trait of +3 is forbidden, but "+3" appears innocently in a margin
  table or in "3 backers" phrasing. Check what it modifies.
- `player character` — forbidden as PRISM's term for a Star, but Chapter 1 must
  explain to a newcomer what a player character *is* before the book renames them
  Stars. That one use is correct and required; every other one is wrong. Listing
  it above would make a correct draft unable to pass Phase 5.
```

- [ ] **Step 4: Verify word targets sum correctly**

Run:
```bash
python -c "
import json; d=json.load(open('projects/prism/state/project_state.json'))
t=d.get('word_count_targets', {})
print(t); print('total:', sum(v if isinstance(v,int) else v.get('target',0) for v in t.values()))
"
```
Expected: total 25,000 (±0 — these are targets, not results).

- [ ] **Step 5: Commit**

```bash
git add projects/prism
git commit -m "Plan PRISM structure: 10 chapters, 25,000 words"
```

---

### Task 9: First drafts (Phase 2)

- [ ] **Step 1: Confirm the previous gate passed**

Run: `python -c "
import json; d=json.load(open('projects/prism/state/project_state.json'))
print(d.get('project_info', {}).get('current_phase'))
"`
Expected: `planning_complete`. Read it from `project_info` — a top-level lookup
returns `None` and would falsely look like the gate had not been passed.

- [ ] **Step 2: Run the command**

Run: `/first-draft prism`

Every drafting pass must read `styles/writing/prism.md`, `references/prism/00-core-rules.md`, and `references/prism/01-terminology.md` before writing. All mechanical claims go through `calculate_sum_probability` — no invented probabilities.

- [ ] **Step 3: Verify every chapter drafted**

Run:
```bash
for i in $(seq -w 1 10); do
  f="projects/prism/content/chapter_$i/draft_01.md"
  printf "%s %s words\n" "$f" "$([ -f "$f" ] && wc -w < "$f" || echo MISSING)"
done
```
Expected: ten files, each within ±25% of its target from Task 8.

- [ ] **Step 4: Check the hard constraints early**

Run:
```bash
grep -rnE "\+3|Difficulty 12|Gamemaster|transform(s|ing)" projects/prism/content/ || echo "clean"
```
Expected: `clean`. Anything found is a constraint violation — fix it now rather than at final draft, where it is ten times the work.

- [ ] **Step 5: Commit**

```bash
git add projects/prism
git commit -m "PRISM first drafts: all ten chapters"
```

---

### Task 10: Architectural review (Phase 3)

- [ ] **Step 1: Run the command**

Run: `/architect-review prism`

- [ ] **Step 2: Verify commentary was produced**

Run: `ls projects/prism/development/review_feedback/`
Expected: per-chapter feedback files.

- [ ] **Step 3: Commit**

```bash
git add projects/prism
git commit -m "PRISM architectural review"
```

---

### Task 11: Second drafts (Phase 4)

- [ ] **Step 1: Run the command**

Run: `/second-draft prism`

- [ ] **Step 2: Verify every chapter advanced**

Run:
```bash
for i in $(seq -w 1 10); do
  f="projects/prism/content/chapter_$i/draft_02.md"
  printf "%s %s words\n" "$f" "$([ -f "$f" ] && wc -w < "$f" || echo MISSING)"
done
```
Expected: ten `draft_02.md` files.

- [ ] **Step 3: Commit**

```bash
git add projects/prism
git commit -m "PRISM second drafts: comments integrated, copy edited"
```

---

### Task 12: Final drafts and deferred art direction (Phase 5)

`/final-draft` invokes `/art-direction` at its Step 2. Because `ideogram-v4` is a `comfyui` profile and the mode probe only speaks to a1111 backends, it will fall back to Prompt Manifest Mode on its own. Do not force Generation Mode — no image models are available.

- [ ] **Step 1: Run the command**

Run: `/final-draft prism`

- [ ] **Step 2: Verify final drafts and the art manifest**

Run:
```bash
for i in $(seq -w 1 10); do
  f="projects/prism/content/chapter_$i/final_draft.md"
  printf "%s %s words\n" "$f" "$([ -f "$f" ] && wc -w < "$f" || echo MISSING)"
done
echo "--- art ---"
ls projects/prism/development/art_prompts.md
python -c "
import json; d=json.load(open('projects/prism/development/art_manifest.json'))
imgs=d.get('images', d.get('artwork', []))
print('entries:', len(imgs))
print('all prompt_only:', all(i.get('source')=='prompt_only' for i in imgs))
"
echo '--- no image files should exist ---'
ls projects/prism/content/art/*.png 2>/dev/null && echo "UNEXPECTED IMAGES" || echo "no images, correct"
```
Expected: ten `final_draft.md` files; `art_prompts.md` present; **roughly 30**
manifest entries, every one `source="prompt_only"`; no `.png` files.

The count is 1 cover + 10 chapter openers + `ceil(25,000 / 2,000)` = 13 content
illustrations + one portrait per major NPC. It is *not* just the density division —
that governs content illustrations alone.

- [ ] **Step 3: Run the forbidden-patterns sweep**

Run:
```bash
# Only the hard-reject sections; stop at the "Review flags" heading.
sed '/^## Review flags/,$d' projects/prism/development/outlines/forbidden_patterns.md \
| while IFS= read -r pat; do
  case "$pat" in -\ \`*) p=$(printf '%s' "$pat" | sed 's/^- `//; s/`.*$//')
    # -w so `transform` does not match the correct words `transformed`/`transformation`.
    if grep -rnw -F "$p" projects/prism/content/*/final_draft.md >/dev/null 2>&1; then
      echo "VIOLATION: $p"; grep -rnw -F "$p" projects/prism/content/*/final_draft.md | head -3
    fi ;;
  esac
done
echo "sweep complete"
```

Whole-word matching is essential here: without `-w`, the `transform` entry would
flag every correct use of `transformation` and `transformed` and the sweep would be
unusable.
Expected: `sweep complete` with no `VIOLATION` lines from the hard-reject
sections. Hits under **Review flags** are not automatic failures — read each
in context and decide. A `+3` in a margin table is fine; a `+3` Trait is not.

- [ ] **Step 4: Verify the pregenerated Stars are complete and playable**

Spec success criterion 8 is that a table can open to Chapter 6, take a Star
each, and play. Check the chapter actually delivers five usable characters:

```bash
f=projects/prism/content/chapter_06/final_draft.md
echo "Stars found:      $(grep -cE '^### ' "$f")            (expect 5)"
for field in Refrain Signature Bond Look Radiance; do
  printf "%-12s appears %s times (expect >=5)\n" "$field" "$(grep -cw "$field" "$f")"
done
echo "Command word:     $(grep -ci 'command word' "$f")     (expect >=1, shared by the team)"
echo "Traits above +2:  $(grep -oE '\+[3-9]' "$f" | wc -l)  (expect 0)"
```
Expected: five Stars, each with all five fields, one shared command word, and
no Trait above +2.

- [ ] **Step 5: Verify the total word count**

Run: `cat projects/prism/content/*/final_draft.md | wc -w`
Expected: 18,750–31,250 (25,000 ±25%).

- [ ] **Step 6: Commit**

```bash
git add projects/prism
git commit -m "PRISM final drafts and deferred art prompt manifest"
```

---

### Task 13: Compile (Phase 6)

- [ ] **Step 1: Run the command**

Run: `/compile prism`

Expect a loud coverless-output warning. That is the correct outcome — `content/art/cover.png` does not exist and will not. Do not run `/art-direction` in generation mode to satisfy it.

- [ ] **Step 2: Verify the compiled manuscript**

Run:
```bash
ls -la projects/prism/output/
wc -w projects/prism/output/compiled_supplement.md
# Count links inside the TOC block only — a rulebook has many level-two headings
# in its chapter bodies, so counting every "## " would massively overcount.
awk '/^## Table of Contents/{t=1; next} t && /^## /{exit} t' \
  projects/prism/output/compiled_supplement.md | grep -cE '^\s*[-*0-9]+\.?\s*\['
```
Expected: `compiled_supplement.md` exists, word count in the 18,750–31,250 band, and
the TOC block contains **10** chapter links. If the TOC heading is worded
differently, adjust the `awk` pattern to match it rather than falling back to
counting every heading.

- [ ] **Step 3: Verify no image references survived**

Run: `grep -nE '!\[.*\]\(.*\.(png|jpg)\)' projects/prism/output/compiled_supplement.md || echo "no image refs, as expected"`
Expected: `no image refs, as expected` — compile strips them when the prompt manifest exists.

- [ ] **Step 4: Final forbidden-patterns check on the compiled output**

Run:
```bash
grep -nE 'TODO|TBD|FIXME|PLACEHOLDER|p\. XX|page XX|ARCHITECT COMMENT|<!-- |Draft Notes:|Word Count:' \
  projects/prism/output/compiled_supplement.md || echo "compiled output is clean"
```
Expected: `compiled output is clean`.

- [ ] **Step 5: Run the whole test suite one last time**

Run: `python -m unittest discover tests -v`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add projects/prism
git commit -m "Compile PRISM core rulebook

Ten chapters assembled with a working table of contents and no forbidden
patterns. No images: art ships as a deferred prompt manifest."
```

---

## Notes for the executor

- **Task 3's test fails partway on purpose.** Two of its assertions depend on files Task 4 creates. Run Tasks 3 and 4 in order and it resolves.
- **Never satisfy the missing cover** by running art generation. The coverless warning is the expected end state.
- **If a chapter lands outside ±25%**, use the word-count-manager role to rebalance against its neighbours rather than padding. Total is the binding number.
- **If the Codex review bot comments on the PR**, verify each finding against the repo before acting — it has been right on every finding so far in this project, including two the human reviewers missed.
