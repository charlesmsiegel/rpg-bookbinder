"""
Shared utilities for cover generation.
All individual cover generators import from here.
"""

import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

WIDTH = 1600
HEIGHT = 2400
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Cross-platform font candidates, tried in order. The last resort is
# PIL's built-in bitmap font (ImageFont.load_default), which has no
# external dependency and always works.
FONT_TITLE_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/timesbd.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
]
FONT_SUB_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def _load_font(candidates, size):
    """Try each candidate TTF path in order; fall back to PIL's built-in
    bitmap font if none are available so the CLI always works."""
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except (IOError, OSError):
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        # Older Pillow: load_default() doesn't accept a size argument.
        return ImageFont.load_default()


# ═══════════════════════════════════════════════════════════════════════════════
# NOISE GENERATION
# ═══════════════════════════════════════════════════════════════════════════════

def smooth_noise(w, h, scale, rng, octaves=4):
    """Generate smooth 2D noise field normalized to [0, 1]."""
    result = np.zeros((h, w), dtype=np.float64)
    for i in range(octaves):
        amp = 0.5 ** i
        freq = max(3, int(scale / (2 ** i)))
        sw = max(4, w // freq)
        sh = max(4, h // freq)
        small = rng.random((sh, sw))
        small_img = Image.fromarray((small * 255).astype(np.uint8))
        big_img = small_img.resize((w, h), Image.BICUBIC)
        result += np.array(big_img, dtype=np.float64) / 255.0 * amp
    mn, mx = result.min(), result.max()
    if mx > mn:
        result = (result - mn) / (mx - mn)
    return result


def angle_noise(w, h, scale, rng, octaves=3):
    """Generate a noise field of angles in [0, 2*pi]."""
    n = smooth_noise(w, h, scale, rng, octaves)
    return n * 2 * math.pi


# ═══════════════════════════════════════════════════════════════════════════════
# BACKGROUND
# ═══════════════════════════════════════════════════════════════════════════════

def draw_background(bg_top, bg_bottom, rng, noise_intensity=20):
    """Create gradient background with noise texture. Returns RGB Image."""
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float64)
    noise = smooth_noise(WIDTH, HEIGHT, 60, rng, octaves=5)
    for c in range(3):
        gradient = np.linspace(bg_top[c], bg_bottom[c], HEIGHT).reshape(-1, 1)
        gradient = np.broadcast_to(gradient, (HEIGHT, WIDTH)).copy()
        pixels[:, :, c] = gradient + (noise - 0.5) * noise_intensity
    pixels = np.clip(pixels, 0, 255).astype(np.uint8)
    return Image.fromarray(pixels)


# ═══════════════════════════════════════════════════════════════════════════════
# COMPOSITING & EFFECTS
# ═══════════════════════════════════════════════════════════════════════════════

def new_layer():
    """Create a fresh transparent RGBA layer at full cover size."""
    return Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))


def composite(base_rgb, *rgba_layers):
    """Composite multiple RGBA layers onto an RGB base. Returns RGB."""
    result = base_rgb.convert('RGBA')
    for layer in rgba_layers:
        result = Image.alpha_composite(result, layer)
    return result.convert('RGB')


def apply_vignette(img, strength=0.65, center_y_ratio=0.5):
    """Darken edges with radial vignette. center_y_ratio shifts the bright center."""
    y, x = np.ogrid[:HEIGHT, :WIDTH]
    cx = WIDTH / 2.0
    cy = HEIGHT * center_y_ratio
    # Elliptical distance normalized
    dist = np.sqrt((x - cx) ** 2 / (cx ** 2) + (y - cy) ** 2 / ((HEIGHT * 0.6) ** 2))
    vig = 1.0 - np.clip((dist - 0.35) * strength, 0, 1) ** 1.4
    mask = (vig * 255).astype(np.uint8)
    mask_img = Image.fromarray(mask)
    r, g, b = img.split()
    return Image.merge('RGB', (
        ImageChops.multiply(r, mask_img),
        ImageChops.multiply(g, mask_img),
        ImageChops.multiply(b, mask_img),
    ))


def add_bloom(layer, radius=25, intensity=1.5):
    """Add a glow/bloom effect to bright areas of an RGBA layer. Returns new RGBA layer."""
    blurred = layer.filter(ImageFilter.GaussianBlur(radius=radius))
    # Brighten the blur
    arr = np.array(blurred, dtype=np.float64)
    arr[:, :, 3] = np.clip(arr[:, :, 3] * intensity, 0, 255)
    bloom = Image.fromarray(arr.astype(np.uint8))
    # Composite bloom under original
    result = Image.alpha_composite(bloom, layer)
    return result


def scatter_particles(layer, rng, color, count=300, min_size=1, max_size=4,
                      min_alpha=30, max_alpha=150, region=None):
    """Scatter bright particles across a layer. region=(x0,y0,x1,y1) or None for full."""
    draw = ImageDraw.Draw(layer, 'RGBA')
    x0, y0, x1, y1 = region if region else (0, 0, WIDTH, HEIGHT)
    for _ in range(count):
        x = rng.uniform(x0, x1)
        y = rng.uniform(y0, y1)
        s = rng.integers(min_size, max_size + 1)
        a = int(rng.uniform(min_alpha, max_alpha))
        draw.ellipse([x - s, y - s, x + s, y + s], fill=(*color, a))


# ═══════════════════════════════════════════════════════════════════════════════
# TEXT RENDERING
# ═══════════════════════════════════════════════════════════════════════════════

def find_title_font_size(title, max_width):
    """Find largest font size where the longest line fits within max_width."""
    lines = title.split('\n')
    longest = max(lines, key=len)
    for size in range(150, 28, -4):
        font = _load_font(FONT_TITLE_CANDIDATES, size)
        bbox = font.getbbox(longest)
        if (bbox[2] - bbox[0]) <= max_width:
            return size
    return 32


def render_cover_text(img, title, subtitle, text_color, accent_color, footer_text: str = ""):
    """Render title with glow, decorative line, subtitle, and an optional
    footer line. Returns RGB image with all text composited.

    footer_text: text to draw at the bottom of the cover; if empty (the
    default), no footer is drawn.
    """
    max_w = int(WIDTH * 0.82)
    tsize = find_title_font_size(title, max_w)
    tfont = _load_font(FONT_TITLE_CANDIDATES, tsize)

    lines = title.split('\n')
    line_h, line_w = [], []
    for ln in lines:
        bb = tfont.getbbox(ln)
        line_h.append(bb[3] - bb[1])
        line_w.append(bb[2] - bb[0])

    spacing = int(tsize * 0.22)
    title_top = int(HEIGHT * 0.09)

    # Glow layer
    glow = new_layer()
    gd = ImageDraw.Draw(glow, 'RGBA')
    y = title_top
    for i, ln in enumerate(lines):
        x = (WIDTH - line_w[i]) // 2
        gd.text((x, y), ln, fill=(*text_color, 220), font=tfont)
        y += line_h[i] + spacing
    glow = glow.filter(ImageFilter.GaussianBlur(radius=22))

    # Crisp text layer
    text_layer = new_layer()
    td = ImageDraw.Draw(text_layer, 'RGBA')
    y = title_top
    for i, ln in enumerate(lines):
        x = (WIDTH - line_w[i]) // 2
        td.text((x + 3, y + 3), ln, fill=(0, 0, 0, 160), font=tfont)
        td.text((x, y), ln, fill=(*text_color, 255), font=tfont)
        y += line_h[i] + spacing

    # Decorative line
    ly = y + int(tsize * 0.25)
    hw = int(WIDTH * 0.22)
    td.line([WIDTH // 2 - hw, ly, WIDTH // 2 + hw, ly], fill=(*accent_color, 140), width=2)
    d = 6
    td.polygon([
        (WIDTH // 2, ly - d), (WIDTH // 2 + d, ly),
        (WIDTH // 2, ly + d), (WIDTH // 2 - d, ly)
    ], fill=(*accent_color, 180))

    # Subtitle
    sub_size = max(24, min(38, tsize // 3))
    sfont = _load_font(FONT_SUB_CANDIDATES, sub_size)
    sy = ly + int(tsize * 0.35)
    dim = tuple(max(0, c - 25) for c in text_color)
    for sl in subtitle.split('\n'):
        bb = sfont.getbbox(sl)
        sw = bb[2] - bb[0]
        sh = bb[3] - bb[1]
        sx = (WIDTH - sw) // 2
        td.text((sx + 1, sy + 1), sl, fill=(0, 0, 0, 100), font=sfont)
        td.text((sx, sy), sl, fill=(*dim, 230), font=sfont)
        sy += sh + int(sub_size * 0.4)

    # Footer (optional)
    if footer_text:
        ffont = _load_font(FONT_SUB_CANDIDATES, 22)
        fb = ffont.getbbox(footer_text)
        fx = (WIDTH - (fb[2] - fb[0])) // 2
        fdim = tuple(max(0, c - 50) for c in text_color)
        td.text((fx, HEIGHT - 100), footer_text, fill=(*fdim, 160), font=ffont)

    # Composite: base + glow + text
    result = img.convert('RGBA')
    result = Image.alpha_composite(result, glow)
    result = Image.alpha_composite(result, text_layer)
    return result.convert('RGB')


# ═══════════════════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════════════════

def save_cover(img, project_dir):
    """Save cover.png into the project's content/art/ directory."""
    art_dir = os.path.join(BASE_DIR, "projects", project_dir, "content", "art")
    os.makedirs(art_dir, exist_ok=True)
    path = os.path.join(art_dir, "cover.png")
    img.save(path, "PNG", optimize=True)
    size_kb = os.path.getsize(path) / 1024
    print(f"    Saved: {path} ({size_kb:.0f} KB)")
    return path
