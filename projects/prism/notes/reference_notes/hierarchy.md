# Reference Hierarchy for PRISM

PRISM is an original system. It cites no external source books, so the usual
precedence question ("which edition wins?") does not arise. What replaces it:

## Precedence, highest first

1. **`references/prism/00-core-rules.md`** — every number and rule. If a draft
   disagrees with this file, the draft is wrong.
2. **`references/prism/01-terminology.md`** — every term and its grammatical
   job. Binding on all ten chapters.
3. **`references/prism/02-probability.md`** — every probability. Generated from
   `calculate_sum_probability`; never quote a figure not in this file or
   produced fresh by that tool.
4. **`docs/superpowers/specs/2026-08-26-prism-core-rulebook-design.md`** — design
   rationale. Explains *why*; the three files above say *what*.

## Source-sensitive areas

- **Any probability.** Estimation is forbidden. Run the tool.
- **Any Trait value.** +2 is the permanent ceiling, including in stat blocks
  and the pregenerated Stars.
- **Difficulty numbers.** 6 / 9 / 11. Dazzling is 11, never 12.
- **The transformation/morph split.** Noun / verb / adjective each have exactly
  one word. See the terminology reference.
- **Gender.** Nothing in the book gates transformation, role, or register on
  gender, and the text never remarks on this — it simply reads that way.

## Citation format

PRISM has no page citations. Internal cross-references use anchor IDs from
`development/outlines/heading_id_registry.md` and nothing else.
