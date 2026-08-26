#!/usr/bin/env python3
"""
Mechanics MCP Server
FastMCP server for generic dice-pool game calculations.

Tools for:
- Dice probability calculations
- Experience point costs
- Damage and soak calculations
- Random table generation
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import mechanics_ops

mcp = FastMCP("Mechanics")


# =============================================================================
# DICE PROBABILITY TOOLS
# =============================================================================

@mcp.tool()
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
    return mechanics_ops.calculate_dice_probability(dice_pool, difficulty, target_successes)


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
        Success chance, expected value, a margin table, and the chance that
        every kept die shows the maximum face.
    """
    return mechanics_ops.calculate_sum_probability(
        dice=dice, sides=sides, modifier=modifier, target=target, keep=keep
    )


@mcp.tool()
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
    return mechanics_ops.calculate_extended_action(dice_pool, difficulty, target_successes, max_rolls)


# =============================================================================
# EXPERIENCE COST TOOLS
# =============================================================================

@mcp.tool()
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
    return mechanics_ops.calculate_experience_cost(trait_type, current_level, target_level)


# =============================================================================
# COMBAT TOOLS
# =============================================================================

@mcp.tool()
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
    return mechanics_ops.calculate_damage_soak(stamina, armor_rating, damage_type)


# =============================================================================
# RANDOM TABLE GENERATION
# =============================================================================

@mcp.tool()
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
    return mechanics_ops.generate_random_table(entries, dice_type)


if __name__ == "__main__":
    mcp.run()
