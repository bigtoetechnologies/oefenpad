# Game art

Every image inside a game is a brush drawing in the logo's hand: cobalt ink on
bare paper, one idea, no words.

This is the shared style guide for clue images, card faces, scene art, reels,
trophies and card backs. It does not cover the painted blocks in the interface
(`designguide.md`), the logo itself, or the 157 photographic word images in
`assets/wordimages/` — those are placeholders, not the target style.

The per-game briefs say *what* each image must show. This says *how* it must be
drawn.

| Brief | What it supplies |
|---|---|
| `voorzetselpaden/a0-a2.html` | The thirty pilot preposition scenes, one card per frame, with their contrasts and what each must not suggest |
| `story-machine-art.md` | The 72 reel tiles, by reel and word |
| This file | Stroke, colour, composition, prompt and checklist |

## The idea in one line

The logo is the reference. A game image should look like it was drawn by the
same hand that painted the O and the P: a few confident, tapered cobalt strokes,
visible bristle splits, loose ends, and a lot of paper.

| Claim | Consequence |
|---|---|
| The stroke is the line | Not a flat vector silhouette, not an icon with a uniform outline |
| Paper is part of the drawing | Transparent background; empty space is composition, not a gap to fill |
| One idea per image | If the silhouette needs a caption, redraw it |

Scene art is drawn in the same hand at sketch weight: a bold brush-pen
drawing with a wide nib, visible dry-brush streaks and directional hatching —
not a thin pen-and-ink illustration and not a pictogram. See *Style anchors*.

## Non-negotiables

These are inherited from `decisions.md` and `designguide.md`.

| Rule | Why |
|---|---|
| No text, letters or numbers in the image, ever | One art set serves every first language; the words are drawn in HTML |
| Cobalt only, no orange | Orange still means "do this now"; the logo's orange dab stays in the logo |
| No culture-specific or Dutch souvenir imagery | The audience is international |
| No meaning carried by colour alone | The drawing must carry the meaning |
| Readable at 64 px | That is a phone-sized clue or reel tile; line weight has to carry it |
| One idea per image | A learner has one glance to connect the picture to the chunk |
| Transparent, vector where possible | It has to sit on paper in both themes |
| Scene art is 2:3 portrait | 512 × 763 shipped; one ratio and one camera keep contrast pairs comparable |

The logo's orange accent is brand identity, not an art convention. Do not copy
it into a scene. If an image needs an accent, use a heavier cobalt stroke.

## Style anchors

Three delivered scenes define the target. Measure a new image against them; if
it would not pass unnoticed beside these three, it is not finished.

| Anchor | What it anchors |
|---|---|
| `wachten-op-vriend.png` | People: seated, in profile, the fold of a coat and a chair |
| `wachten-op-trein.png` | Place: rails in perspective, a figure seen from behind |
| `wachten-op-eten.png` | Hands and objects on a tabletop, in perspective |

All three live in `assets/verb-propositions/referenceimages/`, are 784 × 1168
RGB PNGs with the white paper baked in, and use an ink core of about
`#0A41A6`–`#1657C9`, hue 218–220°. Measured at 784 px wide:

| Measure | Target | How it was measured |
|---|---|---|
| Ink coverage | 14–22% plain, to 27% busy | share of pixels with `min(r,g,b) < 200` |
| Typical stroke | 4–8 px | 60–65% of the ink survives a 3 px erosion, 30–40% a 5 px erosion |
| Boldest contour | 9–14 px | the chair frame, a rail, the edge of a table |
| Hatching | 2–4 px | dense directional strokes on folds and under objects |
| Subject extent | scene 90–100% of the width; person 35–55% | the person is half the scene, not the whole frame |
| Filled mass | hair, plus one or two small accents | clothing, furniture and background stay white inside the contour |

**Where the coverage figure comes from.** The fifty drawn scenes in
`assets/verb-propositions/incoming/` measure 13–27% by the definition above,
median 18. The three anchors measure 14.0, 15.4 and 18.5. An earlier version of
this table said 13–17% with a 20% failure threshold; seventeen of the fifty
broke it, and so did one anchor, so the threshold was describing nothing.
Coverage scales with how much is in the scene: one person on a bench sits near
the bottom of the range, two people with furniture near the top. Judge the
drawing against the anchors, not the number — a generator given a ceiling
will draw thin to stay under it.

The stroke is a **wide-nib brush or chisel marker**, not a pen. Each line is a
broad band with pressure variation, dry-brush streaks and split bristles; the
ink is dark and solid at the core, not pale or washed out. The contour is gone
over a second time on one or two edges. Hatching is drawn in quick, dense
clusters that read as tone at arm's length, with paper still visible between
the strokes.

The fifty shipped scenes went the other way: solid black clothing, big eyes and
motion lines. They are too heavy. But a drawing that comes back as a thin,
even pencil line has also missed the anchors — the reference line is bold,
rough and inky. That is why this is a redraw rather than a tweak.

## The brush

At 784 px wide — the delivered source size — these weights hold:

| Role | At 784 | At 512 shipped | What it does |
|---|---|---|---|
| Primary contour | 9–14 | 6–9 | The shape that must survive at 64 px |
| Secondary | 4–8 | 3–5 | Internal structure, limbs, object parts |
| Detail and hatching | 2–4 | 1.5–3 | Folds, hair, shadow, tabletop lines |

The primary contour becomes roughly 1 px at 64 px. Anything thinner than
2 px at 784 is not load-bearing; if the meaning depends on it, draw it at
primary weight instead. A contour drawn at 1 px at 784 reads as pencil, not
brush.

### One edge, drawn twice

The old rule was one stroke per edge. The anchors do not obey it: they go over
an important edge a second time, a few pixels off, or leave a pale guide line
running beside the final one. That second pass is what makes the result read as
a drawing rather than a traced icon.

- The second pass goes on **one** or **two** edges of a shape, never as a
  symmetrical outline around both sides.
- It may stop short or overshoot by 3–6 px at 784.
- It is thinner than the edge it doubles, usually secondary weight.

### Taper

Every stroke starts thin, widens around the middle or the point of pressure,
and ends thin. The logo's O is a single looping stroke that overshoots its own
start; the P has a long descending stem that narrows as it falls.

A uniform `<line>` or a `stroke-width` that never changes is a pen line, not a
brush. Draw the stroke as a closed, filled shape:

```svg
<!-- a tapered stroke, not a line -->
<path d="M40 80 C90 70 140 74 180 64 C140 88 90 92 40 80 Z"/>
```

Draw with a pressure-sensitive brush in a vector editor and expand the stroke
to an outline if that is easier. The delivered SVG must contain the shape, not
a dependency on the tool.

### Roughness

Roughness is selective. The stroke has a hand, not a noise texture laid over
the whole image.

- Cut two or three narrow bristle splits into one edge of the widest strokes.
  Run them with the stroke; do not scatter dots.
- Let the edge wobble by 1–3 units. Do not make every edge equally ragged.
- Let joins be loose: one stroke can overshoot another by 2–4 units, or stop
  1–3 units short at a corner. Closed, mechanical corners read as vector art.
- Do not close every shape. The logo's frame leaves the corners imperfect.

### What not to draw

Form is line, then hatching, then mass — in that order of preference. The
anchors are contour drawings: interiors stay white and shadow is built with
hatching, not filled in.

- No solid masses beyond hair and one or two small accents. A figure whose whole
  coat is painted black belongs to the old fifty, not to this set.
- No flat vector silhouettes with a uniform outline around them.
- No thin, even pencil line. The contour is a broad, rough brush stroke with
  pressure variation, doubled on one or two important edges. If the drawing
  looks delicate, it is wrong.
- No symmetrical outline tracing both sides of every shape. A second pass on one
  edge is a sketch; a second line all the way round is an icon.
- **Hatching is allowed and wanted**, in one form only: quick, directional
  strokes clustered on the shadow side of a fold or under an object. The strokes
  follow the form, vary in length, and may touch or run together, but the paper
  must still show inside the cluster and they must not become a solid fill or a
  cross-hatch. They must read as a tone at arm's length, not as decoration.
- No gradients, drop shadows, inner shadows, blur, grain or paper-texture
  overlay. The hatching is drawn, not filtered.
- No photographic detail. A face is not the subject, but it is not a smiley
  either; see *People and animals*.
- No decoration. Background is allowed only as **one place cue** — the door, the
  platform, the window that tells the learner where they are. Never wallpaper,
  scenery or a full room.

### People and animals

The audience is adult, and the drawing is a clue, not a cartoon.

- Adult proportions. A standing figure is about seven heads tall, a seated one
  about four. The anchors are drawn from life, not from an icon set.
- Face in profile or three-quarter: a brow, one eye under it, a nose line, a
  mouth, an ear. That is the whole face. No second eye bulging at the viewer, no
  open mouth, no sweat drops, no motion lines around the head.
- Hair is the one place that carries mass: a filled, brushy shape with a few
  strokes through it, as in all three anchors.
- Hands are drawn, not mittened. A thumb and the line of the fingers is enough,
  as on the table in `wachten-op-eten.png`.
- Clothing is contour plus hatching folds, never a black fill. Where the old
  fifty painted a coat solid, draw the outline, hatch the shadow side and let
  the paper show.
- No skin colour. There is one ink.
- Do not caricature. The person is a learner in an everyday situation, not a
  type.

## Composition

Scene art is 512 × 763, 2:3 portrait. Everything else starts at 512 × 512,
`viewBox="0 0 512 512"`.

| Rule | Detail |
|---|---|
| Canvas | 2:3 portrait for scene art; square for tiles, reels and card faces |
| Safe area | 32 units at 784, 20 at 512; the drawing may cross it, nothing required may fall outside it |
| Subject extent | The scene spans 90–100% of the width; the person is 35–55%; it may touch the left or right edge, with paper kept at top and bottom |
| Camera | One camera for the set: eye level or slightly above. The anchors put the subject in the left half, facing right; reverse it only when the chunk reverses the direction |
| Place cue | One object in the other third completes the sentence — a door, a platform, a window, a table edge |
| Element count | One subject and one place cue. A third object only when the chunk needs it |
| Focus | The thing the sentence is about is the clearest mark, not necessarily the largest |
| Background | Paper, both in light and dark mode |
| Frame | None. The logo's border is the mark, not an image convention |
| Contrast pairs | Design the pair together: same camera, same scale, same composition; change only the meaningful element |

At 64 px the lines no longer resolve into a silhouette, so judge the reduced
image by whether the idea is still nameable — who is doing what, where. If it is
not, the composition is wrong, not the detail. A uniform heavy outline added to
save the small size puts the image back in the old style; the answer is a
clearer silhouette, not a thicker border.

For a contrast pair, look at the two images side by side at 64 px. Neither may
suggest the other's sentence. Designing one and then deriving the other
produces near-duplicates with the wrong emphasis.

## Colour and background

| | |
|---|---|
| Light | Cobalt `#2B50C8` |
| Dark | Cobalt `#5C7DEB` |
| Measured ink core in the anchors | `#1657C9`, hue 218–219° |
| Background | Transparent. No white plate, no paper-coloured rectangle |
| Depth | Stroke weight, overlap and hatching, not a second blue or a grey |

The logo uses one cobalt. Do not add `--kobalt-diep` or `--kobalt-licht` to an
illustration to create depth; that is a page-fill behaviour, not an art one.

A generated PNG will not land on the token exactly — the anchors sit at a
slightly deeper `#1657C9`. That is fine, because the shipped file is a mask on a
cobalt block and never carries its own colour; do not correct the hex in the
raster.

Game art has to survive the theme swap without a second file:

- Preferred: inline SVG with `fill="currentColor"`, and CSS sets
  `color: var(--kobalt)`. The token swaps with the theme.
- If the image must be an `<img>`, use a CSS mask on a cobalt block rather than
  baking `#2B50C8` onto a white background.
- Never ship a white rectangle behind the drawing. On dark paper it becomes a
  bright card, and the brush disappears.

### Do not use the interface paint filter

`data-verf` and the `#op-verf` / `#op-verf-klein` filters belong to rectangular
UI fills. Their `baseFrequency` is tuned to the 300 × 150 and 100 × 30 viewBoxes,
and `verf()` is applied by JavaScript. Art must render with JS off and at any
size.

A static brush filter is allowed if it is tuned to the 512 viewBox and checked
at both 512 px and 64 px. The `#lijn` filter in
`design-options/i-penseellijn.html` is the starting point; retune
`baseFrequency` for 512 rather than copying the 1440-wide values. Geometry with
real bristle gaps is more reliable than a filter and is preferred.

Option I was rejected as a *home-page composition*, not as an illustration
style. It is the closest existing visual reference for the brush as a line, and
the frame in option H shows the same loose-corner behaviour. Do not re-propose
either as a page layout; use them to judge a drawing.

## Files and naming

| What | Where |
|---|---|
| A game's own art | `assets/<game>/art/<id>.svg` |
| Story Machine card backs | `assets/storymachine/art/<id>.jpg` (existing) |
| Story Machine tiles | emoji placeholders in `server/Oefenpad.Resources/Games/Data/reels.json` until drawn |
| Preposition scenes | `assets/voorzetselpaden/<scene-id>.png` (shipped raster; see *Delivered raster art*) |
| Shared art | `assets/shared/art/<id>.svg` |

The games themselves live in `client/src/games/`; art never sits beside the
code any more, because only `assets/` is served. A picture's id is what the
server sends in a round view (for example `/assets/wordimages/animals/dog.jpg`).

- One file per idea. Ids are stable, lowercase and hyphenated; they match the
  data key or scene id.
- Do not duplicate a shared image into each game. Put it in `assets/shared/art/`.
- Raster is a placeholder, not a deliverable. The shipped exceptions are the
  BigToe mascot card back in `assets/storymachine/art/`, which is waiting to be
  replaced, and the thirty preposition scenes described below. New art still
  starts as an SVG.

The filename is not the alt text. For a picture-clue exercise the image is the
question, so do not put the answer in `alt`; the exercise's prompt carries the
accessible name. Whether picture-clue games can be made fully screen-reader
playable is a separate accessibility question, not something the artwork can
solve.

## Delivered raster art

The fifty Voorzetselpaden scenes are the one shipped exception to "SVG, 512 ×
512". Batch 1 arrived as 784 × 1168 PNGs; batches 2 and 3 as 1152 × 1712
files; batch 4 mostly at 784 × 1168 with one at 1152 × 1712. All arrived with
the white paper baked in and drawn at 2:3 portrait. The originals stay untouched
in `assets/verb-propositions/archived/`, one folder per batch. They are kept for
provenance only; the three images in `referenceimages/` are the only source art
the redraw uses.

They are not used as they arrived. A baked white background becomes a bright
card on dark paper and the brush disappears, so each file is processed into an
alpha mask and shipped at `assets/voorzetselpaden/*.png`, 512 × 763:

```python
# paper -> 0, ink -> 255; the floor keeps near-white noise out of the mask
d = 255 - min(r, g, b)
a = 0 if d <= 10 else round((d - 10) * 255 / 245)
```

The ink is not recoloured. The mask is drawn on a cobalt block in CSS, so the
theme swap happens without a second file and `--kobalt` stays the only ink:

```css
.beeld{
  background:var(--kobalt);
  -webkit-mask-image:var(--beeld); mask-image:var(--beeld);
  -webkit-mask-size:contain; mask-size:contain;
  -webkit-mask-position:center; mask-position:center;
  aspect-ratio:512/763;
}
```

Set `--beeld` inline per element with `url("art/<scene-id>.png")`. No JavaScript,
no filter, and it renders on paper in both themes.

The portrait ratio is no longer an exception: 2:3 is the default for scene art,
because all the images have one camera and one scale, which is what makes the
contrast pairs comparable. Cropping to squares would cut each scene differently.
Scene art starts at 784 × 1168 and ships at 512 × 763. Square 512 × 512 remains
the default for tiles, reels, trophies and card faces.

A picture-clue tile must not carry the answer in its accessible name. The choice
buttons get `aria-label="Beeld 1"` and the drawing is `aria-hidden`; only the
Ontdek card, where the image is the content, uses the scene's `alt`.

## Generation prompt

One block per fresh context: attach the three style anchors, paste this header,
then that batch's subject list. The header is byte-identical every time and the
anchors are re-attached every time — that is what holds the style still when
Grok's context is reset. The batch order is in `Docs/voorzetselpaden/a0-a2.html`, in the
collapsible *Plan en kaders* section under *Redraw pass*; the paste-ready header and all ten batch blocks are in
`prepositions-art-redraw-prompts.md`.

Do not attach the old drawings being replaced. In a fresh context they read as
the target, and the result is a traced copy of the cartoon.

### Locked header

> You are drawing a set of Dutch verb + preposition scene illustrations for
> Oefenpad. Three finished images are attached: `wachten-op-vriend.png`,
> `wachten-op-trein.png` and `wachten-op-eten.png`.
>
> They are the line reference. Match their drawing exactly: the same bold
> brush-pen line, the same rough ink texture and hatching, the same amount of
> detail, the same composition and camera. Do not copy their subjects,
> furniture or poses, and do not introduce a fourth style.
>
> **Style.** Bold brush-pen sketch, cobalt blue only (#2B50C8; the references
> measure about #0A41A6–#1657C9), on plain white. This is a wide-nib brush or
> chisel marker drawing, not a pencil, fine-liner or engraving. Every contour
> is a broad, pressure-varying band with visible dry-brush streaks and split
> bristles; important edges are gone over a second time, a few pixels off, and
> corners are left open. The ink is dark and solid at the core of each stroke,
> and the line stays loose and energetic — not neat, polished or vector-smooth.
> Interiors stay white — this is not a silhouette or an icon.
>
> **Line weight** at 784 px wide: most lines 4–8 px, the boldest contours 9–14
> px, detail and hatching 2–4 px. Total ink 14–22% of the canvas for a
plain scene and up to 27% where it holds two figures and furniture; below 13%
the drawing is too thin. The figure scales with how much is in the scene —
never thin a busy scene to reach a number. No hairline
> contours. Fill hair only, plus one or two small accents; do not fill
> clothing, furniture or background.
>
> **Shading.** Quick, dense directional hatching on the shadow side of a fold
> or under an object: clusters of 2–4 px strokes that follow the form, with
> white paper still visible inside the cluster. Hatching must read as a tone
> at arm's length, not as a few decorative lines. No cross-hatch, no
> gradients, no drop or inner shadows, no grain or texture overlay.
>
> **People:** adult proportions, profile or three-quarter view, facing right,
> placed in the left half of the frame. The face is a brow, one eye, a nose
> line, a mouth and an ear, with a focused, neutral expression. Hair is a
> filled mass with strokes through it. Hands have a thumb and finger lines. No
> cartoon faces, no open mouths, no motion lines, no stick figures.
>
> **Composition:** 2:3 portrait, 784 × 1168. The scene spans 90–100% of the
> width and the person 35–55%. One place cue in the other third — a door, a
> platform, a window, a table edge. Eye level or slightly above; tabletops and
> rails in simple perspective. The drawing may touch or bleed off the left or
> right edge; keep a margin of paper at top and bottom. No wallpaper, no full
> room.
>
> **Never:** text, letters, numbers, signs, arrows, logos, borders or frames;
> orange, a second blue or grey; Dutch souvenir imagery (windmills, clogs,
> tulips, canals, cheese); a thin, even, pencil-like line.
>
> Flat white background, no border, no shadow around the image.

### Batch protocol

| Rule | Why |
|---|---|
| **5 images per batch, maximum 6** | Style drifts with batch size; the 114-image batch proved it |
| Keep a contrast family in one batch | `boos op` and `boos over` drawn apart get different line weights and stop pairing |
| Never split one frame's variants across batches | The three `wachten op` images are the anchors *because* they were drawn together |
| Same anchor files attached every time | Attaching them only at the start lets the style decay by batch three |
| Reject and redo, do not patch | Restyling a cartoon by thinning its outline leaves a thin cartoon |
| Batch 1 is a test | Draw only the first batch, compare against the anchors at full size and at 64 px, then continue |

The output is a sketch, not a deliverable. Pipeline it as described in
*Delivered raster art*: alpha mask, 512 × 763, tinted by CSS. Do not ship the
raster and do not correct its blue.

## Do / Don't

| Do | Don't |
|---|---|
| Draw the contour, then hatch the shadow | Fill a coat, a chair or a wall black |
| Draw bold, rough, pressure-varying strokes | Draw a thin, even pencil line |
| Use one weight for the edge and a lighter one for detail | Give every line the same thickness |
| Re-draw one or two edges a few pixels off | Outline both sides of every shape |
| Keep interiors white | Shade with a gradient or a filter |
| Let hatching build a tone | Cross-hatch or fill the shadow solid |
| Let the scene fill the frame and touch an edge | Shrink the subject into a card-sized pictogram |
| Give the frame one place cue | Fill the background with scenery |
| Draw the contrast family in one batch | Design one, then tweak a copy |
| Draw the face in profile, neutral | Draw a cartoon face with an open mouth |
| Use one cobalt | Add a second blue, grey or orange for depth |

## Checklist

- [ ] A Dutch speaker can name the target sentence from the image alone,
      without the English gloss.
- [ ] The idea is still nameable at 64 px.
- [ ] It passes unnoticed beside the three anchors at full size.
- [ ] Ink covers 14–22% for a plain scene, up to 27% for a busy one; most
      lines are 4–8 px at 784, bold contours 9–14 px.
- [ ] The line is a bold brush band with dry-brush streaks, not a thin even
      pencil line.
- [ ] Interiors are white; only hair and one or two small accents are filled.
- [ ] Shading is directional hatch clusters that read as tone, with paper
      visible inside them.
- [ ] Faces are in profile with a brow, one eye, nose, mouth and ear, and a
      neutral expression.
- [ ] The scene spans 90–100% of the width; the person is 35–55%; paper is kept
      at top and bottom.
- [ ] There is exactly one place cue, and it carries the chunk's location.
- [ ] The contrast pair is clearly different side by side, and neither image
      suggests the partner.
- [ ] No text, letters, numbers, logos or signage with readable marks.
- [ ] Cobalt only; no orange.
- [ ] 2:3 portrait, 784 × 1168 delivered, 512 × 763 shipped as an alpha mask.
- [ ] Flat white background, no frame and no shadow around the image.
- [ ] Renders in light mode, dark mode and with JavaScript off.

## Why the old word images do not set the style

The 157 images in `assets/wordimages/` are photorealistic white-background
product shots. They were inherited with the vocabulary games and are useful as
placeholders, but they are the opposite of the logo's hand: full colour, full
frame, no line, no paper. Do not add more in that style.

Replacing them is a separate, larger job. Until then, new art follows this
guide, and a mixed set is a known limitation rather than a reason to dilute the
style.
