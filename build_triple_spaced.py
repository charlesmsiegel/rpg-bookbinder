#!/usr/bin/env python3
"""Generate triple-spaced PDFs for editing.

For each project's compiled markdown, build a clean triple-spaced PDF named
<Natural Title>.pdf. By default each PDF is written into that project's own
output/ directory; pass --output-dir to collect all PDFs into a single
shared destination instead.
"""
import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path

# HTML template — minimal styling, large margins, TRIPLE-SPACED line-height
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
@page {{
  size: 8.5in 11in;
  margin: 1in;
  @bottom-center {{
    content: counter(page);
    font-family: Georgia, serif;
    font-size: 10pt;
  }}
}}
body {{
  font-family: Georgia, 'Book Antiqua', Palatino, serif;
  font-size: 12pt;
  line-height: 3.0;
  color: #000;
  text-align: left;
  hyphens: none;
  orphans: 3;
  widows: 3;
}}
h1 {{
  font-family: 'Palatino Linotype', Palatino, serif;
  font-size: 22pt;
  font-weight: bold;
  page-break-before: always;
  page-break-after: avoid;
  margin: 24pt 0 12pt 0;
  line-height: 1.4;
}}
h1:first-of-type {{ page-break-before: avoid; }}
h2 {{
  font-family: 'Palatino Linotype', Palatino, serif;
  font-size: 18pt;
  margin: 18pt 0 6pt 0;
  page-break-after: avoid;
  line-height: 1.4;
}}
h3 {{
  font-family: 'Palatino Linotype', Palatino, serif;
  font-size: 15pt;
  margin: 12pt 0 4pt 0;
  page-break-after: avoid;
  line-height: 1.4;
}}
h4, h5, h6 {{
  font-family: 'Palatino Linotype', Palatino, serif;
  font-size: 13pt;
  margin: 10pt 0 3pt 0;
  page-break-after: avoid;
  line-height: 1.4;
}}
p {{
  margin: 6pt 0;
  text-indent: 0;
  line-height: 3.0;
}}
strong {{ font-weight: bold; }}
em {{ font-style: italic; }}
blockquote {{
  margin: 12pt 0 12pt 0.4in;
  padding-left: 12pt;
  border-left: 2pt solid #888;
  font-style: italic;
  line-height: 3.0;
}}
ul, ol {{
  margin: 6pt 0;
  padding-left: 0.4in;
  line-height: 3.0;
}}
li {{ line-height: 3.0; margin: 3pt 0; }}
table {{
  border-collapse: collapse;
  margin: 12pt auto;
  font-size: 10pt;
  line-height: 1.5;
  page-break-inside: avoid;
}}
table th, table td {{
  padding: 4pt 8pt;
  border: 0.5pt solid #555;
  text-align: left;
  vertical-align: top;
}}
table thead th {{ background: #ddd; font-weight: bold; }}
hr {{
  border: 0;
  border-top: 0.5pt solid #888;
  margin: 18pt auto;
  width: 80%;
}}
a {{ color: #000; text-decoration: none; }}
img {{ max-width: 100%; }}
nav#TOC {{ page-break-after: always; line-height: 2.0; }}
nav#TOC h1 {{ page-break-before: avoid; }}
nav#TOC ul {{ list-style: none; padding-left: 0; }}
nav#TOC ul ul {{ padding-left: 0.3in; }}
nav#TOC li {{ margin: 4pt 0; line-height: 2.0; }}

/* Image references with broken paths get hidden */
img[alt="Cover"] {{ display: none; }}
</style>
</head>
<body>
{toc}
{body}
</body>
</html>"""


def get_natural_title(project_dir: Path, md_path: Path) -> str:
    """Get the natural language title for a project."""
    # Try state/project_state.json first
    state = project_dir / 'state' / 'project_state.json'
    if state.exists():
        try:
            d = json.loads(state.read_text())
            t = d.get('project_title') or d.get('title')
            if t:
                return t
        except Exception:
            pass
    # Fallback: first H1 of the markdown
    if md_path.exists():
        for line in md_path.read_text().split('\n')[:30]:
            m = re.match(r'^#\s+(.+?)\s*(?:\{#.*?\})?\s*$', line)
            if m:
                return m.group(1)
    # Final fallback: project directory name
    return project_dir.name.replace('-', ' ').title()


def safe_filename(title: str) -> str:
    """Convert a natural title into a filesystem-safe filename (preserves spaces and natural chars)."""
    # Remove characters that are invalid on Windows: < > : " / \ | ? *
    cleaned = re.sub(r'[<>:"/\\|?*]', ' - ', title)
    # Collapse whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned + '.pdf'


def build_pdf(md_path: Path, title: str, output_path: Path) -> tuple[bool, str]:
    """Build a triple-spaced PDF from the given markdown file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        html_body = tmp / 'body.html'
        html_full = tmp / 'full.html'

        # Convert MD to HTML body via pandoc (with TOC)
        try:
            result = subprocess.run(
                ['pandoc', str(md_path),
                 '--from', 'markdown-yaml_metadata_block',
                 '--to', 'html5',
                 '--toc', '--toc-depth=3',
                 '-o', str(html_full),
                 '--metadata', f'title={title}',
                 '--standalone'],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode != 0:
                return False, f'pandoc failed: {result.stderr[:200]}'
        except subprocess.TimeoutExpired:
            return False, 'pandoc timeout'

        # Extract body and toc from pandoc-generated HTML
        full_html = html_full.read_text()
        body_match = re.search(r'<body[^>]*>(.*?)</body>', full_html, re.DOTALL)
        if not body_match:
            return False, 'pandoc html missing body'
        body_inner = body_match.group(1)
        # Extract TOC if present (pandoc puts it in <nav id="TOC">...</nav>)
        toc_match = re.search(r'(<nav[^>]*id="TOC".*?</nav>)', body_inner, re.DOTALL)
        toc_html = toc_match.group(1) if toc_match else ''
        if toc_match:
            body_inner = body_inner.replace(toc_match.group(1), '')

        # Wrap in our triple-spaced template
        styled_html = HTML_TEMPLATE.format(title=title, toc=toc_html, body=body_inner)
        styled_path = tmp / 'styled.html'
        styled_path.write_text(styled_html)

        # Run weasyprint
        try:
            result = subprocess.run(
                ['weasyprint', str(styled_path), str(output_path)],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode != 0:
                return False, f'weasyprint failed: {result.stderr[:300]}'
        except subprocess.TimeoutExpired:
            return False, 'weasyprint timeout'

        if not output_path.exists() or output_path.stat().st_size == 0:
            return False, 'output file missing or empty'
        return True, f'{output_path.stat().st_size:,} bytes'


def main():
    parser = argparse.ArgumentParser(
        description="Build triple-spaced PDFs from each project's compiled markdown.")
    parser.add_argument('--projects-dir', type=Path, default=Path('projects'),
                         help="Directory containing project folders (default: ./projects)")
    parser.add_argument('--output-dir', type=Path, default=None,
                         help="Write all PDFs into this single directory instead of each "
                              "project's own output/ directory")
    args = parser.parse_args()

    projects_dir = args.projects_dir
    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    # Find all project compiled markdowns
    targets = []
    for proj_dir in sorted(projects_dir.iterdir()):
        if not proj_dir.is_dir():
            continue
        output_dir = proj_dir / 'output'
        if not output_dir.exists():
            continue
        # Look for .md files in output (skip OLD_, skip -triple-spaced)
        for md in sorted(output_dir.glob('*.md')):
            name = md.name
            if name.startswith('OLD_') or '-triple-spaced' in name:
                continue
            targets.append((proj_dir, md))

    print(f"Found {len(targets)} compiled markdown files\n")

    results = []
    for proj_dir, md_path in targets:
        title = get_natural_title(proj_dir, md_path)
        # For multi-volume projects with multiple .md files, distinguish by stem
        base_md_stem = md_path.stem
        proj_name_normalized = proj_dir.name.replace('-', ' ').lower()

        # If the markdown stem differs from the project's slug, include the stem-derived suffix
        if base_md_stem.lower().replace('-', ' ') != proj_name_normalized:
            # Use the stem-derived natural form as a sub-title or combined name
            stem_natural = base_md_stem.replace('-', ' ').replace('_', ' ').title()
            # Don't double-stamp if title already covers it
            if stem_natural.lower() not in title.lower():
                full_title = f"{title} — {stem_natural}"
            else:
                full_title = title
        else:
            full_title = title

        out_filename = safe_filename(full_title)
        dest_dir = args.output_dir if args.output_dir else (proj_dir / 'output')
        dest_dir.mkdir(parents=True, exist_ok=True)
        out_path = dest_dir / out_filename
        print(f"[{proj_dir.name}]")
        print(f"  Source: {md_path}")
        print(f"  Title:  {full_title}")
        print(f"  Output: {out_path}")
        ok, msg = build_pdf(md_path, full_title, out_path)
        if ok:
            print(f"  ✓ {msg}")
        else:
            print(f"  ✗ FAILED: {msg}")
        results.append((proj_dir.name, full_title, ok, msg))
        print()

    print("=" * 70)
    successes = sum(1 for _, _, ok, _ in results if ok)
    print(f"Built {successes}/{len(results)} triple-spaced PDFs")
    failures = [(p, t, m) for p, t, ok, m in results if not ok]
    if failures:
        print("\nFailures:")
        for p, t, m in failures:
            print(f"  {p} ({t}): {m}")


if __name__ == '__main__':
    main()
