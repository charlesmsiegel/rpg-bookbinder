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

Starting spread: one **+2**, two **+1**, one **+0**. **+3** is reachable only
through advancement, never at creation.

**The Refrain trade**: once at creation, you may lower one Trait by 1 to raise
another by 1, if your Refrain justifies the trade in a sentence. The +2 creation
ceiling still applies.

### 2.2 Outcome ladder

| Result | Outcome |
|---|---|
| Under the Difficulty | **Miss.** It doesn't work, and the GM advances a Gloom clock. |
| Meets it, or beats it by 1–2 | **Mixed.** It works, but it costs — Shine, Sparkle, exposure, or time. |
| Beats it by 3–5 | **Hit.** Clean. |
| Beats it by 6 or more | **Flourish.** Clean, and something extra: a Sparkle back, a Gloom clock rolled back a tick, or a moment that becomes true forever. |

A miss never stalls the scene. The GM's move on a miss always changes the
situation.

**Ceiling note — must be validated in §9.2.** An untransformed `2d6+3` tops out at
15. Against Difficulty 12 that is a maximum margin of +3, so a Dazzling task can
be Hit but never Flourished without backing dice or transformation bonuses. This
is intended — Dazzling should require help — but the bands above are a *starting
proposal*. If `calculate_sum_probability` shows the ladder produces dead bands or
a Flourish rate near zero at realistic Trait values, the band widths change.

### 2.3 Sparkle — the personal resource

Sparkle is PRISM's Willpower/Quintessence analog. It is **personal**, not shared.

- Pool starts at **3**, rising to a maximum of **5** through advancement.
- **Spend 1** to: power a solo transformation; reroll one die; ignore one point of
  Shine loss; fuel a finisher.
- **Refresh** by living up to your **Refrain** — your one-line creed. When your
  Refrain costs you something in a scene, you take Sparkle back. Full refresh at
  an Encore scene.

Sparkle is the thing you spend on yourself. It is deliberately *not* the
friendship lever.

### 2.4 Power of Friendship — the friendship lever

A named subsystem, not a currency. This is the `x` in `xd6 + z`.

**Backing up.** When another character rolls, you may declare that you're backing
them. State how — what you say, what you do, what you put at risk. You add **+1d6**
to their roll; they roll all dice and **drop the lowest**. Multiple allies may
back the same roll; each adds a die.

**Backing costs the backer.** Choose one when you back:
- Lose 1 Shine, or
- Spend 1 Sparkle, or
- Give up your own next action in the scene, or
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
your Radiance abilities and raises your Shine cap by 2 for the scene. Available
any time you can speak.

The book instructs the table to give a solo morph *airtime* — the transforming
player narrates, uninterrupted, and nobody rolls during it.

### 4.2 Synchronized morph
The whole team, together, on the shared command word the players invent in session
one. Costs **1 Sparkle total, split or paid by anyone** — cheaper per person than
going solo, deliberately. Unlocks each character's Radiance *plus* the team's
shared abilities (formation moves, chained backing, group finishers).

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
- `citations.patterns` → internal cross-reference form only; PRISM has no external
  source books, so the librarian role validates internal consistency instead
- `layout.docx_theme` → `"prism"` (new theme file, see 9.3)

### 9.2 New code — sum-based dice probability

The existing `mcp_servers/_lib/mechanics_ops.py` implements
`calculate_dice_probability` for World-of-Darkness-style **dice pools** (count
successes against a per-die difficulty). It cannot express `2d6+3 vs 9`.

Add `calculate_sum_probability(dice, sides, modifier, target, drop_lowest=0)`:

- Exact distribution over the sum of `dice` dice of `sides` sides, optionally
  dropping the `drop_lowest` lowest dice, plus a flat `modifier`.
- Returns probability of meeting `target`, plus the PRISM outcome-ladder bands
  (mixed / hit / flourish) and the expected value.
- Input validation matching the existing module's conventions (return an error
  string rather than raising).
- Exposed as an MCP tool in `mcp_servers/mechanics.py`, delegating to `_lib`.
- Unit tests in `tests/`, including hand-checkable cases (`1d6` uniform, `2d6`
  bell curve, `2d6 drop lowest of 3` against a brute-forced enumeration).

`drop_lowest` is required because Power of Friendship is exactly a drop-lowest
mechanic; without it we cannot check whether backing is appropriately valuable.

**Balance targets to verify with this tool** (these are the acceptance criteria
for the mechanics chapter):

| Situation | Target |
|---|---|
| Trait +1, no backing, vs Difficulty 9 | roughly a coin flip |
| Trait +1, one ally backing, vs Difficulty 9 | clearly better than a coin flip, short of a sure thing |
| Trait +3, two allies backing, vs Difficulty 12 | achievable but not routine |
| Trait +0, no backing, vs Difficulty 12 | possible, rare |

If the math contradicts the Difficulty numbers in §2.1, the numbers change, not
the tool.

### 9.3 New style assets

- `styles/writing/prism.md` — the voice guide (§8)
- `styles/templates/core-rulebook.md` — a book template for core rulebooks:
  chapter list, per-section word expectations, required elements (sheet, quick
  reference, starter adventure, safety tools)
- `styles/layout/prism.theme.json` + a layout note — hyper-saturated palette for
  DOCX export
- `references/prism/` — PRISM's own design documents, so the reference-librarian
  role has something to validate internal consistency against
- `config/README.md` — updated with the new `mechanics.dice.count` and
  `mechanics.dice.default_target` fields and the compatibility constraint above

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

**`/art-direction` is skipped.** No image models are available in this
environment. The compiled book carries art *slots* — placement markers with
descriptive captions — but no generated images. The art manifest is not
populated.

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

- Image generation and the art manifest (no image models available).
- Any supplement beyond the core book.
- Reworking Bookbinder's existing MCP servers beyond the single additive function
  in §9.2.
- A knowledge base — PRISM's canon is small enough to live in `references/prism/`.
