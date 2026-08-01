// Theme-driven DOCX exporter — reads a compiled markdown file and produces a styled DOCX
// Usage: node export-docx.js <input.md> <output.docx> <title>

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, ImageRun
} = require("docx");

const inputFile = process.argv[2];
const outputFile = process.argv[3];
const docTitle = process.argv[4] || path.basename(inputFile, ".md");

if (!inputFile || !outputFile) {
  console.error("Usage: node export-docx.js <input.md> <output.docx> [title]");
  process.exit(1);
}

// === THEME (data-driven; see styles/layout/README in default.md) ===
const repoRoot = path.resolve(__dirname, "..");
let cfg = {};
try { cfg = JSON.parse(fs.readFileSync(path.join(repoRoot, "config", "system.json"), "utf-8")); } catch (e) { /* defaults below */ }
const themeName = (cfg.layout && cfg.layout.docx_theme) || "default";
const themePath = path.join(repoRoot, "styles", "layout", themeName + ".theme.json");
let theme;
try { theme = JSON.parse(fs.readFileSync(themePath, "utf-8")); }
catch (e) { console.error("Cannot read theme " + themePath + " - create it or set layout.docx_theme"); process.exit(1); }
const C = { body: theme.colors.body, maroon: theme.colors.accent1, purple: theme.colors.accent2,
            gold: theme.colors.gold, sidebarBg: theme.colors.sidebarBg, white: theme.colors.white, altRow: theme.colors.altRow };
const F = theme.fonts;
const PG = { ...theme.page };
PG.cw = PG.w - PG.ml - PG.mr;
const publisherLine = (cfg.system && cfg.system.publisher_line) || "";

// === INLINE PARSER ===
function stripAnchors(t) { return t.replace(/\s*\{#[^}]+\}/g, "").trim(); }

function runs(text, defs = {}) {
  const font = defs.font || F.body, size = defs.size || 22, color = defs.color || C.body;
  const bi = defs.italic || false, bb = defs.bold || false;
  const result = [];
  const re = /(\*\*\*(.+?)\*\*\*|\*\*(.+?)\*\*|\*(.+?)\*|\[([^\]]+)\]\([^)]+\))/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) { const s = text.slice(last, m.index); if (s) result.push(new TextRun({ text: s, font, size, color, bold: bb, italics: bi })); }
    if (m[2]) result.push(new TextRun({ text: m[2], font, size, color, bold: true, italics: true }));
    else if (m[3]) result.push(new TextRun({ text: m[3], font, size, color, bold: true, italics: bi }));
    else if (m[4]) result.push(new TextRun({ text: m[4], font, size, color, bold: bb, italics: true }));
    else if (m[5]) result.push(new TextRun({ text: m[5], font, size, color, bold: bb, italics: bi }));
    last = m.index + m[0].length;
  }
  if (last < text.length) { const s = text.slice(last); if (s) result.push(new TextRun({ text: s, font, size, color, bold: bb, italics: bi })); }
  if (!result.length) result.push(new TextRun({ text: text || "", font, size, color, bold: bb, italics: bi }));
  return result;
}

function isAllItalic(l) { const t = l.trim(); return t.startsWith("*") && !t.startsWith("**") && t.endsWith("*") && !t.endsWith("**"); }

// === ELEMENT BUILDERS ===
const bodyP = (t, noIndent) => new Paragraph({
  spacing: { before: 100, after: 100, line: 720 }, alignment: AlignmentType.JUSTIFIED,
  indent: noIndent ? {} : { firstLine: 187 },
  children: runs(t, { italic: isAllItalic(t) }),
});

const h1 = t => new Paragraph({
  heading: HeadingLevel.HEADING_1, pageBreakBefore: true, spacing: { before: 480, after: 120 },
  children: [new TextRun({ text: stripAnchors(t), font: F.heading, size: 56, bold: true, color: C.maroon })],
});

const h2 = t => new Paragraph({
  heading: HeadingLevel.HEADING_2, alignment: AlignmentType.CENTER, spacing: { before: 360, after: 120 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.maroon, space: 4 } },
  children: [new TextRun({ text: stripAnchors(t), font: F.heading, size: 48, color: C.maroon })],
});

const h3 = t => new Paragraph({
  heading: HeadingLevel.HEADING_3, spacing: { before: 240, after: 80 },
  children: [new TextRun({ text: stripAnchors(t), font: F.heading, size: 36, color: C.purple })],
});

const h4 = t => new Paragraph({
  heading: HeadingLevel.HEADING_4, spacing: { before: 200, after: 60 },
  children: [new TextRun({ text: stripAnchors(t), font: F.heading, size: 28, color: C.purple })],
});

const bullet = t => new Paragraph({
  numbering: { reference: "bullets", level: 0 }, spacing: { before: 40, after: 40 },
  children: runs(t),
});

const hr = () => new Paragraph({
  spacing: { before: 240, after: 240 }, alignment: AlignmentType.CENTER,
  border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: C.purple, space: 1 } },
  children: [new TextRun({ text: "", size: 4 })],
});

function sidebarTable(lines) {
  const ch = [];
  for (const line of lines) {
    const s = line.replace(/^>\s?/, "").trim();
    if (!s) continue;
    if (s.startsWith("**") && ch.length === 0) {
      ch.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 80 },
        children: [new TextRun({ text: s.replace(/\*\*/g, "").replace(/\{#[^}]+\}/g, "").trim(), font: F.heading, size: 32, bold: true, color: C.white })],
      }));
    } else {
      ch.push(new Paragraph({ spacing: { before: 40, after: 40 }, children: runs(s, { font: F.sidebar, size: 20, color: C.white }) }));
    }
  }
  if (!ch.length) return null;
  const nb = { style: BorderStyle.NONE, size: 0, color: C.sidebarBg };
  return new Table({ width: { size: PG.cw, type: WidthType.DXA }, columnWidths: [PG.cw], rows: [
    new TableRow({ children: [new TableCell({
      borders: { top: nb, bottom: nb, left: nb, right: nb },
      width: { size: PG.cw, type: WidthType.DXA },
      shading: { fill: C.sidebarBg, type: ShadingType.CLEAR },
      margins: { top: 216, bottom: 216, left: 216, right: 216 }, children: ch,
    })] }),
  ]});
}

function contentTable(rows) {
  if (rows.length < 2) return null;
  const hdr = rows[0].split("|").map(c => c.trim()).filter(c => c);
  const data = rows.slice(2).filter(r => r.trim() && !r.match(/^\|[\s-|]+\|$/));
  const n = hdr.length; if (!n) return null;
  const cw = Math.floor(PG.cw / n);
  const widths = Array(n).fill(cw); widths[n - 1] = PG.cw - cw * (n - 1);
  const b = { style: BorderStyle.SINGLE, size: 1, color: C.body };
  const bdr = { top: b, bottom: b, left: b, right: b };
  const cm = { top: 40, bottom: 40, left: 80, right: 80 };

  const tRows = [new TableRow({ children: hdr.map((c, i) => new TableCell({
    borders: bdr, width: { size: widths[i], type: WidthType.DXA },
    shading: { fill: C.purple, type: ShadingType.CLEAR }, margins: cm,
    children: [new Paragraph({ children: [new TextRun({ text: c, font: F.body, size: 20, bold: true, color: C.white })] })],
  })) })];

  for (let r = 0; r < data.length; r++) {
    const cells = data[r].split("|").map(c => c.trim()).filter(c => c);
    tRows.push(new TableRow({ children: cells.slice(0, n).map((c, i) => new TableCell({
      borders: bdr, width: { size: widths[i] || widths[n - 1], type: WidthType.DXA },
      shading: { fill: r % 2 === 0 ? C.altRow : "FFFFFF", type: ShadingType.CLEAR }, margins: cm,
      children: [new Paragraph({ children: runs(c, { size: 20 }) })],
    })) }));
  }
  return new Table({ width: { size: PG.cw, type: WidthType.DXA }, columnWidths: widths, rows: tRows });
}

// === MAIN ===
async function build() {
  const md = fs.readFileSync(inputFile, "utf-8");
  const lines = md.split("\n");
  const children = [];

  // Detect title and subtitle from first lines
  let title = docTitle, subtitle = "";
  for (let j = 0; j < Math.min(10, lines.length); j++) {
    if (lines[j].startsWith("# ") && !lines[j].startsWith("# Chapter")) { title = stripAnchors(lines[j].slice(2)); }
    if (lines[j].startsWith("## ") && j < 5) { subtitle = stripAnchors(lines[j].slice(3)); }
  }

  // Cover image (if present at the start of the file)
  for (let j = 0; j < Math.min(5, lines.length); j++) {
    const coverMatch = lines[j].match(/^!\[([^\]]*[Cc]over[^\]]*)\]\(([^)]+)\)/);
    if (coverMatch) {
      const coverPath = path.resolve(path.dirname(inputFile), coverMatch[2]);
      if (fs.existsSync(coverPath)) {
        try {
          const coverData = fs.readFileSync(coverPath);
          children.push(new Paragraph({
            alignment: AlignmentType.CENTER,
            spacing: { before: 0, after: 0 },
            children: [new ImageRun({ data: coverData, transformation: { width: 584, height: 876 }, type: "png" })],
          }));
          children.push(new Paragraph({ children: [new PageBreak()] }));
        } catch (e) { /* skip */ }
      }
      break;
    }
  }

  // Title page
  children.push(new Paragraph({ spacing: { before: 4800 }, children: [] }));
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
    children: [new TextRun({ text: title, font: F.heading, size: 120, color: C.maroon })],
  }));
  if (subtitle) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
      children: [new TextRun({ text: subtitle, font: F.heading, size: 36, color: C.purple })],
    }));
  }
  if (publisherLine) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
      children: [new TextRun({ text: publisherLine, font: F.body, size: 22, italics: true, color: C.body })],
    }));
  }
  children.push(new Paragraph({ children: [new PageBreak()] }));

  // TOC
  children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 400 },
    children: [new TextRun({ text: "Table of Contents", font: F.heading, size: 48, color: C.maroon })],
  }));
  children.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }));
  children.push(new Paragraph({ children: [new PageBreak()] }));

  // Find content start — skip title, subtitle, credits, and TOC
  // Strategy: find the TOC section, then start after its closing ---
  // If no TOC, find the first chapter/section heading after line 5
  let start = 0;

  // First, try to find a TOC and skip past it
  for (let j = 0; j < lines.length; j++) {
    if (lines[j].match(/^#{1,2} Table of Contents/i)) {
      // Skip ahead to the --- after the TOC entries
      for (let k = j + 1; k < lines.length; k++) {
        if (lines[k].trim() === "---") { start = k + 1; break; }
        // If we hit a heading that's not a TOC entry, start there
        if (lines[k].match(/^#{1,2} /) && !lines[k].match(/Table of Contents/i) && k > j + 1) { start = k; break; }
      }
      break;
    }
  }

  // Fallback: find first chapter-like heading (H1 or H2) after the front matter
  if (start === 0) {
    for (let j = 5; j < lines.length; j++) {
      if (lines[j].match(/^#{1,2} (Chapter|Appendix|Part|Introduction|Preface|Prologue)/i) ||
          (lines[j].match(/^# /) && j > 10)) {
        start = j; break;
      }
    }
  }

  let i = start, fah = false;

  while (i < lines.length) {
    const line = lines[i], t = line.trim();
    if (!t) { i++; continue; }

    if (t === "---" || t === "***" || t === "___") { children.push(hr()); i++; fah = false; continue; }

    if (t.startsWith("#### ")) { children.push(h4(t.slice(5))); i++; fah = true; continue; }
    if (t.startsWith("### ")) { children.push(h3(t.slice(4))); i++; fah = true; continue; }
    if (t.startsWith("## ")) { children.push(h2(t.slice(3))); i++; fah = true; continue; }
    if (t.startsWith("# ")) { children.push(h1(t.slice(2))); i++; fah = true; continue; }

    if (t.startsWith(">")) {
      const bl = [];
      while (i < lines.length && (lines[i].trim().startsWith(">") || lines[i].trim() === "")) {
        if (lines[i].trim() === "" && i + 1 < lines.length && !lines[i + 1].trim().startsWith(">")) break;
        bl.push(lines[i]); i++;
      }
      const sb = sidebarTable(bl); if (sb) children.push(sb);
      fah = false; continue;
    }

    if (t.startsWith("|")) {
      const tl = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) { tl.push(lines[i].trim()); i++; }
      const tb = contentTable(tl); if (tb) children.push(tb);
      fah = false; continue;
    }

    if (t.startsWith("- ")) {
      while (i < lines.length && lines[i].trim().startsWith("- ")) { children.push(bullet(lines[i].trim().slice(2))); i++; }
      fah = false; continue;
    }

    if (t.startsWith("![")) {
      const imgMatch = t.match(/^!\[([^\]]*)\]\(([^)]+)\)/);
      if (imgMatch) {
        const imgSrc = imgMatch[2];
        const imgPath = path.resolve(path.dirname(inputFile), imgSrc);
        if (fs.existsSync(imgPath)) {
          try {
            const imgData = fs.readFileSync(imgPath);
            // Fit to content width, maintain 2:3 aspect ratio for covers
            const isCover = imgMatch[1].toLowerCase().includes("cover") || imgSrc.includes("cover");
            const imgW = isCover ? 584 : 500;
            const imgH = isCover ? 876 : Math.round(imgW * 1.5);
            const imgPara = new Paragraph({
              alignment: AlignmentType.CENTER,
              spacing: { before: isCover ? 0 : 200, after: isCover ? 0 : 200 },
              children: [new ImageRun({ data: imgData, transformation: { width: imgW, height: imgH }, type: "png" })],
            });
            if (isCover) {
              children.push(imgPara);
              children.push(new Paragraph({ children: [new PageBreak()] }));
            } else {
              children.push(imgPara);
            }
          } catch (e) { /* skip unreadable images */ }
        }
      }
      i++; continue;
    }

    children.push(bodyP(t, fah)); fah = false; i++;
  }

  const doc = new Document({
    styles: {
      default: { document: { run: { font: F.body, size: 22, color: C.body } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: F.heading, size: 56, bold: true, color: C.maroon },
          paragraph: { spacing: { before: 480, after: 120 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: F.heading, size: 48, color: C.maroon },
          paragraph: { spacing: { before: 360, after: 120 }, alignment: AlignmentType.CENTER, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: F.heading, size: 36, color: C.purple },
          paragraph: { spacing: { before: 240, after: 80 }, outlineLevel: 2 } },
        { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: F.heading, size: 28, color: C.purple },
          paragraph: { spacing: { before: 200, after: 60 }, outlineLevel: 3 } },
      ],
    },
    numbering: { config: [{
      reference: "bullets",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 288, hanging: 288 } }, run: { color: C.purple } } }],
    }] },
    sections: [{
      properties: {
        page: { size: { width: PG.w, height: PG.h }, margin: { top: PG.mt, right: PG.mr, bottom: PG.mb, left: PG.ml } },
      },
      headers: { default: new Header({ children: [new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [new TextRun({ text: title, font: F.header, size: 20, color: C.purple })],
      })] }) },
      footers: { default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], font: F.body, size: 18, color: C.body })],
      })] }) },
      children,
    }],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputFile, buffer);
  console.log("  DOCX: " + (buffer.length / 1024).toFixed(0) + " KB");
}

build().catch(err => { console.error(err); process.exit(1); });
