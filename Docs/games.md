# Games for the Companion Website

The website's games are drills with a score, one per content pillar, and they
all read from one shared data file. This is the detail behind `todo.md` item 2
and the module list in `Concept.md`.

They live here, and not on bigtoe.games, for one reason: bigtoe.games treats
language as *presentation* — the same game in four locales, with the UI
translated. These games treat the language pair as the *content*. `wachten op`,
V2 word order and `winkel ≠ winkle` are facts about an English speaker learning
Dutch and are worth nothing in a Ukrainian build.

## The two first games

### Preposition Playground (🟠 Pillar 5)

Drag a verb to the preposition it takes — *wachten* **op**, *denken* **aan**,
*zorgen* **voor**. These are the part of Dutch that cannot be reasoned out and
has to be drilled, which is exactly what a game is for.

| | |
|---|---|
| Effort | Low-Medium. Two columns, drag-to-pair, a check pass |
| Data | `prepositions`: verb, preposition, English gloss, one example sentence |
| Done when | The common fifty are in, each with a plausible distractor |

Design notes: distractors must be prepositions a learner would *actually*
guess, usually the English-calque one (*wachten voor*, from "waiting for"), or
the drill teaches nothing. Reveal the example sentence on a correct pair, not
before. Order sets by frequency.

### Word Order Workshop (🔵 Pillar 7)

The game deals a verb, a tense and a subject — *eten* · past · *wij* — and the
player builds the sentence from a tray of word tiles. Check it, and the tiles
in the wrong place go back to the tray.

| | |
|---|---|
| Effort | Medium-High, and the highest-risk game here |
| Data | `verbs`: infinitive, conjugations by tense and person, strong/weak flag |
| Done when | ~20 high-frequency verbs work in present, past and perfect |

Checking a built sentence means either a conjugation table (bounded, dull,
correct) or parsing free text (unbounded, wrong). Take the table. Scope the
first version to twenty verbs — the data is the whole job, and it is easy to
start eight pillars and finish none.

Difficulty is how much is given: tiles in order → tiles shuffled → tiles plus
distractors → type it yourself. V2 and the "because kicks the verb to the end"
rule are the levels, not a lesson.

## Build order

| # | What | Why |
|---|---|---|
| 1 | Preposition Playground | Smallest data set, and Pillar 5 is already written up with examples |
| 2 | Word Order Workshop | Reuses the tile tray; needs the verb table |
| 3 | Everything else in `Concept.md` | Only after one game has been in front of a stranger |

`mvp.md` says one page, no backend, no accounts, deployed free, and shared into
an expat group to see whether strangers finish it. That still holds. Build the
first game that way and resist the shared layer — bigtoe.games and muziktools
already keep two copies of `i18n.js` and `common.js`, and they have drifted.

## The data file

One file, `grammar.js`, in the shape bigtoe.games uses for `words.js`: a plain
object on `window`, loaded before the game script, with a checker script that
fails if an entry is incomplete. Without the checker the bank rots silently.

```js
{ verb: 'wachten', prep: 'op',  en: 'to wait for',
  example: { nl: 'Ik wacht op de bus.', en: 'I am waiting for the bus.' } }
```

## Not here

**Story Dice** — eight picture dice, tell a story using all eight — stays on
bigtoe.games. It needs no grammar data and works in any language, so it is a
game that happens to suit learners rather than a learning game. Link to it from
here once it exists. Do not call it "Story Cubes": `RORY'S STORY CUBES` is a
registered US trademark owned by Asmodee. The dice-as-story-prompt mechanic is
free (US Copyright Office FL-108), the name is not.

## Naming conflict to settle

Three names exist for the same two games. `Concept.md`'s website module list
calls them **Preposition Playground** and **Word Order Workshop**; the concept
board (`quickwinsindutch_concept.png`) calls the decks **Preposition Paths**
and **Sentence Builder**. This doc currently uses the `Concept.md` names.

One game, one name, on the site and on the box. The board's names are the
better ones.
