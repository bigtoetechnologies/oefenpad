# Voorzetselpaden — style A prompt

Style A is the clean pictogram look of the best early scenes: thick confident
marker, solid cobalt clothing, simple faces, no shading. This file holds the
prompt that reproduced it on 12 Nov 2026, the references it needs, and how far
it has been tested.

It does not yet replace the locked header in `game-art.md` or
`prepositions-art-redraw-prompts.md`. A three-image batch held together on 12
Nov 2026 (see *Test record*); switching the other docs over is a separate
decision.

## What style A is

Style A is a hand-drawn picture-book pictogram in one flat cobalt on white.

| Trait | Style A |
|---|---|
| Line | Thick, crisp, deliberate marker strokes that start and stop cleanly |
| Figures | Simplified: round head, dot or dash eyes, small mouth, simple hair |
| Clothing | Filled solid cobalt, with thin white gaps between parts |
| Skin, faces, hands | White inside a clean outline |
| Furniture and buildings | Clean outlines, the odd small solid accent |
| Shading | None: no hatching, gradients, tone or floor shadows |
| Paper | Pure white `#FFFFFF`, no texture |

The liked examples among the shipped fifty are `kijken-door-sleutelgat`,
`kijken-uit-raam`, `bedanken-voor-de-uitnodiging`, `komen-uit-huis` and
`doorbrengen-met-vriend`. The disliked ones, such as `wachten-op` and
`denken-aan`, are dry-brush: ragged edges and smeared ground patches.

Solid fills give each figure a strong silhouette, so style A survives the
phone choice tile (about 93 CSS px wide) better than a line-only style.

## How to use it

One fresh Grok chat per batch, with the three references attached.

1. Attach the three files in `assets/verb-propositions/referenceimages/style-a/`.
   They are the shipped masks rendered cobalt on white.
2. Paste the style block, then the scenes, format and delivery sections.
3. Name the zip and list every filename. Without that, Grok returns the images
   inline, and inline images cannot be fetched in bulk.
4. Review each image at full size and at phone tile size.

Attaching old drawings is deliberate here. The redraw doc forbids it because it
treats the old style as the thing being removed; for style A, it is the target.

## The style block

Paste unchanged. For a single scene, write "Make one new drawing in exactly
their style." in the first paragraph instead.

````text
Three drawings are attached: bedanken-voor-de-uitnodiging.png, komen-uit-huis.png and doorbrengen-met-vriend.png. Make three new drawings in exactly their style, one per scene below, all three drawn the same way. Copy how they are drawn, not their subjects or composition.

WHAT THE STYLE IS
- Bold, clean picture-book pictogram drawing in one flat cobalt blue on pure white. Think signage or a children's picture book, drawn by hand with a confident thick marker.
- Edges are crisp and deliberate. Every stroke starts and stops cleanly. No dry-brush streaks, no smearing, no fuzzy or ragged edges, no paint texture, no smudged ground patches.
- Figures are simplified: round head, simple face drawn with a dot or short dash for each eye and a small curve or line for the mouth, simple hair shape. No realistic anatomy, no detailed or modelled faces.
- Clothing is filled solid cobalt (jacket, trousers, dress), with thin white gaps where one part meets another (arm against body, collar, legs), so the shapes stay readable. Faces, hands and skin stay white inside a clean outline.
- Furniture and buildings (door, window, table, chair, sofa, house) are clean outlines, with the occasional small solid accent (a handle, a pot, a frame).
- No shading of any kind: no hatching, no crosshatching, no gradients, no tone, no shadows on the floor.
- Generous white space. The scene sits in the middle with nothing touching the edges. It must still read clearly as a small thumbnail on a phone.
- Colour: one flat cobalt, #2B50C8, nothing else. Background pure white #FFFFFF, no paper texture, no border, no shadow around the image.
````

## Scenes, format and delivery

Copy each scene brief verbatim from its batch doc, then close with these two
sections. Change the image count, zip name and filenames to suit.

````text
THE SCENES
<name>.png — <chunk> (<gloss>)
Scene: …
Must read: …
Avoid: …

FORMAT
Each image 784 × 1168 px, 2:3 portrait. No text, letters or numbers anywhere in the drawings.

DELIVERY
Return one zip named <batch-name>.zip containing exactly these files and nothing else:
<name-1>.png, <name-2>.png, <name-3>.png
Attach the zip to your reply.
````

## Why the earlier prompts drifted

Most of the drift came from wording that pulled against the references.

| Wording | What Grok did |
|---|---|
| The locked header's "dense directional hatching… must read as a tone" | Added hatching, then graphite crosshatch, which none of the references have |
| A ceiling on ink ("above 20% fails") | Drew thin and pale to stay under it |
| "Coloured pencil" | Pale, grey, graphite-weight lines |
| "Paper showing through" | Textured grey paper, which turns into a cobalt haze in the mask |
| "No paint texture, no dry-brush" | A clean, almost vector line — which turned out to be what was wanted |

## Test record

| Date | Chat | Scenes | Result |
|---|---|---|---|
| 12 Nov 2026 | `grok.com/c/d0c1ab0d-9464-4fdc-9b49-fe7fb0b0359b` | `zorgen-om-persoon` | Accepted as the target look. Brief miss: the photo stands on the table instead of being held up |
| 12 Nov 2026 | `grok.com/c/97aadcad-3a67-4d99-8969-14b463edb731` | `krijgen-van-vriend`, `passen-op-kind`, `trots-op-kind` | All three drawn the same way, and alike with the first test. All read at phone tile size. Brief misses: the receiver offers one open hand, not two cupped hands; the proud adult looks ahead rather than down at the child |

Test outputs are in `assets/claude/incoming/` as `style02_*.png` and
`style-a-01_*.png`.
