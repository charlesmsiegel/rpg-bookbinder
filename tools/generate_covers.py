#!/usr/bin/env python3
"""
Generic algorithmic book cover generator.

Produces a single PNG cover image from a title, an optional subtitle, and a
color palette, using one of a handful of generative-art "motifs" built on
top of the shared PIL/numpy primitives in scripts/covers/utils.py
(gradient backgrounds, noise fields, layer compositing, particle scatter,
bloom, vignette, and title-text rendering).

Usage:
    python tools/generate_covers.py --title "Book Title" \\
        [--subtitle "A Subtitle"] \\
        [--palette "#263238,#B0A16B"] \\
        [--motif geometric|organic|minimal] \\
        [--footer "Published by Example Press"] \\
        [--seed 12345] \\
        --out path/to/cover.png

If --footer is omitted, the default footer text is read from
config/system.json's system.publisher_line. If that's missing or empty,
no footer is drawn.
"""

import argparse
import json
import math
import os
import sys

from PIL import ImageDraw

# Make the shared cover-generation primitives (scripts/covers/utils.py)
# importable regardless of the caller's working directory.
_SCRIPTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"
)
sys.path.insert(0, _SCRIPTS_DIR)

from covers.utils import (  # noqa: E402
    WIDTH, HEIGHT,
    smooth_noise, angle_noise, draw_background,
    new_layer, composite, apply_vignette, add_bloom, scatter_particles,
    render_cover_text,
)


# =============================================================================
# PALETTE
# =============================================================================

def _hex_to_rgb(value):
    """Convert '#rrggbb' or '#rgb' (with or without leading '#') to an RGB tuple."""
    h = value.strip().lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    if len(h) != 6:
        raise argparse.ArgumentTypeError(f"invalid hex color: {value!r}")
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid hex color: {value!r}")


def _clamp(v):
    return max(0, min(255, int(v)))


def _lighten(rgb, amount):
    return tuple(_clamp(c + (255 - c) * amount) for c in rgb)


def _darken(rgb, amount):
    return tuple(_clamp(c * (1 - amount)) for c in rgb)


def _luminance(rgb):
    return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]


DEFAULT_PALETTE = "#20242c,#c9a25a"


def build_palette(hex_csv):
    """Turn a comma-separated hex color list into the role colors the
    composition functions and render_cover_text need: bg_top, bg_bottom,
    primary, secondary, accent, text_color.

    - 1 color: everything derived from it.
    - 2 colors: first is the background base, second is the accent.
    - 3+ colors: background base, primary, accent (extras ignored).
    """
    colors = [_hex_to_rgb(c) for c in hex_csv.split(',') if c.strip()]
    if not colors:
        raise argparse.ArgumentTypeError("--palette must contain at least one color")

    base = colors[0]
    dark = _luminance(base) < 128

    accent = colors[1] if len(colors) > 1 else (_lighten(base, 0.6) if dark else _darken(base, 0.6))
    primary = colors[2] if len(colors) > 2 else (_lighten(base, 0.3) if dark else _darken(base, 0.3))
    secondary = _darken(accent, 0.3) if dark else _lighten(accent, 0.3)

    bg_top = base
    bg_bottom = _darken(base, 0.35) if dark else _lighten(base, 0.2)
    text_color = (245, 241, 232) if dark else (26, 22, 18)

    return {
        "bg_top": bg_top,
        "bg_bottom": bg_bottom,
        "primary": primary,
        "secondary": secondary,
        "accent": accent,
        "text_color": text_color,
    }


# =============================================================================
# MOTIFS — small composition functions over covers/utils.py primitives
# =============================================================================

def motif_geometric(rng, palette):
    """Angular gradient background with faceted triangles and sparse particles."""
    bg = draw_background(palette["bg_top"], palette["bg_bottom"], rng, noise_intensity=22)

    facets = new_layer()
    draw = ImageDraw.Draw(facets, "RGBA")
    angles = angle_noise(WIDTH, HEIGHT, 55, rng, octaves=3)
    cell = 170
    for gy in range(0, HEIGHT, cell):
        for gx in range(0, WIDTH, cell):
            a = angles[min(gy, HEIGHT - 1), min(gx, WIDTH - 1)]
            cx, cy = gx + cell / 2, gy + cell / 2
            r = cell * 0.72
            pts = [
                (cx + r * math.cos(a + k * (2 * math.pi / 3)),
                 cy + r * math.sin(a + k * (2 * math.pi / 3)))
                for k in range(3)
            ]
            t = (math.sin(a) + 1) / 2
            color = tuple(
                int(palette["primary"][c] * (1 - t) + palette["secondary"][c] * t)
                for c in range(3)
            )
            alpha = int(50 + 55 * t)
            draw.polygon(pts, fill=(*color, alpha), outline=(*palette["accent"], alpha + 40))

    particles = new_layer()
    scatter_particles(particles, rng, palette["accent"], count=140,
                       min_size=1, max_size=3, min_alpha=40, max_alpha=140)

    img = composite(bg, facets, particles)
    img = apply_vignette(img, strength=0.7, center_y_ratio=0.5)
    return img


def motif_organic(rng, palette):
    """Soft gradient background with blurred color blobs and bloom glow."""
    bg = draw_background(palette["bg_top"], palette["bg_bottom"], rng, noise_intensity=10)

    blobs = new_layer()
    draw = ImageDraw.Draw(blobs, "RGBA")
    field = smooth_noise(WIDTH, HEIGHT, 220, rng, octaves=4)
    for _ in range(9):
        bx = rng.uniform(WIDTH * 0.15, WIDTH * 0.85)
        by = rng.uniform(HEIGHT * 0.2, HEIGHT * 0.85)
        br = rng.uniform(180, 420)
        fx = min(max(int(bx), 0), WIDTH - 1)
        fy = min(max(int(by), 0), HEIGHT - 1)
        t = field[fy, fx]
        color = tuple(
            int(palette["primary"][c] * (1 - t) + palette["accent"][c] * t)
            for c in range(3)
        )
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(*color, 65))

    bloomed = add_bloom(blobs, radius=32, intensity=1.6)

    particles = new_layer()
    scatter_particles(particles, rng, palette["accent"], count=200,
                       min_size=1, max_size=3, min_alpha=25, max_alpha=100)

    img = composite(bg, bloomed, particles)
    img = apply_vignette(img, strength=0.55, center_y_ratio=0.5)
    return img


def motif_minimal(rng, palette):
    """Flat background with a vignette — no particles or geometry, text only."""
    bg = draw_background(palette["bg_top"], palette["bg_bottom"], rng, noise_intensity=6)
    img = apply_vignette(bg, strength=0.45, center_y_ratio=0.5)
    return img


MOTIFS = {
    "geometric": motif_geometric,
    "organic": motif_organic,
    "minimal": motif_minimal,
}


# =============================================================================
# CLI
# =============================================================================

_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)


def _derive_seed(title):
    """Deterministic default seed so the same title reproduces the same cover."""
    import zlib
    return zlib.crc32(title.encode("utf-8"))


def _default_footer():
    """Read the default footer from config/system.json's
    system.publisher_line. Missing file, missing key, or an empty value
    all mean "no footer"."""
    config_path = os.path.join(_REPO_ROOT, "config", "system.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError):
        return ""
    return config.get("system", {}).get("publisher_line", "") or ""


def generate_cover(title, subtitle, palette_hex, motif, seed, out_path, footer=None):
    import numpy as np

    palette = build_palette(palette_hex)
    rng_seed = seed if seed is not None else _derive_seed(title)
    rng = np.random.default_rng(rng_seed)
    footer_text = footer if footer is not None else _default_footer()

    motif_fn = MOTIFS[motif]
    img = motif_fn(rng, palette)
    img = render_cover_text(img, title, subtitle, palette["text_color"], palette["accent"],
                             footer_text=footer_text)

    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    parser = argparse.ArgumentParser(description="Generate a generative-art book cover.")
    parser.add_argument("--title", required=True, help="Cover title text.")
    parser.add_argument("--subtitle", default="", help="Optional subtitle text.")
    parser.add_argument("--palette", default=DEFAULT_PALETTE,
                         help="Comma-separated hex colors, e.g. '#263238,#B0A16B'.")
    parser.add_argument("--motif", choices=sorted(MOTIFS), default="minimal",
                         help="Visual motif to use.")
    parser.add_argument("--footer", default=None,
                         help="Footer line (default: config/system.json's "
                              "system.publisher_line; empty means no footer).")
    parser.add_argument("--seed", type=int, default=None,
                         help="Random seed (default: derived from --title).")
    parser.add_argument("--out", required=True, help="Output PNG path.")
    args = parser.parse_args()

    path = generate_cover(args.title, args.subtitle, args.palette, args.motif,
                           args.seed, args.out, footer=args.footer)
    size_kb = os.path.getsize(path) / 1024
    print(f"Saved: {path} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
