# Final Draft Refinement

Collaborative final review, art direction, and consistency validation.

## Your Task

You are executing **Phase 5: Final Draft Refinement**.

**Project identifier**: $ARGUMENTS

### Prerequisites

Read `state/project_state.json` and verify `quality_gates.copy_edit` is `true`.

### Step 1: Final Draft Transformation Checklist

For EACH chapter, create `content/chapter_XX/final_draft.md` from `draft_02.md` by performing ALL of the following transformations:

**1. Metadata Stripping**
- Remove ALL `<!-- -->` HTML comments (no exceptions)
- Remove ALL `[Note:]` or `[Note:` tags
- Remove ALL `Word Count:` lines
- Remove ALL `**End of Chapter**` markers
- Remove ALL `Draft Notes:` sections

**2. Cross-Reference Resolution**
- Replace every `see Chapter X` or `(Chapter X)` with a proper heading link: `[Display Text](#heading-id)`
- Consult `development/outlines/heading_id_registry.md` for valid anchor IDs
- Replace any surviving `p. XX` or `page XX` placeholders with correct heading links
- External source-book references (e.g., "CoreBook p. 42") remain unchanged

**3. NPC Registry Reconciliation**
- Read `development/outlines/npc_registry.md`
- For every NPC mentioned in this chapter, verify ALL numerical values (power ratings, Attributes, Abilities, and other system-specific stats) match the registry exactly
- Fix any discrepancies by using the registry values (the registry is authoritative)

**4. Quick Reference Alignment**
- If the chapter contains a Quick Reference table, verify every entry matches the full stat block in the chapter
- Both the QR table and the full stat block must use registry values
- Flag and fix any mismatches

**5. Prose Polish**
- Tighten chapter openings — no throat-clearing
- Remove redundant cross-chapter explanations (e.g., re-explaining what was already covered in another chapter)
- Standardize sidebar and stat block formatting across all chapters
- Ensure professional presentation matching published supplement quality for this game line

### Step 2: Art Direction

Run `/art-direction [PROJECT_NAME]` to invoke the **art-director** agent.

That command handles art budget calculation (density: 1 content illustration per `art.density_words_per_illustration` words, default 2,250 — not per 1,000). The `a1111`/`comfyui` backends generate images via the art MCP; the `manual` backend produces a prompt manifest (`development/art_prompts.md`) instead. All results are registered in `development/art_manifest.json`.

The final-draft gate does NOT require images to exist — a prompt manifest is an acceptable art deliverable. The compilation step (`/compile`) will embed images if they exist and otherwise skip image references gracefully.

### Step 3: Pre-Compilation Validation Sweep

ALL of the following checks must pass before the quality gate. Record every result in `state/project_state.json` under `validation.final_draft`.

**1. Forbidden Pattern Scan**
- Read `development/outlines/forbidden_patterns.md` for the list of banned patterns
- Grep ALL `final_draft.md` files for every pattern in the list
- **Zero tolerance**: any match is an automatic failure
- Record: pattern, file, line number for any matches found

**2. Word Count Validation**
- Call `check_word_targets` on every `final_draft.md`
- Record pass/fail for each chapter

**3. NPC Registry Cross-Check**
- For every NPC in `development/outlines/npc_registry.md`, verify numerical values match across ALL files that reference that NPC
- Report any discrepancies as Critical errors

**4. Heading Link Integrity**
- Extract all `](#...)` references from every `final_draft.md`
- Verify each target heading actually exists in the supplement (check `heading_id_registry.md` and grep actual headings)
- Report any broken links

**5. Diff Verification**
- For EVERY chapter, confirm that `final_draft.md` differs from `draft_02.md`
- Identical files = automatic failure (indicates the final draft transformation was skipped)
- Record which chapters pass/fail the diff check

**6. Banned-term scan**
- Run `check_banned_terms` on every `final_draft.md`
- Violations (banned phrases, banned names, or `use_sparingly` terms over their per-10k-word threshold — all defined in `config/system.json` → `voice`) must be fixed before the gate passes
- Record results per chapter

### Step 4: Quality Gate - Final Draft Approved

The gate CANNOT pass if ANY validation check in Step 3 failed. Specifically:
- Any forbidden pattern match → gate fails
- Any chapter fails word count → gate fails
- Any NPC registry discrepancy → gate fails
- Any broken heading link → gate fails
- Any chapter where final_draft.md == draft_02.md → gate fails
- Any chapter with unresolved `check_banned_terms` violations → gate fails

If ALL checks pass, update state:
- Set `current_phase` to `"final_draft_complete"`
- Set `quality_gates.final_draft` to `true`
- Log `FINAL_DRAFT_APPROVED` message with summary of all validation results

Tell the user: next step is `/compile [PROJECT_NAME]`
