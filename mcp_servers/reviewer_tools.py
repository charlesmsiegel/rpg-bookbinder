#!/usr/bin/env python3
"""
Quality Reviewer MCP Server
Per-agent server: copy editing + consistency checking + final review.
Quantitative analysis + citation auditing + canon verification.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import project_ops, content_ops, reference_ops, kb_ops

mcp = FastMCP("Reviewer Tools")

# -- Project state (read + gate approval) --
mcp.tool()(project_ops.get_active_project)
mcp.tool()(project_ops.get_project_status)
mcp.tool()(project_ops.pass_quality_gate)
mcp.tool()(project_ops.log_agent_message)

# -- Quantitative content analysis --
mcp.tool()(content_ops.count_words)
mcp.tool()(content_ops.check_word_targets)
mcp.tool()(content_ops.analyze_content_density)
mcp.tool()(content_ops.estimate_reading_time)
mcp.tool()(content_ops.check_banned_terms)

# -- Citation auditing --
mcp.tool()(reference_ops.validate_citation_format)
mcp.tool()(reference_ops.extract_citations_from_file)
mcp.tool()(reference_ops.generate_citation_report)
mcp.tool()(reference_ops.search_references)

# -- Knowledge base cross-check (verify canon claims during review) --
mcp.tool()(kb_ops.kb_search)
mcp.tool()(kb_ops.kb_search_multi)

if __name__ == "__main__":
    mcp.run()
