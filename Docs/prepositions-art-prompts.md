# Voorzetselpaden — art prompt history

Grok online has no access to this repository or the file system, so every
prompt here is self-contained. Paste the prompt as-is; do not rely on it
reading `game-art.md`, `voorzetselpaden/a0-a2.html` or `prepositions.json`.

> **Historical.** The style blocks below are the prompts that produced batches
> 1–3 and are kept as a record. They are not the current style. The anchors are
> a bold brush-pen sketch; the current locked header and style rules are in
> `game-art.md`. Do not paste these style blocks for new art.

The generator's output is a sketch, not a shippable file. It arrives as cobalt
on white paper. Process it into the alpha mask described in `game-art.md`
under *Delivered raster art* and ship at 512 × 763. The thirty existing scenes
are 2:3 portrait, and all new scenes must match that ratio and camera or the
`aspect-ratio: 512 / 763` rule in `style.css` has to change for every scene.

Batch 1 was written for SVG. The delivered set arrived as raster PNGs with the
white paper baked in, so batch 2 asks for PNGs and a white background on
purpose.

---

## Batch 1 — the first ten (2026-11-08)

Status: delivered. The version sent to Grok removed the "Read first" block
because Grok has no file access. Kept verbatim below as the original draft.

````text
Task: create the first ten SVG illustrations for the Voorzetselpaden
(prepositions) game in the Oefenpad repository.

Read first, if the files are present:
Docs/game-art.md — the canonical image style
Docs/voorzetselpaden/a0-a2.html — the scene briefs
Docs/prepositions.md — how the scenes are used

Only create this folder and its files:
assets/voorzetselpaden/
Do not edit game code, docs, CSS, data files, or any existing assets. Do not
commit anything.

Deliver exactly these ten files:
wachten-op-bus.svg
wachten-voor-deur.svg
denken-aan-persoon.svg
denken-over-keuze.svg
uitkijken-naar-vakantie.svg
uitkijken-voor-auto.svg
praten-met-vriend.svg
praten-over-huis.svg
ophouden-met-roken.svg
eraan-denken-afspraak.svg

STYLE — follow this exactly
Each file is a 512 × 512 SVG with viewBox="0 0 512 512" and a transparent
background. Draw in the hand of the Oefenpad logo: confident brush strokes,
not flat vector icons.

Cobalt only: #2B50C8. No orange, no second blue, no grey, no full colour.
Each stroke must taper: thin at both ends, wider in the middle. Use closed,
filled paths with variable width. Do not use uniform stroke-width lines.
Stroke weights at 512 px: primary contour 10–14 units, secondary 5–7,
detail 3–4. Anything the meaning depends on must survive at 64 px.
Add two or three narrow bristle splits to the widest strokes. Let edges
wobble 1–3 units. Let joins be loose: strokes may overshoot by 2–4 units
or stop 1–3 units short. Do not close every corner mechanically.
No flat silhouettes with a uniform outline. No double contours. No hatching,
shading, gradients, shadows, blur, grain overlays or photographic detail.
No text, letters, numbers, logos, readable signs or emoji. Blank signs only.
No frame, border, background shape, white plate or decorative scenery.
One idea per image. People are simple masses, not stick figures: at most one
dot for an eye and one line for a mouth. Posture carries the meaning.
48-unit safe area on every side. Subject about 70–80% of the canvas.
The image must read as a silhouette at 64 × 64.

Use this shell for every file:
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"
     width="512" height="512" color="#2B50C8" role="img">
  <g fill="currentColor">
    <!-- tapered brush paths only -->
  </g>
</svg>

Do not add <title>, <desc>, <text>, <rect> backgrounds, CSS, JavaScript,
external references, embedded fonts, or data-verf. The game data supplies
the alt text. Each file must open standalone in a browser and render cobalt.

THE TEN SCENES

wachten-op-bus.svg
   Scene: one person at a simple bus stop, body angled toward the road,
   looking at a watch or phone. A pole with a blank sign; maybe a bench.
   Must read: waiting for a bus.
   Avoid: a bus arriving or boarding, a queue, a person entering a vehicle.

wachten-voor-deur.svg
   Scene: one person standing outside a closed door, waiting, arms crossed
   or leaning against the wall. A plain door with a handle and a blank
   nameplate; maybe a doormat. The person is outside.
   Must read: waiting in front of a door.
   Avoid: a bus stop, a person walking through the door, a key in hand,
   a queue.

denken-aan-persoon.svg
   Scene: one person sitting or standing still, gazing into space, with a
   thought bubble containing a simple face — a friend or partner.
   Must read: thinking of a person.
   Avoid: a speech bubble, two options, a question mark, a calendar reminder.

denken-over-keuze.svg
   Scene: one person at a table with two simple options side by side — two
   house shapes, two paths, or two holiday photos. Hand on chin, comparing.
   The options are objects, not people.
   Must read: considering a choice.
   Avoid: a thought bubble containing a person, a question mark alone,
   a speech bubble.

uitkijken-naar-vakantie.svg
   Scene: one person with a suitcase, smiling, looking at a wall calendar
   with one day marked and a sun or plane icon. Use a blank grid; no numbers
   or letters.
   Must read: looking forward to a future holiday.
   Avoid: a bus or plane actually leaving, a warning gesture, a sad face.

uitkijken-voor-auto.svg
   Scene: a child at the edge of a road, a car approaching, and an adult
   hand pulling the child back or making a warning gesture. A simple
   warning triangle without text may appear, but must not become the main
   idea.
   Must read: danger; watch out.
   Avoid: a happy person looking at a car, a bus stop, a traffic light
   with readable marks.

praten-met-vriend.svg
   Scene: two people facing each other, both with speech bubbles that meet
   or overlap, relaxed posture. A table is allowed, but no object is the
   topic of the conversation.
   Must read: a conversation with someone.
   Avoid: one person alone, a phone, a house or object between them.

praten-over-huis.svg
   Scene: two people at a table with a house, a photo of a house, or a
   simple blueprint between them. Speech bubbles point at the house; one
   person gestures toward it.
   Must read: talking about a topic or object.
   Avoid: two people just facing each other with no topic, one person
   alone, a phone.

ophouden-met-roken.svg
   Scene: one person stubbing out a cigarette in an ashtray, or holding up
   a hand to refuse a cigarette. Calm and determined. A packet may be put
   away, with no branding or text. A crossed-out cigarette is allowed if
   it stays completely wordless.
   Must read: stopping smoking.
   Avoid: a person smoking happily, a "no smoking" sign with letters,
   a doctor or a lecture.

eraan-denken-afspraak.svg
   Scene: one person with a hand to the forehead or a raised finger —
   sudden recall. A phone or calendar with a bell or reminder icon nearby;
   maybe a clock. No text or numbers.
   Must read: remembering an appointment, "oh, I must remember".
   Avoid: a thought bubble containing a person, two options, a question
   mark, a speech bubble.

CONTRAST PAIRS
Design these together, in the same sitting, with the same camera, scale and
composition. Change only the meaningful element:
1 and 2
3 and 4
5 and 6
7 and 8
At 64 × 64, the two images must be clearly different, and neither may
suggest the other sentence.

VALIDATION
For every file:
Render or downscale to 64 × 64 and check that the idea is still nameable.
Confirm 512 × 512, transparent, and no background rectangle.
Confirm cobalt only: no orange, no second blue, no grey.
Confirm no <text>, <title>, <desc>, letters, numbers or readable signs.
Confirm all strokes are tapered filled paths, not uniform outlines.
Confirm the file opens standalone in a browser and renders cobalt.
Confirm the exact filenames and the exact folder path.
When finished, report the ten file paths and name any image whose 64 px
silhouette is still ambiguous. Do not add or modify anything outside
assets/voorzetselpaden/.
````

---

## Batch 2 — the next ten (2026-11-08)

Status: delivered 2026-11-08. The ten files are in `assets/verbs/`, processed
into the 512 × 763 alpha masks in `assets/voorzetselpaden/`, and wired into
`server/Oefenpad.Resources/Games/Data/prepositions.json`. This is the ten new scenes. The two redraws
(`denken-aan-persoon`, `eraan-denken-afspraak`) are a separate job, per
`Docs/voorzetselpaden/a0-a2.html`.

Changes from batch 1: PNG instead of SVG; 2:3 portrait instead of square; pure
white paper instead of transparent, because the mask pipeline expects dark ink
on light paper; no "read these files" block.

````text
You have no file access. Do not ask to read any repository, document, image or
attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called
Voorzetselpaden, and nothing else. Each image is a wordless clue for one
Dutch verb + preposition chunk. The learner sees the image, recognises the
everyday situation, and connects it to the chunk. A Dutch speaker must be
able to name the situation from the drawing alone, without a caption. The
Dutch and English below are context for you only. None of those words may
appear in the image.

STYLE — FOLLOW EXACTLY
- Hand-painted brush-line illustration in the hand of the Oefenpad logo:
  confident, thick, tapered brush strokes. Not a flat vector icon, not a
  cartoon, not a stock illustration, not photorealistic, not a 3D render, not
  a digital painting with soft shading.
- One ink only: cobalt blue #2B50C8. No orange, no red, no green, no second
  blue, no grey, no skin colour, no full colour.
- No gradients, shading, hatching, cross-hatching, stippling, drop shadows,
  glow, blur, grain, paper texture or vignette.
- Plain pure white background (#FFFFFF). No off-white, cream, beige or grey
  background. The white paper is intentional; it becomes transparency later.
  No border, frame, card, rounded rectangle, white plate or shadow behind the
  scene.
- Mostly empty paper. One idea per image. The subject occupies about 70–80%
  of the canvas, with a clear margin on every side.
- Strokes taper: thin at both ends, wider in the middle. Use closed, filled
  shapes with variable width. Do not use uniform stroke-width lines,
  round-capped lines or a mechanical outline.
- The primary contour must survive at 64 × 64 px. Add two or three narrow
  bristle splits to the widest strokes. Let edges wobble slightly. Let joins
  be loose: strokes may overshoot a little or stop short. Do not close every
  corner mechanically.
- At most one small solid brush mass per image, for example a head, a cup or
  a bag. Everything else is line. Do not build the scene from filled
  silhouettes.
- People are simple masses, not stick figures and not caricatures. At most one
  dot for an eye and one line for a mouth. No hair detail, clothing patterns
  or fingers; a mitten shape is enough for a hand. No skin colour.
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
- Ten separate images, one per subject.
- 2:3 portrait, for example 1024 × 1536 px. All ten use the same camera, the
  same scale and the same line weight, because they sit side by side in one
  game.
- Raster PNG. Do not produce SVG code.
- No contact sheet, grid, collage or extra images. If you must return them one
  at a time, return them in the numbered order.
- Do not put the filename, a number or any label inside the image. Put the
  exact filename in the chat text above or below each image.

THE TEN SUBJECTS, IN ORDER

1. werken-bij-bedrijf — Dutch chunk: werken bij (to work at a company).
   Scene: one person at a desk or counter in front of a plain company
   building facade with a door and two windows; a plain lanyard or badge with
   no text; at most one colleague in the background. The cue is the building
   and the company, not the task.
   Must read at 64 px: someone is employed at a company.
   Avoid: a blueprint or tools as the main object (that is #2); a customer
   queue; a shop with readable signs; a person working from home.

2. werken-aan-project — Dutch chunk: werken aan (to work on).
   Scene: one person leaning over a table with a large drawing, blueprint,
   model or tools; focused, sleeves rolled up; the object of work is the main
   mass.
   Must read: working on a project.
   Avoid: a company building or lanyard (that is #1); a finished building; a
   person just sitting at a laptop with nothing else (too generic).

3. klaar-met-werk — Dutch chunk: klaar met (done with).
   Scene: one person pushing back from a desk, laptop closed, hands behind the
   head or stretching, relaxed; the desk is tidy and the work is finished.
   Must read: finished with work.
   Avoid: a person still typing; a person asleep; a party or celebration
   (that is #4).

4. klaar-voor-feest — Dutch chunk: klaar voor (ready for).
   Scene: one person at a front door, coat on, holding a gift or flowers,
   ready to leave; smiling.
   Must read: ready to go to a party.
   Avoid: a person still working; a person wrapping a gift; a person already
   at the party.

5. vragen-aan-persoon — Dutch chunk: vragen aan (to ask a person).
   Scene: one person leaning toward another, one hand raised, mouth open; the
   other person listening or answering; one blank speech bubble from the
   asker pointing toward the other person.
   Must read: asking a person.
   Avoid: two equal speech bubbles (that is a conversation); a question mark;
   a form or counter; an object being handed over (that is #6).

6. vragen-om-hulp — Dutch chunk: vragen om (to ask for).
   Scene: one person with an open hand, the other person handing over a box,
   tool or bag; the object is the main mass; the asker's posture is
   requesting.
   Must read: asking for a thing or help.
   Avoid: two people just talking (that is #5); money (it can read as
   begging); a shop counter with readable signs.

7. zorgen-voor-kind — Dutch chunk: zorgen voor (to care for).
   Scene: one adult helping a child into a coat, or tying a scarf, with a
   school bag in hand; the adult leans down, the child holds out an arm.
   Must read: caring for a child.
   Avoid: a doctor or nurse; a hospital; a person hugging a pet (that is
   love, not care); a parent scolding.

8. meedoen-met-team — Dutch chunk: meedoen met (to join in).
   Scene: one person pulling a chair up to a group of two or three around a
   table or board game; the newcomer is mid-motion, the group makes space.
   Must read: joining a group activity.
   Avoid: a spectator watching from a distance; a person alone; a classroom
   with a teacher at the front; a queue.

9. zoeken-naar-sleutels — Dutch chunk: zoeken naar (to search for).
   Scene: one person kneeling or crouching, looking under a sofa or table; a
   set of keys visible on the floor just out of reach; one hand reaching.
   Must read: searching for lost keys.
   Avoid: a person holding keys (already found); a lost-and-found counter with
   text; a magnifying glass (too detective).

10. last-hebben-van-lawaai — Dutch chunk: last hebben van (to be bothered
    by).
    Scene: one person covering their ears and frowning near a simple wall; on
    the other side of the wall, a hand-held drill or a loud speaker; the wall
    divides the image. Do not draw a construction worker; the drill is the
    only thing on the far side.
    Must read: bothered by noise from next door.
    Avoid: a person with a headache and no source (too vague); a construction
    worker (that is work); a music party (that reads as fun); readable signs.

CONTRAST PAIRS — DESIGN THESE TOGETHER
1 and 2, 3 and 4, 5 and 6 are pairs. Draw each pair in the same sitting, with
the same camera, scale and composition. Change only the meaningful element.
At 64 × 64 px, the two images must be clearly different, and neither may
suggest the other's situation.

VALIDATION BEFORE YOU FINISH
For every image:
- Downscale mentally or actually to 64 × 64: is the idea still nameable?
- Is it cobalt only, with no orange, no grey and no second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or
  readable sign? Remove it.
- Are the strokes tapered filled shapes, not uniform outlines?
- Is the background plain white, with no border, card, shadow or scenery?
- Is the subject clear of the edges and surrounded by breathing room?
Then check the pairs side by side. If either image in a pair suggests the
other's chunk, redraw it before delivering.

When finished, list the ten filenames and name any image whose 64 px
silhouette is still ambiguous. Do not add any image that is not on this list.
````

---

## Batch 3 — images 21–30 (2026-11-08)

Status: delivered 2026-11-08. The ten files are in `assets/verbs/`, processed
into the 512 × 763 alpha masks in `assets/voorzetselpaden/`, and wired into
`server/Oefenpad.Resources/Games/Data/prepositions.json`. Three pairs plus four high-frequency singles; `vragen naar`
completes the `vragen` level from batch 2 and makes it a set of three. Same
format as batch 2: PNG, 2:3 portrait, cobalt on pure white.

````text
You have no file access. Do not ask to read any repository, document, image or
attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called
Voorzetselpaden, and nothing else. Each image is a wordless clue for one
Dutch verb or adjective plus a fixed preposition. The learner sees the image,
recognises the everyday situation, and connects it to the chunk. A Dutch
speaker must be able to name the situation from the drawing alone, without a
caption. The Dutch and English below are context for you only. None of those
words may appear in the image.

STYLE — FOLLOW EXACTLY
- Hand-painted brush-line illustration in the hand of the Oefenpad logo:
  confident, thick, tapered brush strokes. Not a flat vector icon, not a
  cartoon, not a stock illustration, not photorealistic, not a 3D render, not
  a digital painting with soft shading.
- One ink only: cobalt blue #2B50C8. No orange, no red, no green, no second
  blue, no grey, no skin colour, no full colour.
- No gradients, shading, hatching, cross-hatching, stippling, drop shadows,
  glow, blur, grain, paper texture or vignette.
- Plain pure white background (#FFFFFF). No off-white, cream, beige or grey
  background. The white paper is intentional; it becomes transparency later.
  No border, frame, card, rounded rectangle, white plate or shadow behind the
  scene.
- Mostly empty paper. One idea per image. The subject occupies about 70–80%
  of the canvas, with a clear margin on every side.
- Strokes taper: thin at both ends, wider in the middle. Use closed, filled
  shapes with variable width. Do not use uniform stroke-width lines,
  round-capped lines or a mechanical outline.
- The primary contour must survive at 64 × 64 px. Add two or three narrow
  bristle splits to the widest strokes. Let edges wobble slightly. Let joins
  be loose: strokes may overshoot a little or stop short. Do not close every
  corner mechanically.
- Use solid mass sparingly: at most one small mass per figure, for example a
  head, a cup or a bag. Never build the scene from filled silhouettes.
- People are simple masses, not stick figures and not caricatures. At most one
  dot for an eye and one line for a mouth. No hair detail, clothing patterns
  or fingers; a mitten shape is enough for a hand. No skin colour.
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
- Ten separate images, one per subject.
- 2:3 portrait, for example 1024 × 1536 px. All ten use the same camera, the
  same scale and the same line weight, because they sit side by side in one
  game.
- Raster PNG. Do not produce SVG code.
- No contact sheet, grid, collage or extra images. If you must return them one
  at a time, return them in the numbered order.
- Do not put the filename, a number or any label inside the image. Put the
  exact filename in the chat text above or below each image.

THE TEN SUBJECTS, IN ORDER

1. blij-met-cadeau — Dutch chunk: blij met (happy with).
   Scene: one person holding or opening a simple gift box with a ribbon,
   delighted; the gift is the main mass; no text on the box or ribbon.
   Must read: happy with a thing.
   Avoid: a second person (that is #2); a party scene; a price tag or readable
   label.

2. blij-voor-vriend — Dutch chunk: blij voor (happy for).
   Scene: one person smiling warmly at a friend who holds a diploma, medal or
   small trophy with no text; the happy person's hands are clasped or raised;
   the friend is the main mass.
   Must read: happy for another person.
   Avoid: the happy person holding the object (that is #1); a graduation cap
   with a readable motto; a crowd.

3. boos-op-collega — Dutch chunk: boos op (angry at).
   Scene: one person scowling and pointing at another person; the other person
   leans back defensively; the two face each other.
   Must read: angry at a person.
   Avoid: an object as the target (that is #4); a fist fight; a boss behind a
   desk with readable signs.

4. boos-over-rommel — Dutch chunk: boos over (angry about).
   Scene: one person scowling at a mess or broken object — a fallen plant,
   scattered papers or a cracked cup — with no other person; the mess is the
   main mass.
   Must read: angry about a thing or situation.
   Avoid: a second person (that is #3); a person cleaning happily; readable
   labels.

5. klagen-over-apparaat — Dutch chunk: klagen over (complain about).
   Scene: one person at home, arms crossed or finger raised, complaining at a
   broken washing machine or appliance; the appliance is the main mass; no
   phone.
   Must read: complaining about a thing.
   Avoid: a phone (that reads as calling); a service desk (that is #6); a
   person repairing it happily.

6. klagen-bij-balie — Dutch chunk: klagen bij (complain to).
   Scene: one person leaning toward a clerk at a plain service desk, finger
   raised, dissatisfied; the clerk listens; a blank badge or counter sign, no
   text.
   Must read: complaining to a person or company.
   Avoid: a broken appliance as the main mass (that is #5); a queue; readable
   signs.

7. houden-van-hond — Dutch chunk: houden van (to love).
   Scene: one person hugging a calm dog; both relaxed; the hug is the main
   idea.
   Must read: loving an animal or person.
   Avoid: a barking or aggressive dog (that is #9); a vet; a dog collar tag
   with text.

8. zin-in-koffie — Dutch chunk: zin in (to feel like).
   Scene: one person looking happily at a cup of coffee and a slice of cake,
   hands together or reaching toward them; the cup and cake are the main mass.
   Must read: craving or feeling like something nice.
   Avoid: a full meal; a restaurant with readable menus; a person already
   drinking with a neutral face.

9. bang-voor-hond — Dutch chunk: bang voor (afraid of).
   Scene: one person leaning away from a barking dog, hands raised, eyes wide;
   the dog is larger and more animated than in #7; no owner.
   Must read: afraid of a dog.
   Avoid: a calm dog being hugged (that is #7); a vet; a muzzle; readable
   signs.

10. vragen-naar-informatie — Dutch chunk: vragen naar (to ask about, to ask
    for information).
    Scene: one person at a plain counter pointing at a blank map or brochure on
    the counter; a clerk behind the counter listens; a simple route line on
    the map is allowed, but no letters, numbers or pin labels.
    Must read: asking for information about something.
    Avoid: a question mark; a person asking another person directly with no
    object (that is vragen aan); an object being handed over (that is vragen
    om); readable signs.

CONTRAST PAIRS — DESIGN THESE TOGETHER
1 and 2, 3 and 4, 5 and 6 are pairs. Draw each pair in the same sitting, with
the same camera, scale and composition. Change only the meaningful element.
At 64 × 64 px, the two images must be clearly different, and neither may
suggest the other's situation.
7–10 are singles: draw each one standalone. #10 is the third scene in a
`vragen` set; it must not repeat the situations of asking a person directly
or asking for an object.

VALIDATION BEFORE YOU FINISH
For every image:
- Downscale mentally or actually to 64 × 64: is the idea still nameable?
- Is it cobalt only, with no orange, no grey and no second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or
  readable sign? Remove it.
- Are the strokes tapered filled shapes, not uniform outlines?
- Is the background plain white, with no border, card, shadow or scenery?
- Is the subject clear of the edges and surrounded by breathing room?
Then check the pairs side by side. If either image in a pair suggests the
other's chunk, redraw it before delivering.

When finished, list the ten filenames and name any image whose 64 px
silhouette is still ambiguous. Do not add any image that is not on this list.
````

---

## Notes for batch 4

Batch 4 is planned in `Docs/voorzetselpaden/a0-a2.html`: twenty A0–A2 frames around
`tegen`, `door`, `uit` and `tot`, with supporting `aan`, `met`, `op` and `in`
frames, in two copy-paste Grok prompts. `zonder` is left out because
`zonder + noun` is free prepositional use, not a chunk. The later bands follow
in `Docs/voorzetselpaden/a2-plus.html`, `b1.html`,
`b1-plus.html` and `b2.html`. The items below
still apply.

- `denken-aan-persoon` and `eraan-denken-afspraak` still need redraws; see
  `Docs/voorzetselpaden/a0-a2.html`. Batch 3 did not touch them.
- Deferred candidates: `afhangen van` (hard to draw unambiguously at 64 px),
  `werken voor` (too close to `werken bij`), `zoeken op` (separable
  `opzoeken`, a word-order item, not a frame).
- Batch 3 delivered `blij met/voor`, `boos op/over`, `klagen over/bij`,
  `houden van`, `zin in`, `bang voor` and `vragen naar`.
- `beginnen met/aan`, `rekenen op/met` and `twijfelen aan/over` are deferred:
  the first pair is aspectually subtle, `rekenen met` usually appears as
  `rekening houden met`, and `twijfelen over` overlaps the existing
  `denken over de keuze` scene.
- The singles in batch 3 have their second `bouw` sentence in
  `prepositions.json`, as `ophouden met` and the batch-2 singles have, so each
  level is 3 scored answers, not 2. Keep doing this for any new single.
