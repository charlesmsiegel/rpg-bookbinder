# RPG Supplement Creation - Three-Draft Agent Workflow

## Overview

This system uses a **three-draft iterative process** where each chapter evolves from initial creation through architectural enhancement to final polish. The Project Architect plays a central role in commenting on and improving content coherence across all drafts.

---

## Phase 0: Project Initialization

### Step 0: Project Title Selection & Structure Creation

**Project Architect Agent** begins by:

1. **Title Selection**: Prompt user for project title (e.g., "your-project", or any descriptive working title for the supplement)
2. **Directory Creation**: Generate project directory structure under `projects/[sanitized-project-title]/`
3. **State Initialization**: Create project-specific state files:
   - `projects/[PROJECT_TITLE]/state/project_state.json`
   - `projects/[PROJECT_TITLE]/state/todo_list.json` 
   - `projects/[PROJECT_TITLE]/state/messages.json`
4. **Directory Structure Setup**: Create all necessary subdirectories with draft structure:
   - `content/chapter_XX/` (with draft_01.md, draft_02.md, final_draft.md placeholders)
   - `development/` (outlines, concepts, reviews)
   - `notes/` (agent working notes)
   - `output/` (compiled results)

---

## Phase 1: Project Planning & Foundation

### Step 1: Project-Specific Planning

**Project Architect Agent** continues with project-specific setup:

- Define supplement scope, theme, and target length
- Create section outline with word count targets
- Set design principles and style guidelines
- Create project timeline and milestones
- Save all planning documents to `projects/[PROJECT_TITLE]/development/outlines/`

### Step 2: Reference Foundation

**Reference Librarian Agent**:

- Access shared `references/` directory for relevant source material
- Create project-specific reference notes in `projects/[PROJECT_TITLE]/notes/reference_notes/`
- Identify relevant canon material for this project's theme
- Flag areas requiring special attention for canon consistency
- Create project-specific citation guidelines

**Output**: Project-specific plan + Reference notes ready for first draft creation

---

## Phase 2: First Draft Creation

### Step 3: Initial Content Generation (Parallel)

**Mechanics Designer Agent** creates:

- Rules sections, stat blocks, mechanical systems in `projects/[PROJECT_TITLE]/content/chapter_XX/draft_01.md`
- Game balance calculations and playtesting notes in `projects/[PROJECT_TITLE]/notes/mechanics_notes/`
- Cross-references with Reference Librarian for precedents

**Lore Writer Agent** creates:

- Setting descriptions, narrative content, flavor text in `projects/[PROJECT_TITLE]/content/chapter_XX/draft_01.md`
- NPCs, locations, factions, and story elements
- Project-specific lore notes in `projects/[PROJECT_TITLE]/notes/lore_notes/`
- Cross-references with Reference Librarian for canon consistency

**Coordination**: Both agents communicate through project-specific state files about:

- Shared elements (NPCs that need stats, locations that affect mechanics)
- Potential overlaps or dependencies stored in `projects/[PROJECT_TITLE]/state/messages.json`
- Timeline coordination tracked in `projects/[PROJECT_TITLE]/state/project_state.json`

**Output**: Complete first draft of all chapters in `draft_01.md` files

---

## Phase 3: Architectural Review & Research Enhancement

### Step 4: Architectural Commentary

**Project Architect Agent**:

- Reviews all `draft_01.md` files across the project
- Adds improvement comments **directly within the text** using comment syntax:
  ```markdown
  <!-- ARCHITECT COMMENT: This section needs better flow between paragraphs. 
  Consider adding a transition that connects the mechanical explanation 
  to the narrative example. Also suggest expanding on the thematic implications. -->
  ```
- Focus areas for comments:
  - Content flow and logical progression
  - Coherence between mechanical and narrative elements
  - Thematic consistency across sections
  - Areas needing expansion or clarification
  - Cross-references and internal consistency
- Creates summary of key improvement areas in `projects/[PROJECT_TITLE]/development/review_feedback/architect_comments_summary.md`

### Step 5: Research Enhancement

**Reference Librarian Agent**:

- Reviews Project Architect's comments across all drafts
- Conducts targeted research based on specific improvement suggestions
- Gathers additional canon material, precedents, and examples
- Creates research supplements in `projects/[PROJECT_TITLE]/notes/reference_notes/enhancement_research.md`
- Validates suggested changes against the source material in `references/` (see `references/README.md` for the precedence hierarchy)

**Output**: First drafts with architectural comments + targeted research materials

---

## Phase 4: Second Draft Integration

### Step 6: Content Integration & Enhancement

**Mechanics Designer Agent** and **Lore Writer Agent** working together:

- Read and analyze all Project Architect comments in their respective sections
- Integrate research materials provided by Reference Librarian
- Create enhanced `draft_02.md` files that:
  - Address all architectural comments
  - Incorporate research findings
  - Improve flow and coherence as suggested
  - Maintain original content strengths while fixing identified issues
- Remove architect comments once addressed, replacing with improved content
- Cross-coordinate on shared elements and dependencies

### Step 7: Copy Editing Pass

**Copy Editor Agent**:

- Reviews all `draft_02.md` files for prose quality and the voice defined in `voice.writing_style_file` and `voice.tone_keywords`
- Ensures consistent style throughout the project
- Checks grammar, clarity, and readability improvements
- Validates RPG writing conventions and terminology
- Maintains focus on engagement and accessibility
- Creates polished prose while preserving content improvements

**Output**: Enhanced second drafts with improved coherence and professional polish

---

## Phase 5: Final Draft Refinement

### Step 8: Collaborative Final Review

**Project Architect Agent** and **Final Reviewer Agent** working together:

- Comprehensive review of all `draft_02.md` files
- Project Architect focuses on:
  - Overall project coherence and flow
  - Strategic content alignment with original goals
  - Cross-section consistency and references
- Final Reviewer focuses on:
  - Publication readiness standards
  - Professional quality validation
  - Completeness against project requirements
- Both agents collaborate to create `final_draft.md` files with:
  - Any final refinements needed
  - Professional formatting and presentation
  - Complete cross-references and citations

### Step 9: Final Integration & Art Direction

**Art Director Agent**:

- Reviews all `final_draft.md` files for visual content opportunities
- Sources CC0/public domain artwork fitting the project's aesthetic
- Generates custom artwork using AI tools when needed
- Places visual content in `projects/[PROJECT_TITLE]/content/art/`
- Ensures visual consistency and professional quality

**Consistency Checker Agent**:

- Final comprehensive review of all `final_draft.md` files
- Validates internal logic and cross-references within project
- Ensures no contradictions between sections
- Confirms all terminology usage is consistent
- Signs off on project-wide coherence

---

## Phase 6: Final Compilation

### Step 10: Publication Compilation

**Project Architect Agent**:

- Compiles all `final_draft.md` files into single publication-ready document
- Creates professional table of contents with navigation
- Ensures proper formatting and section breaks
- Validates all internal references and citations
- Generates final output in `projects/[PROJECT_TITLE]/output/compiled_supplement.md`
- Updates project state to completed status

**Final Reviewer Agent**:

- Validates compiled output meets all publication standards
- Confirms professional presentation and completeness
- Signs off on publication readiness
- Archives project with success metrics

---

## Draft File Management

### File Naming Convention

Each chapter follows this structure:
```
projects/[PROJECT_TITLE]/content/chapter_01/
├── draft_01.md      # Initial creation by content agents
├── draft_02.md      # Enhanced version with architect comments integrated
└── final_draft.md   # Publication-ready version after final review
```

### Comment Integration Process

1. **Comment Insertion**: Project Architect adds HTML-style comments within draft_01.md text
2. **Comment Resolution**: Content agents replace comments with improved content in draft_02.md
3. **Comment Removal**: All architectural comments are resolved and removed by final_draft.md stage

### Version Control Benefits

- **Clear Progression**: Each draft shows distinct improvement phase
- **Rollback Capability**: Previous versions preserved if needed
- **Audit Trail**: Complete history of content development
- **Parallel Development**: Multiple chapters can be at different draft stages

---

## Communication Protocols

### Message Types

- `FIRST_DRAFT_COMPLETE`: Initial content creation finished
- `ARCHITECTURAL_COMMENTS_ADDED`: Project Architect commentary complete
- `RESEARCH_ENHANCEMENT_READY`: Reference Librarian research materials prepared
- `SECOND_DRAFT_INTEGRATED`: Comments and research incorporated
- `COPY_EDITING_COMPLETE`: Prose polish finished
- `FINAL_DRAFT_APPROVED`: Publication-ready content confirmed
- `COMPILATION_READY`: All drafts ready for final output generation

### Quality Gates

1. **First Draft Gate**: All chapters have complete draft_01.md files
2. **Architectural Review Gate**: All draft_01.md files have Project Architect comments
3. **Research Gate**: Reference Librarian provides enhancement materials
4. **Integration Gate**: All draft_02.md files address architectural comments
5. **Polish Gate**: Copy Editor approves all draft_02.md prose quality
6. **Final Gate**: Final Reviewer approves all final_draft.md files
7. **Compilation Gate**: Single publication-ready output generated

### Escalation Rules

1. If architectural comments cannot be addressed → escalate to Final Reviewer + Project Architect
2. If canon conflicts emerge during integration → escalate to Reference Librarian + Project Architect
3. If quality standards cannot be met after second draft → escalate to Final Reviewer for guidance

---

## Success Criteria

**Project completion requires**:

- ✅ All chapters progress through three complete draft stages
- ✅ All Project Architect comments addressed and integrated in draft_02.md
- ✅ Reference Librarian research incorporated where applicable
- ✅ Copy Editor approval on prose quality for all final_draft.md files
- ✅ Final Reviewer sign-off on publication readiness
- ✅ Consistency Checker validation of project-wide coherence
- ✅ Art Director integration of visual content
- ✅ Single publication-ready compiled output generated
- ✅ Project state updated to completion with success metrics

**Quality Benefits**:

- 🎯 Enhanced content coherence through architectural review
- 🎯 Stronger canon integration through targeted research
- 🎯 Professional prose quality through dedicated copy editing
- 🎯 Publication-ready output through collaborative final review
- 🎯 Complete audit trail through preserved draft versions