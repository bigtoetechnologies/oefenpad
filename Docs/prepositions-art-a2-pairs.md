# Voorzetselpaden — image plan, A2 pair enhancement (batch 4b)

Status: 14 of 16 drawn, not yet in the game, 10 November 2026; two scenes were
replaced on 12 November 2026 and are still to draw. This extends the shipped
A0–A2 set (`prepositions-art.md`, `prepositions-art-a0-a2.md`) with **sixteen**
frames that turn existing singles into contrast pairs and add two same-verb
pairs. The drawn PNGs are in `assets/verb-propositions/archived/04b-a2-pairs/`;
`prepositions.json` has not been touched. It changes no shipped code and settles
no product decision on its own.
`prepositions.md` and `prepositions-implementation.md` win where they disagree
with this file.

This is **batch 4b** of `prepositions-roadmap.md`. It is not batch 5 (the
spatial set, which opens the A2+ band and belongs in
`prepositions-art-a2-plus.md`). This file was called
`prepositions-art-a2-plus.md` until 10 November 2026; the **A2+** name now
belongs to the 80-frame spatial, adjective, noun and pronominal band in the file
of that name.

## Why this set exists

The shipped set has 19 single frames and only 12 contrast pairs. A single frame
has no partner in the Klopt step, so the learner never has to choose between
two near-identical chunks — which is the moment the preposition actually has to
be noticed. The cheapest pedagogical win left in A0–A2 is therefore not new
vocabulary but **partners for frames that already exist**.

Eleven of the sixteen new frames pair with art that already exists: ten upgrade
a single level to a pair and one upgrades `kijken` to a set of three. The other
five are new: two same-verb pairs (`betalen`, `rekenen`) and one lone single
(`kiezen voor`).

## What it changes

| | Shipped | After set A | After A + B |
|---|---|---|---|
| Frames | 50 | 61 | **66** |
| Scenes | 50 | 61 | **66** |
| Levels | 33 | 35 | **36** |
| Contrast pairs | 12 | 19 | **23** |
| Sets of three | 2 | 3 | **3** |
| Singles | 19 | 13 | **10** |
| Governed prepositions | 13 | 13 | **13** |

The set introduces **no new preposition**. Every frame reuses `aan, bij, door,
in, met, naar, om, op, over, tegen, uit, van, voor`. `tussen` was the one
candidate and was dropped; see *Why `kiezen tussen` was dropped* below.

Level changes:

- New levels: `betalen`, `kiezen` (set A), `rekenen` (set B).
- Singles that become pairs: `stappen`, `ophouden`, `meedoen`, `bang`,
  `geïnteresseerd`, `last hebben`, `komen` (set A); `zorgen`, `letten`,
  `doorgeven` (set B).
- `kijken` grows from a pair to a **set of three** (`door`, `uit`, `naar`), the
  third such level after `praten` and `vragen`.
- Level ids follow the existing cross-verb precedent (`zeggen`/`vertellen`,
  `bedanken`/`feliciteren`): the level is named after its first frame, not after
  an invented theme.

Three level ids currently name only one of their two partners and must be
renamed when the partner arrives:

| Old id | New id | Frames |
|---|---|---|
| `stappen-uit` | `stappen` | `stappen-uit`, `stappen-in` |
| `komen-uit` | `komen` | `komen-uit`, `gaan-naar` |
| `letten-op` | `letten` | `letten-op`, `passen-op` |

**This is a data migration, not just a rename.** Progress is stored per
`LevelId` (`GameProgressService`), so changing an id orphans that level's rows
for every existing user. In alpha that is acceptable; note it in the release
notes. If it is not acceptable, keep the old id and live with the misleading
name — the engine does not care, only the sheet and the catalogue do.

## The three pair types

| Type | What it trains | Shipped example |
|---|---|---|
| Same verb, two prepositions | the preposition *is* the meaning | `wachten op` / `wachten voor` |
| Same preposition, opposite or neighbouring meaning | one preposition across verbs | `bedanken voor` / `feliciteren met` |
| Set of three, one verb | the pattern drill, like a paradigm | `vragen aan/om/naar` |

`meedoen met` / `meespelen met` is a fourth, weaker kind: both take `met`, so it
trains the **verb** contrast, not the preposition. It is still worth drawing,
because the two verbs are easy to confuse and the shared `met` is what makes
them stick together in memory. The same applies to `kijken naar` /
`luisteren naar` (see *Deferred* below).

## Set A — the eleven

Eleven frames: one new same-verb pair (1–2), one lone single (3) and nine
frames that pair with shipped art — eight upgrade a single level to a pair (4,
5, 6, 8, 9, 10, 11) and one joins `kijken` as a set of three (7).

| # | File | Dutch frame | English | Scene | Pair / type | Status |
|---|---|---|---|---|---|---|
| 1 | `betalen-voor-kassa.png` | betalen voor | to pay for | Person at a plain counter pushes coins toward one object standing on it | Pair with 2; same verb, two prepositions | drawn |
| 2 | `betalen-met-kaart.png` | betalen met | to pay with | Same counter, same person: a bank card held up to a small terminal | Pair with 1; same verb, two prepositions | drawn |
| 3 | `kiezen-voor-taart.png` | kiezen voor | to choose | Person square-on at a plain table, an apple on the left and a cake on the right, one hand closed on the cake and the apple untouched | Single; `kiezen tussen` dropped 10 November 2026 | needed |
| 4 | `stappen-in-bus.png` | stappen in | to get into | Person with one foot on the bus step, one hand on the open door | Pairs shipped `stappen-uit-bus`; opposite | drawn |
| 5 | `beginnen-met-hardlopen.png` | beginnen met | to start with | Person crouched at the front door tying a running shoe, bottle beside | Pairs shipped `ophouden-met-roken`; opposite | drawn |
| 6 | `meespelen-met-band.png` | meespelen met | to play along with | Three people with simple instruments; the newest leans in and joins | Pairs shipped `meedoen-met-team`; same preposition | drawn |
| 7 | `kijken-naar-schilderij.png` | kijken naar | to look at | Person standing still, hands behind the back, facing a framed blank picture | Joins shipped `kijken-door` / `kijken-uit` as a set of three | drawn |
| 8 | `trots-op-kind.png` | trots op | proud of | Adult stands tall, hand on chest, looking at a child holding up a drawing | Pairs shipped `bang-voor-hond`; emotion family | drawn |
| 9 | `geloven-in-spiegel.png` | geloven in | to believe in | Person stands straight before a tall plain mirror, hand on chest, chin up | Pairs shipped `geinteresseerd-in`; same preposition | drawn |
| 10 | `genieten-van-zon.png` | genieten van | to enjoy | Person on a bench, leaning back, face up, eyes closed, a small sun above | Pairs shipped `last-hebben-van`; same preposition, opposite valence | drawn |
| 11 | `gaan-naar-gebouw.png` | gaan naar | to go to | Person seen from behind, bag in hand, walking toward an open doorway | Pairs shipped `komen-uit-huis`; opposite | drawn |

## Set B — the five

| # | File | Dutch frame | English | Scene | Pair / type | Status |
|---|---|---|---|---|---|---|
| 1 | `rekenen-op-vriend.png` | rekenen op | to rely on | Person steps onto a low plank over a puddle, held by another's hand | Pair with 2; same verb, two prepositions | drawn |
| 2 | `rekenen-met-regen.png` | rekenen met | to reckon with | Person beside a bicycle, looking at one grey cloud, folding a raincoat into a bag | Pair with 1; same verb, two prepositions | drawn |
| 3 | `zorgen-om-persoon.png` | zorgen om | to worry about | Person alone at a table, one hand holding a small framed photo of another person, the other hand at the forehead, shoulders hunched | Pairs shipped `zorgen-voor-kind`; same verb, two prepositions | needed |
| 4 | `passen-op-kind.png` | passen op | to look after | Person on a low stool beside a small child playing with a block | Pairs shipped `letten-op-verkeer`; same preposition | drawn |
| 5 | `krijgen-van-vriend.png` | krijgen van | to get from | One person places a plain object into the other's two cupped hands | Pairs shipped `doorgeven-aan-buur`; opposite direction | drawn |

Two caveats on set B, both for the reviewer rather than the painter:

- **2 — `rekenen met`** is correct but less frequent than `rekening houden met`.
  If the reviewer prefers the frequent form, substitute the chunk and the scene
  becomes "person makes a list and allows for rain", keeping the grey cloud. The
  drawing does not change.
- **3 — `zorgen om`** is usually reflexive in full (`zich zorgen maken om`). The
  bare frame is what this level uses. The scene must name the person worried
  about; a phone alone reads as `wachten op` or `bellen met`, not as `zorgen om`.

## Why `kiezen tussen` was dropped

`kiezen tussen` was briefed, drawn, and then cut on 10 November 2026. The chunk
is real Dutch — *kiezen tussen twee kwaden* is a set phrase — so it was not a
language error. It was the wrong frame for this set, for four reasons.

1. **Wrong category.** This set is about *vaste voorzetsels*: prepositions that
   have to be memorised because they are not predictable (`betalen **voor**`,
   `trots **op**`, `geloven **in**`). In `kiezen tussen` the preposition is
   literal: the person is physically between two doors. Nothing is being
   memorised, so the frame teaches no fixed chunk. This is the same objection
   that keeps `oversteken` and `afsnijden` out (see below).
2. **It dragged `tussen` in 20 frames early.** `tussen` is a spatial frame in
   the A2+ band (`tussen-twee-mensen.png`, A2+-01). Framing it here meant one
   preposition arrived for one frame, four batches before the set that teaches
   it properly.
3. **The drawing collided with A2+.** `kiezen-tussen-deuren` was *a person
   between two identical doors, hand on chin, touching neither*. A2+
   `twijfelen-tussen-twee-jassen.png` (#74) is *a person between two coats on
   pegs, one hand hovering, a finger on the chin, head tilted, neither touched*.
   Same scene, same gesture, different chunk.
4. **It is already scheduled where it works.** B1+ #111 pairs
   `kiezen-tussen-twee-banen` with `kiezen-uit-het-aanbod` — two equal posts
   against five boxes in a row. That is the contrast that actually teaches the
   chunk.

`kiezen-voor-taart.png` stays as a lone single: `kiezen voor` is a
high-frequency chunk the shipped 50 never framed, and it is worth one card.
`kiezen-tussen-deuren.png` is parked in
`assets/verb-propositions/archived/_dropped/`, not deleted.

## Deferred: `luisteren naar`

`luisteren naar` was considered as the natural partner of `kijken naar` and is
**not** in either set. The reason is structural, not artistic:

- A frame can carry only one `contrast` id, and the Klopt step builds items from
  every frame in the level whose `contrast` resolves — it does not check that the
  partner is *also* in the level.
- `kijken naar` is already needed inside the `kijken` set of three. Pairing it
  with `luisteren naar` in a second level would either duplicate the frame across
  two levels or generate a Klopt item against a scene the learner never saw in
  that level.

If it is wanted later, the clean option is a **`naar` family set of three**:
`kijken naar`, `luisteren naar`, `zoeken naar`. That moves `zoeken naar` out of
its single level and retires the `zoeken` level. Decide that separately; it is a
level-composition change, not an image.

## Not frames: `oversteken`, `afsnijden` and other separable verbs

`oversteken` and `afsnijden` came up in review and are **not** missing from this
set — they are not frames at all.

- `oversteken` splits: *ik steek de straat over*. `over-` is a separable prefix,
  not a governed preposition. The object (`de straat`) is a direct object.
- `afsnijden` splits the same way: *ik snijd een stuk af*. `af-` is a prefix.

A separable verb governs no preposition, so it was never a legal frame here.
This was settled on 10 November 2026 and the cut list is recorded in
`suggestions.md` under *Game idea: separable verbs (scheidbare werkwoorden)*,
which is also where these belong, as part of **Uit Elkaar**.

They are not "B1" either. `oversteken` is A1–A2 vocabulary and `afsnijden` is
A2–B1; the problem is the category, not the level. Other examples that look like
preposition frames but are prefixes: `tegenkomen`, `uitstappen`, `opbellen`,
`aankomen`, `meekomen`, `teruggeven`.

The exception is the opposite direction. At B2, some chunks that *contain* a
separable-prefix verb still govern a real preposition and stay here:
`aandacht vragen voor`, `inwerken in`, `rekening houden met`. The test is
whether the preposition after the chunk is fixed; if it is, it is a frame.

---

## Set A — images 1–11

````text
You have no file access. Do not ask to read any repository, document, image or
attachment. Everything you need is in this message.

TASK
Generate eleven separate images for a Dutch practice game called
Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch
verb or adjective plus a fixed preposition. The learner sees the image,
recognises the everyday situation, and connects it to the chunk. A Dutch speaker
must be able to name the situation from the drawing alone, without a caption.
The Dutch and English below are context for you only. None of those words may
appear in the image.

STYLE — FOLLOW EXACTLY
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  colour or full colour.
- Plain pure white background (#FFFFFF). No off-white, cream, beige or grey
  background. The white paper is intentional; it becomes transparency later.
  No gradients, soft shading, stippling, drop shadows, glow, blur, grain or
  paper texture. No border, frame, card, rounded rectangle or white plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. Strokes taper: thinner at the ends, wider at the
  point of pressure. At 784 px wide: most lines 4–8 px, boldest contours
  9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5). Ink covers
  14–22% of the canvas, up to 27% for a scene with two figures and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour. Never build the scene from filled
  silhouettes.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64 × 64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- Posture carries the meaning. The drawing is a clue for an adult learner,
  not a cartoon for children.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs anywhere. A sign in a scene must be blank. Blank speech
  bubbles are allowed as shapes, but they contain no letters, words or
  punctuation. Do not use a question mark.
- No decorative background: no plants, posters, wallpaper, shelves,
  landscapes or scenery that is not the idea.
- No culture-specific or Dutch souvenir imagery: no windmills, clogs, tulips,
  canals, cheese or similar. Everyday objects are fine.
- If the scene needs a caption to be understood, simplify or redraw it.

FORMAT
- Eleven separate images, one per subject.
- 2:3 portrait, for example 1024 × 1536 px. All eleven use the same camera,
  the same scale and the same line weight, because they sit side by side in one
  game.
- Raster PNG. Do not produce SVG code.
- No contact sheet, grid, collage or extra images. If you must return them one
  at a time, return them in the numbered order.
- Do not put the filename, a number or any label inside the image. Put the
  exact filename in the chat text above or below each image.

THE ELEVEN SUBJECTS, IN ORDER

1. betalen-voor-kassa.png — Dutch chunk: betalen voor (to pay for).
   Scene: one person at a plain shop counter, one hand pushing a few coins
   across the counter toward a single plain object standing on it, eyes on the
   object. The counter edge is a strong horizontal line.
   Must read: paying for the thing on the counter.
   Avoid: a bank card or terminal (that is #2); a queue of people; price tags
   or readable figures.

2. betalen-met-kaart.png — Dutch chunk: betalen met (to pay with).
   Scene: the same counter, the same person and the same object as #1; one
   hand holds a plain bank card up to a small terminal at the counter, the
   other hand rests on the object.
   Must read: paying by a means, a card.
   Avoid: coins lying on the counter (that is #1); a phone; readable card
   details or a signature.

3. kiezen-voor-taart.png — Dutch chunk: kiezen voor (to choose).
   Scene: one person stands square-on at a plain table with an apple on the
   left and a small plain cake on the right, the two side by side at the same
   distance from the person; one hand is closed on the cake and the apple
   stays untouched. Head and shoulders are turned to the cake. The two objects
   and the one gripped hand are the clearest marks.
   Must read: choosing the cake over the apple.
   Avoid: a bite taken out of the cake, a cut slice or a plate (those read as
   eating); coins, a card or price tags (that is betalen voor, #1 in this set);
   a shop counter or till; candles; two objects of the same kind; a second
   person. A single cake with the hands only reaching for it is zin in (A0–A2
   #85), not this frame.

4. stappen-in-bus.png — Dutch chunk: stappen in (to get into).
   Scene: one person with one foot on the step of a bus and one hand on the
   open door, body turned inward toward the dark interior, caught mid-movement.
   Must read: getting onto a bus.
   Avoid: stepping down out of the bus (that is the shipped stappen uit scene);
   a bus shelter; a ticket or a driver.

5. beginnen-met-hardlopen.png — Dutch chunk: beginnen met (to start with).
   Scene: one person crouched at a front door, tying a running shoe; a plain
   water bottle stands beside them on the ground.
   Must read: starting an activity.
   Avoid: a cigarette or ashtray (that is the shipped ophouden met scene); a
   finish line, a stopwatch or a race number.

6. meespelen-met-band.png — Dutch chunk: meespelen met (to play along with).
   Scene: three people standing in a loose half-circle, each holding a simple
   instrument — one guitar shape, one small hand drum; the third person leans in
   to join the group. One shared blank shape floats between them, like a chord.
   Must read: playing along with other people.
   Avoid: a board game or a table (that is the shipped meedoen scene); a stage
   with curtains; readable notes or a music stand with text.

7. kijken-naar-schilderij.png — Dutch chunk: kijken naar (to look at).
   Scene: one person standing still with both hands behind the back, facing a
   framed blank picture hanging on a plain wall. The frame is the second mass.
   Must read: looking at something on a wall.
   Avoid: a window, a keyhole or a mirror; a museum crowd; anything readable in
   the frame.

8. trots-op-kind.png — Dutch chunk: trots op (proud of).
   Scene: one adult standing tall with one hand flat on the chest, looking down
   at a child who holds up a blank sheet of paper with both hands. The adult's
   upright posture carries the meaning.
   Must read: pride in another person.
   Avoid: a trophy or cup (that is the shipped blij voor scene); a wrapped gift
   (that is the shipped feliciteren scene); a medal or a rosette.

9. geloven-in-spiegel.png — Dutch chunk: geloven in (to believe in).
   Scene: one person standing straight in front of a tall plain mirror, one
   hand on the chest, chin up, meeting their own reflection. The mirror frame
   is the second mass.
   Must read: believing in yourself.
   Avoid: praying hands or a church; a book on a table (that is the shipped
   geïnteresseerd scene); a second person.

10. genieten-van-zon.png — Dutch chunk: genieten van (to enjoy).
    Scene: one person sitting on a simple bench, leaning back with the face
    tilted up and eyes closed, a small plain sun in the upper corner; hands
    resting open on the knees.
    Must read: savouring something pleasant.
    Avoid: a cup of coffee and a slice of cake (that is the shipped zin in
    scene); two people (that is the shipped doorbrengen scene); a beach or a
    landscape.

11. gaan-naar-gebouw.png — Dutch chunk: gaan naar (to go to).
    Scene: one person seen from behind, bag in hand, walking up a short path
    toward the open door of a plain building. The doorway is ahead of them and
    the back view is essential.
    Must read: heading towards a place.
    Avoid: stepping out of a door towards the viewer (that is the shipped komen
    uit scene); a bus or a car (that is #4); readable signs.

CONTRAST PAIRS — DESIGN THESE TOGETHER
1 and 2 are a pair: same counter, same person, same object. Change only the
payment — coins pushed across the counter versus a card held to a terminal.
3 is a single: it has no partner in this set.
4 pairs with the shipped stappen uit scene: same bus, same camera, opposite
direction. Do not redraw the shipped scene.
7 joins the shipped kijken door and kijken uit scenes as a set of three. It
must not reuse their openings — no keyhole, no window.
5 pairs with the shipped ophouden met scene as an opposite. 6 pairs with the
shipped meedoen scene and must not reuse its table-game composition.
8, 9, 10 and 11 each pair with a shipped frame (bang voor, geïnteresseerd in,
last hebben van, komen uit). They do not share a camera, so the pair is
conceptual: keep scale and line weight identical so the cards still sit
together.
Draw each pair in the same sitting. At 64 × 64 px the two images must be
clearly different, and neither may suggest the other's chunk.

VALIDATION BEFORE YOU FINISH
For every image:
- Downscale mentally or actually to 64 × 64: is the idea still nameable?
- Is it cobalt only, with no orange, no grey and no second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or
  readable sign? Remove it.
- Are the strokes tapered filled shapes, not uniform outlines?
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check the pairs side by side. If either image in a pair suggests the
other's chunk, redraw it before delivering.

When finished, list the eleven filenames and name any image whose 64 px
silhouette is still ambiguous. Do not add any image that is not on this list.
````

---

## Set B — images 1–5

````text
You have no file access. Do not ask to read any repository, document, image or
attachment. Everything you need is in this message.

TASK
Generate five separate images for a Dutch practice game called Voorzetselpaden,
and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed
preposition. The learner sees the image, recognises the everyday situation, and
connects it to the chunk. A Dutch speaker must be able to name the situation
from the drawing alone, without a caption. The Dutch and English below are
context for you only. None of those words may appear in the image.

STYLE — FOLLOW EXACTLY
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  colour or full colour.
- Plain pure white background (#FFFFFF). No off-white, cream, beige or grey
  background. The white paper is intentional; it becomes transparency later.
  No gradients, soft shading, stippling, drop shadows, glow, blur, grain or
  paper texture. No border, frame, card, rounded rectangle or white plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. Strokes taper: thinner at the ends, wider at the
  point of pressure. At 784 px wide: most lines 4–8 px, boldest contours
  9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5). Ink covers
  14–22% of the canvas, up to 27% for a scene with two figures and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour. Never build the scene from filled
  silhouettes.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64 × 64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- Posture carries the meaning. The drawing is a clue for an adult learner,
  not a cartoon for children.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs anywhere. A sign in a scene must be blank. Blank speech
  bubbles are allowed as shapes, but they contain no letters, words or
  punctuation. Do not use a question mark.
- No decorative background: no plants, posters, wallpaper, shelves,
  landscapes or scenery that is not the idea.
- No culture-specific or Dutch souvenir imagery: no windmills, clogs, tulips,
  canals, cheese or similar. Everyday objects are fine.
- If the scene needs a caption to be understood, simplify or redraw it.

FORMAT
- Five separate images, one per subject.
- 2:3 portrait, for example 1024 × 1536 px. All five use the same camera, the
  same scale and the same line weight, because they sit side by side in one
  game.
- Raster PNG. Do not produce SVG code.
- No contact sheet, grid, collage or extra images. If you must return them one
  at a time, return them in the numbered order.
- Do not put the filename, a number or any label inside the image. Put the
  exact filename in the chat text above or below each image.

THE FIVE SUBJECTS, IN ORDER

1. rekenen-op-vriend.png — Dutch chunk: rekenen op (to rely on).
   Scene: two people; one steps onto a low flat plank laid over a puddle and
   holds the other's outstretched hand. The helper stands firm with both feet
   planted and takes the weight.
   Must read: depending on someone's support.
   Avoid: a calculator, coins or numbers; an umbrella; a crowd.

2. rekenen-met-regen.png — Dutch chunk: rekenen met (to reckon with).
   Scene: one person beside a bicycle, looking up at a single grey cloud, one
   hand folding a raincoat into a bag hanging on the handlebars.
   Must read: allowing for something in advance.
   Avoid: rain actually falling on the person (that is the shipped komen door
   scene); an open umbrella (that is the shipped beschermen scene); a calendar.

3. zorgen-om-persoon.png — Dutch chunk: zorgen om (to worry about).
   Scene: one person sitting alone at a table, one hand holding a small framed
   photo of another person up in front of them, the other hand pressed to the
   forehead; brow drawn down, shoulders hunched. The photo and the worried face
   are the clearest marks.
   Must read: worrying about someone.
   Avoid: an adult helping a child into a coat (that is the shipped zorgen voor
   scene); a second person in the room; a phone; a readable photo.

4. passen-op-kind.png — Dutch chunk: passen op (to look after).
   Scene: one person sitting on a low stool beside a small child who plays on
   the floor with a plain block. The adult watches the child, not the room.
   Must read: minding a child.
   Avoid: watching a road or a car (that is the shipped letten op scene); a pram
   with nobody attending it; a dog.

5. krijgen-van-vriend.png — Dutch chunk: krijgen van (to get from).
   Scene: two people facing each other; one places a plain small object into
   the other's two cupped hands. The receiver's cupped hands are the main mass.
   Must read: receiving something from someone.
   Avoid: a box passed over a fence (that is the shipped doorgeven scene); a
   wrapped gift with a ribbon; money or a wallet.

CONTRAST PAIRS — DESIGN THESE TOGETHER
1 and 2 are a same-verb pair. They do not share a scene, so keep scale and line
weight identical; the shared verb is the lesson.
3, 4 and 5 each pair with a shipped frame — zorgen voor, letten op and
doorgeven aan — and must not reuse those compositions or cameras.
Draw 1 and 2 in the same sitting so the two rekenen cards sit together.

VALIDATION BEFORE YOU FINISH
For every image:
- Downscale mentally or actually to 64 × 64: is the idea still nameable?
- Is it cobalt only, with no orange, no grey and no second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or
  readable sign? Remove it.
- Are the strokes tapered filled shapes, not uniform outlines?
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check 1 and 2 side by side. If either suggests the other's chunk, redraw
it before delivering.

When finished, list the five filenames and name any image whose 64 px
silhouette is still ambiguous. Do not add any image that is not on this list.
````

---

## Replaced scenes — 12 November 2026

Two drawn scenes did not match the chunk and were pulled from the batch:

| Old file | Why it failed | New file |
|---|---|---|
| `kiezen-voor-plank.png` | The drawing showed two identical beakers on a shelf, so the choice was between two identical objects, not one option over another. The filename also named the shelf, not the choice. | `kiezen-voor-taart.png` |
| `zorgen-om-telefoon.png` | A phone alone reads as `wachten op` or `bellen met`; `zorgen om` is about a person, not the device. | `zorgen-om-persoon.png` |

The first replacement for #3 was a bicycle against a bus in the rain, chosen on
12 November 2026 and dropped the same day: a turned foot and a hand still on the
bicycle are too subtle to read at 64 px. The frame now shows a cake taken over
an apple, so the choice is carried by two unequal objects and one gripped hand
rather than by stance.

The old PNGs are in `assets/verb-propositions/archived/_dropped/`. The new
scenes are briefed in the two prompts above and marked `needed`; they are not
drawn yet.

## After delivery

Delivered 10 November 2026: fourteen of the sixteen PNGs are in
`assets/verb-propositions/archived/04b-a2-pairs/`; `kiezen-voor-taart.png` and
`zorgen-om-persoon.png` are still to draw. The status column reads `drawn` for
the fourteen and `needed` for the two replacements. They are **not** in the game
yet. Remaining work, in order:

1. Process each drawn PNG the way batch 3 and batch 4 were processed: white paper to
   alpha, cobalt only, crop to 2:3, ship at 512 × 763 in
   `assets/voorzetselpaden/`. The delivered files are 784 × 1168 RGB with no
   alpha channel, so the paper has to be knocked out the same way batch 4's was.
2. Add the scene records and frames to
   `server/Oefenpad.Resources/Games/Data/prepositions.json`, with `contrast`
   pointing at the partner for pairs and `null` for singles. `kiezen voor` ships
   as a single.
3. Move the shipped partner into the new level or add it to the existing level:
   `stappen-uit-bus` and `stappen-in-bus` share one level, and so on for
   `ophouden`, `meedoen`, `bang`, `geïnteresseerd`, `last hebben`, `komen uit`,
   `zorgen`, `letten`, `doorgeven`. `kijken` keeps all three frames.
4. Give each new single a second `bouw` sentence so the level has three scored
   answers, as batches 3 and 4 did.
5. Rebuild the review sheet and check the new pairs side by side at 64 px.
   Until the frames are in `prepositions.json` the stock builder cannot see
   them; `tools/build-prepositions-preview.py` renders them from this table
   instead.
6. Check the 64 px silhouette in the game, not just in the generated file.
