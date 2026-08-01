# Architecture: Subagents + MCP Servers

How Bookbinder is put together: the per-agent-role MCP server pattern, the shared
`_lib/` library, and the agent hierarchy that drives the pipeline.

---

## Design Principles

1. **One MCP server per domain** — each server exposes a focused set of tools; agents
   only see the servers relevant to their role
2. **Shared library, no duplication where possible** — logic for the actively-used
   servers lives in `mcp_servers/_lib/`, with the server file itself as a thin
   FastMCP wrapper
3. **Five roles, twelve agent files** — the roles are consolidated conceptually, but
   each role's responsibilities are still split across separate agent definition
   files (see below); nothing currently merges them into one file per role
4. **Config-driven, not agent-prose-driven** — voice, terminology, citation patterns,
   mechanics formulas, and art backends live in `config/system.json`, not hardcoded
   in agent instructions
5. **Local execution** — every server runs over stdio, launched by Claude Code via
   `.mcp.json`
6. **Slash commands drive workflow** — `/init-project` through `/compile`, plus the
   standalone `/art-direction`

---

## Architecture Overview

```
User
  │
  ├─ /init-project ──┐
  ├─ /plan-project ──┤
  ├─ /first-draft ───┤
  ├─ /architect-review┤    ┌──────────────────────────────────────┐
  ├─ /second-draft ──┼───▶│  Project Architect (coordinator)     │
  ├─ /final-draft ───┤    │  Orchestrates phase, delegates work  │
  └─ /compile ───────┘    └────────┬───────────────────────────────┘
                                   │ spawns subagents per phase
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
             ┌────────────┐ ┌──────────┐ ┌─────────────┐
             │ Content     │ │ Quality  │ │ Knowledge   │
             │ Creator     │ │ Reviewer │ │ Librarian   │
             │ (mechanics  │ │ (copy,   │ │ (reference, │
             │  + lore)    │ │ consist, │ │  kb search, │
             │             │ │ final)   │ │  parsing)   │
             └──────┬──────┘ └────┬─────┘ └──────┬──────┘
                    │             │               │
         ┌──────────┴─────────────┴───────────────┴──────────┐
         │                  MCP Tool Servers                   │
         │  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐│
         │  │ project  │ │ content │ │mechanics │ │  art   ││
         │  │ state    │ │ & word  │ │ calc     │ │ gen    ││
         │  │ coord    │ │ count   │ │ engine   │ │ (a1111/││
         │  │          │ │         │ │          │ │comfyui)││
         │  └──────────┘ └─────────┘ └──────────┘ └────────┘│
         │  ┌──────────┐ ┌─────────┐                         │
         │  │references│ │   kb    │                         │
         │  │ citation │ │ search  │                         │
         │  │ mgmt     │ │ & org   │                         │
         │  └──────────┘ └─────────┘                         │
         └───────────────────────────────────────────────────┘
```

---

## Agent Hierarchy: 5 Roles, 12 Files

The system organizes agents around five conceptual roles. Each role's work is split
across one or more agent definition files under `.claude/agents/` — 12 files total.
An earlier plan considered collapsing each role into a single file, but that
consolidation was never carried out; the finer-grained files below are what actually
runs.

| # | Role | Agent files | Purpose |
|---|------|--------------|---------|
| 1 | **project-architect** | `book-creation/project-architect.md` | Coordination, planning, state management, word-count tracking, compilation |
| 2 | **content-creator** | `book-creation/mechanics-designer.md`, `book-creation/lore-writer.md` | All content generation — mechanics, stat blocks, lore, narrative |
| 3 | **quality-reviewer** | `book-creation/copy-editor.md`, `book-creation/consistency-checker.md`, `book-creation/final-reviewer.md`, `book-creation/word-count-manager.md` | Prose quality, internal consistency, length management, publication readiness |
| 4 | **knowledge-librarian** | `book-creation/reference-librarian.md`, `knowledge-base/kb-organizer.md`, `knowledge-base/kb-retriever.md`, `knowledge-base/knowledge-parser.md` | Source research, citation management, knowledge-base search and maintenance |
| 5 | **art-director** | `book-creation/art-director.md` | Visual content strategy and generation |

Each slash command spawns the role(s) relevant to its phase; a role backed by
multiple files is invoked one file at a time as the specific sub-task requires (e.g.
`/first-draft` spawns `mechanics-designer` and `lore-writer` in parallel rather than
a single merged "content-creator" agent).

---

## MCP Server Architecture

### File Layout

```
mcp_servers/
├── _lib/                    # Shared implementations (plain Python, no MCP decorators)
│   ├── __init__.py
│   ├── config.py            # config/system.json loader: DEFAULTS + deep merge + caching
│   ├── project_ops.py       # State mgmt, phases, agents, gates, messages
│   ├── content_ops.py       # Word counting, targets, density, compilation, TOC, banned terms
│   ├── mechanics_ops.py     # Dice probability, extended actions, XP costs, soak, random tables
│   ├── reference_ops.py     # Citations, validation, search, bibliography
│   ├── kb_ops.py            # KB search, stats, links, orphans, moves, validation
│   ├── art_ops.py           # Art generation, manifest, prompt building
│   └── art_backends.py      # a1111 / comfyui / manual backend adapters
├── project.py                # State/coordination server
├── content.py                 # Word count + compilation server
├── mechanics.py                # Dice-pool calculation server
├── references.py               # Citation server
├── kb.py                        # Knowledge-base server
├── art.py                        # Art-generation server
├── architect_tools.py            # Role-scoped wrapper: project_ops + content_ops
├── creator_tools.py               # Role-scoped wrapper: project_ops + content_ops + mechanics_ops + reference_ops
├── reviewer_tools.py               # Role-scoped wrapper: project_ops + content_ops + reference_ops + kb_ops
├── librarian_tools.py               # Role-scoped wrapper: project_ops + kb_ops + reference_ops
└── artist_tools.py                   # Role-scoped wrapper: project_ops + art_ops
```

`.mcp.json` wires exactly six of these servers (`project`, `content`, `mechanics`,
`references`, `kb`, `art`) into Claude Code over stdio — those are the servers
agents actually talk to. The five `*_tools.py` files above (`architect_tools.py`,
`creator_tools.py`, `reviewer_tools.py`, `librarian_tools.py`, `artist_tools.py`)
are role-scoped wrapper servers that re-export `_lib/` functions under a narrower,
per-role tool surface. They exist on disk and can be run directly (`fastmcp run
mcp_servers/creator_tools.py`) for per-agent tool scoping, but none of them are
registered in `.mcp.json` by default, so no agent currently talks to them.

### Delegation: current state, not aspiration

Delegation to `_lib/` is inconsistent across the six wired servers, and this
document describes what is actually true today rather than a target state. Verify
with `grep -n "^from _lib" mcp_servers/*.py` — the truth is one grep away and drifts
easily as the servers evolve independently:

- **`mechanics.py`** fully delegates — all 5 tools (`calculate_dice_probability`,
  `calculate_extended_action`, `calculate_experience_cost`, `calculate_damage_soak`,
  `generate_random_table`) are one-line calls into `_lib/mechanics_ops.py`.
- **`references.py`** fully delegates — all 8 tools call straight into
  `_lib/reference_ops.py`.
- **`content.py`** delegates *one* tool: `check_banned_terms` calls
  `_lib/content_ops.check_banned_terms`. Its other 8 tools (`count_words`,
  `count_words_in_directory`, `check_word_targets`, `track_chapter_progress`,
  `estimate_reading_time`, `analyze_content_density`, `compile_supplement`,
  `generate_toc`) are implemented inline in `content.py` itself, even though
  `_lib/content_ops.py` has equivalent functions for most of them. If you're
  changing word-count or compilation behavior, edit `content.py` directly — editing
  `_lib/content_ops.py` will only affect `check_banned_terms` (and the unused
  `creator_tools.py` / `reviewer_tools.py` wrappers).
- **`art.py`** does not import `_lib/art_ops.py` at all — it imports only
  `_lib/art_backends.py` and `_lib/config.py`, and implements all 27 of its tools
  directly in `art.py`. `_lib/art_ops.py` exists as a parallel implementation whose
  only consumer is the unwired `artist_tools.py` wrapper server. If you're changing
  art-generation behavior for the live pipeline, edit `art.py`, not `_lib/art_ops.py`.
- **`kb.py` and `project.py`** implement their tool logic directly in the server
  file; they only import `_lib/config.py` for configuration access. The
  `_lib/kb_ops.py` and `_lib/project_ops.py` modules exist and largely duplicate
  what these two servers already do; their consumers are the unwired
  `reviewer_tools.py` / `librarian_tools.py` / `architect_tools.py` wrappers, not
  `kb.py` or `project.py` themselves. If you're extending knowledge-base or
  project-state tools for the live pipeline, edit the actual server file (`kb.py` /
  `project.py`), not the `_lib` module of the same name.

In short: only `mechanics.py` and `references.py` are genuinely thin wrappers over
`_lib/`. `content.py` is mostly its own implementation with one delegated tool.
`kb.py`, `project.py`, and `art.py` are entirely their own implementations, each
shadowed by an unused `_lib/` module that only the unwired role-scoped wrapper
servers consume.

### Testing

```bash
# Run a server directly (reads MCP requests over stdio)
python mcp_servers/mechanics.py

# Run the unit test suite covering the _lib modules
python -m unittest discover tests
```

---

## Mechanics Server Scope

The mechanics server is intentionally generic to dice-pool systems and carries no
system-specific validation logic:

- `calculate_dice_probability` — success/botch odds for a dice pool vs. a difficulty
- `calculate_extended_action` — completion probability across multiple rolls
- `calculate_experience_cost` — XP cost lookups against `mechanics.xp_costs` in
  `config/system.json`
- `calculate_damage_soak` — bashing/lethal/aggravated soak-pool math
- `generate_random_table` — dice-range tables from a comma-separated entry list

System-legality checks (e.g., is this combination of powers or resources allowed at
this character's power level?) are the responsibility of your bring-your-own toolkit
skill (`skills.toolkit_skill` in `config/system.json`), not this server.

---

## Config Layer

`mcp_servers/_lib/config.py` is the single loader every server uses to read
`config/system.json`. It ships built-in neutral defaults for every key (a missing
file, section, or field falls back safely), performs a recursive deep merge of the
JSON file over those defaults, caches the result per process, and supports a
`BOOKBINDER_CONFIG` environment-variable override for loading a different file. See
`config/README.md` for the full field reference.

The content server's `check_banned_terms` tool is a direct consumer: it scans a
draft file against `voice.banned_phrases`, `voice.banned_names`, and
`voice.use_sparingly` from the loaded config and returns violations with line
numbers.

---

## Art Generation: Multi-Backend

The art server (`art.py`, implemented directly against `_lib/art_backends.py` and
`_lib/config.py` — see the delegation note above) does not hardcode a single
image-generation API. Instead, `config/system.json`'s `art.generators` map holds one
**generator profile** per backend you've configured, and `art.active_generator`
selects the default:

| Backend | What it needs | Notes |
|---|---|---|
| `a1111` | `endpoint` (running AUTOMATIC1111 API) | Supports the full admin surface — model/sampler listing, checkpoint switching, img2img, upscale, interrogate |
| `comfyui` | `endpoint` + `workflow_file` (exported via ComfyUI's "Save (API Format)") | Workflow JSON must contain `{PROMPT}`, `{NEGATIVE}`, `{WIDTH}`, `{HEIGHT}`, `{SEED}` tokens, substituted before submission |
| `manual` | Nothing — no endpoint | Produces a prompt manifest for a human to run generation by hand |

`set_active_generator` / `get_active_generator` switch and inspect which profile is
in effect at runtime. Backend-specific admin tools called against a `comfyui` or
`manual` profile return a clear "requires an a1111 backend profile" error rather than
silently calling the wrong API. Adding a new generator is config-only: drop a
prompting-rules markdown file (and workflow JSON, for `comfyui`) under `styles/art/`
and add an entry to `art.generators` — no code changes required.

---

## BYO-Agent Skeleton

Bookbinder ships no game content, which means it also doesn't ship every agent a
given system might want. Beyond the 12 pipeline agents, systems typically add
**summarizer agents** (character summarizer, location summarizer, item summarizer —
condensing source material into structured fields for quick lookup) and
**object-creator agents** (signature-power or signature-item creators — generating
new mechanically-valid content of a specific kind). These are invoked ad hoc, not
part of the `/init-project`→`/compile` pipeline, so they're a good template for your
first custom agent.

Below is a skeleton for a neutral **location-summarizer** — an agent that reads a
chunk of source material and reduces it to structured fields. It has no game content
of its own; swap in your system's fields and file paths.

```markdown
---
name: location-summarizer
description: >-
  Reads a passage of source material describing a place and reduces it to
  structured fields: name, importance rating, notable features, and adventure
  hooks. Invoked ad hoc when a player or Gamemaster needs a quick-reference
  summary of a location rather than the full source text.
tools: Read, Grep, Glob, Write
---

# Location Summarizer

## Input Contract

You will be given:
- A block of source text describing one location (pasted inline, or a file path
  under `references/` to read)
- Optionally, a target output path (defaults to `knowledge_base/places/<slug>.md`
  if the knowledge base is configured — see `knowledge_base.root` in
  `config/system.json`)

## Output Contract

Produce a single markdown file with this structure:

\`\`\`markdown
# <Location Name>

**Rating:** <importance rating, per your system's scale>
**Region:** <where this fits in the broader setting, if known>

## Features

- <notable feature 1>
- <notable feature 2>

## Hooks

- <adventure hook 1>
- <adventure hook 2>

## Source

<citation back to the source material this was summarized from>
\`\`\`

Every field must trace back to something stated or clearly implied in the source
text — do not invent details the source doesn't support. If the source is silent on
a field (e.g. no rating given), omit that field rather than guessing.

## Workflow

1. Read the source passage (inline text or file).
2. Extract the location's name and identify its most defining trait.
3. Pull out concrete features — geography, notable inhabitants, distinguishing
   mechanics or hazards if your system tracks them.
4. Identify 1–3 hooks: reasons a Player Character party would go there or get
   pulled into trouble there.
5. Write the output file at the target path, creating parent directories if needed.
6. Report the output path and a one-line summary back to the caller.
```

Save your own version under `.claude/agents/<category>/<name>.md`, adjust the
`tools:` list to whatever the agent actually needs, and register any new MCP tools
it should have access to. Nothing else in the pipeline needs to know about it unless
you wire it into a slash command.
