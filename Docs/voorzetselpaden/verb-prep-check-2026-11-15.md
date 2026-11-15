# ZiN and Heard Dutch Here's verb–preposition lists, checked against ours

Checked 15 November 2026 against

- <https://zininnederlands.be/leer-nederlands/woordleer-nederlands/het-verbum/werkwoorden-met-vast-voorzetsel/>
  ("Werkwoorden met vast voorzetsel", 90 entries), and
- <https://www.heardutchhere.net/verbs_prepositions.html>
  (Marco Schuffelen, "Verbs and Their Prepositions", 187 entries).

The question asked was whether the plan holds everything these two pages list,
whether either page shows a mistake of ours, and — where something is missing —
which band it belongs in.

## What the two sources are, and what they are not

Neither page gives levels. ZiN is a Belgian teaching site, so a few entries are
Belgian usage (`bang zijn van` beside `bang zijn voor`). Heard Dutch Here is one
man's collection and says so: *"It is of course not possible to put all verbs
and all possible verb-preposition combinations on this page."* So absence from
either list proves nothing on its own, and presence is not a level.

Both are useful for the one thing they do well: naming combinations we might have
missed, and catching a chunk that teaches the wrong preposition.

## Our side

| When | Chunks (distinct names) | Cards | ZiN absent | HDH absent |
|---|---|---|---|---|
| before the audit (HEAD, `317f9db`) | 593 | 894 | 35 of 90 | 108 of 187 |
| after (15 Nov 2026) | 713 | 1015 | **2** | **12** |

The audit brought **129 entries** into the plan — 33 from ZiN, 96 from Heard
Dutch Here — which is **121 distinct chunks**, eight entries naming the same
chunk on both lists. Every one of those 121 is a proposal card: no art, no
`data-verdict`, `data-status="planned"`.

Measurement is `tools/_vp_tmp/coverage.py`: NFKD-normalise both sides, drop
`zich/zijn/hebben/iemand/iets/het/een/de/er`, then compare the first and last
surviving tokens. That sees `zich aanpassen aan` = `aanpassen aan` and still
keeps `denken aan` apart from `denken om`.

---

## 1. Faults the two lists exposed, and what was done

### 1.1 `ruiken aan` was missing, and with it the everyday sense

`a2.html` carried `ruiken naar` ("to smell of") alone. Heard Dutch Here has both,
and they are not interchangeable: **`ruiken naar`** is what a thing smells like
(`Het ruikt naar regen`), **`ruiken aan`** is what a person does with their nose
(`Hij rook aan de fles`). The page taught the pair's wrong half. `ruiken aan`
is now on `a2.html` beside it; the section heads with `2 prepositions, 2 cards`.

### 1.2 Section counts said "1 prepositions, 1 cards"

The count line above each contrast set was built from the number of chunk groups,
not from the prepositions in the heading and the cards in the section. So a
cluster of three chunks that all take `aan` (`aandacht besteden aan`,
`tijd besteden aan`, `besteden aan`) read "3 prepositions", and a one-card
section read "1 cards". Both now read the truth: `1 preposition, 3 cards`.
Fixed in the loader and re-stamped on every section this audit touched.

A later check of all fifty-seven count lines — comparing each one against its
own `<span class="preps">` and its own cards — found five still wrong in
sections the audit had not touched: `uitkijken` (7 cards, is 8), `vertrouwen`
(2, is 3), `berusten` (2, is 3), `inwerken` ("2 prepositions", there is one),
and `verdedigen` ("3 prepositions", there are two). All five are corrected. The
stamp now holds for every contrast set on all eight pages.

### 1.3 Six cards put meaning in writing

A self-review after the bulk insert found six scene briefs that only worked if
the learner could read something inside the picture or on a printed page:
`bedoelen-met-dat-woord` (a word on a page), `recht-hebben-op-een-vergoeding`
(a letter), `zich-verbazen-over-de-prijs` (a price tag), `strijden-tegen-de-ziekte`
(a banner), `zeker-zijn-van-de-uitslag` and `dreigen-met-ontslag` ("printed …").
All six now carry blank surfaces and name what the drawing shows instead. The
site rule is no text inside artwork, ever, because one art set has to serve
every first language.

### 1.4 The same chunk twice

`geinteresseerd in` and `geïnteresseerd zijn in` were both on `a2.html`. They
were merged into `geïnteresseerd zijn in` (four examples). `interesse hebben in`
is the noun-first twin and is now a separate card on `a2-plus.html`, since it is
a different sentence shape, not a duplicate.

### 1.5 Reported but not a fault

CLAUDE.md item 12 said the `praten-tegen` card on `a2.html` still answered "Ja"
to a question whose scene says no. Checked: `praten-tegen-muur` answers **Nee**,
and so do the other three `praten tegen` cards. The stale sentence is gone from
CLAUDE.md. Nothing in the pages needed changing.

### 1.6 Two entries checked and kept

- **`kijken op`** (`b1.html`) is kept against the drop rule, and the reason is
  written into the card's note: *op is a complement here (`op de klok kijken`,
  `op de kaart kijken`), not a free adjunct like `op` in `afspreken op een tijd`.*
- **`getuigen over`** (`b1-plus.html`) is kept beside `getuigen van`, which is a
  real contrast: `getuigen over` is a witness speaking about something,
  `getuigen van` is a thing being evidence of something.
- **`getuigen over` tested against the normaliser** — no change needed.

---

## 2. Everything added, by band

Every chunk below was absent before the audit and has a card now. The gloss is
the one on the page, borrowed from the source's own gloss. `ZiN+HDH` means both
lists carry the entry.

### A1 — 3

| Chunk | Gloss | Source |
|---|---|---|
| geven aan | to give to | HDH |
| wachten tot | to wait until | HDH |
| zwaaien naar | to wave at | HDH |

`wachten tot` was attached to the existing `wachten op · voor` cluster (now
`op · voor · tot`, 9 cards); the other two are new singles.

### A2 — 27

| Chunk | Gloss | Source |
|---|---|---|
| aanbellen bij | to ring at someone's door | HDH |
| antwoorden op | to answer | ZiN |
| denken om | to keep in mind | ZiN |
| denken van | to think of, to have an opinion about | HDH |
| doen aan | to take part in a sport | HDH |
| dromen over | to dream about | HDH |
| dromen van | to dream of | ZiN+HDH |
| gaan om | to be about, to be at stake | HDH |
| gaan over | to be about | HDH |
| gelukkig zijn met | to be happy with | ZiN |
| geven om | to care about | ZiN+HDH |
| halen uit | to take out of | HDH |
| kopen bij | to buy at | HDH |
| laten zien aan | to show to | HDH |
| oppassen met | to be careful with | HDH |
| rennen naar | to run to | HDH |
| rijden naar | to drive to | HDH |
| ruiken aan | to sniff at | HDH |
| ruiken naar | to smell of | HDH |
| smaken naar | to taste of | HDH |
| sterven aan | to die of | ZiN+HDH |
| sterven van | to die of | ZiN |
| telefoneren naar | to phone | ZiN |
| verkopen aan | to sell to | HDH |
| vinden van | to think of, to find | HDH |
| wachten met | to postpone | HDH |
| zeggen van | to say of, to say about | HDH |

`denken` became a three-way set (`aan · om · van`), `zeggen` a two-way one
(`tegen · van`), and `gaan over · om`, `dromen van · over` and `sterven aan · van`
are new contrast sets rather than singles.

### A2+ — 6

| Chunk | Gloss | Source |
|---|---|---|
| bevriend zijn met | to be friends with | ZiN |
| interesse hebben in | to be interested in | ZiN |
| plezier hebben in | to enjoy doing something | ZiN |
| verdriet hebben om | to grieve over | ZiN |
| verslaafd zijn aan | to be addicted to | ZiN |
| vriendelijk zijn tegen | to be kind to | ZiN |

These are the adjective and noun frames, which is what A2+ is for.

### B1 — 48

| Chunk | Gloss | Source |
|---|---|---|
| aandacht besteden aan | to pay attention to | HDH |
| achterlaten in | to leave behind in | HDH |
| bedekken met | to cover with | HDH |
| bedoelen met | to mean by | HDH |
| begrijpen van | to understand about | HDH |
| besteden aan | to spend on | HDH |
| dreigen met | to threaten with | HDH |
| een hekel hebben aan | to hate | HDH |
| gelijk hebben met | to be right about | HDH |
| gevoelig zijn voor | to be sensitive to | ZiN |
| gooien naar | to throw to | HDH |
| gooien tegen | to throw against | HDH |
| hebben aan | to benefit from | HDH |
| herkennen aan | to recognise by | HDH |
| het hebben over | to be talking about | HDH |
| horen van | to hear of | HDH |
| informeren naar | to ask about | ZiN |
| leiden tot | to lead to | HDH |
| lenen aan | to lend to | HDH |
| lenen van | to borrow from | HDH |
| lijden van | to suffer from | HDH |
| overlaten aan | to leave to | HDH |
| overtuigen van | to convince of | ZiN |
| protesteren tegen | to protest against | ZiN |
| recht hebben op | to be entitled to | ZiN |
| schrijven over | to write about | HDH |
| slagen in | to succeed in | ZiN+HDH |
| spijt hebben van | to regret | ZiN+HDH |
| spreken met | to speak with | ZiN+HDH |
| spreken over | to speak about | ZiN+HDH |
| stelen van | to steal from | HDH |
| studeren voor | to study for | ZiN |
| tijd besteden aan | to spend time on | HDH |
| van plan zijn om te | to intend to | HDH |
| vastmaken aan | to attach to | HDH |
| vastzitten aan | to be stuck to | HDH |
| vechten met | to fight with | HDH |
| vechten om | to fight over | HDH |
| vechten voor | to fight for | HDH |
| veranderen in | to turn into | HDH |
| verdwijnen uit | to disappear from | HDH |
| vermenigvuldigen met | to multiply by | HDH |
| verwachten van | to expect of | HDH |
| weten van | to know about | HDH |
| winnen van | to beat (a person or team) | HDH |
| zeker zijn van | to be sure of | ZiN |
| zich interesseren voor | to be interested in | ZiN |
| zich verbazen over | to be amazed at | HDH |

`slagen` was converted from `voor · in`; `spreken` became `met · over`; `lenen`,
`vechten` (`tegen · met · voor · om`), `gooien` (`naar · tegen`) and `schrijven`
(`aan · over`) are contrast sets.

### B1+ — 27

| Chunk | Gloss | Source |
|---|---|---|
| af zijn van | to be rid of | HDH |
| afwillen van | to want to get rid of | HDH |
| betekenen voor | to mean to | HDH |
| condoleren met | to offer condolences on | HDH |
| delen door | to divide by | HDH |
| delen met | to share with | HDH |
| iets hebben met | to be involved with | HDH |
| in staat zijn tot | to be capable of | ZiN |
| knoeien met | to mess about with | HDH |
| medelijden hebben met | to pity | HDH |
| neerkijken op | to look down on | HDH |
| strijden tegen | to fight against | HDH |
| strijden voor | to fight for | HDH |
| vallen op | to fall for (a person) | HDH |
| verbinden met | to connect to | HDH |
| verdelen in | to divide into | HDH |
| verdelen onder | to share out among | HDH |
| vertrekken naar | to leave for | HDH |
| vertrekken om | to leave at (a time) | HDH |
| vertrekken uit | to leave out of | HDH |
| vertrekken van | to leave from | HDH |
| vrezen voor | to fear for | ZiN+HDH |
| zich abonneren op | to subscribe to | ZiN |
| zich beperken tot | to limit oneself to | ZiN |
| zich specialiseren in | to specialise in | ZiN |
| zich verontschuldigen voor | to apologise for | ZiN |
| zich verzekeren tegen | to insure against | ZiN |

`delen` is now a three-way set (`in · met · door`: a share of what others
achieved; handing part of yours to someone; dividing a number), `verdelen`
two-way (`in · onder`), `vertrekken` four-way (`naar · om · van · uit`).

### B2 — 10

| Chunk | Gloss | Source |
|---|---|---|
| bidden om | to pray for | HDH |
| bidden tot | to pray to | HDH |
| drinken op | to drink to | HDH |
| jagen op | to hunt | HDH |
| schieten op | to shoot at | HDH |
| verdenken van | to suspect of | HDH |
| verlossen uit | to free from | HDH |
| verlossen van | to deliver from | HDH |
| wijten aan | to blame on | HDH |
| zich hechten aan | to become attached to | HDH |

`bidden` is a contrast set (`tot` names who is addressed, `om` what is asked
for), and so is `verlossen` (`uit` names the trap you are taken out of, `van`
the burden you no longer carry).

---

## 3. Deliberately not added

### 3.1 Near-equivalences of a chunk already in the plan

| Entry | Why not |
|---|---|
| `gebruikmaken van` (ZiN) | Same chunk as `gebruik maken van` (B1+), written as one word. Two cards would teach a spelling, not a preposition. |
| `danken voor` | Our plan teaches `bedanken voor` (A1). `danken` alone is the formal/literary verb. |
| `zin hebben in` (ZiN) | In the plan as `zin in` (A0 and A2+). |
| `bang zijn van` (ZiN) | Belgian spoken variant of `bang voor` (A0). In Netherlands Dutch `bang van niet` is a different idiom entirely, and the site teaches Netherlands Dutch. |
| `geïnteresseerd zijn in` | Already at A2 with four examples; `interesse hebben in` was added beside it rather than replacing it. |

### 3.2 The 12 HDH entries still absent, with reasons

These are the only entries of the 187 that have no chunk. Each one was read in
the source with its example sentence before being left out.

| Entry | Their gloss and example | Why it stays out |
|---|---|---|
| `aankunnen op` | to count on, rely on — *Je kunt erop aan* | Same meaning as `rekenen op` (A2 pairs, B1) and `vertrouwen op` (A2+), and `aan` is a separable prefix that splits to the end in a main clause, so a card could not build a statement with the chunk as listed. |
| `aanraken met` | touching with — *aanraken met een stok* | `met` is the instrument, free with any tool. Not a fixed combination. |
| `blijven in` | to stay, remain in — *Ik ben in Amerika gebleven* | Free locative. `blijven bij` is the fixed one and is in the plan. |
| `eten met` | eating with — knife and fork, or friends | `met` is instrument or company, free. |
| `eten van` | eating from — *eten van een bord* | Container choice is not fixed: `van het bord` and `uit de pan` are both ordinary. No rule to teach. `drinken uit` (A0) stays because drinking is nearly always out of a bottle or glass. |
| `gaan met` | going by (transport) — *Ga je met de auto?* | `met` is the means of transport, free. The fixed frame here is `hoe gaat het met …`, which is a different teaching point. |
| `komen voor` | to come for — *We komen voor de muziek* | `voor` is the purpose, free. The "to occur" sense their list does not mean is the separable `voorkomen`, a different verb. |
| `schieten naar` | shooting at a single target — *schoot een pijl naar de boom* | `naar` is direction, `op` is aim. `schieten op` (B2, added) carries the fixed sense; two cards would blur it. |
| `toegeven van` | admitting to — *het moeten toegeven van fouten* | Not a verb + preposition at all: it is a nominalisation (`het toegeven van fouten`), the same `van` any infinitive takes. |
| `vallen van` | to fall from — *van de trap gevallen* | Free ablative. `vallen op` and `vallen uit` are the fixed ones and are in the plan. |
| `willen naar` | to want to go to — *Ik wil naar huis* | Free destination. |
| `willen van` | to want of — *Wat wil je toch van mij?* | Real, but it lives in one question frame, and a card builds statements. Not teachable in this format. |

---

## 4. What this does not settle

- **The 121 new cards have no art.** They are proposals with `not drawn yet`,
  so `tools/import-prepositions-band.py` cannot see them and the game does not
  ship them. 271 of the 1015 cards are in that state.
- **The matrix pages count fewer chunks than the band pages.** That is by
  design, not a bug: `tools/build-prepositions-matrix.py` leaves out cards
  marked `data-verdict="drop"` (b1 129 of 141, B1+ 199 of 256, B2 138 of 212).
- **136 older cards have no English gloss.** Every card on the pages has a
  `<p class="gloss">`, but on a0 (28), a1 (60) and a2 (48) it is empty. Those
  cards predate this audit and none of the 121 added here is among them; their
  only English is in the scene brief and the example translation. Left for a
  separate pass.
- **The game data was not regenerated.** `prepositions.json` is unchanged by
  this audit; regenerating it from the pages would ship unfinished proposals and
  would re-introduce the old `praten-tegen` wording.
- **The A1 gate is unchanged.** `wachten tot`, `geven aan` and `zwaaien naar` are
  behind the same account wall as the rest of A1.
- **Levels are my judgement.** Neither source has levels. A2/A2+/B1 placements
  follow the existing split: concrete-and-frequent at A2, adjective and noun
  frames at A2+, the abstract and the nominal at B1 and up. `delen door` sits at
  B1+ rather than A2 because it belongs in the `delen` contrast set, and contrast
  beats level.
