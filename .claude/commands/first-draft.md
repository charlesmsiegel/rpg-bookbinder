# Create First Drafts

Generate initial content for all chapters using mechanics and lore agents.

## Your Task

You are executing **Phase 2: First Draft Creation** for the supplement project.

**Project identifier**: $ARGUMENTS

### Prerequisites

Read `state/project_state.json` and verify `current_phase` is `"planning_complete"` or later. Read the supplement outline from `development/outlines/`.

**Mandatory reading before drafting anything:**

- `development/outlines/writing_style.md` — the prose voice every draft must follow
- `development/concepts/premise.md` and `development/concepts/themes.md` — the core ideas this supplement argues for
- The chapter's own brief in `development/outlines/chapter_XX_brief.md`

Every drafting agent (mechanics-designer and lore-writer) loads these before writing the first sentence of any chapter.

### Cross-Reference Rules (MANDATORY)

All content created in this phase MUST follow these rules:

1. **Internal references**: ALWAYS use `[Display Text](#heading-id)` format for cross-references within this supplement
2. **Consult the registry**: Look up valid anchor IDs in `development/outlines/heading_id_registry.md` before writing any cross-reference
3. **NEVER use `p. XX` or page numbers** for references within this supplement — page numbers do not exist in markdown output
4. **External source-book references** (e.g., "CoreBook p. 42", "Companion p. 17") remain fine and should be used for citing published source material
5. **New headings**: If you create a heading not in the registry, add it to `heading_id_registry.md` before referencing it

### Step 1: Parallel Content Generation

For each chapter, create `content/chapter_XX/draft_01.md` by running the **mechanics-designer** and **lore-writer** agents in parallel:

**Mechanics Designer** produces:
- Rules sections, stat blocks, mechanical systems in `draft_01.md`
- Cross-references with existing precedents in `references/` (coordinate with **reference-librarian**)
- **Working notes in `notes/mechanics_notes/`** — one file per chapter (e.g., `ch_01_mechanics.md`) capturing:
  - Balance calculations for new powers, traits, or items (dice math via `calculate_dice_probability`/`calculate_extended_action`, XP cost derivation via `calculate_experience_cost`)
  - System-interaction rationale and edge cases considered
  - Design intent: what the mechanic is for and what it deliberately excludes
  - Cut options and why they were rejected
  - Open questions or playtesting flags

**Lore Writer** produces:
- Setting descriptions, narrative content, flavor text in `draft_01.md`
- NPCs, locations, factions, story elements
- Cross-references with existing source material in `references/` (coordinate with **reference-librarian**)
- **Working notes in `notes/lore_notes/`** — one file per chapter (e.g., `ch_01_lore.md`) capturing:
  - Character arc and motivation sketches that informed NPC writing
  - Paradigm / worldview exploration behind each faction or concept
  - Tone and voice experiments, alternate phrasings considered
  - Setting deep-dives that didn't fit in the chapter but inform consistency
  - Story seeds / hooks cut from `draft_01.md` but worth keeping for future use

These notes are required — they feed the second-draft revision and future supplements. At least one file in each directory is a gate requirement in Step 4.

Both agents write into the same `draft_01.md` and coordinate on shared elements (NPCs that need stats, locations that affect mechanics) via `state/messages.json`.

**Toolkit skill for mechanical content.** If `skills.toolkit_skill` is set in `config/system.json`, invoke that skill for stat blocks and mechanical content — characters, NPCs, weapons, powers, items, or any content requiring game statistics. It provides standardized templates, validated data lookups, and checklist-based creation for the configured system's mechanical elements. If no toolkit skill is set, follow the templates in `styles/templates/` instead.

### Step 2: NPC Registry Compliance

Before writing any stat block or character profile:

1. **Check `development/outlines/npc_registry.md`** — if the NPC already has a registry entry, use those exact values
2. **New NPCs**: Add the NPC to the registry FIRST, then write the stat block using registry values
3. **Quick Reference entries**: Must pull all numerical values directly from the registry — never approximate
4. **Do not invent or guess numbers** for NPCs whose full profile lives in another chapter; use the registry values or leave a `<!-- TODO: pull from registry -->` that will be caught in validation
5. **Cross-chapter NPCs**: When an NPC appears in multiple chapters, only ONE chapter contains the full profile; all others reference the registry

### Step 3: Tool-Verified Word Count Check

For EACH chapter's `draft_01.md`, run the MCP tool:

```
check_word_targets(file_path="content/chapter_XX/draft_01.md", target=<chapter_target>, tolerance=0.25)
```

- Record each tool's output (pass/fail, actual count, target, percentage) in `state/project_state.json` under `word_count_results.first_draft`
- If any chapter fails: flag it for expansion or trimming before proceeding
- Do NOT manually estimate word counts — tool output is the only accepted evidence

### Step 4: Quality Gate - First Draft Complete

Verify ALL of the following before the gate can pass:

1. All chapters have complete `draft_01.md` files
2. All `check_word_targets` results are recorded in project_state.json
3. No chapter has a word count failure that has not been addressed
4. `notes/mechanics_notes/` contains at least one note file per chapter that has mechanical content (stat blocks, signature powers, rules)
5. `notes/lore_notes/` contains at least one note file per chapter that has narrative content (NPCs, setting, flavor)

Update state:
- Set `current_phase` to `"first_draft_complete"`
- Set `quality_gates.first_draft` to `true`
- Log `FIRST_DRAFT_COMPLETE` message with summary of word count results

The gate CANNOT pass if any chapter still fails its word count check.

Tell the user: next step is `/architect-review [PROJECT_NAME]`
