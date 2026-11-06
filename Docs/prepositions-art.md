# Voorzetselpaden — first 10 images

Pilot art brief. The activity spec is `prepositions.md`. These ten images are
enough to test the meaning-first loop end to end: four contrast pairs, one
separable single and one pronominal scene. None are drawn yet.

## Where the files go

`src/voorzetselpaden/art/<scene-id>.svg`, mirroring the Story Machine convention
(`src/storymachine/art/<reel>/<tile>.svg`). The folder does not exist yet; create
it with the game. Square, 512 × 512, SVG.

## Rules for every image

| Rule | Why |
|---|---|
| No text or numbers, ever | One art set serves every language; the sentence is drawn in HTML |
| One idea per image, readable as a silhouette at 64 px | It is a phone-sized tile |
| Cobalt `#2B50C8` on white `#FFFFFF` | `designguide.md` |
| No orange | Orange is only the active step or primary button |
| Flat and bold, not photographic | Match the Story Machine tiles |
| No culture-specific symbols or Dutch souvenir imagery | The audience is international |
| Do not encode meaning in colour alone | The scene must carry the meaning |
| Leave breathing room around the scene | The sentence sits beside or below it |

## The ten

| # | File | Scene | Target chunk | Meaning | Contrast | Tests |
|---|---|---|---|---|---|---|
| 1 | `wachten-op-bus.svg` | Person at a bus stop, looking at a watch | `wachten op` | to wait for | `wachten-voor-deur` | Baseline, fixed vs spatial |
| 2 | `wachten-voor-deur.svg` | Person waiting outside a closed door | `wachten voor` | to wait in front of | `wachten-op-bus` | Fixed vs spatial |
| 3 | `denken-aan-persoon.svg` | Person with a thought bubble containing a friend | `denken aan` | to think of | `denken-over-keuze` | Meaning, non-separable |
| 4 | `denken-over-keuze.svg` | Person comparing two options | `denken over` | to think about / consider | `denken-aan-persoon` | Contrast |
| 5 | `uitkijken-naar-vakantie.svg` | Person with a suitcase, smiling at a calendar | `uitkijken naar` | to look forward to | `uitkijken-voor-auto` | Meaning, separable |
| 6 | `uitkijken-voor-auto.svg` | Child at the curb, car approaching | `uitkijken voor` | to watch out for | `uitkijken-naar-vakantie` | Contrast, separable |
| 7 | `praten-met-vriend.svg` | Two people facing each other, talking | `praten met` | to talk with | `praten-over-huis` | Meaning |
| 8 | `praten-over-huis.svg` | Two people talking about a house between them | `praten over` | to talk about | `praten-met-vriend` | Contrast |
| 9 | `ophouden-met-roken.svg` | Person stubbing out a cigarette | `ophouden met` | to stop doing | — | Separable single |
| 10 | `eraan-denken-afspraak.svg` | Person suddenly remembering an appointment | `eraan denken` | to remember it | `denken aan` (same meaning) | Pronominal form |

## Briefs

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

## What the pilot tests

| Mechanic | Images | Question it answers |
|---|---|---|
| Meaning recognition | 1–8, 10 | Does the learner connect the chunk to a situation? |
| Meaning discrimination | 1/2, 3/4, 5/6, 7/8 | Does the preposition change the meaning? |
| Production with a split | 5, 6, 9 | Can the learner put the prefix at the end? |
| Pronominal form | 10 | Can the learner switch to `eraan`? |
| Fixed vs free preposition | 1/2 | Is `voor` always a fixed chunk? |

## Definition of done for the pilot

- Ten SVGs at 512 × 512, cobalt on white, no text or numbers.
- Each image is readable at 64 px.
- A Dutch speaker can name the target sentence from the image alone, without the
  gloss.
- The contrast pairs are clearly different side by side, and neither image
  accidentally suggests the partner.
- The loop works without English: Ontdek → Kies het beeld → Klopt de zin? →
  Bouw de zin.
- The ten images fit the six-minute session in `prepositions.md`.

## Not in the first ten

- `afhangen van`, `zorgen voor`, `meedoen met`, `werken aan` / `voor` / `bij`,
  `zoeken naar` / `op`. These are good candidates for the next batch, but they
  add contrasts without testing a new mechanic.
- Audio. It is blocked by `decisions.md` open question 6.
- The noun `aandenken` ("souvenir"). It is a vocabulary card, not a frame. If it
  is wanted, it needs a souvenir-shop scene, not a preposition scene.
- A separate "wrong" version of any scene. The activity supplies the sentence;
  the art supplies the situation.

## Shared generation prompt

Use this for every image so the set stays consistent:

> Flat vector illustration for Oefenpad. White background (#FFFFFF), bold
> cobalt (#2B50C8) shapes, no other colours, no orange. One clear human
> situation, readable as a silhouette at 64 px. No text, no letters, no numbers,
> no logos, no gradients, no shadows, no photorealistic detail, no Dutch souvenir
> imagery. Square 512 × 512.
