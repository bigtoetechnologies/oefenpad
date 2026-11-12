# Voorzetselpaden — redraw prompts (anchor style)

Paste-ready blocks for bringing the older scene art into the `wachten-op-*`
style. The style itself is specified in `game-art.md` under *Style anchors* and
*Generation prompt*; the order and the reasoning are in
`prepositions-art-a0-a2.md` under *Redraw pass*.

## How to use this file

1. Start a fresh Grok context. Attach the three anchors from
   `assets/verb-propositions/referenceimages/`: `wachten-op-vriend.png`,
   `wachten-op-trein.png`, `wachten-op-eten.png`.
2. Paste the **locked header** below, then one batch block, in the same message.
3. One batch per fresh context. R1 and R2 may share a context if you accept a
   looser, lighter line by the ninth image.
4. Review the returns against the anchors at full size, then at 64 px. Reject
   and redo rather than patch.
5. Rename to `<name>.png` only at integration.

Rules that matter more than the wording:

- **Do not attach the old drawing.** In a fresh context it is the only
  finished-looking image, so it becomes the style reference and you get a
  traced cartoon back.
- **Do not shorten the header.** It is repeated every time precisely because
  nothing survives a context reset.
- **Deliver as `<name>-v2.png`** so the old file survives the comparison.
- **Reject a thin pencil result.** If the return has fine, even, delicate
  lines, the medium was read as pen-and-ink. Redo it with the header intact;
  do not thin the reference down to match the drawing.

## The locked header

```
You are drawing a set of Dutch verb + preposition scene illustrations for
Oefenpad. Three finished images are attached: `wachten-op-vriend.png`,
`wachten-op-trein.png` and `wachten-op-eten.png`.

They are the line reference. Match their drawing exactly: the same bold
brush-pen line, the same rough ink texture and hatching, the same amount of
detail, the same composition and camera. Do not copy their subjects,
furniture or poses, and do not introduce a fourth style.

**Style.** Bold brush-pen sketch, cobalt blue only (#2B50C8; the references
measure about #0A41A6–#1657C9), on plain white. This is a wide-nib brush or
chisel marker drawing, not a pencil, fine-liner or engraving. Every contour
is a broad, pressure-varying band with visible dry-brush streaks and split
bristles; important edges are gone over a second time, a few pixels off, and
corners are left open. The ink is dark and solid at the core of each stroke,
and the line stays loose and energetic — not neat, polished or vector-smooth.
Interiors stay white — this is not a silhouette or an icon.

**Line weight** at 784 px wide: most lines 4–8 px, the boldest contours 9–14
px, detail and hatching 2–4 px. Total ink 14–22% of the canvas for a
plain scene and up to 27% where it holds two figures and furniture; below 13%
the drawing is too thin. The figure scales with how much is in the scene —
never thin a busy scene to reach a number. No hairline
contours. Fill hair only, plus one or two small accents; do not fill
clothing, furniture or background.

**Shading.** Quick, dense directional hatching on the shadow side of a fold
or under an object: clusters of 2–4 px strokes that follow the form, with
white paper still visible inside the cluster. Hatching must read as a tone
at arm's length, not as a few decorative lines. No cross-hatch, no
gradients, no drop or inner shadows, no grain or texture overlay.

**People:** adult proportions, profile or three-quarter view, facing right,
placed in the left half of the frame. The face is a brow, one eye, a nose
line, a mouth and an ear, with a focused, neutral expression. Hair is a
filled mass with strokes through it. Hands have a thumb and finger lines. No
cartoon faces, no open mouths, no motion lines, no stick figures.

**Composition:** 2:3 portrait, 784 × 1168. The scene spans 90–100% of the
width and the person 35–55%. One place cue in the other third — a door, a
platform, a window, a table edge. Eye level or slightly above; tabletops and
rails in simple perspective. The drawing may touch or bleed off the left or
right edge; keep a margin of paper at top and bottom. No wallpaper, no full
room.

**Never:** text, letters, numbers, signs, arrows, logos, borders or frames;
orange, a second blue or grey; Dutch souvenir imagery (windmills, clogs,
tulips, canals, cheese); a thin, even, pencil-like line.

Flat white background, no border, no shadow around the image.
```

Emotion is allowed in the face, at one notch: brows down for anger, brows up
for fear, one mouth corner for pleasure. Never an open mouth, a wide cartoon
eye, a sweat drop or a motion line.

---

## R1 — blij / bang voor (4 images)

````text
Batch R1 — 4 images, 784 × 1168, 2:3 portrait, flat white.

1. blij-met-cadeau.png — blij met (happy with)
   Scene: one person standing three-quarters to the viewer, holding a plain
   gift box with a ribbon at chest height, looking down at it with a quiet
   smile. The box is the clearest mark in the frame.
   Must read: pleased with a thing they have.
   Avoid: a second person; a party; a bow so large it becomes a rosette; a
   price tag or any readable label.

2. blij-voor-vriend.png — blij voor (happy for)
   Scene: two people facing each other; the right-hand one holds a small
   trophy or a rolled diploma with no text; the left-hand one looks at that
   person's face, hands loosely together. The face of the person being
   congratulated is the clearest mark.
   Must read: glad about someone else's good news.
   Avoid: the congratulating person holding the object; a graduation cap with
   a motto; a crowd; applause or motion lines.

3. bang-voor-hond.png — bang voor (afraid of)
   Scene: one person stepping back from a dog that stands facing them, weight
   on the back foot, upper body turned away, one hand lifted to chest height.
   The empty space between them is part of the drawing.
   Must read: fear of the animal.
   Avoid: a calm dog being held or patted; a lead and an owner; cartoon
   barking, a tongue hanging out or spray lines.

4. beschermen-tegen-regen.png — beschermen tegen (to protect against)
   Scene: one person holds an umbrella over a second, smaller person. Both are
   dry; the rain falls diagonally and reaches the ground only beyond the
   umbrella's edge. The adult's outstretched arm is the clearest mark.
   Must read: one person shielding another from the weather.
   Avoid: one person alone under an umbrella; a coat pulled over the head;
   puddles with reflections; wind bending trees.

CROSS-CHECKS — draw these together
- blij met vs blij voor: blij met is one figure and the object in their hands
  is the focus; blij voor is two figures and the other person's face is the
  focus. Neither may be nameable as the other.
- bang voor vs beschermen tegen: fear is one figure retreating from an animal,
  protection is two figures under one umbrella. Only beschermen tegen has two
  people, and only bang voor has an animal.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R2 — klagen / boos op en over (5 images)

````text
Batch R2 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. boos-op-collega.png — boos op (angry at)
   Scene: one person squared up to a second, one hand raised with the palm
   flat and the forefinger up, brows down, mouth a flat line. The second
   person leans away with one hand lifted to chest height. The gap between
   them is part of the drawing.
   Must read: anger aimed at a person.
   Avoid: an object as the target; a fist or a raised chair; a crowd; speech
   bubbles or anger marks.

2. boos-over-rommel.png — boos over (angry about)
   Scene: one person standing over a tipped plant pot, soil across the floor,
   hands open at their sides, brows down. Nobody else in the frame. The mess
   is the clearest mark.
   Must read: anger about a thing or a situation.
   Avoid: a second person; someone tidying up; readable labels.

3. klagen-bij-balie.png — klagen bij (complain to)
   Scene: one person leaning on a plain counter with a low blank screen, one
   forefinger up mid-complaint; behind the counter a clerk stands still,
   listening. Both in profile, facing each other.
   Must read: complaining to a person or a company.
   Avoid: a broken appliance as the clearest mark; a queue; readable signs.

4. klagen-over-apparaat.png — klagen over (complain about)
   Scene: one person turned toward a washing machine with its door open, one
   hand on the open door, the other lifted toward the drum; the head is turned
   to the machine. No clerk, no counter. The machine is the clearest mark.
   Must read: complaining about a thing.
   Avoid: a phone; a service counter; the person repairing it.

5. last-hebben-van-lawaai.png — last hebben van (to be bothered by)
   Scene: one person at a table, both hands pressed over the ears, head down;
   a plain wall behind them. On the far side of the wall the only thing drawn
   is a hand-held drill. The wall divides the frame.
   Must read: bothered by noise coming from next door.
   Avoid: a construction worker; music or a party; a headache with no source;
   sound lines.

CROSS-CHECKS — draw these together
- boos op vs boos over: op is two people and the anger points at the person;
  over is one person and an object or mess. No over scene may contain a second
  person.
- klagen bij vs klagen over: bij has a clerk behind a counter and no broken
  object; over has the appliance and no clerk. Same camera so the difference is
  the setting, not the framing.
- last hebben van must not read as klagen over: the source of the noise is on
  the far side of a wall, and the hands are over the ears, not gesturing at the
  object.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R3 — door / uit + aan (5 images)

````text
Batch R3 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. kijken-door-sleutelgat.png — kijken door (to look through)
   Scene: one person bent slightly, one eye at a keyhole in a closed door, one
   flat hand on the door face. The door fills the right side of the frame and
   the keyhole is the clearest mark.
   Must read: looking through an opening in a door.
   Avoid: a key in the lock; an open door; a person on the other side.

2. kijken-uit-raam.png — kijken uit (to look out of)
   Scene: one person standing at a window, both hands resting on the sill,
   looking out. The window frame fills the upper right; below it a single
   street line. The person stands upright, not bent.
   Must read: looking out of a window.
   Avoid: a keyhole; a narrow slit; a garden with trees; the person looking at
   the viewer.

3. komen-door-regen.png — komen door (to be caused by)
   Scene: one person stepping in from the left, soaked: coat clinging, hair
   flat, no umbrella, one hand pointing back at the diagonal rain behind them.
   Must read: the rain is why they are wet.
   Avoid: an umbrella; puddles with reflections; a storm with bending trees.

4. komen-uit-huis.png — komen uit (to come from)
   Scene: one person with a suitcase stepping out of an open front door, one
   foot on the step, body turning toward the right of the frame; the doorway
   is behind them and they are dry.
   Must read: coming out of a house.
   Avoid: a bus or a car; a person going in; a key in the door; motion lines.

5. doorgeven-aan-buur.png — doorgeven aan (to pass on to)
   Scene: one person on the left holds a plain unlidded box out over a low
   fence; a neighbour on the right takes it with both hands. The hands and the
   box are the clearest marks; the fence is the boundary.
   Must read: handing something over to someone else.
   Avoid: a ribboned gift; money; a doorway or a shop counter.

CROSS-CHECKS — draw these together
- kijken door vs kijken uit: door is a keyhole in a closed door with the
  person close and bent; uit is a window with the person upright and the view
  wide. Neither may show the other's opening.
- komen door vs komen uit: door is the rain as the cause, with a wet person and
  no shelter; uit is a doorway being left, with a dry person. No komen-uit scene
  may be wet.
- doorgeven aan vs krijgen van (R10): here the giver's hands are out over a
  boundary; there the receiver's hands are cupped in front. Only one of the two
  may contain a fence, a counter or a doorway.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R4 — klaar met/voor, meedoen, ophouden, houden van (5 images)

````text
Batch R4 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. klaar-met-werk.png — klaar met (done with)
   Scene: one person leaning back in a chair, both hands behind the head, a
   closed laptop on a tidy desk. The desk edge and the closed lid are the
   clearest marks.
   Must read: finished with the work.
   Avoid: still typing; asleep; a celebration; scattered papers.

2. klaar-voor-feest.png — klaar voor (ready for)
   Scene: one person at an open front door, coat on, a small bouquet or a
   plain box in one hand, looking out. The open door is the clearest mark.
   Must read: dressed and ready to leave for a party.
   Avoid: still working; wrapping a gift; already at the party; a mirror.

3. meedoen-met-team.png — meedoen met (to join in)
   Scene: three people seated round a table with a simple board game; a fourth
   pulls a chair in from the left, one hand on the chair back, body leaning
   into the group. The joining figure is the clearest mark.
   Must read: joining a group that is already doing something.
   Avoid: a spectator standing away; a classroom; a queue.

4. ophouden-met-roken.png — ophouden met (to stop doing)
   Scene: one person stubbing a cigarette out in an ashtray on a table, one
   hand flat on the table, head turned slightly away, mouth set. Calm and
   decided, not angry.
   Must read: stopping, on purpose.
   Avoid: smoking; throwing a packet away; a branded pack; a crossed-out
   symbol.

5. houden-van-hond.png — houden van (to love)
   Scene: one person kneeling beside a calm dog, one arm round its neck, head
   close to the dog's head. Both relaxed; the pair is the clearest mark.
   Must read: affection for an animal.
   Avoid: a barking or aggressive dog; a lead and an owner; a vet; a collar
   tag with text.

CROSS-CHECKS — draw these together
- klaar met vs klaar voor: met is finished, the body loose at the desk; voor is
  dressed and at the door, about to leave. Neither may contain the other's
  setting.
- meedoen met vs ophouden met: joining is a group making space; stopping is one
  person putting a thing down.
- houden van vs bang voor (R1): same animal, same size, same camera. One leans
  in, the other steps back. Neither may be nameable as the other.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R5 — praten / zeggen / vertellen (5 images)

````text
Batch R5 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. praten-met-vriend.png — praten met (to talk with)
   Scene: two people facing each other across a table, both speaking: one open
   hand each, raised between them, eye contact. Nothing sits between them on
   the table.
   Must read: a two-way conversation.
   Avoid: one person turned away; a topic object on the table; speech bubbles.

2. praten-over-huis.png — praten over (to talk about)
   Scene: two people at a table with a small model house standing between
   them; both lean toward it, one points at it with a flat hand, the other
   looks at it.
   Must read: two people discussing a subject they both refer to.
   Avoid: a plain chat with no object; a real building; readable plans.

3. praten-tegen-muur.png — praten tegen (to talk at)
   Scene: one person facing a plain wall, hands open at waist height, mouth in
   a flat line, head slightly forward. There is no listener anywhere in the
   frame.
   Must read: talking with nobody listening.
   Avoid: a second person; a phone; a doorway; a poster on the wall.

4. zeggen-tegen-persoon.png — zeggen tegen (to say to)
   Scene: one person leaning in close to another's ear, one hand cupped at the
   mouth, saying one short thing; the other stands still, listening, not
   answering. The cupped hand is the clearest mark.
   Must read: one short remark aimed at one person.
   Avoid: two equal talkers; a speech bubble; a crowd; a whisper mark.

5. vertellen-aan-kind.png — vertellen aan (to tell to)
   Scene: an adult seated and leaning toward a child, both hands open in front
   at chest height, telling something longer; the child looks up with the
   head tilted. The adult's two open hands are the clearest mark.
   Must read: telling a longer story to a listener.
   Avoid: a cupped hand at the mouth; a book; a classroom; a crowd.

CROSS-CHECKS — draw these together
- met vs over vs tegen: met is mutual, both speak, nothing between them; over
  is mutual with a topic object between them; tegen is one-sided with nobody
  listening. No met scene may have a dominant object; no over scene may read as
  a plain chat; no tegen scene may contain a facing listener.
- zeggen tegen vs vertellen aan: zeggen is short, close to the ear, one hand at
  the mouth; vertellen is longer, seated, both hands open, the listener
  engaged. Same two-figure camera, so the difference is gesture and distance,
  not framing.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R6 — uitkijken naar/voor + vragen aan/naar/om (5 images)

````text
Batch R6 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. uitkijken-naar-vakantie.png — uitkijken naar (to look forward to)
   Scene: one person standing with a suitcase at their feet, looking at a wall
   calendar; one day on the calendar is circled and has a small sun drawn in
   it. The circled day is the clearest mark.
   Must read: looking forward to a future event.
   Avoid: numbers or letters on the calendar; a map; a beach scene; a clock.

2. uitkijken-voor-auto.png — uitkijken voor (to watch out for)
   Scene: an adult holds a child back by the shoulder at a kerb; a single car
   approaches on the road beyond it. The child leans forward, the adult's grip
   is the clearest mark.
   Must read: warning someone about a present danger.
   Avoid: a warning triangle with marks; a crash; a traffic light; motion
   lines behind the car.

3. vragen-aan-persoon.png — vragen aan (to ask a person)
   Scene: one person turned toward another, one hand raised palm up, brows up;
   the other listens with the head slightly tilted. No object, no counter,
   nothing being held.
   Must read: asking a person directly.
   Avoid: a counter or form; an object changing hands; a question mark; two
   equal speech bubbles.

4. vragen-naar-informatie.png — vragen naar (to ask about)
   Scene: one person at a plain counter pointing at a folded blank map lying
   on it; a clerk behind the counter listens. One route line may be drawn on
   the map, but no letters, numbers or pin labels.
   Must read: asking for information about something.
   Avoid: readable text or numbers; a question mark; the map being handed over.

5. vragen-om-hulp.png — vragen om (to ask for)
   Scene: one person holds out an open upturned hand; a neighbour places a box,
   bag or ladder rung into it. The object and the two hands are the clearest
   marks.
   Must read: asking for a thing, and getting it.
   Avoid: money; a counter or a map; two people merely talking.

CROSS-CHECKS — draw these together
- uitkijken naar vs uitkijken voor: naar is a future event, the person faces a
  calendar with the suitcase packed by their feet; voor is a present danger,
  the person faces the traffic and holds someone back. Neither may contain the
  other's cue.
- vragen aan vs naar vs om: aan has no object at all, only a person; naar has
  an information object on a counter; om has an object moving between hands.
  No aan scene may contain a handed object; no om scene may contain a counter
  or a map.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R7 — werken aan/bij, zoeken, zin in, zorgen voor (5 images)

````text
Batch R7 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. werken-aan-project.png — werken aan (to work on)
   Scene: one person leaning over a table with a large sheet of paper spread
   out, a pencil in one hand and the other hand holding the sheet flat, sleeves
   pushed up. The sheet is the clearest mark.
   Must read: working on a thing that is in progress.
   Avoid: a company building; a lanyard; a finished building; a plain laptop
   with nothing else.

2. werken-bij-bedrijf.png — werken bij (to work at)
   Scene: one person standing at the entrance of a plain building with a door
   and two windows, a lanyard round the neck with no text on it. The building
   front is the clearest mark.
   Must read: being employed at a company.
   Avoid: a blueprint or tools; a customer queue; readable signs; working from
   home.

3. zoeken-naar-sleutels.png — zoeken naar (to search for)
   Scene: one person crouched down, one hand reaching under a sofa or table,
   head lowered; a set of keys lies on the floor just out of reach. The keys
   and the reaching hand are the clearest marks.
   Must read: searching for something lost.
   Avoid: the keys already in the hand; a magnifying glass; a lost-and-found
   counter with text.

4. zin-in-koffie.png — zin in (to feel like)
   Scene: one person seated, both hands round a cup, looking at a slice of
   cake on the table; the cup and cake are the clearest marks.
   Must read: wanting something pleasant.
   Avoid: a full meal; a menu with text; someone already drinking with a blank
   face; a shop.

5. zorgen-voor-kind.png — zorgen voor (to care for)
   Scene: an adult crouched to a child's height, tying a scarf or fastening a
   coat; a small school bag stands on the floor. The child holds one arm out,
   the adult's hands are the clearest marks.
   Must read: looking after someone, hands on the task.
   Avoid: a doctor or a nurse; a hospital; an embrace; scolding.

CROSS-CHECKS — draw these together
- werken aan vs werken bij: aan is a sheet or a model on a table indoors; bij is
  a building front and a lanyard. No aan scene may contain a facade; no bij
  scene may contain the work itself.
- zorgen voor vs houden van (R4): care is doing something for the child — coat,
  scarf, bag; love is holding the animal. No zorgen-voor scene may be an
  embrace.
- zoeken naar: the object is visible but not yet in the hand. If the hand holds
  it, the scene is wrong.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R8 — beginnen, meespelen, rekenen met, betalen met/voor (5 images)

````text
Batch R8 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. beginnen-met-hardlopen.png — beginnen met (to start with)
   Scene: one person crouched on a front step tying a running shoe, a bottle
   standing beside them. The shoe and the laces are the clearest marks.
   Must read: starting something new.
   Avoid: running; a finish line; a watch; numbers.

2. meespelen-met-band.png — meespelen met (to play along with)
   Scene: three people with simple instruments — a drum, a guitar shape, one
   standing to sing; a fourth leans in from the left with an instrument,
   joining them. The joining figure is the clearest mark.
   Must read: joining in with people already playing.
   Avoid: a stage with lights; an audience; sheet music with notes; a drummer
   mid-strike with motion lines.

3. rekenen-met-regen.png — rekenen met (to reckon with)
   Scene: one person beside a bicycle, looking up at one single cloud drawn as
   a contour, folding a raincoat into a bag. The folded coat is the clearest
   mark.
   Must read: taking bad weather into account.
   Avoid: rain falling; a wet person; a phone with a weather symbol; a
   lightning bolt.

4. betalen-met-kaart.png — betalen met (to pay with)
   Scene: one person at a plain counter holding a bank card up to a small card
   terminal that stands on the counter; the other hand is flat on the counter.
   The card and the terminal are the clearest marks.
   Must read: paying by card.
   Avoid: coins; a readable screen; a receipt with text; a queue.

5. betalen-voor-kassa.png — betalen voor (to pay for)
   Scene: the same plain counter and the same person, now pushing a small pile
   of coins across the counter toward one object standing on it. The coins and
   the object are the clearest marks.
   Must read: paying for a thing, in cash.
   Avoid: a card or a terminal; a queue; readable price tags.

CROSS-CHECKS — draw these together
- betalen met vs betalen voor: identical camera and identical counter; only the
  payment changes — a card to a terminal, or coins pushed toward the object
  being bought. Neither may contain the other's payment method.
- rekenen met vs rekenen op (R9): met is taking something into account — the
  folded raincoat and the single cloud; op is being supported by a person.
- beginnen met vs ophouden met (R4): beginning is a shoe being tied, the body
  about to move; stopping is a cigarette being put out, the body settling.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R9 — rekenen op, geloven in, kijken naar, gaan naar, stappen in (5 images)

````text
Batch R9 — 5 images, 784 × 1168, 2:3 portrait, flat white.

1. rekenen-op-vriend.png — rekenen op (to rely on)
   Scene: one person stepping onto a low plank laid over a puddle, one hand
   held by another person standing on the far side. The held hands and the
   plank are the clearest marks.
   Must read: depending on someone for support.
   Avoid: a bridge; a handshake between equals; two people walking side by
   side; a puddle with reflections.

2. geloven-in-spiegel.png — geloven in (to believe in)
   Scene: one person standing straight before a tall plain mirror, one hand on
   the chest, chin slightly up. The mirror and the reflected figure are the
   clearest marks; the reflection is the same posture, contour only.
   Must read: believing in oneself, seen in a mirror.
   Avoid: a shop mirror with a price tag; two different people; a motto or a
   caption; a weight scale.

3. kijken-naar-schilderij.png — kijken naar (to look at)
   Scene: one person standing still, both hands behind the back, facing a
   framed blank picture on a wall. The frame is the clearest mark.
   Must read: looking at a picture.
   Avoid: an easel with paints; a museum crowd; a readable plaque; the person
   holding anything.

4. gaan-naar-gebouw.png — gaan naar (to go to)
   Scene: one person seen from behind, a bag in one hand, walking toward an
   open doorway; the doorway is the clearest mark and the person is nearer the
   viewer than the door.
   Must read: heading toward a place.
   Avoid: already inside; a bus or a car; a sign above the door; motion lines.

5. stappen-in-bus.png — stappen in (to get into)
   Scene: one person with one foot on the bus step, one hand on the open door
   frame, body turned into the bus. The step and the door edge are the clearest
   marks.
   Must read: getting into a vehicle.
   Avoid: stepping down out of it; a queue; the driver's face; a readable
   destination sign.

CROSS-CHECKS — draw these together
- rekenen op vs rekenen met (R8): op is support from a person — a held hand and
  a plank; met is taking a condition into account — the raincoat and the cloud.
- geloven in vs kijken naar: geloven in has a mirror and the person's own
  reflection; kijken naar has a picture and hands behind the back. No
  geloven-in scene may be a plain viewer; no kijken-naar scene may contain a
  reflection.
- gaan naar vs stappen in: naar is walking toward a building door; in is a foot
  already on a vehicle's step. Only stappen in has a vehicle.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## R10 — genieten, krijgen, kiezen, passen op, trots op, zorgen om (6 images)

````text
Batch R10 — 6 images, 784 × 1168, 2:3 portrait, flat white.

1. genieten-van-zon.png — genieten van (to enjoy)
   Scene: one person on a bench, leaning back, face turned up, eyes closed,
   arms along the back of the bench; a small sun drawn above them in contour.
   The face and the sun are the clearest marks.
   Must read: enjoying something pleasant.
   Avoid: a beach or a sea; sunglasses; a phone; a picnic spread.

2. krijgen-van-vriend.png — krijgen van (to get from)
   Scene: one person places a plain object into the other's two cupped hands;
   the receiver's cupped hands and the object are the clearest marks. The giver
   is on the left, the receiver on the right, facing each other.
   Must read: receiving something from someone.
   Avoid: a ribboned gift; money; both hands holding the object; a doorway or a
   fence.

3. kiezen-voor-taart.png — kiezen voor (to choose)
   Scene: one person stands square-on at a plain table with an apple on the
   left and a small plain cake on the right, the two side by side at the same
   distance from the person; one hand is closed on the cake and the apple
   stays untouched. Head and shoulders are turned to the cake. The two objects
   and the one gripped hand are the clearest marks.
   Must read: choosing the cake over the apple.
   Avoid: a bite out of the cake, a cut slice or a plate (those read as
   eating); coins, a card or price tags; a shop counter or till; candles; two
   objects of the same kind; a second person; a single cake with the hands
   only reaching for it.

4. passen-op-kind.png — passen op (to look after)
   Scene: one person on a low stool beside a small child playing with a block
   on the floor; the adult watches the child, hands still in the lap.
   Must read: watching over someone else's child.
   Avoid: tying a coat or a scarf; a cot; a playground crowd; a doctor.

5. trots-op-kind.png — trots op (proud of)
   Scene: an adult standing tall, one hand flat on the chest, looking down at a
   child who holds up a drawing; the drawing has no readable marks on it.
   Must read: pride in someone else's achievement.
   Avoid: a trophy; a crowd; the adult holding the drawing; applause lines.

6. zorgen-om-persoon.png — zorgen om (to worry about)
   Scene: one person alone at a table, one hand holding a small framed photo of
   another person up in front of them, the other hand pressed to the forehead;
   brow drawn down, shoulders hunched. The photo is the clearest mark. Nobody
   else in the room.
   Must read: worrying about someone.
   Avoid: a phone; a second person in the room; a readable photo; a clock.

CROSS-CHECKS — draw these together
- krijgen van vs doorgeven aan (R3): the same handover with the opposite camera
  — here the receiver's cupped hands are in front and there is no boundary;
  there the giver's hands go out over a fence.
- passen op vs zorgen voor (R7): op is watching a child at play, seated and
  still; voor is hands-on, tying a coat or a scarf.
- kiezen voor vs betalen voor (R8): both put a hand on an object on a flat
  surface; here two objects stand equal and one is gripped, there coins go
  across a counter and nothing is picked up.
- zorgen om vs zorgen voor (R7): om is worry about a person, shown by the
  framed photo and the hunched shoulders; voor is care, two people and a task.
- trots op vs blij voor (R1): trots op is looking down at a child's work, chest
  up; blij voor is two adults at eye level, one holding the good news.

VALIDATION
For every image: the idea is still nameable at 64 px; the line is a bold brush
band, not a thin pencil line; ink 14–22% of the canvas, up to 27% for a
scene with two figures and furniture; no fills except
hair and one or two small accents; cobalt only; no text, numbers, arrows or
readable signs; 784 × 1168, 2:3 portrait, flat white, no border and no shadow
around the image. Compare against the three anchors at
full size before returning. Name any image that is still ambiguous.
````

---

## Reviewing a batch

Do this before starting the next one, because a wrong style gets copied into
every later batch.

| Check | Failing looks like |
|---|---|
| Beside the anchors at full size | Heavier lines, filled clothing, a shaded background |
| At 64 px | The idea needs the detail to survive; if it disappears, redraw the composition, do not thicken the outline |
| Tone | Even hatching spread across a garment, a wall or a floor. At tile size it collapses into a solid block and takes the clearest mark with it |
| The face | An open mouth, a wide cartoon eye, a second eye facing the viewer |
| The frame | Nothing bleeding off an edge, or all four margins equal |
| The pair | Any two partners that could be swapped without noticing |

If one image fails and the rest pass, redo that one in the same context and say
what was wrong. If the whole batch fails, the header is not doing its job —
check that all three anchors were attached before blaming the wording.
