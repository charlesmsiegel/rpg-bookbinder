# Forbidden Patterns

The following patterns must not appear in any `final_draft.md` or compiled output.
Validation sweeps will grep for each pattern and reject files containing them.

Sweeps match **whole words**, so `transform` does not flag the correct words
`transformation` and `transformed`.

## Draft Metadata
- `<!-- ` (HTML comments — all must be stripped before final)
- `[Note:` (inline editorial notes)
- `Draft Notes:`
- `Word Count:`
- `**End of Chapter`

## Unresolved Placeholders
- `p. XX`
- `page XX`
- `TODO`
- `FIXME`
- `TBD`
- `PLACEHOLDER`

## Review Artifacts
- `ARCHITECT COMMENT`

## Terminology violations (spec section 8.1)
- `transform`
- `transforms`
- `transforming`
- `combined form` (lowercase — must be `Combined Form`)
- `solo morph` (lowercase — must be `Solo Morph`)
- `synchronized morph` (lowercase — must be `Synchronized Morph`)
- `Gamemaster` (must be `Showrunner`)

## Out-of-range values
- `Difficulty 12` (Dazzling is 11)

## Review flags — NOT automatic rejections

**These must not be added to the hard-reject sections above.** The final-draft
gate treats every entry above with zero tolerance, so a term the book is
*required* to use cannot be listed as forbidden. Each of these needs a human
look instead:

- `+3` — a Trait of +3 is forbidden, but "+3" appears innocently in a margin
  table or in "3 backers" phrasing. Check what it modifies.
- `player character` — forbidden as PRISM's term for a Star, but Chapter 1
  must explain to a newcomer what a player character *is* before the book
  renames them Stars. That one use is correct and required; every other one is
  wrong.
