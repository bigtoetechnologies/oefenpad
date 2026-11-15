# Game catalogue — learning goals, coverage and gaps

A goal-first view of the activity grid. `games.md` says **how** the first two games
are built; this says **what every game is for**, which learning goals the set
covers, and what is missing. `designguide.md` is canonical for the names, and it
matches the concept board — so this doc settles the naming conflict in
`games.md`: **Preposition Paths** and **Sentence Builder** are the names, not
Preposition Playground and Word Order Workshop. For what can be lifted from the
BigToe Games repo, see `reuse-bigtoegames.md`.

Two conventions used throughout:

- **R** = recognition (receptive), **P** = production (active use). A game can
  be R-only, P-only, or both.
- **English-free** = works for a learner who does not read English. This matters
  because `decisions.md` says most users will not, and the interface is Dutch.
  English glosses are a convenience, not the only route to meaning: a picture, or
  a Dutch headword the learner can look up in their own dictionary, also works.
  Design the clue so the game survives without the gloss.

Target level is A1 → B1, so most games should sit at recognition first and
production second; B1 adds idioms, longer texts and free output.

---

## The 13 planned games

| Game | Dutch name | Primary learning goal | Also trains | Mode | Pillar |
|---|---|---|---|---|---|
| Story Machine | Verhaalmachine | Spoken narrative: retrieve words and produce connected sentences aloud | Sentence patterns, pronunciation, creativity | P | 7 |
| Memory | Geheugen | Form–meaning recognition and recall | Spelling, pronunciation if audio is added | R → P | 1, 4, 8 |
| Match Up | Koppelen | Fast meaning recognition (word ↔ picture) | Automaticity, vocabulary | R | 1, 3 |
| Word Search | Woordzoeker | Recognising written word forms | Scanning, spelling exposure, word-form familiarity | R | any |
| Hangman | Galgje | Retrieving a word's spelling from a clue | Letter patterns, spelling, form recall | P | any |
| Preposition Paths | Voorzetselpaden | Fixed verb + preposition chunks **and their meaning** | Meaning discrimination, separable prefixes, chunk recall, sentence reading | R/P | 5 |
| Sentence Builder | Zinsbouwer | Dutch word order (V2, inversion, subclauses) | Verb form recognition, syntax | P | 7 |
| Ending Matcher | Uitgangsmatcher | English → Dutch ending rules and word formation | Vocabulary expansion, spelling | R/P | 2 |
| Lego Words | Lego-woorden | Word families, prefixes, diminutives | Vocabulary depth, morphology | P | 3 |
| False Friend Trap | Valse vrienden | Meaning accuracy against L1 lookalikes | Reading, vocabulary depth | R | 4 |
| Flashcards | Flitskaarten | Long-term retention through spaced retrieval | Anything in the deck | R/P | any |
| Fill the Gap | Vul de leegte | Grammar in context: supply the one missing word | Prepositions, verb form, collocations, reading | P | 5, 6, 7 |
| Listening Drill | Luisteroefening | Sound discrimination and listening perception | Sound–spelling mapping | R | 8 |

### Notes that change the design

- **Word Search and Hangman are vocabulary games when the clue carries meaning.**
  Searching for a word holds it in working memory and builds orthographic
  familiarity, which is real vocabulary practice — but meaning retrieval only
  happens when the clue is a picture or a gloss rather than the Dutch word
  itself. Prefer a picture shown with the word, or a picture-only word list, and
  let the learner look the word up in their own dictionary. A dictionary
  affordance also removes the need for an English gloss. End each round on
  meaning: show the picture, the word and the audio together. Hangman should
  correct a wrong letter immediately, or it teaches wrong spellings.
- **Ending Matcher is English-dependent.** Its premise is "turn English endings
  into Dutch equivalents", which needs English literacy — the same problem
  `decisions.md` flags for False Friend. For an English-free site, reframe it as
  Dutch-internal sorting (*which words share `-tie`, `-heid`, `-ing`?*) and keep
  the English→Dutch rule in the book. This is a Pillar 2 content question, not
  just a UI question.
- **False Friend Trap needs a first language** to supply the "friend". Keep it in
  the book, or make it an optional English-interface extra, per `decisions.md`.
- **Story Machine has no score by design** (`story-machine.md`). It is a speaking
  prompt, not a test. If it needs to show learning, add an optional target
  (*use one past-tense sentence*) and a self-check afterwards — not a score.
- **Sentence Builder checks against a table, not free text** (`games.md`). That
  is the right trade; it also means the verb table is the real work.
- **Listening Drill is blocked** on audio (`decisions.md` open question 6). Do not
  build listening UI before the audio exists.
- **Flashcards is only spaced repetition if the scheduler exists.** A flip deck
  without scheduling is just a deck. The review queue and the scheduling
  algorithm are the feature.
- **Fill the Gap is the cheapest grammar-in-context game**: one sentence, one
  gap, one answer, reused across prepositions, verb forms and collocations.
- **Preposition Paths is meaning-first.** The unit is a frame + scene + contrast
  partner (`uitkijken naar` vs `uitkijken voor`), not a verb + preposition pair.
  Matching alone tests recall of the pairing, not meaning; see `prepositions.md`.
- **Preposition Paths shipped as a pilot** in `client/src/games/prepositions/`:
  twenty-eight levels, one per chunk — ten A0 chunks and eighteen A1 chunks —
  each taught across two to four example scenes, ninety-one in all. Every level
  runs Ontdek → Kies het beeld → Bouw de zin, and adds Klopt de zin? when the
  chunk has a contrast partner in the data. A chunk with no partner skips it.
  The ninety-one scene images are delivered raster, not SVG; see
  `game-art.md`. How it is built is `prepositions-implementation.md`. `Krimp` and
  `Hetzelfde of anders?` are still unbuilt, and the pronominal form is shown as a
  line on the Ontdek card rather than as a step.

---

## What the set covers

Coverage is judged by whether a goal is trained with feedback, not by whether it
appears in a game's theme.

| Learning goal | Coverage | Where |
|---|---|---|
| Vocabulary: form–meaning recognition | Strong | Geheugen, Koppelen, Flitskaarten, Woordzoeker/Galgje (picture clues) |
| Vocabulary: active recall | Partial | Flitskaarten (reverse), Vul de leegte, Galgje (picture clue), Woordzoeker (picture-only list) |
| Vocabulary: depth (collocations, polysemy, false friends) | Partial | Vul de leegte, Valse vrienden |
| Word formation / morphology | Strong | Uitgangsmatcher, Lego-woorden |
| Spelling | Partial | Woordzoeker, Galgje — no dictation |
| Verb conjugation | **None** | Zinsbouwer assumes the forms; Vul de leegte only touches them |
| Articles, gender, plurals (de/het) | **None** | — |
| Word order / syntax | Strong | Zinsbouwer |
| Fixed prepositions / chunks | Strong | Voorzetselpaden (meaning + form), Vul de leegte |
| Pronunciation perception | **None today** | Luisteroefening specced, blocked on audio |
| Pronunciation production | **None** | — |
| Listening comprehension | Weak | Luisteroefening is perception only |
| Reading comprehension | Weak | Woordzoeker scans forms; no text + questions |
| Speaking / narrative | Partial | Verhaalmachine, no feedback |
| Interaction / conversation | **None** | — |
| Writing | **None** | — |
| Pragmatics, register, culture | **None** | — |
| Automaticity / speed | Partial | Koppelen, Galgje, Woordzoeker |
| Retention | Strong if the SRS exists | Flitskaarten |
| Error awareness | Weak | Games mark answers wrong but do not explain |

The pillar map is uneven in the same way: Pillar 6 (irregular/strong verbs) has
**no game at all**, and Pillar 8 (pronunciation) has a game that cannot be built
yet. Activity count is not coverage.

---

## What is missing

### 1. Verb conjugation — Pillar 6 is unserved

This is the biggest gap, and it is the user-facing example of a learning goal the
set claims. Nothing currently makes the learner produce *ik liep*, *wij hebben
gelopen*, or *zij wordt*. Sentence Builder deals pre-conjugated tiles, so it
tests order, not form.

**Candidate: Werkwoordtrainer** — show infinitive + subject + tense (or a picture
and a sentence frame), learner types or taps the form. Strong verbs get a
pattern-prediction round (`lopen → liep → gelopen`), then mixed. Add separable
prefixes (`opbellen → ik bel op`) as a level, because they break word order too.
Wrong forms return later in the session. Reuses the verb table Zinsbouwer already
needs, so it is cheap once that data exists.

### 2. Articles and gender — a high-frequency gap with tiny data

English speakers have no grammatical gender and get *de*/*het* wrong constantly.
No game covers it, and the pillars do not mention it.

**Candidate: De of het** — picture + noun → choose *de* or *het*; then the plural
(*het huis → de huizen*). Low effort, huge data value, no audio. It also feeds
every other game that needs a noun.

### 3. Conversation and interaction — a stated goal with zero coverage

Story Machine is a monologue prompt. Nothing trains turn-taking, choosing an
appropriate reply, or the *je/u* register.

**Candidates:**

- **Reageer** — a short dialogue; pick the natural reply, then type it. This is
  the text-only version of conversation practice and the cheapest to build.
  Feedback can be rule-based at first, AI-scored later (see `suggestions.md`).
- **Rollenspel** — branching dialogue (café, GP, gemeente, landlord), or an AI
  role-play once there is sign-in. Higher effort; the authentic version needs AI
  or a person.
- **Jij of u** — politeness/register choices. Small enough to be a level inside
  Reageer rather than its own game.

### 4. Reading real Dutch — signs, forms, letters, messages

The book's whole hook is "read this sign". The site has no reading game. Word
Search is visual scanning, not comprehension.

**Candidates:**

- **Lees & Kies** — a sign, menu, form, NS departure board or letter, plus one to
  three questions. Levels: gist → detail → inference. Strong inburgering
  relevance, text-only, no audio blocker.
- **Bericht** — a WhatsApp-style exchange; understand it and reply to it. This
  bridges reading and conversation.

Use original, copyright-safe texts; do not lift real forms or articles wholesale.

### 5. Writing and spelling from sound

Nothing asks the learner to write a sentence or spell a word they hear.

**Candidates:**

- **Dictee** — hear a word or short sentence, type it, replay, then see errors by
  category. The classic spelling/listening activity; needs audio.
- **Beschrijf het** — a picture; write one sentence. AI-scored or self-checked
  against a model. This is the writing counterpart to Story Machine.
- **Foutenspeurder** — one error per sentence; tap it, choose or type the fix,
  and see why. Text-only, and it reuses all the grammar data. It is also the
  cheapest way to train *noticing*, which games otherwise skip.

### 6. Listening beyond minimal pairs

The Listening Drill is sound discrimination. Real listening needs gist and
detail tasks at natural speed.

**Candidate: Luister & Kies** — a 10–30 second clip, one gist question, one detail
question, transcript on demand. Blocked on the same audio question.

### 7. Pronunciation production

The site can currently only test whether you *hear* a contrast, not whether you
can *say* it.

**Candidate: Nazeggen** — hear a model, record, compare, self-rate or get ASR
feedback. Needs audio, a microphone and a privacy decision. Until then, the book
and a tutor do this job.

### 8. Numbers, time, dates, money

A survival need at A1 that no pillar or game covers, and one of the few things a
learner needs in the first week.

**Candidate: Getallen & Tijd** — hear or see a number, time, date or price; type
the digits or choose the matching clock. Audio optional: a text-first version
works, and the audio version slots into the listening cluster later.

### 9. Vocabulary depth

Matching and gap-fill cover breadth, but not collocations, polysemy, idioms or
rapid retrieval.

**Candidates:**

- **Woordcombinaties** — which verb goes with which noun, or which adjective
  with which noun. Reuses sentence data.
- **Woordweb** — 60 seconds: pick (or type) every word in a category. Trains
  retrieval fluency and semantic networks.
- **Uitdrukkingen** — match an idiom to a scenario or meaning; B1 territory.

### 10. The connective tissue: a mistakes queue

Every game produces errors, and every game forgets them. The highest-value,
lowest-UI feature is a **Foutenlijst**: every miss from any activity goes into
the Flitskaarten queue, and "review your mistakes" becomes one button.

This is what turns thirteen separate drills into a system, and it is the feature
that justifies the SRS existing at all. It needs shared progress storage; local
storage is enough for the MVP, accounts are not.

---

## What games cannot do well

Be honest about the ceiling. Games are good at retrieval, discrimination,
pattern recognition and low-stakes repetition. They are poor at:

- **Free conversation.** Turn-taking, repair, hesitation and real-time
  comprehension need a person or an AI. Reageer/Rollenspel approximate the
  decision, not the interaction.
- **Long-form writing.** A sentence builder does not teach a paragraph.
- **Authentic listening.** Graded clips are not the NS announcement.
- **Pragmatic judgement.** When to be direct, when to soften, when *u* sounds
  distant — that is culture, not a quiz.

Pair the games with graded reading, shadowing, a tutor or AI conversation, and
real-world tasks (read the letter from the gemeente, order in Dutch). The games
are the practice engine, not the whole course.

---

## Already in `suggestions.md` — where each fits

These ideas exist but are not in the 13. They should not be lost, and several
fill the gaps above.

| Idea | Goal it serves | Verdict |
|---|---|---|
| Spot the Imposter | Pattern recognition (sound shifts), odd-one-out | Good, but English-specific like Ending Matcher |
| Translate the Telegram | Sentence decoding, reading recognition | Strong book-to-site bridge; overlaps Sentence Rescue |
| Which Room? | Semantic categorisation, vocabulary depth | Cheap and visual; overlaps Woordweb |
| False Friend or Real Friend? | False-friend meaning | Duplicate of Valse vrienden — keep one |
| Build the Ladder | Difficulty awareness / sound shifts | Teaching device, weak as a scored game |
| Verb Factory | Verb morphology (strip `-en`) | Only the infinitive→stem step; fold into Werkwoordtrainer |
| Double Agent | Polysemy / context-dependent meaning | Fills a real depth gap; text-only |
| Sound-shift Repair Shop | Spelling–sound mapping, production | Fills spelling/pronunciation awareness; text-only |
| Sentence Rescue | Reading fluency under time | Good timed layer for Translate the Telegram |
| Room Raid | Vocabulary in a visual scene | Fills the scene/context gap; stronger than Koppelen for memory |

---

## Recommended order

The constraint from `mvp.md` still applies: one thing in front of a stranger
before the ecosystem. The order below is by *gap filled per unit of work*, not by
how fun the game sounds.

1. **Shared data + mistakes queue.** Extend the one `grammar.js` with verbs,
   nouns (gender/plural), sentences and texts; keep the checker. Add local
   progress so misses feed Flitskaarten.
2. **Werkwoordtrainer.** Fills Pillar 6 and reuses the verb table Sentence
   Builder already needs.
3. **De of het.** Tiny data, high error rate, no audio, and it improves every
   other noun-based game.
4. **Reageer** or **Lees & Kies** — pick one based on the next audience: everyday
   conversation, or inburgering/reading. Both are text-only.
5. **Foutenspeurder.** Cheap once grammar data exists; trains noticing, which no
   current game does.
6. **Audio cluster** — Luisteroefening, Klankparen, Dictee, Luister & Kies — only
   after the audio question in `decisions.md` is settled.
7. **Later** — Nazeggen, Rollenspel/AI, Uitdrukkingen, KNM quiz, Beschrijf het.

Quick engagement wins that reuse existing chapter content and need no new
mechanics: Geheugen, Koppelen, Flitskaarten, Uitgangsmatcher, Lego-woorden. Word
Search and Hangman are also cheap, and their search/guess loop does build
word-form familiarity. Make the clue a picture (or a picture-only word list) and
show the picture, word and audio on completion, so the round spans form and
meaning instead of form alone.

---

## Data implications

`games.md` is right that one shared data file beats a file per game. Add sections
to the same object rather than new globals:

```js
{
  verbs:     [{ infinitive, stem, past, perfect, persons, strong, separable }],
  nouns:     [{ nl, en, gender, plural, picture }],
  frames:    [{ id, frame, verb, separable, prefix, prep, en, scene, example,
                pronominal, pronominalScene, contrast, conceptQuestions }],
  scenes:    [{ id, file, alt }],
  sentences: [{ nl, en, tokens, gap, error }],
  texts:     [{ nl, questions, level, source }],
  dialogues: [{ turns, register }],
  audio:     [{ id, file, transcript }]
}
```

The `frames` entry repeats `separable` and `prefix` from the matching `verbs`
entry so the game does not have to join at render time; `frame.verb` matches
`verbs[].infinitive`. The checker must keep the two consistent. The `contrast`
field points at another frame and is what lets the game generate a minimal-pair
false item.

The checker is not optional: if `nouns` has no `gender`, the De of het game is
silently broken. A missing `audio` file should fail the build, not a lesson.

## Open questions this raises

- Is *de/het* a new pillar, or an extension of Pillar 3? The concept says the
  pillar list is open to extension; this is the strongest candidate so far.
- Does Ending Matcher stay English-only in the book, or get a Dutch-internal
  version on the site?
- Is Valse vrienden a site game at all, given the audience constraint?
- Does "conversation practice" mean scripted dialogue, AI role-play, or both?
  That decision changes the data model and the premium line.
- Where does audio come from — native recordings or TTS? Quality, cost and
  licensing differ, and every listening game depends on the answer.
- Does the SRS/progress queue sit behind premium (`decisions.md` open question 4)?
  It is the strongest candidate for the paid line.
