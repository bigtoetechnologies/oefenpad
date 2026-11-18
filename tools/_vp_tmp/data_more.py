"""Batches added by the 15 Nov 2026 verb-preposition audit.

Schema per group:
  page, band, stem, action (single|cluster|append|convert), preps, noot,
  chunks[{chunk, gloss, cards[{id, scene, must, avoid, note, nl, en,
                              builds[2], q, answer, alt}]}]

Every card here is a proposal: no art yet, so no data-verdict and no counts
beyond the honest ones the page derives from the example total.
"""

GROUPS = [
# ---------------------------------------------------------------- A2
{
 "page": "a2.html", "band": "a2", "stem": "aanbellen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "aanbellen bij", "gloss": "to ring at someone's door",
  "cards": [{
   "id": "aanbellen-bij-de-buren",
   "scene": "a person stands on a doorstep with one finger pressed on a small round doorbell beside a closed front door, the other hand hanging at the side. A bicycle leans against the low garden wall behind. No second person is in the frame and the door stays shut. The finger on the round bell is the clearest mark.",
   "must": "ringing at the door of a house.",
   "avoid": "a fist raised to knock on the wood (kloppen op); a phone at the ear; an open door; a shop counter.",
   "note": "bij names whose door; kloppen op (B1) is knocking with a fist instead.",
   "nl": "Zij belt aan bij de buren.",
   "en": "She rings at the neighbours' door.",
   "builds": ["Zij belt aan bij de buren", "Hij belt aan bij de buren"],
   "q": "Is de deur open?", "answer": "Nee",
   "alt": "Iemand staat op een stoep met een vinger op een kleine ronde bel naast een dichte voordeur; achter hen leunt een fiets tegen een laag muurtje."
  }]
 }]
},
{
 "page": "a2.html", "band": "a2", "stem": "doen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "doen aan", "gloss": "to take part in a sport",
  "cards": [{
   "id": "doen-aan-tennis",
   "scene": "a person in shorts and a loose shirt stands on a tennis court with a racket in the right hand and a ball in the left, knees slightly bent and eyes on the net ahead. A second racket lies on a bench at the side. The court lines and the ball in the hand are the clearest mark.",
   "must": "taking part in a sport.",
   "avoid": "watching a match from a seat; a trophy; a television; a gym machine.",
   "note": "Dutch puts the sport after aan: zij doet aan tennis. The sport is what is taken up, not the place.",
   "nl": "Zij doen aan tennis.",
   "en": "They play tennis.",
   "builds": ["Zij doen aan tennis", "Wij doen aan tennis"],
   "q": "Houdt de persoon een racket vast?", "answer": "Ja",
   "alt": "Iemand in korte broek staat op een tennisbaan met een racket in de ene hand en een bal in de andere, knieen licht gebogen en de blik op het net."
  }]
 }]
},
{
 "page": "a2.html", "band": "a2", "stem": "halen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "halen uit", "gloss": "to take out of",
  "cards": [{
   "id": "halen-uit-de-kast",
   "scene": "a person stands before an open kitchen cupboard with one arm reached in at shoulder height pulling a white plate out towards themselves; a stack of plates stays on the shelf. The other hand holds the cupboard door open. The plate half out of the cupboard is the clearest mark.",
   "must": "taking something out of a container or a place.",
   "avoid": "putting a plate in (zetten in); an open fridge; carrying a plate to a table; a dishwasher.",
   "note": "uit names where the thing comes from; the separable uit goes to the end: zij haalt de borden uit de kast.",
   "nl": "Zij haalt de borden uit de kast.",
   "en": "She takes the plates out of the cupboard.",
   "builds": ["Zij haalt de borden uit de kast", "Hij haalt de borden uit de kast"],
   "q": "Blijven er borden in de kast staan?", "answer": "Ja",
   "alt": "Iemand staat voor een open keukenkastje met een arm naar binnen en trekt een wit bord naar zich toe; de rest van de stapel blijft op de plank."
  }]
 }]
},
{
 "page": "a2.html", "band": "a2", "stem": "rennen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "rennen naar", "gloss": "to run to",
  "cards": [{
   "id": "rennen-naar-de-bus",
   "scene": "a person runs towards a city bus standing with its door open at a stop, arms bent and one foot off the ground, a bag bouncing at the side. The driver waits behind the wheel. The raised leading foot and the open bus door are the clearest mark.",
   "must": "running towards a place.",
   "avoid": "walking calmly (lopen naar); a taxi; a train platform; a finish line with a crowd.",
   "note": "naar names the goal you run to; lopen naar is going there on foot at walking pace.",
   "nl": "Hij rent naar de bus.",
   "en": "He runs to the bus.",
   "builds": ["Hij rent naar de bus", "Zij rent naar de bus"],
   "q": "Staat de bus stil?", "answer": "Ja",
   "alt": "Iemand rent met gebogen armen naar een bus met een open deur bij een halte, een voet van de grond en een tas die meeschommelt."
  }]
 }]
},
{
 "page": "a2.html", "band": "a2", "stem": "rijden", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "rijden naar", "gloss": "to drive to",
  "cards": [{
   "id": "rijden-naar-de-stad",
   "scene": "a driver sits behind the wheel of a small car on an open road, the nose of the car pointed at a low town skyline in the distance and both hands on the wheel. A blank road sign stands at the verge. The car facing the town is the clearest mark.",
   "must": "driving to a place.",
   "avoid": "a bicycle on the road (fietsen naar); a bus stop; a parked car with nobody in it; a map held in a hand.",
   "note": "naar names the destination; rijden is by vehicle, fietsen by bike, lopen on foot.",
   "nl": "Wij rijden naar de stad.",
   "en": "We drive to the town.",
   "builds": ["Wij rijden naar de stad", "Zij rijden naar de stad"],
   "q": "Zit er iemand achter het stuur?", "answer": "Ja",
   "alt": "Iemand zit achter het stuur van een kleine auto op een open weg, de neus van de auto naar een lage skyline in de verte en beide handen aan het stuur."
  }]
 }]
},
{
 "page": "a2.html", "band": "a2", "stem": "smaken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "smaken naar", "gloss": "to taste of",
  "cards": [{
   "id": "smaken-naar-kaneel",
   "scene": "a person at a table lifts a fork with a piece of cake to the mouth, eyes closed and a pleased face. A whole cake on a stand and a cup of coffee stand beside the plate. The cake on the fork at the mouth is the clearest mark.",
   "must": "something having a taste.",
   "avoid": "a nose wrinkled at a bad smell (ruiken naar); a plate being carried; a cook at a stove; an empty plate.",
   "note": "naar names the taste; ruiken naar (A2) is the smell of the same thing.",
   "nl": "De taart smaakt naar kaneel.",
   "en": "The cake tastes of cinnamon.",
   "builds": ["De taart smaakt naar kaneel", "Het brood smaakt naar kaneel"],
   "q": "Proeft de persoon de taart?", "answer": "Ja",
   "alt": "Iemand aan tafel brengt een vork met een stuk taart naar de mond, ogen dicht en een tevreden gezicht; naast het bord staan een hele taart en een kop koffie."
  }]
 }]
},
# ---------------------------------------------------------------- A2+
{
 "page": "a2-plus.html", "band": "a2-plus", "stem": "verslaafd zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "verslaafd zijn aan", "gloss": "to be addicted to",
  "cards": [{
   "id": "verslaafd-aan-de-telefoon",
   "scene": "a person sits hunched on a sofa with a phone held close to the face in both hands, the room dark except for the glow of the screen, a tray of untouched food on the table before them. The phone at the face and the untouched food are the clearest mark.",
   "must": "not being able to stop using something.",
   "avoid": "a person enjoying a phone call; a book; a cigarette packet with a brand; a group of friends.",
   "note": "aan names the thing; verslaafd is an adjective, so zijn carries the tense: zij is verslaafd aan haar telefoon.",
   "nl": "Hij is verslaafd aan zijn telefoon.",
   "en": "He is addicted to his phone.",
   "builds": ["Hij is verslaafd aan zijn telefoon", "Zij is verslaafd aan haar telefoon"],
   "q": "Eet de persoon?", "answer": "Nee",
   "alt": "Iemand zit ineengedoken op een bank met een telefoon dicht bij het gezicht in beide handen; de kamer is donker op het scherm na en het eten op tafel blijft onaangeroerd."
  }]
 }]
},
{
 "page": "a2-plus.html", "band": "a2-plus", "stem": "bevriend zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "bevriend zijn met", "gloss": "to be friends with",
  "cards": [{
   "id": "bevriend-met-de-buurvrouw",
   "scene": "two people walk side by side on a pavement with arms loosely linked, both laughing, one carrying a shopping bag. They lean slightly towards each other and no third person is in the frame. The linked arms and the shared laugh are the clearest mark.",
   "must": "a lasting friendship between two people.",
   "avoid": "a handshake at a first meeting (kennismaken met); a work meeting; a family with children; two people arguing.",
   "note": "met names the other person; bevriend is an adjective, so zijn carries the tense: zij is bevriend met haar buurvrouw.",
   "nl": "Zij is bevriend met haar buurvrouw.",
   "en": "She is friends with her neighbour.",
   "builds": ["Zij is bevriend met haar buurvrouw", "Hij is bevriend met zijn buurman"],
   "q": "Lopen de twee mensen samen?", "answer": "Ja",
   "alt": "Twee mensen lopen gearmd naast elkaar op de stoep en lachen samen; een van hen draagt een boodschappentas en ze leunen licht naar elkaar toe."
  }]
 }]
},
{
 "page": "a2-plus.html", "band": "a2-plus", "stem": "verdriet hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "verdriet hebben om", "gloss": "to grieve over",
  "cards": [{
   "id": "verdriet-om-het-verlies",
   "scene": "a person sits on the edge of a bed with a photograph held in both hands, head bowed and shoulders low; a folded blanket lies beside them. The photograph is turned away from the viewer. The bowed head and the held photograph are the clearest mark.",
   "must": "sadness about something that happened.",
   "avoid": "tears of joy; a crowd at a funeral; a broken object; a person shouting.",
   "note": "om names the cause of the sadness; verdriet is a noun, so hebben carries the tense.",
   "nl": "Zij heeft verdriet om het verlies van haar hond.",
   "en": "She is grieving over the loss of her dog.",
   "builds": ["Zij heeft verdriet om het verlies van haar hond", "Hij heeft verdriet om het verlies van zijn hond"],
   "q": "Kijkt de persoon naar een foto?", "answer": "Ja",
   "alt": "Iemand zit op de rand van een bed met een foto in beide handen, het hoofd gebogen en de schouders laag; naast hen ligt een opgevouwen deken."
  }]
 }]
},
{
 "page": "a2-plus.html", "band": "a2-plus", "stem": "plezier hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "plezier hebben in", "gloss": "to enjoy doing something",
  "cards": [{
   "id": "plezier-in-het-tuinieren",
   "scene": "a person kneels in a vegetable garden with a small trowel, soil on the gloves, laughing with the head slightly back; a basket of carrots stands beside them. The trowel in the soil and the laughing face are the clearest mark.",
   "must": "enjoying an activity.",
   "avoid": "a party with balloons; a trophy; a person resting on a sofa; a shop counter.",
   "note": "in names the activity; plezier is a noun, so hebben carries the tense.",
   "nl": "Zij heeft plezier in het tuinieren.",
   "en": "She enjoys gardening.",
   "builds": ["Zij heeft plezier in het tuinieren", "Hij heeft plezier in het tuinieren"],
   "q": "Werkt de persoon in de tuin?", "answer": "Ja",
   "alt": "Iemand knielt in een groentetuin met een schepje in de grond en aarde aan de handschoenen, lachend met het hoofd licht achterover; naast hen staat een mand met wortels."
  }]
 }]
},
{
 "page": "a2-plus.html", "band": "a2-plus", "stem": "vriendelijk zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "vriendelijk zijn tegen", "gloss": "to be kind to",
  "cards": [{
   "id": "vriendelijk-tegen-de-klant",
   "scene": "a shop assistant stands behind a counter leaning slightly forward with a smile, handing a paper bag to an older customer who reaches for it. Both faces are turned to each other. The bag passing between their hands is the clearest mark.",
   "must": "treating another person kindly.",
   "avoid": "two people shouting; a handshake between strangers (kennismaken met); an empty counter; a queue of impatient people.",
   "note": "tegen names the person who receives the kindness; met is for doing something together.",
   "nl": "De verkoper is vriendelijk tegen de klant.",
   "en": "The shop assistant is kind to the customer.",
   "builds": ["De verkoper is vriendelijk tegen de klant", "De verkoper is vriendelijk tegen de klanten"],
   "q": "Geeft de verkoper iets aan de klant?", "answer": "Ja",
   "alt": "Een verkoper staat voorover geleund achter de toonbank met een glimlach en geeft een papieren zak aan een oudere klant die ervoor reikt; beide gezichten zijn naar elkaar toe."
  }]
 }]
},
]
