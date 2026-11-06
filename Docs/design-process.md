# How the home page was designed

A record of the 4 November 2026 design session: what was tried, what was
rejected and why, and what was chosen. The rules of the chosen direction are in
`designguide.md`; this file is the reasoning behind them, so a later session
does not re-run the argument.

The fifteen prototypes are preserved in `design-options/`. Open
`design-options/index.html` to see them side by side; each is a standalone
page with no dependency on the repo.

## What was being decided

A home page for a site whose users mostly cannot read English and are not
browsing for entertainment. The constraints came in from `decisions.md` and
did not change:

| Constraint | Effect on the design |
|---|---|
| Interface is Dutch | No English chrome; an EN layer may exist but stays secondary |
| Meaning travels in pictures and colour | No explanatory sentence can be load-bearing |
| No text inside artwork | One art set serves every learner |
| Orange means act now, nothing else | A single orange per screen |
| Must survive at 16px and on a phone | Logo and layout both |

A sixth constraint arrived during the session: the design must not look dated.
Stated plainly at 14:35 — the Delftware direction "has grown off me" — and
confirmed when nostalgia filters, card grids and serif display faces were all
ruled out.

## The rounds

Three rounds, narrowing each time. The first round tested whole visual
languages; the second and third tested one idea, the logo's brush stroke,
against itself.

| Round | Options | Question being asked |
|---|---|---|
| 1 | A–E | Which visual language, Delft or something else? |
| 2 | F, G | What does the brush stroke do when it fills a shape? |
| 3 | H–N | What does it do as an outline, and what else could the page be? |

Round 1 ended with A, D and E marked *naslag* — kept as reference, not in
contention. B and C survived. Round 2 repainted both: F is B painted, G is C
painted. Round 3 flipped the brush from fill to outline (H, I), crossed the
survivors (J, K), and then questioned the page itself (L, M, N).

## The fifteen options

<details>
<summary>Round 1 — five visual languages (A–E)</summary>

| | Name | What it was | Verdict |
|---|---|---|---|
| **A** | Delft, structureel | Cobalt half-page carrying a hugely enlarged tile motif; games as a ruled list with diamond markers. No tiles, no cards. | Reference only. The literal Delft reading is the dated one. |
| **B** | Schoolplaat, nu | One flat full-width canal scene — houses, bridge, boat, bikes — with words hanging as labelled leader lines. Thick ink outline, flat colour, no nostalgia filter. | Survived round 1. Judged childish on second look. |
| **C** | Nederlands modernisme | Visible 12-column grid, heavy grotesk, primary colour blocks. Games as modules of unequal size. | Survived round 1, became the chosen lineage. |
| **D** | Logboek | Graph paper, highlighter, handwritten marginalia, a checklist per day. The page as your own exercise book. | Reference only. Handwriting and highlighter are the nostalgia the brief rejects. |
| **E** | Penseel | The logo's stroke becomes the whole language: the path is one long painted haul, games sit on it as nodes. No tiles, no frames. | Reference only, but the brush idea it introduced drove rounds 2 and 3. |

Palettes diverged widely in this round. B ran on brick, ochre, moss and sand;
C on De Stijl red, yellow and blue; D on marker yellow and graphite. Only A
and E stayed near a cobalt. From F onward every option shares one palette.

</details>

<details>
<summary>Rounds 2 and 3 — the brush family (F–N)</summary>

| | Name | What it was | Verdict |
|---|---|---|---|
| **F** | Penseelplaat | B repainted: the same canal scene, now solid cobalt brush fills with bristle texture instead of flat shapes with thick outlines. | Strong, not chosen. Scene-led pages put the games below the fold. |
| **G** | Penseelraster | C repainted: the same rigid grid and heavy type, the colour blocks now painted fills with visible brush grain. | **Chosen.** |
| **H** | Penseelkader | G with the fills removed: every tile is a frame of four tapering strokes that just miss at the corners, echoing the logo's border. White paper, gaps between tiles. | Not chosen. Supplied the frame vocabulary that J, K, L and N reuse. |
| **I** | Penseellijn | F as contour drawing: the same canal in cobalt brush outlines on white, one orange door. | Not chosen. |
| **J** | Gracht + kader | Hybrid — I's scene on top teaching five words, H's frames below as navigation. | Not chosen. Parked idea, see below. |
| **K** | Gemeente | J with the postcard replaced by a real errand: a council counter, and labels showing a pattern rather than single words (*wachten → de wachtrij*). | Not chosen. Parked idea, see below. |
| **L** | Patroon | H with the picture removed and a pattern band in its place: *werkwoord + -ing = de …*, with four worked examples. | Not chosen. Parked idea, see below. |
| **M** | Hulptaal | L plus a selectable helper language (EN, УКР, PL, AR, or off) glossing words in small grey type beneath the Dutch. | Not chosen. Parked idea, see below. |
| **N** | Meteen beginnen | No shop window: the page *is* the first exercise. A drawing, empty letter boxes, letters to pick, and the other games as small framed links at the side. | Not chosen. Parked idea, see below. |

</details>

### Where the brush family splits

This is the distinction the whole second half of the session turned on. Every
option below uses the logo's stroke; they differ in what the stroke is doing.

| Option | The brush is… |
|---|---|
| E | the path — one long stroke carrying the games as nodes |
| F | a filled shape inside a picture |
| **G** | **a filled tile inside a grid** |
| H | the outline of an empty tile |
| I | the outline of a picture |
| J, K | both — outlined picture above, outlined tiles below |
| L, M | the outline, with the picture replaced by a grammar pattern |
| N | the outline, applied to live exercise controls |

Lineage: B → F → I, and C → G → H → L → M, with J and K crossing I against H,
and N taking H's frames into the exercise itself.

## Decisions

| # | Decision | When | Why |
|---|---|---|---|
| 1 | Drop the Delftware direction | 14:35 | It read as dated. The brush stroke from the logo survives; the blue-and-white tile reference does not |
| 2 | A, D, E out, kept as reference | 15:15 | A and D were the two most literal; E was elegant but gave the games no structure |
| 3 | B is too childish to lead | 15:15 | Second-party reaction. The flat scene with labels reads as a children's book, which misprices a product for adults doing inburgering |
| 4 | Try the brush as outline, not only as fill | 15:21 | Explicit request, and new options rather than edits, so the history stays |
| 5 | Keep every option as a file | 15:43 | Nothing is overwritten. This is why `design-options/` has fifteen pages |
| 6 | Mobile layouts for everything still in contention | 16:04 | A phone layout is part of the comparison, not a later chore |
| 7 | **Option G, rolled out to all pages and all games** | 16:25 | The grid gives every game equal, scannable weight; the paint supplies warmth without a picture to decode |
| 8 | Drop C's primary red and yellow | with 7 | De Stijl primaries fight the orange-means-act-now rule. G keeps cobalt, deep cobalt and orange only |
| 9 | Bilingual home page, NL default | 18:40 | English browser gets English, everything else gets Dutch. Verified against `en-GB`, `nl-NL`, and with JS off |
| 10 | The Geheugen tile becomes light cobalt | 6 Nov | The home page carried two oranges — that tile and the live bar in the week meter — which breaks the rule that orange marks one thing. The meter keeps the orange because it is the actual current step |

### Why G and not F

Both were painted versions of surviving round-1 options, so the choice was
between a picture-led page and a grid-led page.

The grid shows all five games above the fold and ranks them by tile size,
which is how a returning learner finds where they stopped. A scene teaches
five words well but pushes navigation down the page, and every new scene is
new artwork. The grid needs no artwork at all.

## Ideas parked, not rejected

These lost as home-page layouts. Their content ideas are better than the
layouts that carried them, and none of them is recorded elsewhere.

| From | The idea | Why it may still be worth doing |
|---|---|---|
| K | Labels teach a *pattern*, not a word — *aanvragen → de aanvraag* | Ties the site to the book's method. Five patterns beat five nouns |
| K | The scene is a real errand (council counter) rather than a postcard canal | Matches what an inburgering learner actually has to survive |
| L | A "pattern of today" band with four worked examples and the honest caveat *"Klopt niet altijd. Wel vaak genoeg om te durven gokken."* | A daily grammar hook that needs no artwork |
| M | Optional helper-language gloss, learner-selected, Dutch stays primary | Directly contradicts the current "no other languages" rule in `decisions.md`. Worth re-arguing, not worth doing by accident |
| N | The home page *is* the first exercise | Removes the shop window for a returning user. Could be the signed-in home page later |
| J | A scene that teaches five words, sitting above the navigation | Could be a section of the home page rather than a replacement for it |

## What shipped

Option G, applied to the whole site rather than the home page alone. All eight
pages load `assets/site/oefenpad.css` and `assets/site/oefenpad.js`: the home
page, the two legal pages, and all five games.

The legal pages themselves were adapted from bigtoegames with the names
changed, which is why `privacy.html` and `voorwaarden.html` predate the
redesign in content and follow it in styling.

Two colours from the old guide are now wrong wherever they still appear: the
cobalt `#1B3A6B` and the warm white `#FBF8F2`. The live palette is `#2B50C8`
on `#FFFFFF`. Four files still carried the retired values after the redesign;
all four were corrected on 6 November 2026:

| File | What it was | Fix |
|---|---|---|
| `Docs/prepositions-art.md` | Art-generation prompts, including the master prompt | Repointed at the live palette. Anything generated before this arrived in the wrong blue on the wrong white |
| `src/shared/common.js:165` | Default confetti colours — the only live code affected | Now cobalt, deep cobalt, light cobalt and the two oranges. The old warm white is dropped: white confetti on a white page is invisible |
| `Docs/reuse-bigtoegames.md:141` | Told a future session to use the old palette | Hexes updated |
| `Docs/identity/` | The 31 October identity sheet and three SVG marks, all in the old palette and referenced by nothing | Moved to `archive/identity-2026-10-31/` rather than recoloured — it is a record of a superseded identity, not a live asset |

## Still open

| # | Question |
|---|---|
| 1 | The week meter is twelve bars with no label. Does anyone know what it means? |
| 2 | Dark mode works on four games but not on the Story Machine, the home page or the legal pages. Finish it or drop it |
| 3 | `--grijs` on `--papier` in dark mode is unverified for contrast |
| 4 | The mascot, the tegeltje unit, and the free/premium line are all still open from `decisions.md` |
| 5 | Whether any parked idea above becomes real work |
