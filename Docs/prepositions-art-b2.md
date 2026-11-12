# Voorzetselpaden — image plan, B2

Status: planning document, 10 November 2026. This is the **B2** band: the
specialist registers, the low-frequency receptive material and the coverage
close-out. It covers roadmap batches 24–32 of `prepositions-roadmap.md`.

The plan was split on 10 November 2026. What used to be one 460-frame B2 file is
now two — **B1+** (`prepositions-art-b1-plus.md`, 250 frames, batches 14–23) and
**B2** (this file, 210 frames, batches 24–32). Nothing was added or cut in the
split.

Scope: **210 new frames**, planned as **21 self-contained Grok batches of ten**,
numbered B2-01 to B2-21. Each batch prints ten separate images.

What is excluded, and must not be redrawn or duplicated:

- The **30 pilot scenes** in `assets/voorzetselpaden/`, listed in
  `prepositions-art.md`.
- The **20 A0–A2 frames** in `prepositions-art-a0-a2.md`.
- The **17 batch-4b frames** in `prepositions-art-a2-pairs.md`.
- The **80 A2+ frames** in `prepositions-art-a2-plus.md`.
- The **120 B1 frames** in `prepositions-art-b1.md`.
- The **250 B1+ frames** in `prepositions-art-b1-plus.md`.

No frame in this file repeats any of those or another frame in this file.

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

## What B2 adds

Two hundred and ten frames in eight register themes and a coverage close-out,
from business and administration through academic, medical, legal and
journalistic Dutch to colloquial, literary and consolidating frames. The
register batches are a cross-cut, not an eighth category, exactly as
`prepositions-roadmap.md` §6 says: they draw from the verb, adjective, noun and
idiom pools rather than adding new grammar. B2-21 is the roadmap's batch-32
coverage close-out.

No frequency list exists in the repo, so the chunks are ordered by register and
usefulness, not by measured frequency. Re-cut any batch around a frequency list
when one arrives, per `prepositions-roadmap.md` §12.1; the art plan survives a
re-cut because each frame stands alone.

About a hundred of the 210 frames are contrast pairs: two frames that share a
verb, adjective, noun or chunk and differ only in the preposition, the sense or
the partner. The rest are singles. A single frame that belongs to no pair gets
an extra `bouw` sentence in `server/Oefenpad.Resources/Games/Data/prepositions.json`
after delivery, so the learner still meets it beside something familiar.

| Image batch | Theme | Frames | Roadmap batch |
|---|---|---|---|
| B2-01 – B2-03 | Business and administration | 30 | 24 |
| B2-04 – B2-06 | Academic and formal | 30 | 25 |
| B2-07 – B2-09 | Medical and technical | 30 | 26 |
| B2-10 – B2-12 | Legal and official | 30 | 27 |
| B2-13 – B2-14 | Journalistic and opinion | 20 | 28 |
| B2-15 – B2-16 | Colloquial and regional | 20 | 29 |
| B2-17 – B2-18 | Literary and idiomatic | 20 | 30 |
| B2-19 – B2-20 | Consolidation and exceptions | 20 | 31 |
| B2-21 | Unframed prepositions: coverage close-out | 10 | 32 |
| **Total** | | **210** | |

Observations on the scope, in the spirit of `prepositions-art-a2-plus.md`:

- The register batches reuse a small set of scene archetypes (office, counter,
  clinic, courtroom, newsroom, workshop), as the brief allows. Each image in a
  batch is still visually distinct, and the contrast note says when a scene is
  reused.
- B2-21 frames the nine prepositions that phases D and E named but no frame
  used. Several of those chunks are abstract and are drawn as a concrete
  situation; the gloss carries the abstraction, and the tracker note says so.
- Some chunks in these registers are correct and rare. The tracker note marks
  the ones that are receptive only, so the level can skip `Bouw` when it ships.

Status values in the tracker: `needed` (not drawn), `drawn` (delivered and
processed), `dropped` (cut after review).

## Tracker

All 210 frames, in batch order. The file column is the Grok filename and the
shipped scene id. "Pair / note" names the partner file for a pair, or says
`Single` plus the camera note.

| # | File | Dutch frame | English | Scene | Pair/note | Status |
|---|---|---|---|---|---|---|
| 1 | `een-bod-uitbrengen-op-het-pand.png` | een bod uitbrengen op | to make an offer on | One person stands in front of a plain building facade with a blank sheet held out in one hand towards a second… | Single. Office and street archetype. The facade is flat with two plain openings. | needed |
| 2 | `investeren-in-een-onderneming.png` | investeren in | to invest in | One person crouches and places a plain heavy block at the base of a low wall already partly built, both hands… | Single. Putting money into something that will grow; same camera as `zich-inzetten-voor-de-buurt`. | needed |
| 3 | `onderhandelen-over-het-tarief.png` | onderhandelen over | to negotiate about | Two people sit at a table with a plain object between them and both hands open above it, neither touching it | Haggling over a number; pair with `overeenstemming-bereiken-over-de-levering`. | needed |
| 4 | `overeenstemming-bereiken-over-de-levering.png` | overeenstemming bereiken over | to come to an agreement about | The same two people with one hand each flat on the same sheet, the object now pushed to one side | Settling on a deal; pair with `onderhandelen-over-het-tarief`. | needed |
| 5 | `sturen-op-omzetdoelen.png` | sturen op | to steer towards | One person stands in front of a wall panel with three plain bars of increasing height, one flat hand held under the… | Single. Office. Bars only; no numerals. | needed |
| 6 | `een-terugbetaling-regelen-met-de-bank.png` | een terugbetaling regelen met | to arrange a repayment with | One person at a counter hands a blank form to a clerk who points with one finger at a small plain box on the form | Single. Counter archetype. Form is blank with one box outline. | needed |
| 7 | `een-leverancier-aanspreken-op-de-vertraging.png` | aanspreken op | to hold someone to account for | One person stands facing a delivery person who holds an empty open crate upright and shrugs | Chasing up a delay; pair with `zich-verzetten-tegen-de-prijsstijging`. | needed |
| 8 | `zich-verzetten-tegen-de-prijsstijging.png` | zich verzetten tegen | to resist | One person stands with both arms crossed in front of a plain sign-shaped board held up by another | Pushing back at a rise in price; pair with `een-leverancier-aanspreken-op-de-vertraging`. | needed |
| 9 | `benoemen-tot-teamleider.png` | benoemen tot | to appoint as | One person slides a plain armband up the upper arm of a newcomer across a desk, the newcomer's posture upright and… | Single. Giving someone a post; same camera as `zich-aanmelden-bij-de-balie`. | needed |
| 10 | `een-oplossing-aandragen-voor-het-probleem.png` | aandragen voor | to put forward for | One person lifts a plain key and holds it out between two others seated at a table, while both turn towards it | Single. Offering an idea. | needed |
| 11 | `in-aanmerking-komen-voor-een-vergoeding.png` | in aanmerking komen voor | to be eligible for | One person stands in front of a plain list board held up by a clerk and taps one ruled line with a finger, while the… | Qualifying for something; pair with `aanspraak-maken-op-een-vergoeding`. | needed |
| 12 | `aanspraak-maken-op-een-vergoeding.png` | aanspraak maken op | to claim | One person holds a blank form out towards a clerk with both hands and a flat, set mouth | Demanding what one is owed; pair with `in-aanmerking-komen-voor-een-vergoeding`. | needed |
| 13 | `beschikken-over-voldoende-middelen.png` | beschikken over voldoende middelen | to have sufficient means | One person holds open a plain tin box showing a small stack of plain discs, tipping it towards a second figure who… | Single. Office. Discs only; no banknotes or currency marks. | needed |
| 14 | `rekening-houden-met-de-markt.png` | rekening houden met de markt | to take the market into account | One person stands at a plain stall with three plain objects on it and looks towards an empty space where a second… | Single. Office and street. | needed |
| 15 | `een-overzicht-geven-van-de-uitgaven.png` | een overzicht geven van | to give an overview of | One person holds up a large sheet divided into three plain columns by ruled lines and points with one finger at the… | Single. Office. Columns only; no numbers. | needed |
| 16 | `afspraken-maken-over-de-levertijd.png` | afspraken maken over | to make arrangements about | Two people stand on either side of a plain crate, one hand each on it, with a wall clock shape with tick marks… | Agreeing on when; pair with `afspraken-maken-over-de-kosten`. | needed |
| 17 | `afspraken-maken-over-de-kosten.png` | afspraken maken over | to make arrangements about | The same two people with one hand each flat on a plain receipt on the crate top | Agreeing on what it costs; pair with `afspraken-maken-over-de-levertijd`. | needed |
| 18 | `de-basis-leggen-voor-een-nieuwe-afdeling.png` | de basis leggen voor | to lay the foundation for | One person places the first of a row of plain empty desks with both hands, while two other figures carry in a second… | Starting something new; same camera as `afstappen-van-het-oude-plan`; pair with `afscheid-nemen-van-de-afdeling`. | needed |
| 19 | `afscheid-nemen-van-de-afdeling.png` | afscheid nemen van | to say goodbye to | One person folds down the legs of a plain desk and carries it towards a doorway, while the room behind is empty… | Closing something down; pair with `de-basis-leggen-voor-een-nieuwe-afdeling`. | needed |
| 20 | `een-prognose-opstellen-voor-het-jaar.png` | een prognose opstellen voor | to draw up a forecast for | One person sits with a ruled sheet in front of them and a single rising stroke drawn across it, pen poised at the… | Single. Office. One rising stroke only; no grid of numbers. | needed |
| 21 | `een-contract-ondertekenen-met-een-klant.png` | een contract ondertekenen met | to sign a contract with | Two people sit at a table and each holds a pen over the same blank sheet, one from each side | An agreement made together; pair with `een-akkoord-bekrachtigen-met-een-stempel`. | needed |
| 22 | `een-akkoord-bekrachtigen-met-een-stempel.png` | bekrachtigen met | to confirm with | One person presses a plain square block down onto a blank sheet with both hands | Office. The block is plain with no carved shape visible; pair with `een-contract-ondertekenen-met-een-klant`. | needed |
| 23 | `de-jaarrekening-deponeren-bij-de-kamer.png` | deponeren bij | to file with | One person slides a thick sealed envelope into a slot in a plain wall panel beneath a small blank plaque shape | Handing records to an office; pair with `de-jaarrekening-controleren-voor-het-bestuur`. | needed |
| 24 | `de-jaarrekening-controleren-voor-het-bestuur.png` | controleren voor | to check for | One person sits with a thick plain book open on the desk and a straight rule laid across one column, a colleague… | Checking the books; pair with `de-jaarrekening-deponeren-bij-de-kamer`. | needed |
| 25 | `een-vergunning-aanvragen-bij-de-gemeente.png` | aanvragen bij | to apply to | One person stands at a counter with a blank form and a pen, holding the form out towards a clerk who reaches for it | Asking an authority for permission; pair with `in-behandeling-nemen-van-de-aanvraag`. | needed |
| 26 | `in-behandeling-nemen-van-de-aanvraag.png` | in behandeling nemen | to process | One seated clerk places the same blank form in a shallow tray marked only by a plain raised ridge | Starting to work through paperwork; pair with `een-vergunning-aanvragen-bij-de-gemeente`. | needed |
| 27 | `de-betaling-verrichten-binnen-de-termijn.png` | verrichten binnen | to carry out within | One person stands at a plain counter and lays a small disc-shaped token into a slot, one hand still holding the… | Paying before the deadline; pair with `in-gebreke-blijven-bij-de-levering`. | needed |
| 28 | `in-gebreke-blijven-bij-de-levering.png` | in gebreke blijven bij | to fail to deliver | One person stands beside a large plain crate that is still closed, both arms folded, facing a customer who points at… | Promising and not coming through; pair with `de-betaling-verrichten-binnen-de-termijn`. | needed |
| 29 | `de-administratie-bijhouden-voor-de-accountant.png` | bijhouden voor | to keep for | One person sits with a ruled page in a binder and a pen making a short mark beside an existing line | Single. Keeping records tidy. | needed |
| 30 | `een-offerte-uitbrengen-aan-een-klant.png` | een offerte uitbrengen aan | to send a quotation to | One person folds a blank sheet into an envelope and holds it out towards a customer across a counter, one hand open… | Single. Offering work at a price; same camera as `een-factuur-versturen-naar-de-klant`. | needed |
| 31 | `een-bijdrage-leveren-aan-het-debat.png` | een bijdrage leveren aan | to contribute to | One person stands at a small lectern with one hand raised open and the other flat on the lectern top | Adding your voice to a discussion; pair with `in-het-debat-gaan-over-het-thema`. | needed |
| 32 | `in-het-debat-gaan-over-het-thema.png` | in het debat gaan over | to engage in debate about | Two people sit facing each other at a small table, each with one hand raised and open towards the other | Arguing the case; pair with `een-bijdrage-leveren-aan-het-debat`. | needed |
| 33 | `een-onderzoek-verrichten-naar-de-oorzaken.png` | een onderzoek verrichten naar | to carry out research into | One person leans over a bench with a small plain object under a round lens on a stand, one hand steadying the lens arm | Looking closely for a cause; pair with `onderzoek-doen-naar-het-effect`. | needed |
| 34 | `een-hypothese-opstellen-over-het-gedrag.png` | een hypothese opstellen over | to formulate a hypothesis about | One person sits at a desk with a sheet bearing a single small square at the top and a long line below it, pen at the… | Single. Framing an explanation. | needed |
| 35 | `zich-beroepen-op-een-onderzoek.png` | zich beroepen op | to invoke, to refer to | One person stands with a thick plain book held open in one hand and the other hand raised flat, facing two listeners | Single. Citing an authority. | needed |
| 36 | `een-conclusie-trekken-uit-de-resultaten.png` | een conclusie trekken uit | to draw a conclusion from | One person stands at a wall panel with three plain bars and pulls one flat hand away from the tallest bar, then… | Single. Academic. Bars only; no numerals. | needed |
| 37 | `een-standpunt-innemen-ten-opzichte-van-het-voorstel.png` | standpunt innemen ten opzichte van | to take a position on | One person steps forward from a standing row and plants both feet apart, one hand flat in front of the chest, facing… | Single. Making one's position clear. | needed |
| 38 | `kritiek-uiten-op-het-model.png` | kritiek uiten op | to criticise | One person stands beside a plain model of a frame with one hand lifted open and the other pointing flat at a loose joint | Single. Pointing out a flaw. | needed |
| 39 | `onderzoek-doen-naar-het-effect.png` | onderzoek doen naar | to conduct research into | Two people stand on either side of a long bench measuring the same plain object with two straight rules, one at each… | Measuring an effect; same camera as `een-voorstel-bespreken-met-de-opleiding`; pair with `een-onderzoek-verrichten-naar-de-oorzaken`. | needed |
| 40 | `een-artikel-publiceren-in-een-vakblad.png` | publiceren in | to publish in | One person holds a plain open booklet upright in both hands, showing it towards three seated figures at a long table | Single. Academic. The booklet is blank with plain ruled blocks. | needed |
| 41 | `een-methode-toepassen-op-de-vraag.png` | een methode toepassen op | to apply a method to | One person places a small plain frame over a sheet of paper on a table, aligning its edges with the sheet's corner | Bringing a procedure to a case; pair with `een-theorie-verbinden-met-de-praktijk`. | needed |
| 42 | `een-theorie-verbinden-met-de-praktijk.png` | een theorie verbinden met | to connect with | One person holds a plain closed book in one hand and lays a flat tool on it with the other, both objects touching | Joining study and work; pair with `een-methode-toepassen-op-de-vraag`. | needed |
| 43 | `een-bewering-onderbouwen-met-cijfers.png` | een bewering onderbouwen met | to support with | One person stands beside a wall panel with three plain bars and rests one hand flat under the tallest bar, facing a… | Single. Backing a claim with evidence. | needed |
| 44 | `zich-uitspreken-tegen-het-voorstel.png` | zich uitspreken tegen | to speak out against | One person stands with one arm flat and low across the body, palm down, towards two seated figures who lean back | Registering disagreement; pair with `een-beroep-doen-op-de-medewerkers`. | needed |
| 45 | `een-analyse-maken-van-de-gegevens.png` | een analyse maken van | to analyse | One person sits with a large sheet of ruled rows in front of them and a pen circling an area with a quick curved stroke | Single. Academic. Ruled rows only; no numbers. | needed |
| 46 | `in-tegenspraak-zijn-met-de-bevindingen.png` | in tegenspraak zijn met | to contradict | Two people stand on either side of two plain blocks placed at different heights and point at each other's block with… | Single. Two results that do not match. | needed |
| 47 | `de-aandacht-vestigen-op-het-probleem.png` | de aandacht vestigen op | to draw attention to | One person stands and holds a small plain lamp up above head height, towards a wall panel with a single crack, while… | Single. Academic. The lamp is a plain shape, no beams. | needed |
| 48 | `een-beroep-doen-op-de-medewerkers.png` | een beroep doen op | to call upon | One person stands with both hands open and raised towards a row of three seated figures, the gesture asking rather… | Asking others to help; pair with `zich-uitspreken-tegen-het-voorstel`. | needed |
| 49 | `een-voorstel-bespreken-met-de-opleiding.png` | een voorstel bespreken met | to discuss with | Two people sit across the corner of a table with a blank sheet between them and one hand near each corner of it | Single. Talking something through; same camera as `onderzoek-doen-naar-het-effect`. | needed |
| 50 | `een-resultaat-behalen-met-een-groep.png` | een resultaat behalen met | to achieve with | One person puts both hands on top of a plain finished object at the end of a bench while two others stand behind… | Single. A shared outcome. | needed |
| 51 | `stelling-nemen-tegen-het-voorstel.png` | stelling nemen tegen | to take a stand against | One person stands with one foot forward and both palms flat against a plain board propped upright on a stand, facing a… | Single. Declaring a position. | needed |
| 52 | `zich-verdiepen-in-de-literatuur.png` | zich verdiepen in de literatuur | to read up on the literature | One person sits at a desk surrounded on both sides by small stacks of plain closed books, one open on the desk in… | Single. Reading widely; same camera as `zich-verdiepen-in-boek`. | needed |
| 53 | `een-document-aanhalen-in-de-tekst.png` | aanhalen in | to quote in | One person points with one finger at a short ruled strip on a page while the other hand holds a second page beside… | Single. Academic. Strips are ruled, not written. | needed |
| 54 | `een-verwijzing-opnemen-in-de-inleiding.png` | een verwijzing opnemen in | to include a reference in | One person places a small blank card between two pages of an open thick book and closes it with both hands | Single. Academic. The card is a plain rectangle. | needed |
| 55 | `een-argument-weerleggen-met-bewijs.png` | weerleggen met | to refute with | One person lays a plain ruled sheet on the table beside a small stack of blocks built by a second figure and pushes it… | Single. Academic. The sheet pushed in beside the stack is the idea. | needed |
| 56 | `een-standpunt-verdedigen-tegen-kritiek.png` | verdedigen tegen | to defend against | One person stands with a large plain panel held upright in both hands in front of them, facing two figures who press… | Single. Academic. The panel is held, not leaning on anything; same camera as `zich-beroepen-op-het-verdrag` and `zich-verweren-tegen-de-eis`. | needed |
| 57 | `een-definitie-geven-van-het-begrip.png` | een definitie geven van | to define | One person holds a small plain frame around a single object on a table, so that only that object sits inside the frame | Single. Academic. The frame is the same square as earlier, here laid flat around an object. | needed |
| 58 | `een-vergelijking-maken-tussen-twee-groepen.png` | een vergelijking maken tussen | to compare | One person stands with one hand over each of two small plain groups of blocks, the left group taller, and looks from… | Single. Academic. Two groups only; keep the blocks identical in shape. | needed |
| 59 | `een-these-verdedigen-voor-de-commissie.png` | verdedigen voor | to defend before | One person stands facing three seated figures behind a long table, a thick plain folder held against the chest with… | Single. Presenting a case to a panel. | needed |
| 60 | `een-beoordeling-krijgen-van-de-begeleider.png` | een beoordeling krijgen van | to be assessed by | One seated figure hands a blank sheet to a standing figure who takes it with both hands | Single. Receiving a verdict on one's work; same camera as `beoordelen-op-de-inhoud`. | needed |
| 61 | `een-patient-onderzoeken-op-klachten.png` | onderzoeken op | to examine for | One person sits on the edge of a plain bench with an arm held out while another figure holds a small round lens… | Checking for a complaint; pair with `een-patient-doorverwijzen-naar-de-specialist`. | needed |
| 62 | `een-patient-doorverwijzen-naar-de-specialist.png` | doorverwijzen naar | to refer to | One person sits at a desk and holds a blank sheet out towards a patient who has half risen from a chair, one hand… | Sending someone further; pair with `een-patient-onderzoeken-op-klachten`, `een-verwijzing-krijgen-naar-de-radioloog`. | needed |
| 63 | `een-behandeling-ondergaan-voor-de-knie.png` | een behandeling ondergaan voor | to undergo treatment for | One person sits with one leg straight out on a small stool and both hands resting on the thigh | Single. Receiving care for a part of the body; same camera as `een-behandeling-toepassen-op-de-wond`. | needed |
| 64 | `een-klacht-aanmelden-bij-de-huisarts.png` | aanmelden bij | to register with | One person stands at a counter and hands a blank card to a seated clerk who has a plain register open in front of them | Single. Clinic and counter archetypes. | needed |
| 65 | `een-medicijn-voorschrijven-tegen-de-pijn.png` | voorschrijven tegen | to prescribe for | One person stands at a counter with a small plain bottle in one hand and a blank slip in the other, held out towards… | Single. Clinic. The bottle is plain with no label. | needed |
| 66 | `zich-herstellen-van-een-operatie.png` | zich herstellen van | to recover from | One person sits up in a bed with the blanket to the waist and a plain folded sheet of paper in one hand | Single. Getting well again; same camera as `zich-herstellen-van-ziekte`. | needed |
| 67 | `lijden-aan-een-chronische-aandoening.png` | lijden aan | to suffer from | One person walks slowly with one hand on a plain low rail beside a wall, body bent slightly forward, one step at a time | Single. A long-lasting complaint. | needed |
| 68 | `een-afspraak-maken-met-de-tandarts.png` | een afspraak maken met | to make an appointment with | One person stands at a counter with a plain telephone receiver in one hand and a small blank card in the other, held… | Single. Fixing a visit; same camera as `een-zitting-bepalen-op-een-latere-datum`. | needed |
| 69 | `een-verwijzing-krijgen-naar-de-radioloog.png` | een verwijzing krijgen naar | to get a referral to | One person holds a sealed blank envelope out to a patient while pointing with the other hand towards an open doorway… | Being sent to another room; pair with `een-patient-doorverwijzen-naar-de-specialist`. | needed |
| 70 | `een-uitleg-geven-over-de-behandeling.png` | een uitleg geven over | to give an explanation of | One person stands at a bench and turns a plain model of a joint shape in both hands towards a seated patient who… | Single. Clinic. The model is a simple rounded shape. | needed |
| 71 | `een-defect-melden-bij-de-technische-dienst.png` | melden bij | to report to | One person holds a plain telephone receiver to the ear with one hand and taps a stalled machine beside them with the… | Calling about a fault; pair with `een-onderdeel-vervangen-door-een-nieuw`. | needed |
| 72 | `een-onderdeel-vervangen-door-een-nieuw.png` | vervangen door | to replace with | One person lifts a plain worn part out of a machine and sets a new part of the same shape beside the empty socket | Swapping a broken piece; pair with `een-defect-melden-bij-de-technische-dienst`. | needed |
| 73 | `te-wijten-zijn-aan-een-storing.png` | te wijten zijn aan | to be due to | One person stands beside a machine with a loose belt, one hand open towards it and the other at the chin, talking to… | Single. What looks like one thing; same camera as `denken-over-een-voorstel`. | needed |
| 74 | `een-systeem-koppelen-aan-het-netwerk.png` | koppelen aan | to connect to | One person holds one end of a plain cable up to a socket on a panel and pushes it in with the other hand steadying… | Single. Plugging one thing into another. | needed |
| 75 | `een-installatie-afstellen-op-de-ruimte.png` | afstellen op | to adjust to | One person turns a small dial on a wall panel and steps back to look, then turns it back a little | Tuning for the place; pair with `een-installatie-uitschakelen-tijdens-onderhoud`. | needed |
| 76 | `een-installatie-uitschakelen-tijdens-onderhoud.png` | uitschakelen tijdens | to switch off during | One person kneels by a wall switch with one hand on the lever, pushing it down, while a second figure holds a plain… | Cutting power to work safely; pair with `een-installatie-afstellen-op-de-ruimte`, `een-installatie-weer-inschakelen-na-onderhoud`. | needed |
| 77 | `een-installatie-weer-inschakelen-na-onderhoud.png` | weer inschakelen na | to switch back on after | The same switch and panel, now closed, with one hand lifting the lever up and the second figure lowering the lamp | Power restored; pair with `een-installatie-uitschakelen-tijdens-onderhoud`, `een-storing-verhelpen-door-het-onderdeel-te-vervangen`. | needed |
| 78 | `een-storing-verhelpen-door-het-onderdeel-te-vervangen.png` | verhelpen door | to remedy by | One person holds the same new part in its socket and presses it home with both thumbs, the machine now standing in… | The fix is in place; pair with `een-installatie-weer-inschakelen-na-onderhoud`. | needed |
| 79 | `een-meting-uitvoeren-met-een-meter.png` | een meting uitvoeren met | to take a reading with | One person holds two short probes against two points on a panel while a plain round dial in the other hand shows its… | Single. Technical. The dial is a plain circle with a pointer; same camera as `een-meting-verrichten-aan-het-toestel`. | needed |
| 80 | `een-technische-fout-opslaan-in-het-logboek.png` | opslaan in | to record in | One person writes with one hand on a ruled log sheet clipped to a board while the other hand holds the board steady… | Single. Technical. Ruled lines only; the board leans on the machine. | needed |
| 81 | `een-diagnose-stellen-op-basis-van-de-klachten.png` | een diagnose stellen op basis van | to base a diagnosis on | One person sits at a desk with a blank sheet in front of them and taps two ruled marks on it with the back of a pen,… | A conclusion drawn from symptoms; pair with `controle-houden-op-de-wond`. | needed |
| 82 | `controle-houden-op-de-wond.png` | controle houden op | to keep a check on | One person sits on a bench with one sleeve pushed up and a plain band wound round the forearm; a second figure leans in with both hands on the band, eyes on it | Watching an injury closely; pair with `een-diagnose-stellen-op-basis-van-de-klachten`. | needed |
| 83 | `een-toestel-onderhouden-volgens-de-handleiding.png` | onderhouden volgens | to maintain according to | One person holds a plain closed booklet in one hand and a small tool in the other, standing before an open machine… | Single. Technical. The booklet is closed and plain. | needed |
| 84 | `een-meting-verrichten-aan-het-toestel.png` | een meting verrichten aan | to take a reading from | One person presses a flat sensor against the side of a plain machine and holds it there with both hands, watching a… | Single. Reading what the machine gives; same camera as `een-meting-uitvoeren-met-een-meter`. | needed |
| 85 | `een-storing-voorkomen-door-regelmatig-onderhoud.png` | voorkomen door | to prevent by | One person closes an already clean machine panel and wipes the outside with a plain cloth in the other hand | Single. Stopping trouble before it starts. | needed |
| 86 | `een-behandeling-toepassen-op-de-wond.png` | toepassen op | to apply to | One person sits with one forearm held out and another figure lays a plain folded bandage across it, pressing it down… | Single. Putting something on an injury; same camera as `een-behandeling-ondergaan-voor-de-knie`. | needed |
| 87 | `een-patient-informeren-over-de-risicos.png` | informeren over | to inform about | One person sits facing a standing figure in a plain coat who holds a blank sheet out and points at one place on it… | Warning before consent; pair with `een-patient-voorbereiden-op-de-ingreep`. | needed |
| 88 | `een-patient-voorbereiden-op-de-ingreep.png` | voorbereiden op | to prepare for | One person sits on a bench with a plain gown folded on the knees and both hands smoothing it, looking at a closed door | Getting ready for treatment; pair with `een-patient-informeren-over-de-risicos`. | needed |
| 89 | `een-onderzoek-uitvoeren-bij-de-patient.png` | uitvoeren bij | to carry out on | One person sits with one arm on a small table while another figure looks through a round lens held to their eye… | Single. Examining a person directly. | needed |
| 90 | `een-toestel-aansluiten-op-het-stroomnet.png` | aansluiten op | to connect to | One person pushes a plain plug into a wall socket with one hand and holds the cable steady with the other | Single. Giving power to a machine. | needed |
| 91 | `in-beroep-gaan-tegen-de-uitspraak.png` | in beroep gaan tegen | to appeal against | One person stands at a counter with a blank sheet in one hand and the other hand flat on the counter, facing a… | Challenging a decision; pair with `een-beroep-behandelen-bij-de-rechter`. | needed |
| 92 | `een-beroep-behandelen-bij-de-rechter.png` | behandelen bij | to hear, to deal with | One person sits behind a raised bench and holds the same blank sheet up to read it | A case looked at properly; pair with `in-beroep-gaan-tegen-de-uitspraak`. | needed |
| 93 | `een-verdachte-beschuldigen-van-diefstal.png` | beschuldigen van | to accuse of | One person stands opposite another and points a flat hand at a plain bag lying open on a table between them | Single. Naming the offence. | needed |
| 94 | `een-getuige-ondervragen-over-de-gebeurtenissen.png` | ondervragen over | to question about | Two people stand facing each other, the questioner leaning in with one hand open, the witness upright with both… | Single. Asking what was seen. | needed |
| 95 | `in-aanmerking-nemen-als-bewijs.png` | in aanmerking nemen als | to take into account as | One person lifts a plain object from a table with both hands and turns it towards a second figure who has a notebook… | Single. Something accepted as proof. | needed |
| 96 | `een-vonnis-uitspreken-over-de-zaak.png` | een vonnis uitspreken over | to pronounce a verdict on | One person at a raised bench lays one hand flat on a closed book and speaks towards the two figures below | Single. The decision is given; same camera as `een-uitspraak-motiveren-met-argumenten`. | needed |
| 97 | `een-zaak-doorverwijzen-naar-een-hogere-instantie.png` | doorverwijzen naar | to refer to | One person at a desk sets the blank sheet into an envelope and holds it out towards a second clerk who stands by a… | Passing a case upward; pair with `een-maatregel-nemen-tegen-de-overtreder`. | needed |
| 98 | `zich-beroepen-op-het-verdrag.png` | zich beroepen op | to invoke | One person stands with a thick plain book open in one hand and the other hand lifted flat, facing a raised bench | Single. Citing the source of a right; same camera as `een-standpunt-verdedigen-tegen-kritiek` and `zich-beroepen-op-de-afspraak`. | needed |
| 99 | `een-maatregel-nemen-tegen-de-overtreder.png` | nemen tegen | to take against | One person stands before a closed door and places a plain narrow band of paper across the join between door and… | Legal. The band is plain with no lettering; pair with `een-dossier-overdragen-aan-de-opvolger`, `een-zaak-doorverwijzen-naar-een-hogere-instantie`. | needed |
| 100 | `een-dossier-overdragen-aan-de-opvolger.png` | overdragen aan | to hand over to | One person places a thick plain folder into the hands of a second, who is already turning towards a desk | The file changes hands; pair with `een-maatregel-nemen-tegen-de-overtreder`. | needed |
| 101 | `een-overeenkomst-sluiten-met-de-eigenaar.png` | een overeenkomst sluiten met | to conclude with | Two people sit at a table and each lays one hand flat on a blank sheet between them | Agreeing on terms; pair with `een-contract-ondertekenen-ten-overstaan-van-een-getuige`. | needed |
| 102 | `een-contract-ondertekenen-ten-overstaan-van-een-getuige.png` | ondertekenen ten overstaan van | to sign in the presence of | One person signs a blank sheet with a pen while a second stands opposite with both hands clasped in front, watching | Signing before a witness; pair with `een-overeenkomst-sluiten-met-de-eigenaar`. | needed |
| 103 | `een-geschil-beslechten-buiten-de-rechter-om.png` | buiten de rechter om | without going to court | Two people sit facing each other at a table and one pushes a plain sheet across to the other, who places a hand on it | Settling apart from the law; pair with `een-claim-afwijzen-op-grond-van-gebrek-aan-bewijs`. | needed |
| 104 | `een-claim-afwijzen-op-grond-van-gebrek-aan-bewijs.png` | afwijzen op grond van | to reject on the grounds of | One person holds a blank sheet in both hands and turns it over, showing the back is empty, towards a second figure | The claim fails for want of evidence; pair with `een-geschil-beslechten-buiten-de-rechter-om`. | needed |
| 105 | `een-eis-indienen-tegen-de-verhuurder.png` | indienen tegen | to file against | One person slides a blank form into a slot in a wall panel while a second figure stands behind with a set face and… | Bringing a formal complaint; pair with `zich-verweren-tegen-de-eis`. | needed |
| 106 | `zich-verweren-tegen-de-eis.png` | zich verweren tegen | to defend against | One person stands with a plain panel held in both hands in front of them, facing another who holds a blank form up | Answering a complaint; same camera as `een-standpunt-verdedigen-tegen-kritiek`; pair with `een-eis-indienen-tegen-de-verhuurder`. | needed |
| 107 | `een-document-vervalsen-om-voordeel-te-behalen.png` | vervalsen om | to falsify in order to | One person holds a blank sheet in one hand and a small plain block in the other, up to the sheet, glancing towards a… | Changing a paper for gain; pair with `een-bekentenis-afleggen-tegenover-de-rechter`. | needed |
| 108 | `een-bekentenis-afleggen-tegenover-de-rechter.png` | tegenover de rechter | before the judge | One person stands before a raised bench with head slightly bowed and both hands open at the sides | Saying it was me; pair with `een-document-vervalsen-om-voordeel-te-behalen`. | needed |
| 109 | `een-zaak-overdragen-van-de-onderzoeker-aan-de-officier.png` | overdragen van … aan | to transfer from … to | One person hands a thick plain folder to another, who takes it with both hands | The case moves up; pair with `een-vonnis-uitvoeren-volgens-de-wet`. | needed |
| 110 | `een-vonnis-uitvoeren-volgens-de-wet.png` | uitvoeren volgens | to carry out according to | One person places a plain band of paper across a closed door while holding an open thick book in the other hand | The decision is acted on; pair with `een-zaak-overdragen-van-de-onderzoeker-aan-de-officier`. | needed |
| 111 | `een-dagvaarding-bezorgen-aan-de-gedaagde.png` | bezorgen aan | to serve on | One person holds a sealed blank envelope out at arm's length towards a second figure who has just opened a door | An official notice arrives; pair with `een-getuige-ophouden-aan-de-uitgang`. | needed |
| 112 | `een-zitting-bepalen-op-een-latere-datum.png` | bepalen op | to set for | One person sits at a desk with a plain calendar sheet of boxes and taps one box with a finger, pen in the other hand | Legal. Boxes only; no numerals; same camera as `een-afspraak-maken-met-de-tandarts`; pair with `een-beroep-aantekenen-binnen-de-termijn`. | needed |
| 113 | `een-getuige-ophouden-aan-de-uitgang.png` | ophouden aan | to stop at, to hold at | One person stands in an open doorway with a flat hand raised towards a second who has stopped mid-step, one hand on… | Stopping someone passing; pair with `een-dagvaarding-bezorgen-aan-de-gedaagde`. | needed |
| 114 | `een-verklaring-afleggen-onder-ed.png` | afleggen onder ede | to testify under oath | One person stands in a bare room with one hand raised flat beside the head and the other on a thick closed book… | Promising to tell the truth; pair with `een-getuigenverklaring-opnemen-in-het-dossier`. | needed |
| 115 | `afzien-van-vervolging.png` | afzien van | to refrain from | One person closes a plain folder and lays both hands flat on top of it, looking up at a second figure with a single… | The case is set aside; pair with `de-verdachte-vrijspreken-van-alle-schuld`. | needed |
| 116 | `een-overtreding-beboeten-met-een-boete.png` | beboeten met | to fine with | One person holds out a small blank slip towards a second figure who takes it, one hand on a bicycle handlebar | Single. Legal. The slip is a plain rectangle. | needed |
| 117 | `een-beroep-aantekenen-binnen-de-termijn.png` | aantekenen binnen | to lodge within | One person writes on a blank form at a counter and taps the corner of the form with the pen, a wall clock shape with… | Filing before time runs out; same camera as `in-de-loop-der-jaren`; pair with `een-zitting-bepalen-op-een-latere-datum`. | needed |
| 118 | `een-getuigenverklaring-opnemen-in-het-dossier.png` | opnemen in | to include in | One person places a small blank card between the pages of a thick plain folder and closes it with both hands | A statement joins the file; pair with `een-verklaring-afleggen-onder-ed`. | needed |
| 119 | `een-uitspraak-motiveren-met-argumenten.png` | motiveren met | to justify with | One person at a raised bench lays one hand on a closed book and speaks, the other hand open towards the two figures… | Single. Giving the reasons; same camera as `een-vonnis-uitspreken-over-de-zaak`. | needed |
| 120 | `de-verdachte-vrijspreken-van-alle-schuld.png` | vrijspreken van | to acquit of | One person at the bench holds a blank sheet up and turns it over so the empty back faces the two figures below, then… | The case ends without proof; pair with `afzien-van-vervolging`. | needed |
| 121 | `een-bericht-verspreiden-via-sociale-media.png` | verspreiden via | to spread via | One person holds a plain device up in both hands with an open square shape glowing as a small burst of strokes, and… | Single. Newsroom archetype. No letters on the screen, only a plain square. | needed |
| 122 | `zich-richten-tot-de-lezers.png` | zich richten tot | to address | One person sits at a desk with a blank sheet and a pen, facing an empty chair drawn as if there were a reader in it,… | Single. Writing for someone. | needed |
| 123 | `commentaar-leveren-op-het-beleid.png` | commentaar leveren op | to comment on | One person stands with one hand open and lifted, the other flat, turning towards two seated figures at a table with… | Adding an opinion; pair with `een-mening-geven-over-de-plannen`. | needed |
| 124 | `een-mening-geven-over-de-plannen.png` | een mening geven over | to give an opinion on | One person stands beside a plain raised board with one hand open towards it and the head tilted, speaking to nobody… | Judging a plan; pair with `commentaar-leveren-op-het-beleid`. | needed |
| 125 | `in-gesprek-gaan-met-de-bewoners.png` | in gesprek gaan met | to enter into discussion with | One person sits down on a low bench beside a resident who turns towards them, both hands on their knees | Single. Newsroom and street. | needed |
| 126 | `zich-beroepen-op-bronnen.png` | zich beroepen op | to cite sources | One person holds a thick plain notebook open in one hand and points with the other hand at one line in it | Backing a story up; pair with `een-onderwerp-aankaarten-bij-het-publiek`. | needed |
| 127 | `een-onderwerp-aankaarten-bij-het-publiek.png` | aankaarten bij | to raise with | One person stands at the head of a small group with one hand raised open, and the group turns towards them from… | Bringing something out into the open; pair with `zich-beroepen-op-bronnen`. | needed |
| 128 | `een-uitspraak-in-twijfel-trekken.png` | in twijfel trekken | to call into question | One person tilts their head and raises one flat hand towards a blank sheet held by another, palm outwards in a stop | Refusing to take it at face value; pair with `ingaan-op-de-kritiek-van-de-lezers`. | needed |
| 129 | `een-bericht-plaatsen-op-de-voorpagina.png` | plaatsen op | to place on | One person lays a large blank page flat on a long table with both hands, aligning its corners with the table's edge | Single. Newsroom. The page is blank with one large ruled block; same camera as `op-de-hoogte-houden-van-het-nieuws`. | needed |
| 130 | `ingaan-op-de-kritiek-van-de-lezers.png` | ingaan op | to respond to | One person reads a folded blank sheet over the counter and nods, one hand open towards the figure who handed it over | Answering the complaints; pair with `een-uitspraak-in-twijfel-trekken`. | needed |
| 131 | `een-standpunt-in-nemen-in-een-column.png` | standpunt innemen in | to take a position in | One person sits at a desk with a ruled sheet in front of them and a pen held upright at its top, head turned towards… | Committing to an opinion in writing; pair with `een-debat-voeren-over-het-beleid`. | needed |
| 132 | `een-debat-voeren-over-het-beleid.png` | een debat voeren over | to debate | Two people sit facing each other with one raised hand each, a small table between them holding two blank sheets | Two sides arguing; pair with `een-standpunt-in-nemen-in-een-column`. | needed |
| 133 | `een-onderzoek-aanhalen-in-een-artikel.png` | aanhalen in | to cite in | One person holds a plain closed booklet in one hand and points to a sheet on the desk with the other, a matching… | Single. Backing a piece with research. | needed |
| 134 | `een-reactie-vragen-op-het-nieuws.png` | een reactie vragen op | to ask for a response to | One person holds out a small plain device towards a second figure who turns away with one hand raised flat, head down | Single. Asking for a comment. | needed |
| 135 | `ruimte-geven-aan-een-mening.png` | ruimte geven aan | to give space to | One person steps back with both hands open towards a second figure who speaks with one hand raised, while a third… | Single. Making room for someone else's view. | needed |
| 136 | `nadenken-over-de-gevolgen.png` | nadenken over | to think about | One person sits alone with both elbows on a table and the forehead resting on the hands, a single blank sheet pushed… | Single. Reflect on what will follow. | needed |
| 137 | `een-verwijt-maken-aan-de-overheid.png` | een verwijt maken aan | to reproach | One person stands with one hand pointing flat towards a plain tall building shape, speaking over the shoulder to a… | Laying blame at the top; pair with `zich-verdedigen-tegen-de-beschuldiging`. | needed |
| 138 | `zich-verdedigen-tegen-de-beschuldiging.png` | zich verdedigen tegen | to defend oneself against | One person stands behind a plain panel held upright with both hands, facing a second figure who points flat at them | Answering a charge in public; pair with `een-verwijt-maken-aan-de-overheid`. | needed |
| 139 | `in-tegenspraak-gaan-met-de-cijfers.png` | in tegenspraak gaan met | to contradict | One person holds up a blank sheet in one hand and a plain block in the other and brings them together, shaking the head | Facts that do not fit; pair with `een-pleidooi-houden-voor-verandering`. | needed |
| 140 | `een-pleidooi-houden-voor-verandering.png` | een pleidooi houden voor | to plead for | One person stands with both hands open and raised, turned towards a seated group, the body leaning forward | Making the case for change; pair with `in-tegenspraak-gaan-met-de-cijfers`. | needed |
| 141 | `op-de-valreep-liggen.png` | op de valreep | at the last moment | One person runs towards a doorway with a bag bouncing behind and one arm outstretched towards the door's edge | Everyday archetype. No arrows; the outstretched arm does it; pair with `trappen-in-een-val`. | needed |
| 142 | `trappen-in-een-val.png` | trappen in | to fall for | One person steps forward with one foot landing flat on a small plain ribbed mat on the floor and arms flung up | Caught by a trick; pair with `op-de-valreep-liggen`. | needed |
| 143 | `voor-de-gek-houden.png` | voor de gek houden | to make a fool of | One person holds out a plainly hollow half-shell of bread towards a second figure who reaches for it with both… | Single. A joke at someone's expense; same camera as `de-handen-uit-de-mouwen-steken`. | needed |
| 144 | `de-handen-uit-de-mouwen-steken.png` | de handen uit de mouwen steken | to get stuck in | One person kneels with both sleeves pushed high and both hands inside a box of loose parts, sorting them | Single. Starting real work; same camera as `voor-de-gek-houden`. | needed |
| 145 | `de-kat-uit-de-boom-kijken.png` | de kat uit de boom kijken | to wait and see | One person stands behind an open door and looks around its edge with both hands on the frame, not stepping in | Watching before entering; pair with `de-moer-onder-de-kinderen-geven`. | needed |
| 146 | `de-moer-onder-de-kinderen-geven.png` | de moer onder de kinderen geven | to give the children a good talking-to | One person leans over a kitchen table with a flat hand on it and an open mouth, facing three small figures who look… | Scolding a group; pair with `de-kat-uit-de-boom-kijken`. | needed |
| 147 | `met-vallen-en-opstaan-leren.png` | met vallen en opstaan | by trial and error | One person sits on the floor with a small bicycle lying on its side beside them and rubs one knee, about to rise | Single. Learning the hard way. | needed |
| 148 | `iets-op-de-grote-hoop-gooien.png` | op de grote hoop gooien | to lump together | One person tips a small basket of mixed plain pieces into one big crate with both hands | Single. Losing the differences. | needed |
| 149 | `terugkijken-op-de-gebeurtenis.png` | terugkijken op | to look back on | One person sits on a step with chin on one hand, looking back over the shoulder towards an open door behind them | Single. Reviewing what has already happened. | needed |
| 150 | `iets-op-de-koop-toenemen.png` | op de koop toenemen | to accept as part of the deal | One person carries a plain crate with a small chipped corner visible, shrugging with one shoulder and mouth flat | Single. Taking the rough with the smooth. | needed |
| 151 | `zich-geen-zorgen-maken-over-het-resultaat.png` | zich geen zorgen maken over | not to worry about | One person sits back in a chair with a cup held loosely in one hand and legs crossed, a single relaxed line for a mouth | Easy confidence; pair with `voet-bij-stuk-houden`. | needed |
| 152 | `voet-bij-stuk-houden.png` | voet bij stuk houden | to stand firm | One person stands with both hands on the table and chin forward, facing two seated figures who have pushed their… | Insisting until others give way; pair with `zich-geen-zorgen-maken-over-het-resultaat`. | needed |
| 153 | `ergens-klaar-mee-zijn.png` | ergens klaar mee zijn | to be done with something | One person stands and drops a plain folder into a bin with one hand, brushing the other hand flat against itself as… | Single. Finished and refusing more. | needed |
| 154 | `op-de-tong-liggen.png` | op de tong liggen | to be on the tip of one's tongue | One person stands with one finger raised and eyes narrowed, mouth slightly open, as if about to speak | Single. Almost remembering; same camera as `tevreden-over-het-werk`. | needed |
| 155 | `met-de-noorderzon-vertrekken.png` | met de noorderzon vertrekken | to disappear without a trace | One person walks away through an open door with a plain bag, and the room behind is completely bare apart from an… | Gone without a word; pair with `weer-op-de-proppen-komen`. | needed |
| 156 | `weer-op-de-proppen-komen.png` | weer op de proppen komen | to turn up again | One person steps back in through the same doorway with the same plain bag, one hand raised in a small wave | Reappearing; pair with `met-de-noorderzon-vertrekken`. | needed |
| 157 | `niet-voldoen-aan-de-verwachtingen.png` | niet voldoen aan | to fall short of | One person holds up a small plain plate with a single flat, unremarkable shape on it towards a second figure whose… | Single. Ordinary and unexciting. | needed |
| 158 | `op-de-tocht-zijn.png` | op de tocht zijn | to be ajar, to be drafty | One person stands in a room with a small doorway left open at the edge | Single. Everyday. Strokes only; no movement lines on the person. | needed |
| 159 | `er-met-de-pet-naar-gooien.png` | er met de pet naar gooien | to do a sloppy job | One person paints a plain wall with a roller held only by the fingertips, head turned away | Single. Everyday. The ragged edge is the idea; same camera as `tevreden-over-het-werk`. | needed |
| 160 | `aan-de-bak-zijn.png` | aan de bak zijn | to have one's work cut out | One person stands behind a counter stacked with plain boxes on both sides, both hands already full, looking at one… | Single. Work piles up. | needed |
| 161 | `de-verbeelding-te-boven-gaan.png` | de verbeelding te boven gaan | to be beyond imagining | One person stands with both hands raised open in front of a wide bright gap between two tall plain blocks, head… | More than one can take in; pair with `in-het-vage-blijven`. | needed |
| 162 | `in-het-vage-blijven.png` | in het vage blijven | to remain vague | One person speaks with one hand open and low, the other held across the mouth, while a listener leans forward with a… | Saying nothing clearly; pair with `de-verbeelding-te-boven-gaan`. | needed |
| 163 | `aan-het-licht-brengen.png` | aan het licht brengen | to bring to light | One person holds a small plain lamp up above a table where an open folder lies, both hands steadying the lamp | Single. Making something visible. | needed |
| 164 | `in-duigen-liggen.png` | in duigen liggen | to lie in ruins | One person stands before a low wall of plain blocks with a wide gap through it and two blocks fallen on the ground | Single. Everything fallen apart. | needed |
| 165 | `met-huid-en-haar-overgeleverd.png` | met huid en haar overgeleverd | delivered entirely | One person sits with both feet up on a chair and both hands raised open, close to a large plain box that has its lid… | Single. No way to hide any of it. | needed |
| 166 | `stilstaan-bij-het-verleden.png` | stilstaan bij | to dwell on | One person stands still in front of a plain wall panel with a single old plain photograph hanging on it, both hands… | Single. A moment that does not move; same camera as `werken-tegen-de-klok`. | needed |
| 167 | `in-het-stof-bijten.png` | in het stof bijten | to bite the dust | One person lies on the floor on one elbow, head low, a small plain puff of dust drawn as short arcs at the elbow and… | Single. Literary. Dust arcs only; no cloud texture. | needed |
| 168 | `een-loden-last-met-zich-meedragen.png` | met zich meedragen | to carry with one | One person walks with a large plain sack on the back and both hands on the straps, neck bent | Single. A burden that comes along; same camera as `gebukt-gaan-onder-de-druk`. | needed |
| 169 | `op-de-loer-liggen.png` | op de loer liggen | to lurk | One person crouches behind the edge of a low plain wall with only the top of the head and one hand visible above it | Single. Waiting out of sight. | needed |
| 170 | `opscheppen-over-de-prestatie.png` | opscheppen over | to boast about | One person stands on a plain chair with both arms raised and chest out, while a second figure below stands with… | Single. Showing off in front of others. | needed |
| 171 | `over-de-schreef-gaan.png` | over de schreef gaan | to go too far | One person steps over a painted straight line on a wide floor, one foot across and the other still behind, both… | Going beyond what is allowed; pair with `in-iemands-schaduw-staan`. | needed |
| 172 | `in-iemands-schaduw-staan.png` | in iemands schaduw staan | to be in someone's shadow | One person stands directly behind another and is drawn smaller and half hidden by the first person's outline | Literary. The overlap is the idea; no cast shadows on the ground; pair with `over-de-schreef-gaan`, `in-de-schaduw-van-het-verleden-leven`. | needed |
| 173 | `vastlopen-in-het-gesprek.png` | vastlopen in | to get stuck in | One person speaks with one hand raised, then stops mid-gesture with the hand frozen and a flat mouth | Single. Losing the sense of what was said. | needed |
| 174 | `uiting-geven-aan-de-gevoelens.png` | uiting geven aan | to give expression to | One person stands with both hands pressed flat on the chest and the head tilted back, mouth open in one sustained… | Single. Literary. Keep the two listeners still and the speaker alone in front. | needed |
| 175 | `op-een-keerpunt-staan.png` | op een keerpunt staan | to be at a turning point | One person stands where a wide path splits into two, one fork rising and one falling, both hands at the sides | Single. Literary. No arrows; the two slopes carry the meaning. | needed |
| 176 | `in-de-schaduw-van-het-verleden-leven.png` | in de schaduw van het verleden leven | to live in the shadow of the past | One person sits with an old plain photograph held in both hands, the head lowered, in a room where a large plain… | The past hanging over the present; pair with `in-iemands-schaduw-staan`. | needed |
| 177 | `afgeven-op-een-collega.png` | afgeven op | to badmouth | One person stands with the head tilted towards a second figure and one hand raised flat, speaking with a hard mouth | Single. Literary. No contact; the third figure turning away carries the harm. | needed |
| 178 | `door-het-oog-van-de-naald-kruipen.png` | door het oog van de naald kruipen | to scrape through | One person crawls on both knees through a narrow gap between two plain tall blocks, body squeezed small | Single. Literary. The two blocks are the only objects. | needed |
| 179 | `te-genade-vallen-bij-het-nageslacht.png` | te genade vallen bij | to fall into the mercy of | One person sits on the floor with the head bowed and both palms turned up on the knees, in front of a raised plain… | Single. Literary. The empty bench is the mass. | needed |
| 180 | `afstappen-van-het-oude-plan.png` | afstappen van | to abandon | One person turns a large plain wheel with both hands, then steps away from it towards an open doorway; a plain floor… | Single. Literary. The wheel is the mass; no ship detail; same camera as `de-basis-leggen-voor-een-nieuwe-afdeling`. | needed |
| 181 | `behalve-de-uitzondering.png` | behalve | except | One person pushes a row of five plain blocks across a table and lifts one block out of the line, setting it apart at… | One thing left out; pair with `behalve-als-het-regent`, `met-inbegrip-van-de-toeslag`. | needed |
| 182 | `met-inbegrip-van-de-toeslag.png` | met inbegrip van | including | One person places one more plain block onto the same row so that six blocks sit evenly together, hands still on the… | One thing counted in; pair with `behalve-de-uitzondering`. | needed |
| 183 | `sinds-de-aanvang-van-het-project.png` | sinds | since | One person draws a plain ruled line across a sheet with a small upright stroke at its start, pen resting at the… | Single. Consolidation. A stroke at one end of a line only. | needed |
| 184 | `tijdens-de-vakantie.png` | tijdens | during | One person sits on a plain chair with a folded coat over the knees and an open suitcase beside them, both hands relaxed | Single. While something else is happening. | needed |
| 185 | `volgens-de-afspraak.png` | volgens | according to | One person holds a blank sheet in one hand and lays the other flat beside a plain block on a table, aligning the… | Single. Going by what was agreed; same camera as `in-afwijking-van-de-regel`. | needed |
| 186 | `wegens-de-weersomstandigheden.png` | wegens | because of | One person holds a folded plain tarp in both hands and looks up at three small cloud shapes, a second figure already… | Single. An official reason for doing something. | needed |
| 187 | `ondanks-de-tegenslag-doorgaan.png` | ondanks | despite | One person steps forward with the body tipped into the stride, past a small plain block fallen on the floor, both… | Single. Going on anyway. | needed |
| 188 | `behalve-als-het-regent.png` | behalve als | unless | One person stands in an open doorway with one foot in and one out, looking back at a small row of cloud shapes on… | An exception to the exception; pair with `behalve-de-uitzondering`, `binnen-de-gestelde-termijn`. | needed |
| 189 | `binnen-de-gestelde-termijn.png` | binnen | within | One person lays a blank form into a shallow tray with one hand while the other rests on a wall clock shape with tick… | Inside the allowed time; pair with `behalve-als-het-regent`, `buiten-de-openingstijden`. | needed |
| 190 | `buiten-de-openingstijden.png` | buiten | outside | One person stands before a closed door with one hand flat on it and the other holding a small plain form, shoulders… | After the place has shut; pair with `binnen-de-gestelde-termijn`. | needed |
| 191 | `zich-richten-op-het-doel-van-de-les.png` | zich richten op | to focus on | One person stands at the front of a plain empty room with both hands raised in a small ring in front of the eye,… | Single. Consolidation. Revisits aiming attention; the room is empty and the post is distant. | needed |
| 192 | `omgaan-met-tegenslag.png` | omgaan met | to deal with | One person sits with elbows on a table and the head lowered onto one hand, while the other hand flattens a crumpled… | Single. Consolidation. Revisits handling; the object is a problem, not a person. | needed |
| 193 | `afhankelijk-zijn-van-goedkeuring.png` | afhankelijk zijn van | to depend on | One person holds a blank form out with both hands towards a seated figure who has a pen lifted over it but has not… | Single. Consolidation. Form in the hand and a pen above it; no signature yet. | needed |
| 194 | `verantwoordelijk-zijn-voor-de-naleving.png` | verantwoordelijk zijn voor | to be responsible for | One person stands at an open doorway with one hand flat on the frame, watching two figures inside work at a table | Single. Consolidation. The doorway is the post; the two inside are drawn small. | needed |
| 195 | `een-beroep-doen-op-het-geduld.png` | een beroep doen op | to call on | One person stands with both hands open and slightly cupped towards a second figure who already has both hands on a… | Single. Consolidation. The asking hands are cupped, not flat. | needed |
| 196 | `zich-beroepen-op-de-afspraak.png` | zich beroepen op | to invoke | One person holds a blank sheet in one hand and taps one corner of it with the other hand, facing a listener who… | Single. Consolidation. The sheet is an agreement, not a book; same camera as `zich-beroepen-op-het-verdrag`. | needed |
| 197 | `beschikken-over-de-benodigde-middelen.png` | beschikken over | to have at one's disposal | One person stands beside a plain bench with three closed plain boxes in a row and turns both open palms down above them | Single. Consolidation. The boxes are closed; the open palms are the offer; same camera as `zich-bezighouden-met-klus`. | needed |
| 198 | `in-aanmerking-komen-voor-kwijtschelding.png` | in aanmerking komen voor | to be eligible for | One person sits at a counter with a blank form in both hands while a clerk leans over with a pen and draws a short… | Single. Consolidation. The clerk's line is the only mark; no letters. | needed |
| 199 | `met-inachtneming-van-de-afspraken.png` | met inachtneming van | subject to, in observance of | One person carries a plain crate towards an open doorway while pressing a single blank sheet against it with one hand | Single. Consolidation. Crate and sheet together; no text on either. | needed |
| 200 | `gebaseerd-zijn-op-de-cijfers.png` | gebaseerd zijn op | to be based on | One person sets a tower of three plain blocks squarely onto a thick stack of blank sheets and steps back, hands open | Single. The tower rests on the stack and the desk is otherwise clear. | needed |
| 201 | `zonder-jas-de-deur-uit.png` | zonder | without | One person strides out through an open doorway with bare arms, a plain coat still hanging on a hook behind | Pair with `het-zonder-de-auto-stellen`; the coat is left behind. | needed |
| 202 | `het-zonder-de-auto-stellen.png` | het zonder … stellen | to do without | One person turns from a parked plain car and wheels a bicycle away, one palm raised towards the car | Pair with `zonder-jas-de-deur-uit`; the car is available but declined. | needed |
| 203 | `vanwege-de-drukte.png` | vanwege | because of | One person stops at a doorway, hand raised, and turns back from a room packed with small figure masses | Pair with `gezien-de-omstandigheden`; the cause is a crowd in plain sight. | needed |
| 204 | `gezien-de-omstandigheden.png` | gezien | in view of | One person stands over a plain crate tipped on its side and lowers one flat hand towards the spill, a second figure waiting | Pair with `vanwege-de-drukte`; calling it off once the state of things is seen. | needed |
| 205 | `richting-de-uitgang.png` | richting | towards | One person walks mid-stride down a bare corridor of two converging lines towards a small open doorway far ahead | Pair with `per-post-versturen`; direction, not arrival. | needed |
| 206 | `per-post-versturen.png` | per | by, by means of | One person slides a blank envelope into the slot of a squat pillar box, the other hand open at the side | Pair with `richting-de-uitgang`; the channel, not the direction. | needed |
| 207 | `aangaande-de-aanvraag.png` | aangaande | concerning | A clerk lifts a plain folder from a drawer at a counter while a visitor holds out a blank form and points to it | Pair with `betreffende-de-wijziging`; a spoken enquiry, no pen in the frame. | needed |
| 208 | `betreffende-de-wijziging.png` | betreffende | regarding | One person at a desk holds a pen above a sheet with one line struck through and a new line beside it | Pair with `aangaande-de-aanvraag`; a written note, one person, a clip. | needed |
| 209 | `jegens-de-klant.png` | jegens | towards a person | One person pulls a plain chair out with one hand, body inclined towards a visitor carrying a plain bag | Single. Courtesy aimed at one person; the host gives, the visitor does not ask. | needed |
| 210 | `overeenkomstig-de-regels.png` | overeenkomstig | in accordance with | One person lays a plain stencil on a board and brushes inside its edge, a matching finished shape beside it | Single. Made to match a given pattern; not a block against a sheet edge. | needed |

## Batch B2-01 — images 1–10

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

1. `een-bod-uitbrengen-op-het-pand.png` — Dutch chunk: een bod uitbrengen op (to make an offer on).
   Scene: One person stands in front of a plain building facade with a blank sheet held out in one hand towards a second figure holding a key.
   Must read: naming a price for a place.
   Avoid: a bank with banknotes; a crowd; a shop.

2. `investeren-in-een-onderneming.png` — Dutch chunk: investeren in (to invest in).
   Scene: One person crouches and places a plain heavy block at the base of a low wall already partly built, both hands steering it into place.
   Must read: putting money into something that will grow.
   Avoid: a bank with coins; a crowd; a shop.

3. `onderhandelen-over-het-tarief.png` — Dutch chunk: onderhandelen over (to negotiate about).
   Scene: Two people sit at a table with a plain object between them and both hands open above it, neither touching it.
   Must read: haggling over a number.
   Avoid: a shop till with digits; a crowd; a handshake.

4. `overeenstemming-bereiken-over-de-levering.png` — Dutch chunk: overeenstemming bereiken over (to come to an agreement about).
   Scene: The same two people with one hand each flat on the same sheet, the object now pushed to one side.
   Must read: settling on a deal.
   Avoid: a crowd; a bank; a shop.

5. `sturen-op-omzetdoelen.png` — Dutch chunk: sturen op (to steer towards).
   Scene: One person stands at a wall panel with three plain bars of increasing height, one flat hand held under the tallest bar, while the other hand turns a small plain wheel mounted beside the panel.
   Must read: steering the work towards a number.
   Avoid: a shop with prices; a crowd; a car.

6. `een-terugbetaling-regelen-met-de-bank.png` — Dutch chunk: een terugbetaling regelen met (to arrange a repayment with).
   Scene: One person at a counter hands a blank form to a clerk who points with one finger at a small plain box on the form.
   Must read: setting up a payment plan.
   Avoid: a crowd; a shop; a phone.

7. `een-leverancier-aanspreken-op-de-vertraging.png` — Dutch chunk: aanspreken op (to hold someone to account for).
   Scene: One person stands facing a delivery person who holds an empty open crate upright and shrugs; a plain clock shape with tick marks is on the wall behind.
   Must read: chasing up a delay.
   Avoid: a crowd; a shop; a bank.

8. `zich-verzetten-tegen-de-prijsstijging.png` — Dutch chunk: zich verzetten tegen (to resist).
   Scene: One person stands with both arms crossed in front of a plain sign-shaped board held up by another; the board is blank.
   Must read: pushing back at a rise in price.
   Avoid: a crowd; a bank; a shop.

9. `benoemen-tot-teamleider.png` — Dutch chunk: benoemen tot (to appoint as).
   Scene: One person slides a plain armband up the upper arm of a newcomer across a desk, the newcomer's posture upright and chin lifted; a third figure watches from one step behind.
   Must read: giving someone a post.
   Avoid: a crowd; a shop; a bank.

10. `een-oplossing-aandragen-voor-het-probleem.png` — Dutch chunk: aandragen voor (to put forward for).
   Scene: One person lifts a plain key and holds it out between two others seated at a table, while both turn towards it.
   Must read: offering an idea.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One, two, five and six are singles on money and buildings: an offer at a facade, a block at the base of a wall, bars on a panel, a form with one box. Four different settings within the office and street archetypes.
Three and four are `onderhandelen over` against `overeenstemming bereiken over`: the same table and object, hands open above it, then hands flat on the sheet. Keep the object identical.
Seven and eight are complaints: a delivery person with an empty crate and a clock, then a crossed-arms refusal in front of a blank board. Do not reuse the crate in subject 8.
Nine and ten are handing-over singles: an armband slid onto an arm, and a key held out at a table. Keep the receiver's posture distinguishable: chin lifted for the armband, both seated figures turning towards the key.

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

## Batch B2-02 — images 11–20

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

1. `in-aanmerking-komen-voor-een-vergoeding.png` — Dutch chunk: in aanmerking komen voor (to be eligible for).
   Scene: One person stands in front of a plain list board held up by a clerk and taps one ruled line with a finger, while the clerk holds a form ready.
   Must read: qualifying for something.
   Avoid: a crowd; a bank; a shop.

2. `aanspraak-maken-op-een-vergoeding.png` — Dutch chunk: aanspraak maken op (to claim).
   Scene: One person holds a blank form out towards a clerk with both hands and a flat, set mouth; the clerk has one hand open beneath the form.
   Must read: demanding what one is owed.
   Avoid: a crowd; a shop; a phone.

3. `beschikken-over-voldoende-middelen.png` — Dutch chunk: beschikken over voldoende middelen (to have sufficient means).
   Scene: One person holds open a plain tin box showing a small stack of plain discs, tipping it towards a second figure who leans in.
   Must read: having the wherewithal.
   Avoid: a bank vault; a shop with prices; a crowd.

4. `rekening-houden-met-de-markt.png` — Dutch chunk: rekening houden met de markt (to take the market into account).
   Scene: One person stands at a plain stall with three plain objects on it and looks towards an empty space where a second stall used to be, a hand on the chin.
   Must read: watching what is around you.
   Avoid: a crowd; a shop with prices; a bank.

5. `een-overzicht-geven-van-de-uitgaven.png` — Dutch chunk: een overzicht geven van (to give an overview of).
   Scene: One person holds up a large sheet divided into three plain columns by ruled lines and points with one finger at the first column.
   Must read: showing the breakdown.
   Avoid: a crowd; a bank; a phone.

6. `afspraken-maken-over-de-levertijd.png` — Dutch chunk: afspraken maken over (to make arrangements about).
   Scene: Two people stand on either side of a plain crate, one hand each on it, with a wall clock shape with tick marks behind them.
   Must read: agreeing on when.
   Avoid: a crowd; a shop; a queue.

7. `afspraken-maken-over-de-kosten.png` — Dutch chunk: afspraken maken over (to make arrangements about).
   Scene: The same two people with one hand each flat on a plain receipt on the crate top; the clock is absent.
   Must read: agreeing on what it costs.
   Avoid: a crowd; a bank vault; a shop.

8. `de-basis-leggen-voor-een-nieuwe-afdeling.png` — Dutch chunk: de basis leggen voor (to lay the foundation for).
   Scene: One person places the first of a row of plain empty desks with both hands, while two other figures carry in a second desk; a plain floor line marks where the row will continue.
   Must read: starting something new.
   Avoid: a crowd; a shop; a bank.

9. `afscheid-nemen-van-de-afdeling.png` — Dutch chunk: afscheid nemen van (to say goodbye to).
   Scene: One person folds down the legs of a plain desk and carries it towards a doorway, pausing to raise one hand in farewell towards the empty room behind, where a second folded desk stands.
   Must read: closing something down and taking leave.
   Avoid: a crowd; a shop; a bank.

10. `een-prognose-opstellen-voor-het-jaar.png` — Dutch chunk: een prognose opstellen voor (to draw up a forecast for).
   Scene: One person sits with a ruled sheet in front of them and a single rising stroke drawn across it, pen poised at the end of the stroke.
   Must read: estimating what comes next.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are `in aanmerking komen voor` against `aanspraak maken op`: a finger on a list and a form held out with both hands. Same counter and clerk; the difference is the set mouth and the reaching hands.
Three and four are single frames on means and surroundings: an open tin of discs, and a stall with a gap where another stood.
Six and 7 share the same crate and clock: clock behind for time, receipt on top for cost. Keep the crate identical.
Eight and nine are `de basis leggen voor` against `afscheid nemen van de afdeling`: a desk being placed, and a desk being folded and carried out. Same plain office and same desk shape.
Five and ten are singles on paper: three ruled columns, and one rising stroke. Do not put the stroke on a grid.

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

## Batch B2-03 — images 21–30

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

1. `een-contract-ondertekenen-met-een-klant.png` — Dutch chunk: een contract ondertekenen met (to sign a contract with).
   Scene: Two people sit at a table and each holds a pen over the same blank sheet, one from each side; the sheet lies flat between them.
   Must read: an agreement made together.
   Avoid: a handshake; a crowd; a bank.

2. `een-akkoord-bekrachtigen-met-een-stempel.png` — Dutch chunk: bekrachtigen met (to confirm with).
   Scene: One person presses a plain square block down onto a blank sheet with both hands; a small open ink pad sits beside it.
   Must read: making an agreement official.
   Avoid: a crowd; a bank; a shop.

3. `de-jaarrekening-deponeren-bij-de-kamer.png` — Dutch chunk: deponeren bij (to file with).
   Scene: One person slides a thick sealed envelope into a slot in a plain wall panel beneath a small blank plaque shape.
   Must read: handing records to an office.
   Avoid: a crowd; a queue; a phone.

4. `de-jaarrekening-controleren-voor-het-bestuur.png` — Dutch chunk: controleren voor (to check for).
   Scene: One person sits with a thick plain book open on the desk and a straight rule laid across one column, a colleague reading over their shoulder.
   Must read: checking the books.
   Avoid: a bank; a crowd; a shop.

5. `een-vergunning-aanvragen-bij-de-gemeente.png` — Dutch chunk: aanvragen bij (to apply to).
   Scene: One person stands at a counter with a blank form and a pen, holding the form out towards a clerk who reaches for it.
   Must read: asking an authority for permission.
   Avoid: a crowd; a shop; a bank.

6. `in-behandeling-nemen-van-de-aanvraag.png` — Dutch chunk: in behandeling nemen (to process).
   Scene: One seated clerk places the same blank form in a shallow tray marked only by a plain raised ridge; a stack of similar forms lies behind.
   Must read: starting to work through paperwork.
   Avoid: a crowd; a phone; a shop.

7. `de-betaling-verrichten-binnen-de-termijn.png` — Dutch chunk: verrichten binnen (to carry out within).
   Scene: One person stands at a plain counter and lays a small disc-shaped token into a slot, one hand still holding the counter edge; a wall clock with tick marks behind.
   Must read: paying before the deadline.
   Avoid: a bank vault; a crowd; a shop.

8. `in-gebreke-blijven-bij-de-levering.png` — Dutch chunk: in gebreke blijven bij (to fail to deliver).
   Scene: One person stands beside a large plain crate that is still closed, both arms folded, facing a customer who points at the crate with a flat hand and looks at the clock.
   Must read: promising and not coming through.
   Avoid: a crowd; a bank; a shop.

9. `de-administratie-bijhouden-voor-de-accountant.png` — Dutch chunk: bijhouden voor (to keep for).
   Scene: One person sits with a ruled page in a binder and a pen making a short mark beside an existing line; a second binder lies closed to one side.
   Must read: keeping records tidy.
   Avoid: a computer screen with text; a crowd; a shop.

10. `een-offerte-uitbrengen-aan-een-klant.png` — Dutch chunk: een offerte uitbrengen aan (to send a quotation to).
   Scene: One person folds a blank sheet into an envelope and holds it out towards a customer across a counter, one hand open beneath.
   Must read: offering work at a price.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are a contract signed together and then confirmed: two pens on one sheet, then a plain block pressed down. Same table; keep the sheet in both.
Three, four and nine are records: an envelope into a slot, a thick book checked with a rule, a binder kept up to date. Three different bindings and no numbers.
Five and six are the same blank form: handed in at a counter, then laid in a tray. Keep the tray and the clerk identical.
Seven and eight are `verrichten binnen` against `in gebreke blijven bij`: a token in a slot with a clock, and a closed crate with folded arms. Same standing camera.
Ten is a single; the envelope is handed over a counter, not slotted into a wall.

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

## Batch B2-04 — images 31–40

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

1. `een-bijdrage-leveren-aan-het-debat.png` — Dutch chunk: een bijdrage leveren aan (to contribute to).
   Scene: One person stands at a small lectern with one hand raised open and the other flat on the lectern top; a seated row of three turns towards them.
   Must read: adding your voice to a discussion.
   Avoid: a crowd; a speech bubble; a phone.

2. `in-het-debat-gaan-over-het-thema.png` — Dutch chunk: in het debat gaan over (to engage in debate about).
   Scene: Two people sit facing each other at a small table, each with one hand raised and open towards the other; a third sits between them looking from one to the other.
   Must read: arguing the case.
   Avoid: a crowd; a fist fight; a phone.

3. `een-onderzoek-verrichten-naar-de-oorzaken.png` — Dutch chunk: een onderzoek verrichten naar (to carry out research into).
   Scene: One person leans over a bench with a small plain object under a round lens on a stand, one hand steadying the lens arm.
   Must read: looking closely for a cause.
   Avoid: a crowd; a lab with bottles; a phone.

4. `een-hypothese-opstellen-over-het-gedrag.png` — Dutch chunk: een hypothese opstellen over (to formulate a hypothesis about).
   Scene: One person sits at a desk with a sheet bearing a single small square at the top and a long line below it, pen at the line's end.
   Must read: framing an explanation.
   Avoid: a crowd; a shop; a phone.

5. `zich-beroepen-op-een-onderzoek.png` — Dutch chunk: zich beroepen op (to invoke, to refer to).
   Scene: One person stands with a thick plain book held open in one hand and the other hand raised flat, facing two listeners.
   Must read: citing an authority.
   Avoid: a courtroom with a judge; a crowd; a phone.

6. `een-conclusie-trekken-uit-de-resultaten.png` — Dutch chunk: een conclusie trekken uit (to draw a conclusion from).
   Scene: One person stands at a wall panel with three plain bars and pulls one flat hand away from the tallest bar, then turns to face the room.
   Must read: deciding from the evidence.
   Avoid: a crowd; a bank; a shop.

7. `een-standpunt-innemen-ten-opzichte-van-het-voorstel.png` — Dutch chunk: standpunt innemen ten opzichte van (to take a position on).
   Scene: One person steps forward from a standing row and plants both feet apart, one hand flat in front of the chest, facing a raised blank board.
   Must read: making one's position clear.
   Avoid: a crowd; a band without letters; a shop.

8. `kritiek-uiten-op-het-model.png` — Dutch chunk: kritiek uiten op (to criticise).
   Scene: One person stands beside a plain model of a frame with one hand lifted open and the other pointing flat at a loose joint; another figure looks on.
   Must read: pointing out a flaw.
   Avoid: a crowd; a bank; a shop.

9. `onderzoek-doen-naar-het-effect.png` — Dutch chunk: onderzoek doen naar (to conduct research into).
   Scene: Two people stand on either side of a long bench measuring the same plain object with two straight rules, one at each end.
   Must read: measuring an effect.
   Avoid: a crowd; a lab with bottles; a phone.

10. `een-artikel-publiceren-in-een-vakblad.png` — Dutch chunk: publiceren in (to publish in).
   Scene: One person holds a plain open booklet upright in both hands, showing it towards three seated figures at a long table.
   Must read: putting work out to readers.
   Avoid: a crowd; a shop with prices; a phone.

CONTRAST PAIRS
One and 2 share a room and a lectern: one voice at the lectern, then two voices at the table with a third listening. Keep the seated row.
Three and nine are `verrichten naar` against `doen naar`: one person with a lens over a small object, and two people with rules at either end of a bench. One bench, different hands.
Four and five are singles on paper and book: a hypothesis written as a square and a line, and a thick book held open as a source.
Six and seven are the wall bars and the raised board: a hand pulled away from a bar, then a figure stepping out of a row. The bars and the board are both flat panels with no marks.
Eight and ten are singles. The booklet in subject 10 is shown open and upright, the book in subject 5 is held open flat.

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

## Batch B2-05 — images 41–50

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

1. `een-methode-toepassen-op-de-vraag.png` — Dutch chunk: een methode toepassen op (to apply a method to).
   Scene: One person places a small plain frame over a sheet of paper on a table, aligning its edges with the sheet's corner.
   Must read: bringing a procedure to a case.
   Avoid: a crowd; a shop; a phone.

2. `een-theorie-verbinden-met-de-praktijk.png` — Dutch chunk: een theorie verbinden met (to connect with).
   Scene: One person holds a plain closed book in one hand and lays a flat tool on it with the other, both objects touching.
   Must read: joining study and work.
   Avoid: a crowd; a shop; a phone.

3. `een-bewering-onderbouwen-met-cijfers.png` — Dutch chunk: een bewering onderbouwen met (to support with).
   Scene: One person stands beside a wall panel with three plain bars and rests one hand flat under the tallest bar, facing a listener.
   Must read: backing a claim with evidence.
   Avoid: a crowd; a bank; a shop.

4. `zich-uitspreken-tegen-het-voorstel.png` — Dutch chunk: zich uitspreken tegen (to speak out against).
   Scene: One person stands with one arm flat and low across the body, palm down, towards two seated figures who lean back.
   Must read: registering disagreement.
   Avoid: a crowd; a band with a mark; a shop.

5. `een-analyse-maken-van-de-gegevens.png` — Dutch chunk: een analyse maken van (to analyse).
   Scene: One person sits with a large sheet of ruled rows in front of them and a pen circling an area with a quick curved stroke.
   Must read: going through the material.
   Avoid: a crowd; a bank; a phone.

6. `in-tegenspraak-zijn-met-de-bevindingen.png` — Dutch chunk: in tegenspraak zijn met (to contradict).
   Scene: Two people stand on either side of two plain blocks placed at different heights and point at each other's block with flat hands.
   Must read: two results that do not match.
   Avoid: a crowd; a shop; a handshake.

7. `de-aandacht-vestigen-op-het-probleem.png` — Dutch chunk: de aandacht vestigen op (to draw attention to).
   Scene: One person stands and holds a small plain lamp up above head height, towards a wall panel with a single crack, while the room turns towards it.
   Must read: pointing something out.
   Avoid: a crowd; a shop; a phone.

8. `een-beroep-doen-op-de-medewerkers.png` — Dutch chunk: een beroep doen op (to call upon).
   Scene: One person stands with both hands open and raised towards a row of three seated figures, the gesture asking rather than giving.
   Must read: asking others to help.
   Avoid: a crowd; a bank; a shop.

9. `een-voorstel-bespreken-met-de-opleiding.png` — Dutch chunk: een voorstel bespreken met (to discuss with).
   Scene: Two people sit across the corner of a table with a blank sheet between them and one hand near each corner of it.
   Must read: talking something through.
   Avoid: a crowd; a shop; a queue.

10. `een-resultaat-behalen-met-een-groep.png` — Dutch chunk: een resultaat behalen met (to achieve with).
   Scene: One person puts both hands on top of a plain finished object at the end of a bench while two others stand behind with hands on the same object's edges.
   Must read: a shared outcome.
   Avoid: a trophy; a crowd; a bank.

CONTRAST PAIRS
One and two are `toepassen op` against `verbinden met`: a frame laid over a sheet, then a book touching a tool. Both are flat and on a table; keep the frame square and the book thick.
Three, five and 6 use the wall bars and ruled sheets: support for a claim, a circled area on rows, and two blocks at different heights. Bars, rows and blocks must not be interchanged.
Four, seven and eight are standing gestures: a low flat arm with the palm down, a lamp held up, and two open hands raised. Three clearly different arm positions.
Nine and ten are singles: a share of one sheet, and a shared object held by three pairs of hands. No frame may show readable numbers.

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

## Batch B2-06 — images 51–60

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

1. `stelling-nemen-tegen-het-voorstel.png` — Dutch chunk: stelling nemen tegen (to take a stand against).
   Scene: One person stands with one foot forward and both palms flat against a plain board propped upright on a stand, holding it steady while facing a seated row behind.
   Must read: taking a stand against an idea.
   Avoid: a crowd; a band with a mark; a phone.

2. `zich-verdiepen-in-de-literatuur.png` — Dutch chunk: zich verdiepen in de literatuur (to read up on the literature).
   Scene: One person sits at a desk surrounded on both sides by small stacks of plain closed books, one open on the desk in front of them.
   Must read: reading widely.
   Avoid: a library shelf; a crowd; a phone.

3. `een-document-aanhalen-in-de-tekst.png` — Dutch chunk: aanhalen in (to quote in).
   Scene: One person points with one finger at a short ruled strip on a page while the other hand holds a second page beside it with a matching strip.
   Must read: bringing a source into the text.
   Avoid: a crowd; a shop; a phone.

4. `een-verwijzing-opnemen-in-de-inleiding.png` — Dutch chunk: een verwijzing opnemen in (to include a reference in).
   Scene: One person places a small blank card between two pages of an open thick book and closes it with both hands.
   Must read: marking a place in a source.
   Avoid: a crowd; a bank; a phone.

5. `een-argument-weerleggen-met-bewijs.png` — Dutch chunk: weerleggen met (to refute with).
   Scene: One person lays a plain ruled sheet on the table beside a small stack of blocks built by a second figure, and pushes the sheet forward with one finger; the second figure's hand stops above the stack.
   Must read: answering a claim with evidence.
   Avoid: a crowd; a shop; a phone.

6. `een-standpunt-verdedigen-tegen-kritiek.png` — Dutch chunk: verdedigen tegen (to defend against).
   Scene: One person stands with a large plain panel held upright in both hands in front of them, facing two figures who press forward with open hands.
   Must read: holding a position under attack.
   Avoid: a crowd; a boxing match; a shop.

7. `een-definitie-geven-van-het-begrip.png` — Dutch chunk: een definitie geven van (to give a definition of).
   Scene: One person holds a small plain frame around a single object on a table, so that only that object sits inside the frame, and speaks towards a second figure who leans in.
   Must read: setting the boundary of a term.
   Avoid: a crowd; a shop; a phone.

8. `een-vergelijking-maken-tussen-twee-groepen.png` — Dutch chunk: een vergelijking maken tussen (to compare).
   Scene: One person stands with one hand over each of two small plain groups of blocks, the left group taller, and looks from one to the other.
   Must read: weighing two sets.
   Avoid: a crowd; a bank; a shop.

9. `een-these-verdedigen-voor-de-commissie.png` — Dutch chunk: verdedigen voor (to defend before).
   Scene: One person stands facing three seated figures behind a long table, a thick plain folder held against the chest with both arms.
   Must read: presenting a case to a panel.
   Avoid: a courtroom with a judge; a crowd; a phone.

10. `een-beoordeling-krijgen-van-de-begeleider.png` — Dutch chunk: een beoordeling krijgen van (to be assessed by).
   Scene: One seated figure hands a blank sheet to a standing figure who takes it with both hands; the giver's pen still lies on the table.
   Must read: receiving a verdict on one's work.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One, five and six are singles in the academic room: a propped board, a ruled sheet laid beside a small stack, a panel held up. Keep the panel wide and the board narrow.
Two and three are desk singles: books stacked on both sides, and two ruled strips held side by side. Both use paper; the books are closed, the page is open.
Four, seven and ten are paper and frame singles: a card between pages, a frame laid around one object, and a sheet handed over. The frame appears twice and must differ: upright in the earlier method frame, flat here.
Eight and nine are `vergelijking maken tussen` and `een these verdedigen voor`: two block groups, then three seated figures. No numerals anywhere.

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

## Batch B2-07 — images 61–70

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

1. `een-patient-onderzoeken-op-klachten.png` — Dutch chunk: onderzoeken op (to examine for).
   Scene: One person sits on the edge of a plain bench with an arm held out while another figure holds a small round lens against the inside of the elbow.
   Must read: checking for a complaint.
   Avoid: a hospital cross; a crowd; a phone.

2. `een-patient-doorverwijzen-naar-de-specialist.png` — Dutch chunk: doorverwijzen naar (to refer to).
   Scene: One person sits at a desk and holds a blank sheet out towards a patient who has half risen from a chair, one hand already on a coat.
   Must read: sending someone further.
   Avoid: a crowd; a bank; a shop.

3. `een-behandeling-ondergaan-voor-de-knie.png` — Dutch chunk: een behandeling ondergaan voor (to undergo treatment for).
   Scene: One person sits with one leg straight out on a small stool and both hands resting on the thigh; a plain folded bandage lies beside them.
   Must read: receiving care for a part of the body.
   Avoid: a hospital cross; a crowd; a phone.

4. `een-klacht-aanmelden-bij-de-huisarts.png` — Dutch chunk: aanmelden bij (to register with).
   Scene: One person stands at a counter and hands a blank card to a seated clerk who has a plain register open in front of them.
   Must read: being listed with a doctor.
   Avoid: a crowd; a bank; a shop.

5. `een-medicijn-voorschrijven-tegen-de-pijn.png` — Dutch chunk: voorschrijven tegen (to prescribe for).
   Scene: One person stands at a counter with a small plain bottle in one hand and a blank slip in the other, held out towards a patient.
   Must read: giving something that works against a symptom.
   Avoid: a crowd; a shop with prices; a phone.

6. `zich-herstellen-van-een-operatie.png` — Dutch chunk: zich herstellen van (to recover from).
   Scene: One person sits up in a bed with the blanket to the waist and a plain folded sheet of paper in one hand; a chair beside the bed is empty.
   Must read: getting well again.
   Avoid: a hospital cross; a crowd; a phone.

7. `lijden-aan-een-chronische-aandoening.png` — Dutch chunk: lijden aan (to suffer from).
   Scene: One person walks slowly with one hand on a plain low rail beside a wall, body bent slightly forward, one step at a time.
   Must read: a long-lasting complaint.
   Avoid: a crowd; a hospital cross; a phone.

8. `een-afspraak-maken-met-de-tandarts.png` — Dutch chunk: een afspraak maken met (to make an appointment with).
   Scene: One person stands at a counter with a plain telephone receiver in one hand and a small blank card in the other, held up towards the counter.
   Must read: fixing a visit.
   Avoid: a crowd; a bank; a shop.

9. `een-verwijzing-krijgen-naar-de-radioloog.png` — Dutch chunk: een verwijzing krijgen naar (to get a referral to).
   Scene: One person holds a sealed blank envelope out to a patient while pointing with the other hand towards an open doorway behind them.
   Must read: being sent to another room.
   Avoid: a crowd; a bank; a shop.

10. `een-uitleg-geven-over-de-behandeling.png` — Dutch chunk: een uitleg geven over (to give an explanation of).
   Scene: One person stands at a bench and turns a plain model of a joint shape in both hands towards a seated patient who leans in.
   Must read: explaining the procedure.
   Avoid: a crowd; a shop; a phone.

CONTRAST PAIRS
One and 2 share the clinic bench and chair: a lens held to an elbow, then a sheet handed over as the patient rises. Keep the room the same.
Three, five and ten are clinic singles with an object in the hand: a folded bandage, a plain bottle with a slip, and a joint model. The three objects must not resemble each other.
Four and eight both happen at a counter with a card; in subject 4 the register is open, in subject 8 the receiver is in the hand.
Six and seven are body-posture singles: sitting up in bed with a sheet, and walking slowly with a rail. Neither may show a hospital cross or a bed with a canopy.
Nine is a single; the envelope is sealed, not opened.

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

## Batch B2-08 — images 71–80

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

1. `een-defect-melden-bij-de-technische-dienst.png` — Dutch chunk: melden bij (to report to).
   Scene: One person holds a plain telephone receiver to the ear with one hand and taps a stalled machine beside them with the other hand.
   Must read: calling about a fault.
   Avoid: a crowd; a bank; a shop.

2. `een-onderdeel-vervangen-door-een-nieuw.png` — Dutch chunk: vervangen door (to replace with).
   Scene: One person lifts a plain worn part out of a machine and sets a new part of the same shape beside the empty socket.
   Must read: swapping a broken piece.
   Avoid: a crowd; a shop; a phone.

3. `te-wijten-zijn-aan-een-storing.png` — Dutch chunk: te wijten zijn aan (to be due to).
   Scene: One person stands beside a stalled machine with a loose belt, one hand open towards it and the other at the chin, explaining to a colleague who nods; the machine is the only thing they both look at.
   Must read: the fault lies with the machine.
   Avoid: a crowd; a bank; a shop.

4. `een-systeem-koppelen-aan-het-netwerk.png` — Dutch chunk: koppelen aan (to connect to).
   Scene: One person holds one end of a plain cable up to a socket on a panel and pushes it in with the other hand steadying the panel.
   Must read: plugging one thing into another.
   Avoid: a crowd; a shop; a phone.

5. `een-installatie-afstellen-op-de-ruimte.png` — Dutch chunk: afstellen op (to adjust to).
   Scene: One person turns a small dial on a wall panel and steps back to look, then turns it back a little; the room around is plain.
   Must read: tuning for the place.
   Avoid: a crowd; a shop; a phone.

6. `een-installatie-uitschakelen-tijdens-onderhoud.png` — Dutch chunk: uitschakelen tijdens (to switch off during).
   Scene: One person kneels by a wall switch with one hand on the lever, pushing it down, while a second figure holds a plain lamp above the open panel.
   Must read: cutting power to work safely.
   Avoid: a crowd; a bank; a shop.

7. `een-installatie-weer-inschakelen-na-onderhoud.png` — Dutch chunk: weer inschakelen na (to switch back on after).
   Scene: The same switch and panel, now closed, with one hand lifting the lever up and the second figure lowering the lamp.
   Must read: power restored.
   Avoid: a crowd; a bank; a shop.

8. `een-storing-verhelpen-door-het-onderdeel-te-vervangen.png` — Dutch chunk: verhelpen door (to remedy by).
   Scene: One person holds the same new part in its socket and presses it home with both thumbs, the machine now standing in the same place as before.
   Must read: the fix is in place.
   Avoid: a crowd; a shop; a phone.

9. `een-meting-uitvoeren-met-een-meter.png` — Dutch chunk: een meting uitvoeren met (to take a reading with).
   Scene: One person holds two short probes against two points on a panel while a plain round dial in the other hand shows its pointer on the right side.
   Must read: testing what a machine is doing.
   Avoid: a crowd; a bank; a shop.

10. `een-technische-fout-opslaan-in-het-logboek.png` — Dutch chunk: opslaan in (to record in).
   Scene: One person writes with one hand on a ruled log sheet clipped to a board while the other hand holds the board steady against the machine.
   Must read: writing a fault down.
   Avoid: a computer screen with text; a crowd; a shop.

CONTRAST PAIRS
One, two and eight are one machine in three states: a fault called in, a worn part lifted out, and the new part pressed home. Keep the machine body identical in all three.
Three is the same machine standing still with a loose belt and two people discussing it; it must not repeat the phone of subject 1.
Four and five are `koppelen aan` against `afstellen op`: a cable pushed into a socket, and a dial turned then turned back. Both panels are plain rectangles.
Six and seven are the same switch and panel, lever down then lever up, panel open then closed. The lamp's position is the second marker.
Nine and ten are singles: probes and a dial, then a ruled log on a board. No frame may show a screen with text.

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

## Batch B2-09 — images 81–90

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

1. `een-diagnose-stellen-op-basis-van-de-klachten.png` — Dutch chunk: een diagnose stellen op basis van (to base a diagnosis on).
   Scene: One person sits at a desk with a blank sheet in front of them and taps two ruled marks on it with the back of a pen, speaking to a patient.
   Must read: a conclusion drawn from symptoms.
   Avoid: a hospital cross; a crowd; a phone.

2. `controle-houden-op-de-wond.png` — Dutch chunk: controle houden op (to keep a check on).
   Scene: One person sits on a bench with one sleeve pushed up and a plain band wound round the forearm; a second figure leans in with both hands on the band, eyes on it.
   Must read: watching an injury closely.
   Avoid: a crowd; a bank; a shop.

3. `een-toestel-onderhouden-volgens-de-handleiding.png` — Dutch chunk: onderhouden volgens (to maintain according to).
   Scene: One person holds a plain closed booklet in one hand and a small tool in the other, standing before an open machine panel, step by step.
   Must read: servicing to the book.
   Avoid: a crowd; a shop; a phone.

4. `een-meting-verrichten-aan-het-toestel.png` — Dutch chunk: een meting verrichten aan (to take a reading from).
   Scene: One person presses a flat sensor against the side of a plain machine and holds it there with both hands, watching a separate dial on a stand.
   Must read: reading what the machine gives.
   Avoid: a crowd; a bank; a shop.

5. `een-storing-voorkomen-door-regelmatig-onderhoud.png` — Dutch chunk: voorkomen door (to prevent by).
   Scene: One person closes an already clean machine panel and wipes the outside with a plain cloth in the other hand; a small oil can stands on the floor.
   Must read: stopping trouble before it starts.
   Avoid: a crowd; a bank; a shop.

6. `een-behandeling-toepassen-op-de-wond.png` — Dutch chunk: toepassen op (to apply to).
   Scene: One person sits with one forearm held out and another figure lays a plain folded bandage across it, pressing it down with a flat hand.
   Must read: putting something on an injury.
   Avoid: a hospital cross; a crowd; a phone.

7. `een-patient-informeren-over-de-risicos.png` — Dutch chunk: informeren over (to inform about).
   Scene: One person sits facing a standing figure in a plain coat who holds a blank sheet out and points at one place on it with a finger.
   Must read: warning before consent.
   Avoid: a crowd; a bank; a shop.

8. `een-patient-voorbereiden-op-de-ingreep.png` — Dutch chunk: voorbereiden op (to prepare for).
   Scene: One person sits on a bench with a plain gown folded on the knees and both hands smoothing it, looking at a closed door.
   Must read: getting ready for treatment.
   Avoid: a crowd; a shop; a phone.

9. `een-onderzoek-uitvoeren-bij-de-patient.png` — Dutch chunk: uitvoeren bij (to carry out on).
   Scene: One person sits with one arm on a small table while another figure looks through a round lens held to their eye towards the arm.
   Must read: examining a person directly.
   Avoid: a crowd; a bank; a shop.

10. `een-toestel-aansluiten-op-het-stroomnet.png` — Dutch chunk: aansluiten op (to connect to).
   Scene: One person pushes a plain plug into a wall socket with one hand and holds the cable steady with the other; a machine sits just beside them.
   Must read: giving power to a machine.
   Avoid: a crowd; a shop; a phone.

CONTRAST PAIRS
One and 2 share a clinic room: a diagnosis marked on a sheet, then a band being checked on a forearm. Keep the desk and bench in the same places.
Two and six both use a band or a folded bandage on a forearm; in subject 2 the band is already wound round the forearm and both hands rest on it, in subject 6 the bandage is still being laid along the forearm. They must not look alike.
Three, four and ten are technical singles on machines: a closed booklet and tool at an open panel, a sensor held to a machine, and a plug pushed into a socket.
Five is the preventive counterpart; the cloth and oil can are its marks; no soap bubbles or shine lines.
Seven, eight and nine are clinic singles with a sheet, a folded gown and a lens at the eye. No frame may show a hospital cross or a readable form.

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

## Batch B2-10 — images 91–100

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

1. `in-beroep-gaan-tegen-de-uitspraak.png` — Dutch chunk: in beroep gaan tegen (to appeal against).
   Scene: One person stands at a counter with a blank sheet in one hand and the other hand flat on the counter, facing a seated clerk who has risen slightly.
   Must read: challenging a decision.
   Avoid: a courtroom with a judge; a crowd; a bank.

2. `een-beroep-behandelen-bij-de-rechter.png` — Dutch chunk: behandelen bij (to hear, to deal with).
   Scene: One person sits behind a raised bench and holds the same blank sheet up to read it; two others sit on a plain bench facing them.
   Must read: a case looked at properly.
   Avoid: a crowd; a bank; a shop.

3. `een-verdachte-beschuldigen-van-diefstal.png` — Dutch chunk: beschuldigen van (to accuse of).
   Scene: One person stands opposite another and points a flat hand at a plain bag lying open on a table between them.
   Must read: naming the offence.
   Avoid: a crowd; a bank; a shop.

4. `een-getuige-ondervragen-over-de-gebeurtenissen.png` — Dutch chunk: ondervragen over (to question about).
   Scene: Two people stand facing each other, the questioner leaning in with one hand open, the witness upright with both hands at the sides.
   Must read: asking what was seen.
   Avoid: a crowd; a shop; a phone.

5. `in-aanmerking-nemen-als-bewijs.png` — Dutch chunk: in aanmerking nemen als (to take into account as).
   Scene: One person lifts a plain object from a table with both hands and turns it towards a second figure who has a notebook open.
   Must read: something accepted as proof.
   Avoid: a crowd; a bank; a shop.

6. `een-vonnis-uitspreken-over-de-zaak.png` — Dutch chunk: een vonnis uitspreken over (to pronounce a verdict on).
   Scene: One person at a raised bench lays one hand flat on a closed book and speaks towards the two figures below.
   Must read: the decision is given.
   Avoid: a crowd; a bank; a shop.

7. `een-zaak-doorverwijzen-naar-een-hogere-instantie.png` — Dutch chunk: doorverwijzen naar (to refer to).
   Scene: One person at a desk sets the blank sheet into an envelope and holds it out towards a second clerk who stands by a doorway.
   Must read: passing a case upward.
   Avoid: a crowd; a bank; a shop.

8. `zich-beroepen-op-het-verdrag.png` — Dutch chunk: zich beroepen op (to invoke).
   Scene: One person stands with a thick plain book open in one hand and the other hand lifted flat, facing a raised bench.
   Must read: citing the source of a right.
   Avoid: a crowd; a shop; a phone.

9. `een-maatregel-nemen-tegen-de-overtreder.png` — Dutch chunk: nemen tegen (to take against).
   Scene: One person stands before a closed door and places a plain narrow band of paper across the join between door and frame with both hands.
   Must read: an official restriction.
   Avoid: a crowd; a shop; a bank.

10. `een-dossier-overdragen-aan-de-opvolger.png` — Dutch chunk: overdragen aan (to hand over to).
   Scene: One person places a thick plain folder into the hands of a second, who is already turning towards a desk; both have one hand on the folder.
   Must read: the file changes hands.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and 2 share the sheet and the raised bench: a challenge made at a counter, then the sheet read at the bench. Keep the two seated figures on the lower bench only in subject 2.
Three and four are people facing each other with a plain object between or a question asked; keep the open bag in subject 3 and the upright witness in subject 4.
Five, seven and ten are documents changing hands: an object lifted as evidence, a sheet pushed up a level in an envelope, and a thick folder passed between hands. Three different holders.
Six, eight and nine are the bench and the doors: a verdict spoken with a closed book, a thick book opened as a source, and a paper band on a door. The bands and the books must differ clearly.
No frame may show a gavel, a wig, a badge or a readable seal.

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

## Batch B2-11 — images 101–110

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

1. `een-overeenkomst-sluiten-met-de-eigenaar.png` — Dutch chunk: een overeenkomst sluiten met (to conclude with).
   Scene: Two people sit at a table and each lays one hand flat on a blank sheet between them; the other hands are still on the table edge.
   Must read: agreeing on terms.
   Avoid: a handshake over a crate; a crowd; a bank.

2. `een-contract-ondertekenen-ten-overstaan-van-een-getuige.png` — Dutch chunk: ondertekenen ten overstaan van (to sign in the presence of).
   Scene: One person signs a blank sheet with a pen while a second stands opposite with both hands clasped in front, watching.
   Must read: signing before a witness.
   Avoid: a crowd; a bank; a shop.

3. `een-geschil-beslechten-buiten-de-rechter-om.png` — Dutch chunk: buiten de rechter om (without going to court).
   Scene: Two people sit facing each other at a table and one pushes a plain sheet across to the other, who places a hand on it.
   Must read: settling apart from the law.
   Avoid: a courtroom with a judge; a crowd; a phone.

4. `een-claim-afwijzen-op-grond-van-gebrek-aan-bewijs.png` — Dutch chunk: afwijzen op grond van (to reject on the grounds of).
   Scene: One person holds a blank sheet in both hands and turns it over, showing the back is empty, towards a second figure.
   Must read: the claim fails for want of evidence.
   Avoid: a crowd; a bank; a shop.

5. `een-eis-indienen-tegen-de-verhuurder.png` — Dutch chunk: indienen tegen (to file against).
   Scene: One person slides a blank form into a slot in a wall panel while a second figure stands behind with a set face and folded arms.
   Must read: bringing a formal complaint.
   Avoid: a crowd; a shop; a phone.

6. `zich-verweren-tegen-de-eis.png` — Dutch chunk: zich verweren tegen (to defend against).
   Scene: One person stands with a plain panel held in both hands in front of them, facing another who holds a blank form up.
   Must read: answering a complaint.
   Avoid: a crowd; a boxing match; a bank.

7. `een-document-vervalsen-om-voordeel-te-behalen.png` — Dutch chunk: vervalsen om (to falsify in order to).
   Scene: One person holds a blank sheet in one hand and a small plain block in the other, up to the sheet, glancing towards a doorway.
   Must read: changing a paper for gain.
   Avoid: a crowd; a bank; a shop.

8. `een-bekentenis-afleggen-tegenover-de-rechter.png` — Dutch chunk: tegenover de rechter (before the judge).
   Scene: One person stands before a raised bench with head slightly bowed and both hands open at the sides; the judge sits still above.
   Must read: saying it was me.
   Avoid: a crowd; a bank; a shop.

9. `een-zaak-overdragen-van-de-onderzoeker-aan-de-officier.png` — Dutch chunk: overdragen van … aan (to transfer from … to).
   Scene: One person hands a thick plain folder to another, who takes it with both hands; a raised bench is drawn behind them in the distance.
   Must read: the case moves up.
   Avoid: a crowd; a bank; a shop.

10. `een-vonnis-uitvoeren-volgens-de-wet.png` — Dutch chunk: uitvoeren volgens (to carry out according to).
   Scene: One person places a plain band of paper across a closed door while holding an open thick book in the other hand.
   Must read: the decision is acted on.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are the same sheet and table: hands flat on it, then a pen signing with a witness clasping hands. The witness must not hold paper.
Three and four are the same sheet handed or turned: settled by a hand on it, and turned back empty. Keep the sheet identical and the flat hand as opposed to both hands.
Five and six are a form in a slot, then a panel held up. The panel is larger than the form and covers the chest.
Seven and eight are the doorway glance and the bowed head: the falsifier looks aside, the confessor looks down. Different rooms.
Nine and ten both reuse objects from earlier legal batches: a thick folder between two hands and a paper band with a book. Keep the bench distant in subject 9 and absent in subject 10.

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

## Batch B2-12 — images 111–120

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

1. `een-dagvaarding-bezorgen-aan-de-gedaagde.png` — Dutch chunk: bezorgen aan (to serve on).
   Scene: One person holds a sealed blank envelope out at arm's length towards a second figure who has just opened a door.
   Must read: an official notice arrives.
   Avoid: a crowd; a bank; a shop.

2. `een-zitting-bepalen-op-een-latere-datum.png` — Dutch chunk: bepalen op (to set for).
   Scene: One person sits at a desk with a plain calendar sheet of boxes and taps one box with a finger, pen in the other hand.
   Must read: fixing the day of the hearing.
   Avoid: a crowd; a shop; a phone.

3. `een-getuige-ophouden-aan-de-uitgang.png` — Dutch chunk: ophouden aan (to stop at, to hold at).
   Scene: One person stands in an open doorway with a flat hand raised towards a second who has stopped mid-step, one hand on the frame.
   Must read: stopping someone passing.
   Avoid: a crowd; a bank; a shop.

4. `een-verklaring-afleggen-onder-ed.png` — Dutch chunk: afleggen onder ede (to testify under oath).
   Scene: One person stands in a bare room with one hand raised flat beside the head and the other on a thick closed book resting on a stand.
   Must read: promising to tell the truth.
   Avoid: a crowd; a bank; a shop.

5. `afzien-van-vervolging.png` — Dutch chunk: afzien van (to refrain from).
   Scene: One person closes a plain folder and lays both hands flat on top of it, then pushes it to the far edge of the desk, looking up at a second figure with a single slow nod.
   Must read: the case is set aside.
   Avoid: a crowd; a bank; a shop.

6. `een-overtreding-beboeten-met-een-boete.png` — Dutch chunk: beboeten met (to fine with).
   Scene: One person holds out a small blank slip towards a second figure who takes it, one hand on a bicycle handlebar.
   Must read: a penalty handed over.
   Avoid: a crowd; a bank; a shop.

7. `een-beroep-aantekenen-binnen-de-termijn.png` — Dutch chunk: aantekenen binnen (to lodge within).
   Scene: One person writes on a blank form at a counter and taps the corner of the form with the pen, a wall clock shape with tick marks behind.
   Must read: filing before time runs out.
   Avoid: a crowd; a bank; a shop.

8. `een-getuigenverklaring-opnemen-in-het-dossier.png` — Dutch chunk: opnemen in (to include in).
   Scene: One person places a small blank card between the pages of a thick plain folder and closes it with both hands.
   Must read: a statement joins the file.
   Avoid: a crowd; a bank; a shop.

9. `een-uitspraak-motiveren-met-argumenten.png` — Dutch chunk: motiveren met (to justify with).
   Scene: One person at a raised bench lays one hand on a closed book and speaks, the other hand open towards the two figures below.
   Must read: giving the reasons.
   Avoid: a crowd; a bank; a shop.

10. `de-verdachte-vrijspreken-van-alle-schuld.png` — Dutch chunk: vrijspreken van (to acquit of).
   Scene: One person at the bench holds a blank sheet up and turns it over so the empty back faces the two figures below, then sets it down.
   Must read: the case ends without proof.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and three both use a doorway: an envelope offered to a figure who has just opened the door, and a flat hand stopping a figure mid-step. Keep the door open in both; in subject 1 nothing is held up except the envelope.
Two and seven are dates: calendar boxes tapped at a desk, and a form written at a counter with a clock behind. Keep the boxes and the clock different sizes.
Four and eight are a thick closed book and a thick closed folder: an oath taken on the book, and a card placed inside the folder. The folder must be visibly thicker.
Five, six and ten are outcomes: a folder closed flat, a slip taken by a cyclist, and a sheet turned empty. Keep the cyclist's handlebar in subject 6 only.
Nine is the bench again; do not reuse the gavel.

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

## Batch B2-13 — images 121–130

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

1. `een-bericht-verspreiden-via-sociale-media.png` — Dutch chunk: verspreiden via (to spread via).
   Scene: One person holds a plain device up in both hands with an open square shape glowing as a small burst of strokes, and two others look over their shoulders.
   Must read: news travelling from phone to phone.
   Avoid: a crowd; a bank; a shop.

2. `zich-richten-tot-de-lezers.png` — Dutch chunk: zich richten tot (to address).
   Scene: One person sits at a desk with a blank sheet and a pen, facing an empty chair drawn as if there were a reader in it, one hand open towards it.
   Must read: writing for someone.
   Avoid: a crowd; a shop; a phone.

3. `commentaar-leveren-op-het-beleid.png` — Dutch chunk: commentaar leveren op (to comment on).
   Scene: One person stands with one hand open and lifted, the other flat, turning towards two seated figures at a table with blank sheets.
   Must read: adding an opinion.
   Avoid: a crowd; a bank; a shop.

4. `een-mening-geven-over-de-plannen.png` — Dutch chunk: een mening geven over (to give an opinion on).
   Scene: One person stands beside a plain raised board with one hand open towards it and the head tilted, speaking to nobody in the room.
   Must read: judging a plan.
   Avoid: a crowd; a bank; a shop.

5. `in-gesprek-gaan-met-de-bewoners.png` — Dutch chunk: in gesprek gaan met (to enter into discussion with).
   Scene: One person sits down on a low bench beside a resident who turns towards them, both hands on their knees; a plain doorway is behind them.
   Must read: listening to people.
   Avoid: a crowd; a shop; a phone.

6. `zich-beroepen-op-bronnen.png` — Dutch chunk: zich beroepen op (to cite sources).
   Scene: One person holds a thick plain notebook open in one hand and points with the other hand at one line in it.
   Must read: backing a story up.
   Avoid: a crowd; a bank; a shop.

7. `een-onderwerp-aankaarten-bij-het-publiek.png` — Dutch chunk: aankaarten bij (to raise with).
   Scene: One person stands at the head of a small group with one hand raised open, and the group turns towards them from their seats.
   Must read: bringing something out into the open.
   Avoid: a crowd; a bank; a shop.

8. `een-uitspraak-in-twijfel-trekken.png` — Dutch chunk: in twijfel trekken (to call into question).
   Scene: One person tilts their head and raises one flat hand towards a blank sheet held by another, palm outwards in a stop.
   Must read: refusing to take it at face value.
   Avoid: a crowd; a bank; a shop.

9. `een-bericht-plaatsen-op-de-voorpagina.png` — Dutch chunk: plaatsen op (to place on).
   Scene: One person lays a large blank page flat on a long table with both hands, aligning its corners with the table's edge.
   Must read: putting the story forward.
   Avoid: a crowd; a bank; a shop.

10. `ingaan-op-de-kritiek-van-de-lezers.png` — Dutch chunk: ingaan op (to respond to).
   Scene: One person reads a folded blank sheet over the counter and nods, one hand open towards the figure who handed it over.
   Must read: answering the complaints.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and nine both use a page held flat, one in the hand as a device and one on a table. Keep the device small and hand-sized, the page large and on the table.
Two and five both involve an empty or occupied chair: a reader imagined opposite a writer, and a resident sitting on a bench. Different postures and rooms.
Three, four and seven are standing speakers: at a table, beside a raised board, and at the head of a seated group. Keep the group only in subject 7.
Six, eight and ten are documents: an open notebook with a line pointed at, a sheet tilted and refused, and a folded sheet read at a counter. The refusal hand must not repeat the pointing hand.
No screen may show letters; the page has rule marks only.

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

## Batch B2-14 — images 131–140

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

1. `een-standpunt-in-nemen-in-een-column.png` — Dutch chunk: standpunt innemen in (to take a position in).
   Scene: One person sits at a desk with a ruled sheet in front of them and a pen held upright at its top, head turned towards a window.
   Must read: committing to an opinion in writing.
   Avoid: a crowd; a bank; a shop.

2. `een-debat-voeren-over-het-beleid.png` — Dutch chunk: een debat voeren over (to debate).
   Scene: Two people sit facing each other with one raised hand each, a small table between them holding two blank sheets.
   Must read: two sides arguing.
   Avoid: a crowd; a bank; a shop.

3. `een-onderzoek-aanhalen-in-een-artikel.png` — Dutch chunk: aanhalen in (to cite in).
   Scene: One person holds a plain closed booklet in one hand and points to a sheet on the desk with the other, a matching block drawn on the sheet.
   Must read: backing a piece with research.
   Avoid: a crowd; a bank; a shop.

4. `een-reactie-vragen-op-het-nieuws.png` — Dutch chunk: een reactie vragen op (to ask for a response to).
   Scene: One person holds out a small plain device towards a second figure who turns away with one hand raised flat, head down.
   Must read: asking for a comment.
   Avoid: a crowd; a bank; a shop.

5. `ruimte-geven-aan-een-mening.png` — Dutch chunk: ruimte geven aan (to give space to).
   Scene: One person steps back with both hands open towards a second figure who speaks with one hand raised, while a third listens; the first figure has visibly made room on the bench.
   Must read: letting someone else's view be heard.
   Avoid: a crowd; a bank; a shop.

6. `nadenken-over-de-gevolgen.png` — Dutch chunk: nadenken over (to think about).
   Scene: One person sits alone with both elbows on a table and the forehead resting on the hands, a single blank sheet pushed to the edge.
   Must read: reflect on what will follow.
   Avoid: a crowd; a bank; a shop.

7. `een-verwijt-maken-aan-de-overheid.png` — Dutch chunk: een verwijt maken aan (to reproach).
   Scene: One person stands with one hand pointing flat towards a plain tall building shape, speaking over the shoulder to a second figure.
   Must read: laying blame at the top.
   Avoid: a crowd; a bank; a shop.

8. `zich-verdedigen-tegen-de-beschuldiging.png` — Dutch chunk: zich verdedigen tegen (to defend oneself against).
   Scene: One person stands behind a plain panel held upright with both hands, facing a second figure who points flat at them.
   Must read: answering a charge in public.
   Avoid: a crowd; a bank; a shop.

9. `in-tegenspraak-gaan-met-de-cijfers.png` — Dutch chunk: in tegenspraak gaan met (to contradict).
   Scene: One person holds up a blank sheet in one hand and a plain block in the other and brings them together, shaking the head.
   Must read: facts that do not fit.
   Avoid: a crowd; a bank; a shop.

10. `een-pleidooi-houden-voor-verandering.png` — Dutch chunk: een pleidooi houden voor (to plead for).
   Scene: One person stands with both hands open and raised, turned towards a seated group, the body leaning forward.
   Must read: making the case for change.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are the same opinion in two forms: written at a desk with a pen upright, and argued across a small table. Keep the ruled sheet in subject 1 only.
Three and four both involve a plain device or a booklet: a closed booklet and a pointed line, and a device held out towards a refusing figure. The hand raised flat must be used only in subject 4.
Five, nine and ten are singles: a figure stepping back with open hands, a sheet and block brought together, and open hands raised. Three different gestures; none may show a speech bubble.
Six is the only still, silent frame in the batch; keep the head on the hands.
Seven and 8 share a pointing hand and a panel; the building shape in subject 7 must not appear in subject 8.

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

## Batch B2-15 — images 141–150

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

1. `op-de-valreep-liggen.png` — Dutch chunk: op de valreep (at the last moment).
   Scene: One person runs towards a doorway with a bag bouncing behind and one arm outstretched towards the door's edge; a plain clock face with tick marks is on the wall.
   Must read: just in time.
   Avoid: a crowd; a bank; a shop.

2. `trappen-in-een-val.png` — Dutch chunk: trappen in (to fall for).
   Scene: One person steps forward with one foot landing flat on a small plain ribbed mat on the floor and arms flung up; a second figure behind has a hand over the mouth.
   Must read: caught by a trick.
   Avoid: a crowd; a bank; a shop.

3. `voor-de-gek-houden.png` — Dutch chunk: voor de gek houden (to make a fool of).
   Scene: One person holds out a plainly hollow half-shell of bread towards a second figure who reaches for it with both hands, while the first holds back a smile.
   Must read: a joke at someone's expense.
   Avoid: a crowd; a bank; a shop.

4. `de-handen-uit-de-mouwen-steken.png` — Dutch chunk: de handen uit de mouwen steken (to get stuck in).
   Scene: One person kneels with both sleeves pushed high and both hands inside a box of loose parts, sorting them.
   Must read: starting real work.
   Avoid: a crowd; a bank; a shop.

5. `de-kat-uit-de-boom-kijken.png` — Dutch chunk: de kat uit de boom kijken (to wait and see).
   Scene: One person stands behind an open door and looks around its edge with both hands on the frame, not stepping in.
   Must read: watching before entering.
   Avoid: a crowd; a bank; a shop.

6. `de-moer-onder-de-kinderen-geven.png` — Dutch chunk: de moer onder de kinderen geven (to give the children a good talking-to).
   Scene: One person leans over a kitchen table with a flat hand on it and an open mouth, facing three small figures who look down.
   Must read: scolding a group.
   Avoid: a crowd; a bank; a shop.

7. `met-vallen-en-opstaan-leren.png` — Dutch chunk: met vallen en opstaan (by trial and error).
   Scene: One person sits on the floor with a small bicycle lying on its side beside them and rubs one knee, about to rise.
   Must read: learning the hard way.
   Avoid: a crowd; a bank; a shop.

8. `iets-op-de-grote-hoop-gooien.png` — Dutch chunk: op de grote hoop gooien (to lump together).
   Scene: One person tips a small basket of mixed plain pieces into one big crate with both hands; the crate is already full of the same pieces.
   Must read: losing the differences.
   Avoid: a crowd; a bank; a shop.

9. `terugkijken-op-de-gebeurtenis.png` — Dutch chunk: terugkijken op (to look back on).
   Scene: One person sits on a step with chin on one hand, looking back over the shoulder towards an open door behind them.
   Must read: reviewing what has already happened.
   Avoid: a crowd; a bank; a shop.

10. `iets-op-de-koop-toenemen.png` — Dutch chunk: op de koop toenemen (to accept as part of the deal).
   Scene: One person carries a plain crate with a small chipped corner visible, shrugging with one shoulder and mouth flat.
   Must read: taking the rough with the smooth.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are a pair: a run for a doorway at the last moment, then the same two figures with a hollow shell and a foot on a ribbed mat. Keep the pair and the doorway in both.
Three and six both happen at a plain table: a knapsack in a box of parts at knee height, and a lean over a table with three small figures. Different heights and different numbers of people.
Four and ten are both looking and carrying: a glance from behind a door, and a crate with a chipped corner. Neither may show a cat or an animal.
Five and nine are singles: a scolding at a table, and a slow look over the shoulder. Keep the scolding mouth open and the remembering mouth closed.
Seven and eight are singles: a tipped basket into one crate, and a step with a hand under the chin. No frame may show readable words in a bubble.

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

## Batch B2-16 — images 151–160

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

1. `zich-geen-zorgen-maken-over-het-resultaat.png` — Dutch chunk: zich geen zorgen maken over (not to worry about).
   Scene: One person sits back in a chair with a cup held loosely in one hand and legs crossed, a single relaxed line for a mouth; a plain closed folder lies untouched on the table beside them.
   Must read: easy confidence.
   Avoid: a crowd; a bank; a shop.

2. `voet-bij-stuk-houden.png` — Dutch chunk: voet bij stuk houden (to stand firm).
   Scene: One person stands with both hands on the table, one foot planted forward and chin lifted, facing two seated figures who have pushed their chairs back.
   Must read: insisting until others give way.
   Avoid: a crowd; a bank; a shop.

3. `ergens-klaar-mee-zijn.png` — Dutch chunk: ergens klaar mee zijn (to be done with something).
   Scene: One person stands and drops a plain folder into a bin with one hand, brushing the other hand flat against itself as they turn away.
   Must read: finished and refusing more.
   Avoid: a crowd; a bank; a shop.

4. `op-de-tong-liggen.png` — Dutch chunk: op de tong liggen (to be on the tip of one's tongue).
   Scene: One person stands with one finger raised and eyes narrowed, mouth slightly open, as if about to speak; a second figure waits with both hands open.
   Must read: almost remembering.
   Avoid: a crowd; a bank; a shop.

5. `met-de-noorderzon-vertrekken.png` — Dutch chunk: met de noorderzon vertrekken (to disappear without a trace).
   Scene: One person walks away through an open door with a plain bag, and the room behind is completely bare apart from an upturned chair.
   Must read: gone without a word.
   Avoid: a crowd; a bank; a shop.

6. `weer-op-de-proppen-komen.png` — Dutch chunk: weer op de proppen komen (to turn up again).
   Scene: One person steps back in through the same doorway with the same plain bag, one hand raised in a small wave; the chair is still upturned.
   Must read: reappearing.
   Avoid: a crowd; a bank; a shop.

7. `niet-voldoen-aan-de-verwachtingen.png` — Dutch chunk: niet voldoen aan (not to meet).
   Scene: One person holds up a small plain plate with a single flat, unremarkable shape on it towards a second figure whose shoulders drop and whose one open hand sinks; a third figure looks away.
   Must read: falling short of what was hoped.
   Avoid: a crowd; a bank; a shop.

8. `op-de-tocht-zijn.png` — Dutch chunk: op de tocht zijn (to be ajar, to be drafty).
   Scene: One person stands in a room with a small doorway left open at the edge; a row of plain draught strokes curves in from the gap towards their ankles.
   Must read: cold air from an open gap.
   Avoid: a crowd; a bank; a shop.

9. `er-met-de-pet-naar-gooien.png` — Dutch chunk: er met de pet naar gooien (to do a sloppy job).
   Scene: One person paints a plain wall with a roller held only by the fingertips, head turned away; the painted area has a ragged lower edge.
   Must read: hasty, careless work.
   Avoid: a crowd; a bank; a shop.

10. `aan-de-bak-zijn.png` — Dutch chunk: aan de bak zijn (to have one's work cut out).
   Scene: One person stands behind a counter stacked with plain boxes on both sides, both hands already full, looking at one more box on the floor.
   Must read: work piles up.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and 2 share a table and a pair of seated figures: relaxed with a cup, then leaned on with chin forward. Keep the chairs pushed back only in subject 2.
Four and five are a doorway pair: a figure walking out with a bag past an upturned chair, and the same figure stepping back with the same bag. The chair stays upturned in both.
Three and nine both involve paper or paint leaving marks: a folder dropped in a bin, and a roller with a ragged edge. The bin and the wall must not resemble each other.
Seven, eight and ten are singles: an unremarkable plate held up to a disappointed face, draught strokes from a gap, and a stack of boxes. Draught strokes must be short and curved, never arrows.
Ten is a single at a counter; keep the boxes lower than the figure's shoulders.

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

## Batch B2-17 — images 161–170

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

1. `de-verbeelding-te-boven-gaan.png` — Dutch chunk: de verbeelding te boven gaan (to be beyond imagining).
   Scene: One person stands with both hands raised open in front of a wide bright gap between two tall plain blocks, head tipped back, arms not reaching the top.
   Must read: more than one can take in.
   Avoid: a crowd; a bank; a shop.

2. `in-het-vage-blijven.png` — Dutch chunk: in het vage blijven (to remain vague).
   Scene: One person speaks with one hand open and low, the other held across the mouth, while a listener leans forward with a raised eyebrow.
   Must read: saying nothing clearly.
   Avoid: a crowd; a bank; a shop.

3. `aan-het-licht-brengen.png` — Dutch chunk: aan het licht brengen (to bring to light).
   Scene: One person holds a small plain lamp up above a table where an open folder lies, both hands steadying the lamp.
   Must read: making something visible.
   Avoid: a crowd; a bank; a shop.

4. `in-duigen-liggen.png` — Dutch chunk: in duigen liggen (to lie in ruins).
   Scene: One person stands before a low wall of plain blocks with a wide gap through it and two blocks fallen on the ground; the person has both hands out.
   Must read: everything fallen apart.
   Avoid: a crowd; a bank; a shop.

5. `met-huid-en-haar-overgeleverd.png` — Dutch chunk: met huid en haar overgeleverd (delivered entirely).
   Scene: One person sits with both feet up on a chair and both hands raised open, close to a large plain box that has its lid slightly raised.
   Must read: no way to hide any of it.
   Avoid: a crowd; a bank; a shop.

6. `stilstaan-bij-het-verleden.png` — Dutch chunk: stilstaan bij (to pause over, to dwell on).
   Scene: One person stands still in front of a plain wall panel with a single old plain photograph hanging on it, both hands at the sides and the head slightly lowered.
   Must read: stopping to dwell on something past.
   Avoid: a crowd; a bank; a shop.

7. `in-het-stof-bijten.png` — Dutch chunk: in het stof bijten (to bite the dust).
   Scene: One person lies on the floor on one elbow, head low, a small plain puff of dust drawn as short arcs at the elbow and knee.
   Must read: defeat on the ground.
   Avoid: a crowd; a bank; a shop.

8. `een-loden-last-met-zich-meedragen.png` — Dutch chunk: met zich meedragen (to carry with one).
   Scene: One person walks with a large plain sack on the back and both hands on the straps, neck bent; the sack is the biggest shape in the image.
   Must read: a burden that comes along.
   Avoid: a crowd; a bank; a shop.

9. `op-de-loer-liggen.png` — Dutch chunk: op de loer liggen (to lurk).
   Scene: One person crouches behind the edge of a low plain wall with only the top of the head and one hand visible above it.
   Must read: waiting out of sight.
   Avoid: a crowd; a bank; a shop.

10. `opscheppen-over-de-prestatie.png` — Dutch chunk: opscheppen over (to boast about).
   Scene: One person stands on a plain chair with both arms raised, one hand pointing at a small plain cup on a shelf, while a second figure below stands with folded arms and shakes their head.
   Must read: showing off in front of others.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are a face-to-face pair with raised hands: an idea above reach, and a hand over the mouth. Keep subject 1's hands wide and open, subject 2's low and closed.
Three, four and ten are all things being revealed or held up around a table: a lamp over a folder, a broken wall, and a small cup on a shelf. Only one lamp per image; subject 10's cup stays on the shelf.
Five and six are stillness: a chair and an open box, and a figure standing before a hanging photograph. The clock shape may not appear in this batch.
Seven and 9 share the floor and the low edge: a figure on one elbow, and a figure crouched behind a wall. Different heights.
Eight and the earlier burden frame use a sack; here the sack is the only way the person appears at all; keep the head low.

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

## Batch B2-18 — images 171–180

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

1. `over-de-schreef-gaan.png` — Dutch chunk: over de schreef gaan (to cross the line).
   Scene: One person steps over a painted straight line on a wide floor, one foot across and the other still behind, both hands held low.
   Must read: going beyond what is allowed.
   Avoid: a crowd; a bank; a shop.

2. `in-iemands-schaduw-staan.png` — Dutch chunk: in iemands schaduw staan (to be in someone's shadow).
   Scene: One person stands directly behind another and is drawn smaller and half hidden by the first person's outline; the front figure is bright and upright.
   Must read: less seen than another.
   Avoid: a crowd; a bank; a shop.

3. `vastlopen-in-het-gesprek.png` — Dutch chunk: vastlopen in (to get stuck in).
   Scene: One person speaks with one hand raised, then stops mid-gesture with the hand frozen and a flat mouth, stuck; a listener waits with both hands open.
   Must read: losing the sense of what was said.
   Avoid: a crowd; a bank; a shop.

4. `uiting-geven-aan-de-gevoelens.png` — Dutch chunk: uiting geven aan (to give expression to).
   Scene: One person stands with both hands pressed flat on the chest and the head tilted back, mouth open in one sustained sound, while two listeners stand still and face them.
   Must read: giving feelings a voice.
   Avoid: a crowd; a bank; a shop.

5. `op-een-keerpunt-staan.png` — Dutch chunk: op een keerpunt staan (to be at a turning point).
   Scene: One person stands where a wide path splits into two, one fork rising and one falling, both hands at the sides.
   Must read: the moment before a choice changes everything.
   Avoid: a crowd; a bank; a shop.

6. `in-de-schaduw-van-het-verleden-leven.png` — Dutch chunk: in de schaduw van het verleden leven (to live in the shadow of the past).
   Scene: One person sits with an old plain photograph held in both hands, the head lowered, in a room where a large plain block stands behind the chair.
   Must read: the past hanging over the present.
   Avoid: a crowd; a bank; a shop.

7. `afgeven-op-een-collega.png` — Dutch chunk: afgeven op (to run someone down).
   Scene: One person stands with the head tilted towards a second figure and one hand raised flat, speaking with a hard mouth, while a third figure in the background turns away with lowered shoulders.
   Must read: running someone down behind their back.
   Avoid: a crowd; a bank; a shop.

8. `door-het-oog-van-de-naald-kruipen.png` — Dutch chunk: door het oog van de naald kruipen (to scrape through).
   Scene: One person crawls on both knees through a narrow gap between two plain tall blocks, body squeezed small; the gap is barely wider than the shoulders.
   Must read: just getting through.
   Avoid: a crowd; a bank; a shop.

9. `te-genade-vallen-bij-het-nageslacht.png` — Dutch chunk: te genade vallen bij (to fall into the mercy of).
   Scene: One person sits on the floor with the head bowed and both palms turned up on the knees, in front of a raised plain bench with no one on it.
   Must read: at someone else's mercy.
   Avoid: a crowd; a bank; a shop.

10. `afstappen-van-het-oude-plan.png` — Dutch chunk: afstappen van (to abandon).
   Scene: One person turns a large plain wheel with both hands, then steps away from it towards an open doorway; a plain floor line runs behind, and an old folded sheet lies on the floor where they stood.
   Must read: leaving the old course behind.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are a painted line and an outline behind: a step over the line, and a smaller figure half hidden. Neither may show a cast shadow on the floor.
Three and nine are a stopped voice and a fallen posture: a hand frozen mid-gesture, and a bowed figure in front of an empty bench. Keep them in different rooms.
Four, six and ten are singles with a body or a heavy object: a figure with both hands on the chest, a block behind a chair, and a big wheel. The block behind the chair must not be mistaken for the wheel.
Five is the two paths: keep the split flat and wide. Seven is a turned shoulder and a hard mouth; no stone anywhere.
Eight is a single; the gap must be visibly narrower than the shoulders.

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

## Batch B2-19 — images 181–190

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

1. `behalve-de-uitzondering.png` — Dutch chunk: behalve (except).
   Scene: One person pushes a row of five plain blocks across a table and lifts one block out of the line, setting it apart at the end.
   Must read: one thing left out.
   Avoid: a crowd; a bank; a shop.

2. `met-inbegrip-van-de-toeslag.png` — Dutch chunk: met inbegrip van (including).
   Scene: One person places one more plain block onto the same row so that six blocks sit evenly together, hands still on the last one.
   Must read: one thing counted in.
   Avoid: a crowd; a bank; a shop.

3. `sinds-de-aanvang-van-het-project.png` — Dutch chunk: sinds (since).
   Scene: One person draws a plain ruled line across a sheet with a small upright stroke at its start, pen resting at the line's end.
   Must read: measured from a starting point.
   Avoid: a crowd; a bank; a shop.

4. `tijdens-de-vakantie.png` — Dutch chunk: tijdens (during).
   Scene: One person sits on a plain chair with a folded coat over the knees and an open suitcase beside them, both hands relaxed.
   Must read: while something else is happening.
   Avoid: a crowd; a bank; a shop.

5. `volgens-de-afspraak.png` — Dutch chunk: volgens (according to).
   Scene: One person holds a blank sheet in one hand and lays the other flat beside a plain block on a table, aligning the block with the sheet's edge.
   Must read: going by what was agreed.
   Avoid: a crowd; a bank; a shop.

6. `wegens-de-weersomstandigheden.png` — Dutch chunk: wegens (because of).
   Scene: One person holds a folded plain tarp in both hands and looks up at three small cloud shapes, a second figure already carrying a crate towards a door.
   Must read: an official reason for doing something.
   Avoid: a crowd; a bank; a shop.

7. `ondanks-de-tegenslag-doorgaan.png` — Dutch chunk: ondanks (despite).
   Scene: One person steps forward with the body tipped into the stride, past a small plain block fallen on the floor, both hands steadying a crate.
   Must read: going on anyway.
   Avoid: a crowd; a bank; a shop.

8. `behalve-als-het-regent.png` — Dutch chunk: behalve als (unless).
   Scene: One person stands in an open doorway with one foot in and one out, looking back at a small row of cloud shapes on the horizon.
   Must read: an exception to the exception.
   Avoid: a crowd; a bank; a shop.

9. `binnen-de-gestelde-termijn.png` — Dutch chunk: binnen (within).
   Scene: One person lays a blank form into a shallow tray with one hand while the other rests on a wall clock shape with tick marks.
   Must read: inside the allowed time.
   Avoid: a crowd; a bank; a shop.

10. `buiten-de-openingstijden.png` — Dutch chunk: buiten (outside).
   Scene: One person stands before a closed door with one hand flat on it and the other holding a small plain form, shoulders lowered.
   Must read: after the place has shut.
   Avoid: a crowd; a bank; a shop.

CONTRAST PAIRS
One and two are the same row of blocks and the same table: one lifted out, one added. Keep the blocks identical in size and shape.
Three, five and nine all use a ruled line or a form: a stroke at the start of a line, a block aligned with a sheet edge, and a form laid in a tray with a clock. The ruled stroke must appear only in subject 3.
Four, six, seven and ten are periods and obstacles: a suitcase and a coat, a tarp with cloud shapes, a fallen block with a stride, and a closed door with a form. No frame may show a sign with words or numbers.
Eight is a single; the figure is half in and half out of the doorway with a hand on the frame.

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

## Batch B2-20 — images 191–200

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

1. `zich-richten-op-het-doel-van-de-les.png` — Dutch chunk: zich richten op (to focus on).
   Scene: One person stands at the front of a plain empty room with both hands raised in a small ring in front of the eye, looking through it at one upright post drawn small in the distance.
   Must read: aiming attention at one thing.
   Avoid: a row of seated learners; a board with marks; a phone.

2. `omgaan-met-tegenslag.png` — Dutch chunk: omgaan met (to deal with).
   Scene: One person sits with elbows on a table and the head lowered onto one hand, while the other hand flattens a crumpled plain sheet against the table.
   Must read: handling a set-back.
   Avoid: a crowd; a bank; a shop.

3. `afhankelijk-zijn-van-goedkeuring.png` — Dutch chunk: afhankelijk zijn van (to depend on).
   Scene: One person holds a blank form out with both hands towards a seated figure who has a pen lifted over it but has not signed.
   Must read: waiting on someone's decision.
   Avoid: a crowd; a bank; a shop.

4. `verantwoordelijk-zijn-voor-de-naleving.png` — Dutch chunk: verantwoordelijk zijn voor (to be responsible for).
   Scene: One person stands at an open doorway with one hand flat on the frame, watching two figures inside work at a table.
   Must read: answerable for what others do.
   Avoid: a crowd; a bank; a shop.

5. `een-beroep-doen-op-het-geduld.png` — Dutch chunk: een beroep doen op (to call on).
   Scene: One person stands with both hands open and slightly cupped towards a second figure who already has both hands on a heavy crate.
   Must read: asking others to give more.
   Avoid: a crowd; a bank; a shop.

6. `zich-beroepen-op-de-afspraak.png` — Dutch chunk: zich beroepen op (to invoke).
   Scene: One person holds a blank sheet in one hand and taps one corner of it with the other hand, facing a listener who leans back.
   Must read: pointing to what was agreed.
   Avoid: a crowd; a bank; a shop.

7. `beschikken-over-de-benodigde-middelen.png` — Dutch chunk: beschikken over (to have at one's disposal).
   Scene: One person stands beside a plain bench with three closed plain boxes in a row and turns both open palms down above them.
   Must read: having what is needed.
   Avoid: a crowd; a bank; a shop.

8. `in-aanmerking-komen-voor-kwijtschelding.png` — Dutch chunk: in aanmerking komen voor (to be eligible for).
   Scene: One person sits at a counter with a blank form in both hands while a clerk leans over with a pen and draws a short line across one part of it.
   Must read: meeting the condition for something.
   Avoid: a crowd; a bank; a shop.

9. `met-inachtneming-van-de-afspraken.png` — Dutch chunk: met inachtneming van (subject to, in observance of).
   Scene: One person carries a plain crate towards an open doorway while pressing a single blank sheet against it with one hand.
   Must read: keeping to what was agreed while working.
   Avoid: a crowd; a bank; a shop.

10. `gebaseerd-zijn-op-de-cijfers.png` — Dutch chunk: gebaseerd zijn op (to be based on).
   Scene: One person sets a small tower of three plain blocks squarely onto a thick stack of blank sheets on the desk and steps back, both hands open at the sides.
   Must read: a structure resting on its base.
   Avoid: a tumbling tower; a person building at height; marks on the stack.

CONTRAST PAIRS
One, two and three are single figures with one object each: a hand ring aimed at a distant post, a head lowered onto a hand over a crumpled sheet, and a blank form held towards a pen. Keep the three rooms unrelated.
Four and five are a doorway and asking hands: a hand flat on a frame with two workers inside, and two hands cupped and raised. Do not merge the doorway into subject 5.
Six, seven and eight all involve a blank sheet at a table or counter, and none may repeat another's pose: a corner tapped, three closed boxes with palms turned down, and a clerk drawing a line.
Nine and ten close the batch with a crate carried through a door, and a block tower set on a stack of sheets before stepping away. No frame may show letters, numbers, a seal or a screen.

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

## Batch B2-21 — images 201–210

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

1. `zonder-jas-de-deur-uit.png` — Dutch chunk: zonder (without).
   Scene: One person strides out through an open doorway with bare arms and nothing held, while a plain coat still hangs on a hook on the wall behind them.
   Must read: gone out lacking something that stays behind.
   Avoid: a person wearing a coat; a closed door; a person leaving angry.

2. `het-zonder-de-auto-stellen.png` — Dutch chunk: het zonder … stellen (to do without).
   Scene: One person turns their back on a parked plain car and wheels a bicycle away by the handlebars, one palm raised towards the car as if declining it.
   Must read: managing without something that is available.
   Avoid: a broken-down car; a bicycle race; a person walking away from a crash.

3. `vanwege-de-drukte.png` — Dutch chunk: vanwege (because of).
   Scene: One person stops at the doorway of a room packed with small figure masses, one hand raised, and turns back with the body half away.
   Must read: a visible cause that makes someone turn back.
   Avoid: a bus queue; a concert; a person pushing through.

4. `gezien-de-omstandigheden.png` — Dutch chunk: gezien (in view of).
   Scene: One person stands over a plain crate tipped on its side with three blocks spilled across the floor, looking down and lowering one flat hand towards the spill, while a second figure waits in the doorway with a bag.
   Must read: calling something off once the state of things is seen.
   Avoid: a doorway full of people (that is subject 3); a person clearing up the spill; an angry face.

5. `richting-de-uitgang.png` — Dutch chunk: richting (towards).
   Scene: One person walks mid-stride along a bare corridor drawn as two converging lines, body tipped forward, towards a small open doorway far ahead.
   Must read: heading in a direction, not yet arrived.
   Avoid: a person standing in the doorway; a finish line; a signpost.

6. `per-post-versturen.png` — Dutch chunk: per (by, by means of).
   Scene: One person slides a plain blank envelope into the slot of a squat pillar box, the flap of the envelope half inside, the other hand open at the side.
   Must read: sending by one particular channel.
   Avoid: a courier van; a counter with a parcel; a screen.

7. `aangaande-de-aanvraag.png` — Dutch chunk: aangaande (concerning).
   Scene: At a counter, a clerk holds one plain folder upright, lifted from a drawer, while a visitor holds a blank form out flat and points to it with the other hand; no pen in the frame.
   Must read: a spoken enquiry about one pending file.
   Avoid: a queue; a person signing; a filing room.

8. `betreffende-de-wijziging.png` — Dutch chunk: betreffende (regarding).
   Scene: One person at a desk holds a pen above a sheet on which one short line is struck through and a new short line sits beside it, a second sheet clipped to the corner.
   Must read: a written note about one changed item.
   Avoid: a counter with a clerk; a stack of sheets; a person tearing paper.

9. `jegens-de-klant.png` — Dutch chunk: jegens (towards a person).
   Scene: One person pulls a plain chair out from a table with one hand and holds the other open towards it, body inclined, facing a second figure who carries a plain bag.
   Must read: courteous behaviour aimed at one person.
   Avoid: a handshake; a person arguing; a shop with prices.

10. `overeenkomstig-de-regels.png` — Dutch chunk: overeenkomstig (in accordance with).
   Scene: One person lays a plain stencil frame onto a board and runs a brush inside its edge, while an identical finished shape already sits beside it on the board.
   Must read: made to match a given pattern.
   Avoid: a block aligned with a sheet edge; a person measuring with a ruler; a mirror.

CONTRAST PAIRS
One and two are both an absence: a coat left on a hook behind a figure striding out, and a car left standing behind a figure wheeling a bicycle. The coat and the car stay the heaviest marks behind the figure.
Three and four are both reasons, kept apart by what is seen: a figure turning back at a doorway full of masses, and a figure looking down at a tipped crate. Show no crowd in subject 4 and no spill in subject 3.
Five and six are direction and means: a stride down a corridor towards a far doorway, and an envelope slid into a pillar box. Subject 5 has no slot and subject 6 has no doorway.
Seven and eight are the near-synonyms of this batch and must not share a pose: seven is two people at a counter with a lifted folder and no pen, eight is one person at a desk with a struck-through line and a clip. The folder appears only in seven and the struck line only in eight.
Nine and ten are singles: a chair pulled out for a visitor, and a stencil beside the shape it produced.
No frame may show letters, numbers, a stamp with readable marks, an arrow or a sign with words.

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
batch are drawn, or set the partner field to a placeholder. Pairs cross between
batches (for example B2-02 subject 5 with B2-01 subject 1); the tracker note
names the partner file in each case, so draw those two batches together. A
partner that names a file which is not in this file sits in the previous band,
`prepositions-art-b1-plus.md` — the B1+-02 / B1+-01 and B1+-05 / B1+-04 pairs
are the examples — so draw that band first.
