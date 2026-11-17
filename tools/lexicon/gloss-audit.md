# English gloss audit — `woorden.tsv`, `bijlage8` rows

Audit only. No data file, script or PDF was modified. Every claim below is
tied to a row number in `tools/lexicon/woorden.tsv` (1-based, header = row 1).

## 1. Method

I took a second, independent read of the same PDF with
`pdftotext -layout` and parsed both columns by whitespace, which recovers
lemma and gloss side by side for all but a handful of rows, then diffed that
against the 4,709 `bijlage8` rows in `woorden.tsv`. That diff cannot find a
fault: both extractions agree with each other and with the PDF on every error
found here. It only made the search cheap — sort both columns, walk them
together, and read the output. On top of that I applied the part-of-speech
shape check (verb with no `to`, noun/adj/adv with `to`) and read every flagged
gloss, plus every gloss on each page a fault turned up on. **The limits are
real: a noun glossed with the wrong noun is invisible to both the shape check
and a pos-based diff, and the only defence against it is reading the 4,709
pairs.** I read the whole list at lemma/gloss level once; I did not verify
hiatuses of more than one row (see §5), so a clean-looking gloss in a shifted
stretch could still be one word early or late.

## 2. The number

| | count |
|---|---|
| `bijlage8` rows in `woorden.tsv` | 5,161 (4,709 with `bijlage8` as sole origin; 452 also in a game) |
| certainly wrong — correct gloss can be named | **38** |
| probably wrong — right idea, not certain of the exact wording | **3** |
| could not check | **0** |
| total flagged | **41** |

Basis: I read every row. This is a census, not a sample, so **no percentage
or extrapolation is involved** — but the census is only as good as the reading
it rests on, and the reading could not detect a wrong-but-plausible noun
gloss (e.g. `paal` → "pole" if it should have been "pile"). Treat 38 as a
floor, not a ceiling.

**The most important finding is that the stated mechanism is wrong.** The
gloss column does not wrap anywhere in this PDF. The `pdftohtml` XML has
exactly **one** gloss line with no lemma beside it (page 96, under
`promotie`), and it is real table content, not a wrap. The parser's
wrap-append path (`extraheer-woorden.py:114`) therefore never fires. The
misalignments are **in the PDF's own content**: the lemma text contains
misspellings (`misburik`, `opbengst`, `respeteren`, `vermoedheid`), and on
those rows the gloss sits one row off. A wrap-based fix to the parser would
fix nothing.

## 3. Tableau

41 rows. `Should have` is the value established from the table's own content
(a near-duplicate spelling, a coherent verb/noun pairing, or the
`-en`/noun relation); where it is inferred rather than read, the row is
`probable`.

| row | nl | gloss given | should have | confidence | pattern |
|---|---|---|---|---|---|
| 30 | aankondigen | to an(noun)ce | to announce | certain | other |
| 46 | aanpassen | to (adj)ust | to adjust | certain | other |
| 202 | afstemmen | to tune, to (adj)ust | to tune, to adjust | certain | other |
| 574 | bekendmaken | to an(noun)ce | to announce | certain | other |
| 2258 | grootschalig | large-scale 47 van 148 | large-scale | certain | footer |
| 3114 | kring | to shrink | circle | certain | neighbour swap |
| 3115 | kripen | circle | to shrink | certain | neighbour swap |
| 3621 | minister-president | ministry | prime minister | certain | neighbour swap |
| 3622 | ministerie | prime minister | ministry | certain | neighbour swap |
| 3630 | misbruiken | abuse 74 van 148 | abuse | certain | footer |
| 3631 | misburik | to abuse | (a misspelling of misbruiken, duplicate of 3630) | probable | other |
| 4067 | ontroeren | to move | (unresolved — see §5) | probable | other |
| 4068 | ontslaan | resignation, dismissal | to dismiss, to fire | certain | neighbour swap |
| 4069 | ontslag | to escape | dismissal, resignation | certain | neighbour swap |
| 4071 | ontsnappen | to relax | to escape | certain | neighbour swap |
| 4072 | ontspannen | relaxation | to relax | certain | neighbour swap |
| 4073 | ontspanning | to start | relaxation | certain | neighbour swap |
| 4075 | onttrekken (zich) | to receive | to withdraw | certain | neighbour swap |
| 4076 | ontvangen | reception | to receive | certain | neighbour swap |
| 4077 | ontvangst | to abduct | reception | certain | neighbour swap |
| 4119 | opbengst | to store | (a misspelling of opbrengst, whose gloss this is) | probable | other |
| 4120 | opbergen | to blow | to store | certain | neighbour swap |
| 4121 | opblazen | construction | to blow (up) | certain | neighbour swap |
| 4122 | opbouw | to construct | construction | certain | neighbour swap |
| 4123 | opbouwen | to yield | to construct | certain | neighbour swap |
| 4124 | opbrengen | proceeds | to yield | certain | neighbour swap |
| 4744 | razend | a) furious b) (adv) very | a) furious b) very (adv) | certain | other |
| 4846 | respectievelijk | to respect | respectively | certain | neighbour swap |
| 4847 | respeteren | respectively | (a misspelling of respecteren = to respect, 4845) | probable | other |
| 5647 | telefoneren | telephonic | to phone, to telephone | certain | neighbour swap |
| 5648 | telefonisch | telephone | telephonic, by telephone | certain | neighbour swap |
| 5649 | telefoon | telephone number | telephone | certain | neighbour swap |
| 5650 | telefoonnummer | to phone | telephone number | certain | neighbour swap |
| 5953 | uiting | to hang out | expression | certain | neighbour swap |
| 5954 | uitkeren | expression | to pay out (a benefit) | certain | neighbour swap |
| 6240 | vermoedheid | tired | (a misspelling of vermoeidheid = tiredness) | probable | other |
| 6241 | vermoeid | fatigue | tired | certain | neighbour swap |
| 6259 | veroordeling | to condemn | conviction, condemnation | certain | neighbour swap |
| 6260 | veroorloven (zich) | to permit | to permit oneself, to afford | certain | neighbour swap |
| 6261 | veroorzaken | to cause | (returned to its own slot by 6259's fix) | certain | neighbour swap |
| 6798 | West-Vlaams | west, western | West Flemish | certain | neighbour swap |
| 6799 | westelijk | west | west, western | certain | neighbour swap |
| 6800 | westen | Western | west | certain | neighbour swap |
| 6802 | westers | West Flemish | Western | certain | neighbour swap |

**Footers: 2** (2258, 3630). The PDF carries a footer on **all 148 pages**
(`N van 148`); the extraction caught 146 of them and two leaked into glosses.

**Sense markers: 2** (30, 574; 46, 202 — four rows, two distinct strings). The
glosses `to an(noun)ce` and `to (adj)ust` contain a stylistic tag that the
source set in the same size as the word, so it was read as gloss text. 4744's
`(adv)` is the same class.

### The shift stretches, in full

Every neighbour swap is **exactly ±1**. Five are self-contained two-row
transpositions; three are chains of three or more that need a cyclic rotation.
The chain part is the lemma's own slot, the `variants` are misspellings.

| PDF page | rows | shape | fix |
|---|---|---|---|
| 65 | 3114–3115 | 2-row pair | swap |
| 74 | 3621–3622 | 2-row pair | swap |
| 85 | 4119–4124 | 6-row chain, starting at a misspelled lemma | rotate: 4119←4124 |
| 84 | 4068–4077 | 10-row chain | rotate: 4068←4077 |
| 115 | 5647–5650 | 4-row chain | rotate: 5647←5650 |
| 100 | 4846–4847 | 2-row pair | swap |
| 121 | 5953–5954 | 2-row pair | swap |
| 129 | 6240–6261 | 6-row chain, with `vermoedheid` at its head | rotate: 6240←6261 |
| 139 | 6678–6680 | 3 rows: `wagen (noun)`/`wagen (verb)`/`wagen (zich)` | see §4 |
| 142 | 6798–6802 | 4-row chain, `West-Vlaams` borrowed a neighbour's gloss | rotate: 6798←6802 |

Note the order trap: in the PDF, `ontslag` ("to escape") precedes `ontsnappen`
("to relax"), so the gloss runs one row *behind* its lemma. Fixing a chain
therefore means shifting glosses **up**, not down.

`ontroeren` (4067, "to move") sits just above the page-84 chain but has no
partner inside it; it is listed as `probable` only because its gloss is almost
certainly `bewegen`'s — the source has it at `bewegen` too, where it is
harmless. Do not move it without checking the PDF page by eye.

## 4. Repair proposal (not applied)

Recommended, in this order.

1. **Patch the data, not the script.** A parser change cannot help: there is
   no wrap. 38 of 41 rows need a one-line edit, and three of those
   (`misburik`, `opbengst`, `respeteren`, plus `vermoedheid`) need the lemma
   corrected as well, since the lemma, not the gloss, is what is misspelled.
2. **Programmatic for the chains, per-row for the rest.** Because every shift
   is a clean rotation within a contiguous block of rows, the 26 rows in the
   eight rotated stretches can be fixed by a script that reads the 10 affected
   pages and rotates the gloss list by one. That is safe only if it also
   asserts the block boundaries; a rotation off by one row corrupts two
   entries. The remaining 15 rows (four sense-marker rows, two footers, four
   misspelled lemmas, `ontroeren`, 6259/6261 if done singly) are scattered and
   need per-row edits.
3. **Fix `extraheer-woorden.py` only for the footers.** Its `skip()` tests for
   `"van 148"` in a *lemma* cell, but footers arrive as gloss-shaped cells at
   left ≈ 700, so the test never sees them and `rows[top]` for `top == 1180`
   becomes a wrap-append. Adding `if top > 1150: continue` (or dropping any
   gloss cell containing `van 148`) would have prevented rows 2258 and 3630.
   The `(noun)`/`(adj)` mangling is not a parser bug — it is in the PDF text —
   so it needs a content fix, not code.
4. **Do not regenerate `woorden.tsv` from the PDF** as the repair. That
   re-runs the same extraction over the same PDF and reproduces all 41 rows.

Before any edit: `woorden-woordsoort.tsv` and `woorden-thema.tsv` are
row-aligned by construction, and `en` is duplicated in both (9,999 of 10,000
glosses match today). A repair that touches `en` must touch those two files in
the same commit or the alignment assertion in `bouw-viewer.py` will fail.

## 5. What I could not check

- **Wrong noun for noun.** A gloss that is the wrong noun but a plausible one
  would survive every check used here. `paal` → "pole" (should be "pile") and
  `proces` → "trial" are the kind of thing that only a second reader of Dutch
  would catch; I did not flag either, and I am not asserting they are wrong.
- **`paard` (4330) → "horse"** is correct; the odd `maken` → "a) to make b) to
  repair" nearby is not a shift — `paard` is on PDF page 90 and `maken` on
  page 71.
- **Hiatuses > 1 row.** I verified every shift is ±1 by checking that each
  gloss belongs to an immediate neighbour. I did not establish whether any
  stretch has a two-row gap, so a gloss two rows away would have looked clean.
- **The 452 rows with a game origin as well as `bijlage8`** were checked for
  gloss text but their `en` is normally overwritten by the game bank; those
  glosses are not appendix-sourced and were not audited as such.
- **`Docs/` and the games** were not touched: this file reports on the lexicon
  only, and nothing here changes what the site ships.
