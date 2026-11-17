# Lexicon

A 10,000-lemma Dutch vocabulary list, classified by part of speech and by the
product's themes. It is **evidence and data, not a learner surface**: a page
that says "learn these 4,000 words" makes the learner read before practising,
which `CLAUDE.md` calls suspect. Nothing in the site reads these files yet.

## The files

| File | Rows | Shape |
|---|---|---|
| `woorden.tsv` | 10,000 | `nl  en  niveau  top2000  herkomst` — the master list |
| `woorden-niveau.tsv` | 10,000 | `nl  niveau  rang  grondslag` — **our** five frequency bands (see below) |
| `woorden-frequentie.tsv` | 10,000 | `nl  zipf  rang` — the wordfreq score the bands are cut from |
| `woorden-woordsoort.tsv` | 10,000 | `nl  pos  en` — same rows, same order |
| `woorden-thema.tsv` | 10,000 | `nl  thema  thema_ook  prioriteit  en` — same rows, same order |
| `woorden-domein.tsv` | 10,000 | `nl  domein  en` — semantic domain, same rows, same order |
| `kandidaten.tsv` | 10,442 | `nl  en  bron  licentie` — the vetted online pool the top-up draws from |
| `knm-kandidaten.tsv` | 321 | `nl  en  knm_thema  knm_sectie` — the TaalCompleet KNM word lists |
| `knm-thema.tsv` | 279 | `nl  thema  prioriteit  waarom` — hand-checked theme for the KNM words |
| `index.html` | — | generated viewer for all of the above (see below) |
| `bronnen.md` | — | **where every row came from and the exact selection rule** — read this before trusting a count |
| `aanvulling.md` | — | the source and licence research behind `kandidaten.tsv` |

The six 10,000-row files are row-aligned by construction: the `nl` column is
byte-identical and in the same order. Each script asserts this.

## Reading them without a terminal

Open `tools/lexicon/index.html` in a browser. It is one self-contained file —
**2.4 MB, no network, no server, works by double-click** — with the whole
10,000-row list joined by position, plus tabs for the KNM list and the
candidate pool. It offers search (case- and accent-insensitive), filters on
`pos`, `thema`, `domein`, `prioriteit`, `niveau` and `herkomst`, sortable
columns, and a summary panel with the per-theme and per-domain counts.

It is generated, never hand-edited:

```sh
python3 tools/lexicon/bouw-viewer.py     # -> tools/lexicon/index.html
```

Re-run it after any change to the TSVs; the build asserts the headers, the row
counts and the row alignment, and fails if a hand-edit has broken the data.

**Every facet must offer a `(geen)` option for a value that can be blank.** The
first version of the `niveau` filter did not, and because that column was the
coursebook tier — blank for 4,839 rows — those rows were counted in `all (N)`
and appeared under no option. The counts looked wrong and were. `trede` now
shows `(geen)`, every facet partitions exactly, and a throwaway headless
harness confirmed it against the rendered page.

`pos` is one of `noun`, `verb`, `adj`, `adv`, `name`, `function`,
`interjection`, `phrase`. `thema` is one of the 24 themes in
`Docs/product.md` §12 plus `algemeen`, `naam` and `plaats`. `domein` is one of
the 30 semantic domains listed in `domein.py`. `prioriteit` is `kern`, `nuttig`
or `laag`. **`niveau` in the viewer is ours** (five frequency bands); the
coursebook's own A1/B1/open tier is shown beside it as `trede`. The `niveau`
column in `woorden.tsv` is that tier, not a level — see §"Our level scale".

## The pipeline

Run in this order. Every step reads and rewrites files in this directory.

```sh
# 1. the coursebook appendix + the games' word banks -> woorden.tsv (7,107)
#    the appendix PDF is not in the repo; pass its path
python3 tools/lexicon/extraheer-woorden.py \
    "/path/to/Bijlage-8-Frequente woorden (1).pdf"

# 2. + the KNM vocabulary -> woorden.tsv (7,232)
python3 tools/lexicon/knm-woorden.py

# 3. + the frequency extension -> woorden.tsv (10,000)
python3 -m pip install --target /tmp/wf wordfreq
python3 tools/lexicon/verrijk-woorden.py --wordfreq /tmp/wf --target 10000

# 4. part of speech -> woorden-woordsoort.tsv
python3 tools/lexicon/woordsoort.py

# 5. theme and priority -> woorden-thema.tsv
python3 tools/lexicon/thema.py

# 6. semantic domain -> woorden-domein.tsv (needs 1 and 5)
python3 tools/lexicon/domein.py

# 7. frequency score -> woorden-frequentie.tsv (needs 1)
#    wordfreq is installed once, to a throwaway directory
python3 -m pip install --target /tmp/wf wordfreq
python3 tools/lexicon/frequentie.py --wordfreq /tmp/wf

# 8. our five bands -> woorden-niveau.tsv (needs 1 and 7)
python3 tools/lexicon/niveau.py
```

**Re-running step 1 rewrites `woorden.tsv` from scratch and drops everything
steps 2 and 3 added.** Run 2 and 3 again afterwards. Steps 4, 5 and 6 must then
be re-run because they are keyed on row order.

Each step is deterministic. No network access after the `pip install`.

## Where the words come from

| `herkomst` | Rows | Source |
|---|---|---|
| `bijlage8` | 4,709 | `Nederlands in actie`, Bijlage 8 — the 5,000 most frequent Dutch lemmas, C. Tiberius & T. Schoonheim (2014), *A Frequency Dictionary of Dutch*, Routledge. Grading read from the page fill: light blue = *Nederlands in gang* (A1), orange = *Nederlands in actie* (B1), unmarked = `open` |
| `spel:<game>` | 2,398 | the six games' own word banks, in `server/Oefenpad.Resources/Games/Data` |
| `kaikki` | 2,768 | English Wiktionary via kaikki.org, chosen by `wordfreq` zipf rank, cut-off 3.29 |
| `knm` | 125 | the TaalCompleet KNM word lists (Nederlands + Engels), extracted to `knm-kandidaten.tsv` |

`niveau` = `open` in `woorden.tsv` means "in the 5,000 most frequent lemmas but
taught in neither coursebook", a candidate pool for B1+. **It is not a B2
label**, and the viewer calls that column `trede` for exactly that reason. No
public B2 word list exists: CEFR publishes none, the Groene Boekje is spelling
only, and SUBTLEX-NL, Routledge and NT2Lex are all restricted (NT2Lex is
CC BY-NC-SA, out on licence grounds). B2 receptive vocabulary is usually put at
8,000–10,000 lemmas, which is where the 10,000 target comes from — it is a
*target*, not a measurement.

**The `kaikki` 2,768 were not chosen one by one.** They are the most frequent
2,768 of the 10,375 usable candidates, ranked with `wordfreq` and cut at zipf
**3.29**; 7,607 candidates were left unused. `bronnen.md` has the arithmetic, the
source table and the provenance counts, and
`python3 tools/lexicon/verrijk-woorden.py --wordfreq /tmp/wf311 --report`
reproduces it without writing anything.

## Our level scale

The coursebook's tiering (`A1`, `B1`, `open`) is not a level. It says which of
two books teaches a word, it borrows CEFR's names without CEFR's meaning, and it
is blank for 4,839 of the 10,000 rows. `niveau.py` therefore writes a second,
separate axis — **`niveau`, ours**, cut by frequency rank from
`woorden-frequentie.tsv`:

| band | rank | roughly | rows |
|---|---|---|---|
| Start | 1–1,000 | A0–A1 | 1,006 |
| Basis | 1,001–2,500 | A1–A2 | 1,505 |
| Midden | 2,501–5,000 | A2–B1 | 2,501 |
| Gevorderd | 5,001–8,000 | B1–B2 | 3,016 |
| Verdieping | 8,001–10,000 | B2 and past it | 1,972 |

Every row has exactly one band, which is why the viewer's filter counts add up.
The rank is wordfreq's Dutch score, not the appendix order, so the band answers
"when does a learner meet this word", not "where does a coursebook put it". The
`trede` column keeps the coursebook answer beside it.

**These cut points were settled on 17 November 2026.** They are a product
decision, not a data one, and the alternatives were weighed: bands taken from
the appendix's own 5,000 tiers with the game banks weighted differently, and
even 2,000-word bands instead of 1,000 / 1,500 / 2,500 / 3,000 / 2,000. Both were
set aside — an uneven ladder follows the rate at which vocabulary actually
accumulates (fast at the start, slow at the top), and the appendix has no
tiering above 5,000 to borrow. The cost of the choice is the second consequence
below: the boundaries are ranks *in this list*, so growth to 12,000 moves them.

**The CEFR ranges are an approximation of convenience, not a measurement.** They
are checked against the appendix tiers, and the check is unflattering:

- **79%** of the words the A1 coursebook teaches are in Start or Basis (729 of
  927). The rest are frequent enough to be in Midden or beyond.
- **42%** of the B1 coursebook's words are in Midden or beyond (323 of 765).
  A B1 coursebook teaches a lot of very frequent words, because B1 is about
  using them, not only meeting them.

So a band is a frequency statement. Never print a CEFR label next to a lemma on
the strength of its band; the ranges above exist so the scale can be read at a
glance, not so a word can be certified.

186 lemmas have no wordfreq score at all — game compounds such as
`ankylosauride`, and a few misspellings such as `belangstellilng`. They rank last
and land in Verdieping, which is what "absent from the corpus" means. The 23 of
them that are appendix words, and the 5 that are KNM words, take their band from
that evidence instead; `grondslag` in `woorden-niveau.tsv` says which rule fired
(`rang`, `trede`, `knm`, `spel`). `niveau.py --why <word>` prints it.

Two consequences worth knowing before this axis is used for planning:

- **The game banks are not a frequency ladder.** With `domein = Animals` and
  `thema = algemeen`, 300 of 435 words are Verdieping: the games deliberately
  carry exotic species (`ankylosaurus`, `zeekomkommer`). Pictures make a rare
  word learnable; frequency still calls it rare.
- **The cut points are ranks in this 10,000.** Growing the list to 12,000 moves
every boundary. Re-run `frequentie.py` and `niveau.py` and re-read the
  calibration table before trusting the bands after a rebuild.

## Licence — unresolved, and it matters

- **`bijlage8` rows** are a derived extraction from a copyrighted Routledge
  dictionary. Internal use only.
- **`knm` rows** are a derived extraction from TaalCompleet's KNM word lists. No
  licence is stated; treat them as internal, like the appendix.
- **`kaikki` rows** are CC BY-SA 4.0 + GFDL. Because they are merged into the
  same files, **the three 10,000-row files are copyleft**.
- **`wordfreq`** supplies the ranking only. Its data derives from Wikipedia,
  ParaCrawl, OpenSubtitles, SUBTLEX-NL and Google Books Ngrams.

The attribution wording, and what each obligation attaches to, is in
`bronnen.md` §Attribution and `aanvulling.md` §Attribution.

Nothing here has been cleared for publication. This needs an owner decision
before any of it ships, and the two extractions cannot ship at all as they
stand.

## How good the classification is

Measured on 16 November 2026 by hand-scoring fixed-seed samples; re-run the
sample print at the end of `thema.py` to check again.

- **part of speech**: 98% correct on appendix rows, 88% on `kaikki` rows. The
  errors are adjectives tagged `noun` (`flexibel`, `getalenteerd`,
  `doelgericht`), adverbs tagged `noun` (`jazeker`, `idem`), and `-weg`
  compounds tagged `adv`.
- **theme**: reliable on the appendix and games rows, because the classifier's
  seed tables were built for them. On `kaikki` rows it is weak: in a sample of
  33 named themes, 16 were wrong (`terugweg` → `Het lichaam`). Treat a `kaikki`
  row's theme as a hint, not a fact.
- **`knm` rows** carry the hand-checked theme in `knm-thema.tsv`; `thema.py`
  reads it and nothing else assigns those rows.
- **priority**: `kaikki` rows are capped at `nuttig` because they lie beyond the
  appendix's 5,000 most frequent lemmas, so they cannot be the teaching core.
  Before that rule, 95 of 100 sampled `kaikki` rows were `kern` and `laag` held
  2 rows out of 2,893.

## The domain axis

`thema` is a *situation*: a supermarket, a doctor's appointment, a form. It
leaves 7,421 words in `algemeen`, which is a bucket, not a category — too large
to browse or to build a theme around. `domein` is the *semantic field*: what
kind of thing the word names, whatever the situation.

It is a second axis, not a replacement. The product's theme list is fixed by
`Docs/product.md` §12 and is not extended here.

`domein.py` is deterministic: structural rules first, then ~100 curated
overrides, then 27 keyword rules, then 13 Dutch compound suffix rules, then the
game seed, then a coarse theme seed, then `Abstract & general`. `--why <word>`
prints which step fired.

Current distribution: only **3,236 of 10,000 (32.4%)** are `Abstract & general`.
The other 6,764 spread across the remaining 29 labels; the largest is `Animals`
at 446 (4.5%), the smallest `War & military` at 79 (0.8%). All 30 labels are
used.

Accuracy, from three blind stratified audits by an independent agent (8, 12 and
12 random rows per label, fresh seeds): 69–81% correct, 12–20% acceptable,
**6.4–12.5% wrong**. The third audit, run after the fixes below, put it at
81.4% correct, 12.2% acceptable, 6.4% wrong on 360 rows.

The collision fixes came in two rounds on 17 November 2026: remove the
ambiguous alternative from the rule (bare `court` from Sport, bare `policy`
from Money, `minister` from Religion, `stage` and `example` from Arts and
Character, `department` from Education) or add a curated override where the
gloss itself misleads (`bewerkstelligen`, `opstarten`, `voorbeeld`). Notable
structural changes: body-part `hand` is no longer matched by the general Body
rule, which was pulling in every gloss containing "on the other hand".

The nine concrete domains the audits found clean are `Animals`, `Arts & media`,
`Food & drink`, `House & home`, `Movement & position`, `Names`, `Technology &
tools`, `Time` and `Transport & travel`.

An earlier method — slicing the list into six files and having an agent label
them — was discarded on 17 November 2026: it was not reproducible and its
labels were close to random (`atoom` → Names, `zus` → Food & drink). The slices
were deleted. Do not restore that method. `domein.py` is the only source of
`woorden-domein.tsv`.

## The theme gap, stated plainly

Only **2,192 of 10,000** words sit in one of the 24 product themes. The other
7,808 are `algemeen` (7,421), `naam` (313) or `plaats` (74). This is the gap the
domain axis above addresses for browsing and for content planning; it does not
change the theme labels themselves.

This is not a classifier failure to be tuned away. The 24 themes are *situations
and concrete domains* — a supermarket, a doctor's appointment, a form — and the
lemmas that a 10,000-word B2 list adds beyond the coursebook are mostly
**abstract** (`toepassing`, `polarisatie`, `voorwaarde`). They have no home in
the 24, and `algemeen` is the honest label for them.

Six themes remain thin and **cannot be filled from open word lists**: `Bellen`
(7), `Afspraken` (7), `Buurt` (11), `Solliciteren` (15), `Klachten` (17),
`Formulieren` (19), `Zorg voor iemand anders` (19). They name situations rather
than semantic domains, so they have to be drafted by hand from the material a
learner actually meets. The KNM list was the one source that moved several of
them (`Formulieren` 12 → 19, `Zorg voor iemand anders` 10 → 19, `Solliciteren`
9 → 15) and it is now exhausted.

## Do not

- Do not edit `woorden.tsv` by hand to fix a theme or a part of speech. Fix the
  table in `thema.py` / `woordsoort.py` and re-run, or the next run undoes it.
- Do not re-run `extraheer-woorden.py` without running steps 2 and 3 after it.
- Do not treat `trede` as a CEFR label. `open` means "not taught in either
  coursebook"; `A1` and `B1` mean "filled light blue / orange in Bijlage 8".
- Do not treat `niveau` as a measurement either: it is a frequency band with an
  approximate CEFR range attached, not a level test result.
- Do not serve this directory from the web app. Only `assets/` and the WebUI
  `wwwroot` are exposed, deliberately.
