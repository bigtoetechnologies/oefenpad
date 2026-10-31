# Decisions and open questions

What was settled on 30–31 October 2026, and what was not. Visual rules live in
`designguide.md`; this is everything else, so a later session does not have to
re-argue it.

## The two products

| | Book | Site |
|---|---|---|
| Name | Quick Wins in Dutch | Oefenpad (oefenpad.nl) |
| Promise | A fast start — you already understand more than you think | Permanent memory through daily practice |
| Sold as | A cheap paperback on Amazon | Free tier plus premium, around €20 a year |
| Role | The acquisition channel. Prints the site URL | Where the learner stays |

They deliberately promise different things. The book sells speed to someone who
has not started; the site sells the long haul to someone who has. That is why
the site is not called Quick Wins.

## The name

`oefenpad` — practice path. Chosen against `nederles` (gone, .com and .nl),
`dutchquickwins`, `taalpad`, `dagmemo` and the rest. The rules it had to pass:

1. Says **practice**, not lessons and not speed.
2. Spellable and typeable by someone who does not read English — so no `quick`,
   no `ck`, `qu`, `tch`, no silent letters.
3. No doubled vowel. Someone who hears "taalmemo" types `talmemo`.
4. Well-formed Dutch. `oefen-` is a normal prefix (`oefenboek`,
   `oefenwedstrijd`); `dagoefen` and `woordoefen` are not and were dropped.

`oe` was accepted despite being a digraph: these readers meet it in week one,
and the name teaches a word on the way past.

## The audience constraint

Most users will not read English. Ukrainian, Syrian, Turkish, Polish, Eritrean,
Indian, Spanish speakers learning Dutch, many for inburgering. Consequences,
and they are not negotiable:

- **The interface is in Dutch.** English is a second barrier, and Dutch chrome
  is itself practice. Small words, endlessly repeated: *oefenen, volgende,
  goed, opnieuw*.
- Meaning travels in pictures and colour, never in a sentence.
- We give English glosses for words. We do not attempt other languages —
  learners use their own dictionary.
- No text inside artwork, ever. One art set has to serve everyone.
- A feature that only works if you have English is suspect. The False Friend
  game is the clearest case: a false friend needs a first language to supply
  the friend, so it may belong to the book rather than the site.

## Settled

- Colours, logo, tile language, typography: see `designguide.md`.
- Blue says what a thing is. Orange says act on it now, and nothing else.
- The eight pillars are distinguished by **motif**, not colour, so they work
  for someone who cannot read the label. Pillar colours in `Concept.md` belong
  to the book.
- Tagline **"Stap voor stap"**, with no English version. If it needs
  translating it is the wrong tagline.
- The activity list and its Dutch names: `designguide.md`.

## Open

| # | Question | Where it stands |
|---|----------|-----------------|
| 1 | Register `oefenpad.nl` and `.com` | Both showed NXDOMAIN on 31 Oct 2026. Not proof — confirm at a registrar. Nothing registered yet |
| 2 | A mascot, and whether to have one | A heron was proposed: patient, in every Dutch canal, steps deliberately, survives 16px, draws in flat cobalt. It would never speak and never nag. Undecided |
| 3 | The tegeltje as the unit of content | One phrase learned is one tile; a finished pillar is a panel the learner built. Proposed, undecided |
| 4 | Where the free/premium line falls | Needs the feature list, not the name |
| 5 | A git remote | The repo is local only. Three commits, no backup off this disk |
| 6 | Pillar 8 (pronunciation) needs audio | Nothing exists. Blocks the Listening Drill |
| 7 | Grammar data | `grammar.js` does not exist yet. Both specced games need it — see `games.md` |

## Not ours

Delftware's *style* is 17th century and free to use. Royal Delft is a live
company: do not borrow a maker's mark or the word "Royal".
