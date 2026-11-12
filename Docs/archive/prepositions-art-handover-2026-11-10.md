# Voorzetselpaden art plan — handover

9 November 2026, revised 10 November. Read `prepositions-roadmap.md` for the
curriculum and `game-art.md` for the drawing rules. `preposition-review-findings-2026-11-10.md`
is the audit this revision came from.

## What this is

The prepositions game shipped with 30 frames. The roadmap takes it to 710
(A0–A2 50, B1 200, B2 460). Three art plans now hold the missing frames as
copy-paste Grok batches of ten. **All 680 planned frames govern a preposition**
(the fused-preposition frames `ten slotte` and `ten einde te` were replaced on
10 November), so every batch is ready to send.

| File | State |
|---|---|
| `Docs/prepositions-art-a0-a2.md` | 20 new frames, done |
| `Docs/prepositions-art-b1.md` | 200 frames, done; 29 replaced 10 Nov |
| `Docs/prepositions-art-b2.md` | 460 frames, re-synced and extended 10 Nov |
| `Docs/prepositions-roadmap.md` | The 710-frame ladder |

Nothing had been drawn or sent to Grok when this handover was written. The game
JSON (`server/Oefenpad.Resources/Games/Data/prepositions.json`) held 30 scenes
and 18 levels, nothing was committed, and `main` was 9 commits ahead.

**Update, 10 November (evening).** The A0–A2 batch (`prepositions-art-a0-a2.md`,
20 frames) was drawn and shipped: the masks are in `assets/voorzetselpaden/`, the
JSON now has **50 scenes, 50 frames and 33 levels**, and a review sheet is built
by `tools/build-prepositions-sheet.py`. The B1 and B2 plans are still undrawn.

## The rule for a frame

It must be a chunk that governs a preposition — verb (`letten op`), adjective
(`bang voor`), noun (`zin in`) or a fixed idiom. Not a bare verb, not a free
adjunct (`zonder afspraak`), not a greeting (`tot ziens`). Both were removed
for this reason.

A pronominal adverb counts. `erover nadenken`, `eraan toe zijn`,
`ergens naartoe`, `waar … vandaan` and `ergens klaar mee zijn` carry their
preposition fused into `er…`, `daar…` or `waar…` rather than standing before a
noun. Roadmap §6 budgets 40 frames for them, so they are in scope and a
"has a preposition?" scan must whitelist them. Eight such frames exist today:
seven in B1-07 and `ergens klaar mee zijn` (B2 #403).

## What was done on 10 November

The audit in `preposition-review-findings-2026-11-10.md` found three classes of fault and
the owner settled the three policy questions the same day.

| Fix | Where |
|---|---|
| 12 duplicated tracker Scene cells copied back from the blocks | B1 |
| 17 batch blocks synced to their tracker frame and filename | B2 |
| 2 batch summaries that counted an eleventh subject (B2-13, B2-26) | B2 |
| 10 tracker Scene cells that described a different scene than the block | B2 |
| 29 bare separable verbs replaced by real preposition chunks | B1 |
| `ten slotte` ×2 replaced by `ten laste van` (#46) and `gebaseerd zijn op` (#450) | B2 |
| New batch B2-46: the nine prepositions no frame had ever used | B2 |

**The 29 B1 separables are gone.** B1-08 was rebuilt whole as the
high-frequency everyday chunks the set was missing (`gaan naar`, `wonen in`,
`kiezen voor`, `twijfelen tussen`, `hopen op`, `zich zorgen maken over`,
`betalen voor`, `uitgeven aan`, `vertrouwen op`, `bellen met`), and nineteen
more were replaced in B1-11…B1-20. The prefix material moved to the
**Uit Elkaar** game idea in `suggestions.md`, which now carries the word list.
Roadmap batch 8 and the B1 "What B1 adds" table were changed to match.

Replacing a frame is four edits, not one: the tracker row, the batch subject
block, the CONTRAST PAIRS line, and every other row whose Pair/note names it.
Ten neighbouring notes were repointed this way (#105, #119, #134, #159, #174,
#185 in B1, plus four CP prose lines in B2). B1-08's prompt preamble also still
told the artist to match the separable *prefix*; its TASK and VALIDATION text
is now the standard preposition wording.

**B2-46 closes the coverage gap.** `zonder`, `vanwege`, `gezien`, `richting`,
`per`, `aangaande`, `betreffende`, `jegens` and `overeenkomstig` had no frame
anywhere; ten new frames teach them the way B2-44 teaches `sinds` and `tijdens`.
B2 is 460 frames in 46 batches, and the roadmap gained a batch 32 for it.

`ten einde te` (#43) was the last fused-preposition frame after `ten slotte`; it
was replaced by `ten dienste staan van`, which keeps B2-05's `ten … van` theme
and governs its `van`.

`tot` still has no frame below B2 — its first is B2 #13 `zich richten tot`, and
all 18 of its frames are B2. `via` appears only inside `verspreiden via`.
Neither is a blocker; both are recorded in roadmap §7.

Two decisions the owner has given, kept here because they are easy to re-open:

1. Keep the B1-01/02 spatial frames and B2-44 (`behalve`, `sinds`, `tijdens`,
   `volgens`, `wegens`, `ondanks`) despite roadmap §11 excluding free use.
   They are the only frames teaching those words. B2-46 follows the same logic.
2. Keep B2's ~68 separable-prefix chunks (`aandacht vragen voor`). They govern
   real prepositions, so they are legal frames; only bare separables were cut.

## Checking an edit

```sh
F=Docs/prepositions-art-b2.md
grep -c '^````' $F            # must be 2 × number of batches
awk -F'|' '/^\| [0-9]+ \|/ && $2 ~ /^ *[0-9]+ *$/ {c++} END{print c}' $F
awk -F'|' '/^\| [0-9]+ \|/ && $2 ~ /^ *[0-9]+ *$/ {f=$3; gsub(/^ +| +$/,"",f); print f}' $F | sort | uniq -d
```

B2 currently: 460 rows, 46 batches, 92 fences, no duplicate filenames and no
tracker↔block mismatches. B1: 200 rows, 20 batches, 40 fences, no duplicate
Scene cells. Across all three files there are no duplicate filenames and no
no-preposition rows once the pronominal forms and `tegenover` are whitelisted.
`preposition-review-findings-2026-11-10.md` has the parser notes for re-running the
tracker↔block and no-preposition checks.

## Traps

- Files are long; find `## Batch` line numbers with `grep -n` and read with
  `sed -n 'A,Bp'`. Edit only with exact matches.
- Batch prompts use four-backtick fences. An unbalanced fence breaks the
  copy-paste block without warning.
- Keep the tracker row and the batch subject block identical — B2 was broken
  because only one side got updated.
- Filenames are ASCII; chunk text keeps its diacritics.
- A new scene is easy to write against the house style. Two drafts this round
  had to be redone: one distinguished two cloths by stripe pattern, which
  `game-art.md` forbids (no hair, clothing pattern or fingers), and one named
  a subject as a pair member in one line and a single in the next.
- A scene must not duplicate an existing one. Check the Scene column for the
  same prop before writing — a wall clock was proposed for #454 when
  `binnen-de-gestelde-termijn` already owns it.
- Never claim a check passed without running it.
