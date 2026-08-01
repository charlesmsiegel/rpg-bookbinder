# Architectural Review & Research Enhancement

Project Architect reviews first drafts and Reference Librarian provides targeted research.

## Your Task

You are executing **Phase 3: Architectural Review & Research Enhancement**.

**Project identifier**: $ARGUMENTS

### Prerequisites

Read `state/project_state.json` and verify `quality_gates.first_draft` is `true`. All `draft_01.md` files must exist.

### Step 1: Architectural Commentary

The **Project Architect** reviews ALL `draft_01.md` files and adds improvement comments directly within the text using this syntax:

```markdown
<!-- ARCHITECT COMMENT: [Specific improvement suggestion here.] -->
```

Focus areas for comments:
- **Content flow**: Logical progression between sections
- **Coherence**: Mechanical and narrative elements supporting each other
- **Thematic consistency**: Tone and themes aligned across chapters
- **Gaps**: Areas needing expansion, clarification, or examples
- **Cross-references**: Internal links and consistency between chapters
- **Canon alignment**: Potential conflicts with `references/` source material

**Comment Numbering**: Number each comment sequentially across the entire project:
```markdown
<!-- ARCHITECT COMMENT [COMMENT-001]: [Specific improvement suggestion here.] -->
<!-- ARCHITECT COMMENT [COMMENT-002]: [Specific improvement suggestion here.] -->
```

**Comment Manifest**: After reviewing ALL chapters, create `development/review_feedback/architect_comments_manifest.md` with every comment listed:

```markdown
# Architect Comments Manifest

Total comments: [N]

| ID | Chapter | Line Context | Comment |
|----|---------|-------------|---------|
| COMMENT-001 | Chapter 1 | "near the opening paragraph about..." | [Full comment text] |
| COMMENT-002 | Chapter 2 | "in the NPC stat block for..." | [Full comment text] |
```

Record the total comment count in `state/project_state.json` under `architect_review.total_comments`.

Save a summary of key improvement areas to `development/review_feedback/architect_comments_summary.md`.

### Step 2: Research Enhancement

The **Reference Librarian** then:
- Reviews all architect comments across all drafts
- Conducts targeted research based on specific improvement suggestions
- Gathers additional source material, precedents, and examples from `references/`
- Creates research supplements in `notes/reference_notes/enhancement_research.md`
- Validates suggested changes against the `references/` source material

### Step 3: Quality Gate - Review Complete

Update state:
- Set `current_phase` to `"architectural_review_complete"`
- Set `quality_gates.architectural_review` to `true`
- Set `quality_gates.research_enhancement` to `true`
- Log `ARCHITECTURAL_COMMENTS_ADDED` and `RESEARCH_ENHANCEMENT_READY` messages

Tell the user: next step is `/second-draft [PROJECT_NAME]`
