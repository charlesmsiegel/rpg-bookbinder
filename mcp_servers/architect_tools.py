#!/usr/bin/env python3
"""
Project Architect MCP Server
Per-agent server: full state authority + word counting + compilation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import project_ops, content_ops

mcp = FastMCP("Architect Tools")

# -- Full project state authority --
mcp.tool()(project_ops.initialize_project)
mcp.tool()(project_ops.list_projects)
mcp.tool()(project_ops.get_active_project)
mcp.tool()(project_ops.get_project_status)
mcp.tool()(project_ops.update_project_state)
mcp.tool()(project_ops.set_project_phase)
mcp.tool()(project_ops.mark_agent_active)
mcp.tool()(project_ops.mark_agent_complete)
mcp.tool()(project_ops.get_active_agents)
mcp.tool()(project_ops.pass_quality_gate)
mcp.tool()(project_ops.check_quality_gates)
mcp.tool()(project_ops.log_agent_message)
mcp.tool()(project_ops.get_recent_messages)

# -- Word counting & compilation --
mcp.tool()(content_ops.count_words)
mcp.tool()(content_ops.count_words_in_directory)
mcp.tool()(content_ops.check_word_targets)
mcp.tool()(content_ops.track_chapter_progress)
mcp.tool()(content_ops.estimate_reading_time)
mcp.tool()(content_ops.analyze_content_density)
mcp.tool()(content_ops.compile_supplement)
mcp.tool()(content_ops.generate_toc)

if __name__ == "__main__":
    mcp.run()
