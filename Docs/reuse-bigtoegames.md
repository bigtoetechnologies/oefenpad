# Reuse from BigToe Games

What in `/media/tony/Data/repos/bigtoegames` is worth copying into Oefenpad, what
needs adapting, and what it does not solve. Assumes both repos are yours; if any
art or word images came from a third-party generator, check that tool's terms
before shipping.

BigToe is vanilla HTML/CSS/JS with no framework and no bundler. The only build
step is `sh deploy.sh`. That matches `mvp.md`'s "one page, no backend" shape, so
the code is unusually easy to move.

## The short version

BigToe already has **four of the thirteen planned games**, complete with Dutch UI
strings, category pickers, difficulty levels, timers, saved state, stats, sound
effects and PWA support:

| Planned game | BigToe equivalent | State |
|---|---|---|
| Galgje | `src/hangman/` | Working |
| Woordzoeker | `src/wordsearch/` | Working |
| Koppelen | `src/matchup/` | Working word ↔ picture |
| Geheugen | `src/memory/` | Ported and adapted: word ↔ picture |

Roughly 3,800 lines of game JavaScript and 2,500 lines of CSS, plus a shared
word bank, image manifest, helpers, service worker and test harness. That is the
head start. The other nine games — prepositions, word order, endings, Lego words,
false friends, flashcards, gap fill, listening, story machine — are either not
there or exist only as separate unrelated pages.

## Copy almost as-is

| What | Source | What you get | Changes needed |
|---|---|---|---|
| Hangman | `src/hangman/` (`index.html`, `style.css`, `script.js`) | Category picker, three difficulties, on-screen keyboard, hints, win/lose overlays, timer, saved game, stats, translation hint | Rebrand, pin language to Dutch, add picture clue |
| Word Search | `src/wordsearch/` | Grid generator, six difficulties, all directions, hints, category picker, translation hint, saved game | Rebrand, pin language, add picture/gloss clue |
| Match Up | `src/matchup/` | Word ↔ picture flip pairing, two panels, 4–12 pairs, categories, celebration | Rebrand; decide whether "Koppelen" stays flip-match or becomes drag |
| Word bank | `src/website/words.js` | 25 categories, ~2,500 entries, `{ en, nl, uk }`, optional fields, `BIGTOE.entries` / `BIGTOE.words` helpers | Curate hard; add missing categories; drop irrelevant ones |
| Image manifest | `build/website/wordimages.js` | `word → category/file.jpg` map, keyed by uppercase English word | Regenerate from the curated set |
| Image pipeline | `tools/gen_wordimages.py`, `assets/wordimages/` | Crops to 256×256 JPEG, fixes typos, aliases multiple words to one image, emits the manifest | Point at Oefenpad assets; rerun |
| i18n layer | `src/website/i18n.js` | `register` / `t` / `data-i18n`, Dutch strings already present in every game | Pin to `nl`, remove switcher |
| Shared helpers | `src/website/common.js` | `shuffle`, `fmtTime`, confetti, Web Audio sound effects, splash, dark mode, PWA install, pressed-state sync | Remove analytics/consent, rebrand keys |
| PWA shell | `src/website/manifest.json`, `sw.js`, `offline.html`, `tools/gen_pwa_icons.py` | Installable app, offline fallback, network-first HTML, cache-first art | Rebrand icons/colours/name/cache prefixes |
| Game specs | `docs/hangman.md`, `docs/memory.md`, `docs/matchup.md` | Ready-made spec format for Galgje, Geheugen, Koppelen | Rename and align with Oefenpad |
| Test harness | `tools/dom_stub.js`, `smoke_common.js`, `smoke_games_boot.js`, `test_word_format.js`, `check_matchup_dict.js` | Fake DOM/audio, boot checks, word-format checks, dictionary completeness | Repoint paths; add Oefenpad assertions |

The games already ship Dutch UI text. For example, Hangman has `Galgje`,
`Nieuw spel`, `Instellingen`, `Geluideffecten`, `Kies een categorie`, and the
Word Search has `Woordzoeker`, `Te vinden woorden`, `Gevonden`. That is a real
translation saving, even though it needs a tone pass.

## Copy and adapt

### Geheugen is the wrong game for "word ↔ picture"

`src/memory/` matches **identical pictures** (image pairs), not a Dutch word to a
picture. The planned Geheugen needs one of:

- port Match Up's word-card/image-card pairing into a single grid, or
- add a `word` face to Memory's card renderer and deal one word card + one image
  card per pair.

Match Up already has the pairing logic and the image manifest. Memory has the
nicer single-grid flip experience. Reuse one, not both.

### Koppelen is flip-and-match, not drag

`src/matchup/` is two panels of face-down cards: flip a word, flip a picture,
match them. The planned Koppelen is "drag words onto the right pictures". The
data, image mapping, level sizes and celebration are reusable; the drag layer is
new. The `suggestions.md` "Room Raid" idea is the closer mechanic for drag-onto-a-
scene, so this may be a deliberate split: Koppelen = flip-match, Room Raid =
drag-to-scene.

### Word Search and Hangman have no picture clues yet

Both have a **translation hint** (English or Ukrainian) rather than a picture
clue. The user-facing idea — hold the word in mind while searching, with a
picture and a dictionary fallback — needs one addition:

- render the clue from `BIGTOE_WORD_IMAGES[entry.en]` beside the word, and
- on completion, show picture + Dutch word + audio together.

Word Search's existing translation hint is a good "look it up" affordance for
learners whose first language is not English, so keep it as an option rather
than deleting it. Hangman's translation hint works the same way.

### The word bank is not the Oefenpad curriculum

`words.js` is a general thematic noun bank, not the Quick Wins pattern set. It
has no **verbs**, no **body**, no **family** category, and no prepositions,
endings, word families, false friends or sentence data. Its 25 categories
include `mythology`, `dinosaurs`, `marine` and `countries`, which are not A1/B1
priorities. Use it as raw material for vocabulary games, then curate:

- keep animals, food, household, travel, professions, nature, sports, music,
  technology, flowers/insects if useful;
- add body, family, verbs, adjectives, function words;
- align the survivors with the book's chapters and the eight pillars;
- add a checker that every playable word has an image or a gloss.

### Images are thin and off-style

There are only **157** images: 48 animals, 94 food, 15 household. Nothing for
body, family, nature (as a category), verbs or most other categories. They are
photorealistic white-background product shots, while `designguide.md` and
`story-machine.md` call for flat, bold, sparse brush art in cobalt. Two options:

- use the 157 as placeholders and regenerate everything in the Oefenpad style,
- or accept a separate photographic vocabulary-icon style and document it.

The pipeline (`tools/gen_wordimages.py`) and the prompt in `docs/imgageprompt.md`
are reusable, but that prompt explicitly asks for photorealistic icons, so it
needs rewriting for the brand look.

Also note the per-category cap: Memory's 8×8 and 10×10 levels need 32 and 50
unique images. Household has 15, so those levels disappear in that category.
Match Up caps pairs at the available mapped words.

### i18n is bigger than Oefenpad wants

`i18n.js` supports `en`, `en-us`, `nl`, `uk`, detects the browser language and
persists a switcher choice. `decisions.md` says the interface is Dutch, full
stop. Pin `lang = 'nl'`, remove the switcher and the "change language restarts
the game" dialogs. Keep the per-game Dutch dictionaries.

If you later want the "show English gloss" hint, use the word-level `translateTo`
setting the games already implement — do not reintroduce a UI language switcher.

### Branding and tracking

Replace, do not ship:

- `bigtoe_holdingtrophy.jpg`, `bigtoe.png`, `playingcard_light.jpg` /
  `playingcard_dark.jpg`, the teal theme and all BigToe copy;
- `© 2026 BigToe Games`, `bigtoe.games` canonical/OG URLs, AdSense/analytics
  snippets and the consent gate (unless you decide to add analytics);
- localStorage keys (`bigtoe-theme`, `hangman-settings`, `memory-best`, …) so
  they cannot collide and so Oefenpad progress is clearly its own.

Use the Oefenpad palette (`#2B50C8`, `#FFFFFF`, `#E8601F`) and `assets/logo/`.
The `16px`/`32px` favicon cut already exists.

### Build and deploy are BigToe-specific

`deploy.sh` does `src/` → `build/website/`, patches site chrome into every page,
fills the precache list, cache-busts JS/CSS by content hash, and checks anchors.
Copy the **ideas**:

- fail the build if a required string/asset is missing;
- hash JS/CSS URLs, leave images alone;
- generate the service-worker precache list rather than hand-maintaining it;
- keep `serve.py`-style no-cache local serving, because plain
  `python3 -m http.server` hides stale HTML.

Do not copy the FTP upload, ads or the BigToe header/footer. `mvp.md` says
Netlify/Vercel, no backend.

## What this does not give you

- **Verb tables, prepositions, sentence tiles, endings, word families, false
  friends.** None of that data exists. `grammar.js` is still the job.
- **SRS scheduling and the mistakes queue.** No spaced-repetition engine, no
  shared progress model beyond per-game localStorage.
- **Reading, writing, conversation, listening comprehension, minimal pairs,
  pronunciation.** No audio assets and no dialogue/text data.
- **Curriculum mapping.** The word bank is thematic, not pillar-based.
- **Dutch audio.** The sound effects are synthesized Web Audio beeps, not speech.
  Do not mistake them for pronunciation or listening material.

## First cut

1. Create a `src/` page set and a small `shared/` folder: `words.js` (curated),
   `wordimages.js`, `i18n.js` (pinned to Dutch), `common.js` (trimmed).
2. Copy Galgje and Woordzoeker first — they are the most complete and the
   closest to the planned games.
3. Copy Koppelen for word ↔ picture; decide whether Geheugen becomes a single-
   grid word ↔ picture game or stays picture-only.
4. Rebrand CSS, card backs, trophy art, metadata, localStorage keys; strip ads
   and analytics.
5. Curate 300–500 core words with images/glosses, and add the build checker.
6. Add picture clues to Galgje/Woordzoeker and the picture + word + audio payoff.
7. Add the PWA shell and offline fallback so daily practice works on a phone.
8. Only then invest in the grammar games and the data they need.

## Mapping to the thirteen

| Planned | Reuse |
|---|---|
| Galgje | Direct |
| Woordzoeker | Direct |
| Koppelen | Direct for flip-match; new drag layer for drag-to-picture |
| Geheugen | Adapt Match Up pairing or add word faces to Memory |
| Others | No equivalent |

The real head start is the vocabulary-game engine, not the language curriculum.
Copying the four pages saves the UI, state, persistence, category, difficulty and
PWA work — the part that is tedious and easy to get wrong — while leaving the
Quick Wins content, the grammar games and the audio as the actual product.

## Port log (first cut, done)

What was actually copied into Oefenpad and how it was changed. BigToe itself was
read only.

### Layout

```
src/shared/i18n.js          Dutch-pinned i18n (no detection, no switcher)
src/shared/common.js        shuffle, fmtTime, confetti, splash, audio, sfx, aria sync
src/shared/words.js         word bank, helpers on window.OEFENPAD
src/shared/wordimages.js    image manifest (OEFENPAD_WORD_IMAGES)
src/galgje/                 from bigtoegames/src/hangman/
src/woordzoeker/            from bigtoegames/src/wordsearch/
src/koppelen/               from bigtoegames/src/matchup/
src/geheugen/               from bigtoegames/src/memory/
assets/wordimages/          all 157 images (animals 48, food 94, household 15)
```

Directory names are Dutch to match the interface; the games map 1:1 to the
canonical names in `games.md`.

### Renames

- Namespace `BIGTOE` → `OEFENPAD`; `BIGTOE_WORDS` → `OEFENPAD_WORDS`;
  `BIGTOE_WORD_IMAGES` → `OEFENPAD_WORD_IMAGES`.
- Theme key `bigtoe-theme` → `oefenpad-theme`.
- Per-game storage: `hangman-*` → `oefenpad-galgje-*`, `wordsearch-*` →
  `oefenpad-woordzoeker-*`, `matchup-*` → `oefenpad-koppelen-*`, `memory-*` →
  `oefenpad-geheugen-*`.
- Image paths `../wordimages/` → `../../assets/wordimages/`.

### Stripped

AdSense meta, canonical/OG/Twitter tags, PWA manifest/icons (until the shell is
added), the language switcher and its confirmation dialog, the consent banner
and analytics, BigToe splash/header/About branding, the trophy photo and the
playing-card back JPGs. Card backs are now a cobalt CSS gradient, and the
trophy slot uses `assets/logo/logo_128px.png`.

### Behaviour changes

- **Geheugen is now word ↔ picture**, not picture ↔ picture. `deal()` creates one
  picture card and one Dutch-word card per item; a match requires the same item
  with different faces. Emoji fallback still exists for categories with no
  images.
- **Galgje shows a picture clue** above the word tiles when the selected word has
  an image, and shows the picture again on the win/lose overlays.
- **Woordzoeker shows a thumbnail** beside each word in the list when one exists.
  Word objects carry `img` through puzzle regeneration and saved games. Default
  difficulty is now `beginner`.
- **Koppelen stays flip-and-match.** It is already word ↔ picture; the drag
  mechanic described in `game-catalogue.md` is still future work.
- Translation hints (`translateTo`) remain as an optional English gloss, default
  off. The Translate dropdown no longer offers a UI language; it only selects
  the gloss language.

### Validation

All eight JS files pass `node --check`. Each page was loaded in headless Chrome
with a fresh profile; no console errors, and the expected dynamic content was
present (Galgje tiles/keyboard/clue, Woordzoeker 10×10 grid with thumbnails,
Koppelen 6 word ↔ picture pairs, Geheugen 18 pairs = 18 words + 18 pictures).

### Still open

- Curate the word bank: it still has no verbs, body, family or adjectives, and
  the 157 images cover only animals, food and household. Cards for words without
  images fall back to text or are filtered out.
- Add a `src/index.html` hub linking the four games (and Verhaalmachine).
- Add the PWA shell and audio (pronunciation), then the grammar-game data.
- Port the BigToe test harness if the games keep growing.
