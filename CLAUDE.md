# Oefenpad

A free Dutch practice site for adult newcomers to the Netherlands, most of
them studying for inburgering. The practice pages are static HTML with no build
step and no framework. Sign-up and account management are a small .NET 10
service in `server/`. A companion paperback, *Quick Wins in Dutch*, is the
acquisition channel and lives in `book.md`.

The practice site is deliberately plain to deploy: open `index.html` over any
static server and it runs. The account pages need the server in `server/`.

## Start here

| Read | To answer |
|---|---|
| `Docs/decisions.md` | Why the product is shaped this way. Read before proposing anything |
| `Docs/designguide.md` | Every visual rule. Canonical |
| `Docs/accounts.md` | How sign-up and account management are built, run and tested |
| `Docs/accounts-handover.md` | Why the account solution is shaped this way, plus the architecture and file-by-file code map |
| `Docs/game-art.md` | How game images are drawn: brush line, cobalt only, 512 px |
| `Docs/prepositions-roadmap.md` | The Voorzetselpaden plan to 710 frames, and what "B2" means |
| `Docs/voorzetselpaden/index.html` | Every Voorzetselpaden frame, one card each, by CEFR band. **The master.** Open it in a browser |
| `Docs/voorzetselpaden/a0-a2.html` … `b2.html` | The six band pages: the chunk, the gloss, the scene brief, Must read, Avoid, the review verdict, and the verbatim Grok prompt per batch |
| `Docs/design-process.md` | Which designs were rejected and why, so you don't re-propose them |
| `Docs/game-catalogue.md` | What each game is and what exists |
| `Docs/games-backend.md` | How the games get their data from the API, and how the React app is built and run |
| `Docs/review-handover.md` | What the 10 Nov 2026 review fixed, what it left, the content-exposure threat model, and the TotumTeams fidelity gaps |
| `Docs/Concept.md`, `Docs/games.md` | The eight pillars and the game specs |
| `Docs/design-options/index.html` | The fifteen home-page prototypes, side by side |

Superseded material lives in `Docs/archive/`. It is history, not guidance.

## Non-negotiables

These come from `Docs/decisions.md` and are not yours to relax.

| Rule | Why |
|---|---|
| The interface is Dutch | Most users have no English. Dutch chrome is itself practice |
| Meaning travels in pictures and colour | Never in a sentence a learner must parse |
| No text inside artwork, ever | One art set has to serve every first language |
| English glosses only, no other languages | Learners use their own dictionary |
| Orange means "do this now", nothing else | It may mark several elements if they are the same idea |
| Blue says what a thing is | Cobalt `#2B50C8`, never the retired `#1B3A6B` |
| No souvenir Dutch imagery | No windmills, clogs, tulips, canals, cheese |

A feature that only works if the learner reads English is suspect. Say so
rather than building it.

## The design system

One stylesheet and one script for the whole site: `assets/site/oefenpad.css`
and `assets/site/oefenpad.js`. Class names are Dutch. A twelve-column grid,
hairline rules, heavy Archivo type, and colour applied as brush-painted
fills. Full rules in `Docs/designguide.md`.

### Two traps that have already cost a day

The painted fills look like plain rectangles if either of these is broken,
and breaking one of them produces no visible change on its own, so you will
think your fix did nothing.

1. **The painted SVG must use a fixed small viewBox** — 300 × 150, or 100 × 30
   with `data-verf-klein` — stretched by `preserveAspectRatio="none"`. The
   filter's `baseFrequency` is tuned to those units. Use the element's real
   pixel size and the bristle texture falls below one pixel.
2. **`verf()` clears `background-color` after inserting the SVG.** The paint
   layer is semi-transparent by design; the flat CSS background is only the
   no-JS fallback. Leave it opaque and it fills in every bristle gap.

Compare any change against `Docs/design-options/g-penseelraster.html`. That
prototype is the agreed design and the reference for what the paint should
look like.

### Other things worth knowing

- **Bilingual markup.** Every page ships both languages; `<span lang="nl">`
  and `<span lang="en">`, switched by CSS on `html[data-taal]`. An inline
  script in `<head>` sets it before first paint.
- **Theme.** Opens light always. The system `prefers-color-scheme` is
  deliberately ignored. `oefenpad.js` injects the `#theme-toggle` button;
  do not hand-write it into pages.
- **The games are React now.** The six games live in `client/` and are served
  from `/spelen/<game>` by the .NET host. `GameShell` renders the chrome: `.vel`,
  `.balk`, `.spel-kop` and `.voet`, with the title outside `.app-container` so
  its rule spans the sheet rather than the 720 px game column. The games are
  Dutch-only, so their `.balk` has no `.taal` switch; `.rechts` holds only the
  injected `#theme-toggle`. The browser gets one round at a time from the game
  API; the word bank and the puzzle generators are server-side.

## Running and checking it

Port 8080 is often in use by something of the owner's. Leave it alone.

```sh
python3 -m http.server 8099 --bind 127.0.0.1
```

To check a visual change, screenshot it headless and compare against the
prototype:

```sh
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --window-size=1400,1000 --virtual-time-budget=7000 \
  --user-data-dir=/tmp/fresh-profile \
  --screenshot=out.png "http://127.0.0.1:8099/index.html?v=1"
```

**Chrome caches aggressively here and will hand you a stale render.** A
screenshot that contradicts the DOM is the symptom. Use a fresh
`--user-data-dir` and a changing query string for every shot that matters.
Two separate wrong conclusions in this repo came from skipping that.

Measuring beats eyeballing: sample pixels with PIL rather than judging a
downscaled screenshot. Brush texture shows up as a spread of roughly 17–20 in
the blue channel down a tile; a flat fill measures 0.

The account system is a separate .NET 10 solution under `server/`. Port 8098 is
for it; leave 8080 alone.

```sh
ASPNETCORE_ENVIRONMENT=Development dotnet run \
  --project server/Oefenpad.WebUI --urls http://127.0.0.1:8098

dotnet test server/Oefenpad.Tests
```

It applies migrations on start. The SQLite database is
`server/Oefenpad.WebUI/oefenpad.db`; account email is written to
`server/Oefenpad.WebUI/email-sink/` when no SMTP host is configured. Do not
serve the repo root to the web app: only `assets/` and the WebUI `wwwroot` are
exposed, and that is deliberate — the old `src/` scripts and word banks are
gone.

The React games build into the host. `dotnet build` and `dotnet publish` run
`npm ci` (when `node_modules` is missing) and `npm run build`, so a normal
build ships the games; `-p:SkipClientBuild=true` builds the server alone. The
npm step is skipped when the client sources are unchanged.

```sh
cd client && npm run build                    # writes wwwroot/spelen by hand
cd client && npm run scope-css                # after a change in styles/source
```

`Docs/games-backend.md` has the API, the round model, the verification record
and what stays in the browser.

## Where things stand

All nine pages — home, the two legal pages, six games — are on one design
system, the six games under the same `.balk` and `.voet` chrome. The home and
legal pages are bilingual and still static; the games are Dutch-only, React,
and served by the .NET host from `/spelen/`, with their content behind
`/api/games`.

Voorzetselpaden (now `client/src/games/prepositions/`, scenes in
`assets/voorzetselpaden/`) is the newest: a pilot with eighteen
levels — ten contrast sets (nine pairs and one set of three) and eight single
frames — and the only game whose art is raster. Its thirty scene images are
alpha masks drawn on a cobalt block, so they need no second file for dark mode. `Docs/game-art.md` has the art
technique; `Docs/prepositions-implementation.md` describes how the game is
built, and `Docs/prepositions.md` is the spec behind it.

**The scene plans are HTML now, and they are the master.** The seven Markdown
plans were replaced on 12 November 2026 by six pages under
`Docs/voorzetselpaden/`, one per CEFR band, 876 cards in all. A card holds the
chunk, the gloss, the scene brief, Must read, Avoid, the review verdict and —
for the fifty frames that are in the game — the example sentence, the build
sentence and the control question. Each batch keeps its Grok prompt verbatim in
a collapsible block, so a batch is still one copy-paste. The old Markdown prose
is preserved on each page under *Plan en kaders*. Edit the HTML, not
`prepositions.json`: the game data is generated from these pages. The originals
are in git at `80e688c`.

It is also the only
game with a gate: the first three levels are free, the next six need an
account, and the remaining nine need a paid plan, which is not built yet (so
that slice is shut). Within a tier a level opens only when the learner has
finished the one before it (`server/Oefenpad.Services/Games/GameAccessService.cs`).

Sign-up and account management live in the .NET 10 solution under `server/`.
It is Razor Pages, not Blazor, with ASP.NET Core Identity and SQLite, and it
serves the static site alongside the account pages from the same host. The
pages are bilingual and use the same `oefenpad.css`. `Docs/accounts.md` has
the architecture, the flows, the rate limits and what must change before
accounts go live. `Docs/accounts-handover.md` is the session record: the
decisions behind the build, the verified build/test evidence, and a
file-by-file map so the next agent does not have to load the solution.

The remote is `git@github.com:bigtoetechnologies/oefenpad.git`; `main` is **8
commits ahead and unpushed**, so the whole redesign exists only on this disk.
Uncommitted on top of that: the game chrome, the whole React client, the
server-side game content and API, the removal of the old `src/` game pages,
and the docs that describe it. Push only when the owner asks.

## Open and unverified

| # | Item |
|---|---|
| 1 | The no-JS fallback is reasoned correct but untested; headless `--disable-javascript` had no effect |
| 2 | `--grijs` on `--papier` in dark mode is unchecked for contrast |
| 3 | The twelve-bar week meter has no label. Nobody knows whether it reads as anything |
| 4 | Six content ideas from the rejected prototypes, listed at the end of `Docs/design-process.md` |
| 5 | The open questions in `Docs/decisions.md`: domain registration, a mascot, whether a paid tier exists above free, audio for pillar 8. The games' free slice is decided there |
| 6 | `privacy.html` and `voorwaarden.html` still say there is no account and no personal data. They must be rewritten before accounts go live; the mail provider is a new processor |
| 7 | The home hero says "no account". Accounts save progress, and Voorzetselpaden locks its last nine levels behind a paid plan that does not exist yet; the six between need an account. Word search is still open to guests, so its free slice is decided in `Docs/decisions.md` but not enforced. Decide whether it gets the same gate and whether sign-up ever becomes required to play at all |
| 8 | Production config: `Email:SmtpHost` is unset, so mail goes to `server/Oefenpad.WebUI/email-sink/`. Choose a provider. Set `App:BaseUrl` (mandatory outside Development — the app refuses to start without it) and `App:KnownProxies` when behind a TLS-terminating proxy, and persist the Data Protection keys. `Docs/accounts.md` lists the required values |
| 9 | The games now need the server. No offline play was accepted by the owner on 2026-11-09. The client build is wired into `dotnet build`/`publish` (`-p:SkipClientBuild=true` to skip it), so that half is closed |
| 10 | The game rounds are in memory, so a restart ends them and a second instance cannot share them. Fine for one host; a shared store is needed before scaling out |
| 11 | The content review of 12 Nov 2026 flagged 510 of the 876 Voorzetselpaden cards, 74 of them as nonsense to drop — chunks that are not governed prepositions (`werken volgens`, bare `sinds`), invented idioms (`de moer onder de kinderen geven`) or scenes that cannot be read. Nothing has been deleted; the verdicts sit on the cards. B1+ and B2 hold 58 of the 74, so their scope is the first question. Report: `~/claude-scratch/voorzetselpaden-content-md-review-2026-11-12.md` |
| 12 | Two shipped errors the review found in `prepositions.json`, both unfixed: the `praten-tegen` control question is keyed `true` but its picture and sentence say the listener is not listening, and the separable-verb hints in `texts.prepositions.json` tell the learner the prefix goes last ("staat achteraan") when every accepted answer puts it straight after the verb |
| 13 | `assets/verb-propositions/incoming/` holds 50 redraws nothing references, including fresh copies of the two scenes dropped as nonsense. `assets/claude/incoming/` is 13 MB of the same kind. Neither is committed; decide whether raster source art belongs in git at all |

## Working style the owner expects

- Lead with the answer. Keep it short; expand only when asked.
- Disagree when you think he is wrong, in the first line, with the reason.
- Never report something as working without having run it.
- Show visual changes before committing to them. A one-line description of a
  colour change is not enough for him to judge it, and a change he approved
  from a description has already had to be reverted once.
