"""Batches added by the 15 Nov 2026 verb-preposition audit.

Schema per group:
  page, band, stem, action (single|cluster|append|convert), preps, noot,
  chunks[{chunk, gloss, cards[{id, scene, must, avoid, note, nl, en,
                              builds[2], q, answer, alt}]}]

Every card here is a proposal: no art yet, so no data-verdict and no counts
beyond the honest ones the page derives from the example total.

B1+ batch 4. Two of these groups are not "single": b1-plus already carries a
section for the stem, so they attach to it instead of opening a second one.
zich verzekeren already holds zich verzekeren van (to secure for oneself), so
the new chunk is an append. delen already holds delen in (to share in), so the
new chunk is a convert.
"""

GROUPS = [
# ---------------------------------------------------------------- B1+
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "zich specialiseren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich specialiseren in", "gloss": "to specialise in",
  "cards": [{
   "id": "zich-specialiseren-in-de-zorg",
   "scene": "a care worker stands close beside an older woman in a high-backed chair, one knee bent to the floor and one hand steadying the woman's forearm while the other holds a blood-pressure cuff wrapped round the upper arm. Around them stand a walking frame, a jug of water and a folded blanket on a low cabinet. The cuff wrapped round the bare upper arm is the clearest mark.",
   "must": "one narrow branch of work, practised on one person.",
   "avoid": "a doctor in a white coat with a nameless diploma on the wall (afstuderen); a wide waiting room full of patients (werken in); a desktop screen with charts; a handshake at a first meeting.",
   "note": "in names the one field of work the person has chosen, not the building or the employer. The verb is reflexive: zij specialiseert zich in de zorg. Compare zich toeleggen op, which is the same choice made of a task rather than a trade.",
   "nl": "Zij specialiseert zich in de zorg voor ouderen.",
   "en": "She specialises in care for the elderly.",
   "builds": ["Zij specialiseert zich in de zorg voor ouderen", "Hij specialiseert zich in de zorg voor ouderen"],
   "q": "Werkt de persoon met een oudere vrouw?", "answer": "Ja",
   "alt": "Een zorgverlener zit op een knie naast een oudere vrouw in een hoge stoel, een hand om haar onderarm en de andere aan een bloeddrukband om haar bovenarm; naast hen staan een rollator, een kan water en een opgevouwen deken."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "zich abonneren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich abonneren op", "gloss": "to subscribe to",
  "cards": [{
   "id": "zich-abonneren-op-de-krant",
   "scene": "a man leans over the corner of a table in his own hallway in a coat that is still on, tearing the paper band off a folded newspaper and easing the first page out with both thumbs. Two more folded newspapers lie in a neat pile beside the door, and a postcard and a brown envelope sit unopened on the sideboard. The paper band being torn off the folded newspaper is the clearest mark.",
   "must": "receiving a paper regularly rather than buying it once.",
   "avoid": "a single newspaper and coins on a shop counter (kopen); a hand posting a letter (opsturen); a blank order form on a screen; a shelf of many different magazines.",
   "note": "op names the thing that arrives, usually by post or feed. The verb is reflexive: hij abonneert zich op de krant. Compare lid worden van, which is joining a club rather than receiving something.",
   "nl": "Hij abonneert zich op de krant.",
   "en": "He subscribes to the newspaper.",
   "builds": ["Hij abonneert zich op de krant", "Zij abonneert zich op de krant"],
   "q": "Liggen er meerdere kranten bij de deur?", "answer": "Ja",
   "alt": "Een man in een jas leunt over een tafeltje in zijn gang en trekt het bandje van een gevouwen krant, met de eerste pagina al los tussen zijn duimen; bij de deur liggen nog twee kranten op een stapel."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "zich beperken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich beperken tot", "gloss": "to limit oneself to",
  "cards": [{
   "id": "zich-beperken-tot-de-kern",
   "scene": "a woman stands at a lectern with a single sheet of paper on it and one finger of her right hand tracing a short line down the sheet, the left hand resting flat on the wood. Behind her a screen shows one shape, and a whole stack of pages lies on the floor beside the lectern, turned face down. The one sheet on the lectern against the stack on the floor is the clearest mark.",
   "must": "choosing to keep to a small part of what is there.",
   "avoid": "a hand holding out one object (beperken tot); a person fenced in (belemmeren); an empty room; two people arguing.",
   "note": "tot names the limit chosen on purpose: de rest laat zij weg. The verb is reflexive in this meaning, zij beperkt zich tot de kern, and the reflexive is what makes it her own choice.",
   "nl": "Zij beperkt zich tot de kern van het verhaal.",
   "en": "She limits herself to the heart of the story.",
   "builds": ["Zij beperkt zich tot de kern van het verhaal", "Hij beperkt zich tot de kern van het verhaal"],
   "q": "Heeft de vrouw een stapel papier op de grond gelegd?", "answer": "Ja",
   "alt": "Een vrouw staat achter een lessenaar met een enkel vel papier en volgt met een vinger een korte regel, haar andere hand plat op het hout; achter haar staat een scherm met een vorm en op de grond een stapel omgekeerde bladzijden."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "verzekeren", "action": "append",
 "preps": ["van", "tegen"], "noot": "van is making sure of something you want; tegen is paying a company to cover a risk.", "chunks": [{
  "chunk": "zich verzekeren tegen", "gloss": "to insure against",
  "cards": [{
   "id": "zich-verzekeren-tegen-schade",
   "scene": "a person sits at a kitchen table signing a sheet with a pen while an adviser opposite slides a folder across. Between them stands a small model of a house with a tiny open umbrella held over its roof. Both people look down at the model house and the room is dry and calm. The umbrella over the model house is the clearest mark.",
   "must": "taking out cover against damage before it happens.",
   "avoid": "a flooded room being inspected after the event (uitkeren); a locked door and a burglar (beveiligen); a car at a garage; a folded umbrella standing by the door with no house in sight.",
   "note": "tegen names the damage or event that is covered: brand, diefstal, schade. The cover is taken before the loss, which is what the umbrella over the model house shows. The twin on this page is zich verzekeren van, which is making certain of a place for yourself, with no money and no risk involved.",
   "nl": "Hij verzekert zich tegen schade aan zijn huis.",
   "en": "He insures against damage to his house.",
   "builds": ["Hij verzekert zich tegen schade aan zijn huis", "Zij verzekert zich tegen schade aan haar huis"],
   "q": "Staat er een paraplu boven het huisje?", "answer": "Ja",
   "alt": "Iemand zit aan een keukentafel een vel te ondertekenen terwijl een adviseur tegenover hen een map overhandigt; tussen hen staat een huisje met een kleine open paraplu erboven."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "zich verontschuldigen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "zich verontschuldigen voor", "gloss": "to apologise for",
  "cards": [{
   "id": "zich-verontschuldigen-voor-het-lawaai",
   "scene": "a man stands on a neighbour's doorstep with his shoulders drawn in and his head lowered, one hand offered forwards palm up and the other holding the edge of a party hat. Through the open door behind the neighbour a long table with many used cups shows, and inside a speaker stands on the floor with its cone facing the hallway. The offered palm and the party hat are the clearest mark.",
   "must": "one person owning a nuisance they made and saying sorry for it.",
   "avoid": "a hand being shaken (bedanken); a doctor explaining a complaint (klagen over); a raised hand asking a question; a wrapped gift held out.",
   "note": "voor names the wrong that is being owned: het lawaai, het misverstand. The verb is reflexive, hij verontschuldigt zich, which is the same shape as zich schamen voor, where the feeling is the thing named.",
   "nl": "Hij verontschuldigt zich voor het lawaai van het feest.",
   "en": "He apologises for the noise from the party.",
   "builds": ["Hij verontschuldigt zich voor het lawaai van het feest", "Zij verontschuldigt zich voor het lawaai van het feest"],
   "q": "Draagt de man een feesthoedje in zijn hand?", "answer": "Ja",
   "alt": "Een man staat met ingetrokken schouders en gebogen hoofd op de stoep van de buren, een hand open naar voren en in de andere een feesthoedje; achter de open deur staat een lange tafel met gebruikte kopjes."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "vrezen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "vrezen voor", "gloss": "to fear for",
  "cards": [{
   "id": "vrezen-voor-de-gevolgen",
   "scene": "a foreman stands at a site gate with both hands on a blank sign board turned towards his chest, the brow low and the mouth flat. Behind the ground-level barrier river water already stands around the feet of a digger, and a crane stands idle with its arm not moving. The water at the digger's feet in the low site is the clearest mark.",
   "must": "expecting a bad result and being worried by it.",
   "avoid": "a person startled by something behind them (schrikken van); a face grinning at a high dive (durven); a mother hiding a small child behind her from a stranger (bang zijn voor); a pile of money.",
   "note": "voor names what is at risk, not the thing that frightens you: hij vreest voor zijn baan. The fear is held about something, the same voor as in bang zijn voor, but vrezen looks forwards to a consequence rather than at a present threat.",
   "nl": "De voorman vreest voor de gevolgen van de regen.",
   "en": "The foreman fears the consequences of the rain.",
   "builds": ["De voorman vreest voor de gevolgen van de regen", "De buurman vreest voor de gevolgen van de regen"],
   "q": "Staat er water bij de graafmachine?", "answer": "Ja",
   "alt": "Een voorman staat bij een bouwhek met beide handen aan een leeg bord tegen zijn borst, wenkbrauwen laag; achter het hek staat water rond de voeten van een graafmachine en een kraan staat stil."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "condoleren", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "condoleren met", "gloss": "to offer condolences on",
  "cards": [{
   "id": "condoleren-met-het-verlies",
   "scene": "a young man stands facing a woman at her own front door, his right hand laid over her forearm and his head bowed slightly, while the woman holds a folded card against her chest and lifts it towards him. A wreath leans against the wall by the door with a blank ribbon, and a van with its back doors open waits at the kerb. The young man's hand laid over her forearm is the clearest mark.",
   "must": "greeting a bereaved person and naming the loss.",
   "avoid": "two people laughing; a handshake over a contract (tekenen bij); a single word of thanks (bedanken voor); a wreath alone with nobody beside it (herdenken).",
   "note": "condoleren is nearly always followed by met and the loss: met het verlies van je vader. It is the fixed phrase for this occasion, and the object is the death, not the person grieving.",
   "nl": "Wij condoleren de familie met het verlies van hun vader.",
   "en": "We offer the family our condolences on the loss of their father.",
   "builds": ["Wij condoleren de familie met het verlies van hun vader", "Zij condoleren de familie met het verlies van hun moeder"],
   "q": "Draagt de vrouw een kaart tegen haar borst?", "answer": "Ja",
   "alt": "Een jonge man staat bij een voordeur met een hand op de onderarm van een vrouw, het hoofd licht gebogen, terwijl zij een gevouwen kaart tegen haar borst houdt; naast de deur leunt een krans met een leeg lint tegen de muur."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "medelijden hebben", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "medelijden hebben met", "gloss": "to pity",
  "cards": [{
   "id": "medelijden-hebben-met-de-bedelaar",
   "scene": "a seated man on a folded cardboard sheet inside a station passage holds an empty paper cup up in one hand while the other grips the edge of the cardboard, knees drawn in and shoulders down. A businesswoman stops a step in front of him with a hand pressed to her chest and her mouth turned down, a briefcase hanging from the other hand while everyone behind her walks on past. The hand pressed to the woman's chest is the clearest mark.",
   "must": "feeling sorry for someone, with no gift passing between them.",
   "avoid": "coins dropped into a cup (geven aan); two people laughing together (plezier hebben in); a doctor and a patient (zorgen voor); a queue at a till.",
   "note": "met names the person the feeling is about; medelijden is a noun, so hebben carries the tense. Nothing changes hands: the person feels it, in the pose and the face, not in a gesture of giving.",
   "nl": "Zij heeft medelijden met de bedelaar.",
   "en": "She pities the beggar.",
   "builds": ["Zij heeft medelijden met de bedelaar", "Hij heeft medelijden met de bedelaar"],
   "q": "Geeft de vrouw de man geld?", "answer": "Nee",
   "alt": "Een zittende man op een stuk karton in een stationsgang houdt een lege papieren beker op, de knieen ingetrokken; een vrouw met aktetas blijft een stap voor hem staan met een hand op haar borst, terwijl de mensen achter haar doorlopen."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "neerkijken", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "neerkijken op", "gloss": "to look down on",
  "cards": [{
   "id": "neerkijken-op-de-buren",
   "scene": "a man stands on his own balcony with both hands on the railing, chin lifted and eyelids lowered, looking down the side of the building at a neighbour who is crouched at street level wiping a bicycle chain with a rag. A folded newspaper is tucked under the standing man's arm. A row of parked bins stands along the kerb. The lowered eyelids on the face turned downwards are the clearest mark.",
   "must": "a person above judging a person below without going down.",
   "avoid": "a person at a window watching the street (kijken naar); a hand holding a phone (afkijken van); two people shaking hands; an open book.",
   "note": "The separable op goes to the end: hij kijkt neer op de buren. It is never literal, unlike kijken naar, which is where the eyes are pointed, and unlike opkijken tegen, which is respect for someone rather than contempt.",
   "nl": "Hij kijkt neer op de buren.",
   "en": "He looks down on the neighbours.",
   "builds": ["Hij kijkt neer op de buren", "Zij kijkt neer op de buren"],
   "q": "Kijkt de man naar beneden?", "answer": "Ja",
   "alt": "Een man staat op zijn eigen balkon met beide handen op de leuning, kin omhoog en oogleden laag, en kijkt langs de gevel naar een buur die op straat een fietsketting schoonmaakt; onder zijn arm zit een krant."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "af zijn", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "af zijn van", "gloss": "to be rid of",
  "cards": [{
   "id": "af-zijn-van-de-griep",
   "scene": "a woman sits up in bed in a bright bedroom with her hair loose and her cheeks clear, balling up a tissue in both hands and turning her face up towards the window. On the bedside table stand an empty glass, a strip of tablets pushed aside, and a folded thermometer. The window is open and a curtain is lifted by the draught. The balled tissue thrown aside on a bright morning is the clearest mark.",
   "must": "a complaint being over, with the person up and about.",
   "avoid": "a person lying flat under a blanket with a thermometer (ziek zijn); a doctor's waiting room; a hand counting money (afrekenen); a person asleep.",
   "note": "The frame is van iets af zijn, with the thing left behind between van and af: zij is van de griep af. af is not separable here but a separate word that the van-phrase comes before.",
   "nl": "Zij is eindelijk van de griep af.",
   "en": "She is finally rid of the flu.",
   "builds": ["Zij is eindelijk van de griep af", "Hij is eindelijk van de griep af"],
   "q": "Is het raam open?", "answer": "Ja",
   "alt": "Een vrouw zit overeind in bed met los haar en een frisse huid, een prop zakdoek in beide handen en het gezicht naar het open raam; op het nachtkastje staan een leeg glas, een strip tabletten en een dichtgeklapte thermometer."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "afwillen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "afwillen van", "gloss": "to want to get rid of",
  "cards": [{
   "id": "afwillen-van-de-oude-bank",
   "scene": "a man stands behind a worn sofa at the top of the steps to his courtyard, both arms opening towards it and his palms turned up at a younger couple standing on the pavement below. The sofa has two torn cushions resting on its seat, and a roll of rope and a trolley with one wheel off stand beside it. The torn cushions lying loose on the seat are the clearest mark.",
   "must": "wanting something out of the house and offering it away.",
   "avoid": "two people pulling one object in a tug (twisten over); a hand sweeping crumbs from a table (opruimen); a shop assistant serving a customer (verkopen aan); a person holding one item at a door (beperken tot).",
   "note": "The frame is van iets af willen, with the thing between van and af: zij wil van die bank af. Here af is a separate word after willen, not glued to the verb.",
   "nl": "Zij willen van de oude bank af.",
   "en": "They want to get rid of the old sofa.",
   "builds": ["Zij willen van de oude bank af", "Hij wil van de oude bank af"],
   "q": "Staan er mensen op de stoep naar de bank te kijken?", "answer": "Ja",
   "alt": "Een man staat achter een versleten bank bovenaan de trap naar zijn binnenplaats en opent beide armen met de handpalmen omhoog voor een jong stel op de stoep; op de bank liggen twee gescheurde kussens."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "betekenen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "betekenen voor", "gloss": "to mean to",
  "cards": [{
   "id": "betekenen-voor-de-buurt",
   "scene": "an older man sits on the low step of his own front door with a boy beside him holding a small pot with a seedling and a sleeve of seed packets in his hands. The man's right hand rests on the boy's shoulder and both are looking at the soil along the path where green shoots already stand in a line. The shoots along the path and the hand on the boy's shoulder are the clearest marks.",
   "must": "the difference one thing makes to a group of people and a place.",
   "avoid": "a shrug and a blank look (bedoelen); a dictionary page; a person making a payment at a till (betalen voor); a face with a question mark.",
   "note": "voor names the people or the place that feels the difference: de tuin betekent veel voor de buurt. The object is what the thing is worth, not what it refers to, which is what bedoelen asks about.",
   "nl": "De buurttuin betekent veel voor de buurt.",
   "en": "The community garden means a lot to the neighbourhood.",
   "builds": ["De buurttuin betekent veel voor de buurt", "Het buurthuis betekent veel voor de buurt"],
   "q": "Kijkt de man naar de planten langs het pad?", "answer": "Ja",
   "alt": "Een oudere man zit op de drempel van zijn huis met een jongen naast zich die een klein potje met een plantje vasthoudt en zaadzakjes in de hand heeft; de man legt een hand op de schouder van de jongen en langs het pad staan groene scheuten."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "knoeien", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "knoeien met", "gloss": "to mess about with",
  "cards": [{
   "id": "knoeien-met-verf",
   "scene": "a child sits at a table with a pot of blue paint tipped on its side, both hands raising a brush over a sheet of paper with a wide blue smear already across it. A trail of drips runs from the pot to the sheet, and a second brush and an empty cup lie where they were dropped. The trail of blue drips from the tipped pot is the clearest mark.",
   "must": "paint spilled by careless handling.",
   "avoid": "a tidy finished picture pinned up (schilderen); a rolling pin over dough (kneden); a hand wiping a table (opruimen); paint being sold at a till (kopen).",
   "note": "met names the substance that is being handled carelessly, and the tone is unskilled or messy by choice. Compare bezig zijn met, which takes the same met and says nothing about how well it goes.",
   "nl": "Het kind knoeit met de verf.",
   "en": "The child is messing about with the paint.",
   "builds": ["Het kind knoeit met de verf", "De jongen knoeit met de verf"],
   "q": "Is de verfpot omgevallen?", "answer": "Ja",
   "alt": "Een kind zit aan tafel met een omgevallen pot blauwe verf en heft een kwast boven een blad met een brede blauwe streek; van de pot naar het blad loopt een spoor van druppels."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "strijden", "action": "cluster",
 "preps": ["voor", "tegen"],
 "noot": "voor is the aim you want; tegen is the thing you want gone.",
 "chunks": [{
  "chunk": "strijden voor", "gloss": "to fight for",
  "cards": [{
   "id": "strijden-voor-de-vrijheid",
   "scene": "a row of people stands linked arm to arm at the head of a street crowd, all facing forwards, one raising a rolled banner pole with a blank flag that catches the light. A grey line of uniformed figures with shields stands still far down the road and nobody moves. The linked arms at the front of the crowd are the clearest mark.",
   "must": "people pushing together for something they want to keep.",
   "avoid": "a crowd with raised fists facing each other (vechten met); a market stall with money (handelen met); a crowd carrying a placard with readable words; a lone person at a desk.",
   "note": "voor names the thing wanted and held up: strijden voor vrijheid. It is a long, public effort, not a single scuffle, which is what vechten om would show.",
   "nl": "Zij strijden voor hun vrijheid.",
   "en": "They fight for their freedom.",
   "builds": ["Zij strijden voor hun vrijheid", "Wij strijden voor onze vrijheid"],
   "q": "Staan de mensen gearmd in een rij?", "answer": "Ja",
   "alt": "Een rij mensen staat gearmd vooraan in een menigte, allemaal naar voren gekeerd, en een van hen houdt een opgerolde stok met een leeg doek omhoog; in de verte staat een linie agenten met schilden stil."
  }]
 }, {
  "chunk": "strijden tegen", "gloss": "to fight against",
  "cards": [{
   "id": "strijden-tegen-de-ziekte",
   "scene": "a researcher in a lab coat stands beside a bench with both gloved hands lifting a clear dish of dull grey culture towards a lamp, the shoulders square and the eyes on the dish. Behind her stands a pale patient in a chair with a blanket over the knees, and a rack of plain vials and a microscope fill the bench. The greyish dish raised to the lamp is the clearest mark.",
   "must": "sustained effort to remove something harmful.",
   "avoid": "two people brawling in a street (vechten met); a document signed at a table (protesteren tegen); a joyful runner crossing a line (winnen van); a shop sign with readable words.",
   "note": "tegen names the thing to be removed: strijden tegen een ziekte. It looks the same as strijden voor with the opposite side named, which is the point of the pair.",
   "nl": "De onderzoekers strijden tegen de ziekte.",
   "en": "The researchers fight against the disease.",
   "builds": ["De onderzoekers strijden tegen de ziekte", "Zij strijden tegen de ziekte"],
   "q": "Werkt de persoon met een schaaltje in een laboratorium?", "answer": "Ja",
   "alt": "Een onderzoekster in een witte jas houdt met handschoenen een schaaltje met grijs weefsel tegen het licht, de schouders recht en de blik op het schaaltje; achter haar zit een bleke zieke in een stoel en op de bank staan een microscoop en flesjes."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "verbinden", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "verbinden met", "gloss": "to connect to",
  "cards": [{
   "id": "verbinden-met-een-touw",
   "scene": "a man on a quayside crouches with a rope end held in both hands, the coil on his hip, looping it round a black bollard in front of him. Behind it a small boat drifts with one hand over the side reaching for the rope, and a second mooring line lies loose on the stones behind him. The rope loop going round the bollard is the clearest mark.",
   "must": "one thing joined to another and held there.",
   "avoid": "a hand wrapping a bandage round an arm (verbinden aan); a cut line lying apart on the stones (losmaken); a knot in mid-air with nothing fastened; a shop counter.",
   "note": "met names the second thing in the joint; the two are tied or wired together, which is why verbinden is used for a wound and for two cables alike. Compare aansluiten op, which is plugging into a fixed point rather than tying two moving things.",
   "nl": "De schipper verbindt de boot met een touw aan de paal.",
   "en": "The skipper ties the boat to the post with a rope.",
   "builds": ["De schipper verbindt de boot met een touw aan de paal", "Zij verbindt de boot met een touw aan de paal"],
   "q": "Houdt de man een touw vast?", "answer": "Ja",
   "alt": "Een man hurkt op de kade met het eind van een touw in beide handen en de rol op zijn heup, en legt het touw om een zwarte paal; achter de paal drijft een kleine boot waar iemand met een hand over de rand naar het touw reikt."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "verdelen", "action": "cluster",
 "preps": ["in", "onder"],
 "noot": "in is the boxes you make; onder is the people who each get one.",
 "chunks": [{
  "chunk": "verdelen in", "gloss": "to divide into",
  "cards": [{
   "id": "verdelen-in-twee-groepen",
   "scene": "a coach stands in the middle of a gym hall with both arms raised open, one pointing left and one right, while the players stand in two facing rows on the floor line. A ball rests at the coach's feet and a whistle hangs from the other hand. The blank line between the two rows of players is the clearest mark.",
   "must": "one set of people split into two sets.",
   "avoid": "one player leaving a row with a bag over the shoulder (opdelen); a hand pushing a plate towards a child (verdelen onder); a number on a shirt; a shop counter.",
   "note": "in names the whole made of parts: de klas verdelen in twee groepen. Each part exists in the room, which is what the two rows show. It says nothing about who receives each part.",
   "nl": "De trainer verdeelt de spelers in twee groepen.",
   "en": "The coach divides the players into two groups.",
   "builds": ["De trainer verdeelt de spelers in twee groepen", "Zij verdeelt de spelers in twee groepen"],
   "q": "Staan de spelers in twee rijen?", "answer": "Ja",
   "alt": "Een trainer staat midden in een gymzaal met beide armen open en wijst met de ene naar links en met de andere naar rechts, terwijl de spelers in twee rijen tegenover elkaar staan; bij zijn voeten ligt een bal."
  }]
 }, {
  "chunk": "verdelen onder", "gloss": "to share out among",
  "cards": [{
   "id": "verdelen-onder-de-kinderen",
   "scene": "a woman leans over a kitchen counter with a knife in her right hand cutting a large cake into four even pieces, one already slid onto a paper plate held by a child at her elbow. Two more children reach up towards the counter with plates in their hands. The four even pieces in the divided cake are the clearest mark.",
   "must": "one whole given out piece by piece to several people.",
   "avoid": "one cake cut in two halves and left there (verdelen in); a child taking the whole plate away (delen met); a slice being eaten from a spoon; a shop counter with a till.",
   "note": "onder names the people who each receive a part: de cake verdelen onder de kinderen. Each child gets something, which in alone does not say. Compare delen met, where the person joins you in what you have rather than being handed a piece.",
   "nl": "Zij verdeelt de taart onder de kinderen.",
   "en": "She shares out the cake among the children.",
   "builds": ["Zij verdeelt de taart onder de kinderen", "Hij verdeelt de taart onder de kinderen"],
   "q": "Krijgt elk kind een stuk taart?", "answer": "Ja",
   "alt": "Een vrouw leunt over het aanrecht met een mes in haar rechterhand en snijdt een grote taart in vier gelijke stukken, waarvan er een al op een papieren bordje ligt dat een kind bij haar elleboog omhoog houdt; twee andere kinderen reiken omhoog."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "delen", "action": "convert",
 "preps": ["in", "met"],
 "noot": "in is having a share of something; met is handing part of what you have to someone.", "chunks": [{
  "chunk": "delen met", "gloss": "to share with",
  "cards": [{
   "id": "delen-met-de-buren",
   "scene": "a woman in her own garden crouches with a pair of pruning shears in one hand and holds out a basket of green beans in the other towards a neighbour leaning over the low fence. Both look at the basket, and tomatoes and a shovel lie in the soil beside her. The basket held out over the fence is the clearest mark.",
   "must": "part of what one person has being handed to another.",
   "avoid": "two people counting coins between them (verdelen onder); a receipt being paid at a table (betalen voor); a single empty plate; a closed gate.",
   "note": "met names the person part of it goes to; you keep some of it yourself, which is what makes it sharing rather than giving away. The twin chunk on this page is delen in, where you receive a part of what others achieved and nothing changes hands. Delen met is giving part of what you have to someone.",
   "nl": "Zij deelt de groente met de buren.",
   "en": "She shares the vegetables with the neighbours.",
   "builds": ["Zij deelt de groente met de buren", "Hij deelt de groente met de buren"],
   "q": "Krijgt de buur een deel van de groente?", "answer": "Ja",
   "alt": "Een vrouw hurkt in haar tuin met een snoeischaar in een hand en houdt met de andere een mand groene bonen voor zich uit naar een buur die over het lage hek hangt; naast haar in de aarde liggen tomaten en een schep."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "vallen", "action": "single",
 "preps": None, "noot": None, "chunks": [{
  "chunk": "vallen op", "gloss": "to fall for (a person)",
  "cards": [{
   "id": "vallen-op-een-collega",
   "scene": "a woman at a shared office table turns her head over her shoulder towards the colleague who has just passed behind her with a file under his arm. Her face is warm and fixed, a pen still raised in her hand, and a mug she has set down has spilled a dark trail across her notes. A blank chart stands on the wall behind. The pen raised and forgotten over the spilled mug is the clearest mark.",
   "must": "a person distracted by someone they are drawn to.",
   "avoid": "a person stumbling over a step (struikelen); a person noticed for a bright shirt in a crowd (opvallen); two people shaking hands (kennismaken met); a hand waving goodbye.",
   "note": "op names the person who draws the feeling, and the object is a person: zij valt op hem. opvallen is the reverse: it is the thing that draws the eye to itself. Falling for someone and standing out are mirror images, so the two must not be drawn the same way.",
   "nl": "Zij valt op een collega.",
   "en": "She has fallen for a colleague.",
   "builds": ["Zij valt op een collega", "Hij valt op een collega"],
   "q": "Kijkt de vrouw naar haar collega?", "answer": "Ja",
   "alt": "Een vrouw aan een gedeelde bureautafel kijkt over haar schouder naar een collega die met een map onder de arm achterlangs loopt; in haar hand hangt een pen en naast haar notities loopt een donker spoor uit een mok."
  }]
 }]
},
{
 "page": "b1-plus.html", "band": "b1-plus", "stem": "vertrekken", "action": "cluster",
 "preps": ["naar", "om", "van", "uit"],
 "noot": "naar is the place you go; om is the clock; van is the platform or place you stand on; uit is the enclosed place you come out of.",
 "chunks": [{
  "chunk": "vertrekken naar", "gloss": "to leave for",
  "cards": [{
   "id": "vertrekken-naar-spanje",
   "scene": "a couple with two suitcases stand at a check-in desk facing a staff member who points along the hall. One case stands upright at their feet and the other lies flat on the belt-scale. A blank board hangs above the desk with no letters on it. The taller suitcase on the counter scale is the clearest mark.",
   "must": "setting off for a far destination.",
   "avoid": "a person at a platform waiting (wachten op); a taxi door being opened at the kerb (stappen in); a person waving from a doorway (blijven); a map spread on a table.",
   "note": "naar names the destination, never the place left. vertrekken is the moment of going, so a person with bags at a desk reads as the start of the journey.",
   "nl": "Zij vertrekken naar Spanje.",
   "en": "They leave for Spain.",
   "builds": ["Zij vertrekken naar Spanje", "Wij vertrekken naar Spanje"],
   "q": "Staat er een koffer op de weegschaal?", "answer": "Ja",
   "alt": "Een stel met twee koffers staat bij een incheckbalie; een medewerker wijst langs de hal en een van de koffers ligt plat op de weegschaal, terwijl boven de balie een leeg bord hangt."
  }]
 }, {
  "chunk": "vertrekken om", "gloss": "to leave at (a time)",
  "cards": [{
   "id": "vertrekken-om-zes-uur",
   "scene": "a man sits on his own doorstep in the early morning light with a packed bag between his feet and one shoe still in his hand, face turned up towards a clock above the door. The hands of that clock stand at six. A folded newspaper lies untouched on the step beside him. The clock hands standing at six are the clearest mark.",
   "must": "leaving at a stated time by the clock.",
   "avoid": "a blank departures board (vertrekken naar); a bus already pulling out (te laat zijn); a person asleep in bed; a calendar with month names.",
   "note": "om names the clock time only: wij vertrekken om zes uur. It never names a place, so om and naar never swap, and the hour is the whole point of the picture.",
   "nl": "Wij vertrekken om zes uur.",
   "en": "We leave at six o'clock.",
   "builds": ["Wij vertrekken om zes uur", "Zij vertrekken om zeven uur"],
   "q": "Staat de klok op zes uur?", "answer": "Ja",
   "alt": "Een man zit in het ochtendlicht op zijn eigen stoep met een gevulde tas tussen zijn voeten en een schoen nog in de hand, het gezicht naar een klok boven de deur waarvan de wijzers op zes staan."
  }]
 }, {
  "chunk": "vertrekken van", "gloss": "to leave from",
  "cards": [{
   "id": "vertrekken-van-het-perron",
   "scene": "a traveller with a rucksack stands on a platform edge with the toes of one boot at the yellow line, both hands on the rucksack straps and head turned one way down the track. A coloured stripe runs along the platform behind the suitcase at their feet and a bench stands empty further back. The boots stopped at the yellow line are the clearest mark.",
   "must": "the place a departure starts from.",
   "avoid": "a train already past the platform (vertrekken uit); a person seated under a roof (wachten in); a hand holding out a banknote (verkopen); a car in a garage (vandaan halen).",
   "note": "van names the place you stand on when the journey begins, which is why it fits a platform, a stop or a town, while uit needs a space you are inside.",
   "nl": "De trein vertrekt van het perron.",
   "en": "The train leaves from the platform.",
   "builds": ["De trein vertrekt van het perron", "De bus vertrekt van het perron"],
   "q": "Staat de reiziger met de tenen aan de gele lijn?", "answer": "Ja",
   "alt": "Een reiziger met een rugzak staat op de rand van het perron met de tenen van een laars aan de gele lijn, beide handen aan de banden en het hoofd opzij langs het spoor; achter hem staat een lege bank."
  }]
 }, {
  "chunk": "vertrekken uit", "gloss": "to leave out of",
  "cards": [{
   "id": "vertrekken-uit-het-hotel",
   "scene": "a woman wheels a suitcase out through a hotel lobby with the key card held up in her other hand, the glass doors behind her still swinging. A brother and sister stand at the reception desk behind her and a trolley with folded towels waits by the lift. The glass doors swinging shut behind the rolling suitcase is the clearest mark.",
   "must": "coming out of a building you were inside.",
   "avoid": "a person standing at a bus stop outside (wachten bij); a closed door with a bag beside it (aankomen); a ticket office counter (kopen); a packet being unpacked (halen uit).",
   "note": "uit needs an enclosed space: het hotel, de stad, het huis. You step out of it, which the swinging doors show. van marks somewhere you were merely standing; uit marks somewhere you were inside.",
   "nl": "Zij vertrekt uit het hotel.",
   "en": "She leaves the hotel.",
   "builds": ["Zij vertrekt uit het hotel", "Hij vertrekt uit het hotel"],
   "q": "Rolt de vrouw met een koffer naar de deur?", "answer": "Ja",
   "alt": "Een vrouw rijdt een koffer door een hotellobby met de sleutelkaart in haar andere hand, terwijl de glazen deuren achter haar nog zwaaien; bij de receptie staan twee mensen en bij de lift staat een kar met handdoeken."
  }]
 }]
},
]
