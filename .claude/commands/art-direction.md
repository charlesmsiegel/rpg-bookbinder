# Art Direction

Invoke the **art-director** agent to produce artwork — or an art-prompt manifest if the art MCP server is unavailable.

## Your Task

**Project identifier**: $ARGUMENTS

### Step 1: Art Budget Calculation

1. Run `count_words_in_directory` on the project's `content/` folder to get total word count
2. List chapter directories under `content/` (exclude `art/`) — each is one chapter
3. Parse `development/outlines/npc_registry.md` to count major NPCs (those with full stat blocks, not cross-chapter-reference-only)

Compute the art budget:

- **1 cover** — the supplement's signature image
- **1 chapter opener per chapter** — full-page, placed before each chapter heading
- **1 portrait per major NPC** — portrait format
- **Content illustrations**: `ceil(total_words / art.density_words_per_illustration)` images (default density is 2,250 words per illustration — check `config/system.json` for the configured value) — alternating landscape and column formats, prioritizing locations first, then items, then scenes

Record the computed budget (counts + word ratio used) in `state/project_state.json` under `art.budget`.

### Step 2: Cover Generation (always produce a real PNG)

The cover is required in every compiled output, so it is generated before anything else and is allowed to cross modes. Pick the first path that is available:

1. **Art MCP** — if the MCP probe below succeeds and the active generator's backend (`config/system.json` → `art.generators[art.active_generator].backend`) is `a1111` or `comfyui`, generate `cover.png` via `mcp__art__generate_full_page` with the supplement's signature prompt, then proceed to Step 3.
2. **Algorithmic art** — if an `algorithmic-art` skill is available in your setup, and the MCP is unavailable or the active backend is `manual`, OR the supplement's aesthetic calls for it (geometric / generative themes: cosmic horror, sacred geometry, hard sci-fi, abstract conceptual material, etc.), invoke that skill. Design a p5.js sketch expressing the supplement's core themes (read `development/concepts/themes.md` and `development/concepts/tone.md`), render it at ≥1600×2400 portrait resolution, and save to `content/art/cover.png`. Register via `update_art_manifest` with `source="algorithmic"` and put the sketch parameters/seed in `description`. (No `algorithmic-art` skill? Fall back to `tools/generate_covers.py`, or to path 3.)
3. **Defer** — only if neither path is usable. Leave the cover as a prompt entry in `development/art_prompts.md` and record `cover.status = "deferred"` in `state/project_state.json`. This is a degraded mode; the compile step will warn loudly.

Ask the user which cover path to prefer if both MCP and algorithmic art are available — algorithmic may be a deliberate aesthetic choice for the book.

### Step 3: Mode Selection — Generation or Prompt Manifest (for non-cover images)

Before writing any image prompt, read the active generator's `rules_file` — found at `config/system.json` → `art.generators[art.active_generator].rules_file` — and follow its prompting conventions. Different generators expect fundamentally different prompt structures (natural-language sentences vs. comma-separated tags), so the rules file is the source of truth for every prompt below.

Check the active generator's `backend` (`config/system.json` → `art.generators[art.active_generator].backend`). Use `get_active_generator` to confirm which profile is currently in force, and `set_active_generator` if the project needs to switch profiles before generating:

- **`a1111` or `comfyui`** — probe the art MCP by calling `mcp__art__get_models` (or `mcp__art__get_options`). If it returns successfully, use **Generation Mode**. If the call fails (tool unavailable, connection error, server not running), fall back to **Prompt Manifest Mode**.
- **`manual`** — always use **Prompt Manifest Mode**. Do not call any art MCP tool.

#### Generation Mode (MCP available)

For every remaining image (chapter openers, portraits, content illustrations):

1. Generate via `mcp__art__txt2img` using consistent model, sampler, and base prompt style
2. Save to `content/art/[filename].png` using the conventions below
3. Register via `update_art_manifest`

Filename conventions:

- `chapter_XX_opener.png`
- `portrait_[name].png` (snake_case NPC name)
- `ch_XX_[subject].png` for content illustrations

#### Prompt Manifest Mode (MCP unavailable, or backend is `manual`)

Do NOT call any art MCP tool. Instead, produce `development/art_prompts.md` with one entry per planned image:

```markdown
## [filename.png]

- **Placement**: cover / chapter X opener / NPC portrait — [name] / content illustration near "[heading or content reference]"
- **Dimensions**: [width] × [height]
- **Generator profile**: [active generator name from `art.active_generator`]
- **Positive prompt**: [full positive prompt text]
- **Negative prompt**: [full negative prompt text]
- **Notes**: [any scene, mood, or composition notes]
```

Pull defaults from the active generator profile at `config/system.json` → `art.generators[art.active_generator]` rather than inventing them:

- **Style stem**: prepend the profile's `style_prefix` to every positive prompt
- **Dimensions**: use the profile's `sizes` map (`portrait`, `landscape`, `column`, `full_page`) for the relevant image category
- **Base negative prompt**: the profile's `negative_prompt`, plus `low quality, blurry, text, watermark, signature, deformed hands, extra limbs, modern logos` and any supplement-specific exclusions
- **Prompt structure**: follow `prompt_style` (`"tags"` or `"natural_language"`) and the conventions documented in the profile's `rules_file`

Even in manifest mode, register each planned image in `art_manifest.json` via `update_art_manifest` with:

- `source="prompt_only"` (the manifest has no `status` field — production state lives in `source`)
- `image_path` set to the intended `content/art/[filename].png` location
- A `description` that names the subject and points at the matching heading in `development/art_prompts.md`

The manifest does not store prompt text — `development/art_prompts.md` is the authoritative record of the positive/negative prompts. Together they let a later run (when MCP is available) generate every deferred image without redoing the prompt work.

### Step 4: Consistency Requirements

Across ALL images/prompts (both modes):

- Same active generator profile (`art.active_generator`)
- Same base style stem (the profile's `style_prefix`, as the opening phrase of every positive prompt)
- Same base negative prompt (the profile's `negative_prompt`)
- Same aesthetic reference (cite the project's `development/outlines/style_guide.md` if present, plus `voice.tone_keywords` from `config/system.json`)

### Step 5: Report

Update `state/project_state.json` under `art.result`:

- `mode`: `"generation"` or `"prompt_manifest"`
- `planned_count`: total images planned
- `produced_count`: images written or prompts authored
- `output_path`: `content/art/` or `development/art_prompts.md`

Tell the user:

- Which mode was used and why
- Count of images or prompts produced
- File locations
- If manifest mode: a one-line command the user can run later to generate images from the manifest (e.g., "re-run `/art-direction [PROJECT]` once the art MCP is available")
