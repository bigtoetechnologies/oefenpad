# Voorzetselpaden art to redo

Fifty-four images were rejected on 13 Nov 2026 (five, then 49) and A2+ is mostly ungenerated. Both are queued for the next Grok session, planned for Wednesday 18 Nov 2026 evening.

## Rejected on 13 Nov, first round (5 cards)

| Card id | Page | Chunk | Note |
|---|---|---|---|
| `komen-door-hond` | `a2.html` | dat komt door | Rejected by the owner |
| `komen-door-regen` | `a2.html` | dat komt door | Rejected by the owner |
| `komen-door-storm` | `a2.html` | dat komt door | Rejected by the owner |
| `komen-door-zon` | `a2.html` | dat komt door | Rejected by the owner |
| `vragen-om-geld` | `a1.html` | vragen om | Characters completely shaded in |

The five PNGs are moved out of `assets/verb-propositions/incoming/` to `~/claude-scratch/rejected-images/2026-11-13/`. Observation, not the owner's reason: the four `komen-door` images draw the figures white on a cobalt ground, the reverse of the other sets.

All five cards are back to the "not drawn yet" placeholder on their pages.

To redo `dat komt door`: `tools/grok/grok.py prompt a2 "dat komt door"`, then `tools/grok/grok.py` `new`, `compose`, `send`, `wait`, `download`, as in `tools/grok/README.md`. The earlier prompt is `~/claude-scratch/oefenpad-a2-run/a2-dat-komt-door.txt`.

## Rejected on 13 Nov, second round (49 cards)

| Card id | Page | Owner's reason |
|---|---|---|
| `vragen-om-hulp` | `a1.html` | Rejected by the owner |
| `vragen-om-pen` | `a1.html` | Rejected by the owner |
| `werken-aan-fiets` | `a1.html` | Looks nothing like a bike |
| `werken-bij-kantoor` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `werken-bij-winkel` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `zeggen-tegen-collega` | `a2.html` | Wrong colour |
| `zoeken-naar-sleutels` | `a0.html` | Character has no face |
| `beginnen-met-hardlopen` | `a2-pairs.html` | A man panting, not running |
| `beschermen-tegen-regen` | `a2.html` | Face is solid block colour, not cobalt outline on white |
| `beschermen-tegen-zon` | `a2.html` | Faces filled in |
| `betalen-voor-kassa` | `a2-pairs.html` | Jagged, pixelated or fuzzy edges; the character pours tea instead of paying |
| `denken-aan-eten` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `denken-aan-huis` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `denken-aan-persoon` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `denken-aan-vakantie` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `denken-over-keuze` | `a2.html` | Jagged, pixelated or fuzzy edges; face shaded in |
| `denken-over-twee-autos` | `a2.html` | Jagged, pixelated or fuzzy edges; faces shaded |
| `denken-over-twee-huizen` | `a2.html` | Jagged, pixelated or fuzzy edges; faces shaded |
| `denken-over-twee-reizen` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `doorgeven-aan-buur` | `a1.html` | Jagged, pixelated or fuzzy edges (the owner wrote `doorbrengen-aan-buur`; read as this card) |
| `doorgeven-aan-collega` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `doorgeven-aan-kind` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `doorgeven-aan-medespeler` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `houden-van-kat` | `a0.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `houden-van-muziek` | `a0.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `kiezen-voor-taart` | `a2-pairs.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `kijken-door-kier` | `a1.html` | Strange head shape |
| `kijken-door-microscoop` | `a1.html` | Strange head shape |
| `kijken-door-sleutelgat` | `a1.html` | Strange head shape |
| `kijken-naar-schilderij` | `a2-pairs.html` | Face shaded |
| `kijken-uit-balkon` | `a1.html` | Face shaded; jagged, pixelated or fuzzy edges |
| `kijken-uit-treinraam` | `a1.html` | Very strange head shape |
| `klagen-bij-leidinggevende` | `a2.html` | Faces shaded, strange shapes |
| `klagen-bij-receptie` | `a2.html` | Faces shaded, strange shapes |
| `krijgen-van-vriend` | `a2-pairs.html` | Faces shaded |
| `last-hebben-van-hoofdpijn` | `a0.html` | Face shaded |
| `last-hebben-van-lawaai` | `a0.html` | Faces shaded |
| `last-hebben-van-muggen` | `a0.html` | Face shaded |
| `letten-op-verkeer` | `a0.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `praten-met-collega` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `praten-tegen-muur` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `praten-tegen-scherm` | `a2.html` | Poor quality (jagged, pixelated or fuzzy edges) |
| `tevreden-zijn-met-resultaat` | `a2.html` | Strange head shape |
| `uitkijken-voor-hond` | `a2.html` | No dog: there is a tram; one man has his arm through another |
| `uitnodigen-voor-het-feest` | `a1.html` | Strange character and head shapes |
| `uitnodigen-voor-wandeling` | `a1.html` | Strange heads |
| `vallen-uit-bed` | `a1.html` | Face shaded |
| `vragen-aan-buur` | `a1.html` | The man asking faces away from the other person instead of facing him |
| `vragen-om-advies` | `a1.html` | Poor quality (jagged, pixelated or fuzzy edges) |

The PNGs are backed up in `~/claude-scratch/rejected-images/2026-11-13/`, along with the four band pages and the old `base-prompt.txt` as they were before this round (`html-before/`). All 49 cards are back to "not drawn yet". Together with the first five, 54 cards need art again.

The recurring faults, and how the base prompt was changed for them, are in the section below.

## Base prompt changes after the 13 Nov feedback

`Docs/voorzetselpaden/base-prompt.txt` was changed to answer the recurring faults. The old version is in `~/claude-scratch/rejected-images/2026-11-13/html-before/base-prompt.txt`.

"Poor quality" means jagged, pixelated or fuzzy edges. Zoomed against good images, the bad ones show stair-stepped edges, speckle and thin lines that break up, mostly where the drawing has hairline strokes or fine detail (spokes, stitching, small windows). This is read from four images, not tested.

| Owner's feedback | Change |
|---|---|
| Faces shaded or filled in; face in block colour | The face stays white inside a cobalt outline and is never filled or shaded. Only hair is solid |
| Strange head shapes | Natural, proportionate human heads: slightly oval, chin, ears, neck. Not a perfect circle |
| Wrong colour | One cobalt only, no lighter or darker blue; never a cobalt background or a white drawing on blue |
| Poor quality: jagged, pixelated, fuzzy | New line-quality rule: thick bold lines only, no hairlines or fine detail, smooth crisp edges, no broken lines |
| Not a bike, a tram instead of a dog, panting instead of running, pouring instead of paying | New section: draw every named object recognisably and the action asked for, not a nearby one |
| The man asking faces away | When people speak to, ask or give to each other, they face each other |
| (all) | A check before returning: natural faces, smooth bold lines, cobalt on white, action matches; redraw any that fail |

A first draft limited drawings to three objects besides the figures. It was softened to "few large elements" because several briefs name more than three.

## A2+ (`a2-plus.html`), not yet usable

| State | Chunks | Images | Where |
|---|---|---|---|
| Generated and downloaded, owner has not accepted them | 31 | 55 | `~/claude-scratch/oefenpad-a2plus-run/out/` |
| Started, no zip (stopped mid-generation) | 1 (`langs`) | 2 | Chat link in `run.log` of that folder |
| Never started | 31 | about 41 | Prompts in the same folder; `plan.txt` lists them in order |

The owner is checking the 31 downloaded chunks one by one on 13 Nov. Nothing is rejected or accepted yet.

## Before the next run

| Item | Reason |
|---|---|
| Make `run.sh` stop at the first failed download | On 13 Nov it carried on after 31 failed downloads and spent the Grok quota |
| Start Chrome on the Grok profile with `--remote-debugging-port=9333` and sign in | The old session had timed out |
