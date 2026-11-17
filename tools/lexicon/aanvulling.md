# Where the next ~3,000 Dutch words can come from

Written 16 November 2026. Research only: nothing here changes `woorden.tsv`,
`woorden-woordsoort.tsv`, `woorden-thema.tsv`, `extraheer-woorden.py` or
`thema.py`. The extracted words are in `tools/lexicon/kandidaten.tsv`.

## The answer in one paragraph

**10,000 ordinary lemmas is reachable; 10,000 *themed* lemmas is not, from open
sources.** kaikki.org's English-Wiktionary extraction for Dutch gives English
glosses, part of speech and lemmas under a licence that permits commercial use,
and after removing names, inflected forms, obsolete registers and words already
on the list it still yields **10,442** new lemmas with clean English glosses.
That number is larger than the 2,893 the project needs, so the lemma count is
no longer the constraint. The constraint is that only about **2,500** of those
new lemmas land in one of the 24 product themes, and about a quarter of those
landings are wrong when you read them. The themed gap (roughly 4,800 themed
everyday words, of which about 1,400 exist) cannot be closed by any open source
found here. It needs a hand-built list, or a theme tag written by a human
against a topic list that open data does not carry.

## What was inspected, and how

Every count below was produced by downloading the source and parsing it on this
machine in `/tmp/lex/`, not recalled. Where a licence statement was checked, the
URL that states it is given. Two sources could not be verified and are marked so.

| Source | URL | What it actually contains | Entries (verified) | English glosses | Lemma or form | POS / level | Licence (and where stated) | Commercially usable | Could add |
|---|---|---|---|---|---|---|---|---|---|
| **kaikki.org Dutch** (English Wiktionary via wiktextract) | `https://kaikki.org/dictionary/Dutch/kaikki.org-dictionary-Dutch.jsonl` (257,235,436 bytes, 146,790 lines) | One JSON object per POS entry: `word`, `pos`, `senses[].glosses` (English), `forms`, etymology, `topics` on 5,360 senses | **146,790 entries, 138,944 distinct words**; 54,377 lowercase lemma words after dropping form-of/alt-of; 146,779 entries carry a gloss | **Yes** — English glosses, the source's whole point | **Lemmas**, with inflected forms separate and tagged `form_of`/`alt_of` (99,214 senses) | POS on every entry (noun 75,799; verb 40,519; adj 13,445; name 12,452; …). **No CEFR level, no frequency, no rank** | **CC BY-SA 4.0 and GFDL**, stated at `https://en.wiktionary.org/wiki/Wiktionary:Copyrights` and inherited by kaikki from the extraction date shown on `https://kaikki.org/dictionary/Dutch/index.html` (extracted 2026-10-30 from the 2026-10-01 enwiktionary dump) | **Yes** | **10,442** (see below) |
| **Open Dutch WordNet 1.4** | `https://raw.githubusercontent.com/cltl/OpenDutchWordnet/master/resources/odwn/odwn_orbn_gwg-LMF_1.4.xml.gz` (15,425,745 bytes) | WordNet-LMF XML: `LexicalEntry` → `Lemma writtenForm`, `partOfSpeech`, `Sense` → English WordNet 3.0 synset id (`synset="eng-30-…"`) | **90,923 lexical entries, 59,578 distinct lemmas** (noun 73,956; verb 15,824; adj 1,143) | **Indirectly** — no gloss text; the English synset id would have to be joined to an English WordNet release to get a gloss | Lemmas | POS yes; **no CEFR level** | **CC BY-SA 4.0**, `https://github.com/cltl/OpenDutchWordnet/blob/master/LICENSE.md` | **Yes** | Small net addition: 42,000+ of its lemmas are already reachable from kaikki, and it has no adjectives worth the name (1,143). Useful as a **second opinion on lemma/POS**, not as a gloss source |
| **OpenTaal word list** | `https://github.com/OpenTaal/opentaal-wordlist` — checked `elements/basiswoorden-gekeurd.txt` (2,532,852 bytes, **199,403 lines**) and `wordlist.txt` (5,104,598 bytes) | Spelling list: base words approved by the Taalunie spelling mark, plus unapproved base words, flexions and word parts | **199,403 approved base words**; >400,000 in the full `wordlist.txt` per the README | **No** — spelling only | `basiswoorden-gekeurd.txt` is **base words (lemmas/compounds)**; `flexies-ongekeurd.txt` and much of `wordlist.txt` are **inflected forms** | **No POS, no level** | **BSD-3-Clause *or* CC BY 3.0, at your discretion**, stated in `https://github.com/OpenTaal/opentaal-wordlist/blob/master/LICENSE.txt` (§3 and §6 of the English text) | **Yes** | **0 on its own** — it has no glosses. Its value is as a **spelling/coverage oracle**: it would confirm which kaikki lemmas are real modern spellings, and catch kaikki omissions |
| **hermitdave/FrequencyWords `nl_50k`** | `https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/nl/nl_50k.txt` (650,762 bytes) | `token count` per line, from OpenSubtitles 2018 | **50,000 lines** | **No** | **Forms**, not lemmas (`is`, `waren`, `gemaakt` all appear) | No | **MIT**, `https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/LICENSE` | **Yes** | **0 on its own** — frequency only, and of forms. Redundant with `wordfreq` below |
| **`wordfreq` 3.1.1** (Robyn Speer) | PyPI wheel `wordfreq-3.1.1-py3-none-any.whl` (56.8 MB), installed to a throwaway target dir | Per-language token frequency, blended from Wikipedia, ParaCrawl, OpenSubtitles, SUBTLEX-NL, Google Books Ngrams | Dutch list queried live (`top_n_list('nl', 50000)`, `zipf_frequency(w,'nl')`) | **No** | **Forms** | No | **Code Apache-2.0; data redistributable under CC BY-SA 4.0**, with SUBTLEX and OpenSubtitles attribution required — `https://github.com/rspeer/wordfreq/blob/master/NOTICE.md`. The `LICENSE.txt` explicitly says "This license applies to the code only. See NOTICE.md" | **Yes**, as data under CC BY-SA 4.0 with attribution | **0 words** — used here only to **rank and gate** kaikki candidates. Any product build that reuses its rankings must carry the attribution |
| **Tatoeba** | `https://tatoeba.org/en/downloads` | Sentence pairs, many Dutch↔English | Sentence counts per export, not a word list | Sentence-level translation, not glosses | Neither | No | **CC BY 2.0 FR**, some sentences **CC0 1.0**, stated on `https://tatoeba.org/en/downloads` | **Yes** (CC BY 2.0 FR permits commercial use with attribution) | **0 lemmas**. Would need lemmatising and sense disambiguation; a gloss-provenance aid at best |
| **NT2Lex** | `https://github.com/anaistack/NT2Lex` | CEFR-graded lexical resource linked to ODWN | Not inspected for content | — | — | — | **CC BY-NC-SA 4.0** per the owner's brief; GitHub reports licence `NOASSERTION`, and the repo was not downloaded | **No** — NC. **Internal levelling reference only** | 0 shippable |
| **SUBTLEX-NL** | `http://crr.ugent.be/programs-data/subtitle-frequencies` | Subtitle frequencies | — | No | Forms | No | Research-licensed (owner's brief); not re-verified here | **No** | 0 |
| **Routledge, *A Frequency Dictionary of Dutch* (2014)** | — | — | — | — | — | — | Copyrighted; already consumed as `bijlage8` under fair-use-style extraction into `woorden.tsv` | **No** as a source | 0 |
| **Numo "Woordenlijst NT2-modules A0-A1"** | `https://assets.numo.nl/wp/Woordenlijst-nt2.pdf` (1,685,302 bytes, fetched) | Word, skill, exercise, POS — a publisher's course word list | Not counted; **no licence statement found in the document** | Only Dutch | Mixed | POS yes; A0–A1 by construction | **No licence stated anywhere in the PDF** — treated as all rights reserved | **No** | 0 |
| **ISK/LOWAN "Basiswoordenschat alfabetisering NT2 — 600 woorden"** | `https://www.wikiwijs.nl/app/uploads/ISK_startwoordenschat-600-woorden.pdf` (96,729 bytes, fetched) | ~600 alphabetisation words grouped by lesson theme | **600 by its own title**; theme grouping is exactly the product's missing dimension | **No** | Mixed, with parenthetical hints | A1-and-below by construction | **No licence statement found in the PDF or in its metadata** | **No** | 0 — but this is the *shape* the product needs |

Not inspected: the CLARIN-NL/INT portal pages (no direct download found to
verify), and `eupassway.com`'s "woordenlijst inburgering (A1–B2)", which is a
commercial site with no licence grant. Neither is counted anywhere below.

## How 10,442 was produced, and why it is not padded

Starting from all 146,790 kaikki entries:

1. Keep `noun`, `verb`, `adj`, `adv` only.
2. Drop every entry whose senses are `form_of` or `alt_of` — that is what makes
   the result a **lemma** list rather than a form list.
3. Drop a word if every sense is tagged `rare`, `archaic`, `obsolete`, `dated`,
   `historical`, `slang`, `neologism`, `nonstandard`, `misspelling`,
   `humorous`, `vulgar`, `derogatory`, `offensive`, `childish` or
   `bureaucratese`.
4. Drop any gloss that is itself a form description ("…indicative of X"), a
   spelling note ("Synonym of", "Official spelling of"), or a cross-reference.
5. Drop anything already in `woorden.tsv`, matching on the lemma with the
   `(verb)`/`(noun)` disambiguator stripped.
6. Apply `wordfreq`'s Dutch zipf score as an everyday-ness gate at **≥ 2.5**
   (roughly "occurs at least occasionally in edited text"). This alone removed
   11,270 unattested and 10,600 near-silent dictionary entries.
7. Drop English loanwords that the corpus frequencies over-supply (`house`,
   `girl`, `big`, `star`, `party`) unless their Dutch frequency is very high.
8. Drop words that kaikki also documents as an inflected form, at moderate
   frequency, to avoid `waren`, `gemaakt`, `wilde`-type homographs.

That leaves **10,442** rows, every one with a non-empty English gloss, no
duplicates, and zero overlap with `woorden.tsv` (checked). Of those, **4,949**
have a zipf ≥ 3.0 — that is, comfortably common words, the kind the product
wants for A2–B1. A sampling of the ≥ 3.0 band: `informatie`, `postkantoor`,
`verblijfsvergunning`, `id-kaart`, `ov-chipkaart`, `registratie`, `annuleren`,
`afzeggen`, `zorgzaam`, `kraamzorg`, `makkelijk`, `vergeet-mij-niet`,
`auto-ongeluk`, `zwart-wit`, `mee-eten`, `kant-en-klaar`, `sleutelwoord`,
`huurwoning`, `buurthuis`, `boodschappenlijst`, `gesprek`, `opleiding`.

**The list is not padded, but it is not clean either.** The tail between zipf
2.5 and 3.0 contains encyclopaedic and specialist words (`zeeniveau`,
`belastingdruk`, `conservatorium`) that are legitimate lemmas but not
A1–B1 teaching material. Anyone merging this must apply a further judgement
step, by cut-off on rank or by hand. I have deliberately not trimmed the file
to disguise that; the report states the numbers at each cut-off so the decision
is made on evidence:

| Gate | New lemmas | Running total with the existing 7,107 |
|---|---|---|
| zipf ≥ 2.5 (the file as shipped) | 10,442 | 17,549 |
| zipf ≥ 3.0 (comfortably common only) | 4,949 | 12,056 |
| zipf ≥ 3.5 | 1,624 | 8,731 |

**So 10,000 is reachable, and reachable from words a learner would actually
meet** — the zipf ≥ 3.0 band alone gives 12,056, needing only ~2,000 more on top
of 7,107 against 4,949 available. There is roughly a 2.7× margin at that gate.
Even the strictest reasonable cut (zipf ≥ 3.5) plus the existing list reaches
8,731, and closing the last 1,300 from the 2.5–3.5 band is easy.

## What the 24 themes still need

The lemma target is met. The **themed** target in `Docs/product.md` §12 is not,
and this is the honest bad news.

Running the project's own classifier (`thema.py`, called directly, unmodified)
over the 10,442 rows:

| Theme | Now | + candidates | After |
|---|---|---|---|
| Mensen | 162 | 398 | 560 |
| Wonen | 191 | 307 | 498 |
| Eten en drinken | 179 | 256 | 435 |
| Reizen | 137 | 229 | 366 |
| Werk | 127 | 142 | 269 |
| Sport en vrije tijd | 131 | 131 | 262 |
| Het lichaam | 76 | 165 | 241 |
| Kinderen en school | 65 | 145 | 210 |
| Nood en politie | 66 | 121 | 187 |
| Kleding | 110 | 61 | 171 |
| Bank en geld | 42 | 114 | 156 |
| Gezondheid | 37 | 118 | 155 |
| **Boodschappen** | 30 | 95 | **125** |
| Gemeente en post | 39 | 56 | 95 |
| Telefoon en internet | 29 | 55 | 84 |
| Mening geven | 21 | 40 | 61 |
| De weg | 17 | 23 | 40 |
| Klachten | 9 | 29 | 38 |
| Solliciteren | 6 | 23 | 29 |
| Afspraken | 5 | 15 | 20 |
| Formulieren | 9 | 9 | 18 |
| Buurt | 6 | 10 | 16 |
| Zorg voor iemand anders | 10 | 6 | 16 |
| Bellen | 5 | 7 | 12 |
| *(algemeen)* | 5,252 | 7,760 | 13,012 |

Total in a world theme: **1,411 now → 3,956 after**, against a §12 target of
~4,800 across 24 themes at ~200 each.

Three qualifications, none of them in the candidates' favour:

1. **The classifier is a keyword matcher, and dictionary glosses trip it.** In
   `Boodschappen` it files `klimaatverandering` (on "change"), `amendement` (on
   "change"), `omkleden` (on "change"), `magazijn` (on "store") and `slager`,
   only one of which belongs. In `Formulieren` it files `tankstation`,
   `pompstation` and `vulling` because their glosses contain "fill". In
   `Buurt` it files `beitel` (a chisel, on "block") and `galerij` (an art
   gallery). **I estimate precision as roughly 70–80% in the mid-size themes and
   below 50% in `Formulieren`, `Buurt` and `De weg`.** The "after" column above
   is therefore an overcount of usable themed words, probably by 500–700.
2. **The thin themes are thin for a reason that no open word list fixes.**
   `Buurt`, `Afspraken`, `Bellen`, `Zorg voor iemand anders`, `Solliciteren` and
   `Formulieren` are *situations*, not semantic domains. Their vocabulary is
   mostly the same high-frequency general words (`deur`, `brief`, `afspreken`,
   `belasting`) already counted under `algemeen`, and adding 10,000 lemmas does
   not change that. Getting `Buurt` to 200 means deciding *which* words belong
   to the neighbourhood and listing them — that is editorial work, not data
   sourcing.
3. **kaikki's `topics` field does not rescue this.** Only 5,360 of 146,790
   entries carry topics at all, and the everyday words that matter do not:
   `supermarkt`, `dokter`, `buurman`, `apotheek`, `postkantoor`, `huurwoning`
   have none. A topic-driven themer cannot be built from this.

What would actually close the themed gap, in order of cost:

- **The `kandidaten.tsv` rows that the classifier places in a theme**, sorted by
  frequency, hand-checked theme by theme. That is ~3,900 rows to review, a
  realistic two or three days, and yields maybe 2,700 usable ones. It gets most
  themes past 150 and a handful past 200.
- **The ISK 600-word alphabetisation list** (`https://www.wikiwijs.nl/app/uploads/ISK_startwoordenschat-600-woorden.pdf`)
  is grouped by exactly the right situations (`Ik ga naar school`, `Ik heb
  vrije tijd`, …). Its licence is unstated, so it can be used as a **checklist
  to write against**, not copied. This is the single most useful artefact found
  for the themed problem and it cannot be shipped.
- **Dutch municipal and government "klare taal" corpora** (gemeente, DUO, DigiD
  explainers) are the right register for `Gemeente en post`, `Formulieren`,
  `Afspraken` — but the ones checked are government copyright, not CC.
- Otherwise: write the themed lists. At ~200 words × 6 thin themes, that is
  ~1,200 rows of hand work with English glosses — less than one day for a
  competent editor, and the only route that produces a list matching the
  product's own themes.

## Attribution obligations before this ships

The CC BY-SA 4.0 obligation is real and applies to whatever is built from
kaikki:

- Credit "English Wiktionary, CC BY-SA 4.0, via kaikki.org/wiktextract" in the
  site's credits or colophon, with a link to the licence.
- The derived gloss list becomes **Adapted Material** and must itself be
  shared under CC BY-SA 4.0. If `kandidaten.tsv` is merged into `woorden.tsv`
  and that file is published, it must carry the BY-SA notice. Keeping
  `woorden.tsv` internal and shipping only the game rounds does not escape this,
  because the glosses reach the learner.
- If `wordfreq` rankings are baked into a shipped ranking, add Robyn Speer,
  SUBTLEX (Brysbaert et al.) and OpenSubtitles attribution per `NOTICE.md`.
- OpenTaal, if used as a spelling oracle, needs its BSD-3 or CC BY 3.0 notice.

This is a licensing decision for the owner, not a technical one: merging kaikki
into `woorden.tsv` makes the vocabulary list itself copyleft.

## Files

- `tools/lexicon/kandidaten.tsv` — 10,442 rows, columns `nl  en  bron  licentie`,
  same shape as `woorden.tsv` minus the three columns this source cannot
  supply (`niveau`, `top2000`, `herkomst` are blank-by-absence). Sorted by
  descending frequency. `bron` is `kaikki:enwiktionary-nl`; `licentie` is
  `CC BY-SA 4.0 + GFDL`.
- The two scripts and the three TSVs were not modified.

## Reproducing

```sh
curl -o nl.jsonl https://kaikki.org/dictionary/Dutch/kaikki.org-dictionary-Dutch.jsonl
pip install --target ./wfenv wordfreq
# then: filter form_of/alt_of, register tags, form-description glosses,
# de-disambiguate woorden.tsv, gate on zipf_frequency(w,'nl') >= 2.5
```
