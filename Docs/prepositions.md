# Voorzetselpaden — activity spec

Status: pilot, agreed 2026-11-06. Supersedes the "Preposition Playground" sketch
in `games.md`. Canonical name: **Voorzetselpaden** / **Preposition Paths**, per
`designguide.md` and `game-catalogue.md`.

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
show that the preposition carries meaning.

Optional fifth stop: **Krimp** — transform a full sentence into its pronominal
form: *Ik denk aan jou* → *Ik denk eraan*; *Ik kijk uit naar de vakantie* → *Ik
kijk ernaar uit*. It uses the same scene and the `pronominal` field. This is
where the `er` + preposition chunk is learned.

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

A pilot session should take about six minutes.

| Step | Time | Items |
|---|---|---|
| Ontdek | 30 sec | 2 contrast scenes |
| Kies het beeld | 1 min | 4 sentences |
| Klopt de zin? | 2 min | 6 true/false items, all minimal pairs |
| Bouw de zin | 2 min | 3 sentences, at least one separable |
| Flitskaarten | 1 min | The misses from this session |

The session ends on retrieval of the items the learner got wrong, not on new
material. That is the bridge to the mistakes queue in `game-catalogue.md`.

## Progression

Do not start with `uitkijken naar`. Layer the difficulty:

1. **Non-separable, one frame** — `wachten op`, `denken aan`.
2. **Non-separable, two frames** — `denken aan` / `denken over`,
   `praten met` / `praten over`.
3. **Separable, one frame** — `ophouden met` (*Ik hou op met roken.*).
4. **Separable, two frames** — `uitkijken naar` / `uitkijken voor`.
5. **Pronominal** — `eraan denken`, `ernaar uitkijken`, `Waar denk je aan?`

`wachten op` / `wachten voor` is a useful side contrast: the first is the
idiomatic "wait for", the second is the spatial "wait in front of". It shows
that not every `voor` is a fixed chunk.

## Data model

The unit is a frame, not a verb. Add a `frames` section to the shared
`grammar.js`:

```js
frames: [
  {
    id: 'uitkijken-naar',
    frame: 'uitkijken naar',
    verb: 'uitkijken',
    separable: true,
    prefix: 'uit',
    prep: 'naar',
    en: 'to look forward to',
    scene: 'uitkijken-naar-vakantie',
    example: {
      nl: 'Ik kijk uit naar de vakantie.',
      en: 'I am looking forward to the holiday.'
    },
    pronominal: {
      nl: 'Ik kijk ernaar uit.',
      en: 'I am looking forward to it.'
    },
    pronominalScene: null,
    contrast: 'uitkijken-voor',
    conceptQuestions: [
      { q: 'Gaat het over later?', a: true },
      { q: 'Is het positief?', a: true }
    ]
  },
  {
    id: 'denken-aan',
    frame: 'denken aan',
    verb: 'denken',
    separable: false,
    prefix: null,
    prep: 'aan',
    en: 'to think of',
    scene: 'denken-aan-persoon',
    example: {
      nl: 'Ik denk aan jou.',
      en: 'I am thinking of you.'
    },
    pronominal: {
      nl: 'Ik denk eraan.',
      en: 'I am thinking of it.'
    },
    pronominalScene: 'eraan-denken-afspraak',
    contrast: 'denken-over',
    conceptQuestions: [
      { q: 'Gaat het over een persoon?', a: true }
    ]
  }
]
```

Scenes are separate records so the alt text has a home and the same image can
be reused:

```js
scenes: [
  { id: 'uitkijken-naar-vakantie',
    file: 'art/uitkijken-naar-vakantie.svg',
    alt: 'Iemand met een koffer kijkt blij naar een kalender.' }
]
```

`scenes[].file` is relative to the activity folder, `src/voorzetselpaden/`.

`frames` repeats `separable` and `prefix` from the matching `verbs` entry so the
game does not have to join at render time; `frame.verb` matches
`verbs[].infinitive`. The checker must keep the two consistent. `contrast` points
at another frame; that field is what lets the game generate a minimal-pair false
item without a hand-written distractor list.

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

- **Kies het beeld** and **Klopt de zin?** are table lookups; no parsing.
- **Bouw de zin** checks token order and the exact position of the prefix. Use
  the same tile-and-table approach as Zinsbouwer; do not parse free text in v1.
- **Krimp** compares the learner's sentence with `pronominal.nl`; it is a
  fixed-answer transformation in v1.
- **Hetzelfde of anders?** compares two frame ids and their glosses.
- **Flitskaarten** stores misses by frame id, so a contrast pair stays together
  in the review queue.

## Scope and non-goals

- The pilot is ten frames, not the full 30–50. See `prepositions-art.md`.
- No audio in v1. Listening is blocked by `decisions.md` open question 6.
- Not a full preposition table, and not a translation drill. The gloss is a
  fallback, never the main task.
- `aandenken` is a noun ("souvenir"), not a verb + preposition chunk. If it is
  wanted, it needs its own vocabulary card; it is not part of this set.
- `opbellen`, `aankomen` and other separable verbs without a fixed preposition
  belong to the verb/word-order work. They are useful preparation, but they are
  not frames in this activity.

## Open questions

- Does **Bouw de zin** live inside Voorzetselpaden or call Zinsbouwer? The tile
  renderer should be shared; the activity and the data can stay separate.
- How many contrast sets should one session hold before it becomes a wall of
  scenes?
- Should the concept question come before or after the true/false answer? The
  current recommendation is after, so the learner judges the scene first.
- Does the review queue need to keep contrast partners together, or is it enough
  to store the frame id and let the scheduler decide?

## Pilot images

The first ten scene briefs are in `prepositions-art.md`.
