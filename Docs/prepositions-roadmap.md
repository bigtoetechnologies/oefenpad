# Voorzetselpaden — curriculum roadmap

Status: planning document, 9 November 2026. This extends the pilot spec in
`prepositions.md` from the thirty-frame pilot to a **700-frame** curriculum. It
changes no shipped code and settles no product decision on its own. Where this
file and `prepositions.md` disagree about the game as built, `prepositions.md`
and `prepositions-implementation.md` win.

Two things it does decide:

1. **The count.** 700 is the **receptive** ceiling — the number of chunks a
   learner should recognise and understand at B2. The **productive** target is
   smaller: roughly 250–400 chunks actually produced in speech.
2. **The shape.** The first ~400 frames get the full four-stop loop. The last
   ~300 are receptive-first and may ship without `Bouw de zin`.

The numbers are estimates. The repo contains no frequency list and no CEFR
chunk count; CEFR does not define one either. Order them by frequency before
trusting the batch boundaries.

---

## 1. Two different counts

Do not conflate the closed class with the chunks built on it.

| What is counted | Dutch total | What it means |
|---|---|---|
| Preposition **words** | ~25 core, ~40–45 including formal | `aan, achter, bij, binnen, boven, buiten, door, in, langs, met, na, naar, naast, om, onder, op, over, rond, sinds, tegen, tussen, uit, van, vanaf, voor, zonder` plus `tijdens, volgens, wegens, ondanks, behalve, vanwege, via, richting, per, gezien, aangaande, betreffende, jegens, overeenkomstig` |
| Verb / adjective / noun + preposition **frames** | 1,000+ fixed combinations | `beschikken over`, `trots op`, `behoefte aan`. The game's unit |

The shipped A0–A2 set already uses **13** of the core prepositions across its
**50 frames**: `aan, bij, door, in, met, naar, om, op, over, tegen, uit, van,
voor`. So the word inventory is not the work. The chunk inventory is.

## 2. What the numbers mean

| Target | Productive (speaking) | Receptive (reading, listening) |
|---|---|---|
| A2 survival kit | ~40–50 | ~80 |
| B1 | ~100–150 | ~250 |
| **B2** | **~250–400** | **~500–700** |

`Docs/Concept.md` commits only to **30–50 chunks** for the survival-kit pillar.
That is an A2 target, not a B2 one. The 700 in this file is the top of the B2
receptive band; 500 is the floor.

The reconciliation with the batch plan below:

- **Phases A–C** build about **400** frames with the full loop, meaning and form
  both scored. That covers the productive B2 band (250–400).
- **Phases D–E** add about **300** more, receptive-first. They extend what the
  learner understands, not what they must produce.

## 3. Where the pilot sits

| | Shipped |
|---|---|
| Frames | 50 |
| Levels | 33 (twelve pairs, two sets of three, nineteen singles) |
| Prepositions governed as frames | 13 |
| Scenes | 50 raster masks |
| CEFR band | A0–A2 |

Batch 4b (`Docs/voorzetselpaden/a2-pairs.html`) is drawn but not yet integrated. When
it ships it takes the set to **66 frames, 36 levels, 23 pairs, three sets of
three, ten singles and 13 prepositions**, as recorded in that file.

The shipped 50 are concentrated at the bottom of the ladder. They are roughly
**7%** of the 710 target and about **12%** of the productive B2 band. The
remaining build is **660 frames**, not ~120.

## 4. The cumulative ladder

Read as “by the end of this band the learner controls this many distinct
chunks”, counted from zero.

| Band | Cumulative chunks | What is added | Roadmap batches |
|---|---|---|---|
| A0 → A1 | 15–25 | Survival: `wonen in`, `gaan naar`, `komen uit`, `kijken naar`, `praten met`, `houden van`, `zin in` | 1–3, 4b (planned) |
| A1 → A2 | 40–50 | Everyday `op/aan/voor/van`, first contrast pairs, separable basics | 1–4b |
| A2 → A2+ | ~147 | `tegen, door, uit, zonder, tot`; the spatial set; adjective and noun chunks; pronominal adverbs | 4b–8 |
| A2+ → B1 | ~267 | High-frequency verb + preposition | 9–13 |
| B1 → B1+ | ~417 | Reflexive chunks, multi-word prepositions, formal verb chunks, contrast at scale, work register | 14–23 |
| B1+ → B2 | ~567 | Low-frequency vocabulary, idioms, business and academic register | 24–27 |
| B2 → B2+ | ~667 | Medical, legal, journalistic and opinion | 28–30 |
| B2+ / C1 doorway | **726** | Colloquial, literary and consolidating frames, exceptions, coverage close-out | 31–32 |

## 5. Batch plan to 710

Batches 1–4 are shipped and 4b is planned. Each later batch is one content
production unit, sized to what one reviewer can vet in a session. `Δ` is frames
added; `Σ` is the cumulative total.

| Batch | Theme | Δ | Σ | Band |
|---|---|---|---|---|
| 1–3 | Pilot: ten contrast sets, eight singles | 30 | 30 | A0–A2 |
| **Phase A — everyday expansion** | | **100** | **130** | A2 → A2+ |
| 4 | `tegen`, `door`, `uit`, `zonder`, `tot` — shipped | 20 | 50 | A2 |
| 4b | A2 pair enhancement: same-verb and same-preposition contrasts — drawn | 16 | 66 | A2 |
| 5 | Spatial: `tussen`, `onder`, `boven`, `naast`, `achter`, `langs` | 20 | 70 | A2+ |
| 6 | Adjective + preposition, core | 20 | 90 | A2+ |
| 7 | Noun + preposition, core | 20 | 110 | A2+ |
| 8 | Pronominal adverbs and high-frequency everyday chunks | 20 | 130 | A2+ |
| **Phase B — B1 floor** | | **120** | **250** | A2+ → B1 |
| 9 | High-frequency verb + preposition I | 25 | 155 | B1 |
| 10 | High-frequency verb + preposition II | 25 | 180 | B1 |
| 11 | High-frequency verb + preposition III | 25 | 205 | B1 |
| 12 | Adjective + preposition II | 25 | 230 | B1 |
| 13 | Noun + preposition II | 20 | 250 | B1 |
| **Phase C — B1+ breadth** | | **150** | **400** | B1 → B1+ |
| 14 | Reflexive and idiomatic chunks | 25 | 275 | B1+ |
| 15 | Multi-word prepositions | 25 | 300 | B1+ |
| 16 | Formal verb + preposition | 25 | 325 | B1+ |
| 17 | Contrast pairs at scale | 25 | 350 | B1+ |
| 18 | Double prepositions and choice | 25 | 375 | B1+ |
| 19 | Work register | 25 | 400 | B1+ |
| **Phase D — B2 receptive breadth** | | **150** | **550** | B1+ → B2 |
| 20 | Low-frequency verb + preposition | 25 | 425 | B1+ |
| 21 | Low-frequency adjective + preposition | 25 | 450 | B1+ |
| 22 | Low-frequency noun + preposition | 25 | 475 | B1+ |
| 23 | Idioms with fixed prepositions | 25 | 500 | B1+ |
| 24 | Business and administration | 25 | 525 | B2 |
| 25 | Academic and formal | 25 | 550 | B2 |
| **Phase E — B2+ receptive** | | **150** | **700** | B2 → B2+ |
| 26 | Medical and technical | 25 | 575 | B2 |
| 27 | Legal and official | 25 | 600 | B2 |
| 28 | Journalistic and opinion | 25 | 625 | B2 |
| 29 | Colloquial and regional | 25 | 650 | B2 |
| 30 | Literary and idiomatic | 25 | 675 | B2 |
| 31 | Consolidation and exceptions | 25 | 700 | B2+ |
| **Close-out** | | **10** | **710** | B2+ |
| 32 | Unframed prepositions: `zonder`, `vanwege`, `gezien`, `richting`, `per`, `aangaande`, `betreffende`, `jegens`, `overeenkomstig` | 10 | 710 | B2+ |

29 new batches, 680 new frames, 710 in total. With batch 4b that becomes **30
new batches, 696 new frames and 726 in total**. At the current maximum of three
frames per level that is roughly **250–300 levels**.

Batch 8 was planned as pronominal adverbs plus separable-prefix frames. A
separable verb governs no preposition, so the 29 separable frames drafted for
it and for batches 9–13 were cut on 10 November 2026 and the prefix material
moved to the **Uit Elkaar** game idea in `suggestions.md`. Batch 8 keeps the
pronominal adverbs; the freed slots went to high-frequency everyday chunks the
set was missing (`hopen op`, `uitgeven aan`, `bellen met`, …). Three of the
originally drafted chunks — `gaan naar`, `kiezen voor` and `betalen voor` — are
also drawn in batch 4b. Each of the three is drawn in a different scene in each band, so only the chunk
repeats; `kiezen voor` (cake over an apple in 4b) cannot be mistaken for its A2+
partner, while the other two differ only in place or object. One of three
resolutions must be chosen before A2+-08 is drawn: keep both scenes and put each
chunk in a level apart from its 4b partner (no new art); drop the three A2+ rows
and plan three replacements from the B1 and B1+ chunks (band stays at 80); or
point the three rows at the 4b art (they become documentation, not frames).
Until then the three rows stay planned. This text moved here from the A2+ page
on 12 Nov 2026, when the old Markdown prose was taken off the band pages. `tussen` was going to move
from batch 5 to 4b; it stays in batch 5 now that `kiezen tussen` has been
dropped from 4b.

Batch 32 exists because phases D and E named nine prepositions that no frame
ever used. It is a coverage close-out, not new curriculum.

Batch 4b adds 16 frames at A2. The `Σ` column below batch 4 is therefore **16
higher** than the table shows: batch 5 is 86, batch 8 is 146, batch 13 is 266,
batch 19 is 416, batch 25 is 566 and the close-out is **726**, not 710. `Δ`
values are unchanged. The extra 16 come out of the same A2 budget, so the 710
in this file's title is now a floor rather than a ceiling.

The image plans were split into six pages on 10 November 2026 so that each
step is smaller, and are now HTML pages in `Docs/voorzetselpaden/`: `a0-a2.html` (batch 4, with the 30 pilot frames), `a2-pairs.html`
(4b), `a2-plus.html` (5–8, 80 frames), `b1.html`
(9–13, 120 frames), `b1-plus.html` (14–23, 250 frames) and
`b2.html` (24–32, 210 frames). `index.html` there is the overview. The batch numbers in this roadmap
are unchanged; only the `Band` column and the page names follow the split. The
`Band` values map to the files one-to-one: A2 → a0-a2 and a2-pairs, A2+ →
a2-plus, B1 → b1, B1+ → b1-plus, B2 → b2.

## 6. Composition of the 710

| Category | Frames | Example |
|---|---|---|
| Verb + preposition | 350 | `beschikken over`, `afhangen van`, `bijdragen aan` |
| Adjective + preposition | 110 | `trots op`, `afhankelijk van`, `gewend aan` |
| Noun + preposition | 100 | `behoefte aan`, `kans op`, `moeite met` |
| Pronominal adverbs | 40 | `eraan`, `ernaar`, `waar…aan`, `daar…over` |
| Multi-word / prepositional expressions | 50 | `met betrekking tot`, `in verband met`, `op basis van` |
| Idioms and fixed expressions | 50 | `op de hoogte zijn van`, `rekening houden met` |
| Bare prepositions taught as free use | 10 | `zonder`, `vanwege`, `richting`, `jegens` |
| **Total** | **710** | |

The last row is batch 32 and is the one category that is not a chunk. These
words govern nothing, so the only way to teach them is the situation they turn
up in; §11 excludes free use everywhere else.

The register batches (19, 24–31) are a cross-cut: they draw from the categories
above rather than adding a seventh category. Do not count them twice.

## 7. Preposition coverage

A sanity check on breadth. “Introduced” means the preposition first appears as a
governed frame, not merely as a prefix or inside a fixed expression.

| Phase | Prepositions introduced | Running total |
|---|---|---|
| Pilot (1–3) | `aan, bij, in, met, naar, om, op, over, van, voor` | 10 |
| 4 (shipped) | `tegen, door, uit` | 13 |
| 4b (drawn) | none — `kiezen tussen` was cut | 13 |
| A (4b–8) | `tussen, zonder, tot, onder, boven, naast, achter, langs, binnen, buiten, na, rond, vanaf` | 26 |
| B (9–13) | none — the verb chunks reuse the prepositions above | 26 |
| C (14–19) | `sinds, tijdens, volgens, wegens, ondanks, behalve` | 32 |
| D (20–25) | `vanwege, via, richting, per, gezien` | 37 |
| E (26–31) | `aangaande, betreffende, jegens, overeenkomstig, met inbegrip van, ten opzichte van` | 43 |

| Close-out (32) | the nine of D–E that no frame used: `zonder`, `vanwege`, `gezien`, `richting`, `per`, `aangaande`, `betreffende`, `jegens`, `overeenkomstig` | 43 |

By the end of phase C the learner has productive frames for every core
preposition. Phases D–E are about register and rarity, not new grammar.

The phase rows above say where a preposition is *introduced in the plan*. An
audit on 10 November 2026 found that nine of them had no frame anywhere in the
art plans, `zonder` included, and that `via` appears only inside
`verspreiden via`. Batch 32 frames the nine. `via` is still single-sourced.

## 8. What changes in the engine

The game now ships 91 example scenes across 28 levels (A0 and A1). 700 needs
these changes.
None of them are in `prepositions-implementation.md` yet.

| Change | Why |
|---|---|
| Split `prepositions.json` by phase or batch | A 700-frame single file is unreviewable and slow to load. One file per phase, merged into the server-side `GameContent` catalog at load |
| Add `band` (`A2`/`A2+`/`B1`/`B1+`/`B2`/`B2+`) to levels | Lets the UI order and gate content without hard-coded level arrays |
| Add `register` (`everyday`/`work`/`academic`/`legal`/`medical`/`colloquial`/`literary`) to frames | A chunk can be correct and still wrong for the situation; the feedback should say so |
| Make `Bouw` conditional, like `Klopt` | Receptive-only frames have no accepted-sentence list. Skip Bouw when `bouw` is absent instead of rendering an empty step |
| Add a `sense` key where a frame string repeats | `werken aan` (a project) and `werken bij` (an employer) should not collide; two frames may share a label but not an id |
| Give receptive-only frames a second exercise type | `Kies` is one item per frame. A 25-frame batch with no contrast and no Bouw is 25 taps and no feedback loop. Either pair them or add a meaning-matching mode |
| Build `Krimp` as a stop | Pronominal adverbs are 40 frames and a core B2 skill. Today the form is a `Korter:` line on Ontdek |
| Persist misses by frame id | 700 frames without a review queue is a dictionary. The mistakes queue in `game-catalogue.md` is the feature |

`contrast` stays the only source of a false item. Do not add random
distractors to make the later batches work; a random wrong preposition teaches
nothing, per `prepositions.md`.

## 9. What happens to the art

710 scenes is not a plan; it is a decade. The pilot already uses raster, which
`game-art.md` calls a placeholder. For this volume:

All six slices are planned, as pages in `Docs/voorzetselpaden/`: `a0-a2.html` has one card for each of the twenty
batch-4 frames and two copy-paste Grok prompts, `a2-pairs.html`
one card for each of the sixteen batch-4b frames, `a2-plus.html` the 80 A2+ frames,
`b1.html` the 120 B1 frames, `b1-plus.html` the
250 B1+ frames and `b2.html` the 210 B2 frames.

| Phase | Frames | New scenes (est.) | Strategy |
|---|---|---|---|
| A | 100 | 50 | One scene per contrast pair, plus one per distinct situation |
| B | 120 | 50 | Reuse everyday scenes; add only where the situation is new |
| C | 150 | 50 | Register scenes reused across chunks (an office, a counter, a clinic) |
| D | 150 | 35 | Register-generic scenes; abstract or symbolic for formal chunks |
| E | 150 | 30 | Reuse the register set; only exceptions get new art |
| Close-out | 10 | 0 | Reuse the register set; bare prepositions need no new scene |
| **Total** | **680 new** | **~215 new (≈245 with pilot)** | |

Three consequences:

- **Return to SVG** for all new art. Raster was a pilot decision; `game-art.md`
  already says new art starts as SVG. Hundreds of redraws in raster is not
  maintainable.
- **Scene reuse becomes a data rule, not an accident.** A scene may serve
  several frames; the data model already allows it (`scenes` is separate from
  `frames`).
- **The meaning-first promise weakens in phases D–E.** A formal chunk like
  `aangaande` has no honest silhouette. Flag those as gloss-and-context frames
  rather than pretending a picture carries the meaning.

## 10. Session, study time and assessment

- A two-frame level is 8 scored answers, roughly six minutes. 250–300 levels is
  about **25–30 hours** of first-pass play, before review.
- At 5–10 new chunks a day, 700 chunks is **70–140 days** of study. That is a
  realistic B2 timeline for an adult learner, not a content defect.
- **This game does not assess speaking.** It trains recognition and written
  production. B2 *speaking* also needs audio, pronunciation and free output,
  which `game-catalogue.md` lists as gaps. Do not claim the 700 closes them.

## 11. What the 700 does not include

- Free spatial and temporal use (`op tafel`, `in de kast`, `na de les`). That is
  grammar and vocabulary, not chunk learning.
- Preposition stranding and word order beyond the frame.
- Audio, pronunciation or listening.
- Free speaking or interaction.
- Every fixed combination in Dutch. The universe is 1,000+; 700 is a B2 slice.

## 12. Sequencing rules

1. **Frequency before completeness.** Order every batch by corpus frequency,
   not by alphabetical neatness. If a frequency list arrives, re-cut the
   batches around it.
2. **Contrast before single.** A pair teaches meaning; a single teaches form.
   Spend the extra art and data on pairs.
3. **One new preposition per level.** Do not introduce two new prepositions and
   a new verb in the same level.
4. **Recycle older frames as options.** Later batches should draw distractors
   from earlier prepositions, not only from the immediate contrast partner, or
   the learner learns the pair and nothing else.
5. **Register last.** A learner who cannot produce `wachten op` does not need
   `aangaande`.

## 13. Open questions

- **Product scope.** `game-catalogue.md` states the target level as A1 → B1.
  This roadmap runs to B2. That is a product decision for the owner, not a doc
  edit: does Voorzetselpaden own B2, or does it stop at B1 and leave B2 to
  reading and speaking work?
- **Ship all 700, or build to 400 and stop?** Phases D–E are receptive and
  expensive to vet. The productive B2 band is complete at the end of phase C.
- **Where does the frequency order come from?** No list exists in the repo.
  SUBTLEX-NL or an NT2 lemma list would settle the batch boundaries.
- **Do receptive-only levels need a new exercise type?** `Kies` alone is too
  thin, and a single frame has no `Klopt`.
- **Does the mistakes queue gate release?** Without it, 700 frames is browsing,
  not learning.
- **Art budget.** ~215 new scenes is still large. Which phases may use one
  scene across several chunks, and who signs that off?

## 14. References

| File | Relationship |
|---|---|
| `prepositions.md` | The activity spec and the design reasoning. Canonical for intent |
| `prepositions-implementation.md` | The shipped code and where the data model diverged from the spec. Canonical for behaviour |
| `voorzetselpaden/index.html` | The scene briefs and art rules, one page per CEFR band |
| `game-catalogue.md` | Learning goals, modes, and the stated A1 → B1 target |
| `Concept.md` | The 30–50 chunk survival-kit commitment and the pillar list |
| `decisions.md` | Non-negotiables: Dutch UI, meaning in pictures, glosses as fallback |
