# Second Draft Integration & Copy Editing

Integrate architectural feedback and research, then polish prose.

## Your Task

You are executing **Phase 4: Second Draft Integration**.

**Project identifier**: $ARGUMENTS

### Prerequisites

Read `state/project_state.json` and verify `quality_gates.architectural_review` is `true`. All `draft_01.md` files must contain architect comments.

### Step 1: Comment Resolution Protocol

Before integrating any feedback, each agent re-reads:

- `development/outlines/writing_style.md` (voice stays consistent across drafts)
- The chapter's own working notes: Mechanics Designer reads `notes/mechanics_notes/ch_XX_mechanics.md`, Lore Writer reads `notes/lore_notes/ch_XX_lore.md`
- The comment manifest and the enhancement research

Working notes are **updated** during this phase — not replaced. Append a `## Draft 02 revisions` section capturing: which design choices survived, which were reversed under architect feedback, and why. These running notes are what makes future supplements easier to write.

The **Mechanics Designer** and **Lore Writer** work on each chapter in parallel — each addresses comments in their own domain (stat blocks, rules vs. prose, NPCs, setting) — using the comment manifest for tracking:

1. Read `development/review_feedback/architect_comments_manifest.md` to get the complete list of comments
2. Read research materials from `notes/reference_notes/enhancement_research.md`
3. For EACH comment in the manifest:
   - Address the comment in `content/chapter_XX/draft_02.md` with improved content
   - Update the manifest entry with status **RESOLVED** and a one-line note describing what was done
   - If deliberately not addressing a comment, mark it **DECLINED** with a justification
4. Create `content/chapter_XX/draft_02.md` that:
   - Incorporates research findings where applicable
   - Improves flow and coherence as suggested
   - Preserves original content strengths
   - Removes ALL `<!-- ARCHITECT COMMENT -->` tags (replaced with actual improvements)

**Verification**: After all chapters are complete:
- Grep all `draft_02.md` files for `<!-- ARCHITECT COMMENT` — this MUST return zero matches
- Verify every entry in the manifest is marked RESOLVED or DECLINED — no entries may remain unmarked

When revising or adding mechanical content (stat blocks, NPCs, weapons, items), invoke the toolkit skill if `skills.toolkit_skill` is set in `config/system.json`, to ensure proper formatting and validated game data. If no toolkit skill is set, follow the templates in `styles/templates/` instead.
### Step 2: Copy Editing Pass

The **Copy Editor** reviews all `draft_02.md` files for:
- Prose quality and engagement — is it fun to read?
- Consistent voice, as defined in `voice.writing_style_file` and `voice.tone_keywords`
- Consistent style across all chapters
- Grammar, clarity, and readability
- RPG writing conventions and terminology
- Active voice and engaging presentation
- Proper use of system-specific terms (per the toolkit skill and `references/`)

### Step 3: Tool-Verified Word Count + Metadata Scan

**Word count check**: For EACH chapter's `draft_02.md`, run the MCP tool:
```
check_word_targets(file_path="content/chapter_XX/draft_02.md", target=<chapter_target>, tolerance=0.25)
```
Record results in `state/project_state.json` under `word_count_results.second_draft`.

**Metadata scan**: Grep ALL `draft_02.md` files for the following patterns — all must return zero matches:
- `<!-- ` (residual HTML comments)
- `[Note:` (editorial notes)
- `Word Count:` (word count metadata)
- `p. XX` (unresolved page placeholders)

Record scan results in `state/project_state.json` under `metadata_scan.second_draft`.

**Banned-term scan**: Run `check_banned_terms` on each revised chapter's `draft_02.md`. Violations (banned phrases, banned names, or `use_sparingly` terms over their per-10k-word threshold — all defined in `config/system.json` → `voice`) must be fixed before the gate passes. Record results in `state/project_state.json` under `banned_terms_scan.second_draft`.

### Step 4: Quality Gate - Second Draft Complete

The gate CANNOT pass if ANY of the following are true:
- Any chapter fails its word count check
- Any `draft_02.md` contains forbidden metadata patterns
- Any `draft_02.md` has unresolved `check_banned_terms` violations
- Any comment in the manifest is neither RESOLVED nor DECLINED
- Any `draft_02.md` still contains `<!-- ARCHITECT COMMENT` tags

If all checks pass, update state:
- Set `current_phase` to `"second_draft_complete"`
- Set `quality_gates.second_draft` to `true`
- Set `quality_gates.copy_edit` to `true`
- Log `SECOND_DRAFT_INTEGRATED` and `COPY_EDITING_COMPLETE` messages with check results

Tell the user: next step is `/final-draft [PROJECT_NAME]`
