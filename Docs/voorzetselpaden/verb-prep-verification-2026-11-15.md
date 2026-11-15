# Verifying the ZiN / Heard Dutch Here additions

Written 15 November 2026, after the audit in
`verb-prep-check-2026-11-15.md` ran out of context partway through. Updated the
same day, once the owner asked for the recommendations to be actioned.

**The changes are now on the pages.** What follows is a read of what the audit
left on disk, with the disputed numbers resolved, plus a record of what was
fixed and what is still open. The band pages are the source of truth; see
`AGENTS.md` in this folder.

Read this together with:

- `verb-prep-check-2026-11-15.md` — the audit's own account, by band
- `dutchgrammar-check.md` — the 13 November check, still partly unactioned
- `AGENTS.md` — how to edit this folder (the pages are master, the JSON is not)

## The answer

Yes, the audit inserted new items: **121 cards across 121 new chunks**. They
are not in the game. No pre-existing card was rewritten except one note. The
audit's arithmetic holds; two numbers in the docs did not, and five of the 121
had real content faults. The faults, the four glosses and one chunk label are
now fixed.

## What was inserted, and how that was measured

Compared by card id against HEAD `f2e7022` (which holds 894 cards / 593 chunks,
so the report's `317f9db` baseline gives the same figures).

| | Before | Now |
|---|---|---|
| Cards | 894 | 1015 |
| Distinct chunks | 593 | 713 |
| Proposal cards | 150 | 271 |

- 121 new cards, 121 new chunk names, none colliding with an existing chunk.
- All 121 carry `data-kind="proposal" data-status="planned"` and "not drawn yet".
- Band split **A1 3 · A2 27 · A2+ 6 · B1 48 · B1+ 27 · B2 10** — exact.
- None appear in `prepositions.json`; `getuigen over` was already there.
- Zero cards removed, zero duplicate ids, zero attribute changes.
- **One existing card edited:** the note on `kijken-op-de-klok`, which is the
  intended §1.6 kept-reason. The audit's "no existing card altered" is off by
  that one.

The two unverified claims in §1.6 both hold:

- `getuigen over` sits in cluster `getuigen`, `<span class="preps">over · van</span>`,
  two cards, beside `getuigen van`.
- The `kijken op` card's note carries the "kept against the drop rule" reason
  verbatim.

## Two numbers in the docs were wrong — both corrected

1. **`Docs/voorzetselpaden/index.html:126`** said "68 chunks appear in more than
   one band". Actual: **58 chunk names**, making **68 extra entries**
   (781 entries − 713 distinct). The table's arithmetic was right; the noun was
   wrong. Now reads: "58 chunks have entries on more than one band page (68
   extra entries)".
2. **`CLAUDE.md` item 14** said "533 chunks have fewer than three example
   scenes". Now it is **636 chunks** (651 if counted by the best group per
   chunk); before the audit it was 516/531. Reaching three everywhere needs
   **1,222 scene briefs**, not "roughly 1,000". The policy question in that item
   still stands.

## The five faults — fixed

| Card | Was | Now |
|---|---|---|
| `verdwijnen-uit-de-kamer` (B1) | Empty-bedroom scene; example was *paintings disappearing from a museum* | Scene kept; example is `De spullen verdwijnen uit de kamer.` and the two builds are `De spullen verdwijnen uit de kamer` / `De koffer verdwijnt uit de kamer` |
| `slagen-in-het-examen` (B1) | Id and gloss said *examen*; scene, example and check question taught `erin slagen` with a stuck window | Renamed to `slagen-erin-het-raam` (id and `.png` footer), matching the `erin` example and the window scene. Chunk stays `slagen in` |
| `delen-door-twaalf` (B1+) | Id said divide *by twelve*; sentence was `twaalf door drie` | Renamed to `delen-door-drie` (id and `.png` footer) |
| `telefoneren-naar-moeder` (A2) | Note shipped "Belgian Dutch prefers telefoneren naar" while `bang zijn van` was rejected *because* it is Belgian | Note now: `telefoneren naar` is standard in Belgium; in the Netherlands `bellen met` (A2+) is the everyday form. Both are correct; keep `naar` with the verb `telefoneren`. |
| `geven-om-familie`, `verslaafd-aan-de-telefoon` (A2, A2+) | Check questions test the distractor, not the meaning | **No change.** The corpus consistently asks about the scene's avoid-mark (e.g. "Trekt de patiënt de arm weg? Nee"), so these are house style, not faults |

`dromen-van-een-reis`'s "Ligt de persoon in bed? **Nee**" is **not** a fault.
The bed is the contrast with `dromen over`, and the brief says no bed is in
sight.

## The four glosses — fixed

A chunk group's gloss is the first non-empty gloss in the group, which is what
the game takes. In these four groups the later cards are empty, so the first
card was the only one to change. (Some groups elsewhere repeat the gloss on
every card, and a few give each card its own variant.)

| Page | Card | Was | Now |
|---|---|---|---|
| A0 | `zoeken-naar-sleutels` | to search for | **to look for** |
| A1 | `vragen-naar-informatie` | to ask about | **to ask about, to ask for a person** |
| A1 | `vragen-om-hulp` | to ask for | **to ask for (a thing)** |
| A2 | `praten-tegen-muur` | to talk at | **to talk to** |

## Chunk-label faults

All eight from `dutchgrammar-check.md` §6 were already marked: `durven om`,
`afspreken op`, `leren met`, `controleren voor`, `behandelen bij`,
`ophouden aan` and `uitvoeren volgens` carry `data-verdict="drop"` and the
`v-drop` badge on every card. Per `317f9db` they stay on the page; they are
left as marked.

`zorgen over` was the exception: it is really `zorgen hebben over` (noun +
governed preposition), so it was relabelled in the chunk group and on both
card headings and moved to **Single frames** as `data-stem="zorgen hebben"`.
`zorgen voor` moved with it (it is a single, and already taught that way on A0
and B1), so the old `zorgen` contrast cluster is gone. The two cross-reference
notes on `a0.html` and `b1.html` now read `zorgen hebben over (B1+)`. The card
stays `data-verdict="drop"`; the drop was **not** cleared in this pass.

## Corrections to the earlier notes

- **"Do not regenerate `prepositions.json`" had the wrong reason.** The
  importer reads only A0/A1 cards carrying `class="beeld"`. Running
  `build_content()` today produces **identical** ids and structure to the live
  JSON (91 scenes / 91 frames / 28 levels, zero symmetric difference). The only
  content delta is the two A0/A1 gloss fixes (`zoeken naar`, `vragen naar`), which
  would propagate on a run. The rule still stands — the JSON is generated and
  irrelevant, so do not touch it unless the owner asks — but regeneration is
  not the hazard the first draft claimed.
- **`praten-tegen-lege-stoel`'s `data-kind="proposal" data-status="planned"` was
  not stale.** 114 art-bearing cards carry that exact pair (43 on A1). Only its
  id and filename were stale; they are now `praten-tegen-de-hond` (id, `.png`
  footer) and the stale "rename the id" note is replaced with a real pair note.
- **The two "weak" check questions are not faults** — see the table above.
- **Section tellers include dropped cards.** `p.contrastnoot` counts every card
  on the page (the `zorgen` cluster read "2 prepositions, 2 cards" with one drop
  in it). Only `matrix-*.html` leaves dropped cards out. The earlier pitfall
  note had this backwards.

## Older faults still open, unchanged

- `dutchgrammar-check.md` §1 ("26 combinations absent anywhere") is now
  **stale**: 12 of those 26 were added by this audit (`geven aan`, `geven om`,
  `sturen naar`, `verslaafd zijn aan`, `besteden aan`, `smeken om`, `vrezen
  voor`, `aansturen op`, `anticiperen op`, `afreageren op`, `zich abonneren
  op`, `zich voegen naar`); 14 remain absent.
- `geinteresseerd in` (A2, no diaeresis) and `geïnteresseerd zijn in` (A2) are
  still the same combination written two ways.
- 136 empty English glosses (a0 28, a1 60, a2 48); all predate the audit.
- The 271 proposals have no art. `import-prepositions-band.py` cannot see them,
  so the game does not ship them.

## What is left for the owner

1. Decide whether any of the 271 proposals earn art.
2. Decide which bands the "three examples per chunk" target applies to
   (`CLAUDE.md` item 14; 636 chunks / 1,222 briefs).
3. Optionally regenerate the game data so the two A0/A1 gloss fixes reach the
   shipped band. Structurally safe (verified identical), but only on request.
4. The document scenes: no legible text remains, but six still use a document
   as visual shorthand. That judgement is still open.
5. `praten-tegen-gesloten-deur` still carries a "rename the id to
   praten-tegen-de-baby" instruction; `praten-tegen-muur`'s note still reads as
   a review remark, though its check question now answers `Nee` as it asks.
6. `tools/import-prepositions-band.py` matches only `class="kaart"`, so the one
   A0 card written `class="kaart sev-weak-picture"` (`letten-op-kind`, which has
   art) is silently left out of the game. Fixing it would ship that card; decide
   that before touching the regex.

## Parsing pitfalls in this repo

- `data-chunk` and `data-examples` are on `div.chunkgroep`, **not** on
  `<article class="kaart">`.
- 22 cards carry a second class (`kaart sev-weak-picture` ×20, `kaart
  sev-minor` ×2), so `class="kaart"` alone misses them. Match `kaart` anywhere
  in the class attribute.
- Do not split band pages on `</section>`; `a1.html` has 15 `<section
  class="cluster">` and 17 `</section>`. Split on `<section class="cluster"`.
- Grepping band pages for short numbers returns base64 image data. Strip
  `src="data:image/png;base64,…"` before searching, or scope the search.
- With `preserveAspectRatio="none"` art embedded as base64, compare card bodies
  with the `src` payload masked out, otherwise every card looks changed.
- The `grep` tool here silently fails on `\|` alternation. Use Python `re`.

## Commands used for this check

```sh
python3 tools/prepositions-pages.py check
python3 tools/prepositions-pages.py patch /tmp/vp_fixes.json --dry-run
python3 tools/build-prepositions-matrix.py
python3 tools/_vp_tmp/coverage.py
```

Everything else was ad-hoc Python: card and chunk diffs by id against
`git show HEAD:…`, per-band `data-examples` counts, empty-gloss counts, a
base64 decode of `praten-tegen-lege-stoel`'s embedded image, and an in-memory
`build_content()` run compared against the live JSON.
