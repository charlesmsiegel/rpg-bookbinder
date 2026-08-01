# Bookbinder

Bookbinder is a multi-agent pipeline for [Claude Code](https://claude.com/claude-code) that turns a game system, a house style, and a pile of reference material into a publication-ready RPG supplement. A five-agent team — project architect, content creator, quality reviewer, knowledge librarian, and art director — carries each chapter through a three-draft workflow (first draft → architectural review → second draft → final draft), coordinating through file-backed MCP state instead of a shared prompt or a message bus. Compiled output exports to DOCX, EPUB, and PDF.

**Bookbinder ships no game content. You bring your system.**

## What you bring

Bookbinder is a skeleton. Everything that makes a supplement belong to *your* game — the rules text, the voice, the look — is a slot you fill in.

| You bring | Goes in | Notes |
|---|---|---|
| Reference books | `references/` | Gitignored. Your own licensed copies. See `references/README.md`. |
| Game-mechanics skill | `skills.toolkit_skill` in `config/system.json` | A bring-your-own Claude Code skill supplying stat-block templates, validated game data, and system-legality checks (e.g. power-limit or resource-cost validation). Skeleton documented in `docs/ARCHITECTURE.md`. Leave empty and agents fall back to whatever structural blueprints you place in `styles/templates/` (which ships with only a README describing the format). |
| Writing voice | `styles/writing/` + `voice.writing_style_file` | House style guide the writing/editing agents read before drafting; also drives the `check_banned_terms` tool. |
| Book templates | `styles/templates/` | Structural blueprints per kind of book (chapter lists, word-count targets, required elements). |
| Layout theme | `styles/layout/<name>.md` + `<name>.theme.json` + `layout.docx_theme` | Human-readable layout spec plus a machine-readable DOCX theme (colors, fonts, rule styles). |
| Image-generator profiles | `styles/art/<gen>.md` rules file (+ ComfyUI workflow for `comfyui` backends) + an `art.generators` entry | One profile per image generator; `art.active_generator` picks the default. |
| *(optional)* `algorithmic-art` skill | Your Claude Code skill set | If installed, the art director can render a procedural p5.js cover instead of a diffusion-model one. Without it, covers fall back to `tools/generate_covers.py` or stay as an entry in the prompt manifest. |
| Config | `config/system.json` | Single source of truth for all of the above plus terminology, citation patterns, and mechanics formulas. See `config/README.md` for the full field reference. |

Every field in `config/system.json` has a built-in neutral default — a missing file, section, or field falls back safely, so you only write the keys you want to change.

## Environment

- **Claude Code** — CLI or desktop.
- **[superpowers plugin](https://github.com/obra/superpowers)** — recommended, not required. It provides the brainstorm → spec → plan flow used when designing a new book from scratch. The eight slash commands that drive the pipeline itself run without it.
- **Python 3.11+** with `pip install "mcp<2" httpx` — the MCP servers use the `mcp` SDK's 1.x API (`mcp.server.fastmcp`); `mcp` 2.0 restructures this under a separate `fastmcp` package, so the version pin matters.
- **Optional export dependencies** (only needed for the formats you use): Node.js + `npm install` (DOCX export, via the `docx` package), [pandoc](https://pandoc.org/) (EPUB/PDF), [weasyprint](https://weasyprint.org/) (PDF), `python-docx`, `Pillow`, `numpy` (algorithmic cover generation).
- **Optional local image generation** via [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui) (`a1111` backend) or [ComfyUI](https://github.com/comfyanonymous/ComfyUI) (`comfyui` backend) — each generator profile in `config/system.json` points at its own endpoint URL and port. Without a running generator, the `manual` backend produces a prompt manifest (`development/art_prompts.md`) for you to run by hand. ComfyUI workflows are exported via **"Save (API Format)"** and must contain the literal tokens `{PROMPT}`, `{NEGATIVE}`, `{WIDTH}`, `{HEIGHT}`, `{SEED}`; see `styles/art/example.workflow.json`.

## Quickstart

1. Clone the repo.
2. Edit `config/system.json` for your game system (see `config/README.md`).
3. Drop your reference books into `references/`.
4. Run the tests to confirm the toolchain works: `python -m unittest discover tests`.
5. Run the pipeline, in order:

| Command | Phase | What It Does |
|---|---|---|
| `/init-project [name]` | Phase 0 | Title selection, directory creation, state initialization |
| `/plan-project [name]` | Phase 1 | Chapter outline, word count targets, reference foundation |
| `/first-draft [name]` | Phase 2 | Parallel content generation (mechanics + lore) |
| `/architect-review [name]` | Phase 3 | Architectural commentary + research enhancement |
| `/second-draft [name]` | Phase 4 | Comment integration + copy editing pass |
| `/final-draft [name]` | Phase 5 | Final review, art direction, consistency validation |
| `/compile [name]` | Phase 6 | Assemble publication-ready output |

Each command checks the previous phase's quality gate before proceeding. (An eighth command, `/art-direction [name]`, can be run standalone to (re)generate artwork or a prompt manifest for a project.)

## Architecture

Bookbinder is coordinator-based: the project-architect agent orchestrates the other four agents, all state lives in per-project JSON files rather than a shared prompt, and computational work (word counts, dice math, citation extraction, art prompts) is handled by Python MCP tools so agents spend their tokens on content, not arithmetic. See `docs/ARCHITECTURE.md` for the full agent and tool breakdown, and `docs/WORKFLOW.md` for how a project moves through the three-draft cycle.

Each project keeps four state files under `projects/<name>/`:

| File | Purpose |
|---|---|
| `state/project_state.json` | Phase, progress metrics, agent status, quality gates |
| `state/todo_list.json` | Task assignments with status, priority, and ownership |
| `state/messages.json` | Agent communication log (decisions, warnings, progress) |
| `development/art_manifest.json` | Art inventory with chapter, source, and license tracking |

## License & IP

MIT. This repository contains no third-party game content. Reference materials you add stay local (`references/` is gitignored) and are your responsibility to license. Knowledge-base or project content you derive from published books should not be pushed to public forks.
