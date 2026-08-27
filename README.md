# Bookbinder

Bookbinder is a multi-agent pipeline for [Claude Code](https://claude.com/claude-code)
that turns a game system, a house style, and a pile of reference material into a
publication-ready RPG supplement. A five-agent team — project architect, content
creator, quality reviewer, knowledge librarian, and art director — carries each
chapter through a three-draft workflow (first draft → architectural review →
second draft → final draft), coordinating through file-backed MCP state instead
of a shared prompt or a message bus. Compiled output exports to DOCX, EPUB, and
PDF.

**Bookbinder ships no game content. You bring your system.**

## Status

The pipeline works. It has been run end to end across multiple game systems and
has produced usable supplements — outlined, drafted three times, reviewed,
art-directed, and compiled out to DOCX, EPUB, and PDF.

Most of that output cannot be in this repository. A supplement written against
somebody else's reference books carries third-party content this project has no
right to redistribute, and that is the rule in [License & IP](#license--ip)
applied to itself: `references/` is gitignored, and what comes out of the far
end inherits the licence of what went in.

One book escapes that, because it was written against nothing but itself.

### PRISM — a complete worked example

[`projects/prism/`](projects/prism) is an original tabletop RPG built end to end
by this pipeline and shipped whole: a sugarpop-fantasy core rulebook about people
who transform, alone and together, to push back a spreading dullness called the
Gloom. Ten chapters, 21,365 words, 33 illustrations. It cites no published game,
so its own canon lives in `references/prism/` in the open and the compiled book
is MIT like everything else here.

What is checked in is not just the finished text but the whole paper trail, which
is the part worth reading if you are deciding whether the pipeline does anything
(paths relative to `projects/prism/`):

- Three drafts of every chapter side by side — `draft_01`, `draft_02`,
  `final_draft` — so each revision is diffable.
- `development/review_feedback/` — 21 numbered architect comments, each marked
  resolved or declined with a reason.
- `development/outlines/` — the NPC registry, heading-ID registry, and forbidden
  patterns the validation sweeps actually grep against.
- `development/art_prompts.md` — all 33 image captions, and
  `content/art/` — all 33 rendered images.
- `output/compiled_supplement.md` — the assembled book. DOCX, EPUB and PDF are
  gitignored build artifacts; `/compile` regenerates them.

The design spec and implementation plan are under `docs/superpowers/`, including
the review rounds that changed the game's mathematics — Power of Friendship was
inflating the dice pool until a review caught it, and the fix is recorded rather
than quietly folded in.

That is worth shipping plainly, because a repository with no sample output and a
repository that has never been run look identical from outside.

State lives in per-project JSON files rather than in a shared prompt, which is
the design commitment everything else follows from: an agent can be restarted, a
phase can be re-run, and what a project believes about itself is readable on disk
rather than reconstructed from a conversation.

The issue tracker is a working backlog rather than a defect list — an open issue
usually records a design decision made and not yet acted on.

Bookbinder is an IP-clean rebuild of a private predecessor developed since 2025; 
this repository carries the pipeline without the third-party game content that 
made the original unshareable.

## What you bring

Bookbinder is a skeleton. Everything that makes a supplement belong to *your*
game — the rules text, the voice, the look — is a slot you fill in.

| You bring | Goes in | Notes |
| --- | --- | --- |
| Reference books | `references/` | Gitignored. Your own licensed copies. See `references/README.md`. |
| Game-mechanics skill | `skills.toolkit_skill` in `config/system.json` | A bring-your-own Claude Code skill supplying stat-block templates, validated game data, and system-legality checks (e.g. power-limit or resource-cost validation). Skeleton documented in `docs/ARCHITECTURE.md`. Leave empty and agents fall back to whatever structural blueprints you place in `styles/templates/` (which ships with only a README describing the format). |
| Writing voice | `styles/writing/` + `voice.writing_style_file` | House style guide the writing/editing agents read before drafting; also drives the `check_banned_terms` tool. |
| Book templates | `styles/templates/` | Structural blueprints per kind of book (chapter lists, word-count targets, required elements). |
| Layout theme | `styles/layout/<name>.md` + `<name>.theme.json` + `layout.docx_theme` | Human-readable layout spec plus a machine-readable DOCX theme (colors, fonts, rule styles). |
| Image-generator profiles | `styles/art/<gen>.md` rules file (+ ComfyUI workflow for `comfyui` backends) + an `art.generators` entry | One profile per image generator; `art.active_generator` picks the default. |
| *(optional)* `algorithmic-art` skill | Your Claude Code skill set | If installed, the art director can render a procedural p5.js cover instead of a diffusion-model one. Without it, covers fall back to `tools/generate_covers.py` or stay as an entry in the prompt manifest. PRISM's cover took this route — see `projects/prism/development/cover_sketch/`, which traces rays through a dispersion model rather than prompting for a picture of one. |
| Config | `config/system.json` | Single source of truth for all of the above plus terminology, citation patterns, and mechanics formulas. See `config/README.md` for the full field reference. |

Every field in `config/system.json` has a built-in neutral default — a missing
file, section, or field falls back safely, so you only write the keys you want to
change.

## Environment

- **Claude Code** — CLI or desktop.
- **[superpowers plugin](https://github.com/obra/superpowers)** — recommended,
  not required. It provides the brainstorm → spec → plan flow used when designing
  a new book from scratch. The eight slash commands that drive the pipeline
  itself run without it.
- **Python 3.11+** with `pip install "mcp<2" httpx` — the MCP servers use the
  `mcp` SDK's 1.x API (`mcp.server.fastmcp`); `mcp` 2.0 restructures this under a
  separate `fastmcp` package, so the version pin matters.
- **Optional export dependencies** (only needed for the formats you use): Node.js
  + `npm install` (DOCX export, via the `docx` package),
  [pandoc](https://pandoc.org/) (EPUB/PDF), [weasyprint](https://weasyprint.org/)
  (PDF), `python-docx`, `Pillow`, `numpy` (algorithmic cover generation).
  WeasyPrint needs the GTK/Pango stack, which is a system-level install and is
  commonly absent on Windows; where it is missing, `tools/html_to_pdf.py` prints
  the same HTML through Playwright's Chromium instead, which also supplies footer
  page numbers that Chromium's CSS paged-media support cannot.
- **Optional local image generation** via
  [AUTOMATIC1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
  (`a1111` backend) or [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
  (`comfyui` backend) — each generator profile in `config/system.json` points at
  its own endpoint URL and port. Without a running generator, the `manual`
  backend produces a prompt manifest (`development/art_prompts.md`) for you to
  run by hand. ComfyUI workflows are exported via **"Save (API Format)"** and
  must contain the literal tokens `{PROMPT}`, `{NEGATIVE}`, `{WIDTH}`,
  `{HEIGHT}`, `{SEED}`; see `styles/art/example.workflow.json`.

  PRISM's 33 illustrations came from **Ideogram 4** running locally in ComfyUI on
  the `ideogram4_fp8_scaled` weights — no hosted API, no per-image cost. Not
  through the token-substitution route above, though: `/art-direction` only
  reaches generation mode for an `a1111` backend, because its probe is a1111-only,
  so a `comfyui` profile always lands in prompt-manifest mode.
  `tools/generate_ideogram.py` is the other half — it reads that manifest back and
  builds the graph in code (Qwen3-VL text encoder, `Ideogram4Scheduler`,
  asymmetric CFG across a second unconditional UNET), mirroring ComfyUI's own
  bundled `image_ideogram4_t2i` template. It will also drive the hosted
  `IdeogramV4` partner node behind `--api`, which despite the name is a cloud call
  billed to a ComfyOrg account. Two things about the model are worth knowing
  before pointing it at a manifest, because both fail silently:

  - It is trained on **structured JSON captions** and validates against that
    schema. A prose prompt comes back as the model's own *"Image blocked by
    safety filter"* card, and so does a JSON caption with no
    `compositional_deconstruction.elements`, whatever the subject.
  - That refusal is **a valid PNG**, so a naive success check writes it to disk
    and reports success. The tool measures edge density to catch it, and says in
    its own docstring what it still cannot catch — the model sometimes paints
    the refusal text into an otherwise real picture.

## Quickstart

1. Clone the repo.
2. Edit `config/system.json` for your game system (see `config/README.md`).
3. Drop your reference books into `references/`.
4. Run the tests to confirm the toolchain works: `python -m unittest discover tests`.
5. Run the pipeline, in order:

| Command | Phase | What it does |
| --- | --- | --- |
| `/init-project [name]` | Phase 0 | Title selection, directory creation, state initialization |
| `/plan-project [name]` | Phase 1 | Chapter outline, word count targets, reference foundation |
| `/first-draft [name]` | Phase 2 | Parallel content generation (mechanics + lore) |
| `/architect-review [name]` | Phase 3 | Architectural commentary + research enhancement |
| `/second-draft [name]` | Phase 4 | Comment integration + copy editing pass |
| `/final-draft [name]` | Phase 5 | Final review, art direction, consistency validation |
| `/compile [name]` | Phase 6 | Assemble publication-ready output |

Each command checks the previous phase's quality gate before proceeding. (An
eighth command, `/art-direction [name]`, can be run standalone to (re)generate
artwork or a prompt manifest for a project.)

## Architecture

Bookbinder is coordinator-based: the project-architect agent orchestrates the
other four agents, all state lives in per-project JSON files rather than a shared
prompt, and computational work (word counts, dice math, citation extraction, art
prompts) is handled by Python MCP tools so agents spend their tokens on content,
not arithmetic. See `docs/ARCHITECTURE.md` for the full agent and tool breakdown,
and `docs/WORKFLOW.md` for how a project moves through the three-draft cycle.

Each project keeps four state files under `projects/<name>/`:

| File | Purpose |
| --- | --- |
| `state/project_state.json` | Phase, progress metrics, agent status, quality gates |
| `state/todo_list.json` | Task assignments with status, priority, and ownership |
| `state/messages.json` | Agent communication log (decisions, warnings, progress) |
| `development/art_manifest.json` | Art inventory with chapter, source, and license tracking |

## License & IP

[MIT](LICENSE). This repository contains no third-party game content. Reference materials
you add stay local (`references/` is gitignored) and are your responsibility to
license. Knowledge-base or project content you derive from published books should
not be pushed to public forks.

## Related

These share a commitment: a system should not be able to assert more than its
artifacts support.

- **[hardy](https://github.com/charlesmsiegel/hardy)** — a proof is proved only
  if Lean's kernel says so, and a result cannot be reported unless the artifacts
  carry it.
- **[ludex-rpg](https://github.com/charlesmsiegel/ludex-rpg)** — a quote and a
  paraphrase must never be confusable, anywhere in the app. Bookbinder is the
  intended source of its next test corpus: a complete, internally consistent,
  freely licensable game built to exercise hard retrieval cases on purpose.
- **[coding-skills](https://github.com/charlesmsiegel/coding-skills)** — a
  finding asserts a defect and carries a fix; a candidate reports a lead and
  carries the benign explanations. Confusing them raises.
- **[grimoire](https://github.com/charlesmsiegel/grimoire)** — the prompt a reply
  came from stays readable after everything it drew on has moved.
