# Explanation cards: brief for authors

Scope: verbs that the picture families (Werkwoorden) skipped because no single honest drawing carries them. Each sense of a verb becomes one card with four examples. Read `Docs/decisions.html` (the "Explanation cards" item) and `Docs/explanation-cards-pilot.html` for the rules and the finished format. `tools/_ex_tmp/laten.json` is a model file.

## What a card is

A card teaches one sense of one verb. The learner sees a picture (not drawn yet, so a brief), two to four short Dutch sentences, and one yes/no question about the scene. Answering the question shows the learner understood the verb. The English gloss appears after the answer.

## Process, per verb

1. Fetch `https://nl.wiktionary.org/wiki/<verb>` and read the verb (Werkwoord) section. List its numbered senses. If the page fails, say so in your report and work from your own knowledge, with the card note starting "Sense not checked on Wiktionary".
2. Choose the senses worth a card: the common, everyday ones for that band. Skip idioms, rare senses and senses that duplicate another. One to three cards per verb. Say in your report which senses you left out.
3. Write each card. Four examples per card, each a different situation, so the learner sees what stays the same.
4. Run `python3 tools/build-explanation-cards.py --check <your file>` and fix every error until it reports 0.
5. Reread every Dutch sentence for naturalness before you finish.

## Card fields (JSON)

```
{
 "verb": "laten",
 "sense": "toestaan dat iets gebeurt (to allow)",   Dutch gloss from Wiktionary, English in brackets
 "gloss": "to let, to allow",                       English, shown after the answer
 "forms": ["laten", "laat"],                        every surface form of the verb you use in the text
 "picture": "...", "mark": "...", "alt": "...",      scene brief for example 1, the one mark that must read, Dutch alt text
 "note": "...",                                      one sentence: why this scene, or the sense boundary
 "examples": [ {"text": ["...", "..."], "question": "...?", "answer": "ja"}, ... 4 of them ],
 "key": "vermoeden (verb)",                          only if the lexicon lists the verb under a suffixed key
 "band": "A1", "band_why": "..."                     only if the sense's band differs from the verb's lemma band
}
```

Examples 2 to 4 also carry `"scene"`: one line in English saying what is drawn. Example 1 uses the card's `picture`.

## Hard rules (the builder fails on these)

- Two to four sentences per example, one question ending in `?`, answer `ja` or `nee`. Mix the answers: about half `ja`.
- Every Dutch word, in text and question, must be at or below the card's band by lemma rank (`tools/lexicon/woorden-niveau.tsv`): A0 rank 250, A1 1000, A2 2500, B1 5000, B2 10000. The verb itself is exempt. Common function words are handled. The allowed names are Sam, Jan, Els, Mark, Anna, Piet, Eva.
- Alt text is Dutch and never contains the verb or a form of it.
- No digits in the text. No banned imagery in scenes (windmill, clog, tulip, canal, cheese, herring, chips, fries).
- A card whose sense is later than the verb's lemma band sets `band` and `band_why`. Set it when the intended band in your task differs from the lemma rank band.
- If a word you need is above the band, choose another word. Do not edit `tools/explanation_lib.py`. If a core word is wrongly ranked (the lexicon rank is a homograph artefact), list it in your report.

## Style rules

- Short, natural sentences a learner at that band could read. Present tense unless the sense needs the perfect.
- The picture rules still apply: no text, letters or digits inside the drawing; one cobalt colour on white, so colour never carries meaning; no souvenir Dutch imagery.
- The scene must show the sense without the text. The text and question then name it. Say in `mark` the one thing that must read.
- Keep the four examples apart: different people, places and objects, same sense. Include one example that shows the edge of the sense (a refusal, an unfinished action) where that helps.
- Avoid violent, sexual or medical-distress scenes. If a verb needs one, tell me in your report instead.
- Never invent a second sense to reach a count. Fewer, better cards are right.

## What to hand back

A short report: files written, cards and verbs done, senses left out and why, words you found wrongly ranked, any verb you could not do. Do not touch nav, index pages, git, or any file except your own JSON file.
