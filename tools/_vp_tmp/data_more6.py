"""Closing batch from the 15 Nov 2026 verb-preposition audit.

The entries that were still absent from the pages after data_more..5, where
the reference list names a genuine fixed combination. Entries that are free
prepositions or variants of a chunk already taught are left out and argued
in Docs/voorzetselpaden/verb-prep-check-2026-11-15.md.
"""

GROUPS = [
# ---------------------------------------------------------------- A2+
{
 "page": "a2-plus.html", "band": "a2-plus", "stem": "interesse hebben",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "interesse hebben in", "gloss": "to be interested in",
  "cards": [{
   "id": "interesse-hebben-in-oude-klokken",
   "scene": "a woman kneels at an open wooden crate in a second-hand shop, lifting one small brass alarm clock up to her ear with both hands, her eyes fixed on its face and a small smile at the corner of her mouth. The crate holds six more clocks of mixed shapes, and the shopkeeper waits behind the counter with one hand on the till. A price card lies face down beside the crate. The clock held to her ear and her fixed eyes on it are the clearest mark.",
   "must": "examining an object with obvious pleasure and attention.",
   "avoid": "a face turned away or a shrug; money changing hands; numbers or letters on the clock faces; a phone held up to take a picture.",
   "note": "The same meaning as geinteresseerd zijn in (A2), with the noun in front of hebben: zij heeft interesse in de oude klokken. The preposition stays in in both.",
   "nl": "Zij heeft interesse in de oude klokken.",
   "en": "She is interested in the old clocks.",
   "builds": ["Zij heeft interesse in de oude klokken", "Hij heeft interesse in de oude klokken"],
   "q": "Houdt de vrouw de klok bij haar oor?", "answer": "Ja",
   "alt": "Een vrouw knielt bij een open houten kist in een tweedehandswinkel en houdt een klein koperen wekkertje aan haar oor, met haar ogen op de wijzerplaat, terwijl de winkelier achter de toonbank wacht."
  }]
 }]
},
# ---------------------------------------------------------------- B1
{
 "page": "b1.html", "band": "b1", "stem": "gelijk hebben",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "gelijk hebben met", "gloss": "to be right about",
  "cards": [{
   "id": "gelijk-hebben-met-de-kritiek",
   "scene": "a woman at the head of a meeting table stands with one finger pressed to a large chart pinned to the wall and her chin lifted towards the two men seated below it. The chart carries a single rising line with nothing written on it. Both men nod, one with a raised eyebrow and a flat hand on the table. A stack of blank papers lies in front of them. The pointing finger on the chart met by two nodding heads is the clearest mark.",
   "must": "one person making a point and the others agreeing with it.",
   "avoid": "words or numbers on the chart; a clenched fist; a person with their back turned; a thumbs-down; two people shaking hands.",
   "note": "met names the point that is right: zij heeft gelijk met haar kritiek. Bare gelijk hebben says only that someone is right; het eens zijn met (B1) is agreeing with a person, which is a different act.",
   "nl": "Zij heeft gelijk met haar kritiek op het plan.",
   "en": "She is right about her criticism of the plan.",
   "builds": ["Zij heeft gelijk met haar kritiek op het plan", "Hij heeft gelijk met zijn kritiek op het plan"],
   "q": "Knikken de twee mannen met de vrouw mee?", "answer": "Ja",
   "alt": "Een vrouw staat aan het hoofd van een vergadertafel en wijst met een vinger naar een grote grafiek aan de muur met een enkele stijgende lijn, terwijl twee mannen aan de tafel instemmend knikken."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "weten van",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "weten van", "gloss": "to know about",
  "cards": [{
   "id": "weten-van-de-verrassing",
   "scene": "two women stand close together in an office corridor, one with a hand cupped at the side of her mouth leaning towards the other, who has a hand pressed flat to her chest and her eyebrows high. Behind them a closed door carries three balloons tied to the handle, and a wrapped box sits on a small table beside it. Every other door in the corridor is shut. The whisper and the hand on the chest are the clearest mark.",
   "must": "news passed quietly to someone who did not know it.",
   "avoid": "a person opening the wrapped box; a burst balloon; a group singing; writing on the door or the box; a telephone held to the ear.",
   "note": "van names the fact or event the person knows about: zij weet van de verrassing. weten alone takes a whole clause; weten van takes only the thing.",
   "nl": "Zij weet van de verrassing.",
   "en": "She knows about the surprise.",
   "builds": ["Zij weet van de verrassing", "Hij weet van de verrassing"],
   "q": "Houdt de vrouw haar hand voor haar mond?", "answer": "Ja",
   "alt": "Twee vrouwen staan dicht bij elkaar in een kantoorgang; de ene fluistert met een hand bij haar mond, de andere legt een hand op haar borst met opgetrokken wenkbrauwen, naast een gesloten deur met drie ballonnen en een ingepakt cadeau."
  }]
 }]
},
{
 "page": "b1.html", "band": "b1", "stem": "hebben aan",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "hebben aan", "gloss": "to benefit from",
  "cards": [{
   "id": "hebben-aan-de-buurman",
   "scene": "a man stands high on an aluminium stepladder with both hands pushing a gutter bracket back into place, and below him a neighbour holds the ladder steady with one foot against the lower rung and both hands on the sides, looking up. A bucket of tools sits on the paving beside them. The ladder held firm by the man below, who watches the man above, is the clearest mark.",
   "must": "one person steadying another's work, and the worker relying on it.",
   "avoid": "money handed over; a handshake; a ladder with nobody below it; a person holding a sign; two people lifting the same object.",
   "note": "aan names where the help comes from: hij heeft veel aan zijn buurman. The thing received is usually veel or niets: daar heb ik niets aan.",
   "nl": "Hij heeft veel aan zijn buurman.",
   "en": "He gets a lot of help from his neighbour.",
   "builds": ["Hij heeft veel aan zijn buurman", "Zij heeft veel aan haar buurman"],
   "q": "Houdt de buurman de ladder vast?", "answer": "Ja",
   "alt": "Een man staat hoog op een aluminium trap en duwt een gootbeugel terug op zijn plaats, terwijl een buurman beneden de trap met beide handen vasthoudt en naar hem opkijkt, naast een emmer gereedschap."
  }]
 }]
},
# ---------------------------------------------------------------- B1+
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "delen",
 "action": "append", "preps": ["in", "met", "door"],
 "noot": "in is having a share of something; met is handing part of what you have to someone; door is dividing a number into equal parts.",
 "chunks": [{
  "chunk": "delen door", "gloss": "to divide by",
  "cards": [{
   "id": "delen-door-twaalf",
   "scene": "a teacher kneels at a low classroom table between three children and moves twelve identical wooden blocks from one pile into three equal rows, one row in front of each child. Each child has both hands open above an empty tray as the last row is filled. The blocks are all the same size and colour, and nothing is written anywhere on the table. The three equal rows of blocks are the clearest mark.",
   "must": "a number of things split into equal shares by a given number.",
   "avoid": "unequal rows; digits or sums written anywhere; a calculator; one child holding all the blocks (verdelen onder); a cake cut in slices (verdelen in).",
   "note": "door names the number you divide by: je deelt twaalf door drie, where twaalf counts the blocks on the table. verdelen in splits one whole into parts, verdelen onder hands those parts to people, and delen door is the sum itself.",
   "nl": "De juf deelt twaalf door drie.",
   "en": "The teacher divides twelve by three.",
   "builds": ["De juf deelt twaalf door drie", "De meester deelt twaalf door drie"],
   "q": "Liggen de blokken in drie gelijke rijen?", "answer": "Ja",
   "alt": "Een juf knielt bij een lage tafel tussen drie kinderen en verdeelt twaalf gelijke houten blokken in drie even grote rijen, terwijl elk kind de handen boven een lege bak houdt."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "in staat zijn",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "in staat zijn tot", "gloss": "to be capable of",
  "cards": [{
   "id": "in-staat-zijn-tot-zware-arbeid",
   "scene": "a woman in dark overalls lifts one end of a long steel beam onto a wooden trestle with her knees bent and both hands under the edge, a dark sweat mark down the back of her shirt. Two men stand in the background with their arms hanging and their tools down, watching her. The other end of the beam already rests on a second trestle. The beam held up alone, with two idle men behind, is the clearest mark.",
   "must": "one person doing physically heavy work alone.",
   "avoid": "two people lifting together; a person sitting down to rest; a doctor with a note in hand; a machine doing the lifting.",
   "note": "tot takes a noun, never a bare verb: in staat zijn tot zware arbeid. The verbal form is in staat zijn om te werken, which says the same about what someone can do.",
   "nl": "Zij is in staat tot zware arbeid.",
   "en": "She is capable of heavy labour.",
   "builds": ["Zij is in staat tot zware arbeid", "Hij is in staat tot zware arbeid"],
   "q": "Tilt de vrouw de balk alleen op?", "answer": "Ja",
   "alt": "Een vrouw in een donkere overall tilt met gebogen knieën en beide handen het ene uiteinde van een lange stalen balk op een houten schraag, terwijl twee mannen op de achtergrond met hangende armen toekijken."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "iets hebben",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "iets hebben met", "gloss": "to be involved with",
  "cards": [{
   "id": "iets-hebben-met-elkaar",
   "scene": "a man and a woman sit at a small cafe table with their chairs pulled close and turned towards each other, her hand resting on his forearm and his head tipped down towards hers. At the next table a woman holds her cup at her lips and watches them over the rim with her eyebrows raised. Two untouched cups stand between the couple. The hand on the forearm and the watching woman behind are the clearest mark.",
   "must": "two people plainly a couple, and a third person noticing.",
   "avoid": "a kiss; hearts; a wedding ring shown close up; a shared bill on the table; two people in office clothes at a desk.",
   "note": "iets hebben met iemand is the everyday way to say two people are romantically involved, and the thing itself is never named: zij heeft iets met hem.",
   "nl": "Zij heeft iets met hem.",
   "en": "She is involved with him.",
   "builds": ["Zij heeft iets met hem", "Hij heeft iets met haar"],
   "q": "Zit er iemand naar het paar te kijken?", "answer": "Ja",
   "alt": "Een man en een vrouw zitten dicht bij elkaar aan een klein cafeetje met haar hand op zijn onderarm, terwijl een vrouw aan de volgende tafel met opgetrokken wenkbrauwen over haar kopje naar hen kijkt."
  }]
 }]
},
# ---------------------------------------------------------------- B2
{
 "page": "b2.html", "band": "b2", "stem": "schieten",
 "action": "single", "preps": None, "noot": None, "chunks": [{
  "chunk": "schieten op", "gloss": "to shoot at",
  "cards": [{
   "id": "schieten-op-het-doel",
   "scene": "a young woman in a sports jacket stands in a shooting-range lane with a small rifle at her shoulder and one eye shut, aiming down the lane at a round paper target on a frame far ahead. Spent cases lie in a row on the bench beside her and a trainer watches from two steps behind with folded arms. The rifle at her shoulder and the distant round target are the clearest mark.",
   "must": "aiming a firearm at a target.",
   "avoid": "a fallen animal; blood; a person on the ground; a wood with deer (jagen op); numbers or writing on the target.",
   "note": "op names what the shot is aimed at. jagen op (B2) is hunting an animal, a different act with a different purpose.",
   "nl": "Zij schiet op het doel.",
   "en": "She shoots at the target.",
   "builds": ["Zij schiet op het doel", "Hij schiet op het doel"],
   "q": "Staat de trainer achter de schutter?", "answer": "Ja",
   "alt": "Een jonge vrouw in een sportjack staat op een schietbaan met een klein geweer tegen haar schouder en een oog dicht, richtend op een ronde papieren schijf ver weg, terwijl een trainer met gekruiste armen achter haar staat."
  }]
 }]
},
{
 "page": "b2.html", "band": "b2", "stem": "verlossen",
 "action": "cluster", "preps": ["uit", "van"],
 "noot": "uit names the trap you are taken out of; van names the burden you no longer carry.",
 "chunks": [
 {
  "chunk": "verlossen uit", "gloss": "to free from",
  "cards": [{
   "id": "verlossen-uit-het-net",
   "scene": "a boy kneels on the grass beside a low hedge with both hands opening the folds of a fine net, and a small bird rises out of it with its wings wide, already above his head. The net lies loose and empty on the ground behind him and a bicycle stands at the edge of the path. The bird in the air over the open net is the clearest mark.",
   "must": "a trapped creature set free and leaving.",
   "avoid": "a bird still caught in the net; a cage with the door shut; a person carrying a gun; a bird held in a hand.",
   "note": "uit names the trap or enclosure you are taken out of: hij verlost de vogel uit het net. van would name a burden instead.",
   "nl": "Hij verlost de vogel uit het net.",
   "en": "He frees the bird from the net.",
   "builds": ["Hij verlost de vogel uit het net", "Zij verlost de vogel uit het net"],
   "q": "Zit de vogel nog in het net?", "answer": "Nee",
   "alt": "Een jongen knielt op het gras bij een lage heg en opent met beide handen de plooien van een fijn net, terwijl een klein vogeltje met wijde vleugels opstijgt boven zijn hoofd en het net leeg achterblijft."
  }]
 },
 {
  "chunk": "verlossen van", "gloss": "to deliver from",
  "cards": [{
   "id": "verlossen-van-de-pijn",
   "scene": "a woman sits back in a dentist chair with her head on the rest and her eyes shut, one hand still gripping the armrest while the other lies open on her lap. The dentist beside her has stepped back and is pulling a glove from one hand, and the tray of instruments is pushed away. The open relaxed hand beside the still gripping one is the clearest mark.",
   "must": "pain or a burden that has just been taken away.",
   "avoid": "a patient still in pain with a clenched jaw; a syringe held up; a person leaving through a door (verlossen uit); writing on the wall.",
   "note": "van names what is taken away: de tandarts verlost haar van de pijn. It is the burden, not a place.",
   "nl": "De tandarts verlost haar van de pijn.",
   "en": "The dentist frees her from the pain.",
   "builds": ["De tandarts verlost haar van de pijn", "De arts verlost hem van de pijn"],
   "q": "Doet de tandarts nog iets aan haar tanden?", "answer": "Nee",
   "alt": "Een vrouw zit achterover in een tandartsstoel met haar ogen dicht en een hand nog om de leuning, terwijl de tandarts terugstapt en een handschoen uittrekt naast een weggeschoven dienblad."
  }]
 }]
},
]
