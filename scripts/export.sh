#!/usr/bin/env bash
# Export a project's compiled supplement to DOCX, EPUB, and PDF.
# Usage: scripts/export.sh <project-name> [title]
set -euo pipefail
PROJ="${1:?usage: export.sh <project-name> [title]}"
TITLE="${2:-$PROJ}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/projects/$PROJ/output/compiled_supplement.md"
OUT="$ROOT/projects/$PROJ/output"
[ -f "$SRC" ] || { echo "No compiled supplement at $SRC (run /compile first)"; exit 1; }

# DOCX — custom Node.js exporter with theme + image support
if command -v node >/dev/null 2>&1; then
  node "$ROOT/scripts/export-docx.js" "$SRC" "$OUT/$PROJ.docx" "$TITLE" \
    && echo "  DOCX: done" \
    || echo "  DOCX: export-docx.js failed"
else
  echo "node not found — skipping DOCX export"
fi

# EPUB via pandoc, with the shared stylesheet and an optional cover image
if command -v pandoc >/dev/null 2>&1; then
  epub_cover_flag=()
  cover_img="$ROOT/projects/$PROJ/content/art/cover.png"
  [ -f "$cover_img" ] && epub_cover_flag=(--epub-cover-image="$cover_img")
  pandoc "$SRC" -o "$OUT/$PROJ.epub" \
    --from markdown --to epub3 \
    --toc --toc-depth=3 \
    --css="$ROOT/scripts/epub.css" \
    --resource-path="$OUT" \
    --metadata title="$TITLE" \
    --metadata lang=en \
    ${epub_cover_flag[@]+"${epub_cover_flag[@]}"} 2>/dev/null \
    && echo "  EPUB: done" \
    || echo "  EPUB: pandoc failed"
else
  echo "pandoc not found — skipping EPUB export"
fi

# PDF via pandoc (styled HTML) + weasyprint
if command -v pandoc >/dev/null 2>&1 && command -v weasyprint >/dev/null 2>&1; then
  pandoc "$SRC" --from markdown --to html5 --standalone \
    --template="$ROOT/scripts/pdf-template.html" --toc --toc-depth=3 \
    --resource-path="$OUT" \
    -o "$OUT/$PROJ.body.html" 2>/dev/null \
    || pandoc "$SRC" -o "$OUT/$PROJ.body.html" --standalone --metadata title="$TITLE" \
    || echo "  PDF: pandoc failed"
  if [ -f "$OUT/$PROJ.body.html" ]; then
    weasyprint "$OUT/$PROJ.body.html" "$OUT/$PROJ.pdf" \
      && echo "  PDF: done" \
      || echo "  PDF: weasyprint failed"
    rm -f "$OUT/$PROJ.body.html"
  fi
elif ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc not found — skipping PDF export"
else
  echo "weasyprint not found — skipping PDF export"
fi

echo "Exports written to $OUT/"
