# Voorzetselpaden — activity spec

Status: pilot, agreed 2026-11-06, built 2026-11-08, now a React game at
`client/src/games/prepositions/` with its content in
`server/Oefenpad.Resources/Games/Data/prepositions.json`.
Supersedes the "Preposition Playground" sketch in `games.md`. Canonical name:
**Voorzetselpaden** / **Preposition Paths**, per `designguide.md` and
`game-catalogue.md`.

This file is the spec and the reasoning. `prepositions-implementation.md`
describes the code as it shipped, including the fields that changed. Where the
two differ, the implementation doc is right.

The A0–A1 slice — twenty-eight chunks over ninety-one example scenes — is the
first slice of a larger curriculum.
`prepositions-roadmap.md` plans the path to 700 frames and B2, and states which
of those numbers are productive and which are receptive.

## The problem

A matching drill asks "which preposition follows this verb?". That tests a
pairing. It does not test meaning. `uitkijken naar` is not the sum of
`uitkijken` + `naar`; it means *to look forward to*. `uitkijken voor` means
something else. A learner who taps `naar` because it was on the card has not
learned either chunk.

The activity has two jobs:

1. teach what the chunk means in a situation, and
2. teach the form, including the separable prefix and the pronominal form.

## Design principle

**Make the situation the answer, and the preposition the consequence.**

- Teach chunks in **contrast sets**: `uitkijken naar` beside `uitkijken voor`,
  `denken aan` beside `denken over`.
- Use **scenes**, not translations, as the main carrier of meaning. English
  glosses are a fallback, per `decisions.md`.
- Ask a **concept question** that can only be answered if the learner understood
  the chunk: *positief of negatief?*, *nu of later?*, *wie doet het?*
- Only then ask for the form, with the prefix split.

## One path, four stops

The four modes share one dataset. A session is a short path, not four separate
games.

| Stop | Learner does | Feedback | Mode |
|---|---|---|---|
| **Ontdek** | Sees a scene, the sentence and the gloss once | None; this is input | R |
| **Kies het beeld** | Picks the scene that matches a sentence | Shows the sentence on the scene | R |
| **Klopt de zin?** | Says whether a sentence fits a scene; the false item is the contrast partner | Names the chunk that would fit, then asks a concept question | R |
| **Bouw de zin** | Builds the sentence from tiles, with the separable prefix at the end | Points at the misplaced prefix, not just "wrong" | P |

Optional warm-up: **Hetzelfde of anders?** — two sentences, same verb,
different preposition; same meaning or different? This is the cheapest way to
show that the preposition carries meaning. Not built.

Optional fifth stop: **Krimp** — transform a full sentence into its pronominal
form: *Ik denk aan jou* → *Ik denk eraan*; *Ik kijk uit naar de vakantie* → *Ik
kijk ernaar uit*. It uses the same scene and the `pronominal` field. This is
where the `er` + preposition chunk is learned. Not built; the shipped game
prints the pronominal form as a `Korter:` line on the Ontdek card instead.

### Example: `uitkijken naar` / `uitkijken voor`

**Ontdek.** Scene: a person with a suitcase, smiling at a calendar with a
circled day. Sentence: *Ik kijk uit naar de vakantie.* Gloss: *to look forward
to*. Then the second scene: a child at the curb, a car approaching. Sentence:
*Kijk uit voor de auto!* Gloss: *to watch out for*.

**Klopt de zin?**

| Scene | Sentence | Answer |
|---|---|---|
| Holiday calendar | Ik kijk uit naar de vakantie. | Klopt |
| Holiday calendar | Ik kijk uit voor de vakantie. | Klopt niet |
| Child at the curb | Kijk uit voor de auto! | Klopt |
| Child at the curb | Kijk uit naar de auto! | Klopt niet |

Then the concept questions: *Is het positief of negatief?* *Gaat het over nu of
later?* A learner can answer those without knowing the word "preposition".

**Bouw de zin.** Scene: holiday calendar. Tiles: `Ik` · `kijk` · `uit` · `naar` ·
`de` · `vakantie`. The frame is shown as two ghost slots, `uitkijken ____ ... ____`.
If `uit` lands next to `kijk`, the feedback is *"uit hoort achteraan"*.

## Session flow

A pilot session was scoped at about six minutes, across a contrast pair. As
shipped, a two-frame level is 8 scored answers (Ontdek is input and unscored),
`vragen` with three frames is 12, and a single-frame level — `ophouden`,
`zorgen`, `meedoen`, `zoeken`, `last hebben`, `houden van`, `zin in`,
`bang voor` — is 3; the table is the design intent, not a measurement.

| Step | Time | Items |
|---|---|---|
| Ontdek | 30 sec | 2 contrast scenes (3 in `denken`, which adds `eraan denken`) |
| Kies het beeld | 1 min | 2 sentences, 3 scene options each |
| Klopt de zin? | 2 min | 4 true/false items, all minimal pairs (6 in `vragen`); skipped when the level has no pair |
| Bouw de zin | 2 min | 2 sentences, one per accepted `bouw` line |
| Flitskaarten | 1 min | Not built; nothing is persisted |

The session ends on retrieval of the items the learner got wrong, not on new
material. That is the bridge to the mistakes queue in `game-catalogue.md`,
and it is still only a design.

## Progression

Do not start with `uitkijken naar`. Layer the difficulty:

1. **Non-separable, one frame** — `wachten op`, `denken aan`.
2. **Non-separable, two frames** — `denken aan` / `denken over`,
   `praten met` / `praten over`.
3. **Separable, one frame** — `ophouden met` (*Ik hou op met roken.*).
4. **Separable, two frames** — `uitkijken naar` / `uitkijken voor`.
5. **Pronominal** — `eraan denken`, `ernaar uitkijken`, `Waar denk je aan?`

Batch 2 adds three more pairs — `werken bij` / `werken aan`, `klaar met` /
`klaar voor`, `vragen aan` / `vragen om` — and four singles: `zorgen voor`,
`meedoen met`, `zoeken naar`, `last hebben van`. They use the same four stops;
the singles skip Klopt, so they have no concept question.

Batch 3 adds three more pairs — `blij met` / `blij voor`, `boos op` /
`boos over`, `klagen over` / `klagen bij` — and three singles: `houden van`,
`zin in`, `bang voor`. It also adds `vragen naar` to the existing `vragen`
level, making it the pilot's only three-frame set: three Kies items, six Klopt
items, three Bouw items. `vragen naar` names `vragen aan` as its one contrast
partner, because `vragen aan` and `vragen om` are already a pair.

`wachten op` / `wachten voor` is a useful side contrast: the first is the
idiomatic "wait for", the second is the spatial "wait in front of". It shows
that not every `voor` is a fixed chunk.

## Data model

The unit is a frame, not a verb: `wachten op`, not `wachten`. A scene is a
separate record so the alt text has a home and one image can serve more than one
frame. `scenes[].file` names a picture under `assets/voorzetselpaden/`.

The shipped shape — every field, and each place it differs from what this spec
proposed — is in `prepositions-implementation.md`. Read it there rather than
here; a second copy of the schema is how the two got out of step once already.

The decisions that still govern the data:

- **The frame carries its own `separable` and `prefix`.** There is no verb table
  in the pilot and no join at render time. If a shared verb table appears later,
  a checker has to keep the two consistent.
- **`contrast` points at another frame.** That single field is what lets the game
  generate a minimal-pair false item without a hand-written distractor list, and
  a `null` contrast is what removes the Klopt stop from a level.
- **A frame carries its accepted sentences as tokens.** One array per accepted
  sentence, so a separable frame can be practised on two persons without the
  engine knowing any grammar.

## Feedback rules

- In the practice modes, never reveal the gloss before the learner has answered
  the meaning question. Ontdek is the exception: it is the input card. The scene
  is the clue; the gloss is the confirmation.
- A wrong preposition is named, not just marked: *"Dit is `uitkijken voor`, niet
  `uitkijken naar`."*
- A misplaced separable prefix is a position error, not a vocabulary error:
  *"uit hoort achteraan."*
- A correct answer shows the scene, the full sentence, the chunk and the gloss
  together, so the form and the meaning are reconnected.
- `Klopt de zin?` must use the contrast partner as the false item. A random
  wrong preposition teaches nothing about this chunk.

## What the game checks

Shipped:

- **Kies het beeld** and **Klopt de zin?** are table lookups; no parsing.
- **Bouw de zin** compares token order and checks the position of the prefix
  separately. It does not share code with Zinsbouwer — that game does not exist
  yet, so only the tile-and-table approach carried over.
- A wrong answer names the frame it belongs to, never just "wrong".

Designed and not built:

- **Krimp** compares the learner's sentence with `pronominal.nl`; it is a
  fixed-answer transformation in v1.
- **Hetzelfde of anders?** compares two frame ids and their glosses.
- **Flitskaarten** stores misses by frame id, so a contrast pair stays together
  in the review queue.

## Scope and non-goals

- A0 and A1 ship twenty-eight chunks, each with two to four example scenes.
  That is the 30–50 chunk target of the survival-kit pillar as far as the first
  two bands reach; A2 (`Voorzetselpaden/a2.html`) is written but not yet drawn.
- No audio in v1. Listening is blocked by `decisions.md` open question 6.
- Not a full preposition table, and not a translation drill. The gloss is a
  fallback, never the main task.
- `aandenken` is a noun ("souvenir"), not a verb + preposition chunk. If it is
  wanted, it needs its own vocabulary card; it is not part of this set.
- `opbellen`, `aankomen` and other separable verbs without a fixed preposition
  belong to the verb/word-order work. They are useful preparation, but they are
  not frames in this activity.

## Open questions

- The stop bar hides the `Klopt de zin?` entry on a chunk without a contrast
  partner rather than dimming it. Three entries in a four-column habit is
  honest, but a learner who did another level first may read the gap as a bug.
- How many example scenes of one chunk should a session hold before it becomes
  repetition? The pilot ships two to four and does not answer this.
- The concept question was placed after the true/false answer. The shipped game
  asks it there, and only at the Klopt stop: a chunk with no contrast partner
  has no Klopt stop, so its concept question never appears. Worth revisiting
  when Krimp is built.
- Does the review queue need to keep contrast partners together, or is it enough
  to store the frame id and let the scheduler decide?

## Pilot images

The scene briefs are in `voorzetselpaden/a0-a2.html`, one card per frame. The images are delivered
and in place; two batch-1 images are flagged there for a redraw.
