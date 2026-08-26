# Research Enhancement — Phase 3

Validation of the architect's 21 comments against `references/prism/`, which is
PRISM's own canon. No external sources exist for this system, so "research"
here means checking each suggestion against the rules of record and reporting
where canon already answers the question.

## Comments canon can answer immediately

**COMMENT-003 — rerolling with backing dice.**
`00-core-rules.md` says Sparkle buys "reroll one die" and separately that you
"always keep exactly two dice". The two together imply: reroll any one die in
the pool, then keep the best two as normal. Canon supports the fix; it simply
never says it in one place. **Recommend the explicit sentence.**

**COMMENT-006 — Signature dropping an Easy task.**
Canon says a Signature "drops a task one Difficulty band ... or makes
attemptable what would otherwise not be rollable". Below Easy there is no band,
and the second clause points at the answer: it stops being a roll. **Recommend
"you simply do it, no roll."** Consistent with Chapter 5's "when not to roll".

**COMMENT-004 — Shine cap.**
Canon is unambiguous: track of 5, Solo Morph grants 2 and raises the cap by 2
while transformed. Chapters 2, 4 and 10 all agree. The gap is purely a missing
forward reference. **No rules change needed.**

**COMMENT-010 — Combined Form array.**
Canon: "the best of each Trait across the team, capped at +2." A team who all
chose the same +2 genuinely gets a weaker Combined Form. This is a real
consequence, not an oversight, and the architect is right that it should be
stated rather than left for a table to discover.

**COMMENT-018 — move precedence.**
Canon lists three moves per Gloom and Chapter 8 lists generic ones. Nothing in
canon establishes precedence. **This is a genuine hole and the fix is
editorial:** state that the Gloom's own three come first.

## Comments requiring a design decision, not research

- **COMMENT-005** (pre-written Bonds vs the honesty rule) — canon does not
  address pregenerated characters at all. Either resolution is consistent.
- **COMMENT-015** (Chapter 7/9 redundancy) — purely structural.
- **COMMENT-019** (The Understudy's clock size) — canon fixes clock sizes at
  4/6/8 and `npc_registry.md` records The Understudy at 8. Changing it means
  updating the registry first, then Chapter 9. Flagging the ordering because the
  registry is the source of truth.

## Consistency check performed

Every numeric value in all ten drafts was checked against
`references/prism/00-core-rules.md` and `npc_registry.md`:

- Difficulties 6 / 9 / 11 — consistent in Chapters 2, 5, 10.
- All five pregen Trait spreads — exact match to the registry.
- The Last Bus clock 6 — consistent in Chapters 9 and 10.
- Chapter 5's worked example — arithmetic verified correct, including the clock
  ticking back up on a Miss with room available.
- Chapter 2's probability tables — match `02-probability.md` exactly
  (41.7 / 68.1 / 82.6 / 90.6 and 2.78 / 7.41 / 13.19 / 19.62).

No canon conflicts found.

## Note on citations

PRISM cites no external works. `references/prism/` is the whole bibliography,
and the citation tooling is deliberately unused for this project — the reference
tools hard-code a `Book, p. N` pattern that cannot express an internal rule
reference. Internal consistency is enforced by the heading registry and this
check instead.
