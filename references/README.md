# References

Drop your game system's source books here (PDF and/or markdown conversions).
**Third-party source material is never committed** (see `.gitignore`) — Bookbinder
ships no game content, and your books are your own licensed copies.

**Exception: your own original canon.** A project whose game system you wrote
yourself has no external books to cite, and its design documents *are* the
reference material the librarian role checks against — so they need to be in the
repository, not only on one machine. `.gitignore` therefore re-includes
`references/prism/`, holding PRISM's own rules, terminology, and probability
references. If you add your own original system, add a matching negation; if you
are dropping in someone else's published books, do not.

## Suggested layout

    references/<game-line>/<edition-or-category>/<book>.pdf

## Precedence hierarchy

Agents resolve contradictions by source priority. Edit this list for your system
(highest priority first):

1. `references/<game-line>/<primary-edition>/` — current edition, authoritative
2. `references/<game-line>/<community>/` — your own or community material
3. `references/<game-line>/<older-editions>/` — historical context only
