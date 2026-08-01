"""
Content analysis operations — shared implementations.
Word counting, target tracking, density analysis, compilation, TOC generation.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional
from . import config


def clean_markdown(content: str) -> str:
    """Clean markdown content for accurate word counting."""
    content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    content = re.sub(r"`[^`]*`", "", content)
    content = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", content)
    content = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", content)
    content = re.sub(r"[*_#>\-\+]", "", content)
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    content = re.sub(r"\s+", " ", content).strip()
    return content


# =========================================================================
# WORD COUNTING
# =========================================================================

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

    sections = []
    header_pattern = r"^(#{1,6})\s+(.+)$"
    lines = content.split("\n")

    current_section = {"title": "Document Start", "level": 0, "content": [], "start": 1}

    for line_num, line in enumerate(lines, 1):
        header_match = re.match(header_pattern, line)
        if header_match:
            if current_section["content"]:
                section_text = "\n".join(current_section["content"])
                word_count = len(clean_markdown(section_text).split())
                sections.append({
                    "title": current_section["title"],
                    "level": current_section["level"],
                    "words": word_count,
                    "lines": f"{current_section['start']}-{line_num - 1}"
                })
            current_section = {
                "title": header_match.group(2).strip(),
                "level": len(header_match.group(1)),
                "content": [],
                "start": line_num
            }
        else:
            current_section["content"].append(line)

    if current_section["content"]:
        section_text = "\n".join(current_section["content"])
        word_count = len(clean_markdown(section_text).split())
        sections.append({
            "title": current_section["title"],
            "level": current_section["level"],
            "words": word_count,
            "lines": f"{current_section['start']}-{len(lines)}"
        })

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


# =========================================================================
# TARGET TRACKING
# =========================================================================

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

    chapter_targets = {}
    if targets:
        for pair in targets.split(","):
            if ":" in pair:
                ch, tgt = pair.split(":", 1)
                try:
                    chapter_targets[ch.strip()] = int(tgt.strip())
                except ValueError:
                    pass

    chapter_dirs = sorted([d for d in path.iterdir() if d.is_dir() and d.name.startswith("chapter_")])

    if not chapter_dirs:
        return "No chapter directories found"

    total_words = 0
    total_target = 0
    results = []

    for ch_dir in chapter_dirs:
        ch_num = ch_dir.name.replace("chapter_", "")

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


# =========================================================================
# CONTENT ANALYSIS
# =========================================================================

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
            time_str = "< 1 minute"
        elif minutes < 60:
            time_str = f"{minutes:.0f} minutes"
        else:
            hours = int(minutes // 60)
            mins = int(minutes % 60)
            time_str = f"{hours}h {mins}m"
        lines.append(f"  {label}: {time_str}")

    return "\n".join(lines)


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


# =========================================================================
# COMPILATION
# =========================================================================

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

    if title:
        compiled.append(f"# {title}")
        compiled.append("")
        compiled.append(f"*Compiled: {datetime.now().strftime('%Y-%m-%d')}*")
        compiled.append("")
        compiled.append("---")
        compiled.append("")

    for ch_dir in chapter_dirs:
        ch_num = ch_dir.name.replace("chapter_", "")
        chapter_count += 1

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

            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            ch_title = title_match.group(1) if title_match else f"Chapter {ch_num}"

            toc_entries.append(f"- [{ch_title}](#chapter-{ch_num})")

            compiled.append(f"## Chapter {ch_num}: {ch_title} {{#chapter-{ch_num}}}")
            compiled.append("")

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

    if include_toc and toc_entries:
        toc = ["## Table of Contents", ""] + toc_entries + ["", "---", ""]
        insert_pos = 6 if title else 0
        compiled[insert_pos:insert_pos] = toc

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(compiled), encoding='utf-8')

    return f"""Supplement compiled successfully!

Output: {output_path}
Chapters: {chapter_count}
Total words: {total_words:,}
Estimated pages: ~{total_words // 250}

Table of Contents: {'Yes' if include_toc else 'No'}"""


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
        anchor = re.sub(r'[^\w\s-]', '', title.lower())
        anchor = re.sub(r'\s+', '-', anchor)

        indent = "  " * (level - 1)
        toc.append(f"{indent}- [{title}](#{anchor})")

    return "\n".join(toc)


# =========================================================================
# BANNED TERMS CHECKING
# =========================================================================

def _phrase_to_regex(phrase: str) -> "re.Pattern":
    """Compile a banned phrase with * wildcards into a case-insensitive regex."""
    parts = [re.escape(p) for p in phrase.split("*")]
    return re.compile(r"[\w'’ ,-]{0,40}".join(parts), re.IGNORECASE)


def check_banned_terms(file_path: str) -> str:
    """
    Check a draft against the voice ban lists in config/system.json:
    banned_phrases (glob * wildcards), banned_names (whole words), and
    use_sparingly terms (per-10k-word thresholds). Returns violations with
    line numbers, or a clean bill of health.
    """
    try:
        text = Path(file_path).read_text(encoding="utf-8")
    except OSError as e:
        return f"Error reading file: {e}"
    lines = text.splitlines()
    word_count = len(re.findall(r"\b\w+\b", text))
    violations = []

    for phrase in config.get("voice.banned_phrases", []):
        rx = _phrase_to_regex(phrase)
        for n, line in enumerate(lines, 1):
            for m in rx.finditer(line):
                violations.append(f"line {n}: banned phrase '{phrase}' -> \"{m.group(0).strip()}\"")

    for name in config.get("voice.banned_names", []):
        rx = re.compile(rf"\b{re.escape(name)}\b")
        for n, line in enumerate(lines, 1):
            if rx.search(line):
                violations.append(f"line {n}: banned name '{name}'")

    for rule in config.get("voice.use_sparingly", []):
        term, cap = rule.get("term", ""), rule.get("max_per_10k_words", 1)
        if not term:
            continue
        count = text.lower().count(term.lower())
        allowed = max(1, round(cap * word_count / 10000)) if word_count else cap
        if count > allowed:
            violations.append(
                f"use-sparingly: '{term}' appears {count}x "
                f"(threshold {allowed} for {word_count} words at {cap}/10k)"
            )

    header = f"Banned-terms check: {file_path} ({word_count} words)"
    if not violations:
        return f"{header}\n\nNo violations."
    return "\n".join([header, "", f"{len(violations)} violation(s):"] + [f"  - {v}" for v in violations])
