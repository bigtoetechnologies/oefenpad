# Voorzetselpaden — how it is built

The game as shipped: **twenty-eight levels** — ten in A0, eighteen in A1 —
holding **ninety-one example scenes**. A level is one verb or expression plus
its preposition (`wachten op`), taught across two to four photographs. The
React page is `client/src/games/prepositions/`; the levels, frames, scenes and
sentences are in
`server/Oefenpad.Resources/Games/Data/prepositions.json`, and the rules that
build the steps and judge every answer are in
`server/Oefenpad.Services/Games/PrepositionsService.cs`. `prepositions.md` is
the activity spec and the reasoning; `game-art.md` is how the images are drawn;
this file is the code.

**The band pages are the source.** `Docs/voorzetselpaden/a0.html` and
`a1.html` hold the cards — chunk, gloss, scene brief, the example sentence,
the build sentence and the control question. `prepositions.json` and
`meta.json` are generated from them by
`tools/import-prepositions-band.py` (read-only over the pages, promoting each
card's image into `assets/voorzetselpaden/`). Do not hand-edit the JSON: edit
the page and re-run the importer, or the next run will overwrite you. Only
cards that carry a `class="beeld"` image are imported; `vragen om` and
`doorgeven aan` have none in A0/A1 and are therefore absent.

## Files

| File | What it holds |
|---|---|
| `client/src/games/prepositions/PrepositionsGame.tsx` | The React page: the stop bar, the four renderers, the level list, the feedback panel |
| `client/src/styles/source/prepositions.css` | A thin layer over `assets/site/oefenpad.css`; tokens only, no new colours. Regenerate `client/src/styles/games/prepositions.css` with `npm run scope-css` |
| `server/Oefenpad.Resources/Games/Data/prepositions.json` | `scenes`, `frames`, `levels`. Content only, no logic |
| `server/Oefenpad.Services/Games/PrepositionsService.cs` | The step engine, the options, the judging, the view |
| `server/Oefenpad.Services/Games/GameAccessService.cs` | The tier and level-chain rule (`PrepositionAccess`) |
| `assets/voorzetselpaden/*.png` | The alpha masks, 512 × 763, one per example scene |
| `tools/import-prepositions-band.py` | Page → JSON importer and art promoter |

`GameShell` supplies the `.balk` / `.spel-kop` / `.voet` chrome and the theme
toggle. The browser never sees the frames, the contrast partner or the tile
order; the service sends one card at a time and judges every answer.

The `.spel-kop` carries one button the other games do not need: `Niveaus`,
the way back to the level list from anywhere inside a level. It is a labelled
`.btn-icon--tekst` rather than a glyph because the arrow beside it already
leaves the game for the site, and two arrows would say the same thing twice.
`GameShell` renders it only while a round is open, so the level list and the
end screen (which has `Ander niveau`) show no button that would go nowhere.
Below about 370 px of width the whole `.stand` wraps under the title; the step
was re-checked at 360 × 740 and still fits on one screen.

There is no `grammar.js` and no `verbs` table. The spec assumed both; the
pilot does not need them.

## The data, as shipped

```js
{
  scenes: { '<scene-id>': { file, alt } },
  frames: [ { id, frame, en, scene, contrast, focus,
              example: { nl, en }, build: [[token, …], …],
              concept: [{ question, answer }],
              separable, prefix } ],
  levels: [ { id, name, band, frames: [frameId, …] } ]
}
```

A **frame** is one example scene of a chunk: `bang-voor-spin` carries
`frame: "bang voor"`, `en: "afraid of"` and its own sentence. The chunk is
repeated on every one of its examples — that repetition is what lets the
client show the same combination four times without a lookup table. A
**level** is one chunk, `band` is the CEFR band it was written for (`a0`,
`a1`), and `frames` lists its examples in page order.

### Where it diverged from the spec

| Spec (`prepositions.md`) | Shipped | Why |
|---|---|---|
| `verb`, `prep` separate fields | One `frame` string, plus `focus[]` | Nothing joins on the verb. `focus` is the list of words the UI underlines — the preposition and, for a separable verb, the prefix |
| `conceptQuestions` | `concept` | Renamed for brevity; same shape. Only `concept[0]` is read |
| `pronominalScene` on every frame | Dropped | The engine never read it, and the band pages do not carry it |
| — | `levels[].band` | The tier rule and the level list both group by band |
| — | `build: [[token, …], …]` | One array per accepted sentence; the importer keeps the card's first build line, the only one that varies |
| — | `contrast` may name a frame in another level | A level is one chunk now, so the partner is always elsewhere — see below |
| `separable` on every frame | `true` + `prefix` on separable frames only | Absence means not separable. The field is documentation; the engine keys off `prefix` |

`scenes[].file` is **relative to the game folder**: `art/bang-voor-hond.png`.

## The step engine

`Start(level)` builds a `RoundState` — level id, steps, step index, item,
score. `BuildSteps(level)` turns the level into its steps; each step is a
`DiscoverStep`, `ChooseStep`, `TrueFalseStep` or `BuildStep`. Empty steps are
dropped before the round starts, because a view indexes item 0 of an empty
list.

| Step | Built from | Items for a level with 4 examples |
|---|---|---|
| `discover` | every example | 4 cards (unscored) |
| `choose` | One item per example, each with 3 scene options | 4 |
| `klopt` | Per example: its own sentence (true) and the contrast partner's (false) | 8 |
| `build` | Every token array of every frame | 4 |

A level with one or two examples gets one or two Kies items, and a level
without a contrast partner has no Klopt step: three stops instead of four.
That is the level, not a data fault.

### Why Klopt is conditional

```csharp
var hasContrast = frames.Any(f =>
    f.Contrast is not null && _byId.ContainsKey(f.Contrast));
```

Klopt only exists when the chunk has a contrast partner that resolves to a
frame **anywhere in the data** — not necessarily in this level. Since a level
is now one chunk, the partner is always in another level: `wachten op` points
at `wachten voor`, and its Klopt questions borrow the partner's sentence. A
wrong preposition that is not the partner teaches nothing about this chunk, so
a chunk with no partner (A0's ten, and `bezig zijn met`, `meedoen met`,
`uitnodigen voor`, `vallen uit`) simply has no Klopt stop. If an entry stops
resolving, the stop silently disappears — check the stop bar after adding
data.

### Choosing the three pictures

`OptionsFor` always shows the right scene plus two distractors. The other
examples of the same level come first, because the question is *which
situation does this sentence describe*; a level with fewer than three examples
borrows scenes from elsewhere in the data. The option list is shuffled before
it is sent.

### The loop

| Member | Does |
|---|---|
| `Next` | Advances the item; at the end of a step, advances the step and skips anything empty. Discovery advances without an answer |
| `Choose` / `TrueFalse` / `Build` | Score the item, set the feedback fields, return the same view with `phase: "feedback"` |
| `Concept` | Records the answer to the post-answer meaning question. Not scored |
| `View` | Projects the current step and item into the one object the client renders |
| `CurrentStep`, `ItemCount` | Guard every action against an index the client should not have |

The client renders from `view` alone. `stepIndex` and `item` drive the stop
bar and the counter, and `steps` lists the kinds this level has, so an absent
Klopt needs no client knowledge.

### Renderers

`renderStep` dispatches on `view.kind` to one of four renderers, all of which
return the same skeleton so a step never scrolls:

```
.vlak
  .beeldvak (the drawing) or .keuzes (the three images)
  .tekst    (.vraag / .uitleg / .zin / .rij / .pool / .terug)
  .verder   (the counter and the primary button)
```

`BuildView` is the exception on the client: it owns local state (the chosen
tiles, the pool) and its own `Controleer` button, then hands off to
`FeedbackBlock`.

### Layout: one step, one screen

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
1366×768 and 1400×900 before the A0/A1 import; the import changed the number
of items per step, not the skeleton, and the A0/A1 screens were re-checked at
1400×1000 on 13 Nov 2026.

## There is no parser

Every check is a lookup or a string compare.

| Stop | Check |
|---|---|
| Kies | `chosen === item.Frame.Scene` |
| Klopt | `answer === item.Truth` — the answer is stored, not derived |
| Bouw | `answer.SequenceEqual(item.Target)`, then `LastIndexOf(prefix) === Target.Count - 1` for the position message |

Bouw's exact-sequence compare means the only accepted sentence is the one in
`prepositions.json`. That is deliberate: a pilot does not need to accept
paraphrases, and a parser would be the largest piece of code in the game. The
cost is that the tile order is the only order: a learner who builds a
different but grammatical sentence is marked wrong.

A misplaced prefix is reported as a position error before any other failure:

```csharp
} else if (item.Frame.Prefix is not null &&
           answer.Contains(item.Frame.Prefix) && !prefixLast) {
    state.LastExplanation = Text("build-almost", ("prefix", item.Frame.Prefix));
}
```

Only `meedoen met` carries `prefix` in A0/A1, because it is the only card the
band pages mark `scheidbaar`. `uitnodigen voor` is separable in its own
sentences too, but the page does not say so, so `build-almost` never fires for
it. That is a content gap, not an engine one.

## Scoring and feedback

- Ontdek is not counted. Kies, Klopt and Bouw each add one to `total`.
- The end screen is `correct / total` with `Nog een keer` (same level) and
  `Ander niveau`. Progress is saved per level for a signed-in account; a guest
  leaves no trace.
- Feedback names the chunk, never just "wrong":
  - a wrong Kies says which **sentence** the picked picture belongs to,
    because the distractors are usually other examples of the same chunk and
    naming the chunk would read "bang voor, niet bang voor";
  - a wrong Klopt names the chunk and the sentence the picture fits;
  - Bouw prints the target sentence, and the prefix message when the prefix is
    in the wrong place.
- The concept question is rendered by `FeedbackBlock`, and only Klopt passes it
  a frame. So it appears at Klopt alone, after the answer, and only
  `concept[0]` is ever read. Chunks without a Klopt stop never show theirs.
- The live region repeats the question or the verdict. Scene images are
  `aria-hidden` in choice buttons (`aria-label="Beeld 1"`), and carry the scene
  `alt` only where the image is the content: Ontdek, Klopt and Bouw.

## Access

`PrepositionAccess.Evaluate` decides per level. The tier comes from the band,
not from an index, because the game grows a band at a time:

| Band | Tier |
|---|---|
| `a0` (and anything unlabelled) | free — no account, no chain |
| `a1` | account. The first level of the band opens the band; each next one waits for the one before it |
| `a2` and up | paid plan. No payment system exists yet, so that slice is shut |

`/options` marks a closed level; `POST /rounds` answers 403 for it. The round
endpoint is the check that matters, because a caller can skip `/options`
entirely. The level list groups rows under an `A0` / `A1` heading
(`.band-kop`); the row number keeps counting across bands.

## The art

The ninety-one files are alpha masks, not pictures. `Scene` sets `--beeld` to
the file URL and `.beeld` paints `var(--kobalt)` through it, so the ink follows
the theme with one file. The formula, the portrait exception and the reason
for it are in `game-art.md` under *Delivered raster art*; do not recolour the
PNGs.

`aspect-ratio: 512 / 763` in `prepositions.css` must match the shipped files.
A new image at another ratio needs that rule changed, which changes every
scene on the page.

## Not built

| Item | State |
|---|---|
| `Krimp` (pronominal transformation) | Not built, and not in the A0/A1 data |
| `Hetzelfde of anders?` | Not built |
| Flitskaarten / review queue | Not built; progress is a best score per level |
| Audio | Not built, blocked by the open question in `decisions.md` |
| Second concept question | In the data for some frames, never rendered |
| Free-text entry | Not built; every stop is taps |
| A2 and up | Not imported; the band pages exist, the images do not yet |

## Open questions

- The stop bar hides the Klopt entry on a chunk without a contrast partner
  rather than dimming it. Three entries in a four-column habit is honest, but a
  learner who did another level first may read the gap as a bug. Unmeasured.
- Klopt is exactly half true, every time: one true and one false item per
  example. With few items a learner could pass on the imbalance rather than the
  meaning. Whether that happens is unchecked.
- Whether four photographs of one chunk read as practice or as repetition is
  unmeasured. It is also the point of the remake: one picture per chunk taught
  the chunk, four teach the situation.
- The A0/A1 split is judgement, not roadmap. `Docs/prepositions-roadmap.md` has
  the plan and the reason per frame.
