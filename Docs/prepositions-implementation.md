# Voorzetselpaden — how it is built

The game as shipped: thirty-three levels, four stops (three in a single-frame
level). The React page is `client/src/games/prepositions/`; the levels, frames,
scenes and sentences are in
`server/Oefenpad.Resources/Games/Data/prepositions.json`, and the rules that
build the four steps and judge every answer are in
`server/Oefenpad.Services/Games/PrepositionsService.cs`. `prepositions.md` is
the activity spec and the reasoning; `game-art.md` is how the images are drawn;
this file is the code.

Read this before changing the JSON or adding a level. Several fields the
spec proposed did not survive contact with the engine, and the differences are
listed below rather than left to be rediscovered.

## Files

| File | What it holds |
|---|---|
| `client/src/games/prepositions/PrepositionsGame.tsx` | The React page: the stop bar, the four renderers, the level list |
| `server/Oefenpad.Resources/Games/Data/prepositions.json` | `scenes`, `frames`, `levels`. Content only, no logic |
| `server/Oefenpad.Services/Games/PrepositionsService.cs` | The step engine, the options, the judging, the view |
| `client/src/styles/source/prepositions.css` | A thin layer over `assets/site/oefenpad.css`; tokens only, no new colours |
| `assets/voorzetselpaden/*.png` | Fifty alpha masks, 512 × 763, one per scene |

`GameShell` supplies the `.balk` / `.spel-kop` / `.voet` chrome and the theme
toggle. The browser never sees the frames, the contrast partner or the tile
order; the service sends one card at a time and judges every answer.

There is no `grammar.js` and no `verbs` table. The spec assumed both; the pilot
does not need them.

## The data, as shipped

```js
{
  scenes: { '<scene-id>': { file, alt } },
  frames: [ { id, frame, en, scene, contrast, focus, example: { nl, en },
              build: [[token, …], …], concept: [{ question, answer }],
              separable, prefix, pronominal, pronominalScene, discoverOnly } ],
  levels: [ { id, name, frames: [frameId, …], extra: [frameId] } ]
}
```

A **frame** is one verb, adjective or fixed expression plus its preposition —
`wachten op`, `klaar met`, `last hebben van` — not a bare word. A **level** is
one such word's contrast set, usually a pair; `vragen` and `praten` are sets of
three, and the other nineteen levels are sets of one. The level is what the
learner picks.

### Where it diverged from the spec

| Spec (`prepositions.md`) | Shipped | Why |
|---|---|---|
| `verb`, `prep` separate fields | One `frame` string, plus `focus[]` | Nothing joins on the verb. `focus` is the list of words the UI underlines — the preposition and, for a separable verb, the prefix |
| `conceptQuestions` | `concept` | Renamed for brevity; same shape |
| `pronominalScene` on every frame | Kept on `denken-aan` only | The engine never reads it. `eraan-denken` is its own frame with its own scene |
| — | `bouw: [[token, …], …]` | One array per accepted sentence, see below |
| — | `discoverOnly` | Marks `eraan-denken` as input-only |
| — | `levels[]` | The session order, which the spec described in prose |
| `contrast` always set | `null` on the single-frame levels | A single frame has no contrast partner, and that null is what removes the third stop |
| `separable` on every frame | `true` + `prefix` on separable frames only | Absence means not separable; `false` and `null` are not used |

`separable` is read by nothing. It records the fact for a human; the engine
keys off `prefix`.

### Why `bouw` is a list of sentences

`ophouden met` was the first frame with two entries; the four singles added with
batch 2 (`zorgen voor`, `meedoen met`, `zoeken naar`, `last hebben van`) follow
the same pattern. `ophouden met` looks like this:

```js
bouw: [['Ik', 'hou', 'op', 'met', 'roken'], ['Zij', 'houdt', 'op', 'met', 'roken']]
```

A separable prefix is a word-order rule, and one person is one data point. Two
persons give the learner the same *op … met*-frame twice with a different verb
form, so the position is what is being learned rather than a memorised string.
Each entry becomes its own Bouw item; the two are never shown side by side.

For a single-frame level this is not optional polish: it is what gives the level
three scored answers (1 Kies + 2 Bouw) instead of two. Adding a second sentence
to any other frame is a one-line change with no engine work.

### The fields that do the work

| Field | Used by | Effect |
|---|---|---|
| `contrast` | `bouwStappen`, Klopt | Names the only wrong sentence allowed in Klopt. `null` removes the stop |

In a two-frame level the two frames point at each other. `vragen` has three
frames, so its pointers form a chain instead: `vragen-aan` ↔ `vragen-om`, and
`vragen-naar` → `vragen-aan` one way. The engine only reads each frame's own
`contrast`, so a non-reciprocal entry is valid; do not "fix" it into a cycle.
| `focus` | `zin()` | Underlines the chunk in cobalt; the rest of the sentence stays black |
| `pronominal` | Ontdek | Printed as a `Korter:` line, not a stop |
| `discoverOnly` | `oefenbaar` | The frame can appear on an Ontdek card but never as a Kies option or a distractor |
| `levels[].extra` | Ontdek | Extra input cards, e.g. `eraan-denken` inside the `denken` level |
| `en` | Ontdek, Kies, Klopt | The English gloss. The game is Dutch-only, but the gloss is the fallback meaning, per `decisions.md` |

`scenes[].file` is **relative to the game folder**, not the repo root:
`art/wachten-op-bus.png`.

## The step engine

`start(level)` builds `sessie = { level, stappen, stap, item, goed, totaal }`.
`bouwStappen(level)` turns a level into an array of steps; each step is
`{ soort, kaarten }` or `{ soort, items }`.

| Step | Built from | Items in a two-frame level |
|---|---|---|
| `ontdek` | `frames` plus `level.extra` | 2 cards (3 in `denken`) |
| `kies` | One item per frame, each with 3 scene options | 2 |
| `klopt` | Per frame: its own sentence (true) and the partner's (false) | 4 |
| `bouw` | Every token array of every frame | 2 |

`vragen` and `praten` have three frames, so they get 3 Kies items, 6 Klopt
items and 3 Bouw items. `ophouden` and the eighteen other single-frame levels
have one frame, so they get 1 Kies item and 2 Bouw items — three scored
answers, three stops, not four. That is the level, not a data fault.

### Why Klopt is conditional

```js
var heeftContrast = frames.some(function (f) {
    return f.contrast && level.frames.indexOf(f.contrast) !== -1;
});
```

Klopt only exists if the level contains a real pair. A level whose frames do not
point at each other would have to invent a distractor, and a wrong preposition
that is not the partner teaches nothing about this chunk. If a future level
breaks the pairing, the stop silently disappears — that is the intended
failure mode, but check the stop bar after adding data.

### The loop

| Function | Does |
|---|---|
| `naarStap(i)` | Sets `stap`, resets `item` to 0, shows `toonKlaar()` past the end |
| `volgendeItem()` | Increments `item`; at the end of a step, advances the step |
| `teken()` | Clears `#scherm` once and dispatches on `stap.soort` |
| `toonStap(soort)` | Hides stop-bar entries this level has no step for, marks the current one orange, earlier ones `geweest` |

Every stop advances through the same `volgendeItem`, including Ontdek, which is
unscored. Only `teken()` writes to `#scherm`, so a renderer may assume an empty
container.

### Renderers

Each renderer appends to `#scherm` and, where there is a right answer, calls
`toonTerug(blok, 'goed'|'fout', frame)` instead of writing feedback itself.
`toonTerug` is the only place a `.terug` panel is created, which is why the
concept question lives there and cannot appear before the answer.

`tekenBouw` is the exception: it owns local state (`gekozen`, `pool`, `klaar`)
and its own `Controleer` button, then hands off to `toonTerug` for the verdict.

### Layout: one step, one screen

Every renderer returns the same skeleton so a step never scrolls:

```
.vlak
  .beeldvak (the drawing) or .keuzes (the three images)
  .tekst    (.vraag / .uitleg / .zin / .kloptzin / .rij / .pool / .terug)
  .verder   (the counter and the primary button)
```

- **Wide screen** (`min-width:800px and min-height:520px`): `.vlak` is a
grid, drawing left spanning both rows, text and buttons right. The drawing
is capped at `min(52vh,430px)`, and at `min(32vh,300px)` once feedback is
showing, because the answer panel makes the text column the tall one. Below
820 px of height the step bar, the sentence and the panel each give up a few
pixels (`@media(min-width:800px) and (max-height:820px)`).
- **Narrow screen**: stacked, `.vlak` centres its content and the drawing
absorbs the slack (`flex:1 1 180px`) so a tall phone does not leave a hole
under the sentence. The answer panel is `position:fixed` at the bottom and
slides in; the step reserves exactly the part it covers. `FeedbackBlock`
measures that (`--terug-hoogte`, a `ResizeObserver` on the panel, using
`offsetHeight` because the entrance animation is a transform) and
`.vlak--na` pads by it, so the sentence is never hidden behind the panel.
The panel grows when its concept question is answered, which is why this is
an observer and not one measurement. `justify-content: safe center` keeps a
too-tall step from spilling up over the step bar.
- **Short phone** (`max-height:760px`) with a concept question: the panel and
the sentence are all that fits, so the drawing is hidden. The sentence is
what is being read; the drawing has already been seen.
- `.vel` is `height:100dvh` at 520 px and above, so the footer stays on
screen and anything that still cannot fit scrolls inside `.app-container`.
Below 520 px (a phone on its side) the page falls back to normal scrolling,
because a step plus the site header does not fit there at all.

Verified in headless Chrome at 360×740, 390×844, 844×390, 1280×600,
1366×768 and 1400×900: every state of a level reports
`scrollHeight === innerHeight`, and a DOM check found no step content behind
the answer panel. The two exceptions are 844×390 (page scroll, by design)
and 1280×600, where the concept-question panel scrolls inside the game area.

## There is no parser

Every check is a lookup or a string compare.

| Stop | Check |
|---|---|
| Kies | `gekozen === item.frame.scene` |
| Klopt | `gekozen === item.waar` — the answer is stored, not derived |
| Bouw | `gekozen.join(' ') === doel.join(' ')`, then `lastIndexOf(prefix) === doel.length - 1` for the position message |

Bouw's exact-string compare means the only accepted sentence is one written in
`prepositions.json`. That is deliberate: a pilot does not need to accept paraphrases, and
a parser would be the largest piece of code in the game. The cost is that the
tile order is the only order: a learner who builds a different but grammatical
sentence is marked wrong.

A misplaced prefix is reported as a position error before any other failure:

```js
} else if (f.prefix && antwoord.indexOf(f.prefix) !== -1 && !prefixLaatst) {
    blok = tekst(['Bijna. ', vet(f.prefix), ' hoort achteraan.']);
}
```

## Scoring and feedback

- Ontdek is not counted. Kies, Klopt and Bouw each add one to `totaal`.
- The end screen is `goed / totaal` with `Nog een keer` (same level) and `Ander
  niveau`. Nothing is stored, so a session leaves no trace — there is no review
  queue yet.
- Feedback names the chunk, never just "wrong": a wrong Kies says which frame
  the chosen image belongs to, a wrong Klopt names the preposition that would
  fit, and Bouw prints the target sentence.
- The concept question is rendered by `toonTerug`, and only Klopt passes it a
  frame. So it appears at Klopt alone, after the answer, and only `concept[0]`
  is ever read. The single-frame levels have no Klopt stop, so their concept
  questions never appear at all.
- `#melding` is `aria-live="polite"` and repeats the question or the verdict.
  Scene images are `aria-hidden` in choice buttons (`aria-label="Beeld 1"`), and
  carry the scene `alt` only where the image is the content: Ontdek, Klopt and
  Bouw.

## The art

The thirty files are alpha masks, not pictures. `beeld(sceneId)` sets `--beeld` to
the file URL and `.beeld` paints `var(--kobalt)` through it, so the ink follows
the theme with one file. The formula, the portrait exception and the reason for
it are in `game-art.md` under *Delivered raster art*; do not recolour the PNGs.

`aspect-ratio: 512 / 763` in `style.css` must match the shipped files. A new
image at another ratio needs that rule changed, which changes every scene on
the page.

## Not built

| Item | State |
|---|---|
| `Krimp` (pronominal transformation) | Not built; the form is a `Korter:` line on Ontdek |
| `Hetzelfde of anders?` | Not built |
| Flitskaarten / review queue | Not built; nothing is persisted |
| Audio | Not built, blocked by the open question in `decisions.md` |
| Second concept question | In the data for three frames, never rendered |
| `pronominalScene` | In the data, never read |
| Shared Zinsbouwer tile renderer | There is no Zinsbouwer module to share with; `tekenBouw` is local |
| Free-text entry | Not built; all four stops are taps |

## Open questions

- The stop bar hides the Klopt entry on every single-frame level rather than
  dimming it. Three entries in a four-column habit is honest, but a learner who
  did another level first may read the gap as a bug. Unmeasured.
- Ten contrast sets exist. Whether a session of scenes reads as a path or a
  wall is still unmeasured.
- Klopt is exactly half true, every time: one true and one false item per
  frame. With few items a learner could pass on the imbalance rather than the
  meaning. Whether that happens is unchecked.
- `denken-aan-persoon` and `eraan-denken-afspraak` are flagged for redraw in
  `Docs/voorzetselpaden/a0-a2.html` (the card for each frame); the game works with them, so the redraw is an art
  decision, not a blocker.
