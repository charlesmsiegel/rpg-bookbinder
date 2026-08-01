# Default Layout Theme

A neutral, professional theme for compiled DOCX output. No publisher-specific branding —
a cool slate-and-gold palette and a classic serif/antiqua pairing that reads as a generic
"quality RPG hardcover" without borrowing any one company's house style. Values below match
`default.theme.json` in this directory; `/compile` reads that file when `layout.docx_theme`
in `config/system.json` is set to `"default"`.

## Palette

| Token | Hex | Usage |
|---|---|---|
| `body` | `#1A1A1A` | Body text color — near-black, not pure black (softer on the page). |
| `accent1` | `#37474F` | Primary accent — chapter headings, rules headers, major dividers. |
| `accent2` | `#546E7A` | Secondary accent — subheadings, pull-quote rules, table header fills. |
| `gold` | `#B0A16B` | Sparing highlight — sidebar title bars, decorative rules, callout borders. Use it as a garnish, not a fill. |
| `sidebarBg` | `#263238` | Background fill for sidebars and stat-block boxes. Pair with `white` text. |
| `white` | `#FFFFFF` | Text on dark fills (`sidebarBg`, `accent1`), and page background. |
| `altRow` | `#F4F4F2` | Alternating table-row fill — a near-white warm gray, not a saturated tint. |

## Typography

| Token | Font | Used for |
|---|---|---|
| `body` | Georgia | Running body text. A widely-available serif with good x-height at print size. |
| `heading` | Book Antiqua | Chapter titles, section headings. |
| `toc` | Book Antiqua | Table of contents entries — matches heading font for visual continuity. |
| `header` | Book Antiqua | Running page headers/footers. |
| `sidebar` | Calibri | Sidebar and stat-block body text — a sans-serif break from body copy signals "boxed content" without a border. |

All four named fonts ship with common office suites; the theme doesn't require any font
installation to render correctly.

## Page and spacing

Page size is US Letter (`w: 12240` × `h: 15840` twips, 8.5in × 11in at 1440 twips/inch).
Margins: `ml`/`mr: 1080` twips (0.75in) for a wide text column typical of RPG hardcovers,
`mt: 1267` twips (~0.88in) to leave room for a running header, `mb: 1440` twips (1in).

- Keep one blank paragraph of spacing above H2/H3 headings, none below — headings should
  sit close to the text they introduce.
- Sidebars and stat blocks get `sidebarBg` fill, `white` text, and a `gold` 0.5pt–1pt top/bottom
  rule; don't box every side (a full border reads as a scanned photocopy, not a printed book).
- Tables use `accent2` for the header row fill (white text), `altRow` for every other body
  row, and no vertical rules — horizontal rules only, to keep dense stat tables legible.

## Creating your own theme

To create your own theme, copy `default.theme.json` to `<name>.theme.json`, adjust the
values, describe it in `<name>.md`, and set `layout.docx_theme` to `<name>` in
`config/system.json`.
