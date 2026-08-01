#!/usr/bin/env python3
"""
References MCP Server
FastMCP server for citation management and reference validation.

Tools for:
- Extracting citations from content
- Validating citations against source materials
- Building reference databases
- Standardizing citation formats
- Generating bibliographies
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP
from _lib import reference_ops

mcp = FastMCP("References")


# =============================================================================
# CITATION EXTRACTION
# =============================================================================

@mcp.tool()
def extract_citations(content: str) -> str:
    """
    Extract all citations from markdown content.

    Args:
        content: Markdown content to analyze

    Returns:
        List of citations found with book names, page numbers, and context.
    """
    return reference_ops.extract_citations(content)


@mcp.tool()
def extract_citations_from_file(file_path: str) -> str:
    """
    Extract all citations from a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        List of citations found in the file.
    """
    return reference_ops.extract_citations_from_file(file_path)


# =============================================================================
# CITATION VALIDATION
# =============================================================================

@mcp.tool()
def validate_citation_format(citation: str) -> str:
    """
    Check if a citation follows the configured citation format and suggest corrections.

    Args:
        citation: The citation string to validate

    Returns:
        Validation result with any suggested corrections.
    """
    return reference_ops.validate_citation_format(citation)


@mcp.tool()
def standardize_citation(
    book_name: str,
    page_number: int,
    chapter: Optional[str] = None,
    section: Optional[str] = None
) -> str:
    """
    Generate a standardized citation string.

    Args:
        book_name: Name of the source book
        page_number: Page number
        chapter: Optional chapter name
        section: Optional section name

    Returns:
        Properly formatted citation string.
    """
    return reference_ops.standardize_citation(book_name, page_number, chapter, section)


# =============================================================================
# REFERENCE DATABASE
# =============================================================================

@mcp.tool()
def list_reference_books(refs_path: Optional[str] = None) -> str:
    """
    List all reference books available in the references directory.

    Args:
        refs_path: Path to references directory (defaults to ./references)

    Returns:
        Hierarchical list of available reference materials.
    """
    return reference_ops.list_reference_books(refs_path)


@mcp.tool()
def search_references(
    query: str,
    refs_path: Optional[str] = None,
    file_type: str = "md"
) -> str:
    """
    Search reference materials for a term.

    Args:
        query: Search term
        refs_path: Path to references directory
        file_type: File type to search ('md' or 'all')

    Returns:
        Files and passages matching the search term.
    """
    return reference_ops.search_references(query, refs_path, file_type)


# =============================================================================
# BIBLIOGRAPHY GENERATION
# =============================================================================

@mcp.tool()
def create_bibliography(citations: str) -> str:
    """
    Create a formatted bibliography from a list of citations.

    Args:
        citations: Newline-separated list of citations or comma-separated book names

    Returns:
        Formatted bibliography section.
    """
    return reference_ops.create_bibliography(citations)


@mcp.tool()
def generate_citation_report(file_path: str) -> str:
    """
    Generate a comprehensive citation report for a file.

    Args:
        file_path: Path to the markdown file to analyze

    Returns:
        Report including citation count, unique sources, and any issues.
    """
    return reference_ops.generate_citation_report(file_path)


if __name__ == "__main__":
    mcp.run()
