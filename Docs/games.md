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

### Voorzetselpaden (🟠 Pillar 5)

The first game is no longer a verb-to-preposition matching drill. Matching tests
whether the learner remembers a pair; it does not teach what the chunk means.
`uitkijken naar` is not "uitkijken + naar" — it means *look forward to*, and
`uitkijken voor` means something else. The activity therefore teaches the chunk
through a situation and a contrast, then asks for the form, including the
separable prefix.

One dataset, four stops on the path:

| Stop | What the learner does | Mode |
|---|---|---|
| Ontdek | Sees a scene + sentence + gloss, unscored | R |
| Kies het beeld | Picks the scene that matches a sentence | R |
| Klopt de zin? | Says whether a sentence fits a scene; the false item is the contrast partner | R |
| Bouw de zin | Builds the sentence from tiles, with the separable prefix at the end | P |

Optional warm-up: **Hetzelfde of anders?** — two sentences, same verb, different
preposition; same meaning or different?

Optional extension: **Krimp** — rewrite a sentence with `er` + preposition
(*Ik denk aan jou* → *Ik denk eraan*).

| | |
|---|---|
| Effort | Medium. The tile tray is shared with Zinsbouwer; the new work is scenes, contrast pairs and the split-sentence check |
| Data | `frames`: frame, verb, separable, prefix, prep, English gloss, scene, sentence, pronominal form, contrast partner, concept questions |
| Done when | Twenty-eight levels — ten A0 chunks and eighteen A1 chunks, each with two to four example scenes — work through the stops without needing the English gloss |

The full spec, including the data shape, feedback rules and the pilot image
list, is in `prepositions.md` and `voorzetselpaden/a0-a2.html`.

### Zinsbouwer (🔵 Pillar 7)

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
| 1 | Voorzetselpaden | Smallest dataset, and Pillar 5 is already written up; the pilot is ten frames |
| 2 | Zinsbouwer | Reuses the tile tray; needs the verb table |
| 3 | Everything else in `Concept.md` | Only after one game has been in front of a stranger |

`mvp.md` says one page, no backend, no accounts, deployed free, and shared into
an expat group to see whether strangers finish it. That still holds for the MVP
as written. Build the first game that way and resist the shared layer —
bigtoe.games and muziktools already keep two copies of `i18n.js` and `common.js`,
and they have drifted.

> Later state (2026-11-09): the site outgrew this. There are now six games, a
> .NET host serves them from `/spelen/`, and their content and puzzle generation
> live server-side so the JS cannot be copied into a clone. `Docs/games-backend.md`
> is the current architecture. The advice below is the MVP-history, not the plan.

## The data file

One file, `grammar.js`, in the shape bigtoe.games uses for `words.js`: a plain
object on `window`, loaded before the game script, with a checker script that
fails if an entry is incomplete. Without the checker the bank rots silently.

```js
{ frame: 'uitkijken naar', verb: 'uitkijken', separable: true, prefix: 'uit',
  prep: 'naar', en: 'to look forward to', scene: 'uitkijken-naar-vakantie',
  example: { nl: 'Ik kijk uit naar de vakantie.',
             en: 'I am looking forward to the holiday.' } }
```

The full frame shape, including `contrast`, `pronominal` and `conceptQuestions`,
is in `prepositions.md`.

## Not here

**Story Dice** — eight picture dice, tell a story using all eight — stays on
bigtoe.games. It needs no grammar data and works in any language, so it is a
game that happens to suit learners rather than a learning game. Link to it from
here once it exists. Do not call it "Story Cubes": `RORY'S STORY CUBES` is a
registered US trademark owned by Asmodee. The dice-as-story-prompt mechanic is
free (US Copyright Office FL-108), the name is not.

## Naming

`designguide.md` and `game-catalogue.md` are canonical: **Voorzetselpaden**
(Preposition Paths) and **Zinsbouwer** (Sentence Builder). This doc previously
used Preposition Playground and Word Order Workshop; those names are retired.
