# Oefenpad

A free Dutch practice site for adult newcomers to the Netherlands, most of
them studying for inburgering. Static HTML, no build step, no framework, no
backend. A companion paperback, *Quick Wins in Dutch*, is the acquisition
channel and lives in `book.md`.

The site is deliberately plain to deploy: open `index.html` over any static
server and it runs.

## Start here

| Read | To answer |
|---|---|
| `Docs/decisions.md` | Why the product is shaped this way. Read before proposing anything |
| `Docs/designguide.md` | Every visual rule. Canonical |
| `Docs/design-process.md` | Which designs were rejected and why, so you don't re-propose them |
| `Docs/game-catalogue.md` | What each game is and what exists |
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
- **Four games still use the old BigToe header** (`.header-right`, not
  `.balk .rechts`): galgje, geheugen, koppelen, woordzoeker. Code that
  touches the nav must handle both.

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

## Where things stand

All eight pages — home, the two legal pages, five games — are committed and
working, on one design system, bilingual, with a working theme switch.

Nothing is uncommitted. The remote is
`git@github.com:bigtoetechnologies/oefenpad.git`; `main` is **8 commits
ahead and unpushed**, so the whole redesign exists only on this disk. Push
only when the owner asks.

## Open and unverified

| # | Item |
|---|---|
| 1 | The no-JS fallback is reasoned correct but untested; headless `--disable-javascript` had no effect |
| 2 | `--grijs` on `--papier` in dark mode is unchecked for contrast |
| 3 | The twelve-bar week meter has no label. Nobody knows whether it reads as anything |
| 4 | Six content ideas from the rejected prototypes, listed at the end of `Docs/design-process.md` |
| 5 | The open questions in `Docs/decisions.md`: domain registration, a mascot, the free/premium line, audio for pillar 8 |

## Working style the owner expects

- Lead with the answer. Keep it short; expand only when asked.
- Disagree when you think he is wrong, in the first line, with the reason.
- Never report something as working without having run it.
- Show visual changes before committing to them. A one-line description of a
  colour change is not enough for him to judge it, and a change he approved
  from a description has already had to be reverted once.
