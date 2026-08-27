#!/usr/bin/env python3
"""Print an HTML file to PDF with headless Chromium.

`scripts/export.sh` renders PDFs with weasyprint, which needs the GTK/Pango
stack. That is a system-level install and is absent on some machines (on
Windows it typically is), so this is the fallback renderer: Playwright driving
the Chromium it already ships.

The one thing bare `chrome --print-to-pdf` cannot do is page numbers — Chromium
does not implement CSS paged-media counters, so `@page { @bottom-center }` is
ignored. Playwright exposes Chromium's own header/footer templates instead,
which is how `--footer` puts a page number on every page.

Usage:
    python tools/html_to_pdf.py in.html out.pdf --footer --margin 1in
"""

from __future__ import annotations

import argparse
import glob
import os
import sys
from pathlib import Path


def find_chromium() -> str | None:
    """Prefer Playwright's own build, then a system Chrome or Edge."""
    pats = [
        os.path.expandvars(r"%LOCALAPPDATA%\ms-playwright\chromium-*\chrome-win64\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Microsoft\Edge\Application\msedge.exe"),
        "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
        "/usr/bin/chromium",
        "/usr/bin/google-chrome",
    ]
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


FOOTER = (
    '<div style="width:100%;font-family:Georgia,serif;font-size:9px;'
    'color:#555;text-align:center;padding-top:6px;">'
    '<span class="pageNumber"></span></div>'
)
BLANK = '<div style="display:none"></div>'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("pdf")
    ap.add_argument("--margin", default="0.75in")
    ap.add_argument("--footer", action="store_true",
                    help="print a centred page number at the foot of each page")
    ap.add_argument("--timeout", type=int, default=180_000)
    args = ap.parse_args()

    exe = find_chromium()
    if not exe:
        print("no Chromium/Chrome/Edge found", file=sys.stderr)
        return 3

    src = Path(args.html).resolve()
    out = Path(args.pdf).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe)
        page = browser.new_page()
        page.goto(src.as_uri(), wait_until="load", timeout=args.timeout)
        # Local images decode after load; give layout a moment so page count is stable.
        page.wait_for_timeout(2500)
        page.pdf(path=str(out), format="Letter", print_background=True,
                 display_header_footer=args.footer,
                 header_template=BLANK,
                 footer_template=FOOTER if args.footer else BLANK,
                 margin={"top": args.margin, "bottom": args.margin,
                         "left": args.margin, "right": args.margin})
        browser.close()

    size = out.stat().st_size
    print("wrote %s (%s bytes)" % (out, format(size, ",")))
    return 0 if size else 1


if __name__ == "__main__":
    raise SystemExit(main())
