# Initialize New Supplement Project

Start a new supplement project for the configured game system. Guide the user through project setup.

## Your Task

You are initiating **Phase 0: Project Initialization** for a new supplement.

**Project name/concept from user**: $ARGUMENTS

### Step 1: Title Selection

If the user hasn't provided a clear title, ask them for one. Then:
- Convert the title to a filesystem-safe directory name (lowercase, hyphens for spaces, no special characters)
- Confirm the directory name with the user

### Step 2: Create the Project

Do **not** hand-write the directory tree or the state files. Call the project MCP tool:

```
initialize_project(project_name="[DIR_NAME]", project_type="[TYPE]")
```

- `project_name` is the filesystem-safe directory name from Step 1.
- `project_type` comes from `config/system.json` → `system.project_type`. Read that value and pass it explicitly; if the key is absent, omit the argument and the tool falls back to the same config lookup (default `"supplement"`).
- Optional `target_length` accepts `short`, `medium`, or `long` (default `medium`).

The tool refuses to overwrite an existing project — if it reports `Project '[DIR_NAME]' already exists`, stop and confirm with the user whether they want a different name.

`initialize_project` creates, under `projects/[DIR_NAME]/`:

```
projects/[DIR_NAME]/
├── state/
│   ├── project_state.json   (project_info / progress / agents / quality_gates)
│   ├── todo_list.json       ({"project", "next_id": 1, "todos": []})
│   └── messages.json        ([])
├── content/                 (chapter_01/, chapter_02/, ... and art/ are added later,
│                             per the outline — each chapter gets draft_01.md,
│                             draft_02.md, final_draft.md)
├── development/
│   ├── outlines/
│   ├── concepts/
│   ├── review_feedback/
│   └── art_manifest.json    ({"project", "created", "images": []})
├── notes/
│   ├── mechanics_notes/
│   ├── lore_notes/
│   └── reference_notes/
└── output/
```

The initial `project_state.json` sets `project_info.current_phase` to `"planning"`, zeroes every counter under `progress`, marks all nine agents `"ready"`, and creates the five quality gates — all `false`:

`initial_draft`, `first_review`, `consistency_check`, `final_review`, `publication_ready`

Those five are the only valid gate names — `pass_quality_gate` rejects anything else, and `check_quality_gates` reports exactly these five. Use `update_project_state` / `set_project_phase` rather than editing the JSON by hand.

`art_manifest.json` is written for you as `{"project": ..., "created": ..., "images": []}` — do not create or overwrite it manually. Register artwork later via the art MCP's `update_art_manifest` (which takes a full `project_path`, e.g. `projects/[DIR_NAME]`).

### Step 3: Knowledge Base Scaffolding

Read `knowledge_base.top_level_dirs` from `config/system.json`. If the list is non-empty, check whether `knowledge_base/` already contains those directories. If any are missing, offer to scaffold them (create the missing top-level folders under `knowledge_base/`). If `top_level_dirs` is empty, skip this step — the knowledge base is allowed to grow organically with no predefined taxonomy.

### Step 4: Confirm Initialization

Report back to the user:
- Project directory created at `projects/[DIR_NAME]/`
- State files initialized by `initialize_project` (phase: `planning`, all quality gates `false`)
- Knowledge base scaffolding created (if applicable)
- Next step: run `/plan-project [DIR_NAME]` to begin planning
