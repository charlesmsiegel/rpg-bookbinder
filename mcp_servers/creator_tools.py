#!/usr/bin/env python3
"""
Content Creator MCP Server
Per-agent server: mechanics + lore + signature content. Balance calculators + inline canon checks.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import project_ops, content_ops, mechanics_ops, reference_ops

mcp = FastMCP("Creator Tools")

# -- Project awareness (read-only + logging) --
mcp.tool()(project_ops.get_active_project)
mcp.tool()(project_ops.get_project_status)
mcp.tool()(project_ops.log_agent_message)

# -- Word count targets (stay on target while writing) --
mcp.tool()(content_ops.count_words)
mcp.tool()(content_ops.check_word_targets)
mcp.tool()(content_ops.check_banned_terms)

# -- All mechanics calculators --
mcp.tool()(mechanics_ops.calculate_dice_probability)
mcp.tool()(mechanics_ops.calculate_extended_action)
mcp.tool()(mechanics_ops.calculate_experience_cost)
mcp.tool()(mechanics_ops.calculate_damage_soak)
mcp.tool()(mechanics_ops.generate_random_table)

# -- Reference lookups for inline canon checks --
mcp.tool()(reference_ops.search_references)
mcp.tool()(reference_ops.list_reference_books)
mcp.tool()(reference_ops.extract_citations)

if __name__ == "__main__":
    mcp.run()
