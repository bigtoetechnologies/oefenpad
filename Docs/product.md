# Oefenpad — product brief

**Status:** first draft, 16 November 2026. Built by interview with the owner;
sections marked `OPEN` are unanswered questions, not blanks to guess at.
This document is the single source for *what the product is and who it is for*.
Everything else in `Docs/` is implementation detail or history.

---

## 1. What this is, in one sentence

> Oefenpad turns the Dutch you have already met into words you can reach for
> mid-sentence — through a repetitive process that pushes them into memory.

## 2. The gap we fill

Courses teach. They do not get people to *fluent*.

The learner who arrives here has usually done some Dutch already — a course, an
inburgering intake, a year of Duolingo, a job where people speak English at
them. They can follow the class and then run out of words halfway through a
sentence.

Owner's framing, 16 November 2026:

> Most courses teach just enough vocabulary to use the grammar they are
> teaching. Courses are roughly 90% grammar, but grammar is about 20% of the
> problem. The other 80% is the actual words people need.

So the gap is **volume of the right words, and reps on them**. The learner does
not need a seventh explanation of `om te` + infinitive. They need two thousand
more words they can produce without stopping, met often enough to stay.

Three consequences, and they bind the whole product:

1. **Vocabulary is the product; grammar is the minority.** Grammar drilling
   stays, but it is the smaller slice, and it exists to serve the words rather
   than the words existing to demonstrate the rule.
2. **The unit of progress is "a word I can now use", not "a rule I now
   understand".** That is what has to be visible on the screen.
3. **Repetition is the feature, not the padding.** Meeting the same words again
   is the mechanism. It is not evidence that we ran out of content.

**The owner's own evidence, 16 November — the sharpest statement of the gap in
this document:**

> I passed inburgering and scored straight 10s in the A2 language tests, so I
> can get citizenship — and I still can't hold a conversation. That is the gap
> we're filling.

No market claim beats that. The exam can be passed perfectly and the
conversation still fails, because the exam measured what the exam measures. It
is also the reason §4's decision is not a retreat: we are not refusing to do
exam prep, we are pointing at what exam prep leaves behind.

**The destination is better fluency.** Holding a conversation without drying up
is what the learner wants and what the product aims at. See §3 for why that is
the aim and not the promise.

**Where the evidence comes from, honestly.** Owner, 16 November: mostly the word
is missing, sometimes it arrives too late, and rarely is it fear of the grammar
— *"but that's me, not others; I suspect from others that it's similar."*

So the founding evidence is **a sample of one plus anecdote**, and §2 should be
read that way. That is not a weakness to hide: the owner is also the first test
subject (§11), and a hypothesis with a named test beats a survey nobody ran. But
no content decision may be justified by "the owner finds it so" on its own.

Two things he reported that generalise well:

- **Prepositions are the worst case.** They carry the most meaning per syllable
  and the least picture, which is why they are the flagship game.
- **Looking things up destroys the exercise.** Television with a dictionary ends
  in zoning out. So an unknown word may never send the learner out of the task —
  see §6, rule 5.

**A2 is a low ceiling, and that is the market.** The owner's straight 10s came
after a year of courses reaching almost B1, so the score measures a modest
level. In his words, 16 November: *"A2 is very low. The biggest gap after A2 is
mostly an enormous amount of vocabulary that needs to be learned, and that's
where we come in."*

That defines the audience more sharply than §4 does: **people who finished the
course.** Indicative sizes, approximate and not load-bearing: A2 ≈ 2,000 words,
comfortable B1 ≈ 3,500–4,000. The gap is a few thousand words, and no course
timetable has room for them.

It also validates the content target: 24 themes at ~200 words is ~4,800 words —
the right size for exactly that gap, and the reason "2,000" was never the number.

**Caveat, to be honest with ourselves:** the 80/20 split is a **product thesis,
not a measured finding**. It should be falsifiable by our own numbers — which is
why vocabulary growth is the natural thing to report in §9.

## 3. The promise, and what we may claim

> We do not teach you Dutch. We give you the words — and the reps that keep
> them.

Explicitly **not** the promise:

- Not "learn Dutch in 24 hours" / "fluent in a month" — no speed claims.
- Not "we'll teach you Dutch" — we are not a course, not a curriculum, not a
  teacher. No lessons, no units, no enrolment.

### What we may claim, and why

The owner raised the temptation directly on 16 November: *"we can't be 100%
honest about what we offer or no one will buy it."* **I think that is the one
place he is wrong**, and the doc records the disagreement rather than settling
it: overclaiming is what the competitors do, and it is the thing his own
opening line rejected. Keeping the promise checkable is also the cheapest
differentiator available — the learner has been sold "fluent in three months"
already and it did not work.

Proposed rule, so honesty does not mean timid:

- **Claim outcomes, never mechanisms.** "You will run out of words less often."
  "You will stop freezing at the counter." Not "we make you fluent", not "in
  eight weeks".
- **A claim we can half-prove with our own numbers beats a claim we cannot.**
  "Members learn 400 new words in their first month" is a sales line *and* a
  measurement in §9.
- **Say what we are not.** "No lessons. No certificate. No teacher." This is a
  selling position, not a disclaimer — it is the reason someone chooses us over
  a course for the fourth time.
- **Why we may not hint at the exam.** §4 puts inburgering out of scope, so no
  copy, image or page may imply a pass, a level, or exam preparation. A
  suggested line that keeps the audience and refuses the claim: **"Geen
  examencursus. Wel de woorden die je toch nodig hebt."**

`OPEN` — owner to accept, adjust or overrule.

### The promise that sells and can be checked

Proposed 16 November, in answer to "what do we promise that's sellable and
measurable":

> **You will know more words every week than you did the week before — and you
> will be able to see it.**

Two halves, both required:

- **Growth** is the sellable half, and it must be a *rate*, not a total — see the
  trap below.
- **Proof** is the measurable half. It is what lets us avoid a speed claim
  entirely and still say something strong.

**The definition, to be wired into the product.** A word *counts* when the
learner answers it correctly in a review that comes **at least three weeks
after they last met it**, having not seen it in between. That word is **held**.
Everything the learner sees derives from that one rule:

| Shown to the learner | What it means |
|---|---|
| **Words met** | seen at least once, in this theme or overall |
| **Words held** | passed a review at a three-week gap |
| **Words due** | held once, and the next review is now |

**Three rules that keep the number honest**, because we are counting our own
exercises:

1. **Never show the same sentence twice.** Otherwise we measure memory for *that
   sentence*, not for the word.
2. **Randomise the distractors.** A word is not held if it was the only
   plausible option.
3. **Count only at a real gap.** Recognition in the same session is not memory.

**The trap: a finite promise kills a subscription.** "2,000 words and you're
done" is a countdown to cancelling, and at €10/month the learner who cancels on
completion is the worst case. So the promise has to be a **rate, not a total** —
more words next week — which means the theme set stays effectively open-ended
and later bands keep arriving. That is a standing commitment, not a slogan.

**What we still may not promise:** fluency, a CEFR level, an exam result, or a
date.

### Destination and promise are not the same sentence

- The learner's **destination** is better fluency — holding a conversation
  without running out of words (§2). That is what we aim at, and it is honest to
  say we are working on the thing that stops them talking.
- Our **promise** is the part a website can actually deliver: **more words,
  held, every week.**
- **Talking needs a person.** The site does not supply one, which is why rung 3
  exists (§5). So we may not say we will make someone fluent — only that we are
  fixing the words that fail them when they try.
- **The dashboard proves words, not conversation.** Conversation comes from using
  the words on a human. Confusing the two is how competitors end up selling a
  guarantee they cannot keep.

## 4. Who it is for

> An adult who has lived in the Netherlands a year or more, has done some Dutch
> already (a course, an intake, or Duolingo), and runs out of words in ordinary
> conversation. Practices on a phone, ten minutes at a time.

Confirmed by the owner, 16 November 2026.

What follows from it:

- **Adults** who already live in the Netherlands, or are about to.
- **Already learning**, not starting from zero. This is a supplement. Typically
  **at or just past A2** — they finished a course and stopped there, which is
  the market in §2.
- **Most read English** — but this must not be load-bearing (see §6).
- **Phone-first** experience matters; assume small screen and short sessions.

**The inburgering exam is out of scope** — settled 16 November, reason given:
it needs specialist knowledge (the exam's own formats, and what the municipality
tests) that this product does not have and should not pretend to have.

The learners are still the audience; it is the *exam* that is out. So the site
is what you use **alongside** an exam course, and the words are the words they
need anyway. It is also a clean position to take in public, and one no exam
course can copy: we are not competing with their results.

## 5. The ladder: passive → active → real world

This is the answer to "how does a word get from known to used", and it defines
what the site does and where it stops.

| Rung | What happens | What carries it | State |
|---|---|---|---|
| **1. Recognise** | The word is met in its theme, often enough to be known on sight and hearing. This is the **target at launch**. | The games | Built |
| **2. Produce** | The learner has to use it — build a sentence, tell a story | The Story Machine (`Docs/story-machine.md`) | Exists; more producer games planned |
| **3. Use it on a person** | We point them at real places to practise — a *taalcafé* in the library, a conversation group, a volunteer scheme | A directory page | **Dropped 16 Nov — deferred, out of the current product** |

Notes:

- **The site's job ends at rung 2.** Rung 3 is signposting, not teaching. We are
  not running a class and we are not stitching together strangers.
- **Rung 3 is dropped for now** (owner, 16 November: out of scope). The
  consequence has to be said plainly: with no directory the product stops at rung
  2, so **copy may not promise conversation** — only words. §3 already draws that
  line; this makes it mandatory rather than careful.
- **The directory is a product decision, not an appendix.** It commits us to
  content that goes stale — places close, times change. `OPEN`: who owns it, how
  often it is checked, and whether it is one national page or per-city.
- **Passive first is deliberate.** Active production needs a partner, a class or
  a teacher; the site can only simulate it. Rung 2 is the honest ceiling of what
  software alone can do, which is why rung 3 exists at all.

## 6. Language policy — a product rule, not a style choice

The site must work for someone who does **not** read English well.

1. **Dutch first, always.** Every control, heading, instruction and error
   message is in Dutch, written in simple Dutch — short sentences, one idea
   each.
2. **English is a convenience, never a dependency.** An English gloss sits
   beside the Dutch where it helps. If removing it breaks the task, the design
   is wrong.
3. **Meaning travels in picture, colour and shape.** A learner should be able to
   do the exercise without parsing any sentence in any language.
4. **Exception:** legal and account pages (`privacy`, `voorwaarden`, account
   mail) are in normal Dutch and normal English. They are contracts, not
   practice.
5. **No lookup detours.** An unknown word is resolved *in place* — a tap, a
   picture, a gloss — and the exercise continues. Anything that sends the learner
   to a dictionary or a second tab has already lost them. This comes straight
   from the owner's own account: television plus a dictionary ends in zoning out.

Consequence to accept: "simple Dutch" is a second writing job on every string,
not a translation of the English one.

`OPEN` — is there a floor below which we do not go, e.g. no Dutch word a
complete beginner could not decode? Or do we accept A2 Dutch chrome?

## 7. Money and the gate

Settled:

- **Volume, not margin.** 1,000 people at €10/month beats 10 at €50.
- **Cheap enough that price is not the reason someone says no.** The learner
  who needs this most often has least.

### The gate — settled 16 November

| Who | Gets | Pays |
|---|---|---|
| **Guest, no account** | Two themes (**Boodschappen**, **Mensen**), **A1 and below**, with every activity inside them. Nothing is remembered. | — |
| **Signed in, first 6 weeks** | Every theme, every band, the word log | Free |
| **After 6 weeks, and after any cancellation** | Back to the two free themes, *with* a log — frozen and read-only | — |
| **Paid** | Every theme, every band, the log at full scope, reviews everywhere | **€10/month or €100/year** |

- **One tier.** No per-band pricing, no second subscription level, no add-ons.
  €100 for a year is the only discount — €8.33 a month against €10.
- **Six weeks, not four.** §3 defines a word as *held* only when it comes back
  correctly after a three-week gap. A four-week trial expires at almost the first
  moment that evidence could exist, and only for someone who started on day one
  and never missed. Six weeks is the first length at which an ordinary starter can
  watch the product prove the one thing it promises.
- **The free tier keeps a log.** After the trial a learner falls back to two themes
  *with* memory, not to a dead end. That is what makes €10 an upgrade — "more
  themes, more words" — rather than a wall. Nobody is asked to pay before they
  have watched the counter move.
- **The free slice is capped twice: two themes, and A1 and below** (owner, 16
  November). Both limits apply, so the taster is the first band of two themes.

### The book is on hold

Owner, 16 November: the book is **not** part of the offer. It is sold separately,
through Amazon.

- €10/month and €100/year do not include it, and buying it grants nothing.
- **It was one acquisition channel, not the only one, and it is now unavailable.**
  So it cannot be counted on: the site has to convert a cold visitor on its own.
  Working out where those visitors come from is an open question, not an
  emergency, and it is not part of this document yet.
- Nothing in the product may depend on a book code or a purchase path that does
  not exist.

### After a cancellation

Owner: the log stays, but *"being careful not to make it easy for them to
download them and use them for another purpose — we need them to come to the site
if they want to learn them."*

So: **frozen, read-only and counted** — words met, held and due, by theme. Not a
word list with glosses, and no export. Honest caveat: anything on a screen can be
copied by hand, so the goal is not to fight copying; it is to not hand over a
tidy export that could stand in for the product.

### What the gate costs to build

Access is one service today (`GameAccessService`), keyed by band and by position
within a band. The gate above adds **three** dimensions: **theme**, **account
state** (guest / trial / free / paid) and **the log's scope**. That is a change to
the access rule itself, not a setting — and §12's theme navigation needs the theme
axis anyway.

Also note §8: a guest has no log, so ten minutes of guest play accumulates
nothing. That is a deliberate trade — it makes an account worth having on day
one — but it means **the taster has to stand up on its own**, with no memory
behind it.

### What the price forces

Self-serve signup and cancellation with no human in the loop; no per-user support
beyond a FAQ; no sales team; no per-learner content authoring. Anything added
per learner has to cost near zero at 1,000 users and still cost near zero at
10,000.

## 8. The memory model: spaced repetition

Owner's answer, 16 November:

> Review sessions at key points, and reviews at random times.

What that means concretely:

- **Sessions, not just streaks.** A review session appears after a set amount of
  new material, and old words are interleaved into new sessions at intervals.
- **It needs per-learner state on the server.** `GET /api/games/{game}/progress`
  exists; there is no scheduling behind it yet. This is the largest piece of
  work the product decision creates.
- **Session-level scheduling is enough to start.** Per-word scheduling (each
  word with its own next-due date) is better and is what "spaced repetition"
  usually means, but a fixed interleave is a legitimate first version and can be
  replaced without changing the learner's experience.

**The state is per word.** Owner, 16 November. Not per chunk, not per theme —
that is what the §3 definition of *held* requires, and it is the most work.

### What the backend must hold

Owner, 16 November:

> Keep a log of the words met, held, due, etc, and a log of what needs to be
> reviewed. We need that as a feature somewhere in the back end for those
> signed in.

Per signed-in learner, the server owns:

| The log | Contents |
|---|---|
| **Word log** | one row per word: first met, times met, last met, whether held, when next due |
| **Review queue** | derived from the word log — what is due now, oldest first |
| **Session history** | enough to recompute the above, and to answer §9's questions |

This is **additive to the existing account system**, not a new one: Identity,
SQLite and sign-in already exist under `server/`, so this is new tables plus an
endpoint. The harder part is not storage but the review scheduling rule.

**The log keeps the picture.** Owner, 16 November: *"pictures are important to
aid memory — our brains remember images better than words."* So a review shows
the **image**, not the English gloss. If the review shows the gloss, the gloss
is what was learned and the picture was decoration. This also means the word row
must carry a reference to its art, not only its text.

Two consequences:

1. **The log only exists for signed-in learners.** A guest plays and learns
   nothing persists. That makes the account genuinely useful rather than a
   gate, and it is the honest basis for the free/paid line in §7.
2. **The log is also the proof in §3.** Words met, held and due are not a
   marketing statistic kept internally — they are the learner's own screen.

## 9. How we know it works

`OPEN` — one or two numbers, checked at a fixed date. The candidates now follow
from the §3 definition of *held*, and there should be one of each kind:

**The product's own number** — does the mechanism work:

- **Share of words met that are later held** (passed at a three-week gap). If
  this is low, the review model in §8 is wrong.
- **Words held per active learner per month.** The headline.

**The business's number** — do people stay and pay:

- Retained learners at 30 days.
- Paying learners who renew at month 2.

## 10. Non-goals

Draft, to confirm:

- **Not a course.** No lessons, no curriculum, no certificate, no teacher.
- **Not a speed promise.** No "fluent by Christmas" (§3).
- **Not exam prep.** No exam formats, no practice tests, no KNM. Settled 16
  November (§4): it needs specialist knowledge.
- **Not a dictionary or translator.**
- **Not a booking service.** The rung-3 directory lists places; it does not
  take bookings or run the group (§5).
- **Not a social network.** `OPEN` — no profiles, comments or leaderboards?

## 11. Engagement is a constraint, not a flavour

Owner, 16 November:

> People advise me to watch TV but I get too frustrated opening the dictionary
> for words I don't know and I zone out, so I want something more engaging. I'm
> actually the very first test subject to see if the system works, because I also
> have ADHD — so if this system can teach me and keep me engaged, that's the test.

What follows:

- **The named user has ADHD.** Short sessions, an obvious next action, immediate
  feedback, and never leaving the exercise (§6, rule 5). These are
  ADHD-friendly and they are also simply good design — they do not turn the
  product into a niche product.
- **The acceptance test is the owner using it for weeks without stopping.** Not
  a survey, not a mockup review. If he stops, that is the finding.
- **He is a fair test, not a flattering one.** His A2 came after a year of courses
  to near B1 — that is precisely the learner in §4, not an expert early-adopter.
- **Engagement is not learning.** Keeping him playing is this section; whether
  the words are held is §9. Both must be true and neither implies the other. A
  product that is fun and teaches nothing fails the same test as a boring one
  that works.
- **Streaks and reminders are not automatically dark patterns here.** The usual
  objection to gamification is that it manufactures a need. When the user's real
  problem is *starting*, external structure helps. The line: structure that
  helps you begin is fine; guilt, loss-framing and nagging are not.
- **The tension with §2 stands.** The mechanism is repetition, so the pleasure has
  to come from pace, feel and getting faster — not from novelty. A game that is
  different every time is a game the learner is not drilling.

**What the mechanism is** — owner, 16 November:

> A reminder will be needed, and a sense of excitement, a visible and obvious
> progress — maybe a tally of how many words I've been exposed to and how many
> are learned.

| Piece | Status |
|---|---|
| **A tally: words met vs words held** | Decided. It is the same counter as §3, so the promise and the progress display are one thing, not two. |
| **A reminder** | Decided in principle; the channel is open. |
| **"Excitement"** | A design goal, not a mechanism. It comes from pace, from the tally moving and from getting faster — not from confetti, and not from novelty (§2). |

**The reminder's honest costs:**

- **Email is the only channel with infrastructure today.** `server/` already sends
  mail, and without an SMTP host it writes to `email-sink/`. Web push is
  unreliable on iOS, which is most of the audience.
- **A reminder is personal data processing.** It needs explicit consent, and
  `privacy.html` currently states there are no accounts and no personal data. That
  page has to change before this ships.

**The home page follows from this.** If the first screen is a tally of words met
and held, then the home is a counter plus an obvious next action — not six equal
painted tiles. This is the structural answer to "the site doesn't match the
product"; it is derived from the product, not from taste.

`OPEN` — which visible mechanism: a streak, a daily target, a visible next step,
several of them, or none.

## 12. Content: words by theme

Owner's answer, 16 November:

> We're building words in themes and I'm sure we can come up with the 2000 most
> commonly needed words, and more. There are no official word lists but we will
> build upon themes.

Consequences:

- **Themes are the navigation unit.** Not a frequency list, not CEFR bands as the
  primary axis. A learner chooses a theme; the words come with it.
- **Completeness is measurable per theme**, which is the answer to "are we done":
  a theme is done when its words are covered and have enough example contexts.
- **We choose themes; no authority chooses them for us.** So the theme set is an
  editorial product decision and needs to be written down and defended once, not
  invented per batch.
- **Frequency lists will disagree with us.** Where they do, we follow themes and
  say why — a word that is frequent but never needed in the learner's life is
  not our word.

### Themes are the navigation, not just the content

Owner, 16 November:

> We can organise the games also by theme. It will be a bit more complex but we
> can offer themes rather than just straight into games, and then guide them
> through a path of different games to practice that theme, so a theme will have
> to crosscut into different games.

So the learner chooses **a theme**, and the site walks them through a sequence of
*different games* that all practise it. The games become tools inside a theme,
not six doors on the home page.

Consequences:

1. **Two axes must be tagged independently.** Every word has a theme; every
   exercise belongs to a game. A theme path is a sequence of (theme, game)
   combinations, and content has to carry both tags.
2. **The game's own internal progression becomes secondary.** Entering by theme
   makes the band ladder inside a game a side door for people who want "more
   prepositions", not the main road.
3. **This answers "several games, different learning goals".** The goals are the
   themes; the games are the tools. A separate skill taxonomy
   (Woorden/Spelling/Betekenis/Zinnen/Spreken) is no longer needed as the top
   axis.

**Blocker to resolve:** Voorzetselpaden is organised by chunk and CEFR band and
its 713 chunks carry no theme tag. Either it gains theme tags — real content
work — or it stays the one game reachable only by its own path. `OPEN`.

### The theme set

Proposed 16 November; the owner called it "a good start" and added three needs.

| Theme | Covers | Picture | Free? |
|---|---|---|---|
| **Boodschappen** | supermarket, prices, quantities, paying, *waar staat de …?* | basket | **yes** |
| **Mensen** | small talk, invitations, feelings, birthdays | two speech bubbles | **yes** |
| **Wonen** | house, neighbours, rent, repairs | key | no |
| **Werk** | shift, tools, colleagues, safety | toolbox | no |
| **Gezondheid** | doctor, pharmacy, body, appointment | plaster | no |
| **Het lichaam** | body parts: head, arm, leg, back, knee, stomach, tooth | a body outline | no |
| **Kinderen en school** | crèche, teacher, playground, notes | school bag | no |
| **Gemeente en post** | letters, forms, DigiD, the system | envelope | no |
| **Reizen** | bus, train, tickets, the city | bus stop | no |
| **De weg** | asking, giving and following directions | turning arrow | no |
| **Afspraken** | booking, moving, cancelling, arriving late | calendar | no |

**Two different kinds of unit were hiding in the answer.** Themes are *worlds* —
where the learner is. Directions, booking an appointment and asking where a
product is are *actions* — what the learner does, and they crosscut worlds: an
appointment happens at the doctor, at the gemeente and at the garage alike.

Resolution taken here, to be confirmed:

- **Asking where a product is** lives **inside Boodschappen** — it is one chunk
  set, not a theme.
- **De weg** and **Afspraken** are promoted to themes, because both are drawable,
  both are exactly the felt need, and both have enough vocabulary to carry a
  theme.
- If more actions accumulate, a second axis gets made explicitly — later, and
  only when the list demands it.

Two themes are still the weakest as pictures even with their word beside them:
**Gemeente en post** (an envelope says "post", not "the system") and **Mensen**
(two speech bubbles say "talking", not "chatting with the neighbour"). Weak is
not the same as unusable — the word carries the rest.

Size check: 2,000 words over 10 themes is ~200 each, still a month of practice
per theme and a finishable unit.

**Body parts are their own theme** (owner, 16 November) rather than only a corner
of Gezondheid: the vocabulary is large, it is in daily use well beyond the
doctor, and it is the easiest theme in the set to draw — a body outline carries
most of it. Worth keeping in mind if the free pair is ever revisited.

### More themes — the owner wants them

Owner, 16 November: *"We need more themes."* Agreed, and it solves a problem:
ten themes makes the free slice 20% of the product and "2,000 words" a total
someone can finish — which fights the rate promise in §3.

**Worlds — where the learner is**

| Theme | Covers | Picture |
|---|---|---|
| **Eten en drinken** | restaurant, café, ordering, allergies | plate and cup |
| **Kleding** | shop, sizes, fitting, returns | hanger |
| **Bank en geld** | account, bills, insurance, borrowing | card |
| **Telefoon en internet** | provider, contract, helpdesk, no signal | phone |
| **Buurt** | neighbours, noise, shared hallway, the street | doorbell |
| **Sport en vrije tijd** | club, gym, hobby, team | whistle |
| **Solliciteren** | finding work, CV, the interview | briefcase |
| **Nood en politie** | emergency, theft, reporting, accident | emergency vehicle, lights on |
| **Zorg voor iemand anders** | calling on someone's behalf, an elderly parent | a hand on a shoulder |

**Actions — what the learner does**

| Theme | Covers | Picture |
|---|---|---|
| **Bellen** | phone calls as a skill: opening, spelling your name, being transferred | traditional handset |
| **Klachten** | broken, refund, complaint, escalating politely | item with a return arrow |
| **Mening geven** | agreeing, disagreeing, saying no, an opinion | head with a speech bubble |
| **Formulieren** | filling in a form, with help, signing | form and pen |

**Cost, so the number is chosen rather than wished.** A theme is roughly 200
words, one 512px pictogram, and a path through the games. 10 themes ≈ 2,000
words, 20 ≈ 4,000, 25 ≈ 5,000. Each theme added also shrinks the two free
themes' share of the product — a gate decision, not only a content one.

**Pictures all round — the owner is right.** Every theme can be drawn. The
picture does not have to carry the meaning alone: **the Dutch word sits with
it**, so the drawing only has to get the learner close. Emergency vehicles for
Nood en politie; a traditional handset for Bellen against a smartphone for
Telefoon en internet; a form and a pen for Formulieren against an envelope for
Gemeente en post.

The one thing no picture plus word can carry is **grammar** — `ik werk` versus
`ik heb gewerkt`, word order, `op` versus `aan`. Those are relations, not things,
which is why grammar lives inside exercises (and why Voorzetselpaden needed
scenes rather than icons).

`OPEN` — how many themes, and which of the above.

### The count

10 base + 13 candidates + **Het lichaam** = **24 themes**. That is:

- **24 drawable themes** — the picture plus the Dutch word together identify each
  one; no theme is left without a picture.
- roughly **4,800 words** at ~200 per theme — past A2 and into B1 territory,
  which is consistent with §2's "2,000 and more" but is a large authoring job.
- a free slice of **2 of 24, about 8%** of the product.

The set can be defined now and shipped over time — but a theme shown as a door
must have content behind it, so the visible set at launch is the content budget,
not the target.

**Words are global; paths are local.** With 24 overlapping themes the same word
arrives in several places — `de rekening` in Boodschappen and Eten en drinken,
`de knie` in Het lichaam and Gezondheid. That is good for practice and a trap
for counting: the word log in §8 must be keyed by **word**, not by
(theme, word), or a word met in two themes is counted twice and the counter in
§3 lies.

### Every theme hosts every activity that fits it

Goal set 16 November: a theme is not a word list, it is a path of different games.
So each theme should carry every activity that makes sense for its words.

Where a game genuinely does not fit a theme — a preposition game may have nothing
to say about `Klachten` — that is acceptable, but it must be a **recorded
decision, not an accident**, and the theme's path still needs enough variety to
feel like a path rather than the same drill relabelled.

## 13. Open decisions, collected

| # | Question | Blocks |
|---|---|---|
| ~~1~~ | ~~Which gap is primary (§2)~~ — **answered: vocabulary volume, pushed into memory by repetition** | — |
| ~~2a~~ | ~~Recognition or production?~~ — **answered: passive first, production via the Story Machine. The directory (rung 3) was dropped on 16 Nov (§5)** | — |
| ~~2b~~ | ~~What "in memory" means?~~ — **answered: spaced review sessions (§8)** | — |
| ~~2c~~ | ~~Where do the words come from?~~ — **answered: themes, ~2000+, our own list (§12)** | — |
| ~~3~~ | ~~Audience in one sentence (§4)~~ — **answered 16 Nov** | — |
| ~~4~~ | ~~May we claim outcomes only, never mechanisms (§3)~~ — **accepted 16 Nov** | All copy and the home page |
| ~~4b~~ | ~~Accept the definition of *held*~~ — **accepted 16 Nov in his own words: a tally of "how many words I've been exposed to and how many are learned"** | — |
| ~~5~~ | ~~Is inburgering exam prep in or out (§4, §10)~~ — **answered 16 Nov: out, it needs specialist knowledge** | — |
| ~~6~~ | ~~What stays free~~ — **answered 16 Nov: two themes (Boodschappen, Mensen) with every activity inside, nothing remembered for a guest** | — |
| ~~6b~~ | ~~Trial at all~~ — **answered 16 Nov: 6 weeks of full access, then paid** | — |
| ~~6c~~ | ~~Free account with a limited log~~ — **answered 16 Nov: the post-trial tier keeps a log on the two free themes** | — |
| ~~6d~~ | ~~The book~~ — **answered 16 Nov: on hold, sold separately via Amazon, grants nothing** | — |
| ~~6e~~ | ~~What a cancelled account keeps~~ — **answered 16 Nov: a frozen, read-only, counts-only log, no export** | — |
| ~~6f~~ | ~~Are the two free themes also capped at A1~~ — **answered 16 Nov: yes, both limits apply** | — |
| 6g | Which games fit which themes (§12) — every theme hosts every activity that makes sense, and exceptions get recorded | The theme paths, and §12's "every activity" in the gate |
| ~~7~~ | ~~Playful design or gamification (§11)~~ — **answered 16 Nov: a reminder, a visible tally (words met vs held), and a sense of excitement** | — |
| 7b | The reminder's channel and its consent (§11) | Email design, and the privacy page, which still says no accounts and no data |
| ~~8~~ | ~~Review state per word, chunk or theme (§8)~~ — **answered 16 Nov: per word, kept in the learner's account** | — |
| 8b | Does Voorzetselpaden gain theme tags, or stay reachable only by its own path (§12) | Whether a theme path can include it |
| 9 | Confirm the 24 themes and the free pair (§12) — **list as of 16 Nov: 24 themes, all drawable; Boodschappen + Mensen free** | All content work |
| ~~10~~ | ~~The rung-3 directory~~ — **dropped 16 Nov, out of scope** | — |
| 11 | ~~How the games group by learning goal~~ — **answered 16 Nov: themes are the axis; games crosscut them (§12)** | — |
| 12 | A second test subject (§11) — so the design is not validated on the founder alone. Not because he is unusually good: §2 says he is the typical post-A2 learner, but one person is still one person | Whether the product ships before a second person has used it for a month |
| 13 | Where visitors come from, now that the book is not carrying them (§7) | Acquisition, and whether the site sells itself cold |

## 14. What this document supersedes

Written 16 November 2026. Where any of these disagree with this file, this file wins.

| Doc | Status |
|---|---|
| `Docs/Concept.md` (now `archive/Concept.md`) | **Superseded on product.** Its audience (English speakers), its promise ("60–70% in days") and its four formats are replaced by §4, §3 and §5. The eight content pillars survive as a *content* taxonomy and are now listed in `game-catalogue.md`. |
| `Docs/mvp.md` (now `archive/mvp.md`) | **Dead.** Two validation experiments whose scope excludes accounts, the backend and more than one content type — all three now exist and ship. |
| `Docs/todo.md` (now `archive/todo.md`) | **Dead.** A pre-pivot book/website sketch; the game list it gestures at is `game-catalogue.md`. |
| `Docs/suggestions.md` (now `archive/suggestions.md`) | **Superseded**, being a pre-pivot brainstorm for English speakers and the book. The one live piece, the Uit Elkaar separable-verbs game and its word list, is now `uit-elkaar.md`. |
| `Docs/rethink/` (now `archive/rethink-2026-11-16/`) | **Superseded on structure** by §11 (home = the tally plus one action) and §12 (themes, not goals). Keep it for the art treatment in C, not for the five goal names. |
| `Docs/decisions.md` | Superseded on **the products and the gate** (§5, §7). Still the record of design decisions: colour, chrome, interface language. |
| `Docs/game-catalogue.md` | The games are still the catalogue. Its **learning-goal taxonomy** is replaced by themes (§12). |
| `Docs/games.md` | Still the game specs. |
| `CLAUDE.md` | Its "Where things stand" now records that §7 replaces the old band gate and that the new one is not built; the open-items table says the same. The old text is not to be restored. |

History is not deleted: the five files above are in `Docs/archive/` with a banner
at the top. By this repo's own convention, anything fully superseded belongs
there once its replacement is in place.
