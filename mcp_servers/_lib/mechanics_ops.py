"""
Generic dice-pool mechanics operations — shared implementations.
Dice probability, XP costs, combat soak, random tables.
"""

import math
from collections import defaultdict
from itertools import product
from typing import Optional

from . import config


# =========================================================================
# DICE PROBABILITY
# =========================================================================

def calculate_dice_probability(
    dice_pool: int,
    difficulty: Optional[int] = None,
    target_successes: int = 1
) -> str:
    """
    Calculate probability outcomes for a dice-pool roll.

    Args:
        dice_pool: Number of dice in the pool (1-20)
        difficulty: Target number a die must meet to count as a success.
            Defaults to mechanics.dice.default_difficulty from config.
        target_successes: Minimum successes needed

    Returns:
        Probability analysis including success, failure, botch chances and expected successes.
    """
    sides = config.get("mechanics.dice.sides", 10)
    if difficulty is None:
        difficulty = config.get("mechanics.dice.default_difficulty", 6)

    if dice_pool <= 0 or dice_pool > 20:
        return "Error: dice_pool must be between 1 and 20"
    if difficulty < 3 or difficulty > sides:
        return f"Error: difficulty must be between 3 and {sides}"

    botch_on_ones = config.get("mechanics.dice.botch_on_ones", True)
    p_success = (sides - difficulty + 1) / sides
    p_botch = 1 / sides if botch_on_ones else 0.0
    # When ones botch, the 1 face is counted separately from plain failures.
    # When they don't, ones join the failure bucket so probabilities sum to 1.
    p_failure = (difficulty - 2) / sides if botch_on_ones else (difficulty - 1) / sides

    # Build probability distribution over NET successes (gross - botches).
    # Each die showing a botch face cancels one success.
    # Net range: -dice_pool (all botches) to +dice_pool (all successes).
    net_probs = {}
    botch_prob = 0.0
    for successes in range(0, dice_pool + 1):
        botch_range = range(0, dice_pool - successes + 1) if p_botch > 0 else [0]
        for botches in botch_range:
            failures = dice_pool - successes - botches
            if failures < 0:
                continue
            coeff = math.factorial(dice_pool) / (
                math.factorial(successes) *
                math.factorial(failures) *
                math.factorial(botches)
            )
            prob = coeff * (p_success**successes) * (p_failure**failures) * (p_botch**botches)
            net = successes - botches
            net_probs[net] = net_probs.get(net, 0.0) + prob
            # Botch: zero successes rolled AND at least one botch face
            if successes == 0 and botches > 0:
                botch_prob += prob

    # Collapse to non-negative net successes for display
    success_probs = {}
    for net, prob in net_probs.items():
        display_key = max(0, net)
        success_probs[display_key] = success_probs.get(display_key, 0.0) + prob

    prob_at_least_target = sum(
        prob for net, prob in net_probs.items() if net >= target_successes
    )
    expected = sum(net * prob for net, prob in net_probs.items())

    lines = [
        f"Dice Pool Analysis: {dice_pool}d{sides} vs difficulty {difficulty}",
        f"Target: {target_successes}+ net successes",
        "",
        f"Success probability: {prob_at_least_target:.1%}",
        f"Botch probability: {botch_prob:.1%}",
        f"Expected net successes: {expected:.2f}",
        "",
        "Net success distribution:"
    ]

    for s in range(min(6, dice_pool + 1)):
        p = success_probs.get(s, 0.0)
        bar = "#" * int(p * 40)
        lines.append(f"  {s} successes: {p:5.1%} {bar}")

    if dice_pool > 5:
        remaining = sum(success_probs.get(s, 0.0) for s in range(6, dice_pool + 1))
        lines.append(f"  6+ successes: {remaining:5.1%}")

    return "\n".join(lines)


def calculate_extended_action(
    dice_pool: int,
    difficulty: int,
    target_successes: int,
    max_rolls: int = 10
) -> str:
    """
    Calculate probability of success in extended actions.

    Args:
        dice_pool: Number of dice per roll
        difficulty: Target number a die must meet to count as a success
        target_successes: Total successes needed
        max_rolls: Maximum number of rolls allowed

    Returns:
        Analysis of extended action success probability and expected rolls.
    """
    sides = config.get("mechanics.dice.sides", 10)
    if dice_pool <= 0 or difficulty < 3 or difficulty > sides:
        return "Error: Invalid parameters"

    p_success = (sides - difficulty + 1) / sides
    expected_per_roll = dice_pool * p_success

    if expected_per_roll <= 0:
        return "Extended action impossible: no expected successes per roll"

    expected_rolls = target_successes / expected_per_roll

    # Binomial CDF: total dice across all rolls, each independently succeeding.
    # P(total successes >= target) = 1 - P(total successes <= target - 1)
    total_dice = dice_pool * max_rolls
    # Use normal approximation to the binomial (no scipy dependency)
    mu = total_dice * p_success
    sigma = math.sqrt(total_dice * p_success * (1 - p_success))
    if sigma > 0:
        # Continuity-corrected normal approximation
        z = (target_successes - 0.5 - mu) / sigma
        # Standard normal CDF via error function
        completion_prob = 0.5 * (1 + math.erf(-z / math.sqrt(2)))
    else:
        completion_prob = 1.0 if mu >= target_successes else 0.0

    lines = [
        f"Extended Action: {target_successes} successes needed",
        f"Rolling {dice_pool}d{sides} vs difficulty {difficulty}",
        f"Maximum {max_rolls} rolls allowed",
        "",
        f"Expected successes/roll: {expected_per_roll:.2f}",
        f"Expected rolls to complete: {expected_rolls:.1f}",
        f"Total dice across {max_rolls} rolls: {total_dice}",
        f"Completion probability: {completion_prob:.1%}",
        "",
        f"{'LIKELY' if expected_rolls <= max_rolls else 'UNLIKELY'} to complete within limit"
    ]

    return "\n".join(lines)


# =========================================================================
# EXPERIENCE COSTS
# =========================================================================

def calculate_experience_cost(
    trait_type: str,
    current_level: int,
    target_level: int,
) -> str:
    """
    Calculate experience point costs for character advancement.

    Args:
        trait_type: A trait category configured in mechanics.xp_costs
            (e.g. 'attribute', 'skill', 'power')
        current_level: Current trait level
        target_level: Desired trait level

    Returns:
        Detailed XP cost breakdown with level-by-level costs.
    """
    if target_level <= current_level:
        return "No XP needed: target is not higher than current"

    cost_multipliers = config.get("mechanics.xp_costs", {})
    if not cost_multipliers:
        return (
            "No XP cost table configured. Add mechanics.xp_costs to "
            "config/system.json (trait -> multiplier; cost per level = "
            "(level-1) x multiplier). See config/README.md."
        )

    trait_lower = trait_type.lower()
    if trait_lower not in cost_multipliers:
        return f"Error: Unknown trait type '{trait_type}'. Valid: {list(cost_multipliers.keys())}"

    multiplier = cost_multipliers[trait_lower]
    breakdown = []
    total = 0

    for level in range(current_level + 1, target_level + 1):
        cost = (level - 1) * multiplier
        breakdown.append(f"  {level - 1} -> {level}: {cost} XP")
        total += cost

    lines = [
        f"Experience Cost: {trait_type.title()}",
        f"From level {current_level} to {target_level}",
        "",
        "Breakdown:",
        *breakdown,
        "",
        f"TOTAL: {total} XP"
    ]

    return "\n".join(lines)


# =========================================================================
# COMBAT
# =========================================================================

def calculate_damage_soak(
    stamina: int,
    armor_rating: int = 0,
    damage_type: str = "bashing"
) -> str:
    """
    Calculate damage soak pools for dice-pool systems (bashing/lethal/aggravated
    damage model).

    Args:
        stamina: Character's Stamina rating (1-5)
        armor_rating: Armor protection value (0-5)
        damage_type: 'bashing', 'lethal', or 'aggravated'

    Returns:
        Soak pool information and dice to roll.
    """
    damage_type = damage_type.lower()
    if damage_type not in ["bashing", "lethal", "aggravated"]:
        return "Error: Invalid damage type. Use 'bashing', 'lethal', or 'aggravated'"

    if damage_type == "bashing":
        soak_pool = stamina + armor_rating
        soak_source = f"Stamina ({stamina}) + Armor ({armor_rating})"
    elif damage_type == "lethal":
        soak_pool = armor_rating
        soak_source = f"Armor only ({armor_rating})"
    else:
        soak_pool = 0
        soak_source = "None (aggravated cannot be soaked normally)"

    default_difficulty = config.get("mechanics.dice.default_difficulty", 6)

    lines = [
        f"Soak Calculation: {damage_type.title()} Damage",
        f"Stamina: {stamina} | Armor: {armor_rating}",
        "",
        f"Soak source: {soak_source}",
        f"SOAK POOL: {soak_pool} dice",
        f"Roll difficulty: {default_difficulty}",
        "",
        f"Expected damage soaked: {soak_pool * 0.5:.1f}" if soak_pool > 0 else "No soak possible"
    ]

    return "\n".join(lines)


# =========================================================================
# RANDOM TABLE GENERATION
# =========================================================================

def generate_random_table(
    entries: str,
    dice_type: str = "d10"
) -> str:
    """
    Generate a formatted random table for supplements.

    Args:
        entries: Comma-separated list of table entries
        dice_type: Type of dice to use ('d6', 'd10', 'd20', 'd100')

    Returns:
        Formatted random table with dice ranges assigned to each entry.
    """
    dice_ranges = {"d6": 6, "d10": 10, "d20": 20, "d100": 100}

    if dice_type not in dice_ranges:
        return f"Error: Unsupported dice type. Use: {list(dice_ranges.keys())}"

    entry_list = [e.strip() for e in entries.split(",") if e.strip()]
    max_value = dice_ranges[dice_type]

    if len(entry_list) > max_value:
        return f"Error: Too many entries ({len(entry_list)}) for {dice_type} ({max_value})"

    if not entry_list:
        return "Error: No entries provided"

    range_per_entry = max_value // len(entry_list)
    remainder = max_value % len(entry_list)

    lines = [
        f"Random Table ({dice_type})",
        f"Roll {dice_type} and consult below:",
        "",
        f"{'Roll':<12} Result",
        "-" * 50
    ]

    current_min = 1
    for i, entry in enumerate(entry_list):
        current_max = current_min + range_per_entry - 1
        if i < remainder:
            current_max += 1

        range_text = str(current_min) if current_min == current_max else f"{current_min}-{current_max}"
        lines.append(f"{range_text:<12} {entry}")
        current_min = current_max + 1

    return "\n".join(lines)


# =========================================================================
# SUM-BASED DICE PROBABILITY
# =========================================================================

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
        Success chance, expected value, a margin table, and the chance that
        every kept die shows the maximum face.
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
