# Stable Diffusion 1.5 Prompting Rules

Conventions for the `stable-diffusion-1.5` art generator profile (A1111/AUTOMATIC1111-style
`backend`, `prompt_style: "tags"` in `config/system.json` → `art.generators`). SD 1.5 does not
read natural-language sentences the way newer models do — it responds best to comma-separated
tag lists, weighted for emphasis, with a disciplined negative prompt doing most of the
quality-control work.

## Prompt structure

Build the prompt as a comma-separated tag list, front-loaded in this order:

1. **Subject** — who/what, in 3-8 tags (pose, key props, distinguishing features).
2. **Style** — medium and rendering approach (`black and white ink illustration`, `pen and ink
   crosshatching`, `woodcut`, `line art`). The active profile's `style_prefix` is prepended
   automatically — don't repeat it in the prompt body.
3. **Quality/technical tags** — last, and only a few (`high detail`, `clean linework`,
   `dynamic composition`). Don't stack redundant quality tags (`masterpiece, best quality,
   ultra detailed, 8k, award winning` all at once) — SD 1.5 saturates fast and extra tags
   crowd out the subject.

Tags closer to the front of the prompt carry more weight than tags near the end. If a detail
matters, say it early.

## Attention weighting

Use parenthetical weighting to nudge emphasis without lengthening the prompt:

- `(term:1.2)` increases attention on `term` by 20%.
- `(term:0.8)` decreases it by 20%.
- Nest sparingly — `((term))` (equivalent to roughly `1.21`) is acceptable, but prefer explicit
  numeric weights over stacked parentheses for anything beyond a single level.
- Reserve weighting for the one or two details that keep getting lost (a specific prop, a
  facial feature, a lighting direction) — weighting everything is equivalent to weighting
  nothing.

## Negative prompt duty

The negative prompt is not optional boilerplate — it is where SD 1.5's known failure modes get
suppressed. At minimum, cover:

- **Anatomy** — `extra fingers, fused fingers, missing limb, extra limb, malformed hands,
  distorted face, asymmetrical eyes`.
- **Text and watermarks** — `text, watermark, signature, logo, artist name, username`. SD 1.5
  cannot render legible text and will produce mangled glyph-like noise if not suppressed.
- **General quality floor** — `blurry, low quality, jpeg artifacts, oversaturated, bad
  anatomy, cropped, out of frame`.

Keep the negative prompt stable across a project's illustrations (append per-image
exceptions rather than rewriting it each time) so the art style stays consistent.

## Token budget

Keep prompts under roughly 75 tokens (SD 1.5's CLIP text encoder truncates beyond 77 tokens,
and tags past that point are silently dropped). A comma-separated tag counts each tag as
several tokens — a 15-20 tag prompt is usually the practical ceiling. If a prompt is running
long, cut quality tags before cutting subject or style tags.

## Resolution guidance

- SD 1.5 was trained at 512x512; native output in the **512-768px** range is most reliable.
  Pushing much past 768px on either dimension increases the risk of duplicated subjects or
  anatomical drift ("multiple heads" artifacts).
- Both width and height **must be divisible by 8** (SD 1.5's latent downsampling factor).
  Non-multiples of 8 get silently rounded by most backends, which can shift framing.
- Match aspect ratio to the layout slot rather than always generating square: portrait
  illustrations, wide landscape banners, and tall column art each want a different width/height
  pair. See the `sizes` map in the active generator profile for this project's slot dimensions.

## Worked example

**Subject:** a generic "cloaked figure on a rain-slick street" illustration for an urban
fantasy chapter opener.

**Prompt:**

```
cloaked figure standing in a narrow alley, hood raised, hands in pockets, looking down the street,
black and white ink illustration, crosshatching, rain-slick cobblestone reflecting streetlight,
(dramatic lighting:1.2), high contrast, clean linework, dynamic composition
```

**Negative prompt:**

```
text, watermark, signature, logo, blurry, low quality, jpeg artifacts, extra fingers, fused fingers,
malformed hands, distorted face, asymmetrical eyes, extra limbs, cropped, out of frame, color, oversaturated
```

(`color` is added to the negative prompt here because the house style is black-and-white ink —
add it whenever the target style is monochrome.)
