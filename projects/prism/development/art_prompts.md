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
  "high_level_description": "Five colour-coded full-length silhouettes stand in a loose row against a plain white background: magenta, cyan, sunburst yellow, violet and mint green, each in a distinct stance. A roster page, flat and poster-like, almost a colour swatch.",
  "style_description": {
    "aesthetics": "Flat poster-style airbrushed illustration, Lisa Frank palette, clean vector-like silhouettes against white, almost a colour swatch.",
    "lighting": "Even flat studio light, no shadows.",
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
    "background": "Flat white, no depth, no shadow.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          60,
          300,
          964,
          1240
        ],
        "desc": "Five evenly spaced standing silhouettes, filled with flat saturated colour, no facial detail, each posed differently.",
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
  "high_level_description": "A Showrunner's-eye view across a kitchen table: dice, a hand-drawn clock on paper, five character sheets, mugs, and spectrum light leaking in from off-frame. Warm, domestic and lived-in.",
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
    "background": "A wooden kitchen table under a low warm pendant lamp, the rest of the room falling away into soft dark, coloured light entering from the left edge.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          120,
          700,
          500,
          1050
        ],
        "desc": "Five paper character sheets fanned out, handwritten, one with a corner folded over.",
        "color_palette": [
          "#F4EFE4",
          "#2B2B2B"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          540,
          760,
          760,
          980
        ],
        "desc": "A hand-drawn circle divided into six segments on a scrap of paper, some segments crossed through in biro.",
        "color_palette": [
          "#F4EFE4",
          "#1A1A1A",
          "#FF2D95"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          760,
          620,
          950,
          900
        ],
        "desc": "Two mugs and a scatter of six-sided dice on the wood.",
        "color_palette": [
          "#FFFFFF",
          "#00C8F0"
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
  "high_level_description": "Seen from the pavement: a bus the length of a whole street, three storeys of chrome and rust, headlights like two dead suns. It is always pulling away. It must read as leaving, never as charging.",
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
    "background": "A spectrum-lit street at night stretching to an impossible vanishing point, the far end of the bus disappearing into gradient haze.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          60,
          400,
          1024,
          1150
        ],
        "desc": "An enormous articulated bus in three-quarter rear view, receding, chrome panels streaked with rust, every window lit warm.",
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
  "high_level_description": "A character portrait of Wren Adeyemi, a hero of a magical-girl and sentai roleplaying game, rendered entirely in magenta and chrome. A coat trails behind them like a comet, throwing off sparks that do not go out where they land. Their hands are deliberately empty. They are moving fast and looking back over one shoulder.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FF2D95",
      "#FFFFFF",
      "#C9D2DA"
    ]
  },
  "compositional_deconstruction": {
    "background": "A soft gradient field in the character's own colour, deepening at the edges, with drifting glitter and faint prismatic flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          120,
          850,
          1000
        ],
        "desc": "A full-length illustrated figure filling most of the frame, rendered in magenta and chrome. A coat trails behind them like a comet, throwing off sparks that do not go out where they land. Their hands are deliberately empty. They are moving fast and looking back over one shoulder.",
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
  "high_level_description": "A character portrait of Tobias 'Toby' Lark, a hero of a magical-girl and sentai roleplaying game, rendered entirely in cyan and holographic oil-slick shimmer. Skates leave a gradient hanging in the air behind them. They carry a battered skateboard covered in somebody else's stickers, caught mid-motion and grinning.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#00C8F0",
      "#B9F2FF",
      "#FF2D95"
    ]
  },
  "compositional_deconstruction": {
    "background": "A soft gradient field in the character's own colour, deepening at the edges, with drifting glitter and faint prismatic flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          120,
          850,
          1000
        ],
        "desc": "A full-length illustrated figure filling most of the frame, rendered in cyan and holographic oil-slick shimmer. Skates leave a gradient hanging in the air behind them. They carry a battered skateboard covered in somebody else's stickers, caught mid-motion and grinning.",
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
  "high_level_description": "A character portrait of Priya Raghunathan, a hero of a magical-girl and sentai roleplaying game, rendered entirely in sunburst yellow and brass. Their coat is made of working clockwork, gears visibly turning at the shoulders and hem. They hold a wrench far too small to be useful, head tilted, examining something off-frame.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#FFD400",
      "#C89B3C",
      "#FFFFFF"
    ]
  },
  "compositional_deconstruction": {
    "background": "A soft gradient field in the character's own colour, deepening at the edges, with drifting glitter and faint prismatic flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          120,
          850,
          1000
        ],
        "desc": "A full-length illustrated figure filling most of the frame, rendered in sunburst yellow and brass. Their coat is made of working clockwork, gears visibly turning at the shoulders and hem. They hold a wrench far too small to be useful, head tilted, examining something off-frame.",
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
  "high_level_description": "A character portrait of Marisol Vega, a hero of a magical-girl and sentai roleplaying game, rendered entirely in violet and starfield. The starfield is not printed on them: it is actual depth, as though something enormous were showing through. They are completely still. A set of door keys is the only thing about them that would make a sound.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#2B0B4A",
      "#7B5CD6",
      "#FFFFFF"
    ]
  },
  "compositional_deconstruction": {
    "background": "A soft gradient field in the character's own colour, deepening at the edges, with drifting glitter and faint prismatic flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          120,
          850,
          1000
        ],
        "desc": "A full-length illustrated figure filling most of the frame, rendered in violet and starfield. The starfield is not printed on them: it is actual depth, as though something enormous were showing through. They are completely still. A set of door keys is the only thing about them that would make a sound.",
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
  "high_level_description": "A character portrait of Danny Okonkwo-Byrne, a hero of a magical-girl and sentai roleplaying game, rendered entirely in mint green and pearl. A soft glow with no obvious source makes the air around them feel like a small room. Hands in pockets, sitting while everyone else stands.",
  "style_description": {
    "aesthetics": "Hyper-saturated airbrushed rainbow illustration in a 1990s Lisa Frank poster idiom. Glossy chrome bevels, neon rim light, prismatic gradients, high-gloss trapper-keeper artwork. Sincere and unembarrassed, never ironic.",
    "lighting": "Neon rim light and internal prismatic glow against deep violet night, with ordinary sodium streetlight wherever the everyday world shows through.",
    "photo": "Clean airbrushed illustration. No film grain, no halftone.",
    "medium": "Airbrush illustration",
    "color_palette": [
      "#7CE7C4",
      "#F2F0E6",
      "#FFD400"
    ]
  },
  "compositional_deconstruction": {
    "background": "A soft gradient field in the character's own colour, deepening at the edges, with drifting glitter and faint prismatic flares.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          120,
          850,
          1000
        ],
        "desc": "A full-length illustrated figure filling most of the frame, rendered in mint green and pearl. A soft glow with no obvious source makes the air around them feel like a small room. Hands in pockets, sitting while everyone else stands.",
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
  "high_level_description": "Library shelves grown so tall and so far apart that the aisles are canyons and the ceiling is only a rumour. Warm and completely silent. A returns slot sits high in one wall, just out of reach.",
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
    "background": "Towering stacks receding into warm gradient dark, dust and glitter hanging in shafts of coloured light.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          60,
          0,
          980,
          1010
        ],
        "desc": "Two ranks of library shelving rising far out of frame, the aisle between them narrowing into warm gradient dark, books receding to specks, a returns slot set high in one wall.",
        "color_palette": [
          "#C89B3C",
          "#FF2D95",
          "#2B0B4A"
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
  "high_level_description": "A chrome tide, mirror-bright and thickening, advancing at the speed of a minute hand. It swallows landmarks and reflects them back slightly wrong.",
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
    "background": "A riverside at dusk in saturated colour, the far bank already under the advancing mirror surface.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          0,
          420,
          1024,
          1010
        ],
        "desc": "A mirror-bright chrome tide filling the lower half of the frame, its edge advancing almost imperceptibly, reflecting the landmarks it has already covered back slightly wrong.",
        "color_palette": [
          "#C9D2DA",
          "#00C8F0",
          "#2B0B4A"
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
  "high_level_description": "A very comfortable room that keeps adding doors, every one of which leads back into the same room. Deep chairs, good light, a blanket exactly warm enough. Nothing here is threatening and that is the problem.",
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
    "background": "A softly lit sitting room in warm saturated colour, more doorways in the walls than the geometry allows, each opening onto the same room again.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          60,
          120,
          980,
          1000
        ],
        "desc": "A softly lit sitting room with deep armchairs and a folded blanket, and more doorways set into its walls than the geometry allows, each opening onto the same room again.",
        "color_palette": [
          "#FFD400",
          "#FF2D95",
          "#7CE7C4"
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
  "high_level_description": "A figure that is almost exactly one of the heroes: same silhouette, same colour, slightly better made. It stands patiently with one hand out, offering to help. It is kind, and that is what is wrong with it.",
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
    "background": "A gradient field in magenta and chrome, a second fainter silhouette ghosted just behind the figure like an alignment error.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          240,
          130,
          820,
          1000
        ],
        "desc": "A standing illustrated figure with one hand extended in offer, patient and kind, and a second fainter silhouette ghosted a few degrees behind it like an alignment error.",
        "color_palette": [
          "#FF2D95",
          "#C9D2DA",
          "#FFFFFF"
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
  "high_level_description": "A single figure in ordinary clothes seen from behind, facing the spectrum version of themselves, which stands in front of them like a reflection that has turned round to look back.",
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
    "background": "A plain interior wall behind the ordinary figure dissolving into gradient spectrum around the transformed one.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          180,
          500,
          590,
          1500
        ],
        "desc": "The everyday figure from behind: jeans, an ordinary jacket, unremarkable.",
        "color_palette": [
          "#6B6459",
          "#3A3A3A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          200,
          300,
          600,
          1400
        ],
        "desc": "The same person, facing us, transformed: coat and silhouette blazing in spectrum, expression calm.",
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
  "high_level_description": "Five figures shout the same word at the same instant, shot from ground level so they loom. Colour erupts from all five simultaneously. It should feel loud.",
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
    "background": "A low camera on wet tarmac, five figures against a night sky already detonating into spectrum.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          40,
          120,
          1496,
          900
        ],
        "desc": "Five figures in a rank, heads back, mouths open on the same syllable, each detonating in a different colour.",
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

## ch_04_combined.png

- **Placement**: content illustration — chapter 4, near 'Combined Form'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: Rare and huge. Should not fit in the frame comfortably.

```json
{
  "high_level_description": "One enormous fused figure, visibly made of five colours braided together, standing in a street far too small for it. Chrome and gradient. It should not fit comfortably inside the frame.",
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
    "background": "A narrow terraced street at night in saturated colour, rooftops well below the figure's shoulders.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          40,
          0,
          728,
          1500
        ],
        "desc": "A single colossal humanoid form whose surface is five distinct colours plaited together, cropped by the top edge of the frame.",
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

## ch_05_dimmed.png

- **Placement**: content illustration — chapter 5, near 'Getting Dimmed'
- **Dimensions**: 768 × 1536 (column)
- **Generator profile**: ideogram-v4 (local `ideogram4_fp8_scaled`)
- **Notes**: The most emotionally important image in the book. Grey figure, saturated world.

```json
{
  "high_level_description": "One completely grey figure stands in the middle of a hyper-saturated spectrum street. All colour has drained out of that one person. Everything around them is still blazing. This is the most emotionally important image in the book.",
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
    "background": "A spectrum street at full saturation, glitter in the gutters, gradient sky, entirely undimmed.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          230,
          500,
          560,
          1400
        ],
        "desc": "A standing human figure rendered in flat desaturated grey, upright and present, not collapsed, surrounded by colour that does not touch them.",
        "color_palette": [
          "#8A8A8A",
          "#B4B4B4"
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
  "high_level_description": "A launderette on a street corner rendered in nine colours with chrome bevelled lettering, glitter banked in the gutters like warm snow. A snow leopard is asleep on the roof and reacts to nothing.",
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
    "background": "A corner shopfront at dusk in full saturation, gradient sky behind, ordinary bollards and drainpipes still perfectly recognisable.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          760,
          180,
          1180,
          480
        ],
        "desc": "A large snow leopard asleep on the flat roof of the launderette, curled up, entirely unbothered.",
        "color_palette": [
          "#FFFFFF",
          "#B9F2FF",
          "#2B0B4A"
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
  "high_level_description": "Dolphins move through the air above a ring road as though it were a reef. The traffic below is entirely unbothered. Joyful, not menacing.",
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
    "background": "A wide gradient sky from cyan into magenta above a dual carriageway at dusk, streetlights just coming on.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          200,
          120,
          1300,
          700
        ],
        "desc": "Three or four dolphins arcing through open air at rooftop height, iridescent, trailing glitter.",
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
        "desc": "Five paper character sheets spread around the table, handwritten.",
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
        "desc": "A hand-drawn circle in biro divided into six segments, three struck through.",
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
  "high_level_description": "Three shapes of very different sizes shown in flat silhouette against a gradient: a small one at knee height, a street-sized one, and one that runs up past the top edge of the frame. A scale comparison.",
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
    "background": "A clean gradient field from magenta through violet, no ground detail beyond a simple horizon line.",
    "elements": [
      {
        "type": "obj",
        "bbox": [
          80,
          620,
          380,
          900
        ],
        "desc": "The smallest silhouette, roughly the size of a parked car.",
        "color_palette": [
          "#2B0B4A"
        ]
      },
      {
        "type": "obj",
        "bbox": [
          440,
          300,
          940,
          900
        ],
        "desc": "The middle silhouette, as long as a street.",
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
        "desc": "The largest silhouette, cropped by the top edge, its full height not visible.",
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
