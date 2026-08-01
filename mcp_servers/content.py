#!/usr/bin/env python3
"""
Content MCP Server
FastMCP server for content analysis and supplement compilation.

Tools for:
- Word counting and section analysis
- Target tracking
- Reading time estimation
- Content density analysis
- Supplement compilation
- Table of contents generation
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from mcp.server.fastmcp import FastMCP

sys.path.insert(0, str(Path(__file__).parent))
from _lib import content_ops

mcp = FastMCP("Content")


def clean_markdown(content: str) -> str:
    """Clean markdown content for accurate word counting."""
    # Remove code blocks
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    # Remove inline code
    content = re.sub(r"`[^`]*`", "", content)
    # Remove links but keep text
    content = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", content)
    # Remove images
    content = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", content)
    # Remove markdown formatting
    content = re.sub(r"[*_#>\-\+]", "", content)
    # Remove HTML comments
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    # Clean up whitespace
    content = re.sub(r"\s+", " ", content).strip()
    return content


# =============================================================================
# WORD COUNTING TOOLS
# =============================================================================

@mcp.tool()
def count_words(file_path: str) -> str:
    """
    Count words in a markdown file with section breakdown.

    Args:
        file_path: Path to markdown file

    Returns:
        Word counts by section with totals and reading time estimate.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    clean_content = clean_markdown(content)
    total_words = len(clean_content.split())

    # Analyze sections
    sections = []
    header_pattern = r"^(#{1,6})\s+(.+)$"
    lines = content.split("\n")

    current_section = {"title": "Document Start", "level": 0, "content": [], "start": 1}

    for line_num, line in enumerate(lines, 1):
        header_match = re.match(header_pattern, line)
        if header_match:
            # Finish current section
            if current_section["content"]:
                section_text = "\n".join(current_section["content"])
                word_count = len(clean_markdown(section_text).split())
                sections.append({
                    "title": current_section["title"],
                    "level": current_section["level"],
                    "words": word_count,
                    "lines": f"{current_section['start']}-{line_num - 1}"
                })

            # Start new section
            current_section = {
                "title": header_match.group(2).strip(),
                "level": len(header_match.group(1)),
                "content": [],
                "start": line_num
            }
        else:
            current_section["content"].append(line)

    # Don't forget last section
    if current_section["content"]:
        section_text = "\n".join(current_section["content"])
        word_count = len(clean_markdown(section_text).split())
        sections.append({
            "title": current_section["title"],
            "level": current_section["level"],
            "words": word_count,
            "lines": f"{current_section['start']}-{len(lines)}"
        })

    # Calculate reading time (avg 200 wpm)
    reading_minutes = total_words / 200

    lines_out = [
        f"Word Count Analysis: {file_path}",
        "",
        f"Total words: {total_words:,}",
        f"Reading time: ~{reading_minutes:.1f} minutes",
        "",
        "Section breakdown:",
        f"{'Section':<40} {'Words':>8} {'Lines':>12}",
        "-" * 62
    ]

    for s in sections:
        indent = "  " * (s["level"] - 1) if s["level"] > 0 else ""
        title = f"{indent}{s['title']}"[:38]
        lines_out.append(f"{title:<40} {s['words']:>8} {s['lines']:>12}")

    return "\n".join(lines_out)


@mcp.tool()
def count_words_in_directory(
    directory: str,
    pattern: str = "*.md"
) -> str:
    """
    Count words across all matching files in a directory.

    Args:
        directory: Directory path to scan
        pattern: Glob pattern for files (default: *.md)

    Returns:
        Per-file word counts with directory total.
    """
    path = Path(directory)
    if not path.exists():
        return f"Directory not found: {directory}"

    files = sorted(path.rglob(pattern))
    if not files:
        return f"No files matching '{pattern}' in {directory}"

    results = []
    total = 0

    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
            words = len(clean_markdown(content).split())
            results.append((str(f.relative_to(path)), words))
            total += words
        except Exception:
            results.append((str(f.relative_to(path)), -1))

    lines = [
        f"Word Count Summary: {directory}",
        f"Files: {len(results)} | Total words: {total:,}",
        "",
        f"{'File':<50} {'Words':>10}",
        "-" * 62
    ]

    for filename, words in sorted(results, key=lambda x: -x[1]):
        if words == -1:
            lines.append(f"{filename:<50} {'ERROR':>10}")
        else:
            lines.append(f"{filename:<50} {words:>10,}")

    return "\n".join(lines)


# =============================================================================
# TARGET TRACKING
# =============================================================================

@mcp.tool()
def check_word_targets(
    file_path: str,
    target: int,
    tolerance: float = 0.25
) -> str:
    """
    Check if a file meets its word count target within tolerance.

    Args:
        file_path: Path to markdown file
        target: Target word count
        tolerance: Acceptable deviation (0.25 = 25%)

    Returns:
        Status report showing whether target is met.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    actual = len(clean_markdown(content).split())

    min_acceptable = int(target * (1 - tolerance))
    max_acceptable = int(target * (1 + tolerance))

    status = "ON TARGET" if min_acceptable <= actual <= max_acceptable else \
             "UNDER TARGET" if actual < min_acceptable else "OVER TARGET"

    diff = actual - target
    diff_pct = (diff / target * 100) if target > 0 else 0

    lines = [
        f"Word Target Check: {file_path}",
        "",
        f"Target: {target:,} words (±{tolerance:.0%})",
        f"Acceptable range: {min_acceptable:,} - {max_acceptable:,}",
        f"Actual: {actual:,} words",
        "",
        f"Difference: {diff:+,} ({diff_pct:+.1f}%)",
        "",
        f"STATUS: {status}"
    ]

    if status == "UNDER TARGET":
        needed = min_acceptable - actual
        lines.append(f"Need {needed:,} more words to reach minimum")
    elif status == "OVER TARGET":
        excess = actual - max_acceptable
        lines.append(f"Consider cutting {excess:,} words to reach maximum")

    return "\n".join(lines)


@mcp.tool()
def track_chapter_progress(
    content_dir: str,
    targets: Optional[str] = None
) -> str:
    """
    Track word count progress across all chapters.

    Args:
        content_dir: Path to content directory with chapter folders
        targets: Optional comma-separated chapter:target pairs (e.g., "01:5000,02:3000")

    Returns:
        Progress report for all chapters.
    """
    path = Path(content_dir)
    if not path.exists():
        return f"Content directory not found: {content_dir}"

    # Parse targets if provided
    chapter_targets = {}
    if targets:
        for pair in targets.split(","):
            if ":" in pair:
                ch, tgt = pair.split(":", 1)
                try:
                    chapter_targets[ch.strip()] = int(tgt.strip())
                except ValueError:
                    pass

    # Find chapter directories
    chapter_dirs = sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("chapter_")])

    if not chapter_dirs:
        return "No chapter directories found"

    total_words = 0
    total_target = 0
    results = []

    for ch_dir in chapter_dirs:
        ch_num = ch_dir.name.replace("chapter_", "")

        # Count words in all markdown files
        ch_words = 0
        for md_file in ch_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                ch_words += len(clean_markdown(content).split())
            except Exception:
                pass

        target = chapter_targets.get(ch_num, 0)
        total_words += ch_words
        total_target += target

        status = ""
        if target > 0:
            pct = ch_words / target * 100
            status = f"{pct:.0f}%"

        results.append((ch_dir.name, ch_words, target, status))

    lines = [
        f"Chapter Progress: {content_dir}",
        "",
        f"{'Chapter':<20} {'Words':>10} {'Target':>10} {'Progress':>10}",
        "-" * 52
    ]

    for name, words, target, status in results:
        target_str = f"{target:,}" if target > 0 else "-"
        lines.append(f"{name:<20} {words:>10,} {target_str:>10} {status:>10}")

    lines.extend([
        "-" * 52,
        f"{'TOTAL':<20} {total_words:>10,} {total_target:>10,}" if total_target else f"{'TOTAL':<20} {total_words:>10,}"
    ])

    if total_target > 0:
        lines.append(f"\nOverall progress: {total_words / total_target:.1%}")

    return "\n".join(lines)


# =============================================================================
# CONTENT ANALYSIS
# =============================================================================

@mcp.tool()
def estimate_reading_time(file_path: str) -> str:
    """
    Estimate reading time for a file with difficulty adjustment.

    Args:
        file_path: Path to markdown file

    Returns:
        Reading time estimates for different reading speeds.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    words = len(clean_markdown(content).split())

    # Different reading speeds
    speeds = {
        "Slow (150 wpm)": 150,
        "Average (200 wpm)": 200,
        "Fast (300 wpm)": 300,
        "Skimming (450 wpm)": 450
    }

    lines = [
        f"Reading Time Estimate: {file_path}",
        f"Word count: {words:,}",
        "",
        "Estimated reading times:"
    ]

    for label, wpm in speeds.items():
        minutes = words / wpm
        if minutes < 1:
            time_str = f"< 1 minute"
        elif minutes < 60:
            time_str = f"{minutes:.0f} minutes"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            time_str = f"{hours}h {mins}m"
        lines.append(f"  {label}: {time_str}")

    return "\n".join(lines)


@mcp.tool()
def analyze_content_density(file_path: str) -> str:
    """
    Analyze content density metrics for a file.

    Args:
        file_path: Path to markdown file

    Returns:
        Content density metrics including header/content ratio, list usage, etc.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    lines_list = content.split("\n")
    total_lines = len(lines_list)

    # Count different content types
    headers = len([l for l in lines_list if re.match(r'^#{1,6}\s', l)])
    list_items = len([l for l in lines_list if re.match(r'^\s*[-*+]\s', l)])
    code_blocks = len(re.findall(r'```', content)) // 2
    blank_lines = len([l for l in lines_list if not l.strip()])

    content_lines = total_lines - blank_lines - headers

    words = len(clean_markdown(content).split())
    words_per_line = words / content_lines if content_lines > 0 else 0

    lines_out = [
        f"Content Density Analysis: {file_path}",
        "",
        "Structure:",
        f"  Total lines: {total_lines}",
        f"  Headers: {headers} ({headers/total_lines*100:.1f}%)",
        f"  List items: {list_items}",
        f"  Code blocks: {code_blocks}",
        f"  Blank lines: {blank_lines} ({blank_lines/total_lines*100:.1f}%)",
        "",
        "Density metrics:",
        f"  Words: {words:,}",
        f"  Content lines: {content_lines}",
        f"  Words per content line: {words_per_line:.1f}",
        f"  Headers per 1000 words: {headers/words*1000:.1f}" if words > 0 else "",
        "",
        "Assessment:"
    ]

    if words_per_line < 8:
        lines_out.append("  - Content is sparse (many short lines)")
    elif words_per_line > 20:
        lines_out.append("  - Content is dense (long paragraphs)")
    else:
        lines_out.append("  - Content density is balanced")

    if headers / max(words, 1) * 1000 > 10:
        lines_out.append("  - Heavy header usage (well-structured)")
    elif headers / max(words, 1) * 1000 < 3:
        lines_out.append("  - Few headers (consider adding more structure)")

    return "\n".join(lines_out)


# =============================================================================
# COMPILATION TOOLS
# =============================================================================

@mcp.tool()
def compile_supplement(
    content_dir: str,
    output_path: str,
    title: Optional[str] = None,
    include_toc: bool = True
) -> str:
    """
    Compile all chapter content into a single supplement file.

    Args:
        content_dir: Path to content directory with chapter folders
        output_path: Output file path
        title: Supplement title
        include_toc: Whether to include table of contents

    Returns:
        Compilation statistics and output location.
    """
    content_path = Path(content_dir)
    if not content_path.exists():
        return f"Content directory not found: {content_dir}"

    chapter_dirs = sorted([d for d in content_path.iterdir()
                          if d.is_dir() and d.name.startswith("chapter_")])

    if not chapter_dirs:
        return "No chapter directories found"

    compiled = []
    toc_entries = []
    total_words = 0
    chapter_count = 0

    # Title page
    if title:
        compiled.append(f"# {title}")
        compiled.append("")
        compiled.append(f"*Compiled: {datetime.now().strftime('%Y-%m-%d')}*")
        compiled.append("")
        compiled.append("---")
        compiled.append("")

    # Process chapters
    for ch_dir in chapter_dirs:
        ch_num = ch_dir.name.replace("chapter_", "")
        chapter_count += 1

        # Look for final_draft.md, then draft_02.md, then draft_01.md
        draft_file = None
        for draft_name in ["final_draft.md", "draft_02.md", "draft_01.md"]:
            candidate = ch_dir / draft_name
            if candidate.exists():
                draft_file = candidate
                break

        if not draft_file:
            continue

        try:
            content = draft_file.read_text(encoding='utf-8')

            # Extract title from first H1
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            ch_title = title_match.group(1) if title_match else f"Chapter {ch_num}"

            toc_entries.append(f"- [{ch_title}](#chapter-{ch_num})")

            compiled.append(f"## Chapter {ch_num}: {ch_title} {{#chapter-{ch_num}}}")
            compiled.append("")

            # Remove the first H1 to avoid duplication
            if title_match:
                content = content[title_match.end():].strip()

            compiled.append(content)
            compiled.append("")
            compiled.append("---")
            compiled.append("")

            total_words += len(clean_markdown(content).split())

        except Exception as e:
            compiled.append(f"*Error loading chapter {ch_num}: {e}*")
            compiled.append("")

    # Insert TOC if requested
    if include_toc and toc_entries:
        toc = ["## Table of Contents", ""] + toc_entries + ["", "---", ""]
        # Insert after title page
        insert_pos = 7 if title else 0
        compiled[insert_pos:insert_pos] = toc

    # Write output
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(compiled), encoding='utf-8')

    return f"""Supplement compiled successfully!

Output: {output_path}
Chapters: {chapter_count}
Total words: {total_words:,}
Estimated pages: ~{total_words // 250}

Table of Contents: {'Yes' if include_toc else 'No'}"""


@mcp.tool()
def generate_toc(file_path: str, max_depth: int = 3) -> str:
    """
    Generate a table of contents from a markdown file.

    Args:
        file_path: Path to markdown file
        max_depth: Maximum header depth to include (1-6)

    Returns:
        Markdown-formatted table of contents.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading file: {e}"

    toc = ["## Table of Contents", ""]
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    for match in header_pattern.finditer(content):
        level = len(match.group(1))
        if level > max_depth:
            continue

        title = match.group(2).strip()
        # Create anchor from title
        anchor = re.sub(r'[^\w\s-]', '', title.lower())
        anchor = re.sub(r'\s+', '-', anchor)

        indent = "  " * (level - 1)
        toc.append(f"{indent}- [{title}](#{anchor})")

    return "\n".join(toc)


# =============================================================================
# BANNED TERMS CHECKING
# =============================================================================

@mcp.tool()
def check_banned_terms(file_path: str) -> str:
    """
    Check a draft against the voice ban lists in config/system.json:
    banned_phrases (glob * wildcards), banned_names (whole words), and
    use_sparingly terms (per-10k-word thresholds). Returns violations with
    line numbers, or a clean bill of health.

    Args:
        file_path: Path to markdown file

    Returns:
        Banned-terms violation report with line numbers and details.
    """
    return content_ops.check_banned_terms(file_path)


if __name__ == "__main__":
    mcp.run()
