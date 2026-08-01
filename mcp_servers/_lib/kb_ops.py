"""
Knowledge base operations — shared implementations.
File stats, search, link management, validation, organization.
"""

import os
import re
from pathlib import Path
from typing import Optional
from collections import defaultdict

from . import config

# Repo root (mcp_servers/_lib/kb_ops.py -> repo root)
_REPO_ROOT = Path(__file__).parent.parent.parent

# Default knowledge base path
DEFAULT_KB_PATH = _REPO_ROOT / config.get("knowledge_base.root", "knowledge_base")


def get_kb_path(kb_path: Optional[str] = None) -> Path:
    """Resolve knowledge base path."""
    if kb_path:
        return Path(kb_path)
    return DEFAULT_KB_PATH


def _count_words(text: str) -> int:
    """Count words in text, excluding markdown syntax."""
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
    return len(text.split())


def _extract_links_from_content(content: str) -> list[tuple[str, str]]:
    """Extract markdown links as (text, path) tuples."""
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    return re.findall(pattern, content)


def _resolve_relative_path(from_file: Path, relative_link: str) -> Path:
    """Resolve a relative link from a file's location."""
    if relative_link.startswith(('http://', 'https://', '#')):
        return None
    relative_link = relative_link.split('#')[0]
    if not relative_link:
        return None
    return (from_file.parent / relative_link).resolve()


# =========================================================================
# KB STATS
# =========================================================================

def kb_file_stats(
    kb_path: Optional[str] = None,
    min_words: int = 0,
    sort_by: str = "words_desc"
) -> str:
    """
    Get word counts for all markdown files in the knowledge base.

    Args:
        kb_path: Path to knowledge base (defaults to ./knowledge_base)
        min_words: Only include files with at least this many words
        sort_by: Sort order - 'words_desc', 'words_asc', 'path', 'name'

    Returns:
        Formatted table of files with word counts and paths.
    """
    kb = get_kb_path(kb_path)

    if not kb.exists():
        return f"Error: Knowledge base not found at {kb}"

    files_data = []
    total_words = 0

    for md_file in kb.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            words = _count_words(content)
            total_words += words

            if words >= min_words:
                rel_path = md_file.relative_to(kb)
                files_data.append({
                    'path': str(rel_path),
                    'name': md_file.name,
                    'words': words,
                    'lines': len(content.splitlines())
                })
        except Exception as e:
            files_data.append({
                'path': str(md_file.relative_to(kb)),
                'name': md_file.name,
                'words': -1,
                'lines': -1,
                'error': str(e)
            })

    if sort_by == "words_desc":
        files_data.sort(key=lambda x: x['words'], reverse=True)
    elif sort_by == "words_asc":
        files_data.sort(key=lambda x: x['words'])
    elif sort_by == "path":
        files_data.sort(key=lambda x: x['path'])
    elif sort_by == "name":
        files_data.sort(key=lambda x: x['name'])

    lines = [
        f"Knowledge Base Statistics: {kb}",
        f"Total files: {len(files_data)} | Total words: {total_words:,}",
        "",
        "Files by word count:",
        "-" * 80
    ]

    for f in files_data:
        if f['words'] == -1:
            lines.append(f"  ERROR: {f['path']} - {f.get('error', 'unknown')}")
        else:
            status = ""
            if f['words'] >= 1000:
                status = " [SPLIT CANDIDATE]"
            elif f['words'] >= 800:
                status = " [REVIEW]"
            lines.append(f"  {f['words']:5d} words | {f['path']}{status}")

    return "\n".join(lines)


def kb_directory_stats(kb_path: Optional[str] = None) -> str:
    """
    Get aggregate statistics per directory in the knowledge base.

    Args:
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        Per-directory file counts, total words, and average file size.
    """
    kb = get_kb_path(kb_path)

    if not kb.exists():
        return f"Error: Knowledge base not found at {kb}"

    dir_stats = defaultdict(lambda: {'files': 0, 'words': 0, 'has_index': False})

    for md_file in kb.rglob("*.md"):
        try:
            rel_dir = md_file.parent.relative_to(kb)
            content = md_file.read_text(encoding='utf-8')
            words = _count_words(content)

            dir_stats[str(rel_dir)]['files'] += 1
            dir_stats[str(rel_dir)]['words'] += words

            if md_file.name == '_index.md':
                dir_stats[str(rel_dir)]['has_index'] = True
        except Exception:
            pass

    sorted_dirs = sorted(dir_stats.items(), key=lambda x: x[1]['words'], reverse=True)

    lines = [
        f"Directory Statistics: {kb}",
        f"Total directories: {len(sorted_dirs)}",
        "",
        f"{'Directory':<50} {'Files':>6} {'Words':>8} {'Avg':>6} {'Index':>6}",
        "-" * 80
    ]

    for dir_path, stats in sorted_dirs:
        avg = stats['words'] // stats['files'] if stats['files'] > 0 else 0
        has_index = "Yes" if stats['has_index'] else "NO"
        lines.append(
            f"{dir_path:<50} {stats['files']:>6} {stats['words']:>8} {avg:>6} {has_index:>6}"
        )

    return "\n".join(lines)


# =========================================================================
# LINK TOOLS
# =========================================================================

def kb_extract_links(file_path: str, kb_path: Optional[str] = None) -> str:
    """
    Extract all markdown links from a file with resolved paths.

    Args:
        file_path: Path to the markdown file (relative to KB or absolute)
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        List of links with their resolved absolute paths and validity status.
    """
    kb = get_kb_path(kb_path)

    fp = Path(file_path)
    if not fp.is_absolute():
        fp = kb / file_path

    if not fp.exists():
        return f"Error: File not found: {fp}"

    content = fp.read_text(encoding='utf-8')
    links = _extract_links_from_content(content)

    lines = [
        f"Links extracted from: {fp.relative_to(kb) if fp.is_relative_to(kb) else fp}",
        f"Total links found: {len(links)}",
        ""
    ]

    for text, link in links:
        resolved = _resolve_relative_path(fp, link)
        if resolved is None:
            lines.append(f"  [{text}]({link}) -> [external/anchor]")
        elif resolved.exists():
            try:
                rel = resolved.relative_to(kb)
                lines.append(f"  [{text}]({link}) -> {rel} [OK]")
            except ValueError:
                lines.append(f"  [{text}]({link}) -> {resolved} [OUTSIDE KB]")
        else:
            lines.append(f"  [{text}]({link}) -> [BROKEN]")

    return "\n".join(lines)


def kb_find_references(target_path: str, kb_path: Optional[str] = None) -> str:
    """
    Find all files that link to a given file (inbound references).

    Args:
        target_path: Path to the target file (relative to KB)
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        List of files containing links to the target, with line numbers.
    """
    kb = get_kb_path(kb_path)
    target = Path(target_path)

    if target.is_absolute():
        try:
            target = target.relative_to(kb)
        except ValueError:
            return "Error: Target path not within knowledge base"

    target_abs = (kb / target).resolve()
    references = []

    for md_file in kb.rglob("*.md"):
        if md_file.resolve() == target_abs:
            continue

        try:
            content = md_file.read_text(encoding='utf-8')

            for line_num, line in enumerate(content.splitlines(), 1):
                line_links = _extract_links_from_content(line)
                for text, link in line_links:
                    resolved = _resolve_relative_path(md_file, link)
                    if resolved and resolved.resolve() == target_abs:
                        references.append({
                            'file': str(md_file.relative_to(kb)),
                            'line': line_num,
                            'text': text,
                            'link': link
                        })
        except Exception:
            pass

    lines = [
        f"References to: {target}",
        f"Found in {len(references)} location(s):",
        ""
    ]

    if not references:
        lines.append("  No references found (orphan file)")
    else:
        for ref in references:
            lines.append(f"  {ref['file']}:{ref['line']} - [{ref['text']}]({ref['link']})")

    return "\n".join(lines)


def kb_find_orphans(kb_path: Optional[str] = None) -> str:
    """
    Find files with no inbound links (orphan files).

    Args:
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        List of files that are not linked from any other file.
    """
    kb = get_kb_path(kb_path)

    if not kb.exists():
        return f"Error: Knowledge base not found at {kb}"

    all_files = set()
    for md_file in kb.rglob("*.md"):
        all_files.add(md_file.resolve())

    referenced = set()

    for md_file in kb.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            links = _extract_links_from_content(content)

            for _, link in links:
                resolved = _resolve_relative_path(md_file, link)
                if resolved:
                    referenced.add(resolved.resolve())
        except Exception:
            pass

    orphans = []
    for f in all_files:
        if f not in referenced and f.name != '_index.md':
            orphans.append(f.relative_to(kb))

    orphans.sort()

    lines = [
        f"Orphan Files (no inbound links): {kb}",
        f"Found: {len(orphans)} orphan(s)",
        ""
    ]

    for orphan in orphans:
        lines.append(f"  {orphan}")

    return "\n".join(lines)


def kb_validate_links(kb_path: Optional[str] = None) -> str:
    """
    Find all broken links in the knowledge base.

    Args:
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        List of broken links with source file, line number, and target path.
    """
    kb = get_kb_path(kb_path)

    if not kb.exists():
        return f"Error: Knowledge base not found at {kb}"

    broken = []
    total_links = 0

    for md_file in kb.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')

            for line_num, line in enumerate(content.splitlines(), 1):
                links = _extract_links_from_content(line)
                for text, link in links:
                    total_links += 1
                    resolved = _resolve_relative_path(md_file, link)
                    if resolved and not resolved.exists():
                        broken.append({
                            'source': str(md_file.relative_to(kb)),
                            'line': line_num,
                            'text': text,
                            'link': link
                        })
        except Exception:
            pass

    lines = [
        f"Link Validation: {kb}",
        f"Total links checked: {total_links}",
        f"Broken links found: {len(broken)}",
        ""
    ]

    if broken:
        lines.append("Broken links:")
        for b in broken:
            lines.append(f"  {b['source']}:{b['line']}")
            lines.append(f"    [{b['text']}]({b['link']})")
    else:
        lines.append("All links valid!")

    return "\n".join(lines)


# =========================================================================
# SEARCH
# =========================================================================

def kb_search(
    query: str,
    kb_path: Optional[str] = None,
    directory: Optional[str] = None,
    case_sensitive: bool = False,
    context_lines: int = 1,
    max_results: int = 50
) -> str:
    """
    Search for terms in the knowledge base with context.

    Args:
        query: Search term or phrase
        kb_path: Path to knowledge base (defaults to ./knowledge_base)
        directory: Subdirectory to search within (e.g., 'factions')
        case_sensitive: Whether search is case-sensitive
        context_lines: Number of context lines before/after match
        max_results: Maximum number of results to return

    Returns:
        Structured search results with file paths, line numbers, and context.
    """
    kb = get_kb_path(kb_path)

    if not kb.exists():
        return f"Error: Knowledge base not found at {kb}"

    search_path = kb
    if directory:
        search_path = kb / directory
        if not search_path.exists():
            return f"Error: Directory not found: {directory}"

    if not case_sensitive:
        query_pattern = re.compile(re.escape(query), re.IGNORECASE)
    else:
        query_pattern = re.compile(re.escape(query))

    results = []

    for md_file in search_path.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            file_lines = content.splitlines()

            for i, line in enumerate(file_lines):
                if query_pattern.search(line):
                    start = max(0, i - context_lines)
                    end = min(len(file_lines), i + context_lines + 1)
                    context = file_lines[start:end]

                    results.append({
                        'file': str(md_file.relative_to(kb)),
                        'line': i + 1,
                        'match': line.strip(),
                        'context': context,
                        'context_start': start + 1
                    })

                    if len(results) >= max_results:
                        break
        except Exception:
            pass

        if len(results) >= max_results:
            break

    output = [
        f"Search results for: '{query}'",
        f"Scope: {directory or 'entire knowledge base'}",
        f"Found: {len(results)} match(es)",
        ""
    ]

    for r in results:
        output.append(f"--- {r['file']}:{r['line']} ---")
        for j, ctx_line in enumerate(r['context']):
            line_num = r['context_start'] + j
            marker = ">>>" if line_num == r['line'] else "   "
            output.append(f"{marker} {line_num}: {ctx_line}")
        output.append("")

    return "\n".join(output)


def kb_search_multi(
    terms: str,
    kb_path: Optional[str] = None,
    operator: str = "AND",
    max_results: int = 30
) -> str:
    """
    Search for multiple terms with AND/OR logic.

    Args:
        terms: Comma-separated search terms (e.g., "ritual,offering,witness")
        kb_path: Path to knowledge base (defaults to ./knowledge_base)
        operator: 'AND' (all terms must match) or 'OR' (any term matches)
        max_results: Maximum number of results to return

    Returns:
        Files matching the search criteria with match details.
    """
    kb = get_kb_path(kb_path)

    if not kb.exists():
        return f"Error: Knowledge base not found at {kb}"

    term_list = [t.strip().lower() for t in terms.split(',')]

    results = []

    for md_file in kb.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8').lower()

            term_matches = {term: term in content for term in term_list}

            if operator == "AND":
                matches = all(term_matches.values())
            else:
                matches = any(term_matches.values())

            if matches:
                matched_terms = [t for t, m in term_matches.items() if m]
                results.append({
                    'file': str(md_file.relative_to(kb)),
                    'matched': matched_terms,
                    'all_matched': all(term_matches.values())
                })

                if len(results) >= max_results:
                    break
        except Exception:
            pass

    results.sort(key=lambda x: (-len(x['matched']), x['file']))

    output = [
        f"Multi-term search: {terms}",
        f"Operator: {operator}",
        f"Found: {len(results)} file(s)",
        ""
    ]

    for r in results:
        match_str = ', '.join(r['matched'])
        full = " [ALL]" if r['all_matched'] else ""
        output.append(f"  {r['file']}{full}")
        output.append(f"    Matched: {match_str}")

    return "\n".join(output)


# =========================================================================
# FILE MOVER
# =========================================================================

def kb_move_file(
    source: str,
    destination: str,
    kb_path: Optional[str] = None,
    dry_run: bool = True
) -> str:
    """
    Move a file and update all cross-references automatically.

    Args:
        source: Current path of file (relative to KB)
        destination: New path for file (relative to KB)
        kb_path: Path to knowledge base (defaults to ./knowledge_base)
        dry_run: If True, show what would change without making changes

    Returns:
        Report of the move operation and all reference updates.
    """
    kb = get_kb_path(kb_path)

    source_path = kb / source
    dest_path = kb / destination

    if not source_path.exists():
        return f"Error: Source file not found: {source}"

    if dest_path.exists():
        return f"Warning: Destination already exists: {destination}"

    source_abs = source_path.resolve()
    updates = []

    for md_file in kb.rglob("*.md"):
        if md_file.resolve() == source_abs:
            continue

        try:
            content = md_file.read_text(encoding='utf-8')
            new_content = content
            file_updated = False

            links = _extract_links_from_content(content)
            for text, link in links:
                resolved = _resolve_relative_path(md_file, link)
                if resolved and resolved.resolve() == source_abs:
                    new_rel = os.path.relpath(dest_path, md_file.parent)
                    old_link = f"[{text}]({link})"
                    new_link = f"[{text}]({new_rel})"
                    new_content = new_content.replace(old_link, new_link)
                    file_updated = True
                    updates.append({
                        'file': str(md_file.relative_to(kb)),
                        'old': link,
                        'new': new_rel
                    })

            if file_updated and not dry_run:
                md_file.write_text(new_content, encoding='utf-8')

        except Exception as e:
            updates.append({
                'file': str(md_file.relative_to(kb)),
                'error': str(e)
            })

    if not dry_run:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.rename(dest_path)

    mode = "DRY RUN - " if dry_run else ""
    lines = [
        f"{mode}Move File Operation",
        f"Source: {source}",
        f"Destination: {destination}",
        f"References to update: {len(updates)}",
        ""
    ]

    if updates:
        lines.append("Reference updates:")
        for u in updates:
            if 'error' in u:
                lines.append(f"  ERROR in {u['file']}: {u['error']}")
            else:
                lines.append(f"  {u['file']}")
                lines.append(f"    {u['old']} -> {u['new']}")

    if dry_run:
        lines.append("")
        lines.append("Run with dry_run=False to execute these changes.")
    else:
        lines.append("")
        lines.append("Move completed successfully.")

    return "\n".join(lines)


# =========================================================================
# SOURCE VALIDATION
# =========================================================================

def kb_check_file_exists(file_path: str, kb_path: Optional[str] = None) -> str:
    """
    Check if a file exists and return its basic info.

    Args:
        file_path: Path to check (relative to KB)
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        File existence status and basic metadata if exists.
    """
    kb = get_kb_path(kb_path)
    fp = kb / file_path

    if fp.exists():
        content = fp.read_text(encoding='utf-8')
        words = _count_words(content)

        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "(no title)"

        source_match = re.search(r'## Source\n([\s\S]*?)(?=\n##|\Z)', content)
        sources = source_match.group(1).strip() if source_match else "(no sources)"

        return f"""File exists: {file_path}

Title: {title}
Words: {words}
Sources:
{sources}

Consider updating this file rather than creating a new one."""
    else:
        parent = fp.parent
        similar = []
        if parent.exists():
            stem = fp.stem.lower()
            for f in parent.glob("*.md"):
                if stem in f.stem.lower() or f.stem.lower() in stem:
                    similar.append(str(f.relative_to(kb)))

        result = f"File does not exist: {file_path}\n"
        if similar:
            result += "\nSimilar files found:\n"
            for s in similar:
                result += f"  {s}\n"

        return result


def kb_validate_source_format(file_path: str, kb_path: Optional[str] = None) -> str:
    """
    Validate that a file follows knowledge base conventions.

    Args:
        file_path: Path to the file to validate (relative to KB)
        kb_path: Path to knowledge base (defaults to ./knowledge_base)

    Returns:
        Validation report with any issues found.
    """
    kb = get_kb_path(kb_path)
    fp = kb / file_path

    if not fp.exists():
        return f"Error: File not found: {file_path}"

    content = fp.read_text(encoding='utf-8')
    issues = []
    info = []

    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        info.append(f"Title: {title_match.group(1)}")
    else:
        issues.append("Missing H1 title at start of file")

    if '## Source' in content:
        source_match = re.search(r'## Source\n([\s\S]*?)(?=\n##|\Z)', content)
        if source_match:
            source_content = source_match.group(1).strip()
            if source_content:
                info.append("Has Source section: Yes")
            else:
                issues.append("Source section is empty")
        else:
            issues.append("Source section format invalid")
    else:
        issues.append("Missing ## Source section")

    if '## See Also' in content:
        info.append("Has See Also section: Yes")
    else:
        info.append("Has See Also section: No (optional but recommended)")

    links = _extract_links_from_content(content)
    broken_links = []
    for text, link in links:
        resolved = _resolve_relative_path(fp, link)
        if resolved and not resolved.exists():
            broken_links.append(f"[{text}]({link})")

    if broken_links:
        issues.append(f"Broken links ({len(broken_links)}):")
        for bl in broken_links:
            issues.append(f"  {bl}")
    else:
        info.append(f"Links validated: {len(links)} (all OK)")

    words = _count_words(content)
    info.append(f"Word count: {words}")
    if words > 1000:
        issues.append(f"File is large ({words} words) - consider splitting")

    lines = [f"Validation: {file_path}", ""]

    if info:
        lines.append("Info:")
        for i in info:
            lines.append(f"  {i}")

    lines.append("")

    if issues:
        lines.append(f"Issues ({len(issues)}):")
        for issue in issues:
            lines.append(f"  - {issue}")
    else:
        lines.append("No issues found!")

    return "\n".join(lines)


def kb_suggest_see_also(
    file_path: str,
    kb_path: Optional[str] = None,
    max_suggestions: int = 10
) -> str:
    """
    Suggest related files for a See Also section based on content overlap.

    Args:
        file_path: Path to the file (relative to KB)
        kb_path: Path to knowledge base (defaults to ./knowledge_base)
        max_suggestions: Maximum number of suggestions

    Returns:
        List of potentially related files with relevance scores.
    """
    kb = get_kb_path(kb_path)
    fp = kb / file_path

    if not fp.exists():
        return f"Error: File not found: {file_path}"

    content = fp.read_text(encoding='utf-8').lower()

    words = re.findall(r'\b[a-z]{4,}\b', content)
    word_freq = defaultdict(int)
    for w in words:
        word_freq[w] += 1

    significant_terms = {w for w, c in word_freq.items() if c >= 2}

    common = {'that', 'this', 'with', 'from', 'have', 'they', 'been', 'were',
              'their', 'which', 'would', 'about', 'into', 'more', 'when',
              'also', 'some', 'than', 'them', 'other', 'what', 'only'}
    significant_terms -= common

    scores = []
    fp_abs = fp.resolve()

    existing_links = set()
    for _, link in _extract_links_from_content(content):
        resolved = _resolve_relative_path(fp, link)
        if resolved:
            existing_links.add(resolved.resolve())

    for md_file in kb.rglob("*.md"):
        if md_file.resolve() == fp_abs:
            continue
        if md_file.resolve() in existing_links:
            continue

        try:
            other_content = md_file.read_text(encoding='utf-8').lower()

            matches = sum(1 for term in significant_terms if term in other_content)

            if matches > 0:
                scores.append({
                    'file': str(md_file.relative_to(kb)),
                    'score': matches,
                    'sample_matches': [t for t in list(significant_terms)[:5] if t in other_content]
                })
        except Exception:
            pass

    scores.sort(key=lambda x: -x['score'])
    scores = scores[:max_suggestions]

    lines = [
        f"See Also suggestions for: {file_path}",
        f"Based on {len(significant_terms)} significant terms",
        ""
    ]

    if scores:
        lines.append("Suggested related files:")
        for s in scores:
            rel_path = os.path.relpath(kb / s['file'], fp.parent)
            lines.append(f"  [{Path(s['file']).stem}]({rel_path})")
            lines.append(f"    Score: {s['score']} | Terms: {', '.join(s['sample_matches'][:3])}")
    else:
        lines.append("No strong matches found.")

    return "\n".join(lines)
