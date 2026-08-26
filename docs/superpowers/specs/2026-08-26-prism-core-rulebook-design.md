# PRISM — Core Rulebook Design Spec

**Date**: 2026-08-26
**Status**: Approved for planning
**Deliverable**: A ~25,000-word core rulebook for an original tabletop RPG, produced
through the Bookbinder pipeline (Phases 0–6, excluding art generation).

---

## 1. What PRISM Is

PRISM is a sugarpop fantasy tabletop RPG about transformation — alone and together —
against a spreading dullness called the Gloom.

It is **a pickup one-shot game**: make characters in twenty minutes, play tonight,
finish the story. It is set in **the modern world you actually live in**, plus one
other layer. The
everyday is exactly itself: your town, the library losing its funding, the river
nobody cleans. Alongside it is **the Spectrum**, the same places in howling
airbrushed rainbow, where that neglect has a body and can be hit. You cross over by
**refracting**, which is also how you morph, and what you win over there changes
things back here.

Its tonal touchstones are My Little Pony, Barbie, magical-girl anime, Super
Sentai / Power Rangers, the Lisa Frank airbrush aesthetic, and the unembarrassed
major-key pop of ABBA and Aqua. It is sincere rather than ironic. It is bright,
loud, and rainbow-saturated. It is not gendered: transformation is framed
throughout as self-expression available to any character, and the book's examples,
pronouns, and art direction reflect that without comment or apology.

### The argument the book makes

Most games make you stronger by accumulating things. PRISM makes you stronger by
being *known*. The mechanical escalation ladder — extra dice, transformation,
Combined Form — is gated behind other people choosing to back you at a cost to
themselves. The game's thesis and its math are the same statement.

### What it is not

- Not a combat-first game. Nobody dies. Damage is dimming, not injury.
- Not a setting bible. The setting is the reader's own town plus one other layer;
  the chapter teaches a conversion procedure, not a canon.
- Not a masquerade game. There is no secret society, no chosen bloodline, and
  nothing to hide from.
- Not a parody. The genre is played straight.

---

## 2. Core Mechanics

### 2.1 The roll

`2d6 + Trait` versus a Difficulty.

| Difficulty | Name | Number |
|---|---|---|
| Easy | Anyone could | 6 |
| Tricky | Takes something from you | 9 |
| Dazzling | Should not be possible | 11 |

**Four Traits**, rated **+0 to +2**:

- **Heart** — sincerity, courage, connection, standing your ground
- **Flash** — speed, grace, performance, physical daring
- **Craft** — cleverness, making, fixing, knowing
- **Cool** — composure, style, reading a room, keeping it together

Starting spread is fixed: one **+2**, two **+1**, one **+0**. There is no trade, no
point-buy, and **no advancement** — **+2 is the ceiling, permanently** (§3.1).

**Why Dazzling is 11 and not 12.** With no advancement the maximum Trait is +2, so
an ordinary roll tops out at **14**. A Hit must beat the Difficulty by 3, so at
Difficulty 12 a Hit would need 15 — unreachable, leaving Dazzling able to produce
Mixed and Flourish but never a clean Hit. Retuning Dazzling to **11** puts a Hit at
exactly the ceiling: possible, and only at full stretch.

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

**Why not a wider 3/2/1/0 spread?** It was considered and rejected. A wider spread
doubles the distinct arrays (4! instead of 4!/2) but breaks the core mechanic. At
Tricky, a **+0 backed by a friend** succeeds 52.3% of the time. Under 2/1/1/0, the
specialist working alone manages 58.3% — a **6-point** gap, cheap enough that tables
will help each other for fiction reasons. Under 3/2/1/0 the specialist alone hits
72.2%, making it a **20-point tax** to involve the weaker character. Power of
Friendship would decay into a fallback for when the expert is busy, and the game's
own math would argue against its thesis.

The array is also the least interesting axis of variation in PRISM — characters are
told apart by Refrain, Signature, Bonds, and Radiance. Doubling combinatorics on the
thinnest axis at the cost of the central mechanic is a bad trade. Sharper specialization, if wanted, belongs in the **Signature** — but **the
Signature is never a bonus to the roll**. A conditional +1 would raise the maximum
total to 15 and invalidate every ceiling argument in this section, including the
reason Dazzling is 11.

Instead a Signature changes *what is possible or which Difficulty applies*: it drops
a task one band (Dazzling to Tricky, Tricky to Easy) when you are unmistakably doing
your own thing, or makes attemptable something the Showrunner would otherwise not
allow a roll for at all. That is a bigger effect than +1 and it leaves the
arithmetic — and the verified probabilities — completely intact.

### 2.2 Outcome ladder

| Result | Outcome |
|---|---|
| Under the Difficulty | **Miss.** It doesn't work, and the GM makes a move (below). |
| Meets it, or beats it by 1–2 | **Mixed.** It works, but it costs (see §2.6). |
| Beats it by 3 or more | **Hit.** Clean. |
| **Both kept dice show 6** (on any success) | **Flourish.** Clean, hits the Gloom twice as hard, and something extra: a Sparkle back, or a moment that becomes true forever. |

**Flourish is double sixes, not a margin.** A fixed margin cannot work here, and the
first two revisions of this spec both got it wrong. Two kept d6 cap at 12 and the
maximum Trait is +2, so an ordinary roll tops out at **14**. Any margin band wide
enough to feel special at Difficulty 6 is unreachable at the top Difficulty — a
permanently dead band at the top of a ladder the book presents as universal.

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

**Dazzling stays hard.** A Hit at Difficulty 11 needs a 14 — Trait +2 and both dice
sixes. The ordinary Dazzling success is therefore Mixed: you do the impossible
thing, and it costs you. That is the intended feel.

Full ladder, verified by enumeration (chance of meeting the Difficulty):

| | 0 backers | 1 | 2 | 3 |
|---|---|---|---|---|
| Easy (6), Trait +1 | 83.3% | 94.9% | 98.5% | 99.5% |
| Tricky (9), Trait +1 | 41.7% | 68.1% | 82.6% | 90.6% |
| Tricky (9), Trait +0 | 27.8% | 52.3% | 69.4% | 80.6% |
| Dazzling (11), Trait +2 | 27.8% | 52.3% | 69.4% | 80.6% |
| Dazzling (11), Trait +0 | 8.3% | 19.9% | 32.0% | 43.4% |

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
- **A Dimmed character is brought back by another character reaching them** — a
  scene, a truth, a hand held out. This takes the rescuer's action, and costs them
  **1 Shine or 1 Sparkle** (rescuer's choice). The Dimmed Star returns with
  **2 Shine**, and being reached **sounds the rescued Star's note** on the Chord
  (§4.3). This is always possible; no roll is required. Someone reaching you always
  works, which is the single most important thing this game believes.
- Shine restores fully at an Encore scene.

**Gloom** is the opposition — clocks that both sides push (§2.7). Sizes 4, 6, or 8,
each starting full. If the team is ground down before a clock empties, the *world*
keeps the loss: a place loses its color, a person forgets what they loved, a rule of
the setting bends. Consequences land on the world and on NPCs, not on PC hit
points.

Gloom is not evil. It is what happens when something stops being cared about.

---

### 2.6 What a Mixed result costs

Mixed is the most common successful outcome, so it needs a procedure rather than a
mood. **The GM names one cost from this list. The player may always refuse it and
lose 1 Shine instead.**

| Cost | Magnitude |
|---|---|
| **Shine** | Lose 1. |
| **Sparkle** | Spend 1. If you have none, this cost cannot be chosen. |
| **Exposure** | Something true comes out — a secret, a position, a feeling. No number; the fiction changes. |
| **Time** | The Gloom gains 1 tick (§2.7). The thing you're fighting got a beat while you were busy. |

The player's 1-Shine substitution guarantees every Mixed is resolvable, keeps the
GM from choosing a cost the player finds unbearable, and puts a hard number on the
resource economy so the probabilities in §9.2 mean something.

### 2.7 Beating a Gloom

A Gloom clock is a **tug-of-war on one track**, not a doom timer. It is the
monster's hold on the thing it has taken, and both sides push it.

**A Gloom clock starts full.** Its size *is* its starting value: **4** (a bad
afternoon), **6** (a real problem), **8** (a season's antagonist). A full clock is
how deep the neglect goes. You win by emptying it.

| Result | Effect on the clock |
|---|---|
| **Miss** | Gloom **+1**, never above its starting size. **This is the GM's move** — do not advance the clock and *also* make a separate clock move. |
| **Mixed** | Gloom **−1**, and you pay a cost (§2.6). |
| **Hit** | Gloom **−1**, clean. |
| **Flourish** | Gloom **−2**, clean, plus the extra. |

- **Clock empties → you win.** The monster breaks and the thing it held comes back:
  the library reopens, the neighbour answers the door, the river runs clear.
- **The Gloom wins only if every Star is Dimmed.** Nobody dies. The team simply
  can't go on tonight, the world keeps the loss, and that place stays grey until
  someone comes back for it.

**The clock cannot be taken below 1 before the Big Finish.** However well the Verse
and Chorus go, the last tick belongs to the climax. This is a one-sentence pacing
guarantee that costs nothing and stops a hot streak from ending the Number in its
second scene.

A Miss's +1 is capped at the starting size, so a bad run can undo progress but can
never make a problem worse than it was. The Gloom does not grow; it endures. That is
what makes it Gloom rather than a villain.

**This is what makes the Big Finish a race**: the team's Shine draining against the
Gloom's clock emptying, on the table, in front of everyone.

#### Finishers

A **Finisher** requires you to be transformed and costs **1 Sparkle**: it **doubles
the Gloom your roll removes**. A Hit finisher takes 2; a Flourish finisher takes 4.

The **Combined Form's finisher empties the clock outright.** It costs **1 Sparkle,
paid by any single Star, chosen by the players** — the same payment rule as the
Synchronized Morph, since Sparkle stays personal even when everything else pools. If
no Star has a Sparkle left, the finisher is unavailable and the team has to win the
ordinary way.

That is why the Combined Form is the climax, and why the Chord gates it — the team's
one guaranteed win condition is the one they can only reach by making sure nobody
was left out.

## 3. Characters

A PRISM character is built from six things:

1. **Traits** — Heart / Flash / Craft / Cool, spread as above.
2. **Refrain** — a one-line creed in the character's own voice. Drives Sparkle
   refresh. ("I don't leave people in the dark." / "Somebody has to be ridiculous
   first.")
3. **Signature** — the one thing you're unmistakably about. Mechanically it
   **drops a task one Difficulty band** (Dazzling→Tricky, Tricky→Easy) when you are
   unmistakably doing your own thing, or makes attemptable something the Showrunner
   would not otherwise allow a roll for. It is **never a bonus to the roll** — see
   §2.1; a numeric Signature would break the ceiling the Difficulty bands rest on.
   Each Signature also names a transformed-state ability.
4. **Bonds** — one written line per other PC, stating a specific shared truth.
   Bonds are spendable in Power of Friendship and deepen through play.
5. **Look** — untransformed. Grounded, ordinary, specific.
6. **Radiance** — your transformed form: color, silhouette, sound, the phrase you
   say, and the object (if any) you hold. This is the sheet's most important
   creative prompt and gets the most page space.

Character creation is a **session-one group activity** with a fixed running order,
because the team's shared command word and the Bond web have to be made together.
Target: **twenty minutes** — or zero, if the table uses the pregenerated Stars in
Chapter 6.

### 3.1 One-shot by default, and what "minimal advancement" means

PRISM is built for **a pickup one-shot**: one Number, one evening, one problem
solved. That is genre fidelity rather than a limitation dressed up as a virtue — the
touchstones are episodic formats where the numbers famously do not go up. Characters
don't get stronger; they get better known.

**There is no numeric Trait advancement, ever.** Traits cap at +2 and stay there.
This keeps the probability ladder small enough to verify exhaustively, and it
removes the +3 ceiling that broke the Flourish math twice during this spec's
development.

**What changes if a group runs a second Number:**

- **Bonds** rewrite. A Bond spent and returned at the Encore comes back saying
  something different, because something different is now true.
- **Radiance** evolves. New colour, new sound, a new line you say. Free, narrative,
  unbounded.
- **Refrain** may be rewritten once it has been genuinely tested — the clearest
  statement available that a character has grown.
- **Sparkle maximum** rises by 1 after every second Number, hard cap **5**. This is
  the only numeric growth in the game, and deliberately the one that touches no
  Difficulty and no ceiling.

That is all of advancement. It occupies roughly 400 words inside Chapter 5 beside
the Encore scene. There is no advancement chapter.

---

## 4. Transformation

PRISM fuses the magical-girl register (individual, sincere, private, a personal
phrase and object) with the sentai register (collective, synchronized, color-coded,
a shared command word). Three gears:

### 4.1 Solo Morph
One character. Costs **1 Sparkle**. Declared with your personal phrase. Unlocks
your Radiance abilities and **grants 2 Shine, raising your cap by the same 2** while
you remain transformed — the boxes arrive filled, not empty.

**When it ends.** The transformed state lasts until the Gloom clock resolves, or
until the Encore, whichever comes first — the same duration as a Synchronized Morph.
The Shine cap returns to 5 then, and any Shine above it is lost. The
once-only restriction below resets at that same boundary, so a Star morphs afresh in
the next Number.

**You can only be transformed once at a time.** The Shine is granted on *entering*
the transformed state and never again. Morphing while already transformed does
nothing and costs nothing — you are already there — and you may not revert early and
re-morph to farm the grant. Without this, three Sparkle converts into six Shine and
the five-box pressure the whole conflict system rests on evaporates.

**A Dimmed Star cannot morph.** Morphing requires you to be in the scene, and being
Dimmed means you are not. A Star at 0 Shine comes back one way only: somebody
reaches them (§2.5). Without this rule, 1 Sparkle would buy a self-rescue, which
would bypass both the cost the rescuer pays and the Chord note the rescue sounds —
and would quietly delete the most important thing the game has to say.

The book instructs the table to give a Solo Morph *airtime* — the morphing player
narrates, uninterrupted, and nobody rolls during it.

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

### 4.2 Synchronized Morph
The whole team, together, on the shared command word the players invent in session
one. Costs **1 Sparkle, paid in full by any single character** — cheaper for the team
than each member morphing solo, deliberately. Sparkle is never split or fractional;
one person pays, and the whole team morphs. Unlocks each character's Radiance
*plus* the team's shared abilities (formation moves, chained backing, group
finishers).

**It ends when the Number does** — when the Gloom clock that prompted it resolves,
or at the Encore, whichever comes first. Without this, one Sparkle in the first
session would buy a permanently transformed team, bypassing both the recurring cost
and the Bridge structure entirely.

### 4.3 Combined Form
The team fuses: one sheet, one Trait array, one pooled Shine, one enormous
finisher. Lasts until the Gloom clock resolves.

**The Trait array is the best of each Trait across the team, capped at +2.** No
value above +2 exists anywhere in PRISM, including here — an earlier draft added +1
to the best Trait, which would have produced a +3 and broken both the ceiling in
§2.1 and the probability analysis built on it. The cap costs nothing: a four-Star
team that chose different +2s fuses into +2 across all four Traits, which is already
better than any Star has ever been.

**Pooled Shine is the sum of the team's *current* Shine**, not their caps. A team
that arrives battered fuses into something fragile, and a team that arrives intact
fuses into something formidable — the Combined Form is as strong as whatever you
have left, which is the right kind of dramatic.

**On dissolution**, divide the remaining pooled Shine as evenly as possible among
the Stars; the players choose who takes any remainder. Anyone who ends on 0 is
**Dimmed**, and needs reaching like anyone else.

**The gate is the Chord.** Three conditions, all required:

1. The team has made a **Synchronized Morph**.
2. **The Chord is full** (below).
3. You are in the **Big Finish**.

#### The Chord

Every Star is a note. **You sound your note** the first time in a Number that you:

- **back another Star** at a cost, or
- have your **Refrain** cost you something, or
- are **pulled back from Dimmed** by someone reaching you.

One mark per Star, so the track is exactly the size of the team. The Chord is full
when **every note is sounding** — and the Combined Form is unavailable until it is.

**Why a chord and not a unison.** A unison is everyone on the same note; a chord is
distinct notes sounding together. That is the same principle as the fixed Trait
spread in §2.1 — the team combines *because* its members are shaped differently,
not despite it.

#### Why this gate does what we want

The design goal is a Combined Form that players feel they are **working toward**,
with real agency, that is nonetheless **near-certain by the climax**. The Chord
delivers all three:

- **It cannot fill early.** It requires that *every* Star has had a moment, which
  naturally takes most of a Number. No amount of luck accelerates it.
- **It is player-driven, not GM-granted.** Each player owns their own note and can
  go and get it deliberately. Nothing is being handed out.
- **It is near-certain by the Big Finish**, because backing is the core mechanic
  and the triggers are things players do constantly. Modelled over a session with
  four Stars, by the chance that all four have marked via backing alone:

| Backs this share of opportunities | 10 chances each | 15 | 20 |
|---|---|---|---|
| 15% | 41.6% | 69.4% | 85.4% |
| 20% | 63.5% | 86.7% | 95.5% |
| 30% | 89.2% | 98.1% | 99.7% |
| 40% | 97.6% | 99.8% | ~100% |

  The Refrain and Dimmed-rescue triggers are *additional* paths on top of this, and
  any player who simply decides to sound their note can do so on purpose. Real play
  sits at the bottom of that table or below it.

- **The failure case is the correct one.** A table where people genuinely never
  help each other does not get the Combined Form — and should not. The gate is only
  demanding of groups who aren't playing the game.
- **It produces the right table behaviour.** The group becomes mechanically
  motivated to make sure the quiet player gets a spotlight moment, because the
  Chord will not complete without them. A rule that makes a table turn toward
  whoever has been silent is doing more work than any dice modifier could.

**The Combined Form requires that nobody has been left out.** That is the whole
thesis of the game, stated as a trigger condition.

**It is the intended climax of a Number, not a rare event.** Earlier drafts of this
spec made it something a long campaign might see three times. In a one-shot game
that framing is incoherent: it would either never fire, or fire once and be a
scripted set piece rather than an earned one. A group that plays PRISM the way PRISM
asks should reach the Combined Form in the Big Finish of most Numbers — and should
feel, correctly, that they got there by looking after each other all evening.

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
| **Big Finish** | The climax, fought transformed. Finishers, Combined Form, the Gloom clock racing the team's Shine. |

**Encore** is the between-adventure downtime scene: curtain call, Bonds deepen and
change, Sparkle and Shine fully refresh, advancement is spent. It sits *between*
Numbers, not inside one.

---

## 6. Setting — your town, and the Spectrum

**The setting is the modern world you actually live in, plus one other layer.**

Everyday life is exactly itself: your town, your job, your school, the library
that's losing its funding, the river nobody cleans, the bus route they cancelled,
the neighbour nobody checks on. No masquerade, no secret academy, no chosen
bloodline. Just the ordinary business of things being allowed to go grey.

Underneath — or alongside, or one turn to the left — is **the Spectrum**: the same
places rendered in howling airbrushed rainbow. Chrome and neon and leopard print,
impossible animals, gradient skies, glitter that behaves like weather. What is a
funding shortfall in the everyday is, in the Spectrum, a **monster made of the
exact shape of that neglect** — and it can be found, named, and hit. On robot
unicorns.

**Crossing over is called refracting**, which is also how you morph: you refract
into the Spectrum and you arrive transformed. One act, not two. It happens at the
Bridge.

### 6.1 Why this framing earns its place

- **It gives the Gloom a referent.** The Gloom was already defined as what happens
  when something stops being cared about. Now that has an address: disinvestment,
  burnout, apathy, a place losing its colour. The metaphor stops being a metaphor
  and becomes a thing you can punch.
- **It makes the title literal.** White light carries every colour already; the
  Spectrum is what you see when it's split. The everyday world isn't the drab
  world — it's the world with the colour still folded up inside it.
- **It solves the thinness problem.** We are not writing a gazetteer because we
  are not inventing a world. The chapter teaches a *procedure*: take a real local
  problem, find its shape, build the Spectrum version, and stat the monster. The
  reader's own town is the setting, and 2,500 words is generous for that.
- **Lisa Frank stops being decoration and becomes diegetic.** The airbrushed
  rainbow is not a house style applied to the art — it is what a place looks like
  over there. The art direction and the fiction now say the same thing.
- **It fits the song structure exactly.** Verse: the everyday, and the problem
  shows up as a real thing. Chorus: first contact goes badly. Bridge: refract.
  Big Finish: the fight, in full colour. Encore: home again — and the real thing
  has changed.
- **The stakes stay human and ungendered.** This is a game about caring for your
  actual community, not about destiny or chosen-ones.

### 6.2 What the chapter contains

- **The Spectrum** — what it looks like, how it behaves, what the rules of the
  place are (few, and mostly about colour and sincerity).
- **The Gloom** — how neglect becomes a monster, what it wants (nothing; that is
  the horror of it), and what winning actually changes back home.
- **Refracting** — where the seams are, who can find them, what it costs.
- **Four or five worked examples**, each a real mundane problem paired with its
  Spectrum monster, as models rather than canon.
- **The conversion procedure** — explicit, step-by-step: local problem → Gloom
  clock → monster → what changes in the everyday when it falls. This is the
  chapter's actual payload.

---

## 7. Book Structure

Target: **25,000 words**, ±25% tolerance per Bookbinder convention.

| # | Chapter | Words | Content |
|---|---|---|---|
| 1 | Welcome to the Show | 1,800 | Pitch, tone, what you need, safety and consent tools, how to read this book |
| 2 | How to Play | 3,000 | The roll, Difficulties, outcome ladder, Mixed costs, Sparkle, Power of Friendship, Shine and Gloom |
| 3 | Making a Star | 3,200 | Traits, Refrain, Signature, Bonds, Look, Radiance; the twenty-minute group procedure |
| 4 | Transformation | 2,800 | Solo, Synchronized, Combined Form; the Chord; finishers; giving morphs airtime |
| 5 | Trouble | 3,000 | Conflict, beating a Gloom, chases, social pressure, Dimming and rescue, the Encore scene, minimal advancement (~400) |
| 6 | **Five Stars, Ready to Play** | 1,800 | **Pregenerated characters** with Bonds pre-written between them, a shared command word, and a filled sheet each |
| 7 | Your Town and the Spectrum | 2,500 | The two layers, refracting, the Gloom, worked examples, the conversion procedure |
| 8 | Running the Game | 3,300 | Building a Number, GM moves, tone dials, escalation, making the Bridge land |
| 9 | The Gloom | 1,900 | Monsters and antagonists with stat blocks, built from real neglect |
| 10 | The First Number | 1,700 | Starter adventure, quick reference, character sheet |

**Total: 25,000**

**What changed for the one-shot pivot.** The old Chapter 6, "Growing" (1,600 words
of advancement), is gone; its surviving content is ~400 words beside the Encore
scene in Chapter 5. The freed budget buys **Chapter 6: Five Stars, Ready to Play** —
five pregenerated characters, colour-coded, with Bonds already written between them.

For a pickup one-shot book that is the highest-value page count available: it takes
time-to-play from twenty minutes to zero, it is exactly what the genre supports (a
colour-coded team is *the* sentai image), and it doubles as the clearest possible
worked example of what Chapter 3 is asking for. An advancement chapter in a one-shot
game would have been the least-read pages in the book.

---

## 8. Voice

Warm, direct, second person, unembarrassed. Short declarative sentences with
occasional long enthusiastic ones. Rules text is plain and unfussy; flavor text is
sincere and specific. No irony about the genre, ever. No hedging about whether
this is a "real" RPG.

Codified in `styles/writing/prism.md`, produced during `/plan-project` Step 2 and
read by every drafting agent thereafter.

### 8.1 Terminology discipline — transformation vs. morph

PRISM deliberately runs two registers at once: the magical-girl one (sincere,
personal, ceremonial) and the sentai one (punchy, collective, commanded). That mix
is the point. Left uncontrolled it reads as sloppiness rather than range, so each
word gets exactly one grammatical job:

| Slot | Word | Use |
|---|---|---|
| **Noun** — the phenomenon, the concept, the chapter | **Transformation** | "Transformation is how PRISM escalates." Magical-girl register. |
| **Verb** — what a character does | **morph** | "When you morph…", "the morphing player". **Never** "transform" as a verb in rules text. Sentai register. |
| **Adjective** — the state you are in | **transformed** | "fought transformed", "your transformed form". |
| **Named moves** | **Solo Morph**, **Synchronized Morph**, **Combined Form** | Capitalized, always these exact names. |
| **Your personal expression of it** | **Radiance** | The look, sound, phrase, and object. Never a synonym for the act. |
| **Crossing into the Spectrum** | **refract** | "you refract at the Bridge". Refracting and morphing are the same act; never describe them as two steps. |
| **The two layers** | **the everyday** / **the Spectrum** | Lowercase "everyday", capitalised "Spectrum". Never "the real world" — both are real. |
| **The team-fusion gate** | **the Chord** | Each Star *sounds their note*. Never "meter", "gauge", or "bar". |

Transformation is the thing; morphing is the doing; transformed is the being. One
word per job, no overlap.

The consistency-checker pass must verify this across all ten chapters, and
`development/outlines/forbidden_patterns.md` gains an entry for "transform" used as
a verb (`transforms`, `transforming`, `to transform`). The one licensed exception is
quoted in-world dialogue, where a character may say whatever they like.

Banned throughout: gendered assumptions about who morphs or how; "it's not X,
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
- `art.density_words_per_illustration` → `2000`.

  **The density governs content illustrations only, not the whole budget.**
  `.claude/commands/art-direction.md` Step 1 computes 1 cover + 1 opener per chapter
  + 1 portrait per major NPC + `ceil(total_words / density)` content illustrations.
  At 25,000 words and density 2,000 that is:

  | Category | Count |
  |---|---|
  | Cover | 1 |
  | Chapter openers | 10 |
  | Content illustrations | 13 |
  | Major-NPC portraits | ~6 |
  | **Total prompts** | **~30** |

  An earlier revision of this spec set density to 1,500 and described the result as
  "~17 slots", mistaking the content-illustration count for the total. The real
  figure was over 30. Density 2,000 keeps the book visually dense — roughly an image
  every other page — with a stated workload of about thirty prompts rather than an
  unstated one.
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
| Trait +2, two allies backing, vs Difficulty 11 | achievable but not routine | **69.4%** ✓ |
| Trait +0, no backing, vs Difficulty 11 | possible, rare | **8.3%** ✓ |

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
portraits.

**And the prompts are not portable — correcting an earlier claim in this spec.**
`.claude/commands/art-direction.md` requires every prompt to follow the *active*
generator's `rules_file`, `prompt_style`, `style_prefix`, `negative_prompt`, and
`sizes`, precisely because different generators need fundamentally different
structures. The manifest will therefore be Ideogram-shaped natural language, not
model-agnostic text.

What survives a backend switch is the **art plan** — which images exist, where they
sit, what each depicts, and their reserved `content/art/` paths. What does not
survive is the prompt wording, which has to be regenerated by re-running
`/art-direction` under the new profile. That is a cheap re-run against an unchanged
book, not a rewrite; but it is a re-run, and this spec should not have implied
otherwise.

**The mode probe cannot see a ComfyUI server.** `.claude/commands/art-direction.md`
(line 40) selects Generation vs. Prompt Manifest mode by probing
`mcp__art__get_models` / `mcp__art__get_options` — but both call `_require_a1111()`
and return an error immediately for any non-`a1111` backend
(`mcp_servers/art.py` lines 706–717 and 809–820). Since `ideogram-v4` is a
`comfyui` profile, that probe **always** fails and the command **always** falls back
to Prompt Manifest Mode, without ever contacting a server.

For this project that is exactly the behaviour we want, and it is load-bearing
rather than incidental — worth stating plainly instead of implying we chose manifest
mode by preference. But it also means a later ComfyUI render can never be
auto-detected: anyone picking these prompts up will need a ComfyUI-aware health
check added to the mode selection, or will have to force Generation Mode by hand.

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

**What the compiled book actually contains — corrected.** Earlier revisions of this
spec claimed the book would carry visible art *slots*. It will not.
`.claude/commands/compile.md` Step 2.4 **strips** every image reference whose file is
missing whenever `development/art_prompts.md` exists. So the compiled manuscript
comes out clean: no images, and no placeholder markers either.

The art record lives in two files beside the book, not inside it:

- **`development/art_prompts.md`** — the authoritative record: placement, size, and
  the full positive/negative prompt for every planned image.
- **`development/art_manifest.json`** — **populated**, contrary to this spec's
  earlier claim. `.claude/commands/art-direction.md` (lines 79–83) requires
  `update_art_manifest` for every planned image in Prompt Manifest Mode, with
  `source="prompt_only"` and `image_path` set to its intended
  `content/art/[filename].png`. Those reserved paths are what lets a later run
  generate and drop every image into place without redoing the prompt work.
  Discarding them would throw away the main deliverable of the phase.

`source="prompt_only"` is the field that distinguishes a planned image from a
generated one; the manifest has no separate status field. Compile is expected to
emit its coverless-output warning; that is the correct outcome here, not a failure.

**Emitting visible slots would require a compile change.** We are not making one —
the clean manuscript is the better artifact, and the manifest is a more useful
record than an inline `[ART HERE]` marker.

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
   character in twenty minutes.
8. A group can open to Chapter 6, take a pregenerated Star each, read Chapter 10's
   starter Number, and be playing inside ten minutes with no prep and no
   advancement rules to consult.
9. No Trait above +2 appears anywhere in the book, including stat blocks and
   pregenerated characters.

---

## 12. Out of Scope

- Image *generation* (no image models available). The prompt manifest **and** the
  `source="prompt_only"` manifest records are in scope; only the images themselves
  are not.
- Emitting visible art placeholders into the compiled manuscript, which would
  require changing `/compile`'s image-stripping behaviour.
- Any supplement beyond the core book.
- Reworking Bookbinder's existing MCP servers beyond the single additive function
  in §9.2, and beyond the two drafting-prompt corrections in §9.5.
- A knowledge base — PRISM's canon is small enough to live in `references/prism/`.
