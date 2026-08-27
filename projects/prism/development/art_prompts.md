# PRISM — Art Prompt Manifest

**Mode**: structured captions for local Ideogram 4.

**Why**: `config/system.json` points at a `comfyui` backend, and
`/art-direction` probes with `get_models`, which is a1111-only, so the
command can never reach Generation Mode under this profile. Rendering is
therefore done by `tools/generate_ideogram.py`, which reads this file and
drives a local ComfyUI running the `ideogram4_fp8_scaled` weights. No API
key and no per-image cost.

**Prompt format**: Ideogram 4 is trained on **structured JSON captions**
and validates against that schema. A prose prompt for the same subject
comes back as the model's own *"Image blocked by safety filter"* grey
card; the identical content expressed as JSON renders correctly. Every
caption below is therefore JSON. Neither the local model nor the hosted
`IdeogramV4` node takes a negative prompt: guidance is asymmetric CFG,
where the unconditional pass drops text tokens.


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
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The signature image. Ordinary street furniture must remain recognisable behind the spectrum treatment — the contrast is the whole point. Title lettering required.

```json
{
  "high_level_description": "The cover of a tabletop roleplaying game. Five figures stand in a line across an ordinary suburban street at night, seen from below so they tower. Each blazes a different colour, magenta, cyan, sunburst yellow, violet and mint green, their coats and skates and clockwork armour trailing light. Behind them the street has split into spectrum. The title PRISM runs in heavy geometric sans across the upper third.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A quiet residential street at night that has come apart into colour: gradient sky from magenta into deep violet, glitter falling like warm snow, an impossible dolphin arcing over the rooftops. Ordinary street furniture stays recognisable underneath the spectrum treatment.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          90,
          300,
          934,
          560
        ],
        "desc": "The word PRISM in heavy geometric sans, chrome bevelled, spanning the upper third of the frame.",
        "color_palette": [
          "#FFFFFF",
          "#FF2D95",
          "#00C8F0"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          80,
          620,
          944,
          1400
        ],
        "desc": "Five full-length figures in a rank across the street, seen from a low angle, each lit in one of the five colours, each in a distinct stance.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          120,
          900,
          500,
          1300
        ],
        "desc": "A bus shelter rendered in nine colours with chrome bevelled edges, still clearly a bus shelter.",
        "color_palette": [
          "#00C8F0",
          "#FF2D95",
          "#FFD400"
        ]
      }
    ]
  }
}
```

## chapter_01_opener.png

- **Placement**: chapter 1 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Establishes the two layers in one image. The everyday half must look genuinely ordinary, not drab.

```json
{
  "high_level_description": "A suburban bus shelter at night split straight down the vertical centre of the frame. The left half sits in ordinary sodium streetlight, drab and real. The right half has exploded into hyper-saturated airbrushed rainbow, the same shelter in nine glossy chrome-edged colours. The seam is a clean vertical line of prismatic light.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A quiet residential street at night receding to a vanishing point: muted grey-orange under streetlight on the left, a gradient sky of magenta into violet with falling glitter on the right.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          80,
          500,
          512,
          1180
        ],
        "desc": "The left half of a glass-and-steel bus shelter, entirely ordinary: scratched perspex, grey metal frame, unlit timetable panel, worn bench. Realistic and unglamorous, but not dingy.",
        "color_palette": [
          "#6B6459",
          "#9AA0A6",
          "#3A3A3A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          512,
          500,
          944,
          1180
        ],
        "desc": "The right half of the same shelter, refracted: identical geometry in saturated colour with chrome bevelled edges, the perspex iridescent, the bench glowing.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#7CE7C4"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          496,
          120,
          528,
          1400
        ],
        "desc": "A clean vertical seam of white prismatic light the full height of the frame, throwing a narrow spectrum fringe either side.",
        "color_palette": [
          "#FFFFFF",
          "#FF2D95",
          "#00C8F0"
        ]
      }
    ]
  }
}
```

## chapter_02_opener.png

- **Placement**: chapter 2 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The three ghost dice are the backing dice. Keep it readable as a rules-chapter opener.

```json
{
  "high_level_description": "Two enormous six-sided dice tumble through a gradient void, chrome-edged and throwing off spectrum light, with three fainter dice ghosting in behind them. A rules-chapter opener: bold, readable, uncluttered.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A deep gradient void from magenta through violet, lit from within, with soft prismatic flares and drifting glitter.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          380,
          700,
          900
        ],
        "desc": "Two large six-sided dice mid-tumble, glossy white faces with chrome bevelled edges and pips catching spectrum light.",
        "color_palette": [
          "#FFFFFF",
          "#00C8F0",
          "#FF2D95"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          520,
          700,
          940,
          1200
        ],
        "desc": "Three more dice, semi-transparent and ghosted, trailing behind the solid pair as afterimages.",
        "color_palette": [
          "#7CE7C4",
          "#FFD400",
          "#00C8F0"
        ]
      }
    ]
  }
}
```

## chapter_03_opener.png

- **Placement**: chapter 3 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Character creation. Absence of people is deliberate: these are roles not yet filled.

```json
{
  "high_level_description": "An empty magenta coat, an empty pair of cyan skates and an empty clockwork sleeve are laid out on a bedroom floor as though waiting to be put on. Nobody is present. The absence is the subject.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Warm low lamplight and kitchen overheads, with spectrum light leaking in from off-frame.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A carpeted bedroom floor in warm lamplight, glitter worked into the pile, the edge of a bed and a skirting board visible.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          120,
          500,
          560,
          1100
        ],
        "desc": "A magenta coat laid flat and open, chrome-lined, still holding the shape of shoulders.",
        "color_palette": [
          "#FF2D95",
          "#FFFFFF"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          520,
          900,
          860,
          1240
        ],
        "desc": "A pair of cyan skates set neatly side by side, holographic oil-slick sheen on the boots.",
        "color_palette": [
          "#00C8F0",
          "#B9F2FF"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          600,
          480,
          940,
          880
        ],
        "desc": "A single sleeve of working brass clockwork, gears visible and stopped, lying across the carpet.",
        "color_palette": [
          "#FFD400",
          "#C89B3C"
        ]
      }
    ]
  }
}
```

## chapter_04_opener.png

- **Placement**: chapter 4 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The transformation chapter's hero image. Genderless silhouette.

```json
{
  "high_level_description": "A single genderless figure caught at the exact instant of refracting: their ordinary silhouette still visible inside the colour, one hand raised, light leaving them outward in hard spectrum bands. The hero image of the transformation chapter.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A dark violet field with radial spectrum bands driven outward from the figure, glitter suspended in the air.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          300,
          340,
          730,
          1300
        ],
        "desc": "A full-length genderless human silhouette, one hand raised, the body reading as an ordinary person at the core and as separated spectrum at the edges.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      }
    ]
  }
}
```

## chapter_05_opener.png

- **Placement**: chapter 5 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The Gloom clock made literal. Should feel like pressure, not menace.

```json
{
  "high_level_description": "A chrome clock face divided into six segments floats above a wet pavement that reflects it. Three segments are cracked and leaking colour. The mood is pressure and weight, not menace.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "Wet night pavement under sodium light, the clock's reflection broken across puddles, deep violet sky above.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          230,
          380,
          800,
          950
        ],
        "desc": "A large chrome disc marked into six equal segments, three of them fractured with light bleeding from the cracks.",
        "color_palette": [
          "#C9D2DA",
          "#FF2D95",
          "#FFD400"
        ]
      }
    ]
  }
}
```

## chapter_06_opener.png

- **Placement**: chapter 6 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Pregen roster page. Flat, poster-like, almost a colour swatch.

```json
{
  "high_level_description": "A roster poster for a magical-girl and sentai roleplaying game: five young heroes standing together in a row against a rainbow gradient, three young women and two young men, colour coded magenta, cyan, sunburst yellow, violet and mint green. Glossy airbrushed poster art, each hero in a confident pose.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A broad horizontal rainbow gradient sweeping magenta through cyan into mint, scattered with star-sparkles and drifting glitter.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          40,
          300,
          990,
          1290
        ],
        "desc": "A row of five costumed heroes standing shoulder to shoulder across the frame: a magenta young woman in a long streaming coat, a cyan young man on skates holding a skateboard, a sunburst yellow young woman in a coat of brass clockwork, a violet young woman standing perfectly still, and a mint green young man with his hands in his pockets. Airbrushed in glossy rainbow with chrome edging.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      }
    ]
  }
}
```

## chapter_07_opener.png

- **Placement**: chapter 7 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The setting chapter. Same geometry both times — that is the point.

```json
{
  "high_level_description": "One ordinary residential street rendered twice in the same frame, interleaved in vertical bands: plain daylight in some bands, full airbrushed spectrum in others. The geometry is identical in both, which is the entire point.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A terraced residential street with parked cars and wheelie bins, alternating in vertical stripes between flat overcast daylight and saturated prismatic colour.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          0,
          0,
          1024,
          1536
        ],
        "desc": "Regular vertical bands across the whole frame switching between the everyday and spectrum renderings of exactly the same buildings and pavement.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4",
          "#9AA0A6"
        ]
      }
    ]
  }
}
```

## chapter_08_opener.png

- **Placement**: chapter 8 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The GM chapter, from behind the screen. Warm and domestic.

```json
{
  "high_level_description": "A close three-quarter still life of a tabletop roleplaying game in progress: a heap of glossy iridescent rainbow dice catching the light, a chunky ceramic mug, and a pencil, all on a polished wooden surface. Shot close and low so the dice fill the frame. Glittering Lisa Frank airbrush.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A polished wooden tabletop filling the frame, falling away into soft rainbow bokeh and drifting glitter at the top edge.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          120,
          520,
          920,
          1180
        ],
        "desc": "A generous heap of glossy six-sided dice in rainbow holographic finishes, chrome pips, scattered across polished wood with a ceramic mug behind them and a yellow pencil lying alongside.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#FFFFFF"
        ]
      }
    ]
  }
}
```

## chapter_09_opener.png

- **Placement**: chapter 9 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The antagonist chapter. It must read as leaving, never as charging.

```json
{
  "high_level_description": "An enormous bus as long as a whole street and three storeys tall, chrome and rust, seen from the pavement as it draws away into the distance. Rendered in full Lisa Frank rainbow airbrush. It is always leaving.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A rainbow spectrum street at night stretching to a far vanishing point, glitter banked in the gutters, star-sparkles across a magenta and violet sky.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          40,
          380,
          990,
          1180
        ],
        "desc": "A colossal articulated bus seen from behind and to one side, drawing away down the street, iridescent chrome panels streaked with rust, every window lit warm gold, tail lights glowing red.",
        "color_palette": [
          "#C9D2DA",
          "#B5651D",
          "#FFD400",
          "#2B0B4A"
        ]
      }
    ]
  }
}
```

## chapter_10_opener.png

- **Placement**: chapter 10 opener
- **Dimensions**: 1024 × 1536 (full_page)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Starter adventure opener. Lettering on the timetable is required and should be legible.

```json
{
  "high_level_description": "A night bus timetable mounted on a chrome post, rendered in nine colours. One printed strip at the bottom of the timetable glows brighter than everything else on the board. The lettering is legible.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A spectrum street at night behind the post, softly out of focus, gradient sky and drifting glitter.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          260,
          300,
          780,
          1180
        ],
        "desc": "A rectangular timetable board on a chrome post, columns of small legible printed times, the whole board iridescent.",
        "color_palette": [
          "#00C8F0",
          "#FF2D95",
          "#FFFFFF"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          300,
          980,
          740,
          1120
        ],
        "desc": "One printed strip near the bottom of the board glowing markedly brighter than the rows above it, clearly legible.",
        "color_palette": [
          "#FFD400",
          "#FFFFFF"
        ]
      }
    ]
  }
}
```

## portrait_wren_adeyemi.png

- **Placement**: NPC portrait — Wren Adeyemi
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Ungendered presentation: no gendered styling cues beyond what is described. The assigned colour is canonical and must not drift.
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

```json
{
  "high_level_description": "A glowing Lisa Frank style character portrait of Wren Adeyemi, a young Black woman, a hero of a magical-girl and sentai roleplaying game, rendered throughout in magenta and chrome. Her long coat streams behind her like a comet tail throwing off sparks that keep burning where they land. Her hands are deliberately empty. She is mid-stride, moving fast and looking back over one shoulder.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#FFFFFF",
      "#C9D2DA"
    ]
  },
  "compositional_deconstruction": {
    "background": "A rainbow gradient field in the character's own colour deepening at the edges, thick with drifting glitter, star-sparkles and soft prismatic lens flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          150,
          90,
          880,
          1010
        ],
        "desc": "A single full-length figure of a young Black woman filling most of the frame, airbrushed in magenta and chrome with glossy chrome edging and rainbow rim light. Her long coat streams behind her like a comet tail throwing off sparks that keep burning where they land. Her hands are deliberately empty. She is mid-stride, moving fast and looking back over one shoulder.",
        "color_palette": [
          "#FF2D95",
          "#FFFFFF",
          "#C9D2DA"
        ]
      }
    ]
  }
}
```

## portrait_tobias_lark.png

- **Placement**: NPC portrait — Tobias 'Toby' Lark
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Ungendered presentation: no gendered styling cues beyond what is described. The assigned colour is canonical and must not drift.
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

```json
{
  "high_level_description": "A glowing Lisa Frank style character portrait of Tobias 'Toby' Lark, a young man, a hero of a magical-girl and sentai roleplaying game, rendered throughout in cyan and holographic oil-slick shimmer. He stands grinning with a battered skateboard under one arm, covered in somebody else's stickers, and his skates leave a rainbow gradient hanging in the air behind him. Head and shoulders and upper body fill the frame.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#00C8F0",
      "#B9F2FF",
      "#FF2D95"
    ]
  },
  "compositional_deconstruction": {
    "background": "A rainbow gradient field in the character's own colour deepening at the edges, thick with drifting glitter, star-sparkles and soft prismatic lens flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          150,
          90,
          880,
          1010
        ],
        "desc": "A single full-length figure of a young man filling most of the frame, airbrushed in cyan and holographic oil-slick shimmer with glossy chrome edging and rainbow rim light. He stands grinning with a battered skateboard under one arm, covered in somebody else's stickers, and his skates leave a rainbow gradient hanging in the air behind him. Head and shoulders and upper body fill the frame.",
        "color_palette": [
          "#00C8F0",
          "#B9F2FF",
          "#FF2D95"
        ]
      }
    ]
  }
}
```

## portrait_priya_raghunathan.png

- **Placement**: NPC portrait — Priya Raghunathan
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Ungendered presentation: no gendered styling cues beyond what is described. The assigned colour is canonical and must not drift.
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

```json
{
  "high_level_description": "A glowing Lisa Frank style character portrait of exactly one person: Priya Raghunathan, a single young South Asian woman, a hero of a magical-girl and sentai roleplaying game, rendered throughout in sunburst yellow and polished brass. One woman only, alone in the frame, one head and one pair of hands.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FFD400",
      "#C89B3C",
      "#FFFFFF"
    ]
  },
  "compositional_deconstruction": {
    "background": "A sunburst yellow and brass rainbow gradient deepening at the edges, thick with drifting glitter, star-sparkles and soft prismatic lens flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          210,
          110,
          830,
          1010
        ],
        "desc": "A single solitary young South Asian woman, one figure alone, shown from the waist up and centred in the frame. She wears a long coat made of working brass clockwork with gears turning at the shoulders, and holds up one tiny wrench, head tilted, studying it. Airbrushed in glossy sunburst yellow with chrome edging and rainbow rim light.",
        "color_palette": [
          "#FFD400",
          "#C89B3C",
          "#FFFFFF"
        ]
      }
    ]
  }
}
```

## portrait_marisol_vega.png

- **Placement**: NPC portrait — Marisol Vega
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Ungendered presentation: no gendered styling cues beyond what is described. The assigned colour is canonical and must not drift.
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

```json
{
  "high_level_description": "A glowing Lisa Frank style character portrait of Marisol Vega, a young Latina woman, a hero of a magical-girl and sentai roleplaying game, rendered throughout in violet and deep starfield. The starfield is not printed on her: it is real depth, as though something enormous were showing through her coat. She is completely still, calm and centred, a ring of door keys hooked on one finger.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#2B0B4A",
      "#7B5CD6",
      "#FFFFFF"
    ]
  },
  "compositional_deconstruction": {
    "background": "A rainbow gradient field in the character's own colour deepening at the edges, thick with drifting glitter, star-sparkles and soft prismatic lens flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          150,
          90,
          880,
          1010
        ],
        "desc": "A single full-length figure of a young Latina woman filling most of the frame, airbrushed in violet and deep starfield with glossy chrome edging and rainbow rim light. The starfield is not printed on her: it is real depth, as though something enormous were showing through her coat. She is completely still, calm and centred, a ring of door keys hooked on one finger.",
        "color_palette": [
          "#2B0B4A",
          "#7B5CD6",
          "#FFFFFF"
        ]
      }
    ]
  }
}
```

## portrait_danny_okonkwo_byrne.png

- **Placement**: NPC portrait — Danny Okonkwo-Byrne
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Ungendered presentation: no gendered styling cues beyond what is described. The assigned colour is canonical and must not drift.
- **Notes**: Pregenerated Star. Colour is canonical and must not drift. Ungendered presentation; do not add gendered styling cues not present in the description.

```json
{
  "high_level_description": "A glowing Lisa Frank style character portrait of Danny Okonkwo-Byrne, a young man, a hero of a magical-girl and sentai roleplaying game, rendered throughout in mint green and pearl. A soft glow with no obvious source surrounds him and makes the air feel like a small warm room. He sits easily with his hands in his pockets, relaxed, listening.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#7CE7C4",
      "#F2F0E6",
      "#FFD400"
    ]
  },
  "compositional_deconstruction": {
    "background": "A rainbow gradient field in the character's own colour deepening at the edges, thick with drifting glitter, star-sparkles and soft prismatic lens flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          150,
          90,
          880,
          1010
        ],
        "desc": "A single full-length figure of a young man filling most of the frame, airbrushed in mint green and pearl with glossy chrome edging and rainbow rim light. A soft glow with no obvious source surrounds him and makes the air feel like a small warm room. He sits easily with his hands in his pockets, relaxed, listening.",
        "color_palette": [
          "#7CE7C4",
          "#F2F0E6",
          "#FFD400"
        ]
      }
    ]
  }
}
```

## portrait_the_last_bus.png

- **Placement**: NPC portrait — The Last Bus (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Indifferent, never attacking or gloating: it is doing one thing forever. Fully saturated; the Glooms are not grey.
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

```json
{
  "high_level_description": "A bus the length of a street, three storeys of chrome and rust. Every window is lit warm and full of people who are not looking out. Its doors are always closing. It is forever pulling away, indifferent.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A spectrum street at night, the far end of the vehicle lost in gradient haze.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          40,
          260,
          990,
          900
        ],
        "desc": "An enormous articulated bus filling the frame in three-quarter rear view, chrome panels streaked with rust, every window lit warm and full of seated people facing away, doors caught mid-close.",
        "color_palette": [
          "#C9D2DA",
          "#B5651D",
          "#FFD400",
          "#2B0B4A"
        ]
      }
    ]
  }
}
```

## portrait_the_quiet_shelf.png

- **Placement**: NPC portrait — The Quiet Shelf (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Indifferent, never attacking or gloating: it is doing one thing forever. Fully saturated; the Glooms are not grey.
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

```json
{
  "high_level_description": "Library shelves grown so tall and so far apart that the aisle between them is a canyon and the ceiling is only a rumour. Warm, silent and glittering, rendered in Lisa Frank rainbow airbrush. A returns slot sits high in one wall, far out of reach.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "Towering stacks receding into warm rainbow gradient, dust and glitter hanging in shafts of prismatic light.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          40,
          0,
          990,
          1010
        ],
        "desc": "Two vast ranks of library shelving in iridescent brass and magenta, packed with glowing book spines, converging into glittering gradient dark.",
        "color_palette": [
          "#C89B3C",
          "#FF2D95",
          "#7CE7C4"
        ]
      }
    ]
  }
}
```

## portrait_the_silt.png

- **Placement**: NPC portrait — The Silt (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Indifferent, never attacking or gloating: it is doing one thing forever. Fully saturated; the Glooms are not grey.
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

```json
{
  "high_level_description": "A vast mirror-bright chrome surface seen from just above, filling the whole frame, with an iridescent oil-slick rainbow swimming across it. It reflects a row of rooftops and a footbridge, but the reflection is very slightly out of true. Glossy, saturated Lisa Frank airbrush.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "The mirrored chrome surface fills the frame edge to edge, star-sparkles caught on it, a thin band of magenta and violet sky at the very top.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          0,
          120,
          1024,
          1010
        ],
        "desc": "A huge sheet of mirror-bright liquid chrome with holographic oil-slick rainbow bands rippling across its surface, holding a soft reflection of rooftops and a footbridge that does not quite line up.",
        "color_palette": [
          "#C9D2DA",
          "#00C8F0",
          "#FF2D95",
          "#FFD400"
        ]
      }
    ]
  }
}
```

## portrait_the_long_weekend.png

- **Placement**: NPC portrait — The Long Weekend (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Indifferent, never attacking or gloating: it is doing one thing forever. Fully saturated; the Glooms are not grey.
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

```json
{
  "high_level_description": "One extremely comfortable armchair with a folded blanket over its arm, floating alone in a warm rainbow void, ringed by six free-standing doorframes that all open back onto the very same armchair. Cosy, glowing and endless. Lisa Frank airbrush poster art.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A warm golden and magenta rainbow gradient void with star-sparkles and drifting glitter, no walls and no floor.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          260,
          380,
          780,
          900
        ],
        "desc": "A deep, plush, very inviting armchair in iridescent fabric with a folded rainbow blanket over one arm, glowing softly.",
        "color_palette": [
          "#FFD400",
          "#FF2D95",
          "#7CE7C4"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          60,
          120,
          980,
          1010
        ],
        "desc": "Six free-standing doorframes arranged in a ring around the armchair, each one framing a small identical copy of the very same armchair.",
        "color_palette": [
          "#00C8F0",
          "#FFD400"
        ]
      }
    ]
  }
}
```

## portrait_the_grey_ledger.png

- **Placement**: NPC portrait — The Grey Ledger (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Indifferent, never attacking or gloating: it is doing one thing forever. Fully saturated; the Glooms are not grey.
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

```json
{
  "high_level_description": "An enormous filing structure of shelves, drawers and pneumatic tubes rising up past where the sky should be. Everything it processes comes out perfectly accurate and completely drained of colour.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A vast institutional interior in saturated violet and brass, tubes converging overhead into gradient haze.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          380,
          900,
          700,
          1250
        ],
        "desc": "A chute at the base of the structure delivering papers that are entirely grey, in contrast to the saturated colour everywhere else in the frame.",
        "color_palette": [
          "#9AA0A6",
          "#D8D8D8"
        ]
      }
    ]
  }
}
```

## portrait_the_understudy.png

- **Placement**: NPC portrait — The Understudy (Gloom)
- **Dimensions**: 1024 × 1024 (portrait)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Constraint**: Indifferent, never attacking or gloating: it is doing one thing forever. Fully saturated; the Glooms are not grey.
- **Notes**: Antagonist. It must never look like it is attacking or gloating — it is doing one thing forever, indifferently. Keep it saturated; the Glooms are not grey.

```json
{
  "high_level_description": "Two nearly identical magical-girl heroes stand side by side in rainbow airbrush: the same silhouette, the same magenta colour, but the one on the right is a little brighter and a little more perfect, and she is holding out one hand to help. Kind, patient and quietly wrong.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A magenta and chrome gradient field with star-sparkles and drifting glitter.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          90,
          140,
          520,
          1010
        ],
        "desc": "The first hero, ordinary and slightly tired, standing with her arms at her sides.",
        "color_palette": [
          "#FF2D95",
          "#C9D2DA"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          500,
          120,
          940,
          1010
        ],
        "desc": "Her near-double, identical but glossier and brighter, offering one hand with a patient, kindly expression.",
        "color_palette": [
          "#FF2D95",
          "#FFFFFF",
          "#FFD400"
        ]
      }
    ]
  }
}
```

## ch_02_backing.png

- **Placement**: content illustration — chapter 2, near 'Power of Friendship'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The core mechanic as an image.

```json
{
  "high_level_description": "A hand reaches into frame to steady another hand that is holding dice. Both figures are colour-coded and half-transformed. Spectrum light passes between the two hands.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A close, shallow field in deep violet, everything but the hands falling away into gradient.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          120,
          200,
          760,
          800
        ],
        "desc": "Two hands close together at frame centre, one cupping dice, the other steadying it from beneath, skin edged in prismatic rim light.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFFFFF"
        ]
      }
    ]
  }
}
```

## ch_03_radiance.png

- **Placement**: content illustration — chapter 3, near 'Radiance'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Look versus Radiance in one frame.

```json
{
  "high_level_description": "A young woman in ordinary clothes stands in her bedroom looking into a tall chrome-framed mirror. What the mirror shows is not ordinary: it is the same woman transformed into a rainbow hero, glowing and glittering, calmly looking back out at her. Airbrushed Lisa Frank poster art.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A plain bedroom wall on the near side of the frame, opening into rainbow gradient and star-sparkles inside the mirror.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          90,
          300,
          700,
          1480
        ],
        "desc": "A tall chrome-framed mirror standing against the wall, with an ordinary young woman in jeans and a jacket seen from behind in front of it, and her reflection inside the glass rendered as a glowing rainbow hero in a spectrum coat.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      }
    ]
  }
}
```

## ch_04_synchronized.png

- **Placement**: content illustration — chapter 4, near 'Synchronized Morph'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The sentai register. Should feel loud.

```json
{
  "high_level_description": "Five magical-girl and sentai heroes, three young women and two young men, call out their transformation word together at the same moment, seen from ground level so they tower over the viewer. Rainbow colour blooms outward from all five at once in wide airbrushed bands. Joyful and spectacular. They wear glossy colour-coded hero costumes.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A night sky already opening into rainbow spectrum above wet tarmac, star-sparkles and glitter carried outward on the light.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          30,
          150,
          1500,
          950
        ],
        "desc": "A row of five costumed heroes seen from below, heads lifted and mouths open on the same word, three young women and two young men, each glowing in one colour: magenta, cyan, sunburst yellow, violet and mint green, rainbow light blooming out around them.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          0,
          900,
          1536,
          1024
        ],
        "desc": "The wet tarmac of the road in the immediate foreground, holding long rainbow reflections of the five figures above.",
        "color_palette": [
          "#2B0B4A",
          "#FF2D95",
          "#00C8F0"
        ]
      }
    ]
  }
}
```

## ch_04_combined.png

- **Placement**: content illustration — chapter 4, near 'Combined Form'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Rare and huge. Should not fit in the frame comfortably.

```json
{
  "high_level_description": "One colossal fused hero standing in a narrow street far too small for it, its surface visibly braided from five different colours of light. Chrome and rainbow gradient, glittering, cropped by the top of the frame.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A narrow terraced street at night drenched in rainbow spectrum, rooftops far below the figure's shoulders, glitter falling like warm snow.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          30,
          0,
          740,
          1480
        ],
        "desc": "A single enormous humanoid figure whose armour is five colours plaited together in glossy airbrushed bands, chrome bevelled, its head and shoulders cut off by the top edge.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          40,
          1200,
          730,
          1520
        ],
        "desc": "The ordinary street below: parked cars and wheelie bins, tiny by comparison, lit rainbow by the figure above.",
        "color_palette": [
          "#00C8F0",
          "#FF2D95"
        ]
      }
    ]
  }
}
```

## ch_05_dimmed.png

- **Placement**: content illustration — chapter 5, near 'Getting Dimmed'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The most emotionally important image in the book. Grey figure, saturated world.

```json
{
  "high_level_description": "An adult woman in ordinary everyday clothes, drawn entirely in soft pearl greys and silver, stands at the centre of a street blazing with rainbow spectrum colour. She is upright, calm and composed. The picture is about the contrast between her quiet silver and the candy-bright world around her.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A hyper-saturated rainbow street at night, iridescent shopfronts, glitter banked in the gutters, star-sparkles everywhere, entirely undimmed.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          220,
          480,
          570,
          1420
        ],
        "desc": "A grown woman in jeans, boots and a warm winter coat, rendered entirely in soft pearl grey and silver airbrush, standing squarely with her hands at her sides, fully and warmly dressed, surrounded by colour that does not touch her.",
        "color_palette": [
          "#B4B4B4",
          "#E6E6E6",
          "#8A8A8A"
        ]
      }
    ]
  }
}
```

## ch_05_reaching.png

- **Placement**: content illustration — chapter 5, near 'Reaching someone'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Pairs with ch_05_dimmed. This is the game's thesis as a picture.

```json
{
  "high_level_description": "One colour-blazing figure kneels to take the hand of a grey, drained figure. At the point where their hands meet, colour is just beginning to bleed back into the grey one.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A spectrum street at night, saturated and warm, the two figures at centre frame.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          560,
          260,
          1180,
          940
        ],
        "desc": "A kneeling figure in full spectrum colour, one hand extended and closed around the other's hand.",
        "color_palette": [
          "#FF2D95",
          "#00C8F0",
          "#FFD400",
          "#2B0B4A",
          "#7CE7C4"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          200,
          320,
          700,
          960
        ],
        "desc": "A seated grey figure taking that hand, colour returning first at the wrist and spreading up the forearm.",
        "color_palette": [
          "#8A8A8A",
          "#FF2D95",
          "#7CE7C4"
        ]
      }
    ]
  }
}
```

## ch_07_spectrum_street.png

- **Placement**: content illustration — chapter 7, near 'The Spectrum'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Establishing shot for the setting. The leopard does not react to anything.

```json
{
  "high_level_description": "A corner launderette rendered in nine iridescent colours with glossy chrome bevelled trim, glitter banked in the gutters like warm snow. A friendly rainbow-spotted snow leopard is asleep on the flat roof, completely at ease and reacting to nothing. Pure Lisa Frank.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A suburban corner shopfront at dusk under a magenta-into-cyan gradient sky, ordinary bollards and drainpipes still perfectly recognisable beneath the rainbow treatment, star-sparkles throughout.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          120,
          380,
          1050,
          950
        ],
        "desc": "An ordinary corner launderette shopfront, airbrushed in glossy rainbow with chrome trim and glowing windows.",
        "color_palette": [
          "#00C8F0",
          "#FF2D95",
          "#FFD400"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          700,
          150,
          1180,
          430
        ],
        "desc": "A large snow leopard with iridescent rainbow rosettes curled up asleep on the flat roof, peaceful and friendly.",
        "color_palette": [
          "#FFFFFF",
          "#B9F2FF",
          "#FF2D95"
        ]
      }
    ]
  }
}
```

## ch_07_dolphins.png

- **Placement**: content illustration — chapter 7, near 'The Spectrum'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Pure Lisa Frank. Should be joyful, not surreal-menacing.

```json
{
  "high_level_description": "A pod of iridescent rainbow dolphins gliding through open air high above a ring road, as though the sky were a coral reef, trailing glitter and star-sparkles behind them. The traffic far below carries on as normal. Joyful and dreamlike, classic Lisa Frank airbrush.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A vast gradient sky from cyan through magenta above a dual carriageway at dusk, streetlights just coming on, glitter drifting across the frame.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          100,
          1340,
          700
        ],
        "desc": "Four dolphins arcing gracefully through the air at rooftop height, their skin a glossy holographic rainbow, sparkling wakes trailing behind them.",
        "color_palette": [
          "#00C8F0",
          "#B9F2FF",
          "#FF2D95"
        ]
      }
    ]
  }
}
```

## ch_08_table.png

- **Placement**: content illustration — chapter 8, near 'Pacing a first session'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Practical GM-chapter image. The empty chair is deliberate.

```json
{
  "high_level_description": "An overhead view of a kitchen table mid-session: dice, a hand-drawn six-segment clock with three segments crossed off, five character sheets, and one empty chair. The empty chair is deliberate.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Warm low lamplight and kitchen overheads, with spectrum light leaking in from off-frame.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A wooden tabletop shot straight down under a warm pendant lamp, the floor and chair backs visible at the edges.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          120,
          200,
          650,
          700
        ],
        "desc": "Five sheets of blank unmarked paper fanned across the table, plain and empty.",
        "color_palette": [
          "#F4EFE4",
          "#2B2B2B"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          260,
          720,
          520,
          980
        ],
        "desc": "A circle drawn on a scrap of paper and divided into six plain wedges, three of them shaded solid.",
        "color_palette": [
          "#F4EFE4",
          "#1A1A1A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          40,
          1150,
          400,
          1500
        ],
        "desc": "One empty chair pulled back from the table, seen from above.",
        "color_palette": [
          "#6B4F2A"
        ]
      }
    ]
  }
}
```

## ch_09_gloom_scale.png

- **Placement**: content illustration — chapter 9, near 'How to read a Gloom'
- **Dimensions**: 1536 × 1024 (landscape)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Clock sizes 4, 6 and 8 made visual.

```json
{
  "high_level_description": "A scale comparison: three monster silhouettes of very different sizes standing on a simple ground line against a rainbow gradient. A small one the size of a parked car, a middle one as long as a street, and a huge one cut off by the top of the frame. Clean, bold and poster-like.",
  "style_description": {
    "aesthetics": "Full 1990s Lisa Frank airbrush poster art. Hyper-saturated rainbow gradients, iridescent holographic sheen, candy-bright neon, glossy chrome bevelled edges, scattered star-sparkles and lens flares, glitter drifting through the air, dreamy prismatic bloom. Joyful, sincere and unembarrassed. Never muted, never ironic, never grim.",
    "lighting": "Prismatic rainbow glow with neon rim light and bright star-sparkle highlights, over deep magenta-into-violet gradients.",
    "photo": "Glossy airbrushed poster illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration on poster stock",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "A smooth rainbow gradient from magenta through violet into cyan, with star-sparkles and a single simple horizon line.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          60,
          620,
          380,
          900
        ],
        "desc": "The smallest creature silhouette, roughly the size of a parked car, filled with deep violet.",
        "color_palette": [
          "#2B0B4A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          430,
          320,
          950,
          900
        ],
        "desc": "The middle creature silhouette, as long as a street, filled with deep violet.",
        "color_palette": [
          "#2B0B4A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          1000,
          0,
          1500,
          900
        ],
        "desc": "The largest creature silhouette, so tall it is cropped by the top edge of the frame, filled with deep violet.",
        "color_palette": [
          "#2B0B4A"
        ]
      }
    ]
  }
}
```

## ch_10_timetable.png

- **Placement**: content illustration — chapter 10, near 'The last thirty seconds'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The payoff image. Back in the everyday. Lettering required and must be legible.

```json
{
  "high_level_description": "A close view of a bus timetable in ordinary daylight. One printed strip at the bottom reads 'Fridays, late service, 00:15' and is clearly legible. A single piece of glitter is caught in the frame. The payoff image: back in the everyday.",
  "style_description": {
    "aesthetics": "Clean airbrushed illustration, realistic and restrained, in the same polished style as the rest of the book but almost entirely desaturated.",
    "lighting": "Flat overcast daylight. This image is in the everyday, not the Spectrum, so the colour is ordinary apart from one detail.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#00C8F0",
      "#FFD400",
      "#2B0B4A",
      "#7CE7C4"
    ]
  },
  "compositional_deconstruction": {
    "background": "An ordinary bus shelter panel in flat daylight, greys and greens, a residential street softly out of focus behind.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          160,
          300,
          620,
          1200
        ],
        "desc": "A printed paper timetable behind scratched perspex, columns of small legible times, entirely mundane.",
        "color_palette": [
          "#F4F4F0",
          "#2B2B2B",
          "#1F6B3A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          200,
          980,
          600,
          1090
        ],
        "desc": "A printed strip near the bottom reading 'Fridays, late service, 00:15', legible and unremarkable.",
        "color_palette": [
          "#F4F4F0",
          "#1A1A1A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          600,
          700,
          700,
          800
        ],
        "desc": "One single speck of magenta glitter caught on the perspex, the only saturated colour in the image.",
        "color_palette": [
          "#FF2D95"
        ]
      }
    ]
  }
}
```
