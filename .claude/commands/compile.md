# Compile Final Supplement

Assemble all final drafts into a single publication-ready document.

## Your Task

You are executing **Phase 6: Final Compilation**.

**Project identifier**: $ARGUMENTS

### Prerequisites

Read `state/project_state.json` and verify `quality_gates.final_draft` is `true`. All `final_draft.md` files must exist and be approved.

### Step 1: Compilation

The **Project Architect** assembles the complete supplement:

1. Read all `content/chapter_XX/final_draft.md` files in order
2. Read the art manifest via `list_art_manifest` to get all generated artwork
3. Create `output/compiled_supplement.md` containing:
   - Cover image: `![Cover](../content/art/cover.png)` as the very first element
   - Professional title page with supplement name, tagline, and credits — include the publisher line from `system.publisher_line` in `config/system.json` if it is set (omit the line entirely if empty)
   - Table of contents with chapter/section navigation
   - For each chapter:
     - Chapter opener image before the chapter heading: `![Chapter X](../content/art/chapter_XX_opener.png)`
     - Chapter content with art placed inline:
       - Character portraits inserted near the NPC's first appearance or stat block
       - Content illustrations (landscape/column) distributed per `art.density_words_per_illustration` in `config/system.json` (default 2,250 words), placed near the content they depict
   - Appendices (quick reference tables, index, etc.)
   - Legal/credits page with art attributions
4. Validate all internal cross-references resolve correctly
5. Ensure consistent formatting throughout
6. Verify all referenced image files exist in `content/art/`

### Step 2: Post-Compilation Validation

The **Final Reviewer** (publication standards) and **Consistency Checker** (cross-reference integrity) together perform tool-verified checks on the compiled output:

**1. Total Word Count**
- Run `count_words_in_directory` on the content directory
- Run `count_words` on the compiled output file
- Record totals in project_state.json

**2. Forbidden Pattern Scan**
- Read `development/outlines/forbidden_patterns.md`
- Grep the compiled output for every forbidden pattern
- Zero tolerance — any match means the compilation is not ready

**3. Heading Link Integrity**
- Extract all `](#...)` references from the compiled document
- Verify each target heading exists within the compiled document (not just individual files)
- Report any broken links

**4. Image Reference Verification**
- Extract all `![...](...png)` and `![...](...jpg)` references
- Verify each referenced image file exists in `content/art/`
- If `development/art_prompts.md` exists (prompt-manifest mode from `/art-direction`), missing images are expected and acceptable — strip the corresponding image references from the compiled output instead of failing
- Otherwise, report any missing images as errors

**5. Duplicate Heading ID Check**
- Scan the compiled document for duplicate heading text that would create conflicting anchor IDs
- Report any duplicates that could break cross-references

**6. Cohesion Review**
- Compiled document reads as a cohesive whole
- No formatting artifacts from file concatenation
- Professional presentation throughout
- Document is ready for layout/typesetting

### Step 3: Layout Style Selection

Before generating exports, confirm the **layout style** (visual design for DOCX/PDF). Layout is config-driven, not chosen by hand each time:

1. Read `layout.style_file` and `layout.docx_theme` from `config/system.json`
2. List all `.md` files in the `styles/layout/` directory and confirm `layout.style_file` points at one of them
3. Read the chosen style file — it documents the design language (palette, typography, page geometry) that the `docx_theme` JSON data file implements for the DOCX exporter
4. If the project calls for a different look than the configured default, ask the user whether to switch `layout.style_file`/`layout.docx_theme` to another available style (or create a new one) before proceeding — otherwise proceed with the configured style

(Writing style was fixed during planning and is not re-selected here — see `development/outlines/writing_style.md` if you need to recall it.)

### Step 4: Export Formats

After validation passes and a style is selected, generate publication-ready exports from `output/compiled_supplement.md`. All export files go in `output/`, named from `[PROJECT_NAME]` (the project directory slug) — the supplement title is used only as the document's internal title metadata, not the filename.

**Cover placement (applies to every export)**: `content/art/cover.png` must appear as the first visible element of every output format below (DOCX, PDF, EPUB, triple-spaced PDF). If the cover does not exist, halt and run `/art-direction [PROJECT_NAME]` first — compile may not complete without a cover. (If the user explicitly chose a deferred/prompt-only cover in `/art-direction`, proceed but emit a loud warning in the final report naming each output that shipped coverless.)

**1-3. DOCX / EPUB / PDF Export**

Run the export pipeline script:

```bash
scripts/export.sh [PROJECT_NAME] "[Supplement Title]"
```

This produces `output/[PROJECT_NAME].docx`, `output/[PROJECT_NAME].epub`, and `output/[PROJECT_NAME].pdf` in one pass — filenames come from the first (project-slug) argument, not the title:

- **DOCX**: `scripts/export-docx.js` reads `layout.docx_theme` from `config/system.json`, loads the matching `styles/layout/[theme].theme.json` data file for fonts/colors/page geometry, and applies `system.publisher_line` to the title-page subtitle. It embeds images via `ImageRun`, builds proper heading styles with `outlineLevel` for the TOC, and renders sidebars as shaded single-cell tables. This is the only export format that reads the configured layout theme.
- **EPUB**: via pandoc, using the shared `scripts/epub.css` stylesheet (a static, neutral stylesheet — not theme-driven); includes `content/art/cover.png` as the cover image if it exists. Edit `scripts/epub.css` directly to restyle EPUB output.
- **PDF**: via pandoc (`scripts/pdf-template.html`) piped through weasyprint. `scripts/pdf-template.html` is also a static, neutral stylesheet — it does not read `layout.docx_theme` or any other config; PDF and DOCX will not visually match unless `scripts/pdf-template.html` is edited by hand to mirror the theme.

If `scripts/export.sh` is unavailable or a format needs to be regenerated individually, the script's own steps (`node scripts/export-docx.js`, pandoc, weasyprint) can be invoked directly — see the script for exact invocations.

**4. Triple-Spaced Editing PDF**

A second PDF is generated at triple line spacing for editorial markup.

- Use a minimal serif template (Georgia / Palatino fallback chain) — no decorative styling; the goal is high-margin readable text the editor can mark up.
- **Critical**: `body`, `p`, `li`, `blockquote` all carry `line-height: 3.0`. Headings keep tight spacing (`line-height: 1.4`) so they remain visually distinct. TOC entries use `line-height: 2.0`.
- Page layout: US Letter, 1" margins on all sides, page numbers bottom-center.
- **Include the cover** as the first page (full-bleed or centered within the page; do NOT suppress it). The editor needs to see the same visual identity the reader does.
- Convert via pandoc HTML5 → weasyprint (same toolchain as the styled PDF).
- **Verify spacing**: page count of the triple-spaced PDF must be at least ~2.5x the page count of the normal styled PDF. If the ratio is below 2.5x, the line-height did not apply correctly — investigate before proceeding.
- The triple-spaced output is **not** placed in `output/` (it is a working artifact, not a supplement export). It is placed at:

```
<EDITING_DIR>/<Natural Title>.pdf
```

Where `<EDITING_DIR>` is a user-configured local folder for editorial review copies (e.g. a synced desktop or documents folder — set this to whatever path makes sense on your machine), and `<Natural Title>` is the supplement's natural-language title from `state/project_state.json` `project_title` (with Windows-illegal characters `< > : " / \ | ? *` replaced by ` - ` and whitespace collapsed). Examples:
- `project_title: "Craft Book: The Salt Roads"` → `Craft Book - The Salt Roads.pdf`
- `project_title: "The Crucible: A Continent at War"` → `The Crucible - A Continent at War.pdf`

If the destination directory does not exist, create it with `mkdir -p`.

**5. Verify Exports**
- Confirm all four files exist and have non-zero size:
  - `output/compiled_supplement.md`, `output/[PROJECT_NAME].docx`, `output/[PROJECT_NAME].pdf`, `output/[PROJECT_NAME].epub`
  - `<EDITING_DIR>/<Natural Title>.pdf` (triple-spaced)
- Report file sizes in the output summary
- Report the triple-spaced page-count ratio as evidence the spacing applied

### Step 5: Project Completion

Update `state/project_state.json`:
- Set `current_phase` to `"completed"`
- Set `status` to `"completed"`
- Set `quality_gates.compilation` to `true`
- Log `COMPILATION_READY` message
- Record final word counts and completion metrics

### Output

Report to user:
- Final supplement files in `projects/[PROJECT_NAME]/output/`:
  - `compiled_supplement.md` — source markdown
  - `[PROJECT_NAME].docx` — Word document, styled per `layout.docx_theme`
  - `[PROJECT_NAME].pdf` — PDF, styled per the static `scripts/pdf-template.html` (not theme-driven)
  - `[PROJECT_NAME].epub` — e-book, styled per the static `scripts/epub.css` (not theme-driven)
- Editing copy at `<EDITING_DIR>/<Natural Title>.pdf` — triple-spaced for editorial markup
- File sizes for each format (including triple-spaced)
- Triple-spaced page-count ratio (should be ~3x; flag if <2.5x)
- Total word count and per-chapter breakdown
- Quality gate summary (all should be true)
- Any notes or recommendations for future revision
