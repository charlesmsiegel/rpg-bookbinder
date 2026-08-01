# Projects

One directory per supplement, created by `/init-project`. Structure:

    projects/<name>/
    ├── state/        project_state.json, todo_list.json, messages.json
    ├── content/      chapter_NN/draft_01.md → draft_02.md → final_draft.md; art/
    ├── development/  outlines/, concepts/, review_feedback/, art_manifest.json
    ├── notes/        agent working notes
    └── output/       compiled_supplement.md + exports

Manage state through the project MCP tools, not by editing JSON directly.
