# First Draft — findings carried into later phases

## 1. Em-dash overuse (systemic, all ten chapters)

`check_banned_terms` flags `—` against the configured limit of 20 per 10,000
words (`voice.use_sparingly`).

| Chapter | Words | Em-dashes | Allowed |
|---|---|---|---|
| 01 | 1459 | 12 | 2 |
| 02 | 2361 | 31 | 4 |
| 03 | 2581 | 34 | 5 |
| 04 | 2154 | 22 | 4 |
| 05 | 2303 | 22 | 4 |
| 06 | 1544 | 23 | 3 |
| 07 | 1936 | 18 | 3 |
| 08 | 2546 | 23 | 5 |
| 09 | 1683 | 22 | 3 |
| 10 | 1511 | 27 | 3 |
| **Total** | **20078** | **234** | **40** |

Roughly 194 to remove book-wide. **Fix in the copy-editing pass (Phase 4).**
Most are parenthetical asides that work as commas, colons, or full stops. Do
not mechanically replace all of them — the ones setting up a beat before a
punchline are doing real work and should survive.

## 2. Word counts are at the low end of every band

Total 20,078 against a 25,000 target — inside the ±25% band, but only just, and
every chapter sits below its own target rather than around it. Phase 4 should
add rather than trim. Chapters 8 and 9 have the most room.

## 3. Casing violations caught and fixed at draft

Two instances of lowercase `synchronized morph` in Chapter 10, caught by the
forbidden-pattern sweep and corrected in place. The sweep works; keep running it
after every phase.

## 4. Clean

- No `transform` as a verb anywhere.
- No Trait above +2.
- No `Difficulty 12`.
- `player character` appears exactly once, in Chapter 1, as licensed.
- All five pregen Stars match `npc_registry.md` exactly.
