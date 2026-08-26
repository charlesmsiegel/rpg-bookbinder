# Cover sketch — "Refraction"

Generative p5.js sketch that produced `projects/prism/content/art/cover.png`.
The philosophy behind it is `../concepts/cover_philosophy.md`.

## What it does

One achromatic beam descends a column, meets a noise-perturbed boundary, and
separates. Outgoing angles come from Snell's law against a Cauchy dispersion
model, `n(lambda) = A + B / lambda^2`; the angular disagreement between
wavelengths is real but tiny (about 0.009 rad across the visible band), so
`dispersionGain` scales it to canvas scale while preserving the ordering and
the non-linear spacing that is dispersion's actual signature. Colour is never
sampled from a palette — each ray carries a wavelength in nanometres and its
RGB comes from that wavelength alone. Brightness is the density of accumulated
sub-rays in a `Float32Array` light buffer, tone-mapped at the end.

Five wavelengths (404, 492, 516, 578, 660 nm — nearest the five Stars' colours)
carry a small weight boost, so the fan has five faint spines in it. They are
the only hand-placed numbers in the algorithm.

## Reproducing it

```sh
pip install playwright
curl -o p5.min.js https://cdn.jsdelivr.net/npm/p5@1.11.3/lib/p5.min.js
python3 render.py ../../content/art/cover.png
```

`render.py` drives headless Chromium at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`;
point `executable_path` at whatever Chromium you have. `p5.min.js` is not
checked in — fetch it next to `index.html` before rendering. Output is
1600 × 2400. Seed is `20260826`; a different seed re-rolls the noise field and
the dust and gives a different but equally valid member of the movement.

## Status

This is a **placeholder that stands on its own**, not a stand-in. It is not the
image described in `../art_prompts.md § cover.png` — that prompt is a figurative
Lisa Frank scene of the Nightline on a street, and is still reserved for a run
on Ideogram v4. If that render lands and is better, overwrite `cover.png` and
change the manifest entry's `source` from `algorithmic` to `ai_generated`.
