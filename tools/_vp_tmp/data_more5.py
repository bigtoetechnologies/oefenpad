"""Batches added by the 15 Nov 2026 verb-preposition audit.

Schema per group:
  page, band, stem, action (single|cluster|append|convert), preps, noot,
  chunks[{chunk, gloss, cards[{id, scene, must, avoid, note, nl, en,
                              builds[2], q, answer, alt}]}]

Every card here is a proposal: no art yet, so no data-verdict and no counts
beyond the honest ones the page derives from the example total.
"""

GROUPS = [
# ---------------------------------------------------------------- B2
{
 "page": "b2.html", "band": "b2", "stem": "bidden", "action": "cluster",
 "preps": ["tot", "om"],
 "noot": "tot names who is addressed; om names what is asked for",
 "chunks": [
 {
  "chunk": "bidden tot", "gloss": "to pray to",
  "cards": [{
   "id": "bidden-tot-god",
   "scene": "a woman in a headscarf kneels on a wooden bench in a dim church with her palms pressed flat together under her chin, eyes shut and lips slightly parted. A single candle burns in a holder beside her and the pew behind her stays empty. Her hands pressed together at the chin and the candle beside them are the clearest mark.",
   "must": "praying, addressed to someone.",
   "avoid": "bent over a prayer mat on the floor, face towards the ground (bidden om); a person at a desk with hands clasped asking for a job; a handshake; a seated person reading from a book.",
   "note": "tot names the one you address, and that addressee takes no article: zij bidt tot God. The ask itself goes with om in the twin chunk.",
   "nl": "Zij bidt tot God om kracht.",
   "en": "She prays to God for strength.",
   "builds": ["Zij bidt tot God om kracht", "Hij bidt tot God om kracht"],
   "q": "Heeft de vrouw haar ogen dicht?", "answer": "Ja",
   "alt": "Een vrouw met een hoofddoek knielt op een houten bank in een schemerige kerk met de handpalmen tegen elkaar onder haar kin en haar ogen dicht, naast een brandende kaars."
  }]
 }, {
  "chunk": "bidden om", "gloss": "to pray for",
  "cards": [{
   "id": "bidden-om-regen",
   "scene": "a row of farmers kneel in a dry field with their faces turned up to a white empty sky, hands lifted open at waist height. The cracked soil crumbles under their knees and one cow stands thin and still at the fence behind them. A single empty plastic watering can lies on its side. The lifted open hands and the cracked earth under them are the clearest mark.",
   "must": "asking for something in prayer.",
   "avoid": "hands pressed together in a church interior (bidden tot); a group carrying water to the field; a rain cloud already hanging overhead; a crowd singing.",
   "note": "om names what is asked for, not who is addressed; the same sentence can carry both: bidden tot God om regen.",
   "nl": "De boeren bidden om regen.",
   "en": "The farmers pray for rain.",
   "builds": ["De boeren bidden om regen", "De tuinders bidden om regen"],
   "q": "Staat er al een regenwolk boven het veld?", "answer": "Nee",
   "alt": "Een rij boeren knielt op een kurkdroog veld met de handen open opgeheven en het gezicht naar een lege lucht, naast droge gescheurde aarde en een omgevallen gieter."
  }]
 }]
},
{
 "page": "b2.html", "band": "b2", "stem": "drinken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "drinken op", "gloss": "to drink to",
  "cards": [{
   "id": "drinken-op-de-gezondheid",
   "scene": "an older man sits at a long table with a full glass of red wine in his raised right hand and both eyes on the woman across from him, who sits with her own glass lifted to shoulder height. Three other guests have glasses raised, and one carved cake stands untouched at the end of the table. The raised glasses held towards each other are the clearest mark.",
   "must": "drinking together as a wish for someone.",
   "avoid": "a glass tipped to the mouth and emptied (drinken uit, A0); a waiter carrying a tray; a group posing with empty glasses; a spilled drink.",
   "note": "The toast itself is proosten op (B1); drinken op is the act of drinking that follows it. The person wished well comes straight after op: drinken op de gezondheid.",
   "nl": "Zij drinken op de gezondheid van de bruid.",
   "en": "They drink to the bride's health.",
   "builds": ["Zij drinken op de gezondheid van de bruid", "Wij drinken op de gezondheid van de bruid"],
   "q": "Houdt de man zijn glas nog boven tafel?", "answer": "Ja",
   "alt": "Een oudere man zit aan een lange tafel met een vol glas wijn opgeheven in zijn hand, net als een vrouw en drie gasten tegenover hem, terwijl de taart onaangeroerd blijft."
  }]
 }]
},
{
 "page": "b2.html", "band": "b2", "stem": "jagen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "jagen op", "gloss": "to hunt",
  "cards": [{
   "id": "jagen-op-de-herten",
   "scene": "two hunters move between tall bare trees in a winter wood, both bent forward through the undergrowth with their whole attention ahead of them. The first one has paused with one flat open hand raised to signal a halt to the other. Far ahead between the trunks two deer stand still with their heads lifted towards the hunters. The open flat hand raised to stop the other hunter is the clearest mark.",
   "must": "pursuing wild animals.",
   "avoid": "shooting up into the trees (schieten op); a picture of deer on a wall; a person following someone through the city; a dog alone in a field.",
   "note": "op names the animal being pursued; schieten op is firing at something, which this scene does not show. jagen op also carries the everyday sense of chasing someone, as in de politie jaagt op de verdachte.",
   "nl": "Zij jagen op de herten in het bos.",
   "en": "They hunt deer in the wood.",
   "builds": ["Zij jagen op de herten in het bos", "Hij jaagt op de herten in het bos"],
   "q": "Rent er wild weg uit beeld?", "answer": "Nee",
   "alt": "Twee jagers bewegen gebogen tussen hoge kale bomen en een van hen steekt een vlakke hand op om de ander te laten stoppen, terwijl ver weg twee herten met geheven kop stilstaan."
  }]
 }]
},
{
 "page": "b2.html", "band": "b2", "stem": "zich hechten", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich hechten aan", "gloss": "to become attached to",
  "cards": [{
   "id": "zich-hechten-aan-de-gewoonte",
   "scene": "a man sits alone at a small kitchen table with a worn coffee cup cupped in both hands aslant so that only a little lies at the bottom. His eyes are on the window and a newspaper lies unopened on the cloth beside him. On the counter behind him a shelf of other cups stands untouched. The near-empty cup held aslant in both hands is the clearest mark.",
   "must": "a habit quietly becoming a need.",
   "avoid": "a man sniffing a full cup (wennen aan, B1); a bottle of spirits; a dog on his lap; a second person at the table.",
   "note": "Both pronouns show what is meant: hij hecht zich aan de gewoonte, but het hecht zich aan hem, the habit sticks to him. wennen aan (B1) is getting used to a thing so it stops bothering you; zich hechten aan is starting to depend on it.",
   "nl": "Hij hecht zich aan de gewoonte.",
   "en": "He is becoming attached to the habit.",
   "builds": ["Hij hecht zich aan de gewoonte", "Zij hecht zich aan de gewoonte"],
   "q": "Is het kopje nog helemaal vol?", "answer": "Nee",
   "alt": "Een man zit alleen aan een kleine keukentafel met een afgesleten halfleeg kopje schuin in zijn beide handen en kijkt uit het raam, naast een ongeopende krant en een rij onaangeroerde kopjes."
  }]
 }]
},
{
 "page": "b2.html", "band": "b2", "stem": "verdenken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "verdenken van", "gloss": "to suspect of",
  "cards": [{
   "id": "verdenken-van-diefstal",
   "scene": "a man in a dark coat stands in a shop doorway with one arm out and a finger pointing straight at the man by the till, who has turned his face away towards the window with both hands buried in his coat pockets. The shop assistant behind the counter has stopped halfway through wrapping a parcel and is looking from one man to the other. An empty space on the shelf beside the till is the same shape as the parcel in her hands. The pointing finger and the turned-away face are the clearest mark.",
   "must": "pointing at someone with an accusation.",
   "avoid": "a court room with a judge (beschuldigen van); a person holding a stolen object; readable labels on the shelves; a crowd of people, one of them singled out.",
   "note": "van names the deed the suspect is thought to have done: iemand verdenken van diefstal. beschuldigen van (B2) is the open charge; verdenken van is the doubt that comes first and needs no proof.",
   "nl": "Zij verdenken hem van diefstal.",
   "en": "They suspect him of theft.",
   "builds": ["Zij verdenken hem van diefstal", "Zij verdenken de buurman van diefstal"],
   "q": "Kijkt de beschuldigde de man met de wijzende vinger aan?", "answer": "Nee",
   "alt": "Een man in een donkere jas staat in een winkeldeur en wijst met gestrekte vinger naar een man bij de kassa die zijn gezicht afwendt met zijn handen in zijn zakken, terwijl de verkoopster aarzelt met een pakje."
  }]
 }]
},
{
 "page": "b2.html", "band": "b2", "stem": "wijten", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "wijten aan", "gloss": "to blame on",
  "cards": [{
   "id": "wijten-aan-het-weer",
   "scene": "a market trader stands in a half-empty stall with her arms out towards the wet street and her face turned up to the dark sky and the slanting rain. Her crates of fruit are stacked under a plastic sheet that is already blown loose at one corner. Three people pass under one umbrella without stopping, and a puddle spreads across the front of the stall. The bare stall under the rain is the clearest mark.",
   "must": "blaming a cause for a loss.",
   "avoid": "a leaking roof above her (liggen aan); a person blaming another person with a raised voice; a brightly lit stall full of customers; a shop closing sign with words on it.",
   "note": "The blamed cause follows aan, and it takes the whole weather, not the sky: hij wijt de lege kraam aan het weer. liggen aan names a cause as a plain fact; wijten aan adds that someone is laying the blame.",
   "nl": "Hij wijt de lege kraam aan het weer.",
   "en": "He blames the empty stall on the weather.",
   "builds": ["Hij wijt de lege kraam aan het weer", "Zij wijt de lege kraam aan het weer"],
   "q": "Verkoopt de marktkoopvrouw nog fruit?", "answer": "Nee",
   "alt": "Een marktkoopvrouw staat met gespreide armen in een halflege kraam onder de slagregen en kijkt naar de donkere lucht, terwijl drie mensen met een paraplu voorbijgaan en de kisten fruit onder een losgewaaide plaat liggen."
  }]
 }]
},
]
