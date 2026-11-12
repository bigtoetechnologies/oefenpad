# Prepositions art plan — review findings

10 November 2026, audit; same day, **every step of the recommendation applied**.
The audit ran against the rule in `prepositions-art-handover-2026-11-10.md` and the
curriculum in `prepositions-roadmap.md`. Three further defects the first pass
missed are marked **New** below and were fixed in the same sweep.

Scope: every tracked frame in the three art plans plus the 30 shipped pilot
frames.

| File | Rows |
|---|---|
| `Docs/prepositions-art-a0-a2.md` | 20 |
| `Docs/prepositions-art-b1.md` | 200 |
| `Docs/prepositions-art-b2.md` | 460 |
| `server/Oefenpad.Resources/Games/Data/prepositions.json` (pilot) | 30 |

Total **710** tracked frames, **585** distinct chunk strings. `prepositions.json`
is untouched: still 30 scenes and 18 levels, and no artwork has been drawn.

## What was applied

| # | Fix | Where | State |
|---|---|---|---|
| 1 | 12 duplicated tracker Scene cells copied back from the blocks | `prepositions-art-b1.md` | done |
| 2 | 17 batch blocks synced to their tracker frame and filename | `prepositions-art-b2.md` | done |
| 3 | Two batch summaries that counted an eleventh subject | `prepositions-art-b2.md` B2-13, B2-26 (**New**) | done |
| 4 | 10 tracker Scene cells describing a different scene than the block, and 4 notes with them | `prepositions-art-b2.md` (**New**) | done |
| 5 | Pronominal adverbs written into the frame rule; 32 corrected to 29 | `prepositions-art-handover-2026-11-10.md` | done |
| 6 | 29 B1 bare separable verbs replaced by real preposition chunks | `prepositions-art-b1.md` | done |
| 7 | New batch B2-46 for the 9 unframed prepositions | `prepositions-art-b2.md` | done |
| 8 | `ten slotte` ×2 replaced (`ten laste van`, `gebaseerd zijn op`) | `prepositions-art-b2.md` | done |
| 9 | Batch 8 retheme, batch 32, totals | `prepositions-roadmap.md` | done |
| 10 | Separable word list handed to **Uit Elkaar** | `suggestions.md` | done |
| 11 | `ten einde te` replaced by `ten dienste staan van` | `prepositions-art-b2.md` | done |

After the sweep and that final replacement: **0** tracker↔block mismatches, **0**
duplicate Scene cells and **0** duplicate filenames across all three files; B1 is
200 rows / 20 batches / 40 fences and B2 is 460 rows / 46 batches / 92 fences.
The whole set is 710 frames including the 30 pilots. A whitelisted
no-preposition scan is clean for A0–A2, B1 and the B2 blocks; before the final
replacement its only remaining hit was `ten einde te` (#43), a fused-`ten`
conjunction.

## Bottom line

Every frame has an English explanation and a Scene/art note, and there are
**zero greeting/formula fakes** — `tot ziens` was correctly removed. Every
blocking fault found in the audit has been fixed:

- The **36 B1 frames with no bare preposition** were resolved: 29 bare
  separable verbs were replaced and the 7 pronominal-adverb frames stay.
- The **17 B2 batch blocks that had drifted** from their tracker rows were
  re-synced to the tracker.
- The **9 prepositions in roadmap §7** that no frame used are now framed in
  B2-46.

`ten einde te` (#43) was the last off-rule frame and has since been replaced by
`ten dienste staan van`. The plans are ready to send to Grok.

---

## 1. Does every frame have a preposition, an explanation, and an art design?

### Explanation and art design — complete

| File | Rows | Empty cells (frame / English / Scene / note / file) |
|---|---|---|
| `prepositions-art-a0-a2.md` | 20 | 0 |
| `prepositions-art-b1.md` | 200 | 0 |
| `prepositions-art-b2.md` | 460 | 0 |

Every row has a Dutch frame, an English gloss, a Scene and a pair/note.
`Status` is `needed` on all rows, which is expected before delivery.

### A governing preposition — complete

| Level | Frames with a real preposition | Frames without |
|---|---|---|
| A0–A2 | 20 / 20 | 0 |
| B1 | 200 / 200 | 0 (29 replaced; 7 pronominal adverbs whitelisted) |
| B2 tracker | 460 / 460 | 0 |
| B2 batch blocks | 460 / 460 | 0 |

A scripted "has a preposition?" pass is clean for A0–A2, B1 and the B2 blocks
once the pronominal forms are whitelisted.

**Correction to the first pass:** `ergens klaar mee zijn` (#403) does carry a
preposition, inside `mee`; the two rows a whitelisted scan flagged were
`ten slotte` #46 and #450. `ten slotte` is a fixed adverbial with a fused
preposition (`te` + `den`), not a chunk that governs one; both were replaced.
The same test then left `ten einde te` (#43), which has now been replaced by
`ten dienste staan van`.

### The 36 B1 frames that had no preposition (fixed)

| Batch | # | Frames |
|---|---|---|
| B1-07 | 7 | #61 `ergens naartoe`, #62 `ergens vandaan`, #63 `ergens mee bezig`, #66 `waar … naartoe`, #67 `waar … vandaan`, #69 `erover nadenken`, #70 `eraan toe zijn` |
| B1-08 | 10 | #71 `opbellen`, #72 `aankomen`, #73 `weggaan`, #74 `terugkomen`, #75 `opruimen`, #76 `thuiskomen`, #77 `opschrijven`, #78 `uitdoen`, #79 `meenemen`, #80 `uitleggen` |
| B1-11 | 4 | #106 `ophangen`, #107 `afwassen`, #108 `invullen`, #110 `afslaan` |
| B1-12 | 3 | #113 `afslaan`, #114 `invullen`, #118 `ophangen` |
| B1-14 | 2 | #131 `dwarszitten`, #138 `zich vervelen` |
| B1-15 | 1 | #149 `zich afvragen` |
| B1-16 | 1 | #157 `afwassen` |
| B1-17 | 5 | #162 `oprotten`, #163 `afronden`, #164 `uitpakken`, #165 `inpakken`, #166 `zich aankleden` |
| B1-18 | 1 | #180 `zich vervelen` |
| B1-19 | 1 | #184 `vergeten` |
| B1-20 | 1 | #197 `ophangen` |

**Correction to the handover:** it says "B1 has 32 frames with no preposition —
13 in B1-07/08". The real number is **36**, and **17** of them are in B1-07/08.
The handover misses the pronominal-adverb group in B1-07. Of the 36, **29 are
bare separable verbs** and **7 are pronominal-adverb frames** (see §3).

All 29 bare separable frames in the table were replaced on 10 November. The
seven B1-07 pronominals remain, because a pronominal adverb carries its
preposition inside `er…`, `daar…` or `waar…`.

B1-08's own VALIDATION line — "Does the direction of action in the drawing match
the **prefix**, not just the verb stem?" — confirms these were written as
separable-prefix frames, not preposition frames.

---

## 2. Are the frames correct? (tracker ↔ batch block)

B1 block↔tracker: **0 mismatches across all 200.** Clean.

B2: **17 mismatches, all now fixed** by rewriting the block's filename and
chunk to the tracker's. 16 had a different file *and* a different chunk; #227
differed only in chunk wording. The Scene, Must-read and Avoid lines already
matched the tracker's scene, so only two Must-read lines needed rewording with
the restored chunk (#121 "acting in a role" → "being in charge of a group",
#146 "completing a form" → "signing yourself in at a counter"), plus four
CONTRAST PAIRS lines that named a drifted chunk.

| # | Tracker frame (correct side) | Batch-block chunk | File mismatch? |
|---|---|---|---|
| 115 | `afwegen tegen` | `afwegen` | yes |
| 116 | `besluiten tot` | `besluiten` | no |
| 121 | `leidinggeven aan` | `functioneren als` | yes |
| 124 | `een punt zetten achter` | `afronden` | yes |
| 125 | `inplannen in` | `inplannen` | yes |
| 126 | `inwerken in` | `inwerken` | no |
| 130 | `een vergoeding krijgen voor` | `vergoeden` | yes |
| 136 | `ingrijpen bij` | `ingrijpen` | no |
| 142 | `een einde maken aan` | `een contract beëindigen` | yes |
| 143 | `verlengen met` | `verlengen` | yes |
| 146 | `zich aanmelden bij` | `invullen` | yes |
| 147 | `in ontvangst nemen` | `opvangen` | yes |
| 148 | `overdragen aan` | `doorgeven` | yes |
| 176 | `zich neerleggen bij` | `loslaten` | yes |
| 227 | `ter beschikking stellen van` | `ter beschikking stellen` | no |
| 239 | `de waarde bepalen van` | `een taxatie laten uitvoeren` | yes |
| 260 | `aandragen voor` | `aandragen` | yes |

Two consequences:

- **The file mismatches** (#115, 121, 124, 125, 130, 142, 143, 146, 147, 148,
  176, 239) fork the asset name from the tracker, so the shipped scene id would
  not resolve.
- **`functioneren als` (#121) is not a preposition frame at all.** `als` is not
  in this curriculum's preposition set, and it contradicts the tracker's
  `leidinggeven aan`.

**Also wrong, both fixed:** B2-13's CONTRAST PAIRS said "One, four, five,
eight, nine, ten and **11** are singles"; the batch has ten subjects. **New:**
B2-26 has the same fault and the first pass missed it — "Nine, ten and **11**
are handing-over singles" went on to describe a third image, "a folder pushed
across a desk", that no subject in the batch asks for. An artist working from
that block would have drawn an eleventh picture.

Aside from the drift, the frames use standard Dutch collocations. The unusual
ones were spot-checked and are valid: `beschikken tot` (#53), `noodzaken tot`,
`bewogen worden tot`, `benodigd zijn tot`, `zich verlagen tot`. A full native
collocation pass is beyond what a script can prove.

---

## 3. Are any frames not really prepositions? (the `tot ziens` question)

**No greetings or formulae anywhere.** A search of all 710 frames (including the
pilot) for `tot ziens`, `tot morgen`, `tot straks`, `tot later`, `tot nu toe`,
`tot volgende week` and `hoe gaat het` returned **zero hits**. `prepositions-art-a0-a2.md`
L58–68 documents the removal and what replaced it. This part is already correct.

What was off-rule fell into three buckets. The first two have been fixed; the
third stays.

### (a) 29 bare separable verbs in B1 (replaced)

The list in §1 minus the 7 B1-07 pronominals: `opbellen`, `afwassen`,
`invullen`, `ophangen`, `zich vervelen`, `oprotten`, `afronden`, `inpakken`,
`uitpakken`, `zich aankleden`, `vergeten`, … None governs a preposition. All 29
were replaced on 10 November.

### (b) 16 bare/other verbs in B2 batch blocks (fixed)

The §2 mismatches, minus #227 (which is a wording loss, not a bare verb).
Notably `functioneren als`, `een contract beëindigen`, `opvangen`,
`een taxatie laten uitvoeren`, `loslaten`, `aandragen`, `afronden`, `inplannen`,
`inwerken`, `vergoeden`, `ingrijpen`. All 16 blocks were re-synced to their
tracker chunk.

### (c) 8 pronominal-adverb frames — keep these

`ergens naartoe`, `waar … vandaan`, `erover nadenken`, `eraan toe zijn`
(B1-07) and `ergens klaar mee zijn` (#403). These have no *bare* preposition but
carry one inside a pronominal adverb. Roadmap §6 budgets 40 frames for
"Pronominal adverbs"; they are in scope. The fix is to add pronominal adverbs to
the handover's frame rule (L23–28), not to replace the frames.

**Conclusion:** the `tot ziens` class is gone, and the 29 B1 separables, 16 B2
block-side bare verbs and `als` in #121 have all been fixed. The last
non-preposition frame, `ten einde te` (#43), was replaced by `ten dienste staan
van`.

---

## 4. Are any verb+preposition chunks missing?

This is judgement-based: the repo has **no frequency list** (roadmap §12.1 says
re-cut everything when one arrives). Cross-checked against all 568 chunks and
the 30 pilots at audit time, **23 common chunks appeared nowhere**:

`wonen in`, `gaan naar`, `kiezen voor`, `hopen op`, `wijzen op`,
`vertrouwen op`, `bestaan uit`, `leiden tot`, `akkoord gaan met`,
`het eens zijn met`, `gebaseerd zijn op`, `afkomstig zijn uit`,
`vergelijken met`, `het verschil tussen`, `passen op`, `afgaan op`,
`zich verlaten op`, `ontstaan uit`, `ruimte voor`, `tellen als`,
`werken voor`, `twijfelen tussen`, `zich zorgen maken over`.

- **`kiezen voor`** was the standout: the corpus framed `kiezen tussen` /
  `kiezen uit`, `opteren voor` and `beslissen tot`, but never the most common
  form. It is now B1 #73.
- `werken voor` is deliberately excluded (too close to `werken bij`). The
  positive `zich zorgen maken over` was absent while `zich geen zorgen maken over`
  (#401) was present; it is now B1 #76.
- Beware substring false positives: `gaan naar` is *not* covered by
  `uitgaan naar` (#82), nor `wijzen op` by `afwijzen op grond van` (#354), nor
  `leiden tot` by `opleiden tot` (#149), nor `passen op` by `toepassen op`
  (#336).

Fifteen of the 23 are now framed, mostly by the B1 replacement: `wonen in`,
`gaan naar`, `kiezen voor`, `hopen op`, `wijzen op`, `vertrouwen op`,
`bestaan uit`, `akkoord gaan met`, `het eens zijn met`, `gebaseerd zijn op`,
`vergelijken met`, `passen op`, `ruimte voor`, `twijfelen tussen` and
`zich zorgen maken over`.
Eight remain absent: `leiden tot`, `afkomstig zijn uit`, `ontstaan uit`, `het
verschil tussen`, `afgaan op`, `zich verlaten op`, `tellen als` and `werken voor`.
The last two are deliberate exclusions; the other six are the frequency-list
backlog. Three further common chunks are also absent — `antwoorden op`, `wijzen
naar` and `gewend zijn aan` — though `gewend aan` is already framed (#25, #26,
#39).

### Preposition coverage gaps (roadmap §7)

**9 prepositions were never framed anywhere at audit time:** `zonder`, `vanwege`,
`gezien`, `richting`, `per`, `aangaande`, `betreffende`, `jegens`,
`overeenkomstig`.

- `zonder` was absent entirely (handover L49 and roadmap §7 both flag it).
- `vanwege`, `gezien`, `richting`, `per` are roadmap §7 **phase D**
  (batches 20–25); `aangaande`, `betreffende`, `jegens`, `overeenkomstig` are
  **phase E** (26–31). Both phases are B2, and no B2 frame used any of them.
  That was a roadmap gap, not just an art-plan gap.
- `met inbegrip van` and `ten opzichte van` *are* present, so §7's E-row was
  only partly unmet.

All nine are now framed in B2-46 (#451–#460), and the roadmap's batch 32
records the close-out.

`tot` appears 18 times, but **all in B2** — first at B2 **#13 `zich richten tot`**.
The handover's claim that `tot` has no frame below B2 is correct; the summary's
"first at #23" is off by ten rows.

B1 first-introduces many prepositions roadmap §7 assigns to A2 batch 5
(`achter, bij, binnen, boven, buiten, langs, na, naar, naast, om, onder, over,
rond, tussen, van, vanaf`). That is consistent with handover decision 2 ("keep
the B1-01/02 spatial frames — they're the only frames teaching those words"),
but it means A0–A2 covers only `aan, door, in, met, op, tegen, uit, voor`.

---

## 5. Other defects worth fixing in the same pass

### 12 duplicate B1 tracker Scene cells (off-by-one copy-paste) — fixed

The last subject of a batch took the first subject of the next batch's scene.
The batch blocks are correct and unique, so only the tracker Scene column was
wrong, and each cell was copied back from its block:

| Wrongly shared | Rows |
|---|---|
| `vanaf` ↔ `binnen` | #10 / #11 |
| `de hele dag door` ↔ `trots op` | #20 / #21 |
| `boos over` ↔ `verliefd op` | #30 / #31 |
| `kwaad op` ↔ `behoefte aan` | #40 / #41 |
| `gebrek aan` ↔ `kritiek op` | #50 / #51 |
| `schrik van` ↔ `ergens naartoe` | #60 / #61 |
| `eraan toe zijn` ↔ `opbellen` | #70 / #71 |
| `uitleggen` ↔ `beginnen met` | #80 / #81 |
| `praten tegen jezelf` ↔ `wachten op` | #90 / #91 |
| `praten met` ↔ `zich verheugen op` | #100 / #101 |
| `afslaan` ↔ `afspreken met` | #110 / #111 |
| `denken aan` ↔ `raken aan` | #120 / #121 |

B2 has **0** duplicated Scene cells.

### New: 10 B2 tracker Scene cells described a different scene — fixed

A duplicate-cell scan does not catch a cell that is merely stale, so the first
pass missed these. The B2 tracker Scene column is a condensed version of the
block's Scene; in ten rows it described something the block does not show. The
block is the considered side in every case — it is the one that matches the
chunk — so the tracker cell was rewritten from it, together with four Pair/note
cells that repeated the stale idea.

| # | Chunk | Tracker said | Block says |
|---|---|---|---|
| 62 | `afstand nemen van` | palm down, speaking precisely | palm turned outward, pushing the idea away |
| 259 | `benoemen tot` | a plain object into the hands | an armband slid up the upper arm |
| 301 | `stelling nemen tegen` | at a lectern, hand resting on a board | foot forward, both palms flat against the board |
| 305 | `weerleggen met` | lifts a block out of a sagging stack | lays a ruled sheet beside the stack and pushes it forward |
| 385 | `ruimte geven aan` | arms flung wide, speaking to a circle | steps back and makes room on the bench for another speaker |
| 407 | `niet voldoen aan` | the holder shrugs | the second figure's shoulders drop |
| 416 | `stilstaan bij` | a bench and a handless wall clock | standing before an old photograph on a panel |
| 424 | `uiting geven aan` | repeats a gesture in front of five seated figures | hands on the chest, one sustained sound, two listeners |
| 427 | `afgeven op` | a stone held ready to throw | speaking hard about a third figure who turns away |
| 430 | `afstappen van` | feet planted on the far side of the wheel | turns the wheel, then walks away towards a doorway |

Five tracker English glosses also read differently from their block
(`een definitie geven van`, `niet voldoen aan`, `stilstaan bij`,
`over de schreef gaan`, `afgeven op`); all five are synonyms and were left
alone. A sixth, #385 `ruimte geven aan`, said "to give voice to" against the
block's "to give space to" — two different chunks — and was set to the block's.

The remaining differences between the two columns are condensations, not
contradictions. Three of them drop the detail that carries the chunk — #269
`afscheid nemen van` loses the raised hand, #365 `afzien van` loses the push to
the desk edge, #402 `voet bij stuk houden` loses the planted foot. The blocks
are right; the tracker is only a summary, so these were left alone.

### Duplicates that are likely by design

Duplicate chunk strings are mostly intentional contrast variants. Notable
repeats: B1 `denken aan` ×11, `zorgen voor` ×4; B2 `zich beroepen op` ×4,
`zich richten tot` ×3. A few look like pure duplicates rather than contrast
pairs (`bereid tot` #183/#184, `geschikt voor` #185/#186, `rekening houden met`
#224/#225). That is a curation call, not an error.

### Filenames

No duplicate filenames in any file; all ASCII. Pilot filename references resolve
against `assets/voorzetselpaden/` and `prepositions.json`.

---

## Recommendation (safe order)

1. ~~Fix the 12 duplicate B1 tracker Scene cells.~~ **Done.**
2. ~~Fix the 17 B2 tracker↔block mismatches, and the "11" in B2-13.~~ **Done**,
   plus the same fault in B2-26 and the 10 stale B2 Scene cells.
3. ~~Document pronominal adverbs in the handover rule; correct "32".~~ **Done.**
4. ~~Decide the 29 B1 bare separable verbs.~~ **Done:** replaced, and the
   prefix material moved to **Uit Elkaar**. B1-08 was rebuilt whole; nineteen
   more frames were replaced across B1-11…B1-20. Twenty-two of the 29 came from
   the missing-chunk list in §4; the other seven are `kloppen op`,
   `hulp vragen aan`, `passen bij`, `drukken op`, `spelen met`, `kijken op` and
   `zich vergissen in`. `kijken op` is deliberately placed beside
   `kijken naar` in B1-18 so one verb carries two prepositions.
5. ~~Close the roadmap §7 D/E coverage gap.~~ **Done:** batch B2-46, ten frames,
   in the style of B2-44.
6. ~~Decide `ten slotte`.~~ **Done:** replaced by `ten laste van` (#46, which
   keeps B2-05's `ten … van` theme) and `gebaseerd zijn op` (#450).
7. ~~Decide `ten einde te`.~~ **Done:** replaced by `ten dienste staan van`
   (#43), which keeps B2-05's `ten … van` theme and governs its `van`.

The frequency-list backlog is `leiden tot`, `afkomstig zijn uit`, `ontstaan uit`,
`het verschil tussen`, `afgaan op` and `zich verlaten op`, plus three common
chunks the original list did not name: `antwoorden op`, `wijzen naar` and
`gewend zijn aan` (though `gewend aan` is already framed). `tellen als` and
`werken voor` stay out — `als` is not in the preposition set, and `werken voor`
sits too close to `werken bij`.

All three art plans are now ready to send to Grok. The next step is external:
draw the images and load the delivered frames into `prepositions.json`.

---

## Reproducing the checks

```sh
cd repos/oefenpad

# Row and fence counts (a0-a2 20/4, b1 200/40, b2 460/92)
for f in Docs/prepositions-art-a0-a2.md Docs/prepositions-art-b1.md Docs/prepositions-art-b2.md; do
  echo "$f $(grep -c '^````' "$f") $(awk -F'|' '/^\| [0-9]+ \|/ && $2 ~ /^ *[0-9]+ *$/ {c++} END{print c+0}' "$f")"
done

# Duplicate filenames (expect empty)
awk -F'|' '/^\| [0-9]+ \|/ && $2 ~ /^ *[0-9]+ *$/ {f=$3; gsub(/^ +| +$/,"",f); print f}' \
  Docs/prepositions-art-b2.md | sort | uniq -d
```

The no-preposition, tracker↔block, duplicate-Scene and coverage checks were run
with a small Python parser over the tracker tables and the `## Batch` subject
blocks. Key points for re-running:

- Whitelist **`tegenover`** — it is a real preposition, so a naive scan falsely
  flags #358. Whitelist the pronominal forms too (`naartoe`, `vandaan`, `mee`,
  `toe`, and any `er…`/`daar…`/`waar…` chunk), or the scan reports the eight
  pronominal frames as failures. Before the 10 November replacements it also
  reported 36 B1 failures; after them it is clean.
- Compare the tracker Scene cell against the block Scene as well as the
  filename and chunk. It is a condensed copy, so match it as a prefix and read
  the misses by hand: most are legitimate condensations and ten were stale.
- Block subjects renumber from 1, so compare block subject `N` to tracker row
  `batch_start + N − 1`.
- Only treat a backticked token as a filename if it is ASCII-hyphenated or ends
  in `.png`; backticks in the Pair/note column are usually prepositions.
