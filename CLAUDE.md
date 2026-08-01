# Bookbinder — Multi-Agent RPG Supplement Creation System

## Project Overview

Bookbinder is a multi-agent system for producing professional-quality supplements
for a tabletop RPG. It ships no game content of its own — the game system, source
material, house voice, and art style are all configured per project (see
`config/system.json` and `config/README.md`). Five agent roles collaborate,
coordinating through file-backed state, to carry a supplement from planning through
publication.

## System Architecture

### Core Concept

- **Coordinator-based**: the project-architect agent orchestrates all other agents
- **File-based state**: per-project JSON files for coordination, no message bus
- **Tool-driven**: MCP servers handle computational tasks (word counts, dice math,
  citation extraction, art prompts) so agents spend their tokens on content, not
  arithmetic
- **Config-driven**: everything that varies by game system — voice, terminology,
  citation patterns, mechanics formulas, art backends, layout theme — lives in
  `config/system.json`, not in agent prose
- **Source-aware**: maintains consistency with the reference material you drop into
  `references/` (see `references/README.md` for the precedence hierarchy you define)

### Agent Roles

The workflow is organized around five conceptual roles. Each role is backed by one
or more agent definition files under `.claude/agents/` — 12 files total (9 in
`book-creation/`, 3 in `knowledge-base/`); an earlier plan to consolidate these into
one file per role was never carried out, so the finer-grained files are what actually
run today.

| Role | Responsibilities | Agent files |
|---|---|---|
| **Project Architect** | Strategic coordination, planning, state management, word count tracking, final compilation | `project-architect.md` |
| **Content Creator** | Rules, mechanics, stat blocks, lore, narrative content (use the configured `skills.toolkit_skill`, if any, for mechanical content — otherwise the templates in `styles/templates/`) | `mechanics-designer.md`, `lore-writer.md` |
| **Quality Reviewer** | Prose quality, consistency checking, word-count optimization, final review | `copy-editor.md`, `consistency-checker.md`, `final-reviewer.md`, `word-count-manager.md` |
| **Knowledge Librarian** | Source-material research, knowledge-base maintenance and search, citation validation | `reference-librarian.md`, `kb-organizer.md`, `kb-retriever.md`, `knowledge-parser.md` |
| **Art Director** | Visual content strategy, illustration generation across configured backends | `art-director.md` |

## Directory Structure

```text
.
├── mcp_servers/               # MCP tool servers, wired via .mcp.json (stdio)
│   ├── _lib/                  # Shared implementations (plain Python, no MCP decorators)
│   │   ├── config.py          # config/system.json loader (deep-merge over defaults)
│   │   ├── project_ops.py     # State mgmt, phases, agents, gates, messages
│   │   ├── content_ops.py     # Word counting, targets, density, compilation, TOC, banned terms
│   │   ├── mechanics_ops.py   # Dice probability, extended actions, XP, soak, random tables
│   │   ├── reference_ops.py   # Citations, validation, search, bibliography
│   │   ├── kb_ops.py          # KB search, stats, links, orphans, moves, validation
│   │   ├── art_ops.py         # Art generation, manifest, prompts
│   │   └── art_backends.py    # a1111 / comfyui / manual backend adapters
│   ├── project.py             # State/coordination server (implements its own logic; see docs/ARCHITECTURE.md)
│   ├── content.py             # Word count + compilation server (only check_banned_terms delegates to _lib/content_ops.py; other 8 tools inline)
│   ├── mechanics.py           # Dice-pool calculation server (fully delegates to _lib/mechanics_ops.py)
│   ├── references.py          # Citation server (fully delegates to _lib/reference_ops.py)
│   ├── kb.py                  # Knowledge-base server (implements its own logic; see docs/ARCHITECTURE.md)
│   ├── art.py                 # Art-generation server (implements its own logic using _lib/art_backends.py + config.py; see docs/ARCHITECTURE.md)
│   └── architect_tools.py, creator_tools.py, reviewer_tools.py, librarian_tools.py, artist_tools.py
│                                # Role-scoped wrapper servers re-exporting _lib functions; not wired into .mcp.json by default
├── config/
│   ├── system.json            # Per-game-system configuration — single source of truth
│   └── README.md              # Field-by-field reference for system.json
├── styles/                    # Bring-your-own house style
│   ├── writing/                # Voice/style guide (voice.writing_style_file)
│   ├── layout/                 # Layout spec + <name>.theme.json DOCX theme data
│   ├── templates/              # Structural blueprints per kind of book
│   └── art/                    # Per-generator prompting-rules files + ComfyUI workflows
├── references/                 # Your game system's source books (gitignored)
├── knowledge_base/             # Optional wiki of extracted setting knowledge
├── projects/                   # Individual project workspaces
│   ├── [PROJECT_TITLE_1]/      # Generated from user-chosen title
│   │   ├── state/               # Project-specific agent coordination
│   │   │   ├── project_state.json
│   │   │   ├── todo_list.json
│   │   │   └── messages.json
│   │   ├── content/              # Work in progress
│   │   │   ├── chapter_01/       # One folder per chapter
│   │   │   │   ├── draft_01.md
│   │   │   │   ├── draft_02.md
│   │   │   │   └── final_draft.md
│   │   │   ├── chapter_02/
│   │   │   └── art/              # Artwork files by chapter
│   │   ├── development/          # Project artifacts
│   │   │   ├── outlines/
│   │   │   ├── concepts/
│   │   │   ├── review_feedback/
│   │   │   └── art_manifest.json
│   │   ├── notes/                # Agent working notes
│   │   └── output/               # compiled_supplement.md + DOCX/EPUB/PDF exports
│   └── [PROJECT_TITLE_2]/        # Additional projects...
├── scripts/                    # export.sh, export-docx.js (theme-driven DOCX),
│                                #   epub.css / pdf-template.html (static EPUB/PDF stylesheets)
├── tools/                       # generate_covers.py (cover art CLI), convert_supplements.py
├── tests/                       # unittest suite covering the _lib modules
├── build_triple_spaced.py       # Builds a triple-line-spaced editing PDF; invoked by /compile
└── .claude/
    ├── agents/
    │   ├── book-creation/        # 9 agent definitions
    │   └── knowledge-base/       # 3 agent definitions
    └── commands/                 # Slash commands driving the pipeline
```

## State Coordination

Each project has three state files in `projects/[PROJECT_TITLE]/state/`:

| File | Purpose | MCP Tools |
|---|---|---|
| `project_state.json` | Phase, progress metrics, agent status, quality gates | `get_project_status`, `update_project_state`, `set_project_phase`, `mark_agent_active`, `mark_agent_complete`, `get_active_agents`, `pass_quality_gate`, `check_quality_gates` |
| `todo_list.json` | Task assignments with status, priority, and ownership | `create_todo`, `update_todo`, `list_todos`, `complete_todo` |
| `messages.json` | Agent communication log (decisions, warnings, progress) | `log_agent_message`, `get_recent_messages` |
| `development/art_manifest.json` | Art inventory with chapter, source, and license tracking | `update_art_manifest`, `list_art_manifest`, `generate_attribution` (art MCP) |

**Important**: Agents should use MCP tools to manage state — not edit JSON files directly.

**Note**: Art manifest tools (from the art MCP server) take a full `project_path` (e.g., `projects/my-project`), not just the project name.

### todo_list.json Schema

```json
{
  "project": "project-name",
  "next_id": 1,
  "todos": [
    {
      "id": 1,
      "task": "Task description",
      "status": "pending|in_progress|completed",
      "assigned_to": "agent_name",
      "priority": "high|medium|low",
      "phase": "planning|first_draft|review|second_draft|editing|final",
      "created_date": "ISO timestamp",
      "updated_date": null,
      "completed_date": null,
      "notes": ""
    }
  ]
}
```

### Agent State Workflow

1. Agent calls `mark_agent_active` → checks `list_todos` for assignments
2. Agent calls `update_todo` (status: "in_progress") → does work → calls `complete_todo`
3. Agent calls `mark_agent_complete` → logs summary via `log_agent_message`

## Slash Commands

The supplement creation workflow uses a **three-draft iterative process**. Each phase has a dedicated slash command:

| Command | Phase | What It Does |
|---|---|---|
| `/init-project [name]` | Phase 0 | Title selection, directory creation, state initialization |
| `/plan-project [name]` | Phase 1 | Chapter outline, word count targets, reference foundation |
| `/first-draft [name]` | Phase 2 | Parallel content generation (mechanics + lore) |
| `/architect-review [name]` | Phase 3 | Architectural commentary + research enhancement |
| `/second-draft [name]` | Phase 4 | Comment integration + copy editing pass |
| `/final-draft [name]` | Phase 5 | Final review, art direction, consistency validation |
| `/compile [name]` | Phase 6 | Assemble publication-ready output |

Run them in order. Each command checks the previous phase's quality gate before proceeding.
An eighth command, `/art-direction [name]`, can be run standalone at any time to
(re)generate artwork or a prompt manifest for a project.

## Draft File Convention

Each chapter progresses through three files: `draft_01.md` → `draft_02.md` → `final_draft.md`.

## Getting Started

1. Read `README.md` for the quickstart and the full "what you bring" table.
2. Edit `config/system.json` for your game system — display name, voice, terminology,
   citation patterns, mechanics formulas, art-generator profiles, layout theme. Every
   field has a neutral default; see `config/README.md` for the complete reference.
3. Drop your reference books into `references/` (gitignored — see `references/README.md`).
4. Install dependencies: `pip install "mcp<2" httpx` for the MCP servers; optional
   `npm install` for DOCX export; optional pandoc/weasyprint for EPUB/PDF.
5. Run the test suite (`python -m unittest discover tests`) to confirm the toolchain is working.
6. Start with `/init-project [name]` and proceed through the slash commands in order.

See `docs/ARCHITECTURE.md` for the agent/MCP-server design and `docs/WORKFLOW.md` for
how a project moves through the three-draft cycle.
