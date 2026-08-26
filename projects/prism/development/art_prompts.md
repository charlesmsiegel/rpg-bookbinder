# PRISM — Art Prompt Manifest

**Mode**: Prompt Manifest (deferred). No images generated.

**Why**: the active generator profile is `ideogram-v4`, whose backend is
`comfyui`. `/art-direction` selects its mode by probing `mcp__art__get_models`,
and that tool requires an `a1111` backend — it returns
*"This tool requires an a1111-backend generator profile"* for any other. A
comfyui profile therefore always falls back to Prompt Manifest Mode without
contacting a server. That is the correct outcome here: no image models are
available in this environment.

**Cover exception**: `content/art/cover.png` **already exists**. It was produced
algorithmically (a p5.js sketch, `development/cover_sketch/refraction.js`),
because `/art-direction` requires a real cover in every compiled output and
allows that one image to cross modes. It is a standalone piece, *not* a render
of the `cover.png` prompt below — that prompt is still reserved. If the Ideogram
run produces something better, overwrite `cover.png` and change the manifest
entry's `source` from `algorithmic` to `ai_generated`.

**Total prompts**: 33
(1 cover + 10 chapter openers + 11 NPC portraits + 11 content illustrations)

**Density**: 1 content illustration per 2000
words across 20,865 words of final draft.

## Before generating

1. `styles/art/example.workflow.json` is a **template, not a workflow** — its own
   `_readme` says so, and it has no model loader, decoder, or output node. Export
   a real workflow from ComfyUI via *Save (API Format)* and point
   `art.generators["ideogram-v4"].workflow_file` at it.
2. These prompts are **Ideogram-shaped natural language**, per the profile's
   `prompt_style: "natural"`. They are not portable to another generator
   unchanged. Switching backends means re-running `/art-direction` under the new
   profile — the placement plan and reserved paths survive, the wording does not.
3. **Three prompts require legible lettering** (`cover.png`,
   `chapter_10_opener.png`, `ch_10_timetable.png`) and deliberately omit `text`
   from their negative prompts. Do not add it back; Ideogram was chosen partly
   for its lettering.

## Style consistency

Every positive prompt below opens with the profile's `style_prefix`:

> `hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, `

Tone keywords: sugarpop, sincere, rainbow, loud, kind, unembarrassed.

---

## cover.png

- **Placement**: cover
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a five-person team standing in a line on an ordinary suburban street at night, seen from below, each figure blazing a different colour — magenta, cyan, sunburst yellow, violet, mint green — their coats and skates and clockwork armour trailing light; behind them the street has split into spectrum, a bus shelter rendered in nine colours with chrome bevelled edges, gradient sky, glitter falling like warm snow, an impossible dolphin arcing over the rooftops; the title PRISM in heavy geometric sans across the upper third
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos
- **Notes**: The signature image. Ordinary street furniture must remain recognisable behind the spectrum treatment — the contrast is the whole point. Title lettering required.

## chapter_01_opener.png

- **Placement**: chapter 1 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a bus shelter at night, half in ordinary streetlight and half exploded into airbrushed rainbow, the split running vertically down the middle of the frame
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Establishes the two layers in one image. The everyday half must look genuinely ordinary, not drab.

## chapter_02_opener.png

- **Placement**: chapter 2 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, two enormous six-sided dice tumbling through a gradient void, chrome-edged, throwing off spectrum light, with three more dice ghosting in behind them
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The three ghost dice are the backing dice. Keep it readable as a rules-chapter opener.

## chapter_03_opener.png

- **Placement**: chapter 3 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, an empty magenta coat, an empty pair of cyan skates, and an empty clockwork sleeve arranged on a bedroom floor as though waiting, warm lamplight, glitter in the carpet
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Character creation. Absence of people is deliberate: these are roles not yet filled.

## chapter_04_opener.png

- **Placement**: chapter 4 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a single figure mid-refraction, caught at the instant of splitting into spectrum, their ordinary silhouette still visible inside the colour, one hand raised, light going outward in bands
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The transformation chapter's hero image. Genderless silhouette.

## chapter_05_opener.png

- **Placement**: chapter 5 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a chrome clock face with six segments, three of them cracked and leaking colour, floating above a wet pavement that reflects it
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The Gloom clock made literal. Should feel like pressure, not menace.

## chapter_06_opener.png

- **Placement**: chapter 6 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, five colour-coded silhouettes in a loose row against a white background, magenta cyan yellow violet mint, each in a distinct stance
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pregen roster page. Flat, poster-like, almost a colour swatch.

## chapter_07_opener.png

- **Placement**: chapter 7 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, an ordinary residential street rendered twice in the same frame, once in plain daylight and once in full airbrushed spectrum, the two versions interleaved in vertical bands
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The setting chapter. Same geometry both times — that is the point.

## chapter_08_opener.png

- **Placement**: chapter 8 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a Showrunner's-eye view across a kitchen table: dice, a hand-drawn clock on paper, five character sheets, mugs, and spectrum light leaking in from off-frame
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The GM chapter, from behind the screen. Warm and domestic.

## chapter_09_opener.png

- **Placement**: chapter 9 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a bus the length of a street, three storeys of chrome and rust, headlights like two dead suns, always pulling away, seen from the pavement in spectrum colour
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The antagonist chapter. It must read as leaving, never as charging.

## chapter_10_opener.png

- **Placement**: chapter 10 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a night bus timetable on a chrome post, nine colours, with one printed strip at the bottom glowing brighter than the rest
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos
- **Notes**: Starter adventure opener. Lettering on the timetable is required and should be legible.

## portrait_wren_adeyemi.png

- **Placement**: NPC portrait — Wren Adeyemi
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, portrait of Wren Adeyemi, magenta and chrome, a coat trailing behind her like a comet throwing off sparks that do not go out when they land, hands deliberately empty, moving fast and looking back over her shoulder
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

## portrait_tobias_lark.png

- **Placement**: NPC portrait — Tobias 'Toby' Lark
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, portrait of Tobias 'Toby' Lark, cyan and holographic oil-slick shimmer, skates leaving a gradient hanging in the air behind him, a battered skateboard covered in someone else's stickers, mid-motion and grinning
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

## portrait_priya_raghunathan.png

- **Placement**: NPC portrait — Priya Raghunathan
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, portrait of Priya Raghunathan, sunburst yellow and brass, a coat made of working clockwork with gears visibly turning at the shoulders and hem, holding a wrench far too small for anything, head tilted, examining something off-frame
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

## portrait_marisol_vega.png

- **Placement**: NPC portrait — Marisol Vega
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, portrait of Marisol Vega, violet and starfield, not printed stars but actual depth as though something enormous were showing through, completely still, a set of door keys the only thing about her that would make a sound
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

## portrait_danny_okonkwo_byrne.png

- **Placement**: NPC portrait — Danny Okonkwo-Byrne
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, portrait of Danny Okonkwo-Byrne, mint green and pearl, a soft glow with no obvious source that makes the air around him feel like a small room, hands in pockets, sitting while everyone else stands
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

## portrait_the_last_bus.png

- **Placement**: NPC portrait — The Last Bus (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a bus the length of a street, three storeys of chrome and rust, every window lit warm and full of people not looking out, doors always closing, forever pulling away
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

## portrait_the_quiet_shelf.png

- **Placement**: NPC portrait — The Quiet Shelf (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, library shelves growing taller and further apart until the aisles are canyons and the ceiling is a rumour, warm and silent, a returns slot high in one wall just out of reach
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

## portrait_the_silt.png

- **Placement**: NPC portrait — The Silt (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a chrome tide, mirror-bright and thickening, moving at the speed of a minute hand, swallowing landmarks and reflecting them back slightly wrong
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

## portrait_the_long_weekend.png

- **Placement**: NPC portrait — The Long Weekend (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a very comfortable room that keeps adding doors, all of which lead back into it, deep chairs, good light, a blanket exactly warm enough
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

## portrait_the_grey_ledger.png

- **Placement**: NPC portrait — The Grey Ledger (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, an enormous filing structure of shelves and drawers and pneumatic tubes going up past where the sky should be, everything it processes coming out accurate and completely drained
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

## portrait_the_understudy.png

- **Placement**: NPC portrait — The Understudy (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a figure that is almost exactly one of the Stars — same silhouette, same colour, slightly better — standing patiently and offering to help
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

## ch_02_backing.png

- **Placement**: content illustration — chapter 2, near 'Power of Friendship'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a hand reaching into frame to steady another hand that is holding dice, both figures colour-coded and half-transformed, spectrum light between them
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The core mechanic as an image.

## ch_03_radiance.png

- **Placement**: content illustration — chapter 3, near 'Radiance'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a single figure seen from behind, ordinary clothes, with the spectrum version of themselves standing in front of them like a reflection that has turned around
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Look versus Radiance in one frame.

## ch_04_synchronized.png

- **Placement**: content illustration — chapter 4, near 'Synchronized Morph'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, five figures shouting the same word at the same instant, colour erupting from all of them simultaneously, shot from ground level
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The sentai register. Should feel loud.

## ch_04_combined.png

- **Placement**: content illustration — chapter 4, near 'Combined Form'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, one enormous fused figure made visibly of five colours braided together, too big for the street it is standing in, chrome and gradient
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Rare and huge. Should not fit in the frame comfortably.

## ch_05_dimmed.png

- **Placement**: content illustration — chapter 5, near 'Getting Dimmed'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a single completely grey figure standing in the middle of a hyper-saturated spectrum street, all colour drained out of them, everything around them still blazing
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: The most emotionally important image in the book. Grey figure, saturated world.

## ch_05_reaching.png

- **Placement**: content illustration — chapter 5, near 'Reaching someone'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, one colour-blazing figure kneeling to take the hand of a grey Dimmed figure, colour just beginning to bleed back into the grey one at the point of contact
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pairs with ch_05_dimmed. This is the game's thesis as a picture.

## ch_07_spectrum_street.png

- **Placement**: content illustration — chapter 7, near 'The Spectrum'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a launderette on a corner rendered in nine colours with chrome bevelled lettering, glitter banked in the gutters like warm snow, a snow leopard asleep on the roof
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Establishing shot for the setting. The leopard does not react to anything.

## ch_07_dolphins.png

- **Placement**: content illustration — chapter 7, near 'The Spectrum'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, dolphins moving through the air above a ring road as though it were a reef, gradient sky, traffic below entirely unbothered
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Pure Lisa Frank. Should be joyful, not surreal-menacing.

## ch_08_table.png

- **Placement**: content illustration — chapter 8, near 'Pacing a first session'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, an overhead view of a kitchen table mid-session: dice, a hand-drawn six-segment clock with three crossed off, five sheets, one empty chair
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Practical GM-chapter image. The empty chair is deliberate.

## ch_09_gloom_scale.png

- **Placement**: content illustration — chapter 9, near 'How to read a Gloom'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, three Glooms of different sizes shown in silhouette against a gradient — a small one, a street-sized one, and one going up past the top of the frame
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos, text
- **Notes**: Clock sizes 4, 6 and 8 made visual.

## ch_10_timetable.png

- **Placement**: content illustration — chapter 10, near 'The last thirty seconds'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4
- **Positive prompt**: hyper-saturated airbrushed rainbow illustration, Lisa Frank palette, glossy chrome and neon, a close view of a bus timetable in ordinary daylight, one printed strip at the bottom reading 'Fridays, late service, 00:15', a single piece of glitter caught in the frame
- **Negative prompt**: muted colors, desaturated, grimdark, photorealistic, watermark, low quality, blurry, signature, deformed hands, extra limbs, modern logos
- **Notes**: The payoff image. Back in the everyday. Lettering required and must be legible.

