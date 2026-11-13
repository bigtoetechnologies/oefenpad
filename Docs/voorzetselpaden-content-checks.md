# Voorzetselpaden content checks

Ten checks decide whether a card is correct and fit to teach. Each card is checked against all ten before it goes into the game.

"English" is the label for the English meaning of a chunk (`wachten op` = "to wait for"). It is not always a literal translation: `wachten voor` is "to wait in front of".

## The checks

| # | Check | What it catches | Done by |
|---|---|---|---|
| 1 | Correct Dutch | Wrong preposition, article or word order in the chunk, example or build sentence | LLM first pass, native sample |
| 2 | Correct examples | The example does not use the chunk, or uses another sense of it | LLM |
| 3 | Correct contrasts | In a contrast set such as `wachten op` / `wachten voor`, both answers are acceptable in the scene | LLM, native sample |
| 4 | Control questions | The answer key is wrong or ambiguous | LLM, native sample |
| 5 | Single right answer | A distractor is also valid, or the build sentence accepts more than one order | Script and LLM |
| 6 | English | The English meaning is wrong, too loose, or blurs a contrast partner | LLM |
| 7 | Picture matches brief | The image shows something other than the scene brief | A person, or a vision model |
| 8 | Picture teaches alone | The scene cannot be read without text, or fits two chunks | A person |
| 9 | CEFR fit | The sentences use vocabulary or grammar above the band's level | LLM with a word list |
| 10 | House rules | Souvenir Dutch imagery, text inside the art, or English needed to understand the picture | Script for text in art, a person for the rest |

## Known failures to recheck

| Source | Failure |
|---|---|
| `CLAUDE.md` open item 12 | `praten-tegen` control question is keyed `true` but its picture and sentence say the listener is not listening |
| `CLAUDE.md` open item 12 | Separable-verb hints say the prefix goes last ("staat achteraan") when every accepted answer puts it straight after the verb |
| Memory note | Two of four A0 briefs failed when set against the real image |

## Sampling

A native Dutch speaker or inburgering teacher checks a sample of cards for checks 1, 3 and 4. The sample size is open.

## What the 12 Nov review covered

The review read only the seven plan Markdown files. It read no JSON, code or images. Source: `~/claude-scratch/voorzetselpaden-content-md-review-2026-11-12.md`, summarised by a subagent and not yet spot-checked.

| # | Check | Covered | Basis |
|---|---|---|---|
| 1 | Correct Dutch | Partly | Chunk only, rarely an example. No build sentences, no native sample |
| 2 | Correct examples | Partly | One hit. Example sentences were not read systematically |
| 3 | Correct contrasts | Fully | Contrast sets judged, for example `rekenen op` / `met` |
| 4 | Control questions | Not at all | Answer keys were out of scope |
| 5 | Single right answer | Partly | One false "Klopt" item. Distractors and build-sentence order not checked |
| 6 | English | Fully | Checked on every row's chunk and English line |
| 7 | Picture matches brief | Not at all | No image was read |
| 8 | Picture teaches alone | Partly | Judged on the brief text, not the image |
| 9 | CEFR fit | Not at all | Bands were taken as given |
| 10 | House rules | Not at all | Nothing on souvenir imagery, text in art or English needed to read a picture |

Still to run: checks 4, 7, 9 and 10 in full, and 1, 2, 5 and 8 properly.

## Open

| # | Question |
|---|---|
| 1 | Who is the native checker, and what share of cards do they sample? |
