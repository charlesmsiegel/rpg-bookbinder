#!/usr/bin/env python3
"""Assemble a project's final drafts and artwork into one publication markdown.

Reads `content/chapter_*/final_draft.md` in order and `development/art_prompts.md`
for placement, and writes `output/compiled_supplement.md`: cover, title page,
table of contents, then each chapter preceded by its opener image with portraits
and content illustrations placed inline, followed by a credits page.

Image paths are written relative to `output/`, since that is where the compiled
markdown lives and where the exporters run from.

Usage:
    python tools/compile_supplement.py prism --title PRISM --tagline "Split the light"
"""

from __future__ import annotations

import argparse
import io
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def slug(heading: str) -> str:
    s = heading.strip().lower()
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"\*\*|\*|_", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s.strip())


def read_placements(project: Path) -> tuple[dict, dict, dict]:
    """-> (openers by chapter, portraits by subject, illustrations by (chapter, heading))"""
    path = project / "development" / "art_prompts.md"
    openers, portraits, illos = {}, {}, {}
    if not path.exists():
        return openers, portraits, illos
    for block in path.read_text(encoding="utf-8").split("\n## ")[1:]:
        name = block.split("\n", 1)[0].strip()
        if not name.endswith(".png"):
            continue
        m = re.search(r"- \*\*Placement\*\*: (.+)", block)
        if not m:
            continue
        place = m.group(1).strip()
        if (mm := re.match(r"chapter (\d+) opener", place)):
            openers[int(mm.group(1))] = name
        elif (mm := re.match(r"NPC portrait . (.+)", place)):
            subject = mm.group(1).replace("(Gloom)", "").strip()
            portraits[subject] = name
        elif (mm := re.match(r"content illustration . chapter (\d+), near '(.+)'", place)):
            illos.setdefault((int(mm.group(1)), mm.group(2).lower()), []).append(name)
    return openers, portraits, illos


def portrait_key(heading: str, subjects: list[str]) -> str | None:
    """Match a chapter heading against a portrait subject.

    Headings carry decoration the manifest does not ('## Wren Adeyemi (magenta)',
    '## The Last Bus (clock 6)'), so compare on the bare name.
    """
    bare = re.sub(r"\s*\(.*?\)\s*", " ", heading).strip().lower()
    for s in subjects:
        clean = re.sub(r"['\"]", "", re.sub(r"\s*\(.*?\)\s*", " ", s)).strip().lower()
        head = re.sub(r"['\"]", "", bare)
        if clean == head:
            return s
        # "Tobias 'Toby' Lark" vs "Tobias \"Toby\" Lark"
        if clean.split()[0] == head.split()[0] and clean.split()[-1] == head.split()[-1]:
            return s
    return None


def place_art(body: str, number: int, portraits: dict, illos: dict,
              used: set) -> tuple[str, int]:
    """Insert portraits and illustrations after the headings they belong to."""
    out, placed = [], 0
    subjects = list(portraits)
    for line in body.split("\n"):
        out.append(line)
        m = re.match(r"^(#{2,3})\s+(.*?)\s*$", line)
        if not m:
            continue
        heading = m.group(2)
        key = portrait_key(heading, subjects)
        if key and portraits[key] not in used:
            fn = portraits[key]
            out += ["", "![%s](../content/art/%s)" % (key, fn)]
            used.add(fn)
            placed += 1
        for fn in illos.get((number, heading.lower()), []):
            if fn in used:
                continue
            out += ["", "![%s](../content/art/%s)" % (heading, fn)]
            used.add(fn)
            placed += 1
    return "\n".join(out), placed


def write_export_variant(md_path: Path, art_dir: Path, text: str,
                         max_edge: int = 1600, quality: int = 88) -> None:
    """Emit a sibling markdown whose images are downscaled JPEGs.

    The PNG masters stay the source of truth and stay in `compiled_supplement.md`.
    But every exporter embeds its images, and 33 photographic PNGs make an 82 MB
    DOCX and an 88 MB EPUB — past what most e-readers will open. The exports are
    therefore built from this variant instead.
    """
    from PIL import Image
    out_art = md_path.parent / "art"
    out_art.mkdir(parents=True, exist_ok=True)
    swapped = text
    for png in sorted(art_dir.glob("*.png")):
        jpg = out_art / (png.stem + ".jpg")
        with Image.open(png) as im:
            im = im.convert("RGB")
            if max(im.size) > max_edge:
                im.thumbnail((max_edge, max_edge), Image.LANCZOS)
            im.save(jpg, "JPEG", quality=quality, optimize=True, progressive=True)
        swapped = swapped.replace("../content/art/%s" % png.name, "art/%s" % jpg.name)
    variant = md_path.with_suffix(".export.md")
    variant.write_text(swapped, encoding="utf-8")
    before = sum(p.stat().st_size for p in art_dir.glob("*.png"))
    after = sum(p.stat().st_size for p in out_art.glob("*.jpg"))
    print("export variant: %s | art %.1f MB -> %.1f MB"
          % (variant.name, before / 1e6, after / 1e6))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--title", required=True)
    ap.add_argument("--tagline", default="")
    ap.add_argument("--export-variant", action="store_true",
                    help="also write compiled_supplement.export.md with "
                         "downscaled JPEGs, for the DOCX/EPUB/PDF exporters")
    args = ap.parse_args()

    project = REPO_ROOT / "projects" / args.project
    art_dir = project / "content" / "art"
    state = json.loads((project / "state" / "project_state.json").read_text("utf-8"))
    config = json.loads((REPO_ROOT / "config" / "system.json").read_text("utf-8"))
    publisher = (config.get("system", {}).get("publisher_line") or "").strip()

    openers, portraits, illos = read_placements(project)
    chapters = sorted(state["chapters"], key=lambda c: c["number"])

    doc: list[str] = []
    if (art_dir / "cover.png").exists():
        doc += ["![Cover](../content/art/cover.png)", ""]
    doc += ["# %s" % args.title, ""]
    if args.tagline:
        doc += ["*%s*" % args.tagline, ""]
    doc += ["A tabletop roleplaying game.", ""]
    if publisher:
        doc += [publisher, ""]
    doc += ["---", "", "## Contents", ""]

    # Body first, so the TOC can be built from what actually landed.
    bodies, used = [], set()
    total_placed = 0
    for ch in chapters:
        src = project / "content" / ch["dir"] / "final_draft.md"
        raw = src.read_text(encoding="utf-8").rstrip()
        body, n = place_art(raw, ch["number"], portraits, illos, used)
        total_placed += n
        opener = openers.get(ch["number"])
        head = []
        if opener and (art_dir / opener).exists():
            head = ["![Chapter %d](../content/art/%s)" % (ch["number"], opener), ""]
        bodies.append("\n".join(head) + body)

    for ch in chapters:
        title = ch["title"]
        doc.append("%d. [%s](#%s)" % (ch["number"], title, slug(title)))
    doc += ["", "---", ""]
    doc.append("\n\n---\n\n".join(bodies))

    # Credits
    manifest_path = project / "development" / "art_manifest.json"
    doc += ["", "---", "", "## Credits", "",
            "**%s** — text and design." % args.title, ""]
    if manifest_path.exists():
        images = json.loads(manifest_path.read_text("utf-8")).get("images", [])
        by_source: dict[str, int] = {}
        for i in images:
            by_source[i.get("source", "unknown")] = by_source.get(i.get("source", "unknown"), 0) + 1
        doc += ["### Artwork", ""]
        for source, count in sorted(by_source.items()):
            label = {"ai_generated": ("Generated locally with Ideogram 4 via ComfyUI, "
                                      "from the structured captions in "
                                      "`development/art_prompts.md`"),
                     "algorithmic": ("Generative artwork produced in-repo by "
                                     "`development/cover_sketch/refraction.js`"),
                     }.get(source, source)
            doc += ["- %d image%s — %s." % (count, "" if count == 1 else "s", label)]
        doc += ["", "No third-party image assets are used.", ""]

    out_dir = project / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "compiled_supplement.md"
    text = "\n".join(doc).rstrip() + "\n"
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    out_path.write_text(text, encoding="utf-8")

    if args.export_variant:
        write_export_variant(out_path, art_dir, text)

    expected = set(portraits.values()) | {f for v in illos.values() for f in v}
    unplaced = sorted(expected - used)
    words = len(re.findall(r"\S+", re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)))
    print("wrote %s" % out_path)
    print("chapters: %d | art placed inline: %d | openers: %d | words: %s"
          % (len(chapters), total_placed, len(openers), format(words, ",")))
    if unplaced:
        print("NOT PLACED: %s" % ", ".join(unplaced))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
