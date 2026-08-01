# Plan Supplement Structure

Design the supplement structure, chapter outline, and word count targets.

## Your Task

You are executing **Phase 1: Project Planning & Foundation** for the supplement project.

**Project identifier**: $ARGUMENTS

### Step 1: Locate the Project

Find the project directory under `projects/`. Read `state/project_state.json` to understand current status. If the project doesn't exist, tell the user to run `/init-project` first.

### Step 2: Writing Style Selection

Pick the **writing style** (prose voice) that will guide all drafting. Layout style is chosen later at compile time — this step is only about voice.

Offer the user three paths and ask which they prefer:

**Path A — Pick an existing writing style**

1. List all `.md` files in `styles/writing/`
2. For each, show filename and first heading line
3. User picks one
4. Copy or reference-link the chosen style to `development/outlines/writing_style.md`

**Path B — Describe the desired voice**

The user writes a short free-form description ("terse, sardonic, in-world narrator" / "warm and discursive like a tutor"). Turn the description into a short `development/outlines/writing_style.md` with headings: Voice, Register, POV, Humor, Hedging, Sample Cadence.

**Path C — Answer guided questions**

Ask these one at a time or as a numbered list; the user can skip any. From their answers, write `development/outlines/writing_style.md` with the same heading structure as Path B.

1. **Register**: academic / literary / conversational / dramatic / pulp / other?
2. **POV**: third-person omniscient in-world narrator / designer addressing reader / mixed / first-person character voice?
3. **Humor**: none / dry understatement / overt / ironic / deadpan?
4. **Sentence length**: short declarative / varied / long literary?
5. **Hedging**: confident and direct / cautiously qualified / explicitly opinionated?
6. **Politics & ethics**: embedded in fiction / explicit authorial stance / avoided?
7. **Do you want to imitate a specific published author?** (name or pasted sample — optional)
8. **Words or mannerisms to avoid?** ("intricate," em-dash drama, purple prose, etc.)

Regardless of path, the output is a single file at `development/outlines/writing_style.md` that every drafting agent in later phases must read and follow. Record the path taken in `state/project_state.json` under `writing_style.source` (one of `"picked"`, `"described"`, `"questionnaire"`) and the filename if picked.

### Step 3: Supplement Structure

Using the **project-architect** agent's expertise, create a chapter outline. Save it to `development/outlines/supplement_outline.md` with:

- Chapter titles and descriptions
- Section breakdowns within each chapter
- Logical flow and narrative arc
- Estimated word counts per section

Check `styles/templates/` for a book template matching this supplement's kind (e.g. a faction book, location book, or genre anthology). If a matching template exists, follow its structure — chapter list, expected word counts per section, and required elements. Otherwise, follow standard supplement conventions:
- Introduction / "What Is This Book?"
- Core content chapters (setting, mechanics, characters)
- Gamemaster resources chapter
- Appendices (quick reference, index)

### Step 4: Word Count Strategy

Set word count targets in `state/project_state.json`. Use ±25% tolerance. Typical supplement ranges:
- Short supplement: 30,000-50,000 words
- Standard supplement: 50,000-80,000 words
- Major supplement: 80,000-120,000 words

### Step 5: Reference Foundation

Use the **reference-librarian** agent to:
- Identify relevant source material by consulting `references/` per the hierarchy documented in `references/README.md`
- Create initial reference notes in `notes/reference_notes/`
- Flag source-sensitive areas that need special attention
- Document the reference hierarchy for this project's themes

### Step 6: Concept Exploration

Before locking content briefs, explore the supplement's core ideas in `development/concepts/`. These are short working docs that capture the thinking behind the book — material that would otherwise live only in the conversation and be lost.

Create at minimum:

- `development/concepts/premise.md` — the one-paragraph core pitch, then a longer riff: what is this book really about, what question is it trying to answer, and what does it argue that existing material in `references/` doesn't?
- `development/concepts/themes.md` — the emotional/thematic spine (2–5 themes), each with a one-sentence statement and a short note on how it will show up mechanically and narratively
- `development/concepts/paradigm.md` (for faction/culture/organization books) — worldview exploration of the featured group: their metaphysics, their blind spots, their internal conflicts
- `development/concepts/tone.md` — mood/vibe reference: comparable works, atmospheric touchstones, what the reader should feel

Optionally, add further concept files as the project demands (e.g., `development/concepts/setting.md`, `development/concepts/antagonist.md`).

These documents are read by all drafting agents in later phases alongside the writing style guide and chapter briefs. They are NOT part of the final supplement — they're the thinking that produces it. This is a gate requirement: Step 9 cannot complete unless `development/concepts/` contains at least `premise.md` and `themes.md`.

### Step 7: Create Content Briefs

For each chapter, create a brief in `development/outlines/` covering:
- Chapter goals and key content
- Required system-specific mechanics (per the toolkit skill and `references/`)
- Source references to incorporate
- Design principles specific to this chapter
- **Link to the relevant concept files in `development/concepts/`** so drafting agents can trace the chapter back to its core ideas

### Step 8: Pipeline Artifacts

Create three artifacts that enforce consistency across the entire draft pipeline:

**a) Heading ID Registry** — `development/outlines/heading_id_registry.md`

For every heading in the supplement outline, record its markdown anchor ID. This is the canonical lookup for all internal cross-references.

Format:
```markdown
| Chapter | Heading | Anchor ID |
|---------|---------|-----------|
| Chapter 1 | Introduction | `#introduction` |
| Chapter 1 | What Is This Book? | `#what-is-this-book` |
| Chapter 2 | The Inner Circle | `#the-inner-circle` |
```

Rules:
- Anchor IDs follow standard markdown rules: lowercase, spaces become hyphens, punctuation removed
- Every heading from the outline must have an entry
- New headings added during drafting must be added here first
- All internal cross-references in the supplement MUST use IDs from this registry

**b) NPC & Entity Registry** — `development/outlines/npc_registry.md`

For every named NPC, location, or item that appears in 2+ chapters, create a canonical entry. This is the single source of truth for all numerical values.

Format:
```markdown
## [NPC Name]

- **Canonical Stats**: [Key power ratings, Attributes/Abilities, and other system-specific values]
- **Chapter of Full Profile**: Chapter X
- **Chapters That Reference**: Chapters X, Y, Z
- **Notes**: [Any important details about this entity]
```

Rules:
- Any NPC with a stat block must have a registry entry
- All chapters referencing this NPC must use registry values — no approximations
- Changes to stats require updating the registry FIRST, then all references
- Quick Reference table entries must match registry values exactly

**c) Forbidden Patterns List** — `development/outlines/forbidden_patterns.md`

Canonical list of patterns that must never appear in final output. Used by validation sweeps in later phases.

```markdown
# Forbidden Patterns

The following patterns must not appear in any `final_draft.md` or compiled output.
Validation sweeps will grep for each pattern and reject files containing them.

## Draft Metadata
- `<!-- ` (HTML comments — all must be stripped before final)
- `[Note:` (inline editorial notes)
- `Draft Notes:`
- `Word Count:`
- `**End of Chapter`

## Unresolved Placeholders
- `p. XX`
- `page XX`
- `TODO`
- `FIXME`
- `TBD`
- `PLACEHOLDER`

## Review Artifacts
- `ARCHITECT COMMENT`
```

### Step 9: Update Project State

Update `state/project_state.json`:
- Set `current_phase` to `"planning_complete"`
- Set `current_step` to `1`
- Populate `chapters` array with chapter metadata
- Populate `word_count_targets`

Tell the user: next step is `/first-draft [PROJECT_NAME]`
