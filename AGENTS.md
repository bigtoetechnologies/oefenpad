# Oefenpad — agent router

Read this file first, then only the files your task names. The point of this
page is that you do **not** read the repo. It is 18 MB of docs and 47 MB of art.

The documentation is HTML and the HTML is the document. There is no Markdown
copy and no doc build: edit the page. Never add `.md` under `Docs/`.

---

## 1. Do not read

| Don't open | Why |
|---|---|
| `Docs/<family>/a0.html` … `b2.html` | 90 KB–1.8 MB each; 3,124 preposition cards alone. Generated from the source files in §4. |
| `Docs/explanation-cards/*` | up to **1.4 MB** of prose per band |
| `Docs/design-options/**`, `Docs/archive/**` | 15 rejected home-page prototypes; history, not guidance |
| `assets/**/*.png` | 47 MB of art. Never read an image, never list the directory |
| `server/Oefenpad.WebUI/wwwroot/spelen/` | build output (bundled JS/CSS) |

Do not `read_file` a generated page to find one card. `grep -n` it, or read the
source file it was built from.

## 2. Read these, in this order

1. `Docs/project-rules.html` — what the site is, the non-negotiables, the
   commands, where things stand, what is open. Requirement before proposing.
2. `Docs/product.html` §7 — the offer and the gate, before proposing a feature.
3. `Docs/<family>/AGENTS.html` — the playbook for the family you are touching
   (only `voorzetselpaden` and `werkwoorden` have one).
4. The source file for the family (§4). For content work that is a **TSV of a
   few KB**, not the HTML.

`Docs/index.html` lists every document if you need to find one.

## 3. Reading a Docs page cheaply

Every page repeats the same ~170 lines of `<head>` and CSS. The content sits in
`<article class="prose">`:

```sh
grep -n '<article' Docs/project-rules.html    # content starts here
```

then `read_file` from that line. For a whole page in one go:

```sh
python3 -c "import re,sys;s=open(sys.argv[1]).read();i=s.find('<article');print(re.sub(r'<[^>]+>',' ',s[i:]))" FILE
```

## 4. Card families: where the truth lives

The generated HTML is never the master except where the table says so.

| Family | Master (edit this) | Build | Check |
|---|---|---|---|
| Voorzetselpaden | `Docs/voorzetselpaden/{a0..b2}.html` — **the HTML is the master** | `tools/build-prepositions-matrix.py`, `tools/composite-prepositions-art.py` | `tools/prepositions-pages.py check` |
| Werkwoorden | `tools/_ww_tmp/select.py` + `tools/_ww_tmp/scenes/*.tsv` + `tools/_ww_tmp/contrasts.tsv` | `tools/build-verb-cards.py` | `tools/check-verb-cards.py` |
| Zelfstandige naamwoorden | `tools/_zn_tmp/{selection.json,clusters.txt,scenes/*.tsv}` | `tools/build-zelfstandige-naamwoorden-cards.py` | `tools/check-zelfstandige-naamwoorden-cards.py` |
| Bijvoeglijke naamwoorden | `tools/_bn_tmp/` | `tools/build-adjective-cards.py` | `tools/check-adjective-cards.py` |
| Bijwoorden | `tools/_bw_tmp/` | `tools/build-bijwoorden-cards.py` | `tools/check-bijwoorden-cards.py` |
| Scheidbare werkwoorden | `tools/_sw_tmp/` | `tools/build-scheidbare-werkwoorden-cards.py` | `tools/check-scheidbare-werkwoorden-cards.py` |
| Vaste uitdrukkingen | `tools/_vu_tmp/` | `tools/build-vaste-uitdrukkingen-cards.py` | `tools/check-vaste-uitdrukkingen-cards.py` |
| Explanation cards | `tools/_ex_tmp/*.json` | `tools/build-explanation-cards.py` | none |

After any family rebuild, run `tools/check-card-families.py`. It asserts the
shared spine (`Scene`/`Must read`/`Avoid`/`Alt`), the example rule, the two-build
and ja/nee-question rule for Voorzetselpaden, and reciprocal contrast partners
across every family. A contrast partner is optional and may cross bands.

Art, per family: `assets/verbs/<slug>.png` (werkwoorden, plain `<img>`),
`assets/voorzetselpaden/<id>.png` (one composited cobalt-on-paper file per
scene, shown by both the docs and the game). Explanation cards have no game
yet; Werkwoorden has a picture-choice game built from its 90 drawn A0/A1 cards
(`tools/import-verb-game.py` → `server/.../verbs.json`).

**Run `tools/check-prepositions-art.py` on the delivered drawings or
`assets/verb-propositions/incoming`, never on the shipped files** — those are
already composited, so a check on them audits the output, not the drawing.

**Never regenerate a family's data unless asked.** Voorzetselpaden's reviewed
content and its shipped `prepositions.json` diverge on purpose.

## 5. Code map

| Path | What |
|---|---|
| `index.html`, `privacy.html`, `voorwaarden.html` | static site, bilingual, no build step |
| `assets/site/oefenpad.css`, `oefenpad.js` | the one stylesheet and script for the whole site |
| `client/src/` | the six React games: `site/` (GameShell chrome), `shared/`, `games/<game>/`, `api.ts` |
| `client/src/styles/source/` | per-game CSS source; `client/src/styles/games/` is the scoped build output |
| `server/` | .NET 10, Razor Pages + Identity + SQLite. `Oefenpad.Services/Games/` holds the round machine; `Oefenpad.Resources/Games/Data/*.json` is game content |
| `tools/lexicon/` | `woorden.tsv` = master vocabulary (10,000 lemmas). `woorden-niveau.tsv` = band per word |
| `tools/grok/grok.py` | image prompts and downloads (`prompt`, `verbprompt`) |

## 6. Commands

```sh
python3 -m http.server 8099 --bind 127.0.0.1   # never 8080, that is in use
dotnet run --project server/Oefenpad.WebUI --urls http://127.0.0.1:8098
dotnet test server/Oefenpad.Tests
cd client && npm run build                     # writes wwwroot/spelen
cd client && npm run scope-css                 # after a styles/source change
python3 tools/check-card-families.py           # every family, one schema
```

`dotnet build` runs `npm ci` + `npm run build`; `-p:SkipClientBuild=true` skips
the client. Screenshot checks need a fresh `--user-data-dir` and a changing
query string, or Chrome hands you a stale render.

On this machine the host shell may have `python`, not `python3`. The docs say
`python3`; run whichever exists.

## 7. Traps that have already cost time

- **`grep` here fails on `\|` alternation.** Use Python `re`.
- `class="kaart"` also matches `class="kaarten"` (the container). Match `kaart`
  anywhere in the attribute.
- Don't split band pages on `</section>`; the counts differ. Split on
  `<section class="cluster">`.
- **Never inline images as base64.** Pages reference art by path. `data:` URIs
  made band pages 6.5 MB and unreadable to every agent.
- **No dark mode.** Art bakes the cobalt; no masks, no second file per scene.
- Never hand-edit generated JSON (`prepositions.json`, `matrix-*.html`,
  `index.html` of a TSV-built family).
- The interface is Dutch; glosses are English; never text inside artwork.

## 8. Working style the owner expects

- Lead with the answer. Short. Expand only when asked.
- Disagree in the first line, with the reason.
- **Delegate reading to sub-agents.** Each starts blank: give every path, rule
  and constraint, keep write scopes disjoint, ask for a short report.
- Never report something as working without having run it.
- Show visual changes; a description is not enough.

## 9. Where to look next

`Docs/project-rules.html` is the canonical state of the project, including the
open questions and what is unverified. If this file and that page disagree,
that page wins and this file needs fixing.
