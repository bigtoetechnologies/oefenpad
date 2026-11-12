# Voorzetselpaden — image plan, B1+

Status: planning document, 10 November 2026. This is the **B1+** band: the
productive upper band between B1 and B2. It covers roadmap batches 14–23 of
`prepositions-roadmap.md`.

The plan was split on 10 November 2026. What used to be one 460-frame B2 file is
now two — **B1+** (this file, 250 frames, batches 14–23) and **B2**
(`prepositions-art-b2.md`, 210 frames, batches 24–32). Nothing was added or cut
in the split. The seam is the old file's own boundary between its productive
band (old B2-01 – B2-25) and its B2+ edges (old B2-26 – B2-46).

Scope: **250 new frames**, planned as **25 self-contained Grok batches of ten**,
numbered B1+-01 to B1+-25. Each batch prints ten separate images.

What is excluded, and must not be redrawn or duplicated:

- The **30 pilot scenes** in `assets/voorzetselpaden/`, listed in
  `prepositions-art.md`.
- The **20 A0–A2 frames** in `prepositions-art-a0-a2.md`.
- The **17 batch-4b frames** in `prepositions-art-a2-pairs.md`.
- The **80 A2+ frames** in `prepositions-art-a2-plus.md`.
- The **120 B1 frames** in `prepositions-art-b1.md`.
- The **210 B2 frames** in `prepositions-art-b2.md`.

No frame in this file repeats any of those or another frame in this file.

**A note on the band name.** B1+ is named for its position, not for a strict
CEFR claim. The first fifteen batches — reflexive chunks, multi-word
prepositions, formal verb chunks, contrast at scale, double prepositions and the
work register — are productive B1+ material. The last ten add low-frequency
verbs, adjectives, nouns and idioms, which a strict reading would place at B2.
They are kept here so that the 460 old-B2 frames split into two near-equal
steps of 250 and 210 rather than 150 and 310. If strict CEFR labels matter more
than the size of the step, move B1+-16 – B1+-25 to B2 and the counts here become
150 and 310.

## How to use this file

Each numbered section is one self-contained prompt. Paste the whole fenced
block into Grok, one block at a time. Grok has no file access, so nothing
outside the block is assumed. Ask for the ten images, then process the result
as described in `game-art.md` under *Delivered raster art* and ship at
512 × 763.

The house style is the bold brush-pen sketch defined in `game-art.md`: cobalt
`#2B50C8` only, wide-nib contour with directional hatching, 2:3 portrait, one
idea per image, no text. The prompts repeat those rules because the generator
cannot read `game-art.md`.

A batch block is complete on its own: TASK, STYLE, FORMAT, the ten subjects,
CONTRAST PAIRS and VALIDATION. Nothing in a block requires another block to be
understood. The note on a frame may name a contrast partner that sits in a
neighbouring batch; the partner's filename is enough, because the tracker names
it too. Draw a pair in one sitting wherever you can.

## What B1+ adds

Two hundred and fifty frames in ten themes, from reflexive chunks and
multi-word prepositions through formal verb chunks, contrast at scale and the
work register to low-frequency vocabulary and fixed idioms. The last four
themes are a receptive cross-cut, not a new category, exactly as
`prepositions-roadmap.md` §6 says: they draw from the verb, adjective, noun and
idiom pools rather than adding new grammar.

No frequency list exists in the repo, so the chunks are ordered by register and
usefulness, not by measured frequency. Re-cut any batch around a frequency list
when one arrives, per `prepositions-roadmap.md` §12.1; the art plan survives a
re-cut because each frame stands alone.

About 110 of the 250 frames are contrast pairs: two frames that share a verb,
adjective, noun or chunk and differ only in the preposition, the sense or the
partner. The rest are singles. A single frame that belongs to no pair gets an
extra `bouw` sentence in `server/Oefenpad.Resources/Games/Data/prepositions.json`
after delivery, so the learner still meets it beside something familiar.

| Image batch | Theme | Frames | Roadmap batch |
|---|---|---|---|
| B1+-01 – B1+-03 | Reflexive and idiomatic chunks | 30 | 14 |
| B1+-04 – B1+-05 | Multi-word prepositions | 20 | 15 |
| B1+-06 – B1+-08 | Formal verb + preposition | 30 | 16 |
| B1+-09 – B1+-10 | Contrast pairs at scale | 20 | 17 |
| B1+-11 – B1+-12 | Double prepositions and choice | 20 | 18 |
| B1+-13 – B1+-15 | Work register | 30 | 19 |
| B1+-16 – B1+-18 | Low-frequency verb + preposition | 30 | 20 |
| B1+-19 – B1+-20 | Low-frequency adjective + preposition | 20 | 21 |
| B1+-21 – B1+-22 | Low-frequency noun + preposition | 20 | 22 |
| B1+-23 – B1+-25 | Idioms with fixed prepositions | 30 | 23 |
| **Total** | | **250** | |

Observations on the scope, in the spirit of `prepositions-art-a2-plus.md`:

- The reflexive batches B1+-01 to B1+-03 carry the reflexive verb itself, not a
  new preposition. Reflexivity is posture: a figure that does something to
  itself, or that pushes against something. Do not draw a mirror, a second
  self, or a thought bubble with a face inside it.
- B1+-04 and B1+-05 are built on multi-word prepositions (`met betrekking tot`,
  `ten behoeve van`, `in afwijking van`), and B1+-23 on idioms whose
  preposition is fixed (`op de hoogte zijn van`, `rekening houden met`). Every
  frame in the idioms theme governs a fixed preposition; the tracker note on
  each row says whether it is a pair or a single.
- The low-frequency and register batches reuse a small set of scene archetypes
  (office, counter, clinic, workshop), as the brief allows. Each image in a
  batch is still visually distinct, and the contrast note says when a scene is
  reused.
- Some chunks are abstract. Each such frame is drawn as a concrete situation
  and the note says so; the gloss carries the abstraction.

Status values in the tracker: `needed` (not drawn), `drawn` (delivered and
processed), `dropped` (cut after review).

## Tracker

All 250 frames, in batch order. The file column is the Grok filename and the
shipped scene id. "Pair / note" names the partner file for a pair, or says
`Single` plus the camera note.

| # | File | Dutch frame | English | Scene | Pair/note | Status |
|---|---|---|---|---|---|---|
| 1 | `zich-herinneren-aan-naam.png` | zich herinneren aan | to remember | One person stands still in an open doorway with a hand flat on the forehead and a small blank thought bubble drawn… | Single. Abstract chunk shown as a concrete pause; the bubble is blank; same camera as `een-klap-in-het-gezicht-zijn` and `zich-ontdoen-van-afval`. | needed |
| 2 | `zich-verdiepen-in-boek.png` | zich verdiepen in | to immerse oneself in | One person is bent low over a single open book on a plain table, elbows planted, forehead almost on the page | Single. Complete absorption in one text; same camera as `zich-verdiepen-in-de-literatuur`. | needed |
| 3 | `zich-bezighouden-met-klus.png` | zich bezighouden met | to occupy oneself with | One person kneels on the floor with both hands inside an open box of loose parts, sorting them into two small plain… | Single. Concrete task for an abstract verb; same camera as `beschikken-over-de-benodigde-middelen`. | needed |
| 4 | `zich-verzetten-tegen-plan.png` | zich verzetten tegen | to resist, to oppose | One person stands with both arms braced flat against a large board being pushed towards them by two others | Pushing back against something; pair with `zich-schikken-naar-beslissing`. | needed |
| 5 | `zich-schikken-naar-beslissing.png` | zich schikken naar | to comply with, to accept | One person stands with both hands lowered and head slightly bowed in front of a large blank board held upright by… | Accepting an order; pair with `zich-verzetten-tegen-plan`. | needed |
| 6 | `zich-ergeren-aan-geluid.png` | zich ergeren aan | to be annoyed by | One person sits at a table with both hands pressed over the ears and eyes squeezed shut | Irritation at noise; pair with `zich-afsluiten-voor-geluid`, `zich-vermaken-met-spel`. | needed |
| 7 | `zich-vermaken-met-spel.png` | zich vermaken met | to amuse oneself with | One person sits on the floor with a small board game laid out and both hands raised mid-move, mouth open in delight | Enjoying a game alone; pair with `zich-ergeren-aan-geluid`. | needed |
| 8 | `zich-iets-voorstellen-bij-het-huis.png` | zich iets voorstellen bij | to picture something by | One person stands with one hand open towards a large blank thought bubble in which a simple house outline floats,… | Single. The bubble is the only indoor object; keep it blank. | needed |
| 9 | `zich-haasten-naar-de-trein.png` | zich haasten naar | to rush to | One person runs with the body tipped forward, one arm swinging and a bag bouncing behind | Single. No arrows; speed comes from the tipped body. | needed |
| 10 | `zich-afsluiten-voor-geluid.png` | zich afsluiten voor | to shut oneself off from | One person sits inside a large plain box open on one side, knees drawn up and hands on the head | Cutting oneself off; pair with `zich-ergeren-aan-geluid`. | needed |
| 11 | `zich-ontfermen-over-kind.png` | zich ontfermen over | to take under one's wing | One tall person wraps a coat around a small figure's shoulders from behind, both hands on the coat collar | Sheltering someone smaller; pair with `zich-bedienen-van-hulp`. | needed |
| 12 | `zich-bedienen-van-hulp.png` | zich bedienen van | to make use of, to avail oneself of | One person holds a short plain stick out towards a high shelf and lifts a box down with it, other hand steadying the… | Register: formal 'use'. Concrete: the tool; pair with `zich-ontfermen-over-kind`. | needed |
| 13 | `zich-richten-tot-publiek.png` | zich richten tot | to address oneself to | One person stands at the front of a small group of seated figures, one arm open wide towards them and the head… | Speaking to an audience; pair with `zich-wenden-tot-balie`. | needed |
| 14 | `zich-wenden-tot-balie.png` | zich wenden tot | to turn to, to approach | One person stands at a counter and leans in towards a clerk, one hand resting on the counter edge | Asking someone for help at a desk; pair with `zich-richten-tot-publiek`. | needed |
| 15 | `zich-ontdoen-van-afval.png` | zich ontdoen van | to dispose of | One person tips a bin bag into a large container with a hinged lid, one hand holding the lid up and the bag already… | Single. Rubbish is plain, with no logos; same camera as `zich-herinneren-aan-naam`. | needed |
| 16 | `zich-herstellen-van-ziekte.png` | zich herstellen van | to recover from | One person sits up in a bed with a blanket to the waist and a bowl on a side table, back straight and face calm | Single. Clinic archetype; keep it minimal; same camera as `zich-herstellen-van-een-operatie`. | needed |
| 17 | `zich-verdiepen-in-de-zaak.png` | zich verdiepen in | to go into, to study | One person holds a large open folder with both hands and leans into it, head lowered | Single. Office archetype, reused; file stack is the mass, not the person. | needed |
| 18 | `zich-laten-leiden-door-advies.png` | zich laten leiden door | to be guided by | One person walks forward behind a blindfolded figure who holds a short plain stick in front and points it forward | Single. Being steered by another's judgement. | needed |
| 19 | `zich-neerleggen-bij-uitslag.png` | zich neerleggen bij | to accept, to resign oneself to | One person sits with shoulders dropped and both hands open on the knees, looking down at a single plain sheet lying… | Single. Giving up the argument. | needed |
| 20 | `zich-verheugen-op-feest.png` | zich verheugen op | to look forward to | One person stands at a mirrorless wall with a small blank invitation card in one hand and the other hand already… | Single. Keep the pilot's gift scene out of it: no box, no ribbon. | needed |
| 21 | `zich-inzetten-voor-de-buurt.png` | zich inzetten voor | to work hard for | Two people carry a long plank between them towards a low unfinished wall, both leaning into the load | Effort for a shared cause; same camera as `investeren-in-een-onderneming`; pair with `zich-verzekeren-van-een-plaats`. | needed |
| 22 | `zich-verzekeren-van-een-plaats.png` | zich verzekeren van | to secure, to make sure of | One person stands at a ticket counter with one hand on a blank ticket held close to the chest and the other hand… | Counter archetype, reused; the ticket is the mass; pair with `zich-inzetten-voor-de-buurt`. | needed |
| 23 | `zich-verlagen-tot-een-scheldwoord.png` | zich verlagen tot | to stoop to | One figure stands over another who points up at them with an open mouth | Single. The refusal is the idea: head away, palm outwards; same camera as `zich-inleven-in-de-ander`. | needed |
| 24 | `zich-vergewissen-van-de-vraag.png` | zich vergewissen van | to make sure of, to verify | One person holds a small plain lamp up beside a switch on a wall panel while the other hand rests on the switch | Single. Formal register made concrete: check before use. | needed |
| 25 | `zich-tegoeddoen-aan-een-maaltijd.png` | zich tegoeddoen aan | to help oneself generously to | One person sits at a loaded table with a full plate in both hands, leaning back with eyes closed in contentment | Single. Table archetype; food is plain masses. | needed |
| 26 | `zich-onttrekken-aan-de-verplichting.png` | zich onttrekken aan | to withdraw from, to evade | One person slips sideways out of a row of standing figures towards an open door, body turned away and one foot… | Leaving a duty quietly; pair with `zich-voegen-bij-de-groep`. | needed |
| 27 | `zich-voegen-bij-de-groep.png` | zich voegen bij | to join | One person steps into line between two standing figures, one hand raised in greeting | Joining a group; pair with `zich-onttrekken-aan-de-verplichting`. | needed |
| 28 | `zich-wreken-op-een-collega.png` | zich wreken op | to take revenge on | One person stands behind another's chair and tips it slightly backwards with both hands while the seated person… | Single. Office archetype, reused. No smiling: this is not a joke. | needed |
| 29 | `zich-inleven-in-de-ander.png` | zich inleven in | to empathise with | Two people sit facing each other on low stools, the first leaning far forward with both hands open towards the… | Single. Muted posture: leaning, not embracing; same camera as `zich-verlagen-tot-een-scheldwoord`; pair with `zich-verplaatsen-in-de-ander`. | needed |
| 30 | `zich-verplaatsen-in-de-ander.png` | zich verplaatsen in | to put oneself in the place of | Two people sit on low stools facing each other | Single. Seat pair kept from the batch camera; the hand on the knee is the only contact; pair with `zich-inleven-in-de-ander`. | needed |
| 31 | `met-betrekking-tot-de-offerte.png` | met betrekking tot | with regard to | One person stands beside a tall stack of plain folders and taps the top folder with one hand, looking towards a… | Single. Office archetype, reused. Avoid putting numbers on the folders. | needed |
| 32 | `in-verband-met-de-verhuizing.png` | in verband met | in connection with, because of | One person carries a box out of a doorway while another holds the door and takes the next box | Linked cause for an activity; same camera as `ten-gevolge-van-de-storing`; pair with `ten-behoeve-van-het-onderhoud`. | needed |
| 33 | `ten-behoeve-van-het-onderhoud.png` | ten behoeve van | for the benefit of | One person kneels with a plain oil can and a cloth beside a large machine with exposed round parts, one hand wiping… | Serving the upkeep of a machine; pair with `in-verband-met-de-verhuizing`. | needed |
| 34 | `ten-koste-van-de-pauze.png` | ten koste van | at the expense of | One person sits at a desk with a large clock face with tick marks but no hands beside them and a sandwich lying… | Giving something up to keep working; same camera as `ten-opzichte-van-de-collega`; pair with `ten-nadele-van-de-klant`. | needed |
| 35 | `ten-nadele-van-de-klant.png` | ten nadele van | to the detriment of | One person stands behind a counter and slides a shorter pile of paper towards a customer who holds out an open hand | Someone gets less than they should; same camera as `ten-spijt-van-de-weigering`; pair with `ten-koste-van-de-pauze`. | needed |
| 36 | `met-het-oog-op-de-toekomst.png` | met het oog op | with a view to | One person stands at a plain table and places a small sapling shape into a pot beside an open notebook with a ruled… | Single. Growth shape only, no leaves detail; same camera as `afhankelijk-van-goed-weer`. | needed |
| 37 | `aan-de-hand-van-de-kaart.png` | aan de hand van | on the basis of, using | One person holds a large blank map open with both hands and leans over it, while a second figure points at one spot… | Steering by a guide; pair with `op-basis-van-de-cijfers`. | needed |
| 38 | `op-basis-van-de-cijfers.png` | op basis van | on the basis of | One person stands in front of a plain wall panel on which three thick vertical bars of different heights are… | Deciding from measured results; pair with `aan-de-hand-van-de-kaart`. | needed |
| 39 | `met-inachtneming-van-de-termijn.png` | met inachtneming van | subject to, in observance of | One person writes on a blank sheet at a desk with a large calendar sheet pinned on the wall behind, its grid drawn… | Single. Calendar boxes only, no numerals. | needed |
| 40 | `in-afwijking-van-de-regel.png` | in afwijking van | in deviation from | One person steps over a painted straight line on the floor while two others stand behind it, watching | Single. No arrows or signs at the line; same camera as `volgens-de-afspraak`. | needed |
| 41 | `ten-opzichte-van-de-collega.png` | ten opzichte van | in relation to, towards | Two people stand face to face at equal distance with a plain straight line drawn on the floor between them and… | Single. A measured relationship to someone; same camera as `ten-koste-van-de-pauze`. | needed |
| 42 | `ten-aanzien-van-de-kosten.png` | ten aanzien van | with regard to, as regards | One person stands behind a plain counter with a stack of blank receipts on one side and a single coin-shaped disc on… | Single. Office archetype, reused. | needed |
| 43 | `ten-dienste-staan-van-de-klant.png` | ten dienste staan van | to be of service to | One person stands behind a low plain counter, body turned towards a visitor who holds out a flat folder; both of the standing… | Single. Formal service posture; the folder is the only object held. | needed |
| 44 | `ten-gevolge-van-de-storing.png` | ten gevolge van | as a result of | One person stands in a dim room with a plain lamp dangling from a wall socket by a loose cord, holding the cord up | Single. Consequence of a fault; same camera as `in-verband-met-de-verhuizing`. | needed |
| 45 | `ten-gunste-van-de-kandidaat.png` | ten gunste van | in favour of | One person lays one hand flat on a plain sheet bearing a single round seal shape and slides it towards a seated… | Single. Backing one side. | needed |
| 46 | `ten-laste-van-de-werkgever.png` | ten laste van | chargeable to, at the expense of | One person stands light with a tool bag and open hands while a larger figure beside them bends under a heavy sack | Single. The cost sits on the other figure's back; keep it a sack, not the crate of subject 7. | needed |
| 47 | `ten-spijt-van-de-weigering.png` | ten spijt van | in spite of | One person moves a heavy crate across the floor towards a closed door while another figure stands at the door with… | Single. Carrying on despite a refusal; same camera as `ten-nadele-van-de-klant`. | needed |
| 48 | `ten-tijde-van-het-onderzoek.png` | ten tijde van | at the time of | One person stands in the middle of a room holding a small plain clipboard, looking at empty shelving on one wall | Single. Formal time phrase made concrete as an emptied room. | needed |
| 49 | `ten-overstaan-van-de-notaris.png` | ten overstaan van | in the presence of | One person signs a blank sheet on a table while a second figure stands opposite with both hands clasped in front,… | Single. Office archetype; the witness is the mass. | needed |
| 50 | `ten-voordele-van-de-buurt.png` | ten voordele van | in aid of, for the benefit of | One person holds out a plain collecting tin with a slot towards two passing figures while a third has already… | Single. The slot in the tin is the clue; no hearts or logos. | needed |
| 51 | `beschikken-over-een-kantoor.png` | beschikken over | to have at one's disposal | One person stands in the middle of an empty office with both arms spread wide, palms up, towards a large desk and… | Single. Office archetype, reused. | needed |
| 52 | `afhangen-van-droog-weer.png` | afhangen van | to depend on | One person stands at a window under a small row of plain cloud shapes while holding up a folded coat in one hand,… | Single. A decision held up by the weather; same camera as `afhangen-van-de-beslissing`. | needed |
| 53 | `beschikken-tot-uitstel.png` | beschikken tot | to decide to, to order | One person sits behind a desk and lays one hand flat on a blank sheet while pushing a small tray of papers away with… | Single. Office archetype. Formal decision, no readable stamp; same camera as `noodzaken-tot-actie`. | needed |
| 54 | `bijdragen-aan-de-discussie.png` | bijdragen aan | to contribute to | One person leans forward at a long table with one hand raised and the other flat on the table | Meeting archetype, reused; pair with `instemmen-met-het-voorstel`. | needed |
| 55 | `instemmen-met-het-voorstel.png` | instemmen met | to agree with | One person at the same long table lowers a raised hand to the table and nods, head forward | Saying yes to what was proposed; pair with `bijdragen-aan-de-discussie`. | needed |
| 56 | `verwijzen-naar-de-nota.png` | verwijzen naar | to refer to | One person stands and points a hand towards a thin blank booklet lying on the corner of the table, while three… | Single. Meeting archetype. No arrows; the pointing hand carries it. | needed |
| 57 | `volstaan-met-een-knikje.png` | volstaan met | to suffice with, to settle for | One person receives a thick folder from a colleague and answers with a single slow nod of the head, both hands still… | Single. A minimal answer. | needed |
| 58 | `verzoeken-om-uitstel.png` | verzoeken om | to request, to ask for | One person hands a blank form across a counter to a clerk, one hand open underneath, head lowered slightly | Single. Counter archetype, reused. | needed |
| 59 | `getuigen-van-toewijding.png` | getuigen van | to testify to, to show | One person stands beside a table on which sits a single worn pair of plain work gloves and a cracked tool handle | Single. Evidence of long effort. | needed |
| 60 | `betrekking-hebben-op-de-onkosten.png` | betrekking hebben op | to relate to, to concern | One person sits at a desk with a small stack of plain receipts in one hand and points a finger at one of them with the other | Single. Office archetype. The pointed receipt is the clue; no dashes or numbers. | needed |
| 61 | `vasthouden-aan-de-bewering.png` | vasthouden aan | to stick to | One person stands with both arms wide and chin lifted, mouth open mid-sentence, while a seated listener leans back… | Stating something forcefully; pair with `afstand-nemen-van-de-bewering`. | needed |
| 62 | `afstand-nemen-van-de-bewering.png` | afstand nemen van | to distance oneself from | One person holds one flat hand out at chest height, palm turned outward towards a second figure, as if pushing the idea away | Pushing an idea away from oneself; pair with `vasthouden-aan-de-bewering`. | needed |
| 63 | `werken-volgens-een-werkwijze.png` | werken volgens | to work according to | One person holds a plain tool with both hands in front of them and aligns it with a marked line drawn on a workbench, eyes on the line | Single. Workshop archetype; the drawn line is the method; no text on it. | needed |
| 64 | `noodzaken-tot-actie.png` | noodzaken tot | to make necessary | One person stands with both hands raised and open in a shrug in front of a stalled machine with a loose belt, while… | Single. Circumstances force an action; same camera as `beschikken-tot-uitstel`. | needed |
| 65 | `controleren-op-kwaliteit.png` | controleren op | to check for | One person checks a row of three identical plain blocks on a bench with a small square gauge held against one of… | Single. Workshop archetype. | needed |
| 66 | `zich-houden-aan-de-norm.png` | zich houden aan | to adhere to, to stick to | One person holds a straight rule up against the edge of a large panel and squints along it, one eye closed, while a second figure holds the panel steady | Single. Same rule as #9; here the rule is the standard that is kept to. | needed |
| 67 | `voortvloeien-uit-het-beleid.png` | voortvloeien uit | to result from, to follow from | One person stands at the top of a short flight of plain steps and lets one hand rest on the rail, looking down at a… | Single. Steps are the mass; no arrows. | needed |
| 68 | `aandacht-vragen-voor-het-plan.png` | aandacht vragen voor | to call attention to | One person sits at a desk with both hands framing a single page and a closed door behind them | Single. The bell is the demand; keep its shape simple. | needed |
| 69 | `wijzigingen-aanbrengen-in-de-afspraak.png` | wijzigingen aanbrengen in | to make changes to | One person sits with a blank sheet in one hand and a pen in the other, crossing out a line and starting again below it, an earlier crumpled sheet at the desk edge | Single. Changing an agreement; the crossed-out line and the replacement carry it. | needed |
| 70 | `optreden-tegen-de-overtreders.png` | optreden tegen | to take action against | One person stands at an open doorway with one arm across it, palm flat and face turned to three figures who have… | Single. Acting against those who cross a rule; the barring arm is the shape. | needed |
| 71 | `gepaard-gaan-met-een-risico.png` | gepaard gaan met | to be accompanied by, to go hand in hand with | One person holds a large plain parcel in both arms and steps towards a narrow gap between two stacked crates, body… | Single. A task that brings a risk with it; the tight gap carries it. | needed |
| 72 | `het-oneens-zijn-met-de-uitslag.png` | het oneens zijn met | to disagree with | One person holds up a blank sheet and shakes their head, one hand flat towards a second figure who holds the same… | Single. Disagreeing with a result; the flat hand and shaken head carry it. | needed |
| 73 | `blijken-uit-de-meting.png` | blijken uit | to emerge from | One person stands beside a large plain meter dial with a single pointer turned to the right side, one hand open… | Single. The dial is a plain circle with a pointer. | needed |
| 74 | `uitgaan-van-een-aanname.png` | uitgaan van | to go on the assumption of | One person stands with one hand on a switch and the other lifted with a finger raised, speaking to a colleague who nods | Single. Same machine as #3's dial but switched off. | needed |
| 75 | `onderhoud-verrichten-aan-de-machine.png` | onderhoud verrichten aan | to carry out maintenance on | One person kneels beside a large machine with the front panel removed and lays a plain tool inside it | Single. Reuse of the machine archetype; panel opening is the marker. | needed |
| 76 | `een-oordeel-vellen-over-het-onderdeel.png` | een oordeel vellen over | to pass judgement on | One person taps a small cracked part lying on a bench with one finger and turns to a colleague with a flat mouth line | Single. Judging something wrong. | needed |
| 77 | `beoordelen-op-de-inhoud.png` | beoordelen op | to assess by | One person sits at a desk with a large open folder of blank pages and a pen resting across it, head tilted, looking… | Single. Giving a judgement on someone's work; same camera as `een-beoordeling-krijgen-van-de-begeleider`. | needed |
| 78 | `een-subsidie-toekennen-aan-de-aanvrager.png` | toekennen aan | to award to | One person slides a plain envelope across a desk towards an applicant whose hand is already outstretched | Single. Office archetype, reused. No readable stamp or seal text. | needed |
| 79 | `afstand-doen-van-de-schuld.png` | afstand doen van | to relinquish, to give up | One person holds a blank sheet and draws a wide diagonal stroke across it, then lifts it towards a second figure who… | Single. Giving up a claim; the cancelling stroke carries it. | needed |
| 80 | `informatie-verstrekken-over-de-regeling.png` | informatie verstrekken over | to provide information about | One person stands at a counter and pushes a small stack of blank sheets towards a waiting figure, one hand flat on… | Single. Counter archetype, reused. Keep the stack low and plain. | needed |
| 81 | `uitgaan-van-het-ergste.png` | uitgaan van | to assume, to proceed from | One person stands with one hand flat on a large closed box in front of them, looking steadily at a colleague | Taking the downside as the starting point; pair with `uitgaan-naar-de-zaal`. | needed |
| 82 | `uitgaan-naar-de-zaal.png` | uitgaan naar | to go out to | One person steps out through a wide door into an open space, one hand raised towards a distant figure walking in the… | Single. Movement outwards, not a belief; pair with `uitgaan-van-het-ergste`. | needed |
| 83 | `afhangen-van-de-beslissing.png` | afhangen van | to depend on | One person stands on one side of a doorway waiting, hands behind the back, looking at a second figure inside who… | Single. Waiting for another's decision; same camera as `afhangen-van-droog-weer`. | needed |
| 84 | `berusten-op-een-afspraak.png` | berusten op | to rest on, to be based on | Two people stand side by side with one hand each on a large plain stone block between them, holding it together | Standing on a shared agreement; pair with `berusten-in-het-verlies`. | needed |
| 85 | `berusten-in-het-verlies.png` | berusten in | to accept, to come to terms with | One person stands with both hands open at the sides and a slight bow of the head in front of an empty chair with a… | Settling into a loss; pair with `berusten-op-een-afspraak`. | needed |
| 86 | `zich-richten-op-het-doel.png` | zich richten op | to focus on | One person stands with both hands raised in a ring in front of the eye, looking straight ahead through it at a… | Aiming attention at one target; pair with `zich-richten-tot-de-zaal`. | needed |
| 87 | `zich-richten-tot-de-zaal.png` | zich richten tot | to address | One person stands with one arm open towards three seated figures and the body turned fully towards them | Same as earlier group frames; keep the seated backs identical; pair with `zich-richten-op-het-doel`. | needed |
| 88 | `verschillen-van-de-rest.png` | verschillen van | to differ from | One figure stands in front of four identical plain blocks, holding a fifth block of clearly different height beside… | Standing out from the rest; pair with `afwijken-van-het-plan`. | needed |
| 89 | `afwijken-van-het-plan.png` | afwijken van | to deviate from | One person walks in a straight path away from a painted line on the floor, one foot already off the line, while a… | Leaving a laid-down course; same camera as `houden-aan-het-licht`; pair with `verschillen-van-de-rest`. | needed |
| 90 | `voortkomen-uit-het-verleden.png` | voortkomen uit | to arise from | One person holds an old split branch in both hands with a young straight shoot growing out of the fork, one hand… | Single. Branch and shoot only; no leaves. | needed |
| 91 | `houden-van-het-klimaat.png` | houden van | to be fond of, to love | One person sits on a low rock with both hands relaxed on the knees, face lifted to a large plain ring for the sun | Single. Reused chunk with a new scene; not a repetition of the pilot. | needed |
| 92 | `houden-aan-het-licht.png` | houden aan | to keep to, to stick by | One person walks steadily along a straight painted line laid on a wide floor, one foot exactly on it, hands at the… | Single. Keeping to a rule; same camera as `afwijken-van-het-plan`. | needed |
| 93 | `twijfelen-aan-de-oplossing.png` | twijfelen aan | to doubt | One person holds up a small plain gear piece at eye level, one hand turning it, mouth pulled to one side, and looks… | Not trusting something; pair with `twijfelen-over-de-keuze`. | needed |
| 94 | `twijfelen-over-de-keuze.png` | twijfelen over | to be undecided about | One person stands between two identical plain doors, arms hanging, head turned from one to the other | Hesitation between two equal options; pair with `twijfelen-aan-de-oplossing`. | needed |
| 95 | `geloven-in-de-goede-afloop.png` | geloven in | to believe in | One person walks forward with head up and one hand raised open, towards a wide bright gap between two tall blocks | Single. The blocks are plain shapes with no doors or windows. | needed |
| 96 | `denken-aan-het-klimaat.png` | denken aan | to think of, to bear in mind | One person pauses with one hand on a bicycle handlebar and the other at the chin, looking at a plain globe shape… | Single. Reuse of the shipped verb with a new object; the globe is a bare ring. | needed |
| 97 | `zorgen-voor-de-planten.png` | zorgen voor | to look after | One person waters a row of three potted plants with a plain can, tilting the spout towards the middle pot | Single. Plant shapes are simple stems, no leaves detail. | needed |
| 98 | `zorgen-over-het-examen.png` | zorgen over | to worry about | One person sits on the edge of a chair with both hands clasped tightly in the lap and eyebrows drawn down | Single. Anxiety about a test. | needed |
| 99 | `denken-over-een-voorstel.png` | denken over | to think about, to consider | One person sits with a blank sheet in one hand and a pen held still in the other, chin on the pen hand, eyes towards… | Single. Reuse of the shipped verb with a new object; the window is the anchor; same camera as `te-wijten-zijn-aan-een-storing`. | needed |
| 100 | `oplossen-door-te-luisteren.png` | oplossen door | to solve by | Two people sit facing each other, one leaning in with an open palm on the table between them | Single. The table between them is empty. | needed |
| 101 | `tussen-de-regels-door-lezen.png` | tussen de regels door | between the lines | One person holds a blank page close to the face with both hands and one eye squinting past the edge of it | Single. Ruled lines are the only marks; no writing; pair with `werken-tegen-de-klok`. | needed |
| 102 | `vanaf-het-moment-van-aankomst.png` | vanaf het moment van | from the moment of | One person stands just inside a doorway with a plain suitcase beside them and a hand still on the bag handle | Reuse of doorway: the bag is inside, the door open; pair with `van-tijd-tot-tijd-bellen`. | needed |
| 103 | `werken-tegen-de-klok.png` | tegen de klok | against the clock | One person sits at a desk with papers under both hands, writing fast and leaning forward; a large wall clock above the desk shows tick marks and two hands, no numerals | Single. Speed under time pressure; the clock is the only fixed point; same camera as `stilstaan-bij-het-verleden`; pair with `tussen-de-regels-door-lezen`. | needed |
| 104 | `van-tijd-tot-tijd-bellen.png` | van tijd tot tijd | from time to time | One person sits with a plain telephone receiver held to the ear, a second hand raised | Single. Two separated bars carry the intermittency; pair with `vanaf-het-moment-van-aankomst`. | needed |
| 105 | `door-de-week-heen-werken.png` | door de week | during the week | One person stands with one hand on a large plain calendar of boxes, covering the left part with a flat hand while… | Single. Calendar boxes only; no letters or numbers. | needed |
| 106 | `op-de-hoogte-zijn-van-het-nieuws.png` | op de hoogte zijn van | to be aware of, to be informed about | One person stands with a folded blank newspaper held against the chest and one hand lifted to the chest in a small,… | Single. Same folded paper shape as the journalistic batches; keep it upright here. | needed |
| 107 | `buiten-kijf-blijven.png` | buiten kijf | beyond dispute | Two people stand on either side of a large plain upright stone slab with one hand each flat on it, facing outward… | Single. A settled matter between two. | needed |
| 108 | `tegen-de-verwachting-in-winnen.png` | tegen de verwachting in | contrary to expectation | One figure stands with both arms raised beside a low plain block, while three figures behind look towards them with… | Single. The tilted heads of the three behind carry surprise. | needed |
| 109 | `in-de-loop-der-jaren.png` | in de loop der jaren | over the years | One person stands beside a single tall tree trunk with several narrow rings drawn at its base, one hand resting on… | Single. Rings at the base only; no numerals; same camera as `een-beroep-aantekenen-binnen-de-termijn`. | needed |
| 110 | `onder-het-mom-van-uitstel.png` | onder het mom van | under the pretext of | One person holds a plain folder in front of the chest and steps forward with chin up, while a second figure behind… | Single. The second sheet is the only revealing detail. | needed |
| 111 | `kiezen-tussen-twee-banen.png` | kiezen tussen | to choose between | One person stands at the centre of a wide floor with a plain upright post on each side at equal distance, both hands… | Weighing two options; pair with `kiezen-uit-het-aanbod`. | needed |
| 112 | `kiezen-uit-het-aanbod.png` | kiezen uit | to choose from | One person stands in front of a row of five identical plain boxes on a shelf and has one hand out towards the middle… | Picking one of many; pair with `kiezen-tussen-twee-banen`. | needed |
| 113 | `beslissen-over-de-aanvraag.png` | beslissen over | to decide on | One person sits behind a desk with a blank form held in both hands, thumb on one corner, eyes down | A decision still open in someone's hands; pair with `beslissen-tot-verkoop`. | needed |
| 114 | `beslissen-tot-verkoop.png` | beslissen tot | to decide to, to resolve on | One person lays a plain key on the table and pushes it towards a second figure with one flat hand, the other hand… | Committing to an action; pair with `beslissen-over-de-aanvraag`. | needed |
| 115 | `belangen-afwegen-tegen-elkaar.png` | afwegen tegen | to weigh against | One person holds a simple balance with a plain block in each pan, one pan clearly lower | Single. Two pans, two blocks; same camera as `besluiten-tot-uitstel`. | needed |
| 116 | `besluiten-tot-uitstel.png` | besluiten tot | to decide to | One person sits with a blank sheet turned face down on the desk and both hands resting flat on it, looking up at a… | Single. Face-down sheet is the marker; keep it flat; same camera as `belangen-afwegen-tegen-elkaar`. | needed |
| 117 | `opteren-voor-een-oplossing.png` | opteren voor | to opt for | One person kneels beside a low shelf with two plain tools lying on it and has already lifted the longer one into… | Making a single choice; pair with `aarzelen-tussen-twee-mogelijkheden`. | needed |
| 118 | `aarzelen-tussen-twee-mogelijkheden.png` | aarzelen tussen | to hesitate between | One person stands with one hand extended towards each of two plain objects on a table, both hands equally open, body… | Being stuck between two; pair with `opteren-voor-een-oplossing`. | needed |
| 119 | `afzien-van-een-plaats.png` | afzien van | to give up, to forgo | One person holds a blank ticket out towards a clerk across a counter while shaking their head slightly, the other… | Single. Counter archetype, reused. The ticket stays in the hand. | needed |
| 120 | `zich-beraden-op-het-voorstel.png` | zich beraden op | to deliberate on | Two people sit facing each other across a corner of a table with one blank sheet between them and no pens | Single. Two hands near one sheet, neither touching. | needed |
| 121 | `leidinggeven-aan-het-team.png` | leidinggeven aan | to be in charge of | One person stands at the head of a small table in an office with one hand open towards three seated figures and the… | Single. Office archetype, reused. Reuse of an earlier group scene; keep the rolled plan rolled here. | needed |
| 122 | `rapporteren-aan-de-chef.png` | rapporteren aan | to report to | One person stands at a desk with a plain folder held out towards a seated figure who does not look up | Answering to someone above; pair with `overleggen-met-collega`. | needed |
| 123 | `overleggen-met-collega.png` | overleggen met | to consult with | Two people sit side by side at one desk, the first holding a blank sheet and the second leaning over the same sheet | Deciding together; pair with `rapporteren-aan-de-chef`. | needed |
| 124 | `een-punt-zetten-achter-de-klus.png` | een punt zetten achter | to round off | One person sets the last of a stack of plain folders square on top of a small pile and straightens it with both hands | Single. The last action of a task; same camera as `solliciteren-op-een-vacature`. | needed |
| 125 | `een-gesprek-inplannen-in-de-agenda.png` | inplannen in | to schedule into | One person stands with a large plain calendar of boxes held against the wall with one hand and draws a single circle… | Single. Office archetype. Circle drawn in the air; no numerals. | needed |
| 126 | `inwerken-in-de-functie.png` | inwerken in | to train someone into | One person stands behind a seated newcomer and guides their hand towards a switch panel on a wall | Learning a job from a colleague; pair with `zich-inwerken-in-het-systeem`. | needed |
| 127 | `zich-inwerken-in-het-systeem.png` | zich inwerken in | to work one's way into, to master | One person sits alone at a desk with a thick manual propped open against a small stand and one finger following a… | Self-study into a system; pair with `inwerken-in-de-functie`. | needed |
| 128 | `onderhandelen-over-het-contract.png` | onderhandelen over | to negotiate about | Two people sit opposite each other at a table with a blank contract sheet between them and one pencil turned towards… | Single. Working out terms together. | needed |
| 129 | `solliciteren-naar-een-functie.png` | solliciteren naar | to apply for | One person sits on the far side of a desk with a blank sheet held in both hands, back straight | Single. Applying for a job. | needed |
| 130 | `een-vergoeding-krijgen-voor-de-kosten.png` | een vergoeding krijgen voor | to be reimbursed for | One person holds out a small pile of plain receipts in one hand towards another who counts them into a tin box with… | Single. Office. Receipts are plain rectangles; no currency marks. | needed |
| 131 | `omgaan-met-moeilijke-klanten.png` | omgaan met | to deal with | One person stands behind a counter with one hand open and the other steady on the counter, facing a customer who… | Single. Counter archetype, reused; same camera as `ervaring-met-moeilijke-klanten`. | needed |
| 132 | `omspringen-met-de-tijd.png` | omspringen met | to handle, to deal with | One person holds a large clock face with tick marks loose in both hands, tilted like a tray, with a small pile of… | Single. Using time carelessly. | needed |
| 133 | `afstemmen-op-de-ander.png` | afstemmen op | to align with | Two people sit side by side turning a shared dial panel with two sets of small marks until one hand on the dial… | Bringing two things into line; pair with `zich-aanpassen-aan-de-collega`. | needed |
| 134 | `zich-aanpassen-aan-de-collega.png` | zich aanpassen aan | to adapt to | One person changes their standing stance to copy the posture of a colleague beside them, both now with arms crossed… | Adjusting yourself to another; pair with `afstemmen-op-de-ander`. | needed |
| 135 | `toezien-op-de-veiligheid.png` | toezien op | to supervise | One person stands at the edge of a room with both hands behind the back, watching three others at a low bench… | Keeping watch over work; pair with `ingrijpen-bij-een-conflict`. | needed |
| 136 | `ingrijpen-bij-een-conflict.png` | ingrijpen bij | to step in on | One person steps between two others who lean towards each other with hands raised, both arms spread flat to separate… | Stepping into the middle; pair with `toezien-op-de-veiligheid`. | needed |
| 137 | `delegeren-aan-een-collega.png` | delegeren aan | to delegate to | One person places a plain folder into the open hands of a colleague and lets go, stepping back half a pace | Passing work on; pair with `samenwerken-met-de-afdeling`. | needed |
| 138 | `samenwerken-met-de-afdeling.png` | samenwerken met | to cooperate with | Two people stand on either side of a large panel, each holding one edge, and lift it together | Shared work by several; pair with `delegeren-aan-een-collega`. | needed |
| 139 | `een-overzicht-bijhouden-van.png` | een overzicht bijhouden van | to keep track of | One person stands at a high desk with a long ruled sheet clipped to a board and a pen making a short mark beside an… | Single. Office. Ruled lines only, no words or numbers. | needed |
| 140 | `terugkoppelen-aan-het-team.png` | terugkoppelen aan | to report back to | One person stands at the end of a table and speaks with one hand open towards five seated figures, a folder closed… | Single. Meeting archetype, reused. | needed |
| 141 | `solliciteren-op-een-vacature.png` | solliciteren op | to apply for | One person sits at a plain table with a blank form and a pen, the pen already lifted, looking at a single empty… | Single. Writing to get a job; same camera as `een-punt-zetten-achter-de-klus`. | needed |
| 142 | `een-einde-maken-aan-het-contract.png` | een einde maken aan | to put an end to | One person tears a plain sheet across the middle with both hands, the tear running from the top edge | Ending an agreement; pair with `het-contract-verlengen-met-een-jaar`. | needed |
| 143 | `het-contract-verlengen-met-een-jaar.png` | verlengen met | to extend by | One person—who is the same sexless neutral figure—holds a blank sheet and adds another blank sheet edge to edge… | Making an agreement longer; pair with `een-einde-maken-aan-het-contract`. | needed |
| 144 | `zich-afmelden-voor-het-abonnement.png` | zich afmelden voor | to cancel, to unsubscribe from | One person holds a plain card in one hand and a pair of plain scissors in the other, about to close the blades… | Single. Office. No card text or magnetic stripe detail. | needed |
| 145 | `overnemen-van-de-voorganger.png` | overnemen van | to take over from | One person is handed a plain key ring by a departing figure who already has a bag over one shoulder and one foot… | Single. Inheriting a role. | needed |
| 146 | `zich-aanmelden-bij-de-balie.png` | zich aanmelden bij | to sign up with | One person stands at a counter with a ruled blank list on a clipboard and a pen held ready, one box already marked… | Single. Counter archetype, reused. One mark only; no letters; same camera as `benoemen-tot-teamleider`. | needed |
| 147 | `een-klacht-in-ontvangst-nemen.png` | in ontvangst nemen | to receive, to take in | One person nods and takes a folded note from an angry customer's hand, the other hand open and raised slightly to calm | Receiving a complaint calmly; pair with `de-klacht-overdragen-aan-een-collega`. | needed |
| 148 | `de-klacht-overdragen-aan-een-collega.png` | overdragen aan | to hand over to | The same three figures as #7: the clerk now hands the folded note over a desk to a colleague who reads it, the… | Counter and office archetypes; pair with `een-klacht-in-ontvangst-nemen`. | needed |
| 149 | `opleiden-tot-vakman.png` | opleiden tot | to train as, to train into | One person guides a younger figure's hands on a plain tool held over a workbench, both bent over the same small object | Teaching a trade; pair with `uitvoeren-volgens-plan`. | needed |
| 150 | `uitvoeren-volgens-plan.png` | uitvoeren volgens | to carry out according to | One person sets out plain blocks on a bench in the order drawn on a single blank ruled sheet propped against a small… | Working to a written plan; pair with `opleiden-tot-vakman`. | needed |
| 151 | `beschikken-over-de-vrije-tijd.png` | beschikken over de vrije tijd | to have one's free time | One person sits on a low step with both hands behind the head and legs stretched out, an open book face down beside… | Single. Leisure is the absence of objects; same camera as `genieten-van-de-stilte`. | needed |
| 152 | `bewogen-worden-tot-hulp.png` | bewogen worden tot | to be moved to | One person steps forward and places a hand flat on the shoulder of a second who sits hunched on a bench | Single. An inner push to act. | needed |
| 153 | `waarschuwen-voor-gevaar.png` | waarschuwen voor | to warn against | One person stands well back from the edge of a step and holds out a flat hand towards a second figure who walks… | Stopping someone in time; pair with `gedwongen-zijn-tot-uitstel`. | needed |
| 154 | `gedwongen-zijn-tot-uitstel.png` | gedwongen zijn tot | to be forced into | One person stands at a closed door with a blank sheet in one hand and the other flat against the door, shoulders… | Single. The closed door is the pressure; no lock detail; pair with `waarschuwen-voor-gevaar`. | needed |
| 155 | `getuigen-over-de-gebeurtenis.png` | getuigen over | to give evidence about | One person sits on a plain chair in an otherwise empty room with both hands on the knees and head level, speaking… | Single. Courtroom archetype, reused. | needed |
| 156 | `te-kampen-hebben-met-tegenstand.png` | te kampen hebben met | to struggle with, to be faced with | One person pushes a wheeled cart up a shallow slope, body leaning into it and both hands on the handlebar | Single. Struggling against resistance; the slope is subtle; do not turn it into a mountain. | needed |
| 157 | `uitkomen-voor-de-fout.png` | uitkomen voor | to own up to, to admit | One person says aloud with one hand on the chest and the other lifted open, and the listener beside them has… | Admitting a fact about oneself; pair with `bezwaar-maken-tegen-de-claim`. | needed |
| 158 | `bezwaar-maken-tegen-de-claim.png` | bezwaar maken tegen | to object to | One person shakes their head with one hand flat and raised like a stop, while a second holds up a blank sheet… | Saying that is not true; pair with `uitkomen-voor-de-fout`. | needed |
| 159 | `voldoen-aan-de-eisen.png` | voldoen aan | to meet, to satisfy | One person stands with a long plain checklist on a board held in one arm and ticks the final point with a finger | Single. Office. The checklist is ruled with tick marks only. | needed |
| 160 | `overtuigd-zijn-van-het-tegendeel.png` | overtuigd zijn van | to be convinced of | One person stands with chin lifted and both arms folded, looking steadily at a second figure who points at a plain… | Single. Keep the folded arms identical to the earlier folded-arms door frame so the posture reads as refusal. | needed |
| 161 | `genieten-van-de-stilte.png` | genieten van | to enjoy | One person sits with eyes closed and the head tilted back slightly in a room with a single open window, both hands… | Single. Pleasure in quiet; same camera as `beschikken-over-de-vrije-tijd`. | needed |
| 162 | `terugdeinzen-voor-de-klus.png` | terugdeinzen voor | to shrink back from | One person steps back with one hand raised palm outward in front of a cluttered workbench and a heavy tool lying on… | Single. Pulling away from work. | needed |
| 163 | `opdraaien-voor-de-kosten.png` | opdraaien voor | to bear, to be liable for | One person holds out both hands open beneath a small pile of plain receipts held by another figure, who is about to… | Office archetype, reused; pair with `afzien-van-de-vergoeding`. | needed |
| 164 | `afzien-van-de-vergoeding.png` | afzien van | to forgo | One person holds the same plain receipts in both hands and pushes them back towards the other figure with a flat… | Giving up a claim; pair with `opdraaien-voor-de-kosten`. | needed |
| 165 | `berusten-op-een-vermoeden.png` | berusten op | to rest on, to be founded on | One person stands with one hand flat on a small plain stone block and looks towards a second who holds up an empty… | Single. Pair available with the earlier block frame; the hand is empty here. | needed |
| 166 | `uitmonden-in-een-akkoord.png` | uitmonden in | to result in, to end in | Two people stand facing each other with the near hands joined in a handshake while their other hands still hold… | Single. An outcome reached at last. | needed |
| 167 | `instaan-voor-de-kwaliteit.png` | instaan voor | to vouch for | One person lays one hand flat on a plain finished object on a bench and the other hand on the chest, facing a… | Single. Standing behind the work. | needed |
| 168 | `gebukt-gaan-onder-de-druk.png` | gebukt gaan onder | to labour under | One person carries a large plain sack on the back with both straps in the hands, knees bent and neck lowered | Carrying a heavy burden; same camera as `een-loden-last-met-zich-meedragen`; pair with `delen-in-het-succes`. | needed |
| 169 | `delen-in-het-succes.png` | delen in | to share in | Two people stand beside a plain podium with one hand each on its edge, both turned towards the viewer with heads level | Sharing a result together; pair with `gebukt-gaan-onder-de-druk`. | needed |
| 170 | `uitblinken-in-een-vak.png` | uitblinken in | to excel at | One person stands at a bench holding up a plain finished object with both hands above head height, while three… | Single. The raised object is the whole idea. | needed |
| 171 | `uitwijken-naar-de-zijkant.png` | uitwijken naar | to move aside to | One person steps sideways towards a plain painted margin on a wide floor while a heavy plain crate is rolled past on… | Single. No arrows; the painted margin carries the direction; same camera as `afkomen-op-het-geluid`. | needed |
| 172 | `voorbijgaan-aan-de-vraag.png` | voorbijgaan aan | to pass over, to ignore | One person walks past a second figure who holds up a blank sheet with both hands and leans towards them | Walking past a question; pair with `ingaan-op-het-verzoek`. | needed |
| 173 | `ingaan-op-het-verzoek.png` | ingaan op | to go into, to accept | One person sits down on a chair opposite a standing figure who holds the same blank sheet, one hand already open… | Accepting someone's request; pair with `voorbijgaan-aan-de-vraag`. | needed |
| 174 | `afkomen-op-het-geluid.png` | afkomen op | to come towards, to head for | One person walks quickly towards a small plain bell on a table with one hand already out, drawn from the far side of… | Single. Moving towards a signal; same camera as `uitwijken-naar-de-zijkant`. | needed |
| 175 | `terugkomen-op-een-besluit.png` | terugkomen op | to return to, to reverse | One person stands at a desk with a blank sheet in one hand and draws it back towards the chest while a finger of the… | Reversing what was decided; pair with `zich-neerleggen-bij-het-besluit`. | needed |
| 176 | `zich-neerleggen-bij-het-besluit.png` | zich neerleggen bij | to resign oneself to | One person opens both hands palms down above a table and lets a blank sheet fall flat onto it, both hands lifting away | Dropping an idea; pair with `terugkomen-op-een-besluit`. | needed |
| 177 | `voortborduren-op-een-idee.png` | voortborduren op | to build on | One person places a second plain block onto a small stack already begun by a colleague and taps the top block once | Single. Continuing another's work. | needed |
| 178 | `vasthouden-aan-het-standpunt.png` | vasthouden aan | to stick to | One person grips the edge of a desk with both hands and leans forward, chin down, while a second figure has both… | Refusing to give ground; pair with `toegeven-aan-de-druk`. | needed |
| 179 | `toegeven-aan-de-druk.png` | toegeven aan | to give in to | One person lets go of the same desk edge and settles back into the chair, shoulders dropping, while the appealing… | Giving way; pair with `vasthouden-aan-het-standpunt`. | needed |
| 180 | `afhangen-van-een-telefoontje.png` | afhangen van | to depend on | One person sits with a plain telephone receiver held to the ear and one hand flat on the table, waiting | Single. Office. The empty chair carries the doubt; no numbers on the receiver. | needed |
| 181 | `afhankelijk-van-een-uitkering.png` | afhankelijk van | to depend on | One person stands with an open hand underneath a plain sheet being held out by a second figure | Leaning on someone's support; pair with `gehecht-aan-de-eigen-buurt`. | needed |
| 182 | `gehecht-aan-de-eigen-buurt.png` | gehecht aan | to be attached to | One person stands with one hand flat against the outside wall of a plain building and the other resting over the… | Belonging to a place; pair with `afhankelijk-van-een-uitkering`. | needed |
| 183 | `bereid-tot-een-gesprek.png` | bereid tot | to be willing to | One person pulls an empty chair out from a table with both hands and turns it towards a second figure, one hand open… | Ready to talk; pair with `bereid-tot-opoffering`. | needed |
| 184 | `bereid-tot-opoffering.png` | bereid tot | to be prepared to | One person stands with one hand on the back of a chair and the other held out flat, offering the better seat to a… | Giving up something for another; pair with `bereid-tot-een-gesprek`. | needed |
| 185 | `geschikt-voor-kinderen.png` | geschikt voor | to be suitable for | One person hands a small plain rounded object to a small figure with both hands, while the small figure holds… | Single. Right for someone young. | needed |
| 186 | `geschikt-voor-een-krappe-ruimte.png` | geschikt voor | to be suitable for | One person crouches in a narrow gap between two plain walls, turning a flat board sideways with both hands to fit it… | Single. The two walls are close and parallel. | needed |
| 187 | `tevreden-over-de-uitslag.png` | tevreden over | to be satisfied with | One person sits with a blank sheet held loosely in one hand and leans back, a single raised line for a smile | Pleased with a result; pair with `trots-op-het-kind`. | needed |
| 188 | `trots-op-het-kind.png` | trots op | to be proud of | One person stands behind a small figure with both hands on the small figure's shoulders, chin up and chest forward,… | Pride in someone; same camera as `trots-op-de-eigen-afkomst`; pair with `tevreden-over-de-uitslag`. | needed |
| 189 | `verantwoordelijk-voor-de-veiligheid.png` | verantwoordelijk voor | to be responsible for | One person stands at the foot of a plain flight of steps with a hand on the rail, looking up at two figures on the… | Single. Three figures at most; the rail and steps are the mass. | needed |
| 190 | `verlegen-om-een-antwoord.png` | verlegen om | to be short of, to need | One person stands with both hands open and empty in front of a second figure who has turned their back and is… | Single. Empty open hands, back turned. | needed |
| 191 | `aandacht-voor-de-details.png` | aandacht voor | attention for | One person leans low over a small object on a bench, both hands framing it, while another larger object beside it is… | Close attention to small things; pair with `onverschillig-voor-de-uitslag`. | needed |
| 192 | `onverschillig-voor-de-uitslag.png` | onverschillig voor | indifferent to | One person accepts a blank sheet held out by another with a loose grip and turns it face down on the table without… | Not caring about a result; pair with `aandacht-voor-de-details`. | needed |
| 193 | `tevreden-met-de-uitkomst.png` | tevreden met | to be satisfied with | One person holds a plain cup with both hands and sits back with shoulders relaxed, a single line for a smile | Single. Content with what there is. | needed |
| 194 | `vertrouwd-met-het-systeem.png` | vertrouwd met | to be familiar with | One person's hands move easily over a plain control panel, two switches already turned, without looking down | Single. Knowing something by habit. | needed |
| 195 | `belangrijk-voor-de-zaak.png` | belangrijk voor | to matter to | One person holds up a single plain block between two fingers and turns to a seated figure who has leaned forward,… | Single. Something that counts. | needed |
| 196 | `bezorgd-om-de-lage-cijfers.png` | bezorgd om | to be worried about | One person sits with a plain sheet of three descending horizontal bars in both hands, eyebrows drawn down, and turns… | Office. The bars are plain, heights only; pair with `tevreden-over-het-werk`. | needed |
| 197 | `afhankelijk-van-goed-weer.png` | afhankelijk van | to depend on | One person stands with a folded plain tarp in both hands, looking up at three small cloud shapes | Single. Workshop and open-air scene; same camera as `met-het-oog-op-de-toekomst`. | needed |
| 198 | `tevreden-over-het-werk.png` | tevreden over | to be satisfied with | One person steps back half a pace from a plain painted wall with a roller in one hand, head tilted, both edges of… | Happy with the job done; same camera as `er-met-de-pet-naar-gooien` and `op-de-tong-liggen`; pair with `bezorgd-om-de-lage-cijfers`. | needed |
| 199 | `verantwoordelijk-voor-de-afdeling.png` | verantwoordelijk voor | to be responsible for | One person stands at a doorway with one hand open towards the room behind them, in which four figures sit at desks | Single. Office. Keep the four at desks low and small. | needed |
| 200 | `trots-op-de-eigen-afkomst.png` | trots op | to be proud of | One person stands with one arm across the chest and the other lifted open, facing a plain repeated shape drawn three… | Single. Pride in where one comes from; same camera as `trots-op-het-kind`. | needed |
| 201 | `behoefte-aan-stilte.png` | behoefte aan | need for | One person lies flat on a plain bench with an arm across the eyes and both legs along the bench | Single. The bench is the only furniture. | needed |
| 202 | `kans-op-een-baan.png` | kans op | chance of | One person stands at a door with a blank sheet in one hand and the other hand raised towards a plain knocker shape… | A possibility that must be tried; pair with `risico-op-een-ongeluk`. | needed |
| 203 | `risico-op-een-ongeluk.png` | risico op | to risk of | One person walks along a narrow raised edge with arms spread for balance, one foot just ahead of the other | The danger of falling; pair with `kans-op-een-baan`. | needed |
| 204 | `moeite-met-de-uitspraak.png` | moeite met | difficulty with | One person sits facing a second figure and holds one hand near the mouth while the listener leans in, one hand… | Single. Struggling to be understood; same camera as `zin-in-een-ommetje`. | needed |
| 205 | `zin-in-een-ommetje.png` | zin in | a wish for, in the mood for | One person stands in an open doorway with a plain pair of boots already in one hand and one hand on the door frame,… | Single. Reuse of the shipped chunk with a new object; the doorway does the work; same camera as `moeite-met-de-uitspraak`. | needed |
| 206 | `belang-bij-een-oplossing.png` | belang bij | interest in | One person sits at a table with both hands on top of a loose blank sheet, leaning forward, while a second figure… | Having a stake in the answer; pair with `gebrek-aan-handen`. | needed |
| 207 | `gebrek-aan-handen.png` | gebrek aan | lack of | One person stands with an upturned empty bag open at the bottom and gives it a small shake | Running out of time; same camera as `kennis-van-de-regels`; pair with `belang-bij-een-oplossing`. | needed |
| 208 | `verband-tussen-roken-en-longklachten.png` | verband tussen | connection between | Two plain objects are drawn apart on a table, a rolled paper tube on one side and a small round form on the other,… | Single. The tube is not to be drawn as a recognisable cigarette; a rolled paper is enough. | needed |
| 209 | `vertrouwen-in-de-afspraak.png` | vertrouwen in | trust in | One person stands with head up and both hands open at the sides, facing a wide gap between two tall plain blocks | Single. Belief in what comes next. | needed |
| 210 | `twijfel-aan-de-bedoeling.png` | twijfel aan | doubt about | One person holds a blank sheet at arm's length with one hand and tilts it, one shoulder raised, mouth pulled to one… | Single. Not understanding the intent. | needed |
| 211 | `reden-voor-de-klacht.png` | reden voor | reason for | One person stands at a counter with a broken plain appliance held in both hands, showing it to a clerk who leans… | Justification for complaining; pair with `beschuldiging-van-diefstal`. | needed |
| 212 | `beschuldiging-van-diefstal.png` | beschuldiging van | accusation of | One person points a flat hand at a second figure's open bag on a table, while the bag's owner stands with both hands… | Being blamed for taking something; pair with `reden-voor-de-klacht`. | needed |
| 213 | `oplossing-voor-de-storing.png` | oplossing voor | solution for | One person places a plain key into a socket on a large closed box and turns it | Something that unlocks a difficulty; pair with `gevolg-van-een-fout`. | needed |
| 214 | `gevolg-van-een-fout.png` | gevolg van | consequence of | One person stands looking at a plain wall panel with a long crack running down it while a second figure lowers their… | What a mistake leaves behind; pair with `oplossing-voor-de-storing`. | needed |
| 215 | `ervaring-met-moeilijke-klanten.png` | ervaring met | experience with | One person stands behind a counter and listens calmly with both hands on the counter as a customer leans over it… | Single. Having dealt with this before; same camera as `omgaan-met-moeilijke-klanten`. | needed |
| 216 | `kennis-van-de-regels.png` | kennis van | knowledge of | One person holds a small ruled booklet open in both hands and taps one page while a standing colleague looks on with… | Single. Office. Ruled pages only, no letters; same camera as `gebrek-aan-handen`. | needed |
| 217 | `invloed-op-de-uitslag.png` | invloed op | influence on | One person leans over a table and moves one of three plain blocks with a single finger while two seated figures… | Changing an outcome; pair with `gebrek-aan-informatie`. | needed |
| 218 | `gebrek-aan-informatie.png` | gebrek aan | lack of | One person holds an open empty folder towards a colleague and turns both hands palm up | Nothing to go on; pair with `invloed-op-de-uitslag`. | needed |
| 219 | `oorzaak-van-de-vertraging.png` | oorzaak van | cause of | One person kneels beside a stalled machine with a loose belt hanging in one hand, while another figure checks the… | What held everything up; pair with `belangstelling-voor-het-onderwerp`. | needed |
| 220 | `belangstelling-voor-het-onderwerp.png` | belangstelling voor | interest in | One person leans across a table towards a small plain object with both hands lifted open, eyes fixed on it | Keen attention to a subject; pair with `oorzaak-van-de-vertraging`. | needed |
| 221 | `op-de-hoogte-zijn-van-de-plannen.png` | op de hoogte zijn van | to be informed about | One person stands with a folded blank paper in one hand and touches the brow with the fingers of the other, a small… | Having the news; same camera as `met-succes-afronden-van-de-klus` and `niet-op-de-hoogte-zijn`; pair with `op-de-hoogte-houden-van-het-nieuws`. | needed |
| 222 | `op-de-hoogte-houden-van-het-nieuws.png` | op de hoogte houden van | to keep informed of | One person hands a folded blank paper to a colleague who is seated and reaching for it, the giver's other hand still… | Passing news on; same camera as `een-bericht-plaatsen-op-de-voorpagina`; pair with `op-de-hoogte-zijn-van-de-plannen`. | needed |
| 223 | `op-de-hoogte-brengen-van-het-plan.png` | op de hoogte brengen van | to inform about | One person stands talking to a seated figure, one hand open and the other holding a rolled blank sheet that is not… | Single. Office. The rolled sheet is the marker. | needed |
| 224 | `rekening-houden-met-het-verkeer.png` | rekening houden met | to take into account | One person stops at a kerb and looks both ways, one hand steadying a plain bag | Single. The distant moving shape carries the traffic; pair with `rekening-houden-met-de-gevoelens`. | needed |
| 225 | `rekening-houden-met-de-gevoelens.png` | rekening houden met | to take into account | Two people sit facing each other, one leaning forward with both hands raised gently open | Same chunk, other sense; pair with `rekening-houden-met-het-verkeer`. | needed |
| 226 | `tot-stand-brengen-van-een-akkoord.png` | tot stand brengen | to bring about | Two people push a heavy plain slab upright together so that its top edge stands level | Single. Getting something done. | needed |
| 227 | `ter-beschikking-stellen-van-ruimte.png` | ter beschikking stellen van | to make available to | One person opens both arms towards a bare room with a table and two chairs, one hand flat towards the table top | Offering a place to use; pair with `gebruik-maken-van-de-kans`. | needed |
| 228 | `gebruik-maken-van-de-kans.png` | gebruik maken van | to make use of | One person steps through an open doorway with one hand already on the frame and a plain bag in the other, head… | Seizing an offered opening; pair with `ter-beschikking-stellen-van-ruimte`. | needed |
| 229 | `in-het-oog-houden-van-de-klant.png` | in het oog houden | to keep an eye on | One person stands behind a counter with both hands flat on its top, watching a customer move through a plain room | Watching while others move; pair with `tekortschieten-in-de-dienstverlening`. | needed |
| 230 | `tekortschieten-in-de-dienstverlening.png` | tekortschieten in | to fall short in | One person behind the counter has both hands open and empty over the counter while a customer taps the counter top… | Failing to deliver; pair with `in-het-oog-houden-van-de-klant`. | needed |
| 231 | `in-het-kader-van-het-project.png` | in het kader van | within the framework of | One person holds a large plain frame of four joined planks upright and stands behind it, with a second figure… | Single. Office. The frame is empty, not a picture. | needed |
| 232 | `met-succes-afronden-van-de-klus.png` | met succes afronden | to complete successfully | One person sets the last of a short row of plain boxes onto a shelf, both hands still on it, while a colleague… | Single. Finishing well; same camera as `op-de-hoogte-zijn-van-de-plannen`. | needed |
| 233 | `een-verzoek-indienen-bij-de-afdeling.png` | een verzoek indienen bij | to submit a request to | One person slides a blank envelope into a slot in a plain wall panel | Handing paperwork onward; pair with `afgehandeld-worden-door-de-afdeling`. | needed |
| 234 | `afgehandeld-worden-door-de-afdeling.png` | afgehandeld worden door | to be dealt with by | One seated figure takes the same blank envelope out of a tray and slits it open with a small plain knife, a stack of… | The paperwork lands on someone's desk; pair with `een-verzoek-indienen-bij-de-afdeling`. | needed |
| 235 | `in-het-beheer-zijn-van-de-directie.png` | in het beheer zijn van | to be managed by | One person hands a plain key to another, who closes both hands over it | Single. Control passing to someone else. | needed |
| 236 | `de-verantwoordelijkheid-dragen-voor-het-budget.png` | de verantwoordelijkheid dragen voor | to carry responsibility for | One person holds a large plain ledger book in both arms against the chest, chin just above the top edge of it | Single. Office. The ledger is plain; no columns of numbers. | needed |
| 237 | `zich-verantwoorden-voor-het-bestuur.png` | zich verantwoorden voor | to account for oneself to | One person stands facing three seated figures at a long table, both hands open and lowered | Meeting archetype, reused; pair with `verantwoording-afleggen-aan-de-leden`. | needed |
| 238 | `verantwoording-afleggen-aan-de-leden.png` | verantwoording afleggen aan | to give an account to | The same three seated figures receive one standing figure who now holds a plain sheet open in both hands, showing it… | Showing the numbers to the members; pair with `zich-verantwoorden-voor-het-bestuur`. | needed |
| 239 | `de-waarde-bepalen-van-het-object.png` | de waarde bepalen van | to determine the value of | One person holds a straight rule against a plain object on a table while a second figure writes on a small pad held… | Single. Working out what something is worth. | needed |
| 240 | `een-factuur-versturen-naar-de-klant.png` | een factuur versturen naar | to send an invoice to | One person folds a blank sheet into an envelope and holds it above a plain outgoing tray | Single. Billing someone afterwards; same camera as `een-offerte-uitbrengen-aan-een-klant`. | needed |
| 241 | `de-vinger-op-de-zere-plek-leggen.png` | de vinger op de zere plek leggen | to put one's finger on the sore spot | One person presses a single finger flat onto a small plain patch on a colleague's shoulder while the colleague… | Single. Office. The patch is a shape, not a wound. | needed |
| 242 | `olie-op-het-vuur-gooien.png` | olie op het vuur gooien | to add fuel to the fire | One figure stands between two others leaning towards each other with fists, and tips a plain can forward over their… | Single. The flame is a simple shape with no detail. | needed |
| 243 | `een-klap-in-het-gezicht-zijn.png` | een klap in het gezicht zijn | to be a slap in the face | One person turns their head sharply aside with one hand raised to the cheek while a second figure behind stands with… | Single. Office. The sheet is the thing that stings, not a hand; same camera as `zich-herinneren-aan-naam`. | needed |
| 244 | `met-de-deur-in-huis-vallen.png` | met de deur in huis vallen | to come straight to the point | One person steps through an already open door with one foot in the room and one hand already pointing at a table | Single. Office. The door is open and the step is mid-way. | needed |
| 245 | `niet-op-de-hoogte-zijn.png` | niet op de hoogte zijn | to be unaware | One person looks up from a plain desk with a tilted head and both hands flat, towards a second figure who holds a… | Single. The news has not arrived; same camera as `op-de-hoogte-zijn-van-de-plannen`. | needed |
| 246 | `ophef-maken-over-een-klein-probleem.png` | ophef maken over | to make a fuss about | One person stands with both arms flung back and mouth open wide while two others turn to look with raised eyebrows | Single. Office. One figure only shouting; the others are still. | needed |
| 247 | `tegen-de-klippen-opzien.png` | tegen de klippen opzien | to dread something | One person stands at the bottom of a steep plain slope with a hand shading the eyes, looking up | Single. The slope is one line; the blocks are the only objects at the top. | needed |
| 248 | `geduld-hebben-met-de-drukte.png` | geduld hebben met | to be patient with | One person stands with a plain ticket in one hand and the other hand resting patiently at the side | Single. Counter archetype. The ticket is the patience marker. | needed |
| 249 | `de-vruchten-plukken-van-het-werk.png` | de vruchten plukken van het werk | to reap the rewards | One person stands beside a small plain tree with three round fruit shapes on it, one hand already cupped around the… | Single. The tree is a simple trunk and three circles. | needed |
| 250 | `niet-door-de-mandel-kunnen.png` | niet door de mand kunnen vallen | to be exposed | One person stands on a plain bench with one foot on the edge of a woven basket that is giving way beneath them, arms… | Single. The basket is a plain woven oval with simple crossing lines. | needed |

## Batch B1+-01 — images 1–10

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `zich-herinneren-aan-naam.png` — Dutch chunk: zich herinneren aan (to remember).
   Scene: One person stands still in an open doorway with a hand flat on the forehead and a small blank thought bubble drawn beside the head; the bubble holds a single round face outline. The doorway frame is the largest mass.
   Must read: stopping to recall something.
   Avoid: a calendar or an appointment; a notebook; the pilot face-in-bubble scene with no doorway.

2. `zich-verdiepen-in-boek.png` — Dutch chunk: zich verdiepen in (to immerse oneself in).
   Scene: One person is bent low over a single open book on a plain table, elbows planted, forehead almost on the page; a cup and a phone are pushed to the far edge of the table.
   Must read: complete absorption in one text.
   Avoid: a sleeping person; a computer screen; a second person at the table.

3. `zich-bezighouden-met-klus.png` — Dutch chunk: zich bezighouden met (to occupy oneself with).
   Scene: One person kneels on the floor with both hands inside an open box of loose parts, sorting them into two small plain piles; the box and piles fill the lower half.
   Must read: keeping oneself busy with a practical job.
   Avoid: a person resting; a second person watching; a finished object.

4. `zich-verzetten-tegen-plan.png` — Dutch chunk: zich verzetten tegen (to resist, to oppose).
   Scene: One person stands with both arms braced flat against a large board being pushed towards them by two others; the person's heels are dug in and the body leans back.
   Must read: pushing back against something.
   Avoid: an argument with speech bubbles; a sports push; a person leaning against a wall alone.

5. `zich-schikken-naar-beslissing.png` — Dutch chunk: zich schikken naar (to comply with, to accept).
   Scene: One person stands with both hands lowered and head slightly bowed in front of a large blank board held upright by another; nobody is pushing, and the space between them is calm.
   Must read: accepting an order.
   Avoid: a person reading a notice; a handshake; a queue.

6. `zich-ergeren-aan-geluid.png` — Dutch chunk: zich ergeren aan (to be annoyed by).
   Scene: One person sits at a table with both hands pressed over the ears and eyes squeezed shut; an open window behind lets in a row of plain sound strokes.
   Must read: irritation at noise.
   Avoid: a person crying; a radio with readable buttons; two people arguing.

7. `zich-vermaken-met-spel.png` — Dutch chunk: zich vermaken met (to amuse oneself with).
   Scene: One person sits on the floor with a small board game laid out and both hands raised mid-move, mouth open in delight; a single other seat is empty.
   Must read: enjoying a game alone.
   Avoid: a crowd at a party; a person bored at the same board; a phone.

8. `zich-iets-voorstellen-bij-het-huis.png` — Dutch chunk: zich iets voorstellen bij (to picture something by).
   Scene: One person stands with one hand open towards a large blank thought bubble in which a simple house outline floats, fully drawn; the person looks up at it.
   Must read: picturing something that is not there.
   Avoid: a builder with tools; a photo on the wall; a real house in the street.

9. `zich-haasten-naar-de-trein.png` — Dutch chunk: zich haasten naar (to rush to).
   Scene: One person runs with the body tipped forward, one arm swinging and a bag bouncing behind; an open train door stands at the edge of the frame ahead of them.
   Must read: rushing towards a place.
   Avoid: a person jogging for sport; a bus; a pile of luggage.

10. `zich-afsluiten-voor-geluid.png` — Dutch chunk: zich afsluiten voor (to shut oneself off from).
   Scene: One person sits inside a large plain box open on one side, knees drawn up and hands on the head; outside the box a row of plain sound strokes bounces off the wall.
   Must read: cutting oneself off.
   Avoid: a person in a wardrobe; a person hiding in play; a second person knocking.

CONTRAST PAIRS
Subjects one and three carry the reflexive verb itself as a task: a pause to recall, and a box of loose parts to sort. The reflexivity is posture, never a mirror or a second self.
Four and five are `zich verzetten tegen` against `zich schikken naar`: the same blank board pushed by two people, once resisted and once accepted. In subject four the figure leans back with heels dug in; in subject five the figure yields with both hands down.
Six and seven share one seat and one table: irritation with hands over the ears, then delight with both hands raised over a board game. Change only the hands and the mood.
Two, eight, nine and ten are singles. Nine is the only frame with speed in it; the tipped body carries it, and there is no motion stroke on the ground.

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

## Batch B1+-02 — images 11–20

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `zich-ontfermen-over-kind.png` — Dutch chunk: zich ontfermen over (to take under one's wing).
   Scene: One tall person wraps a coat around a small figure's shoulders from behind, both hands on the coat collar; the small figure is turned slightly away.
   Must read: sheltering someone smaller.
   Avoid: a hug; a rescue from water; two adults of equal height.

2. `zich-bedienen-van-hulp.png` — Dutch chunk: zich bedienen van (to make use of, to avail oneself of).
   Scene: One person holds a short plain stick out towards a high shelf and lifts a box down with it, other hand steadying the shelf; the stick is the main diagonal.
   Must read: using a tool to get something.
   Avoid: a walking stick; a pointer in a classroom; a person climbing on a chair.

3. `zich-richten-tot-publiek.png` — Dutch chunk: zich richten tot (to address oneself to).
   Scene: One person stands at the front of a small group of seated figures, one arm open wide towards them and the head turned to the group; the group is drawn as three rounded backs.
   Must read: speaking to an audience.
   Avoid: a teacher at a board with readable text; a queue at a counter; a phone call.

4. `zich-wenden-tot-balie.png` — Dutch chunk: zich wenden tot (to turn to, to approach).
   Scene: One person stands at a counter and leans in towards a clerk, one hand resting on the counter edge; the clerk has turned their head towards them.
   Must read: asking someone for help at a desk.
   Avoid: a queue of people; a cash register with numbers; a phone.

5. `zich-ontdoen-van-afval.png` — Dutch chunk: zich ontdoen van (to dispose of).
   Scene: One person tips a bin bag into a large container with a hinged lid, one hand holding the lid up and the bag already half empty; nothing spills.
   Must read: getting rid of something.
   Avoid: a recycling symbol; a person throwing litter on the ground; a shopping bag.

6. `zich-herstellen-van-ziekte.png` — Dutch chunk: zich herstellen van (to recover from).
   Scene: One person sits up in a bed with a blanket to the waist and a bowl on a side table, back straight and face calm; a folded walking stick leans on the wall.
   Must read: getting better after illness.
   Avoid: a hospital with a cross; a doctor; a person in pain.

7. `zich-verdiepen-in-de-zaak.png` — Dutch chunk: zich verdiepen in (to go into, to study).
   Scene: One person holds a large open folder with both hands and leans into it, head lowered; three loose sheets slide off the folder's edge towards the floor.
   Must read: digging into a dossier.
   Avoid: a person reading a newspaper; a laptop; a second person across a desk.

8. `zich-laten-leiden-door-advies.png` — Dutch chunk: zich laten leiden door (to be guided by).
   Scene: One person walks forward behind a blindfolded figure who holds a short plain stick in front and points it forward; one hand of the follower rests on the leader's shoulder.
   Must read: being steered by another's judgement.
   Avoid: a police arrest; a game of blind man's buff; a person alone with a stick.

9. `zich-neerleggen-bij-uitslag.png` — Dutch chunk: zich neerleggen bij (to accept, to resign oneself to).
   Scene: One person sits with shoulders dropped and both hands open on the knees, looking down at a single plain sheet lying flat on the floor in front of them.
   Must read: giving up the argument.
   Avoid: a person asleep; a person reading a letter; two people shaking hands.

10. `zich-verheugen-op-feest.png` — Dutch chunk: zich verheugen op (to look forward to).
   Scene: One person stands at a mirrorless wall with a small blank invitation card in one hand and the other hand already raised, chin up and mouth open in a smile; a hanging string of plain paper shapes is behind them.
   Must read: anticipation of an event.
   Avoid: a wrapped present; a calendar with dates; a person leaving.

CONTRAST PAIRS
One and eight are both support in pairs: a coat placed around a small figure, and a blind leader followed. Keep subject 1 close and still, subject 2 walking with the stick ahead.
Three and four are `zich richten tot` against `zich wenden tot`: a group versus one clerk. In subject 3 the arm opens towards three backs; in subject 4 only the head turns towards the clerk behind the counter.
Nine is alone in the batch in showing defeat; the sheet lies on the floor and the shoulders drop.
Two, five, six, seven and ten are singles. subject 7 reuses the office archetype from later batches; keep the folder and the sliding sheets as the main shape.

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

## Batch B1+-03 — images 21–30

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `zich-inzetten-voor-de-buurt.png` — Dutch chunk: zich inzetten voor (to work hard for).
   Scene: Two people carry a long plank between them towards a low unfinished wall, both leaning into the load; a third figure waits on the wall with a hand raised.
   Must read: effort for a shared cause.
   Avoid: a protest march; a donation box with coins; a person alone lifting.

2. `zich-verzekeren-van-een-plaats.png` — Dutch chunk: zich verzekeren van (to secure, to make sure of).
   Scene: One person stands at a ticket counter with one hand on a blank ticket held close to the chest and the other hand flat on the counter; the clerk pushes a second blank ticket across.
   Must read: making certain of a place.
   Avoid: a queue at a cinema; a person waving a ticket; a phone call.

3. `zich-verlagen-tot-een-scheldwoord.png` — Dutch chunk: zich verlagen tot (to stoop to).
   Scene: One figure stands over another who points up at them with an open mouth; the standing figure has turned their head away and one hand raised flat, refusing.
   Must read: refusing to go as low as the other.
   Avoid: a boxing match; two people laughing; a person looking down a ladder.

4. `zich-vergewissen-van-de-vraag.png` — Dutch chunk: zich vergewissen van (to make sure of, to verify).
   Scene: One person holds a small plain lamp up beside a switch on a wall panel while the other hand rests on the switch; the lamp is drawn as a burst of short strokes.
   Must read: checking that something is as expected.
   Avoid: a person repairing an appliance; a torch in the dark; a tool box.

5. `zich-tegoeddoen-aan-een-maaltijd.png` — Dutch chunk: zich tegoeddoen aan (to help oneself generously to).
   Scene: One person sits at a loaded table with a full plate in both hands, leaning back with eyes closed in contentment; the plate holds three plain rounded shapes.
   Must read: eating a lot with pleasure.
   Avoid: a person on a diet; a restaurant menu; two people sharing.

6. `zich-onttrekken-aan-de-verplichting.png` — Dutch chunk: zich onttrekken aan (to withdraw from, to evade).
   Scene: One person slips sideways out of a row of standing figures towards an open door, body turned away and one foot already past the last shoulder.
   Must read: leaving a duty quietly.
   Avoid: a person being pushed out; a queue; a person alone walking.

7. `zich-voegen-bij-de-groep.png` — Dutch chunk: zich voegen bij (to join).
   Scene: One person steps into line between two standing figures, one hand raised in greeting; the row is closed on both sides of them.
   Must read: joining a group.
   Avoid: a queue at a ticket desk; a person pushing in; two people greeting only.

8. `zich-wreken-op-een-collega.png` — Dutch chunk: zich wreken op (to take revenge on).
   Scene: One person stands behind another's chair and tips it slightly backwards with both hands while the seated person grips the desk edge; the twist of the chair is the main shape.
   Must read: getting back at someone.
   Avoid: a fight with fists; a prank with laughter; two people arguing.

9. `zich-inleven-in-de-ander.png` — Dutch chunk: zich inleven in (to empathise with).
   Scene: Two people sit facing each other on low stools, the first leaning far forward with both hands open towards the second, whose shoulders have just dropped.
   Must read: understanding another's feeling.
   Avoid: a hug; a doctor examining a patient; two people laughing.

10. `zich-verplaatsen-in-de-ander.png` — Dutch chunk: zich verplaatsen in (to put oneself in the place of).
   Scene: Two people sit on low stools facing each other; the first leans forward and lays a flat hand on the second's knee, while the second has just let both shoulders drop.
   Must read: sharing another's point of view.
   Avoid: a hug; a doctor with a patient; a crowd.

CONTRAST PAIRS
One and two are both effort in a group or a queue: carrying for the neighbourhood, and securing a seat. Same standing camera; subject 1 has a plank and a wall, subject 2 a counter and a ticket.
Seven and eight are `zich onttrekken aan` against `zich voegen bij`: the same row of standing figures, once left through a door and once entered from the side. Keep the row identical in both and change only the direction of the one figure.
Three, four, five, six, nine and ten are singles. subject 6 and subject 8 reuse the table and office archetypes; the plate of food and the tipped chair must stay the dominant masses.
No arrows: direction is shown by where the feet point.

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

## Batch B1+-04 — images 31–40

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `met-betrekking-tot-de-offerte.png` — Dutch chunk: met betrekking tot (with regard to).
   Scene: One person stands beside a tall stack of plain folders and taps the top folder with one hand, looking towards a seated colleague who leans in; the stack is the tallest mass.
   Must read: referring to one particular document.
   Avoid: a press conference; a computer screen with text; a person alone reading.

2. `in-verband-met-de-verhuizing.png` — Dutch chunk: in verband met (in connection with, because of).
   Scene: One person carries a box out of a doorway while another holds the door and takes the next box; three more boxes sit stacked on the doorstep.
   Must read: linked cause for an activity.
   Avoid: a removal van with a logo; a person moving furniture alone; a shop sale.

3. `ten-behoeve-van-het-onderhoud.png` — Dutch chunk: ten behoeve van (for the benefit of).
   Scene: One person kneels with a plain oil can and a cloth beside a large machine with exposed round parts, one hand wiping a cog; a second figure holds a lamp above them.
   Must read: serving the upkeep of a machine.
   Avoid: a car garage with signs; a person fixing a bike; a donation box.

4. `ten-koste-van-de-pauze.png` — Dutch chunk: ten koste van (at the expense of).
   Scene: One person sits at a desk with a large clock face with tick marks but no hands beside them and a sandwich lying untouched on the desk; the clock is the mass, the back is turned to the food.
   Must read: giving something up to keep working.
   Avoid: a person eating lunch; a bank with coins; a person sleeping at a desk.

5. `ten-nadele-van-de-klant.png` — Dutch chunk: ten nadele van (to the detriment of).
   Scene: One person stands behind a counter and slides a shorter pile of paper towards a customer who holds out an open hand; a tall pile stays behind the clerk, half hidden.
   Must read: someone gets less than they should.
   Avoid: a shop robbery; a person counting money; two people shaking hands.

6. `met-het-oog-op-de-toekomst.png` — Dutch chunk: met het oog op (with a view to).
   Scene: One person stands at a plain table and places a small sapling shape into a pot beside an open notebook with a ruled line drawn on it; one hand rests on the pot rim.
   Must read: planning ahead towards something.
   Avoid: a garden with many plants; a person digging; a calendar with dates.

7. `aan-de-hand-van-de-kaart.png` — Dutch chunk: aan de hand van (on the basis of, using).
   Scene: One person holds a large blank map open with both hands and leans over it, while a second figure points at one spot on the map with a single finger.
   Must read: steering by a guide.
   Avoid: a tourist with a camera; a car dashboard; a person lost.

8. `op-basis-van-de-cijfers.png` — Dutch chunk: op basis van (on the basis of).
   Scene: One person stands in front of a plain wall panel on which three thick vertical bars of different heights are painted, one hand flat under the shortest bar.
   Must read: deciding from measured results.
   Avoid: a calculator with digits; a bank vault; a bar chart with labels.

9. `met-inachtneming-van-de-termijn.png` — Dutch chunk: met inachtneming van (subject to, in observance of).
   Scene: One person writes on a blank sheet at a desk with a large calendar sheet pinned on the wall behind, its grid drawn in plain boxes; a pen is held over one box.
   Must read: keeping to a fixed deadline.
   Avoid: a clock with hands; a person late at a station; a letter with stamps.

10. `in-afwijking-van-de-regel.png` — Dutch chunk: in afwijking van (in deviation from).
   Scene: One person steps over a painted straight line on the floor while two others stand behind it, watching; the step across the line is the whole idea.
   Must read: going against the norm.
   Avoid: a game of hopscotch; a queue being skipped; a broken fence.

CONTRAST PAIRS
One, six and nine are singles built on multi-word prepositions; each is an everyday action with an object, not an abstract diagram. subject 1 is a stack of folders, subject 6 a pot and a notebook, subject 9 a wall calendar and a pen.
Two and 3 contrast `in verband met, because of` with `ten behoeve van, for`: carrying boxes because of a move, and tending a machine for its upkeep. Same standing camera.
Four and 5 contrast `ten koste van` with `ten nadele van`: in subject 4 the worker sacrifices the break himself, with the untouched sandwich; in subject 5 a clerk short-changes a customer while a tall pile stays behind the counter. Keep the two piles in subject 5 unequal.
Seven and eight are both decisions made from a flat panel: a map followed with a finger, and bars stacked on a wall. Same panel size; a map is folded paper, bars are painted.

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

## Batch B1+-05 — images 41–50

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `ten-opzichte-van-de-collega.png` — Dutch chunk: ten opzichte van (in relation to, towards).
   Scene: Two people stand face to face at equal distance with a plain straight line drawn on the floor between them and another figure standing well back behind the first.
   Must read: a measured relationship to someone.
   Avoid: a boxing ring; a ruler in the hand; a person alone.

2. `ten-aanzien-van-de-kosten.png` — Dutch chunk: ten aanzien van (with regard to, as regards).
   Scene: One person stands behind a plain counter with a stack of blank receipts on one side and a single coin-shaped disc on the other, both hands empty and open above the counter.
   Must read: regarding the money side.
   Avoid: a bank vault; a person counting notes; a shop with prices.

3. `ten-dienste-staan-van-de-klant.png` — Dutch chunk: ten dienste staan van (to be of service to).
   Scene: One person stands behind a low plain counter, body turned towards a visitor who holds out a flat folder; both of the standing figure's hands are open and ready, and an empty stool waits at the end of the counter.
   Must read: someone standing ready to help a visitor.
   Avoid: a shop with prices; a reception desk with a sign; two people just talking.

4. `ten-gevolge-van-de-storing.png` — Dutch chunk: ten gevolge van (as a result of).
   Scene: One person stands in a dim room with a plain lamp dangling from a wall socket by a loose cord, holding the cord up; everything else in the room is still.
   Must read: consequence of a fault.
   Avoid: a fire; a person angry at a machine; a repair van.

5. `ten-gunste-van-de-kandidaat.png` — Dutch chunk: ten gunste van (in favour of).
   Scene: One person lays one hand flat on a plain sheet bearing a single round seal shape and slides it towards a seated figure who has already lifted a pen.
   Must read: backing one side.
   Avoid: two candidates facing each other; a handshake; a ballot box.

6. `ten-laste-van-de-werkgever.png` — Dutch chunk: ten laste van (chargeable to, at the expense of).
   Scene: One person stands upright and light with a small plain tool bag and both hands open, while a second, larger figure beside them bends under a heavy sack with a single plain round disc drawn on its side.
   Must read: the cost carried by someone else.
   Avoid: a porter with luggage; a person begging; a bank.

7. `ten-spijt-van-de-weigering.png` — Dutch chunk: ten spijt van (in spite of).
   Scene: One person moves a heavy crate across the floor towards a closed door while another figure stands at the door with arms folded and a flat line for a mouth.
   Must read: carrying on despite a refusal.
   Avoid: a person breaking a door; a protest; a delivery van.

8. `ten-tijde-van-het-onderzoek.png` — Dutch chunk: ten tijde van (at the time of).
   Scene: One person stands in the middle of a room holding a small plain clipboard, looking at empty shelving on one wall; a large wall clock shows tick marks only.
   Must read: the state of things at one time.
   Avoid: a news camera; a police tape; a person reading a file.

9. `ten-overstaan-van-de-notaris.png` — Dutch chunk: ten overstaan van (in the presence of).
   Scene: One person signs a blank sheet on a table while a second figure stands opposite with both hands clasped in front, watching; a plain lamp sits between them on the table.
   Must read: signing witnessed by an official.
   Avoid: a courtroom with a judge; two people alone; a bank with a vault.

10. `ten-voordele-van-de-buurt.png` — Dutch chunk: ten voordele van (in aid of, for the benefit of).
   Scene: One person holds out a plain collecting tin with a slot towards two passing figures while a third has already dropped something in; a small table with cakes stands behind.
   Must read: raising money for a cause.
   Avoid: a shop sale sign; a person begging; a bank.

CONTRAST PAIRS
One, two and three are all `ten … van` frames: in subject 1 two people measured by a floor line with a third behind, in subject 2 a counter with receipts on one side and a stacked ledger on the other, in subject 3 a staff member turned towards a visitor at a low counter. Same standing camera; subject 1 has no furniture except the line.
Four and seven both go on against a pressure: a lamp hanging loose on its cord, and a door held shut by a figure with folded arms. Keep the lamp and the door the heaviest marks in their images.
Three, five, six, eight, nine and ten are singles. In subject 6 the standing worker's hands are empty and open and the sack on the second figure's back is the heaviest mark; keep it a sack, not the crate of subject 7.
No frame may show a coat of arms, a seal with a readable inscription, or a banknote.

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

## Batch B1+-06 — images 51–60

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `beschikken-over-een-kantoor.png` — Dutch chunk: beschikken over (to have at one's disposal).
   Scene: One person stands in the middle of an empty office with both arms spread wide, palms up, towards a large desk and two chairs; the room is bare apart from that furniture.
   Must read: having something available.
   Avoid: a person alone at a desk working; a shop full of goods; a bank.

2. `afhangen-van-droog-weer.png` — Dutch chunk: afhangen van (to depend on).
   Scene: One person stands at a window under a small row of plain cloud shapes while holding up a folded coat in one hand, undecided; the cloud and coat are the two poles.
   Must read: a decision held up by the weather.
   Avoid: a weather chart with numbers; rain falling on the person; a bus stop.

3. `beschikken-tot-uitstel.png` — Dutch chunk: beschikken tot (to decide to, to order).
   Scene: One person sits behind a desk and lays one hand flat on a blank sheet while pushing a small tray of papers away with the other; a second figure stands waiting with a folder.
   Must read: an official decision on paper.
   Avoid: a person signing with a pen; a judge with a gavel; a queue.

4. `bijdragen-aan-de-discussie.png` — Dutch chunk: bijdragen aan (to contribute to).
   Scene: One person leans forward at a long table with one hand raised and the other flat on the table; four other seated figures turn towards them.
   Must read: adding to a shared conversation.
   Avoid: a speaker at a podium; a person writing minutes; an argument.

5. `instemmen-met-het-voorstel.png` — Dutch chunk: instemmen met (to agree with).
   Scene: One person at the same long table lowers a raised hand to the table and nods, head forward; the seated figures beside them also lower their hands.
   Must read: saying yes to what was proposed.
   Avoid: a handshake across a table; a person voting at a booth; a signature.

6. `verwijzen-naar-de-nota.png` — Dutch chunk: verwijzen naar (to refer to).
   Scene: One person stands and points a hand towards a thin blank booklet lying on the corner of the table, while three seated figures follow the pointing hand.
   Must read: directing attention to a document.
   Avoid: a person reading aloud; a projector screen; a book with a title.

7. `volstaan-met-een-knikje.png` — Dutch chunk: volstaan met (to suffice with, to settle for).
   Scene: One person receives a thick folder from a colleague and answers with a single slow nod of the head, both hands still at their sides.
   Must read: a minimal answer.
   Avoid: a person refusing the folder; a handshake; two people arguing.

8. `verzoeken-om-uitstel.png` — Dutch chunk: verzoeken om (to request, to ask for).
   Scene: One person hands a blank form across a counter to a clerk, one hand open underneath, head lowered slightly; the clerk is already reaching for it.
   Must read: formally asking for more time.
   Avoid: the pilot counter scenes with a queue; a phone call; a person begging.

9. `getuigen-van-toewijding.png` — Dutch chunk: getuigen van (to testify to, to show).
   Scene: One person stands beside a table on which sits a single worn pair of plain work gloves and a cracked tool handle; the person has one hand open towards them.
   Must read: evidence of long effort.
   Avoid: a courtroom witness box; a medal; a certificate.

10. `betrekking-hebben-op-de-onkosten.png` — Dutch chunk: betrekking hebben op (to relate to, to concern).
   Scene: One person sits at a desk with a small stack of plain receipts in one hand and points a finger at one of them with the other; a calculator lies closed beside the stack.
   Must read: a matter that relates to these costs.
   Avoid: a bank robber; a pile of banknotes; a person at a till.

CONTRAST PAIRS
Two is a window with cloud shapes and a folded coat in the hand: dependence on the weather. It is not rain falling on a person, which belongs to the protection chunk.
Four and five are `bijdragen aan` against `instemmen met`: the same long meeting table, once a hand going up to add something, once a hand coming down to settle the matter. Keep the four other figures in identical seats in both.
One, three, six, seven, eight, nine and ten are singles in the office and meeting archetypes. subject 7 and subject 8 have the same standing posture facing a second figure; subject 7 receives a folder with a nod, subject 8 offers a blank form across a counter.
No frame in this batch shows a readable stamp, signature or minute book.

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

## Batch B1+-07 — images 61–70

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `vasthouden-aan-de-bewering.png` — Dutch chunk: vasthouden aan (to stick to).
   Scene: One person stands with both hands raised and open, palms out, chin lifted, insisting; a seated listener leans back with folded arms and a flat mouth line.
   Must read: refusing to give up a claim.
   Avoid: a speech bubble with letters; an argument with two bubbles; a crowd.

2. `afstand-nemen-van-de-bewering.png` — Dutch chunk: afstand nemen van (to distance oneself from).
   Scene: One person holds one flat hand out at chest height, palm turned outward towards a second figure, as if pushing the idea away; the second figure nods slowly.
   Must read: putting distance between oneself and a statement.
   Avoid: a person pointing at a board; a handshake; two people laughing.

3. `werken-volgens-een-werkwijze.png` — Dutch chunk: werken volgens (to work according to).
   Scene: One person holds a plain tool with both hands and aligns it with a marked line drawn on a workbench, eyes on the line, ready to follow it rather than striking with it.
   Must read: working by a set method.
   Avoid: a person hitting with the tool; a toolbox; a machine in motion.

4. `noodzaken-tot-actie.png` — Dutch chunk: noodzaken tot (to make necessary).
   Scene: One person stands with both hands raised and open in a shrug in front of a stalled machine with a loose belt, while another points at it.
   Must read: circumstances force an action.
   Avoid: a person angry with a colleague; a broken window; a fire.

5. `controleren-op-kwaliteit.png` — Dutch chunk: controleren op (to check for).
   Scene: One person checks a row of three identical plain blocks on a bench with a small square gauge held against one of them, eyes level with the edge.
   Must read: testing against a standard.
   Avoid: a shop with prices; a person approving a stack of paper; a factory robot.

6. `zich-houden-aan-de-norm.png` — Dutch chunk: zich houden aan (to adhere to, to stick to).
   Scene: One person holds a straight rule up against the edge of a large panel and squints along it, one eye closed; a second figure holds the panel steady.
   Must read: keeping to a fixed standard.
   Avoid: a school ruler in a child's hand; a level with a bubble; a chart.

7. `voortvloeien-uit-het-beleid.png` — Dutch chunk: voortvloeien uit (to result from, to follow from).
   Scene: One person stands at the top of a short flight of plain steps and lets one hand rest on the rail, looking down at a second figure standing at the bottom.
   Must read: one thing following from another.
   Avoid: a waterfall; a queue on stairs; a person climbing alone.

8. `aandacht-vragen-voor-het-plan.png` — Dutch chunk: aandacht vragen voor (to call attention to).
   Scene: One person sits at a desk with both hands framing a single page, leaning towards a second figure; a closed door stands behind them.
   Must read: asking others to look at this.
   Avoid: a person asleep at a desk; a phone ringing; two people talking.

9. `wijzigingen-aanbrengen-in-de-afspraak.png` — Dutch chunk: wijzigingen aanbrengen in (to make changes to).
   Scene: One person sits with a blank sheet in one hand and a pen in the other, crossing out a line and starting again below it; one earlier sheet lies crumpled at the desk edge.
   Must read: making changes to an agreement.
   Avoid: a person tearing up paper in anger; a contract with a seal; two people.

10. `optreden-tegen-de-overtreders.png` — Dutch chunk: optreden tegen (to take action against).
   Scene: One person stands at an open doorway with one arm across it, palm flat and face turned to three figures who have stopped in front of them.
   Must read: taking action against those who break a rule.
   Avoid: a police officer with a badge; a queue; two people arguing.

CONTRAST PAIRS
One and two are the same two figures, standing against seated: a wide claim with chin up, and a flat hand and a careful sentence. Keep the listener identical and change only the speaker's arms and chin.
Three, five and six all show a plain tool at a bench: subject 3 rests it aligned on a line, subject 5 holds a small square gauge to a block, subject 6 holds a rule to a panel with a helper. Three different tools, one bench.
Four is the stalled machine that subject 3's tool would be used on.
Seven, eight, nine and ten are singles. subject 10 reuses the doorway archetype; the arm across it and the three halted figures are the whole idea.

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

## Batch B1+-08 — images 71–80

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `gepaard-gaan-met-een-risico.png` — Dutch chunk: gepaard gaan met (to be accompanied by, to go hand in hand with).
   Scene: One person holds a large plain parcel in both arms and steps towards a narrow gap between two stacked crates, body turned sideways.
   Must read: a job that brings a risk with it.
   Avoid: a warning triangle; a person falling; an open fire.

2. `het-oneens-zijn-met-de-uitslag.png` — Dutch chunk: het oneens zijn met (to disagree with).
   Scene: One person holds up a blank sheet and shakes their head, one hand flat towards a second figure who holds the same sheet close to the chest.
   Must read: disagreeing with a result.
   Avoid: a courtroom with a judge; two people fighting; a queue.

3. `blijken-uit-de-meting.png` — Dutch chunk: blijken uit (to emerge from).
   Scene: One person stands beside a large plain meter dial with a single pointer turned to the right side, one hand open towards it; another figure looks up from a notebook.
   Must read: the measurement settles a doubt.
   Avoid: a clock with many marks; a thermometer; a chart with numbers.

4. `uitgaan-van-een-aanname.png` — Dutch chunk: uitgaan van (to go on the assumption of).
   Scene: One person stands with one hand on a switch and the other lifted with a finger raised, speaking to a colleague who nods; the machine beside them is dark and still.
   Must read: taking something for granted before testing.
   Avoid: a working machine with motion; a diagram on a wall; a person alone.

5. `onderhoud-verrichten-aan-de-machine.png` — Dutch chunk: onderhoud verrichten aan (to carry out maintenance on).
   Scene: One person kneels beside a large machine with the front panel removed and lays a plain tool inside it; a second figure holds a lamp steady above.
   Must read: doing maintenance work.
   Avoid: a car garage with signs; a person washing a floor; a toolbox.

6. `een-oordeel-vellen-over-het-onderdeel.png` — Dutch chunk: een oordeel vellen over (to pass judgement on).
   Scene: One person taps a small cracked part lying on a bench with one finger and turns to a colleague with a flat mouth line; the part has a clear split through it.
   Must read: judging something wrong.
   Avoid: a person breaking the part; a rubbish bin; a certificate.

7. `beoordelen-op-de-inhoud.png` — Dutch chunk: beoordelen op (to assess by).
   Scene: One person sits at a desk with a large open folder of blank pages and a pen resting across it, head tilted, looking at a standing figure whose hands are clasped.
   Must read: giving a judgement on someone's work.
   Avoid: a judge's bench; a school exam with questions; two people chatting.

8. `een-subsidie-toekennen-aan-de-aanvrager.png` — Dutch chunk: toekennen aan (to award to).
   Scene: One person slides a plain envelope across a desk towards an applicant whose hand is already outstretched; a stamp-shaped pad lies untouched beside the envelope.
   Must read: granting something officially.
   Avoid: a bank vault; a person counting notes; a handshake.

9. `afstand-doen-van-de-schuld.png` — Dutch chunk: afstand doen van (to relinquish, to give up).
   Scene: One person holds a blank sheet and draws a wide diagonal stroke across it, then lifts it towards a second figure who sits with lowered shoulders.
   Must read: giving up a claim.
   Avoid: a bank with coins; a courtroom; two people fighting.

10. `informatie-verstrekken-over-de-regeling.png` — Dutch chunk: informatie verstrekken over (to provide information about).
   Scene: One person stands at a counter and pushes a small stack of blank sheets towards a waiting figure, one hand flat on top of the stack for support.
   Must read: handing over information.
   Avoid: a phone call; a person writing a letter; a queue.

CONTRAST PAIRS
One and two are both held up against someone: the parcel carried into a gap with a risk, and the same sheet held by two people who disagree. Same standing camera; in subject 1 nothing is disputed, only carried.
Three and 4 share the machine: subject 3's dial pointer settles the question, subject 4's person assumes and the machine is dark. Keep the machine body identical.
Six and seven are `beschouwen als` against `beoordelen`: a cracked part judged on the bench, and a standing person judged from behind a folder. Same desk and bench height; one judgement is about a thing, one about a person.
Five, eight, nine and ten are singles. subject 8 and subject 10 both happen at a desk or a counter and both slide paper across; the envelope and the stack must look different.
No frame may show a readable stamp, form or grade.

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

## Batch B1+-09 — images 81–90

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `uitgaan-van-het-ergste.png` — Dutch chunk: uitgaan van (to assume, to proceed from).
   Scene: One person stands with one hand flat on a large closed box in front of them, looking steadily at a colleague; a second, open and empty box sits beside it.
   Must read: taking the downside as the starting point.
   Avoid: a person opening the box; a gift; a calculator.

2. `uitgaan-naar-de-zaal.png` — Dutch chunk: uitgaan naar (to go out to).
   Scene: One person steps out through a wide door into an open space, one hand raised towards a distant figure walking in the opposite direction.
   Must read: moving out towards somewhere.
   Avoid: a fire exit with a sign; a crowd leaving; a bus at a stop.

3. `afhangen-van-de-beslissing.png` — Dutch chunk: afhangen van (to depend on).
   Scene: One person stands on one side of a doorway waiting, hands behind the back, looking at a second figure inside who holds a blank sheet up to a lamp.
   Must read: waiting for another's decision.
   Avoid: a person signing a contract; a queue at a counter; a phone call.

4. `berusten-op-een-afspraak.png` — Dutch chunk: berusten op (to rest on, to be based on).
   Scene: Two people stand side by side with one hand each on a large plain stone block between them, holding it together; a folded sheet lies on top of the block.
   Must read: standing on a shared agreement.
   Avoid: a building foundation in a ditch; a handshake alone; a court.

5. `berusten-in-het-verlies.png` — Dutch chunk: berusten in (to accept, to come to terms with).
   Scene: One person stands with both hands open at the sides and a slight bow of the head in front of an empty chair with a folded coat on it.
   Must read: settling into a loss.
   Avoid: a person crying; a funeral; two people comforting.

6. `zich-richten-op-het-doel.png` — Dutch chunk: zich richten op (to focus on).
   Scene: One person stands with both hands raised in a ring in front of the eye, looking straight ahead through it at a single plain upright post in the distance.
   Must read: aiming attention at one target.
   Avoid: a telescope on a tripod; a camera; a person with a speech.

7. `zich-richten-tot-de-zaal.png` — Dutch chunk: zich richten tot (to address).
   Scene: One person stands with one arm open towards three seated figures and the body turned fully towards them.
   Must read: speaking to a room.
   Avoid: a single clerk at a desk; a person with an earpiece; a crowd outside.

8. `verschillen-van-de-rest.png` — Dutch chunk: verschillen van (to differ from).
   Scene: One figure stands in front of four identical plain blocks, holding a fifth block of clearly different height beside them, comparing with a level hand.
   Must read: standing out from the rest.
   Avoid: a queue of people; a chart; a person alone.

9. `afwijken-van-het-plan.png` — Dutch chunk: afwijken van (to deviate from).
   Scene: One person walks in a straight path away from a painted line on the floor, one foot already off the line, while a second figure stays on it.
   Must read: leaving a laid-down course.
   Avoid: a map with a route; a person lost; a broken sign.

10. `voortkomen-uit-het-verleden.png` — Dutch chunk: voortkomen uit (to arise from).
   Scene: One person holds an old split branch in both hands with a young straight shoot growing out of the fork, one hand running along the shoot.
   Must read: a cause that carries on.
   Avoid: a genealogy chart; a family with children; a tree in a park.

CONTRAST PAIRS
One, two and 3 share the same standing figure and room: subject 1 an assumption held over a closed box, subject 2 a walk out through a door, subject 3 waiting for a speaker who holds a sheet to a lamp.
Four and five are `berusten op` against `berusten in`: two people holding a block together against one person bowing before an empty chair. Same standing camera; the support is hands in subject 4, absent in subject 5.
Six and seven are `zich richten op` against `zich richten tot`: a hand ring aimed at a distant post, and an open arm towards seated backs. Keep the standing figure identical and change only the target.
Eight and nine are both measured against a mark: a block of a different height beside four equals, and a figure stepping off a painted line. Same painted line on the floor in both.
Ten is a single; no person appears apart from the carrier and the branch is the mass.

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

## Batch B1+-10 — images 91–100

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `houden-van-het-klimaat.png` — Dutch chunk: houden van (to be fond of, to love).
   Scene: One person sits on a low rock with both hands relaxed on the knees, face lifted to a large plain ring for the sun; one bird shape is drawn as a simple curve above.
   Must read: loving something.
   Avoid: the shipped frame with a dog; a couple embracing; a party.

2. `houden-aan-het-licht.png` — Dutch chunk: houden aan (to keep to, to stick by).
   Scene: One person walks steadily along a straight painted line laid on a wide floor, one foot exactly on it, hands at the sides and face forward.
   Must read: keeping to a rule.
   Avoid: a person stepping off a line; a queue; a road sign.

3. `twijfelen-aan-de-oplossing.png` — Dutch chunk: twijfelen aan (to doubt).
   Scene: One person holds up a small plain gear piece at eye level, one hand turning it, mouth pulled to one side, and looks past it rather than at it.
   Must read: not trusting something.
   Avoid: a person choosing between two objects; a broken machine; a shrug.

4. `twijfelen-over-de-keuze.png` — Dutch chunk: twijfelen over (to be undecided about).
   Scene: One person stands between two identical plain doors, arms hanging, head turned from one to the other; the two doors fill the width.
   Must read: hesitation between two equal options.
   Avoid: a person inside one room; a maze; a sign with arrows.

5. `geloven-in-de-goede-afloop.png` — Dutch chunk: geloven in (to believe in).
   Scene: One person walks forward with head up and one hand raised open, towards a wide bright gap between two tall blocks; the gap is the shape.
   Must read: confidence in a good outcome.
   Avoid: a person praying; a church; a person alone on the floor.

6. `denken-aan-het-klimaat.png` — Dutch chunk: denken aan (to think of, to bear in mind).
   Scene: One person pauses with one hand on a bicycle handlebar and the other at the chin, looking at a plain globe shape held under one arm.
   Must read: remembering something bigger.
   Avoid: the shipped thought-bubble frame with a face; a car; a globe with land masses.

7. `zorgen-voor-de-planten.png` — Dutch chunk: zorgen voor (to look after).
   Scene: One person waters a row of three potted plants with a plain can, tilting the spout towards the middle pot; one plant is taller than the others.
   Must read: care for living things.
   Avoid: the shipped child scene; a garden centre; a person asleep.

8. `zorgen-over-het-examen.png` — Dutch chunk: zorgen over (to worry about).
   Scene: One person sits on the edge of a chair with both hands clasped tightly in the lap and eyebrows drawn down; a blank sheet lies face down on the table.
   Must read: anxiety about a test.
   Avoid: the shipped mess scene; a person studying happily; a clock.

9. `denken-over-een-voorstel.png` — Dutch chunk: denken over (to think about, to consider).
   Scene: One person sits with a blank sheet in one hand and a pen held still in the other, chin on the pen hand, eyes towards a window.
   Must read: weighing a proposal.
   Avoid: the shipped choice frame at a counter; a person signing; two people.

10. `oplossen-door-te-luisteren.png` — Dutch chunk: oplossen door (to solve by).
   Scene: Two people sit facing each other, one leaning in with an open palm on the table between them; the other has just lifted their head, hands no longer crossed.
   Must read: a problem cleared by dialogue.
   Avoid: two people arguing; a person alone at a puzzle; a toolbox.

CONTRAST PAIRS
One and six both reuse shipped verbs with new scenes: fondness for open air, and remembering something larger while out on a bicycle. Neither may reuse the dog, the gift or the pilot face bubble.
Three and four are `twijfelen aan` against `twijfelen over`: one object turned in the hand, and two identical doors. Same standing camera; the door frame must be wide, not narrow.
Five and 7 show confidence and care with objects: an open gap between two blocks, and a watering can over three plants. Both are upright and calm.
Eight and nine are `zorgen over` against `denken over`: worry at a chair edge, and consideration at a desk. Keep the sheet face down in subject 8 and held in the hand in subject 9.
Two and ten are singles on their own verbs. No arrows on the ground; the painted line does the work.

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

## Batch B1+-11 — images 101–110

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `tussen-de-regels-door-lezen.png` — Dutch chunk: tussen de regels door (between the lines).
   Scene: One person holds a blank page close to the face with both hands and one eye squinting past the edge of it; a second blank page lies on the table, ruled in straight lines.
   Must read: reading what is not written.
   Avoid: a person reading aloud; a book with letters; a person asleep.

2. `vanaf-het-moment-van-aankomst.png` — Dutch chunk: vanaf het moment van (from the moment of).
   Scene: One person stands just inside a doorway with a plain suitcase beside them and a hand still on the bag handle; the open door behind frames the moment of arrival.
   Must read: the start of something.
   Avoid: a person leaving; a train platform; a clock with hands.

3. `werken-tegen-de-klok.png` — Dutch chunk: tegen de klok (against the clock).
   Scene: One person sits at a desk with papers under both hands, writing fast and leaning forward; a large wall clock above the desk shows tick marks and two hands, no numerals.
   Must read: working faster because time is short.
   Avoid: a person eating; a person asleep at a desk; a bus timetable.

4. `van-tijd-tot-tijd-bellen.png` — Dutch chunk: van tijd tot tijd (from time to time).
   Scene: One person sits with a plain telephone receiver held to the ear, a second hand raised; two interrupted plain horizontal bars are drawn behind them, far apart.
   Must read: an occasional call.
   Avoid: a phone with a screen; a person writing letters; a crowd.

5. `door-de-week-heen-werken.png` — Dutch chunk: door de week (during the week).
   Scene: One person stands with one hand on a large plain calendar of boxes, covering the left part with a flat hand while the right side stays visible.
   Must read: the ordinary days.
   Avoid: a weekend scene with leisure; a person asleep; a clock.

6. `op-de-hoogte-zijn-van-het-nieuws.png` — Dutch chunk: op de hoogte zijn van (to be aware of, to be informed about).
   Scene: One person stands with a folded blank newspaper held against the chest and one hand lifted to the chest in a small, satisfied pat; a small second folded paper sits on the table.
   Must read: knowing what has happened.
   Avoid: a person reading aloud; a newsroom with screens; a phone.

7. `buiten-kijf-blijven.png` — Dutch chunk: buiten kijf (beyond dispute).
   Scene: Two people stand on either side of a large plain upright stone slab with one hand each flat on it, facing outward towards the viewer.
   Must read: a settled matter between two.
   Avoid: a courtroom with a judge; an argument; a handshake.

8. `tegen-de-verwachting-in-winnen.png` — Dutch chunk: tegen de verwachting in (contrary to expectation).
   Scene: One figure stands with both arms raised beside a low plain block, while three figures behind look towards them with heads tilted and mouths open.
   Must read: an upset result.
   Avoid: a trophy; a crowd cheering in unison; a person alone.

9. `in-de-loop-der-jaren.png` — Dutch chunk: in de loop der jaren (over the years).
   Scene: One person stands beside a single tall tree trunk with several narrow rings drawn at its base, one hand resting on the bark; a small shoot beside it is younger and straighter.
   Must read: time passing slowly.
   Avoid: a calendar; a clock; a person ageing with a cane.

10. `onder-het-mom-van-uitstel.png` — Dutch chunk: onder het mom van (under the pretext of).
   Scene: One person holds a plain folder in front of the chest and steps forward with chin up, while a second figure behind them lifts the back of the folder slightly, showing a second plain sheet underneath.
   Must read: a false reason covering a real one.
   Avoid: a mask; a costume; two people arguing.

CONTRAST PAIRS
One and ten both hinge on a second piece of paper: a ruled page over an unread one, and a sheet hidden behind a folder. Keep subject 1 close to the face and subject 10 held at chest level so the two do not read as the same image.
Three and five both use a flat calendar or clock face. The clock stands upright on a wall in subject 3; the calendar lies under a hand in subject 5. Do not put numerals on either.
Six and the journalistic batches share a folded paper; here it is held upright against the chest and the image is calm.
Two, four, seven, eight and nine are singles. subject 8 is the only frame with four people; the three tilted heads are the mass.

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

## Batch B1+-12 — images 111–120

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `kiezen-tussen-twee-banen.png` — Dutch chunk: kiezen tussen (to choose between).
   Scene: One person stands at the centre of a wide floor with a plain upright post on each side at equal distance, both hands hanging, head turned to the left post.
   Must read: weighing two options.
   Avoid: two doors; a person pointing; a shop counter.

2. `kiezen-uit-het-aanbod.png` — Dutch chunk: kiezen uit (to choose from).
   Scene: One person stands in front of a row of five identical plain boxes on a shelf and has one hand out towards the middle box, the others untouched.
   Must read: picking one of many.
   Avoid: two objects only; a shop with prices; a person deciding to leave.

3. `beslissen-over-de-aanvraag.png` — Dutch chunk: beslissen over (to decide on).
   Scene: One person sits behind a desk with a blank form held in both hands, thumb on one corner, eyes down; a second figure waits on a chair opposite.
   Must read: a decision still open in someone's hands.
   Avoid: a person signing already; a queue; a judge with a gavel.

4. `beslissen-tot-verkoop.png` — Dutch chunk: beslissen tot (to decide to, to resolve on).
   Scene: One person lays a plain key on the table and pushes it towards a second figure with one flat hand, the other hand already withdrawn.
   Must read: committing to an action.
   Avoid: a bank with coins; a shop with a sign; two people arguing.

5. `belangen-afwegen-tegen-elkaar.png` — Dutch chunk: afwegen tegen (to weigh against).
   Scene: One person holds a simple balance with a plain block in each pan, one pan clearly lower; the hand keeps the beam level with a finger.
   Must read: comparing two options carefully.
   Avoid: a shop scale with prices; a person tossing a coin; a calculator.

6. `besluiten-tot-uitstel.png` — Dutch chunk: besluiten tot (to decide to).
   Scene: One person sits with a blank sheet turned face down on the desk and both hands resting flat on it, looking up at a standing colleague who waits with a folder.
   Must read: settling on no action yet.
   Avoid: a person signing at once; a customer leaving; a queue.

7. `opteren-voor-een-oplossing.png` — Dutch chunk: opteren voor (to opt for).
   Scene: One person kneels beside a low shelf with two plain tools lying on it and has already lifted the longer one into both hands.
   Must read: making a single choice.
   Avoid: two identical doors; a person comparing; a toolbox on the floor.

8. `aarzelen-tussen-twee-mogelijkheden.png` — Dutch chunk: aarzelen tussen (to hesitate between).
   Scene: One person stands with one hand extended towards each of two plain objects on a table, both hands equally open, body squared to the table edge.
   Must read: being stuck between two.
   Avoid: a person picking one up; a shop; a queue.

9. `afzien-van-een-plaats.png` — Dutch chunk: afzien van (to give up, to forgo).
   Scene: One person holds a blank ticket out towards a clerk across a counter while shaking their head slightly, the other hand still on the counter.
   Must read: declining what was offered.
   Avoid: a queue at a cinema; a person waving goodbye; a bank.

10. `zich-beraden-op-het-voorstel.png` — Dutch chunk: zich beraden op (to deliberate on).
   Scene: Two people sit facing each other across a corner of a table with one blank sheet between them and no pens; both have one hand near, not on, the sheet.
   Must read: taking time over a proposal.
   Avoid: a meeting with a speaker; a person alone reading; a signature.

CONTRAST PAIRS
One and two are `kiezen tussen` against `kiezen uit`: two equal posts, and five boxes in a row. Keep the standing figure identical and change only the number of objects.
Three and four are `beslissen over` against `beslissen tot`: a form still in two hands at a desk, and a key pushed across the table. Same seated camera; the second figure waits in subject 3 and receives in subject 4.
Seven and eight are `opteren voor` against `aarzelen tussen`: one tool already lifted, and two objects with both hands open and neither taken. Keep the table edge and the tools identical.
Five, six, nine and ten are singles. subject 5's balance has two pans only and no weights.

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

## Batch B1+-13 — images 121–130

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `leidinggeven-aan-het-team.png` — Dutch chunk: leidinggeven aan (to be in charge of).
   Scene: One person stands at the head of a small table in an office with one hand open towards three seated figures and the other resting on a printed plan rolled on the table.
   Must read: being in charge of a group.
   Avoid: a throne; a uniform with badges; a crowd.

2. `rapporteren-aan-de-chef.png` — Dutch chunk: rapporteren aan (to report to).
   Scene: One person stands at a desk with a plain folder held out towards a seated figure who does not look up; the standing figure's shoulders are lowered.
   Must read: answering to someone above.
   Avoid: a handshake between equals; two people at the same level; a phone.

3. `overleggen-met-collega.png` — Dutch chunk: overleggen met (to consult with).
   Scene: Two people sit side by side at one desk, the first holding a blank sheet and the second leaning over the same sheet; both have one hand near the paper's centre.
   Must read: deciding together.
   Avoid: one person reporting to a boss; an argument; a crowd.

4. `een-punt-zetten-achter-de-klus.png` — Dutch chunk: een punt zetten achter (to round off).
   Scene: One person sets the last of a stack of plain folders square on top of a small pile and straightens it with both hands; the desk behind is clear.
   Must read: the last action of a task.
   Avoid: a person starting work; a broken machine; a queue.

5. `een-gesprek-inplannen-in-de-agenda.png` — Dutch chunk: inplannen in (to schedule into).
   Scene: One person stands with a large plain calendar of boxes held against the wall with one hand and draws a single circle in the air over one box with a finger.
   Must read: fixing an appointment.
   Avoid: a clock with hands; a person late at a station; a phone call.

6. `inwerken-in-de-functie.png` — Dutch chunk: inwerken in (to train someone into).
   Scene: One person stands behind a seated newcomer and guides their hand towards a switch panel on a wall; the newcomer's head turns towards the explaining figure.
   Must read: learning a job from a colleague.
   Avoid: a classroom with a board; two people at a computer; a toolbox.

7. `zich-inwerken-in-het-systeem.png` — Dutch chunk: zich inwerken in (to work one's way into, to master).
   Scene: One person sits alone at a desk with a thick manual propped open against a small stand and one finger following a column of blank ruled lines.
   Must read: self-study into a system.
   Avoid: the same desk with a guide standing over them; a phone; a crowd.

8. `onderhandelen-over-het-contract.png` — Dutch chunk: onderhandelen over (to negotiate about).
   Scene: Two people sit opposite each other at a table with a blank contract sheet between them and one pencil turned towards each side.
   Must read: working out terms together.
   Avoid: a person signing alone; a handshake; a judge.

9. `solliciteren-naar-een-functie.png` — Dutch chunk: solliciteren naar (to apply for).
   Scene: One person sits on the far side of a desk with a blank sheet held in both hands, back straight; two interviewers sit opposite with the same blank sheet in front of them.
   Must read: applying for a job.
   Avoid: a queue at a job centre; a person handing over a CV with text; a phone.

10. `een-vergoeding-krijgen-voor-de-kosten.png` — Dutch chunk: een vergoeding krijgen voor (to be reimbursed for).
   Scene: One person holds out a small pile of plain receipts in one hand towards another who counts them into a tin box with the other hand open.
   Must read: paying back expenses.
   Avoid: a bank with banknotes; a shop till with numbers; a payslip.

CONTRAST PAIRS
Two and three are `rapporteren aan` against `overleggen met`: a folder handed up to a seated boss, and two people leaning over the same sheet as equals. Same office camera; the difference is who is higher.
Six and seven are `inwerken in` against `zich inwerken in`: a guide at the shoulder with a switch panel, and a person alone with a manual on a stand. Keep the desk identical and change the guide's presence.
One, four, five, eight, nine and ten are singles in the office and meeting archetypes. subject 8's pencil points towards neither side; subject 9 and subject 10 share a desk and an applicant, with interviewers opposite in subject 9 and a receipt pile in subject 10.
No screen may show text; notebooks are ruled only.

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

## Batch B1+-14 — images 131–140

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `omgaan-met-moeilijke-klanten.png` — Dutch chunk: omgaan met (to deal with).
   Scene: One person stands behind a counter with one hand open and the other steady on the counter, facing a customer who leans in with both hands flat on the counter top.
   Must read: handling a difficult person.
   Avoid: two people shouting; a cash register; a queue.

2. `omspringen-met-de-tijd.png` — Dutch chunk: omspringen met (to handle, to deal with).
   Scene: One person holds a large clock face with tick marks loose in both hands, tilted like a tray, with a small pile of loose sheets balanced on it.
   Must read: using time carelessly.
   Avoid: a person late at a station; an alarm clock on a bedside table; a calendar.

3. `afstemmen-op-de-ander.png` — Dutch chunk: afstemmen op (to align with).
   Scene: Two people sit side by side turning a shared dial panel with two sets of small marks until one hand on the dial meets the other at the same point.
   Must read: bringing two things into line.
   Avoid: a radio with a screen; a person tuning alone; a meeting.

4. `zich-aanpassen-aan-de-collega.png` — Dutch chunk: zich aanpassen aan (to adapt to).
   Scene: One person changes their standing stance to copy the posture of a colleague beside them, both now with arms crossed and the same head tilt.
   Must read: adjusting yourself to another.
   Avoid: two people arguing; a handshake; a person alone.

5. `toezien-op-de-veiligheid.png` — Dutch chunk: toezien op (to supervise).
   Scene: One person stands at the edge of a room with both hands behind the back, watching three others at a low bench working with plain tools.
   Must read: keeping watch over work.
   Avoid: a police officer with a badge; a crowd; a machine running alone.

6. `ingrijpen-bij-een-conflict.png` — Dutch chunk: ingrijpen bij (to step in on).
   Scene: One person steps between two others who lean towards each other with hands raised, both arms spread flat to separate them.
   Must read: stepping into the middle.
   Avoid: a boxing match; a person alone pointing; a queue.

7. `delegeren-aan-een-collega.png` — Dutch chunk: delegeren aan (to delegate to).
   Scene: One person places a plain folder into the open hands of a colleague and lets go, stepping back half a pace; the folder is now the other's.
   Must read: passing work on.
   Avoid: a handshake; two people holding the same folder; a queue.

8. `samenwerken-met-de-afdeling.png` — Dutch chunk: samenwerken met (to cooperate with).
   Scene: Two people stand on either side of a large panel, each holding one edge, and lift it together; a third holds the bottom corner.
   Must read: shared work by several.
   Avoid: one person carrying the panel alone; a handshake; an argument.

9. `een-overzicht-bijhouden-van.png` — Dutch chunk: een overzicht bijhouden van (to keep track of).
   Scene: One person stands at a high desk with a long ruled sheet clipped to a board and a pen making a short mark beside an existing line; a second board hangs behind with a grid.
   Must read: recording as things happen.
   Avoid: a person reading a newspaper; a phone; a crowd.

10. `terugkoppelen-aan-het-team.png` — Dutch chunk: terugkoppelen aan (to report back to).
   Scene: One person stands at the end of a table and speaks with one hand open towards five seated figures, a folder closed under the other arm.
   Must read: bringing news back to the group.
   Avoid: a customer at a counter; a phone call; one person alone.

CONTRAST PAIRS
One and two both sit behind or hold everyday objects: a customer leaning on the counter, and a clock carried like a tray. Keep the counter in subject 1 and the tilted clock in subject 2; neither may show the other's object.
Three and four are `afstemmen op` against `zich aanpassen aan`: two hands meeting on a dial, and one body copying another's stance. Same standing and sitting camera; subject 3 is seated, subject 4 standing.
Five and six are `toezien op` against `ingrijpen bij`: hands behind the back at the edge, then between two people with arms spread. Keep the watcher's stance identical and change only the position.
Seven and eight are `delegeren aan` against `samenwerken met`: a folder released into two hands, and a panel lifted by three. Same standing camera.
Nine and ten are singles. subject 10 repeats the group speaking pose of earlier batches; the closed folder under the arm must stay closed.

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

## Batch B1+-15 — images 141–150

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `solliciteren-op-een-vacature.png` — Dutch chunk: solliciteren op (to apply for).
   Scene: One person sits at a plain table with a blank form and a pen, the pen already lifted, looking at a single empty chair set opposite.
   Must read: writing to get a job.
   Avoid: two interviewers; a queue; a phone call.

2. `een-einde-maken-aan-het-contract.png` — Dutch chunk: een einde maken aan (to put an end to).
   Scene: One person tears a plain sheet across the middle with both hands, the tear running from the top edge; a second intact sheet lies on the table.
   Must read: ending an agreement.
   Avoid: a person signing; a handshake; a company logo.

3. `het-contract-verlengen-met-een-jaar.png` — Dutch chunk: verlengen met (to extend by).
   Scene: One person—who is the same sexless neutral figure—holds a blank sheet and adds another blank sheet edge to edge beneath it, aligning the corners with both hands.
   Must read: making an agreement longer.
   Avoid: a calendar; a person signing twice; a handshake.

4. `zich-afmelden-voor-het-abonnement.png` — Dutch chunk: zich afmelden voor (to cancel, to unsubscribe from).
   Scene: One person holds a plain card in one hand and a pair of plain scissors in the other, about to close the blades across the card.
   Must read: ending a subscription.
   Avoid: a bank with coins; a shop with a sign; a phone.

5. `overnemen-van-de-voorganger.png` — Dutch chunk: overnemen van (to take over from).
   Scene: One person is handed a plain key ring by a departing figure who already has a bag over one shoulder and one foot towards the door.
   Must read: inheriting a role.
   Avoid: a handshake between equals; a queue; a crowd.

6. `zich-aanmelden-bij-de-balie.png` — Dutch chunk: zich aanmelden bij (to sign up with).
   Scene: One person stands at a counter with a ruled blank list on a clipboard and a pen held ready, one box already marked with a single stroke.
   Must read: signing yourself in at a counter.
   Avoid: a person reading a book; a phone screen; a queue.

7. `een-klacht-in-ontvangst-nemen.png` — Dutch chunk: in ontvangst nemen (to receive, to take in).
   Scene: One person nods and takes a folded note from an angry customer's hand, the other hand open and raised slightly to calm; the customer leans over the counter.
   Must read: receiving a complaint calmly.
   Avoid: two people shouting; a cash register; a shop with a sign.

8. `de-klacht-overdragen-aan-een-collega.png` — Dutch chunk: overdragen aan (to hand over to).
   Scene: The same three figures as #7: the clerk now hands the folded note over a desk to a colleague who reads it, the second hand flat on the desk to steady it.
   Must read: sending a complaint onward.
   Avoid: a person keeping the note; two people arguing; a queue.

9. `opleiden-tot-vakman.png` — Dutch chunk: opleiden tot (to train as, to train into).
   Scene: One person guides a younger figure's hands on a plain tool held over a workbench, both bent over the same small object.
   Must read: teaching a trade.
   Avoid: a classroom; a person alone at a bench; a toolbox.

10. `uitvoeren-volgens-plan.png` — Dutch chunk: uitvoeren volgens (to carry out according to).
   Scene: One person sets out plain blocks on a bench in the order drawn on a single blank ruled sheet propped against a small stand, one block in hand.
   Must read: working to a written plan.
   Avoid: a person alone at a bench with a finished machine; a toolbox; a crowd.

CONTRAST PAIRS
Three and four are `een einde maken aan` against `verlengen met`: the same blank sheet, once torn across, once laid edge to edge with a second. Same table and camera; keep the tear visible at the top edge.
Seven and eight are one scene in two halves: an angry customer leaning over a counter, then the same folded note moving on to a colleague at a desk. Keep the note identical in both and the customer absent from subject 8.
One, two, five, six, nine and ten are singles in the office, counter and workshop archetypes. subject 9 and subject 10 must not look alike: subject 9 is two pairs of hands on one tool at a bench, subject 10 is loose blocks and a propped plan.
No form, card or plan may show letters or numbers; only ruled lines and single strokes.

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

## Batch B1+-16 — images 151–160

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `beschikken-over-de-vrije-tijd.png` — Dutch chunk: beschikken over de vrije tijd (to have one's free time).
   Scene: One person sits on a low step with both hands behind the head and legs stretched out, an open book face down beside them and nothing else around.
   Must read: having time to spend.
   Avoid: a person hurrying with a bag; a desk full of work; a clock.

2. `bewogen-worden-tot-hulp.png` — Dutch chunk: bewogen worden tot (to be moved to).
   Scene: One person steps forward and places a hand flat on the shoulder of a second who sits hunched on a bench; the helper's head is low and close.
   Must read: an inner push to act.
   Avoid: a flag or banner; a donation box; a police officer.

3. `waarschuwen-voor-gevaar.png` — Dutch chunk: waarschuwen voor (to warn against).
   Scene: One person stands well back from the edge of a step and holds out a flat hand towards a second figure who walks carelessly near it, head turned away.
   Must read: stopping someone in time.
   Avoid: a warning sign with a mark; a fence; a rescue.

4. `gedwongen-zijn-tot-uitstel.png` — Dutch chunk: gedwongen zijn tot (to be forced into).
   Scene: One person stands at a closed door with a blank sheet in one hand and the other flat against the door, shoulders squared against it.
   Must read: no way through.
   Avoid: a person opening the door freely; a queue; a phone.

5. `getuigen-over-de-gebeurtenis.png` — Dutch chunk: getuigen over (to give evidence about).
   Scene: One person sits on a plain chair in an otherwise empty room with both hands on the knees and head level, speaking towards the viewer's space with an open mouth.
   Must read: telling what was seen.
   Avoid: a courtroom with a judge; a crowd; a handshake.

6. `te-kampen-hebben-met-tegenstand.png` — Dutch chunk: te kampen hebben met (to struggle with, to be faced with).
   Scene: One person pushes a wheeled cart up a shallow slope, body leaning into it and both hands on the handlebar; the cart's front wheel is near a loose stone.
   Must read: struggling against resistance in a task.
   Avoid: a car on a hill; a person resting; a delivery van.

7. `uitkomen-voor-de-fout.png` — Dutch chunk: uitkomen voor (to own up to, to admit).
   Scene: One person says aloud with one hand on the chest and the other lifted open, and the listener beside them has unfolded their arms.
   Must read: openly owning up to a mistake.
   Avoid: a row of people; a certificate; two people fighting.

8. `bezwaar-maken-tegen-de-claim.png` — Dutch chunk: bezwaar maken tegen (to object to).
   Scene: One person shakes their head with one hand flat and raised like a stop, while a second holds up a blank sheet towards them.
   Must read: objecting to a claim.
   Avoid: a courtroom with a judge; a person signing; a crowd.

9. `voldoen-aan-de-eisen.png` — Dutch chunk: voldoen aan (to meet, to satisfy).
   Scene: One person stands with a long plain checklist on a board held in one arm and ticks the final point with a finger; a short stack of plain boxes sits on the floor beside them.
   Must read: passing every requirement.
   Avoid: a shop with prices; a person failing; a queue.

10. `overtuigd-zijn-van-het-tegendeel.png` — Dutch chunk: overtuigd zijn van (to be convinced of).
   Scene: One person stands with chin lifted and both arms folded, looking steadily at a second figure who points at a plain panel on the wall.
   Must read: sure of one's own view.
   Avoid: a handshake; a person reading; a crowd.

CONTRAST PAIRS
Three and four both use an edge or a stopping edge: a step where a warning hand goes out, and a closed door with a shoulder against it. Same standing camera; subject 3 has a second walking figure, subject 4 is alone.
Seven and eight are `uitkomen voor` against `bezwaar maken tegen`: a chest hand and unfolded arms, then the same blank sheet pushed back with a flat stop hand. Keep the sheet and the standing pair identical.
One, two, five, six, nine and ten are singles. subject 2 and subject 10 are both two figures facing each other; in subject 2 the hand reaches to a hunched shoulder, in subject 10 arms fold against a pointing finger.
subject 5 reuses the courtroom archetype with a bare chair only; subject 9 reuses the office archetype with a board.

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

## Batch B1+-17 — images 161–170

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `genieten-van-de-stilte.png` — Dutch chunk: genieten van (to enjoy).
   Scene: One person sits with eyes closed and the head tilted back slightly in a room with a single open window, both hands relaxed on the thighs; no other objects are drawn.
   Must read: pleasure in quiet.
   Avoid: a party; a radio; a person talking.

2. `terugdeinzen-voor-de-klus.png` — Dutch chunk: terugdeinzen voor (to shrink back from).
   Scene: One person steps back with one hand raised palm outward in front of a cluttered workbench and a heavy tool lying on it, feet angled away.
   Must read: pulling away from work.
   Avoid: a finished task; a person working happily; a queue.

3. `opdraaien-voor-de-kosten.png` — Dutch chunk: opdraaien voor (to bear, to be liable for).
   Scene: One person holds out both hands open beneath a small pile of plain receipts held by another figure, who is about to let them drop.
   Must read: being left to pay.
   Avoid: a bank with banknotes; a shop till; a handshake.

4. `afzien-van-de-vergoeding.png` — Dutch chunk: afzien van (to forgo).
   Scene: One person holds the same plain receipts in both hands and pushes them back towards the other figure with a flat palm above them.
   Must read: giving up a claim.
   Avoid: a queue; a person counting money; a crowd.

5. `berusten-op-een-vermoeden.png` — Dutch chunk: berusten op (to rest on, to be founded on).
   Scene: One person stands with one hand flat on a small plain stone block and looks towards a second who holds up an empty open hand.
   Must read: a weak foundation.
   Avoid: a handshake; a person signing; a building site.

6. `uitmonden-in-een-akkoord.png` — Dutch chunk: uitmonden in (to result in, to end in).
   Scene: Two people stand facing each other with the near hands joined in a handshake while their other hands still hold sheets at their sides.
   Must read: an outcome reached at last.
   Avoid: a courtroom; a crowd; a person alone.

7. `instaan-voor-de-kwaliteit.png` — Dutch chunk: instaan voor (to vouch for).
   Scene: One person lays one hand flat on a plain finished object on a bench and the other hand on the chest, facing a customer who leans in.
   Must read: standing behind the work.
   Avoid: a shop with prices; a machine running; a crowd.

8. `gebukt-gaan-onder-de-druk.png` — Dutch chunk: gebukt gaan onder (to labour under).
   Scene: One person carries a large plain sack on the back with both straps in the hands, knees bent and neck lowered; the sack is the largest shape.
   Must read: carrying a heavy burden.
   Avoid: a person with a suitcase; a hiker on a hill; a queue.

9. `delen-in-het-succes.png` — Dutch chunk: delen in (to share in).
   Scene: Two people stand beside a plain podium with one hand each on its edge, both turned towards the viewer with heads level.
   Must read: sharing a result together.
   Avoid: a trophy with names; a crowd cheering; one person alone.

10. `uitblinken-in-een-vak.png` — Dutch chunk: uitblinken in (to excel at).
   Scene: One person stands at a bench holding up a plain finished object with both hands above head height, while three others lean in from behind to look.
   Must read: standing out through skill.
   Avoid: a trophy; a queue; a crowd outside.

CONTRAST PAIRS
One, two and ten all show one person against a room or a bench: quiet enjoyment with the head back, a step back from a heavy tool, and an object held up by a bench. Keep the window in subject 1, the cluttered bench in subject 2 and the clean bench in subject 10.
Three and four are `opdraaien voor` against `afzien van`: the same hands and the same plain receipts, once received open-handed, once pushed back with a flat palm. Keep the second figure identical.
Eight and nine are `gebukt gaan onder` against `delen in`: a sack on the back with bent knees, and two hands on a podium edge. Same standing camera; one figure in subject 8, two in subject 9.
Five, six and seven are singles. subject 6 and subject 7 both have two people standing and holding paper or an object; the handshake and the finished object must read differently.

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

## Batch B1+-18 — images 171–180

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `uitwijken-naar-de-zijkant.png` — Dutch chunk: uitwijken naar (to move aside to).
   Scene: One person steps sideways towards a plain painted margin on a wide floor while a heavy plain crate is rolled past on the other side by nobody visible; the step is the main diagonal.
   Must read: getting out of the way.
   Avoid: a fire exit with a sign; a crowd; a person falling.

2. `voorbijgaan-aan-de-vraag.png` — Dutch chunk: voorbijgaan aan (to pass over, to ignore).
   Scene: One person walks past a second figure who holds up a blank sheet with both hands and leans towards them; the walker's head faces straight ahead.
   Must read: walking past a question.
   Avoid: two people shaking hands; a queue; a crowd.

3. `ingaan-op-het-verzoek.png` — Dutch chunk: ingaan op (to go into, to accept).
   Scene: One person sits down on a chair opposite a standing figure who holds the same blank sheet, one hand already open towards the offered seat.
   Must read: accepting someone's request.
   Avoid: a queue at a counter; a person leaving; a crowd.

4. `afkomen-op-het-geluid.png` — Dutch chunk: afkomen op (to come towards, to head for).
   Scene: One person walks quickly towards a small plain bell on a table with one hand already out, drawn from the far side of the room.
   Must read: moving towards a signal.
   Avoid: a busy street; a crowd; a person running from something.

5. `terugkomen-op-een-besluit.png` — Dutch chunk: terugkomen op (to return to, to reverse).
   Scene: One person stands at a desk with a blank sheet in one hand and draws it back towards the chest while a finger of the other hand points at the same sheet.
   Must read: reversing what was decided.
   Avoid: a person signing for the first time; a queue; a handshake.

6. `zich-neerleggen-bij-het-besluit.png` — Dutch chunk: zich neerleggen bij (to resign oneself to).
   Scene: One person opens both hands palms down above a table and lets a blank sheet fall flat onto it, both hands lifting away.
   Must read: dropping an idea.
   Avoid: a person signing; a torn sheet; a crowd.

7. `voortborduren-op-een-idee.png` — Dutch chunk: voortborduren op (to build on).
   Scene: One person places a second plain block onto a small stack already begun by a colleague and taps the top block once.
   Must read: continuing another's work.
   Avoid: a person starting from nothing; a queue; a handshake.

8. `vasthouden-aan-het-standpunt.png` — Dutch chunk: vasthouden aan (to stick to).
   Scene: One person grips the edge of a desk with both hands and leans forward, chin down, while a second figure has both arms open and raised in appeal.
   Must read: refusing to give ground.
   Avoid: a person agreeing; a handshake; a crowd.

9. `toegeven-aan-de-druk.png` — Dutch chunk: toegeven aan (to give in to).
   Scene: One person lets go of the same desk edge and settles back into the chair, shoulders dropping, while the appealing figure lowers their arms.
   Must read: giving way.
   Avoid: a person leaving the room; a queue; an argument with bubbles.

10. `afhangen-van-een-telefoontje.png` — Dutch chunk: afhangen van (to depend on).
   Scene: One person sits with a plain telephone receiver held to the ear and one hand flat on the table, waiting; the other chair at the table is empty.
   Must read: an outcome not yet known.
   Avoid: a person talking happily on the phone; a queue; a clock.

CONTRAST PAIRS
One and the painted margin: only subject 1 has a line on the floor. Do not reuse it in other frames in this batch.
Two and three are `voorbijgaan aan` against `ingaan op`: the same raised blank sheet, once walked past with the head forward, once accepted with a hand to a chair. Keep the sheet identical.
Four, five and six all turn on paper on a table: a bell being approached, a sheet drawn back to the chest, a sheet dropped from open palms. Three distinct hand positions.
Seven and eight are `voortborduren op` against `vasthouden aan`: building a stack upwards, and gripping the desk edge. Both upright; the stack is small and low, the grip is at waist height.
Nine is the release of subject 8; keep the chair and the second figure in the same places.
Ten is a single; the telephone has no numbers or screen.

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

## Batch B1+-19 — images 181–190

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `afhankelijk-van-een-uitkering.png` — Dutch chunk: afhankelijk van (to depend on).
   Scene: One person stands with an open hand underneath a plain sheet being held out by a second figure; the receiver's posture is upright but the head is lowered.
   Must read: leaning on someone's support.
   Avoid: a bank with banknotes; a shop; a handshake between equals.

2. `gehecht-aan-de-eigen-buurt.png` — Dutch chunk: gehecht aan (to be attached to).
   Scene: One person stands with one hand flat against the outside wall of a plain building and the other resting over the chest, face towards the wall.
   Must read: belonging to a place.
   Avoid: a person moving house with boxes; a map; a crowd.

3. `bereid-tot-een-gesprek.png` — Dutch chunk: bereid tot (to be willing to).
   Scene: One person pulls an empty chair out from a table with both hands and turns it towards a second figure, one hand open over the seat.
   Must read: ready to talk.
   Avoid: a person leaving; a crowd; a phone call.

4. `bereid-tot-opoffering.png` — Dutch chunk: bereid tot (to be prepared to).
   Scene: One person stands with one hand on the back of a chair and the other held out flat, offering the better seat to a second figure who is already sitting.
   Must read: giving up something for another.
   Avoid: a queue; a handshake; a crowd.

5. `geschikt-voor-kinderen.png` — Dutch chunk: geschikt voor (to be suitable for).
   Scene: One person hands a small plain rounded object to a small figure with both hands, while the small figure holds another of the same shape.
   Must read: right for someone young.
   Avoid: a playground; a shop; a crowd.

6. `geschikt-voor-een-krappe-ruimte.png` — Dutch chunk: geschikt voor (to be suitable for).
   Scene: One person crouches in a narrow gap between two plain walls, turning a flat board sideways with both hands to fit it against the gap.
   Must read: right for a tight place.
   Avoid: two people; a shop with prices; a crowd.

7. `tevreden-over-de-uitslag.png` — Dutch chunk: tevreden over (to be satisfied with).
   Scene: One person sits with a blank sheet held loosely in one hand and leans back, a single raised line for a smile; one elbow rests on the desk.
   Must read: pleased with a result.
   Avoid: a person disappointed; a crowd cheering; a tray of food.

8. `trots-op-het-kind.png` — Dutch chunk: trots op (to be proud of).
   Scene: One person stands behind a small figure with both hands on the small figure's shoulders, chin up and chest forward, looking at the viewer.
   Must read: pride in someone.
   Avoid: a trophy; a crowd; a person alone on a podium.

9. `verantwoordelijk-voor-de-veiligheid.png` — Dutch chunk: verantwoordelijk voor (to be responsible for).
   Scene: One person stands at the foot of a plain flight of steps with a hand on the rail, looking up at two figures on the top step.
   Must read: being answerable for others.
   Avoid: a police officer with a badge; a crowd; a machine.

10. `verlegen-om-een-antwoord.png` — Dutch chunk: verlegen om (to be short of, to need).
   Scene: One person stands with both hands open and empty in front of a second figure who has turned their back and is shutting a drawer.
   Must read: having nothing to answer with.
   Avoid: a person begging; a bank; a crowd.

CONTRAST PAIRS
One and two are `afhankelijk van` against `gehecht aan`: a sheet received in an open hand, and a hand flat on a wall. Keep the standing figure identical and change only the object.
Three and four are both `bereid tot`: a chair turned towards someone, and the better seat given away. Same chair; in subject 3 it is empty and offered, in subject 4 it is occupied by the other.
Seven and eight are `tevreden over` against `trots op`: pleasure in a result, and pride in a person. Keep the camera at the same height; subject 7 is seated, subject 8 stands behind a small figure.
Five and six both use the same chunk in different senses: an object handed to a child, and a board turned in a narrow gap. Different rooms, no repetition of the other's objects.
Nine and ten are singles. subject 10's back-turned figure reuses the folded-arms idea only in the shoulders; the drawer is the marker.

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

## Batch B1+-20 — images 191–200

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `aandacht-voor-de-details.png` — Dutch chunk: aandacht voor (attention for).
   Scene: One person leans low over a small object on a bench, both hands framing it, while another larger object beside it is left untouched.
   Must read: close attention to small things.
   Avoid: a crowd; a shop with prices; a person away from the bench.

2. `onverschillig-voor-de-uitslag.png` — Dutch chunk: onverschillig voor (indifferent to).
   Scene: One person accepts a blank sheet held out by another with a loose grip and turns it face down on the table without looking at it.
   Must read: not caring about a result.
   Avoid: a person disappointed; a crowd; a torn sheet.

3. `tevreden-met-de-uitkomst.png` — Dutch chunk: tevreden met (to be satisfied with).
   Scene: One person holds a plain cup with both hands and sits back with shoulders relaxed, a single line for a smile; a closed folder lies on the table.
   Must read: content with what there is.
   Avoid: a person disappointed; a crowd; a tray of food.

4. `vertrouwd-met-het-systeem.png` — Dutch chunk: vertrouwd met (to be familiar with).
   Scene: One person's hands move easily over a plain control panel, two switches already turned, without looking down; their eyes are on a colleague.
   Must read: knowing something by habit.
   Avoid: a manual on a stand; a person reading; a crowd.

5. `belangrijk-voor-de-zaak.png` — Dutch chunk: belangrijk voor (to matter to).
   Scene: One person holds up a single plain block between two fingers and turns to a seated figure who has leaned forward, both hands on the table edge.
   Must read: something that counts.
   Avoid: a crowd; a shop with prices; a trophy.

6. `bezorgd-om-de-lage-cijfers.png` — Dutch chunk: bezorgd om (to be worried about).
   Scene: One person sits with a plain sheet of three descending horizontal bars in both hands, eyebrows drawn down, and turns to a colleague in the next chair.
   Must read: anxiety about numbers.
   Avoid: the shipped mess scene; a crowd; a celebration.

7. `afhankelijk-van-goed-weer.png` — Dutch chunk: afhankelijk van (to depend on).
   Scene: One person stands with a folded plain tarp in both hands, looking up at three small cloud shapes; a set of stacked crates sits beside them ready to cover.
   Must read: held up by the sky.
   Avoid: rain falling on a person; a weather chart; a bus.

8. `tevreden-over-het-werk.png` — Dutch chunk: tevreden over (to be satisfied with).
   Scene: One person steps back half a pace from a plain painted wall with a roller in one hand, head tilted, both edges of the painted area straight.
   Must read: happy with the job done.
   Avoid: a person with a bucket of numbers; a crowd; a handshake.

9. `verantwoordelijk-voor-de-afdeling.png` — Dutch chunk: verantwoordelijk voor (to be responsible for).
   Scene: One person stands at a doorway with one hand open towards the room behind them, in which four figures sit at desks; the open hand is the shape.
   Must read: answerable for a group.
   Avoid: a crowd outside; a machine; a queue.

10. `trots-op-de-eigen-afkomst.png` — Dutch chunk: trots op (to be proud of).
   Scene: One person stands with one arm across the chest and the other lifted open, facing a plain repeated shape drawn three times behind them as a simple pattern of circles.
   Must read: pride in where one comes from.
   Avoid: a flag with a mark; a crowd; a trophy.

CONTRAST PAIRS
One and two are `aandacht voor` against `onverschillig voor`: hands framing a small object, and a sheet turned face down unread. Same standing and seated camera; subject 1 is at a bench, subject 2 at a desk.
Three, four and eight all involve a settled result: a cup held in both hands, hands on a familiar panel, and a step back from a painted wall. Keep three different rooms and three different objects.
Five, six and seven are singles. subject 6's bars are plain descending rectangles with no numerals; subject 7's tarp is folded, not draped over a person.
Nine and ten both use a person facing the viewer with an open arm. In subject 9 the arm opens into a room of desks; in subject 10 it opens towards a repeated circle pattern on the wall. The repetition must be identical shapes, not a flag or a crest.

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

## Batch B1+-21 — images 201–210

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `behoefte-aan-stilte.png` — Dutch chunk: behoefte aan (need for).
   Scene: One person lies flat on a plain bench with an arm across the eyes and both legs along the bench; a single open door lets in one plain stroke of light.
   Must read: a need for rest.
   Avoid: a person asleep in bed; a crowd; a cup of coffee.

2. `kans-op-een-baan.png` — Dutch chunk: kans op (chance of).
   Scene: One person stands at a door with a blank sheet in one hand and the other hand raised towards a plain knocker shape on the door.
   Must read: a possibility that must be tried.
   Avoid: a queue outside; a crowd; a phone.

3. `risico-op-een-ongeluk.png` — Dutch chunk: risico op (to risk of).
   Scene: One person walks along a narrow raised edge with arms spread for balance, one foot just ahead of the other; nothing supports the edge below.
   Must read: the danger of falling.
   Avoid: a person jumping; a crowd; a warning sign.

4. `moeite-met-de-uitspraak.png` — Dutch chunk: moeite met (difficulty with).
   Scene: One person sits facing a second figure and holds one hand near the mouth while the listener leans in, one hand cupped behind the ear.
   Must read: struggling to be understood.
   Avoid: a crowd; a person singing; a phone.

5. `zin-in-een-ommetje.png` — Dutch chunk: zin in (a wish for, in the mood for).
   Scene: One person stands in an open doorway with a plain pair of boots already in one hand and one hand on the door frame, leaning out.
   Must read: wanting to go outside.
   Avoid: the shipped coffee scene; a crowd; a bus.

6. `belang-bij-een-oplossing.png` — Dutch chunk: belang bij (interest in).
   Scene: One person sits at a table with both hands on top of a loose blank sheet, leaning forward, while a second figure opposite holds a pen ready.
   Must read: having a stake in the answer.
   Avoid: a crowd; a shop with prices; a bank.

7. `gebrek-aan-handen.png` — Dutch chunk: gebrek aan (lack of).
   Scene: One person stands with an upturned empty bag open at the bottom and gives it a small shake; a large plain clock face with tick marks hangs behind.
   Must read: running out of time.
   Avoid: a person rushing; a cup; a calendar.

8. `verband-tussen-roken-en-longklachten.png` — Dutch chunk: verband tussen (connection between).
   Scene: Two plain objects are drawn apart on a table, a rolled paper tube on one side and a small round form on the other, with a single straight line linking them.
   Must read: one thing causing another.
   Avoid: a crowd; a chart with numbers; a person smoking.

9. `vertrouwen-in-de-afspraak.png` — Dutch chunk: vertrouwen in (trust in).
   Scene: One person stands with head up and both hands open at the sides, facing a wide gap between two tall plain blocks; one small bird shape curves above the gap.
   Must read: belief in what comes next.
   Avoid: a bird cage; a crowd; a clock.

10. `twijfel-aan-de-bedoeling.png` — Dutch chunk: twijfel aan (doubt about).
   Scene: One person holds a blank sheet at arm's length with one hand and tilts it, one shoulder raised, mouth pulled to one side.
   Must read: not understanding the intent.
   Avoid: two people arguing; a crowd; a shop.

CONTRAST PAIRS
One, five, seven and nine are singles. subject 1's light stroke is a plain shape from the door, not a beam with rays. subject 7's bag is open at the bottom, not just empty, so it reads as lacking.
Two and three are `kans op` against `risico op`: a knocker on a door, and a narrow edge with arms spread. Same standing camera.
Four and five both involve the mouth or the boots at the door; subject 4 is speaking with difficulty, subject 5 is ready to walk. Keep the ear-cupping listener only in subject 4.
Six and seven are singles that could be confused: a stake in a solution is a seated pair with a pen; a lack of time is a shake of an empty bag. Keep them in different rooms.
Eight and ten are singles. The linking line in subject 8 is a single stroke between two objects, not an arrow.

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

## Batch B1+-22 — images 211–220

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `reden-voor-de-klacht.png` — Dutch chunk: reden voor (reason for).
   Scene: One person stands at a counter with a broken plain appliance held in both hands, showing it to a clerk who leans over it.
   Must read: justification for complaining.
   Avoid: the shipped counter complaint; a crowd; a phone.

2. `beschuldiging-van-diefstal.png` — Dutch chunk: beschuldiging van (accusation of).
   Scene: One person points a flat hand at a second figure's open bag on a table, while the bag's owner stands with both hands up in protest.
   Must read: being blamed for taking something.
   Avoid: a police officer; a courtroom; a crowd.

3. `oplossing-voor-de-storing.png` — Dutch chunk: oplossing voor (solution for).
   Scene: One person places a plain key into a socket on a large closed box and turns it; the box lid opens a crack.
   Must read: something that unlocks a difficulty.
   Avoid: a crowd; a shop; a bank.

4. `gevolg-van-een-fout.png` — Dutch chunk: gevolg van (consequence of).
   Scene: One person stands looking at a plain wall panel with a long crack running down it while a second figure lowers their head, one hand on a tool.
   Must read: what a mistake leaves behind.
   Avoid: a crowd; a fire; a machine running.

5. `ervaring-met-moeilijke-klanten.png` — Dutch chunk: ervaring met (experience with).
   Scene: One person stands behind a counter and listens calmly with both hands on the counter as a customer leans over it with a raised fist shape.
   Must read: having dealt with this before.
   Avoid: a crowd; a shop with prices; a queue.

6. `kennis-van-de-regels.png` — Dutch chunk: kennis van (knowledge of).
   Scene: One person holds a small ruled booklet open in both hands and taps one page while a standing colleague looks on with a raised eyebrow.
   Must read: knowing the rules.
   Avoid: a courtroom with a judge; a crowd; a phone.

7. `invloed-op-de-uitslag.png` — Dutch chunk: invloed op (influence on).
   Scene: One person leans over a table and moves one of three plain blocks with a single finger while two seated figures watch the block position.
   Must read: changing an outcome.
   Avoid: a handshake; a crowd; a phone.

8. `gebrek-aan-informatie.png` — Dutch chunk: gebrek aan (lack of).
   Scene: One person holds an open empty folder towards a colleague and turns both hands palm up; the colleague shakes their head with a shrug.
   Must read: nothing to go on.
   Avoid: a full folder; a crowd; a phone.

9. `oorzaak-van-de-vertraging.png` — Dutch chunk: oorzaak van (cause of).
   Scene: One person kneels beside a stalled machine with a loose belt hanging in one hand, while another figure checks the clock face above.
   Must read: what held everything up.
   Avoid: a crowd; a fire; a traffic jam.

10. `belangstelling-voor-het-onderwerp.png` — Dutch chunk: belangstelling voor (interest in).
   Scene: One person leans across a table towards a small plain object with both hands lifted open, eyes fixed on it; a colleague beside them is turned away.
   Must read: keen attention to a subject.
   Avoid: a crowd; a shop with prices; a person asleep.

CONTRAST PAIRS
One and two are `reden voor` against `beschuldiging van`: a broken appliance shown at a counter, and an open bag pointed at. Keep the counter and the clerk, and swap the object.
Three and four are `oplossing voor` against `gevolg van`: a key turning in a box, and a cracked panel with a lowered head. Same workshop; one is fixed, one is already broken.
Five and the earlier difficult-customer frame share the counter; here the clerk's hands rest calmly on it and the customer's hand is a fist shape at the shoulder.
Six and seven are single and paired with 8: a booklet read, blocks moved by one finger, and an empty folder. Three different hand positions on paper or blocks.
Eight, nine and ten are `gebrek aan`, `oorzaak van` and `belangstelling voor`: empty folder, loose belt, hands open towards an object. Keep three distinct objects.

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

## Batch B1+-23 — images 221–230

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `op-de-hoogte-zijn-van-de-plannen.png` — Dutch chunk: op de hoogte zijn van (to be informed about).
   Scene: One person stands with a folded blank paper in one hand and touches the brow with the fingers of the other, a small satisfied nod; a second figure raises a thumb-less open hand in thanks.
   Must read: having the news.
   Avoid: a crowd; a phone screen; a newsroom.

2. `op-de-hoogte-houden-van-het-nieuws.png` — Dutch chunk: op de hoogte houden van (to keep informed of).
   Scene: One person hands a folded blank paper to a colleague who is seated and reaching for it, the giver's other hand still on a drawer of papers.
   Must read: passing news on.
   Avoid: a crowd; a phone; a queue.

3. `op-de-hoogte-brengen-van-het-plan.png` — Dutch chunk: op de hoogte brengen van (to inform about).
   Scene: One person stands talking to a seated figure, one hand open and the other holding a rolled blank sheet that is not yet unrolled.
   Must read: telling someone officially.
   Avoid: a crowd; a phone; a handshake.

4. `rekening-houden-met-het-verkeer.png` — Dutch chunk: rekening houden met (to take into account).
   Scene: One person stops at a kerb and looks both ways, one hand steadying a plain bag; a moving plain shape passes in the distance.
   Must read: allowing for what is out there.
   Avoid: a traffic sign with a mark; a crowd; a bus.

5. `rekening-houden-met-de-gevoelens.png` — Dutch chunk: rekening houden met (to take into account).
   Scene: Two people sit facing each other, one leaning forward with both hands raised gently open; the other has a hand over the heart.
   Must read: allowing for another's feelings.
   Avoid: a crowd; a handshake; a meeting table.

6. `tot-stand-brengen-van-een-akkoord.png` — Dutch chunk: tot stand brengen (to bring about).
   Scene: Two people push a heavy plain slab upright together so that its top edge stands level; both lean in with both hands.
   Must read: getting something done.
   Avoid: a crowd; a handshake; a broken wall.

7. `ter-beschikking-stellen-van-ruimte.png` — Dutch chunk: ter beschikking stellen van (to make available to).
   Scene: One person opens both arms towards a bare room with a table and two chairs, one hand flat towards the table top.
   Must read: offering a place to use.
   Avoid: a crowd; a shop; a bank.

8. `gebruik-maken-van-de-kans.png` — Dutch chunk: gebruik maken van (to make use of).
   Scene: One person steps through an open doorway with one hand already on the frame and a plain bag in the other, head turned back towards a seated figure who waves them on.
   Must read: seizing an offered opening.
   Avoid: a crowd; a queue; a person alone.

9. `in-het-oog-houden-van-de-klant.png` — Dutch chunk: in het oog houden (to keep an eye on).
   Scene: One person stands behind a counter with both hands flat on its top, watching a customer move through a plain room; the head is turned but the hands stay.
   Must read: watching while others move.
   Avoid: a crowd; a queue; a phone.

10. `tekortschieten-in-de-dienstverlening.png` — Dutch chunk: tekortschieten in (to fall short in).
   Scene: One person behind the counter has both hands open and empty over the counter while a customer taps the counter top with one finger.
   Must read: failing to deliver.
   Avoid: a crowd; a shop with prices; a queue.

CONTRAST PAIRS
One, two and three all turn on a paper folded or rolled: held and tapped at the brow, handed over, and kept rolled while talking. Keep the sheet's state distinct in each.
Four and 5 use the same chunk in two senses: traffic at a kerb, and feelings across a table. Do not reuse the kerb in the second.
Seven and eight are `ter beschikking stellen van` against `gebruik maken van`: arms opening towards a bare room, and a step through a doorway. Same room and door, opposite movement.
Six and nine are singles. subject 9's customer moves through a plain room, not through a queue.
Ten is the empty-handed mirror of subject 9: the same counter, one figure watching and one figure tapping.

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

## Batch B1+-24 — images 231–240

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `in-het-kader-van-het-project.png` — Dutch chunk: in het kader van (within the framework of).
   Scene: One person holds a large plain frame of four joined planks upright and stands behind it, with a second figure looking through from the other side.
   Must read: inside a set boundary.
   Avoid: a crowd; a shop; a sign with a mark.

2. `met-succes-afronden-van-de-klus.png` — Dutch chunk: met succes afronden (to complete successfully).
   Scene: One person sets the last of a short row of plain boxes onto a shelf, both hands still on it, while a colleague behind nods once.
   Must read: finishing well.
   Avoid: a crowd; a trophy; a calendar.

3. `een-verzoek-indienen-bij-de-afdeling.png` — Dutch chunk: een verzoek indienen bij (to submit a request to).
   Scene: One person slides a blank envelope into a slot in a plain wall panel; the slot is wide and empty, without a label.
   Must read: handing paperwork onward.
   Avoid: a crowd; a queue; a phone.

4. `afgehandeld-worden-door-de-afdeling.png` — Dutch chunk: afgehandeld worden door (to be dealt with by).
   Scene: One seated figure takes the same blank envelope out of a tray and slits it open with a small plain knife, a stack of similar envelopes beside them.
   Must read: the paperwork lands on someone's desk.
   Avoid: a crowd; a queue; a phone.

5. `in-het-beheer-zijn-van-de-directie.png` — Dutch chunk: in het beheer zijn van (to be managed by).
   Scene: One person hands a plain key to another, who closes both hands over it; a large plain door stands behind them with no signs.
   Must read: control passing to someone else.
   Avoid: a crowd; a shop; a bank.

6. `de-verantwoordelijkheid-dragen-voor-het-budget.png` — Dutch chunk: de verantwoordelijkheid dragen voor (to carry responsibility for).
   Scene: One person holds a large plain ledger book in both arms against the chest, chin just above the top edge of it.
   Must read: carrying the weight of an account.
   Avoid: a bank with banknotes; a crowd; a trophy.

7. `zich-verantwoorden-voor-het-bestuur.png` — Dutch chunk: zich verantwoorden voor (to account for oneself to).
   Scene: One person stands facing three seated figures at a long table, both hands open and lowered; the three have blank sheets in front of them.
   Must read: being called to explain.
   Avoid: a crowd; a courtroom with a judge; a handshake.

8. `verantwoording-afleggen-aan-de-leden.png` — Dutch chunk: verantwoording afleggen aan (to give an account to).
   Scene: The same three seated figures receive one standing figure who now holds a plain sheet open in both hands, showing it towards them.
   Must read: showing the numbers to the members.
   Avoid: a crowd; a queue; a bank.

9. `de-waarde-bepalen-van-het-object.png` — Dutch chunk: de waarde bepalen van (to determine the value of).
   Scene: One person holds a straight rule against a plain object on a table while a second figure writes on a small pad held in one hand.
   Must read: working out what something is worth.
   Avoid: a bank with banknotes; a shop with prices; a crowd.

10. `een-factuur-versturen-naar-de-klant.png` — Dutch chunk: een factuur versturen naar (to send an invoice to).
   Scene: One person folds a blank sheet into an envelope and holds it above a plain outgoing tray; a small stack of envelopes sits behind the tray.
   Must read: billing someone afterwards.
   Avoid: a crowd; a bank with banknotes; a shop.

CONTRAST PAIRS
One, five and six are singles on structure: an empty frame held upright, a key passing between hands, and a plain ledger hugged to the chest. Keep the frame larger than a person's shoulders and the ledger thick.
Two and 3 share a short row of plain boxes and a blank envelope: finishing a shelf, then pushing paperwork towards a slot.
Three and four are the same envelope: pushed through a slot, then slit open in a tray. The second image must not show the slot.
Seven and eight are the same long table and the same three seated figures; in subject 7 the standing figure's hands are open and empty, in subject 8 they hold the open sheet.
Nine and 10 close the loop: a rule and a pad, then a folded envelope above a tray.

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

## Batch B1+-25 — images 241–250

````text
You have no file access. Do not ask to read any repository, document, image or attachment. Everything you need is in this message.

TASK
Generate ten separate images for a Dutch practice game called Voorzetselpaden, and nothing else. Each image is a wordless clue for one Dutch chunk built on a preposition. The learner sees the image, recognises the situation, and connects it to the chunk. A Dutch speaker must be able to name the situation from the drawing alone, without a caption. The Dutch and English below are context for you only. None of those words may appear in the image.

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

1. `de-vinger-op-de-zere-plek-leggen.png` — Dutch chunk: de vinger op de zere plek leggen (to put one's finger on the sore spot).
   Scene: One person presses a single finger flat onto a small plain patch on a colleague's shoulder while the colleague winces and pulls away; the patch is a simple filled oval.
   Must read: naming exactly what hurts.
   Avoid: a crowd; a shop; a phone.

2. `olie-op-het-vuur-gooien.png` — Dutch chunk: olie op het vuur gooien (to add fuel to the fire).
   Scene: One figure stands between two others leaning towards each other with fists, and tips a plain can forward over their heads; a small plain flame shape rises between them.
   Must read: making an argument worse.
   Avoid: a crowd; a kitchen; a camp fire.

3. `een-klap-in-het-gezicht-zijn.png` — Dutch chunk: een klap in het gezicht zijn (to be a slap in the face).
   Scene: One person turns their head sharply aside with one hand raised to the cheek while a second figure behind stands with a blank sheet held out; the turned head is the mass.
   Must read: an insult that lands.
   Avoid: a boxing match; a crowd; two people fighting.

4. `met-de-deur-in-huis-vallen.png` — Dutch chunk: met de deur in huis vallen (to come straight to the point).
   Scene: One person steps through an already open door with one foot in the room and one hand already pointing at a table.
   Must read: arriving straight at the matter.
   Avoid: a crowd; a phone; a closed door.

5. `niet-op-de-hoogte-zijn.png` — Dutch chunk: niet op de hoogte zijn (to be unaware).
   Scene: One person looks up from a plain desk with a tilted head and both hands flat, towards a second figure who holds a folded blank paper out towards them.
   Must read: the news has not arrived.
   Avoid: a crowd; a phone; a queue.

6. `ophef-maken-over-een-klein-probleem.png` — Dutch chunk: ophef maken over (to make a fuss about).
   Scene: One person stands with both arms flung back and mouth open wide, chin thrust down towards a single small plain cup on the corner of a table; two others turn to look with raised eyebrows.
   Must read: an outsize protest about something tiny.
   Avoid: a crowd; a shop; a phone.

7. `tegen-de-klippen-opzien.png` — Dutch chunk: tegen de klippen opzien (to dread something).
   Scene: One person stands at the bottom of a steep plain slope with a hand shading the eyes, looking up; two block shapes at the top are the obstacle.
   Must read: fearing a climb ahead.
   Avoid: a crowd; a mountain range; a bus.

8. `geduld-hebben-met-de-drukte.png` — Dutch chunk: geduld hebben met (to be patient with).
   Scene: One person stands at a counter with a plain ticket in one hand and the other hand resting calmly at the side, while the clerk behind the counter deals slowly with a second customer; a short queue of two figures waits ahead.
   Must read: keeping calm while others are slow.
   Avoid: a crowd; a phone; a clock with hands.

9. `de-vruchten-plukken-van-het-werk.png` — Dutch chunk: de vruchten plukken van het werk (to reap the rewards).
   Scene: One person stands beside a small plain tree with three round fruit shapes on it, one hand already cupped around the lowest fruit.
   Must read: enjoying what one sowed.
   Avoid: a garden with flowers; a market; a crowd.

10. `niet-door-de-mandel-kunnen.png` — Dutch chunk: niet door de mand kunnen vallen (to be exposed).
   Scene: One person stands on a plain bench with one foot on the edge of a woven basket that is giving way beneath them, arms flung out.
   Must read: the pretence collapses.
   Avoid: a crowd; a broken chair; a market stall.

CONTRAST PAIRS
One, two and three all involve a sharp reaction from a second figure; keep subject 1's patch, subject 2's tipped can, subject 3's held sheet as three clearly different objects, and only one figure reacts in each.
Four, five and six are office singles: a step through an open door, a tilted head with a folded paper, and a wide open mouth with two calm onlookers. Keep subject 6's onlookers still, not laughing.
Seven, eight, nine and ten are singles with one main shape each: a slope, a queue at a counter, a small tree with three fruit, and a basket underfoot.
No frame may show a weapon, a fist in contact, or readable text.

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

For each batch that comes back:

1. **Process the PNGs** as `game-art.md` says under *Delivered raster art*:
   trim, keep the cobalt ink, make the white transparent, export at
   512 × 763. Check one frame at 64 × 64 before batching the rest.
2. **Rename nothing.** The delivered filename is the scene id. If a frame came
   back with the wrong subject, redraw it rather than renaming a different
   image to fit.
3. **Add to `server/Oefenpad.Resources/Games/Data/prepositions.json`.** One scene per frame, chunk as the
   `chunk`, gloss as the English, and the batch's contrast pairs set with the
   same partner field the pilot scenes use. Keep the order of this file: a
   batch is a walk, not a list.
4. **Second `bouw` sentence for singles.** Every frame whose note says
   `Single` needs its own build sentence that puts the chunk in a plain
   sentence of its own; a pair already has its partner sentence, so it does
   not get a second one unless the pair is split.
5. **Update the status** in the tracker from `needed` to `drawn`, and to
   `dropped` for anything cut after review. Leave the rest of the row alone.
6. **Run the game.** Check that every new scene id resolves to a file, that no
   pair points at a missing partner, and that a 64 px thumbnail is still
   readable in the strip on the Ontdek screen.

Do not ship a register batch before its pair partners from a neighbouring
batch are drawn, or set the partner field to a placeholder. Many pairs cross
between batches (for example B1+-02 subject 5 with B1+-01 subject 1, and B1+-05
subjects 1, 4 and 7 with B1+-04 subjects 4, 2 and 5); the tracker note names the
partner file in each case, so draw those two batches together. A partner that
names a file from `prepositions-art-b2.md` sits in the next band: draw the two
bands in order rather than booking the pair in advance.
