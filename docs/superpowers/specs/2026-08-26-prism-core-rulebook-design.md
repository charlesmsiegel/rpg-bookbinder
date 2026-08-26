# PRISM — Core Rulebook Design Spec

**Date**: 2026-08-26
**Status**: Approved for planning
**Deliverable**: A ~25,000-word core rulebook for an original tabletop RPG, produced
through the Bookbinder pipeline (Phases 0–6, excluding art generation).

---

## 1. What PRISM Is

PRISM is a sugarpop fantasy tabletop RPG about people who transform — alone and
together — to push back a spreading dullness called the Gloom.

Its tonal touchstones are My Little Pony, Barbie, magical-girl anime, Super
Sentai / Power Rangers, the Lisa Frank airbrush aesthetic, and the unembarrassed
major-key pop of ABBA and Aqua. It is sincere rather than ironic. It is bright,
loud, and rainbow-saturated. It is not gendered: transformation is framed
throughout as self-expression available to any character, and the book's examples,
pronouns, and art direction reflect that without comment or apology.

### The argument the book makes

Most games make you stronger by accumulating things. PRISM makes you stronger by
being *known*. The mechanical escalation ladder — extra dice, transformation,
combined form — is gated behind other people choosing to back you at a cost to
themselves. The game's thesis and its math are the same statement.

### What it is not

- Not a combat-first game. Nobody dies. Damage is dimming, not injury.
- Not a setting bible. Setting is a sketch and a color grammar, not a canon.
- Not a parody. The genre is played straight.

---

## 2. Core Mechanics

### 2.1 The roll

`2d6 + Trait` versus a Difficulty.

| Difficulty | Name | Number |
|---|---|---|
| Easy | Anyone could | 6 |
| Tricky | Takes something from you | 9 |
| Dazzling | Should not be possible | 12 |

**Four Traits**, rated **+0 to +3** at creation:

- **Heart** — sincerity, courage, connection, standing your ground
- **Flash** — speed, grace, performance, physical daring
- **Craft** — cleverness, making, fixing, knowing
- **Cool** — composure, style, reading a room, keeping it together

Starting spread is fixed: one **+2**, two **+1**, one **+0**. **+3** is reachable
only through advancement, never at creation. There is no trade or point-buy.

**The fixed spread is a feature, not a simplification.** A flat character has no
shape — nothing they reach for first, nothing they need anyone else for. The **+0**
is the most important number on the sheet: it is the slot where Power of Friendship
stops being optional. Every Star is good at one thing, shaky at one thing, and
ordinary at two, and that asymmetry is what makes backing each other structural
rather than polite. Characters are distinguished by Refrain, Signature, Bonds, and
Radiance — not by arithmetic.

Chapter 3 must teach the +0 as a creative prompt rather than a penalty: *what do you
do when the thing in front of you is the thing you're worst at?* The answer the game
wants is "ask someone."

### 2.2 Outcome ladder

| Result | Outcome |
|---|---|
| Under the Difficulty | **Miss.** It doesn't work, and the GM makes a move (below). |
| Meets it, or beats it by 1–2 | **Mixed.** It works, but it costs — Shine, Sparkle, exposure, or time. |
| Beats it by 3 or more | **Hit.** Clean. |
| **Both kept dice show 6** (on any success) | **Flourish.** Clean, and something extra: a Sparkle back, a Gloom clock rolled back a tick, or a moment that becomes true forever. |

**Flourish is double sixes, not a margin.** A fixed margin cannot work here, and the
first two revisions of this spec both got it wrong. Two kept d6 cap at 12 and the
maximum Trait is +3, so an ordinary roll tops out at **15**; even the combined form
(best Trait +1) reaches only **16**. Any margin band wide enough to feel special at
Difficulty 6 is unreachable at Difficulty 12 — a permanently dead band at the top of
a ladder the book presents as universal.

Double sixes fixes this and pays a dividend: because you keep the best two dice,
**more backers make Flourishes likelier**, verified by enumeration —

| Backers | Dice | Flourish chance |
|---|---|---|
| 0 | 2d6 keep 2 | 2.78% |
| 1 | 3d6 keep 2 | 7.41% |
| 2 | 4d6 keep 2 | 13.19% |
| 3 | 5d6 keep 2 | 19.62% |

Friendship is what makes the spectacular possible, not merely the reliable. That is
the whole game in one row of numbers.

A miss never stalls the scene. The GM's move on a miss always changes the
situation. If a Gloom clock is in play, the default move is to advance it. If none
is — an early Verse, an ordinary-life scene — the GM instead **starts** one, or
reveals that one has been quietly filling all along. A miss can be the moment the
problem arrives; that is a feature, and the GM chapter says so.

**Dazzling stays hard.** A Hit at Difficulty 12 needs a 15 — Trait +3 and both
dice sixes. The ordinary Dazzling success is therefore Mixed: you do the impossible
thing, and it costs you. That is the intended feel.

### 2.3 Sparkle — the personal resource

Sparkle is PRISM's Willpower/Quintessence analog. It is **personal**, not shared.

- Pool starts at **3**, rising to a maximum of **5** through advancement.
- **Spend 1** to: power a solo transformation; reroll one die; ignore one point of
  Shine loss; fuel a finisher.
- **Refresh**: when your **Refrain** costs you something in a scene, take back
  **1 Sparkle**, once per scene, never above your maximum. Full refresh at an
  Encore scene. The amount is fixed so tables don't drift into wildly different
  economies off the same trigger.

Sparkle is the thing you spend on yourself. It is deliberately *not* the
friendship lever.

### 2.4 Power of Friendship — the friendship lever

A named subsystem, not a currency. This is the `x` in `xd6 + z`.

**Backing up.** When another character rolls, you may declare that you're backing
them. State how — what you say, what you do, what you put at risk. You add **+1d6**
to their roll. Multiple allies may back the same roll; each adds a die.

**You always keep exactly two dice.** Roll the whole pool and keep the best two;
every die added by backing also drops a die. Backing makes a good result *likelier*,
never larger — the target numbers are calibrated for a two-die sum and stay that way
no matter how many people help.

Verified by exact enumeration (Trait +1 vs Difficulty 9): **41.7%** unbacked,
**68.1%** with one backer, **82.6%** with two, **90.6%** with three. Real help,
diminishing returns, no ceiling break.

**Backing costs the backer.** Choose one when you back:
- Lose 1 Shine, or
- Spend 1 Sparkle, or
- Give up your own next action — **only if you actually have one pending**. If the
  scene ends before you would have acted, the forfeit carries into the next scene.
  You may not choose this option after your last action of a scene; pick another
  cost. A cost you were never going to pay is not a cost.
- Expose something — a secret, a weakness, a feeling you'd rather not say aloud.

A backer who has an unspent **Bond** with the roller may **spend the Bond**
instead. A spent Bond is marked and cannot be spent again until the next Encore,
where it deepens and returns. This is the cheapest way to back someone, and it is
finite on purpose.

**The rule that makes it matter:** you cannot back yourself, and you cannot back
someone you have never been honest with. The GM is instructed to enforce this
warmly, as an invitation, not a gotcha.

### 2.5 Shine and Gloom

**Shine** is your track — the character-side clock. Default **5 boxes**.

- You lose Shine to failure costs, backing costs, Gloom attacks, and pushing too
  hard.
- At **0 Shine** you are **Dimmed**: out of the scene, greyed, still present.
  Not dead. Never dead.
- A Dimmed character is brought back by another character reaching them — a
  scene, a truth, a hand held out. This is always possible and always costs the
  rescuer something.
- Shine restores fully at an Encore scene.

**Gloom** is the opposition — clocks that fill. Sizes: 4 (a bad afternoon), 6 (a
real problem), 8 (a season's antagonist). When a Gloom clock fills, the *world*
gets worse: a place loses its color, a person forgets what they loved, a rule of
the setting bends. Consequences land on the world and on NPCs, not on PC hit
points.

Gloom is not evil. It is what happens when something stops being cared about.

---

## 3. Characters

A PRISM character is built from six things:

1. **Traits** — Heart / Flash / Craft / Cool, spread as above.
2. **Refrain** — a one-line creed in the character's own voice. Drives Sparkle
   refresh. ("I don't leave people in the dark." / "Somebody has to be ridiculous
   first.")
3. **Signature** — the one thing you're unmistakably about, mechanically expressed
   as a small always-on edge plus a transformed-state ability.
4. **Bonds** — one written line per other PC, stating a specific shared truth.
   Bonds are spendable in Power of Friendship and deepen through play.
5. **Look** — untransformed. Grounded, ordinary, specific.
6. **Radiance** — your transformed form: color, silhouette, sound, the phrase you
   say, and the object (if any) you hold. This is the sheet's most important
   creative prompt and gets the most page space.

Character creation is a **session-one group activity** with a fixed running order,
because the team's shared command word and the Bond web have to be made together.

---

## 4. Transformation

PRISM fuses the magical-girl register (individual, sincere, private, a personal
phrase and object) with the sentai register (collective, synchronized, color-coded,
a shared command word). Three gears:

### 4.1 Solo morph
One character. Costs **1 Sparkle**. Declared with your personal phrase. Unlocks
your Radiance abilities and **grants 2 Shine, raising your cap by the same 2** for
the scene — the boxes arrive filled, not empty. Available any time you can speak.

The book instructs the table to give a solo morph *airtime* — the transforming
player narrates, uninterrupted, and nobody rolls during it.

**Early morphs are allowed once there is something to morph *at*.** From the moment
the problem is on the table — which is the end of the Verse at the latest — a player
may morph whenever they like, and that morph *is* the Bridge: the key change has been
spent early and the GM moves the Number toward its Big Finish from there. If no Gloom
clock is running yet, the morph starts one; a transformation is itself a declaration
that something is wrong.

Before the problem arrives, in the ordinary-life opening, a morph is not a structural
beat at all — it's flavor. Someone showing off in the kitchen. It costs the Sparkle,
it looks fantastic, and it moves nothing. The Bridge is a position in the Number, not
a clock time, so this rule is about where the key change *falls*, never about
forbidding a player from reaching for it.

### 4.2 Synchronized morph
The whole team, together, on the shared command word the players invent in session
one. Costs **1 Sparkle, paid in full by any single character** — cheaper for the team
than each member morphing solo, deliberately. Sparkle is never split or fractional;
one person pays, and the whole team transforms. Unlocks each character's Radiance
*plus* the team's shared abilities (formation moves, chained backing, group
finishers).

**It ends when the Number does** — when the Gloom clock that prompted it resolves,
or at the Encore, whichever comes first. Without this, one Sparkle in the first
session would buy a permanently transformed team, bypassing both the recurring cost
and the Bridge structure entirely.

### 4.3 Combined form
Available **only after a synchronized morph**, and **only when a Gloom clock is at
one tick from full**. The team fuses: one sheet, one Trait array (best of each,
+1), one pooled Shine, one enormous finisher. Lasts until the clock resolves.

Deliberately rare. The book is explicit that a campaign might see it three times,
and that this is correct.

### 4.4 Placement in the scene
Transformation belongs at the **Bridge** (§5) — during the action, escalating into
the climax. The GM chapter states this as a hard structural rule and gives
techniques for making the Bridge arrive on time.

---

## 5. Song Structure

Scenes and sessions are organized as a pop song. A session is a **Number**.

| Beat | What happens |
|---|---|
| **Verse** | Ordinary life. Who these people are when nothing is wrong. The problem arrives at the end. |
| **Chorus** | First engagement. It goes badly. The Gloom asserts itself and a clock starts filling. |
| **Bridge** | The key change. Someone says the thing they've been avoiding. **Transformation happens here.** |
| **Big Finish** | The climax, fought transformed. Finishers, combined form, the Gloom clock racing the team's Shine. |

**Encore** is the between-adventure downtime scene: curtain call, Bonds deepen and
change, Sparkle and Shine fully refresh, advancement is spent. It sits *between*
Numbers, not inside one.

---

## 6. Setting — deliberately thin

Setting is roughly 2,500 words and functions as a color grammar plus a starter kit,
not a gazetteer. It covers:

- **The Gloom** — what it is, how it spreads, what it wants (nothing; that's the
  horror of it), and what it leaves behind.
- **Rainbow cosmology** — light, refraction, and color as the setting's physics.
  The title concept: one light, many colors, and neither is complete alone.
- **Four or five sketched places**, each a paragraph and a hook, chosen to be
  visually maximal in the Lisa Frank register — airbrushed, hyper-saturated,
  impossible animals, chrome and neon and leopard print.
- **Explicit instructions for building your own**, with the sketched places as
  worked examples. The chapter's stance is that the reader's setting is the real
  one.

---

## 7. Book Structure

Target: **25,000 words**, ±25% tolerance per Bookbinder convention.

| # | Chapter | Words | Content |
|---|---|---|---|
| 1 | Welcome to the Show | 1,800 | Pitch, tone, what you need, safety and consent tools, how to read this book |
| 2 | How to Play | 3,000 | The roll, difficulties, outcome ladder, Sparkle, Power of Friendship, Shine and Gloom |
| 3 | Making a Star | 3,500 | Traits, Refrain, Signature, Bonds, Look, Radiance; session-one group procedure |
| 4 | Transformation | 2,800 | Solo, synchronized, combined; finishers; giving morphs airtime |
| 5 | Trouble | 3,000 | Conflict, chases, social pressure, Gloom clocks, Dimming and rescue |
| 6 | Growing | 1,600 | Advancement, Bond evolution, the Encore scene |
| 7 | The World | 2,500 | The Gloom, rainbow cosmology, sketched places, build-your-own |
| 8 | Running the Game | 3,300 | Building a Number, GM moves, tone dials, escalation, making the Bridge land |
| 9 | The Cast & The Gloom | 1,800 | Sample antagonists and allies with stat blocks |
| 10 | The First Number | 1,700 | Starter adventure, quick reference, character sheet |

**Total: 25,000**

---

## 8. Voice

Warm, direct, second person, unembarrassed. Short declarative sentences with
occasional long enthusiastic ones. Rules text is plain and unfussy; flavor text is
sincere and specific. No irony about the genre, ever. No hedging about whether
this is a "real" RPG.

Codified in `styles/writing/prism.md`, produced during `/plan-project` Step 2 and
read by every drafting agent thereafter.

Banned throughout: gendered assumptions about who transforms or how; "it's not X,
it's Y" constructions; the words *whimsical*, *quirky*, and *adorkable*; any joke
whose punchline is that the game is silly.

---

## 9. Bookbinder Configuration Changes

### 9.1 `config/system.json`

- `system.name` → `"PRISM"`
- `system.project_type` → `"core rulebook"`
- `voice.writing_style_file` → `"styles/writing/prism.md"`
- `voice.tone_keywords` → sugarpop, sincere, rainbow, loud, kind
- `voice.banned_phrases` / `banned_names` extended per §8
- `terminology.gamemaster` → `"Showrunner"`
- `terminology.player_character` → `"Star"`
- `terminology.supplement` → `"rulebook"`
- `mechanics.dice` → `{"sides": 6, "count": 2, "default_target": 9, "default_difficulty": 6, "botch_on_ones": false}`

  **Compatibility constraint.** The legacy `calculate_dice_probability` validates
  `3 <= difficulty <= sides`, so `default_difficulty` must stay ≤ 6 or that tool
  errors on its own defaults. PRISM's sum target therefore lives under a new key,
  `default_target`, read only by `calculate_sum_probability`. The legacy pool tool
  is unused by PRISM but must not be left broken.
- `citations` → **left at defaults and unused.** PRISM cites no external source
  books. Configuration cannot repurpose this tooling for internal cross-references:
  `extract_citations` hard-codes `Book, p. N` patterns and merely *appends*
  configured ones, `validate_citation_format` unconditionally requires `p. N`, and
  `generate_citation_report` ignores configured patterns entirely. Internal
  cross-reference integrity is enforced instead by the heading ID registry
  (`/plan-project` Step 8a) and the consistency-checker pass — which is what those
  artifacts are for.
- `art.active_generator` → `"ideogram-v4"` (see §9.4)
- **`art.generators["ideogram-v4"].sizes` must be added** — the shipped profile has
  no `sizes` map, and `.claude/commands/art-direction.md` (line 75) requires every
  manifest entry to take its dimensions from it rather than inventing them. Add
  `portrait`, `landscape`, `column`, and `full_page` at Ideogram-appropriate
  resolutions.
- `art.density_words_per_illustration` → `1500`. At 25,000 words that is ~17 art
  slots — appropriate for a visually-forward book, where the default 2,250
  (~11 slots) would read as sparse.
- `layout.style_file` → `"styles/layout/prism.md"` and `layout.docx_theme` →
  `"prism"`. **Both keys move together**: `/compile` Step 3 reads `style_file` as
  the design language that the selected theme implements, and confirms it points at
  a real file in `styles/layout/`. Leaving it on the neutral slate-and-gold default
  would feed the compile step layout instructions that contradict the theme.

### 9.2 New code — sum-based dice probability

The existing `mcp_servers/_lib/mechanics_ops.py` implements
`calculate_dice_probability` for World-of-Darkness-style **dice pools** (count
successes against a per-die difficulty). It cannot express `2d6+3 vs 9`.

Add `calculate_sum_probability(dice=None, sides=None, modifier=0, target=None, keep=None)`:

Every parameter is optional and falls back to config — `dice` to
`mechanics.dice.count`, `sides` to `mechanics.dice.sides`, `target` to
`mechanics.dice.default_target` — so the configured defaults are live, not
decorative. Called bare, it answers "what are the odds on a standard PRISM roll?"

`keep` (default: all dice) replaces the originally-specified `drop_lowest`, because
Power of Friendship keeps a fixed *two* dice regardless of pool size; expressing
that as a drop-count would force the caller to recompute it per backer and would
re-admit the P1 bug above.

- Exact distribution over the sum of the best `keep` of `dice` dice of `sides`
  sides, plus a flat `modifier`.
- Returns probability of meeting `target`, plus the PRISM outcome-ladder bands
  (mixed / hit / flourish) and the expected value.
- Input validation matching the existing module's conventions (return an error
  string rather than raising).
- Exposed as an MCP tool in `mcp_servers/mechanics.py`, delegating to `_lib`.
- Unit tests in `tests/`, including hand-checkable cases (`1d6` uniform, `2d6`
  bell curve, `best 2 of 3d6` against a brute-forced enumeration, and config
  fallback when arguments are omitted).

A keep-best-N parameter is required because Power of Friendship is exactly a
keep-best-two mechanic; without it we cannot check whether backing is appropriately
valuable — as the P1 finding on this spec's first revision demonstrated.

**Balance targets to verify with this tool** (these are the acceptance criteria
for the mechanics chapter):

| Situation | Target | Verified |
|---|---|---|
| Trait +1, no backing, vs Difficulty 9 | roughly a coin flip | **41.7%** ✓ |
| Trait +1, one ally backing, vs Difficulty 9 | clearly better, short of a sure thing | **68.1%** ✓ |
| Trait +3, two allies backing, vs Difficulty 12 | achievable but not routine | **69.4%** ✓ |
| Trait +0, no backing, vs Difficulty 12 | possible, rare | **2.8%** ✓ |

All four verified by exact enumeration against the keep-best-two rule. The
implementation must reproduce these numbers; they are test cases, not aspirations.

If the math contradicts the Difficulty numbers in §2.1, the numbers change, not
the tool.

### 9.3 New style assets

- `styles/writing/prism.md` — the voice guide (§8)
- `styles/templates/core-rulebook.md` — a book template for core rulebooks:
  chapter list, per-section word expectations, required elements (sheet, quick
  reference, starter adventure, safety tools)
- `styles/layout/prism.md` + `styles/layout/prism.theme.json` — the layout design
  language and its DOCX theme data: hyper-saturated Lisa Frank palette, both files
  required by `/compile` Step 3
- `references/prism/` — PRISM's own design documents, so the reference-librarian
  role has something to check internal consistency against. **Requires a
  `.gitignore` change**: the repo currently ignores `references/**` except
  `references/README.md`, which would leave these untracked and absent from fresh
  clones. Add negations for `references/prism/` and its contents. This is safe
  precisely because PRISM's canon is our own original content — the blanket ignore
  exists to keep third-party source books out of the repo, and nothing here is
  third-party.
- `config/README.md` — updated with the new `mechanics.dice.count` and
  `mechanics.dice.default_target` fields and the compatibility constraint above

### 9.4 Art generator: Ideogram 4

**Decision: Ideogram 4 for the entire book, single model.** (Alternative considered:
Anima.)

- **The Lisa Frank anchor is not anime.** It is 90s airbrushed commercial
  illustration — rainbow gradients, chrome, hyper-saturated impossible animals.
  Anima is an anime specialist; that register fights its training on every image.
- **Rulebook art is subject-diverse**: chapter openers, places, objects, Gloom
  clocks, spot art. Anime checkpoints are character-centric and weaker on
  environments, objects, and abstract composition.
- **Sentai ensembles are a prompt-adherence problem.** "Five color-coded figures in
  synchronized formation, each distinct" is where anime checkpoints blur and lose
  count. The repo's `ideogram-v4` profile drives a structured JSON caption that
  names each element separately — built for exactly this.
- **Text rendering.** A cover wordmark and in-world signage; PRISM's transformation
  phrases belong on the page. Ideogram is strong here; anime models are not.
- **Consistency beats peak quality.** Mixing two visual languages across one book
  reads as incoherent.
- **Tiebreaker, not the reason**: `styles/art/ideogram-v4.md` and its ComfyUI
  workflow already exist and are complete. Anima has no profile, rules file, or
  workflow in this repo.

**What this costs**: Anima would produce better expressive close-up transformation
portraits. This is recoverable — the prompt manifest is model-agnostic text, so
those slots can be re-rendered through another backend later without rewriting the
book. The manifest flags which slots are character splashes for exactly that reason.

**Caveat on "already exists".** The `ideogram-v4` profile's prompting rules are
complete, but its `workflow_file` points at `styles/art/example.workflow.json`,
whose own `_readme` calls it a template to replace — it has no model loader, no
decoder, and no image-output node. Rendering through this backend will require a
real workflow exported from ComfyUI via *Save (API Format)*. That is out of scope
here (we generate no images), but it is a prerequisite for anyone who later picks
the manifest up, and the manifest must say so rather than implying the backend is
ready to run.

### 9.5 Drafting prompts must be corrected too

The additive MCP function is not sufficient on its own. Two shipped prompts still
route PRISM's balance work to the wrong probability model, and would have the
drafting agent validate a sum-based `2d6+Trait` game with a World-of-Darkness
success-counting tool:

- `.claude/commands/first-draft.md` **line 41** directs dice math to
  `calculate_dice_probability` / `calculate_extended_action`.
- `.claude/agents/book-creation/mechanics-designer.md` **line 111** recommends
  `calculate_dice_probability` for balance testing, and **line 78** mandates
  dice-pool success thresholds ("Simple=1, Complex=3-5, Extreme=10+") that have no
  meaning in PRISM.

Both must point at `calculate_sum_probability`, and the success-threshold guidance
must be replaced with PRISM's Difficulty bands. Leaving this out would let the
rulebook's own mechanics get validated against a model the spec elsewhere says
cannot express the game.

---

## 10. Pipeline Plan

Run in order, with the standard quality gate between each:

| Phase | Command | Notes |
|---|---|---|
| 0 | `/init-project prism` | Title, directories, state |
| 1 | `/plan-project prism` | Outline, briefs, concepts, registries |
| 2 | `/first-draft prism` | `draft_01.md` per chapter |
| 3 | `/architect-review prism` | Architectural commentary |
| 4 | `/second-draft prism` | `draft_02.md` — comment integration + copy edit |
| 5 | `/final-draft prism` | `final_draft.md` — consistency, final review |
| 6 | `/compile prism` | Assembled manuscript + exports |

**Art direction is not a separate phase.** `/final-draft` already invokes
`/art-direction` at its Step 2 (`.claude/commands/final-draft.md`, line 50), so
adding a standalone Phase 5.5 — as this spec's previous revision did — would plan
every image twice. `update_art_manifest` appends entries without deduplicating, so
the second pass would leave duplicate records and compilation could place or
attribute the same artwork repeatedly. The art-direction step inside Phase 5 runs in
deferred mode; that is the only invocation.

**No images are generated**, since no image models are available in this
environment. But `/art-direction` is **not skipped outright** — it runs in its
deferred / prompt-manifest mode, which writes `development/art_prompts.md`
(placement, size, and a written prompt per slot) and produces no image files.

This is required for `/compile` to run at all. `.claude/commands/compile.md`
inserts cover and chapter-opener image references, and treats missing image files
as an error *unless* `development/art_prompts.md` exists (line 58) — and it halts
outright on a missing `content/art/cover.png` unless a deferred cover was
explicitly chosen (line 86). Skipping the phase entirely, as this spec's first
revision proposed, would have stalled the pipeline at the final step.

The compiled book therefore carries art *slots* — placement markers with
descriptive captions and a ready-to-run prompt for each — and no generated
images. The art manifest is not populated. Compile is expected to emit its
coverless-output warning; that is the correct outcome here, not a failure.

Agent roles are executed inline in the driving session rather than dispatched as
subagents, per the session's configuration.

---

## 11. Success Criteria

1. `python -m unittest discover tests` passes, including the new
   `calculate_sum_probability` tests.
2. The Difficulty numbers in §2.1 are verified against
   `calculate_sum_probability` output, and §9.2's four balance targets hold.
3. Ten chapters exist at `final_draft.md` stage, within ±25% of their word
   targets, totaling 25,000 ±25%.
4. `/compile` produces `projects/prism/output/compiled_supplement.md` with a
   working table of contents and no forbidden patterns (no `TODO`, `TBD`,
   `p. XX`, HTML comments, or review artifacts).
5. Every mechanical term in this spec is used consistently across all ten
   chapters — verified by the consistency-checker pass.
6. Nothing in the book gates transformation, role, or tone on gender.
7. A reader who has never played an RPG can finish Chapters 1–3 and make a
   character.

---

## 12. Out of Scope

- Image *generation* and the populated art manifest (no image models available).
  The deferred prompt manifest is in scope; the images it describes are not.
- Any supplement beyond the core book.
- Reworking Bookbinder's existing MCP servers beyond the single additive function
  in §9.2, and beyond the two drafting-prompt corrections in §9.5.
- A knowledge base — PRISM's canon is small enough to live in `references/prism/`.
