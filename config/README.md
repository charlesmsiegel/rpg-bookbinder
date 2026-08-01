# Configuration Reference — `config/system.json`

`config/system.json` is Bookbinder's single source of truth for everything that varies
per game system: display names, house-style voice rules, terminology, citation formats,
mechanical formulas, art-generation backends, DOCX theming, and knowledge-base layout.

It is loaded by `mcp_servers/_lib/config.py`:

- **Every key has a built-in neutral default** (see `config.DEFAULTS` in that file). A
  missing file, a missing section, or a missing individual field all fall back safely —
  you only need to write the keys you want to change.
- **Deep merge, not replace.** The JSON file is merged over the defaults key-by-key
  (dicts merge recursively; anything else — strings, numbers, booleans, lists — is
  replaced wholesale). Setting `"voice": {"tone_keywords": ["wry"]}` does not clear the
  rest of `voice`; only `tone_keywords` changes.
- **Cached.** The file is read once per process. Tools that need a fresh read (e.g. tests)
  call `config.load(force_reload=True)`.
- **Path override:** set the environment variable `BOOKBINDER_CONFIG` to an absolute path
  to load a different file instead of `config/system.json` — useful for keeping a
  game-specific config outside the repo (an "overlay") without editing the shipped
  default. Example:

  ```bash
  BOOKBINDER_CONFIG=/path/to/my-game/system.json python -m mcp_servers.project
  ```

- **Dotted-path access:** all servers read values with `config.get("mechanics.dice.sides")`
  style calls. Agent prompts are told to "consult `config/system.json`" directly rather
  than parsing it programmatically.

Every example below uses an invented system, **Example Quest RPG**, to show a fully
filled-in configuration. None of the values are required — they illustrate the shape.

---

## `system`

General identity fields, consumed by the project server (`project_type` default),
export scripts (`publisher_line` on cover/title pages), and agent prompts (`name`, used
whenever an agent needs to refer to "the game system").

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `name` | string | Display name of the game system | Agent prompts, exporters |
| `publisher_line` | string | Optional line printed on export covers/title pages (e.g. "A supplement for..."); omitted entirely when empty | `export-docx.js` and other exporters |
| `project_type` | string | Default value for a new project's type | `project.py` (`initialize_project`) |

```json
"system": {
  "name": "Example Quest RPG",
  "publisher_line": "A supplement for Example Quest RPG",
  "project_type": "supplement"
}
```

---

## `voice`

House-style rules for prose. Read by the writing and editing agents (lore-writer,
mechanics-designer, copy-editor) before they draft or revise text, and enforced
mechanically by the content server's `check_banned_terms` tool, which scans a draft
file against `banned_phrases`, `banned_names`, and `use_sparingly` and returns
violations with line numbers.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `writing_style_file` | string (path) | Markdown file with the house voice/style guide, relative to repo root | Writing/editing agent prompts |
| `tone_keywords` | array of strings | Short tone descriptors agents should aim for | Writing/editing agent prompts |
| `banned_phrases` | array of strings | Phrases/clichés that must not appear in prose. Supports a glob-style wildcard: `*` matches any run of text. Compiled to regex by `check_banned_terms` | `check_banned_terms` (content server) |
| `banned_names` | array of strings | Character/place names to avoid (e.g. overused fantasy-name generator output) | `check_banned_terms` |
| `use_sparingly` | array of `{term, max_per_10k_words}` | Terms that are allowed but capped at a rate per 10,000 words of draft text | `check_banned_terms` |

**Wildcard syntax:** in `banned_phrases`, `*` means "any text, including none." For
example `"It's not *, it's *"` matches `"It's not a bug, it's a feature"` and also
`"It's not, it's"`. Every other character is matched literally (case-insensitive).

```json
"voice": {
  "writing_style_file": "styles/writing/default.md",
  "tone_keywords": ["direct", "grounded", "a little dry"],
  "banned_phrases": [
    "It's not *, it's *",
    "a testament to",
    "little did they know",
    "delve into"
  ],
  "banned_names": ["Elara", "Kael", "Lyra", "Seraphina", "Aria"],
  "use_sparingly": [
    { "term": "tapestry", "max_per_10k_words": 1 },
    { "term": "—", "max_per_10k_words": 20 }
  ]
}
```

---

## `terminology`

A vocabulary map agents consult while writing so a supplement uses consistent, correct
nomenclature for its system (e.g. calling the referee a "Gamemaster" rather than a
"Game Master" or "GM," or the player's character a "Player Character" rather than a
"hero"). This is **guidance applied while drafting, not a mechanical find/replace
pass** — a blind substitution over existing prose could mangle text. You can add any
additional key/value pairs your system needs beyond the three shipped by default;
agents treat the whole map as a glossary.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `gamemaster` | string | Preferred term for the person running the game | Agent prompts |
| `player_character` | string | Preferred term for a player's character | Agent prompts |
| `supplement` | string | Preferred term for the document being written | Agent prompts |

```json
"terminology": {
  "gamemaster": "Quest Warden",
  "player_character": "Adventurer",
  "supplement": "sourcebook"
}
```

---

## `citations`

Controls how the references server recognizes, validates, and formats citations to
source books.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `book_map` | object, alias → canonical title | Maps lowercase abbreviations/aliases found in citation text to their full canonical book title | References server (`search_references`, `standardize_citation`, `validate_citation_format`) |
| `patterns` | array of regex strings | Python regexes (with named groups `book` and `page`) used to extract `Book, p. N`-style citations from prose | References server (`extract_citations`, `extract_citations_from_file`) |
| `bibliography` | object, alias → full citation | Maps the same aliases to a formatted bibliography entry | References server (`create_bibliography`, `generate_citation_report`) |

An **empty `book_map`** (the shipped default) is a valid, supported state: the generic
`Title, p. N` pattern in `patterns` still works as a built-in fallback, but tools that
need a configured book map (validation, bibliography generation) return a "no book map
configured" guidance message instead of silently doing nothing or erroring.

```json
"citations": {
  "book_map": {
    "eqc": "Example Quest Core Rulebook",
    "eqb": "Example Quest Bestiary"
  },
  "patterns": [
    "(?P<book>[A-Z][\\w :']+?),?\\s*p\\.\\s*(?P<page>\\d+)"
  ],
  "bibliography": {
    "eqc": "Example Quest Core Rulebook. Example Games Press, 2024.",
    "eqb": "Example Quest Bestiary. Example Games Press, 2025."
  }
}
```

---

## `mechanics`

Parameters for the mechanics server's dice-pool math and experience-point costs.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `xp_costs` | object, trait type → multiplier | Per-trait-type cost multiplier used to compute experience-point costs | Mechanics server (`calculate_experience_cost`) |
| `dice.sides` | int | Number of sides per die in the dice pool | Mechanics server (dice-pool tools) |
| `dice.default_difficulty` | int | Default target number for a success, when not specified per roll | Mechanics server |
| `dice.botch_on_ones` | bool | Whether rolling all 1s (or however the system defines it) counts as a botch | Mechanics server |

**Experience cost formula:** for a given trait type with multiplier `m`, raising the
trait from level `L-1` to level `L` costs `cost(L) = (L - 1) × m` experience points.
Raising a trait across a range sums the per-level cost for each level crossed. An
**empty `xp_costs`** (the shipped default) is valid: `calculate_experience_cost` returns
configuration guidance (how to add trait types) instead of a bogus number.

Example: with `"skill": 2`, raising a skill from 2 to 4 costs `cost(3) + cost(4) =
(3-1)×2 + (4-1)×2 = 4 + 6 = 10` XP.

```json
"mechanics": {
  "xp_costs": {
    "attribute": 4,
    "skill": 2,
    "power": 6,
    "resolve": 1
  },
  "dice": {
    "sides": 10,
    "default_difficulty": 6,
    "botch_on_ones": true
  }
}
```

---

## `art`

Image-generation backend configuration for the art server. `active_generator` selects
which entry in `generators` is used by default; each entry is a self-contained
**generator profile**.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `active_generator` | string | Key into `generators` used when no generator is explicitly requested | Art server |
| `density_words_per_illustration` | int | Target ratio of prose words to illustrations, used to plan how many images a chapter needs | Art server, `/final-draft` art-density check |
| `generators` | object, name → profile | One entry per configured image generator (see below) | Art server |

### Generator profile fields

| Field | Type | Required | Purpose |
|---|---|---|---|
| `backend` | `"a1111"` \| `"comfyui"` \| `"manual"` | yes | Which backend integration handles this profile |
| `endpoint` | string (URL) | a1111/comfyui only | Base URL of the running generator API |
| `rules_file` | string (path) | yes | Markdown file of prompting conventions for this generator/model; the art-director agent reads it before writing any image prompt |
| `workflow_file` | string (path) | comfyui only | ComfyUI workflow exported via ComfyUI's **"Save (API Format)"** menu option. Must contain the literal tokens `{PROMPT}`, `{NEGATIVE}`, `{WIDTH}`, `{HEIGHT}`, `{SEED}` somewhere in the JSON — these are substituted at generation time before the workflow is submitted |
| `style_prefix` | string | yes | Text prepended to every generated prompt (e.g. a medium/style descriptor) |
| `negative_prompt` | string | yes | Default negative prompt (a1111-style backends) |
| `sampler` | string | optional | Sampler/algorithm name passed through to the backend |
| `scheduler` | string or `null` | optional | Scheduler name passed through to the backend |
| `steps` | int | optional | Denoising steps |
| `cfg_scale` | number | optional | Classifier-free guidance scale |
| `prompt_style` | `"tags"` \| `"natural"` | optional | Whether this model expects comma-separated tags or natural-language prompts |
| `sizes` | object, preset name → `[width, height]` | optional | Named size presets (e.g. `portrait`, `landscape`, `column`, `full_page`) this profile supports |

The `manual` backend has no `endpoint`/`workflow_file` — it routes through a prompt
manifest for a human to run generation by hand, for setups with no local API.

The shipped `config/system.json` default ships two example generator profiles named
`stable-diffusion-1.5` (an `a1111`-backend profile) and `ideogram-v4` (a `comfyui`-backend
profile whose `workflow_file` points at the shipped placeholder
`styles/art/example.workflow.json` — a four-node API-format skeleton you replace with your
own workflow exported from ComfyUI via "Save (API Format)", keeping the `{PROMPT}`,
`{NEGATIVE}`, `{WIDTH}`, `{HEIGHT}`, and `{SEED}` tokens). Rename, remove, or add to these
profiles freely; the names are just map keys you choose.

Backend-specific admin tools (model listing, sampler listing, checkpoint switching,
img2img, upscale, etc.) only work against an `a1111`-backend profile; called against a
`comfyui` or `manual` profile they return a clear "requires an a1111 backend profile"
error rather than calling the wrong API.

**How to add a generator:** drop a prompting-rules markdown file in `styles/art/`
(and, for a `comfyui` backend, a workflow JSON exported from ComfyUI's "Save (API
Format)" option, also under `styles/art/`), then add an entry under `art.generators`
in `config/system.json` pointing at those files and set `art.active_generator` to its
key if you want it to be the default. No code changes required.

```json
"art": {
  "active_generator": "eq-ink",
  "density_words_per_illustration": 2250,
  "generators": {
    "eq-ink": {
      "backend": "a1111",
      "endpoint": "http://127.0.0.1:7860",
      "rules_file": "styles/art/eq-ink.md",
      "style_prefix": "black and white ink illustration, ",
      "negative_prompt": "color, photo, watermark",
      "sampler": "DPM++ 2S a",
      "scheduler": null,
      "steps": 20,
      "cfg_scale": 7.0,
      "prompt_style": "tags",
      "sizes": {
        "portrait": [512, 512],
        "landscape": [768, 512],
        "column": [384, 768],
        "full_page": [512, 768]
      }
    },
    "eq-comfy": {
      "backend": "comfyui",
      "endpoint": "http://127.0.0.1:8188",
      "rules_file": "styles/art/eq-comfy.md",
      "workflow_file": "styles/art/eq-comfy.workflow.json",
      "style_prefix": "",
      "negative_prompt": ""
    }
  }
}
```

---

## `layout`

Controls export formatting.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `style_file` | string (path) | Human-readable layout spec markdown describing page/heading conventions | `/compile`, `convert_supplements.py` |
| `docx_theme` | string | Name of a DOCX theme — resolves to `styles/layout/<name>.theme.json`, a machine-readable theme data file (colors, fonts, rules) | `export-docx.js` |

**How to add a DOCX theme:** drop a `<name>.theme.json` file in `styles/layout/`
(colors, fonts, and rule styles — see `styles/layout/default.theme.json` for the
shape) and set `layout.docx_theme` to `<name>`. No code changes required.

```json
"layout": {
  "style_file": "styles/layout/default.md",
  "docx_theme": "eq-house-theme"
}
```

---

## `knowledge_base`

Configures the on-disk knowledge base used for canon research and consistency.

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `root` | string (path) | Root directory of the knowledge base | KB server (`kb.py`) |
| `top_level_dirs` | array of strings | Suggested top-level category folders (e.g. `factions`, `places`, `mechanics`, `history`); offered as scaffolding by `/init-project` for a new project | `/init-project` |

```json
"knowledge_base": {
  "root": "knowledge_base",
  "top_level_dirs": ["factions", "places", "mechanics", "history"]
}
```

---

## `skills`

| Field | Type | Purpose | Consumer |
|---|---|---|---|
| `toolkit_skill` | string | Name of a bring-your-own Claude Code skill that provides stat-block templates, validated game data, and system-legality checks for mechanical content. Empty string means no toolkit skill is configured; content-creation agents fall back to the generic templates in `styles/templates/` | Content-creation agent prompts |

```json
"skills": {
  "toolkit_skill": "example-quest-toolkit"
}
```

---

## Full example: Example Quest RPG

A complete, fully filled `config/system.json` for the invented "Example Quest RPG",
combining every section above:

```json
{
  "system": {
    "name": "Example Quest RPG",
    "publisher_line": "A supplement for Example Quest RPG",
    "project_type": "supplement"
  },
  "voice": {
    "writing_style_file": "styles/writing/default.md",
    "tone_keywords": ["direct", "grounded", "a little dry"],
    "banned_phrases": [
      "It's not *, it's *",
      "a testament to",
      "little did they know",
      "delve into"
    ],
    "banned_names": ["Elara", "Kael", "Lyra", "Seraphina", "Aria"],
    "use_sparingly": [
      { "term": "tapestry", "max_per_10k_words": 1 },
      { "term": "—", "max_per_10k_words": 20 }
    ]
  },
  "terminology": {
    "gamemaster": "Quest Warden",
    "player_character": "Adventurer",
    "supplement": "sourcebook"
  },
  "citations": {
    "book_map": {
      "eqc": "Example Quest Core Rulebook",
      "eqb": "Example Quest Bestiary"
    },
    "patterns": [
      "(?P<book>[A-Z][\\w :']+?),?\\s*p\\.\\s*(?P<page>\\d+)"
    ],
    "bibliography": {
      "eqc": "Example Quest Core Rulebook. Example Games Press, 2024.",
      "eqb": "Example Quest Bestiary. Example Games Press, 2025."
    }
  },
  "mechanics": {
    "xp_costs": {
      "attribute": 4,
      "skill": 2,
      "power": 6,
      "resolve": 1
    },
    "dice": {
      "sides": 10,
      "default_difficulty": 6,
      "botch_on_ones": true
    }
  },
  "art": {
    "active_generator": "eq-ink",
    "density_words_per_illustration": 2250,
    "generators": {
      "eq-ink": {
        "backend": "a1111",
        "endpoint": "http://127.0.0.1:7860",
        "rules_file": "styles/art/eq-ink.md",
        "style_prefix": "black and white ink illustration, ",
        "negative_prompt": "color, photo, watermark",
        "sampler": "DPM++ 2S a",
        "scheduler": null,
        "steps": 20,
        "cfg_scale": 7.0,
        "prompt_style": "tags",
        "sizes": {
          "portrait": [512, 512],
          "landscape": [768, 512],
          "column": [384, 768],
          "full_page": [512, 768]
        }
      },
      "eq-comfy": {
        "backend": "comfyui",
        "endpoint": "http://127.0.0.1:8188",
        "rules_file": "styles/art/eq-comfy.md",
        "workflow_file": "styles/art/eq-comfy.workflow.json",
        "style_prefix": "",
        "negative_prompt": ""
      }
    }
  },
  "layout": {
    "style_file": "styles/layout/default.md",
    "docx_theme": "eq-house-theme"
  },
  "knowledge_base": {
    "root": "knowledge_base",
    "top_level_dirs": ["factions", "places", "mechanics", "history"]
  },
  "skills": {
    "toolkit_skill": "example-quest-toolkit"
  }
}
```

You do not need to specify every field shown above — `config/system.json` as shipped
contains only neutral defaults, and any field you omit falls back to that default (see
`mcp_servers/_lib/config.py`'s `DEFAULTS`).
