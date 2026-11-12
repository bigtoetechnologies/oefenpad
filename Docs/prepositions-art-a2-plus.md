# Voorzetselpaden — image plan, A2+

Status: planning document, 10 November 2026. This is the **A2+** band of the
image plan: the frames between the shipped A0–A2 set and the B1 verb band. It
covers roadmap batches 5–8 of `prepositions-roadmap.md`.

The plan was split on 10 November 2026. What used to be one 200-frame B1 file is
now two — **A2+** (this file, 80 frames, batches 5–8) and **B1**
(`prepositions-art-b1.md`, 120 frames, batches 9–13). Nothing was added or cut
in the split. The seam is the one the old file's own theme table already drew:
the spatial, adjective, noun and pronominal themes here, the verb chunks there.

Scope: **80 new frames**, planned as **8 self-contained Grok batches of ten**,
numbered A2+-01 to A2+-08. The artwork comes back as 80 separate 2:3 PNGs, one
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
- The **16 batch-4b frames** in `prepositions-art-a2-pairs.md`.
- The **120 B1 frames** in `prepositions-art-b1.md`.
- Free spatial and temporal use (`op tafel`, `in de kast`, `na de les`). That is
  grammar, not a chunk — see `prepositions-roadmap.md` §11.

No frame in this file repeats a pilot frame, an A0–A2 frame, a batch-4b frame,
a B1 frame or another frame in this file. Where a chunk that already has a pilot
image comes back, it does so in a visibly different situation and the tracker
says which; the chunk list deliberately stays broader than the pilot's twenty.

## How to use this file

Each batch section is a single fenced text block. Paste **one block at a time**
into Grok. Grok has no file access, so every block repeats the task, the style,
the format and its ten subjects; nothing outside the block is assumed and no
block depends on another having been sent first. Ask for the ten images, then
process the result as described in `game-art.md` under *Delivered raster art*
and ship at 512 × 763.

Two rules make the set teach rather than decorate:

- **Contrast before single.** Where two frames share a verb, adjective or noun
  and differ only in the preposition, they are a pair and are drawn in the same
  sitting: same camera, same scale, one meaningful difference. The pair is the
  thing that teaches, so a pair is kept inside one batch wherever the
  ten-frame rhythm allows it. Where a pair spans two batches the blocks say so,
  and the second half names its partner file.
- **Concrete over abstract.** A chunk like `rustig aan` or `eraan toe zijn` has
  no honest silhouette. Those frames get a concrete everyday situation, and the
  gloss carries the abstraction. The tracker column marks them `gloss-picture`.
  `prepositions-roadmap.md` §9 predicts this; this file is the honest version of
  it at A2+.

The house style is the bold brush-pen sketch defined in `game-art.md`: cobalt
`#2B50C8` only, wide-nib contour with directional hatching, 2:3 portrait, one
idea per image, no text. The prompts repeat those rules because the generator
cannot read `game-art.md`.

## What A2+ adds

Eighty frames in four themes. The spatial set, the core adjective chunks, the
core noun chunks and the pronominal group are speculative in the sense that the
repo has no frequency list. Re-cut any batch around a frequency list when one
arrives, per `prepositions-roadmap.md` §12.1; the art plan survives a re-cut
because each frame stands alone.

| Image batch | Theme | Frames | Roadmap batch |
|---|---|---|---|
| A2+-01 – A2+-02 | Spatial set: `tussen, onder, boven, naast, achter, langs` and `binnen, buiten, na, rond, vanaf` | 20 | 5 |
| A2+-03 – A2+-04 | Adjective + preposition, core | 20 | 6 |
| A2+-05 – A2+-06 | Noun + preposition, core | 20 | 7 |
| A2+-07 – A2+-08 | Pronominal adverbs, and the everyday chunks the set was missing | 20 | 8 |
| **Total** | | **80** | |

New prepositions governed as frames by the end of A2+: `tussen, onder, boven,
naast, achter, langs, binnen, buiten, na, rond, vanaf` on top of the ten shipped
and the five A2 ones. The roadmap's remaining core prepositions — `sinds,
tijdens, volgens, wegens, ondanks, behalve` from phase C onward — are not in
this file.

Sections:

- A2+-01 – A2+-02: the spatial set, two batches, 14 paired frames and 6 singles.
  The first batch fixes the axes — between, under, above, beside, behind,
  past/along, around, from; the second turns to the boundary and time words
  `binnen, buiten, na, rond, vanaf`, plus `om` and the extended `door`.
- A2+-03 – A2+-04: adjective chunks, 16 paired frames and 4 singles. A pair is
  the same adjective on two objects of feeling, or two prepositions on the same
  adjective stem; the singles are the ones the language has only once.
- A2+-05 – A2+-06: noun chunks, 14 paired frames and 6 singles. Here the noun
  carries the meaning and the preposition is fixed; pairs are the same noun on
  two situations, so the preposition is what the learner confirms.
- A2+-07 – A2+-08: pronominal adverbs (`er…`, `daar…`, `waar…`) in A2+-07, and
  in A2+-08 the high-frequency everyday chunks the whole set turned out to be
  missing (`hopen op`, `uitgeven aan`, `bellen met`, …). Twelve paired frames and
  eight singles. No letters appear in any frame: the situation and the person
  carry `erover`, `eraan`, `daar…aan`, `waar…naartoe`. A2+-08 was originally ten
  separable-prefix verbs; a separable
  verb governs no preposition, so on 10 November 2026 those ten and nineteen
  more elsewhere in the old B1 file were replaced and the prefix material moved
  to the **Uit Elkaar** game idea in `suggestions.md`.

### Chunk overlap with batch 4b

Three A2+-08 frames use a chunk that `prepositions-art-a2-pairs.md` already
draws in a different scene:

| A2+ frame | Batch 4b frame |
|---|---|
| `gaan-naar-het-werk.png` | `gaan-naar-gebouw.png` |
| `kiezen-voor-de-fiets.png` | `kiezen-voor-taart.png` |
| `betalen-voor-de-boodschappen.png` | `betalen-voor-kassa.png` |

Both plans agree that a frequent chunk is worth two scenes, because a chunk is
met in more than one situation. Batch 4b's `kiezen voor` scene is a cake taken
over an apple, with no vehicle of any kind, so only the chunk overlaps there and
the two drawings cannot be mistaken for each other. The other two pairs differ
only in place or object and are the ones to watch. But the two frames must not
end up in levels that the Klopt step confuses, and `prepositions-roadmap.md` §5
records that batch 8 "drops them and needs three replacements". Decide one of the
following before drawing A2+-08 and record it in the tracker:

1. Keep the second scenes and place each chunk in a level separate from its
   batch-4b partner. Costs nothing and needs no new art.
2. Drop the three A2+ rows and plan three replacements from the chunk lists in
   `prepositions-art-b1.md` and `prepositions-art-b1-plus.md`, keeping the band
   at 80 frames.
3. Point the three rows at the batch-4b scene and reuse that art, which turns
   them into documentation rather than new frames.

Until one is chosen the three rows stay `needed`, marked *same chunk as batch
4b*, and A2+-08 keeps its ten planned images.

Status values in the tracker: `needed` (not drawn), `drawn` (delivered and
processed), `gloss-picture` in the note column (see above).

## Tracker

All 80 frames, in batch order. The file column is the Grok filename and the
shipped scene id. "Pair/note" names the partner file for a pair, or `single`.

| # | File | Dutch frame | English | Scene | Pair/note | Status |
|---|---|---|---|---|---|---|
| 1 | `tussen-twee-mensen.png` | tussen | between | two people stand a step apart, facing the viewer; a third, smaller figure strides through the gap between them, one hand forward. The two are a gate; the third passes through it | Pair with `onder-de-tafel` | needed |
| 2 | `onder-de-tafel.png` | onder | under | a plain table seen from the side, legs visible; beneath it a cat sits upright, while a hand above the table holds a plate. The empty space under the table is where the cat sits | Pair with `tussen-twee-mensen` | needed |
| 3 | `boven-de-wolken.png` | boven | above | a small aeroplane, seen in profile and flying to the right, crosses the top of the frame; a flat band of rounded clouds runs below it. The gaps of white paper between plane and clouds carry the height | Pair with `naast-elkaar` | needed |
| 4 | `naast-elkaar.png` | naast | next to | two people sit side by side on a simple bench, both facing the viewer, shoulders level, an easy shared smile; one holds a cup. Their two outlines are the composition | Pair with `boven-de-wolken` | needed |
| 5 | `achter-het-hek.png` | achter | behind | a low garden fence runs across the lower third of the image; behind it, further back and drawn slightly smaller, a child waves with one arm raised. The fence is in front of the child | Pair with `achter-de-ander-aan` | needed |
| 6 | `achter-de-ander-aan.png` | achter … aan | following behind | two people walk in single file to the right, both seen from behind; the nearer one has just started, the far one is mid-stride ahead of them. A single loose ground stroke under their feet suggests the path | Pair with `achter-het-hek` | needed |
| 7 | `langs-het-huis-lopen.png` | langs | past | a simple house stands at the left edge; one person walks past it towards the right, still glancing back at the wall, body sideways to the door. The house is behind the walker, not in front | Pair with `langs-het-water-wandelen` | needed |
| 8 | `langs-het-water-wandelen.png` | langs | along | two people stroll along a winding path; on one side of the path runs a wavy line of water with a few short wave strokes. The pair walk parallel to the water, towards the top of the frame | Pair with `langs-het-huis-lopen` | needed |
| 9 | `rond-de-tafel-zitten.png` | rond | around | seen from slightly above, four people sit on chairs around a round table, each facing the middle, a large open book on it. The table is a circle; the people are evenly spaced | Single; positional `rond` | needed |
| 10 | `vanaf-de-brug-zien.png` | vanaf | from | a raised bridge deck is in the lower part of the frame; one person stands on it, leaning on the rail, looking down and out across a river; a small boat lies far below. The viewer looks with the person, from high to low | Single; `vanaf`, view from a point | needed |
| 11 | `binnen-onder-de-parasol.png` | binnen | inside, indoors | a tent or large parasol shape covers the upper half; underneath it a person sits cross-legged on a small mat, warm and settled, a cup beside them; rain falls outside the edges of the cover | Pair with `buiten-in-de-tuin` | needed |
| 12 | `buiten-in-de-tuin.png` | buiten | outside | the same cover as #1, same camera; now the person stands in the open beside it, on the grass, arms spread, no rain. A simple house wall with one window is the boundary behind them | Pair with `binnen-onder-de-parasol` | needed |
| 13 | `na-de-maaltijd.png` | na | after | a plain table with an empty plate, a used cup and crumpled napkin; one person pushes their chair back and pats their stomach, satisfied; nobody is eating | Single; temporal `na` | needed |
| 14 | `na-de-vergadering.png` | na | after | a meeting room, two people pushing their chairs back from a table; a third is already at the door with a coat over the arm. The table holds only a closed folder. Everyone is leaving | Single; temporal `na` | needed |
| 15 | `rond-etenstijd-thuis.png` | rond | around | a person comes through the front door, coat still on, bag in hand; behind them in the kitchen the oven glow is drawn as a small plain flame shape and a plain wall clock with hands but no numbers points to roughly seven. The arrival happens near that hour | Single; temporal `rond` | needed |
| 16 | `rond-de-stad-fietsen.png` | rond | around | seen from above, a person on a bicycle follows a large loop path drawn as one bold curved stroke; inside the loop sit three simple house roofs and a small tree shape. The path returns to where it started | Pair with `om-de-tafel-rennen` | needed |
| 17 | `vanaf-vandaag-stoppen.png` | vanaf vandaag | from today | a person stands with an open calendar page that is blank except for one heavy black dot at its top left; one hand is raised on the dot. Everything after it is paper. No numbers, no letters | Pair with `vanaf-de-eerste-dag` | needed |
| 18 | `vanaf-de-eerste-dag.png` | vanaf | from | an empty staircase rises from bottom left to top right; a person stands on the lowest step and looks up; on the top step, far away, sits a small chair. The distance is the idea | Pair with `vanaf-vandaag-stoppen` | needed |
| 19 | `om-de-tafel-rennen.png` | om | around | seen from above, a round table with four chairs; a child runs along a circular path drawn around the outside of the table, arms swinging. The table stays in the centre | Pair with `rond-de-stad-fietsen` | needed |
| 20 | `de-hele-dag-door-werken.png` | de hele dag door | all day long | one person at a desk, bent over a laptop, sleeves pushed up; behind them a tall wall clock with hands only, no numbers, and a window that shows a crescent moon at the top and a lifted sun shape lower down. The worker stays at the desk | Single; temporal `door` | needed |
| 21 | `trots-op-baan.png` | trots op | proud of | one person stands square to the viewer, chin up, one hand on the chest, a warm smile; beside them a simple framed certificate shape, blank, hung on a plain wall. The frame is plain, no letters | Pair with `trots-op-dochter` | needed |
| 22 | `trots-op-dochter.png` | trots op | proud of | same camera as #1; now the person stands to the left, one hand on the shoulder of a child at their side, both facing the viewer; the child holds a small plain medal. The pride points at the child | Pair with `trots-op-baan` | needed |
| 23 | `afhankelijk-van-auto.png` | afhankelijk van | dependent on | one person stands at the open bonnet of a small car, tools in hand and a worried posture, one hand on the bodywork; the car is the only vehicle and the road ahead is empty | Pair with `afhankelijk-van-weer` | needed |
| 24 | `afhankelijk-van-weer.png` | afhankelijk van | dependent on | one person at a plain window, forehead to the glass, looking out at rain; behind them a bicycle leans unused and a coat hangs with an umbrella beside it. The weather decides their day | Pair with `afhankelijk-van-auto` | needed |
| 25 | `gewend-aan-vroeg-opstaan.png` | gewend aan | used to | one person stands easily in a kitchen, stretching, a cup steaming on the counter, a wall clock with hands but no numbers showing the small hours; the posture is relaxed, not tired | Pair with `gewend-aan-kou` | needed |
| 26 | `gewend-aan-kou.png` | gewend aan | used to | one person outside in falling snow, coat open, scarf loose, hands relaxed at the sides, face calm; another person in the background is hunched and wrapped up, small. The contrast is the idea | Pair with `gewend-aan-vroeg-opstaan` | needed |
| 27 | `tevreden-met-resultaat.png` | tevreden met | satisfied with | one person leans back from a table, hands behind the head, looking at a large drawing on the table; a gentle smile. The drawing is plain, with only a few loose strokes | Pair with `klaar-met-studeren` | needed |
| 28 | `klaar-met-studeren.png` | klaar met | finished with | one person drops a heavy book onto a tall stack of books, one hand still pushing it down, the other lifting a cup; body turned away from the desk, done | Pair with `tevreden-met-resultaat` | needed |
| 29 | `ergens-goed-in-zijn.png` | goed in | good at | one person plays a guitar, fingers spread, relaxed and confident, a single musical curve of brush strokes rising from the instrument; nobody else in the frame | Single; gloss-picture | needed |
| 30 | `boos-over-de-rekening.png` | boos over | angry about | one person holds up a long paper receipt, frowning, one finger tapping it; the receipt is a blank strip with a ragged edge and no marks. No second person | Single; contrasts with shipped `boos op` | needed |
| 31 | `verliefd-op-persoon.png` | verliefd op | in love with | two people face each other close, one leaning in and smiling, hands nearly touching; a soft ring of short strokes around their heads. The other person smiles back | Pair with `jaloers-op-collega` | needed |
| 32 | `jaloers-op-collega.png` | jaloers op | jealous of | one person stands slightly turned away, arms crossed, sideways glance at a colleague who is showing a new phone to a third person; the jealous person is the largest figure and clearly left out | Pair with `verliefd-op-persoon` | needed |
| 33 | `bezorgd-over-de-toekomst.png` | bezorgd over | worried about | one person sits at a table with a blank letter and a pen, head lowered onto the palm, brow drawn as a single short line; a plain road shape continues out of the frame behind them, leading nowhere yet | Pair with `nieuwsgierig-naar-antwoord` | needed |
| 34 | `tevreden-met-huis.png` | tevreden met | satisfied with | one person stands in the doorway of a small plain house, one hand on the frame, looking back over the room inside with an easy smile; a suitcase sits closed by the door | Pair with `trots-op-huis` | needed |
| 35 | `verantwoordelijk-voor-team.png` | verantwoordelijk voor | responsible for | one person stands at the front of a small group of three seated colleagues, one arm open towards them; a plain clipboard is held in the other hand. The standing person is clearly the one who answers for them | Pair with `verantwoordelijk-voor-fout` | needed |
| 36 | `verantwoordelijk-voor-fout.png` | verantwoordelijk voor | responsible for | one person stands beside a fallen stack of papers on the floor, head lowered, one hand raised as if admitting it; nobody else in the room, but a plain door stands open behind them | Pair with `verantwoordelijk-voor-team` | needed |
| 37 | `nieuwsgierig-naar-antwoord.png` | nieuwsgierig naar | curious about | one person leans forward over a sealed envelope, both hands flat on the table around it, eyes wide; the envelope is plain with a blank flap | Pair with `bezorgd-over-de-toekomst` | needed |
| 38 | `trots-op-huis.png` | trots op | proud of | one person stands in front of a freshly built plain house, dusting off both hands, chest out and smiling; a ladder leans against the wall and a small paint pot sits by the door; the tool belt is still on | Pair with `tevreden-met-huis` | needed |
| 39 | `gewend-aan-de-drukte.png` | gewend aan | used to | one person stands calm at the centre of a busy street, arms relaxed; around them several smaller figures hurry in different directions with bags and phones; the calm figure is larger and still | Single; gloss-picture | needed |
| 40 | `kwaad-op-de-buurman.png` | kwaad op | angry at | one person stands on their side of a low fence, one hand raised and pointing across it; a second person on the far side turns away with a shrug. The fence separates them | Single; contrasts with shipped `boos op` | needed |
| 41 | `behoefte-aan-rust.png` | behoefte aan | need for | one person sits slumped on a simple chair, eyes closed, head back, shoes kicked off and a cup untouched beside them; the room is bare. There is only one figure and it is worn out | Pair with `behoefte-aan-een-pauze` | needed |
| 42 | `behoefte-aan-een-pauze.png` | behoefte aan | need for | one person stands with both hands pressed to their lower back, looking across the room at an open door with daylight beyond it; a closed laptop and a stack of folders sit on the desk behind them | Pair with `behoefte-aan-rust` | needed |
| 43 | `kans-op-regen.png` | kans op | chance of | one person at an open door, holding a small closed umbrella in one hand and squinting up at a large single cloud overhead; a bright empty stretch of pavement runs in front of them | Pair with `kans-op-werk` | needed |
| 44 | `kans-op-werk.png` | kans op | chance of | one person stands at a plain noticeboard where a single blank sheet hangs; they read it with one hand raised to the chin, hopeful; a small bag on the ground beside them | Pair with `kans-op-regen` | needed |
| 45 | `moeite-met-opstaan.png` | moeite met | difficulty with | one person sits on the edge of the bed with both hands on the mattress, pushing up slowly, one leg out; the posture shows effort, not injury. No clock | Pair with `moeite-met-namen-ontvangen` | needed |
| 46 | `moeite-met-namen-ontvangen.png` | moeite met | difficulty with | one person strains to lift one end of a long plank while a second person holds the other end, red-faced but wordless; bends in both knees; the plank is the main mass | Pair with `moeite-met-opstaan` | needed |
| 47 | `schaamte-over-de-fout.png` | schaamte over | shame over | one person stands with both hands in front of the face, shoulders drawn in and turned slightly away; on the table beside them a plain sheet lies face up with a single loose cross on it. No other person | Single; counterpart of `kritiek op` | needed |
| 48 | `honger-naar-eten.png` | honger naar | hunger for | one person sits at a table with an empty plate, fork raised, eyes on an open kitchen door through which a steaming pot shape is visible; the posture is eager and waiting | Single; noun + `naar` | needed |
| 49 | `zin-in-een-wandeling.png` | zin in | feel like | one person stands at the open door, one hand on the handle, looking out at a simple winding path with trees drawn only as trunks and round crowns; a coat on but unbuttoned | Single; same chunk as shipped `zin in` | needed |
| 50 | `gebrek-aan-tijd.png` | gebrek aan | lack of | one person runs while holding a pile of folders, one shoe half off, hair drawn as a single loose stroke swept back; a wall clock with hands but no numbers behind them, and the clock itself is small and plain | Single; noun + `aan` | needed |
| 51 | `kritiek-op-het-ontwerp.png` | kritiek op | criticism of | one person stands pointing at a large plain drawing on a wall, one finger up and a frown; a second person beside them listens with arms folded. The drawing is plain, marked only with a single loose cross | Pair with `vraag-om-hulp` | needed |
| 52 | `vraag-om-hulp.png` | vraag om | request for | one person holds out an open hand towards a neighbour; the neighbour hands over a ladder, both hands on the rungs. The ladder is the main mass | Pair with `kritiek-op-het-ontwerp` | needed |
| 53 | `vertrouwen-in-de-toekomst.png` | vertrouwen in | confidence in, trust | one person walks up a path towards a distant plain house, upright, unhurried, a bag on their shoulder; the path is one broad stroke from bottom to a point on the horizon. No worry in the body | Pair with `vertrouwen-in-de-baas` | needed |
| 54 | `vertrouwen-in-de-baas.png` | vertrouwen in | trust in a person | two people shake hands firmly, both standing square and looking at each other, smiles easy; the nearer handshake is the centre of the image. No documents | Pair with `vertrouwen-in-de-toekomst` | needed |
| 55 | `oplossing-voor-het-probleem.png` | oplossing voor | solution to | one person at a table with a broken bicycle wheel in front of them; both hands are raised in a satisfied gesture, and a small plain tool lies beside the wheel. A single clean loose stroke connects the broken part to the tool | Pair with `voorbereiding-op-het-examen` | needed |
| 56 | `voorbereiding-op-het-examen.png` | voorbereiding op | preparation for | one person sits at a desk with an open book, a pile of notes and a pen, focused; a plain wall calendar beside them with one day marked by a black dot and no numbers | Pair with `oplossing-voor-het-probleem` | needed |
| 57 | `gevolg-van-de-val.png` | gevolg van | consequence of | a person sits on the ground with one leg stretched out and one hand on a swollen ankle; a plain bicycle lies on its side a couple of steps away. The fall and its result are in one image | Pair with `schuld-aan-de-buurman` | needed |
| 58 | `schuld-aan-de-buurman.png` | schuld aan | blame for | one person points a thumb back at themselves while looking down, then a second person beside them points at them too; a broken flower pot lies on the ground between them. No speech bubbles | Pair with `gevolg-van-de-val` | needed |
| 59 | `tijd-voor-een-pauze.png` | tijd voor | time for | one person sets a cup down on a table and pushes the laptop lid closed with the other hand, stretching; a plain clock with hands and tick marks but no numbers stands on the desk | Single; noun + `voor` | needed |
| 60 | `schrik-van-het-geluid.png` | schrik van | fright at | one person jumps back with both hands raised, eyes wide, mouth a short open line; in front of them a plain loudspeaker on a stand with three short strokes of sound leaving it. Only one figure | Single; contrasts with shipped `bang voor` | needed |
| 61 | `ergens-naar-toe-gaan.png` | ergens naartoe | to somewhere | one person walks towards a small plain building in the middle distance, back to the viewer, one hand holding a bag; a single broad path sweeps from the bottom edge to the door | Pair with `ergens-vandaan-komen` | needed |
| 62 | `ergens-vandaan-komen.png` | ergens vandaan | from somewhere | one person has just come out of a doorway on the left and is now walking towards the viewer, one hand shielding their eyes; the open door is behind them, the path ahead is empty | Pair with `ergens-naar-toe-gaan` | needed |
| 63 | `ergens-mee-bezig-zijn.png` | ergens mee bezig | busy with | one person is halfway inside a cupboard, one arm reaching, a second arm holding a cloth; the cupboard door hangs open. Nothing else in the room | Single; `er…mee` | needed |
| 64 | `daar-komt-hij-aan.png` | daar komt hij aan | here he comes | one person stands waiting on a pavement, one hand raised in greeting, smile; a second person approaches in the distance on a bicycle, drawn small. The near figure looks towards the arriving one | Single; `daar…aan` | needed |
| 65 | `daar-gaat-het-over.png` | daar gaat het over | that is what it's about | two people sit at a table, one holding up a plain square card; the other leans in, pointing at the card. Both speech bubbles are blank and small. The card is the topic | Single; `daar…over` | needed |
| 66 | `waar-ga-je-naartoe.png` | waar … naartoe | where to | one person stands at a crossroads drawn as a bold branching stroke; a second person beside them points at one branch and raises the eyebrows. A bag on the ground. No signs | Pair with `waar-kom-je-vandaan` | needed |
| 67 | `waar-kom-je-vandaan.png` | waar … vandaan | where from | one person stands over a suitcase that is still open on the floor, one hand on the lid, looking up at a second person who is asking; the second person's palms are open | Pair with `waar-ga-je-naartoe` | needed |
| 68 | `er-is-nog-tijd-voor.png` | er is nog tijd voor | there is still time for | one person sits at a table and pushes back a plate; a plain clock with hands and no numbers stands beside them, and one hand of the clock is still well before the top; the person smiles and lifts a cup | Single; `er…voor` | needed |
| 69 | `erover-nadenken.png` | erover nadenken | think it over | one person sits at a table with a large plain card flat in front of them, chin on one hand, eyes on the card; a small blank thought bubble drifts above. Only one option on the table | Single; `er…over`, distinct from shipped `denken over` | needed |
| 70 | `eraan-toe-zijn.png` | eraan toe zijn | to be ready for it, to need it | one person sits heavily on a simple chair, bag still on the shoulder and coat still on, head tipped back, eyes half closed; the whole posture says that rest is overdue | Single; `er…aan toe`; gloss-picture | needed |
| 71 | `gaan-naar-het-werk.png` | gaan naar | to go to | a tall plain block of window squares stands at the left edge; one person in profile strides away from it to the right, bag over the shoulder, towards a low flat-roofed building at the far right edge. One broad ground stroke joins the two buildings | Pair with `wonen-in-een-flat`; same block and camera, figure outside and moving — same chunk as batch 4b (`gaan-naar-gebouw`); see *Chunk overlap with batch 4b*. | needed |
| 72 | `wonen-in-een-flat.png` | wonen in | to live in | the same tall block of window squares, now filling the left two-thirds of the frame; one window is open and a person leans out on both elbows, a small plant pot on the sill. Every other window is plain and closed | Pair with `gaan-naar-het-werk`; same block and camera, figure inside and staying | needed |
| 73 | `kiezen-voor-de-fiets.png` | kiezen voor | to choose, to opt for | one person stands front-on between a bicycle on the left and a small plain car on the right, both the same size; one hand grips the bicycle handlebar and the body turns towards it. The car stands empty and the bicycle's front wheel already points away | Pair with `twijfelen-tussen-twee-jassen`; here one hand grips, there the hand hangs in mid-air — same chunk as batch 4b (`kiezen-voor-taart`), a different scene; see *Chunk overlap with batch 4b*. | needed |
| 74 | `twijfelen-tussen-twee-jassen.png` | twijfelen tussen | to waver between | one person stands front-on between two coats hanging on two wall pegs, the same size on each side; one hand hovers in mid-air between them, a finger on the chin of the other, head tilted. Neither coat is touched | Pair with `kiezen-voor-de-fiets`; same camera and layout, hand off both objects | needed |
| 75 | `hopen-op-goed-nieuws.png` | hopen op | to hope for | one person stands at a small hall table beside the front door, hands clasped under the chin, one hand with crossed fingers raised; a single thin envelope is dropping through the letterbox. The table is bare and the face is bright | Pair with `zich-zorgen-maken-over-de-rekening`; same door, hall table and camera | needed |
| 76 | `zich-zorgen-maken-over-de-rekening.png` | zich zorgen maken over | to worry about | the same hall table and door; now three thick envelopes are piled on the table beside a flat, empty open purse with two coins. The person stands hunched, one hand pressed to the stomach and the other to the forehead | Pair with `hopen-op-goed-nieuws`; swap the thin envelope for the pile | needed |
| 77 | `betalen-voor-de-boodschappen.png` | betalen voor | to pay for | one person stands at the end of a plain counter, an open palm held out over it with a small stack of coins; on the counter a paper bag with a long loaf and a bottle neck sticking out. A bare hand enters from the frame edge, palm up, to receive | Pair with `uitgeven-aan-de-huur`; same counter and handful of coins, food on the counter — same chunk as batch 4b (`betalen-voor-kassa`); see *Chunk overlap with batch 4b*. | needed |
| 78 | `uitgeven-aan-de-huur.png` | uitgeven aan | to spend on | the same counter and the same person, with the same held-out handful of coins; on the counter, where the bag was, stands a small simple house shape with one door and one window, and a bigger stack of coins is already gone from the palm | Pair with `betalen-voor-de-boodschappen`; swap the food bag for the small house shape | needed |
| 79 | `vertrouwen-op-een-collega.png` | vertrouwen op | to rely on | one person in a coat with a bag at the door, one open hand raised in a relaxed goodbye, shoulders loose; behind them a colleague sits at a desk piled with folders and lifts a hand back. The leaver does not look worried | Single. Relying on someone who carries on while you go | needed |
| 80 | `bellen-met-de-huisarts.png` | bellen met | to be on the phone with | one person stands at a table with an old-fashioned handset to one ear, the other hand raised, a coiled cord looping down; the cord runs across the lower frame to the right where a smaller figure with a loop of stethoscope round the neck holds a matching handset, head tilted, listening. Both are on their own side of white space | Single. The cord gives the far end of the call | needed |

## Batch A2+-01 — images 1–10

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `tussen-twee-mensen.png` — Dutch chunk: tussen (between).
   Scene: two people stand a step apart, facing the viewer; a third, smaller figure strides through the gap between them, one hand forward. The two are a gate; the third passes through it.
   Must read: one person walking between two others.
   Avoid: someone peeking from behind a wall or doorway; three people side by side walking the same way; a crowd.

2. `onder-de-tafel.png` — Dutch chunk: onder (under).
   Scene: a plain table seen from the side, legs visible; beneath it a cat sits upright, while a hand above the table holds a plate. The empty space under the table is where the cat sits.
   Must read: the cat is underneath the table.
   Avoid: a cat on the table top; a cat climbing the leg; a floor mat or rug.

3. `boven-de-wolken.png` — Dutch chunk: boven (above).
   Scene: a small aeroplane, seen in profile and flying to the right, crosses the top of the frame; a flat band of rounded clouds runs below it. The gaps of white paper between plane and clouds carry the height.
   Must read: a plane flying above the clouds.
   Avoid: a bird; a plane on a runway; a person pointing up.

4. `naast-elkaar.png` — Dutch chunk: naast (next to).
   Scene: two people sit side by side on a simple bench, both facing the viewer, shoulders level, an easy shared smile; one holds a cup. Their two outlines are the composition.
   Must read: two people sitting next to each other.
   Avoid: people facing each other talking (that is opposite); a person alone; a sofa or living room.

5. `achter-het-hek.png` — Dutch chunk: achter (behind).
   Scene: a low garden fence runs across the lower third of the image; behind it, further back and drawn slightly smaller, a child waves with one arm raised. The fence is in front of the child.
   Must read: someone standing behind a fence.
   Avoid: a person leaning on the fence in front of it; a wall with a window; a garden with plants.

6. `achter-de-ander-aan.png` — Dutch chunk: achter … aan (following behind).
   Scene: two people walk in single file to the right, both seen from behind; the nearer one has just started, the far one is mid-stride ahead of them. A single loose ground stroke under their feet suggests the path.
   Must read: one person walking behind another.
   Avoid: a race or running; a queue standing still; a person hiding.

7. `langs-het-huis-lopen.png` — Dutch chunk: langs (past).
   Scene: a simple house stands at the left edge; one person walks past it towards the right, still glancing back at the wall, body sideways to the door. The house is behind the walker, not in front.
   Must read: walking past a building.
   Avoid: a person entering the door; a person standing still in front of the house; a street with several houses.

8. `langs-het-water-wandelen.png` — Dutch chunk: langs (along).
   Scene: two people stroll along a winding path; on one side of the path runs a wavy line of water with a few short wave strokes. The pair walk parallel to the water, towards the top of the frame.
   Must read: walking alongside water.
   Avoid: people swimming; a boat; a bridge.

9. `rond-de-tafel-zitten.png` — Dutch chunk: rond (around).
   Scene: seen from slightly above, four people sit on chairs around a round table, each facing the middle, a large open book on it. The table is a circle; the people are evenly spaced.
   Must read: a group seated around a round table.
   Avoid: a meeting with a speaker at the head (that is at the front); a square table with people on one side; a dining plate.

10. `vanaf-de-brug-zien.png` — Dutch chunk: vanaf (from).
    Scene: a raised bridge deck is in the lower part of the frame; one person stands on it, leaning on the rail, looking down and out across a river; a small boat lies far below. The viewer looks with the person, from high to low.
    Must read: a view from the top of a bridge.
    Avoid: a person on the bank looking up at the bridge; a person jumping; a person on a bus (that reads as getting off).

CONTRAST PAIRS
1 and 2 are a positional pair: same camera and scale, vertical space. In #1 the gap is between two upright bodies; in #2 it is under a horizontal surface. #1 must not read as two people standing in front of someone, #2 must not read as a person crawling.
3 and 4 are a pair on the vertical axis: above and beside. Same camera. #3 is landscape and horizontal, #4 is portrait and vertical, so the two are distinguishable at 64 px.
5 and 6 are a pair on the depth axis behind a person. Same camera and scale. In #5 the fence is nearer the viewer than the child; in #6 the nearer walker is nearer than the far walker and both face away.
7 and 8 are both `langs`, and are the pair that matters most in this batch: #7 crosses an object, #8 runs alongside one. Draw them with the same walking figures and the same ground line; change only the crossing versus the parallel relation.
9 and 10 are singles.

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

## Batch A2+-02 — images 11–20

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `binnen-onder-de-parasol.png` — Dutch chunk: binnen (inside, indoors).
   Scene: a tent or large parasol shape covers the upper half; underneath it a person sits cross-legged on a small mat, warm and settled, a cup beside them; rain falls outside the edges of the cover.
   Must read: a person sheltered indoors or under cover.
   Avoid: a person under an open umbrella standing (that is a different chunk, protected against the rain); a person at a window; a hot summer scene.

2. `buiten-in-de-tuin.png` — Dutch chunk: buiten (outside).
   Scene: the same cover as #1, same camera; now the person stands in the open beside it, on the grass, arms spread, no rain. A simple house wall with one window is the boundary behind them.
   Must read: a person is outdoors.
   Avoid: someone standing under the cover (that is #1); a garden with flowers; a bench and a terrace.

3. `na-de-maaltijd.png` — Dutch chunk: na (after).
   Scene: a plain table with an empty plate, a used cup and crumpled napkin; one person pushes their chair back and pats their stomach, satisfied; nobody is eating.
   Must read: the meal is already over.
   Avoid: a full plate or food being eaten (that is during); a clock; dishes being washed.

4. `na-de-vergadering.png` — Dutch chunk: na (after).
   Scene: a meeting room, two people pushing their chairs back from a table; a third is already at the door with a coat over the arm. The table holds only a closed folder. Everyone is leaving.
   Must read: people leaving a meeting that has ended.
   Avoid: people still seated and listening; a whiteboard with readable marks; a party.

5. `rond-etenstijd-thuis.png` — Dutch chunk: rond (around).
   Scene: a person comes through the front door, coat still on, bag in hand; behind them in the kitchen the oven glow is drawn as a small plain flame shape and a plain wall clock with hands but no numbers points to roughly seven. The arrival happens near that hour.
   Must read: arriving home roughly at dinner time.
   Avoid: readable numbers or times; a person asleep; a person eating at a table (that is during).

6. `rond-de-stad-fietsen.png` — Dutch chunk: rond (around).
   Scene: seen from above, a person on a bicycle follows a large loop path drawn as one bold curved stroke; inside the loop sit three simple house roofs and a small tree shape. The path returns to where it started.
   Must read: riding a loop around a town.
   Avoid: a straight road; a bicycle race with a finish line; a rider standing still.

7. `vanaf-vandaag-stoppen.png` — Dutch chunk: vanaf vandaag (from today).
   Scene: a person stands with an open calendar page that is blank except for one heavy black dot at its top left; one hand is raised on the dot. Everything after it is paper. No numbers, no letters.
   Must read: counting from this day onwards.
   Avoid: a wristwatch; a date with numbers; a start line for a race.

8. `vanaf-de-eerste-dag.png` — Dutch chunk: vanaf (from).
   Scene: an empty staircase rises from bottom left to top right; a person stands on the lowest step and looks up; on the top step, far away, sits a small chair. The distance is the idea.
   Must read: starting from the very bottom.
   Avoid: a person descending; a person at the top; a mountain with a flag.

9. `om-de-tafel-rennen.png` — Dutch chunk: om (around).
   Scene: seen from above, a round table with four chairs; a child runs along a circular path drawn around the outside of the table, arms swinging. The table stays in the centre.
   Must read: running around the table.
   Avoid: a person sitting at the table (that is seated around); a person running on a straight track; a gift being handed over (that is a different `om` chunk).

10. `de-hele-dag-door-werken.png` — Dutch chunk: de hele dag door (all day long).
    Scene: one person at a desk, bent over a laptop, sleeves pushed up; behind them a tall wall clock with hands only, no numbers, and a window that shows a crescent moon at the top and a lifted sun shape lower down. The worker stays at the desk.
    Must read: working through the whole day.
    Avoid: a person asleep; numbers or readable time; a coffee break with others.

CONTRAST PAIRS
1 and 2 are a pair: same tent or parasol, same camera, same ground line. Change only whether the person is under the cover or out in the open, and the rain. At 64 px the cover must be the obvious difference, and neither may read as the other.
3 and 4 are both `na`: same idea of "after", two different events. Draw them as situations, not as copies; #3 has one person and a table, #4 has three people and a door.
5 and 7 are both temporal and both use one marked point in time; keep them apart by object (a clock on a wall versus a calendar page with a dot).
6 and 9 are both `rond`/`om` loops seen from above; use the same camera and the same bold loop stroke, but a bicycle in #6 and a running child in #9, around a roof group in one and a table in the other.
8 and 10 are singles.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the temporal or spatial relation obvious from the layout, not from a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check the pairs side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch A2+-03 — images 21–30

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch adjective plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `trots-op-baan.png` — Dutch chunk: trots op (proud of).
   Scene: one person stands square to the viewer, chin up, one hand on the chest, a warm smile; beside them a simple framed certificate shape, blank, hung on a plain wall. The frame is plain, no letters.
   Must read: pride in an achievement.
   Avoid: a person looking at another person (that is proud of someone); a trophy cup as the main mass; a crowd.

2. `trots-op-dochter.png` — Dutch chunk: trots op (proud of).
   Scene: same camera as #1; now the person stands to the left, one hand on the shoulder of a child at their side, both facing the viewer; the child holds a small plain medal. The pride points at the child.
   Must read: pride in another person.
   Avoid: a certificate on the wall (that is #1); a graduation cap with tassel detail and a motto; a party.

3. `afhankelijk-van-auto.png` — Dutch chunk: afhankelijk van (dependent on).
   Scene: one person stands at the open bonnet of a small car, tools in hand and a worried posture, one hand on the bodywork; the car is the only vehicle and the road ahead is empty.
   Must read: depending on a machine to get anywhere.
   Avoid: a bus stop; a person waiting at a garage counter; a bicycle.

4. `afhankelijk-van-weer.png` — Dutch chunk: afhankelijk van (dependent on).
   Scene: one person at a plain window, forehead to the glass, looking out at rain; behind them a bicycle leans unused and a coat hangs with an umbrella beside it. The weather decides their day.
   Must read: plans that depend on the weather.
   Avoid: a person already wearing the coat and going out; a weather map with symbols; a phone app.

5. `gewend-aan-vroeg-opstaan.png` — Dutch chunk: gewend aan (used to).
   Scene: one person stands easily in a kitchen, stretching, a cup steaming on the counter, a wall clock with hands but no numbers showing the small hours; the posture is relaxed, not tired.
   Must read: an early start that is now routine.
   Avoid: a person yawning in bed; numbers on the clock; a sunrise over a landscape.

6. `gewend-aan-kou.png` — Dutch chunk: gewend aan (used to).
   Scene: one person outside in falling snow, coat open, scarf loose, hands relaxed at the sides, face calm; another person in the background is hunched and wrapped up, small. The contrast is the idea.
   Must read: someone accustomed to cold.
   Avoid: a person shivering (that is not used to it); a snowy landscape with trees; a snowman.

7. `tevreden-met-resultaat.png` — Dutch chunk: tevreden met (satisfied with).
   Scene: one person leans back from a table, hands behind the head, looking at a large drawing on the table; a gentle smile. The drawing is plain, with only a few loose strokes.
   Must read: pleased with the result of work.
   Avoid: a person frowning at the work; a celebration with others; readable plans or charts.

8. `klaar-met-studeren.png` — Dutch chunk: klaar met (finished with).
   Scene: one person drops a heavy book onto a tall stack of books, one hand still pushing it down, the other lifting a cup; body turned away from the desk, done.
   Must read: finished with study.
   Avoid: a person reading on; a graduation with a hat and readable banner; a library shelf.

9. `ergens-goed-in-zijn.png` — Dutch chunk: goed in (good at).
   Scene: one person plays a guitar, fingers spread, relaxed and confident, a single musical curve of brush strokes rising from the instrument; nobody else in the frame.
   Must read: skilful at something.
   Avoid: a music stand with readable notes; a stage and audience; a person frowning at the instrument.

10. `boos-over-de-rekening.png` — Dutch chunk: boos over (angry about).
    Scene: one person holds up a long paper receipt, frowning, one finger tapping it; the receipt is a blank strip with a ragged edge and no marks. No second person.
    Must read: angry about a bill or a situation.
    Avoid: a cashier or a queue; readable prices or numbers; a red stamp shape.

CONTRAST PAIRS
1 and 2 are a pair: same person, same camera. Change only the object of pride — a blank wall certificate versus a child at the side. At 64 px the second figure must be obvious in #2.
3 and 4 are a pair: same person, same camera distance, opposite postures of dependence — a broken thing in front of them versus weather beyond a window.
5 and 6 are a pair: the same calm posture of routine, with the early hour versus the cold as the difference. Same camera and scale; #6 adds the second, hunched figure as the visual counterweight.
7 and 8 are a contrast on `klaar` and on the mood of finishing: #7 is pleased with the thing, #8 is finished and leaving it. Make the posture the difference, not the objects.
9 and 10 are singles.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Does the posture carry the feeling, rather than a symbol?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch A2+-04 — images 31–40

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch adjective plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `verliefd-op-persoon.png` — Dutch chunk: verliefd op (in love with).
   Scene: two people face each other close, one leaning in and smiling, hands nearly touching; a soft ring of short strokes around their heads. The other person smiles back.
   Must read: romantic feelings for someone.
   Avoid: a heart with an arrow or readable symbols; a wedding ring; a party.

2. `jaloers-op-collega.png` — Dutch chunk: jaloers op (jealous of).
   Scene: one person stands slightly turned away, arms crossed, sideways glance at a colleague who is showing a new phone to a third person; the jealous person is the largest figure and clearly left out.
   Must read: jealousy of another person.
   Avoid: an argument; a gift; someone crying.

3. `bezorgd-over-de-toekomst.png` — Dutch chunk: bezorgd over (worried about).
   Scene: one person sits at a table with a blank letter and a pen, head lowered onto the palm, brow drawn as a single short line; a plain road shape continues out of the frame behind them, leading nowhere yet.
   Must read: worry about what is coming.
   Avoid: a person crying; readable documents; a clock.

4. `tevreden-met-huis.png` — Dutch chunk: tevreden met (satisfied with).
   Scene: one person stands in the doorway of a small plain house, one hand on the frame, looking back over the room inside with an easy smile; a suitcase sits closed by the door.
   Must read: content with a home, settled.
   Avoid: a person packing to leave; a large villa; a crowd.

5. `verantwoordelijk-voor-team.png` — Dutch chunk: verantwoordelijk voor (responsible for).
   Scene: one person stands at the front of a small group of three seated colleagues, one arm open towards them; a plain clipboard is held in the other hand. The standing person is clearly the one who answers for them.
   Must read: being the one in charge of a group.
   Avoid: a person handing out paperwork to one other; a teacher at a blackboard (that is teaching); readable charts.

6. `verantwoordelijk-voor-fout.png` — Dutch chunk: verantwoordelijk voor (responsible for).
   Scene: one person stands beside a fallen stack of papers on the floor, head lowered, one hand raised as if admitting it; nobody else in the room, but a plain door stands open behind them.
   Must read: owning up to a mistake.
   Avoid: a person angry at someone; a broken window; readable papers.

7. `nieuwsgierig-naar-antwoord.png` — Dutch chunk: nieuwsgierig naar (curious about).
   Scene: one person leans forward over a sealed envelope, both hands flat on the table around it, eyes wide; the envelope is plain with a blank flap.
   Must read: wanting to know what is inside.
   Avoid: the envelope already open; a person yawning; a hand pulling out a letter.

8. `trots-op-huis.png` — Dutch chunk: trots op (proud of).
   Scene: one person stands in front of a freshly built plain house, dusting off both hands, chest out and smiling; a ladder leans against the wall and a small paint pot sits by the door; the tool belt is still on.
   Must read: pride in something you made.
   Avoid: a certificate (that is #1 in the previous batch); a builder crew; a for-sale sign with letters.

9. `gewend-aan-de-drukte.png` — Dutch chunk: gewend aan (used to).
   Scene: one person stands calm at the centre of a busy street, arms relaxed; around them several smaller figures hurry in different directions with bags and phones; the calm figure is larger and still.
   Must read: someone at ease in a busy place.
   Avoid: a person covering their ears or holding their head; a traffic jam with cars; readable street signs.

10. `kwaad-op-de-buurman.png` — Dutch chunk: kwaad op (angry at).
    Scene: one person stands on their side of a low fence, one hand raised and pointing across it; a second person on the far side turns away with a shrug. The fence separates them.
    Must read: anger at a neighbour.
    Avoid: a fight; a broken window (that is anger about a thing); a wall with a drill.

CONTRAST PAIRS
1 and 2 are the same `op` with two feelings: a warm attachment to a person, and a resentful one at a colleague. Same camera and two figures; #1 leans in smiling, #2 stands turned away with arms folded.
3 and 7 are the worry/curiosity pair: both lean forward into the unknown. #3 is still and heavy, #7 is eager and open. Same camera and scale.
4 and 9 are both `tevreden met` and `gewend aan`: being at ease with what is around you. #4 is a house, #9 is a busy street; keep the posture relaxed in both.
5 and 6 are both `verantwoordelijk voor`: one is standing for a team, one is standing for a mistake. Use the same standing figure and the same camera; change only the group beside them versus the mess behind them.
8 and 10 are singles: pride in a home, and anger at a neighbour.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Does the posture carry the feeling, rather than a symbol?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch A2+-05 — images 41–50

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch noun plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `behoefte-aan-rust.png` — Dutch chunk: behoefte aan (need for).
   Scene: one person sits slumped on a simple chair, eyes closed, head back, shoes kicked off and a cup untouched beside them; the room is bare. There is only one figure and it is worn out.
   Must read: a plain need for rest.
   Avoid: a bed and sleepwear (that is differently read as going to bed); a doctor; a checklist.

2. `behoefte-aan-een-pauze.png` — Dutch chunk: behoefte aan (need for).
   Scene: one person stands with both hands pressed to their lower back, looking across the room at an open door with daylight beyond it; a closed laptop and a stack of folders sit on the desk behind them.
   Must read: a strong need for a break.
   Avoid: a person packing up and leaving (that is finished with); a beach or holiday postcard; a clock.

3. `kans-op-regen.png` — Dutch chunk: kans op (chance of).
   Scene: one person at an open door, holding a small closed umbrella in one hand and squinting up at a large single cloud overhead; a bright empty stretch of pavement runs in front of them.
   Must read: weather that may turn.
   Avoid: someone dry under an umbrella in the rain; a weather chart with symbols; several clouds filling the sky.

4. `kans-op-werk.png` — Dutch chunk: kans op (chance of).
   Scene: one person stands at a plain noticeboard where a single blank sheet hangs; they read it with one hand raised to the chin, hopeful; a small bag on the ground beside them.
   Must read: a possible job opening.
   Avoid: a job interview with a desk and two people (that is later in the process); a readable noticeboard.

5. `moeite-met-opstaan.png` — Dutch chunk: moeite met (difficulty with).
   Scene: one person sits on the edge of the bed with both hands on the mattress, pushing up slowly, one leg out; the posture shows effort, not injury. No clock.
   Must read: finding it hard to get up in the morning.
   Avoid: a person stretching happily (that is used to it); a person asleep; a hospital.

6. `moeite-met-namen-ontvangen.png` — Dutch chunk: moeite met (difficulty with).
   Scene: one person strains to lift one end of a long plank while a second person holds the other end, red-faced but wordless; bends in both knees; the plank is the main mass.
   Must read: struggling to carry something with someone else.
   Avoid: a person lifting alone with ease; a forklift; a broken plank.

7. `schaamte-over-de-fout.png` — Dutch chunk: schaamte over (shame over).
   Scene: one person stands with both hands in front of the face, shoulders drawn in and turned slightly away; on the table beside them a plain sheet lies face up with a single loose cross on it. No other person.
   Must read: embarrassment about a mistake.
   Avoid: a person crying loudly; anger at someone; readable documents or grades.

8. `honger-naar-eten.png` — Dutch chunk: honger naar (hunger for).
   Scene: one person sits at a table with an empty plate, fork raised, eyes on an open kitchen door through which a steaming pot shape is visible; the posture is eager and waiting.
   Must read: real hunger before a meal.
   Avoid: a full plate being eaten; a supermarket; a person looking at a menu with letters.

9. `zin-in-een-wandeling.png` — Dutch chunk: zin in (feel like).
   Scene: one person stands at the open door, one hand on the handle, looking out at a simple winding path with trees drawn only as trunks and round crowns; a coat on but unbuttoned.
   Must read: feeling like a walk.
   Avoid: a coffee cup (used by the pilot); a person already far along the path; rain.

10. `gebrek-aan-tijd.png` — Dutch chunk: gebrek aan (lack of).
    Scene: one person runs while holding a pile of folders, one shoe half off, hair drawn as a single loose stroke swept back; a wall clock with hands but no numbers behind them, and the clock itself is small and plain.
    Must read: not enough time.
    Avoid: numbers or readable times; a person sitting calmly; a traffic jam.

CONTRAST PAIRS
1 and 2 are the same chunk, `behoefte aan`, twice: a body that has run out, and a back that needs a break from work. Same camera and one figure; #1 is slumped and still, #2 is upright and looking at a door.
3 and 4 are the same chunk, `kans op`, an open possibility: a cloud overhead and an umbrella in the hand, versus a noticeboard with one blank sheet. In both the figure looks up or out; the umbrella of #3 must not appear in #4.
5 and 6 are both `moeite met`: effort in a body, and effort in a load. Same camera; #5 is one figure and a bed, #6 is two figures and a plank. Show the effort in the posture, not in sweat drops or strain lines.
7 is the counterpart of `kritiek op` in the next batch: the same plain sheet, but with the person turned away and hiding their face. Keep the sheet present in both, since the sheet is what the shame is about.
8, 9 and 10 are singles: hunger, a wish for a walk, and a clock that will not wait.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the noun's idea carried by the object or situation, not by a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch A2+-06 — images 51–60

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch noun plus a fixed preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `kritiek-op-het-ontwerp.png` — Dutch chunk: kritiek op (criticism of).
   Scene: one person stands pointing at a large plain drawing on a wall, one finger up and a frown; a second person beside them listens with arms folded. The drawing is plain, marked only with a single loose cross.
   Must read: criticism of a piece of work.
   Avoid: anger at a person (that is a different chunk); a speech bubble; readable charts.

2. `vraag-om-hulp.png` — Dutch chunk: vraag om (request for).
   Scene: one person holds out an open hand towards a neighbour; the neighbour hands over a ladder, both hands on the rungs. The ladder is the main mass.
   Must read: asking for help with a task.
   Avoid: two people just talking; a phone; money.

3. `vertrouwen-in-de-toekomst.png` — Dutch chunk: vertrouwen in (confidence in, trust).
   Scene: one person walks up a path towards a distant plain house, upright, unhurried, a bag on their shoulder; the path is one broad stroke from bottom to a point on the horizon. No worry in the body.
   Must read: quiet confidence about what is ahead.
   Avoid: a person running away; a person looking down; a horizon full of objects.

4. `vertrouwen-in-de-baas.png` — Dutch chunk: vertrouwen in (trust in a person).
   Scene: two people shake hands firmly, both standing square and looking at each other, smiles easy; the nearer handshake is the centre of the image. No documents.
   Must read: mutual trust between people.
   Avoid: a handshake at a sales counter with papers; a firm handshake with a hidden knife or trick; a crowd.

5. `oplossing-voor-het-probleem.png` — Dutch chunk: oplossing voor (solution to).
   Scene: one person at a table with a broken bicycle wheel in front of them; both hands are raised in a satisfied gesture, and a small plain tool lies beside the wheel. A single clean loose stroke connects the broken part to the tool.
   Must read: a fix for a concrete problem.
   Avoid: a light bulb or idea symbol; a person still struggling; a workshop full of tools.

6. `voorbereiding-op-het-examen.png` — Dutch chunk: voorbereiding op (preparation for).
   Scene: one person sits at a desk with an open book, a pile of notes and a pen, focused; a plain wall calendar beside them with one day marked by a black dot and no numbers.
   Must read: getting ready for an exam.
   Avoid: a person taking the exam with a paper and no numbers; a graduation hat; readable notes.

7. `gevolg-van-de-val.png` — Dutch chunk: gevolg van (consequence of).
   Scene: a person sits on the ground with one leg stretched out and one hand on a swollen ankle; a plain bicycle lies on its side a couple of steps away. The fall and its result are in one image.
   Must read: the aftermath of an accident.
   Avoid: a hospital bed; the moment of falling; readable warning signs.

8. `schuld-aan-de-buurman.png` — Dutch chunk: schuld aan (blame for).
   Scene: one person points a thumb back at themselves while looking down, then a second person beside them points at them too; a broken flower pot lies on the ground between them. No speech bubbles.
   Must read: responsibility for a fault.
   Avoid: a fight; a courtroom; a person running away.

9. `tijd-voor-een-pauze.png` — Dutch chunk: tijd voor (time for).
   Scene: one person sets a cup down on a table and pushes the laptop lid closed with the other hand, stretching; a plain clock with hands and tick marks but no numbers stands on the desk.
   Must read: the moment a break begins.
   Avoid: a person still working; readable numbers on the clock; a plate of food.

10. `schrik-van-het-geluid.png` — Dutch chunk: schrik van (fright at).
    Scene: one person jumps back with both hands raised, eyes wide, mouth a short open line; in front of them a plain loudspeaker on a stand with three short strokes of sound leaving it. Only one figure.
    Must read: being startled by a sudden noise.
    Avoid: a person afraid of a dog (used by the pilot); a monster; readable music notes.

CONTRAST PAIRS
1 and 2 are both about saying what is needed: a pointed critique of work versus a request for help. Same camera, one or two figures; the relation is the difference.
3 and 4 are both `vertrouwen in`: a place and a person. #3 uses the path and the horizon, #4 uses the handshake; keep the postures upright in both.
5 and 6 are both about being ready: a solution found and a preparation under way. Same desk, same camera; change the object — a broken wheel and a tool versus a book and a marked day.
7 and 8 are both about responsibility for a result: #7 is the result of an accident, #8 is blame between people. In #7 there is no other person, in #8 two people are present.
9 and 10 are singles: a pause with time to spare, and a sudden fright at a loud sound.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Is the noun's idea carried by the object or situation, not by a caption?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch A2+-07 — images 61–70

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk in which a preposition is carried inside a short word: er…, daar… or waar… . The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image. These chunks are grammatical shorthand for a thing, not letters on paper: show the situation and the person, never letters or symbols.

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

1. `ergens-naar-toe-gaan.png` — Dutch chunk: ergens naartoe (to somewhere).
   Scene: one person walks towards a small plain building in the middle distance, back to the viewer, one hand holding a bag; a single broad path sweeps from the bottom edge to the door.
   Must read: heading towards a place.
   Avoid: a person standing still; a map or pin; a building with readable signs.

2. `ergens-vandaan-komen.png` — Dutch chunk: ergens vandaan (from somewhere).
   Scene: one person has just come out of a doorway on the left and is now walking towards the viewer, one hand shielding their eyes; the open door is behind them, the path ahead is empty.
   Must read: having come from a place.
   Avoid: a person entering the door (that reads as going in); a suitcase with stickers; a road map.

3. `ergens-mee-bezig-zijn.png` — Dutch chunk: ergens mee bezig (busy with).
   Scene: one person is halfway inside a cupboard, one arm reaching, a second arm holding a cloth; the cupboard door hangs open. Nothing else in the room.
   Must read: occupied with a task right now.
   Avoid: a person sitting and reading; a checklist; another person.

4. `daar-komt-hij-aan.png` — Dutch chunk: daar komt hij aan (here he comes).
   Scene: one person stands waiting on a pavement, one hand raised in greeting, smile; a second person approaches in the distance on a bicycle, drawn small. The near figure looks towards the arriving one.
   Must read: someone arriving and being welcomed.
   Avoid: a person leaving and waving goodbye (that is a different chunk); a bus; a crowd.

5. `daar-gaat-het-over.png` — Dutch chunk: daar gaat het over (that is what it's about).
   Scene: two people sit at a table, one holding up a plain square card; the other leans in, pointing at the card. Both speech bubbles are blank and small. The card is the topic.
   Must read: this object is the subject of the conversation.
   Avoid: two people just chatting (used by the pilot); readable cards; a question mark.

6. `waar-ga-je-naartoe.png` — Dutch chunk: waar … naartoe (where to).
   Scene: one person stands at a crossroads drawn as a bold branching stroke; a second person beside them points at one branch and raises the eyebrows. A bag on the ground. No signs.
   Must read: choosing a destination.
   Avoid: a compass with letters; arrows on posts; a map with marks.

7. `waar-kom-je-vandaan.png` — Dutch chunk: waar … vandaan (where from).
   Scene: one person stands over a suitcase that is still open on the floor, one hand on the lid, looking up at a second person who is asking; the second person's palms are open.
   Must read: asking about a place of origin.
   Avoid: a suitcase pulled by a taxi; a globe with continents; two people arguing.

8. `er-is-nog-tijd-voor.png` — Dutch chunk: er is nog tijd voor (there is still time for).
   Scene: one person sits at a table and pushes back a plate; a plain clock with hands and no numbers stands beside them, and one hand of the clock is still well before the top; the person smiles and lifts a cup.
   Must read: time left for one more thing.
   Avoid: readable times; a person asleep; a person running.

9. `erover-nadenken.png` — Dutch chunk: erover nadenken (think it over).
   Scene: one person sits at a table with a large plain card flat in front of them, chin on one hand, eyes on the card; a small blank thought bubble drifts above. Only one option on the table.
   Must read: thinking about one thing.
   Avoid: two options side by side (that is choosing between things); a question mark; two people.

10. `eraan-toe-zijn.png` — Dutch chunk: eraan toe zijn (to be ready for it, to need it).
    Scene: one person sits heavily on a simple chair, bag still on the shoulder and coat still on, head tipped back, eyes half closed; the whole posture says that rest is overdue.
    Must read: badly needing a rest.
    Avoid: a person sleeping in bed; a person with a medical bandage; a second person.

CONTRAST PAIRS
1 and 2 are a pair: the same path stroke and the same building, same camera. In #1 the person walks away towards the building; in #2 the person walks towards the viewer from an open door. The direction of the figure is the only real change.
6 and 7 are a pair: the same two figures, same camera. In #6 a fork is drawn on the ground and one person points; in #7 there is no road at all and a suitcase is open on the floor. Neither may contain the other's prop.
4 and 10 are both arrival and exhaustion but not a pair; keep the postures opposite — upright and open versus collapsed and closed.
3, 5, 8 and 9 are singles. #9 must be visually distinct from the pilot's thinking-about-a-choice scene: one object, not two.

VALIDATION
For every image:
- Downscale mentally or actually to 64×64: is the idea still nameable?
- Are you showing the situation and the person, not letters, arrows or symbols?
- Is it cobalt only, with no orange, grey or second blue?
- Is there any text, letter, number, logo, emoji, punctuation, arrow or readable sign? Remove it.
- Is the background plain white, with no border, card, shadow or scenery?
- Does the scene span the frame without shrinking into a card, with the person 35–55% of the width?
Then check each pair side by side. If either image suggests the other's chunk, redraw it.

When finished, list the ten filenames and name any image whose 64 px silhouette is still ambiguous. Do not add any image that is not on this list.
````

## Batch A2+-08 — images 71–80

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the everyday situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `gaan-naar-het-werk.png` — Dutch chunk: gaan naar (to go to).
   Scene: a tall plain block of window squares stands at the left edge; one person in profile strides away from it to the right, bag over the shoulder, towards a low flat-roofed building at the far right edge. One broad ground stroke joins the two buildings.
   Must read: going to work.
   Avoid: a person entering a front door (that is leaving home); a bus or bicycle ride; a building with readable signs.

2. `wonen-in-een-flat.png` — Dutch chunk: wonen in (to live in).
   Scene: the same tall block of window squares, now filling the left two-thirds of the frame; one window is open and a person leans out on both elbows, a small plant pot on the sill. Every other window is plain and closed.
   Must read: someone who lives in a flat.
   Avoid: a person looking at rain through glass; a house with a garden; a crane or building site.

3. `kiezen-voor-de-fiets.png` — Dutch chunk: kiezen voor (to choose, to opt for).
   Scene: one person stands front-on between a bicycle on the left and a small plain car on the right, both the same size; one hand grips the bicycle handlebar and the body turns towards it. The car stands empty and the bicycle's front wheel already points away.
   Must read: choosing the bicycle over the car.
   Avoid: a person riding the bicycle; a crossroads; a car park with many vehicles.

4. `twijfelen-tussen-twee-jassen.png` — Dutch chunk: twijfelen tussen (to waver between).
   Scene: one person stands front-on between two coats hanging on two wall pegs, the same size on each side; one hand hovers in mid-air between them, a finger on the chin of the other, head tilted. Neither coat is touched.
   Must read: unable to decide between two coats.
   Avoid: a person trying on a coat; a shop rail with many coats; a doorway with two identical rooms.

5. `hopen-op-goed-nieuws.png` — Dutch chunk: hopen op (to hope for).
   Scene: one person stands at a small hall table beside the front door, hands clasped under the chin, one hand with crossed fingers raised; a single thin envelope is dropping through the letterbox. The table is bare and the face is bright.
   Must read: hoping for good news in the post.
   Avoid: a person reading the letter; a person at a phone waiting; a party or gift.

6. `zich-zorgen-maken-over-de-rekening.png` — Dutch chunk: zich zorgen maken over (to worry about).
   Scene: the same hall table and door; now three thick envelopes are piled on the table beside a flat, empty open purse with two coins. The person stands hunched, one hand pressed to the stomach and the other to the forehead.
   Must read: worrying about the bills.
   Avoid: a long receipt held up in anger (that is `boos over`); a person at a desk with a calculator; a person crying.

7. `betalen-voor-de-boodschappen.png` — Dutch chunk: betalen voor (to pay for).
   Scene: one person stands at the end of a plain counter, an open palm held out over it with a small stack of coins; on the counter a paper bag with a long loaf and a bottle neck sticking out. A bare hand enters from the frame edge, palm up, to receive.
   Must read: paying for shopping.
   Avoid: a supermarket trolley; a card machine with a screen; a till receipt.

8. `uitgeven-aan-de-huur.png` — Dutch chunk: uitgeven aan (to spend on).
   Scene: the same counter and the same person, with the same held-out handful of coins; on the counter, where the bag was, stands a small simple house shape with one door and one window, and a bigger stack of coins is already gone from the palm.
   Must read: spending money on rent for a home.
   Avoid: a for-sale sign; a key being handed over; a wallet with banknotes.

9. `vertrouwen-op-een-collega.png` — Dutch chunk: vertrouwen op (to rely on).
   Scene: one person in a coat with a bag at the door, one open hand raised in a relaxed goodbye, shoulders loose; behind them a colleague sits at a desk piled with folders and lifts a hand back. The leaver does not look worried.
   Must read: leaving the work with a colleague without worry.
   Avoid: a firm handshake; a hand from a ladder holding someone's weight; a meeting room with a table.

10. `bellen-met-de-huisarts.png` — Dutch chunk: bellen met (to be on the phone with).
    Scene: one person stands at a table with an old-fashioned handset to one ear, the other hand raised, a coiled cord looping down; the cord runs across the lower frame to the right where a smaller figure with a loop of stethoscope round the neck holds a matching handset, head tilted, listening. Both are on their own side of white space.
    Must read: talking on the phone with a doctor.
    Avoid: two people face to face in a consulting room (that is `praten met de dokter`); a mobile phone with a screen; a person talking to nobody.

CONTRAST PAIRS
1 and 2 are the same block of flats: one figure walks away from it towards a low building, one leans out of its window. Same camera and scale; the block is the constant and the figure's position is the only change.
3 and 4 are choosing and not choosing: a hand gripping one of two objects, and a hand hovering between two. Same centred figure, two objects of equal size; in #4 nothing is touched.
5 and 6 are the same hall table and front door: one thin envelope arriving with clasped hands, and a pile of thick ones with a hand on the forehead. Keep the table and the door identical.
7 and 8 are the same counter and the same handful of coins: once over a bag of food, once over a small house shape. Change only what stands on the counter.
9 and 10 are singles. #10 must not read as two people in one room: the cord and the band of white between them carry the call.

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
