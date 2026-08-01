"""
Reference and citation operations — shared implementations.
Citation extraction, validation, search, bibliography generation.
"""

import os
import re
from pathlib import Path
from typing import Optional
from collections import defaultdict

from . import config

# Default references path
DEFAULT_REFS_PATH = Path(__file__).parent.parent.parent / "references"


def get_citation_context(content: str, start: int, end: int, context_chars: int = 100) -> str:
    """Get surrounding context for a citation."""
    ctx_start = max(0, start - context_chars)
    ctx_end = min(len(content), end + context_chars)
    return content[ctx_start:ctx_end].strip()


# =========================================================================
# CITATION EXTRACTION
# =========================================================================

def _spans_overlap(a: tuple, b: tuple) -> bool:
    """True if two (start, end) character spans intersect."""
    return a[0] < b[1] and b[0] < a[1]


def _is_same_citation(a: dict, b: dict) -> bool:
    """
    True if two raw matches describe the same citation.

    Several extraction patterns match the same text (a bare pattern, a
    parenthetical one, a 'see ...' one, and the configured one), and they
    capture different amounts of leading prose into the book name — e.g.
    "As shown in CoreBook" vs "CoreBook", or "see Companion" vs "Companion".
    Two matches are the same citation when their spans overlap, they name the
    same page, and one book name is a suffix of the other.
    """
    if not _spans_overlap(a["span"], b["span"]):
        return False
    if a["page"] != b["page"]:
        return False
    book_a, book_b = a["book"].lower(), b["book"].lower()
    return book_a == book_b or book_a.endswith(book_b) or book_b.endswith(book_a)


def _dedupe_citations(citations: list) -> list:
    """
    Collapse overlapping matches of the same citation, keeping the best entry:
    an entry carrying an edition beats one without, and otherwise the most
    specific (shortest, least prose-contaminated) book name wins.
    """
    kept: list = []

    for cite in citations:
        for i, existing in enumerate(kept):
            if not _is_same_citation(cite, existing):
                continue
            better = (cite["edition"] and not existing["edition"]) or (
                bool(cite["edition"]) == bool(existing["edition"])
                and len(cite["book"]) < len(existing["book"])
            )
            if better:
                kept[i] = cite
            break
        else:
            kept.append(cite)

    return kept


def extract_citations(content: str) -> str:
    """
    Extract all citations from markdown content.

    Args:
        content: Markdown content to analyze

    Returns:
        List of citations found with book names, page numbers, and context.
    """
    citations = []

    patterns = [
        (r"([A-Za-z\s:]+),\s*p\.\s*(\d+)", "book_page"),
        (r"([A-Za-z\s:]+)\s*\(([^)]+)\),\s*p\.\s*(\d+)", "book_edition_page"),
        (r"see\s+([A-Za-z\s:]+),\s*p\.\s*(\d+)", "see_reference"),
        (r"\(([A-Za-z\s:]+),\s*p\.\s*(\d+)\)", "parenthetical"),
    ]

    for configured_pattern in config.get("citations.patterns", []):
        patterns.append((configured_pattern, "configured"))

    for pattern, pattern_type in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            groups = match.groups()

            if pattern_type in ("book_page", "see_reference", "parenthetical"):
                book = groups[0].strip()
                page = groups[1]
                edition = None
            elif pattern_type == "book_edition_page":
                book = groups[0].strip()
                edition = groups[1].strip()
                page = groups[2]
            elif pattern_type == "configured":
                if len(groups) > 2:
                    book = " ".join(g.strip() for g in groups[:-1] if g)
                else:
                    book = groups[0].strip()
                page = groups[-1]
                edition = None
            else:
                continue

            citations.append({
                "book": book,
                "page": page,
                "edition": edition,
                "full_text": match.group(0),
                "span": (match.start(), match.end()),
                "context": get_citation_context(content, match.start(), match.end())
            })

    citations = _dedupe_citations(citations)
    citations.sort(key=lambda c: c["span"])

    if not citations:
        return "No citations found in content."

    lines = [f"Found {len(citations)} citation(s):", ""]

    for i, cite in enumerate(citations, 1):
        lines.append(f"{i}. {cite['book']}, p. {cite['page']}")
        if cite['edition']:
            lines.append(f"   Edition: {cite['edition']}")
        lines.append(f"   Context: ...{cite['context'][:80]}...")
        lines.append("")

    return "\n".join(lines)


def extract_citations_from_file(file_path: str) -> str:
    """
    Extract all citations from a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        List of citations found in the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        result = extract_citations(content)
        return f"Citations from: {file_path}\n\n{result}"
    except Exception as e:
        return f"Error reading file: {e}"


# =========================================================================
# CITATION VALIDATION
# =========================================================================

def validate_citation_format(citation: str) -> str:
    """
    Check if a citation follows the configured citation format and suggest corrections.

    Args:
        citation: The citation string to validate

    Returns:
        Validation result with any suggested corrections.
    """
    issues = []
    suggestions = []

    if not re.search(r'p\.\s*\d+', citation):
        issues.append("Missing page number (should use 'p. X' format)")

    if re.search(r'pg\.?\s*\d+', citation):
        issues.append("Uses 'pg' instead of 'p.'")
        suggestions.append("Replace 'pg.' or 'pg' with 'p.'")

    if re.search(r'page\s*\d+', citation, re.IGNORECASE):
        issues.append("Uses 'page' instead of 'p.'")
        suggestions.append("Replace 'page' with 'p.'")

    if not re.search(r',\s*p\.', citation):
        issues.append("Missing comma before page reference")
        suggestions.append("Add comma before 'p.'")

    known_books = config.get("citations.book_map", {})

    standardized = None
    for abbrev, full in known_books.items():
        if abbrev.lower() in citation.lower():
            standardized = f"{full}, " + citation.split(",")[-1].strip() if "," in citation else citation
            break

    lines = [f"Citation: {citation}", ""]

    if issues:
        lines.append("Issues found:")
        for issue in issues:
            lines.append(f"  - {issue}")
        lines.append("")

    if suggestions:
        lines.append("Suggestions:")
        for sug in suggestions:
            lines.append(f"  - {sug}")
        lines.append("")

    if standardized:
        lines.append(f"Standardized form: {standardized}")
    elif not issues:
        lines.append("Citation format is valid.")

    if not known_books:
        lines.append("(No citations.book_map configured in config/system.json — see config/README.md.)")

    return "\n".join(lines)


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
    book_map = config.get("citations.book_map", {})

    standard_name = book_map.get(book_name.lower(), book_name)

    parts = [standard_name]
    if chapter:
        parts.append(f"Chapter {chapter}" if not chapter.startswith("Chapter") else chapter)
    if section:
        parts.append(section)

    citation = ", ".join(parts) + f", p. {page_number}"

    return f"Standardized citation:\n{citation}"


# =========================================================================
# REFERENCE DATABASE
# =========================================================================

def list_reference_books(refs_path: Optional[str] = None) -> str:
    """
    List all reference books available in the references directory.

    Args:
        refs_path: Path to references directory (defaults to ./references)

    Returns:
        Hierarchical list of available reference materials.
    """
    path = Path(refs_path) if refs_path else DEFAULT_REFS_PATH

    if not path.exists():
        return f"References directory not found: {path}"

    lines = [f"Reference Materials: {path}", ""]

    for game_dir in sorted(path.iterdir()):
        if not game_dir.is_dir() or game_dir.name.startswith('.'):
            continue

        lines.append(f"{game_dir.name}/")

        for edition_dir in sorted(game_dir.iterdir()):
            if not edition_dir.is_dir():
                continue

            files = list(edition_dir.glob("*.pdf")) + list(edition_dir.glob("*.md"))
            if files:
                lines.append(f"  {edition_dir.name}/ ({len(files)} files)")
                for f in sorted(files)[:5]:
                    lines.append(f"    - {f.name}")
                if len(files) > 5:
                    lines.append(f"    ... and {len(files) - 5} more")

    return "\n".join(lines)


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
    path = Path(refs_path) if refs_path else DEFAULT_REFS_PATH

    if not path.exists():
        return f"References directory not found: {path}"

    results = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)

    glob_pattern = "**/*.md" if file_type == "md" else "**/*"

    for ref_file in path.glob(glob_pattern):
        if not ref_file.is_file():
            continue
        if ref_file.suffix not in ['.md', '.txt']:
            continue

        try:
            content = ref_file.read_text(encoding='utf-8', errors='ignore')
            matches = list(pattern.finditer(content))

            if matches:
                results.append({
                    'file': str(ref_file.relative_to(path)),
                    'matches': len(matches),
                    'sample': get_citation_context(content, matches[0].start(), matches[0].end(), 150)
                })
        except Exception:
            pass

    if not results:
        return f"No results found for '{query}'"

    results.sort(key=lambda x: -x['matches'])

    lines = [
        f"Search results for: '{query}'",
        f"Found in {len(results)} file(s)",
        ""
    ]

    for r in results[:20]:
        lines.append(f"--- {r['file']} ({r['matches']} match(es)) ---")
        lines.append(f"  ...{r['sample']}...")
        lines.append("")

    return "\n".join(lines)


# =========================================================================
# BIBLIOGRAPHY
# =========================================================================

def create_bibliography(citations: str) -> str:
    """
    Create a formatted bibliography from a list of citations.

    Args:
        citations: Newline-separated list of citations or comma-separated book names

    Returns:
        Formatted bibliography section.
    """
    if "\n" in citations:
        items = [c.strip() for c in citations.split("\n") if c.strip()]
    else:
        items = [c.strip() for c in citations.split(",") if c.strip()]

    books = set()
    for item in items:
        match = re.match(r"([^,]+)", item)
        if match:
            book = match.group(1).strip()
            book = re.sub(r',?\s*p\.\s*\d+.*$', '', book).strip()
            if book:
                books.add(book)

    if not books:
        return "No books found in citations."

    full_titles = config.get("citations.bibliography", {})

    lines = ["## Bibliography", ""]

    for book in sorted(books):
        full = full_titles.get(book)
        if full:
            lines.append(f"- {full}")
        else:
            lines.append(f"- {book}. [No bibliography entry — add to citations.bibliography in config/system.json]")

    if not full_titles:
        lines.append("(No citations.book_map/bibliography configured in config/system.json — see config/README.md.)")

    return "\n".join(lines)


def generate_citation_report(file_path: str) -> str:
    """
    Generate a comprehensive citation report for a file.

    Args:
        file_path: Path to the markdown file to analyze

    Returns:
        Report including citation count, unique sources, and any issues.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    citations = []
    patterns = [
        r"([A-Za-z\s:]+),\s*p\.\s*(\d+)",
        r"\(([A-Za-z\s:]+),\s*p\.\s*(\d+)\)",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            citations.append({
                'book': match.group(1).strip(),
                'page': match.group(2)
            })

    if not citations:
        lines = [
            f"Citation Report: {file_path}",
            "",
            "No citations found.",
            "",
            "Consider adding source citations to maintain canon consistency."
        ]
        return "\n".join(lines)

    books = defaultdict(list)
    for c in citations:
        books[c['book']].append(c['page'])

    lines = [
        f"Citation Report: {file_path}",
        "",
        f"Total citations: {len(citations)}",
        f"Unique sources: {len(books)}",
        "",
        "Sources referenced:"
    ]

    for book, pages in sorted(books.items()):
        unique_pages = sorted(set(pages), key=int)
        page_str = ", ".join(unique_pages[:5])
        if len(unique_pages) > 5:
            page_str += f" (+{len(unique_pages) - 5} more)"
        lines.append(f"  - {book}: pp. {page_str}")

    return "\n".join(lines)
