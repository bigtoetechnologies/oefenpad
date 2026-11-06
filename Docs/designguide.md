# Oefenpad design guide

The rules for every Oefenpad page. This describes option **G, penseelraster** —
the direction chosen on 4 November 2026 and implemented in
`assets/site/oefenpad.css` and `assets/site/oefenpad.js`.

For how we got here and what was rejected, see `design-process.md`. The earlier
Delftware guide is kept at `archive/designguide-delft-2026-10-31.md` and no
longer applies.

## The idea in one line

A hard editorial grid, heavy grotesk type, and colour applied as if painted —
brush texture carried only in the fill of a block, never in its border.

Three claims follow from that, and the rest of this guide is their detail:

| Claim | Consequence |
|---|---|
| The grid is the structure | Hairline rules, no cards, no shadows, no rounded corners |
| The type is the decoration | Weight 900, tight tracking, large sizes; no ornament |
| The paint is the warmth | Texture lives in the SVG fill, applied to a minority of blocks |

## Colour

Four colours carry meaning; the greys are structure. Cobalt names a thing,
orange acts on it. Nothing else is allowed to signal.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--kobalt` | `#2B50C8` | `#5C7DEB` | Brand, links, painted blocks, done days |
| `--kobalt-diep` | `#15307F` | `#8FA8F2` | Second painted block, button hover |
| `--kobalt-licht` | `#7E9BE0` | `#3A57A8` | Tints only, never text |
| `--oranje` | `#E8601F` | `#FF7A3D` | The current step, the primary action, focus rings |
| `--oranje-diep` | `#C44A12` | `#FF9666` | Orange hover |
| `--inkt` | `#101522` | `#ECEFF5` | Body text, hard rules, the language toggle |
| `--papier` | `#FFFFFF` | `#0E1117` | Page |
| `--raster` | `#DFE2E8` | `#262C38` | Hairline rules |
| `--raster-zacht` | `#F2F4F7` | `#171C25` | Hover wash on plain tiles |
| `--grijs` | `#5C6578` | `#A3ACBD` | Secondary text |
| `--zacht` | `#8A91A1` | `#788295` | Tertiary text, timestamps |
| `--goed` | `#1F7A4D` | `#3FA873` | Correct answer |
| `--fout` | `#C4342A` | `#E8625A` | Wrong answer |

Rules:

1. Orange marks exactly one thing per screen — the live step or the primary
   button. A second orange makes both meaningless.
2. Pure white is the page, not a surface. There is no second elevation.
3. Dark mode is a token swap on `html.dark`, nothing more. Never write a
   second rule set.

The old Delft cobalt `#1B3A6B` and warm white `#FBF8F2` are retired.
`design-process.md` lists the four files still carrying them.

## Typography

One family, **Archivo**, loaded from Google Fonts at weights 400–900. The
system stack `system-ui, -apple-system, 'Segoe UI', sans-serif` is the
fallback and is close enough that a failed font load is not a broken page.

| Role | Size | Weight | Tracking |
|---|---|---|---|
| Hero `h1` | `clamp(34px, 6.4vw, 96px)` | 900 | `-.048em`, line-height `.88` |
| Game page `h1` | `clamp(24px, 2.8vw, 40px)` | 900 | `-.04em` |
| `h2` | `clamp(21px, 2.1vw, 30px)` | 900 | `-.035em` |
| `h3` | `clamp(17px, 1.6vw, 22px)` | 800 | `-.035em` |
| Tile name `.naam` | `clamp(18px, 1.9vw, 28px)` | 800 | `-.032em` |
| Body / reading `.lees p` | `15.5px` | 450 | line-height `1.65` |
| Tile blurb `.om` | `14px` | 500 | max `32ch` |
| Label `.et` | `12px` | 700 | — |

Headlines break by hand with `<br>`, because the line break is a composition
decision. Negative tracking is what makes the heavy weights read as designed
rather than as shouting; do not drop it when adding a new heading.

## Grid

Twelve columns, everywhere, with no gutters. The column count is the only
layout vocabulary the site has.

`.vel` is the sheet: `max-width: 1420px`, centred, with `--kolom` of
`clamp(16px, 2vw, 30px)` side padding and a hairline border left and right.
Those side borders disappear below 900px.

| Region | Class | Columns |
|---|---|---|
| Nav bar | `.balk` | brand 4, each link 2, right group `11/-1` |
| Hero | `.kop` | headline 8, side panel 4 |
| Week meter | `.meter` | 12 bars of 1 |
| Tile grid | `.raster` | spans set per tile |
| Reading column | `.lees` | 8, max `72ch` |
| Footer | `.voet` | 6 + 6 |

Below 900px the nav collapses to a 4-column grid, the hero stacks to full
width with the side panel moving under a top rule, and tiles drop their right
border. Nothing is hidden at small sizes.

## The painted fill

Colour arrives as paint, not as a flat swatch. `assets/site/oefenpad.js`
inserts an SVG behind any element carrying `data-verf`, filling it with a
four-point path whose corners are jittered, run through two `feTurbulence`
filters for bristle grain and edge displacement.

<details>
<summary>How to use it, and the constraints</summary>

| Attribute | Meaning |
|---|---|
| `data-verf="kobalt \| diep \| oranje \| licht"` | Which paint, matching the JS `KLEUR` map |
| `data-zaad="<n>"` | Seed for the corner jitter; fixes the shape across reloads |
| `data-verf-klein` | Uses the tighter `#op-verf-klein` filter, for small elements |

The element also needs class `geverfd` plus the matching colour class
(`kobalt`, `diep`, `oranje`, `licht`). That class sets a flat CSS background in the same
colour, so a page with JS disabled or still loading shows a solid block rather
than nothing. The painted SVG then lands on top. This fallback is the reason
the colour is specified twice; keep both in sync.

Constraints:

- Give every painted element a distinct `data-zaad`. Two blocks with the same
  seed get the same silhouette and the eye catches it.
- Paint a minority of blocks. On the home page, three of five tiles are
  painted and two are plain. All five painted reads as a toy.
- The filter re-runs on resize (debounced 150 ms) and after
  `document.fonts.ready`. Do not call `Oefenpad.verfAlles()` in a loop.
- Painted text is `--papier` at full strength; secondary text inside a painted
  block uses `.zacht`, which becomes `rgba(255,255,255,.82)`.

</details>

## Components

| Class | What it is | Notes |
|---|---|---|
| `.vel` | Page sheet | The outer frame; everything sits inside it |
| `.balk` | Nav bar | Hard `--inkt` rule beneath, logo + wordmark at 900 |
| `.kop` | Hero | Headline 8 cols, side panel 4 with a hairline left border |
| `.meter` | Week strip | 12 bars: `.gedaan` cobalt, `.nu` orange, rest grey |
| `.raster` / `.mod` | Tile grid | `.geverfd` painted or `.kaal` plain; `.kaal:hover` washes |
| `.knop` | Button | Square, weight 800, min-height 46px; `.oranje`, `.leeg`, `.klein` |
| `.vakje` | Cell | Letters and cards; `2px` inset shadow, states `vol/goed/fout/nu` |
| `.taal` | NL/EN toggle | Inset `2px` ink box, pressed state filled ink |
| `.lees` | Text column | Legal and prose pages; links are orange here |
| `.spel` / `.spel-kop` / `.werkvlak` | Exercise page frame | Title left, score right, hard rule under |
| `.voet` | Footer | Hard top rule, 6+6, pushed down by `margin-top:auto` |

The home page adds its own span classes (`.groot`, `.b2`–`.b5`) inline, because
the tile arrangement is specific to that page. Other pages should not copy
them; set spans for the layout you actually have.

## Bilingual pages

Every page ships both languages in the markup. An inline script in `<head>`
sets `data-taal` on `<html>` before first paint, so nothing flashes in the
wrong language.

Order of precedence: a stored choice in `localStorage['oefenpad-taal']`, then
the first entry in `navigator.languages` matching `nl` or `en`, then Dutch.
Dutch is also what a no-JS visitor gets, because `data-taal="nl"` is in the
static attribute.

CSS does the switching: `html[data-taal="nl"] [lang="en"]{display:none}` and
its mirror. To add translated text, wrap each version in a `<span lang="nl">`
and `<span lang="en">`. Page titles use `data-titel-nl` and `data-titel-en`
on `<html>`.

This covers Dutch and English only. Per `decisions.md` the product does not
translate into learners' own languages; meaning travels in pictures.

## Dark mode

A `dark` class on `<html>` swaps the tokens listed above. No component has a
second rule set, and nothing outside `:root` and `html.dark` should name a
colour literally.

The switch is an inline script at the top of each page's `<head>`, before
`oefenpad.css` loads, so the page never paints light and then flips:

| Step | Behaviour |
|---|---|
| Stored choice | `localStorage['oefenpad-theme']`, values `dark` or `light` |
| No stored choice | Follows `prefers-color-scheme` |
| Toggle | Any element with `id="theme-toggle"`; delegated click handler |
| Across tabs | A `storage` listener re-applies the new value |
| Canvas and JS drawing | Listen for the `themechange` event; `galgje/script.js` reads the class to colour its drawing |

Carried by four of the five games — galgje, geheugen, koppelen, woordzoeker.
The Story Machine, the home page and the two legal pages do not have the
script, so they stay light. That is an inconsistency, not a decision.

## Accessibility

| Requirement | How it is met |
|---|---|
| Focus visible | `.knop` and `.taal` take a 3px orange outline; `.mod` a 4px inset cobalt |
| Hit size | Buttons `min-height: 46px`, small variant 38px, toggle 32px |
| Reduced motion | `prefers-reduced-motion` kills animation and transition durations |
| Decorative SVG | Every painted layer is `aria-hidden` and `focusable="false"` |
| Language | `lang` is updated on `<html>` with every toggle, not only `data-taal` |
| Screen-reader text | `.alleen-lezer` clips without hiding |

Measured on the home page, 6 November 2026, sampling the rendered pixels:

| Pair | Light | Dark |
|---|---|---|
| `.zacht` on a `licht` painted tile | 5.56:1 | 4.92:1 |

Both clear AA for normal text. The painted tiles are the awkward case because
the fill is mid-tone; `kobalt`, `diep` and `oranje` all carry white or
near-black text and are not close to the line.

Still unverified: `--grijs` on `--papier` in dark mode, and whether a 12-bar
week meter is understandable without a label.

## What this design does not do

- No cards, shadows, gradients, or rounded corners. `--radius` is `0` and is
  not a knob to turn.
- No second typeface, and no script or display face.
- No souvenir Dutch imagery — windmills, clogs, tulips, canals, cheese.
- No text inside artwork, ever. One art set serves every learner.
- No colour-coded meaning that a reader must have been taught. Motif
  distinguishes, colour does not.
