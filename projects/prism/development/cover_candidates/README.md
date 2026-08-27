# Cover candidates

Two covers exist. `content/art/cover.png` is currently the algorithmic one.

## algorithmic_refraction.png — in use
1600x2400. Generative p5.js sketch, seed 20260826, source in
`../cover_sketch/refraction.js` and philosophy in
`../concepts/cover_philosophy.md`. One achromatic beam meets a perturbed
boundary and separates; outgoing angles come from Snell's law over a Cauchy
dispersion model, colour is computed from wavelength rather than sampled, and
five weighted spines correspond to the five Stars.

## ideogram_default.png / ideogram_turbo.png — candidate
1024x1536. Ideogram 4, rendered locally, from the `cover.png` caption in
`../art_prompts.md`: the Nightline on a suburban street at night, chrome PRISM
lettering, dolphin over the rooftops, bus shelter in nine colours.

Only the Turbo (12-step) render exists. It came from the first sample batch;
everything else in the book was finalised at Default (20 steps). Re-render for
a fair comparison with ComfyUI running:

    python tools/generate_ideogram.py prism --only cover.png --preset Default \
        --out-dir projects/prism/development/cover_candidates

## To adopt the Ideogram cover

    cp projects/prism/development/cover_candidates/ideogram_default.png \
       projects/prism/content/art/cover.png

Then change that image's `source` in `development/art_manifest.json` from
`algorithmic` to `ai_generated`, and re-run `/compile` so every export picks up
the new cover.
