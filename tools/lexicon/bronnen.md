# Where the 10,000 words come from, and how each one was chosen

Written 17 November 2026. Every number below was measured by re-running the
selection against the files in this directory, not copied from an earlier
report. All source research — what was downloaded, what it contained, what it
was licensed under — is in `aanvulling.md`; this file states the *selection
rule* and the *provenance counts*, and points there for the rest.

## The answer in one paragraph

Nobody chose the online words by hand. The 10,000 is **7,232 words the owner
already owned** (the coursebook appendix, the games' picture vocabulary, the
TaalCompleet KNM list) plus **2,768 words taken from English Wiktionary by
frequency rank**: the 10,442 kaikki candidates were scored with `wordfreq`, sorted
by descending zipf frequency (alphabetical on ties), and cut at **zipf 3.29**. The
alphabetical tie-break at that cut-off decided 42 of the 61 words sitting exactly
on the boundary, so the last few words in the file are arbitrary. **7,607 usable
candidates were left unused** — that is the headroom if the target ever rises.

## The three steps

| Step | Script | Adds | Running total |
|---|---|---|---|
| 1 | `extraheer-woorden.py` | Bijlage 8 appendix + the six games' word banks | **7,107** |
| 2 | `knm-woorden.py` | TaalCompleet KNM vocabulary | **7,232** |
| 3 | `verrijk-woorden.py` | kaikki candidates, ranked by `wordfreq` | **10,000** |

Only step 3 involves a choice. Steps 1 and 2 are exhaustive: every lemma those
sources supply that is not already present is taken.

## The selection rule, as arithmetic

Inputs: `kandidaten.tsv` (10,442 rows) and `woorden.tsv` as step 2 left it
(7,232 rows).

| | count |
|---|---|
| candidate rows in `kandidaten.tsv` | 10,442 |
| already present after step 2 (the 67 KNM lemmas that also sit in the pool) | −67 |
| rows with an empty gloss | −0 |
| duplicate lemmas among the survivors | −0 |
| **actually scored with `zipf_frequency(nl, "nl")`** | **10,375** |
| needed to reach 10,000 | 2,768 |
| sorted by | `(-zipf, nl)` — descending frequency, alphabetical tie-break |
| **cut-off** | **zipf 3.2900** |
| candidates sitting exactly at 3.29 | 61 |
| of those, taken | 42 |
| **unused survivors** | **7,607** |

The 67 is not a coincidence: `knm-woorden.py` runs *before* the top-up, so the
KNM words the pool also contains are already in `woorden.tsv` and are skipped
rather than double-counted. The KNM step itself: 321 rows / 279 distinct
headwords → **125 added**, 152 already present or repeated, **44 phrases skipped**
(multi-word or containing digits), 0 empty glosses.

## What was left on the table

All 10,442 candidates already passed the `zipf >= 2.5` gate when
`kandidaten.tsv` was built (step 6 of the recipe in `aanvulling.md`). The
selection therefore threw away real, usable, glossed lemmas:

| unused candidates with zipf ≥ | count |
|---|---|
| 2.50 | 7,607 |
| 3.00 | 2,128 |
| 3.10 | 1,320 |
| 3.20 | 620 |
| 3.25 | 288 |
| 3.28 | 75 |

That is deliberate, not an oversight: the appendix is the 5,000 most frequent
Dutch lemmas, so the honest continuation of it is the *next* most frequent words.
Nothing rarer than the cut-off was taken while a more frequent word was
available. The cost is that the tail is dull rather than useful — the 2.5–3.0
band holds encyclopaedic and specialist vocabulary (`zeeniveau`, `belastingdruk`,
`conservatorium`), and nothing here reads the "topics" tags Wiktionary carries on
5,360 senses.

If the target moved to 12,000, the next 2,000 words are already on disk and need
no new source — `verrijk-woorden.py --target 12000` is the whole change; at that
point the cut-off is around zipf 2.9. The pool runs out at **17,607** in total
(7,232 + 10,375), beyond which a new extraction from a lower gate would be
needed.

## The 2,768 are mostly nouns, and that matters

Part of speech of the `kaikki` rows:

| pos | rows | share |
|---|---|---|
| noun | 2,142 | 77.4% |
| adj | 294 | 10.6% |
| verb | 277 | 10.0% |
| adv | 41 | 1.5% |
| function | 9 | 0.3% |
| interjection | 3 | 0.1% |
| name | 2 | 0.1% |

So "10,000 words to B2" is a *noun* claim more than anything. The appendix
already carries the verb and adjective spine (1,330 verbs, 844 adjectives); the
extension adds nouns. If the goal is B2 reading, that is defensible — most of
what a B2 text adds beyond B1 is nominal — but it is not a balanced list, and no
source found supplies a frequency-ranked B2 verb or adjective list to fix it.

## Provenance of the 10,000

| `herkomst` | rows | what it is |
|---|---|---|
| `bijlage8` (sole origin) | 4,709 | the coursebook appendix |
| `bijlage8;spel:…` | 452 | appendix words that are also in a game's picture bank |
| `spel:…` (games only) | 1,946 | picture vocabulary from the six games |
| `knm` | 125 | TaalCompleet KNM |
| `kaikki` | 2,768 | frequency-ranked Wiktionary extension |
| **total** | **10,000** | |

The 26 game banks behind the `spel:` tags are `animals`, `art`, `cities`,
`countries`, `dinosaurs`, `fashion`, `flowers`, `food`, `history`, `household`,
`insects`, `literature`, `marine`, `mountains`, `movies`, `music`, `mythology`,
`nature`, `oceans`, `professions`, `reels`, `science`, `space`, `sports`,
`technology`, `travel`. Many rows carry two or three tags.

Read another way:

- **5,161** rows come from the frequency appendix (4,709 + 452).
- **2,398** rows are in at least one game bank; 452 of those are also appendix
  words, so **1,946** are game-only.
- The "general Dutch spine" — appendix, KNM and Wiktionary, no picture game —
  is **8,054** words. The remaining 1,946 are concrete, pictureable vocabulary.

## What counts as a "word" here

`woorden-woordsoort.tsv` gives the shape of the 10,000:

| pos | rows | |
|---|---|---|
| noun | 6,335 | |
| verb | 1,607 | |
| adj | 1,138 | |
| adv | 364 | |
| name | 315 | countries, cities, people — proper nouns, not vocabulary |
| function | 205 | prepositions, pronouns, conjunctions, numerals |
| interjection | 35 | |
| phrase | 1 | |

If "word a learner wants to learn" means a content word, the usable figure is
**9,480** after removing the 205 function words and 315 proper names — and 1,946
of those are picture vocabulary the games already teach. The 205 function words
are deliberately kept: a learner needs them, but they are taught as grammar, not
as vocabulary, which is why `thema` files them all as `algemeen`/`laag` and the
domain axis puts them in `Function words`.

## Sources

Every source with a URL, a verified byte/row count, a licence and where that
licence is stated is tabulated in `aanvulling.md` §"What was inspected, and how".
Summary of the three that contributed rows:

| Source | URL | Licence (where stated) | Rows used |
|---|---|---|---|
| **English Wiktionary via kaikki.org** | `https://kaikki.org/dictionary/Dutch/kaikki.org-dictionary-Dutch.jsonl` — 257,235,436 B, 146,790 entries, extracted 2026-10-30 from the 2026-10-01 dump | **CC BY-SA 4.0 + GFDL** — `https://en.wiktionary.org/wiki/Wiktionary:Copyrights` | 2,768 |
| **Bijlage 8**, *Nederlands in actie* | `/home/tony/Downloads/filen/DutchCourses/NederlandsInActie/Bijlage-8-Frequente woorden (1).pdf` — 148 pp, 1,938,987 B; credits C. Tiberius & T. Schoonheim (2014), *A Frequency Dictionary of Dutch*, Routledge | Copyrighted, no grant. Tier read from the page *fill colour*, not text | 5,161 (any) |
| **TaalCompleet KNM** word lists | `…/4 Woordenlijst KNM - Engels.pdf` (10 pp) and `…/6 Woordenlijst KNM - Nederlands.pdf` (26 pp) | None stated anywhere — treat as internal | 125 |
| **The six games' word banks** | `server/Oefenpad.Resources/Games/Data` (`words.json`, `reels.json`) | Project's own | 2,398 (any) |
| **wordfreq 3.1.1** | PyPI wheel, 56.8 MB | Code Apache-2.0, data **CC BY-SA 4.0**, per `NOTICE.md` | ranking only, 0 words |

Note what the appendix is: it is a *tiered* list. Light blue page fill means the
word is taught in *Nederlands in gang* (A1), orange means *Nederlands in actie*
(B1), unmarked means it is in the 5,000 most frequent but in neither coursebook
— which `woorden.tsv` records as `niveau = open` (3,469 rows). There is no B2
tier in that source and no B2 label anywhere in these files.

**No public B2 word list exists.** CEFR publishes none; the Groene Boekje is
spelling only; SUBTLEX-NL and Routledge are restricted; NT2Lex is CC BY-NC-SA.
8,000–10,000 lemmas is the usual estimate for B2 receptive vocabulary — see
`README.md` for the citations. It is a **target**, not a measurement, and the
10,000 here is a frequency-ordered approximation of it, not a validated B2 list.

## Attribution

Copied from `aanvulling.md` §"Attribution obligations before this ships", because
it binds whatever is built from these files:

- Credit "English Wiktionary, CC BY-SA 4.0, via kaikki.org/wiktextract" with a
  link to the licence.
- The merged list is **Adapted Material** and must itself be CC BY-SA 4.0. That
  makes `woorden.tsv` and the three files derived from it **copyleft**.
- If `wordfreq` rankings ship, add Robyn Speer, SUBTLEX (Brysbaert et al.) and
  OpenSubtitles attribution per `NOTICE.md`.
- The `bijlage8` and `knm` rows are copyrighted extractions. They cannot ship at
  all as they stand, independently of the CC BY-SA question.

None of this is cleared. It is an owner licensing decision.

## What we did not use, and why

| Source | Why not |
|---|---|
| Open Dutch WordNet 1.4 (CC BY-SA 4.0) | No glosses of its own — it links to English WordNet synsets, and 42,000+ of its lemmas are already reachable from kaikki. It has 1,143 adjectives, so it cannot balance the noun skew |
| OpenTaal word list (BSD-3 or CC BY 3.0) | Spelling only, no glosses, no POS. Useful as a spelling oracle, not as a source |
| hermitdave/FrequencyWords `nl_50k` (MIT) | Forms, not lemmas, and redundant with wordfreq |
| Tatoeba (CC BY 2.0 FR) | Sentence pairs, not a word list |
| NT2Lex (CC BY-NC-SA 4.0) | Non-commercial, so it cannot be used for anything that ships |
| SUBTLEX-NL | Research licence |
| Routledge *A Frequency Dictionary of Dutch* | Already consumed via the appendix; the work itself is copyrighted |
| Numo A0–A1, ISK/LOWAN 600 woorden | Exactly the right shape — themed, A1-and-below — but **no licence is stated in either PDF**, so treated as all rights reserved |
| `eupassway.com` "woordenlijst inburgering A1–B2" | Commercial site, no licence grant, not counted anywhere |

The full comparison, including what each source could have added, is
`aanvulling.md`.

## Reproducing the selection without changing anything

```sh
python3 -m pip install --target /tmp/wf wordfreq
python3 tools/lexicon/verrijk-woorden.py --wordfreq /tmp/wf --report
```

`--report` scores the pool and prints the arithmetic above — pool size, how many
are already present, the cut-off, how many sit on it, what the next band would
cost — and exits without writing. A plain run adds words and stops once the
target is reached.

## Known defects in the result

- **41 wrong English glosses** on `bijlage8` rows, with row numbers, in
  `gloss-audit.md`. Cause is the PDF extraction; fix by hand, do not regenerate.
- **`rechercheur`'s gloss** was corrected by hand in `woorden.tsv`, so a full
  regeneration reverts it. The `luifel` domain correction lives in `domein.py`
  and survives.
- **Theme accuracy is weak on `kaikki` rows**: 16 of 33 sampled named themes were
  wrong. `domein` is the axis to browse by; `thema` on those rows is a hint.
- **The boundary is arbitrary.** 42 of 61 words at zipf 3.29 got in by
  alphabetical order. Do not treat inclusion or exclusion at the tail as
  meaningful.
