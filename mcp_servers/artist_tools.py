#!/usr/bin/env python3
"""
Art Director MCP Server
Per-agent server: full art generation authority.
Style, backend, and endpoint come from the active generator profile in
config/system.json (art.active_generator / art.generators).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import project_ops, art_ops

mcp = FastMCP("Artist Tools")

# -- Project awareness (read-only + logging) --
mcp.tool()(project_ops.get_active_project)
mcp.tool()(project_ops.get_project_status)
mcp.tool()(project_ops.log_agent_message)

# -- Illustration generation (active backend from config) --
mcp.tool()(art_ops.txt2img)
mcp.tool()(art_ops.img2img)
mcp.tool()(art_ops.upscale)
mcp.tool()(art_ops.generate_portrait)
mcp.tool()(art_ops.generate_landscape)
mcp.tool()(art_ops.generate_column_image)
mcp.tool()(art_ops.generate_full_page)

# -- Prompt building --
mcp.tool()(art_ops.generate_art_prompt)

# -- API status --
mcp.tool()(art_ops.get_progress)
mcp.tool()(art_ops.get_models)
mcp.tool()(art_ops.get_samplers)
mcp.tool()(art_ops.get_upscalers)
mcp.tool()(art_ops.get_loras)
mcp.tool()(art_ops.get_options)
mcp.tool()(art_ops.set_options)
mcp.tool()(art_ops.interrogate)
mcp.tool()(art_ops.png_info)
mcp.tool()(art_ops.interrupt)
mcp.tool()(art_ops.skip)
mcp.tool()(art_ops.refresh_checkpoints)
mcp.tool()(art_ops.get_embeddings)
mcp.tool()(art_ops.get_memory)

# -- Art manifest management --
mcp.tool()(art_ops.update_art_manifest)
mcp.tool()(art_ops.list_art_manifest)
mcp.tool()(art_ops.generate_attribution)

if __name__ == "__main__":
    mcp.run()
