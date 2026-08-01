#!/usr/bin/env python3
"""
Knowledge Librarian MCP Server
Per-agent server: full KB authority + full reference authority.
Deep canon research, citation management, knowledge base maintenance.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import project_ops, kb_ops, reference_ops

mcp = FastMCP("Librarian Tools")

# -- Project awareness (read-only + logging) --
mcp.tool()(project_ops.get_active_project)
mcp.tool()(project_ops.get_project_status)
mcp.tool()(project_ops.log_agent_message)

# -- Full KB authority --
mcp.tool()(kb_ops.kb_file_stats)
mcp.tool()(kb_ops.kb_directory_stats)
mcp.tool()(kb_ops.kb_extract_links)
mcp.tool()(kb_ops.kb_find_references)
mcp.tool()(kb_ops.kb_find_orphans)
mcp.tool()(kb_ops.kb_validate_links)
mcp.tool()(kb_ops.kb_search)
mcp.tool()(kb_ops.kb_search_multi)
mcp.tool()(kb_ops.kb_move_file)
mcp.tool()(kb_ops.kb_check_file_exists)
mcp.tool()(kb_ops.kb_validate_source_format)
mcp.tool()(kb_ops.kb_suggest_see_also)

# -- Full reference authority --
mcp.tool()(reference_ops.extract_citations)
mcp.tool()(reference_ops.extract_citations_from_file)
mcp.tool()(reference_ops.validate_citation_format)
mcp.tool()(reference_ops.standardize_citation)
mcp.tool()(reference_ops.list_reference_books)
mcp.tool()(reference_ops.search_references)
mcp.tool()(reference_ops.create_bibliography)
mcp.tool()(reference_ops.generate_citation_report)

if __name__ == "__main__":
    mcp.run()
