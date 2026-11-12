# Voorzetselpaden — image plan, B1

Status: planning document, 10 November 2026. This is the **B1** band: the
high-frequency verb + preposition frames. It covers roadmap batches 9–13 of
`prepositions-roadmap.md`.

The plan was split on 10 November 2026. What used to be one 200-frame B1 file is
now two — **A2+** (`prepositions-art-a2-plus.md`, 80 frames, batches 5–8) and
**B1** (this file, 120 frames, batches 9–13). Nothing was added or cut in the
split.

Scope: **120 new frames**, planned as **12 self-contained Grok batches of ten**,
numbered B1-01 to B1-12. The artwork comes back as 120 separate 2:3 PNGs, one
worldless clue per frame, in the house style of `game-art.md`.

What is excluded, and must not be redrawn or duplicated:

- The **30 pilot scenes** already in `assets/voorzetselpaden/` and described in
  `prepositions-art.md`: `wachten`, `denken`, `praten`, `ophouden`, `uitkijken`,
  `werken`, `klaar`, `vragen`, `zorgen`, `meedoen`, `zoeken`, `last hebben`,
  `blij`, `boos`, `klagen`, `houden van`, `zin in`, `bang voor`, `eraan denken`.
- The **20 A0–A2 frames** planned in `prepositions-art-a0-a2.md` (batch 4):
  `zeggen tegen`, `vertellen aan`, `praten tegen`, `beschermen tegen`,
  `komen door`, `komen uit`, `kijken door`, `kijken uit`, `doorgeven aan`,
  `doorbrengen met`, `stappen uit`, `drinken uit`, `vallen uit`,
  `letten op`, `bezig zijn met`, `geïnteresseerd zijn in`, `tevreden zijn met`,
  `bedanken voor`, `feliciteren met`, `uitnodigen voor`.
- The **17 batch-4b frames** in `prepositions-art-a2-pairs.md`.
- The **80 A2+ frames** in `prepositions-art-a2-plus.md` — the spatial set, the
  adjective and noun chunks and the pronominal adverbs.
- Free spatial and temporal use (`op tafel`, `in de kast`, `na de les`). That is
  grammar, not a chunk — see `prepositions-roadmap.md` §11.

No frame in this file repeats a pilot frame, an A0–A2 frame, a batch-4b frame,
an A2+ frame or another frame in this file. Where a chunk that already has a
pilot image comes back, it does so in a visibly different situation and the
tracker says which; the chunk list deliberately stays broader than the pilot's
twenty.

## How to use this file

Each batch section is a single fenced text block. Paste **one block at a time**
into Grok. Grok has no file access, so every block repeats the task, the style,
the format and its ten subjects; nothing outside the block is assumed and no
block depends on another having been sent first. Ask for the ten images, then
process the result as described in `game-art.md` under *Delivered raster art*
and ship at 512 × 763.

Two rules make the set teach rather than decorate:

- **Contrast before single.** Where two frames share a verb and differ only in
  the preposition, they are a pair and are drawn in the same sitting: same
  camera, same scale, one meaningful difference. The pair is the thing that
  teaches, so a pair is kept inside one batch wherever the ten-frame rhythm
  allows it. Where a pair spans two batches the blocks say so, and the second
  half names its partner file.
- **Concrete over abstract.** A chunk with no honest silhouette gets a concrete
  everyday situation, and the gloss carries the abstraction. The tracker column
  marks them `gloss-picture`. `prepositions-roadmap.md` §9 predicts this; this
  file is the honest version of it at B1.

The house style is the bold brush-pen sketch defined in `game-art.md`: cobalt
`#2B50C8` only, wide-nib contour with directional hatching, 2:3 portrait, one
idea per image, no text. The prompts repeat those rules because the generator
cannot read `game-art.md`.

## What B1 adds

One hundred and twenty verb chunks in a single theme, ordered roughly from
everyday concrete situations towards more abstract ones. The order is
speculative in the sense that the repo has no frequency list; re-cut any batch
around one when it arrives, per `prepositions-roadmap.md` §12.1. The art plan
survives a re-cut because each frame stands alone.

| Image batch | Theme | Frames | Roadmap batch |
|---|---|---|---|
| B1-01 – B1-12 | High-frequency verb + preposition | 120 | 9–13 |
| **Total** | | **120** | |

Sections:

- B1-01 – B1-12: verb chunks, 120 frames in 72 paired frames and 48 singles.
  Pairs sit next to each other inside a batch wherever the batch allows;
  singles share a batch with a related situation, because a verb chunk is
  usually learned with its preposition and not against a neighbour.

No new governed preposition is introduced in this band. The verb chunks reuse
what the earlier bands established, with `naar`, `met`, `op`, `voor`, `van`,
`aan` and `over` doing most of the work.

Status values in the tracker: `needed` (not drawn), `drawn` (delivered and
processed), `gloss-picture` in the note column (see above).

## Tracker

All 120 frames, in batch order. The file column is the Grok filename and the
shipped scene id. "Pair/note" names the partner file for a pair, or `single`.

| # | File | Dutch frame | English | Scene | Pair/note | Status |
|---|---|---|---|---|---|---|
| 1 | `beginnen-met-de-les.png` | beginnen met | to begin with | one person stands at the front of a simple room, one hand on an open book and the other raised for attention; three seated heads face them, all upright and ready. The first moment of a session | Pair with `beginnen-aan-een-nieuw-huis` | needed |
| 2 | `beginnen-aan-een-nieuw-huis.png` | beginnen aan | to start on | one person stands in front of a half-built wall of bricks, one hand holding a trowel, the other resting on the wall; the wall ends mid-course and continues as empty space | Pair with `beginnen-met-de-les` | needed |
| 3 | `helpen-met-de-afwas.png` | helpen met | to help with | two people stand side by side at a sink; one washes a plate and hands it sideways, the other takes it and stacks it. Their arms form a simple relay | Pair with `helpen-aan-de-balie` | needed |
| 4 | `helpen-aan-de-balie.png` | helpen aan | to help, at a counter | a clerk stands behind a plain desk, leaning forward and pointing at a small form on the desk; a customer sits in front, pen raised. Both look at the form | Pair with `helpen-met-de-afwas` | needed |
| 5 | `zoeken-onder-de-bank.png` | zoeken onder | to search under | one person crouches with one cheek near the floor, peering under a bench; one hand reaches into the gap, a bag lies on its side beside them. The bench and the gap are the main mass | Pair with `zoeken-in-de-tas` | needed |
| 6 | `zoeken-in-de-tas.png` | zoeken in | to search in | one person holds a large open bag at chest height and looks down into it, the other hand buried inside; a single loose stroke shows one item pushed up. The bag is the main mass | Pair with `zoeken-onder-de-bank` | needed |
| 7 | `zorgen-voor-het-huisdier.png` | zorgen voor | to look after | one person crouches to fill a bowl on the floor while a cat waits with its tail up, one hand steadying the bowl. The cat and bowl are the main mass | Single; same chunk as shipped, an animal | needed |
| 8 | `denken-aan-de-toekomst.png` | denken aan | to think about | one person sits by a plain window at dusk, chin on the hand, looking out; a small blank thought bubble floats beside them and contains only an open road shape. No second figure | Part of the `denken aan` group, 7–10 | needed |
| 9 | `praten-over-het-weer.png` | praten over | to talk about | two people stand under a shop awning, both looking up and outward at a rain cloud; one points at the cloud, both speech bubbles are blank. The cloud is the topic | Single; contrasts with shipped `praten over het huis` by scene only | needed |
| 10 | `praten-tegen-zichzelf.png` | praten tegen jezelf | to talk to yourself | one person walks alone along a path, one hand gesturing in the air in front of them, mouth a short line; a single small blank speech bubble near the head, and nobody else in the frame | Single; `praten tegen`, no listener | needed |
| 11 | `wachten-op-antwoord.png` | wachten op | to wait for | one person sits at a table with a phone flat in front of them, both hands clasped, eyes on the phone; the posture is patient and tense. Only one figure | Single; contrasts with shipped `wachten op de bus` | needed |
| 12 | `rekenen-op-hulp.png` | rekenen op | to count on | one person stands with one arm raised towards a second person who is offering a steadying hand from a ladder; the first person leans their weight on that hand. The hand is the main mass | Pair with `geloven-in-jezelf` | needed |
| 13 | `denken-aan-een-oplossing.png` | denken aan | to think of | one person snaps their fingers with an open smile, eyes lifted; one finger of the other hand points up. No bubble, no second person, only the sudden thought | Part of the `denken aan` group, 7–10 | needed |
| 14 | `geloven-in-jezelf.png` | geloven in | to believe in | one person stands in front of a mirror shape drawn as a single tall frame; the reflection is the same figure, chin up, fist lightly closed at the chest. Both figures are calm and strong | Pair with `rekenen-op-hulp` | needed |
| 15 | `zorgen-voor-elkaar.png` | zorgen voor | to care for | one person covers another's shoulders with a blanket while the other sits on a sofa with a cup; both are relaxed and close. The blanket is the main mass | Single; same chunk as shipped, reciprocal | needed |
| 16 | `denken-over-een-beslissing.png` | denken over | to think about | one person stands at a doorway between two rooms, one hand on each side of the frame, head turned to look first one way then the other. The two rooms are drawn identically | Single; contrasts with shipped `denken over de keuze` by scene only | needed |
| 17 | `klagen-over-het-weer.png` | klagen over | to complain about | one person wraps both arms around themselves, shoulders hunched, mouth a downward line, looking up at slanting rain; one hand is held out, palm up, at the rain. No second figure | Single; contrasts with shipped `klagen over` by scene only | needed |
| 18 | `zoeken-naar-een-baan.png` | zoeken naar | to search for | one person sits at a laptop, one hand at the chin and the other on a heap of blank papers; a small blank noticeboard with one sheet pinned on the wall behind. Focused, not reading comfortably | Single; contrasts with shipped `zoeken naar` by scene only | needed |
| 19 | `kijken-naar-een-vogel.png` | kijken naar | to look at | one person stands at a plain window, both hands on the sill, leaning forward with their nose near the glass; outside the glass one small bird sits on a bare branch, wings folded. Steady attention, not surprise | Single; same chunk as 9 in B1-02, new scene | needed |
| 20 | `praten-met-de-dokter.png` | praten met | to talk with | one person sits on the edge of a plain bed and speaks with raised hand to a second person in a plain coat, who listens and points at a clipboard; the clipboard is blank. No readable charts | Single; contrasts with shipped `praten met` by scene only | needed |
| 21 | `zich-verheugen-op-de-vakantie.png` | zich verheugen op | to look forward to | one person sits with knees drawn up, arms wrapped around them, smiling and looking at a plain suitcase standing by the door; the suitcase has no stickers or labels. Content, not busy | Pair with `genieten-van-de-zon` | needed |
| 22 | `genieten-van-de-zon.png` | genieten van | to enjoy | one person lies back on a striped deckchair, eyes closed, hands behind the head, a single sun shape drawn as an open ring of short strokes in the top corner. Relaxed mouth | Pair with `zich-verheugen-op-de-vakantie` | needed |
| 23 | `rekening-houden-met-de-buren.png` | rekening houden met | to take into account | one person carries a loud musical instrument or a drill case towards a shared wall, then stops with one hand raised flat, mouth closed; on the other side of the wall a second person holds a finger to their lips. The wall divides them | Pair with `ruzie-maken-met-collega` | needed |
| 24 | `ruzie-maken-met-collega.png` | ruzie maken met | to argue with | two people face each other with one arm each raised and pointed, both leaning forward, mouths drawn as short open lines; a small gap of white between them. No bubbles | Pair with `rekening-houden-met-de-buren` | needed |
| 25 | `denken-aan-de-kosten.png` | denken aan | to think of | one person sits at a table with a small calculator and a plain long receipt in front of them, chin on hand and brow a single line; the other hand counts on the edge of a coin stack. One figure | Pair with `akkoord-gaan-met-het-voorstel` | needed |
| 26 | `wijzen-op-een-fout.png` | wijzen op | to point out | a row of five identical plain framed pictures hangs on a wall; four are level and one hangs tilted. One person stands at the side, arm stretched, one finger pointing at the tilted frame, head turned towards the viewer | Single. A flaw among equals; the wall and flat object are reused | needed |
| 27 | `passen-op-de-buurkinderen.png` | passen op | to look after | one adult sits upright on the edge of a sofa, hands on the knees and one hand half raised, eyes following two small children at the far side of the room, one of whom has climbed onto a low stool. The adult is alert, not joining in | Single. Minding someone else's children | needed |
| 28 | `akkoord-gaan-met-het-voorstel.png` | akkoord gaan met | to agree to | one person sits at the same desk and chair, a single sheet in front and a pen touching one short line on it, nodding with an easy mouth line. The desk is otherwise bare | Pair with `denken-aan-de-kosten`; same desk and camera, nod instead of frown | needed |
| 29 | `kennismaken-met-de-nieuwe-buur.png` | kennismaken met | to get acquainted with | two people on either side of a low fence shake hands across it, both smiling; a small potted shape or a bunch of keys in one free hand. The handshake crosses the fence | Pair with `kennismaken-met-nieuwe-mensen` | needed |
| 30 | `kloppen-op-de-deur.png` | kloppen op | to knock on | one person stands in profile at a closed plain door with a round knob and no window, one fist raised and touching it; three short strokes of sound sit at the fist. The other arm hangs loose | Single. Knuckles on the door | needed |
| 31 | `afspreken-met-een-vriend.png` | afspreken met | to arrange to meet | two people stand facing each other with a small blank calendar page held between them; both point at the same spot on the page, smiling. The page floats mid-air, plain, with one thick dot | Pair with `afspreken-op-een-tijd` | needed |
| 32 | `afspreken-op-een-tijd.png` | afspreken op | to agree on a time | one person holds up a wristwatch and points at its face while looking at a second person beside them, who nods; the watch is plain with hands and no numbers | Pair with `afspreken-met-een-vriend` | needed |
| 33 | `hulp-vragen-aan-de-buurman.png` | hulp vragen aan | to ask help from | two people stand a few steps apart, side-on, with a gap of white between them; the first holds a closed jar out in both hands with head tilted and brow raised, and the neighbour steps forward with both hands open to take it. No ladder | Single. Two figures side-on with a gap of white; not the box of #5 | needed |
| 34 | `schrijven-aan-de-gemeente.png` | schrijven aan | to write to | one person sits at a desk writing a letter with a pen on a single page of long lines; beside it lies a large plain envelope with a small pillared public-building shape drawn on its front. The page has no marks that read as words | Pair with `oefenen-voor-het-examen`; same desk height, pen and page | needed |
| 35 | `helpen-bij-de-verhuizing.png` | helpen bij | to help with | two people carry one open box together, each holding one side, moving towards the viewer; a third box sits on the ground behind them. Bodies lean into the weight | Single; `helpen bij` a shared job | needed |
| 36 | `blijven-bij-een-vriend.png` | blijven bij | to stay with | one person sits down on a simple sofa beside another who is wrapped in a blanket with a cup; the arriving person's hand rests on the other's shoulder. The seated pair, close together | Single; `blijven bij` a person | needed |
| 37 | `kennismaken-met-nieuwe-mensen.png` | kennismaken met | to meet | three people stand in a loose circle, the nearest one reaching a hand towards the middle; a fourth approaches from the side with a raised hand and a smile. Simple figures, no name tags | Pair with `kennismaken-met-de-nieuwe-buur` | needed |
| 38 | `passen-bij-elkaar.png` | passen bij | to go with, to match | two cloths hang side by side on a clothes line, the same size and the same squared-off shape, their lower corners level; a third, visibly narrower cloth hangs apart at the far end with a gap of white. A small figure at the left steps back, one hand on the chin, nodding | Single. The line and cloths are reused; no pegging hand | needed |
| 39 | `oefenen-voor-het-examen.png` | oefenen voor | to practise for | one person sits at a table with a blank test paper and a pen, writing, a stack of books beside them; on the wall behind, a large plain clock with hands but no numbers. Focused | Pair with `schrijven-aan-de-gemeente` | needed |
| 40 | `denken-aan-het-verleden.png` | denken aan | to think back to | one person sits by a window with an old photo in one hand and the other hand on the heart; the photo is a plain rectangle showing a small simple couple shape. The posture is wistful, not sad | Single; gloss-picture, part of the `denken aan` group | needed |
| 41 | `raken-aan-de-schouder.png` | raken aan | to touch | one person taps a seated colleague on the shoulder with the flat of a hand; the seated person turns their head. Only the hand rests on the shoulder | Pair with `raken-aan-het-plafond` | needed |
| 42 | `raken-aan-het-plafond.png` | raken aan | to reach, to touch | one person stands on tiptoe with one hand stretched up, fingertips nearly on a plain ceiling line above; the other arm balances out sideways | Pair with `raken-aan-de-schouder` | needed |
| 43 | `leren-van-je-fouten.png` | leren van | to learn from | one person sits at a desk with a blank sheet of paper and a pen, looking at a small plain cross drawn on it, then drawing a clean circle beside it; one figure, focused | Pair with `leren-nederlands-met-zinnen` | needed |
| 44 | `leren-nederlands-met-zinnen.png` | leren met | to learn with | one person sits at a table with a notebook open and a pen raised, mouth set in concentration; a plain card lies beside the book with a single simple stroke on it. One figure | Pair with `leren-van-je-fouten` | needed |
| 45 | `denken-aan-kerstmis.png` | denken aan | to think of | one person sits on a simple chair with a blank folded card in their hands, a small plain fir-tree shape drawn beside them, eyes soft and lifted. One figure | Part of the `denken aan` group, 5–7 | needed |
| 46 | `denken-aan-vroeger.png` | denken aan | to think back to | one person sits by a window with an old photo in one hand and the other hand on the heart; the photo is a plain rectangle showing a small simple couple shape. Wistful, not sad | Part of the `denken aan` group, 5–7 | needed |
| 47 | `denken-aan-een-cadeau.png` | denken aan | to think of | one person stands in a shop aisle, one finger on the chin, looking at a plain box on a shelf; the other hand holds a blank card. Only one figure | Part of the `denken aan` group, 5–7 | needed |
| 48 | `trouwen-met-de-liefde.png` | trouwen met | to marry | two people stand face to face holding hands, both smiling; a simple ring shape is drawn on a small cushion between them. Plain figures, no dress detail | Single; `met` with a person | needed |
| 49 | `verliezen-van-het-team.png` | verliezen van | to lose against | two teams are drawn as a row of three figures each, facing each other; one side slumps with lowered heads, the other raises both arms. A plain ball lies between them | Single; contrast with `winnen van` | needed |
| 50 | `proosten-op-het-succes.png` | proosten op | to toast to | two people stand facing each other with glasses raised and just touching, both smiling; a plain folded document on the table between them. Glasses are plain | Single; `op` with an event | needed |
| 51 | `horen-bij-de-groep.png` | horen bij | to belong to | four people stand shoulder to shoulder facing the viewer, arms across one another's backs; the fourth has just stepped in, one arm still settling onto the neighbour's shoulder as a gap closes. No bubble, no objects | Pair with `reageren-op-de-vraag`; contact is by arms, not words, and no speech bubble | needed |
| 52 | `opkomen-voor-een-vriend.png` | opkomen voor | to stand up for | one person steps in front of a smaller friend, arms spread wide and chest out, facing a larger figure who leans back. The defender is the nearest figure | Pair with `stemmen-op-een-partij` | needed |
| 53 | `klikken-met-de-leraar.png` | klikken met | to click, to get on with | one person sits with a small square device on the table and presses it with one finger; on the plain wall behind, a small square panel lights up as a short burst of strokes. Only one figure | Pair with `zich-concentreren-op-de-opgave` | needed |
| 54 | `reageren-op-de-vraag.png` | reageren op | to respond to | one person leans in with an open hand and one blank speech bubble; the second person turns their head and lifts one hand in answer, mouth moving. One bubble only, from the first | Pair with `horen-bij-de-groep` | needed |
| 55 | `stemmen-op-een-partij.png` | stemmen op | to vote for | one person stands at a plain booth, one hand sliding a folded blank paper into a slot on top of a box; the box is plain with no marks | Pair with `opkomen-voor-een-vriend` | needed |
| 56 | `profiteren-van-de-zon.png` | profiteren van | to take advantage of | one person sits in a garden chair with a book closed on the knee, face lifted towards a single sun ring above; a second empty chair beside them. Content | Single; gloss-picture | needed |
| 57 | `je-verdiepen-in-het-onderwerp.png` | zich verdiepen in | to delve into | one person leans over a big pile of open books and papers on a desk, elbows on the table, head down into the pages; a mug untouched at the edge. Deep focus | Single; `zich verdiepen in` | needed |
| 58 | `verlangen-naar-buiten.png` | verlangen naar | to long for | a pupil at a desk in a classroom has swung the whole body towards a large window and one hand reaches out to the frame, pencil still in the other hand; outside the window is a tree crown and a plain swing. The chin is up and the eyes wide | Single. The classroom is reused; the desire is aimed out of the window | needed |
| 59 | `zich-concentreren-op-de-opgave.png` | zich concentreren op | to concentrate on | one person sits with both hands framing a single blank page on a desk, elbows down, eyes fixed; everything else on the desk is cleared away | Pair with `klikken-met-de-leraar` | needed |
| 60 | `lachen-om-de-grap.png` | lachen om | to laugh at | two people stand facing each other, one with head tipped back and mouth wide open, the other covering their mouth with one hand; a blank speech bubble between them. Both relaxed | Single; `om` with a cause | needed |
| 61 | `overlijden-aan-een-ziekte.png` | overlijden aan | to die of | a tree stands bare and half fallen beside a small grave-mark shape, a single flower laid at its foot, no person; the trunk is split and still standing | Pair with `houden-van-de-avond` (no shared scene) | needed |
| 62 | `deelnemen-aan-de-wedstrijd.png` | deelnemen aan | to take part in | one person stands at the edge of a plain track with both hands raised, while two others hold a baton shape out towards them; all three turn back towards the new runner | Pair with `slagen-voor-het-examen` | needed |
| 63 | `bijdragen-aan-het-project.png` | bijdragen aan | to contribute to | one person places a plain brick into a low wall being built by two others; all three crouch around the same wall. The wall is a shared mass | Pair with `zorgen-voor-overlast` | needed |
| 64 | `vertellen-over-de-reis.png` | vertellen over | to tell about | one person sits with a large blank folded map open on the knees and both hands raised in a wide gesture, speaking to two seated listeners; the listeners lean in | Single; contrasts with shipped `vertellen aan` | needed |
| 65 | `zorgen-voor-overlast.png` | zorgen voor | to cause | one person carries a large open box that is spilling paper scraps behind them as they walk; the trail of scraps is the main mass, and the person looks back at it | Pair with `bijdragen-aan-het-project` | needed |
| 66 | `houden-van-de-avond.png` | houden van | to love, to like | one person sits on a doorstep at dusk with a cup, a single crescent moon shape above, content and still; the doorway behind is open. One figure | Single; same chunk, new sense | needed |
| 67 | `wennen-aan-het-weer.png` | wennen aan | to get used to | one person walks in slanting rain without an umbrella, coat open, one hand casually shielding the eyes; a small second figure far behind hugs their arms against the rain | Single; same chunk as 5–6, new scene | needed |
| 68 | `slagen-voor-het-examen.png` | slagen voor | to pass | one person leaps with both arms up beside a plain sheet of paper held high; the paper is blank and the leap is the main shape | Pair with `deelnemen-aan-de-wedstrijd` | needed |
| 69 | `vergelijken-met-het-origineel.png` | vergelijken met | to compare with | one person stands side-on, holding a small plain jug out at arm's length beside a larger identical jug on a shelf at the same height, head tilted and eyes moving between them. One figure, no bubble | Pair with `wennen-aan-het-weer`; same camera, the held-out jug is the arm's-length object | needed |
| 70 | `lijken-op-een-bekende.png` | lijken op | to look like | two people stand side by side with identical postures, one taller, both with the same short hair stroke and same profile; a third person points at them both in surprise | Single; `lijken op` | needed |
| 71 | `verhuizen-naar-een-andere-stad.png` | verhuizen naar | to move to | one person carries a large open box up the steps of a plain house, the door open, a van shape parked behind at the kerb with no lettering. The door is the destination | Pair with `wennen-aan-de-nieuwe-baan` | needed |
| 72 | `beloven-aan-de-kinderen.png` | beloven aan | to promise | one adult crouches to eye level with a child and holds out a pinky finger; the child holds out their own pinky; both look at each other. The linked hands are the centre | Pair with `durven-om-hulp-te-vragen` | needed |
| 73 | `wennen-aan-de-nieuwe-baan.png` | wennen aan | to get used to | one person stands in a plain office with a small blank badge shape on the chest, looking around uncertainly, a stack of folders in both arms; a colleague's empty chair behind | Pair with `verhuizen-naar-een-andere-stad` | needed |
| 74 | `zich-ergeren-aan-het-geluid.png` | zich ergeren aan | to be annoyed by | one person sits at a table with a finger pressed into one ear, brow drawn, glaring sideways at a plain radio on the shelf with two short sound strokes. One figure | Pair with `ontbreken-aan-het-overleg` | needed |
| 75 | `geloven-in-het-plan.png` | geloven in | to believe in | one person holds up a large plain drawing with both hands, smiling and nodding, eyes on it; the drawing has one bold loose line suggesting a building. One figure | Pair with `houden-van-de-natuur` | needed |
| 76 | `houden-van-de-natuur.png` | houden van | to love | one person walks away from the viewer along a winding path between two simple round-crowned trees, arms swinging, head tilted up at the crowns. One figure | Pair with `geloven-in-het-plan` | needed |
| 77 | `drukken-op-de-knop.png` | drukken op | to press | one hand with one finger presses a single large round button set into the top of a plain box on a desk; the button is half sunk, with two short strokes under the rim. The other hand rests flat on the desk and the head is bent over it | Pair with `twijfelen-aan-het-antwoord`; same desk height, one hand at a task | needed |
| 78 | `ontbreken-aan-het-overleg.png` | ontbreken aan | to be missing, lacking | one person sits at a round table with three empty chairs around it, alone, looking at the empty seats with an open palm. The empty chairs are the main mass | Pair with `zich-ergeren-aan-het-geluid` | needed |
| 79 | `twijfelen-aan-het-antwoord.png` | twijfelen aan | to doubt | one person sits at a table with a raised pen above a blank sheet, frozen, eyes on the ceiling, head tilted; the free hand is a fist under the chin. One figure | Pair with `drukken-op-de-knop` | needed |
| 80 | `durven-om-hulp-te-vragen.png` | durven om | to dare to | one person stands half-turned away with one hand raised to the mouth, hesitating; a second person two steps away has both hands open, waiting. The raised hand is the main gesture | Pair with `beloven-aan-de-kinderen` | needed |
| 81 | `solliciteren-naar-een-baan.png` | solliciteren naar | to apply for | one person sits opposite a second across a plain desk, one hand holding out a single blank sheet, the other flat on the knee; both are upright and formal. The desk divides them | Pair with `denken-aan-een-andere-baan` | needed |
| 82 | `ruimte-voor-een-tafel.png` | ruimte voor | room for | a big sofa fills the left of the room and a bookcase block the right; between them a clear patch of floor is left white, and one person carries a small table in both hands, just reaching it. The gap is the idea | Single. The space between two big objects is the anchor | needed |
| 83 | `het-eens-zijn-met-de-collega.png` | het eens zijn met | to agree with | two people stand facing each other at a table, each holding a blank card up at chest height; both cards carry the same single heavy dot, and both heads tilt in the same nod. Nothing else is on the table | Single. A mirrored pair of cards, not a one-person acceptance | needed |
| 84 | `bestaan-uit-drie-delen.png` | bestaan uit | to consist of | one person crouches beside a low open box divided by two slats into three equal compartments, each holding a different plain shape; one hand sweeps level along the three, eyes following it left to right. No paper | Pair with `op-zoek-zijn-naar-de-sleutels`; same low box and camera, hand travelling level | needed |
| 85 | `op-zoek-zijn-naar-de-sleutels.png` | op zoek zijn naar | to be looking for | the same crouching person at the same low box, now with no slats; both hands dive down inside it, things spilling over the rim, and one small key-ring shape half lifted. The eyes look down | Pair with `bestaan-uit-drie-delen`; same box and camera, hand diving down, no dividers | needed |
| 86 | `spelen-met-de-kinderen.png` | spelen met | to play with | one adult sits cross-legged on the floor between two children, all three leaning in towards a plain ball mid-roll between the adult and one child, hands out, smiling. The room is bare | Single. Shared play on the floor | needed |
| 87 | `richten-op-het-doel.png` | zich richten op | to aim at | one person stands sideways with one arm raised and a small ball poised, a round target drawn as two plain rings at the far end of the room. The line from hand to target is the idea | Single; `zich richten op` | needed |
| 88 | `denken-aan-een-oplossing-voor-het-probleem.png` | denken aan | to think about | one person sits on the floor with a broken chair beside them and one hand on the cracked leg, brow drawn, eyes on the break. One figure | Single; same chunk, new scene | needed |
| 89 | `denken-aan-een-andere-baan.png` | denken aan | to think about | one person sits at a desk with a blank envelope in one hand, the other resting on a closed laptop lid. One figure, the eyes lifted | Pair with `solliciteren-naar-een-baan` | needed |
| 90 | `zorgen-voor-de-kinderen.png` | zorgen voor | to care for | one adult stands at a table cutting bread with a knife, handing half to a child; a second child at the table holds a plate out. Simple masses, cropped at the shoulders | Single; same chunk as shipped | needed |
| 91 | `beloven-aan-de-buur.png` | beloven aan | to promise | one person stands at a low fence holding up an open hand flat, palm out, as if making a vow; the neighbour on the far side nods and holds up their own hand. The two raised hands face each other | Single; same chunk as 16, new scene | needed |
| 92 | `afhangen-van-de-bus.png` | afhangen van | to depend on | one person stands at a stop with a bag over the shoulder, looking down the empty road and checking a watch; nothing is arriving. Only the waiting is shown | Pair with `afhangen-van-het-weer` | needed |
| 93 | `afhangen-van-het-weer.png` | afhangen van | to depend on | one person stands in the open doorway between inside and outside, one hand on the frame, looking up at a single cloud; behind them indoor furniture, in front an empty street | Pair with `afhangen-van-de-bus` | needed |
| 94 | `kijken-naar-de-klok.png` | kijken naar | to look at | one person stands with one hand on a wall-mounted clock, fingers near the hands, face turned up towards it; the clock face is blank apart from hands and tick marks. One figure | Pair with `kijken-op-de-klok` | needed |
| 95 | `luisteren-naar-de-juf.png` | luisteren naar | to listen to | one person sits at a desk in front, chin on both hands, eyes fixed forward; a second figure stands facing the row with one hand raised. The seated listeners face the standing speaker | Single; `luisteren naar` a person | needed |
| 96 | `lijden-aan-hoofdpijn.png` | lijden aan | to suffer from | one person sits with both temples pressed between two palms, eyes closed tight, head low; a small plain cup and a lamp beside them. One figure, no bandage | Single; `lijden aan` | needed |
| 97 | `genieten-van-de-maaltijd.png` | genieten van | to enjoy | one person sits at a table with a fork halfway to the mouth, eyes closed and an easy smile; the plate holds a simple round meal. One figure | Single; `genieten van` | needed |
| 98 | `stoppen-met-roken.png` | stoppen met | to stop | one person stands outside a building with both hands in their pockets, deliberately turning away from two others who are smoking; no cigarette in their own hand | Single; contrasts with shipped `ophouden met` | needed |
| 99 | `denken-aan-de-toekomst-van-het-kind.png` | denken aan | to think about | one adult stands with one hand on the shoulder of a child seen from behind, both looking out along a long empty path. No bubble; the path is the future | Single; same chunk, new scene | needed |
| 100 | `kijken-op-de-klok.png` | kijken op | to check the time on | the same wall clock as #4, same size and place; one person strides past below it in profile, bag on the shoulder, head turned up for a one-second glance. Both feet are mid-step and no hand touches the clock | Pair with `kijken-naar-de-klok`; the same verb with two prepositions | needed |
| 101 | `vechten-tegen-de-vermoeidheid.png` | vechten tegen | to fight against | one person sits at a desk with heavy eyes, one hand holding the head up by the chin, the other flat on the work. No second figure | Pair with `doorgaan-met-de-les` | needed |
| 102 | `waarschuwen-voor-het-gevaar.png` | waarschuwen voor | to warn about | one person stands with one arm out to stop a second from stepping forward; ahead of them an open hole in the ground is drawn as a plain dark gap. The outstretched arm is the main shape | Pair with `helpen-bij-de-verhuizing-van-de-buren` | needed |
| 103 | `trots-zijn-op-de-afkomst.png` | trots zijn op | to be proud of | one person stands with a hand on an old family album open on the table, chin up, smiling; a simple house shape and a row of small figures on the page are loose strokes | Pair with `onderhandelen-over-de-prijs` | needed |
| 104 | `zich-vergissen-in-de-dag.png` | zich vergissen in | to be mistaken about | one person in a coat with a bag stands in an otherwise empty room with two empty chairs, one fingertip touching one square of a wall calendar while a heavy dot sits in the next square along; the head tilts, brow raised | Pair with `zich-schamen-over-de-fout`; same camera, the wall calendar stays | needed |
| 105 | `zich-schamen-over-de-fout.png` | zich schamen over | to be ashamed of | one person holds both hands over the face, elbows close, shoulders turned in; a second person beside them stands with arms loose, not angry. The hidden face is the idea | Pair with `zich-vergissen-in-de-dag` | needed |
| 106 | `helpen-bij-de-verhuizing-van-de-buren.png` | helpen bij | to help with | one person holds a door open with one arm while a second carries a box through, both leaning with the weight. The door is the main mass | Pair with `waarschuwen-voor-het-gevaar` | needed |
| 107 | `onderhandelen-over-de-prijs.png` | onderhandelen over | to negotiate about | two people sit across a table, one with both palms up and leaning back, the other leaning in with one finger raised; a plain object sits between them. The energy between them is the idea | Pair with `trots-zijn-op-de-afkomst` | needed |
| 108 | `denken-aan-een-andere-oplossing.png` | denken aan | to think of | one person stands over a broken shelf with a plain toolbox open at the feet, one finger on the chin; the broken piece lies beside, and the hand hovers over a single tool | Pair with `zich-voorbereiden-op-het-gesprek` | needed |
| 109 | `zich-voorbereiden-op-het-gesprek.png` | zich voorbereiden op | to prepare for | one person stands in front of a mirror frame, tying a knot at the throat, lips slightly moving as if rehearsing; the reflection is the same figure. One person, two shapes | Pair with `denken-aan-een-andere-oplossing` | needed |
| 110 | `doorgaan-met-de-les.png` | doorgaan met | to continue with | one person stands at the front with an open book in one hand, the other pointing down at the book; two seated heads lean forward. The same session carrying on | Pair with `vechten-tegen-de-vermoeidheid` | needed |
| 111 | `scheiden-van-de-partner.png` | scheiden van | to separate from | two people stand apart with a gap of white between them, each holding one end of the same blank paper; their bodies turn away from each other. No anger, only distance | Pair with `geloven-in-de-liefde` | needed |
| 112 | `deelnemen-aan-het-debat.png` | deelnemen aan | to take part in | one person stands at a table with a hand raised, speaking, facing three seated people who listen; a single blank bubble above the speaker. The raised hand and the seated three are the idea | Pair with `blijven-bij-de-afspraak` | needed |
| 113 | `geloven-in-de-liefde.png` | geloven in | to believe in | one person stands gesturing towards two people who hold hands, all three calm; the standing one has an open palm and a smile. The pair holding hands is the centre | Pair with `scheiden-van-de-partner` | needed |
| 114 | `zich-aanpassen-aan-het-klimaat.png` | zich aanpassen aan | to adapt to | one person in a heavy coat and scarf walks beside one in shirt sleeves, both on the same snowy street; the second is calm, the first hunched. Two figures, one street line | Pair with `zonnen-op-het-balkon` | needed |
| 115 | `herinneren-aan-de-afspraak.png` | herinneren aan | to remind of | one person stands with a small blank card held up towards another, tapping it; the other's hand flies to the forehead in sudden recall. One card only | Single; `herinneren aan` (remind) | needed |
| 116 | `zonnen-op-het-balkon.png` | zonnen op | to sunbathe on | one person lies back on a plain lounger, hands behind the head, eyes closed; a low railing line runs beside them and one sun ring above. One figure | Pair with `zich-aanpassen-aan-het-klimaat` | needed |
| 117 | `hangen-aan-de-haak.png` | hangen aan | to hang on | a plain wall with a single heavy hook at head height; a coat hangs from it by its collar loop, sleeves slack and two short swing strokes at the hem, a bag strap on a lower hook beside it. A band of white lies between hem and floor; no person | Pair with `herinneren-aan-de-afspraak`; same camera and height, the coat hangs from the hook | needed |
| 118 | `beginnen-bij-het-begin.png` | beginnen bij | to start at | one person stands at the first of a row of plain stepping stones, one foot lifted onto it, looking along the row towards a small building at the end | Single; `beginnen bij` | needed |
| 119 | `blijven-bij-de-afspraak.png` | blijven bij | to stick to | one person holds a plain folded paper and taps one spot on it twice with a fingertip, nodding firmly; a second person listens. One marked spot only, no lines of text | Pair with `deelnemen-aan-het-debat` | needed |
| 120 | `zich-schamen-voor-de-klas.png` | zich schamen voor | to be ashamed in front of | one person stands at the front with both hands behind the back and head bowed, one cheek drawn with a small round blush mark; three seated figures look on, drawn plain. No board, no text | Pair with `zich-schamen-over-de-fout` (B1-11) | needed |

## Batch B1-01 — images 1–10

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `beginnen-met-de-les.png` — Dutch chunk: beginnen met (to begin with).
   Scene: one person stands at the front of a simple room, one hand on an open book and the other raised for attention; three seated heads face them, all upright and ready. The first moment of a session.
   Must read: starting a lesson.
   Avoid: a person leaving the room; a clock; readers deep in books already.

2. `beginnen-aan-een-nieuw-huis.png` — Dutch chunk: beginnen aan (to start on).
   Scene: one person stands in front of a half-built wall of bricks, one hand holding a trowel, the other resting on the wall; the wall ends mid-course and continues as empty space.
   Must read: starting a big job.
   Avoid: a finished house; a completed project; a person leaving a building site.

3. `helpen-met-de-afwas.png` — Dutch chunk: helpen met (to help with).
   Scene: two people stand side by side at a sink; one washes a plate and hands it sideways, the other takes it and stacks it. Their arms form a simple relay.
   Must read: sharing a household job.
   Avoid: one person working alone; a restaurant; a dishwasher machine.

4. `helpen-aan-de-balie.png` — Dutch chunk: helpen aan (to help, at a counter).
   Scene: a clerk stands behind a plain desk, leaning forward and pointing at a small form on the desk; a customer sits in front, pen raised. Both look at the form.
   Must read: a helper serving someone at a counter.
   Avoid: two people at a sink (that is the previous pair partner); a queue; readable forms.

5. `zoeken-onder-de-bank.png` — Dutch chunk: zoeken onder (to search under).
   Scene: one person crouches with one cheek near the floor, peering under a bench; one hand reaches into the gap, a bag lies on its side beside them. The bench and the gap are the main mass.
   Must read: searching underneath furniture.
   Avoid: keys on the floor that are already found (used by the pilot); a magnifying glass; a person looking in a cupboard.

6. `zoeken-in-de-tas.png` — Dutch chunk: zoeken in (to search in).
   Scene: one person holds a large open bag at chest height and looks down into it, the other hand buried inside; a single loose stroke shows one item pushed up. The bag is the main mass.
   Must read: rummaging inside a bag.
   Avoid: an empty bag with an item falling out; a person going through someone else's drawers; a wallet with cards.

7. `zorgen-voor-het-huisdier.png` — Dutch chunk: zorgen voor (to look after).
   Scene: one person crouches to fill a bowl on the floor while a cat waits with its tail up, one hand steadying the bowl. The cat and bowl are the main mass.
   Must read: taking care of a pet.
   Avoid: a person hugging the animal (that is love, used by the pilot); a vet; a dog on a lead.

8. `denken-aan-de-toekomst.png` — Dutch chunk: denken aan (to think about).
   Scene: one person sits by a plain window at dusk, chin on the hand, looking out; a small blank thought bubble floats beside them and contains only an open road shape. No second figure.
   Must read: thinking ahead about future plans.
   Avoid: a face in the thought bubble (used by the pilot); two options; a calendar with numbers.

9. `praten-over-het-weer.png` — Dutch chunk: praten over (to talk about).
   Scene: two people stand under a shop awning, both looking up and outward at a rain cloud; one points at the cloud, both speech bubbles are blank. The cloud is the topic.
   Must read: small talk about the weather.
   Avoid: a house between them (used by the pilot); an umbrella open over them both; readable weather signs.

10. `praten-tegen-zichzelf.png` — Dutch chunk: praten tegen jezelf (to talk to yourself).
    Scene: one person walks alone along a path, one hand gesturing in the air in front of them, mouth a short line; a single small blank speech bubble near the head, and nobody else in the frame.
    Must read: talking aloud with no one else there.
    Avoid: a phone at the ear; a second figure in the distance; a person lecturing a group.

CONTRAST PAIRS
1 and 2 are `beginnen` with two prepositions: the start of a session versus the start of a large task. Same camera, one figure in the foreground. In #1 there are listeners; in #2 there is a wall that stops mid-course.
3 and 4 are `helpen` with two prepositions: helping with a job beside someone versus helping someone at a counter. Same camera; the relation between the two figures is the difference — side by side versus across.
5 and 6 are `zoeken` with two prepositions: under versus inside. Same searching body and same reaching hand; change only the container.
1 and 2 are `beginnen` again, and 3 and 4 `helpen` again: two small-task batches where the same verb returns with a different preposition, so the pairs read as one family.
7, 8, 9 and 10 are singles. #7 must not repeat the caring-for-a-child pilot scene; the animal is the cared-for one. #8 must not repeat the pilot thought-bubble face. #9 must not repeat the pilot talking-about-a-house scene. #10 must not look like the pilot talk-at-a-person scene: there is no other person at all.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition obvious from the layout of shapes, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-02 — images 11–20

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `wachten-op-antwoord.png` — Dutch chunk: wachten op (to wait for).
   Scene: one person sits at a table with a phone flat in front of them, both hands clasped, eyes on the phone; the posture is patient and tense. Only one figure.
   Must read: waiting for a reply.
   Avoid: a bus stop (used by the pilot); a queue; two people talking.

2. `rekenen-op-hulp.png` — Dutch chunk: rekenen op (to count on).
   Scene: one person stands with one arm raised towards a second person who is offering a steadying hand from a ladder; the first person leans their weight on that hand. The hand is the main mass.
   Must read: relying on someone's help.
   Avoid: a person doing arithmetic with a calculator; money being counted; a handshake.

3. `denken-aan-een-oplossing.png` — Dutch chunk: denken aan (to think of).
   Scene: one person snaps their fingers with an open smile, eyes lifted; one finger of the other hand points up. No bubble, no second person, only the sudden thought.
   Must read: suddenly recalling an answer.
   Avoid: a light bulb symbol; a question mark; a calendar (used by the pilot memory scene).

4. `geloven-in-jezelf.png` — Dutch chunk: geloven in (to believe in).
   Scene: one person stands in front of a mirror shape drawn as a single tall frame; the reflection is the same figure, chin up, fist lightly closed at the chest. Both figures are calm and strong.
   Must read: self-belief.
   Avoid: two different people; a heart; a medal.

5. `zorgen-voor-elkaar.png` — Dutch chunk: zorgen voor (to care for).
   Scene: one person covers another's shoulders with a blanket while the other sits on a sofa with a cup; both are relaxed and close. The blanket is the main mass.
   Must read: two people looking after one another.
   Avoid: a child (used by the pilot); a doctor with a bandage; a pet.

6. `denken-over-een-beslissing.png` — Dutch chunk: denken over (to think about).
   Scene: one person stands at a doorway between two rooms, one hand on each side of the frame, head turned to look first one way then the other. The two rooms are drawn identically.
   Must read: weighing up a decision between two places.
   Avoid: two objects side by side on a table (used by the pilot); a question mark; a crowd.

7. `klagen-over-het-weer.png` — Dutch chunk: klagen over (to complain about).
   Scene: one person wraps both arms around themselves, shoulders hunched, mouth a downward line, looking up at slanting rain; one hand is held out, palm up, at the rain. No second figure.
   Must read: grumbling about bad weather.
   Avoid: a broken machine (used by the pilot); an umbrella; a service desk.

8. `zoeken-naar-een-baan.png` — Dutch chunk: zoeken naar (to search for).
   Scene: one person sits at a laptop, one hand at the chin and the other on a heap of blank papers; a small blank noticeboard with one sheet pinned on the wall behind. Focused, not reading comfortably.
   Must read: hunting for work.
   Avoid: a job interview; keys on the floor (used by the pilot); readable job adverts.

9. `kijken-naar-een-vogel.png` — Dutch chunk: kijken naar (to look at).
   Scene: one person stands at a plain window, both hands on the sill, leaning forward with their nose near the glass; outside the glass one small bird sits on a bare branch, wings folded. Steady attention, not surprise.
   Must read: watching something outside from indoors.
   Avoid: binoculars; a cat beside the window; two people watching together.

10. `praten-met-de-dokter.png` — Dutch chunk: praten met (to talk with).
    Scene: one person sits on the edge of a plain bed and speaks with raised hand to a second person in a plain coat, who listens and points at a clipboard; the clipboard is blank. No readable charts.
    Must read: a conversation with a professional.
    Avoid: two friends chatting (used by the pilot); a stethoscope as the main object; a hospital corridor.

CONTRAST PAIRS
1 and 6 are the two sides of waiting for a decision: a reply that has not come, and a choice between two doors. Same camera, one figure; #6 adds the second room.
2 and 5 are both reliance on other people: counting on help, and mutual care. Same camera; #2 is a hand from above, #5 is a blanket.
3 and 4 are both about confidence from inside: a sudden idea and self-belief. Same upright, bright posture; the difference is the mirror in #4 and the empty air in #3.
1 and 7 are both about something withheld or unwanted from outside: no reply, and bad weather. Same lone figure, same tense shoulders; #1 looks down at a phone, #7 looks up at rain.
9 and 10 are singles, and the only frames here with a second body in view: a bird outside the glass, and a professional seated opposite.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then compare the three pairs side by side. If either image in a pair suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-03 — images 21–30

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `zich-verheugen-op-de-vakantie.png` — Dutch chunk: zich verheugen op (to look forward to).
   Scene: one person sits with knees drawn up, arms wrapped around them, smiling and looking at a plain suitcase standing by the door; the suitcase has no stickers or labels. Content, not busy.
   Must read: happy anticipation of a trip.
   Avoid: a calendar with a marked day (used by the pilot for looking forward to a holiday); a person already on the beach; a clock.

2. `genieten-van-de-zon.png` — Dutch chunk: genieten van (to enjoy).
   Scene: one person lies back on a striped deckchair, eyes closed, hands behind the head, a single sun shape drawn as an open ring of short strokes in the top corner. Relaxed mouth.
   Must read: pleasure in the sun.
   Avoid: a beach ball or ice cream; a person sleeping with a blanket; a sun with rays as a solid star.

3. `rekening-houden-met-de-buren.png` — Dutch chunk: rekening houden met (to take into account).
   Scene: one person carries a loud musical instrument or a drill case towards a shared wall, then stops with one hand raised flat, mouth closed; on the other side of the wall a second person holds a finger to their lips. The wall divides them.
   Must read: being considerate of neighbours.
   Avoid: a person covering their ears (used by the pilot for noise annoyance); a bill or receipt; an argument across the wall.

4. `ruzie-maken-met-collega.png` — Dutch chunk: ruzie maken met (to argue with).
   Scene: two people face each other with one arm each raised and pointed, both leaning forward, mouths drawn as short open lines; a small gap of white between them. No bubbles.
   Must read: a conflict between two people.
   Avoid: someone looking sad alone; a fist fight; a boss behind a desk.

5. `denken-aan-de-kosten.png` — Dutch chunk: denken aan (to think of).
   Scene: one person sits at a table with a small calculator and a plain long receipt in front of them, chin on hand and brow a single line; the other hand counts on the edge of a coin stack. One figure.
   Must read: thinking about the expense.
   Avoid: readable numbers or prices; a shop counter; a second person.

6. `wijzen-op-een-fout.png` — Dutch chunk: wijzen op (to point out).
   Scene: a row of five identical plain framed pictures hangs on a wall; four are level and one hangs tilted. One person stands at the side, arm stretched, one finger pointing at the tilted frame, head turned towards the viewer.
   Must read: pointing out a mistake.
   Avoid: a person hanging up a picture; a person pointing at a drawing marked with a cross (that is `kritiek op`); a teacher at a board.

7. `passen-op-de-buurkinderen.png` — Dutch chunk: passen op (to look after).
   Scene: one adult sits upright on the edge of a sofa, hands on the knees and one hand half raised, eyes following two small children at the far side of the room, one of whom has climbed onto a low stool. The adult is alert, not joining in.
   Must read: watching over small children.
   Avoid: playing with the children (that is `spelen met`); a person feeding a child; an adult asleep on the sofa.

8. `akkoord-gaan-met-het-voorstel.png` — Dutch chunk: akkoord gaan met (to agree to).
   Scene: one person sits at the same desk and chair, a single sheet in front and a pen touching one short line on it, nodding with an easy mouth line. The desk is otherwise bare.
   Must read: agreeing to a proposal.
   Avoid: a person frozen over a sheet with a raised pen; a handshake across a table; a calculator and receipts.

9. `kennismaken-met-de-nieuwe-buur.png` — Dutch chunk: kennismaken met (to get acquainted with).
   Scene: two people on either side of a low fence shake hands across it, both smiling; a small potted shape or a bunch of keys in one free hand. The handshake crosses the fence.
   Must read: meeting a new neighbour.
   Avoid: a formal interview across a desk; three or more people; readable name plates.

10. `kloppen-op-de-deur.png` — Dutch chunk: kloppen op (to knock on).
    Scene: one person stands in profile at a closed plain door with a round knob and no window, one fist raised and touching it; three short strokes of sound sit at the fist. The other arm hangs loose.
    Must read: knocking on a door.
    Avoid: a person ringing a bell; a person already entering; someone tapping a window.

CONTRAST PAIRS
1 and 2 are both enjoyment ahead and in the moment: #1 looks at the suitcase, #2 lies back in the sun. Same camera, one figure; change the posture from anticipation to bliss.
3 and 4 are both `met` relations that go wrong or right for people around you: consideration for a neighbour versus an argument with a colleague. #3 uses a wall and two figures apart; #4 uses a face-to-face pair. Neither may show a wall and a face-to-face pair at once.
5 and 8 are both a decision at a desk: weighing money versus accepting a proposal. Same desk and camera; change the props (calculator and receipt versus one sheet and a pen).
6, 7, 9 and 10 are singles. #6 points at a flaw with no cross on it; #7 watches children but does not join in.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-04 — images 31–40

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `afspreken-met-een-vriend.png` — Dutch chunk: afspreken met (to arrange to meet).
   Scene: two people stand facing each other with a small blank calendar page held between them; both point at the same spot on the page, smiling. The page floats mid-air, plain, with one thick dot.
   Must read: agreeing on a shared time.
   Avoid: a phone; a diary with numbers; a person alone.

2. `afspreken-op-een-tijd.png` — Dutch chunk: afspreken op (to agree on a time).
   Scene: one person holds up a wristwatch and points at its face while looking at a second person beside them, who nods; the watch is plain with hands and no numbers.
   Must read: settling on an hour.
   Avoid: readable times; a person late and running; a calendar.

3. `hulp-vragen-aan-de-buurman.png` — Dutch chunk: hulp vragen aan (to ask help from).
   Scene: two people stand a few steps apart, side-on, with a gap of white between them; the first holds a closed jar out in both hands with head tilted and brow raised, and the neighbour steps forward with both hands open to take it. No ladder.
   Must read: asking a neighbour for help.
   Avoid: a gift being handed over; a ladder being given; two people arguing.

4. `schrijven-aan-de-gemeente.png` — Dutch chunk: schrijven aan (to write to).
   Scene: one person sits at a desk writing a letter with a pen on a single page of long lines; beside it lies a large plain envelope with a small pillared public-building shape drawn on its front. The page has no marks that read as words.
   Must read: writing a letter to an office.
   Avoid: filling in a form; a person at a laptop; a postman or letterbox.

5. `helpen-bij-de-verhuizing.png` — Dutch chunk: helpen bij (to help with).
   Scene: two people carry one open box together, each holding one side, moving towards the viewer; a third box sits on the ground behind them. Bodies lean into the weight.
   Must read: helping someone move house.
   Avoid: handing a box across a fence (used by the pilot for passing on); a moving van with logos; a person lifting alone.

6. `blijven-bij-een-vriend.png` — Dutch chunk: blijven bij (to stay with).
   Scene: one person sits down on a simple sofa beside another who is wrapped in a blanket with a cup; the arriving person's hand rests on the other's shoulder. The seated pair, close together.
   Must read: staying with someone.
   Avoid: a person leaving through a door; a doctor; a party.

7. `kennismaken-met-nieuwe-mensen.png` — Dutch chunk: kennismaken met (to meet).
   Scene: three people stand in a loose circle, the nearest one reaching a hand towards the middle; a fourth approaches from the side with a raised hand and a smile. Simple figures, no name tags.
   Must read: introductions in a group.
   Avoid: a queue; a stage and audience; readable badges.

8. `passen-bij-elkaar.png` — Dutch chunk: passen bij (to go with, to match).
   Scene: two cloths hang side by side on a clothes line, the same size and the same squared-off shape, their lower corners level; a third, visibly narrower cloth hangs apart at the far end with a gap of white. A small figure at the left steps back, one hand on the chin, nodding.
   Must read: two things that match.
   Avoid: a person pegging washing; two cloths that clearly differ in size; a wardrobe full of clothes.

9. `oefenen-voor-het-examen.png` — Dutch chunk: oefenen voor (to practise for).
   Scene: one person sits at a table with a blank test paper and a pen, writing, a stack of books beside them; on the wall behind, a large plain clock with hands but no numbers. Focused.
   Must read: rehearsing for a test.
   Avoid: a person taking the exam with a teacher walking between desks; readable questions; a graduation cap.

10. `denken-aan-het-verleden.png` — Dutch chunk: denken aan (to think back to).
    Scene: one person sits by a window with an old photo in one hand and the other hand on the heart; the photo is a plain rectangle showing a small simple couple shape. The posture is wistful, not sad.
    Must read: remembering long ago.
    Avoid: a thought bubble with a face (used by the pilot); a telephone; a clock.

CONTRAST PAIRS
1 and 2 are both `afspreken`: a shared plan versus a specific hour. Same two figures, same camera; #1 holds a page with a dot, #2 holds a wristwatch.
3 is a single: two figures side-on with a gap of white, a jar held out and open hands coming to take it. It must not repeat #5, where a box is carried between two people.
4 and 9 are a pen on a page: a letter to an office, and rehearsing for a test. Same desk height, same pen and page; #4 has an envelope with a building shape, #9 books and a clock.
5 is a box carried by two, and 8 is two matching cloths on a line: both are singles. Do not pair them with each other; #8 shows no pegging hand and no picture on a wall.
7 is the only group scene here: three or four people, no queue, no stage.
1 and 2 are the same `afspreken` in one batch: a shared plan versus a settled hour.
6 is a single. It must not repeat the pilot caring-for-a-child scene: the person in the blanket is an adult, and the hand on the shoulder is the `bij`.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-05 — images 41–50

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `raken-aan-de-schouder.png` — Dutch chunk: raken aan (to touch).
   Scene: one person taps a seated colleague on the shoulder with the flat of a hand; the seated person turns their head. Only the hand rests on the shoulder.
   Must read: a touch on the shoulder.
   Avoid: a tap on the door; a handshake; a person pushing.

2. `raken-aan-het-plafond.png` — Dutch chunk: raken aan (to reach, to touch).
   Scene: one person stands on tiptoe with one hand stretched up, fingertips nearly on a plain ceiling line above; the other arm balances out sideways.
   Must read: stretching up to reach a height.
   Avoid: a ladder; a chair underfoot; a person jumping.

3. `leren-van-je-fouten.png` — Dutch chunk: leren van (to learn from).
   Scene: one person sits at a desk with a blank sheet of paper and a pen, looking at a small plain cross drawn on it, then drawing a clean circle beside it; one figure, focused.
   Must read: learning from a mistake.
   Avoid: a teacher; a red mark; a book with readable text.

4. `leren-nederlands-met-zinnen.png` — Dutch chunk: leren met (to learn with).
   Scene: one person sits at a table with a notebook open and a pen raised, mouth set in concentration; a plain card lies beside the book with a single simple stroke on it. One figure.
   Must read: practising a language.
   Avoid: readable words; a teacher in front of a class; a phone.

5. `denken-aan-kerstmis.png` — Dutch chunk: denken aan (to think of).
   Scene: one person sits on a simple chair with a blank folded card in their hands, a small plain fir-tree shape drawn beside them, eyes soft and lifted. One figure.
   Must read: fondly remembering a festive time.
   Avoid: a decorated tree with ornaments; a gift with a ribbon; a Santa figure.

6. `denken-aan-vroeger.png` — Dutch chunk: denken aan (to think back to).
   Scene: one person sits by a window with an old photo in one hand and the other hand on the heart; the photo is a plain rectangle showing a small simple couple shape. Wistful, not sad.
   Must read: remembering long ago.
   Avoid: a thought bubble with a face (used by the pilot); a telephone; a clock.

7. `denken-aan-een-cadeau.png` — Dutch chunk: denken aan (to think of).
   Scene: one person stands in a shop aisle, one finger on the chin, looking at a plain box on a shelf; the other hand holds a blank card. Only one figure.
   Must read: choosing a present in the mind.
   Avoid: a wrapped ribbon gift (used by the pilot); a shop sign; a second person.

8. `trouwen-met-de-liefde.png` — Dutch chunk: trouwen met (to marry).
   Scene: two people stand face to face holding hands, both smiling; a simple ring shape is drawn on a small cushion between them. Plain figures, no dress detail.
   Must read: marrying someone.
   Avoid: a church building; a bouquet; a crowd of guests.

9. `verliezen-van-het-team.png` — Dutch chunk: verliezen van (to lose against).
   Scene: two teams are drawn as a row of three figures each, facing each other; one side slumps with lowered heads, the other raises both arms. A plain ball lies between them.
   Must read: losing a match to another side.
   Avoid: a referee; a trophy; readable scores.

10. `proosten-op-het-succes.png` — Dutch chunk: proosten op (to toast to).
   Scene: two people stand facing each other with glasses raised and just touching, both smiling; a plain folded document on the table between them. Glasses are plain.
   Must read: celebrating a success.
   Avoid: a party with many guests; readable bottles; a cake.

CONTRAST PAIRS
1 and 2 are both `raken aan`: a touch on a person and a stretch to a height. Same camera and one figure each; the difference is the shoulder versus the ceiling.
3 and 4 are both `leren`: learning from a mistake on a plain sheet, and working at a language with a card. Same desk and camera.
5, 6 and 7 are `denken aan` with one object of thought each: a card and a fir-tree shape, a photo, a box on a shelf.
8, 9 and 10 are singles. #8 must not reuse a pair of people at a table; the pair stand hand in hand.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-06 — images 51–60

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `horen-bij-de-groep.png` — Dutch chunk: horen bij (to belong to).
   Scene: four people stand shoulder to shoulder facing the viewer, arms across one another's backs; the fourth has just stepped in, one arm still settling onto the neighbour's shoulder as a gap closes. No bubble, no objects.
   Must read: belonging to a group.
   Avoid: a loose circle meeting a stranger (that is `kennismaken met`); a person alone at the edge; a team photo with a banner.

2. `opkomen-voor-een-vriend.png` — Dutch chunk: opkomen voor (to stand up for).
   Scene: one person steps in front of a smaller friend, arms spread wide and chest out, facing a larger figure who leans back. The defender is the nearest figure.
   Must read: defending a friend.
   Avoid: a fight; a legal scene; a crowd.

3. `klikken-met-de-leraar.png` — Dutch chunk: klikken met (to click, to get on with).
   Scene: one person sits with a small square device on the table and presses it with one finger; on the plain wall behind, a small square panel lights up as a short burst of strokes. Only one figure.
   Must read: pressing to switch a thing on.
   Avoid: a mouse and computer screen (that reads as using a computer); two people laughing (that asks for a different verb); a camera.

4. `reageren-op-de-vraag.png` — Dutch chunk: reageren op (to respond to).
   Scene: one person leans in with an open hand and one blank speech bubble; the second person turns their head and lifts one hand in answer, mouth moving. One bubble only, from the first.
   Must read: answering what was said.
   Avoid: a letter with readable text; a person ignoring; an argument.

5. `stemmen-op-een-partij.png` — Dutch chunk: stemmen op (to vote for).
   Scene: one person stands at a plain booth, one hand sliding a folded blank paper into a slot on top of a box; the box is plain with no marks.
   Must read: casting a vote.
   Avoid: a readable ballot; a crowd at a rally; a flag.

6. `profiteren-van-de-zon.png` — Dutch chunk: profiteren van (to take advantage of).
   Scene: one person sits in a garden chair with a book closed on the knee, face lifted towards a single sun ring above; a second empty chair beside them. Content.
   Must read: enjoying a good chance.
   Avoid: a shop sale; a calculator; a person asleep.

7. `je-verdiepen-in-het-onderwerp.png` — Dutch chunk: zich verdiepen in (to delve into).
   Scene: one person leans over a big pile of open books and papers on a desk, elbows on the table, head down into the pages; a mug untouched at the edge. Deep focus.
   Must read: studying something closely.
   Avoid: a library shelf; readable titles; a laptop screen.

8. `verlangen-naar-buiten.png` — Dutch chunk: verlangen naar (to long for).
   Scene: a pupil at a desk in a classroom has swung the whole body towards a large window and one hand reaches out to the frame, pencil still in the other hand; outside the window is a tree crown and a plain swing. The chin is up and the eyes wide.
   Must read: longing to be outside.
   Avoid: a pupil with chin on both hands, bored; a person looking at a bird; an open front door.

9. `zich-concentreren-op-de-opgave.png` — Dutch chunk: zich concentreren op (to concentrate on).
   Scene: one person sits with both hands framing a single blank page on a desk, elbows down, eyes fixed; everything else on the desk is cleared away.
   Must read: complete attention to one task.
   Avoid: a phone; two papers side by side; a person yawning.

10. `lachen-om-de-grap.png` — Dutch chunk: lachen om (to laugh at).
   Scene: two people stand facing each other, one with head tipped back and mouth wide open, the other covering their mouth with one hand; a blank speech bubble between them. Both relaxed.
   Must read: laughing at something funny.
   Avoid: a person crying; a jest at someone's expense with pointing fingers; a joke written on paper.

CONTRAST PAIRS
1 and 4 are both exchanges between people at close range: one belongs by arm and shoulder, one answers in words. In #4 there is a speech bubble; in #1 there is none.
2 and 5 are both standing up for something or joining something: defending a friend, and casting a vote. Both use a raised or forward gesture; #5 is alone at a booth.
3 and 9 are both attention on one small square on a table: a device, and a cleared page framed by hands. Same camera; keep #3's wall panel and #9's empty desk.
6, 7, 8 and 10 are singles. #8 is the classroom with a window; no pupil bored with chin on hands.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-07 — images 61–70

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `overlijden-aan-een-ziekte.png` — Dutch chunk: overlijden aan (to die of).
   Scene: a tree stands bare and half fallen beside a small grave-mark shape, a single flower laid at its foot, no person; the trunk is split and still standing.
   Must read: death caused by illness.
   Avoid: a cross; a church; a person in bed.

2. `deelnemen-aan-de-wedstrijd.png` — Dutch chunk: deelnemen aan (to take part in).
   Scene: one person stands at the edge of a plain track with both hands raised, while two others hold a baton shape out towards them; all three turn back towards the new runner.
   Must read: joining a race.
   Avoid: a finish line with tape; a crowd; a trophy.

3. `bijdragen-aan-het-project.png` — Dutch chunk: bijdragen aan (to contribute to).
   Scene: one person places a plain brick into a low wall being built by two others; all three crouch around the same wall. The wall is a shared mass.
   Must read: adding your part to a shared job.
   Avoid: a donation box with coins; a person carrying a brick away; readable plans.

4. `vertellen-over-de-reis.png` — Dutch chunk: vertellen over (to tell about).
   Scene: one person sits with a large blank folded map open on the knees and both hands raised in a wide gesture, speaking to two seated listeners; the listeners lean in.
   Must read: recounting a journey.
   Avoid: a map with readable place names; a slideshow screen; a person alone.

5. `zorgen-voor-overlast.png` — Dutch chunk: zorgen voor (to cause).
   Scene: one person carries a large open box that is spilling paper scraps behind them as they walk; the trail of scraps is the main mass, and the person looks back at it.
   Must read: causing a mess.
   Avoid: a person cleaning up; a bin; two people arguing about it.

6. `houden-van-de-avond.png` — Dutch chunk: houden van (to love, to like).
   Scene: one person sits on a doorstep at dusk with a cup, a single crescent moon shape above, content and still; the doorway behind is open. One figure.
   Must read: loving the evening itself.
   Avoid: a person hugging a dog (used by the pilot); a party; a night city with lit windows.

7. `wennen-aan-het-weer.png` — Dutch chunk: wennen aan (to get used to).
   Scene: one person walks in slanting rain without an umbrella, coat open, one hand casually shielding the eyes; a small second figure far behind hugs their arms against the rain.
   Must read: becoming used to bad weather.
   Avoid: a person dry under an umbrella; snow; a weather chart.

8. `slagen-voor-het-examen.png` — Dutch chunk: slagen voor (to pass).
   Scene: one person leaps with both arms up beside a plain sheet of paper held high; the paper is blank and the leap is the main shape.
   Must read: passing a test.
   Avoid: a graduation cap with a motto; a diploma with readable text; a crowd.

9. `vergelijken-met-het-origineel.png` — Dutch chunk: vergelijken met (to compare with).
   Scene: one person stands side-on, holding a small plain jug out at arm's length beside a larger identical jug on a shelf at the same height, head tilted and eyes moving between them. One figure, no bubble.
   Must read: checking a copy against the original.
   Avoid: a mirror with a reflection; two people comparing; a shop display of many items.

10. `lijken-op-een-bekende.png` — Dutch chunk: lijken op (to look like).
   Scene: two people stand side by side with identical postures, one taller, both with the same short hair stroke and same profile; a third person points at them both in surprise.
   Must read: resembling someone.
   Avoid: a mirror (that is a reflection); a mask; a photo.

CONTRAST PAIRS
1 and 6 are both `aan`/`van` frames one would never draw as a hand reaching towards someone: a life ending beside a bare tree, and calm affection for an evening. Keep the tree and the grave still and horizontal, the figure on the doorstep upright and small.
2 and 8 are both trying to win or complete something: taking part in a race and passing a test. Same upright, forward posture; #2 has three runners on a track, #8 one person leaping with a blank paper.
3 and 5 are both contributions: building up and making a mess. Same walk and same wall-like mass; change only whether the pieces are being placed or spilling.
7 and 9 are both a body measured against something: the weather, and an original. Same camera, one figure each; #9 holds a small jug out at arm's length.
4 and 10 are singles.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-08 — images 71–80

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `verhuizen-naar-een-andere-stad.png` — Dutch chunk: verhuizen naar (to move to).
   Scene: one person carries a large open box up the steps of a plain house, the door open, a van shape parked behind at the kerb with no lettering. The door is the destination.
   Must read: moving to a new home.
   Avoid: a person leaving a house (that is going away); a suitcase flight; readable street signs.

2. `beloven-aan-de-kinderen.png` — Dutch chunk: beloven aan (to promise).
   Scene: one adult crouches to eye level with a child and holds out a pinky finger; the child holds out their own pinky; both look at each other. The linked hands are the centre.
   Must read: making a promise to someone.
   Avoid: a written contract; a handshake between adults; a gift.

3. `wennen-aan-de-nieuwe-baan.png` — Dutch chunk: wennen aan (to get used to).
   Scene: one person stands in a plain office with a small blank badge shape on the chest, looking around uncertainly, a stack of folders in both arms; a colleague's empty chair behind.
   Must read: settling into a new job.
   Avoid: a person doing the job confidently; a boss pointing; readable posters.

4. `zich-ergeren-aan-het-geluid.png` — Dutch chunk: zich ergeren aan (to be annoyed by).
   Scene: one person sits at a table with a finger pressed into one ear, brow drawn, glaring sideways at a plain radio on the shelf with two short sound strokes. One figure.
   Must read: irritation at a noise.
   Avoid: covering both ears in fright (used by the pilot); a broken machine; a person asleep.

5. `geloven-in-het-plan.png` — Dutch chunk: geloven in (to believe in).
   Scene: one person holds up a large plain drawing with both hands, smiling and nodding, eyes on it; the drawing has one bold loose line suggesting a building. One figure.
   Must read: confidence in a plan.
   Avoid: a person criticising the plan; a light bulb; a second person.

6. `houden-van-de-natuur.png` — Dutch chunk: houden van (to love).
   Scene: one person walks away from the viewer along a winding path between two simple round-crowned trees, arms swinging, head tilted up at the crowns. One figure.
   Must read: affection for the outdoors.
   Avoid: a person hugging a tree; a flower bouquet; a lake with boats.

7. `drukken-op-de-knop.png` — Dutch chunk: drukken op (to press).
   Scene: one hand with one finger presses a single large round button set into the top of a plain box on a desk; the button is half sunk, with two short strokes under the rim. The other hand rests flat on the desk and the head is bent over it.
   Must read: pressing a button.
   Avoid: a lit panel or light on the wall; a keyboard; a doorbell on a wall.

8. `ontbreken-aan-het-overleg.png` — Dutch chunk: ontbreken aan (to be missing, lacking).
   Scene: one person sits at a round table with three empty chairs around it, alone, looking at the empty seats with an open palm. The empty chairs are the main mass.
   Must read: someone who is not there.
   Avoid: a person arriving late and running; a clock; a phone.

9. `twijfelen-aan-het-antwoord.png` — Dutch chunk: twijfelen aan (to doubt).
   Scene: one person sits at a table with a raised pen above a blank sheet, frozen, eyes on the ceiling, head tilted; the free hand is a fist under the chin. One figure.
   Must read: uncertainty about the answer.
   Avoid: two options side by side; a person writing confidently; a question mark.

10. `durven-om-hulp-te-vragen.png` — Dutch chunk: durven om (to dare to).
   Scene: one person stands half-turned away with one hand raised to the mouth, hesitating; a second person two steps away has both hands open, waiting. The raised hand is the main gesture.
   Must read: finding the courage to ask.
   Avoid: a question mark; a phone; a crowd.

CONTRAST PAIRS
1 and 3 are both arriving in a new place with something in both arms: a box carried into a new home, and folders carried into a new office. Same camera; change the door and the desk.
2 and 10 are both a small signal between two people at arm's length: a pinky promise, and a half-raised hand of hesitation. #2 links hands; #10 keeps a step of white between them.
4 and 8 are both alone at a table set for more people: an ear stopped against a radio, and empty chairs around a round table. Same camera; #8 has no other object but chairs.
5 and 6 are both a person's affection for something bigger than a person: a plan held up, and a path through trees. One figure each.
7 and 9 are both a single hand at a task: a finger pressing a button, and a pen that will not start. Same desk height and camera.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-09 — images 81–90

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `solliciteren-naar-een-baan.png` — Dutch chunk: solliciteren naar (to apply for).
   Scene: one person sits opposite a second across a plain desk, one hand holding out a single blank sheet, the other flat on the knee; both are upright and formal. The desk divides them.
   Must read: applying for a job.
   Avoid: a queue; readable job adverts; two friends chatting.

2. `ruimte-voor-een-tafel.png` — Dutch chunk: ruimte voor (room for).
   Scene: a big sofa fills the left of the room and a bookcase block the right; between them a clear patch of floor is left white, and one person carries a small table in both hands, just reaching it. The gap is the idea.
   Must read: there is room for a table.
   Avoid: a person measuring with a tape; a crowded room; moving boxes into a house.

3. `het-eens-zijn-met-de-collega.png` — Dutch chunk: het eens zijn met (to agree with).
   Scene: two people stand facing each other at a table, each holding a blank card up at chest height; both cards carry the same single heavy dot, and both heads tilt in the same nod. Nothing else is on the table.
   Must read: two people who hold the same view.
   Avoid: a handshake across a table; one person signing a paper (that is `akkoord gaan met`); two cards with different marks.

4. `bestaan-uit-drie-delen.png` — Dutch chunk: bestaan uit (to consist of).
   Scene: one person crouches beside a low open box divided by two slats into three equal compartments, each holding a different plain shape; one hand sweeps level along the three, eyes following it left to right. No paper.
   Must read: a whole made of three parts.
   Avoid: a box being unpacked with paper hanging out; a shelf of objects; a measuring tool.

5. `op-zoek-zijn-naar-de-sleutels.png` — Dutch chunk: op zoek zijn naar (to be looking for).
   Scene: the same crouching person at the same low box, now with no slats; both hands dive down inside it, things spilling over the rim, and one small key-ring shape half lifted. The eyes look down.
   Must read: searching for keys.
   Avoid: a person holding the keys already; a locked door; a bag held at chest height.

6. `spelen-met-de-kinderen.png` — Dutch chunk: spelen met (to play with).
   Scene: one adult sits cross-legged on the floor between two children, all three leaning in towards a plain ball mid-roll between the adult and one child, hands out, smiling. The room is bare.
   Must read: playing with children.
   Avoid: an adult watching from a sofa (that is `passen op`); stacking blocks; a team game.

7. `richten-op-het-doel.png` — Dutch chunk: zich richten op (to aim at).
   Scene: one person stands sideways with one arm raised and a small ball poised, a round target drawn as two plain rings at the far end of the room. The line from hand to target is the idea.
   Must read: aiming at a goal.
   Avoid: a dartboard with numbers; a crowd; a second player.

8. `denken-aan-een-oplossing-voor-het-probleem.png` — Dutch chunk: denken aan (to think about).
   Scene: one person sits on the floor with a broken chair beside them and one hand on the cracked leg, brow drawn, eyes on the break. One figure.
   Must read: considering how to repair something.
   Avoid: a toolkit with labelled tools; a second person; a light bulb.

9. `denken-aan-een-andere-baan.png` — Dutch chunk: denken aan (to think about).
   Scene: one person sits at a desk with a blank envelope in one hand, the other resting on a closed laptop lid. One figure, the eyes lifted.
   Must read: considering another job.
   Avoid: a second person behind a desk (that is an interview); readable job adverts; a phone.

10. `zorgen-voor-de-kinderen.png` — Dutch chunk: zorgen voor (to care for).
   Scene: one adult stands at a table cutting bread with a knife, handing half to a child; a second child at the table holds a plate out. Simple masses, cropped at the shoulders.
   Must read: feeding and looking after children.
   Avoid: a school gate; a doctor; a busy kitchen.

CONTRAST PAIRS
1 and 9 are both `naar`/`aan` frames about work: an interview across a desk, and considering a change at a desk. Same camera; #1 has two figures, #9 has one figure and an envelope.
2, 3 and 7 each own a room with a character of its own: a table carried into a gap, two cards that match, aiming at a ring. Keep each with its own anchor object.
4 and 5 are a pair: the same low box-like object, the same crouching body, the same camera. Change the direction — a hand sweeping level across three parts, a hand diving down after keys. #4 has no keys; #5 has no dividers.
6 and 8 are both low to the floor: sitting among children with a ball, and sitting by a broken chair. Same floor line; #6 has three bodies, #8 one.
10 is a single.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-10 — images 91–100

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `beloven-aan-de-buur.png` — Dutch chunk: beloven aan (to promise).
   Scene: one person stands at a low fence holding up an open hand flat, palm out, as if making a vow; the neighbour on the far side nods and holds up their own hand. The two raised hands face each other.
   Must read: giving a promise to a neighbour.
   Avoid: a handshake (that is a deal); a written contract; a child.

2. `afhangen-van-de-bus.png` — Dutch chunk: afhangen van (to depend on).
   Scene: one person stands at a stop with a bag over the shoulder, looking down the empty road and checking a watch; nothing is arriving. Only the waiting is shown.
   Must read: depending on transport that may not come.
   Avoid: a bus arriving (that is the event, not the dependence); a phone; a second person.

3. `afhangen-van-het-weer.png` — Dutch chunk: afhangen van (to depend on).
   Scene: one person stands in the open doorway between inside and outside, one hand on the frame, looking up at a single cloud; behind them indoor furniture, in front an empty street.
   Must read: letting weather decide.
   Avoid: a person already under an umbrella; a weather symbol; two people.

4. `kijken-naar-de-klok.png` — Dutch chunk: kijken naar (to look at).
   Scene: one person stands with one hand on a wall-mounted clock, fingers near the hands, face turned up towards it; the clock face is blank apart from hands and tick marks. One figure.
   Must read: checking the time.
   Avoid: readable numbers; a queue.

5. `luisteren-naar-de-juf.png` — Dutch chunk: luisteren naar (to listen to).
   Scene: one person sits at a desk in front, chin on both hands, eyes fixed forward; a second figure stands facing the row with one hand raised. The seated listeners face the standing speaker.
   Must read: listening to a teacher.
   Avoid: a phone; a person asleep; a crowd at a rally.

6. `lijden-aan-hoofdpijn.png` — Dutch chunk: lijden aan (to suffer from).
   Scene: one person sits with both temples pressed between two palms, eyes closed tight, head low; a small plain cup and a lamp beside them. One figure, no bandage.
   Must read: ongoing pain.
   Avoid: a hospital bed; a thermometer with marks; a person frowning at another.

7. `genieten-van-de-maaltijd.png` — Dutch chunk: genieten van (to enjoy).
   Scene: one person sits at a table with a fork halfway to the mouth, eyes closed and an easy smile; the plate holds a simple round meal. One figure.
   Must read: savouring food.
   Avoid: a crowded restaurant; readable menus; a person eating with a neutral face.

8. `stoppen-met-roken.png` — Dutch chunk: stoppen met (to stop).
   Scene: one person stands outside a building with both hands in their pockets, deliberately turning away from two others who are smoking; no cigarette in their own hand.
   Must read: giving up a habit.
   Avoid: a person stubbing out a cigarette in an ashtray (used by the pilot); a crossed-out sign; a doctor.

9. `denken-aan-de-toekomst-van-het-kind.png` — Dutch chunk: denken aan (to think about).
   Scene: one adult stands with one hand on the shoulder of a child seen from behind, both looking out along a long empty path. No bubble; the path is the future.
   Must read: thinking of a child's future.
   Avoid: a thought bubble with a face; a school building with letters; a second adult.

10. `kijken-op-de-klok.png` — Dutch chunk: kijken op (to check the time on).
   Scene: the same wall clock as #4, same size and place; one person strides past below it in profile, bag on the shoulder, head turned up for a one-second glance. Both feet are mid-step and no hand touches the clock.
   Must read: a quick check of the time in passing.
   Avoid: a person studying the clock face (that is `kijken naar`); a person checking a wristwatch at a stop; a person running late.

CONTRAST PAIRS
2 and 3 are the same chunk on different things: transport and weather. Same camera at a road's edge; #2 has a bag and a watch, #3 has a door frame and a cloud. Neither may contain the other's prop.
4 and 10 are the same verb with two prepositions, and are the teaching point of this batch: `kijken naar` studies the clock's face, `kijken op` checks it in passing. Same clock shape, two postures.
1 and 9 are both `aan` frames with one adult and something carried forward: a raised palm across a fence, and a hand on a child's shoulder. Keep the child seen from behind in #9.
5, 6, 7 and 8 are singles. #8 must not use the pilot's ashtray image.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-11 — images 101–110

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `vechten-tegen-de-vermoeidheid.png` — Dutch chunk: vechten tegen (to fight against).
   Scene: one person sits at a desk with heavy eyes, one hand holding the head up by the chin, the other flat on the work. No second figure.
   Must read: struggling against sleepiness.
   Avoid: a person asleep in bed; a boxing ring; a coffee cup as the main mass.

2. `waarschuwen-voor-het-gevaar.png` — Dutch chunk: waarschuwen voor (to warn about).
   Scene: one person stands with one arm out to stop a second from stepping forward; ahead of them an open hole in the ground is drawn as a plain dark gap. The outstretched arm is the main shape.
   Must read: warning someone of danger.
   Avoid: a triangle warning sign with an exclamation mark; a car; a crowd.

3. `trots-zijn-op-de-afkomst.png` — Dutch chunk: trots zijn op (to be proud of).
   Scene: one person stands with a hand on an old family album open on the table, chin up, smiling; a simple house shape and a row of small figures on the page are loose strokes.
   Must read: pride in where you come from.
   Avoid: a flag; a passport with letters; a crowd.

4. `zich-vergissen-in-de-dag.png` — Dutch chunk: zich vergissen in (to be mistaken about).
   Scene: one person in a coat with a bag stands in an otherwise empty room with two empty chairs, one fingertip touching one square of a wall calendar while a heavy dot sits in the next square along; the head tilts, brow raised.
   Must read: arriving on the wrong day.
   Avoid: a person walking past the calendar; a person oversleeping in bed; readable dates or numbers.

5. `zich-schamen-over-de-fout.png` — Dutch chunk: zich schamen over (to be ashamed of).
   Scene: one person holds both hands over the face, elbows close, shoulders turned in; a second person beside them stands with arms loose, not angry. The hidden face is the idea.
   Must read: embarrassment about a mistake.
   Avoid: a person angry and pointing; a crossed-out sign; a crowd.

6. `helpen-bij-de-verhuizing-van-de-buren.png` — Dutch chunk: helpen bij (to help with).
   Scene: one person holds a door open with one arm while a second carries a box through, both leaning with the weight. The door is the main mass.
   Must read: helping neighbours move.
   Avoid: a moving van with a logo; a person unloading alone; money changing hands.

7. `onderhandelen-over-de-prijs.png` — Dutch chunk: onderhandelen over (to negotiate about).
   Scene: two people sit across a table, one with both palms up and leaning back, the other leaning in with one finger raised; a plain object sits between them. The energy between them is the idea.
   Must read: haggling over a price.
   Avoid: a counter with a menu; readable price tags; a calculator.

8. `denken-aan-een-andere-oplossing.png` — Dutch chunk: denken aan (to think of).
   Scene: one person stands over a broken shelf with a plain toolbox open at the feet, one finger on the chin; the broken piece lies beside, and the hand hovers over a single tool.
   Must read: finding another way to fix it.
   Avoid: two objects side by side (that reads as choosing); a light bulb; a second person.

9. `zich-voorbereiden-op-het-gesprek.png` — Dutch chunk: zich voorbereiden op (to prepare for).
   Scene: one person stands in front of a mirror frame, tying a knot at the throat, lips slightly moving as if rehearsing; the reflection is the same figure. One person, two shapes.
   Must read: practising before an important talk.
   Avoid: a speech bubble; a printed script; a second person.

10. `doorgaan-met-de-les.png` — Dutch chunk: doorgaan met (to continue with).
   Scene: one person stands at the front with an open book in one hand, the other pointing down at the book; two seated heads lean forward. The same session carrying on.
   Must read: carrying on with a lesson.
   Avoid: a person leaving the room; a clock; a person starting with a raised hand.

CONTRAST PAIRS
1 and 10 are both effort or persistence: a body fighting sleep at a desk, and a lesson carrying on. Same camera; #1 has one figure stooped, #10 has a speaker and two listeners.
2 and 6 are both an open arm between two people: one stops a neighbour at a hole, one holds a door for a neighbour carrying a box.
3 and 7 are both a table with an item held in common: a family album, and an object on the table being argued over.
4 and 5 are both a mistake the person now sees: a finger on the wrong square of a calendar, and a face hidden behind both hands.
8 and 9 are both single-figure rehearsal and repair: keep the toolbox low in #8 and the mirror upright in #9.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch B1-12 — images 111–120

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch verb plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

STYLE — DO NOT DEVIATE
- Bold brush-pen sketch in the hand of the Oefenpad logo: a wide-nib brush or
  chisel marker, thick pressure-varying strokes with dry-brush streaks and
  split bristles. Not pencil, fine-liner, flat vector, cartoon, stock,
  photorealistic, 3D or soft-shaded.
- Cobalt blue #2B50C8 only. No orange, red, green, second blue, grey, skin
  tone or full colour.
- Plain pure white background. No gradients, soft shading, stippling, drop
  shadows, glow, blur, grain, paper texture, border, frame, card or white
  plate.
- Contour plus hatching. Important edges are drawn twice, a few pixels off,
  and corners may stay open. At 784 px wide: most lines 4–8 px, boldest
  contours 9–14 px, hatching 2–4 px (at 1024 px wide: 5–10, 12–18, 3–5).
  Ink covers 14–22% of the canvas, up to 27% for a scene with two figures
  and furniture.
- Hatching is wanted: quick, dense, directional strokes on the shadow side of
  folds and under objects, with white paper still visible between them. Never
  cross-hatch.
- Fill hair only, plus one or two small accents. Clothing, furniture and
  background stay white inside the contour.
- One idea per image. The scene spans 90–100% of the width and the person
  35–55%; it may touch the left or right edge, with paper kept at top and
  bottom. Must still be nameable at 64×64 px.
- People have adult proportions, profile or three-quarter view, facing right:
  brow, one eye, nose line, mouth, ear, filled hair. Hands have a thumb and
  finger lines. No cartoon faces, open mouths or motion lines.
- No text, letters, numbers, words, logos, emoji, punctuation, arrows or
  readable signs. Signs and speech bubbles are blank shapes.
- No Dutch souvenir imagery: no windmills, clogs, tulips, canals or cheese.
- Posture and objects carry the meaning. If it needs a caption, simplify.

FORMAT
- Ten separate images, one per subject.
- 2:3 portrait, 1024×1536 px, same camera and scale across the ten.
- Raster PNG, no SVG, no contact sheet, no extra images.
- Return in numbered order. Put the filename in chat text, never inside the
  image.

THE TEN SUBJECTS

1. `scheiden-van-de-partner.png` — Dutch chunk: scheiden van (to separate from).
   Scene: two people stand apart with a gap of white between them, each holding one end of the same blank paper; their bodies turn away from each other. No anger, only distance.
   Must read: end of a relationship.
   Avoid: two wedding rings (they read as marriage); a lawyer; a child between them.

2. `deelnemen-aan-het-debat.png` — Dutch chunk: deelnemen aan (to take part in).
   Scene: one person stands at a table with a hand raised, speaking, facing three seated people who listen; a single blank bubble above the speaker. The raised hand and the seated three are the idea.
   Must read: joining a debate.
   Avoid: readable arguments on a board; an argument of shouting; a big crowd.

3. `geloven-in-de-liefde.png` — Dutch chunk: geloven in (to believe in).
   Scene: one person stands gesturing towards two people who hold hands, all three calm; the standing one has an open palm and a smile. The pair holding hands is the centre.
   Must read: belief in love between people.
   Avoid: a heart symbol; a wedding; a broken heart.

4. `zich-aanpassen-aan-het-klimaat.png` — Dutch chunk: zich aanpassen aan (to adapt to).
   Scene: one person in a heavy coat and scarf walks beside one in shirt sleeves, both on the same snowy street; the second is calm, the first hunched. Two figures, one street line.
   Must read: getting used to a cold place.
   Avoid: a thermometer; a weather map; a snowman.

5. `herinneren-aan-de-afspraak.png` — Dutch chunk: herinneren aan (to remind of).
   Scene: one person stands with a small blank card held up towards another, tapping it; the other's hand flies to the forehead in sudden recall. One card only.
   Must read: a reminder passed to someone.
   Avoid: a phone alarm; a person thinking alone (that is remembering); a calendar with numbers.

6. `zonnen-op-het-balkon.png` — Dutch chunk: zonnen op (to sunbathe on).
   Scene: one person lies back on a plain lounger, hands behind the head, eyes closed; a low railing line runs beside them and one sun ring above. One figure.
   Must read: relaxing on a balcony.
   Avoid: a beach with people; a sun with a face; a pool.

7. `hangen-aan-de-haak.png` — Dutch chunk: hangen aan (to hang on).
   Scene: a plain wall with a single heavy hook at head height; a coat hangs from it by its collar loop, sleeves slack and two short swing strokes at the hem, a bag strap on a lower hook beside it. A band of white lies between hem and floor; no person.
   Must read: a coat hanging on a hook.
   Avoid: a person putting the coat up; a mirror or a wardrobe; a coat lying on a chair.

8. `beginnen-bij-het-begin.png` — Dutch chunk: beginnen bij (to start at).
   Scene: one person stands at the first of a row of plain stepping stones, one foot lifted onto it, looking along the row towards a small building at the end.
   Must read: starting at the beginning.
   Avoid: a person at the far end; a staircase; a map with arrows.

9. `blijven-bij-de-afspraak.png` — Dutch chunk: blijven bij (to stick to).
   Scene: one person holds a plain folded paper and taps one spot on it twice with a fingertip, nodding firmly; a second person listens. One marked spot only, no lines of text.
   Must read: holding to what was agreed.
   Avoid: two papers side by side (that reads as choosing); a handshake; an argument.

10. `zich-schamen-voor-de-klas.png` — Dutch chunk: zich schamen voor (to be ashamed in front of).
   Scene: one person stands at the front with both hands behind the back and head bowed, one cheek drawn with a small round blush mark; three seated figures look on, drawn plain. No board, no text.
   Must read: embarrassment in front of a group.
   Avoid: a thought bubble; a teacher pointing; a crying face.

CONTRAST PAIRS
1 and 3 are both about love or belief between people: two turning apart, and two holding hands. Same camera and pair size; the gap versus the joined hands is the only change.
2 and 9 are both holding a position in front of a group: a raised hand in a debate, and an agreed paper tapped twice. #2 has three listeners; #9 has one.
4 and 6 are both one figure out in the open air: a snowy street, and a balcony in the sun. Same camera and one figure; keep the coat in #4 and the lounger in #6.
5 and 7 are both a small object held between two levels: a card held up, and a coat hanging from a hook. Neither may show a mirror or a wardrobe; #7 has nobody putting the coat up.
1 and 8 are both leaving one place for another: a relationship ending, and a first step onto a path. #8 looks along the path, #1 holds one end of a shared paper.
10 is the only frame here with a row of other people looking at the subject; keep them plain seated masses.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the preposition or the partner in the scene obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## After delivery

When the ten PNGs for a batch come back:

1. **Process the PNGs** as described in `game-art.md` under *Delivered raster
   art*: trim to the cobalt mass, keep the 2:3 frame, save into
   `assets/voorzetselpaden/` under the filename in this file, and build the
   alpha mask at 512 × 763.
2. **Add the scenes to `server/Oefenpad.Resources/Games/Data/prepositions.json`** — one scene per frame,
   with the Dutch chunk exactly as written in this file, the English gloss
   matching the tracker, and the frame filename.
3. **Wire the pair.** For a frame marked as a pair, point `contrast` at the
   partner filename. For a single, set `contrast` to `null`.
4. **Write a second `bouw` sentence** for every single. A pair already has two
   sentences to its credit, one on each half; a single needs a second sentence
   that uses the same chunk in a different situation, so the learner meets the
   preposition twice.
5. **Update the tracker.** Change `needed` to `drawn` in the Status column and
   write the delivery date beside it.
6. **Check at 64 px in the game.** Open the scene at thumbnail size in
   `client/src/games/prepositions/`; if the idea is no longer nameable, redraw the frame
   rather than adding a caption. Report the redraw in this file's tracker.

Nothing else in the plan changes. Frames that come back wrong can be redrawn
from the same subject text without touching the other nine in the batch.
