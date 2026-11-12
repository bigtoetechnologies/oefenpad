# Voorzetselpaden — scene art

Pilot art briefs. The activity spec is `prepositions.md`; the code is
`prepositions-implementation.md`. The first ten images were enough to test the
meaning-first loop end to end; batches 2–4 take the set to fifty scenes and
thirty-three levels. Batch 4b is planned and would take it to sixty-seven
scenes and thirty-six levels.

The shared drawing rules are in `game-art.md`. This file lists what each scene
must show; that file says how it must be drawn. The generation prompts for each
batch are in `prepositions-art-prompts.md`.

Status: fifty images are drawn and in place — the first ten (batch 1), the next
ten (batch 2), the last ten of the pilot (batch 3) and the twenty A0–A2 frames
of batch 4. All fifty match their briefs.
Batch 3 is drawn with heavier, more solid masses than batches 1–2 and is not
literally in the brush line of the first set; it still reads at 64 px and no
scene was redrawn for it. Two batch-1 images are weaker and worth a redraw:
`denken-aan-persoon` reads as a portrait rather than a full scene, and
`eraan-denken-afspraak` has no cue that clearly separates it from `denken aan`
— the pair is meant to test the pronominal form, not a meaning contrast, so it
should not compete with the thought-bubble image.

Batch 4 is recorded in `prepositions-art-a0-a2.md`: twenty A0–A2 frames around
`tegen`, `door`, `uit` and `tot`, with supporting `aan`, `met`, `op` and `in`
frames. `zonder` is left out because `zonder + noun` is free prepositional use,
not a chunk. The later bands are in `prepositions-art-a2-plus.md` (A2+),
`prepositions-art-b1.md` (B1), `prepositions-art-b1-plus.md` (B1+) and
`prepositions-art-b2.md` (B2). All fifty scenes below are delivered; do not redraw
them.

Batch 4b is **drawn, not yet integrated**: sixteen frames that give existing
singles a partner and add two same-verb pairs plus one lone single. Its briefs
and prompts are in `prepositions-art-a2-pairs.md`. This file records only the
level composition, which that file decides.

## Where the files go

`assets/voorzetselpaden/<scene-id>.png`. Square was the plan; the delivered
set is portrait and is kept at that ratio so all fifty share one camera and one
scale — which matters most for the contrast pairs. Batch 1 arrived at
784 × 1168, batches 2 and 3 at 1152 × 1712, batch 4 mostly at 784 × 1168 with
`vallen-uit-tas` at 1152 × 1712; all ship at 512 × 763. See
"Delivered raster art" in `game-art.md` for how the files are prepared and drawn.
The untouched originals of batch 4 are in
`assets/verb-propositions/archived/04-a0-a2/`; the folder is grouped by batch,
see its `README.md`.

## Rules for every image

| Rule | Why |
|---|---|
| No text or numbers, ever | One art set serves every language; the sentence is drawn in HTML |
| One idea per image, still nameable at 64 px | It is a phone-sized tile |
| Cobalt ink on a transparent background | `game-art.md`; there is no white plate |
| No orange | Orange is only the active step or primary button |
| Bold brush-pen in cobalt, with dense directional hatching | `game-art.md`; match the three anchor scenes |
| No culture-specific symbols or Dutch souvenir imagery | The audience is international |
| Do not encode meaning in colour alone | The scene must carry the meaning |
| Let the scene span the width and touch a side edge, keeping paper at top and bottom | The sentence sits beside or below it |

## The frame rule (all six plans)

A frame must be a chunk that governs a preposition — a verb (`letten op`), an
adjective (`bang voor`), a noun (`zin in`) or a fixed idiom. Not a bare verb,
not a free adjunct (`zonder afspraak`), not a greeting (`tot ziens`). A
pronominal adverb counts, because it carries its preposition inside `er…`,
`daar…` or `waar…` (`erover nadenken`, `ergens naartoe`, `ergens klaar mee
zijn`); the roadmap budgets 40 such frames.

Beyond the pilot, the plans are `prepositions-art-a0-a2.md` (20 frames),
`prepositions-art-a2-pairs.md` (16), `prepositions-art-a2-plus.md` (80),
`prepositions-art-b1.md` (120), `prepositions-art-b1-plus.md` (250) and
`prepositions-art-b2.md` (210): 696 new frames, 726 with the thirty pilot
scenes.

When editing a plan:

- Keep the tracker row and its batch subject identical — both filename and
  chunk. A plan breaks when only one side is updated.
- Batch prompts use four-backtick fences; an unbalanced fence silently breaks
  the copy-paste block.
- Filenames are ASCII; chunk text keeps its diacritics. No duplicate filenames
  and no duplicate Scene cells.
- A “has a preposition?” scan is clean once `tegenover` and the pronominal forms
  are whitelisted.

The audit that established this, and the scripts to re-run the checks, are in
`archive/preposition-review-findings-2026-11-10.md`.

## The first ten

| # | File | Scene | Target chunk | Meaning | Contrast | Tests |
|---|---|---|---|---|---|---|
| 1 | `wachten-op-bus.png` | Person at a bus stop, looking at a watch | `wachten op` | to wait for | `wachten-voor-deur` | Baseline, fixed vs spatial |
| 2 | `wachten-voor-deur.png` | Person waiting outside a closed door | `wachten voor` | to wait in front of | `wachten-op-bus` | Fixed vs spatial |
| 3 | `denken-aan-persoon.png` | Person with a thought bubble containing a friend | `denken aan` | to think of | `denken-over-keuze` | Meaning, non-separable |
| 4 | `denken-over-keuze.png` | Person comparing two options | `denken over` | to think about / consider | `denken-aan-persoon` | Contrast |
| 5 | `uitkijken-naar-vakantie.png` | Person with a suitcase, smiling at a calendar | `uitkijken naar` | to look forward to | `uitkijken-voor-auto` | Meaning, separable |
| 6 | `uitkijken-voor-auto.png` | Child at the curb, car approaching | `uitkijken voor` | to watch out for | `uitkijken-naar-vakantie` | Contrast, separable |
| 7 | `praten-met-vriend.png` | Two people facing each other, talking | `praten met` | to talk with | `praten-over-huis` | Meaning |
| 8 | `praten-over-huis.png` | Two people talking about a house between them | `praten over` | to talk about | `praten-met-vriend` | Contrast |
| 9 | `ophouden-met-roken.png` | Person stubbing out a cigarette | `ophouden met` | to stop doing | — | Separable single |
| 10 | `eraan-denken-afspraak.png` | Person suddenly remembering an appointment | `eraan denken` | to remember it | `denken aan` (same meaning) | Pronominal form |

## Briefs — batch 1

### 1. `wachten-op-bus.svg`

**Scene.** One person at a simple bus stop, body angled toward the road, looking
at a watch or phone. A pole with a blank sign (no text), maybe a bench.

**Must read at 64 px.** Waiting; a bus stop; for a bus.

**Avoid.** A bus arriving or a person boarding — that shows the event, not the
waiting. Avoid a queue, which suggests waiting in line rather than waiting for a
vehicle.

**Supports.** `Ik wacht op de bus.` / `Wachten op de bus.`

**Contrast.** `wachten-voor-deur`. This is the idiomatic "wait for", not the
spatial "wait in front of".

**Mode.** Ontdek, Kies het beeld, Klopt de zin?, Bouw de zin.

### 2. `wachten-voor-deur.svg`

**Scene.** One person standing outside a closed door, arms crossed or leaning
against the wall, clearly waiting. A plain door with a handle and a blank
nameplate (no text), maybe a doormat. The person is outside, not inside.

**Must read at 64 px.** Waiting; in front of a door.

**Avoid.** A bus stop, a person walking through the door, a key in hand (that
suggests entering, not waiting). Avoid a queue.

**Supports.** `Ik wacht voor de deur.` / `Wachten voor de deur.`

**Contrast.** `wachten-op-bus`. This is the spatial "in front of", not the
idiomatic "wait for". It exists to make the `op` in `wachten op` visible.

**Mode.** Ontdek, Kies het beeld, Klopt de zin?, Bouw de zin.

### 3. `denken-aan-persoon.svg`

**Scene.** A person sitting or standing still, gazing into space, with a thought
bubble containing a simple face (a friend or partner). Maybe a phone in hand, but
the face is in the thought bubble, not on the screen.

**Must read at 64 px.** Thinking of a person.

**Avoid.** A speech bubble (that is talking), two options or a question mark
(that is `denken over`), a calendar with a reminder (that is `eraan denken`).

**Supports.** `Ik denk aan jou.` / `Ik denk aan mijn vriend.`

**Contrast.** `denken-over-keuze`.

**Mode.** Ontdek, Kies het beeld, Klopt de zin?, Bouw de zin.

### 4. `denken-over-keuze.svg`

**Scene.** A person at a table with two simple options side by side — two house
shapes, two holiday photos, or two paths. Hand on chin, comparing. The options
are objects, not people.

**Must read at 64 px.** Considering a choice.

**Avoid.** A thought bubble containing a person (that is `denken aan`), a
question mark alone (too vague), a speech bubble.

**Supports.** `Ik denk over de keuze.` / `We denken over het plan.`

**Contrast.** `denken-aan-persoon`.

**Mode.** Ontdek, Kies het beeld, Klopt de zin?, Bouw de zin.

### 5. `uitkijken-naar-vakantie.svg`

**Scene.** A person with a suitcase, smiling, looking at a wall calendar with one
day circled and a sun or plane icon. No numbers or letters: use a blank grid with
one marked square.

**Must read at 64 px.** Looking forward to a future holiday.

**Avoid.** A bus or plane actually leaving (that is departure, not anticipation),
a warning gesture, a sad face.

**Supports.** `Ik kijk uit naar de vakantie.` / `We kijken uit naar de zomer.`

**Contrast.** `uitkijken-voor-auto`.

**Mode.** All four, including Bouw de zin. This is the main separable example:
`uit` belongs at the end.

### 6. `uitkijken-voor-auto.svg`

**Scene.** A child at the edge of a road, a car approaching, an adult hand
pulling the child back or an adult making a warning gesture. A simple warning
triangle without text can sit in the scene if it does not become the main idea.

**Must read at 64 px.** Danger; watch out.

**Avoid.** A happy person looking at a car (that is `uitkijken naar`), a bus stop,
a traffic light with text.

**Supports.** `Kijk uit voor de auto!` / `We moeten uitkijken voor het verkeer.`

**Contrast.** `uitkijken-naar-vakantie`.

**Mode.** All four. This is the second half of the `uitkijken` contrast and a
second split example.

### 7. `praten-met-vriend.svg`

**Scene.** Two people facing each other, both with speech bubbles that meet or
overlap, relaxed posture. Maybe a table between them, but no object that is the
topic of the conversation.

**Must read at 64 px.** A conversation with someone.

**Avoid.** One person alone, a phone (that is `bellen`), a house or object
between them (that is `praten over`).

**Supports.** `Ik praat met mijn vriend.` / `Zij praat met de buurman.`

**Contrast.** `praten-over-huis`.

**Mode.** Ontdek, Kies het beeld, Klopt de zin?, Bouw de zin.

### 8. `praten-over-huis.svg`

**Scene.** Two people at a table with a house, a photo of a house or a simple
blueprint between them. Speech bubbles point at the house; one person gestures
toward it.

**Must read at 64 px.** Talking about a topic or object.

**Avoid.** Two people just facing each other with no topic (that is
`praten met`), a person alone, a phone.

**Supports.** `We praten over het huis.` / `Zij praten over de plannen.`

**Contrast.** `praten-met-vriend`.

**Mode.** Ontdek, Kies het beeld, Klopt de zin?, Bouw de zin.

### 9. `ophouden-met-roken.svg`

**Scene.** A person stubbing out a cigarette in an ashtray, or holding up a hand
to refuse a cigarette, calm and determined. A packet of cigarettes can be put
away, but with no branding or text. A crossed-out cigarette symbol is allowed if
it stays wordless.

**Must read at 64 px.** Stopping smoking.

**Avoid.** A person smoking happily (that is the opposite), a "no smoking" sign
with letters, a doctor or a lecture.

**Supports.** `Ik hou op met roken.` / `Zij houdt op met roken.`

**Contrast.** None in the pilot. Use it in Ontdek, Kies het beeld and Bouw de
zin; skip `Klopt de zin?` until it has a partner.

**Note.** `ophouden` is separable, so `op` goes to the end. This is a second
split example beyond `uitkijken`, and it does not repeat the same prefix.

### 10. `eraan-denken-afspraak.svg`

**Scene.** A person with a hand to the forehead or a raised finger, sudden
recall. A phone or calendar with a bell or reminder icon nearby; maybe a clock.
No text or numbers.

**Must read at 64 px.** Remembering an appointment, "oh, I must remember".

**Avoid.** A thought bubble containing a person (that is `denken aan`), two
options or a question mark (that is `denken over`), a speech bubble.

**Supports.** `Ik denk eraan.` / `Ik moet eraan denken.` It also supports
`Ik denk aan de afspraak.`

**Related form.** `denken aan`, same meaning, pronoun form. This is not a meaning
contrast; it is the pronominal transformation.

**Mode.** Ontdek, Klopt de zin?, Hetzelfde of anders?, Krimp and the pronominal
step of Bouw de zin.

## Batch 2 — the next ten

Delivered at 1152 × 1712 and processed to the same 512 × 763 masks as batch 1.
These add seven levels: `werken`, `klaar` and `vragen` are contrast pairs;
`zorgen`, `meedoen`, `zoeken` and `last hebben` are single frames. The singles
carry a second `bouw` sentence so each still has three scored answers.

| # | File | Scene | Target chunk | Meaning | Contrast |
|---|---|---|---|---|---|
| 11 | `werken-bij-bedrijf.png` | Person at a counter in front of a company building, badge on | `werken bij` | to work at | `werken-aan-project` |
| 12 | `werken-aan-project.png` | Person leaning over a table with a large drawing or blueprint | `werken aan` | to work on | `werken-bij-bedrijf` |
| 13 | `klaar-met-werk.png` | Person leaning back, hands behind the head, laptop closed, tidy desk | `klaar met` | done with | `klaar-voor-feest` |
| 14 | `klaar-voor-feest.png` | Person at the front door in a coat, holding a gift, ready to leave | `klaar voor` | ready for | `klaar-met-werk` |
| 15 | `vragen-aan-persoon.png` | One person leaning in, hand raised, one speech bubble toward a listener | `vragen aan` | to ask a person | `vragen-om-hulp` |
| 16 | `vragen-om-hulp.png` | One person asking; the other hands over a bag or box | `vragen om` | to ask for | `vragen-aan-persoon` |
| 17 | `zorgen-voor-kind.png` | Adult helping a child into a coat, school bag in hand | `zorgen voor` | to care for | — |
| 18 | `meedoen-met-team.png` | Person pulling a chair up to a group at a table or board game | `meedoen met` | to join in | — |
| 19 | `zoeken-naar-sleutels.png` | Person kneeling to look under a bench; keys on the floor, hand reaching | `zoeken naar` | to search for | — |
| 20 | `last-hebben-van-lawaai.png` | Person covering their ears at a wall; a drill on the other side | `last hebben van` | to be bothered by | — |

The per-image briefs and the generation prompt are in
`prepositions-art-prompts.md` under *Batch 2*.

## Batch 3 — the last ten

Delivered at 1152 × 1712 and processed to the same 512 × 763 masks. These add
six levels: `blij`, `boos` and `klagen` are contrast pairs; `houden van`,
`zin in` and `bang voor` are single frames with a second `bouw` sentence.
`vragen naar` completes the `vragen` level from batch 2, which becomes a set of
three: the Kies stop offers three scenes and Klopt has six items. Its `contrast`
points at `vragen-aan` one way only, because `vragen-aan` and `vragen-om` are
already each other's partner.

| # | File | Scene | Target chunk | Meaning | Contrast |
|---|---|---|---|---|---|
| 21 | `blij-met-cadeau.png` | Person holding a ribboned gift box, delighted | `blij met` | happy with | `blij-voor-vriend` |
| 22 | `blij-voor-vriend.png` | Person beaming at a friend who holds up a small trophy | `blij voor` | happy for | `blij-met-cadeau` |
| 23 | `boos-op-collega.png` | Person pointing angrily at another, who leans back | `boos op` | angry at | `boos-over-rommel` |
| 24 | `boos-over-rommel.png` | Person glaring at scattered papers and a cracked cup | `boos over` | angry about | `boos-op-collega` |
| 25 | `klagen-over-apparaat.png` | Person at a broken washing machine, finger raised | `klagen over` | to complain about | `klagen-bij-balie` |
| 26 | `klagen-bij-balie.png` | Person leaning over a service desk, complaining at the clerk | `klagen bij` | to complain to | `klagen-over-apparaat` |
| 27 | `houden-van-hond.png` | Person hugging a calm dog, both relaxed | `houden van` | to love | — |
| 28 | `zin-in-koffie.png` | Person looking happily at a coffee cup and a slice of cake | `zin in` | to feel like | — |
| 29 | `bang-voor-hond.png` | Person recoiling from a barking dog, hands raised | `bang voor` | afraid of | — |
| 30 | `vragen-naar-informatie.png` | Person at a counter pointing at a blank map; clerk listening | `vragen naar` | to ask about | `vragen-aan-persoon` (one way) |

The per-image briefs and the generation prompt are in
`prepositions-art-prompts.md` under *Batch 3*.

## Batch 4 — completing A0–A2

Delivered at 784 × 1168, except `vallen-uit-tas` at 1152 × 1712, and processed
to the same 512 × 763 masks. These add fifteen levels: four contrast pairs
(`zeggen`, `beschermen`, `kijken`, `bedanken`), eleven singles, and
`praten-tegen` completes the `praten` level from batch 1, which becomes a set of
three. `praten-tegen` contrasts with `praten-met` one way only; `praten-over`
keeps its own partner.

| # | File | Scene | Target chunk | Meaning | Contrast |
|---|---|---|---|---|---|
| 31 | `zeggen-tegen-persoon.png` | Person leans in and says one short thing to another | `zeggen tegen` | to say to | `vertellen-aan-kind` |
| 32 | `vertellen-aan-kind.png` | Adult tells a longer story to a child, hands moving | `vertellen aan` | to tell to | `zeggen-tegen-persoon` |
| 33 | `praten-tegen-muur.png` | Person talks at someone whose back is turned | `praten tegen` | to talk at | `praten-met-vriend` (one way) |
| 34 | `beschermen-tegen-regen.png` | Person dry under an umbrella in slanting rain | `beschermen tegen` | to protect against | `komen-door-regen` |
| 35 | `komen-door-regen.png` | Soaked person points at the rain, no umbrella | `komen door` | to be caused by | `beschermen-tegen-regen` |
| 36 | `komen-uit-huis.png` | Person with a suitcase steps out of a house door | `komen uit` | to come from | — |
| 37 | `kijken-door-sleutelgat.png` | Person peers through a keyhole | `kijken door` | to look through | `kijken-uit-raam` |
| 38 | `kijken-uit-raam.png` | Person looks out of an open window | `kijken uit` | to look out of | `kijken-door-sleutelgat` |
| 39 | `doorgeven-aan-buur.png` | Person hands a plain box to another over a fence | `doorgeven aan` | to pass on to | — |
| 40 | `doorbrengen-met-vriend.png` | Two people relaxed on a sofa, one reading, one with a cup | `doorbrengen met` | to spend time with | — |
| 41 | `stappen-uit-bus.png` | Person stepping down from a bus, one foot on the pavement | `stappen uit` | to get out of | — |
| 42 | `drinken-uit-glas.png` | Person tilting a glass to drink | `drinken uit` | to drink from | — |
| 43 | `vallen-uit-tas.png` | Open bag tipped over, a book and an apple falling out | `vallen uit` | to fall out of | — |
| 44 | `letten-op-verkeer.png` | Person at the edge of a road, hand shading the eyes | `letten op` | to pay attention to | — |
| 45 | `bezig-zijn-met-klus.png` | Person over a workbench fitting a wheel onto an axle | `bezig zijn met` | to be busy with | — |
| 46 | `geinteresseerd-in-onderwerp.png` | Person bent over a book at a table | `geïnteresseerd zijn in` | to be interested in | — |
| 47 | `tevreden-zijn-met-resultaat.png` | Person standing back from a finished panel, calm approval | `tevreden zijn met` | to be satisfied with | — |
| 48 | `bedanken-voor-de-uitnodiging.png` | Two people at a doorway, one holding out an open hand in thanks | `bedanken voor` | to thank for | `feliciteren-met-de-verjaardag` |
| 49 | `feliciteren-met-de-verjaardag.png` | Same two people; one holds out a small wrapped box | `feliciteren met` | to congratulate on | `bedanken-voor-de-uitnodiging` |
| 50 | `uitnodigen-voor-het-feest.png` | Person holds out a blank card; the other reaches for it | `uitnodigen voor` | to invite to | — |

The per-image briefs and the generation prompts are in
`prepositions-art-a0-a2.md`.

## Batch 4b — A2 pair enhancement (drawn)

Drawn 10 November 2026, not yet integrated. Sixteen frames, all in
`prepositions-art-a2-pairs.md`, which holds the scene briefs, the prompts and
the caveats. The point of the batch is that
**ten shipped singles become pairs**, so the Klopt step gains a real choice at
no cost to the partner scene. Two new same-verb pairs (`betalen`, `rekenen`) and
one lone single (`kiezen voor`) complete the set. `kiezen tussen` was briefed,
drawn and cut — see that file.

| Level | Frames after 4b | Change |
|---|---|---|
| `betalen` | `betalen voor`, `betalen met` | new pair |
| `kiezen` | `kiezen voor` | new single |
| `rekenen` | `rekenen op`, `rekenen met` | new pair |
| `stappen` | `stappen uit` **+ `stappen in`** | single → pair |
| `ophouden` | `ophouden met` **+ `beginnen met`** | single → pair |
| `meedoen` | `meedoen met` **+ `meespelen met`** | single → pair |
| `bang` | `bang voor` **+ `trots op`** | single → pair |
| `geïnteresseerd` | `geïnteresseerd in` **+ `geloven in`** | single → pair |
| `last hebben` | `last hebben van` **+ `genieten van`** | single → pair |
| `komen` | `komen uit` **+ `gaan naar`** | single → pair |
| `zorgen` | `zorgen voor` **+ `zorgen om`** | single → pair |
| `letten` | `letten op` **+ `passen op`** | single → pair |
| `doorgeven` | `doorgeven aan` **+ `krijgen van`** | single → pair |
| `kijken` | `kijken door`, `kijken uit` **+ `kijken naar`** | pair → set of three |

That is 14 levels touched: three new, ten upgraded to pairs, one upgraded to a
set of three. Eleven of the sixteen new frames pair with art that already
exists; the other five are two same-verb pairs and one single.

`luisteren naar` is deliberately deferred — see the note in the plan file. A
further two verbs raised in review, `oversteken` and `afsnijden`, are separable
prefix verbs, not frames, and belong to the Uit Elkaar game; that file explains
the test.

## Review sheet

`tools/build-prepositions-sheet.py` renders every frame in
`prepositions.json` — image, chunk, gloss, example (NL/EN), build sentences,
concept question and contrast partner — to
`assets/site/prepositions-sheet.html`.

The page is fully static: each mask is composited to cobalt, downscaled to
320 × 477, quantised to 16 colours and embedded as a PNG `data:` URI, so there
is no `<script>`, no CSS `mask-image` and no reference to `assets/`. It opens by
double-clicking the file and prints at three columns (`Ctrl+P`). Re-run it after
any change to the JSON or the masks:

```sh
python3 tools/build-prepositions-sheet.py
```

`tools/build-prepositions-preview.py` writes the same page but appends the
batches that are drawn and not yet in `prepositions.json`, reading their PNGs
from the batch's folder under `assets/verb-propositions/` (archived batches keep
their own subfolder) and their rows from the batch plan. It imports the stock
builder for the shell, the CSS and the shipped cards, so the two sheets cannot
drift apart. Those cards have no example, build step or concept question yet, so
they show the gap instead of inventing the text, and each one carries a 64 px
strip with its contrast partner to check the pair.

```sh
python3 tools/build-prepositions-preview.py
```

Both write `assets/site/prepositions-sheet.html`, so the last one run wins: use
the preview while reviewing new art, the stock builder after a promotion.

Do not switch it back to CSS masks or linked image files: a failed mask load
hides the element, so a `file://` render comes out blank.

## What the pilot tests

| Mechanic | Images | Question it answers |
|---|---|---|
| Meaning recognition | 1–50 | Does the learner connect the chunk to a situation? |
| Meaning discrimination | 1/2, 3/4, 5/6, 7/8, 11/12, 13/14, 15/16, 21/22, 23/24, 25/26, 31/32, 34/35, 37/38, 48/49 | Does the preposition change the meaning? |
| Asking a person, a thing or for information | 15, 16, 30 | Does the learner separate `vragen aan`, `vragen om` and `vragen naar`? |
| Talking to, with or about | 7, 8, 33 | Does the learner separate `praten met`, `praten over` and `praten tegen`? |
| Production with a split | 5, 6, 9, 18 | Can the learner put the prefix in the right place? |
| Pronominal form | 10 | Can the learner switch to `eraan`? |
| Fixed vs free preposition | 1/2 | Is `voor` always a fixed chunk? |

## Definition of done for the pilot

- Thirty images at 512 × 763, cobalt ink on transparency, no text or numbers.
- Each image is readable at 64 px.
- A Dutch speaker can name the target sentence from the image alone, without the
  gloss.
- The contrast pairs are clearly different side by side, and neither image
  accidentally suggests the partner.
- The loop works without English: Ontdek → Kies het beeld → Klopt de zin? →
  Bouw de zin.
- The thirty images fit the six-minute session in `prepositions.md`.

## Not in this set

- `afhangen van` (hard to draw unambiguously at 64 px), `werken voor` (too
  close to `werken bij`) and `zoeken op` (separable `opzoeken`, a word-order
  item, not a frame).

- Audio. It is blocked by `decisions.md` open question 6.
- The noun `aandenken` ("souvenir"). It is a vocabulary card, not a frame. If it
  is wanted, it needs a souvenir-shop scene, not a preposition scene.
- A separate "wrong" version of any scene. The activity supplies the sentence;
  the art supplies the situation.

## Shared generation prompt

The prompt, negative rules and checklist are in `game-art.md`. Use that prompt
for every image, changing only the subject line to the scene above. This list
is the content spec; `game-art.md` is the style.

### One prompt for the first ten

Superseded in style by the locked header in `game-art.md`, which is what every
current batch uses. The ten subjects below are still the content spec for the
pilot and have been drawn; keep them as a record, not as a template. The
original block follows, with its style paragraph replaced.

> You are drawing a set of ten illustrations for a Dutch practice game about
> verbs with fixed prepositions. Work in the style of the three attached anchor
> images: bold brush-pen sketch, cobalt blue (#2B50C8) only on plain white, wide
> contours with white interiors, most lines 4–8 px at 784 px wide, dense
> directional hatching for shadow, hair as the only filled mass. One idea per
> image. Adult proportions, profile or three-quarter view, focused neutral face
> with a brow, one eye, a nose line, a mouth and an ear; hands with a thumb and
> finger lines. The scene spans 90–100% of the width and the person 35–55%, with
> one place cue and paper kept at top and bottom. No text, letters or numbers
> anywhere. No orange, no second blue, no grey, no gradients, no drop shadows,
> no frames, no white background plate, no Dutch souvenir imagery (windmills,
> clogs, tulips, canals, cheese). The audience is an adult newcomer to the
> Netherlands; the drawing is a clue, not a cartoon. Leave the background flat
> white and export 784 × 1168, 2:3 portrait.
>
> The ten subjects, in order:
>
> 1. One person at a simple bus stop, looking at a watch. A blank sign on a
>    pole, maybe a bench. No bus arriving.
> 2. One person waiting outside a closed door, arms crossed or leaning on the
>    wall. A plain door with a handle, blank nameplate. No key, nobody entering.
> 3. A person gazing into space with a thought bubble containing a simple face.
>    No speech bubble, no question mark, no calendar.
> 4. A person at a table comparing two simple objects side by side, hand on
>    chin. Objects, not people.
> 5. A smiling person with a suitcase looking at a wall calendar with one day
>    marked and a sun. No numbers or letters.
> 6. A child at the edge of a road with a car approaching and an adult hand
>    pulling the child back. One warning triangle at most, no readable signs.
> 7. Two people facing each other, talking, speech bubbles meeting. No object
>    between them, no phone.
> 8. Two people at a table with a simple house between them, speech bubbles
>    pointing at the house, one gesturing toward it.
> 9. A person stubbing out a cigarette in an ashtray, calm and determined. No
>    branded packet, no readable sign.
> 10. A person with a hand to the forehead and a raised finger, sudden recall,
>    with a phone or calendar showing a bell nearby.
>
> Deliver the ten as separate files named `wachten-op-bus`,
> `wachten-voor-deur`, `denken-aan-persoon`, `denken-over-keuze`,
> `uitkijken-naar-vakantie`, `uitkijken-voor-auto`, `praten-met-vriend`,
> `praten-over-huis`, `ophouden-met-roken`, `eraan-denken-afspraak`. Before you
> finish, check each one: a Dutch speaker can name the situation from the
> drawing alone, the idea is still nameable at 64 px, and each of the four
> contrast pairs (1/2, 3/4, 5/6, 7/8) is clearly different side by side —
> neither image may suggest the other's sentence. Also compare every image
> against the three anchors: if it would not pass unnoticed beside them, redraw
> it rather than patching it.
