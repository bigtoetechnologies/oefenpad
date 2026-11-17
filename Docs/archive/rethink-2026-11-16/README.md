# Rethink: structure and art

> **Archived 16 November 2026.** A design proposal, never wired into the site.
> `Docs/product.md` §11 (home = a tally of words met and held, plus one obvious
> next action) and §12 (themes, not goals, are the navigation) settle what this
> folder was arguing about, so the five-goal taxonomy below is superseded. Keep
> it for the art treatment and the three prototypes, not for the structure.

A working proposal, 16 November 2026. Nothing here is wired into the site.
The three pages are standalone prototypes on the live tokens and the live
scene art, so they can be compared like `design-options/` was. The folder is
scratch: promote or delete it once the direction is settled.

## What prompted it

Two complaints, and they turn out to have one cause.

1. The Voorzetselpaden art changed to style A because the brush could not be
   kept consistent across a batch. The home page is still option G, brush and
   heavy editorial type. Inside a game the two meet: a rounded, friendly
   pictogram on a page of hard rules and painted blocks.
2. The home page shows six equal tiles. It has no way to say that the games
   train different things, that some have levels, or where the learner is. The
   thirteen-game plan in `game-catalogue.md` is goal-first; the interface is
   not.

The cause: **the home page is a shop window for games, and the paint is doing
the job a picture should do.** There is no picture on the way in, so the first
one a learner meets is inside a game, out of context and in another hand.

### Evidence

`shots/home-1400.png` is the live page. `shots/prep-discover-1400.png` and
`shots/prep-choose-1400.png` are the live game. The game's own three scenes
are consistent with each other (`shots/prep-choose-1400.png`); the mismatch is
between the drawing and the chrome.

Two things on the live home page are also not real:

| What it says | Where | Reality |
|---|---|---|
| "4 dagen op rij" | `index.html`, `.telling` | Hardcoded. A first-time visitor is told they have a streak |
| "Je was gebleven bij *op het station*" | `index.html`, Woordzoeker tile | Hardcoded. Nothing reads progress |

`assets/site/oefenpad.js` never touches either; the only storage it reads is
the language choice. Accounts and game progress exist (`GET
/api/games/{game}/progress`), so both can be real — but not from a static
`index.html`.

## The three prototypes

| | File | What it tests | Verdict |
|---|---|---|---|
| **A** | `a-sporen.html` | The games grouped by what they train, with the band ladder where one exists | The answer to "different learning goals". Better as the index than as the home |
| **B** | `b-les.html` | The home as today's ten-minute path: three steps across three goals | **Recommended as the home page** |
| **C** | `c-vandaag.html` | The home as one picture and one exercise; everything else below the fold | Recommended for how the art is treated, not as the whole home |

All three are checked at 1400 × 1000 and 430 × 932. Screenshots:
`shots/a-1400.png`, `shots/b-1400.png`, `shots/c-1400.png` and the `-430`
versions.

### A — Sporen

Four tracks, one per goal — Woorden, Spelling, Betekenis, Spreken — with the
games as rows inside them. A game that has CEFR bands shows them
(`A0 4/10`, `A1 account`); a game without bands says how you choose instead
(`Kies een categorie`). This is the screen that makes the portfolio legible:
it can hold thirteen games without changing shape, and it says what each one
is for.

It is too long to be the first screen, and it still makes the learner choose.

### B — Les

The home page is a session: three steps, one per goal, ten minutes, in an
order. The current step is the only orange thing on the page. The other steps
are outlined buttons, so orange keeps meaning "do this now". The picture
appears on the step that needs it — the Voorzetselpaden step — at the size a
phone choice tile uses (about 93 px), which is what style A was drawn for.

This is the structure that matches the name and the promise: *oefenpad*, ten
minutes a day, not a shelf of games. It also gives the account something to
save: which step you reached.

### C — Vandaag

One plate, one sentence, one orange button. The drawing is 320 px wide on
paper, not in a card, not on a painted block. The page reads as a picture book
plate, and the heavy type sits beside it as caption. This is the direct answer
to the art complaint: put the picture on the way in, give it air, and it stops
looking like clipart inside an editorial page.

Below it, four goal cards are the only navigation. That part is weaker than A.

## Recommendation

Combine them, in this order:

1. **Home = B.** Today's path, three steps, real progress, one orange action.
   Steps are composed server-side from the goals the learner has not practised
   recently, so it does not need a scheduler to start.
2. **Index = A.** `Oefeningen` becomes the goal map. The home's "Liever zelf
   kiezen?" links to it. This is where thirteen games can live.
3. **Art = C's treatment everywhere.** A drawing is a plate on paper with air
   around it, never a decoration inside a tile or on a painted block.

### One art register, not two

Retire the brush as the illustration style. Keep it as the brand and the
interface's action/status paint. Reasons:

- The brush cannot be produced consistently at scale. That is not a Grok
  problem, it is the nature of a hand-drawn line: 91 scenes now, 72 reels and
  hundreds of word images later. Style A holds a batch together.
- A scene is a picture for a learner to read; the grid is the structure for
  them to navigate. Letting each do its own job is not a style clash, it is a
  division of labour.
- The prototypes have almost no paint — only the logo and the orange action —
  and still read as Oefenpad. The grid and the type carry the identity. The
  large painted tiles were competing with the drawings.

Concretely, this changes `game-art.md`: the style A section becomes the rule
for **all** game art, not only Voorzetselpaden. The brush section stays as the
spec for the logo and the painted interface fills, which is a different job.
`designguide.md`'s "Illustration and game art" table ("the brush is the line")
has to be rewritten.

### Goal taxonomy

The learner-facing taxonomy is five goals, not the book's eight pillars:

| Goal | Games now | Games planned |
|---|---|---|
| Woorden | Geheugen, Koppelen | Flitskaarten, Woordzoeker/Galgje with picture clues |
| Spelling | Woordzoeker, Galgje | — |
| Betekenis | Voorzetselpaden | Valse vrienden, Vul de leegte, Lego-woorden |
| Zinnen | — | Zinsbouwer, Vul de leegte |
| Spreken | Verhaalmachine | Luisteroefening (blocked on audio) |

Pillars stay the content taxonomy (the book's chapters). The "eight pillars by
motif" idea in `decisions.md` was never built and is not needed to distinguish
five goals in a list. Motifs can come later as one small drawing per goal, in
style A, if the labels test badly.

## What it costs

| Work | Where |
|---|---|
| Home page reads progress | `index.html` is static. Either make it a Razor Page or add a small client fetch of `/api/games` + `/api/games/{game}/progress`. Accounts already persist progress |
| Game metadata: goal, band, level count, availability | `client/src/site/GameList.tsx` hardcodes six entries with `kind`. Move it to the API (`/api/games`) so the home, the index and `GameShell` share one source |
| Plate component | The mask technique exists in `client/src/styles/source/prepositions.css`; lift `.beeld` / `.plaat` into `oefenpad.css` so the home can use it |
| Session composer | A small server rule: pick three steps across goals, shortest unfinished first. It can start as a fixed rotation, no scheduling |
| Bilingual home | The prototypes are Dutch-only to keep the comparison about structure. The live home still ships both languages |

No new art is needed for any of this. The one picture in the prototypes is
already in `assets/voorzetselpaden/`.

## Open, for the owner

1. **Is the product "pick a game" or "do today's practice"?** B says the
   second. If it is the first, A is the home page and this rethink is smaller.
2. **Does the home show progress to a guest?** B needs *a* step to start from
   even with no history; the prototype shows a sample signed-in state.
3. **One art register?** Retiring the brush for content art is a bigger call
   than changing the home page, and it contradicts `game-art.md` today.
4. **Which goal names are canonical?** Woorden / Spelling / Betekenis /
   Spreken is what the live tiles already say, minus the missing labels. It is
   four words a beginner can meet on day one, which is the point.
5. If "multiple language games" was meant as other **learner** languages rather
   than the several Dutch games, that contradicts `decisions.md` and is a
   separate decision.
