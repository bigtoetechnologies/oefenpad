# Games: server-side data and the React app

The six practice games no longer ship their content or their puzzle
generators to the browser. The .NET service owns the word banks, the
pictures, the prepositions, the story reels and the Dutch interface
strings; it also builds the Word Search grid, the Memory deck and the
Matching board. The browser asks for one round and posts the player's
actions back.

This document is the map: what lives where, why, and how to run it.

## Why this exists

Until this change every game was a static page:

```
src/galgje/script.js          src/shared/words.js      (2,699 lines)
src/geheugen/script.js        src/shared/wordimages.js
src/koppelen/script.js        src/shared/i18n.js
src/woordzoeker/script.js     src/shared/common.js
src/storymachine/script.js
src/voorzetselpaden/script.js
```

A visitor could save the HTML, the scripts and the 25-category word bank
and rehost the whole thing. The Word Search generator was in the script
as well, so the bank and the puzzle engine both left with the page.

Now the only game data that crosses the wire is the view of the round
the player is in.

## What the browser can get

| Request | Response |
|---|---|
| `GET /api/games` | the game ids |
| `GET /api/games/{game}/options` | category names, icons and counts; level ids and names, plus `locked` / `lockReason` for a level the visitor may not start. No words |
| `GET /api/games/{game}/texts` | the Dutch interface strings for that game |
| `GET /api/games/{game}/saved` | the signed-in player's saved round, or `{ "saved": false }` |
| `GET /api/games/{game}/progress` | finished levels and their best scores, or `{}` for a guest |
| `POST /api/games/{game}/rounds` | `{ roundId, view }` for one round, or **403** when the level is locked |
| `POST /api/games/{game}/rounds/{id}/moves` | the new view, plus whether the move was correct and any feedback |

The browser never receives the word bank, the image manifest, the
translation column for unplayed words, or the placement list of a Word
Search puzzle. A `wordsearch` round for a 10×10 beginner puzzle is about
1.3 KB; the embedded bank it was drawn from is about 169 KB.

A player can still read the ten words on their own board — that is the
game. They cannot enumerate the bank without playing rounds, and the
game API is rate limited (600 requests per five minutes per address).

This is not encryption. It moves the asset that was worth copying — the
content and the generator — behind the API. The renderer is still
readable, by design: it is only the parts that make the product.

## Level gating

`/options` marks each level with `locked` and a `lockReason`:

| `lockReason` | Meaning | The client shows |
|---|---|---|
| `progress` | the previous level has not been finished | a lock and "Haal eerst het vorige niveau." |
| `account` | the visitor is past the free slice and not signed in | a lock, "Maak een account om verder te gaan." and a Registreren link |
| `premium` | the level belongs to the paid slice | a lock and "Hiervoor komt een abonnement." (no link: there is no payment system yet) |

Voorzetselpaden is the only game with a policy today. Its tiers follow the
CEFR bands the content comes in (`PrepositionAccess` in
`GameAccessService.cs`):

| Levels | Who can play |
|---|---|
| the A0 band | everyone |
| the A1 band | a signed-in learner |
| A2 and up | a paid plan — not built, so shut (and not imported yet) |

A band starts at its first level; within it a level opens only when the one
before it is finished, and
finishing counts as passing — the gate exists to make a crawler play, not to
grade the player. A finished level stays playable if an earlier row is missing,
but a finished premium level locks again without a plan: progress survives,
access does not. `POST .../rounds` re-checks the rule and answers 403, so hiding
a level in `/options` is not the only defence. The decision and threat model are
in `review-handover.md`.

## The round model

A round is created with `POST .../rounds` and lives in memory:

- `RoundStore` holds the private state (grid, solution, deck, order);
- a round lasts **3 hours**, and at most **4,000** are held; when the
  store is full the oldest half is dropped;
- an unknown or expired round answers **410 Gone** with
  `{ "error": "Deze ronde bestaat niet meer." }`; the client shows the
  message and offers a new game;
- an invalid action answers **400** with the server's Dutch reason.

Because state is in memory, restarting the service ends open rounds for a
guest. A signed-in player's round is copied to the account after every
answer, so it survives a restart and can be rebuilt (see below).

## Progress on an account

Progress is optional and never gates a game. A guest plays exactly as before:
the progress service answers nothing and writes nothing.

For a signed-in player the API does three things on the normal paths:

- after `POST .../rounds` and after every accepted move, it serializes the
game's private state with `IGameService.Export` and upserts one
`GameSaves` row per `(user, game)`;
- `GET .../saved` loads that row, rebuilds a fresh in-memory round with
`IGameService.Resume`, and returns `{ saved: true, roundId, view, resume }`.
The game then reuses the new round id for its moves. A blob the game can no
longer rebuild is deleted and answered as `{ saved: false }`;
- when a move finishes a round, the save is cleared. If `IGameService.LevelOf`
names a level (prepositions today), the result is written to
`GameLevelProgress`, keeping the best score. Nothing else invents levels:
Hangman, Memory, Matching, Story Machine and Word Search have settings, not
levels.

The stored JSON is the same private state `RoundStore` would hold: the hidden
word, the deck, the placement table. It never leaves the server. The two
exceptions are deliberate and narrow:

- Word Search's resume payload carries `placements`, and only for words the
player has already found, so the canvas can redraw their outlines;
- Prepositions serializes its whole step tree. Rebuilding it from the level id
would reshuffle the questions and hand out points twice.

The client asks for `/saved` once when a game mounts, before its own first
round. A resumed round shows one quiet Dutch line, "We gaan verder waar je
gebleven was.", and disappears after a few seconds. `GameSaves` and
`GameLevelProgress` cascade-delete with the user.

### Actions per game

| Game | Start body | Move bodies |
|---|---|---|
| `hangman` | `{ category, difficulty, translateTo? }` | `{ action: "guess", letter }`, `{ action: "hint" }` |
| `memory` | `{ category, level }` | `{ action: "flip", index }` |
| `matching` | `{ category, pairs }` | `{ action: "flip", index }` |
| `wordsearch` | `{ category, difficulty, translateTo? }` | `{ action: "select", r1, c1, r2, c2 }`, `{ action: "hint" }` |
| `storymachine` | `{ count, language }` | `{ action: "hold", index, held }`, `{ action: "language", language }`, `{ action: "spin" }` |
| `prepositions` | `{ level }` | `{ action: "next" }`, `{ action: "concept", answer }`, `{ action: "choose", scene }`, `{ action: "trueFalse", answer }`, `{ action: "build", tiles: [] }` |

The server judges every answer. The Word Search checks the line the
player selected against the hidden solution; the Memory and Matching
services decide whether two cards form a pair; Hangman owns the pattern
and the wrong-letter count.

## Where the content lives

`server/Oefenpad.Resources/Games/Data/` — embedded resources, read once
by `GameContent`:

| File | What it holds |
|---|---|
| `words.json` | 25 categories, 2,518 entries (Dutch, English, optional image key) |
| `wordimages.json` | English word → image file |
| `prepositions.json` | 28 levels (A0, A1), 91 example scenes, frames, examples, build tiles |
| `reels.json` | the six story reels and their tiles |
| `meta.json` | counts for tests and documentation |
| `texts.<game>.json` | the Dutch interface strings, one file per game |

Editing content means editing these JSON files and rebuilding the
resource project. The generated pictures stay under
`assets/wordimages/` and `assets/voorzetselpaden/`; the API sends a path
such as `/assets/wordimages/animals/dog.jpg`.

`meta.json` is the canonical count table; the tests read it.

## The React app

`client/` is a Vite 5 + React 18 single-page app. It is served from
`/spelen/` by the .NET host, not from the repo root.

```
client/
  index.html                    shell, theme pre-paint, site CSS + JS
  vite.config.ts                base /spelen/, outDir the host's wwwroot
  scripts/scope-css.mjs         page sheets -> route-scoped sheets
  src/
    api.ts                      the only network layer
    App.tsx, main.tsx           routes and stylesheet imports
    site/GameShell.tsx          .vel, .balk, .spel-kop, .voet, splash
    site/GameList.tsx           the /spelen/ index
    shared/                     timer, splash, sound, confetti, storage,
                                overlay, zoom pop, word image, game data
    games/<game>/               one folder per game
    styles/base.css             page shell and reset
    styles/source/*.css         the unmodified per-page sheets
    styles/games/*.css          generated, scoped to .game--<game>
```

Routes: `/spelen/`, `/spelen/hangman`, `/spelen/memory`,
`/spelen/matching`, `/spelen/wordsearch`, `/spelen/storymachine`,
`/spelen/prepositions`.

`GameShell` renders the same chrome the old pages had: the `.vel`
column, the site bar with the injected `#theme-toggle`, the `.spel-kop`
with the back and settings buttons — plus a start button where a game hands
the shell an `onBegin`, as Voorzetselpaden does mid-level — the splash where
a game has one, and the `.voet` footer. The wrapper carries `.game--<game>`, which is
the scope of that game's stylesheet.

### Code in English, content in Dutch

Identifiers, comments, file names, routes and JSON field names are
English. Dutch survives as content: the strings in
`texts.<game>.json`, category and level names, the words on the cards,
and the feedback sentences. The markup class names stay Dutch
(`.vel`, `.balk`, `.spel-kop`, `.knop`) because they are the contract
with `assets/site/oefenpad.css`.

### Why the game styles are scoped

One bundle loads all six sheets, and the old pages reused the same class
names for different things (`.card` is a memory card on one page and a
story card on another). `scripts/scope-css.mjs` prefixes every selector
with `.game--<game>`, passes `@keyframes` through untouched, and recurses
into `@media`. Page resets (`:root`, `body`, the universal reset,
`button`, `:focus-visible`) are dropped: `base.css` owns them once, and
a scoped `*` reset would otherwise override the padding of `.vel`
because it comes later in the cascade at equal specificity.

After editing a sheet in `client/src/styles/source/`, run:

```sh
cd client && npm run scope-css
```

### What deliberately stays in the browser

Timers, the WebAudio sound set, confetti, the hangman canvas, the Word
Search selection line, pointer and tap handling, the card zoom, and
`localStorage` for settings and best scores. These are presentation and
input; moving them would add latency and buy nothing.

The old storage keys are kept unchanged, so settings and records survive
the move: `oefenpad-theme`, `oefenpad-taal`, `oefenpad-geheugen-settings`,
`oefenpad-geheugen-best`, `oefenpad-koppelen-settings`,
`oefenpad-koppelen-stats`, `oefenpad-galgje-settings`,
`oefenpad-galgje-stats`, `oefenpad-woordzoeker-settings`,
`oefenpad-woordzoeker-stats`.

## Running it

The host builds the app. `dotnet build` and `dotnet publish` run `npm ci`
(only when `node_modules` is missing) and `npm run build`, then ship
`wwwroot/spelen/`. The build is incremental: the npm step is skipped unless
something under `client/src`, `client/scripts`, `index.html`, `package.json`,
`package-lock.json`, `tsconfig.json` or `vite.config.ts` changed. Pass
`-p:SkipClientBuild=true` to build the server alone.

```sh
cd client
npm install          # once, if you want to run vite directly
npm run build        # tsc --noEmit && vite build, into wwwroot/spelen
```

Run the service (port 8098; 8080 belongs to the owner):

```sh
ASPNETCORE_ENVIRONMENT=Development dotnet run \
  --project server/Oefenpad.WebUI --urls http://127.0.0.1:8098
```

Then open `http://127.0.0.1:8098/spelen/`. The home page links straight
to the React routes.

During front-end work, `npm run dev` serves the app with a proxy to
`8098` for `/api` and `/assets`; the built app is what the host serves.

Check the API without a browser:

```sh
python3 tools/smoke-games-api.py
python3 tools/smoke-game-progress.py   # server in Development
ASPNETCORE_ENVIRONMENT=Development dotnet test server/Oefenpad.Tests
```

## What changed on disk

- All six `src/<game>/` folders and `src/shared/` are gone. The old
  scripts, the word bank and the client-side generators are no longer in
  the repo.
- `client/src/styles/source/*.css` keeps the six page stylesheets, vendored
  so `scope-css` still works. Nothing under the old `src/` remains.
- `assets/voorzetselpaden/` now holds the 30 scene images (moved from the
  old `src/voorzetselpaden/art/`). `assets/storymachine/art/` holds the two
  card backs (moved from `src/storymachine/art/`).
- The home page links to `/spelen/<game>`.
- `assets/site/oefenpad.js` exports `window.Oefenpad.ensureThemeToggle`,
  because the React bar is drawn after that script runs.

## Port notes and verification

This port was checked end to end on 2026-11-09, not just built.

| Check | What was run or seen |
|---|---|
| Server build | `cd server && dotnet build Oefenpad.sln` — 0 warnings, 0 errors |
| Tests | `dotnet test server/Oefenpad.Tests` — 29 passed: the game-content and round tests in `GameContentTests.cs`, plus the save/resume and progress tests in `GameProgressTests.cs` |
| API smoke | `python3 tools/smoke-games-api.py` — all six games start a round and accept moves; the Word Search view is checked for leaked placements, Hangman for a leaked answer, and prepositions for a full level walk |
| Client build | `cd client && npm run build` — `tsc --noEmit` clean, Vite writes into `server/Oefenpad.WebUI/wwwroot/spelen/` |
| Visual equivalence | Headless Chrome screenshots of each game against the old pages served from git HEAD, on port 8099. Memory, Hangman, Matching, Story Machine and Prepositions match. Word Search matches except for the intentionally restored first-visit category picker |
| Interaction | Chrome DevTools drove every game through a round: no console errors |
| Account progress | `python3 tools/smoke-game-progress.py` — registers and signs in, then checks `/saved`, the Word Search placements, a finished level in `/progress`, and both database rows. Headless Chrome showed the resumed board with its Dutch notice and `✓ 3/8` on the finished level |

### Bugs found and fixed during the port

These cost time; do not reintroduce them.

1. **A scoped universal reset overrode `.vel` padding.**
   `scope-css.mjs` must skip `*`, `*::before` and `*::after`. They arrive
   split by commas, so a naive prefix pass scoped the reset and it won the
   cascade at equal specificity, silently flattening the page padding.
2. **Memory stopped re-rendering after the zoom pop.** `pendingFirst` was a
   ref, so the second card turning over did not trigger a render. It now
   drives a `bump()` from `useReducer`. A missed pair also stayed face up;
   the hidden mask uses `hidden` / `hiddenRef` and `turnFirst` is kept as a
   ref until the pair is judged.
3. **Word Search carried a stray `.status-chip`** from the old page and lost
   the first-visit category picker. The chip is gone; the picker is back,
   gated on `oefenpad-woordzoeker-visited`.

## Known limits

1. **The games need the server.** The old static pages worked offline;
   the API-gated ones do not. The owner accepted this on 2026-11-09 as the
   price of keeping the bank private. Offline play can be revisited later,
   but it is not missing by accident.
2. **The build output is no longer missing from `dotnet publish`.**
   `Oefenpad.WebUI.csproj` runs the npm build in a `ClientBuild` target and
   adds `wwwroot/spelen/**` as publish files, so a publish ships the games.
   The npm step is skipped when the client sources are unchanged, and
   `-p:SkipClientBuild=true` turns it off for a server-only build.
3. **Live rounds are in memory.** A guest's round ends with a restart; a
   signed-in round is saved to the account and rebuilt. A second instance
   still cannot share a round that has not been saved yet, so a shared
   `RoundStore` is needed before scaling out.
4. **The rate limit is per remote address.** Behind a proxy that
   rewrites the address, every player shares one budget.
